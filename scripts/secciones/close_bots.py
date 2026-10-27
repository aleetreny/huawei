"""P4 bots (no Claude quota): the same energy bot with and without a final-year cleanup.

Stories take the first listed option and the main action is Apply for a key project (lab
devices from T10, never Skill content). Arms differ only in the Energy mix of the last year:
  base        Health recovery, Mental recovery, Prepare report materials all run
  close       same, then from the final year Defuse legacy risk + Health recovery
  close-mind  same, then from the final year Defuse legacy risk + Mental recovery
Only careers that reach the final year can differ; compare their ending dimensions.

    CAREERLAB_DATA=~/careerlab-data/secciones-bots nice -n 10 uv run python scripts/secciones/close_bots.py --n 150 --slots 2
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("CAREERLAB_DATA", str(Path.home() / "careerlab-data" / "secciones-bots"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "energy-bots"))

from run import DEFUSE, HEALTH, MENTAL, NET, REPORT, EnergyBot, summarise  # noqa: E402

from careerlab.config import load_settings  # noqa: E402
from careerlab.episode import Decision, run_driven_episode  # noqa: E402
from careerlab.pool import ServerPool  # noqa: E402

FINAL_YEAR_FROM = 37  # lab parameter: first month of the last year (published length 48)
ARMS = {"base": None, "close": [DEFUSE, HEALTH], "close-mind": [DEFUSE, MENTAL]}


class CloseBot(EnergyBot):
    def __init__(self, arm: str):
        super().__init__("recovery+report")
        self.close_arm, self.name = arm, f"close-{arm}"

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision:
        month = int(obs.get("current_state", {}).get("time", {}).get("current_month") or 0)
        late = ARMS[self.close_arm]
        self.arm = "recovery+report"
        if late and month >= FINAL_YEAR_FROM:
            from run import ARMS as EARMS
            EARMS["_late"] = late
            self.arm = "_late"
        return await super().decide(obs, memory)


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--slots", type=int, default=2)
    a = ap.parse_args()
    s = load_settings()
    queue: asyncio.Queue = asyncio.Queue()
    for r in range(a.n):
        for arm in ARMS:
            queue.put_nowait((arm, r))
    rows: list[dict[str, Any]] = []

    async def worker(pool: ServerPool) -> None:
        while True:
            try:
                arm, r = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            run_dir = s.runs_dir / f"close-{arm}-{r:03d}"
            if not (run_dir / "result.json").exists():
                async with pool.lease() as client:
                    await run_driven_episode(client, CloseBot(arm), run_dir.name, run_dir)
            rows.append({"arm": arm, "rep": r, **summarise(run_dir)})
            (s.data_dir / "close-bots.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))

    async with ServerPool(s, s.servers_dir / "close-bots", slots=a.slots) as pool:
        await asyncio.gather(*(worker(pool) for _ in range(a.slots)))
    print(f"{len(rows)} episodes -> {s.data_dir / 'close-bots.jsonl'}")


if __name__ == "__main__":
    asyncio.run(main())
