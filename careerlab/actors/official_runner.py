"""Target actor: the official participation runner (JiuwenSwarm 0.2.4b3 + designated model).

Each slot is an isolated copy of the runner at the pinned commit with its own HOME,
so the JiuwenSwarm instance ``career_emu``, the runner's ``.career_sim_runner``
directory and the game database are private to the slot. Slots never share a
database and run one game at a time, matching how the runner itself is used.
Credentials come from a file outside the repository (``CAREERLAB_TARGET_ENV``) and
are never logged. Nothing here changes the runner's pinned configuration.

A game follows ``make play``: reload the packaged dev dataset, start the instance,
wait until its AgentServer accepts connections, run ``play``, then read the score
report written by that play (never an older game's report or session). Every
process is started in its own process group and stopped with all its children.
Budget control and registry bookkeeping live in ``careerlab.target``.

Status: slot preparation, dataset reload and the runner's checks ran on 26 Oct
(dry run, ``careerlab.target``); a full paid episode has not run yet.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import math
import os
import math
import re
import shutil
import signal
import socket
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.episode import EpisodeResult, atomic_write_json

RUNNER_COMMIT = "00b084a8"
INSTANCE = "career_emu"
PLAY_GRACE_S = 900.0  # the runner stops driving at --timeout-s and still writes its report; kill only after this
DATASET_RELOAD = ("career-emulator-engine", "update", "--source", "distribution", "--split", "dev")


def credentials_path(settings: Settings) -> Path:
    return Path(os.environ.get("CAREERLAB_TARGET_ENV") or settings.data_dir/"secrets"/"competition.env").expanduser().resolve()


def credential_status(settings: Settings) -> dict[str,Any]:
    """Never return secret values, contents, or parser exceptions containing them."""
    path=credentials_path(settings)
    values={}
    if path.is_file():
        for line in path.read_text().splitlines():
            match=re.match(r"^\s*(API_BASE|API_KEY|MODEL_NAME)\s*=\s*(.*?)\s*$",line)
            if match:
                values[match[1]]=match[2].strip().strip("\"'")
    present={k:bool(values.get(k)) for k in ("API_BASE","API_KEY","MODEL_NAME")}
    return {"configured":all(present.values()),"fields_present":present,"env_file":str(path),
            "runner_present":(settings.runner_dir/".git").exists()}


def development_bundle(bundle: Path, run_dir: Path) -> Path:
    """Ephemeral local-play wrapper, never the team's final design documents."""
    out=run_dir/"development-submission"
    shutil.copytree(bundle,out,dirs_exist_ok=True)
    (out/"design").mkdir(exist_ok=True)
    for name in ("README.md","design/skills_design.md","design/decision_report.md"):
        if not (out/name).exists():
            (out/name).write_text("# Development evaluation fixture\n\nThis directory is an isolated local-play wrapper, not a final submission. "
                                 "The registered manifest and Skills are copied unchanged. Results are recorded separately; "
                                 "no superiority or final document-quality claim is made.\n")
    return out


@dataclass(frozen=True)
class TargetConfig:
    route: str                       # "competition-key" | "team-openrouter"
    model_name: str = "deepseek-v4-flash"
    timeout_s: float = 7200.0
    runner_commit: str = RUNNER_COMMIT

    def record(self) -> dict[str, Any]:
        return {"kind": "jiuwenswarm-target", **asdict(self), "jiuwenswarm": "0.2.4b3", "mode": "agent"}


def slot_dir(settings: Settings, slot: int) -> Path:
    return settings.data_dir / "target-slots" / f"slot{slot}"


def instance_env_path(home: Path) -> Path:
    """JiuwenSwarm's instance env file; the runner's ``setup`` copies the key into it."""
    return home / ".jiuwenswarm-instances" / INSTANCE / "config" / ".env"


def prepare_slot(settings: Settings, slot: int) -> Path:
    """Create (once) a private runner copy and HOME for one target slot."""
    root = slot_dir(settings, slot)
    repo, home = root / "runner", root / "home"
    home.mkdir(parents=True, exist_ok=True)
    if not (repo / ".git").exists():
        subprocess.run(["git", "clone", "--quiet", str(settings.runner_dir), str(repo)], check=True, stdin=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(repo), "checkout", "--quiet", RUNNER_COMMIT], check=True, stdin=subprocess.DEVNULL)
        subprocess.run(["uv", "sync", "--frozen", "--quiet"], cwd=repo, check=True, env=_env(home), stdin=subprocess.DEVNULL)
    env_src = os.environ.get("CAREERLAB_TARGET_ENV", "")
    if env_src and Path(env_src).is_file():
        shutil.copyfile(env_src, repo / ".env")
        os.chmod(repo / ".env", 0o600)
    # stdin closed: `jiuwenswarm-init` asks for a language when stdin is a terminal, and with the output
    # captured that prompt would wait forever. Without a terminal it takes its non-interactive default.
    setup = subprocess.run(["uv", "run", "python", "-m", "career_sim_runner", "setup"], cwd=repo, env=_env(home),
                           stdin=subprocess.DEVNULL, capture_output=True, text=True)
    (root / "setup.log").write_text(setup.stdout + setup.stderr, encoding="utf-8")  # paths and ports only
    if setup.returncode != 0:
        raise RuntimeError(f"runner setup failed (exit {setup.returncode}); see {root / 'setup.log'}")
    if instance_env_path(home).is_file():
        os.chmod(instance_env_path(home), 0o600)  # setup writes the key there with default permissions
    return root


def reload_dev_dataset(repo: Path, home: Path, log_path: Path) -> int:
    """What ``make play`` runs before every game: load the packaged dev dataset (engine CLI, no model call)."""
    with log_path.open("w", encoding="utf-8") as log:
        return subprocess.run(["uv", "run", *DATASET_RELOAD], cwd=repo, env=_env(home), stdin=subprocess.DEVNULL,
                              stdout=log, stderr=subprocess.STDOUT, timeout=900).returncode


def _env(home: Path) -> dict[str, str]:
    keep = ("PATH", "USER", "LOGNAME", "LANG", "TMPDIR", "SHELL")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    env["HOME"] = str(home)
    return env


def _port_open(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


def _ws_url(repo: Path, home: Path) -> str | None:
    """AgentServer URL once the instance runs and accepts connections, else None.

    ``jiuwenswarm-start --list`` also lists stopped instances with their ports, so
    both the status column and the port itself are checked before ``play`` connects.
    """
    try:
        out = subprocess.run(["uv", "run", "jiuwenswarm-start", "--list"], cwd=repo, env=_env(home),
                             stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None
    for line in out.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0] == INSTANCE and parts[1] == "running" and "/" in parts[-1]:
            try:
                port = int(parts[-1].split("/", 1)[0])
            except ValueError:
                return None
            return f"ws://127.0.0.1:{port}" if _port_open(port) else None
    return None


def _stop_stale_instance(repo: Path, home: Path) -> None:
    """Official stop of an instance an earlier crash left running in this slot (no-op when none runs)."""
    with contextlib.suppress(subprocess.TimeoutExpired):
        subprocess.run(["uv", "run", "jiuwenswarm-start", "--stop", INSTANCE], cwd=repo, env=_env(home),
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)


def _reports(report_root: Path) -> dict[Path, int]:
    if not report_root.exists():
        return {}
    return {p: p.stat().st_mtime_ns for p in report_root.rglob("score_report.json")}


def _new_report(report_root: Path, before: dict[Path, int]) -> Path | None:
    """The newest score report created or rewritten since ``before`` was taken; an older game's is never reused."""
    fresh = {p: mtime for p, mtime in _reports(report_root).items() if before.get(p) != mtime}
    return max(fresh, key=fresh.__getitem__) if fresh else None


async def _spawn(*cmd: str, repo: Path, home: Path, log: Path) -> asyncio.subprocess.Process:
    with log.open("w", encoding="utf-8") as out:  # the child keeps its own descriptor
        return await asyncio.create_subprocess_exec(*cmd, cwd=str(repo), env=_env(home), stdin=subprocess.DEVNULL,
                                                    stdout=out, stderr=subprocess.STDOUT, start_new_session=True)


def _signal_group(proc: asyncio.subprocess.Process, kill: bool) -> None:
    if not hasattr(os, "killpg"):  # no process groups (Windows)
        if proc.returncode is None:
            if kill:
                proc.kill()
            else:
                proc.terminate()
        return
    try:
        os.killpg(proc.pid, signal.SIGKILL if kill else signal.SIGTERM)
    except (ProcessLookupError, PermissionError):  # group already gone
        pass


async def _stop(proc: asyncio.subprocess.Process | None, grace_s: float = 30.0) -> None:
    """Stop a child started in its own session and everything it spawned (JiuwenSwarm's app, web and tools):
    SIGTERM to the whole process group, then SIGKILL to whatever is left."""
    if proc is None:
        return
    for kill in (False, True):
        _signal_group(proc, kill)
        try:
            await asyncio.wait_for(proc.wait(), 5.0 if kill else grace_s)
        except asyncio.TimeoutError:
            pass


async def run_target_episode(settings: Settings, cfg: TargetConfig, solution_dir: Path, job_id: str,
                             run_dir: Path, slot: int) -> EpisodeResult:
    """Play one game the way ``make play`` does and collect the score report written by this play.

    Operational failures end as ``interrupted`` with the evidence kept; a score is only taken from a
    report this play wrote, about a game session this play touched. Cancelling the coroutine (budget
    watchdog, Ctrl-C) stops ``play`` and the instance before the cancellation propagates.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    instance = play = None
    try:
        root = await asyncio.to_thread(prepare_slot, settings, slot)
        repo, home = root / "runner", root / "home"
        if not (repo / ".env").exists():
            result = EpisodeResult(job_id, None, "interrupted", interruption="no target credentials configured")
        elif await asyncio.to_thread(reload_dev_dataset, repo, home, run_dir / "dataset.log") != 0:
            result = EpisodeResult(job_id, None, "interrupted", interruption="dev dataset reload failed (see dataset.log)")
        else:
            atomic_write_json(run_dir / "actor.json", cfg.record())
            report_root = repo / ".career_sim_runner" / INSTANCE / "outputs"
            await asyncio.to_thread(_stop_stale_instance, repo, home)
            instance = await _spawn("uv", "run", "jiuwenswarm-start", "--name", INSTANCE, "all",
                                    repo=repo, home=home, log=run_dir / "jiuwen.log")
            url = None
            for _ in range(120):
                url = await asyncio.to_thread(_ws_url, repo, home)
                if url or instance.returncode is not None:
                    break
                await asyncio.sleep(1)
            if not url:
                result = EpisodeResult(job_id, None, "interrupted", interruption="JiuwenSwarm instance did not come up (see jiuwen.log)")
            else:
                before = _reports(report_root)
                play = await _spawn("uv", "run", "python", "-m", "career_sim_runner", "play", "--submission", str(solution_dir),
                                    "--ws-url", url, "--timeout-s", str(cfg.timeout_s), repo=repo, home=home, log=run_dir / "play.log")
                try:
                    await asyncio.wait_for(play.wait(), cfg.timeout_s + PLAY_GRACE_S)
                except asyncio.TimeoutError:
                    await _stop(play, grace_s=10.0)
                report = _new_report(report_root, before)
                result = _from_report(job_id, report, run_dir) if report else EpisodeResult(
                    job_id, None, "interrupted", interruption=f"play wrote no new score report (exit {play.returncode}; see play.log)")
    except Exception as exc:  # operational failure: keep the evidence, never fabricate a score
        result = EpisodeResult(job_id, None, "interrupted", interruption=f"target episode failed: {exc!r}")
    finally:
        await _stop(play, grace_s=10.0)
        await _stop(instance)
    result.wall_seconds = round(time.perf_counter() - started, 1)
    atomic_write_json(run_dir / "result.json", asdict(result))
    return result


def _copy_evidence(path: str | None, allowed: Path, dest: Path) -> Path | None:
    """Copy one runner log beside result.json, only from the report's own output folder."""
    if not path:
        return None
    src = Path(path).resolve()
    if not src.is_file() or not src.is_relative_to(allowed.resolve()):
        return None
    shutil.copyfile(src, dest)
    return dest


def _valid_score(score: dict[str, Any]) -> bool:
    q, months = score.get("quantitative_score"), score.get("survival_months")
    return (isinstance(q, (int, float)) and not isinstance(q, bool) and math.isfinite(q) and 0 <= q <= 100
            and isinstance(months, int) and not isinstance(months, bool) and 0 < months <= 48)


def _from_report(job_id: str, report_path: Path, run_dir: Path) -> EpisodeResult:
    """Episode result from the runner's score report.

    When the drive never saw a session id, the runner scores the database's latest session,
    which in a reused slot is an earlier game; so a score is accepted only for a session that
    appears in this play's own events log.
    """
    report = json.loads(report_path.read_text(encoding="utf-8"))
    shutil.copyfile(report_path, run_dir / "score_report.json")
    events = _copy_evidence(report.get("events_log"), report_path.parent, run_dir / "events.jsonl")
    _copy_evidence(report.get("transcript_log"), report_path.parent, run_dir / "transcript.log")
    score = report.get("ending_score") or {}
    usage = report.get("token_usage") or {}
    session = report.get("session_id") or None
    actor_usage = {"tokens": usage, "total_tokens": usage.get("total_tokens"), "runner_cost": usage.get("total_cost"),
                   "termination_reason": report.get("termination_reason"), "play_exit_code": report.get("play_exit_code")}
    trajectory = str(events) if events else None
    if not score:
        problem = f"runner ended without ending_score: {report.get('termination_reason')}"
    elif not session or events is None or session not in events.read_text(encoding="utf-8", errors="replace"):
        problem = "score report names a game session this play never touched (runner fell back to an older session)"
    elif not _valid_score(score):
        problem = "invalid official score report"
    else:
        completed = bool(score.get("completed"))
        return EpisodeResult(job_id, session, "completed" if completed else "eliminated",
                             survival_months=score.get("survival_months"), quantitative_score=score.get("quantitative_score"),
                             ending_score=score, failure_reason=None if completed else score.get("outcome"),
                             actor_usage=actor_usage, trajectory_path=trajectory)
    return EpisodeResult(job_id, session, "interrupted", interruption=problem, actor_usage=actor_usage, trajectory_path=trajectory)
