"""General-rule bot for the replica: only what an agent can see or infer (research, not Skill text).

Perception: the announced effect of each option and only the SIGN of its hidden risk (risky / neutral /
careful); the HR remark (risk shown as min(risk, 4)); the visible ceiling of each stat at the current
level (an agent detects it when a gain stops registering). No thresholds, no event names, no numbers
from the dev data. Each rule can be switched off to measure its contribution.

Rules:
  R1 risk: keep the HR remark calm; when it is not calm, refuse risky options and use the quarter to
     lower risk (Lay low / Defuse).
  R2 review: in the month before a review, never give up a point of Skill, Network or Output.
  R3 ceiling: grow the stat furthest below its visible ceiling first; gains above the ceiling are worth 0.
  R4 skill: once Network and Output sit at their ceiling, put everything into Skill (it is the bottleneck).
  R5 endgame: in the last quarter, clear risk and restore health and dignity (they count in the ending).
  R6 money: at higher levels avoid options that cost money (losses scale with level).
  R7 health: never let health fall near zero; recover in the quarter when it is low.
"""

from __future__ import annotations

from typing import Any

import replica as R

ALL = ("R1", "R2", "R3", "R4", "R5", "R6", "R7")


class RuleBot(R.Policy):
    def __init__(self, on=ALL):
        self.on = set(on)

    def cap(self, st: R.State, k: str) -> float:
        """Ceiling the bot believes for stat k at its level (subclasses may learn it in-run)."""
        return R.cap(st.level, k)

    def _val(self, st: R.State, fx: dict[str, float], risk_sign: int) -> float:
        on = self.on
        lv = st.level
        v = 0.0
        pre_review = st.month % 6 == 5
        endgame = st.month >= 46 and "R5" in on
        at_cap = {k: getattr(st, k) >= self.cap(st, k) for k in R.GROWTH}
        for k in R.GROWTH:
            x = fx.get(k, 0)
            cur = getattr(st, k)
            c = self.cap(st, k)
            gain = (min(c, cur + x) - min(c, cur)) if "R3" in on else x
            if x < 0:
                gain = max(R.MINS[k], cur + x) - cur
            w = 1.0
            if "R3" in on:
                w += 2.0 * max(0.0, (c - cur) / max(1.0, c))
            if "R4" in on and k == "skill" and at_cap["network"] and at_cap["output"]:
                w += 2.0
            if "R2" in on and pre_review and x < 0:
                w += 6.0
            if endgame:
                w = 0.3 if k != "output" else 0.0
            v += w * gain
        h = min(10, st.health + fx.get("health", 0))
        d = min(10, st.dignity + fx.get("dignity", 0))
        v += 0.5 * (h - st.health) + 0.5 * (d - st.dignity)
        if endgame:
            v += 0.8 * ((h - st.health) + (d - st.dignity))
        if "R7" in on and h <= 2:
            v -= 30
        if d < 4:
            v -= 3 * (4 - d)
        wl = fx.get("wealth", 0)
        if wl < 0 and "R6" in on:
            wl *= (lv + 1) // 2
        v += 0.5 * wl
        hr = min(st.risk, 4)
        if "R1" in on:
            v -= risk_sign * (1.0 + 3.0 * hr)
            if risk_sign > 0 and hr >= 2:
                v -= 20
        if endgame:
            v -= 3.0 * risk_sign
        return v

    def story(self, rep, st, node):
        best, bv = 1, -1e18
        for k, ch in rep.cat.nodes[node]["choices"].items():
            r = rep.cat.answer_risk(node, int(k))
            sign = (r > 0) - (r < 0)
            v = self._val(st, ch["d"], sign)
            if v > bv:
                best, bv = int(k), v
        return best

    def energy(self, rep, st):
        on = self.on
        if "R7" in on and st.health <= 4 and st.energy >= 1:
            return "Health recovery"
        if "R1" in on and min(st.risk, 4) >= 2 and st.energy >= 2:
            return "Defuse legacy risk"
        if "R5" in on and st.month >= 46:
            if st.risk > 0 and st.energy >= 2:
                return "Defuse legacy risk"
            if st.health < 10 and st.energy >= 1:
                return "Health recovery"
            if st.dignity < 10 and st.energy >= 1:
                return "Mental recovery"
        opts = []
        for a in ("Prepare report materials", "Network maintenance", "Skill learning", "Mental recovery", "Health recovery"):
            fx, cost = R.ENERGY_FX[a]
            if cost <= st.energy:
                opts.append((self._val(st, fx, 0) / cost, a))
        if not opts:
            return None
        v, a = max(opts)
        return a if v > 0 else None

    def main(self, rep, st):
        if ("R1" in self.on and min(st.risk, 4) >= 2) or ("R5" in self.on and st.month >= 46 and st.risk > 0):
            return "Lay low and reduce risk"
        return max(R.MAIN_FX, key=lambda a: self._val(st, R.MAIN_FX[a], 0))
