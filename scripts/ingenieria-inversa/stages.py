"""Stage experiment: the oracle plays well everywhere except one half-year, where it decides at random
(story answers only, or quarterly actions only). The loss against the all-greedy arm measures how
much that stage and that kind of decision matter.

    python3 stages.py b02-stages
"""

from __future__ import annotations

import collections
import math
import statistics as st
import sys

from bbdata import IDX, Batch, grade_of, promotion_of


def mean_ci(xs: list[float]) -> tuple[float, float]:
    if len(xs) < 2:
        return (xs[0] if xs else float("nan"), float("nan"))
    return st.mean(xs), 1.96 * st.stdev(xs) / math.sqrt(len(xs))


def main() -> None:
    b = Batch(*sys.argv[1].split(","))
    arms: dict[int, dict] = {}
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    for g in b.games():
        if g["outcome"] == "interrupted":
            continue
        a = g["par"].get("arm", 0)
        arms[a] = g["par"]
        d = data[a]
        e = g["end"]
        d["q"].append(e["q"])
        d["done"].append(1.0 if e["done"] else 0.0)
        d["level"].append(g["final"]["s"][IDX["level"]])
        promos = collections.Counter()
        k = 0
        fail = ""
        for c, m in b.log_entries(g):
            if grade_of(m):
                k += 1
            if promotion_of(m):
                promos[k] += 1
            if c == "X":
                fail = m.split("—")[0].strip()[:20]
        d["fail"].append(fail)
        d["promo_by12"].append(1.0 if sum(v for kk, v in promos.items() if kk <= 2) >= 2 else 0.0)
        d["promo_r1"].append(1.0 if promos.get(1) else 0.0)
        for name in ("wealth", "skill", "network", "output"):
            d[name].append(g["final"]["s"][IDX[name]])
    base_q = data[0]["q"]
    print(f"{'arm':>3} {'kind':8} {'months':>7} {'n':>4} {'mean Q':>13} {'dQ vs base':>10} {'done':>5} {'L':>5} {'L2@m6':>6} {'L3@m12':>6}  failures")
    for a in sorted(data):
        d = data[a]
        p = arms[a]
        kind = p.get("explore_kind", "none")
        months = f"{p.get('explore_from')}-{p.get('explore_to')}" if kind != "none" else "-"
        q, ci = mean_ci(d["q"])
        dq = q - st.mean(base_q)
        fails = collections.Counter(f for f in d["fail"] if f)
        print(f"{a:>3} {kind:8} {months:>7} {len(d['q']):>4} {q:7.1f}±{ci:4.1f} {dq:+10.1f} {st.mean(d['done']):5.0%} "
              f"{st.mean(d['level']):5.2f} {st.mean(d['promo_r1']):6.0%} {st.mean(d['promo_by12']):6.0%}  {dict(fails.most_common(3))}")


if __name__ == "__main__":
    main()
