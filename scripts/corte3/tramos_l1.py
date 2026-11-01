"""Resumen de tramos fieles hasta salir de L1: por brazo, cuántos ascienden y en qué mes, cuántos mueren
(salud, ruina, crisis) y cuántos siguen en L1 al parar; coste. Uso:
    python3 scripts/corte3/tramos_l1.py ~/careerlab-data/tramos/c3r1
"""
import collections
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).expanduser() / "segments"
rows = collections.defaultdict(list)
for f in sorted(root.glob("*.json")):
    if f.name.endswith(".messages.json"):
        continue
    d = json.loads(f.read_text())
    fin = d.get("final") or {}
    st = fin.get("status") or {}
    m = (fin.get("time") or {}).get("current_month")
    reason = ((fin.get("simulation_flags") or {}).get("failure_reason") or "").split(" ")[0]
    if d["stop"] == "promoted":
        out = f"asc{m}"
    elif d["stop"] == "game_over":
        out = "muere:" + reason.strip("—")
    else:
        out = f"{d['stop']}@{m}"
    rows[d["arm"]].append((out, round(d.get("cost") or 0, 3), st.get("health")))
for arm, rs in rows.items():
    c = collections.Counter(o for o, _, _ in rs)
    exit12 = sum(1 for o, _, _ in rs if o in ("asc6", "asc12"))
    exit18 = exit12 + c.get("asc18", 0)
    cost = sum(x for _, x, _ in rs)
    print(f"{arm:8} n={len(rs):2}  sale de L1 antes del 12: {exit12:2}  antes del 18: {exit18:2}  {dict(c)}  coste {cost:.2f} USD")
