"""Parametric policies and actor models for SynthCareer.

A *policy* is an interpretable parameter vector ``theta`` (see ``THETA_SPACE``)
executed by ``ParamPolicy``, which decides from what a player sees only: the
visible statistics, the listed choices with their ``energy_cost`` and
``status_updates``, and the ``events`` feedback text (warnings, review grades,
reviewer comments). It reads story options and feedback through a small keyword
vocabulary of SynthCareer's own templates, never through hidden state.

An *actor model* executes a policy imperfectly, which is problem (A): the
actor that will run a policy in competition is not the actor used to evaluate
it in development.

- capability: each time a rule's condition fires, the actor executes it with
  probability ``1 - miss`` where ``miss = miss_base + miss_per_rule *
  complexity(theta)`` (capped), so complex policies degrade more;
- slips: with probability ``slip`` a uniformly random valid choice;
- bias: ``caution`` replaces options with a shown Health/Dignity cost by
  recovery and overwork-style story options by rest/decline; ``eager``
  over-accepts extra work and replaces recovery by high-intensity work.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from typing import Any, Protocol

from careerlab.synthetic import game as g
from careerlab.synthetic.game import (DONE, ENERGY, ENERGY_COST, ENERGY_FINISH, MAIN, MAIN_NONE, STORY, View)


class UniformRng(Protocol):
    """Anything with ``random()`` in [0, 1): random.Random or numpy.random.Generator."""

    def random(self) -> float: ...


# ---------------------------------------------------------------------------
# Parameter space
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Param:
    kind: str  # "int" | "float" | "choice"
    low: float = 0.0
    high: float = 1.0
    choices: tuple[str, ...] = ()
    default: Any = None
    group: str = ""
    doc: str = ""


THETA_SPACE: dict[str, Param] = {
    "health_floor": Param("int", 0, 8, default=4, group="recovery",
                          doc="Recover Health first (energy and main action) when Health <= this; 0 disables the rule."),
    "dignity_floor": Param("int", 0, 8, default=3, group="recovery",
                           doc="Spend on Dignity recovery / relationship repair when Dignity <= this; 0 disables."),
    "invest_build": Param("float", 0.0, 1.0, default=0.85, group="invest",
                          doc="Share of free quarterly Energy spent on Skill/Network while in build mode."),
    "invest_deliver": Param("float", 0.0, 1.0, default=0.15, group="invest",
                            doc="Share of free quarterly Energy spent on Skill/Network while in deliver mode."),
    "network_share": Param("float", 0.0, 1.0, default=0.35, group="invest",
                           doc="Part of the investment that goes to Network rather than Skill."),
    "visibility_pref": Param("float", 0.0, 1.0, default=0.3, group="invest",
                             doc="Deliver-mode main action weight on Dignity/Network next to Output (showcase vs fight)."),
    "overtime_rule": Param("choice", choices=("never", "if_healthy", "always"), default="if_healthy", group="overtime",
                           doc="Accept extra-work story options never, while delivering with Health >= overtime_health, or always."),
    "overtime_health": Param("int", 1, 10, default=6, group="overtime", doc="Health needed for if_healthy overtime."),
    "risk_reaction": Param("choice", choices=("ignore", "defuse", "lay_low"), default="defuse", group="risk",
                           doc="Reaction to risk warnings in the feedback text: none, Defuse legacy risk, or Lay low."),
    "risk_warnings": Param("int", 1, 3, default=1, group="risk",
                           doc="Warnings within the last 6 months needed to trigger the reaction."),
    "switch_rule": Param("choice", choices=("none", "calendar", "state", "feedback"), default="state", group="switch",
                         doc="How build/deliver mode is chosen."),
    "start_mode": Param("choice", choices=("build", "deliver"), default="build", group="switch",
                        doc="Fixed mode when switch_rule is none."),
    "switch_month": Param("int", 1, 48, default=8, group="switch", doc="calendar: deliver from this month on."),
    "switch_skill_base": Param("int", 0, 40, default=10, group="switch",
                               doc="state: deliver while Skill >= base + step * (level index - 1)."),
    "switch_skill_step": Param("int", 0, 12, default=6, group="switch", doc="state: per-level increment."),
    "wealth_floor": Param("float", -1.0, 3.0, default=0.5, group="money",
                          doc="Pay expenses from savings only when Wealth >= this; negative disables the rule."),
    "assert_dignity": Param("int", 0, 10, default=0, group="social",
                            doc="Speak up in conflicts when Dignity <= this; 0 disables."),
}
GROUPS: tuple[str, ...] = tuple(dict.fromkeys(p.group for p in THETA_SPACE.values()))


def default_theta() -> dict[str, Any]:
    return {k: p.default for k, p in THETA_SPACE.items()}


def normalize(theta: dict[str, Any]) -> dict[str, Any]:
    """Fill defaults, clip to bounds, cast types; unknown keys are an error."""
    unknown = set(theta) - set(THETA_SPACE)
    if unknown:
        raise ValueError(f"unknown theta parameters: {sorted(unknown)}")
    out: dict[str, Any] = {}
    for k, p in THETA_SPACE.items():
        v = theta.get(k, p.default)
        if p.kind == "choice":
            if v not in p.choices:
                raise ValueError(f"{k}={v!r} not in {p.choices}")
        elif p.kind == "int":
            v = int(min(max(round(float(v)), p.low), p.high))
        else:
            v = round(float(min(max(float(v), p.low), p.high)), 4)
        out[k] = v
    return out


def theta_id(theta: dict[str, Any]) -> str:
    """Stable short hash of a normalized theta (for registries and logs)."""
    blob = json.dumps(normalize(theta), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def complexity(theta: dict[str, Any]) -> int:
    """Number of active conditional rules (state/feedback switches count twice)."""
    t = normalize(theta)
    return (int(t["health_floor"] > 0) + int(t["dignity_floor"] > 0) + int(t["overtime_rule"] == "if_healthy")
            + int(t["risk_reaction"] != "ignore") + int(t["wealth_floor"] >= 0) + int(t["assert_dignity"] > 0)
            + {"none": 0, "calendar": 1, "state": 2, "feedback": 2}[t["switch_rule"]])


# Behaviour families: fixed values, (low, high) ranges or lists of allowed choices.
FAMILIES: dict[str, dict[str, Any]] = {
    "grinder": {"switch_rule": "none", "start_mode": "deliver", "invest_deliver": (0.0, 0.25),
                "overtime_rule": ["always", "if_healthy"], "overtime_health": (3, 6), "health_floor": (0, 4),
                "risk_reaction": ["ignore", "defuse"]},
    "builder": {"switch_rule": "none", "start_mode": "build", "invest_build": (0.6, 1.0),
                "overtime_rule": ["never", "if_healthy"]},
    "calendar": {"switch_rule": "calendar", "switch_month": (4, 18), "invest_build": (0.6, 1.0),
                 "invest_deliver": (0.0, 0.4)},
    "state": {"switch_rule": "state", "switch_skill_base": (4, 16), "switch_skill_step": (3, 9),
              "invest_build": (0.6, 1.0), "invest_deliver": (0.0, 0.4)},
    "feedback": {"switch_rule": "feedback", "invest_build": (0.6, 1.0), "invest_deliver": (0.0, 0.4)},
    "cautious": {"health_floor": (5, 8), "dignity_floor": (4, 7), "overtime_rule": "never",
                 "risk_reaction": ["defuse", "lay_low"], "risk_warnings": 1, "wealth_floor": (0.5, 3.0)},
    "random": {},
}


def _pick(rng: UniformRng, seq: Any) -> Any:
    return seq[min(int(rng.random() * len(seq)), len(seq) - 1)]


def _normal(rng: UniformRng) -> float:
    u1, u2 = rng.random(), rng.random()
    return math.sqrt(-2.0 * math.log(1.0 - u1)) * math.cos(2.0 * math.pi * u2)


def _sample(rng: UniformRng, p: Param, spec: Any = None) -> Any:
    if spec is not None and not isinstance(spec, (tuple, list)):
        return spec
    if p.kind == "choice":
        return _pick(rng, spec if isinstance(spec, list) else p.choices)
    lo, hi = spec if isinstance(spec, tuple) else (p.low, p.high)
    if p.kind == "int":
        return int(lo) + min(int(rng.random() * (int(hi) - int(lo) + 1)), int(hi) - int(lo))
    return lo + rng.random() * (hi - lo)


def random_theta(rng: UniformRng, family: str = "random") -> dict[str, Any]:
    """Sample a theta of one behaviour family (unconstrained parameters span the full space)."""
    if family not in FAMILIES:
        raise ValueError(f"unknown family {family!r}; known: {sorted(FAMILIES)}")
    spec = FAMILIES[family]
    return normalize({k: _sample(rng, p, spec.get(k)) for k, p in THETA_SPACE.items()})


def mutate(theta: dict[str, Any], rng: UniformRng, scale: float = 0.2) -> dict[str, Any]:
    """Perturb about a quarter of the parameters (at least one); numeric sd = scale x range."""
    t = normalize(theta)
    keys = list(THETA_SPACE)
    chosen = [k for k in keys if rng.random() < 0.25] or [_pick(rng, keys)]
    for k in chosen:
        p = THETA_SPACE[k]
        if p.kind == "choice":
            t[k] = _pick(rng, [c for c in p.choices if c != t[k]])
        else:
            step = _normal(rng) * scale * (p.high - p.low)
            if p.kind == "int" and abs(step) < 1.0:
                step = 1.0 if step >= 0 else -1.0
            t[k] = t[k] + step
    return normalize(t)


def crossover(a: dict[str, Any], b: dict[str, Any], rng: UniformRng) -> dict[str, Any]:
    """Uniform crossover over parameter groups, so coupled parameters travel together."""
    a, b = normalize(a), normalize(b)
    take_a = {grp: rng.random() < 0.5 for grp in GROUPS}
    return normalize({k: (a if take_a[p.group] else b)[k] for k, p in THETA_SPACE.items()})


# Named designed policies used by the tests and as lab baselines. They share a common
# core so that each pair differs in the one behaviour the pair is meant to isolate.
_CORE = {"invest_build": 1.0, "invest_deliver": 0.33, "network_share": 0.25, "overtime_rule": "if_healthy",
         "overtime_health": 6, "health_floor": 4, "dignity_floor": 3, "risk_reaction": "defuse"}
DESIGNED: dict[str, dict[str, Any]] = {
    # Problem B: deliver from month 1 without investing vs a deep early investment (build to Skill 20 first).
    "no_invest": normalize({**_CORE, "switch_rule": "none", "start_mode": "deliver", "invest_deliver": 0.0}),
    "early_invest": normalize({**_CORE, "switch_rule": "state", "switch_skill_base": 20, "switch_skill_step": 6}),
    # Problem C: deliver once Skill reaches the level's bar vs a fixed calendar switch.
    "state_switch": normalize({**_CORE, "switch_rule": "state", "switch_skill_base": 12, "switch_skill_step": 6}),
    "calendar8": normalize({**_CORE, "switch_rule": "calendar", "switch_month": 8}),
    "feedback_switch": normalize({**_CORE, "switch_rule": "feedback"}),
    # Problem A: accepting every extra-work request vs a steady networker that never pushes. A cautious
    # actor curbs the first one's overtime (rescuing it) and changes nothing for the second.
    "overcommit": normalize({**_CORE, "switch_rule": "state", "switch_skill_base": 12, "switch_skill_step": 6,
                             "network_share": 0.0, "overtime_rule": "always", "health_floor": 3}),
    "steady_networker": normalize({**_CORE, "switch_rule": "none", "start_mode": "build", "invest_build": 0.6,
                                   "network_share": 1.0, "health_floor": 8, "dignity_floor": 4,
                                   "overtime_rule": "never", "visibility_pref": 1.0, "risk_reaction": "lay_low"}),
}


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------

# Story style base preferences per mode (OVERTIME, DECLINE, COLLAB, LEARN, REST, ASSERT, SHORTCUT, SPEND, UNKNOWN).
_STYLE_BUILD = (0.0, 2.0, 4.0, 5.0, 1.0, 2.0, 0.0, 3.0, 0.5)
_STYLE_DELIVER = (0.0, 2.0, 4.0, 2.0, 1.0, 5.0, 0.0, 3.0, 0.5)


class ParamPolicy:
    """Executes theta on Views; keeps its own memory (mode, warnings, quarter plan)."""

    def __init__(self, theta: dict[str, Any]):
        t = normalize(theta)
        self.theta = t
        self.health_floor: int = t["health_floor"]
        self.dignity_floor: int = t["dignity_floor"]
        self.invest_build: float = t["invest_build"]
        self.invest_deliver: float = t["invest_deliver"]
        self.network_share: float = t["network_share"]
        self.overtime_rule: str = t["overtime_rule"]
        self.overtime_health: int = t["overtime_health"]
        self.risk_reaction: str = t["risk_reaction"]
        self.risk_warnings: int = t["risk_warnings"]
        self.switch_rule: str = t["switch_rule"]
        self.switch_month: int = t["switch_month"]
        self.switch_skill_base: int = t["switch_skill_base"]
        self.switch_skill_step: int = t["switch_skill_step"]
        self.wealth_floor: float = t["wealth_floor"]
        self.assert_dignity: int = t["assert_dignity"]
        vp = t["visibility_pref"]
        wn = 0.2 + 2.0 * self.network_share
        # Main-action weights over shown (Health, Dignity, Skill, Network, Output, HiddenRisk).
        self.w_build = (0.2, 0.2, 1.0, wn, 0.15, 0.0)
        self.w_deliver = (0.2, 0.2 + 1.5 * vp, 0.15, 0.2 + 1.0 * vp, 1.0, 0.0)
        # Switch rules start in build mode and re-evaluate the mode at every decision.
        self.mode = t["start_mode"] if self.switch_rule == "none" else "build"
        self.warn_months: list[int] = []
        self.handled_warning = 0
        self.plan: list[int] = []
        self.plan_month = -1
        self.credit = 0.0
        self.ncredit = 0.0
        self.ok = _always  # replaced by the actor model: did the actor execute this rule?

    # -- memory -----------------------------------------------------------
    def _observe(self, v: View) -> None:
        fb = v.feedback
        if fb:
            month = v.month
            for code in fb:
                if code == g.F_WARN:
                    if not self.warn_months or self.warn_months[-1] != month:
                        self.warn_months.append(month)
            if self.switch_rule == "feedback":
                target = None
                if g.F_DEPTH_OK in fb:
                    target = "deliver"
                if g.F_DEPTH_LOW in fb or g.F_PROMOTED in fb:
                    target = "build"
                if target is not None and target != self.mode and self.ok():
                    self.mode = target
        rule = self.switch_rule
        if rule == "calendar":
            target = "deliver" if v.month >= self.switch_month else "build"
        elif rule == "state":
            target = "deliver" if v.skill >= self.switch_skill_base + self.switch_skill_step * (v.level - 1) else "build"
        else:
            return
        if target != self.mode and self.ok():
            self.mode = target

    def _warning_pending(self, month: int) -> bool:
        w = self.warn_months
        if not w or w[-1] <= self.handled_warning:
            return False
        recent = 0
        for m in reversed(w):
            if m <= month - 6:
                break
            recent += 1
        return recent >= self.risk_warnings

    # -- decisions --------------------------------------------------------
    def decide(self, v: View) -> int:
        self._observe(v)
        phase = v.phase
        if phase == STORY:
            return self._story(v)
        if phase == ENERGY:
            return self._energy(v)
        if phase == MAIN:
            return self._main(v)
        return 1

    def _story(self, v: View) -> int:
        styles = v.styles
        base = _STYLE_BUILD if self.mode == "build" else _STYLE_DELIVER
        h = v.health
        rest_rule = bool(self.health_floor) and h <= self.health_floor + 1 and g.REST in styles and self.ok()
        rule = self.overtime_rule
        ot = rule == "always" or (rule == "if_healthy" and self.mode == "deliver" and g.OVERTIME in styles
                                  and h >= self.overtime_health and self.ok())
        spend = 3.0
        if self.wealth_floor >= 0 and g.SPEND in styles and self.ok():
            spend = 6.0 if v.wealth >= self.wealth_floor else -1.0
        assert_bonus = 3.0 if (self.assert_dignity and v.dignity <= self.assert_dignity and g.ASSERT in styles and self.ok()) else 0.0
        shortcut = 3.0 if (self.risk_reaction == "ignore" and self.mode == "deliver") else 0.0
        best, best_score = 1, -1e9
        for i, st in enumerate(styles):
            if st == g.OVERTIME:
                s = 7.0 if ot else -2.0
            elif st == g.REST:
                s = 8.0 if rest_rule else base[st]
            elif st == g.SPEND:
                s = spend
            elif st == g.ASSERT:
                s = base[st] + assert_bonus
            elif st == g.SHORTCUT:
                s = shortcut
            else:
                s = base[st]
            if s > best_score:
                best, best_score = i + 1, s
        return best

    def _plan_quarter(self, v: View) -> None:
        plan: list[int] = []
        budget = v.energy
        h, d = v.health, v.dignity
        hf = self.health_floor
        if hf and h <= hf and self.ok():
            plan.append(g.HEALTH_REC)
            budget -= 1
            if h <= hf - 2:
                plan.append(g.HEALTH_REC)
                budget -= 1
        if self.dignity_floor and d <= self.dignity_floor and budget >= 1 and self.ok():
            plan.append(g.MENTAL_REC)
            budget -= 1
        if self.risk_reaction == "defuse" and budget >= 2 and self._warning_pending(v.month) and self.ok():
            plan.append(g.DEFUSE)
            budget -= 2
            self.handled_warning = self.warn_months[-1]
        share = self.invest_build if self.mode == "build" else self.invest_deliver
        self.credit += share * budget
        inv = min(budget, int(self.credit + 0.5))
        self.credit -= inv
        self.ncredit += self.network_share * inv
        net = min(inv, int(self.ncredit + 0.5))
        self.ncredit -= net
        skill = inv - net
        while skill >= 2:
            plan.append(g.SKILL_LEARNING)
            skill -= 2
        plan.extend([g.NETWORK_MAINT] * (net + skill))
        out = budget - inv
        if out >= 2 and (not hf or h > hf + 1):
            plan.append(g.HIGH_INTENSITY)
            out -= 2
        plan.extend([g.PREPARE_REPORT] * out)
        self.plan = plan

    def _energy(self, v: View) -> int:
        if self.plan_month != v.month:
            self.plan_month = v.month
            self._plan_quarter(v)
        plan = self.plan
        while plan:
            a = plan.pop(0)
            if ENERGY_COST[a] <= v.energy:
                return a + 1
        if v.energy >= 1:
            return (g.PREPARE_REPORT if self.mode == "deliver" else g.NETWORK_MAINT) + 1
        return ENERGY_FINISH

    def _main(self, v: View) -> int:
        h, d = v.health, v.dignity
        if self.health_floor and h <= self.health_floor and self.ok():
            return g.LAY_LOW + 1
        if self.risk_reaction == "lay_low" and self._warning_pending(v.month) and self.ok():
            self.handled_warning = self.warn_months[-1]
            return g.LAY_LOW + 1
        if self.dignity_floor and d <= self.dignity_floor and self.ok():
            return g.REPAIR + 1
        w = self.w_build if self.mode == "build" else self.w_deliver
        best, best_score = MAIN_NONE, 0.0
        for choice, a, _, shown in v.options:
            if a < 0:
                continue
            s = w[0] * shown[0] + w[1] * shown[1] + w[2] * shown[2] + w[3] * shown[3] + w[4] * shown[4]
            if s > best_score:
                best, best_score = choice, s
        return best


def _always() -> bool:
    return True


# ---------------------------------------------------------------------------
# Actor models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ActorModel:
    """How faithfully (and with which bias) an actor executes a policy."""

    name: str
    miss_base: float = 0.0
    miss_per_rule: float = 0.0
    miss_cap: float = 0.6
    slip: float = 0.0
    bias: str = "none"  # none | caution | eager
    bias_strength: float = 0.0

    def miss(self, complexity_value: int) -> float:
        return min(self.miss_cap, self.miss_base + self.miss_per_rule * complexity_value)

    def record(self) -> dict[str, Any]:
        return asdict(self)


ACTORS: dict[str, ActorModel] = {
    "exact": ActorModel("exact"),
    "target": ActorModel("target", miss_base=0.005, miss_per_rule=0.005, slip=0.01),
    "cheap_capability": ActorModel("cheap_capability", miss_base=0.02, miss_per_rule=0.07, slip=0.04),
    "cheap_biased": ActorModel("cheap_biased", miss_base=0.01, miss_per_rule=0.01, slip=0.02,
                               bias="caution", bias_strength=0.6),
    "eager": ActorModel("eager", miss_base=0.01, miss_per_rule=0.01, slip=0.02, bias="eager", bias_strength=0.5),
}


def get_actor(actor: "str | ActorModel") -> ActorModel:
    if isinstance(actor, ActorModel):
        return actor
    try:
        return ACTORS[actor]
    except KeyError:
        raise ValueError(f"unknown actor {actor!r}; known: {sorted(ACTORS)}") from None


class Agent:
    """A policy executed by an actor model with its own deterministic random stream."""

    def __init__(self, theta: dict[str, Any], actor: "str | ActorModel", seed: int):
        self.actor = get_actor(actor)
        self.policy = ParamPolicy(theta)
        salt = int(hashlib.md5(self.actor.name.encode()).hexdigest()[:8], 16)
        self.rng = random.Random((seed * 1_000_003) ^ salt)
        miss = self.actor.miss(complexity(self.policy.theta))
        if miss > 0.0:
            rnd = self.rng.random
            self.policy.ok = lambda: rnd() >= miss
        self._slip = self.actor.slip
        self._bias = self.actor.bias if self.actor.bias_strength > 0 else "none"
        self._strength = self.actor.bias_strength

    def choose(self, v: View) -> int:
        c = self.policy.decide(v)
        if v.phase == DONE:
            return c
        rnd = self.rng.random
        if self._slip and rnd() < self._slip:
            return self._random_valid(v)
        if self._bias == "none":
            return c
        return self._biased(v, c)

    def _random_valid(self, v: View) -> int:
        if v.phase == STORY:
            return _pick(self.rng, range(1, len(v.styles) + 1))
        return _pick(self.rng, [opt[0] for opt in v.options if opt[2] <= v.energy])

    def _biased(self, v: View, c: int) -> int:
        rnd = self.rng.random
        if self._bias == "caution":
            if v.phase == STORY:
                st = v.styles[c - 1]
                if st in (g.OVERTIME, g.SHORTCUT, g.ASSERT) and rnd() < self._strength:
                    for alt in (g.REST, g.DECLINE):
                        if alt in v.styles:
                            return v.styles.index(alt) + 1
            elif v.phase == ENERGY and c != ENERGY_FINISH:
                shown = v.options[c - 1][3]
                if (shown[0] < 0 or shown[1] < 0) and rnd() < self._strength:
                    return (g.HEALTH_REC if v.health <= v.dignity else g.MENTAL_REC) + 1
            return c
        # eager
        if v.phase == STORY:
            if g.OVERTIME in v.styles and v.styles[c - 1] != g.OVERTIME and rnd() < self._strength:
                return v.styles.index(g.OVERTIME) + 1
        elif v.phase == ENERGY:
            if c - 1 in (g.HEALTH_REC, g.MENTAL_REC) and v.energy >= 2 and rnd() < self._strength:
                return g.HIGH_INTENSITY + 1
        elif v.phase == MAIN:
            if c - 1 == g.LAY_LOW and rnd() < self._strength:
                return g.FIGHT_RESOURCES + 1
        return c


def make_agent(theta: dict[str, Any], actor: "str | ActorModel" = "target", seed: int = 0) -> Agent:
    return Agent(theta, actor, seed)


# ---------------------------------------------------------------------------
# Reading official-schema observations
# ---------------------------------------------------------------------------

# Keyword reading of story options, checked in this order (first match wins).
STYLE_KEYWORDS: tuple[tuple[int, tuple[str, ...]], ...] = (
    (g.SHORTCUT, ("quickly",)),
    (g.SPEND, ("savings",)),
    (g.OVERTIME, ("take on", "stay late", "push through", "extra hours")),
    (g.REST, ("rest", "day off", "let it go")),
    (g.ASSERT, ("speak up", "negotiate", "defend", "advance", "leadership")),
    (g.COLLAB, ("colleague", "team", "join", "mentor", "people")),
    (g.LEARN, ("study", "rework", "enrol")),
    (g.DECLINE, ("decline", "skip", "postpone")),
)


def classify_option(text: str) -> int:
    low = text.lower()
    for style, words in STYLE_KEYWORDS:
        for word in words:
            if word in low:
                return style
    return g.UNKNOWN


_FIXED_LINES = {text: code for code, text in g.FIXED_TEXTS.items()}
_FIXED_LINES.update({t: g.F_WARN for t in g.WARN_TEXTS})
_FIXED_LINES.update({t: g.F_NOISE for t in g.NOISE_TEXTS})
_PREFIXES = (("Payday:", g.F_SALARY), ("Half-year bonus paid:", g.F_BONUS),
             ("Promotion window: you have been promoted", g.F_PROMOTED), ("Career over:", g.F_FAILED))
_GRADE_PREFIX = "Half-year performance review: grade "


def feedback_codes(events: str) -> list[int]:
    codes: list[int] = []
    for line in (events or "").splitlines():
        line = line.strip()
        if not line:
            continue
        code = _FIXED_LINES.get(line)
        if code is None:
            if line.startswith(_GRADE_PREFIX):
                code = g.F_GRADE_CODES[g.GRADES.index(line[len(_GRADE_PREFIX)])]
            else:
                code = next((c for prefix, c in _PREFIXES if line.startswith(prefix)), -1)
        codes.append(code)
    return codes


_ENERGY_INDEX = {name: i for i, name in enumerate(g.ENERGY_NAMES)}
_MAIN_INDEX = {name: i for i, name in enumerate(g.MAIN_NAMES)}


def _shown(updates: dict[str, Any] | None) -> tuple[int, ...]:
    updates = updates or {}
    return tuple(int(updates.get(k, 0)) for k in g.UPDATE_KEYS)


def view_from_obs(obs: dict[str, Any]) -> View:
    """Build the policy's View from an official-schema observation only."""
    state = obs.get("current_state") or {}
    status = state.get("status") or {}
    flags = state.get("simulation_flags") or {}
    event = obs.get("current_event") or {}
    choices = obs.get("choices") or []
    v = View()
    v.month = int((state.get("time") or {}).get("current_month") or 0)
    v.health = int(status.get("health", 0))
    v.dignity = int(status.get("dignity", 0))
    v.skill = int(status.get("skill", 0))
    v.network = int(status.get("network", 0))
    v.output = int(status.get("output", 0))
    v.wealth = float(status.get("wealth", 0.0))
    v.level = int(str(status.get("level", "L1")).lstrip("L") or 1)
    v.duration = int(status.get("duration_in_level", 0))
    v.energy = int(status.get("energy", 0))
    v.feedback = feedback_codes(obs.get("events") or "")
    if obs.get("ending_score") or flags.get("alive") is False:
        v.phase = DONE
    elif "energy_budget" in event or "remaining_energy" in event:
        v.phase = ENERGY
        v.options = tuple((int(c["choice"]), _ENERGY_INDEX.get(c.get("action", ""), -1), int(c.get("energy_cost", 0)),
                           _shown(c.get("status_updates"))) for c in choices)
    elif "max_selections" in event:
        v.phase = MAIN
        v.options = tuple((int(c["choice"]), _MAIN_INDEX.get(c.get("action", ""), -1), int(c.get("energy_cost", 0)),
                           _shown(c.get("status_updates"))) for c in choices)
    else:
        v.phase = STORY
        v.styles = tuple(classify_option(str(c.get("action", ""))) for c in choices)
    return v


class PolicyActor:
    """DrivenActor adapter: plays a theta through any official-schema MCP client."""

    def __init__(self, theta: dict[str, Any], actor: "str | ActorModel" = "target", seed: int = 0):
        self.theta = normalize(theta)
        self.seed = seed
        self.agent = make_agent(self.theta, actor, seed)

    def config(self) -> dict[str, Any]:
        return {"kind": "synthetic-param", "theta": self.theta, "theta_id": theta_id(self.theta),
                "actor": self.agent.actor.record(), "seed": self.seed}

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Any:
        from careerlab.episode import Decision

        choice = self.agent.choose(view_from_obs(obs))
        return Decision(choice, notes=f"mode={self.agent.policy.mode}")
