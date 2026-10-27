"""Write a live snapshot of one running game for lab/panel/live.html.

Reads only the worker's own transcript (official tool replies) every few seconds and
writes lab/panel/live/game.json: stats after every decision, promotions, review grades
and the latest decisions with the worker's notes. Stops after the game has ended.

    uv run python scripts/panel/live.py ~/careerlab-data/huawei-leah/runs/<job_id>
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from careerlab.digest import GRADE, calls

OUT = Path(__file__).resolve().parents[2] / "lab" / "panel" / "live" / "game.json"
STATS = ("health", "dignity", "skill", "network", "output", "wealth")


def snapshot(run: Path) -> dict:
    points, decisions, grades, promotions = [], [], [], []
    obs, level = None, None
    for tool, args, reply in calls(run):
        if tool.endswith("observe"):
            try:
                obs = json.loads(reply)
            except ValueError:
                continue
            st = obs.get("current_state") or {}
            status, month = st.get("status") or {}, (st.get("time") or {}).get("current_month")
            if not status or month is None:
                continue
            if level and status.get("level") != level:
                promotions.append({"month": month, "level": status["level"]})
            level = status.get("level", level)
            points.append({"i": len(points), "month": month, "level": level, **{k: status.get(k) for k in STATS}})
            for g in GRADE.findall(obs.get("events") or ""):
                if not grades or grades[-1]["month"] != month:
                    grades.append({"month": month, "grade": g})
        elif tool.endswith("take_action") and obs:
            ev = obs.get("current_event") or {}
            chosen = next((c for c in obs.get("choices", []) if c.get("choice") == args.get("choice")), {})
            title = ev.get("title", "")
            kind = "energy" if title.startswith("Quarterly energy") else "main" if title.startswith("Quarterly main") else "story"
            decisions.append({"month": (obs.get("current_state") or {}).get("time", {}).get("current_month"), "kind": kind,
                              "action": chosen.get("action", "?"), "notes": (args.get("notes") or "")[:240]})
    result = run / "result.json"
    ending = json.loads(result.read_text()) if result.exists() else None
    return {"job": run.name, "policy": json.loads((run / "actor.json").read_text()).get("model", "") if (run / "actor.json").exists() else "",
            "updated": time.time(), "points": points, "promotions": promotions, "grades": grades,
            "decisions": decisions[-12:], "n_decisions": len(decisions),
            "ending": {k: ending.get(k) for k in ("outcome", "quantitative_score", "survival_months", "failure_reason")} if ending else None}


def write(data: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(data))
    os.replace(tmp, OUT)


if __name__ == "__main__":
    run = Path(sys.argv[1]).expanduser()
    label = sys.argv[2] if len(sys.argv) > 2 else run.name
    while True:
        data = snapshot(run)
        data["label"] = label
        write(data)
        if data["ending"]:
            break
        time.sleep(4)
