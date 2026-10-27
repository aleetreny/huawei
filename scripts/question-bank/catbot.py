"""Question 2 in the replica of main-1nddsg: how much does an agent lose if it only sees the
CATEGORY of each story option (as DeepSeek would, reading the wording) instead of its exact effect
and hidden-risk sign?

Story perception per arm (Energy and main action always follow the 7-rule bot, rules.py):
  oracle       exact effect and exact risk sign (rules.RuleBot as published)
  category     effect = mean effect of the option's category, risk sign = category is risky;
               category means taken from the OTHER half of the titles (2-fold by title)
  category-noisy  same, with 20 % of labels replaced by a random category (labelling mistakes)
  exact effect, category risk / category effect, exact risk   split the loss between the two perceptions
  rank         no effects at all: pick the best-ranked category, ties at random
  random       uniform random story answer
Same game seeds across arms.

    python3 scripts/question-bank/catbot.py --rx /path/to/main-1nddsg/checkout --answers answers.json --games 1000
"""

import argparse
import collections
import json
import random
import sys

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--rx", required=True, help="checkout of branch main-1nddsg")
ap.add_argument("--answers", required=True)
ap.add_argument("--games", type=int, default=1000)
ap.add_argument("--seed", type=int, default=4242)
ap.add_argument("--tags", help="stat tags {node:choice: {up: [...], down: [...]}} guessed from the wording")
args = ap.parse_args()
sys.path.insert(0, f"{args.rx}/scripts/ingenieria-inversa")
import replica as R  # noqa: E402
import rules  # noqa: E402

cat = R.Catalog(json.load(open(f"{args.rx}/lab/data/ingenieria-inversa/catalog_v2.json")))
A = json.load(open(args.answers))
CATS = ["OWN", "FIX", "ESCALATE", "GUARD", "SELL", "AVOID", "YIELD", "PERSIST", "ATTACK", "HIDE"]
RISKY = {"AVOID", "SELL", "YIELD", "PERSIST", "ATTACK", "HIDE"}
RANK = {c: i for i, c in enumerate(CATS)}
K = ["health", "dignity", "skill", "network", "output", "wealth"]
label = {(a["node"], a["choice"]): a["cat"] for a in A}
tags = {}
if args.tags:
    for key, t in json.load(open(args.tags)).items():
        n, c = key.split(":")
        tags[(n, int(c))] = t
title_of = {a["node"]: a["title"] for a in A}
titles = sorted(set(title_of.values()))
fold = {t: i % 2 for i, t in enumerate(random.Random(7).sample(titles, len(titles)))}
# category mean effect, estimated on the other fold
means = {}
for f in (0, 1):
    for c in CATS:
        aa = [a for a in A if a["cat"] == c and fold[a["title"]] != f]
        means[(f, c)] = {k: float(np.mean([a["d"].get(k, 0) for a in aa])) for k in K}


class CatBot(rules.RuleBot):
    def __init__(self, mode, noise=0.0, seed=0, fx="category", risk="category"):
        super().__init__()
        self.mode, self.noise, self.rng = mode, noise, random.Random(seed)
        self.fx, self.risk = fx, risk  # perception of effect / of risk sign: "category" or "exact"

    def story(self, rep, st, node):
        ks = [int(k) for k in rep.cat.nodes[node]["choices"]]
        if self.mode == "oracle":
            return super().story(rep, st, node)
        if self.mode == "random":
            return self.rng.choice(ks)
        f = fold.get(title_of.get(node), 0)
        labs = {}
        for k in ks:
            c = label.get((node, k), "FIX")
            if self.noise and self.rng.random() < self.noise:
                c = self.rng.choice(CATS)
            labs[k] = c
        if self.mode == "rank":
            top = min(RANK[c] for c in labs.values())
            return self.rng.choice([k for k in ks if RANK[labs[k]] == top])
        best, bv = ks[0], -1e18
        for k in ks:
            c = labs[k]
            d = rep.cat.nodes[node]["choices"][str(k)]["d"]
            if self.fx == "exact":
                fx = d
            elif self.fx == "signs":  # perfect stat tags: direction of every effect, size 1
                fx = {s: float(np.sign(v)) for s, v in d.items()}
            elif self.fx == "tags":  # category mean, overridden by the guessed stat tags
                fx = dict(means[(f, c)])
                t = tags.get((node, k), {})
                for s in t.get("up", []):
                    fx[s] = max(fx.get(s, 0), 1.0)
                for s in t.get("down", []):
                    fx[s] = min(fx.get(s, 0), -1.0)
            else:
                fx = means[(f, c)]
            if self.risk == "exact":
                r = rep.cat.answer_risk(node, k)
                sign = (r > 0) - (r < 0)
            else:
                sign = 1 if c in RISKY else 0
            v = self._val(st, fx, sign) + 1e-6 * self.rng.random()
            if v > bv:
                best, bv = k, v
        return best


arms = {"oracle": dict(mode="oracle"), "category": dict(mode="category"),
        "category-noisy20": dict(mode="category", noise=0.2), "rank": dict(mode="rank"), "random": dict(mode="random"),
        "exact effect, category risk": dict(mode="category", fx="exact"),
        "category effect, exact risk": dict(mode="category", risk="exact"),
        "category + perfect stat tags": dict(mode="category", fx="signs")}
if tags:
    arms["category + guessed stat tags"] = dict(mode="category", fx="tags")
    arms["guessed tags, noisy20"] = dict(mode="category", fx="tags", noise=0.2)
print(f"{args.games} games per arm, same seeds")
res = {}
for name, kw in arms.items():
    scores, lv, out = [], collections.Counter(), collections.Counter()
    for i in range(args.games):
        st, _ = R.play(cat, CatBot(seed=i, **kw), random.Random(args.seed + i))
        scores.append(R.Replica.score(st))
        lv[st.level] += 1
        out[st.failure or "completed"] += 1
    s = np.array(scores)
    res[name] = s
    print(f"  {name:17s} mean {s.mean():5.1f} ± {s.std(ddof=1) / np.sqrt(len(s)):.2f}  L6+ {sum(v for k, v in lv.items() if k >= 6) / len(s):4.0%}  "
          f"outcomes {dict(out)}")
for name in [n for n in arms if n != "oracle"]:
    d = res["oracle"] - res[name]
    print(f"  oracle - {name}: {d.mean():.1f} ± {d.std(ddof=1) / np.sqrt(len(d)):.2f} (paired)")
