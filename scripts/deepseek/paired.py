"""Paired comparison of two bank arms on the items both answered: per rule, the difference in right answers
and in regret (final-score points), with a bootstrap 95 % interval over items.

    uv run python scripts/deepseek/paired.py --a ds-control --b ds-t13-final [--phase e]
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts" / "transmision"))
from ds import DATA  # noqa: E402

os.environ["TRANSMISION_DATA"] = str(DATA)
from score import RULES, arm_results, decisive, load_items, right_set  # noqa: E402


def boot(xs: list[float], n: int = 4000) -> tuple[float, float]:
    rng = random.Random(1)
    means = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--phase", choices=("e", "q", "m"))
    a = ap.parse_args()
    items = load_items(DATA / "items.jsonl")
    ra, rb = arm_results(a.a), arm_results(a.b)
    common = [i for i in set(ra) & set(rb) if i in items and items[i]["rule"]]
    print(f"| rule | n | right {a.a} → {a.b} | Δ right (95 %) | regret {a.a} → {a.b} | Δ regret (95 %) | same choice |")
    print("|---|---:|---|---|---|---|---:|")
    rows = {r: [] for r in RULES}
    for i in common:
        it = items[i]
        if a.phase and it["phase"] != a.phase:
            continue
        rule = it["rule"]
        if not decisive(it, rule):
            continue
        q = {int(k): v for k, v in it["q"].items()}
        ka, kb = ra[i].get("choice"), rb[i].get("choice")
        if ka not in q or kb not in q:
            continue
        ok = right_set(it, rule)
        rows[rule].append((int(ka in ok), int(kb in ok), max(q.values()) - q[ka], max(q.values()) - q[kb], int(ka == kb)))
    allrows = []
    for rule, xs in rows.items():
        if not xs:
            continue
        allrows += xs
        _print(rule, xs)
    _print("all", allrows)


def _print(rule: str, xs: list[tuple]) -> None:
    n = len(xs)
    dr = [b - a for a, b, *_ in xs]
    dg = [rb - ra for _, _, ra, rb, _ in xs]
    lo, hi = boot(dr)
    glo, ghi = boot(dg)
    print(f"| {rule} | {n} | {100 * sum(x[0] for x in xs) / n:.0f} % → {100 * sum(x[1] for x in xs) / n:.0f} % | "
          f"{100 * sum(dr) / n:+.0f} ({100 * lo:+.0f} a {100 * hi:+.0f}) | {sum(x[2] for x in xs) / n:.2f} → "
          f"{sum(x[3] for x in xs) / n:.2f} | {sum(dg) / n:+.2f} ({glo:+.2f} a {ghi:+.2f}) | {100 * sum(x[4] for x in xs) / n:.0f} % |")


if __name__ == "__main__":
    main()
