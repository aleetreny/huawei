"""Combine several stat labellings without new Haiku calls: a per-stat vote, or per-stat picks.

    python3 scripts/leah/stat_perception/combine.py --out vote.json --vote tags-plain.json tags-defs.json tags-contrast.json
    python3 scripts/leah/stat_perception/combine.py --out mix.json --pick skill=tags-defs.json network=tags-plain.json ...

Vote: the sign most labellings give (ties go to 0). Pick: each stat taken from one labelling.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

STATS = ["skill", "network", "output", "health", "dignity"]

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--vote", nargs="+")
ap.add_argument("--pick", nargs="+", help="stat=path")
args = ap.parse_args()
out = {}
if args.vote:
    sets = [json.load(open(p)) for p in args.vote]
    for k in sets[0]:
        row = {}
        for s in STATS:
            c = Counter(t.get(k, {}).get(s, 0) for t in sets).most_common()
            row[s] = c[0][0] if len(c) == 1 or c[0][1] > c[1][1] else 0
        out[k] = row
else:
    picks = {s: json.load(open(p)) for s, p in (x.split("=", 1) for x in args.pick)}
    keys = next(iter(picks.values())).keys()
    out = {k: {s: picks[s].get(k, {}).get(s, 0) if s in picks else 0 for s in STATS} for k in keys}
Path(args.out).write_text(json.dumps(out, indent=0, sort_keys=True))
print(f"{len(out)} answers -> {args.out}")
