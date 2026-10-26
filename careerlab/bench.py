"""Throughput measurement for scripted episodes through the official MCP server."""

from __future__ import annotations

import asyncio
import json
import statistics
import time
import uuid
from typing import Any

from careerlab.actors.scripted import make_scripted
from careerlab.config import Settings
from careerlab.episode import run_driven_episode
from careerlab.pool import ServerPool


async def bench(settings: Settings, slots: int, per_slot: int, episodes: int, actor: str = "uniform-affordable",
                seed0: int = 0, sessions_per_db: int = 12, tag: str | None = None) -> dict[str, Any]:
    """Steady-state throughput with the rotating pool; start-up time is reported separately."""
    tag = tag or f"bench-pool-{slots}x{per_slot}-{uuid.uuid4().hex[:6]}"
    runs = settings.runs_dir / tag
    queue: asyncio.Queue[int] = asyncio.Queue()
    for i in range(episodes):
        queue.put_nowait(i)
    results: list[dict[str, Any]] = []

    async def worker(pool: ServerPool) -> None:
        while True:
            try:
                i = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            async with pool.lease() as client:
                res = await run_driven_episode(client, make_scripted(actor, seed0 + i), f"{tag}-{i}", runs / f"ep{i:05d}")
            results.append({"outcome": res.outcome, "steps": res.steps, "wall": res.wall_seconds,
                            "months": res.survival_months, "score": res.quantitative_score,
                            "observe_s": res.tool_seconds.get("observe", 0) / max(res.tool_calls.get("observe", 1), 1),
                            "act_s": res.tool_seconds.get("take_action", 0) / max(res.tool_calls.get("take_action", 1), 1)})

    t0 = time.perf_counter()
    async with ServerPool(settings, settings.servers_dir / tag, slots=slots, per_slot=per_slot, sessions_per_db=sessions_per_db) as pool:
        startup = time.perf_counter() - t0
        t1 = time.perf_counter()
        await asyncio.gather(*(worker(pool) for _ in range(slots * per_slot)))
        elapsed = time.perf_counter() - t1
        processes = pool.started_processes
    steps = sum(r["steps"] for r in results)
    summary = {
        "tag": tag, "slots": slots, "per_slot": per_slot, "actor": actor, "sessions_per_db": sessions_per_db,
        "episodes": len(results), "startup_s": round(startup, 2), "elapsed_s": round(elapsed, 2), "processes": processes,
        "episodes_per_s": round(len(results) / elapsed, 2), "steps_per_s": round(steps / elapsed, 1),
        "mean_steps": round(steps / max(len(results), 1), 1),
        "median_observe_ms": round(1000 * statistics.median(r["observe_s"] for r in results), 2),
        "median_action_ms": round(1000 * statistics.median(r["act_s"] for r in results), 2),
        "outcomes": {o: sum(r["outcome"] == o for r in results) for o in {r["outcome"] for r in results}},
    }
    (runs / "bench_summary.json").write_text(json.dumps(summary, indent=2))
    return summary
