"""Batch overview: outcomes, failure reasons, levels, grades, promotion timing and score parts.

    python3 summary.py b01-oracle-eps10
"""

from __future__ import annotations

import collections
import statistics as st
import sys

from bbdata import IDX, Batch, grade_of, promotion_of


def main() -> None:
    b = Batch(*sys.argv[1].split(","))
    out = collections.Counter()
    fails = collections.Counter()
    lv = collections.Counter()
    q_by_lv = collections.defaultdict(list)
    grades_by_k = collections.defaultdict(collections.Counter)
    promo_month = collections.defaultdict(collections.Counter)
    dims = collections.defaultdict(list)
    qs, months = [], []
    for g in b.games():
        out[g["outcome"]] += 1
        if g["outcome"] == "interrupted":
            continue
        e = g["end"]
        qs.append(e["q"])
        months.append(e["months"])
        L = g["final"]["s"][IDX["level"]]
        lv[L] += 1
        q_by_lv[L].append(e["q"])
        if e["done"]:
            for name, (raw, norm, w) in e["dims"].items():
                dims[name].append((raw, norm))
        k = 0
        for c, m in b.log_entries(g):
            if c == "X":
                fails[m.split("—")[0].split(".")[0][:40]] += 1
            gr = grade_of(m)
            if gr:
                k += 1
                grades_by_k[k][gr] += 1
            pr = promotion_of(m)
            if pr:
                promo_month[pr][k] += 1
    n = sum(out.values())
    print(f"games {n}  outcomes {dict(out)}")
    if qs:
        print(f"mean Q {st.mean(qs):.1f}  median Q {st.median(qs):.1f}  max Q {max(qs):.1f}  mean months {st.mean(months):.1f}")
    print("failures:", fails.most_common())
    print("final level:", {k: f"{v} (Q {st.mean(q_by_lv[k]):.1f})" for k, v in sorted(lv.items())})
    print("grades by review number:")
    for k in sorted(grades_by_k):
        c = grades_by_k[k]
        tot = sum(c.values())
        print(f"  review {k} (month {6*k}): n={tot}  " + "  ".join(f"{g}:{c[g]/tot:.0%}" for g in "SABCD" if c[g]))
    print("promotions (from->to): at which review number")
    for pr in sorted(promo_month):
        c = promo_month[pr]
        print(f"  L{pr[0]}->L{pr[1]}: {sum(c.values())}  by review: {dict(sorted(c.items()))}")
    if dims:
        print("completed games, mean raw / normalised per dimension:")
        for name, v in dims.items():
            print(f"  {name:13s} raw {st.mean(r for r, _ in v):7.2f}   norm {st.mean(x for _, x in v):6.2f}")


if __name__ == "__main__":
    main()
