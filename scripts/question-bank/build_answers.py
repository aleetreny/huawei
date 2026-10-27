"""Build answers.json: one row per story answer, joining the exact catalogue of main-1nddsg
(effect, hidden-risk step) with the blind category labels (lab/reports/question-bank/labels.json).

    python3 scripts/question-bank/build_answers.py --rx <checkout of main-1nddsg> --out answers.json

The output carries development-dataset text (titles, options): keep it outside Git.
"""

import argparse
import glob
import json

ap = argparse.ArgumentParser()
ap.add_argument("--rx", required=True)
ap.add_argument("--labels", default="lab/reports/question-bank/labels.json")
ap.add_argument("--out", required=True)
args = ap.parse_args()
data = f"{args.rx}/lab/data/ingenieria-inversa"
cat = json.load(open(f"{data}/catalog_v2.json"))
risk = json.load(open(f"{data}/riskd_v2.json"))
labels = json.load(open(args.labels))
texts = {}
for f in glob.glob(f"{data}/*/nodes-*.jsonl"):
    for line in open(f):
        try:
            n = json.loads(line)
        except ValueError:
            continue
        texts[n["id"]] = n
rows = []
for nid, nd in cat["nodes"].items():
    t = texts.get(nid)
    if not t or t["phase"] != "event":
        continue
    for ch, v in nd["choices"].items():
        opt = next((c["action"] for c in t["choices"] if str(c["choice"]) == ch), None)
        rows.append({"node": nid, "title": nd["title"], "desc": t["description"], "choice": int(ch), "text": opt,
                     "d": v["d"], "n": v["n"], "risk": risk.get(f"E|{nid}|{ch}", 0),
                     "first": cat["first_node"].get(nd["title"]) == nid, "cat": labels.get(f"{nid}:{ch}")})
json.dump(rows, open(args.out, "w"), ensure_ascii=False)
print(len(rows), "answers;", sum(r["cat"] is None for r in rows), "without a label")
