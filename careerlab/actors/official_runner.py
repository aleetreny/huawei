"""Target actor: the official participation runner (JiuwenSwarm 0.2.4b3 + designated model).

Each slot is an isolated copy of the runner at the pinned commit with its own HOME,
so the JiuwenSwarm instance ``career_emu``, the runner's ``.career_sim_runner``
directory and the game database are private to the slot. Slots never share a
database and run one game at a time, matching how the runner itself is used.
Credentials come from a file outside the repository (``CAREERLAB_TARGET_ENV``) and
are never logged. Nothing here changes the runner's pinned configuration.

Status: slot preparation is tested; a full episode needs the competition key or an
approved team-funded route (see lab/gate.json).
"""

from __future__ import annotations

import asyncio
import json
import os
import math
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.episode import EpisodeResult, atomic_write_json

RUNNER_COMMIT = "00b084a8"


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


def prepare_slot(settings: Settings, slot: int) -> Path:
    """Create (once) a private runner copy and HOME for one target slot."""
    root = slot_dir(settings, slot)
    repo, home = root / "runner", root / "home"
    home.mkdir(parents=True, exist_ok=True)
    if not (repo / ".git").exists():
        subprocess.run(["git", "clone", "--quiet", str(settings.runner_dir), str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "checkout", "--quiet", RUNNER_COMMIT], check=True)
        subprocess.run(["uv", "sync", "--frozen", "--quiet"], cwd=repo, check=True, env=_env(home))
    env_src = credentials_path(settings)
    if not credential_status(settings)["configured"]:
        raise ValueError("target credentials are incomplete; configure them outside the repository")
    shutil.copyfile(env_src, repo / ".env")
    os.chmod(repo / ".env", 0o600)
    subprocess.run(["uv", "run", "python", "-m", "career_sim_runner", "setup"], cwd=repo, check=True,
                   env=_env(home), capture_output=True)
    return root


def _env(home: Path) -> dict[str, str]:
    keep = ("PATH", "USER", "LOGNAME", "LANG", "TMPDIR", "SHELL")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    env["HOME"] = str(home)
    return env


def _ws_url(repo: Path, home: Path) -> str | None:
    out = subprocess.run(["uv", "run", "jiuwenswarm-start", "--list"], cwd=repo, env=_env(home),
                         capture_output=True, text=True, timeout=60)
    for line in out.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0] == "career_emu" and "/" in parts[-1]:
            return f"ws://127.0.0.1:{parts[-1].split('/', 1)[0]}"
    return None


async def run_target_episode(settings: Settings, cfg: TargetConfig, solution_dir: Path, job_id: str,
                             run_dir: Path, slot: int, budget=None) -> EpisodeResult:
    """Start the slot's JiuwenSwarm instance, play one game with the official runner, collect its report."""
    run_dir.mkdir(parents=True, exist_ok=True)
    solution_dir=development_bundle(solution_dir,run_dir)
    from careerlab.budget import BudgetClosed
    if budget is None:
        raise BudgetClosed("target execution requires a fresh paid-budget reservation")
    if cfg.route!="competition-key" or cfg.model_name!="deepseek-v4-flash" or cfg.runner_commit!=RUNNER_COMMIT:
        raise ValueError("only the pinned official competition-key actor is enabled")
    if not math.isfinite(cfg.timeout_s) or cfg.timeout_s<=0:
        raise ValueError("target timeout must be positive and finite")
    root = await asyncio.to_thread(prepare_slot,settings,slot)
    repo, home = root / "runner", root / "home"
    if not (repo / ".env").exists():
        result = EpisodeResult(job_id, None, "interrupted", interruption="no target credentials configured")
        atomic_write_json(run_dir / "result.json", asdict(result))
        return result
    atomic_write_json(run_dir / "actor.json", cfg.record())
    started = time.perf_counter()
    report_root=repo/".career_sim_runner"/"career_emu"/"outputs"
    previous={str(p):p.stat().st_mtime_ns for p in report_root.rglob("score_report.json")}
    instance = await asyncio.create_subprocess_exec("uv", "run", "jiuwenswarm-start", "--name", "career_emu", "all",
                                                    cwd=str(repo), env=_env(home), stdout=(run_dir / "jiuwen.log").open("w"),
                                                    stderr=subprocess.STDOUT)
    play = None
    try:
        url = None
        for _ in range(120):
            url = _ws_url(repo, home)
            if url:
                break
            await asyncio.sleep(1)
        if not url:
            result = EpisodeResult(job_id, None, "interrupted", interruption="JiuwenSwarm instance did not come up")
        else:
            budget.start(job_id)  # committed before the first paid play request
            play = await asyncio.create_subprocess_exec(
                "uv", "run", "python", "-m", "career_sim_runner", "play", "--submission", str(solution_dir),
                "--ws-url", url, "--timeout-s", str(cfg.timeout_s), cwd=str(repo), env=_env(home),
                stdout=(run_dir / "play.log").open("w"), stderr=subprocess.STDOUT)
            try:
                await asyncio.wait_for(play.wait(),cfg.timeout_s)
            except asyncio.TimeoutError:
                play.kill()
                await play.wait()
            reports = sorted((p for p in report_root.rglob("score_report.json") if previous.get(str(p))!=p.stat().st_mtime_ns), key=os.path.getmtime)
            result = _from_report(job_id, reports[-1], run_dir) if reports else EpisodeResult(job_id, None, "interrupted", interruption="no score report")
    finally:
        if play is not None and play.returncode is None:
            play.kill()
            await play.wait()
        if instance.returncode is None:
            instance.terminate()
        try:
            await asyncio.wait_for(instance.wait(), 30)
        except asyncio.TimeoutError:
            instance.kill()
    result.wall_seconds = round(time.perf_counter() - started, 1)
    atomic_write_json(run_dir / "result.json", asdict(result))
    return result


def _from_report(job_id: str, report_path: Path, run_dir: Path) -> EpisodeResult:
    report = json.loads(report_path.read_text())
    shutil.copyfile(report_path, run_dir / "score_report.json")
    score = report.get("ending_score") or {}
    usage = report.get("token_usage") or {}
    if not score:
        return EpisodeResult(job_id, report.get("session_id"), "interrupted",
                             interruption=f"runner ended without ending_score: {report.get('termination_reason')}",
                             actor_usage={"tokens": usage})
    q,t=score.get("quantitative_score"),score.get("survival_months")
    if (not isinstance(q,(int,float)) or isinstance(q,bool) or not math.isfinite(q) or not 0<=q<=100
            or not isinstance(t,int) or isinstance(t,bool) or not 0<t<=48):
        return EpisodeResult(job_id,report.get("session_id"),"interrupted",interruption="invalid official score report",actor_usage={"tokens":usage})
    events=report.get("events_log")
    if events:
        source=Path(events).resolve()
        # Only the runner's own output directory, never arbitrary paths such as .env.
        if source.is_file() and source.is_relative_to(report_path.parent.resolve()):
            shutil.copyfile(source,run_dir/"target-transcript.jsonl")
            events=str(run_dir/"target-transcript.jsonl")
        else:
            events=None
    cost={k:usage[k] for k in ("billed_cost_usd","cost_usd","total_cost_usd") if k in usage}
    return EpisodeResult(job_id, report.get("session_id"), "completed" if score.get("completed") else "eliminated",
                         survival_months=score.get("survival_months"), quantitative_score=score.get("quantitative_score"),
                         ending_score=score, failure_reason=report.get("failure_reason") or score.get("failure_reason"),
                         actor_usage={"tokens": usage, "total_tokens": usage.get("total_tokens"),**cost,
                                                          "termination_reason": report.get("termination_reason")},
                         trajectory_path=events)
