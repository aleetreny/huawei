"""Reversible policy archive: nodes, lineage, per-actor outcomes and behaviour descriptors.

The archive is the search's memory. Each node is one complete, frozen policy
(a SynthCareer ``theta`` here; a Skill bundle in the real lab) with its
parents (a multi-parent graph), the operator and hypothesis that produced it,
and every episode it played, kept per actor role so cheap and target evidence
never mix. Status follows the pre-registration: ``dormant`` is reversible and
records why and what would reopen it; ``retired`` is only for invalid or
duplicate artefacts; ``frozen`` marks finalists. Behaviour descriptors are
computed from outcomes, never from the policy text, so two policies that
behave alike look alike whatever their parameters say.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from careerlab import stats
from careerlab.synthetic.policy import normalize

STATUSES = ("active", "dormant", "retired", "frozen")
ROLES = ("target", "cheap")


def theta_hash(theta: dict[str, Any]) -> str:
    """Canonical hash of a normalized theta: equal behaviour parameters, equal hash."""
    blob = json.dumps(normalize(theta), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


@dataclass
class Outcome:
    """One episode as the lab records it (complete, or truncated at ``horizon`` for proxies)."""

    Y: float
    Q: float
    T: int
    completed: bool
    failure: str | None
    seed: int
    horizon: int = 48  # months the episode was allowed to run (the game length for complete episodes)
    launch: int = 0  # 1-based launch index within (node, role, complete or partial)
    block: int = 0
    purpose: str = ""
    resolved_block: int = 0  # block boundary by which the result is back (prefix-complete inclusion)
    monthly: tuple[float, ...] = ()  # score after each month played
    switch_month: int | None = None  # first month in deliver mode (None: never switched)
    level: int = 1
    promotions: int = 0
    grades: str = ""
    skill: int = 0
    network: int = 0
    decisions: int = 0
    recovery: int = 0  # rest / health / mental recovery / lay low / repair choices
    energy: int = 0  # Energy spent
    invest: int = 0  # Energy spent on Skill learning or Network maintenance
    invest_early: int = 0  # ... of which in months 1-12


@dataclass
class Node:
    id: str
    theta: dict[str, Any]
    hash: str
    family: str
    parents: tuple[str, ...] = ()
    operator: str = "root"
    hypothesis: str = ""
    status: str = "active"
    dormancy_reason: str | None = None
    review_trigger: str | None = None
    created_block: int = 0
    meta: dict[str, Any] = field(default_factory=dict)
    outcomes: dict[str, list[Outcome]] = field(default_factory=lambda: {r: [] for r in ROLES})
    partial: dict[str, list[Outcome]] = field(default_factory=lambda: {r: [] for r in ROLES})

    def ys(self, role: str = "target", at_block: int | None = None) -> list[float]:
        """Complete-episode utilities; with ``at_block``, only the launch-order prefix resolved by then."""
        outs = self.outcomes[role]
        if at_block is None:
            return [o.Y for o in outs]
        return stats.prefix_complete([(o.launch, o.Y if o.resolved_block <= at_block else None) for o in outs])

    def n(self, role: str = "target", at_block: int | None = None) -> int:
        return len(self.ys(role, at_block))

    def mean(self, role: str = "target") -> float:
        ys = self.ys(role)
        return sum(ys) / len(ys) if ys else float("nan")

    def descriptors(self, role: str = "target") -> dict[str, Any]:
        return descriptors(self.outcomes[role])


def descriptors(outcomes: Sequence[Outcome]) -> dict[str, Any]:
    """Behaviour descriptors of complete episodes.

    Survival (completion, Kaplan-Meier at 12/24/36, RMST), failure profile,
    share of recovery choices, investment share and timing (share of the
    investment Energy spent in months 1-12), mode-switch timing, final level,
    promotions and the share of C/D reviews. These are what the refine
    operator reads as "diagnostics" and what novelty checks would compare.
    """
    n = len(outcomes)
    if n == 0:
        return {"n": 0}
    times = [o.T for o in outcomes]
    events = [0 if o.completed else 1 for o in outcomes]
    km = stats.kaplan_meier(times, events)
    fails = Counter(o.failure for o in outcomes if not o.completed and o.failure)
    decisions = sum(o.decisions for o in outcomes)
    energy = sum(o.energy for o in outcomes)
    invest = sum(o.invest for o in outcomes)
    switched = [o.switch_month for o in outcomes if o.switch_month is not None]
    grades = "".join(o.grades for o in outcomes)
    return {
        "n": n,
        "mean_y": sum(o.Y for o in outcomes) / n,
        "completion": 1.0 - sum(events) / n,
        "km": {m: km.at(m) for m in (12, 24, 36)},
        "rmst": stats.rmst(times, events),
        "failures": {k: v / n for k, v in fails.most_common()},
        "recovery_share": sum(o.recovery for o in outcomes) / decisions if decisions else 0.0,
        "invest_share": invest / energy if energy else 0.0,
        "invest_early_share": sum(o.invest_early for o in outcomes) / invest if invest else 0.0,
        "switch_share": len(switched) / n,
        "switch_month": sum(switched) / len(switched) if switched else None,
        "mean_level": sum(o.level for o in outcomes) / n,
        "mean_promotions": sum(o.promotions for o in outcomes) / n,
        "low_grade_share": sum(grades.count(g) for g in "CD") / len(grades) if grades else 0.0,
        "mean_skill": sum(o.skill for o in outcomes) / n,
        "mean_network": sum(o.network for o in outcomes) / n,
    }


class PolicyArchive:
    """All proposed policies with lineage, status history and outcomes."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self._by_hash: dict[str, str] = {}
        self.events: list[dict[str, Any]] = []
        self.duplicates = 0

    def __len__(self) -> int:
        return len(self.nodes)

    def __getitem__(self, node_id: str) -> Node:
        return self.nodes[node_id]

    def add(self, theta: dict[str, Any], family: str, parents: Iterable[str] = (), operator: str = "root",
            hypothesis: str = "", block: int = 0, meta: dict[str, Any] | None = None) -> tuple[Node, bool]:
        """Add a proposal; returns (node, True) for a new policy or (existing node, False) for a duplicate.

        Duplicates are detected by canonical theta hash and never create a
        node: the proposal is retired on arrival and logged. An invalid theta
        (unknown parameter or choice) becomes a retired node so the attempt
        stays on record.
        """
        try:
            h = theta_hash(theta)
            theta = normalize(theta)
        except ValueError as exc:
            node = self._new(theta, "invalid:" + hashlib.sha256(repr(theta).encode()).hexdigest()[:12], family,
                             parents, operator, hypothesis, block, meta)
            self.set_status(node.id, "retired", f"invalid theta: {exc}", None, block)
            return node, False
        if h in self._by_hash:
            self.duplicates += 1
            existing = self.nodes[self._by_hash[h]]
            self.events.append({"block": block, "kind": "retired_duplicate", "subject": existing.id,
                                "operator": operator, "explanation": f"proposal by {operator} duplicates {existing.id} "
                                                                    f"(theta hash {h}); not added"})
            return existing, False
        node = self._new(theta, h, family, parents, operator, hypothesis, block, meta)
        self._by_hash[h] = node.id
        return node, True

    def _new(self, theta: dict[str, Any], h: str, family: str, parents: Iterable[str], operator: str, hypothesis: str,
             block: int, meta: dict[str, Any] | None) -> Node:
        node = Node(f"n{len(self.nodes):04d}", dict(theta), h, family, tuple(parents), operator, hypothesis,
                    created_block=block, meta=dict(meta or {}))
        self.nodes[node.id] = node
        self.events.append({"block": block, "kind": "created", "subject": node.id, "operator": operator,
                            "explanation": hypothesis})
        return node

    def set_status(self, node_id: str, status: str, reason: str | None, trigger: str | None = None,
                   block: int = 0) -> None:
        """Change status; dormancy keeps its reason and the trigger that would reopen it."""
        if status not in STATUSES:
            raise ValueError(f"unknown status {status!r}")
        node = self.nodes[node_id]
        if node.status == "retired" and status != "retired":
            raise ValueError(f"{node_id} is retired; retirement is final")
        previous = node.status
        node.status = status
        node.dormancy_reason = reason if status in ("dormant", "retired") else None
        node.review_trigger = trigger if status == "dormant" else None
        self.events.append({"block": block, "kind": f"{previous}->{status}", "subject": node_id,
                            "explanation": reason or ""})

    def record(self, node_id: str, role: str, outcome: Outcome, partial: bool = False) -> None:
        """Store an episode; truncated (proxy) episodes go to ``partial`` and never enter ``cells``."""
        node = self.nodes[node_id]
        (node.partial if partial else node.outcomes)[role].append(outcome)

    def by_status(self, *statuses: str) -> list[Node]:
        return [n for n in self.nodes.values() if n.status in statuses]

    def cells(self, role: str = "target", ids: Iterable[str] | None = None, at_block: int | None = None,
              min_n: int = 1) -> dict[str, tuple[str, list[float]]]:
        """{node id: (family, prefix-complete Y list)} for the statistics module."""
        nodes = self.nodes.values() if ids is None else (self.nodes[i] for i in ids)
        out = {}
        for node in nodes:
            if node.status == "retired":
                continue
            ys = node.ys(role, at_block)
            if len(ys) >= min_n:
                out[node.id] = (node.family, ys)
        return out

    def family_episodes(self, family: str, role: str = "target") -> int:
        """Terminal episodes in the family's subtree (N_f of progressive widening)."""
        return sum(len(n.outcomes[role]) for n in self.nodes.values() if n.family == family)

    def family_children(self, family: str) -> int:
        """Policies derived from a parent in the family (fresh family draws, duplicates and retired excluded)."""
        return sum(1 for n in self.nodes.values() if n.family == family and n.parents and n.status != "retired")

    def children(self, node_id: str) -> list[str]:
        return [n.id for n in self.nodes.values() if node_id in n.parents]

    def lineage(self, node_id: str) -> list[str]:
        """All ancestors through the multi-parent graph, nearest first."""
        seen: list[str] = []
        frontier = list(self.nodes[node_id].parents)
        while frontier:
            nxt = []
            for p in frontier:
                if p not in seen and p in self.nodes:
                    seen.append(p)
                    nxt.extend(self.nodes[p].parents)
            frontier = nxt
        return seen

    def families(self, evaluated_only: bool = True) -> set[str]:
        return {n.family for n in self.nodes.values() if n.status != "retired"
                and (not evaluated_only or any(n.outcomes[r] or n.partial[r] for r in ROLES))}

    def summary(self) -> list[dict[str, Any]]:
        """JSON-ready node table (no per-episode records)."""
        rows = []
        for n in self.nodes.values():
            rows.append({"id": n.id, "family": n.family, "parents": list(n.parents), "operator": n.operator,
                         "hypothesis": n.hypothesis, "status": n.status, "dormancy_reason": n.dormancy_reason,
                         "review_trigger": n.review_trigger, "hash": n.hash, "theta": n.theta,
                         "n_target": len(n.outcomes["target"]), "n_cheap": len(n.outcomes["cheap"]),
                         "n_partial": sum(len(v) for v in n.partial.values()),
                         "mean_target": _finite(n.mean("target")), "mean_cheap": _finite(n.mean("cheap")),
                         "meta": n.meta})
        return rows


def _finite(x: float) -> float | None:
    return None if math.isnan(x) else round(x, 3)
