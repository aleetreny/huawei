"""Por brazo: decisiones de historia de los meses 4–5 en L1 que bajan Network u Output (diferencia de estado con la
siguiente decisión del tramo) y estado de RR. HH. al llegar a la primera evaluación. Uso:
    python3 scripts/corte3/tramos_ventana.py ~/careerlab-data/tramos/c3r1 [~/careerlab-data/tramos/c3r2 ...]
"""
import collections
import json
import sys
from pathlib import Path

acc = collections.defaultdict(collections.Counter)
for root in sys.argv[1:]:
    for f in sorted((Path(root).expanduser() / "segments").glob("*.json")):
        if f.name.endswith(".messages.json"):
            continue
        d = json.loads(f.read_text())
        ds = d["decisions"]
        a = acc[d["arm"]]
        a["tramos"] += 1
        for x, y in zip(ds, ds[1:]):
            if x["month"] in (4, 5) and x["phase"] == "event" and x["status"].get("level") == "L1":
                a["decisiones"] += 1
                dn = y["status"].get("network", 0) - x["status"].get("network", 0)
                do = y["status"].get("output", 0) - x["status"].get("output", 0)
                a["bajan_N_u_O"] += (dn < 0 or do < 0)
for arm, a in sorted(acc.items()):
    print(f"{arm:8} tramos {a['tramos']:2}  decisiones meses 4-5 {a['decisiones']:3}  bajan N/O {a['bajan_N_u_O']:3} "
          f"({a['bajan_N_u_O'] / max(1, a['decisiones']):.0%})")
