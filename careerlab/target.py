"""Real games of the target model (DeepSeek ``deepseek-v4-flash`` in the official runner) under an exact-cost guard.

The competition key is an OpenRouter key with a USD credit limit. ``key_status`` reads its usage from
``GET {API_BASE}/key``, which is free and calls no model. ``play_target`` plays a short series:

- before every game it refuses to start unless ``limit_remaining - reserve_usd >= max_usd_per_game``;
- every game is a registry job (actor ``jiuwenswarm-target``, route ``competition-key``) played by
  ``careerlab.actors.official_runner.run_target_episode`` and ingested like any other episode;
- its exact cost is the key's usage after the game minus before it, read until the figure settles;
- a watchdog polls the key during the game and stops the game once it has spent more than ``max_usd_per_game``;
- the series stops after a game that cost more than ``max_usd_per_game`` or was interrupted.

``dry_run=True`` does everything except starting JiuwenSwarm or ``play``: it prepares the slot, reloads the dev
dataset, builds the solution, runs the runner's own checks and reads the key status. It spends nothing.

Credentials stay in the git-ignored env file (``CAREERLAB_TARGET_ENV``, default ``<runner>/.env``). The key is
read only to build an HTTP header; it is never printed, logged or returned, and run directories are scrubbed for
it after every game.

Target games belong to origin ``deepseek``: their own data directory, job ids and registry, so they never collide
with the cloud race. From a worktree, point ``CAREERLAB_RUNNER_DIR`` at the runner checkout (``local-runs`` is not
in Git)::

    export CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=<huawei>/local-runs/official-runner
    uv run python -m careerlab.target key
    uv run python -m careerlab.target register lab/policies-src/matteo-feedback-growth/observed-growth-v3
    uv run python -m careerlab.target play --policy observed-growth-v3 --dry-run
    uv run python -m careerlab.target play --policy observed-growth-v3 --spend   # one real game: costs money
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import hashlib
import json
import math
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterator

from careerlab.actors import official_runner as runner
from careerlab.actors.official_runner import DATASET_RELOAD, INSTANCE, PLAY_GRACE_S, RUNNER_COMMIT, TargetConfig
from careerlab.config import OFFICIAL_ENGINE_ENV, Settings
from careerlab.episode import EpisodeResult, atomic_write_json
from careerlab.store import Registry, bundle_hash

TARGET_ORIGIN = "deepseek"
ACTOR_KIND = "jiuwenswarm-target"
ROUTE = "competition-key"
DEFAULT_WHY = "target pilot: cost, tokens and fidelity of one real deepseek-v4-flash game (research/careerlab/target-budget.md)"
PLAY_REQUIRED = ("README.md", "design/skills_design.md", "design/decision_report.md")
PLACEHOLDER = """# NOT FOR SUBMISSION

Placeholder written by `careerlab.target` only because the official runner's local `play` refuses a folder
without this file. The agent never reads it: `play` installs `skills/` and the manifest instruction only.
The team's real README and design documents are separate and are packaged with `careerlab package`.
"""


class KeyStatusError(RuntimeError):
    """The key's usage could not be read. Messages never contain the key."""


# -- credentials and key usage ------------------------------------------------------------------------------

def target_env_path(settings: Settings) -> Path:
    """The git-ignored credentials file: ``$CAREERLAB_TARGET_ENV``, else the runner checkout's ``.env``."""
    value = os.environ.get("CAREERLAB_TARGET_ENV", "").strip()
    return Path(value).expanduser().resolve() if value else settings.runner_dir / ".env"


def read_env_file(path: Path) -> dict[str, str]:
    """``KEY=value`` lines of a dotenv file (quotes, ``export`` and comments handled). Values can be secret."""
    values: dict[str, str] = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values


def _scrub(text: str, secret: str) -> str:
    return text.replace(secret, "<redacted>") if secret else text


def key_status(env_path: Path, timeout_s: float = 20.0) -> dict[str, Any]:
    """Usage, credit limit and remaining credit (USD) of the competition key; no secret in the result.

    ``GET {API_BASE}/key`` is OpenRouter's free key-information endpoint: it calls no model.
    """
    values = read_env_file(Path(env_path))
    base, key = values.get("API_BASE", "").rstrip("/"), values.get("API_KEY", "")
    if not base or not key:
        raise KeyStatusError(f"{env_path} lacks API_BASE or API_KEY")
    if urllib.parse.urlsplit(base).scheme != "https":
        raise KeyStatusError("API_BASE must be an https URL")
    request = urllib.request.Request(f"{base}/key", headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise KeyStatusError(f"GET {base}/key failed: HTTP {exc.code}") from None
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise KeyStatusError(_scrub(f"GET {base}/key failed: {exc!r}", key)) from None
    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict) or not isinstance(data.get("usage"), (int, float)):
        raise KeyStatusError("unexpected /key response: no data.usage")
    usage = float(data["usage"])
    limit = float(data["limit"]) if isinstance(data.get("limit"), (int, float)) else None
    remaining = data.get("limit_remaining")
    remaining = float(remaining) if isinstance(remaining, (int, float)) else (None if limit is None else limit - usage)
    return {"usage": usage, "limit": limit, "limit_remaining": remaining, "api_base": base,
            "model_name": values.get("MODEL_NAME", "")}


def _settled_status(env_path: Path, wait_s: float, max_wait_s: float) -> tuple[dict[str, Any], bool]:
    """Key status once two readings ``wait_s`` apart agree: OpenRouter books a generation shortly after it ends."""
    last = key_status(env_path)
    for _ in range(max(1, math.ceil(max_wait_s / wait_s)) if wait_s > 0 else 0):
        time.sleep(wait_s)
        current = key_status(env_path)
        if abs(current["usage"] - last["usage"]) < 1e-9:
            return current, True
        last = current
    return last, False


def _redact(directory: Path, secret: str) -> int:
    """Replace the key in every file of a run directory; returns how many files held it (expected 0)."""
    if len(secret) < 8 or not directory.exists():
        return 0
    needle, hits = secret.encode(), 0
    for path in directory.rglob("*"):
        if path.is_file():
            data = path.read_bytes()
            if needle in data:
                path.write_bytes(data.replace(needle, b"<redacted>"))
                hits += 1
    return hits


@contextlib.contextmanager
def _credentials(env_path: Path) -> Iterator[None]:
    """``prepare_slot`` copies the file named by CAREERLAB_TARGET_ENV into the slot; point it at ``env_path``."""
    old = os.environ.get("CAREERLAB_TARGET_ENV")
    os.environ["CAREERLAB_TARGET_ENV"] = str(env_path)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("CAREERLAB_TARGET_ENV", None)
        else:
            os.environ["CAREERLAB_TARGET_ENV"] = old


@contextlib.contextmanager
def _signals_as_interrupt() -> Iterator[None]:
    """JiuwenSwarm and ``play`` run in their own session, out of reach of the terminal's signals. Closing the
    terminal (SIGHUP) or a plain ``kill`` (SIGTERM) therefore becomes Ctrl-C here, so the game is still stopped.
    A signal that is already ignored (``nohup``) or handled stays as it is."""
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    old = {sig: signal.signal(sig, signal.default_int_handler)
           for sig in (getattr(signal, "SIGHUP", None), signal.SIGTERM)
           if sig is not None and signal.getsignal(sig) == signal.SIG_DFL}
    try:
        yield
    finally:
        for sig, handler in old.items():
            signal.signal(sig, handler)


@contextlib.contextmanager
def _slot_lock(path: Path) -> Iterator[None]:
    """One target series per slot at a time (two would share one JiuwenSwarm instance and one database)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fcntl
    except ImportError:  # Windows: no advisory lock
        yield
        return
    with path.open("w") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise RuntimeError(f"target slot is in use by another process ({path})") from None
        yield


# -- policies and solutions ----------------------------------------------------------------------------------

def register_policy_folder(settings: Settings, reg: Registry, folder: Path, by: str = "target",
                           allow_lint_errors: bool = False) -> str:
    """Register a policy folder as ``careerlab register`` does, registering missing ancestors first.

    Another origin's registry often lacks the parents of the policy to play. They are looked up by name (or id)
    among ``lab/policies-src/**/policy.json``. Ids are content hashes, so each policy gets the same id as in the
    race registry and a later merge of this origin's results stays conflict-free.
    """
    return _register(settings, reg, Path(folder).resolve(), by, allow_lint_errors, None, ())


def _register(settings: Settings, reg: Registry, src: Path, by: str, allow_lint_errors: bool,
              index: dict[str, Path] | None, stack: tuple[str, ...]) -> str:
    from careerlab.compliance import lint_bundle

    meta = json.loads((src / "policy.json").read_text(encoding="utf-8"))
    if meta["name"] in stack:
        raise ValueError(f"policy ancestry loops through {meta['name']!r}")
    if not (src / "bundle" / "scripted.json").exists():
        errors = [f for f in lint_bundle(src / "bundle") if f.severity == "error"]
        if errors and not allow_lint_errors:
            raise ValueError(f"{meta['name']}: compliance errors:\n" + "\n".join(map(str, errors)))
    lookup = "SELECT policy_id FROM policies WHERE policy_id=? OR name=?"
    parents = []
    for parent in meta.get("parents", []):
        row = reg.db.execute(lookup, (parent, parent)).fetchone()
        if row is None:
            index = _policy_sources(settings) if index is None else index
            folder = index.get(parent) or next((f for f in index.values() if bundle_hash(f / "bundle")[:16] == parent), None)
            if folder is None:
                raise ValueError(f"unknown parent {parent!r} of {meta['name']!r}: not registered and not under lab/policies-src")
            _register(settings, reg, folder, by, allow_lint_errors, index, stack + (meta["name"],))
            row = reg.db.execute(lookup, (parent, parent)).fetchone()
        parents.append(row[0])
    return reg.register_policy(src / "bundle", meta["family"], meta["name"], parents, meta["hypothesis"],
                               meta.get("change", ""), created_by=by, meta=meta)


def _policy_sources(settings: Settings) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted((settings.lab_dir / "policies-src").rglob("policy.json")):
        try:
            index.setdefault(json.loads(path.read_text(encoding="utf-8"))["name"], path.parent)
        except (ValueError, KeyError):
            continue
    return index


def _bundle_dir(settings: Settings, stored: str) -> Path:
    """The registered bundle; if it was registered from another checkout, the same path under this lab dir."""
    path = Path(stored)
    if path.is_dir():
        return path
    marker, text = "/lab/policies-src/", "/" + stored.replace("\\", "/")
    if marker in text:
        moved = settings.lab_dir / "policies-src" / text.rsplit(marker, 1)[1]
        if moved.is_dir():
            return moved
    raise FileNotFoundError(f"policy bundle {stored} not found")


def _digest(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for rel in files:
        digest.update(str(rel).encode() + b"\0" + (root / rel).read_bytes() + b"\0")
    return digest.hexdigest()


def solution_sha256(solution: Path) -> str:
    """SHA-256 over relative paths and bytes of every file in a solution folder."""
    return _digest(solution, sorted(p.relative_to(solution) for p in solution.rglob("*") if p.is_file()))


def build_solution(settings: Settings, reg: Registry, policy_id: str, out_dir: Path) -> Path:
    """Play-ready folder ``out_dir/solution``: the registered Skills and manifest byte for byte, plus placeholders.

    The runner's ``play`` checks the folder like ``validate`` but without the video, so it also needs
    ``README.md``, ``design/skills_design.md`` and ``design/decision_report.md``. Those are written as short
    placeholders marked NOT FOR SUBMISSION; nothing else is added.
    """
    row = reg.db.execute("SELECT * FROM policies WHERE policy_id=?", (policy_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown policy {policy_id}")
    bundle = _bundle_dir(settings, row["bundle_path"])
    if bundle_hash(bundle)[:16] != policy_id:
        raise ValueError(f"bundle bytes of {row['name']} changed since registration; register a new version instead")
    files = sorted(p.relative_to(bundle) for p in bundle.rglob("*") if p.is_file() and p.name != ".DS_Store"
                   and (p.relative_to(bundle).parts[0] == "skills" or p.relative_to(bundle) == Path("manifest.json")))
    if Path("manifest.json") not in files or not list((bundle / "skills").glob("*/SKILL.md")):
        raise ValueError(f"{row['name']} is not a Skills bundle (manifest.json and skills/*/SKILL.md)")
    solution = Path(out_dir) / "solution"
    if solution.exists():
        shutil.rmtree(solution)
    for rel in files:
        (solution / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(bundle / rel, solution / rel)
    if _digest(solution, files) != _digest(bundle, files):
        raise RuntimeError("solution copy differs from the registered bundle")
    for name in PLAY_REQUIRED:
        (solution / name).parent.mkdir(parents=True, exist_ok=True)
        (solution / name).write_text(PLACEHOLDER, encoding="utf-8")
    return solution


# -- slot checks and identities ------------------------------------------------------------------------------

_SLOT_CHECK = r"""
import asyncio, json, sys
from pathlib import Path
from career_sim_runner.setup import resolve_instance_ws_url
from career_sim_runner.validate import validate_environment, validate_submission
submission = validate_submission(Path(sys.argv[1]), require_presentation=False)
environment = asyncio.run(validate_environment(ws_url=resolve_instance_ws_url()))
print(json.dumps({"submission": submission.to_dict(), "environment": environment.to_dict()}))
"""


def check_slot(slot_root: Path, solution: Path) -> dict[str, Any]:
    """The runner's own checks inside the slot: the submission check ``play`` makes before installing (no video)
    and its environment check. Files and a local port probe only, no model call. ``failures`` lists every failed
    check except ``backend-reachable``, which only passes while JiuwenSwarm runs."""
    repo, home = slot_root / "runner", slot_root / "home"
    out = subprocess.run(["uv", "run", "python", "-c", _SLOT_CHECK, str(solution)], cwd=repo, env=runner._env(home),
                         stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
    lines = [line for line in out.stdout.splitlines() if line.startswith("{")]
    if out.returncode != 0 or not lines:
        raise RuntimeError(f"runner checks did not run (exit {out.returncode}): {(out.stderr or out.stdout)[-800:]}")
    report = json.loads(lines[-1])
    report["failures"] = [f"{c['name']}: {c['detail']}" for part in ("submission", "environment")
                          for c in report[part]["checks"] if not c["ok"] and c["name"] != "backend-reachable"]
    return report


def _slot_versions(repo: Path) -> dict[str, str]:
    from importlib.metadata import distributions

    wanted = {"career-emulator-engine": "engine", "career-emulator-techarena": "dataset", "jiuwenswarm": "jiuwenswarm",
              "fastmcp": "fastmcp"}
    found: dict[str, str] = {}
    for site in [*sorted(repo.glob(".venv/lib/python*/site-packages")), repo / ".venv" / "Lib" / "site-packages"]:
        if site.is_dir():
            for dist in distributions(path=[str(site)]):
                name = (dist.metadata["Name"] or "").lower().replace("_", "-")
                if name in wanted:
                    found[wanted[name]] = dist.version
    missing = sorted(set(wanted.values()) - set(found))
    if missing:
        raise RuntimeError(f"slot environment at {repo / '.venv'} lacks {missing}")
    return found


def target_environment(slot_root: Path) -> dict[str, Any]:
    """Environment fingerprint of a target slot: runner commit, installed versions, engine settings, language."""
    config = slot_root / "home" / ".jiuwenswarm-instances" / INSTANCE / "config" / "config.yaml"
    match = re.search(r"^preferred_language:\s*([A-Za-z_-]+)", config.read_text(encoding="utf-8"), re.M) if config.is_file() else None
    return {"environment": "real-dev", "split": "dev", "transport": "stdio", "engine_env": dict(OFFICIAL_ENGINE_ENV),
            "runner": f"official-runner@{RUNNER_COMMIT}", "dataset_reload": " ".join(DATASET_RELOAD),
            **_slot_versions(slot_root / "runner"), "jiuwenswarm_language": match.group(1) if match else "unknown"}


def _check_gate(settings: Settings, reg: Registry) -> None:
    from careerlab.scheduler import GateClosed, check_gate, load_gate

    check_gate(settings, reg, ACTOR_KIND, "real-dev", 1)
    routes = load_gate(settings)["environments"]["real-dev"]["actors"][ACTOR_KIND].get("routes", {})
    if ROUTE not in routes:
        raise GateClosed(f"lab/gate.json has no {ROUTE!r} route for {ACTOR_KIND}")


def _prepare(settings: Settings, reg: Registry, policy_id: str, slot: int, cfg: TargetConfig) -> dict[str, Any]:
    """Everything a game needs before JiuwenSwarm starts; free (no model call)."""
    work = settings.data_dir / "target-solutions" / policy_id
    work.mkdir(parents=True, exist_ok=True)
    root = runner.prepare_slot(settings, slot)
    if runner.reload_dev_dataset(root / "runner", root / "home", work / "dataset.log") != 0:
        raise RuntimeError(f"dev dataset reload failed; see {work / 'dataset.log'}")
    solution = build_solution(settings, reg, policy_id, work)
    checks = check_slot(root, solution)
    environment = target_environment(root)
    return {"slot": root, "solution": solution, "solution_sha256": solution_sha256(solution), "checks": checks,
            "actor_id": reg.register_actor(ACTOR_KIND, cfg.record()), "env_id": reg.register_environment(environment),
            "environment": environment}


# -- games ---------------------------------------------------------------------------------------------------

def _claim_job(reg: Registry, policy_id: str, actor_id: str, env_id: str, purpose: str, why: str, owner: str,
               lease_s: float) -> str:
    """Enqueue (or reuse the queued) target job of this cell and lease it; one target game at a time."""
    rows = reg.db.execute(
        "SELECT j.job_id, j.status, j.policy_id, j.actor_id, j.env_id, j.purpose FROM jobs j JOIN actors a USING(actor_id) "
        "WHERE a.kind=? AND j.origin=? AND j.status IN ('queued','leased','running')", (ACTOR_KIND, reg.origin)).fetchall()
    busy = [r["job_id"] for r in rows if r["status"] != "queued"]
    if busy:
        raise RuntimeError(f"target job(s) {busy} still leased or running; if no game is playing, run "
                           f"`CAREERLAB_ORIGIN={reg.origin} uv run careerlab recover` first")
    other = [r["job_id"] for r in rows if (r["policy_id"], r["actor_id"], r["env_id"], r["purpose"]) != (policy_id, actor_id, env_id, purpose)]
    if other:
        raise RuntimeError(f"other target job(s) {other} are queued; resolve them before playing this one")
    if not rows:
        jobs = reg.enqueue(policy_id, actor_id, env_id, purpose, 1)
        reg.decide("enqueue", policy_id, {"actor_kind": ACTOR_KIND, "route": ROUTE, "n": 1, "purpose": purpose, "jobs": jobs}, why)
    leased = reg.lease(owner, 1, lease_s=lease_s, actor_kind=ACTOR_KIND, purpose=purpose)
    if not leased:
        raise RuntimeError("could not lease the target job")
    return leased[0]["job_id"]


async def _episode_with_watchdog(settings: Settings, cfg: TargetConfig, solution: Path, job_id: str, run_dir: Path,
                                 slot: int, env_path: Path, usage_before: float, cap: float, poll_s: float) -> float | None:
    """Play one episode; stop it once the key has spent more than ``cap`` since it started. Returns that spend."""
    episode = asyncio.create_task(runner.run_target_episode(settings, cfg, solution, job_id, run_dir, slot))
    try:
        while True:
            done, _ = await asyncio.wait({episode}, timeout=poll_s)
            if done:
                episode.result()
                return None
            try:
                spent = (await asyncio.to_thread(key_status, env_path))["usage"] - usage_before
            except KeyStatusError:
                continue  # one failed reading; the next poll retries
            if spent > cap and not episode.done():
                episode.cancel()  # run_target_episode stops play and JiuwenSwarm before the cancellation ends
                with contextlib.suppress(asyncio.CancelledError):
                    await episode
                run_dir.mkdir(parents=True, exist_ok=True)
                atomic_write_json(run_dir / "result.json", asdict(EpisodeResult(
                    job_id, None, "interrupted",
                    interruption=f"budget watchdog: the key spent USD {spent:.4f} during the game, above the USD {cap:.2f} cap")))
                return spent
    finally:
        if not episode.done():
            episode.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await episode


def _play_one(settings: Settings, reg: Registry, policy_id: str, prep: dict[str, Any], cfg: TargetConfig, env_path: Path,
              game: int, max_usd: float, reserve_usd: float, purpose: str, why: str, slot: int, poll_s: float,
              settle_s: float, settle_max_s: float, stop_on_interruption: bool) -> dict[str, Any]:
    owner = f"{socket.gethostname()}:{os.getpid()}:target"
    before = key_status(env_path)  # read first: a failed reading must not leave a claimed job behind
    job_id = _claim_job(reg, policy_id, prep["actor_id"], prep["env_id"], purpose, why, owner,
                        lease_s=cfg.timeout_s + 2 * PLAY_GRACE_S)
    run_dir = settings.runs_dir / job_id
    if not reg.mark_running(job_id, os.getpid(), str(run_dir), owner=owner):
        raise RuntimeError(f"could not claim {job_id}")
    aborted: BaseException | None = None
    tripped = None
    try:
        tripped = asyncio.run(_episode_with_watchdog(settings, cfg, prep["solution"], job_id, run_dir, slot, env_path,
                                                     before["usage"], max_usd, poll_s))
    except BaseException as exc:  # Ctrl-C or a crash: the episode has already stopped its processes
        aborted = exc
    if not (run_dir / "result.json").exists():
        run_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(run_dir / "result.json", asdict(EpisodeResult(job_id, None, "interrupted",
                                                                        interruption=f"play_target aborted: {aborted!r}")))
    try:
        after, settled = _settled_status(env_path, settle_s, settle_max_s if aborted is None else settle_s)
    except KeyStatusError:
        after, settled = None, False
    cost = None if after is None else round(after["usage"] - before["usage"], 6)
    redactions = _redact(run_dir, read_env_file(env_path).get("API_KEY", ""))
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    result.setdefault("actor_usage", {}).update({"key_cost_usd": cost, "key_cost_settled": settled})
    atomic_write_json(run_dir / "result.json", result)
    outcome = reg.ingest(job_id, run_dir)
    if aborted is not None:
        stopped = f"aborted: {aborted!r}"
    elif cost is None:
        stopped = "key usage unreadable after the game"
    elif cost > max_usd:
        stopped = f"game cost USD {cost:.4f}, above the USD {max_usd:.2f} cap"
    elif outcome == "interrupted" and stop_on_interruption:
        stopped = f"game interrupted: {result.get('interruption')}"
    else:
        stopped = None
    usage = result.get("actor_usage") or {}
    entry = {
        "game": game, "started": True, "job_id": job_id, "policy_id": policy_id, "model_name": before["model_name"],
        "outcome": outcome,
        "score": result.get("quantitative_score") if outcome != "interrupted" else None,
        "survival_months": result.get("survival_months"), "interruption": result.get("interruption"),
        "cost_usd": cost, "cost_settled": settled, "usage_before": before["usage"],
        "usage_after": None if after is None else after["usage"],
        "limit_remaining_after": None if after is None else after["limit_remaining"],
        "tokens": usage.get("tokens"), "total_tokens": usage.get("total_tokens"), "runner_cost": usage.get("runner_cost"),
        "termination_reason": usage.get("termination_reason"), "wall_seconds": result.get("wall_seconds"),
        "watchdog_spend_usd": tripped, "max_usd_per_game": max_usd, "reserve_usd": reserve_usd,
        "actor_id": prep["actor_id"], "env_id": prep["env_id"], "solution_sha256": prep["solution_sha256"],
        "run_dir": str(run_dir), "trajectory": result.get("trajectory_path"), "redacted_files": redactions,
        "stopped": stopped,
    }
    reg.decide("target_game", policy_id, entry, why)
    if aborted is not None:
        raise aborted
    return entry


def play_target(settings: Settings, reg: Registry, policy_id: str, games: int = 1, max_usd_per_game: float = 3.0,
                reserve_usd: float = 15.0, dry_run: bool = False, *, slot: int = 0, purpose: str = "pilot",
                why: str = DEFAULT_WHY, env_path: Path | None = None, poll_s: float = 60.0, settle_s: float = 15.0,
                settle_max_s: float = 240.0, stop_on_interruption: bool = True) -> list[dict[str, Any]]:
    """Play up to ``games`` real target games under the budget guard; one dict per game (see module docstring)."""
    if reg.origin != TARGET_ORIGIN or settings.origin != TARGET_ORIGIN:
        raise ValueError(f"target games are recorded under origin {TARGET_ORIGIN!r}: set CAREERLAB_ORIGIN={TARGET_ORIGIN}")
    if games < 1 or not max_usd_per_game > 0 or reserve_usd < 0:
        raise ValueError("need games >= 1, max_usd_per_game > 0 and reserve_usd >= 0")
    policy = reg.db.execute("SELECT name FROM policies WHERE policy_id=?", (policy_id,)).fetchone()
    if policy is None:
        raise ValueError(f"unknown policy {policy_id} in the {reg.origin} registry; register it first")
    if not (settings.runner_dir / "career_sim_runner").is_dir():
        raise FileNotFoundError(f"official runner not found at {settings.runner_dir}; set CAREERLAB_RUNNER_DIR")
    env_path = Path(env_path).expanduser().resolve() if env_path else target_env_path(settings)
    cfg = TargetConfig(route=ROUTE)
    model = read_env_file(env_path).get("MODEL_NAME", "")
    if model.rsplit("/", 1)[-1] != cfg.model_name:  # the organiser email may give the provider-qualified form
        raise ValueError(f"MODEL_NAME in {env_path} is {model!r}, not the designated {cfg.model_name!r}")
    _check_gate(settings, reg)
    out: list[dict[str, Any]] = []
    with _slot_lock(runner.slot_dir(settings, slot).with_suffix(".lock")), _credentials(env_path), _signals_as_interrupt():
        for game in range(1, games + 1):
            status = key_status(env_path)
            headroom = None if status["limit_remaining"] is None else status["limit_remaining"] - reserve_usd
            budget = {"usage": status["usage"], "limit": status["limit"], "limit_remaining": status["limit_remaining"],
                      "reserve_usd": reserve_usd, "max_usd_per_game": max_usd_per_game, "headroom_usd": headroom,
                      "games_affordable": max(0, math.floor(headroom / max_usd_per_game)) if headroom is not None else 0}
            budget_ok = headroom is not None and headroom >= max_usd_per_game
            if not budget_ok and not dry_run:
                entry = {"game": game, "started": False, "policy_id": policy_id, "budget": budget,
                         "reason": "limit_remaining - reserve_usd < max_usd_per_game (or the key has no limit)"}
                reg.decide("target_refused", policy_id, entry, why)
                out.append(entry)
                break
            prep = _prepare(settings, reg, policy_id, slot, cfg)
            failures = prep["checks"]["failures"]
            if dry_run:
                repo = prep["slot"] / "runner"
                plan = {
                    "dry_run": True, "policy_id": policy_id, "policy": policy["name"], "origin": reg.origin,
                    "model_name": status["model_name"], "api_base": status["api_base"], "budget": budget,
                    "games_requested": games, "would_start": budget_ok and not failures, "preflight_failures": failures,
                    "checks": prep["checks"], "slot": str(prep["slot"]), "solution": str(prep["solution"]),
                    "solution_sha256": prep["solution_sha256"], "placeholders": list(PLAY_REQUIRED),
                    "actor_id": prep["actor_id"], "actor": cfg.record(), "env_id": prep["env_id"],
                    "environment": prep["environment"], "runs_dir": str(settings.runs_dir),
                    "would_run": [f"(cd {repo} && uv run {' '.join(DATASET_RELOAD)})",
                                  f"(cd {repo} && uv run jiuwenswarm-start --name {INSTANCE} all)",
                                  f"(cd {repo} && uv run python -m career_sim_runner play --submission {prep['solution']} "
                                  f"--ws-url ws://127.0.0.1:<agent port> --timeout-s {cfg.timeout_s})"],
                }
                reg.decide("target_dry_run", policy_id, {k: plan[k] for k in (
                    "budget", "would_start", "preflight_failures", "solution_sha256", "actor_id", "env_id", "games_requested")},
                    "dry run: slot, dataset reload, solution and runner checks; JiuwenSwarm and play not started")
                out.append(plan)
                break
            if failures:
                entry = {"game": game, "started": False, "policy_id": policy_id, "budget": budget,
                         "reason": "runner checks failed", "failures": failures}
                reg.decide("target_refused", policy_id, entry, why)
                out.append(entry)
                break
            entry = _play_one(settings, reg, policy_id, prep, cfg, env_path, game, max_usd_per_game, reserve_usd, purpose,
                              why, slot, poll_s, settle_s, settle_max_s, stop_on_interruption)
            out.append(entry)
            if entry["stopped"]:
                break
    return out


# -- command line ----------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    from careerlab.config import load_settings

    parser = argparse.ArgumentParser(prog="python -m careerlab.target", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("key", help="usage and remaining credit of the competition key (free, no model call)")
    reg_p = sub.add_parser("register", help="register a policy folder and its missing ancestors in this origin's registry")
    reg_p.add_argument("path")
    reg_p.add_argument("--by", default="target")
    play = sub.add_parser("play", help="play real target games under the budget guard")
    play.add_argument("--policy", required=True, help="policy id or name")
    mode = play.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="everything except JiuwenSwarm and play; spends nothing")
    mode.add_argument("--spend", action="store_true", help="really play: spends money on the competition key")
    play.add_argument("--games", type=int, default=1)
    play.add_argument("--max-usd-per-game", type=float, default=3.0)
    play.add_argument("--reserve-usd", type=float, default=15.0)
    play.add_argument("--purpose", default="pilot", choices=["pilot", "screen", "calibrate", "audit", "confirm", "infra"])
    play.add_argument("--why", default=DEFAULT_WHY, help="decision rationale recorded in the registry")
    play.add_argument("--slot", type=int, default=0)
    args = parser.parse_args(argv)
    settings = load_settings()
    if args.cmd == "key":
        print(json.dumps(key_status(target_env_path(settings)), indent=2))
        return 0
    if settings.origin != TARGET_ORIGIN:
        print(f"set CAREERLAB_ORIGIN={TARGET_ORIGIN}: target games never use the race registry", file=sys.stderr)
        return 2
    reg = settings.registry()
    if args.cmd == "register":
        print(register_policy_folder(settings, reg, Path(args.path), by=args.by))
        return 0
    row = reg.db.execute("SELECT policy_id FROM policies WHERE policy_id=? OR name=?", (args.policy, args.policy)).fetchone()
    if row is None:
        print(f"unknown policy {args.policy!r} in the {settings.origin} registry; register it first", file=sys.stderr)
        return 2
    out = play_target(settings, reg, row[0], games=args.games, max_usd_per_game=args.max_usd_per_game,
                      reserve_usd=args.reserve_usd, dry_run=args.dry_run, slot=args.slot, purpose=args.purpose, why=args.why)
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
