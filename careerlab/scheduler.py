"""Programmatic planner: leases queued jobs, runs them, and integrates results.

The scheduler is the single writer of the registry. Real-game work is checked
against the authorisation gate in ``lab/gate.json`` before any job starts;
the gate is part of the pre-registered protocol and is edited only by the
orchestrator after a written organiser clarification or a user decision.
"""

from __future__ import annotations

import asyncio
import json
import os
import socket
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from careerlab.actors.claude_cli import ClaudeWorkerConfig, run_claude_episode
from careerlab.actors.scripted import make_scripted
from careerlab.config import Settings
from careerlab.episode import run_driven_episode
from careerlab.mcp_client import GameClient, ServerSpec
from careerlab.pool import ServerPool
from careerlab.store import Registry


class GateClosed(RuntimeError):
    pass


def load_gate(settings: Settings) -> dict[str, Any]:
    return json.loads((settings.lab_dir / "gate.json").read_text())


def check_gate(settings: Settings, registry: Registry, actor_kind: str, environment: str, n_new: int) -> None:
    """Refuse work the current authorisation does not cover."""
    gate = load_gate(settings)
    rule = gate["environments"][environment]["actors"].get(actor_kind)
    if not rule or not rule.get("allowed"):
        raise GateClosed(f"{actor_kind} actors on {environment} are not authorised: {rule and rule.get('reason')}")
    cap = rule.get("max_episodes")
    if cap is not None:
        used = registry.db.execute(
            "SELECT COUNT(*) FROM jobs j JOIN actors a USING(actor_id) JOIN environments e USING(env_id) "
            "WHERE a.kind=? AND json_extract(e.fingerprint,'$.environment')=?", (actor_kind, environment)).fetchone()[0]
        used += int(rule.get("prior_sessions", 0))
        if used + n_new > cap:
            raise GateClosed(f"{actor_kind} on {environment}: {used}+{n_new} episodes would exceed the gate cap {cap}")


class Scheduler:
    def __init__(self, settings: Settings, registry: Registry, owner: str | None = None):
        self.settings, self.registry = settings, registry
        self.owner = owner or f"{socket.gethostname()}:{os.getpid()}:{uuid.uuid4().hex[:6]}"
        self.heartbeat = settings.data_dir / "scheduler.heartbeat.json"

    def _beat(self, state: dict[str, Any]) -> None:
        tmp = self.heartbeat.with_suffix(".tmp")
        tmp.write_text(json.dumps({"owner": self.owner, "pid": os.getpid(), "at": time.time(), **state}))
        os.replace(tmp, self.heartbeat)

    def owner_alive(self, owner: str | None) -> bool:
        if not owner or not self.heartbeat.exists():
            return False
        beat = json.loads(self.heartbeat.read_text())
        return beat.get("owner") == owner and time.time() - beat.get("at", 0) < 120

    def recover(self) -> dict[str, int]:
        counts = self.registry.recover(self.owner_alive)
        self.registry.decide("recover", None, counts, "reconciled leased/running jobs with real processes at start-up")
        return counts

    async def run_scripted(self, slots: int = 8, limit: int | None = None) -> dict[str, int]:
        """Run queued scripted-actor jobs on a rotating stdio server pool."""
        jobs = self.registry.lease(self.owner, limit or 10**9, actor_kind="scripted")
        if not jobs:
            return {}
        counts: dict[str, int] = {}
        queue: asyncio.Queue[Any] = asyncio.Queue()
        for job in jobs:
            queue.put_nowait(job)
        rules = {r["policy_id"]: json.loads((Path(r["bundle_path"]) / "scripted.json").read_text())
                 for r in self.registry.db.execute("SELECT policy_id, bundle_path FROM policies")
                 if (Path(r["bundle_path"]) / "scripted.json").exists()}

        async def worker(pool: ServerPool) -> None:
            while True:
                try:
                    job = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                run_dir = self.settings.runs_dir / job["job_id"]
                self.registry.mark_running(job["job_id"], os.getpid(), str(run_dir))
                actor = make_scripted(rules[job["policy_id"]]["rule_set"], _seed(job["job_id"]))
                async with pool.lease() as client:
                    await run_driven_episode(client, actor, job["job_id"], run_dir,
                                             on_session=lambda sid, root, j=job["job_id"]: self.registry.set_session(j, sid, root))
                outcome = self.registry.ingest(job["job_id"], run_dir)
                counts[outcome] = counts.get(outcome, 0) + 1
                self._beat({"running": "scripted", "done": sum(counts.values())})

        async with ServerPool(self.settings, self.settings.servers_dir / f"sched-{uuid.uuid4().hex[:6]}", slots=slots) as pool:
            await asyncio.gather(*(worker(pool) for _ in range(slots)))
        return counts

    async def resume_scripted(self) -> dict[str, int]:
        """Continue interrupted scripted episodes in their own game session (flagged resumed).

        Observation comes first: if the session is already over, its ending is recorded;
        if the session is gone, the attempt stays interrupted and a new attempt is queued.
        """
        counts = {"resumed": 0, "requeued": 0}
        rules = {r["policy_id"]: json.loads((Path(r["bundle_path"]) / "scripted.json").read_text())
                 for r in self.registry.db.execute("SELECT policy_id, bundle_path FROM policies")
                 if (Path(r["bundle_path"]) / "scripted.json").exists()}
        rows = self.registry.db.execute(
            "SELECT j.* FROM jobs j JOIN actors a USING(actor_id) WHERE j.status='interrupted' AND a.kind='scripted' "
            "AND j.job_id NOT IN (SELECT job_id FROM evaluations)").fetchall()
        for job in rows:
            if job["policy_id"] not in rules:
                continue
            root = job["db_root"]
            if job["session_id"] and root and Path(root, "career_emulator.sqlite3").exists():
                spec = ServerSpec(f"resume-{job['job_id']}", Path(root))
                async with GameClient(spec, self.settings) as client:
                    actor = make_scripted(rules[job["policy_id"]]["rule_set"], _seed(job["job_id"] + "-resume"))
                    await run_driven_episode(client.view(), actor, job["job_id"], Path(job["run_dir"]), session_id=job["session_id"])
                outcome = self.registry.ingest(job["job_id"], Path(job["run_dir"]))
                if outcome == "interrupted":
                    self.registry.requeue_interrupted(job["job_id"], "resume failed; replacement attempt")
                    counts["requeued"] += 1
                else:
                    counts["resumed"] += 1
            else:
                self.registry.requeue_interrupted(job["job_id"], "no resumable session; replacement attempt")
                counts["requeued"] += 1
        self.registry.decide("resume", None, counts, "observe-first continuation of interrupted scripted episodes")
        return counts

    async def run_claude(self, concurrency: int = 2, limit: int | None = None) -> dict[str, int]:
        jobs = self.registry.lease(self.owner, limit or 10**9, actor_kind="claude-cli")
        counts: dict[str, int] = {}
        sem = asyncio.Semaphore(concurrency)
        actors = {r["actor_id"]: json.loads(r["config"]) for r in self.registry.db.execute("SELECT * FROM actors")}
        policies = {r["policy_id"]: r["bundle_path"] for r in self.registry.db.execute("SELECT policy_id, bundle_path FROM policies")}

        async def one(job: Any) -> None:
            async with sem:
                raw = actors[job["actor_id"]]
                cfg = ClaudeWorkerConfig(**{k: raw[k] for k in ClaudeWorkerConfig.__dataclass_fields__ if k in raw})
                run_dir = self.settings.runs_dir / job["job_id"]
                self.registry.mark_running(job["job_id"], os.getpid(), str(run_dir))
                await run_claude_episode(self.settings, cfg, Path(policies[job["policy_id"]]) / "bundle", job["job_id"], run_dir)
                outcome = self.registry.ingest(job["job_id"], run_dir)
                counts[outcome] = counts.get(outcome, 0) + 1
                self._beat({"running": "claude", "done": sum(counts.values())})

        await asyncio.gather(*(one(j) for j in jobs))
        return counts


def _seed(job_id: str) -> int:
    import hashlib

    return int(hashlib.sha256(job_id.encode()).hexdigest()[:8], 16)
