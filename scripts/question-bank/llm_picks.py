"""How much avoidable hidden risk did the Claude proxies take? Joins the story decisions in
lab/reports/teacher-digests/*/*.md with answers.json (exact risk step and category).

    python3 scripts/question-bank/llm_picks.py --answers answers.json
"""

import argparse
import collections
import glob
import json
import re

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--answers", required=True)
args = ap.parse_args()
A = json.load(open(args.answers))
idx = {(a["title"], a["text"]): a for a in A}
by_node = collections.defaultdict(list)
for a in A:
    by_node[a["node"]].append(a)
pat = re.compile(r"^- M(\d+) \[[^\]]*\] (.+?) → \[(\d+)\] (.+?)(?: \(declined: .*?\))?(?: — notes: .*)?$")
games, rows = {}, []
for f in glob.glob("lab/reports/teacher-digests/*/*.md"):
    lines = open(f).read().splitlines()
    m = re.search(r"Policy `([^`]*)`, actor `([^`]*)`: \*\*(\w+)\*\*, (\d+) months, Q (\d+(?:\.\d+)?)", lines[2] if len(lines) > 2 else "")
    if not m:
        continue
    games[f] = {"actor": m[2], "outcome": m[3]}
    for line in lines:
        mm = pat.match(line)
        a = idx.get((mm[2], mm[4])) if mm else None
        if a:
            alts = by_node[a["node"]]
            rows.append({"g": f, "risk": a["risk"], "cat": a["cat"], "extra": a["risk"] - min(x["risk"] for x in alts),
                         "avoidable": a["risk"] > 0 and any(x["risk"] <= 0 for x in alts)})
print(f"{len(games)} games, {len(rows)} story decisions matched to the catalogue")
for actor in sorted({g["actor"] for g in games.values()}):
    rr = [x for x in rows if games[x["g"]]["actor"] == actor]
    risky = [x for x in rr if x["risk"] > 0]
    print(f"{actor:10s} {len(rr):6d} decisions: risky {len(risky) / len(rr):.1%}, avoidable {np.mean([x['avoidable'] for x in rr]):.1%}; "
          f"picks by category {dict(collections.Counter(x['cat'] for x in rr).most_common())}")
    print(f"{'':10s} risky picks by category {dict(collections.Counter(x['cat'] for x in risky).most_common())}")
per = collections.defaultdict(list)
for x in rows:
    if games[x["g"]]["actor"] == "haiku":
        per[x["g"]].append(x["extra"])
for lab, want in (("completed", True), ("eliminated", False)):
    gs = [g for g in per if (games[g]["outcome"] == "completed") == want]
    print(f"haiku {lab}: {len(gs)} games, avoidable risk steps per 100 decisions "
          f"{100 * sum(sum(per[g]) for g in gs) / sum(len(per[g]) for g in gs):.1f}")
