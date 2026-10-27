"""Questions 1-2 on the exact answer catalogue of the reverse-engineering branch (main-1nddsg).

Inputs:
  --answers  answers.json: one row per story answer (node, title, choice, text, exact effect d,
             exact hidden-risk step, category label given blind by Haiku from the wording only)
  --values   answer_values.csv of main-1nddsg (expected final score of each answer at 225
             decision points, under the tuned planner)
Prints:
  1. per category: exact risk and effects; how well "category says risky" predicts a risk step > 0;
     stability across two random halves of the titles;
  2. dominance: in how many questions one answer is at least as good on every visible stat AND on risk;
  3. per decision point of answer_values: is the best answer in the best-ranked category? regret of
     choosing by category rank, against random and against the planner.

    python3 scripts/question-bank/categories.py --answers answers.json --values answer_values.csv
"""

import argparse
import collections
import csv
import json
import random

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--answers", required=True)
ap.add_argument("--values", required=True)
args = ap.parse_args()
A = json.load(open(args.answers))
K = ["health", "dignity", "skill", "network", "output", "wealth"]
CATS = ["OWN", "ESCALATE", "FIX", "GUARD", "AVOID", "SELL", "YIELD", "PERSIST", "ATTACK", "HIDE"]
RISKY = {"AVOID", "SELL", "YIELD", "PERSIST", "ATTACK", "HIDE"}

print("1. Categories against exact effects (936 answers)")
by = collections.defaultdict(list)
for a in A:
    by[a["cat"]].append(a)
print(f"{'cat':9}{'n':>5} {'risk':>5} {'P(r>0)':>6} {'P(r<0)':>6} " + " ".join(f"{k[:4]:>5}" for k in K))
for c in sorted(by, key=lambda c: np.mean([a["risk"] for a in by[c]])):
    aa = by[c]
    r = np.array([a["risk"] for a in aa])
    print(f"{c:9}{len(aa):5d} {r.mean():5.2f} {np.mean(r > 0):6.2f} {np.mean(r < 0):6.2f} "
          + " ".join(f"{np.mean([a['d'].get(k, 0) for a in aa]):5.2f}" for k in K))
r = np.array([a["risk"] > 0 for a in A])
p = np.array([a["cat"] in RISKY for a in A])
print(f"risky = category in {sorted(RISKY)}: accuracy {np.mean(r == p):.3f} (base rate not risky {1 - r.mean():.3f}); "
      f"recall of risky answers {np.mean(p[r]):.3f}; precision {np.mean(r[p]):.3f}")
big = np.array([a["risk"] >= 2 for a in A])
print(f"answers with risk step >= 2: {big.sum()}, flagged by category: {np.mean(p[big]):.3f}")
titles = sorted({a["title"] for a in A})
for seed in (1, 2, 3):
    rng = random.Random(seed)
    half = set(rng.sample(titles, len(titles) // 2))
    m = {}
    for part in (True, False):
        m[part] = {c: np.mean([a["risk"] for a in A if a["cat"] == c and (a["title"] in half) == part] or [np.nan]) for c in CATS}
    order = [sorted(CATS, key=lambda c: m[part][c]) for part in (True, False)]
    rho = np.corrcoef([m[True][c] for c in CATS], [m[False][c] for c in CATS])[0, 1]
    print(f"  split {seed}: mean risk by category correlates {rho:.2f} between halves; orders {order[0]} | {order[1]}")

print("\n2. Is there always a best answer? (per question: one answer >= every other on all visible stats and <= on risk)")
q = collections.defaultdict(list)
for a in A:
    q[a["node"]].append(a)
dom = 0
dom_cat = collections.Counter()
for node, aa in q.items():
    def ge(x, y):
        return all(x["d"].get(k, 0) >= y["d"].get(k, 0) for k in K) and x["risk"] <= y["risk"]
    winners = [x for x in aa if all(ge(x, y) for y in aa if y is not x)]
    if winners:
        dom += 1
        dom_cat[winners[0]["cat"]] += 1
print(f"  {dom} of {len(q)} questions have an answer that dominates all others; its category: {dict(dom_cat.most_common())}")
safe_best = 0
for node, aa in q.items():
    mn = min(x["risk"] for x in aa)
    if any(x["risk"] == mn and x["cat"] not in RISKY for x in aa):
        safe_best += 1
print(f"  {safe_best} of {len(q)} questions: the lowest-risk answer is in a safe category")

print("\n3. Expected final score per answer at 225 decision points (planner continuations)")
rows = list(csv.DictReader(open(args.values)))
cat_of = {(a["node"], a["choice"]): a["cat"] for a in A}
pts = collections.defaultdict(list)
for x in rows:
    pts[(x["month"], x["node"])].append(x)
reg = {"category rank": [], "random": [], "planner": [], "safe set, best stats": []}
hit = 0
rank = {c: i for i, c in enumerate(CATS)}
eff = {(a["node"], a["choice"]): a for a in A}
for (m, node), xs in pts.items():
    if len(xs) < 2:
        continue
    best = max(float(x["exp_score"]) for x in xs)
    def r_of(x):
        return best - float(x["exp_score"])
    cats = [cat_of.get((node, int(x["answer"]))) for x in xs]
    top = min(rank.get(c, 99) for c in cats)
    cand = [x for x, c in zip(xs, cats) if rank.get(c, 99) == top]
    reg["category rank"].append(np.mean([r_of(x) for x in cand]))
    reg["random"].append(np.mean([r_of(x) for x in xs]))
    reg["planner"].append(np.mean([r_of(x) for x in xs if x["policy_pick"] == "1"] or [0]))
    safe = [x for x, c in zip(xs, cats) if c not in RISKY] or xs
    gain = lambda x: sum(eff[(node, int(x["answer"]))]["d"].get(k, 0) for k in ("skill", "network", "output", "dignity", "health"))
    reg["safe set, best stats"].append(r_of(max(safe, key=gain)))
    bx = max(xs, key=lambda x: float(x["exp_score"]))
    hit += rank.get(cat_of.get((node, int(bx["answer"]))), 99) == top
print(f"  best answer is in the best-ranked category present: {hit}/{len(reg['random'])}")
for k, v in reg.items():
    print(f"  mean regret per decision, {k:22s}: {np.mean(v):.2f} points")
