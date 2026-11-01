"""Reaching L6 in the replica: what the quarter must do from the middle levels, with the t13-read-v4 story rules.

Story decisions follow the v4-like LexBot of l1_trap.py (TrapBot). Only the quarterly phase changes:
  blind      DeepSeek as observed: Energy on report materials and Network, main action key project, never
             Skill learning (v4's "Stalled" switch is never filled in by DeepSeek)
  ref        the 7-rule bot's quarter, which knows every level's ceiling (an upper reference)
  sk<L>      from level L: Skill learning first (Health above the low band), then one point on Output or
             Network, whichever is further below its Best; main action key project
  sk<L>r     the same, main action Apply for rotation (Skill +2, Network +1)
Health, risk and final-quarter lines keep priority in every arm (v4 lines 1-3).

For each review at L5 it records which promotion condition failed.

    .venv/bin/python scripts/stat-perception/l6.py --games 2000 --reading perfect --arms blind,ref,sk4,sk4r
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import l1_trap as T  # noqa: E402

G, R = T.G, T.R


class L6Bot(T.TrapBot):
    def __init__(self, per, seed, quarter="blind", skill_from=99, rotation=False, net3=False, skill_story=99):
        super().__init__(per, seed=seed)
        self.q, self.skill_from, self.rotation = quarter, skill_from, rotation
        self.net3 = net3                 # at L3: quarter on Network (maintenance first, main action Build a mentorship)
        self.skill_story = skill_story   # from this level: in stories, take a safe option that raises Skill if there is one

    def story(self, rep, st, node):
        pick = super().story(rep, st, node)
        if st.level < self.skill_story or st.month >= 46 or (st.month % 6 and 6 - st.month % 6 <= 1):
            return pick  # never overrides the review-month protection or the final quarter
        seen = {int(k): self.per.see(node, int(k)) for k in rep.cat.nodes[node]["choices"]}
        if seen[pick][0].get("skill", 0) > 0:
            return pick
        ok = [k for k, (fx, r) in seen.items() if fx.get("skill", 0) > 0 and r <= 0
              and fx.get("network", 0) >= 0 and fx.get("output", 0) >= 0
              and not (st.health <= 3 and fx.get("health", 0) < 0) and not (st.dignity <= 4 and fx.get("dignity", 0) < 0)]
        if not ok:
            return pick
        return max(ok, key=lambda k: (sum(seen[k][0].get(x, 0) > 0 for x in R.GROWTH), self.rng.random()))

    def energy(self, rep, st):
        if self.q == "ref":
            return G.rules.RuleBot.energy(self, rep, st)
        # v4 lines 1-3: final quarter, recovery, HR remark (LexBot keeps them before the blind quarter)
        if st.month >= 46 or st.health <= 4 or (min(st.risk, 4) >= self.defuse_at and st.energy >= 3):
            return super().energy(rep, st)
        if self.net3 and st.level == 3 and st.network < R.THRESH[3][1] + 1 and st.energy >= 1:
            return "Network maintenance"
        if st.level >= self.skill_from:
            if st.energy >= 2 and st.health > 4:
                return "Skill learning"
            if st.energy >= 1:
                gap = {k: getattr(st, k) - self.best.get(k, getattr(st, k)) for k in ("network", "output")}
                return "Network maintenance" if gap["network"] < gap["output"] else "Prepare report materials"
            return None
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.q == "ref":
            return G.rules.RuleBot.main(self, rep, st)
        if min(st.risk, 4) >= self.laylow_at and st.month < 46:
            return "Lay low and reduce risk"
        if self.net3 and st.level == 3 and st.network < R.THRESH[3][1] + 1 and st.month < 46:
            return "Build a mentorship"
        if self.rotation and st.level >= self.skill_from and st.month < 46:
            return "Apply for rotation"
        return super().main(rep, st)


def spec(name: str) -> dict:
    """blind | ref | sk<L>[r] | any of those joined with +net3 and/or +ss<L> (story Skill rule from level L)."""
    base, *extra = name.split("+")
    kw = {"quarter": base} if base in ("blind", "ref") else {"quarter": "skill", "skill_from": int(base[2]), "rotation": base.endswith("r")}
    for x in extra:
        if x == "net3":
            kw["net3"] = True
        elif x.startswith("ss"):
            kw["skill_story"] = int(x[2:])
    return kw


_ARMS: dict = {}


def _init(arms):
    _ARMS.update(arms)


def _play(args):
    name, i, seed0 = args
    per, kw = _ARMS[name]
    bot = L6Bot(per, seed=i, **kw)
    l5 = []
    orig = R.Replica.review

    def review(self, st, explosion_now=False):
        lvl, s, n, o = st.level, st.skill, st.network, st.output
        out = orig(self, st, explosion_now)
        if lvl == 5:
            t = R.THRESH[5]
            l5.append(tuple(x for x, bad in (("skill", s < t[0]), ("network", n < t[1]), ("output", o < t[2]),
                                             ("grade D", out["grade"] == "D")) if bad))
        return out
    R.Replica.review = review
    try:
        st, trace = R.play(G.CAT, bot, random.Random(seed0 + i))
    finally:
        R.Replica.review = orig
    promos = [t[0] for t in trace if t[1] == "r" and t[2].get("promoted")]
    return R.Replica.score(st), st.level, st.failure or "completed", st.skill, st.network, l5, promos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--reading", default="perfect", help="perfect, or tag files joined by +")
    ap.add_argument("--arms", default="blind,ref,sk4,sk4r")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    if a.reading == "perfect":
        per = G.Perception(T.perfect(), "signs", "group")
    else:
        reads = [G.Perception(T.labels_from(f), "signs", "group") for f in a.reading.split("+")]
        per = reads[0] if len(reads) == 1 else G.Mixed(reads)
    arms = {n: (per, spec(n)) for n in a.arms.split(",")}
    rows = {}
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(arms,)) as ex:
        for name in arms:
            out = list(ex.map(_play, [(name, i, a.seed) for i in range(a.games)], chunksize=25))
            sc = np.array([o[0] for o in out])
            lv = collections.Counter(o[1] for o in out)
            done = [o for o in out if o[2] == "completed"]
            reached5 = [o for o in out if o[1] >= 5]
            l5why = collections.Counter(x for o in out for r in o[5] for x in (r or ("promoted",)))
            m5 = [o[6][3] for o in out if len(o[6]) >= 4]
            rows[name] = {"score": sc.mean(), "se": sc.std(ddof=1) / np.sqrt(len(sc)),
                          "l6": sum(v for k, v in lv.items() if k >= 6) / len(sc), "l5plus": len(reached5) / len(sc),
                          "levels": dict(sorted(lv.items())), "completed": len(done) / len(sc),
                          "skill_end_completed": float(np.mean([o[3] for o in done])) if done else None,
                          "network_end_completed": float(np.mean([o[4] for o in done])) if done else None,
                          "month_reach_l5": float(np.mean(m5)) if m5 else None, "l5_reviews": dict(l5why),
                          "failures": dict(collections.Counter(o[2] for o in out))}
            r = rows[name]
            print(f"{name:6s} {r['score']:5.1f} ± {r['se']:.2f}  L6+ {r['l6']:5.1%}  L5+ {r['l5plus']:5.1%}  completed {r['completed']:5.1%}  "
                  f"Skill end {r['skill_end_completed']:5.1f}  Network end {r['network_end_completed']:4.1f}  "
                  f"reach L5 at m{r['month_reach_l5'] or 0:4.1f}  L5 reviews {r['l5_reviews']}  {r['failures']}", flush=True)
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=1, default=float))


if __name__ == "__main__":
    main()
