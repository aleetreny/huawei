"""Fitted value function on replica afterstates (approximate policy iteration). Research bot only."""
from __future__ import annotations

import copy
import json
import random
import sys

import numpy as np

import game as G
import planner
import replica as R


def feats(st: R.State) -> list[float]:
    lv = st.level
    t = R.THRESH.get(lv, R.THRESH[6])
    to_rev = 6 - (st.month % 6) if st.month % 6 else 6
    return [st.month, lv, st.duration_in_level, st.skill, st.network, st.output, st.health, st.dignity, st.wealth,
            st.risk, st.blowups, st.skill - t[0], st.network - t[1], st.output - t[2],
            st.skill - R.cap(lv, "skill"), st.network - R.cap(lv, "network"), st.output - R.cap(lv, "output"),
            to_rev, 4 * st.dignity + st.health - 8 * st.risk - 16 * st.blowups,
            st.neg_wealth_months, st.zero_net_months]


def generate(cat, params, n_games, seed, eps=0.1, keep=0.25):
    pol = planner.Planner(**params)
    rng = random.Random(seed)
    X, Y = [], []
    for i in range(n_games):
        g = G.Game(cat, random.Random(seed * 100000 + i))
        rows = []
        while True:
            d = g.next()
            if d is None:
                break
            opts = g.options(d)
            a = rng.choice(opts) if rng.random() < eps else g.policy_move(pol, d)
            g.apply(a)
            if rng.random() < keep:
                rows.append(feats(g.st))
        sc = R.Replica.score(g.st)
        X += rows
        Y += [sc] * len(rows)
    return np.array(X, float), np.array(Y, float)


class ValuePolicy(R.Policy):
    """Pick the option whose afterstate has the highest learned value (ties broken by the planner)."""

    def __init__(self, model, base: planner.Planner, mix: float = 0.0):
        self.m, self.base, self.mix = model, base, mix

    def _after(self, rep, st, fn):
        s2 = copy.deepcopy(st)
        fn(s2)
        return feats(s2)

    def _pick(self, rep, st, opts, fn_for, default):
        X = np.array([self._after(rep, st, fn_for(o)) for o in opts])
        v = self.m.predict(X)
        if self.mix:
            v = v + self.mix * np.array([o == default for o in opts])
        return opts[int(np.argmax(v))]

    def story(self, rep, st, node):
        default = self.base.story(rep, st, node)
        opts = [int(k) for k in rep.cat.nodes[node]["choices"]]
        tmp = R.Replica(rep.cat, random.Random(0))
        return self._pick(rep, st, opts, lambda k: (lambda s: tmp.answer(s, node, k)), default)

    def energy(self, rep, st):
        default = self.base.energy(rep, st)
        opts = [None] + [a for a, (fx, c) in R.ENERGY_FX.items() if 0 < c <= st.energy]
        tmp = R.Replica(rep.cat, random.Random(0))
        return self._pick(rep, st, opts, lambda a: (lambda s: tmp.energy_action(s, a) if a else None), default)

    def main(self, rep, st):
        default = self.base.main(rep, st)
        opts = list(R.MAIN_FX)
        tmp = R.Replica(rep.cat, random.Random(0))
        return self._pick(rep, st, opts, lambda a: (lambda s: tmp.main_action(s, a)), default)
