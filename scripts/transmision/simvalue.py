"""How much final score each point of obedience is worth, in the replica (T20, phase 2).

    python3 scripts/transmision/simvalue.py --games 400

The tuned planner (the bot that scores 70.5 in the real game) plays; for one rule at a time, in the
situations that rule covers, it obeys with probability p and otherwise plays a "default" move like the
one Haiku makes without Skills in the bank (main action Apply for a key project, Energy on recovery or
Network, story option at random). Same seeds for every arm, so differences are paired.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ingenieria-inversa"))
sys.path.insert(0, str(HERE))
import planner as P  # noqa: E402
import replica as R  # noqa: E402
from bank import CATALOG, best_params  # noqa: E402

RULES = ("pre_review", "skill_l4", "hr_risk", "trigger", "early_ruin", "closing")


class Knob(P.Planner):
    def __init__(self, rule: str | None, p: float, seed: int, **kw):
        super().__init__(**kw)
        self.rule, self.obey_p, self.rng = rule, p, random.Random(seed)

    def _obey(self) -> bool:
        return self.rng.random() < self.obey_p

    def _covers(self, st: R.State, phase: str, rep: R.Replica | None = None, node: str | None = None) -> bool:
        r = self.rule
        if r == "pre_review":
            return phase == "e" and st.month % 6 == 5 and st.level <= 3
        if r == "skill_l4":
            return phase in ("q", "m") and st.level >= 4 and st.risk < 2 and st.month < 45
        if r == "hr_risk":
            return phase in ("q", "m") and st.risk >= 2 and st.month < 45
        if r == "trigger":
            return phase == "e" and st.risk >= 2
        if r == "early_ruin":
            return phase == "e" and st.level <= 2 and st.wealth < 2
        if r == "closing":
            return st.month >= 45
        return False

    def story(self, rep, st, node):
        if self.rule and self._covers(st, "e") and not self._obey():
            return int(self.rng.choice(list(rep.cat.nodes[node]["choices"])))
        return super().story(rep, st, node)

    def energy(self, rep, st):
        if self.rule and self._covers(st, "q") and not self._obey():
            for a in ("Health recovery", "Network maintenance", "Prepare report materials"):
                if R.ENERGY_FX[a][1] <= st.energy and (a != "Health recovery" or st.health < 10):
                    return a
            return None
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.rule and self._covers(st, "m") and not self._obey():
            return "Apply for a key project"
        return super().main(rep, st)


def run(rule: str | None, p: float, games: int, cat: R.Catalog) -> dict:
    scores, fails = [], 0
    for i in range(games):
        pol = Knob(rule, p, 10_000 + i, **best_params())
        st, _ = R.play(cat, pol, random.Random(i))
        scores.append(R.Replica.score(st))
        fails += int(st.failure is not None)
    m = sum(scores) / games
    sd = (sum((x - m) ** 2 for x in scores) / (games - 1)) ** 0.5
    return {"rule": rule, "p": p, "mean": round(m, 2), "se": round(sd / games ** 0.5, 2), "fail": round(fails / games, 3)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=400)
    a = ap.parse_args()
    cat = R.Catalog(json.loads(CATALOG.read_text()))
    base = run(None, 1.0, a.games, cat)
    print(json.dumps(base))
    for rule in RULES:
        rows = [run(rule, p, a.games, cat) for p in (0.0, 0.5)]
        for r in rows:
            r["loss_vs_full"] = round(base["mean"] - r["mean"], 2)
            print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
