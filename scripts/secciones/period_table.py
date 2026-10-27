"""Per-period table from full games of one batch (T18).

P1: promoted at the first review; P2: level after the review of month 18; P3: level after the review
of month 36; P4: completed share, final level and Q (mean ± SE), ending dimensions of completed games.
Games that ended before a review month keep the level they had (an elimination counts as stuck).

    uv run python scripts/secciones/period_table.py --batch final-periodos-v1
"""
from __future__ import annotations

import argparse
import math
import statistics as st
from collections import defaultdict

from periods import rows


def ms(xs: list[float]) -> str:
    xs = [x for x in xs if x is not None]
    if not xs:
        return "–"
    if len(xs) == 1:
        return f"{xs[0]:.1f}"
    return f"{st.mean(xs):.1f} ± {st.stdev(xs) / math.sqrt(len(xs)):.1f}"


def level_at(p: dict, month: int) -> int | None:
    revs = [r for r in (p.get("reviews") or []) if r["month"] <= month]
    if revs:
        return (revs[-1].get("after") or {}).get("level")
    fs = p.get("final_state") or {}
    return fs.get("level")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    a = ap.parse_args()
    by = defaultdict(list)
    for r in rows(None, None, a.batch):
        if r["outcome"] in ("completed", "eliminated") and r["periods"] and "reviews" in r["periods"]:
            by[r["policy"]].append(r)
    print("| Manual | Partidas | P1: ascienden en la 1.ª | P2: nivel en el mes 18 | P3: nivel en el mes 36 | P4: terminadas | Nivel final | Q media ± SE | Riesgo · Salud+Dig. · Red · Skill · Dinero (terminadas) |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for pol, g in sorted(by.items()):
        n = len(g)
        r1 = sum(1 for x in g if any(rv["review"] == 1 and rv["promoted"] for rv in x["periods"]["reviews"]))
        l18 = [level_at(x["periods"], 18) for x in g]
        l36 = [level_at(x["periods"], 36) for x in g]
        fin = [(x["periods"].get("final_state") or {}).get("level") for x in g]
        done = [x for x in g if x["outcome"] == "completed"]
        dims = lambda k: ms([(x["dims"] or {}).get(k) for x in done])
        print(f"| {pol} | {n} | {r1}/{n} = {100 * r1 / n:.0f} % | {ms(l18)} | {ms(l36)} | {len(done)}/{n} | {ms(fin)} | {ms([x['score'] for x in g])} | "
              f"{dims('risk_control')} · {dims('resilience')} · {dims('network')} · {dims('skill')} · {dims('wealth')} |")
    for pol, g in sorted(by.items()):
        fails = [x["failure"][:25] for x in g if x["outcome"] == "eliminated" and x["failure"]]
        print(f"- {pol}: eliminaciones {len(fails)}: {', '.join(sorted(fails))}")


if __name__ == "__main__":
    main()
