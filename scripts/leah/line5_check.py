"""Does the player follow line 5 of l6-routine-v1? Reads one game's transcript (official tool replies only).

Line 5 applies at L1-L3 when no earlier line matched: Energy in the order Health recovery, Mental recovery,
Prepare report materials; main action Apply for a key project; no Skill learning, Network maintenance or
High-intensity work. Quarters where an earlier line could have matched (low Health or Dignity, or an HR
remark other than the mild ones) are reported apart, since the earlier line wins there.

    uv run python scripts/leah/line5_check.py ~/careerlab-data/huawei-leah/runs/<job_id>
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from careerlab.digest import calls

ROUTINE = ["Health recovery", "Mental recovery", "Prepare report materials"]
BANNED = {"Skill learning", "Network maintenance", "High-intensity work"}


def quarters(run: Path) -> list[dict]:
    """One record per quarter: level, Health, Dignity, Energy actions in order, main action, the notes."""
    out, obs, cur = [], None, None
    for tool, args, reply in calls(run):
        if tool.endswith("observe"):
            try:
                obs = json.loads(reply)
            except ValueError:
                continue
            continue
        if not tool.endswith("take_action") or not obs:
            continue
        title = (obs.get("current_event") or {}).get("title", "")
        if not title.startswith(("Quarterly energy", "Quarterly main")):
            continue
        st = obs.get("current_state") or {}
        status, month = st.get("status") or {}, (st.get("time") or {}).get("current_month")
        chosen = next((c for c in obs.get("choices", []) if c.get("choice") == args.get("choice")), {})
        if cur is None or cur["month"] != month:
            cur = {"month": month, "level": status.get("level"), "health": status.get("health"),
                   "dignity": status.get("dignity"), "energy": [], "main": None, "notes": []}
            out.append(cur)
        if title.startswith("Quarterly energy"):
            cur["energy"].append(chosen.get("action", "?"))
        else:
            cur["main"] = chosen.get("action", "?")
        cur["notes"].append((args.get("notes") or "")[:120])
    return out


def level_num(level) -> int:
    try:
        return int(str(level).lstrip("L"))
    except ValueError:
        return 0


def main() -> None:
    run = Path(sys.argv[1]).expanduser()
    qs = [q for q in quarters(run) if 1 <= level_num(q["level"]) <= 3]
    energy = Counter(a for q in qs for a in q["energy"] if a != "Reserve energy")
    n_energy = sum(energy.values())
    key = sum(1 for q in qs if (q["main"] or "").startswith("Apply for a key project"))
    exact = sum(1 for q in qs if [a for a in q["energy"] if a != "Reserve energy"][:3] == ROUTINE)
    banned = sum(n for a, n in energy.items() if a in BANNED)
    print(f"L1-L3 quarters: {len(qs)}")
    print(f"main action key project: {key}/{len(qs)} ({100 * key / max(len(qs), 1):.0f}%)  prediction >= 90%, refuted below 70%")
    print(f"Energy exactly Health, Mental, Report in order: {exact}/{len(qs)}")
    print(f"Energy actions banned at L1-L3: {banned}/{n_energy} ({100 * banned / max(n_energy, 1):.0f}%)  Skill learning {energy.get('Skill learning', 0)} (prediction < 5%)")
    print("Energy mix:", dict(energy.most_common()))
    print("Main actions:", dict(Counter(q["main"] for q in qs).most_common()))
    print("\nmonth level H D | energy -> main | first note")
    for q in qs:
        print(f"{q['month']:>5} {q['level']} {q['health']} {q['dignity']} | {', '.join(q['energy'])} -> {q['main']} | {q['notes'][0] if q['notes'] else ''}")


if __name__ == "__main__":
    main()
