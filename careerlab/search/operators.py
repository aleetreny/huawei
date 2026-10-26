"""Emulated policy generation on SynthCareer's ``THETA_SPACE``.

Substitution, stated plainly: in the real lab an Opus orchestrator reads a
parent's traces and diagnostics and writes a natural-language revision of a
Skill bundle. Here each operator is a small parametric rule that produces a
new theta and a one-line hypothesis of the kind the orchestrator would write.
The operators are deliberately simple and only as "smart" as their written
rules; they exist so that the allocation, selection and validation machinery
in ``methods`` can be exercised thousands of times against known ground
truth. Conclusions about generation quality do not transfer to LLM-written
policies.

Operators (all return a ``Proposal``):

- ``new_family``: a fresh draw from a behaviour family;
- ``refine``: a targeted change driven by the parent's failure profile
  (e.g. most failures are Health collapses -> recover earlier);
- ``recombine``: parameter groups (modules) from two parents;
- ``specialize``: adds a build/deliver mode switch triggered by observable
  state or feedback, never by the calendar unless a calendar hypothesis is
  tested on purpose (flagged diagnostic);
- ``wild``: a large contrarian jump, used on stagnation.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Sequence

from careerlab.synthetic.policy import FAMILIES, GROUPS, THETA_SPACE, mutate, normalize, random_theta

if TYPE_CHECKING:  # pragma: no cover
    from careerlab.search.archive import Node

ALL_FAMILIES: tuple[str, ...] = tuple(FAMILIES)

FAMILY_HYPOTHESES = {
    "grinder": "deliver from month 1 and accept extra work: output now beats investment",
    "builder": "keep investing in Skill and Network: promotions need them",
    "calendar": "build first, then deliver from a fixed month (calendar hypothesis; diagnostic in the real lab)",
    "state": "build until Skill reaches the level's bar, then deliver: readiness decides, not the calendar",
    "feedback": "switch between building and delivering on reviewer comments about depth",
    "cautious": "protect Health, Dignity and Wealth first and react to every risk warning",
    "random": "unconstrained sample of the parameter space",
}


@dataclass(frozen=True)
class Proposal:
    theta: dict[str, Any]
    hypothesis: str
    operator: str
    family: str
    parents: tuple[str, ...] = ()
    meta: dict[str, Any] = field(default_factory=dict)


class CandidateStream:
    """Shared fresh draws per family: the k-th draw of family f depends only on (seed, f, k).

    Every method of one replication builds its own stream from the same
    seed, so their initial candidates coincide (common random numbers across
    methods) however differently they consume them later.
    """

    def __init__(self, seed: int):
        self.seed = seed
        self.counts: Counter[str] = Counter()

    def draw(self, family: str) -> dict[str, Any]:
        k = self.counts[family]
        self.counts[family] += 1
        return random_theta(random.Random(f"stream:{self.seed}:{family}:{k}"), family)


def new_family(rng: random.Random, stream: CandidateStream | None = None, family: str | None = None,
               families: Sequence[str] = ALL_FAMILIES) -> Proposal:
    """A fresh policy from a behaviour family (uniform over ``families`` unless one is given)."""
    family = family or families[min(int(rng.random() * len(families)), len(families) - 1)]
    theta = stream.draw(family) if stream is not None else random_theta(rng, family)
    return Proposal(theta, f"new family {family}: {FAMILY_HYPOTHESES.get(family, 'new behaviour family')}",
                    "new_family", family)


# ---------------------------------------------------------------------------
# refine: targeted fixes from the failure profile
# ---------------------------------------------------------------------------

Fix = Callable[[dict[str, Any], random.Random], tuple[dict[str, Any], str]]


def _fix_health(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    c: dict[str, Any] = {"health_floor": t["health_floor"] + rng.choice((1, 2))}
    if t["overtime_rule"] == "always":
        c["overtime_rule"] = "if_healthy"
    else:
        c["overtime_health"] = t["overtime_health"] + 1
    return c, "recover Health earlier and accept less overwork"


def _fix_dignity(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    floor = t["dignity_floor"] + rng.choice((1, 2))
    return {"dignity_floor": floor, "assert_dignity": max(t["assert_dignity"], floor - 1)}, \
        "repair Dignity and speak up before it collapses"


def _fix_risk(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    c: dict[str, Any] = {"risk_reaction": {"ignore": "defuse", "defuse": "lay_low"}.get(t["risk_reaction"], "lay_low"),
                         "risk_warnings": 1}
    if t["overtime_rule"] == "always":
        c["overtime_rule"] = "if_healthy"
    return c, "react to the first risk warning instead of letting hidden risk build up"


def _fix_depth(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    c: dict[str, Any] = {"overtime_rule": "never" if t["overtime_rule"] == "always" else t["overtime_rule"],
                         "switch_skill_base": t["switch_skill_base"] + rng.choice((2, 3, 4)),
                         "switch_month": t["switch_month"] + rng.choice((3, 4, 6)),
                         "invest_build": t["invest_build"] + 0.15}
    if t["switch_rule"] == "none" and t["start_mode"] == "deliver":
        c["invest_deliver"] = t["invest_deliver"] + 0.25
    return c, "stop overworking before Skill matches the role: build longer, deliver later"


def _fix_skill_gap(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    return {"invest_build": t["invest_build"] + 0.15, "invest_deliver": t["invest_deliver"] + 0.15,
            "network_share": t["network_share"] - 0.15}, "put more Energy into Skill learning"


def _fix_low_perf(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    return {"switch_skill_base": t["switch_skill_base"] - rng.choice((2, 3, 4)),
            "switch_month": t["switch_month"] - rng.choice((2, 3)),
            "invest_deliver": t["invest_deliver"] - 0.15, "visibility_pref": t["visibility_pref"] + 0.25}, \
        "deliver and show results earlier to avoid weak reviews"


def _fix_insolvency(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    return {"wealth_floor": t["wealth_floor"] + 1.0}, "keep a cash buffer before paying from savings"


def _fix_isolation(t: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str]:
    return {"network_share": t["network_share"] + 0.3}, "maintain Network so it never runs out"


FIXES: dict[str, Fix] = {
    "health_depleted": _fix_health, "dignity_collapse": _fix_dignity, "risk_incident": _fix_risk,
    "out_of_depth": _fix_depth, "skill_gap": _fix_skill_gap, "low_performance": _fix_low_perf,
    "insolvency": _fix_insolvency, "isolation": _fix_isolation,
}


def _score_fix(t: dict[str, Any], d: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], str, str]:
    """Change for a policy that mostly survives: weak reviews, slow promotions, or fine-tuning."""
    level, low = d.get("mean_level", 1.0), d.get("low_grade_share", 0.0)
    if level < 2.5 and low >= 0.35:
        c, why = _fix_low_perf(t, rng)
        return c, why, f"it survives but {low:.0%} of reviews are C/D"
    if level < 3.5:
        if d.get("mean_network", 0.0) < d.get("mean_skill", 0.0) / 3:
            return ({"network_share": t["network_share"] + 0.15},
                    "shift investment towards Network, which promotions also consider",
                    f"promotions are slow (mean final level L{level:.1f}) and Network lags Skill")
        return ({"invest_build": t["invest_build"] + 0.1, "switch_skill_base": t["switch_skill_base"] + 2},
                "build a little longer before delivering", f"promotions are slow (mean final level L{level:.1f})")
    return {}, "fine-tune around a policy that completes and promotes", f"no dominant failure (level L{level:.1f})"


def refine(parent: "Node", diagnostics: dict[str, Any], rng: random.Random) -> Proposal:
    """Targeted change guided by the parent's failure profile (emulated reflective mutation)."""
    t = normalize(parent.theta)
    fails = diagnostics.get("failures") or {}
    n = diagnostics.get("n", 0)
    issue, share = max(fails.items(), key=lambda kv: kv[1]) if fails else (None, 0.0)
    if issue in FIXES and share >= 0.15:
        changes, why = FIXES[issue](t, rng)
        reason = f"{share:.0%} of {n} episodes end in {issue}"
    else:
        changes, why, reason = _score_fix(t, diagnostics, rng)
    theta = normalize({**t, **changes})
    if theta == t:
        theta = mutate(t, rng, 0.1)
        why += " (rule at its bounds: small random step instead)"
    changed = sorted(k for k in theta if theta[k] != t[k])
    return Proposal(theta, f"refine {parent.id}: {reason}; {why} [{', '.join(changed)}]", "refine", parent.family,
                    (parent.id,), {"issue": issue if share >= 0.15 else None, "changed": changed})


def recombine(a: "Node", b: "Node", rng: random.Random) -> Proposal:
    """Parameter groups from two parents, at least one group from each (modules travel whole)."""
    ta, tb = normalize(a.theta), normalize(b.theta)
    take_a = {g: rng.random() < 0.5 for g in GROUPS}
    if all(take_a.values()) or not any(take_a.values()):
        flip = GROUPS[min(int(rng.random() * len(GROUPS)), len(GROUPS) - 1)]
        take_a[flip] = not take_a[flip]
    theta = normalize({k: (ta if take_a[p.group] else tb)[k] for k, p in THETA_SPACE.items()})
    from_a = [g for g in GROUPS if take_a[g]]
    from_b = [g for g in GROUPS if not take_a[g]]
    return Proposal(theta, f"recombine {a.id} ({', '.join(from_a)}) with {b.id} ({', '.join(from_b)}): "
                           f"keep each parent's strongest modules", "recombine", a.family, (a.id, b.id),
                    {"from_a": from_a, "from_b": from_b})


def specialize(parent: "Node", rng: random.Random, calendar: bool = False) -> Proposal:
    """Add a mode switch triggered by observable state or feedback.

    A calendar trigger is produced only with ``calendar=True``, and the
    proposal is then marked diagnostic (the real lab never ships one).
    Parents that already switch on state get the other observable trigger
    or a state-conditioned overtime rule.
    """
    t = normalize(parent.theta)
    split = {"invest_build": max(t["invest_build"], 0.7), "invest_deliver": min(t["invest_deliver"], 0.3)}
    if calendar:
        month = rng.randint(4, 18)
        c, trigger = {"switch_rule": "calendar", "switch_month": month, **split}, "calendar"
        why = f"deliver from month {month} (diagnostic calendar hypothesis, never shipped)"
    elif t["switch_rule"] in ("none", "calendar"):
        if rng.random() < 0.6:
            base, step = rng.randint(8, 16), rng.randint(4, 8)
            c, trigger = {"switch_rule": "state", "switch_skill_base": base, "switch_skill_step": step, **split}, "state"
            why = f"build until Skill >= {base} + {step} per level, then deliver"
        else:
            c, trigger = {"switch_rule": "feedback", **split}, "feedback"
            why = "deliver after a review says depth is solid, build again after a promotion or a depth warning"
    elif rng.random() < 0.5 and t["overtime_rule"] != "if_healthy":
        health = rng.randint(5, 8)
        c, trigger = {"overtime_rule": "if_healthy", "overtime_health": health}, "state"
        why = f"accept extra work only in deliver mode while Health >= {health}"
    else:
        other = "feedback" if t["switch_rule"] == "state" else "state"
        c, trigger = {"switch_rule": other}, other
        why = f"switch modes on {other} instead of {t['switch_rule']}"
    theta = normalize({**t, **c})
    if theta == t:
        theta = normalize({**t, "switch_skill_base": t["switch_skill_base"] + rng.choice((-2, 2))})
    return Proposal(theta, f"specialize {parent.id}: {why}", "specialize", parent.family, (parent.id,),
                    {"specialization": True, "trigger": trigger, "base": parent.id, "diagnostic": calendar})


def wild(parent: "Node", rng: random.Random) -> Proposal:
    """Large contrarian jump: invert several of the parent's main choices, then a wide mutation."""
    t = normalize(parent.theta)
    contrarian: dict[str, Any] = {
        "start_mode": "deliver" if t["start_mode"] == "build" else "build",
        "switch_rule": rng.choice([r for r in ("none", "state", "feedback") if r != t["switch_rule"]]),
        "invest_build": 1.0 - t["invest_build"],
        "invest_deliver": 1.0 - t["invest_deliver"],
        "network_share": 1.0 - t["network_share"],
        "visibility_pref": 1.0 - t["visibility_pref"],
        "overtime_rule": {"never": "always", "always": "never"}.get(t["overtime_rule"], rng.choice(("never", "always"))),
        "risk_reaction": rng.choice([r for r in ("ignore", "defuse", "lay_low") if r != t["risk_reaction"]]),
    }
    keys = sorted(contrarian)
    rng.shuffle(keys)
    chosen = sorted(keys[: rng.randint(3, 6)])
    theta = mutate(normalize({**t, **{k: contrarian[k] for k in chosen}}), rng, 0.3)
    return Proposal(theta, f"wild from {parent.id}: invert {', '.join(chosen)}; learning goal: test whether the "
                           f"leader's region is a local optimum", "wild", parent.family, (parent.id,),
                    {"inverted": chosen})
