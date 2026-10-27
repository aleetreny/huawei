"""One row per half-year review: the state just before it is applied, and what it decided.

The review of month 6k is applied when the clock moves from 6k-1 to 6k, before that month's
events and quarter-end allocation. The state just before it is the state before the last
decision of month 6k-1 plus that decision's logged effect, clipped to the current level's
ceilings (ceilings from the model's clamp estimates).
"""

from __future__ import annotations

import collections
import csv
import json
import sys
from pathlib import Path
from typing import Any

from bbdata import IDX, Batch, grade_of, parse_choice_entry, promotion_of
from model import aligned, risk_level

FLOORS = {"skill": 1, "network": 0, "output": -1, "health": 0, "dignity": 0}


def pre_review_state(pairs, steps, month: int, caps: dict[int, dict[str, int]]) -> dict[str, float] | None:
    last = [(s, e) for s, e in pairs if s[0] == month - 1]
    if not last:
        return None
    s, e = last[-1]
    lv = s[4][IDX["level"]]
    out = {"level": lv, "wealth": s[4][IDX["wealth"]] + e["d"].get("wealth", 0), "dur": s[4][IDX["duration_in_level"]]}
    for k in ("skill", "network", "output", "health", "dignity"):
        v = s[4][IDX[k]] + e["d"].get(k, 0)
        hi = caps.get(lv, {}).get(k, 10 if k in ("health", "dignity") else 10**9)
        out[k] = max(FLOORS[k], min(hi, v))
    return out


def rows_for_game(b: Batch, g: dict[str, Any], caps) -> list[dict[str, Any]]:
    pairs = aligned(b, g)
    if pairs is None:
        return []
    steps = g["steps"]
    logs = b.log_entries(g)
    grades = [grade_of(m) for c, m in logs if c == "P" and grade_of(m)]
    talks = [m for c, m in logs if c == "T"]
    promos = [promotion_of(m) for c, m in logs if c == "R" and promotion_of(m)]
    fail = next((m for c, m in logs if c == "X"), "")
    hr: dict[int, int] = {}
    blow_months = []
    for s in steps:
        if s[5]:
            t = b.texts.get(s[5], "")
            lv = risk_level(t)
            if lv is not None and s[0] not in hr:
                hr[s[0]] = lv
            if "Old landmines" in t:
                blow_months.append(s[0])
    first_step_month = {}
    for s in steps:
        first_step_month.setdefault(s[0], s)
    rows = []
    last_month = g["final"]["t"] if g.get("final") else 0
    prev_grades: list[str] = []
    for k, month in enumerate(range(6, 49, 6)):
        if month > last_month:
            break
        pre = pre_review_state(pairs, steps, month, caps)
        nxt = first_step_month.get(month)
        if pre is None:
            break
        after_level = nxt[4][IDX["level"]] if nxt else (g["final"]["s"][IDX["level"]])
        grade = grades[k] if k < len(grades) else None
        row = {"game": g["g"], "pol": g["pol"], "k": k + 1, "month": month, **{f"pre_{x}": v for x, v in pre.items()},
               "promoted": int(after_level > pre["level"]), "grade": grade,
               "prev_grades": "".join(prev_grades), "talk": (talks[k][-160:] if k < len(talks) else ""),
               "hr_prev": hr.get(month - 1), "hr_now": hr.get(month), "blowups_before": sum(1 for m in blow_months if m < month),
               "blowup_at": int(month in blow_months), "ended_here": int(not nxt),
               "fail": fail[:60] if not nxt else ""}
        rows.append(row)
        if grade:
            prev_grades.append(grade)
    return rows


def main() -> None:
    batches = sys.argv[1].split(",")
    out = Path(sys.argv[2]).expanduser()
    model = json.loads(Path(sys.argv[3]).expanduser().read_text())
    caps = {int(k): v for k, v in model["ceil"].items()}
    b = Batch(*batches)
    n = 0
    with out.open("w", newline="") as f:
        w = None
        for g in b.games():
            for row in rows_for_game(b, g, caps):
                if w is None:
                    w = csv.DictWriter(f, fieldnames=list(row))
                    w.writeheader()
                w.writerow(row)
                n += 1
    print(json.dumps({"rows": n, "out": str(out)}))


if __name__ == "__main__":
    main()
