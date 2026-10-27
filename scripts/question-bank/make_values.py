"""Turn bank.json into a question -> option score file for the greedy bot (run.py --values).

Score = adjusted final score of the option, shrunk towards 0 with k pseudo-draws so rare
options are not trusted on a handful of games. Research device only: it encodes answers
to specific questions and must never go into a Skill.

    python3 scripts/question-bank/make_values.py <analysis dir>/bank.json <out.json> --k 30
"""

import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("bank")
ap.add_argument("out")
ap.add_argument("--k", type=float, default=30)
args = ap.parse_args()
bank = json.load(open(args.bank))
values = {}
for q, v in bank.items():
    vals = []
    for o in v["options"]:
        n, adv = o["n"], o["adv"] or 0.0
        vals.append(round(n / (n + args.k) * adv, 3))
    values[q] = vals
json.dump(values, open(args.out, "w"))
print(len(values), "questions")
