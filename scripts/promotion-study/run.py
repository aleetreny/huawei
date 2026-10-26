"""Promotion study: scripted bots that survive long enough to reach promotion windows,
with randomised story choices and main actions, to look for general factors behind the
first promotion. No Claude quota. Own CAREERLAB_DATA (default ~/careerlab-data/promotion-study):
own server pool and run folders, nothing in the race's registry.

Each episode draws, from its own seed:
  - one Energy mix among the three most survivable mixes of T10 (lab/reports/energy-bots);
  - a uniformly random option for every story event;
  - a uniformly random quarterly main action.
Findings feed general Skill principles only; never event titles or fixed answers.

    CAREERLAB_DATA=~/careerlab-data/promotion-study nice -n 19 uv run python scripts/promotion-study/run.py --n 2000 --slots 2
"""

from __future__ import annotations

import argparse
import asyncio
import os
import random
from pathlib import Path
from typing import Any

os.environ.setdefault("CAREERLAB_DATA", str(Path.home() / "careerlab-data" / "promotion-study"))

from careerlab.config import load_settings  # noqa: E402
from careerlab.episode import Decision, run_driven_episode  # noqa: E402
from careerlab.mcp_client import phase  # noqa: E402
from careerlab.pool import ServerPool  # noqa: E402

DEFUSE, NET, HEALTH, MENTAL, REPORT, RESERVE = (
    "Defuse legacy risk", "Network maintenance", "Health recovery", "Mental recovery", "Prepare report materials", "Reserve energy")
MIXES: dict[str, list[str]] = {
    "defuse+health": [DEFUSE, HEALTH],
    "recovery+report": [HEALTH, MENTAL, REPORT],
    "report+network+health": [REPORT, NET, HEALTH],
}


class RandomStoryBot:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.mix = self.rng.choice(sorted(MIXES))
        self.name = f"promo-random-{self.mix}"

    def config(self) -> dict[str, Any]:
        return {"kind": "scripted", "name": self.name, "story": "uniform random", "main": "uniform random", "mix": self.mix}

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision:
        choices = obs.get("choices") or []
        ph = phase(obs)
        if ph == "energy":
            return Decision(self._energy(obs, choices, memory), notes=f"energy:{self.mix}")
        memory.pop("taken", None)
        pick = self.rng.choice(choices)
        return Decision(pick["choice"], notes=f"{ph}:random")

    def _energy(self, obs: dict[str, Any], choices: list[dict[str, Any]], memory: dict[str, Any]) -> int:
        left = (obs.get("current_event") or {}).get("remaining_energy", 0)
        taken = memory.setdefault("taken", [])
        by_name = {c.get("action", ""): c for c in choices}
        for name in MIXES[self.mix]:
            c = by_name.get(name)
            if c and c.get("energy_cost", 0) <= left and name not in taken:
                taken.append(name)
                return c["choice"]
        for name in (HEALTH, REPORT, NET, MENTAL):
            c = by_name.get(name)
            if c and 0 < c.get("energy_cost", 0) <= left:
                return c["choice"]
        reserve = by_name.get(RESERVE) or next((c for c in choices if c.get("energy_cost", 0) == 0), choices[0])
        return reserve["choice"]


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--slots", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=9_000_000)
    args = ap.parse_args()
    s = load_settings()
    queue: asyncio.Queue[int] = asyncio.Queue()
    for r in range(args.n):
        queue.put_nowait(r)
    done = 0

    async def worker(pool: ServerPool) -> None:
        nonlocal done
        while True:
            try:
                r = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            job_id = f"promo-{r:05d}"
            run_dir = s.runs_dir / job_id
            if not (run_dir / "result.json").exists():
                async with pool.lease() as client:
                    try:
                        await run_driven_episode(client, RandomStoryBot(args.seed0 + r), job_id, run_dir)
                    except Exception as exc:  # keep the batch going; the episode is simply missing
                        print(f"{job_id}: {exc!r}", flush=True)
            done += 1
            if done % 50 == 0:
                print(f"{done} episodes", flush=True)

    async with ServerPool(s, s.servers_dir / "promotion-study", slots=args.slots) as pool:
        await asyncio.gather(*(worker(pool) for _ in range(args.slots)))
    print(f"finished {done} episodes in {s.runs_dir}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
