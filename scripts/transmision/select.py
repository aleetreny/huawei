"""Keep the decisive bank items (T20), at most --cap per rule, balanced between dev and reserved titles.

    python3 scripts/transmision/select.py --raw bank-raw.jsonl --out bank.jsonl --cap 360
"""
import argparse, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import rule_of, decisive  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--raw", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--cap", type=int, default=360)
ap.add_argument("--per-title", type=int, default=8)
a = ap.parse_args()
by: dict = {}
for line in open(a.raw):
    it = json.loads(line)
    r = rule_of(it)
    if r and decisive(it, r):
        by.setdefault(r, []).append(it)
rng = random.Random(3)
with open(a.out, "w") as f:
    for r, lst in sorted(by.items()):
        rng.shuffle(lst)
        seen: dict = {}
        keep = []
        for it in lst:
            t = it["title"] if it["phase"] == "e" else it["game"]
            if seen.get(t, 0) < (a.per_title * 4 if r == "early_ruin" else a.per_title) and len(keep) < a.cap:
                seen[t] = seen.get(t, 0) + 1
                keep.append(it)
        print(r, len(lst), "decisive ->", len(keep), "kept;", sum(it["holdout"] for it in keep), "reserved", file=sys.stderr)
        for it in keep:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
