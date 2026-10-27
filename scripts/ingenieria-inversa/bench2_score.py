"""Score the context benchmark: each question carries one context (neutral, the month before a
review with every growth input exactly at the bar, or built-up risk), and the value of an answer
depends on it:
- neutral: growth inputs count fully, Health/Dignity/Wealth partly, blow-up excess penalised;
- pre_review: any point of Skill, Network or Output lost costs heavily (gains cannot register);
- risk_high: as neutral, plus the measured chance that the answer sets off the built-up risk.

    python3 bench2_score.py <bench2 dir> <bench2-key.json> B C
"""

from __future__ import annotations

import collections
import json
import statistics as st
import sys
from pathlib import Path

GROWTH = ("skill", "network", "output")


def value(e: dict, ctx: str) -> float:
    m = e["mean"]
    blow = e.get("blow3", 0) or 0
    soft = 0.4 * m.get("health", 0) + 0.4 * m.get("dignity", 0) + 0.3 * m.get("wealth", 0)
    if ctx == "pre_review":
        return -10 * sum(max(0.0, -m.get(s, 0)) for s in GROWTH) + soft - 25 * blow
    v = sum(m.get(s, 0) for s in GROWTH) + soft - 25 * blow
    if ctx == "risk_high":
        v -= 30 * (e.get("det_hi") or 0)
    return v


def main() -> None:
    root = Path(sys.argv[1])
    key = json.loads(Path(sys.argv[2]).expanduser().read_text())
    print(f"{'variant':8s} {'context':11s} {'n':>3s} {'best%':>6s} {'value':>7s} {'loses SNO%':>10s} {'detonator%':>10s} {'risky%':>7s}")
    for variant in ["random"] + sys.argv[3:]:
        if variant != "random":
            path = root / variant / "choices.json"
            if not path.exists():
                print(f"{variant}: no choices yet")
                continue
            choices = json.loads(path.read_text())
        agg = collections.defaultdict(lambda: collections.defaultdict(list))
        for qid, q in key.items():
            ctx, effs = q["ctx"], q["effects"]
            vals = {k: value(e, ctx) for k, e in effs.items()}
            picks = list(effs) if variant == "random" else [str(choices.get(qid, ""))]
            for k in picks:
                if k not in effs:
                    continue
                e = effs[k]
                w = 1 / len(picks)
                a = agg[ctx]
                a["best"].append((1.0 if vals[k] == max(vals.values()) else 0.0, w))
                a["value"].append((vals[k], w))
                a["loses"].append((1.0 if any(e["mean"].get(s, 0) < 0 for s in GROWTH) else 0.0, w))
                a["det"].append((1.0 if (e.get("det_hi") or 0) >= 0.3 else 0.0, w))
                a["risky"].append((1.0 if (e.get("blow3") or 0) >= 0.10 else 0.0, w))
        for ctx in ("neutral", "pre_review", "risk_high"):
            a = agg[ctx]
            if not a:
                continue
            f = lambda name: sum(x * w for x, w in a[name]) / sum(w for _, w in a[name])
            n = round(sum(w for _, w in a["best"]))
            print(f"{variant:8s} {ctx:11s} {n:3d} {f('best'):6.0%} {f('value'):7.2f} {f('loses'):10.0%} {f('det'):10.0%} {f('risky'):7.0%}")


if __name__ == "__main__":
    main()
