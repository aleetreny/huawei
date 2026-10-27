"""Stage analysis: what to pursue at each point of the career (question 3).

Uses the analysis dir written by analyse.py (decisions.jsonl, episodes.json):
  1. visible ceilings per level (highest Skill/Network/Output seen at each level);
  2. every half-year review: state just before it, grade, promotion; promotion rate by
     how many of Skill/Network/Output sit at the level's ceiling, and by Dignity/HR risk;
  3. value of the state: final competition score regressed on standardised state at
     checkpoints (months 5, 11, 17, 23, 29, 35, 41), so the weights say which visible
     variable matters most at each stage.

    python3 scripts/question-bank/stages.py <analysis dir>
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

d = Path(sys.argv[1])
eps = json.load(open(d / "episodes.json"))
by_ep = defaultdict(list)
for line in open(d / "decisions.jsonl"):
    x = json.loads(line)
    by_ep[x["ep"]].append(x)
S = ["health", "dignity", "skill", "network", "output", "wealth"]
out = {}

# 1. ceilings per level
seen = defaultdict(lambda: defaultdict(int))
for rows in by_ep.values():
    for x in rows:
        st = x["state"]
        L = st[7]
        for i, k in ((2, "skill"), (3, "network"), (4, "output")):
            seen[L][k] = max(seen[L][k], st[i])
# robust ceiling: 99th percentile of values seen at that level
vals = defaultdict(lambda: defaultdict(list))
for rows in by_ep.values():
    for x in rows:
        st = x["state"]
        for i, k in ((2, "skill"), (3, "network"), (4, "output")):
            vals[st[7]][k].append(st[i])
ceil = {L: {k: int(np.percentile(v, 99.5)) for k, v in ks.items()} for L, ks in vals.items()}
out["ceilings"] = {str(L): {**ceil[L], "max": dict(seen[L]), "n": len(vals[L]["skill"])} for L in sorted(ceil)}
print("ceilings", json.dumps(out["ceilings"]))

# 2. reviews
recs = []
for e_i, rows in by_ep.items():
    ep = eps[e_i]
    promos = set(ep["promotions"])
    for k, (m, grade) in enumerate(ep["reviews"]):
        prev = [x for x in rows if x["m"] < m]
        if not prev:
            continue
        st = prev[-1]["state"]  # before the last decision of the previous month; "after" already carries the review
        L = st[7]
        c = ceil.get(L, {})
        at = [st[2] >= c.get("skill", 99), st[3] >= c.get("network", 99), st[4] >= c.get("output", 99)]
        hr = next((x["hr_now"] for x in reversed(prev) if x["hr_now"] is not None), None)
        recs.append({"review": k + 1, "m": m, "level": L, "grade": grade, "promoted": int(m in promos),
                     "at_ceiling": sum(at), "at": at, "state": st, "hr": hr, "Y": ep["Y"]})
out["reviews"] = recs
tab = defaultdict(lambda: [0, 0])
for r in recs:
    t = tab[(r["level"], r["at_ceiling"])]
    t[0] += 1
    t[1] += r["promoted"]
print("\npromotion rate by level and number of S/N/O at ceiling (n, promoted)")
for key in sorted(tab):
    n, p = tab[key]
    print(f"  L{key[0]} at={key[1]}: {n:5d}  {p/n:5.2f}")
full = [r for r in recs if r["at_ceiling"] == 3]
for lab, f in (("dignity<=2", lambda r: r["state"][1] <= 2), ("hr>=2", lambda r: (r["hr"] or 0) >= 2),
               ("health<=3", lambda r: r["state"][0] <= 3)):
    a = [r["promoted"] for r in full if f(r)]
    b = [r["promoted"] for r in full if not f(r)]
    if a and b:
        print(f"  at full ceiling, {lab}: {np.mean(a):.2f} (n={len(a)}) vs not {np.mean(b):.2f} (n={len(b)})")
gr = defaultdict(lambda: [0, 0])
for r in recs:
    gr[r["grade"]][0] += 1
    gr[r["grade"]][1] += r["promoted"]
print("  promotion by grade", {g: (n, round(p / n, 2)) for g, (n, p) in gr.items()})

# 3. value of state at checkpoints
print("\nfinal score vs state at checkpoint (standardised weights; alive at checkpoint)")
out["value"] = {}
for cp in (5, 11, 17, 23, 29, 35, 41):
    X, Y = [], []
    for e_i, rows in by_ep.items():
        prev = [x for x in rows if x["m"] <= cp]
        if not prev or prev[-1]["m"] != cp:
            continue
        st = prev[-1]["after"]
        hr = next((x["hr_now"] for x in reversed(prev) if x["hr_now"] is not None), 0)
        X.append([st[0], st[1], st[2], st[3], st[4], st[5], st[7], hr])
        Y.append(eps[e_i]["Y"] or 0)
    if len(X) < 100:
        continue
    X, Y = np.array(X, float), np.array(Y, float)
    sd = X.std(0)
    sd[sd == 0] = 1
    Z = (X - X.mean(0)) / sd
    A = np.c_[np.ones(len(Z)), Z]
    b, *_ = np.linalg.lstsq(A, Y, rcond=None)
    r2 = 1 - np.var(Y - A @ b) / np.var(Y)
    names = ["health", "dignity", "skill", "network", "output", "wealth", "level", "hr_risk"]
    w = dict(zip(names, np.round(b[1:], 2).tolist()))
    out["value"][cp] = {"n": len(X), "r2": round(float(r2), 3), "w": w, "meanY": round(float(Y.mean()), 1)}
    print(f"  m{cp:2d} n={len(X):5d} R2={r2:.2f} meanY={Y.mean():.1f} ", w)
(d / "stages.json").write_text(json.dumps(out))
