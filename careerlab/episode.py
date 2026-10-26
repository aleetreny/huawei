"""Run one episode to its real end and write evidence in the worker's own directory.

Outcome classes keep game results apart from operational problems:

- ``completed``: the career reached month 48 (ending_score.completed is true);
- ``eliminated``: the game ended early through a game failure condition;
- ``interrupted``: an operational problem stopped the episode (tool error,
  timeout, actor failure, step cap). It carries no score and is never counted
  as a zero; the session id is kept so it can be inspected or resumed.
"""

from __future__ import annotations

import json
import os
import time
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from careerlab.mcp_client import GameClient, is_terminal, phase


@dataclass
class Decision:
    choice: int
    notes: str = ""
    meta: dict[str, Any] = field(default_factory=dict)


class DrivenActor(Protocol):
    """An actor that decides one step at a time while the runner drives the game."""

    def config(self) -> dict[str, Any]: ...

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision: ...


@dataclass
class EpisodeResult:
    job_id: str
    session_id: str | None
    outcome: str  # completed | eliminated | interrupted
    survival_months: int | None = None
    quantitative_score: float | None = None
    ending_score: dict[str, Any] | None = None
    failure_reason: str | None = None
    interruption: str | None = None
    steps: int = 0
    rejected_actions: int = 0
    ambiguous_actions: int = 0
    wall_seconds: float = 0.0
    tool_calls: dict[str, int] = field(default_factory=dict)
    tool_seconds: dict[str, float] = field(default_factory=dict)
    actor_usage: dict[str, Any] = field(default_factory=dict)
    trajectory_path: str | None = None
    resumed: bool = False
    db_root: str | None = None


def atomic_write_json(path: Path, payload: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def result_from_terminal(job_id: str, session_id: str, obs: dict[str, Any]) -> EpisodeResult:
    score = obs.get("ending_score") or {}
    flags = obs.get("current_state", {}).get("simulation_flags", {})
    completed = bool(score.get("completed"))
    return EpisodeResult(
        job_id=job_id,
        session_id=session_id,
        outcome="completed" if completed else "eliminated",
        survival_months=score.get("survival_months"),
        quantitative_score=score.get("quantitative_score"),
        ending_score=score or None,
        failure_reason=flags.get("failure_reason"),
    )


async def run_driven_episode(
    client: GameClient,
    actor: DrivenActor,
    job_id: str,
    run_dir: Path,
    max_steps: int = 4000,
    max_rejections_in_a_row: int = 5,
    session_id: str | None = None,
    on_session: Any = None,
) -> EpisodeResult:
    """Play a fresh (or resumed) session until the game itself ends."""
    run_dir.mkdir(parents=True, exist_ok=True)
    traj_path = run_dir / "trajectory.jsonl"
    started = time.perf_counter()
    resumed = session_id is not None
    db_root: str | None = None
    memory: dict[str, Any] = {}
    steps = rejected = rejected_streak = 0
    obs: dict[str, Any] = {}
    with traj_path.open("a", encoding="utf-8") as traj:
        def log(kind: str, **payload: Any) -> None:
            traj.write(json.dumps({"kind": kind, "t": round(time.perf_counter() - started, 4), **payload}, ensure_ascii=False) + "\n")
            traj.flush()

        try:
            spec = getattr(client, "spec", None)
            db_root = getattr(client, "db_root", None) or (str(spec.root) if spec is not None else None)
            if session_id is None:
                session_id = await client.new_game()
                log("new_game", session_id=session_id, db_root=db_root, actor=actor.config())
                if on_session:
                    on_session(session_id, db_root)
            else:
                log("resume", session_id=session_id, db_root=db_root, actor=actor.config())
            while True:
                obs = await client.observe(session_id)
                log("obs", step=steps, phase=phase(obs), obs=obs)
                if is_terminal(obs):
                    result = result_from_terminal(job_id, session_id, obs)
                    break
                if steps >= max_steps:
                    result = EpisodeResult(job_id, session_id, "interrupted", interruption=f"step cap {max_steps} reached")
                    break
                decision = await actor.decide(obs, memory)
                outcome = await client.take_action(session_id, decision.choice, decision.notes, before=obs)
                log("act", step=steps, choice=decision.choice, notes=decision.notes, meta=decision.meta,
                    applied=outcome.applied, reply=outcome.reply, attempts=outcome.attempts, ambiguous=outcome.ambiguous)
                steps += 1
                if outcome.applied:
                    rejected_streak = 0
                else:
                    rejected += 1
                    rejected_streak += 1
                    memory.setdefault("rejections", []).append({"choice": decision.choice, "reply": outcome.reply})
                    if rejected_streak >= max_rejections_in_a_row:
                        result = EpisodeResult(job_id, session_id, "interrupted", interruption=f"{rejected_streak} rejected actions in a row")
                        break
        except Exception as exc:  # operational failure: keep evidence, never fabricate a score
            log("error", error=repr(exc), traceback=traceback.format_exc())
            result = EpisodeResult(job_id, session_id, "interrupted", interruption=repr(exc))
    result.steps = steps
    result.rejected_actions = rejected
    result.ambiguous_actions = client.stats.ambiguous_actions
    result.wall_seconds = round(time.perf_counter() - started, 3)
    result.tool_calls = dict(client.stats.calls)
    result.tool_seconds = {k: round(v, 4) for k, v in client.stats.seconds.items()}
    usage = getattr(actor, "usage", None)
    if callable(usage):
        result.actor_usage = usage()
    result.trajectory_path = str(traj_path)
    result.resumed = resumed
    result.db_root = db_root
    atomic_write_json(run_dir / "result.json", asdict(result))
    return result
