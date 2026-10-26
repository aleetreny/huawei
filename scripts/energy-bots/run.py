"""T10 energy bots: scripted players that differ only in how they spend quarterly Energy.

Story events always take the first listed option and the quarterly main action is always
"Apply for a key project" (or the first option), so arms differ only in the Energy mix.
No Claude quota is used. Everything lives in its own CAREERLAB_DATA directory (default
~/careerlab-data/energy-bots): own server pool and run folders, nothing in the race's
registry. Thresholds below are lab parameters for the experiment, never Skill content.

    CAREERLAB_DATA=~/careerlab-data/energy-bots nice -n 19 uv run python scripts/energy-bots/run.py --n 30 --slots 2
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any

os.environ.setdefault("CAREERLAB_DATA", str(Path.home() / "careerlab-data" / "energy-bots"))

from careerlab.config import load_settings  # noqa: E402
from careerlab.episode import Decision, run_driven_episode  # noqa: E402
from careerlab.mcp_client import phase  # noqa: E402
from careerlab.pool import ServerPool  # noqa: E402

HIW, SKILL, DEFUSE = "High-intensity work", "Skill learning", "Defuse legacy risk"
NET, HEALTH, MENTAL, REPORT, RESERVE = "Network maintenance", "Health recovery", "Mental recovery", "Prepare report materials", "Reserve energy"
LOW = 4.0  # lab parameter: "low" Health or Dignity for the adaptive arm only

ARMS: dict[str, list[str]] = {
    "report+hiw": [REPORT, HIW],
    "report+skill": [REPORT, SKILL],
    "report+defuse": [REPORT, DEFUSE],
    "report+network+health": [REPORT, NET, HEALTH],
    "recovery+report": [HEALTH, MENTAL, REPORT],
    "hiw+network": [HIW, NET],
    "defuse+health": [DEFUSE, HEALTH],
    "network+recovery": [NET, HEALTH, MENTAL],
    "adaptive": [],  # recovery when Health or Dignity is low, otherwise report+hiw
    "reserve": [RESERVE],  # spend nothing: control
}
GRADE = re.compile(r"Half-year performance bonus \(([A-E][+-]?)\)")


def _stat(obs: dict[str, Any], key: str) -> float:
    return float(obs.get("current_state", {}).get("status", {}).get(key, 0) or 0)


class EnergyBot:
    def __init__(self, arm: str):
        self.arm, self.name = arm, f"energy-{arm}"

    def config(self) -> dict[str, Any]:
        return {"kind": "scripted", "name": self.name, "story": "first option", "main": "Apply for a key project", "low": LOW}

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision:
        choices = obs.get("choices") or []
        ph = phase(obs)
        if ph == "energy":
            return Decision(self._energy(obs, choices, memory), notes=self.name)
        memory.pop("taken", None)
        if ph == "main_action":
            pick = next((c for c in choices if c.get("action", "").startswith("Apply for a key project")), choices[0])
            return Decision(pick["choice"], notes="main: key project")
        return Decision(choices[0]["choice"], notes="story: first option")

    def _energy(self, obs: dict[str, Any], choices: list[dict[str, Any]], memory: dict[str, Any]) -> int:
        left = (obs.get("current_event") or {}).get("remaining_energy", 0)
        prefs = ARMS[self.arm]
        if self.arm == "adaptive":
            low = min(_stat(obs, "health"), _stat(obs, "dignity")) <= LOW
            prefs = [HEALTH, MENTAL, REPORT] if low else [REPORT, HIW]
        taken = memory.setdefault("taken", [])
        by_name = {c.get("action", ""): c for c in choices}
        for name in prefs:
            c = by_name.get(name)
            if c and c.get("energy_cost", 0) <= left and (name not in taken or name == RESERVE):
                taken.append(name)
                return c["choice"]
        cheap = sorted((c for c in choices if 0 < c.get("energy_cost", 0) <= left and c.get("action") in (REPORT, NET, HEALTH, MENTAL)),
                       key=lambda c: (prefs + [REPORT, HEALTH, NET, MENTAL]).index(c["action"]) if c["action"] in prefs + [REPORT, HEALTH, NET, MENTAL] else 99)
        if cheap and self.arm != "reserve":
            return cheap[0]["choice"]
        reserve = by_name.get(RESERVE) or next((c for c in choices if c.get("energy_cost", 0) == 0), choices[0])
        return reserve["choice"]


def summarise(run_dir: Path) -> dict[str, Any]:
    res = json.loads((run_dir / "result.json").read_text())
    grades, last = [], ""
    for line in (run_dir / "trajectory.jsonl").open(encoding="utf-8", errors="replace"):
        if '"obs"' not in line:
            continue
        rec = json.loads(line)
        ev = (rec.get("obs") or {}).get("events") or "" if isinstance(rec, dict) else ""
        if ev and ev != last:
            grades += GRADE.findall(ev)
        last = ev
    dims = {d["name"]: d.get("normalized_score") for d in (res.get("ending_score") or {}).get("dimensions", [])}
    return {"outcome": res["outcome"], "Q": res.get("quantitative_score"), "T": res.get("survival_months"),
            "failure": res.get("failure_reason") or res.get("interruption"), "grades": grades, **dims}


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--slots", type=int, default=2)
    ap.add_argument("--arms", nargs="*", default=list(ARMS))
    args = ap.parse_args()
    s = load_settings()
    out_dir = s.runs_dir
    jobs = [(arm, r) for r in range(args.n) for arm in args.arms]  # interleaved by replicate
    queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
    for j in jobs:
        queue.put_nowait(j)
    rows: list[dict[str, Any]] = []

    async def worker(pool: ServerPool) -> None:
        while True:
            try:
                arm, r = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            job_id = f"bot-{arm.replace('+', '-')}-{r:03d}"
            run_dir = out_dir / job_id
            if not (run_dir / "result.json").exists():
                async with pool.lease() as client:
                    await run_driven_episode(client, EnergyBot(arm), job_id, run_dir)
            rows.append({"arm": arm, "rep": r, **summarise(run_dir)})

    async with ServerPool(s, s.servers_dir / "energy-bots", slots=args.slots) as pool:
        await asyncio.gather(*(worker(pool) for _ in range(args.slots)))
    (s.data_dir / "energy-bots.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"{len(rows)} episodes -> {s.data_dir / 'energy-bots.jsonl'}")


if __name__ == "__main__":
    asyncio.run(main())
