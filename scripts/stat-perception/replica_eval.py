"""What each stat labelling is worth in the replica of main-1nddsg, with the same seeds for every arm.

Uses Alejandro's catbot (scripts/question-bank/catbot.py on branch alejandro/optimistic-gauss-edyw1j) logic:
Energy and the main action follow the 7-rule bot; only the perception of story options changes.
Two ways to use a labelling, both with risk judged by the category (as a reader would):
  cat+tags   the category's mean effect (learnt on the other half of the titles), overridden by the labels
             (Alejandro's "category + guessed stat tags" arm)
  tags       the labels' signs alone, size 1 (like his "perfect stat tags" arm, but with guessed signs)
Reference arms: oracle, category only, category + perfect signs.

    .venv/bin/python scripts/stat-perception/replica_eval.py --rx <main-1nddsg checkout> \\
        --answers answers.json --tags-dir <dir of up/down files> --games 1000
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--rx", required=True)
ap.add_argument("--answers", required=True)
ap.add_argument("--tags-dir", required=True)
ap.add_argument("--games", type=int, default=1000)
ap.add_argument("--seed", type=int, default=4242)
ap.add_argument("--json-out")
args = ap.parse_args()
sys.path.insert(0, f"{args.rx}/scripts/ingenieria-inversa")
import replica as R  # noqa: E402
import rules  # noqa: E402

cat = R.Catalog(json.load(open(f"{args.rx}/lab/data/ingenieria-inversa/catalog_v2.json")))
A = json.load(open(Path(args.answers).expanduser()))
CATS = ["OWN", "FIX", "ESCALATE", "GUARD", "SELL", "AVOID", "YIELD", "PERSIST", "ATTACK", "HIDE"]
RISKY = {"AVOID", "SELL", "YIELD", "PERSIST", "ATTACK", "HIDE"}
K = ["health", "dignity", "skill", "network", "output", "wealth"]
label = {(a["node"], a["choice"]): a["cat"] for a in A}
title_of = {a["node"]: a["title"] for a in A}
titles = sorted(set(title_of.values()))
fold = {t: i % 2 for i, t in enumerate(random.Random(7).sample(titles, len(titles)))}  # same folds as catbot.py
means = {(f, c): {k: float(np.mean([a["d"].get(k, 0) for a in A if a["cat"] == c and fold[a["title"]] != f] or [0])) for k in K}
         for f in (0, 1) for c in CATS}
TAGS = {}
for p in sorted(Path(args.tags_dir).expanduser().glob("*.json")):
    TAGS[p.stem] = {(k.split(":")[0], int(k.split(":")[1])): v for k, v in json.load(open(p)).items()}


class Bot(rules.RuleBot):
    def __init__(self, fx, tags=None, seed=0):
        super().__init__()
        self.fx, self.tags, self.rng = fx, tags or {}, random.Random(seed)

    def story(self, rep, st, node):
        if self.fx == "oracle":
            return super().story(rep, st, node)
        ks = [int(k) for k in rep.cat.nodes[node]["choices"]]
        f = fold.get(title_of.get(node), 0)
        best, bv = ks[0], -1e18
        for k in ks:
            c = label.get((node, k), "FIX")
            d = rep.cat.nodes[node]["choices"][str(k)]["d"]
            t = self.tags.get((node, k), {})
            if self.fx == "signs":
                fx = {s: float(np.sign(v)) for s, v in d.items()}
            elif self.fx == "tags":
                fx = {s: 1.0 for s in t.get("up", [])} | {s: -1.0 for s in t.get("down", [])}
            elif self.fx == "cat+tags":
                fx = dict(means[(f, c)])
                for s in t.get("up", []):
                    fx[s] = max(fx.get(s, 0), 1.0)
                for s in t.get("down", []):
                    fx[s] = min(fx.get(s, 0), -1.0)
            else:
                fx = means[(f, c)]
            v = self._val(st, fx, 1 if c in RISKY else 0) + 1e-6 * self.rng.random()
            if v > bv:
                best, bv = k, v
        return best


arms = {"oracle": dict(fx="oracle"), "category only": dict(fx="category"), "perfect signs": dict(fx="signs")}
for name, t in TAGS.items():
    arms[f"{name} cat+tags"] = dict(fx="cat+tags", tags=t)
    arms[f"{name} tags"] = dict(fx="tags", tags=t)
res, rows = {}, {}
for name, kw in arms.items():
    scores, lv, out = [], collections.Counter(), collections.Counter()
    for i in range(args.games):
        st, _ = R.play(cat, Bot(seed=i, **kw), random.Random(args.seed + i))
        scores.append(R.Replica.score(st))
        lv[st.level] += 1
        out[st.failure or "completed"] += 1
    s = np.array(scores)
    res[name] = s
    d = s - res.get("category only", s)
    rows[name] = {"mean": s.mean(), "se": s.std(ddof=1) / np.sqrt(len(s)), "l6": sum(v for k, v in lv.items() if k >= 6) / len(s),
                  "vs_category": d.mean(), "vs_category_se": d.std(ddof=1) / np.sqrt(len(d)), "outcomes": dict(out)}
    r = rows[name]
    print(f"{name:22s} {r['mean']:5.1f} ± {r['se']:.2f}   vs category {r['vs_category']:+5.1f} ± {r['vs_category_se']:.2f}   "
          f"L6+ {r['l6']:4.0%}  dismissed {out['dismissed']:4d} trust {out['trust']:4d}")
if args.json_out:
    Path(args.json_out).write_text(json.dumps(rows, indent=1, default=float))
