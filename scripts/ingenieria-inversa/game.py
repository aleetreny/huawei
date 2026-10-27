"""Step-wise replica game (copyable at any decision) and a rollout policy-improvement player.

Game.next() returns the pending decision: ("e", node) | ("q", None) | ("m", None) | None (game over).
Game.apply(x) applies the answer k / energy action name (None ends the energy phase) / main action name.
"""

from __future__ import annotations

import copy
import random
from typing import Any

import replica as R


class Game:
    def __init__(self, cat: R.Catalog, rng: random.Random, months: int = 48,
                 settle_completion: bool = True):
        self.cat, self.rng, self.months = cat, rng, months
        self.settle_completion = settle_completion
        self.rep = R.Replica(cat, rng)
        self.st = R.State()
        self.st.out_hist[1] = self.st.output
        self.used: set[str] = set()
        self.pending: list[str] = []
        self.queue: list[str] = []
        self.slots = 3
        self.node: str | None = None
        self.phase = "events"
        self.trace: list = []
        self._start_month()

    def _start_month(self) -> None:
        self.queue, self.pending, self.slots, self.node, self.phase = self.pending, [], 3, None, "events"

    def _fill(self) -> None:
        """Make sure self.node is the next event to answer, or move on to the quarter / month change."""
        while self.phase == "events" and self.node is None:
            if self.slots <= 0 or not self.st.alive:
                self._end_events()
                continue
            if self.queue:
                self.node = self.queue.pop(0)
            else:
                t = R.draw_title(self.cat, self.st, self.used, self.rng)
                if t is None:
                    self._end_events()
                    continue
                self.used.add(t)
                self.node = self.cat.d["first_node"][t]
            n = self.cat.nodes.get(self.node)
            if not n or not n["choices"]:
                self.node = None
                self.slots -= 1

    def _end_events(self) -> None:
        if not self.st.alive:
            self.phase = "over"
            return
        if self.st.month % 3 == 0:
            self.st.energy = 3
            self.phase = "energy"
        else:
            self._advance()

    def _advance(self) -> None:
        if self.st.month >= self.months or not self.st.alive:
            if self.st.alive and self.months == 48 and self.st.month == 48 and self.settle_completion:
                self.rep.month_change(self.st)
            self.phase = "over"
            return
        info = self.rep.month_change(self.st)
        if info.get("grade"):
            self.trace.append((self.st.month, "r", info))
        if not self.st.alive:
            self.phase = "over"
            return
        self._start_month()

    def next(self):
        self._fill()
        if self.phase == "events":
            return ("e", self.node)
        if self.phase == "energy":
            return ("q", None)
        if self.phase == "main":
            return ("m", None)
        return None

    def apply(self, x) -> None:
        if self.phase == "events":
            node = self.node
            self.rep.answer(self.st, node, x)
            self.trace.append((self.st.month, "e", node, x))
            self.slots -= 1
            ch = self.cat.nodes[node]["choices"].get(str(x), {})
            self.node = None
            if "next" in ch:
                if ch.get("when") == "same" and self.slots > 0:
                    self.queue.insert(0, ch["next"])
                else:
                    self.pending.append(ch["next"])
            if not self.st.alive:
                self.phase = "over"
        elif self.phase == "energy":
            if x is None or R.ENERGY_FX.get(x, ({}, 9))[1] > self.st.energy:
                self.phase = "main"
            else:
                self.rep.energy_action(self.st, x)
                if not self.st.alive:
                    self.phase = "over"
        elif self.phase == "main":
            self.rep.main_action(self.st, x)
            self.trace.append((self.st.month, "m", x))
            self._advance()

    def options(self, d):
        if d[0] == "e":
            return [int(k) for k in self.cat.nodes[d[1]]["choices"]]
        if d[0] == "q":
            return [None] + [a for a, (fx, c) in R.ENERGY_FX.items() if 0 < c <= self.st.energy]
        return list(R.MAIN_FX)

    def policy_move(self, pol: R.Policy, d):
        if d[0] == "e":
            return pol.story(self.rep, self.st, d[1])
        if d[0] == "q":
            return pol.energy(self.rep, self.st)
        return pol.main(self.rep, self.st)

    def finish(self, pol: R.Policy) -> float:
        while True:
            d = self.next()
            if d is None:
                return R.Replica.score(self.st)
            self.apply(self.policy_move(pol, d))

    def clone(self, seed: int) -> "Game":
        g = copy.copy(self)
        g.st = copy.deepcopy(self.st)
        g.used, g.pending, g.queue, g.trace = set(self.used), list(self.pending), list(self.queue), []
        g.rng = random.Random(seed)
        g.rep = R.Replica(self.cat, g.rng)
        return g


class Rollout(R.Policy):
    """One-step policy improvement: value each option by n rollouts of the base policy to the end."""

    def __init__(self, base: R.Policy, n: int = 8, margin: float = 3.0, kinds=("e", "q", "m"), seed: int = 0):
        self.base, self.n, self.margin, self.kinds = base, n, margin, kinds
        self.rng = random.Random(seed)

    def choose(self, game: Game, d):
        default = game.policy_move(self.base, d)
        if d[0] not in self.kinds:
            return default
        opts = game.options(d)
        if len(opts) <= 1:
            return default
        seeds = [self.rng.randrange(1 << 30) for _ in range(self.n)]   # common random numbers across options
        best, bv = default, None
        for o in opts:
            tot = 0.0
            for sd in seeds:
                g = game.clone(sd)
                g.apply(o)
                tot += g.finish(self.base)
            v = tot / self.n + (self.margin / self.n if o == default else 0.0)
            if bv is None or v > bv:
                best, bv = o, v
        return best


def play_game(cat: R.Catalog, chooser, seed: int):
    g = Game(cat, random.Random(seed))
    while True:
        d = g.next()
        if d is None:
            return g
        g.apply(chooser(g, d))
