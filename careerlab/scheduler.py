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
        beat_dir = self.settings.data_dir / "heartbeats"
        beat_dir.mkdir(parents=True, exist_ok=True)
        path = beat_dir / f"{self.owner.replace(':', '_')}.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"owner": self.owner, "pid": os.getpid(), "at": time.time(), **state}))
        os.replace(tmp, path)

    async def _heartbeat_loop(self) -> None:
        while True:
            self._beat({"alive": True})
            await asyncio.sleep(20)

    def owner_alive(self, owner: str | None) -> bool:
        """A lease owner is alive if its process exists on this host or its own heartbeat is fresh."""
        if not owner:
            return False
        host, _, rest = owner.partition(":")
        pid = rest.split(":", 1)[0]
        if host == socket.gethostname() and pid.isdigit():
            try:
                os.kill(int(pid), 0)
                return True
            except OSError:
                return False
        beat_file = self.settings.data_dir / "heartbeats" / f"{owner.replace(':', '_')}.json"
        return beat_file.exists() and time.time() - json.loads(beat_file.read_text()).get("at", 0) < 120

    def recover(self) -> dict[str, int]:
        counts = self.registry.recover(self.owner_alive)
        self.registry.decide("recover", None, counts, "reconciled leased/running jobs with real processes at start-up")
        return counts

    async def run_scripted(self, slots: int = 8, limit: int | None = None, purpose: str | None = None) -> dict[str, int]:
        """Run queued scripted-actor jobs on a rotating stdio server pool."""
        jobs = self.registry.lease(self.owner, limit or 10**9, actor_kind="scripted", purpose=purpose)
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
                if not self.registry.mark_running(job["job_id"], os.getpid(), str(run_dir), owner=self.owner):
                    continue
                actor = make_scripted(rules[job["policy_id"]]["rule_set"], _seed(job["job_id"]))
                async with pool.lease() as client:
                    await run_driven_episode(client, actor, job["job_id"], run_dir,
                                             on_session=lambda sid, root, j=job["job_id"]: self.registry.set_session(j, sid, root))
                outcome = self.registry.ingest(job["job_id"], run_dir)
                counts[outcome] = counts.get(outcome, 0) + 1
                self._beat({"running": "scripted", "done": sum(counts.values())})

        beat = asyncio.create_task(self._heartbeat_loop())
        async with ServerPool(self.settings, self.settings.servers_dir / f"sched-{uuid.uuid4().hex[:6]}", slots=slots) as pool:
            await asyncio.gather(*(worker(pool) for _ in range(slots)))
        beat.cancel()
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
            "AND j.origin=? AND j.job_id NOT IN (SELECT job_id FROM evaluations)", (self.registry.origin,)).fetchall()
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

    async def wait_for_quota(self, max_five_hour: float) -> None:
        """Hold new episodes while the shared five-hour window is above the cap (it also serves the orchestrator)
        or the seven-day window is ahead of its pace to the last cutoff (see `weekly_allowance`)."""
        while True:
            cap_file = self.settings.data_dir / "quota_cap.json"  # live override, editable while schedulers run
            cap, pace = max_five_hour, None
            if cap_file.exists():
                try:
                    cfg = json.loads(cap_file.read_text())
                    pace = cfg.get("weekly_pace")
                    cap = float(cfg["max_five_hour"])
                except (ValueError, KeyError):
                    pass
            now = time.time()
            util, resets_at = latest_quota(self.settings.runs_dir)
            week, week_resets = latest_quota(self.settings.runs_dir, window="seven_day")
            five_ok = util is None or util < cap or bool(resets_at and now > resets_at)
            week_ok = week is None or not week_resets or now > week_resets or week < weekly_allowance(now, week_resets, pace)
            if five_ok and week_ok:
                return
            self._beat({"waiting_for_quota": util, "resets_at": resets_at, "seven_day": week, "seven_day_resets_at": week_resets})
            await asyncio.sleep(60)

    async def run_claude(self, concurrency: int = 2, limit: int | None = None, purpose: str | None = None,
                         max_five_hour: float = 0.75) -> dict[str, int]:
        jobs = self.registry.lease(self.owner, limit or 10**9, actor_kind="claude-cli", purpose=purpose)
        counts: dict[str, int] = {}
        sem = asyncio.Semaphore(concurrency)
        actors = {r["actor_id"]: json.loads(r["config"]) for r in self.registry.db.execute("SELECT * FROM actors")}
        policies = {r["policy_id"]: r["bundle_path"] for r in self.registry.db.execute("SELECT policy_id, bundle_path FROM policies")}

        async def one(job: Any) -> None:
            async with sem:
                await self.wait_for_quota(max_five_hour)
                raw = actors[job["actor_id"]]
                cfg = ClaudeWorkerConfig(**{k: raw[k] for k in ClaudeWorkerConfig.__dataclass_fields__ if k in raw})
                run_dir = self.settings.runs_dir / job["job_id"]
                if not self.registry.mark_running(job["job_id"], os.getpid(), str(run_dir), owner=self.owner):
                    return
                await run_claude_episode(self.settings, cfg, Path(policies[job["policy_id"]]), job["job_id"], run_dir)
                outcome = self.registry.ingest(job["job_id"], run_dir)
                counts[outcome] = counts.get(outcome, 0) + 1
                self._beat({"running": "claude", "done": sum(counts.values())})

        beat = asyncio.create_task(self._heartbeat_loop())
        await asyncio.gather(*(one(j) for j in jobs))
        beat.cancel()
        return counts

    async def run_claude_continuous(self, concurrency: int, stop_file: Path, max_five_hour: float = 0.80,
                                    purpose: str | None = None, poll_s: float = 20.0) -> dict[str, int]:
        """Fast race: lease one job whenever a slot frees, so a job queued a minute ago with a higher priority
        runs next. Stops leasing when `stop_file` exists and lets the games in flight finish."""
        counts: dict[str, int] = {}

        async def one(job: Any) -> None:
            row = self.registry.db.execute("SELECT config FROM actors WHERE actor_id=?", (job["actor_id"],)).fetchone()
            raw = json.loads(row["config"])
            cfg = ClaudeWorkerConfig(**{k: raw[k] for k in ClaudeWorkerConfig.__dataclass_fields__ if k in raw})
            bundle = self.registry.db.execute("SELECT bundle_path FROM policies WHERE policy_id=?", (job["policy_id"],)).fetchone()[0]
            run_dir = self.settings.runs_dir / job["job_id"]
            if not self.registry.mark_running(job["job_id"], os.getpid(), str(run_dir), owner=self.owner):
                return
            await run_claude_episode(self.settings, cfg, Path(bundle), job["job_id"], run_dir)
            outcome = self.registry.ingest(job["job_id"], run_dir)
            counts[outcome] = counts.get(outcome, 0) + 1
            self._beat({"running": "claude-continuous", "done": sum(counts.values())})

        beat = asyncio.create_task(self._heartbeat_loop())
        running: set[asyncio.Task[None]] = set()
        while not stop_file.exists():
            while len(running) < concurrency and not stop_file.exists():
                await self.wait_for_quota(max_five_hour)
                jobs = self.registry.lease(self.owner, 1, actor_kind="claude-cli", purpose=purpose)
                if not jobs:
                    break
                running.add(asyncio.create_task(one(jobs[0])))
            if running:
                done, running = await asyncio.wait(running, timeout=poll_s, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    if task.exception() is not None:  # the job stays running until `recover` marks it interrupted
                        counts["error"] = counts.get("error", 0) + 1
                        self._beat({"error": repr(task.exception())})
            else:
                await asyncio.sleep(poll_s)
        if running:
            await asyncio.gather(*running)
        beat.cancel()
        return counts


COMPETITION_END = 1793577600.0  # 2 Nov 2026 00:00 UTC, i.e. the last cutoff (1 Nov 24:00 UK)


def weekly_allowance(now: float, resets_at: float, pace: dict[str, float] | None = None) -> float:
    """Share of the seven-day window the lab may have used by `now`.

    A straight line from `initial` at the window start to `final` at the last
    cutoff (or the window end, if sooner). Running at the five-hour cap in every
    window would empty the week in about two days; the line spreads it over the
    competition and keeps the rest for the team's own chats. `pace` (from
    quota_cap.json "weekly_pace") overrides start, end, initial or final.
    """
    pace = pace or {}
    if pace.get("knots"):  # [[unix time, share], ...]: piecewise line, flat before the first and after the last knot
        knots = sorted((float(t), float(v)) for t, v in pace["knots"])
        if now <= knots[0][0]:
            return knots[0][1]
        for (t0, v0), (t1, v1) in zip(knots, knots[1:]):
            if now <= t1:
                return v0 + (v1 - v0) * (now - t0) / max(t1 - t0, 1.0)
        return knots[-1][1]
    start = pace.get("start", resets_at - 7 * 86400)
    end = pace.get("end", min(resets_at, COMPETITION_END))
    initial, final = pace.get("initial", 0.10), pace.get("final", 0.90)
    frac = min(max((now - start) / max(end - start, 1.0), 0.0), 1.0)
    return initial + (final - initial) * frac


def latest_quota(runs_dir: Path, newest: int = 40, window: str = "five_hour") -> tuple[float | None, float | None]:
    """Latest utilisation and reset time of one rate-limit window ("five_hour" or "seven_day") seen by any worker."""
    streams = sorted(runs_dir.glob("*/stream-*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:newest]
    best: tuple[float, float, float] | None = None
    for path in streams:
        mtime = path.stat().st_mtime
        for line in path.open(encoding="utf-8", errors="replace"):
            if '"rate_limit_event"' not in line:
                continue
            window_info = json.loads(line).get("rate_limit_info", {}).get("unifiedWindows", {}).get(window, {})
            if window_info.get("utilization") is not None and (best is None or mtime >= best[0]):
                best = (mtime, float(window_info["utilization"]), float(window_info.get("resetsAt") or 0))
    return (best[1], best[2]) if best else (None, None)


def _seed(job_id: str) -> int:
    import hashlib

    return int(hashlib.sha256(job_id.encode()).hexdigest()[:8], 16)
