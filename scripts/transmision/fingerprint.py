"""Behavioural fingerprint of an arm (T20): mean effect of the chosen story options, against the control.

    uv run python scripts/transmision/fingerprint.py --items items-gen.jsonl --arms control,f3lean,... [--months 1-5]

A rule can win its own situations and still shift every other choice (for example away from options
that teach). The mean announced change of Skill, Network, Output, Health, Dignity, Wealth and hidden
risk of the chosen options, on the same items for every arm, shows such a shift.
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import arm_results  # noqa: E402

KEYS = ("skill", "network", "output", "health", "dignity", "wealth")
ap = argparse.ArgumentParser()
ap.add_argument("--items", required=True)
ap.add_argument("--arms", required=True)
ap.add_argument("--months", default="1-44")
a = ap.parse_args()
lo, hi = map(int, a.months.split("-"))
items = {}
for line in open(a.items):
    it = json.loads(line)
    if it["phase"] == "e" and lo <= it["month"] <= hi:
        items[it["id"]] = it
arms = a.arms.split(",")
res = {arm: arm_results(arm) for arm in arms}
common = set(items).intersection(*(set(r) for r in res.values()))
print(f"{len(common)} story items, months {a.months}")
print("| arm | " + " | ".join(KEYS) + " | risk | same choice as control % |")
print("|---|" + "---:|" * (len(KEYS) + 2))
for arm in arms:
    s = {k: 0.0 for k in KEYS + ("risk",)}
    same = 0
    for i in common:
        k = res[arm][i].get("choice")
        f = items[i]["fx"].get(str(k))
        if f is None:
            continue
        for kk in KEYS:
            s[kk] += f["d"].get(kk, 0)
        s["risk"] += f["dr"]
        same += int(res[arm][i].get("choice") == res[arms[0]][i].get("choice"))
    n = max(1, len(common))
    print(f"| {arm} | " + " | ".join(f"{s[k]/n:+.2f}" for k in KEYS) + f" | {s['risk']/n:+.2f} | {100*same/n:.0f} |")
