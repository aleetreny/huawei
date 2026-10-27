"""Stage-aware planner for the replica (research bot, not Skill content).

The value of a decision mixes:
- progress towards the next promotion thresholds (heavier just before a review);
- Skill banking from L4 (the bottleneck of the second half);
- hidden-risk budget: never reach 5; keep room for the review warning; cheaper risk when the
  counter is low; Defuse / Lay low when it rises;
- wealth losses scale with level (M13);
- end game: from `end_from` the score itself is the target (risk to 0, health and dignity to 10).
A one-step lookahead adds the best continuation of the same story (the catalog knows it).
"""

from __future__ import annotations

import random
from typing import Any

import replica as R


DEFAULT = dict(w_below=4.0, w_above=0.6, w_skill_hi=1.6, review_boost=3.0, w_h=0.6, w_d=0.5, h_floor=4, d_floor=5,
               w_wealth=0.7, risk_cost=1.2, risk_cap=3, w_cont=0.6, end_from=44, w_end=1.0, low_n_risk=1, defuse_at=2,
               laylow_at=3, unknown_pen=0.5)


class Planner(R.Policy):
    def __init__(self, **p: Any):
        self.p = dict(DEFAULT, **p)

    # ------------------------------------------------------------------ value
    def value(self, rep: R.Replica, st: R.State, fx: dict[str, float], dr: int) -> float:
        p = self.p
        lv = st.level
        t = R.THRESH.get(lv, R.THRESH[6])
        pre_review = st.month % 6 == 5
        endgame = st.month >= p["end_from"]
        v = 0.0
        for i, k in enumerate(R.GROWTH):
            x = fx.get(k, 0)
            cur = getattr(st, k)
            new = min(max(R.cap(lv, k), cur), cur + x) if x > 0 else max(R.MINS[k], cur + x)
            below = min(new, t[i]) - min(cur, t[i])
            above = (new - cur) - below
            wb = p["w_below"] * (p["review_boost"] if pre_review else 1.0)
            wa = p["w_above"] * (p["w_skill_hi"] if (k == "skill" and lv >= 4) else 1.0)
            if endgame:  # only the ending score counts now
                wb, wa = 0.0, {"skill": 0.15 * 100 / 120, "network": 0.1 * 100 / 60, "output": 0.0}[k] * (1 if new <= {"skill": 120, "network": 60, "output": 1e9}[k] else 0)
            v += wb * below + wa * above
        h = min(10, st.health + fx.get("health", 0))
        d = min(10, st.dignity + fx.get("dignity", 0))
        if endgame:
            v += 0.75 * p["w_end"] * ((h - st.health) + (d - st.dignity))
        else:
            v += p["w_h"] * (h - st.health) + p["w_d"] * (d - st.dignity)
        v -= 6 * max(0, p["h_floor"] - h) - 6 * max(0, p["h_floor"] - st.health)
        v -= 4 * max(0, p["d_floor"] - d) - 4 * max(0, p["d_floor"] - st.dignity)
        if h <= 0:
            v -= 1000
        if d < 4 and pre_review:
            v -= 30
        w = fx.get("wealth", 0)
        if w < 0:
            w *= (lv + 1) // 2
        v += p["w_wealth"] * w - 5 * max(0, -(st.wealth + w))
        r = st.risk + dr
        if r >= R.BLOW_AT:
            v -= 200 + 100 * st.blowups
        else:
            room = p["risk_cap"] - (1 if pre_review else 0)
            v -= p["risk_cost"] * dr + 6 * max(0, r - room) - 6 * max(0, st.risk - room)
            if endgame:
                v -= p["w_end"] * dr
        return v

    def _risk(self, rep: R.Replica, node: str, k: int) -> int:
        dr = rep.cat.answer_risk(node, k)
        n = rep.cat.nodes[node]["choices"][str(k)].get("n", 0)
        if n < 10:
            dr = max(dr, 0) + self.p["low_n_risk"]   # poorly measured answers: assume worse
        return dr

    def story(self, rep: R.Replica, st: R.State, node: str) -> int:
        best, bv = 1, -1e18
        n = rep.cat.nodes[node]
        for k, ch in n["choices"].items():
            k = int(k)
            dr = self._risk(rep, node, k)
            v = self.value(rep, st, ch["d"], dr)
            nxt = ch.get("next")
            if nxt and nxt in rep.cat.nodes:
                # best continuation from the state after this answer (ignoring caps of the next step)
                tmp = R.State(**{kk: vv for kk, vv in st.__dict__.items() if kk not in ("out_hist", "grades")})
                R.apply_delta(tmp, ch["d"])
                tmp.risk = max(0, tmp.risk + dr)
                cont = [self.value(rep, tmp, c2["d"], self._risk(rep, nxt, int(k2)))
                        for k2, c2 in rep.cat.nodes[nxt]["choices"].items()]
                if cont:
                    v += self.p["w_cont"] * max(cont)
            if v > bv:
                best, bv = k, v
        return best

    def energy(self, rep: R.Replica, st: R.State) -> str | None:
        p = self.p
        endgame = st.month >= p["end_from"]
        if st.health <= p["h_floor"] + 1 and st.energy >= 1 and st.health < 10:
            return "Health recovery"
        if st.risk >= p["defuse_at"] and st.energy >= 2:
            return "Defuse legacy risk"
        if endgame:
            if st.risk >= 1 and st.energy >= 2:
                return "Defuse legacy risk"
            if st.health < 10 and st.energy >= 1:
                return "Health recovery"
            if st.dignity < 10 and st.energy >= 1:
                return "Mental recovery"
        opts = []
        for a in ("Prepare report materials", "Network maintenance", "Skill learning", "Mental recovery", "Health recovery"):
            fx, cost = R.ENERGY_FX[a]
            if cost <= st.energy:
                opts.append((self.value(rep, st, fx, R.ACTION_RISK.get("q|" + a, 0)) / max(1, cost), a))
        if not opts:
            return None
        v, a = max(opts)
        return a if v > 0 else None

    def main(self, rep: R.Replica, st: R.State) -> str:
        if st.risk >= self.p["laylow_at"] or (st.month >= self.p["end_from"] and st.risk >= 1):
            return "Lay low and reduce risk"
        return max(R.MAIN_FX, key=lambda a: self.value(rep, st, R.MAIN_FX[a], R.ACTION_RISK.get("m|" + a, 0)))
