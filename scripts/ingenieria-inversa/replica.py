"""Replica of the Career Survival engine, rebuilt only from black-box bot games (dev 1.0.8).

Research only: nothing here is Skill content. Every rule below was measured from the
answers of the five official tools in our own games (see
lab/reports/ingenieria-inversa/motor-exacto.md, sections M1-M14).

Two uses:
- `Replica` + `Catalog`: a generative simulator (draw events, apply answers, quarters,
  month changes, reviews, risk, explosions, failures, final score) to test strategies offline.
- `validate`: given the real state and decision of every step of recorded games, predict the
  next visible state, each review's promotion and the final score, and count the hits.

    python3 replica.py build --batches b00-random-safe,b01-oracle-eps --risk riskd.json --out catalog.json
    python3 replica.py validate --catalog catalog.json --batches v01-validation
    python3 replica.py play --catalog catalog.json --policy greedy --games 2000
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import random
import re
import sys
from dataclasses import dataclass, field
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------- rules (M1-M14)
CAPS = {1: {"skill": 9, "network": 3, "output": 3}, 2: {"skill": 21, "network": 7, "output": 6},
        3: {"skill": 42, "network": 21, "output": 16}, 4: {"skill": 108, "network": 36, "output": 26},
        5: {"skill": 154, "network": 54, "output": 38}, 6: {"skill": 220, "network": 72, "output": 54}, 7: {"skill": 300, "network": 90, "output": 70}}
MINS = {"health": 0, "dignity": 0, "skill": 1, "network": 0, "output": -1}
THRESH = {1: (8, 3, 3), 2: (18, 6, 5), 3: (35, 18, 14), 4: (90, 30, 22), 5: (130, 45, 32), 6: (170, 60, 45)}
SALARY = {1: 0.3, 2: 0.4, 3: 0.5, 4: 0.7, 5: 1.0, 6: 1.5, 7: 2.3, 8: 3.6, 9: 5.7, 10: 9.1}
BONUS = {"S": 3.0, "A": 2.0, "B": 1.0, "C": 0.25, "D": 0.0}
PROMO_NET = {1: 0, 2: 0, 3: -2, 4: -2, 5: -3, 6: -4}          # Network lost when promoted out of level L
TOOFAST_NET = {2: -3, 3: -3, 4: -3, 5: -3, 6: -3}  # extra when promoted after 6 months in L
MAIN_FX = {"Apply for a key project": {"output": 2, "skill": 1, "network": 1},
           "Report results to your manager": {"output": 1, "network": 1, "dignity": 1},
           "Fight for resources": {"output": 1, "network": 1},
           "Apply for rotation": {"skill": 2, "network": 1},
           "Showcase results": {"output": 1, "dignity": 1},
           "Build a mentorship": {"skill": 1, "network": 2},
           "Repair a key relationship": {"network": 1, "dignity": 1},
           "Lay low and reduce risk": {"health": 1}, "No action": {}}
ENERGY_FX = {"High-intensity work": ({"output": 2, "health": -1, "dignity": -1}, 2),
             "Skill learning": ({"skill": 1, "health": -1}, 2), "Network maintenance": ({"network": 1, "dignity": 1}, 1),
             "Defuse legacy risk": ({}, 2), "Mental recovery": ({"dignity": 2}, 1), "Health recovery": ({"health": 2}, 1),
             "Prepare report materials": ({"output": 1, "dignity": 1}, 1), "Reserve energy (no action)": ({}, 0)}
BLOW_AT = 5
DISPLAY = lambda w: math.floor(w + 1e-9)
DISP_LO, DISP_HI = 0.0, 0.99
PENALTY_EVERY_MONTH = False
ACTION_RISK = {"q|High-intensity work": 1, "q|Defuse legacy risk": -1, "m|Lay low and reduce risk": -1}
WARN_TONE = ("I had hopes", "The room feels tense", "HR marks the note")
PRAISE_TONE = ("Your manager closes", "To be honest, I worried", "The talk is shorter")
GROWTH = ("skill", "network", "output")
VIS = ("health", "dignity", "skill", "network", "level", "duration_in_level", "output", "wealth", "energy")


@dataclass
class State:
    health: float = 5
    dignity: float = 5
    skill: float = 1
    network: float = 1
    level: int = 1
    duration_in_level: int = 1
    output: float = 0
    wealth: float = 1.0
    energy: int = 3
    month: int = 1
    risk: int = 0                 # hidden risk (the HR remark shows min(risk, 4))
    blowups: int = 0
    out_hist: dict = field(default_factory=dict)   # Output at the start of each month (M4)
    neg_wealth_months: int = 0
    zero_net_months: int = 0
    low_dig_months: int = 0
    grades: list = field(default_factory=list)
    alive: bool = True
    failure: str | None = None

    def vis(self) -> list:
        return [self.health, self.dignity, self.skill, self.network, self.level, self.duration_in_level,
                self.output, DISPLAY(self.wealth), self.energy]


def cap(level: int, stat: str) -> float:
    return CAPS.get(level, CAPS[6]).get(stat, 1e9)


def apply_delta(st: State, d: dict[str, float]) -> None:
    """M3: per-stat bounds; a Skill loss at the floor turns into Dignity -1 and Output -1."""
    d = dict(d)
    if "skill" in d and st.skill + d["skill"] < MINS["skill"]:
        d["dignity"] = d.get("dignity", 0) - 1
        d["output"] = d.get("output", 0) - 1
    for k, x in d.items():
        if k == "wealth":
            st.wealth = round(st.wealth + x, 1)
            continue
        if k not in ("health", "dignity", "skill", "network", "output"):
            continue
        v = getattr(st, k) + x
        if k in ("health", "dignity"):
            v = min(10, v)
        if k in GROWTH and x > 0:
            v = min(v, max(cap(st.level, k), getattr(st, k)))
        v = max(MINS[k], v)
        setattr(st, k, v)


def explode(st: State) -> None:
    """M4: Dignity -2, Wealth -2, Output back to its value at the start of month m-5; risk reset."""
    st.blowups += 1
    st.dignity = max(0, st.dignity - 2)
    st.wealth = round(st.wealth - 2, 3)
    st.output = st.out_hist.get(st.month - 5, 0)
    st.risk = 0
    if st.blowups >= 2:
        st.alive, st.failure = False, "trust"


# ----------------------------------------------------------------------------- grade model (M11)
GRADE_FEATS = ("S/c", "N/c", "O/c", "S/t", "N/t", "O/t", "dur", "R", "D", "H", "nblow", "blow_now")


def grade_features(st: State, blow_now: bool) -> list[float]:
    c = CAPS.get(st.level, CAPS[6])
    t = THRESH.get(st.level, THRESH[6])
    return [st.skill / c["skill"], st.network / c["network"], st.output / c["output"], st.skill / t[0],
            st.network / t[1], st.output / t[2], st.duration_in_level, st.risk, st.dignity, st.health,
            st.blowups, int(blow_now)]


class GradeModel:
    """Per-level multinomial logistic model fitted on review states (dev games)."""

    def __init__(self, params: dict[str, Any]):
        self.p = params

    def grade(self, st: State, blow_now: bool = False) -> str:
        lv = str(min(st.level, 5))
        m = self.p.get(lv)
        if not m:
            return "B"
        x = grade_features(st, blow_now)
        if len(m["classes"]) == 2:
            z = sum(a * b for a, b in zip(m["coef"][0], x)) + m["intercept"][0]
            return m["classes"][1] if z > 0 else m["classes"][0]
        best, bv = None, -1e18
        for cl, co, ic in zip(m["classes"], m["coef"], m["intercept"]):
            z = sum(a * b for a, b in zip(co, x)) + ic
            if z > bv:
                best, bv = cl, z
        return best


# ----------------------------------------------------------------------------- catalog
class Catalog:
    def __init__(self, data: dict[str, Any]):
        self.d = data
        self.nodes = data["nodes"]
        self.risk = data.get("risk", {})
        self.grade = GradeModel(data.get("grade", {}))
        self.tone = data.get("tone", {})
        self.pools = data.get("pools", {})

    def effect(self, node: str, k: int) -> dict[str, float] | None:
        n = self.nodes.get(node)
        if not n:
            return None
        c = n["choices"].get(str(k))
        return c["d"] if c else None

    def answer_risk(self, node: str, k: int) -> int:
        return self.risk.get(f"E|{node}|{k}", 0)


# ----------------------------------------------------------------------------- engine
class Replica:
    def __init__(self, cat: Catalog, rng: random.Random | None = None):
        self.cat = cat
        self.rng = rng or random.Random(0)

    # ---- decisions
    def answer(self, st: State, node: str, k: int) -> None:
        d = dict(self.cat.effect(node, k) or {})
        if d.get("wealth", 0) < 0:
            d["wealth"] *= (st.level + 1) // 2      # M13: losses x1 (L1-2), x2 (L3-4), x3 (L5-6)
        apply_delta(st, d)
        st.risk = max(0, st.risk + self.cat.answer_risk(node, k))
        self._maybe_explode(st)
        self._check_health(st)

    def energy_action(self, st: State, name: str) -> None:
        fx, cost = ENERGY_FX.get(name, ({}, 0))
        apply_delta(st, fx)
        st.energy -= cost
        st.risk = max(0, st.risk + ACTION_RISK.get("q|" + name, 0))
        self._maybe_explode(st)
        self._check_health(st)

    def main_action(self, st: State, name: str) -> None:
        apply_delta(st, MAIN_FX.get(name, {}))
        st.risk = max(0, st.risk + ACTION_RISK.get("m|" + name, 0))

    @staticmethod
    def _maybe_explode(st: State) -> bool:
        """M10: the buried risk goes off as soon as hidden risk reaches 5."""
        if st.risk >= BLOW_AT and st.alive:
            explode(st)
            return True
        return False

    def _check_health(self, st: State) -> None:
        if st.health <= 0 and st.alive:
            st.alive, st.failure = False, "health"

    # ---- month change (M1, M6, M7)
    def month_change(self, st: State, explosion: bool | None = None) -> dict[str, Any]:
        """Advance from month m to m+1. `explosion` forces the month-start blow-up (None = draw it)."""
        info: dict[str, Any] = {}
        st.month += 1
        st.duration_in_level += 1
        # persistent-condition counters (M15): checked on the state before the salary
        st.neg_wealth_months = st.neg_wealth_months + 1 if st.wealth < 0 else 0
        st.zero_net_months = st.zero_net_months + 1 if st.network <= 0 else 0
        st.low_dig_months = st.low_dig_months + 1 if st.dignity <= 1 else 0
        st.wealth = round(st.wealth + SALARY[st.level], 1)
        review = st.month % 6 == 0
        if review:
            info.update(self.review(st, explosion_now=bool(explosion)))
        # warnings: shown once, at the 3rd month of the condition; failure at the 6th (M15)
        pen = (lambda n: n >= 3) if PENALTY_EVERY_MONTH else (lambda n: n == 3)
        if pen(st.neg_wealth_months):
            apply_delta(st, {"dignity": -1})
        if pen(st.zero_net_months):
            apply_delta(st, {"health": -1, "dignity": -1, "output": -2})
        if pen(st.low_dig_months):
            apply_delta(st, {"health": -2, "network": -1})
        # month-start explosion (M10): deterministic once hidden risk reaches 5
        info["explosion"] = self._maybe_explode(st) if explosion is None or explosion else False
        st.out_hist[st.month] = st.output
        if st.alive:
            if st.neg_wealth_months >= 6:
                st.alive, st.failure = False, "broke"
            elif st.zero_net_months >= 6:
                st.alive, st.failure = False, "isolated"
            elif st.low_dig_months >= 6:
                st.alive, st.failure = False, "breakdown"
        self._check_health(st)
        return info

    def review(self, st: State, explosion_now: bool = False) -> dict[str, Any]:
        """M7, M11: grade, talk tone, bonus, promotion and its Network cost."""
        g = self.cat.grade.grade(st, explosion_now)
        st.grades.append(g)
        st.wealth = round(st.wealth + BONUS[g] * SALARY[st.level], 1)
        tone = "warn" if g in ("C", "D") and self._warn(st, g) else ("praise" if g == "A" else "neu")
        t = THRESH.get(st.level)
        meets = bool(t) and st.skill >= t[0] and st.network >= t[1] and st.output >= t[2]
        promoted = meets and st.dignity >= 4 and g != "D"
        fast = promoted and st.duration_in_level <= 7 and st.level in TOOFAST_NET
        if tone == "warn":
            apply_delta(st, {"health": -1, "dignity": -2})
            st.risk += 1
        elif tone == "praise":
            apply_delta(st, {"dignity": 2, "network": 1})
        else:
            apply_delta(st, {"dignity": 1})
        if g == "D" and st.level == 1:
            apply_delta(st, {"dignity": -3, "network": -1})   # "This half-year review fell short"
        if fast:
            apply_delta(st, {"dignity": -1})
        if promoted:
            st.network = max(0, st.network + PROMO_NET.get(st.level, -3) + (TOOFAST_NET[st.level] if fast else 0))
            st.level += 1
            st.duration_in_level = 1
        if st.level == 1 and st.month >= 24 and st.alive:
            st.alive, st.failure = False, "dismissed"
        return {"grade": g, "tone": tone, "promoted": promoted}

    def _warn(self, st: State, g: str) -> bool:
        """M24: the talk warns exactly when 4*Dignity + Health < 22 + 8*risk + 16*blow-ups (C grades;
        100 % of 10,216 reviews). D grades always warn."""
        if g == "D":
            return True
        return 4 * st.dignity + st.health < 22 + 8 * st.risk + 16 * st.blowups

    # ---- ending (H11)
    @staticmethod
    def score(st: State) -> float:
        lv = 10 * st.level
        w = min(100, max(0, st.wealth) / 80 * 100)
        hd = min(100, (st.health + st.dignity) / 20 * 100)
        sk = min(100, st.skill / 120 * 100)
        rk = max(0, (10 - (st.risk + 5 * st.blowups if st.failure != "trust" else 10)) * 10)
        nw = min(100, st.network / 60 * 100)
        return round(0.3 * lv + 0.2 * w + 0.15 * hd + 0.15 * sk + 0.1 * rk + 0.1 * nw, 2)


# ----------------------------------------------------------------------------- build
def key(s, e) -> str:
    if s[1] == "e":
        return "E|" + s[2] + "|" + str(s[3])
    return s[1] + "|" + e["chosen"]


def build(batches: list[str], risk_path: str | None) -> dict[str, Any]:
    import tl
    from bbdata import Batch
    b = Batch(*batches)
    eff: dict[tuple[str, int], collections.Counter] = collections.defaultdict(collections.Counter)
    nxt: dict[tuple[str, int], collections.Counter] = collections.defaultdict(collections.Counter)
    pools: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    first_node: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for g in b.games():
        r = tl.timeline(b, g)
        if r is None:
            continue
        out = r[1]
        seen_titles: set[str] = set()
        for i, (s, e, a) in enumerate(out):
            if s[1] != "e":
                continue
            eff[(s[2], s[3])][json.dumps(e["d"], sort_keys=True)] += 1
            t = e["title"]
            if t not in seen_titles:
                seen_titles.add(t)
                pools[s[4][4]][t] += 1
                first_node[t][s[2]] += 1
            done = any(c == "E" for c, _ in a)
            if not done:
                for j in range(i + 1, len(out)):
                    s2, e2, _ = out[j]
                    if s2[1] == "e" and e2["title"] == t:
                        nxt[(s[2], s[3])][(s2[2], "same" if s2[0] == s[0] else "next")] += 1
                        break
    nodes: dict[str, Any] = {}
    for (node, k), c in eff.items():
        meta = b.nodes.get(node, {})
        n = nodes.setdefault(node, {"title": meta.get("title"), "n_choices": len(meta.get("choices") or []), "choices": {}})
        d = json.loads(c.most_common(1)[0][0])
        ch = {"d": d, "n": sum(c.values())}
        if nxt[(node, k)]:
            (nn, when), cnt = nxt[(node, k)].most_common(1)[0]
            ch["next"], ch["when"] = nn, when
        n["choices"][str(k)] = ch
    risk = json.load(open(risk_path)) if risk_path else {}
    return {"batches": batches, "nodes": nodes, "risk": {k: v for k, v in risk.items() if v},
            "pools": {str(k): dict(v) for k, v in pools.items()},
            "first_node": {t: c.most_common(1)[0][0] for t, c in first_node.items()},
            "p_blow_month": 0.27}


def fit_reviews(batches: list[str], cat: dict[str, Any]) -> None:
    """Fit the grade and warning-tone models on the review states of the discovery batches."""
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    rows = collect_reviews(batches, Catalog(cat))
    cat["grade"], cat["tone"] = {}, {}
    for lv in range(1, 6):
        sub = [r for r in rows if r["level"] == lv]
        if len(sub) < 10:
            continue
        X = np.array([r["x"] for r in sub])
        y = [r["grade"] for r in sub]
        if len(set(y)) >= 2:
            m = LogisticRegression(max_iter=5000, C=100).fit(X, y)
            cat["grade"][str(lv)] = {"classes": list(m.classes_), "coef": m.coef_.tolist(), "intercept": m.intercept_.tolist()}
        else:
            cat["grade"][str(lv)] = {"classes": [y[0], y[0]], "coef": [[0] * X.shape[1]], "intercept": [-1]}
        cs = [r for r in sub if r["grade"] == "C"]
        if len(cs) >= 10 and len(set(r["tone"] == "warn" for r in cs)) == 2:
            Xc = np.array([r["x"] for r in cs])
            yc = [int(r["tone"] == "warn") for r in cs]
            m = LogisticRegression(max_iter=5000, C=100).fit(Xc, yc)
            cat["tone"][str(lv)] = {"coef": m.coef_[0].tolist(), "intercept": float(m.intercept_[0])}


# ----------------------------------------------------------------------------- replay helpers
def obs_state(vec: list, month: int) -> State:
    return State(health=vec[0], dignity=vec[1], skill=vec[2], network=vec[3], level=vec[4], duration_in_level=vec[5],
                 output=vec[6], wealth=float(vec[7]), energy=vec[8], month=month)


def decide_apply(rep: Replica, st: State, s, e) -> None:
    if s[1] == "e":
        rep.answer(st, s[2], s[3])
    elif s[1] == "q":
        rep.energy_action(st, e["chosen"])
    elif s[1] == "m":
        rep.main_action(st, e["chosen"])


def collect_reviews(batches: list[str], cat: Catalog) -> list[dict[str, Any]]:
    """State just before each review (risk tracked by the replica, synced to the HR remark)."""
    import tl
    from bbdata import Batch
    b = Batch(*batches)
    rep = Replica(cat)
    rows = []
    for g in b.games():
        r = tl.timeline(b, g)
        if r is None:
            continue
        out = r[1]
        R, nb = 0, 0
        for i, (s, e, a) in enumerate(out):
            t = b.texts.get(s[5], "") if s[5] else ""
            if i > 0 and s[0] != out[i - 1][0][0] and "Half-year talk" in t:
                ps, pe, _ = out[i - 1]
                st = obs_state(ps[4], ps[0])
                decide_apply(rep, st, ps, pe)
                st.risk, st.blowups = R, nb
                gm = re.search(r"bonus \((\w)\)", t)
                tone = "warn" if any(x in t for x in WARN_TONE) else ("praise" if any(x in t for x in PRAISE_TONE) else "neu")
                rows.append({"g": g["g"], "month": s[0], "level": st.level, "x": grade_features(st, "Old landmines" in t),
                             "grade": gm.group(1) if gm else "?", "tone": tone, "promo": s[4][4] > ps[4][4]})
            h = hr_level(t)
            if h is not None and h < 4:
                R = h
            if "Old landmines" in t:
                R, nb = 0, nb + 1
            R = max(0, R + step_risk(cat, s, e))
    return rows


def step_risk(cat: Catalog, s, e) -> int:
    k = key(s, e)
    return cat.risk.get(k, 0) if s[1] == "e" else ACTION_RISK.get(k, 0)


HR_WORDS = (("smiling", 0), ("quietly", 1), ("frowning", 2), ("uneasy", 3), ("angry", 4))


def hr_level(t: str) -> int | None:
    m = re.search(r"An HR partner you get on with says,? (\w+)", t or "")
    if not m:
        return None
    for w, lv in HR_WORDS:
        if m.group(1).startswith(w):
            return lv
    return None


DEBUG: collections.Counter | None = None

# ----------------------------------------------------------------------------- validation
def validate(cat: Catalog, batches: list[str], verbose: bool = True) -> dict[str, Any]:
    """One-step prediction on recorded games: the replica gets the observed state and the decision
    of each step (plus what the player sees: HR remark, blow-up notices) and predicts the next state."""
    import tl
    from bbdata import Batch
    b = Batch(*batches)
    rep = Replica(cat, random.Random(1))
    steps = hits = 0
    field_miss: collections.Counter = collections.Counter()
    kind_miss: collections.Counter = collections.Counter()
    rev_n = rev_hit = 0
    rev_conf: collections.Counter = collections.Counter()
    score_err: list[float] = []
    by_phase: dict[str, list[int]] = {}
    games = 0
    for g in b.games():
        if g["outcome"] not in ("eliminated", "completed"):
            continue
        r = tl.timeline(b, g)
        if r is None:
            continue
        games += 1
        out = r[1]
        W, R, nb = 1.0, 0, 0
        Wlo = Whi = 1.0  # interval of the true wealth consistent with every displayed (floored) value
        out_hist: dict[int, float] = {}
        counters = (0, 0, 0)
        for i, (s, e, a) in enumerate(out):
            t = b.texts.get(s[5], "") if s[5] else ""
            if i == 0 or s[0] != out[i - 1][0][0]:
                out_hist.setdefault(s[0], s[4][6])
            h = hr_level(t)
            if h is not None and h < 4:
                R = h
            if "Old landmines" in t:
                R, nb = 0, nb + 1
            st = obs_state(s[4], s[0])
            W = (Wlo + Whi) / 2
            st.wealth, st.risk, st.blowups, st.out_hist = W, R, nb, dict(out_hist)
            st.neg_wealth_months, st.zero_net_months, st.low_dig_months = counters
            decide_apply(rep, st, s, e)
            info = {}
            last = i + 1 >= len(out)
            nxt = None if last else out[i + 1][0]
            if nxt is not None and s[1] == "e" and nxt[1] == "q":
                st.energy = 3  # the quarter phase opens with 3 Energy
            if nxt is not None and nxt[0] != s[0]:
                info = rep.month_change(st)
                if "promoted" in info:
                    actual = nxt[4][4] > s[4][4]
                    rev_n += 1
                    rev_hit += int(info["promoted"] == actual)
                    rev_conf[(info["promoted"], actual)] += 1
            R = st.risk
            counters = (st.neg_wealth_months, st.zero_net_months, st.low_dig_months)
            if nxt is not None:
                pred = st.vis()
                obs = list(nxt[4])
                steps += 1
                nt = b.texts.get(nxt[5], "") if nxt[5] else ""
                ok = all(abs(p - o) < 1e-6 for p, o in zip(pred, obs))
                hits += int(ok)
                by_phase.setdefault(s[1], [0, 0])
                by_phase[s[1]][0] += 1
                by_phase[s[1]][1] += int(ok)
                if not ok:
                    for name, p, o in zip(VIS, pred, obs):
                        if abs(p - o) > 1e-6:
                            field_miss[name] += 1
                    kind_miss[("blowup" if "Old landmines" in nt else "") + ("|month" if nxt[0] != s[0] else "|in-month") + "|" + s[1]] += 1
                    if DEBUG is not None:
                        diff = tuple((nm, round(o - p, 2)) for nm, p, o in zip(VIS, pred, obs) if abs(p - o) > 1e-6)
                        tg = tuple(x for x in ("Old landmines", "Payday", "nobody asks", "self-respect", "fell short", "climbed too fast", "Half-year talk", "jargon") if x in nt)
                        DEBUG[(s[1], nxt[0] != s[0], tg, diff)] += 1
                # wealth: keep the replica's fraction, resync the integer part if it drifted
                dw = st.wealth - W
                Wlo, Whi = max(Wlo + dw, obs[7] + DISP_LO), min(Whi + dw, obs[7] + DISP_HI)
                if Wlo > Whi + 1e-9:
                    Wlo, Whi = obs[7] + DISP_LO, obs[7] + DISP_HI
                W = (Wlo + Whi) / 2
        # final score from the last observed state and the replica's hidden risk
        fin = g["final"]["s"]
        stf = obs_state(fin, g["final"]["t"])
        stf.wealth, stf.risk, stf.blowups = W, R, nb
        if (g["final"]["flags"].get("failure_reason") or "").startswith("Trust crisis"):
            stf.failure, stf.blowups = "trust", max(2, nb)
        q = g["end"]["q"]
        if q is not None:
            score_err.append(abs(Replica.score(stf) - q))
    res = {"games": games, "steps": steps, "step_acc": hits / max(1, steps), "reviews": rev_n,
           "promo_acc": rev_hit / max(1, rev_n), "score_mae": sum(score_err) / max(1, len(score_err)),
           "score_within_2": sum(1 for x in score_err if x <= 2) / max(1, len(score_err)),
           "field_miss": dict(field_miss.most_common()), "kind_miss": dict(kind_miss.most_common(12)),
           "promo_confusion": {f"pred={k[0]} real={k[1]}": v for k, v in rev_conf.items()},
           "by_phase": {k: {"steps": v[0], "acc": v[1] / max(1, v[0])} for k, v in by_phase.items()},
           "score_err_max": max(score_err) if score_err else None}
    if verbose:
        print(json.dumps(res, indent=1))
        print(table(res, batches))
    return res


def table(res: dict[str, Any], batches: list[str]) -> str:
    ph = res["by_phase"]
    names = {"e": "respuestas a eventos", "q": "acciones de energía", "m": "acción principal"}
    rows = [f"| Lote | {', '.join(batches)} ({res['games']} partidas) | |", "|---|---:|---|",
            f"| Estado exacto tras cada paso (todos) | {res['step_acc']:.1%} de {res['steps']} pasos | objetivo ≥ 95 % |"]
    for k in ("e", "q", "m"):
        if k in ph:
            rows.append(f"| … tras {names[k]} | {ph[k]['acc']:.1%} de {ph[k]['steps']} | |")
    rows += [f"| Ascenso sí/no en cada evaluación | {res['promo_acc']:.1%} de {res['reviews']} evaluaciones | objetivo ≥ 95 % |",
             f"| Error medio de la nota final | {res['score_mae']:.2f} puntos (máx. {res['score_err_max']:.2f}; ≤2 en el {res['score_within_2']:.1%}) | objetivo ≤ 2 |"]
    return "\n".join(rows)


# ----------------------------------------------------------------------------- generative play
class Policy:
    """Interface for replica policies: story(st, node) -> k, energy(st, left) -> name|None, main(st) -> name."""
    def story(self, rep: "Replica", st: State, node: str) -> int: ...
    def energy(self, rep: "Replica", st: State) -> str | None: ...
    def main(self, rep: "Replica", st: State) -> str: ...


def draw_title(cat: Catalog, st: State, used: set[str], rng: random.Random) -> str | None:
    """M18: titles unlock in blocks at the start of a semester (months 1, 6, 12, 18, 24, 30) whatever the
    level; the draw is close to uniform among unlocked unused titles. Stories that carry over to the next
    month weigh ~0.6 (only one long story may be open at a time)."""
    smp = cat.d.get("sampler")
    if smp:
        pool = {t: smp["weight"][t] for t, (m0, _m1) in smp["window"].items()
                if m0 <= st.month and t not in used and t in cat.d["first_node"]}
    else:
        lv = st.level
        while str(lv) not in cat.pools and lv > 1:
            lv -= 1
        pool = {t: w for t, w in cat.pools.get(str(lv), {}).items() if t not in used and t in cat.d["first_node"]}
    if not pool:
        return None
    tot = sum(pool.values())
    x = rng.random() * tot
    for t, w in pool.items():
        x -= w
        if x <= 0:
            return t
    return t


def play(cat: Catalog, policy: Policy, rng: random.Random, months: int = 48,
         settle_completion: bool = True) -> tuple[State, list]:
    """One whole career in the replica: 3 event decisions a month, quarter phases, month changes."""
    rep = Replica(cat, rng)
    st = State()
    st.out_hist[1] = st.output
    used: set[str] = set()
    pending: list[str] = []
    trace: list = []
    for month in range(1, months + 1):
        queue, pending, slots = pending, [], 3
        while slots > 0 and st.alive:
            if queue:
                node = queue.pop(0)
            else:
                t = draw_title(cat, st, used, rng)
                if t is None:
                    break
                used.add(t)
                node = cat.d["first_node"][t]
            while st.alive:
                n = cat.nodes.get(node)
                if not n or not n["choices"]:
                    break
                k = policy.story(rep, st, node)
                rep.answer(st, node, k)
                trace.append((month, "e", node, k))
                slots -= 1
                ch = n["choices"].get(str(k), {})
                if "next" in ch:
                    if ch.get("when") == "same" and slots > 0:
                        node = ch["next"]
                        continue
                    pending.append(ch["next"])
                break
        if not st.alive:
            break
        if month % 3 == 0:
            st.energy = 3
            while st.alive:
                a = policy.energy(rep, st)
                if not a or ENERGY_FX.get(a, ({}, 9))[1] > st.energy:
                    break
                rep.energy_action(st, a)
                trace.append((month, "q", a))
            if not st.alive:
                break
            a = policy.main(rep, st)
            rep.main_action(st, a)
            trace.append((month, "m", a))
        if month == months:
            # The official completion state is month 49: the last action settles
            # month 48's salary and monthly conditions before the ending score.
            # Short research horizons stop at their requested decision boundary.
            if months == 48 and st.alive and settle_completion:
                rep.month_change(st)
            break
        info = rep.month_change(st)
        if info.get("grade"):
            trace.append((st.month, "r", info))
        if not st.alive:
            break
    return st, trace


GROW_W = {"skill": 1.0, "network": 1.0, "output": 1.0}


class Greedy(Policy):
    """One-step greedy on the replica's own rules (a baseline, not an optimum)."""

    def __init__(self, risk_cap: int = 3, w=None):
        self.risk_cap, self.w = risk_cap, w or GROW_W

    def value(self, rep: Replica, st: State, fx: dict[str, float], dr: int) -> float:
        v = 0.0
        t = THRESH.get(st.level, THRESH[6])
        for i, k in enumerate(GROWTH):
            x = fx.get(k, 0)
            cur = getattr(st, k)
            new = min(max(cap(st.level, k), cur), cur + x) if x > 0 else max(MINS[k], cur + x)
            below = min(new, t[i]) - min(cur, t[i])
            v += self.w[k] * (3 * below + (new - cur - below))
        h = min(10, st.health + fx.get("health", 0))
        d = min(10, st.dignity + fx.get("dignity", 0))
        v += 0.5 * (h - st.health) + 0.4 * (d - st.dignity) - 4 * max(0, 3 - h) - 3 * max(0, 4 - d)
        w = fx.get("wealth", 0) * (((st.level + 1) // 2) if fx.get("wealth", 0) < 0 else 1)
        v += 0.6 * w - 4 * max(0, -(st.wealth + w))
        r = st.risk + dr
        v -= 1.5 * dr + (40 if r >= BLOW_AT else 0) + (8 * max(0, r - self.risk_cap))
        return v

    def story(self, rep, st, node):
        best, bv = 1, -1e18
        for k, ch in rep.cat.nodes[node]["choices"].items():
            v = self.value(rep, st, ch["d"], rep.cat.answer_risk(node, int(k)))
            if v > bv:
                best, bv = int(k), v
        return best

    def energy(self, rep, st):
        if st.health <= 5 and st.energy >= 1:
            return "Health recovery"
        if st.risk >= 2 and st.energy >= 2:
            return "Defuse legacy risk"
        opts = [(self.value(rep, st, ENERGY_FX[a][0], ACTION_RISK.get("q|" + a, 0)) / max(1, ENERGY_FX[a][1]), a)
                for a in ("Prepare report materials", "Network maintenance", "Skill learning", "Mental recovery", "Health recovery")
                if ENERGY_FX[a][1] <= st.energy]
        if not opts:
            return None
        v, a = max(opts)
        return a if v > 0 else None

    def main(self, rep, st):
        if st.risk >= 3:
            return "Lay low and reduce risk"
        return max(MAIN_FX, key=lambda a: self.value(rep, st, MAIN_FX[a], ACTION_RISK.get("m|" + a, 0)))


def simulate(cat: Catalog, policy: Policy, games: int, seed: int = 0) -> dict[str, Any]:
    scores, levels, fails = [], collections.Counter(), collections.Counter()
    for i in range(games):
        st, _ = play(cat, policy, random.Random(seed + i))
        scores.append(Replica.score(st))
        levels[st.level] += 1
        fails[st.failure or "completed"] += 1
    return {"games": games, "mean": round(sum(scores) / games, 2), "max": max(scores),
            "levels": dict(sorted(levels.items())), "outcomes": dict(fails)}


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--batches", required=True)
    p.add_argument("--risk")
    p.add_argument("--out", required=True)
    p = sub.add_parser("validate")
    p.add_argument("--catalog", required=True)
    p.add_argument("--batches", required=True)
    p = sub.add_parser("play")
    p.add_argument("--catalog", required=True)
    p.add_argument("--games", type=int, default=500)
    a = ap.parse_args()
    if a.cmd == "build":
        cat = build(a.batches.split(","), a.risk)
        fit_reviews(a.batches.split(","), cat)
        json.dump(cat, open(a.out, "w"))
        print(json.dumps({"nodes": len(cat["nodes"]), "answers": sum(len(n["choices"]) for n in cat["nodes"].values()),
                          "risk_keys": len(cat["risk"]), "grade_levels": list(cat["grade"]), "tone_levels": list(cat["tone"])}))
    elif a.cmd == "validate":
        validate(Catalog(json.load(open(a.catalog))), a.batches.split(","))
    elif a.cmd == "play":
        print(json.dumps(simulate(Catalog(json.load(open(a.catalog))), Greedy(), a.games)))


if __name__ == "__main__":
    main()
