"""SynthCareer MCP server: the five official tool names over synthetic sessions.

Used to smoke-test worker harnesses (LLM or scripted) through the same tool
interface and observation schema as the official server, without touching the
real game. Run with::

    uv run python -m careerlab.synthetic.server [--months 6] [--seed-base 0] [--config '{...}']

Sessions. Like the official server, sessions are shared by every process that
points at the same game root and isolated from other roots, because the lab
checks results with a second process (``run_claude_episode`` verifies the end
state with its own client; resumes start a new process). The game root is the
directory of ``CAREER_EMULATOR_DB`` (or ``--state-dir``); sessions are kept in
``<root>/synthcareer/<session_id>.jsonl`` as a header (seed, full config) plus
one line per ``take_action`` call, and any process rebuilds a session by
replaying those calls, which is exact because the game is deterministic. The
``.sqlite3`` file at ``CAREER_EMULATOR_DB`` is never created or opened. Without
``CAREER_EMULATOR_DB`` or ``--state-dir`` sessions live in memory only.

Configuration of new games, first source wins:

1. flags ``--seed-base`` and ``--config`` (JSON ``SynthConfig`` overrides);
2. ``<root>/synthcareer/config.json`` written by ``prepare_root``. This is the
   channel that reaches a Claude worker's server: ``mcp_config`` forwards only
   ``CAREER_EMULATOR*``/``FASTMCP*`` variables, so ``CAREERLAB_SYNTH_*`` never
   arrive there, but the root does;
3. env ``CAREERLAB_SYNTH_SEED_BASE`` and ``CAREERLAB_SYNTH_CONFIG``;
4. defaults (seed base 0, 48 months).

``--months`` is applied last. The k-th game created in a root plays seed base +
k. An existing session always replays with the seed and config in its header.
The options the official runner passes (``--update``, ``--log-level``,
``--competition``, ``--transport/--host/--port/--path``) are accepted, so a
launcher from ``write_launcher`` can stand in as ``Settings.mcp_executable``.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterator

from fastmcp import FastMCP

from careerlab.synthetic.game import SynthConfig, SynthGame, handbook_text, session_id_for

try:
    import fcntl
except ImportError:  # Windows: no advisory locks; concurrent writers to one session are then unsupported
    fcntl = None  # type: ignore[assignment]

SERVER_NAME = "synthcareer"
STATE_DIRNAME = "synthcareer"
ROOT_CONFIG = "config.json"
NOTE_LIMIT = 1000
SESSION_RE = re.compile(r"[0-9a-f]{32}")
REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class _Live:
    """A session rebuilt in this process and how many bytes of its file it has applied."""

    game: SynthGame
    offset: int = 0


class SessionStore:
    """Sessions of one server process, persisted under ``state_dir`` when one is given."""

    def __init__(self, seed_base: int = 0, config: SynthConfig | None = None, competition: bool = False,
                 state_dir: Path | None = None):
        self.seed_base = seed_base
        self.config = config or SynthConfig()
        self.competition = competition
        self.state_dir = Path(state_dir) if state_dir is not None else None
        self.sessions: dict[str, _Live] = {}
        self.created = 0  # games created by this process (competition mode allows one)
        if self.state_dir is not None:
            self.state_dir.mkdir(parents=True, exist_ok=True)

    def new_game(self) -> dict[str, Any]:
        if self.competition and self.created >= 1:
            return {"error": "Competition mode: only one new game session allowed."}
        self.created += 1
        k = len(list(self.state_dir.glob("*.jsonl"))) if self.state_dir else self.created - 1
        while True:
            seed = self.seed_base + k
            sid = session_id_for(seed, salt=f"{self.seed_base}:{k + 1}")
            if self.state_dir is None:
                break
            header = json.dumps({"session_id": sid, "seed": seed, "config": self.config.to_dict()}) + "\n"
            try:  # exclusive create: two processes racing for the same k cannot share a file
                with self._path(sid).open("x", encoding="utf-8") as fh:
                    fh.write(header)
                break
            except FileExistsError:
                k += 1
        self.sessions[sid] = _Live(SynthGame(seed, self.config, session_id=sid), len(header.encode()) if self.state_dir else 0)
        return {"session_id": sid, "message": "New SynthCareer session started. Call observe to see the first event."}

    def get(self, session_id: str) -> SynthGame | None:
        """The session's current game, first applying actions other processes appended."""
        sid = str(session_id)
        if self.state_dir is None:
            live = self.sessions.get(sid)
            return live.game if live else None
        if not SESSION_RE.fullmatch(sid):  # never build a path from an arbitrary string
            return None
        try:
            with self._path(sid).open("rb") as fh:
                live = self.sessions.get(sid)
                fh.seek(live.offset if live else 0)
                data = fh.read()
        except FileNotFoundError:
            return None
        end = data.rfind(b"\n") + 1  # a line still being written is applied on a later call
        lines = data[:end].splitlines()
        if live is None:
            if not lines:
                return None
            header = json.loads(lines.pop(0))
            live = _Live(SynthGame(int(header["seed"]), SynthConfig.from_dict(header["config"]), session_id=sid))
            self.sessions[sid] = live
        for line in lines:
            call = json.loads(line)
            live.game.take_action(call["choice"], call["notes"])
        live.offset += end
        return live.game

    def take_action(self, session_id: str, choice: int, notes: str = "") -> dict[str, Any] | None:
        """Apply one call; persisted calls are written before they are applied (write-ahead)."""
        if self.state_dir is None or not SESSION_RE.fullmatch(str(session_id)):
            game = self.get(session_id)
            return game.take_action(choice, notes) if game else None
        with self._locked(str(session_id)) as fh:
            game = self.get(session_id)
            if game is None or fh is None:
                return None
            line = (json.dumps({"choice": choice, "notes": str(notes)[:NOTE_LIMIT]}) + "\n").encode()
            fh.write(line)
            fh.flush()
            self.sessions[str(session_id)].offset += len(line)
            return game.take_action(choice, notes)

    def _path(self, sid: str) -> Path:
        assert self.state_dir is not None
        return self.state_dir / f"{sid}.jsonl"

    @contextlib.contextmanager
    def _locked(self, sid: str) -> Iterator[Any]:
        """Serialise writers of one session across processes (advisory lock on its file)."""
        try:  # no O_CREAT: an unknown session id must not leave a file behind
            fh = os.fdopen(os.open(self._path(sid), os.O_WRONLY | os.O_APPEND), "ab")
        except FileNotFoundError:
            yield None
            return
        with fh:
            if fcntl is not None:
                fcntl.flock(fh, fcntl.LOCK_EX)
            yield fh


def build_server(seed_base: int = 0, config: SynthConfig | None = None, competition: bool = False,
                 state_dir: Path | None = None) -> FastMCP:
    """FastMCP app exposing exactly new_game, observe, take_action, check_latest_logs, show_employee_handbook."""
    store = SessionStore(seed_base, config, competition, state_dir)
    cfg = store.config
    mcp = FastMCP(SERVER_NAME, instructions="SynthCareer: a synthetic career simulation for testing agents. "
                                            "Start with new_game, then observe and take_action until the run ends.")

    @mcp.tool
    def new_game() -> dict[str, Any]:
        """Start a new simulation and return its session_id."""
        return store.new_game()

    @mcp.tool
    def observe(session_id: str) -> dict[str, Any]:
        """Return the current state, event and choices of a session."""
        game = store.get(session_id)
        if game is None:
            return {"current_state": {"error": f"Unknown session_id: {session_id}"}}
        return game.observe()

    @mcp.tool
    def take_action(session_id: str, choice: int, notes: str = "") -> dict[str, Any]:
        """Apply the selected choice and record an agent note."""
        reply = store.take_action(session_id, choice, notes)
        if reply is None:
            return {"success": False, "error": f"Unknown session_id: {session_id}"}
        return reply

    @mcp.tool
    def check_latest_logs(session_id: str, count: int = 10) -> dict[str, Any]:
        """Return recent log entries for the session."""
        game = store.get(session_id)
        if game is None:
            return {"error": f"Unknown session_id: {session_id}", "entries": []}
        return game.logs(count)

    @mcp.tool
    def show_employee_handbook() -> str:
        """Return the public employee handbook."""
        return handbook_text(cfg)

    mcp.synth_store = store  # type: ignore[attr-defined]  # for in-process inspection in tests
    return mcp


def prepare_root(root: Path, seed_base: int = 0, config: dict[str, Any] | SynthConfig | None = None) -> Path:
    """Bind a game root to a seed base and config before handing it to a harness.

    Pass the same ``root`` as ``game_root`` to ``run_claude_episode`` (or as a
    ``ServerSpec`` root): every server process started on it then creates its
    games from these values, whatever environment it inherits.
    """
    overrides = config.to_dict() if isinstance(config, SynthConfig) else dict(config or {})
    SynthConfig.from_dict(overrides)  # fail here, not inside a worker's server
    path = Path(root) / STATE_DIRNAME / ROOT_CONFIG
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"seed_base": int(seed_base), "config": overrides}, indent=1), encoding="utf-8")
    return path


def write_launcher(path: Path, *flags: str) -> Path:
    """Write an executable that starts this server, for ``Settings.mcp_executable``.

    ``mcp_config`` and ``ServerSpec`` call the executable with the official
    runner's flags only, so fixed extras (``--months 6``) are baked in here.
    """
    path = Path(path)
    pythonpath = shlex.quote(str(REPO_ROOT))
    args = " ".join(shlex.quote(f) for f in flags)
    path.write_text("#!/bin/sh\n"
                    f'PYTHONPATH={pythonpath}${{PYTHONPATH:+:$PYTHONPATH}}; export PYTHONPATH\n'
                    f'exec {shlex.quote(sys.executable)} -m careerlab.synthetic.server {args} "$@"\n', encoding="utf-8")
    path.chmod(0o755)
    return path


def config_from_env(months: int | None = None, override: str | None = None,
                    root_config: dict[str, Any] | None = None) -> SynthConfig:
    """SynthConfig from the first source that is set: flag JSON, root config, ``CAREERLAB_SYNTH_CONFIG``."""
    if override is not None:
        data = json.loads(override) if override.strip() else {}
    elif root_config is not None and "config" in root_config:
        data = dict(root_config["config"] or {})
    else:
        raw = os.environ.get("CAREERLAB_SYNTH_CONFIG", "")
        data = json.loads(raw) if raw.strip() else {}
    cfg = SynthConfig.from_dict(data)
    if months is not None:
        if not 1 <= months <= 48:
            raise ValueError("--months must be between 1 and 48")
        cfg = replace(cfg, months=months)
    return cfg


def resolve_state_dir(flag: str | None = None) -> Path | None:
    """Where sessions persist: ``--state-dir``, else beside ``CAREER_EMULATOR_DB``, else nowhere (memory)."""
    if flag:
        return Path(flag).expanduser().resolve()
    db = os.environ.get("CAREER_EMULATOR_DB", "").strip()
    return Path(db).expanduser().resolve().parent / STATE_DIRNAME if db else None


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SynthCareer MCP server (synthetic test game).")
    parser.add_argument("--months", type=int, default=None, help="shorten games (smoke tests)")
    parser.add_argument("--seed-base", type=int, default=None)
    parser.add_argument("--config", default=None, help="JSON SynthConfig overrides")
    parser.add_argument("--state-dir", default=None, help="session directory (default: <dir of CAREER_EMULATOR_DB>/synthcareer)")
    parser.add_argument("-c", "--competition", action="store_true", help="only one new game per server")
    parser.add_argument("--transport", default="stdio", choices=("stdio", "http", "streamable-http", "sse"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--path", default="/mcp")
    parser.add_argument("--update", default=None, help="accepted for compatibility; ignored")
    parser.add_argument("--log-level", default=None, help="accepted for compatibility; ignored")
    args = parser.parse_args(argv)
    state_dir = resolve_state_dir(args.state_dir)
    root_file = state_dir / ROOT_CONFIG if state_dir else None
    root_config = json.loads(root_file.read_text(encoding="utf-8")) if root_file and root_file.exists() else None
    if args.seed_base is not None:
        seed_base = args.seed_base
    elif root_config is not None and "seed_base" in root_config:
        seed_base = int(root_config["seed_base"])
    else:
        seed_base = int(os.environ.get("CAREERLAB_SYNTH_SEED_BASE", "0") or 0)
    cfg = config_from_env(args.months, args.config, root_config)
    print(f"SynthCareer server: seed_base={seed_base} months={cfg.months} sessions={state_dir or 'in-memory'} "
          f"root_config={'yes' if root_config is not None else 'no'}", file=sys.stderr, flush=True)
    mcp = build_server(seed_base, cfg, args.competition, state_dir)
    if args.transport == "stdio":
        mcp.run(show_banner=False)
    else:
        transport = "streamable-http" if args.transport == "http" else args.transport
        mcp.run(transport=transport, show_banner=False, host=args.host, port=args.port, path=args.path)


if __name__ == "__main__":
    main()
