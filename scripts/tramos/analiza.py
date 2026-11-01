"""Summary of the faithful segments (``fiel.py``) next to the real runs of the same manuals.

Per arm: first promotion at month 6 (with a Wilson 95 % interval), what was short at the review, how the agent
used the turns (calls per decision, take_action + observe pairs, visible text, hidden reasoning, continuations,
skill reads), providers and cost. The real runs come from ``lab/data/deepseek/decisiones.csv.gz``.

    uv run python scripts/tramos/analiza.py --data ~/careerlab-data/tramos/r2-fiel
    uv run python scripts/tramos/analiza.py --data lab/data/deepseek/tramos/r2-fiel     # the copy in Git
"""

from __future__ import annotations

import argparse
import collections
import csv
import gzip
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REAL = {"v4": ("t13-read-v2", "t13-read-v3", "t13-read-v4", "t13-read-v5", "t13-read-v7"), "v4loop": ("v4-loop",),
        "mv5r": ("mv-5r",), "mv4": ("mv-4",)}


def wilson(k: int, n: int) -> tuple[float, float]:
    if not n:
        return 0.0, 0.0
    z, p = 1.96, k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, c - h), min(1.0, c + h)


def real_rates() -> dict[str, tuple[int, int]]:
    rows = list(csv.DictReader(gzip.open(REPO / "lab/data/deepseek/decisiones.csv.gz", "rt")))
    by: dict[str, dict[int, str]] = collections.defaultdict(dict)
    man: dict[str, str] = {}
    for r in rows:
        try:
            by[r["partida"]].setdefault(int(r["mes"]), r["nivel"])
        except ValueError:
            continue
        man[r["partida"]] = r["manual"]
    out = {}
    for arm, manuals in REAL.items():
        games = [lv for p, lv in by.items() if man[p] in manuals and max(lv) >= 6]
        out[arm] = (sum(1 for lv in games if lv.get(6, "L1") != "L1"), len(games))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(Path.home() / "careerlab-data" / "tramos"))
    a = ap.parse_args()
    root = Path(a.data).expanduser()
    root = root / "segments" if (root / "segments").is_dir() else root  # local batch, or an exported copy in Git
    segs = [json.loads(gzip.open(p, "rt").read() if p.suffix == ".gz" else p.read_text())
            for p in sorted(root.glob("*.json*")) if "messages" not in p.name and not p.name.startswith("calls")]
    real = real_rates()
    by = collections.defaultdict(list)
    for s in segs:
        by[s["arm"]].append(s)
    for arm, rs in sorted(by.items()):
        n = len(rs)
        k = sum(1 for r in rs if r["stop"] == "promoted")
        lo, hi = wilson(k, n)
        rk, rn = real.get(arm, (0, 0))
        print(f"\n== {arm}: promoted at the month-6 review {k}/{n} = {k / n:.0%} (95 % {lo:.0%}–{hi:.0%}); "
              f"real runs {rk}/{rn}")
        print("   stops:", dict(collections.Counter(r["stop"] for r in rs)))
        short = collections.Counter()
        for r in rs:
            if r["stop"] != "promoted":
                m5 = [d for d in r["decisions"] if d["month"] == 5]
                st = (r["final"] or {}).get("status") or {}
                last = m5[-1]["status"] if m5 else {}
                short[f"m6 S{st.get('skill')} N{st.get('network')} O{st.get('output')} D{st.get('dignity')}"
                      f" (m5 before last: N{last.get('network')} O{last.get('output')})"] += 1
        for key, c in short.most_common():
            print(f"   not promoted: {key} x{c}")
        calls = [c for r in rs for c in r["calls"]]
        dec = sum(len(r["decisions"]) for r in rs)
        pairs = sum(1 for c in calls if c["n_tools"] >= 2)
        prov = collections.Counter(c["provider"] for c in calls)
        print(f"   calls/segment {len(calls) / n:.1f}, decisions/segment {dec / n:.1f}, calls/decision {len(calls) / max(dec, 1):.2f}, "
              f"replies with 2+ tool calls {pairs / len(calls):.0%}")
        print(f"   visible text/call {sum(c['text'] for c in calls) / len(calls):.0f} chars, hidden reasoning/call "
              f"{sum(c['reasoning'] or 0 for c in calls) / len(calls):.0f} tokens, continuations {sum(r['continuations'] for r in rs)}, "
              f"odd tools {sum(len(r['odd_tools']) for r in rs)}, skill reads after month 1: "
              f"{sum(1 for r in rs for m in r['skill_reads'] if m > 1)}")
        print(f"   providers {dict(prov.most_common(6))}")
        notes = [len(d["notes"]) for r in rs for d in r["decisions"]]
        print(f"   note length median {sorted(notes)[len(notes) // 2] if notes else 0} (cut at 300), cost {sum(r['cost'] for r in rs):.3f} USD "
              f"({sum(r['cost'] for r in rs) / n:.4f}/segment), minutes/segment {sum(r['seconds'] for r in rs) / n / 60:.1f}")


if __name__ == "__main__":
    main()
