"""Check whether a Claude worker followed a manual: quarterly choices, Health, grades and promotions per game.

Reads only the worker's own transcript (official tool replies), like careerlab.digest.

    uv run python scripts/leah/behaviour.py ~/careerlab-data/huawei-leah/runs/leah-scre-*-a2
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from careerlab.digest import GRADE, calls


def game(run_dir: Path) -> dict:
    energy, main, grades = Counter(), Counter(), []
    levels, health_q, notes = [], [], []
    obs = None
    for tool, args, reply in calls(run_dir):
        if tool.endswith("observe"):
            try:
                obs = json.loads(reply)
            except ValueError:
                continue
            st = obs.get("current_state") or {}
            month, status = (st.get("time") or {}).get("current_month"), st.get("status") or {}
            if status.get("level") and (not levels or levels[-1][1] != status["level"]):
                levels.append((month, status["level"]))
            grades += [g for g in GRADE.findall(obs.get("events") or "") if not grades or (month, g) not in grades]
        elif tool.endswith("take_action") and obs:
            title = (obs.get("current_event") or {}).get("title", "")
            chosen = next((c for c in obs.get("choices", []) if c.get("choice") == args.get("choice")), {})
            label = chosen.get("action", "?")
            status = (obs.get("current_state") or {}).get("status") or {}
            if title.startswith("Quarterly energy"):
                energy[label.split(" (")[0]] += 1
            elif title.startswith("Quarterly main"):
                main[label] += 1
                health_q.append(status.get("health"))
            if args.get("notes") and len(notes) < 3:
                notes.append(args["notes"][:160])
    result = json.loads((run_dir / "result.json").read_text()) if (run_dir / "result.json").exists() else {}
    return {"job": run_dir.name, "outcome": result.get("outcome"), "score": result.get("quantitative_score"),
            "months": result.get("survival_months"), "promotions": levels[1:], "energy": dict(energy.most_common()),
            "main": dict(main.most_common()), "health_at_main_action": health_q, "sample_notes": notes,
            "cost_usd": (result.get("actor_usage") or {}).get("cost_usd_list_price")}


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(json.dumps(game(Path(path).expanduser()), ensure_ascii=False))
