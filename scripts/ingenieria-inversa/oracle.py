"""Research "oracle" bot: plays with the dev-dataset effect model to reach late career stages.

It exists to *observe* the game far beyond month 6 (ceilings, reviews and failures at
L2-L9). It uses dataset knowledge (per-question answer effects), so nothing about it is
Skill material; the lessons drawn from its games are translated into general principles
separately. Lab parameters below (weights, margins) are bot settings, not game thresholds.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from careerlab.mcp_client import phase

from model import risk_level
from policies import DEFUSE, HEALTH, HIGH, MENTAL, NET_M, REPORT, SKILL_L, Base, affordable, by_action, reserve_choice

GROWTH = ("skill", "network", "output")
MAIN_FX = {  # measured in b00 (deterministic); see hallazgos H4
    "Apply for a key project": {"output": 2, "skill": 1, "network": 1},
    "Apply for rotation": {"skill": 2, "network": 1, "risk": 0.15},
    "Build a mentorship": {"skill": 1, "network": 2},
    "Fight for resources": {"output": 1, "network": 1, "risk": 0.15},
    "Report results to your manager": {"output": 1, "network": 1, "dignity": 1},
    "Showcase results": {"output": 1, "dignity": 1},
    "Repair a key relationship": {"network": 1, "dignity": 1},
    "Lay low and reduce risk": {"health": 1, "risk": -0.6},
}
ENERGY_FX = {HIGH: {"output": 2, "health": -1, "dignity": -1, "risk": 1}, SKILL_L: {"skill": 1, "health": -1},
             NET_M: {"network": 1, "dignity": 1}, DEFUSE: {"risk": -1}, MENTAL: {"dignity": 2},
             HEALTH: {"health": 2}, REPORT: {"output": 1, "dignity": 1}}
REVIEW_MONTHS = set(range(6, 49, 6))
# Promotion minima measured in b00+b01 (hallazgos H6). Research-bot settings, never Skill content.
THRESH = {1: {"skill": 8, "network": 3, "output": 3}, 2: {"skill": 18, "network": 6, "output": 5},
          3: {"skill": 35, "network": 18, "output": 14}, 4: {"skill": 90, "network": 33, "output": 22},
          5: {"skill": 130, "network": 45, "output": 33}}


def months_to_review(month: int) -> int:
    """Months of play left before the next review is applied (at the start of a review month)."""
    nxt = ((month // 6) + 1) * 6
    return nxt - month


class Oracle(Base):
    name = "oracle"

    @staticmethod
    def load_shared(model: str, **_: Any) -> dict[str, Any]:
        m = json.loads(Path(model).expanduser().read_text())
        caps = {int(k): v for k, v in m.get("ceil", {}).items()}
        return {"nodes": m["nodes"], "caps": caps, "name": Path(model).stem}

    def __init__(self, seed: int, shared: dict[str, Any] | None = None, model: str | None = None,
                 eps: float = 0.0, explore_from: int = 99, explore_to: int = 0, w_net: float = 2.0,
                 w_out: float = 2.0, w_skill: float = 1.0, risk_w: float = 1.5, gamma: float = 0.6,
                 health_floor: int = 5, blow_cost: float = 25.0, w_below: float = 3.0, review_boost: float = 1.0,
                 skill_focus_from: int = 99, w_skill_hi: float = 1.0, **params: Any):
        super().__init__(seed, eps=eps, explore_from=explore_from, explore_to=explore_to, w_net=w_net, w_out=w_out,
                         w_skill=w_skill, risk_w=risk_w, gamma=gamma, health_floor=health_floor, blow_cost=blow_cost,
                         w_below=w_below, review_boost=review_boost, skill_focus_from=skill_focus_from,
                         w_skill_hi=w_skill_hi, **params)
        self.sh = shared or {}
        self.nodes = self.sh.get("nodes", {})
        self.caps = self.sh.get("caps", {})
        self.p["model"] = self.sh.get("name")

    # ------------------------------------------------------------------ state helpers
    def cap(self, level: int, stat: str) -> float:
        c = self.caps.get(level, {})
        v = c.get(stat)
        if v and v > (self.caps.get(level - 1, {}).get(stat) or 0):
            return v
        return 1e9  # unknown level: treat as open

    def track(self, obs: dict[str, Any], ctx: dict[str, Any]) -> None:
        ev = obs.get("events") or ""
        if ev:
            lv = risk_level(ev)
            if lv is not None:
                ctx["risk"] = lv
            if "Old landmines" in ev:
                ctx["blowups"] = ctx.get("blowups", 0) + 1
                ctx["risk"] = 0

    def explore_now(self, month: int, kind: str = "story") -> bool:
        lo, hi = self.p["explore_from"], max(self.p["explore_to"], self.p["explore_from"])
        if lo <= month <= hi and self.p.get("explore_kind", "all") in ("all", kind):
            return True
        return self.p["eps"] > 0 and self.rng.random() < self.p["eps"]

    def decide(self, obs: dict[str, Any], ctx: dict[str, Any]) -> tuple[int, str]:
        self.track(obs, ctx)
        return super().decide(obs, ctx)

    # ------------------------------------------------------------------ value of a change
    def gain(self, st: dict[str, Any], d: dict[str, float], month: int, ctx: dict[str, Any]) -> float:
        lv = int(str(st["level"])[1:])
        v = 0.0
        w_skill = self.p["w_skill_hi"] if lv >= self.p["skill_focus_from"] else self.p["w_skill"]
        weights = {"skill": w_skill, "network": self.p["w_net"], "output": self.p["w_out"]}
        thr = THRESH.get(lv, {})
        for stat in GROWTH:
            x = st[stat]
            cap = self.cap(lv, stat)
            dx = d.get(stat, 0)
            new = min(cap, x + dx)
            old = min(cap, x)
            t = min(thr.get(stat, cap), cap)
            below = min(new, t) - min(old, t)          # progress (or loss) under the promotion minimum
            above = (new - old) - below                # progress between the minimum and the ceiling
            boost = self.p["review_boost"] if month % 6 == 5 else 1.0  # last month before a review
            v += weights[stat] * (self.p["w_below"] * boost * below + above)
        h, dg = st["health"], st["dignity"]
        dh, dd = d.get("health", 0), d.get("dignity", 0)
        nh, nd = min(10, h + dh), min(10, dg + dd)
        v += 0.6 * (self._hval(nh) - self._hval(h))
        v += 0.4 * (self._dval(nd) - self._dval(dg))
        w = st["wealth"]
        dw = d.get("wealth", 0)
        v += 0.3 * dw + (3.0 * min(0, w + dw) - 3.0 * min(0, w))
        r = d.get("risk", 0)
        pressure = 1 + 0.5 * ctx.get("risk", 0) + 3 * ctx.get("blowups", 0)
        if r:
            v -= self.p["risk_w"] * pressure * r
        bl = d.get("blow3", 0)
        if bl:
            v -= self.p["blow_cost"] * pressure * bl
        return v

    def _hval(self, h: float) -> float:
        floor = self.p["health_floor"]
        return h - 3.0 * max(0, floor - h) - 25.0 * max(0, 2 - h)

    def _dval(self, d: float) -> float:
        return d - 2.0 * max(0, 4 - d) - 15.0 * max(0, 1 - d)

    # ------------------------------------------------------------------ story events
    def option_fx(self, node: str, k: int) -> tuple[dict[str, float], int]:
        e = self.nodes.get(node, {}).get(str(k))
        if not e:
            return {}, 0
        d = dict(e["mean"])
        if "risk" in e and e.get("risk_n", 0) >= 3:
            d["risk"] = e["risk"]
        if "blow3" in e and e.get("blow_n", 0) >= 10:
            d["blow3"] = e["blow3"]
        return d, e["n"]

    def story(self, obs, choices, ctx):
        st = obs["current_state"]["status"]
        month = obs["current_state"]["time"]["current_month"]
        if self.explore_now(month):
            return self.rng.choice(choices)["choice"], "x"
        node = self._node_id(obs)
        best, best_v = None, -1e18
        for c in choices:
            d, n = self.option_fx(node, c["choice"])
            v = self.gain(st, d, month, ctx) if n else -0.5  # unknown answers: mildly avoided
            v += self.p["gamma"] * self._chain_value(node, c["choice"], st, d, month, ctx)
            if v > best_v:
                best, best_v = c, v
        return best["choice"], "g"

    def _chain_value(self, node: str, k: int, st, d, month, ctx) -> float:
        e = self.nodes.get(node, {}).get(str(k))
        if not e or not e.get("next"):
            return 0.0
        total = sum(e["next"].values())
        st2 = dict(st)
        for stat, dv in d.items():
            if stat in st2 and isinstance(st2[stat], (int, float)):
                st2[stat] = st2[stat] + dv
        val = 0.0
        for nxt, cnt in e["next"].items():
            opts = self.nodes.get(nxt, {})
            if not opts:
                continue
            vals = [self.gain(st2, o["mean"] | ({"risk": o["risk"]} if o.get("risk_n", 0) >= 3 else {})
                              | ({"blow3": o["blow3"]} if o.get("blow_n", 0) >= 10 else {}), month, ctx)
                    for o in opts.values()]
            val += cnt / total * max(vals)
        return val

    def _node_id(self, obs: dict[str, Any]) -> str:
        import hashlib
        ev = obs.get("current_event") or {}
        key = json.dumps([ev.get("title"), ev.get("description"), [c.get("action") for c in obs.get("choices") or []]],
                         ensure_ascii=False)
        return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]

    # ------------------------------------------------------------------ quarterly actions
    def energy(self, obs, choices, ctx):
        st = dict(obs["current_state"]["status"])
        month = obs["current_state"]["time"]["current_month"]
        if self.explore_now(month, "quarter"):
            return self.rng.choice(affordable(obs, choices))["choice"], "x"
        ok = by_action(affordable(obs, choices))
        spent = ctx["spent"].setdefault(month, [])
        left = (obs.get("current_event") or {}).get("remaining_energy", 0) or 0
        risk = ctx.get("risk", 0)
        # 1) health first (story events drain it between quarters)
        if st["health"] <= self.p["health_floor"] + 1 and HEALTH in ok and spent.count(HEALTH) < 2:
            spent.append(HEALTH)
            return ok[HEALTH]["choice"], "g"
        # 2) defuse when the HR remark is no longer calm, or after a blow-up
        if (risk >= 2 or (risk >= 1 and ctx.get("blowups", 0))) and DEFUSE in ok and spent.count(DEFUSE) < 1:
            spent.append(DEFUSE)
            return ok[DEFUSE]["choice"], "g"
        # 3) fill the largest gap to the current ceilings
        best, best_v = None, 0.05
        for name in (REPORT, NET_M, SKILL_L, MENTAL, HEALTH):
            if name not in ok:
                continue
            v = self.gain(st, ENERGY_FX[name], month, ctx) / max(1, ok[name].get("energy_cost") or 1)
            if v > best_v:
                best, best_v = name, v
        if best:
            spent.append(best)
            return ok[best]["choice"], "g"
        if risk >= 1 and DEFUSE in ok and DEFUSE not in spent:
            spent.append(DEFUSE)
            return ok[DEFUSE]["choice"], "g"
        if HEALTH in ok and st["health"] < 10:
            spent.append(HEALTH)
            return ok[HEALTH]["choice"], "g"
        return reserve_choice(choices), "g"

    def main(self, obs, choices, ctx):
        st = obs["current_state"]["status"]
        month = obs["current_state"]["time"]["current_month"]
        if self.explore_now(month, "quarter"):
            return self.rng.choice(choices)["choice"], "x"
        ok = by_action(choices)
        best, best_v = None, -1e9
        for name, fx in MAIN_FX.items():
            if name not in ok:
                continue
            v = self.gain(st, fx, month, ctx)
            if v > best_v:
                best, best_v = name, v
        if best is None:
            return choices[0]["choice"], "g"
        return ok[best]["choice"], "g"


class Principles(Oracle):
    """What general rules alone could achieve: answer effects come from a trait model fitted on other
    stories (out-of-fold predictions), ceilings are discovered in-run (a predicted gain that does not
    register means the stat is at its ceiling), and no promotion minimum is known in advance."""

    name = "principles"

    def __init__(self, seed: int, shared: dict[str, Any] | None = None, know_caps: bool = False,
                 know_thresholds: bool = False, **params: Any):
        super().__init__(seed, shared=shared, know_caps=know_caps, know_thresholds=know_thresholds, **params)
        if not know_caps:
            self.caps = {}

    def decide(self, obs, ctx):
        st = obs["current_state"]["status"]
        lv = int(str(st["level"])[1:])
        last = ctx.get("last")
        if last and not self.p["know_caps"]:
            before, pred, month = last
            if month == obs["current_state"]["time"]["current_month"] and int(str(before["level"])[1:]) == lv:
                for stat in GROWTH:
                    if pred.get(stat, 0) >= 1 and st[stat] - before[stat] < 0.5 and st[stat] >= before[stat]:
                        ctx.setdefault("caps", {})[(lv, stat)] = st[stat]
        choice, tag = super().decide(obs, ctx)
        pred = {}
        for c in obs.get("choices") or []:
            if c["choice"] == choice:
                # only quarterly actions have exactly known effects; a story answer's effect is a guess,
                # so a gain that does not register there says nothing reliable about a ceiling
                if c.get("status_updates"):
                    pred = {k.lower(): v for k, v in c["status_updates"].items()}
                elif phase(obs) == "main_action":
                    pred = MAIN_FX.get(c.get("action", ""), {})
        ctx["last"] = (dict(st), pred, obs["current_state"]["time"]["current_month"])
        ctx["_level"] = lv
        return choice, tag

    def cap(self, level: int, stat: str) -> float:
        if self.p["know_caps"]:
            return super().cap(level, stat)
        return self._ctx_caps.get((level, stat), 1e9) if hasattr(self, "_ctx_caps") else 1e9

    def new_game(self, game_id):
        ctx = super().new_game(game_id)
        self._ctx_caps = ctx.setdefault("caps", {})
        return ctx

    def gain(self, st, d, month, ctx):
        if self.p["know_thresholds"]:
            return super().gain(st, d, month, ctx)
        saved = THRESH.copy()
        try:
            THRESH.clear()  # no promotion minima: everything up to the (detected) ceiling counts as 'below'
            return super().gain(st, d, month, ctx)
        finally:
            THRESH.update(saved)


class Integrity(Principles):
    """Simplest general rule: pick the most principled answer (trait label), break ties by the
    trait-predicted growth value. Quarterly play is the same as the other bots."""

    name = "integrity"

    def story(self, obs, choices, ctx):
        st = obs["current_state"]["status"]
        month = obs["current_state"]["time"]["current_month"]
        if self.explore_now(month):
            return self.rng.choice(choices)["choice"], "x"
        node = self._node_id(obs)
        opts = self.nodes.get(node, {})
        def key(c):
            e = opts.get(str(c["choice"]), {})
            d, n = self.option_fx(node, c["choice"])
            return (e.get("integrity", 0), self.gain(st, d, month, ctx) if n else 0.0)
        return max(choices, key=key)["choice"], "g"
