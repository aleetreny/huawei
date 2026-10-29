"""Ajusta el modelo de elección por subconjunto de manuales (v4 frente a cp) y lo guarda para dssim."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import choice_model as CM
import numpy as np

SUBS = {"v4fam": {"t13-read-v2", "t13-read-v3", "t13-read-v4", "t13-read-v5", "t13-read-v7"},
        "cpfam": {"cp-v3", "cp-v5a", "cp-v7", "cp-v8", "cp-v10", "cp-v11", "cp-v12"},
        "v4only": {"t13-read-v4"}}
names = CM.SETS["both+ctx"]
for nm, s in SUBS.items():
    data = CM.load(s)
    b, f, cols = CM.fit(data, names)
    ll, acc = CM.evaluate(b, cols, data)
    print(nm, len(data), f"ll {ll:.3f} acc {acc:.3f}")
    json.dump({"names": names, "beta": b.tolist()}, open(CM.ROOT / f"lab/data/exploracion/choice_beta_{nm}.json", "w"), indent=1)
# cross-prediction: does the v4 model predict cp decisions as well as the cp model?
dv4 = CM.load(SUBS["v4fam"]); dcp = CM.load(SUBS["cpfam"])
b4, _, cols = CM.fit(dv4, names); bcp, _, _ = CM.fit(dcp, names)
print("cp decisions: own", CM.evaluate(bcp, cols, dcp), "v4 model", CM.evaluate(b4, cols, dcp))
print("v4 decisions: own", CM.evaluate(b4, cols, dv4), "cp model", CM.evaluate(bcp, cols, dv4))
for n, x, y in zip(names, b4, bcp):
    print(f"  {n:12s} v4 {x:+.2f}  cp {y:+.2f}")
