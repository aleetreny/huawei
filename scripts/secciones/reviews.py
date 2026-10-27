"""Per-review table (T18): for each arm and review k, how many reached it, were promoted, held the floor, and which input was short.

    uv run python scripts/secciones/reviews.py --batch full-base
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from periods import FLOORS, at_floor, rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch")
    ap.add_argument("--purpose")
    a = ap.parse_args()
    by = defaultdict(lambda: defaultdict(Counter))
    levels = defaultdict(lambda: defaultdict(list))
    for r in rows(a.purpose, None, a.batch):
        p = r["periods"] or {}
        for rev in p.get("reviews") or []:
            c = by[r["policy"]][rev["review"]]
            c["reached"] += 1
            lv = (rev.get("before") or {}).get("level")
            c[f"from_L{lv}"] += 1
            c["promoted"] += rev["promoted"]
            c["floor"] += at_floor(rev)
            c[f"grade_{rev.get('grade')}"] += 1
            if not rev["promoted"] and lv in FLOORS:
                snap = rev["after"]
                short = [k[0].upper() for k, f in zip(("skill", "network", "output"), FLOORS[lv]) if (snap.get(k) or 0) < f]
                c["short_" + ("".join(short) or "none")] += 1
            levels[r["policy"]][rev["month"]].append((rev.get("after") or {}).get("level"))
    for pol, revs in sorted(by.items()):
        print(f"## {pol}")
        for k in sorted(revs):
            c = revs[k]
            lv = levels[pol][6 * k]
            extra = " ".join(f"{key}={v}" for key, v in sorted(c.items()) if key.startswith(("from_", "short_", "grade_")))
            print(f"R{k} (m{6*k}): reached {c['reached']}, promoted {c['promoted']}, at floor {c['floor']}, mean level after {sum(lv)/len(lv):.2f} | {extra}")


if __name__ == "__main__":
    main()
