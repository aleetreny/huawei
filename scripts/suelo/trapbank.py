"""Suelo: a bank of the situations where a game sinks (research only; items carry dev-game text and stay
under ~/careerlab-data/suelo, outside Git).

Reuses transmision/bank.py (extract: replay recorded bot games with the replica's hidden-state tracking;
truth: value every option with planner rollouts) with the floor line's own tags:
  l1_rescue   L1 after two reviews without promotion (months 13-17): story options that differ in
              hidden-risk sign, or quarterly choices (months 12 and 15)
  l1_prep     L1 in the month before a review (5 or 11): some option lowers Network or Output, some not
  all_risky   every option adds hidden risk, with different sizes
  after_blow  after a blow-up with HR not friendly: some option adds risk, some lowers it

    python3 scripts/suelo/trapbank.py extract      # -> $SUELO_DATA/sit.jsonl (slow: ~2,900 games)
    python3 scripts/suelo/trapbank.py truth --per-tag 45 --rollouts 48   # -> bank.jsonl
    python3 scripts/suelo/trapbank.py ids --out ids-suelo.txt           # item ids, stratified
Then runbench.py assemble / run (see lab/reports/suelo/README.md).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "transmision"))
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
os.environ.setdefault("BB_DATA", str(REPO / "lab" / "data" / "ingenieria-inversa"))
import bank as B  # noqa: E402
import replica as R  # noqa: E402

DATA = Path(os.environ.get("SUELO_DATA", Path.home() / "careerlab-data" / "suelo"))
BATCHES = "v03-validation,v02-validation,b01-oracle-eps,d01-planner2,c01-greedy-real,h01-l6hunt"


def trap_tags(cat: R.Catalog, sit: dict[str, Any], fx: dict[str, dict[str, Any]]) -> list[str]:
    st = sit["state"]
    lv, m, ph = st["level"], sit["month"], sit["phase"]
    out = []
    drs = [f["dr"] for f in fx.values()]
    if lv == 1 and 13 <= m <= 17 and ph == "e" and any(d > 0 for d in drs) and any(d <= 0 for d in drs):
        out.append("l1_rescue")
    if lv == 1 and m in (12, 15) and ph in ("q", "m"):
        out.append("l1_rescue")
    if lv == 1 and m in (5, 11) and ph == "e":
        for k in ("network", "output"):
            if any(f["d"].get(k, 0) < 0 for f in fx.values()) and any(f["d"].get(k, 0) >= 0 for f in fx.values()):
                out.append("l1_prep")
                break
    if ph == "e" and m < 45 and len(drs) > 1 and all(d > 0 for d in drs) and min(drs) < max(drs):
        out.append("all_risky")
    if ph == "e" and m < 45 and st.get("blowups", 0) >= 1 and st["risk"] >= 1 \
            and any(d > 0 for d in drs) and any(d <= 0 for d in drs):
        out.append("after_blow")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("extract")
    p.add_argument("--batches", default=BATCHES)
    p = sub.add_parser("truth")
    p.add_argument("--per-tag", type=int, default=45)
    p.add_argument("--rollouts", type=int, default=48)
    p.add_argument("--seed", type=int, default=28)
    p = sub.add_parser("ids")
    p.add_argument("--out", default=str(DATA / "ids-suelo.txt"))
    p.add_argument("--per-tag", type=int, default=45)
    a = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    if a.cmd == "extract":
        B.extract(a.batches.split(","), DATA / "sit.jsonl", None)
    elif a.cmd == "truth":
        B.tags = trap_tags
        B.truth(DATA / "sit.jsonl", DATA / "bank.jsonl", a.rollouts, a.per_tag, a.seed)
    else:
        import random
        by: dict[str, list[str]] = {}
        for line in (DATA / "bank.jsonl").open():
            it = json.loads(line)
            for t in it["tags"]:
                by.setdefault(t, []).append(it["id"])
        rng = random.Random(28)
        ids: list[str] = []
        for t, lst in sorted(by.items()):
            lst = sorted(set(lst))
            rng.shuffle(lst)
            ids.extend(lst[: a.per_tag])
            print(t, len(lst), file=sys.stderr)
        Path(a.out).write_text("\n".join(sorted(set(ids))) + "\n")
        print(f"{len(set(ids))} ids -> {a.out}")


if __name__ == "__main__":
    main()
