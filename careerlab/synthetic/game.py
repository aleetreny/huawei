"""SynthCareer: a synthetic career game with known ground truth.

Only the *public structure* follows the official documentation: 48 months, story
events every month, a quarterly phase with 3 Energy points spent on the
published Energy actions at the published costs, one quarterly main action (or
none), a six-monthly review graded S..D with the published bonus multipliers,
ten levels with the published salary table, the published visible statistics
and ranges, the published failure directions and the published ending
dimensions. **Every formula and number below is invented for this testbed and
says nothing about the real game.** Event texts are generic templates written
for SynthCareer and are parameterised by a latent event type.

Synthetic mechanics (all knobs live in ``SynthConfig``)
-------------------------------------------------------
Randomness. Each episode pre-draws ``SLOTS`` uniforms per month from
``random.Random(seed)``; every random effect reads a fixed slot of its month.
Two policies played on the same seed meet the same events, outcome draws,
review noise and promotion draws (common random numbers).

Start. Health, Dignity, Skill, Network and Wealth are drawn from the
``start_*`` ranges. A latent learning *aptitude* (``aptitude_values`` with
``aptitude_weights``) is the Skill gained per learning action; it is shown
honestly in the ``status_updates`` of Skill learning / key project / rotation /
mentorship (rotation gives aptitude + 1), and story learning gives
``max(1, round(s * aptitude / 2))``. Aptitude and starting Skill make the
moment a player is "ready to deliver" differ widely between games.

Month. Pay ``SALARY[level] - living_cost``; present ``events_per_month`` story
events of weighted latent types; every quarter (month % 3 == 0) run the Energy
phase then the main-action phase; then settle: hidden risk decays by
``risk_decay``; a warning line appears with probability
``clip(warn_base + warn_slope * (risk - warn_center), warn_base, 0.9)``
(false alarms at low risk, misses at high risk); a risk incident ends the run
with probability ``max(0, risk - blowup_start) * blowup_slope``; failure
counters advance (see below); every 6 months a review and promotion window.

Effects. Visible stats are integers (Health/Dignity clipped to 0..10); Wealth
is kept in thousandths so salaries and bonuses are exact. High-intensity work
yields ``Output 2 + Skill // hi_skill_div`` (skill compounds into output).
``status_updates`` show the real visible effects; hidden side effects are
hidden risk (key project, fight for resources +1; lay low -2), *visibility*
credit counted by the next review (report +2, showcase +2, prepare materials
+1, rotation -2, lay low -1; at most ``vis_cap`` per half), a key-project
failure chance ``1 - key_project_success`` and Health -1 on key projects.
Story options have fixed effects or a chance ``p0 + slope * Network`` of the
good outcome.

Out of depth. Each overwork action (high-intensity work and overtime-style
story choices) with ``gap = (E - Skill) / E > 0`` adds ``ood_risk * gap``
hidden risk and ends the run ("out_of_depth") with probability
``ood_incident * gap``. ``E`` is the promotion bar of the current level,
``req_skill(L)``, phased in at L1 linearly between months ``ramp_start`` and
``ramp_end``. Building (learning, networking) never triggers it, so delivering
before one is ready is what is dangerous.

Review (every 6 months). ``perf = (Output gained in the half + capped
visibility) / expected * U(1 - review_noise, 1 + review_noise)`` with
``expected = (out_base + out_step * (L-1)) * (1 + out_stagnation * max(0,
duration - 6) / 6)``; grades by ``grade_cuts``; Dignity changes by
``grade_dignity``; bonus = published multiplier x base salary. A reviewer
comment says whether Skill looks adequate for the next level, judged as
``Skill + U(-fb_noise, fb_noise) >= req_skill(L)``.

Promotion (same window; needs grade S/A/B and, with ``promo_needs_prev_not_d``,
no D in the previous review). ``p = grade_prob[grade] * sigmoid((Skill -
req_skill(L)) / promo_soft) * sigmoid((Network - req_net(L)) / promo_soft)``
with ``req_skill(L) = req_skill_base + req_skill_step * (L-1)`` and
``req_net(L) = req_net_base + req_net_step * (L-1)``. This is the late-benefit
lever (problem B): investment lowers early Output and grades but is what later
promotions (salary, level) need. Because the bar rises with the level and
aptitude varies, the right moment to switch from building to delivering
depends on Skill relative to the bar, not on the calendar (problem C).

Failures. Health 0 (immediate); a serious out-of-depth mistake (immediate);
Dignity <= ``dignity_fail_level`` for ``dignity_fail_months`` consecutive
months; a risk incident; ``low_perf_reviews`` consecutive D grades; Network 0
for ``network_fail_months`` months; Wealth < 0 for ``wealth_fail_months``
months; Skill below ``skill_gap_frac * E`` at ``skill_gap_reviews``
consecutive reviews.

Ending score. Six dimensions with ``score_weights``: career level
``(L-1)/level_ref``, total wealth ``Wealth/wealth_ref``, health & dignity
``(H+D)/20``, skill ``Skill/skill_ref``, risk control ``1 - (risk - risk_ok) /
(risk_bad - risk_ok)`` (0 after a risk incident or out-of-depth mistake),
network ``Network/net_ref``, each clipped to [0, 1]. ``quantitative_score =
100 * sum(weight * normalized)``, computed the same way for early exits from
the state at exit. ``survival_months`` is the month reached.
"""

from __future__ import annotations

import hashlib
import math
import random
import time
from dataclasses import asdict, dataclass, field, fields, replace
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:  # pragma: no cover
    from careerlab.synthetic.policy import ActorModel

# ---------------------------------------------------------------------------
# Public structure (from the official docs)
# ---------------------------------------------------------------------------

LEVELS = tuple(f"L{i}" for i in range(1, 11))
SALARY = (0.3, 0.4, 0.5, 0.7, 1.0, 1.5, 2.3, 3.6, 5.7, 9.1)
SALARY_M = tuple(round(s * 1000) for s in SALARY)  # thousandths: exact arithmetic
GRADES = ("S", "A", "B", "C", "D")
BONUS_QUARTERS = (12, 8, 4, 1, 0)  # bonus = BONUS_QUARTERS/4 x monthly base (3x, 2x, 1x, 0.25x, 0)
ENERGY_BUDGET = 3

# Energy actions, published order and costs. Choice number = index + 1; FINISH ends the phase.
HIGH_INTENSITY, SKILL_LEARNING, NETWORK_MAINT, DEFUSE, MENTAL_REC, HEALTH_REC, PREPARE_REPORT = range(7)
ENERGY_NAMES = ("High-intensity work", "Skill learning", "Network maintenance", "Defuse legacy risk",
                "Mental recovery", "Health recovery", "Prepare report materials")
ENERGY_COST = (2, 2, 1, 2, 1, 1, 1)
ENERGY_FINISH_NAME = "End energy actions"
ENERGY_FINISH = len(ENERGY_NAMES) + 1  # choice number

# Main actions, published order. Choice number = index + 1; MAIN_NONE selects no main action.
KEY_PROJECT, REPORT_MANAGER, FIGHT_RESOURCES, ROTATION, SHOWCASE, MENTORSHIP, REPAIR, LAY_LOW = range(8)
MAIN_NAMES = ("Apply for a key project", "Report results to your manager", "Fight for resources",
              "Apply for rotation", "Showcase results", "Build a mentorship", "Repair a key relationship",
              "Lay low and reduce risk")
MAIN_NONE_NAME = "No main action this quarter"
MAIN_NONE = len(MAIN_NAMES) + 1

# Order of the effect tuples used everywhere: Health, Dignity, Skill, Network, Output, HiddenRisk.
UPDATE_KEYS = ("Health", "Dignity", "Skill", "Network", "Output", "HiddenRisk")

STORY, ENERGY, MAIN, DONE = range(4)
PHASE_NAMES = ("event", "energy", "main_action", "terminal")

# ---------------------------------------------------------------------------
# Synthetic content (invented)
# ---------------------------------------------------------------------------

# Choice styles: what kind of response a story option is. Policies infer them from the text.
OVERTIME, DECLINE, COLLAB, LEARN, REST, ASSERT, SHORTCUT, SPEND, UNKNOWN = range(9)
STYLE_NAMES = ("overtime", "decline", "collab", "learn", "rest", "assert", "shortcut", "spend", "unknown")

SLOTS = 17  # uniforms per month
_S_NEV, _S_TYPE, _S_CHANCE, _S_TEXT, _S_WARN, _S_WARNV, _S_NOISE, _S_BLOW, _S_REVIEW, _S_DEPTH, _S_PROMO, _S_MAIN, _S_HI = (
    0, 1, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)


@dataclass(frozen=True)
class Effect:
    """Synthetic effect of one option: deltas plus optional chance of a good outcome."""

    h: int = 0
    d: int = 0
    s: int = 0
    n: int = 0
    o: int = 0
    w: int = 0      # Wealth in thousandths
    r: float = 0.0  # hidden risk
    v: int = 0      # hidden visibility credit for the next review
    depth: bool = False  # overwork: out-of-depth extra risk applies
    p0: float = 1.0      # chance of the good outcome = p0 + slope * Network (1.0 = certain)
    slope: float = 0.0
    fail: "Effect | None" = None


@dataclass(frozen=True)
class EventType:
    name: str
    titles: tuple[str, ...]
    descriptions: tuple[str, ...]
    options: tuple[tuple[int, str, Effect], ...]  # (style, action text, effect)


_E = Effect
EVENT_TYPES: tuple[EventType, ...] = (
    EventType("extra_work", ("Deadline crunch", "Extra work request"),
              ("A teammate asks you to cover extra work before a deadline.",
               "Your team lead asks whether you can absorb an extra task this sprint."),
              ((OVERTIME, "Take on the extra work yourself", _E(h=-1, o=2, r=1.0, depth=True)),
               (COLLAB, "Split the task with a colleague", _E(o=1, n=1, p0=0.45, slope=0.05, fail=_E(d=-1))),
               (DECLINE, "Politely decline and protect your plan", _E(d=1, p0=0.5, fail=_E(n=-1))))),
    EventType("credit", ("Credit for your work",),
              ("In a meeting, a colleague presents part of your work as their own.",
               "Your contribution is missing from a project summary sent upwards."),
              ((ASSERT, "Speak up and clarify your contribution", _E(d=1, v=1, p0=0.6, fail=_E(d=1, n=-1))),
               (COLLAB, "Talk privately with your colleague about sharing credit",
                _E(n=1, v=1, p0=0.4, slope=0.05, fail=_E(d=-1))),
               (REST, "Let it go this time", _E(d=-1)))),
    EventType("learning", ("Learning opportunity",),
              ("An internal course on a new technology opens for registration.",
               "A senior colleague offers a deep-dive session on the system architecture."),
              ((LEARN, "Enrol and study in the evenings", _E(s=2, h=-1)),
               (COLLAB, "Join a study group with your team", _E(s=1, n=1)),
               (DECLINE, "Skip it and focus on current deliverables", _E(o=1)))),
    EventType("urgent", ("Urgent request",),
              ("Your manager needs a status summary by tonight.",
               "A stakeholder escalates and wants an answer before the end of the day."),
              ((OVERTIME, "Stay late and deliver it tonight", _E(h=-1, o=1, v=1, r=0.5, depth=True)),
               (ASSERT, "Negotiate a smaller scope and a firm deadline",
                _E(d=1, v=1, p0=0.5, slope=0.03, fail=_E(d=-1))),
               (DECLINE, "Postpone it until tomorrow morning", _E(p0=0.5, fail=_E(n=-1, v=-1))))),
    EventType("legacy", ("Fragile legacy component",),
              ("You discover that your service depends on a fragile legacy script.",
               "An old configuration nobody owns keeps failing in production."),
              ((SHORTCUT, "Patch it quickly and move on", _E(o=1, r=2.0)),
               (COLLAB, "Document it and escalate it with the owning team", _E(n=1, r=-1.0)),
               (LEARN, "Rework the critical part properly", _E(s=1, h=-1, r=-2.0)))),
    EventType("social", ("Team gathering",),
              ("The team organises an after-work gathering.",
               "A cross-team meetup is happening on Friday evening."),
              ((COLLAB, "Join and get to know people", _E(n=1, w=-100)),
               (REST, "Go home and rest", _E(h=1)))),
    EventType("expense", ("Unexpected expense",),
              ("An unexpected personal expense comes up this month.",
               "Your rent goes up at short notice."),
              ((SPEND, "Pay it from your savings", _E(w=-700)),
               (OVERTIME, "Pick up paid extra hours to cover it", _E(h=-1, r=0.5, w=-200)),
               (ASSERT, "Ask for an advance on your salary", _E(d=-1, w=-300)))),
    EventType("fatigue", ("Running low",),
              ("You have been sleeping badly for several weeks.",
               "A long stretch without a break is catching up with you."),
              ((REST, "Take a day off to recover", _E(h=2, o=-1)),
               (OVERTIME, "Push through and keep working", _E(h=-1, o=1, r=0.5, depth=True)))),
    EventType("feedback", ("Candid feedback",),
              ("A senior engineer gives you blunt feedback on your design.",
               "A code review of your work turns into a long list of concerns."),
              ((LEARN, "Listen carefully and rework the design", _E(s=1)),
               (ASSERT, "Defend your design choices", _E(d=1, n=-1)),
               (COLLAB, "Ask them to mentor you", _E(s=1, n=1, p0=0.3, slope=0.04, fail=_E(d=-1))))),
    EventType("recognition", ("Recognition",),
              ("A partner team thanks your group for a recent fix.",
               "Your work is mentioned positively in a department update."),
              ((ASSERT, "Share the success with leadership", _E(d=1, v=1)),
               (COLLAB, "Credit the whole team publicly", _E(n=1, d=1)))),
)
EVENT_STYLES = tuple(tuple(style for style, _, _ in et.options) for et in EVENT_TYPES)

# Nominal (shown) effects per action as (Health, Dignity, Skill, Network, Output, HiddenRisk).
ENERGY_SHOWN = ((-1, -1, 0, 0, 2, 1), (-1, 0, 2, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 0, 0, 0, -3),
                (0, 2, 0, 0, 0, 0), (2, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 0))
ENERGY_VIS = (0, 0, 0, 0, 0, 0, 1)  # hidden visibility credit
MAIN_SHOWN = ((0, 0, 2, 1, 2, 0), (0, 1, 0, 1, 1, 0), (0, 0, 0, 1, 3, 0), (0, 0, 3, 1, 0, 0),
              (0, 1, 0, 0, 2, 0), (0, 0, 2, 2, 0, 0), (0, 2, 0, 2, 0, 0), (2, 0, 0, 0, 0, 0))
MAIN_HIDDEN = ((-1, 1.0, 0), (0, 0.0, 2), (0, 1.0, 0), (0, 0.0, -2),  # (Health, risk, visibility)
               (0, 0.0, 2), (0, 0.0, 0), (0, 0.0, 0), (0, -2.0, -1))

# Feedback codes; text templates are rendered only for MCP observations.
(F_SALARY, F_WARN, F_NOISE, F_GRADE, F_BONUS, F_DEPTH_OK, F_DEPTH_LOW, F_PROMOTED, F_NOT_PROMOTED,
 F_HEALTH_LOW, F_DIGNITY_LOW, F_WEALTH_NEG, F_SKILL_GAP, F_LOW_PERF, F_GOOD, F_BAD, F_FAILED) = range(17)
F_GRADE_CODES = tuple(100 + i for i in range(5))  # S..D grade lines carry the grade in the code
WARN_TEXTS = ("HR circulated a reminder about sustainable workloads and process compliance.",
              "Rumours say an audit of older services is being planned.",
              "A colleague mentions that some of your recent shortcuts have been noticed.")
NOISE_TEXTS = ("The office kitchen was refurbished this month.",
               "A new team calendar tool was rolled out.",
               "The quarterly town hall was postponed.")
FIXED_TEXTS = {
    F_DEPTH_OK: "Reviewer comment: your technical depth is solid; more visible delivery would strengthen your case.",
    F_DEPTH_LOW: "Reviewer comment: your technical foundations need to grow before the next level.",
    F_NOT_PROMOTED: "Promotion window: no promotion this cycle.",
    F_HEALTH_LOW: "You feel worn out; your body is asking for rest.",
    F_DIGNITY_LOW: "You feel sidelined and undervalued at work.",
    F_WEALTH_NEG: "Your account is overdrawn.",
    F_SKILL_GAP: "Your manager notes that your skills are falling behind what your role expects.",
    F_LOW_PERF: "HR notes a very weak performance result; corrective action is expected.",
    F_GOOD: "That worked out well.",
    F_BAD: "That did not go as hoped.",
}
FAILURE_TEXTS = {
    "health_depleted": "Your health collapsed and you had to leave the company.",
    "dignity_collapse": "After months of feeling sidelined you resigned.",
    "risk_incident": "An accumulated hidden risk turned into a serious incident; you were let go.",
    "low_performance": "Repeated very weak reviews ended your employment.",
    "isolation": "With no working relationships left, your role was eliminated.",
    "insolvency": "Prolonged debt forced you to leave for another job.",
    "skill_gap": "Your skills fell too far behind your role's expectations; you were let go.",
    "out_of_depth": "Working far beyond your depth led to a serious mistake; you were let go.",
}


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SynthConfig:
    """Knobs of the synthetic mechanics (see the module docstring for the formulas)."""

    months: int = 48
    events_per_month: tuple[int, int] = (1, 2)
    event_weights: tuple[float, ...] = (1.4, 1.0, 1.0, 1.2, 0.9, 0.8, 0.7, 0.8, 0.9, 0.6)
    start_health: tuple[int, int] = (6, 8)
    start_dignity: tuple[int, int] = (5, 7)
    start_skill: tuple[int, int] = (0, 6)
    start_network: tuple[int, int] = (1, 3)
    start_wealth: tuple[float, float] = (1.0, 2.0)
    aptitude_values: tuple[int, ...] = (1, 2, 4)  # latent learning aptitude: Skill per learning action
    aptitude_weights: tuple[float, ...] = (0.3, 0.4, 0.3)
    living_cost: float = 0.25
    hi_skill_div: int = 3
    key_project_success: float = 0.6
    req_skill_base: float = 12.0
    req_skill_step: float = 6.0
    req_net_base: float = 3.0
    req_net_step: float = 2.5
    promo_soft: float = 1.2
    promo_needs_prev_not_d: bool = True  # "sustained results": no D in the previous review
    grade_prob: tuple[float, float, float] = (0.95, 0.85, 0.55)  # S, A, B
    out_base: float = 12.0
    out_step: float = 4.0
    out_stagnation: float = 0.12
    review_noise: float = 0.2
    grade_cuts: tuple[float, float, float, float] = (1.5, 1.15, 0.85, 0.45)
    fb_noise: float = 3.0
    ramp_start: float = 9.0   # months before L1 expectations start to rise
    ramp_end: float = 18.0    # month at which the full L1 bar is expected
    vis_cap: int = 4
    grade_dignity: tuple[int, int, int, int, int] = (2, 1, 0, -1, -2)
    ood_risk: float = 2.0
    ood_incident: float = 1.2
    risk_decay: float = 0.25
    warn_base: float = 0.04
    warn_slope: float = 0.08
    warn_center: float = 3.0
    blowup_start: float = 6.0
    blowup_slope: float = 0.03
    dignity_fail_level: int = 1
    dignity_fail_months: int = 3
    low_perf_reviews: int = 3
    network_fail_months: int = 6
    wealth_fail_months: int = 6
    skill_gap_frac: float = 0.5
    skill_gap_reviews: int = 2
    score_weights: tuple[float, ...] = (0.30, 0.30, 0.25, 0.05, 0.05, 0.05)
    level_ref: float = 7.0
    wealth_ref: float = 25.0
    skill_ref: float = 80.0
    net_ref: float = 60.0
    risk_ok: float = 6.0
    risk_bad: float = 16.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SynthConfig":
        """Build from JSON-like overrides; list values become tuples."""
        known = {f.name for f in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"unknown SynthConfig fields: {sorted(unknown)}")
        return replace(cls(), **{k: tuple(v) if isinstance(v, list) else v for k, v in data.items()})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_CONFIG = SynthConfig()

DIMENSIONS = (("career_level", "Career level"), ("total_wealth", "Total wealth"), ("health_dignity", "Health & dignity"),
              ("professional_skill", "Professional skill"), ("risk_control", "Risk control"),
              ("workplace_network", "Workplace network"))


def _clip01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def score_state(level: int, wealth: float, health: int, dignity: int, skill: int, risk: float, network: int,
                cfg: SynthConfig, incident: bool = False) -> tuple[float, list[tuple[str, str, Any, float, float, float]]]:
    """Synthetic ending evaluation: (quantitative_score, [(name, label, raw, normalized, weight, weighted)])."""
    norms = (_clip01((level - 1) / cfg.level_ref), _clip01(wealth / cfg.wealth_ref), (health + dignity) / 20.0,
             _clip01(skill / cfg.skill_ref),
             0.0 if incident else 1.0 - _clip01((risk - cfg.risk_ok) / (cfg.risk_bad - cfg.risk_ok)),
             _clip01(network / cfg.net_ref))
    raws = (LEVELS[level - 1], round(wealth, 3), health + dignity, skill, round(risk, 2), network)
    dims = [(name, label, raw, nv, w, 100.0 * w * nv) for (name, label), raw, nv, w in zip(DIMENSIONS, raws, norms, cfg.score_weights)]
    return round(sum(d[5] for d in dims), 4), dims


def quick_score(level: int, wealth: float, health: int, dignity: int, skill: int, risk: float, network: int,
                cfg: SynthConfig, incident: bool = False) -> float:
    """Same number as ``score_state`` without building the dimension list (hot path)."""
    w = cfg.score_weights
    total = (w[0] * _clip01((level - 1) / cfg.level_ref) + w[1] * _clip01(wealth / cfg.wealth_ref)
             + w[2] * (health + dignity) / 20.0 + w[3] * _clip01(skill / cfg.skill_ref)
             + w[4] * (0.0 if incident else 1.0 - _clip01((risk - cfg.risk_ok) / (cfg.risk_bad - cfg.risk_ok)))
             + w[5] * _clip01(network / cfg.net_ref))
    return round(100.0 * total, 4)


# ---------------------------------------------------------------------------
# Engine (shared by the fast path and the MCP path)
# ---------------------------------------------------------------------------

class View:
    """Everything a player can see at a decision point; nothing hidden.

    ``options`` are (choice, action index, energy cost, shown effects) for the
    quarterly phases; ``styles`` are the story options' styles (choice i+1 has
    style ``styles[i]``); ``feedback`` are the feedback codes rendered in the
    observation's ``events`` text since the previous accepted action.
    """

    __slots__ = ("month", "phase", "health", "dignity", "skill", "network", "output", "wealth", "level",
                 "duration", "energy", "styles", "options", "feedback")

    def __init__(self) -> None:
        self.month = self.phase = self.health = self.dignity = self.skill = self.network = 0
        self.output = self.level = self.duration = self.energy = 0
        self.wealth = 0.0
        self.styles: tuple[int, ...] = ()
        self.options: tuple[tuple[int, int, int, tuple[int, ...]], ...] = ()
        self.feedback: list[int] = []

    def key(self) -> tuple[Any, ...]:
        """Comparable snapshot (used to prove the fast and MCP paths see the same thing)."""
        return tuple(tuple(v) if isinstance(v, list) else v for v in (getattr(self, s) for s in self.__slots__))


def _req_skill(cfg: SynthConfig, level: int) -> float:
    return cfg.req_skill_base + cfg.req_skill_step * (level - 1)


def _expected_skill(cfg: SynthConfig, level: int, month: int) -> float:
    """Skill the current role demands: the level's promotion bar, ramped in over the first months at L1."""
    bar = _req_skill(cfg, level)
    if level > 1:
        return bar
    ramp = (month - cfg.ramp_start) / (cfg.ramp_end - cfg.ramp_start)
    return bar * (0.0 if ramp < 0.0 else (1.0 if ramp > 1.0 else ramp))


Option = tuple[int, int, int, tuple[int, ...]]  # (choice, action index or -1, energy cost, shown effects)
_ENERGY_OPTION_CACHE: dict[tuple[int, int], tuple[Option, ...]] = {}
_MAIN_OPTION_CACHE: dict[int, tuple[Option, ...]] = {}


def energy_shown(hi_output: int, apt: int) -> list[tuple[int, ...]]:
    shown = list(ENERGY_SHOWN)
    shown[HIGH_INTENSITY] = (-1, -1, 0, 0, hi_output, 1)
    shown[SKILL_LEARNING] = (-1, 0, apt, 0, 0, 0)
    return shown


def main_shown(apt: int) -> list[tuple[int, ...]]:
    shown = list(MAIN_SHOWN)
    shown[KEY_PROJECT] = (0, 0, apt, 1, 2, 0)
    shown[ROTATION] = (0, 0, apt + 1, 1, 0, 0)
    shown[MENTORSHIP] = (0, 0, apt, 2, 0, 0)
    return shown


def _energy_options(hi_output: int, apt: int) -> tuple[Option, ...]:
    opts = _ENERGY_OPTION_CACHE.get((hi_output, apt))
    if opts is None:
        shown = energy_shown(hi_output, apt)
        opts = tuple((i + 1, i, ENERGY_COST[i], shown[i]) for i in range(len(ENERGY_NAMES))) + ((ENERGY_FINISH, -1, 0, (0,) * 6),)
        _ENERGY_OPTION_CACHE[(hi_output, apt)] = opts
    return opts


def _main_options(apt: int) -> tuple[Option, ...]:
    opts = _MAIN_OPTION_CACHE.get(apt)
    if opts is None:
        shown = main_shown(apt)
        opts = tuple((i + 1, i, 0, shown[i]) for i in range(len(MAIN_NAMES))) + ((MAIN_NONE, -1, 0, (0,) * 6),)
        _MAIN_OPTION_CACHE[apt] = opts
    return opts


class Engine:
    """SynthCareer state machine. ``apply`` returns an error string or None."""

    def __init__(self, seed: int, cfg: SynthConfig = DEFAULT_CONFIG, record: bool = True):
        self.cfg = cfg
        self.record = record
        rnd = random.Random(seed).random
        self.u = [rnd() for _ in range(SLOTS * (cfg.months + 1))]
        u = self.u
        lo, hi = cfg.start_health
        self.health = lo + int(u[0] * (hi - lo + 1))
        lo, hi = cfg.start_dignity
        self.dignity = lo + int(u[1] * (hi - lo + 1))
        lo, hi = cfg.start_skill
        self.skill = lo + int(u[2] * (hi - lo + 1))
        lo, hi = cfg.start_network
        self.network = lo + int(u[3] * (hi - lo + 1))
        lo_w, hi_w = cfg.start_wealth
        self.wealth_m = int(round(1000 * (lo_w + u[4] * (hi_w - lo_w)) / 10)) * 10
        x, self.apt = u[5], cfg.aptitude_values[-1]
        for k, w in enumerate(cfg.aptitude_weights):
            if x < w:
                self.apt = cfg.aptitude_values[k]
                break
            x -= w
        self.main_options = _main_options(self.apt)
        self.main_shown = main_shown(self.apt)
        self.output = 0
        self.level = 1
        self.duration = 0
        self.month = 0
        self.energy = 0
        self.risk = 0.0
        self.vis = 0
        self.out_at_review = 0
        self.last_grade = -1
        self.low_perf = self.low_dignity = self.neg_wealth = self.zero_net = self.gap_reviews = 0
        self.alive = True
        self.completed = False
        self.failure_reason: str | None = None
        self.incident = False
        self.mistake = False
        self.phase = STORY
        self.events: list[int] = []
        self.ev_i = 0
        self.fb: list[int] = []
        self.fb_args: list[Any] = []
        self.history: list[dict[str, Any]] = []
        self.grade_this_month: str | None = None
        self.reviews: list[str] = []
        self.promotions: list[int] = []
        cum, total = [], 0.0
        for w in cfg.event_weights:
            total += w
            cum.append(total)
        self._cum = [c / total for c in cum]
        self._living_m = round(cfg.living_cost * 1000)
        self.view = View()
        self._start_month()

    # -- feedback ---------------------------------------------------------
    def _say(self, code: int, arg: Any = None) -> None:
        self.fb.append(code)
        self.fb_args.append(arg)

    # -- month flow -------------------------------------------------------
    def _start_month(self) -> None:
        self.month += 1
        self.duration += 1
        self.grade_this_month = None
        salary = SALARY_M[self.level - 1]
        self.wealth_m += salary - self._living_m
        self._say(F_SALARY, (salary, self._living_m, self.level))
        base = SLOTS * self.month
        u = self.u
        lo, hi = self.cfg.events_per_month
        n = min(3, lo + int(u[base + _S_NEV] * (hi - lo + 1)))
        cum = self._cum
        events = []
        for k in range(n):
            x = u[base + _S_TYPE + k]
            t = 0
            while cum[t] < x:
                t += 1
            events.append(t)
        self.events = events
        self.ev_i = 0
        self.phase = STORY
        self._refresh()

    def _end_month(self) -> None:
        cfg = self.cfg
        u = self.u
        base = SLOTS * self.month
        risk = self.risk - cfg.risk_decay
        self.risk = risk = risk if risk > 0.0 else 0.0
        p = cfg.warn_base + cfg.warn_slope * (risk - cfg.warn_center)
        p = cfg.warn_base if p < cfg.warn_base else (0.9 if p > 0.9 else p)
        if u[base + _S_WARN] < p:
            self._say(F_WARN, int(u[base + _S_WARNV] * len(WARN_TEXTS)))
        x = u[base + _S_NOISE]
        if x < 0.15:
            self._say(F_NOISE, int(x / 0.15 * len(NOISE_TEXTS)))
        if risk > cfg.blowup_start and u[base + _S_BLOW] < (risk - cfg.blowup_start) * cfg.blowup_slope:
            self.incident = True
            return self._fail("risk_incident")
        if self.dignity <= cfg.dignity_fail_level:
            self.low_dignity += 1
            if self.low_dignity >= cfg.dignity_fail_months:
                return self._fail("dignity_collapse")
        else:
            self.low_dignity = 0
        if self.dignity <= 2:
            self._say(F_DIGNITY_LOW)
        if self.health <= 2:
            self._say(F_HEALTH_LOW)
        if self.wealth_m < 0:
            self.neg_wealth += 1
            self._say(F_WEALTH_NEG)
            if self.neg_wealth >= cfg.wealth_fail_months:
                return self._fail("insolvency")
        else:
            self.neg_wealth = 0
        if self.network <= 0:
            self.zero_net += 1
            if self.zero_net >= cfg.network_fail_months:
                return self._fail("isolation")
        else:
            self.zero_net = 0
        if self.month % 6 == 0:
            self._review()
            if not self.alive:
                return
        self._snapshot()
        if self.month >= cfg.months:
            self.completed = True
            self.phase = DONE
            self._refresh()
            return
        self._start_month()

    def _review(self) -> None:
        cfg = self.cfg
        u = self.u
        base = SLOTS * self.month
        lvl = self.level
        expected = (cfg.out_base + cfg.out_step * (lvl - 1)) * (1.0 + cfg.out_stagnation * max(0, self.duration - 6) / 6.0)
        gain = self.output - self.out_at_review + min(self.vis, cfg.vis_cap)
        perf = gain / expected * (1.0 - cfg.review_noise + 2.0 * cfg.review_noise * u[base + _S_REVIEW])
        cuts = cfg.grade_cuts
        g = 0
        while g < 4 and perf < cuts[g]:
            g += 1
        grade = GRADES[g]
        self.grade_this_month = grade
        self.reviews.append(grade)
        self._say(F_GRADE_CODES[g], grade)
        bonus = SALARY_M[lvl - 1] * BONUS_QUARTERS[g] // 4
        x = self.dignity + cfg.grade_dignity[g]
        self.dignity = 0 if x < 0 else (10 if x > 10 else x)
        if bonus:
            self.wealth_m += bonus
            self._say(F_BONUS, bonus)
        req = _req_skill(cfg, lvl)
        depth_ok = self.skill + (2.0 * u[base + _S_DEPTH] - 1.0) * cfg.fb_noise >= req
        self._say(F_DEPTH_OK if depth_ok else F_DEPTH_LOW)
        prev = self.last_grade
        self.last_grade = g
        if g == 4:
            self.low_perf += 1
            self._say(F_LOW_PERF)
            if self.low_perf >= cfg.low_perf_reviews:
                return self._fail("low_performance")
        else:
            self.low_perf = 0
        promoted = False
        if lvl < 10 and g <= 2 and not (cfg.promo_needs_prev_not_d and prev == 4):
            soft = cfg.promo_soft
            net_req = cfg.req_net_base + cfg.req_net_step * (lvl - 1)
            p = (cfg.grade_prob[g] / (1.0 + math.exp(-(self.skill - req) / soft))
                 / (1.0 + math.exp(-(self.network - net_req) / soft)))
            if u[base + _S_PROMO] < p:
                promoted = True
                self.level = lvl + 1
                self.duration = 0
                self.promotions.append(self.month)
                self._say(F_PROMOTED, LEVELS[lvl])
        if not promoted:
            self._say(F_NOT_PROMOTED)
        if self.skill < cfg.skill_gap_frac * _expected_skill(cfg, self.level, self.month):
            self.gap_reviews += 1
            self._say(F_SKILL_GAP)
            if self.gap_reviews >= cfg.skill_gap_reviews:
                return self._fail("skill_gap")
        else:
            self.gap_reviews = 0
        self.out_at_review = self.output
        self.vis = 0

    def _fail(self, reason: str) -> None:
        self.alive = False
        self.failure_reason = reason
        self._say(F_FAILED, reason)
        self._snapshot()
        self.phase = DONE
        self._refresh()

    def _snapshot(self) -> None:
        if not self.record:
            return
        wealth = self.wealth_m / 1000
        self.history.append({
            "month": self.month, "health": self.health, "dignity": self.dignity, "skill": self.skill,
            "network": self.network, "output": self.output, "wealth": wealth, "level": self.level,
            "review": self.grade_this_month, "alive": self.alive,
            "q": quick_score(self.level, wealth, self.health, self.dignity, self.skill, self.risk, self.network,
                             self.cfg, self.incident),
        })

    # -- effects ----------------------------------------------------------
    def _effect(self, h: int, d: int, s: int, n: int, o: int, w: int, r: float, v: int) -> None:
        x = self.health + h
        self.health = 0 if x < 0 else (10 if x > 10 else x)
        x = self.dignity + d
        self.dignity = 0 if x < 0 else (10 if x > 10 else x)
        if s:
            x = self.skill + s
            self.skill = x if x > 0 else 0
        if n:
            x = self.network + n
            self.network = x if x > 0 else 0
        if o:
            x = self.output + o
            self.output = x if x > 0 else 0
        self.wealth_m += w
        if r:
            x = self.risk + r
            self.risk = x if x > 0.0 else 0.0
        self.vis += v

    def _overwork(self, slot: int) -> float:
        """Extra hidden risk of overwork beyond one's depth; may also cause a serious mistake."""
        expect = _expected_skill(self.cfg, self.level, self.month)
        if expect <= self.skill:
            return 0.0
        gap = (expect - self.skill) / expect
        if self.u[slot] < self.cfg.ood_incident * gap:
            self.mistake = True
        return self.cfg.ood_risk * gap

    def _story(self, etype: int, option: int) -> None:
        eff = EVENT_TYPES[etype].options[option][2]
        if eff.p0 < 1.0:
            p = eff.p0 + eff.slope * self.network
            if self.u[SLOTS * self.month + _S_CHANCE + self.ev_i] < p:
                self._say(F_GOOD)
            else:
                self._say(F_BAD)
                eff = eff.fail  # type: ignore[assignment]
        r = eff.r + self._overwork(SLOTS * self.month + _S_CHANCE + self.ev_i) if eff.depth else eff.r
        s = max(1, round(eff.s * self.apt / 2)) if eff.s > 0 else eff.s
        self._effect(eff.h, eff.d, s, eff.n, eff.o, eff.w, r, eff.v)

    # -- decisions --------------------------------------------------------
    def apply(self, choice: int) -> str | None:
        """Apply one choice; return an error message (state unchanged) or None."""
        phase = self.phase
        if phase == DONE:
            return "The game is over."
        if phase == STORY:
            etype = self.events[self.ev_i]
            if not 1 <= choice <= len(EVENT_STYLES[etype]):
                return f"Invalid choice {choice}."
            self.fb = []
            self.fb_args = []
            self._story(etype, choice - 1)
            if self.mistake:
                self.incident = True
                return self._fail("out_of_depth")
            if self.health <= 0:
                return self._fail("health_depleted")
            self.ev_i += 1
            if self.ev_i < len(self.events):
                self._refresh()
            elif self.month % 3 == 0:
                self.phase = ENERGY
                self.energy = ENERGY_BUDGET
                self._refresh()
            else:
                self._end_month()
            return None
        if phase == ENERGY:
            if choice == ENERGY_FINISH:
                self.fb = []
                self.fb_args = []
                self._enter_main()
                return None
            if not 1 <= choice <= len(ENERGY_NAMES):
                return f"Invalid choice {choice}."
            a = choice - 1
            cost = ENERGY_COST[a]
            if cost > self.energy:
                return f"Insufficient energy: {ENERGY_NAMES[a]} costs {cost}, {self.energy} remaining."
            self.fb = []
            self.fb_args = []
            self.energy -= cost
            if a == HIGH_INTENSITY:
                self._effect(-1, -1, 0, 0, 2 + self.skill // self.cfg.hi_skill_div, 0,
                             1.0 + self._overwork(SLOTS * self.month + _S_HI), 0)
            elif a == SKILL_LEARNING:
                self._effect(-1, 0, self.apt, 0, 0, 0, 0.0, 0)
            else:
                h, d, s, n, o, r = ENERGY_SHOWN[a]
                self._effect(h, d, s, n, o, 0, float(r), ENERGY_VIS[a])
            if self.mistake:
                self.incident = True
                return self._fail("out_of_depth")
            if self.health <= 0:
                return self._fail("health_depleted")
            if self.energy <= 0:
                self._enter_main()
            else:
                self._refresh()
            return None
        # MAIN
        if not 1 <= choice <= MAIN_NONE:
            return f"Invalid choice {choice}."
        self.fb = []
        self.fb_args = []
        if choice != MAIN_NONE:
            a = choice - 1
            h, d, s, n, o, _ = self.main_shown[a]
            hh, rr, vv = MAIN_HIDDEN[a]
            if a == KEY_PROJECT:
                if self.u[SLOTS * self.month + _S_MAIN] < self.cfg.key_project_success:
                    self._say(F_GOOD)
                else:
                    self._say(F_BAD)
                    d, s, n, o = -1, 1 if s > 1 else s, 0, 0
            self._effect(h + hh, d, s, n, o, 0, rr, vv)
            if self.health <= 0:
                return self._fail("health_depleted")
        self.energy = 0
        self._end_month()
        return None

    def _enter_main(self) -> None:
        self.energy = 0
        self.phase = MAIN
        self._refresh()

    def _refresh(self) -> None:
        v = self.view
        v.month = self.month
        v.phase = self.phase
        v.health = self.health
        v.dignity = self.dignity
        v.skill = self.skill
        v.network = self.network
        v.output = self.output
        v.wealth = self.wealth_m / 1000
        v.level = self.level
        v.duration = self.duration
        v.energy = self.energy
        phase = self.phase
        if phase == STORY:
            v.styles = EVENT_STYLES[self.events[self.ev_i]]
            v.options = ()
        elif phase == ENERGY:
            v.styles = ()
            v.options = _energy_options(2 + self.skill // self.cfg.hi_skill_div, self.apt)
        elif phase == MAIN:
            v.styles = ()
            v.options = self.main_options
        else:
            v.styles = ()
            v.options = ()
        v.feedback = self.fb

    @property
    def done(self) -> bool:
        return self.phase == DONE

    @property
    def wealth(self) -> float:
        return self.wealth_m / 1000

    def survival_months(self) -> int:
        return self.month

    def score(self) -> float:
        return quick_score(self.level, self.wealth, self.health, self.dignity, self.skill, self.risk, self.network,
                           self.cfg, self.incident)

    def ending(self) -> dict[str, Any]:
        _, dims = score_state(self.level, self.wealth, self.health, self.dignity, self.skill, self.risk,
                              self.network, self.cfg, self.incident)
        q = round(self.score(), 2)  # same summation as the fast path
        return {
            "outcome": "completed" if self.completed else "eliminated",
            "survival_months": self.month,
            "completed": self.completed,
            "quantitative_score": q,
            "competition_partial_score": round(q * 0.7, 2),
            "dimensions": [{"name": n, "label": lab, "raw_value": raw, "normalized_score": round(nv, 4),
                            "weight": w, "weighted_score": round(ws, 4)} for n, lab, raw, nv, w, ws in dims],
        }


# ---------------------------------------------------------------------------
# MCP-shaped game (official-like observation schema)
# ---------------------------------------------------------------------------

def session_id_for(seed: int, salt: str = "") -> str:
    """Deterministic 32-hex session id (the same shape as the official ids)."""
    return hashlib.md5(f"synthcareer:{salt}:{seed}".encode()).hexdigest()


def feedback_text(code: int, arg: Any) -> str:
    if code == F_SALARY:
        salary, living, level = arg
        return (f"Payday: base salary +{salary / 1000:g} Wealth ({LEVELS[level - 1]}); "
                f"living costs -{living / 1000:g} Wealth.")
    if code == F_WARN:
        return WARN_TEXTS[arg]
    if code == F_NOISE:
        return NOISE_TEXTS[arg]
    if code in F_GRADE_CODES:
        return f"Half-year performance review: grade {arg}."
    if code == F_BONUS:
        return f"Half-year bonus paid: +{arg / 1000:g} Wealth."
    if code == F_PROMOTED:
        return f"Promotion window: you have been promoted to {arg}."
    if code == F_FAILED:
        return f"Career over: {FAILURE_TEXTS[arg]}"
    return FIXED_TEXTS[code]


def handbook_text(cfg: SynthConfig = DEFAULT_CONFIG) -> str:
    """Public handbook of SynthCareer: structure only, no internal formulas."""
    salary = "\n".join(f"- {lvl}: {s} Wealth / month" for lvl, s in zip(LEVELS, SALARY))
    energy = "\n".join(f"- {n} (cost {c})" for n, c in zip(ENERGY_NAMES, ENERGY_COST))
    main = "\n".join(f"- {n}" for n in MAIN_NAMES)
    return f"""SynthCareer employee handbook (synthetic test game; not the official game)

A run lasts {cfg.months} months. Each month pays the base salary of your level and
presents story events. At the end of each quarter you receive {ENERGY_BUDGET} Energy for
energy actions, then choose one main action or none. Every six months a performance
review (S, A, B, C, D) settles a bonus (3x, 2x, 1x, 0.25x, 0x monthly base) and a
promotion window opens; promotion considers Skill, Network and sustained results.

Visible statistics: Health 0-10, Dignity 0-10, Skill, Network, Output (0 and above),
Wealth (may be negative), Level L1-L10, Energy 0-3, months in the current level.

Monthly base salary:
{salary}

Energy actions:
{energy}

Main actions:
{main}

Risks: health reaching zero, sustained very low dignity, accumulated hidden risks,
repeated very weak reviews, no network for a long time, prolonged negative wealth,
skills far behind your role. Warnings in the feedback may hint at rising risk.
The ending evaluation considers career level, total wealth, health & dignity,
professional skill, risk control and workplace network.
"""


def _updates_dict(shown: tuple[int, ...]) -> dict[str, int]:
    return {k: v for k, v in zip(UPDATE_KEYS, shown) if v}


class SynthGame:
    """One SynthCareer session exposed through the official observation schema."""

    def __init__(self, seed: int, config: SynthConfig | None = None, session_id: str | None = None):
        self.seed = seed
        self.cfg = config or DEFAULT_CONFIG
        self.engine = Engine(seed, self.cfg, record=True)
        self.session_id = session_id or session_id_for(seed)
        self.log: list[dict[str, Any]] = []
        self.steps = 0

    @property
    def done(self) -> bool:
        return self.engine.done

    def observe(self) -> dict[str, Any]:
        eng = self.engine
        month = eng.month
        state = {
            "time": {"current_month": month, "current_quarter": (month - 1) % 12 // 3 + 1,
                     "current_year": (month - 1) // 12 + 1},
            "status": {"health": eng.health, "dignity": eng.dignity, "skill": eng.skill, "network": eng.network,
                       "level": LEVELS[eng.level - 1], "duration_in_level": eng.duration, "output": eng.output,
                       "wealth": eng.wealth, "energy": eng.energy},
            "simulation_flags": {"alive": eng.alive, "failed": not eng.alive, "failure_reason": eng.failure_reason},
            "session_id": self.session_id,
        }
        events = "\n".join(feedback_text(c, a) for c, a in zip(eng.fb, eng.fb_args))
        obs: dict[str, Any] = {"current_state": state}
        if eng.phase == STORY:
            et = EVENT_TYPES[eng.events[eng.ev_i]]
            k = int(eng.u[SLOTS * month + _S_TEXT] * 997) + eng.ev_i
            obs["current_event"] = {"title": et.titles[k % len(et.titles)],
                                    "description": et.descriptions[k % len(et.descriptions)]}
            obs["choices"] = [{"choice": i + 1, "action": text} for i, (_, text, _) in enumerate(et.options)]
        elif eng.phase == ENERGY:
            obs["current_event"] = {
                "title": "Quarterly energy actions",
                "description": "Spend your quarterly Energy on energy actions, or end the phase.",
                "energy_budget": ENERGY_BUDGET, "remaining_energy": eng.energy,
                "rules": "Each action costs Energy; unused Energy does not carry over. "
                         f"Choose {ENERGY_FINISH} to end the energy phase.",
            }
            obs["choices"] = [{"choice": c, "action": ENERGY_NAMES[a] if a >= 0 else ENERGY_FINISH_NAME,
                               "energy_cost": cost, "status_updates": _updates_dict(shown)}
                              for c, a, cost, shown in eng.view.options]
        elif eng.phase == MAIN:
            obs["current_event"] = {
                "title": "Quarterly main action",
                "description": "Choose the principal career focus for this quarter, or no main action.",
                "max_selections": 1,
                "rules": "Select exactly one option.",
            }
            obs["choices"] = [{"choice": c, "action": MAIN_NAMES[a] if a >= 0 else MAIN_NONE_NAME,
                               "status_updates": _updates_dict(shown)} for c, a, _, shown in eng.main_options]
        else:
            obs["current_event"] = {"title": "Career finished" if eng.completed else "Career ended early",
                                    "description": "The simulation has ended."}
            obs["choices"] = []
        obs["events"] = events
        if eng.phase == DONE:
            obs["ending_score"] = eng.ending()
        return obs

    def take_action(self, choice: int, notes: str = "") -> dict[str, Any]:
        eng = self.engine
        try:
            choice = int(choice)
        except (TypeError, ValueError):
            return {"success": False, "error": f"Invalid choice {choice!r}."}
        before = (eng.month, PHASE_NAMES[eng.phase])
        title = ""
        if eng.phase == STORY:
            et = EVENT_TYPES[eng.events[eng.ev_i]]
            action = et.options[choice - 1][1] if 1 <= choice <= len(et.options) else None
            title = et.name
        elif eng.phase == ENERGY:
            action = ENERGY_FINISH_NAME if choice == ENERGY_FINISH else (ENERGY_NAMES[choice - 1] if 1 <= choice <= len(ENERGY_NAMES) else None)
        elif eng.phase == MAIN:
            action = MAIN_NONE_NAME if choice == MAIN_NONE else (MAIN_NAMES[choice - 1] if 1 <= choice <= len(MAIN_NAMES) else None)
        else:
            action = None
        error = eng.apply(choice)
        self.steps += 1
        self.log.append({"step": len(self.log) + 1, "month": before[0], "phase": before[1], "choice": choice,
                         "action": action, "notes": str(notes)[:1000], "success": error is None, "error": error,
                         **({"event": title} if title else {})})
        return {"success": error is None, "error": error}

    def logs(self, count: int = 10) -> dict[str, Any]:
        count = max(0, int(count))
        return {"session_id": self.session_id, "entries": self.log[-count:] if count else []}

    def handbook(self) -> str:
        return handbook_text(self.cfg)

    def outcome(self) -> "EpisodeOutcome":
        eng = self.engine
        return _outcome(eng, self.steps, [None] * len(eng.history))


# ---------------------------------------------------------------------------
# Fast path
# ---------------------------------------------------------------------------

TOKENS_PER_STEP = 3000  # proxy for an LLM worker's tokens per decision


@dataclass
class EpisodeOutcome:
    Q: float
    T: int
    completed: bool
    outcome: str  # completed | eliminated
    failure_reason: str | None
    monthly: list[dict[str, Any]] = field(default_factory=list)
    tokens_proxy: int = 0
    steps: int = 0
    rejected: int = 0
    reviews: list[str] = field(default_factory=list)
    promotions: list[int] = field(default_factory=list)

    @property
    def Y(self) -> float:
        """Synthetic automated score: 0.8 Q + 0.1 E (token term full marks, capped at 50 for early exits)."""
        return 0.8 * self.Q + 0.1 * (100.0 if self.completed else 50.0)


def _outcome(eng: Engine, steps: int, modes: list[str | None], rejected: int = 0) -> EpisodeOutcome:
    monthly = []
    for rec, mode in zip(eng.history, modes):
        row = dict(rec)
        row["mode"] = mode
        monthly.append(row)
    return EpisodeOutcome(Q=round(eng.score(), 2), T=eng.month, completed=eng.completed,
                          outcome="completed" if eng.completed else "eliminated", failure_reason=eng.failure_reason,
                          monthly=monthly, tokens_proxy=steps * TOKENS_PER_STEP, steps=steps, rejected=rejected,
                          reviews=list(eng.reviews), promotions=list(eng.promotions))


def fast_episode(theta: dict[str, Any], actor: "str | ActorModel" = "target", seed: int = 0,
                 config: SynthConfig | None = None, record: bool = True, max_steps: int = 3000) -> EpisodeOutcome:
    """Play one episode without building JSON observations.

    Decision-for-decision identical to driving ``SynthGame`` through
    ``observe``/``take_action`` with the same theta, actor and seed.
    """
    from careerlab.synthetic.policy import make_agent

    cfg = config or DEFAULT_CONFIG
    eng = Engine(seed, cfg, record)
    agent = make_agent(theta, actor, seed)
    choose = agent.choose
    view = eng.view
    apply = eng.apply
    history = eng.history
    modes: list[str | None] = []
    policy = agent.policy
    steps = rejected = 0
    while eng.phase != DONE and steps < max_steps:
        if apply(choose(view)) is not None:
            rejected += 1
        steps += 1
        if record and len(history) > len(modes):
            modes.append(policy.mode)
    if record:
        modes.extend([policy.mode] * (len(history) - len(modes)))
    return _outcome(eng, steps, modes, rejected) if record else EpisodeOutcome(
        Q=round(eng.score(), 2), T=eng.month, completed=eng.completed,
        outcome="completed" if eng.completed else "eliminated", failure_reason=eng.failure_reason,
        tokens_proxy=steps * TOKENS_PER_STEP, steps=steps, rejected=rejected,
        reviews=list(eng.reviews), promotions=list(eng.promotions))


class Truth(NamedTuple):
    mean_q: float
    mean_y: float


TRUTH_SEED_BASE = 1_000_000_000  # truth seeds never overlap small evaluation seeds


def truth(theta: dict[str, Any], actor: "str | ActorModel" = "target", n: int = 20000, seed: int = 0,
          config: SynthConfig | None = None) -> Truth:
    """Ground-truth mean Q and mean Y over ``n`` fresh games (seeds TRUTH_SEED_BASE + seed*n + i)."""
    q = y = 0.0
    start = TRUTH_SEED_BASE + seed * n
    for i in range(n):
        out = fast_episode(theta, actor, start + i, config, record=False)
        q += out.Q
        y += 0.8 * out.Q + (10.0 if out.completed else 5.0)
    return Truth(q / n, y / n)


def throughput(theta: dict[str, Any], actor: "str | ActorModel" = "target", n: int = 2000,
               config: SynthConfig | None = None) -> float:
    """Measured single-core episodes per second of the fast path (record=False)."""
    start = time.perf_counter()
    for i in range(n):
        fast_episode(theta, actor, 7_000_000 + i, config, record=False)
    return n / (time.perf_counter() - start)
