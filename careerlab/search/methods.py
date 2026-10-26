"""Outer-loop policy search at equal cost: baselines, the CareerLab method and its ablations.

Budget is in cost units: a complete target-actor episode costs ``env.c_target``
(default 10) and a complete cheap-actor episode ``env.c_cheap`` (default 1);
a truncated episode costs the share of the game it plays. This mirrors
scarce target evaluations against plentiful cheap ones.

Substitution, stated plainly: the real lab's generation step is an Opus
orchestrator writing natural-language policy revisions. Here generation is
emulated by the parametric operators in ``careerlab.search.operators``.
Everything after generation (block allocation, dormancy, robustness refits,
audits and reopening, cheap-actor calibration and pruning authority,
specialization gating, freeze and confirmation) runs through the same
statistics module the real lab uses. A result here is evidence about that
machinery under known mechanisms, not about LLM-written policies or the real
game.

Methods (``run_search(method, env, budget, rng)``):

- ``best_of_n``: N fresh family draws, equal target episodes each, best mean.
- ``refine_leader``: hill climbing; each refine child of the leader gets a
  fixed n and replaces it if its mean is higher. Target only.
- ``racing``: iterated F-Race/irace-like racing; a pool is evaluated in
  blocks, candidates are eliminated by the pre-registered DORMANT posterior
  rule (or, optionally, disjoint hedged-capital confidence sequences), and
  new candidates are sampled around the elites when the race thins out.
- ``full``: the CareerLab method (see ``_Full``).
- ablations of ``full``: ``no_diversity``, ``no_reopen``, ``no_calibration``,
  ``partial_screening``, ``no_specialization``, ``target_only``. Each changes
  one component and nothing else; ``no_diversity`` draws every root policy
  from one randomly chosen family, and generation afterwards (operator
  weights, the ``new_family`` operator over all families, the fallback when no
  parent has room) is exactly ``full``'s.
"""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Protocol as TypingProtocol

import numpy as np
from scipy import stats as st

from careerlab import stats
from careerlab.search.archive import Node, Outcome, PolicyArchive
from careerlab.search.operators import (ALL_FAMILIES, FAMILY_HYPOTHESES, CandidateStream, Proposal, new_family,
                                        recombine, refine, specialize, wild)
from careerlab.synthetic.policy import mutate

DORMANT_TRIGGER = "audit draw (q per block), a new child hypothesis built on it, or an epoch change"


class SearchEnv(TypingProtocol):
    """What a search method needs from an evaluation environment (see ``testbed.SynthEnv``)."""

    c_target: float
    c_cheap: float
    proxy_month: int
    stream_seed: int
    incumbent: dict[str, Any]

    def cost(self, role: str, horizon: int | None = None) -> float: ...

    def episodes(self, theta: dict[str, Any], role: str, n: int, start: int = 1, horizon: int | None = None,
                 stream: str = "dev", block: int = 0) -> list[Outcome]: ...


@dataclass(frozen=True)
class SearchConfig:
    """Knobs of every method; defaults follow ``lab/protocol/prereg-v1.json`` where it fixes one."""

    protocol: stats.Protocol = stats.Protocol()
    # baselines
    n_per_candidate: int = 10  # best_of_n and refine_leader: target episodes per candidate
    n_init: int = 7  # refine_leader: initial candidates (one per family)
    pool_size: int = 24  # racing: candidates per race iteration
    race_rule: str = "posterior"  # racing elimination: "posterior" (DORMANT rule) or "cs" (disjoint CS)
    min_survivors: int = 3  # racing: start a new iteration below this many survivors
    race_iterations: int = 5  # racing: planned iterations; each gets remaining budget / iterations left (irace)
    # full method
    roots_per_family: int = 2
    block_slots: int = 20  # target episodes per block
    gen_share: float = 0.25  # minimum budget share of a block for new candidates (prereg >= 0.20)
    widening_alpha: float = 0.5
    beta: float = 0.5  # top-two Thompson
    audit_q: float = 0.2
    audit_episodes: int = 2
    confirm_share: float = 0.15
    n_cal_cheap: int = 6  # cheap episodes per target-evaluated policy, for calibration
    n_screen_cheap: int = 8  # cheap episodes before a pruning decision
    stagnation_blocks: int = 3
    spec_delta: float = 4.0  # specialization accepted if P(mu_spec > mu_parent + delta) >= spec_p
    spec_p: float = 0.8
    calendar_tests: float = 0.0  # share of specializations that test a calendar hypothesis (diagnostic)
    op_weights: tuple[tuple[str, float], ...] = (("refine", 0.45), ("recombine", 0.15), ("specialize", 0.15),
                                                 ("new_family", 0.25))
    n_boot: int = 2000
    # ablation switches
    diversity: bool = True  # False: all roots from one family (generation unchanged)
    reopen: bool = True
    cheap: str = "calibrated"  # calibrated | uncalibrated (prunes from the start) | off
    screening: str = "cheap"  # cheap | partial (successive halving on truncated episodes)
    specialization: bool = True
    proxy_actor: str = "target"  # actor of the truncated-episode proxy
    sh_batch: int = 4  # candidates per successive-halving batch; 4 -> 1 keeps generation spend near full's
    sh_keep: int = 1


FULL_VARIANTS: dict[str, dict[str, Any]] = {
    "full": {},
    "no_diversity": {"diversity": False},
    "no_reopen": {"reopen": False},
    "no_calibration": {"cheap": "uncalibrated"},
    "partial_screening": {"screening": "partial", "cheap": "off"},
    "no_specialization": {"specialization": False},
    "target_only": {"cheap": "off"},
}
ABLATION_CHANGES: dict[str, str] = {
    "no_diversity": "all roots drawn from one random family (same root count); generation unchanged",
    "no_reopen": "dormancy is permanent: no audits, no reopening on new child hypotheses",
    "no_calibration": "cheap actor prunes from the start, without calibration or pruning authority",
    "partial_screening": "successive halving on truncated (proxy_month) target episodes; no cheap actor",
    "no_specialization": "no specialize operator (its weight goes to refine)",
    "target_only": "no cheap actor: every evaluation on target",
}
METHODS: tuple[str, ...] = ("best_of_n", "refine_leader", "racing", *FULL_VARIANTS)
# Spend on new candidates; the generation quota and ``generation_share`` count these purposes only
# (reopen episodes for a dormant parent are re-evaluations, not new candidates).
GEN_PURPOSES: tuple[str, ...] = ("initial", "screen", "proxy", "calibration")


@dataclass
class SearchResult:
    method: str
    selected: str
    selected_theta: dict[str, Any]
    selected_family: str
    estimate: float  # what the method would report as the selected policy's target mean
    estimate_kind: str  # fresh (confirmation batch) | in_sample (selection data) | posterior
    finalists: list[str]
    confirmation: dict[str, Any]
    history: list[dict[str, Any]]
    cost_by_actor: dict[str, float]
    cost_by_purpose: dict[str, float]
    spent: float
    budget: float
    rejected: list[str]  # set aside by an elimination rule and still set aside at the end
    families_explored: int
    n_policies: int
    extra: dict[str, Any] = field(default_factory=dict)
    archive: PolicyArchive = field(default_factory=PolicyArchive, repr=False)

    def to_dict(self, with_archive: bool = False) -> dict[str, Any]:
        out = {k: v for k, v in self.__dict__.items() if k != "archive"}
        if with_archive:
            out["archive"] = self.archive.summary()
        return out


class _Run:
    """Shared bookkeeping: archive, budget ledger, decision history and evaluation."""

    def __init__(self, method: str, env: SearchEnv, budget: float, rng: np.random.Generator, cfg: SearchConfig):
        self.method = method
        self.env = env
        self.budget = float(budget)
        self.rng = rng
        self.prng = random.Random(int(rng.integers(2**62)))
        self.cfg = cfg
        self.pr = cfg.protocol
        self.archive = PolicyArchive()
        self.stream = CandidateStream(env.stream_seed)
        self.by_actor: Counter[str] = Counter()
        self.by_purpose: Counter[str] = Counter()
        self.history: list[dict[str, Any]] = []
        self.block = 0
        self.c_t = env.cost("target")

    @property
    def spent(self) -> float:
        return float(sum(self.by_actor.values()))

    def log(self, kind: str, subject: str | None, explanation: str, **extra: Any) -> None:
        self.history.append({"block": self.block, "kind": kind, "subject": subject, "explanation": explanation,
                             **extra})

    def add(self, prop: Proposal) -> Node | None:
        node, new = self.archive.add(prop.theta, prop.family, prop.parents, prop.operator, prop.hypothesis,
                                     self.block, prop.meta)
        return node if new else None

    def fresh(self, family: str) -> Node | None:
        """A shared stream draw of one family (common random numbers across methods)."""
        return self.add(Proposal(self.stream.draw(family), f"new family {family}: {FAMILY_HYPOTHESES[family]}",
                                 "new_family", family))

    def evaluate(self, node: Node, role: str, n: int, purpose: str, horizon: int | None = None,
                 stream: str = "dev", cap: float | None = None) -> list[Outcome]:
        """Play up to ``n`` episodes without spending beyond ``cap`` (default: the whole budget).

        Confirmation episodes (stream "confirm") are kept in ``node.meta`` and
        never reach the cells that selection reads.
        """
        cap = self.budget if cap is None else cap
        unit = self.env.cost(role, horizon)
        n = min(int(n), int((cap - self.spent + 1e-9) // unit))
        if n <= 0:
            return []
        partial = horizon is not None
        if stream == "confirm":
            start = len(node.meta.get("confirmation", [])) + 1
        else:
            start = len((node.partial if partial else node.outcomes)[role]) + 1
        outs = self.env.episodes(node.theta, role, n, start=start, horizon=horizon, stream=stream, block=self.block)
        self.by_actor[role] += unit * n
        self.by_purpose[purpose] += unit * n
        for o in outs:
            o.purpose = purpose
            if stream == "confirm":
                node.meta.setdefault("confirmation", []).append(o.Y)
            else:
                self.archive.record(node.id, role, o, partial=partial)
        return outs

    def result(self, selected: Node, estimate: float, kind: str, finalists: list[str] | None = None,
               confirmation: dict[str, Any] | None = None, rejected: list[str] | None = None,
               extra: dict[str, Any] | None = None) -> SearchResult:
        return SearchResult(
            method=self.method, selected=selected.id, selected_theta=dict(selected.theta),
            selected_family=selected.family, estimate=float(estimate), estimate_kind=kind,
            finalists=finalists or [selected.id], confirmation=confirmation or {}, history=self.history,
            cost_by_actor={k: float(v) for k, v in self.by_actor.items()},
            cost_by_purpose={k: float(v) for k, v in self.by_purpose.items()}, spent=self.spent,
            budget=self.budget, rejected=rejected or [], families_explored=len(self.archive.families()),
            n_policies=sum(1 for n in self.archive.nodes.values() if n.status != "retired"),
            extra={"duplicates_rejected": self.archive.duplicates, **(extra or {})}, archive=self.archive)


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

def _round_robin(run: _Run, count: int) -> list[Node]:
    nodes = []
    for j in range(count):
        node = run.fresh(ALL_FAMILIES[j % len(ALL_FAMILIES)])
        if node is not None:
            nodes.append(node)
    return nodes


def _best_of_n(run: _Run) -> SearchResult:
    n = run.cfg.n_per_candidate
    nodes = _round_robin(run, max(1, int(run.budget // (n * run.c_t))))
    for node in nodes:
        run.evaluate(node, "target", n, "select")
    nodes = [x for x in nodes if x.n()] or nodes
    best = max(nodes, key=lambda x: x.mean())
    run.log("select", best.id, f"highest mean {best.mean():.1f} of {len(nodes)} fresh candidates with {n} target "
                               f"episodes each (in-sample estimate, no confirmation)")
    return run.result(best, best.mean(), "in_sample")


def _refine_leader(run: _Run) -> SearchResult:
    n = run.cfg.n_per_candidate
    init = _round_robin(run, run.cfg.n_init)
    for node in init:
        run.evaluate(node, "target", n, "select")
    leader = max((x for x in init if x.n()), key=lambda x: x.mean())
    run.log("leader", leader.id, f"initial leader, mean {leader.mean():.1f} over {leader.n()} episodes")
    while run.budget - run.spent >= n * run.c_t:
        run.block += 1
        child = None
        for attempt in range(8):
            prop = refine(leader, leader.descriptors("target"), run.prng) if attempt < 4 else Proposal(
                mutate(leader.theta, run.prng, 0.2), f"mutate {leader.id} (refine kept proposing duplicates)",
                "mutate", leader.family, (leader.id,))
            child = run.add(prop)
            if child is not None:
                break
        if child is None:
            break
        run.evaluate(child, "target", n, "select")
        if child.mean() > leader.mean():
            run.log("accept", child.id, f"child mean {child.mean():.1f} > leader {leader.id} {leader.mean():.1f}: "
                                        f"new leader ({child.hypothesis})")
            leader = child
        else:
            run.log("discard", child.id, f"child mean {child.mean():.1f} <= leader {leader.id} {leader.mean():.1f}")
    return run.result(leader, leader.mean(), "in_sample")


def _cs_eliminate(run: _Run, survivors: list[Node]) -> dict[str, str]:
    """Eliminate candidates whose hedged-capital CS lies wholly below the best lower bound."""
    ready = [s for s in survivors if s.n() >= run.pr.n0]
    if len(ready) < 2:
        return {}
    cs = {s.id: stats.hedged_capital_cs(s.ys(), bounds=(0.0, stats.Y_MAX)) for s in ready}
    best = max(cs, key=lambda k: cs[k][0])
    return {k: f"CS upper bound {hi:.1f} < best lower bound {cs[best][0]:.1f} ({best})"
            for k, (lo, hi) in cs.items() if hi < cs[best][0]}


def _racing(run: _Run) -> SearchResult:
    cfg, pr = run.cfg, run.pr
    survivors = _round_robin(run, cfg.pool_size)
    scale, iteration = 0.2, 1
    iter_start, iter_budget = 0.0, run.budget / cfg.race_iterations
    post: dict[str, stats.Posterior] = {}
    while run.budget - run.spent >= run.c_t and survivors:
        run.block += 1
        for node in survivors:
            run.evaluate(node, "target", 1, "race")
        post = stats.partial_pool(run.archive.cells("target"))
        if cfg.race_rule == "cs":
            out = _cs_eliminate(run, survivors)
        else:
            dec = stats.decide({s.id: post[s.id] for s in survivors if s.id in post}, protocol=pr)
            out = {k: d.reason for k, d in dec.items() if d.action == "DORMANT"}
        for k, why in out.items():
            run.archive.set_status(k, "dormant", f"eliminated: {why}", None, run.block)
            run.log("eliminate", k, why)
        survivors = [s for s in survivors if s.id not in out]
        thin = len(survivors) <= cfg.min_survivors
        spent_out = run.spent - iter_start >= iter_budget
        if survivors and (thin or spent_out or min(s.n() for s in survivors) >= pr.n_max_screen):
            ranked = sorted(survivors, key=lambda s: post[s.id].mean if s.id in post else -math.inf, reverse=True)
            elites = ranked[:cfg.min_survivors]
            for s in ranked[cfg.min_survivors:]:
                run.archive.set_status(s.id, "dormant", "eliminated: not an elite when the race iteration ended",
                                       None, run.block)
            new: list[Node] = []
            weights = [len(elites) - i for i in range(len(elites))]
            for _ in range(cfg.pool_size // 2):
                parent = run.prng.choices(elites, weights)[0]
                for _attempt in range(5):
                    node = run.add(Proposal(mutate(parent.theta, run.prng, scale),
                                            f"irace iteration {iteration + 1}: sample around elite {parent.id} "
                                            f"(scale {scale:.2f})", "mutate", parent.family, (parent.id,)))
                    if node is not None:
                        new.append(node)
                        break
            run.log("iteration", None, f"race iteration {iteration} ended with {len(survivors)} survivors "
                                       f"({'thinned out' if thin else 'iteration budget spent'}); elites "
                                       f"{[e.id for e in elites]} carried over with {len(new)} new candidates")
            iteration += 1
            scale = max(0.05, scale * 0.8)
            survivors = elites + new
            iter_start = run.spent
            iter_budget = (run.budget - run.spent) / max(1, cfg.race_iterations - iteration + 1)
    pool = [s for s in survivors if s.n() >= pr.n0 and s.id in post] or \
        [n for n in run.archive.nodes.values() if n.id in post]
    best = max(pool, key=lambda s: post[s.id].mean)
    rejected = [n.id for n in run.archive.by_status("dormant")]
    run.log("select", best.id, f"highest posterior mean {post[best.id].mean:.1f} among {len(pool)} survivors "
                               f"(raw mean {best.mean():.1f}, n={best.n()})")
    return run.result(best, best.mean(), "in_sample", rejected=rejected, extra={"iterations": iteration})


# ---------------------------------------------------------------------------
# The CareerLab method
# ---------------------------------------------------------------------------

class _Full(_Run):
    """CareerLab outer loop (``full``) and, through ``SearchConfig`` switches, its ablations.

    Root: diverse behaviour families (``roots_per_family`` fresh draws each;
    ``no_diversity`` draws the same number from one family).
    Blocks of ``block_slots`` target episodes; per block:

    1. top-up: active policies with fewer than n0 complete target episodes;
    2. generation: at least ``gen_share`` of the block's budget goes to new
       candidates (refine / recombine / specialize / new family; wild on
       stagnation), counting top-up but not the reopen episodes a new child
       triggers on a dormant parent. Parents are drawn by Thompson sampling
       from their posteriors plus their family's recent child-minus-parent
       gain, and a family may hold at most ceil((1 + N_f)^alpha) derived
       policies, N_f being its terminal target episodes (progressive
       widening); when no family has room, a new family is drawn instead;
    3. screening of new candidates: with pruning authority, n_screen cheap
       episodes and the DORMANT rule on cheap posteriors (``partial``:
       successive halving on month-``proxy_month`` truncated episodes);
    4. racing: remaining slots by top-two Thompson sampling among active
       policies on the posteriors of the last block boundary;
    5. audit: with probability q one dormant policy (logged inclusion
       probability q / #dormant) gets ``audit_episodes`` target episodes and
       is reactivated at P(mu >= mu_L - delta_s) >= p_reactivate;
    6. decision at the boundary on prefix-complete complete episodes:
       normal partial pooling, DORMANT rule, Bayesian-bootstrap/Student-t
       robustness (a flipped dormancy is not acted on), specialization gate,
       stagnation, and the cheap actor's pruning authority (calibration plus
       a retrospective audit of what cheap pruning would have retired among
       calibrated policies; real audits revoke it per family).

    Freeze: the top policy by posterior mean (plus the runner-up if P(best) >=
    p_promote) among eligible policies (a specialization only once accepted),
    then a fresh confirmation batch on target for finalists and the incumbent
    that never feeds selection.
    """

    def search(self) -> SearchResult:
        cfg = self.cfg
        self.sel_budget = self.budget * (1.0 - cfg.confirm_share)
        self.authority = cfg.cheap == "uncalibrated"
        self.authority_ever = self.authority
        self.revoked: set[str] = set()
        self.audits: list[dict[str, Any]] = []
        self.trace: list[float] = []
        self.stagnant = False
        self.gains: dict[str, list[float]] = defaultdict(list)
        self.gain_seen: set[str] = set()
        self.post: dict[str, stats.Posterior] = {}
        self.ncell: dict[str, int] = {}
        self.inconclusive = 0
        self.empty_gen_blocks = 0
        self.last_cal: dict[str, Any] = {}
        # The ablation narrows the root only; new_family keeps drawing from every family.
        self.families = list(ALL_FAMILIES)
        self.root_families = self.families if cfg.diversity else [self.prng.choice(ALL_FAMILIES)]
        self.roots()
        self.decision()
        while self.sel_budget - self.spent >= self.c_t:
            self.block += 1
            start, gen0 = self.spent, self.gen_spent()
            end = min(start + cfg.block_slots * self.c_t, self.sel_budget)
            self.top_up(end)
            self.generate(gen0 + cfg.gen_share * (end - start), end)
            self.race(end)
            self.audit()
            self.decision()
            if self.spent <= start:
                break
        return self.freeze_and_confirm()

    # -- evaluation helpers -------------------------------------------------
    def gen_spent(self) -> float:
        return float(sum(self.by_purpose[p] for p in GEN_PURPOSES))

    def initial(self, nodes: list[Node], cap: float, purpose: str = "initial") -> None:
        """Bring new or reopened policies to n0 complete target episodes (+ calibration cheap episodes)."""
        for node in nodes:
            self.evaluate(node, "target", self.pr.n0 - node.n(), purpose, cap=cap)
            if self.cfg.cheap == "calibrated" and node.n() >= 2:
                self.evaluate(node, "cheap", self.cfg.n_cal_cheap - node.n("cheap"),
                              "root_calibration" if purpose == "root" else "calibration", cap=cap)

    def authority_for(self, family: str) -> bool:
        if self.cfg.cheap == "uncalibrated":
            return True
        return self.cfg.cheap == "calibrated" and self.authority and family not in self.revoked

    def screen(self, nodes: list[Node], cap: float, keep_share: float = 0.0) -> list[Node]:
        """Screening before target spend; returns the candidates that go on to target episodes."""
        if self.cfg.screening == "partial":
            return self.sh_screen(nodes, cap, keep_share)
        cheap = [n for n in nodes if self.authority_for(n.family)]
        return [n for n in nodes if n not in cheap] + self.cheap_screen(cheap, cap)

    def cheap_screen(self, nodes: list[Node], cap: float) -> list[Node]:
        if not nodes:
            return []
        for node in nodes:
            self.evaluate(node, "cheap", self.cfg.n_screen_cheap - node.n("cheap"), "screen", cap=cap)
        cells = self.archive.cells("cheap")
        post = stats.partial_pool(cells)
        ref = [k for k in post if self.archive[k].status in ("active", "frozen") and len(cells[k][1]) >= self.pr.n0]
        if not ref:
            return nodes
        lead = max(ref, key=lambda k: post[k].mean)
        passed = []
        for node in nodes:
            if node.id not in post or node.id == lead:
                passed.append(node)
                continue
            pw = stats.prob_within(post[node.id], post[lead], self.pr.delta_s)
            if pw < self.pr.p_dormant:
                why = (f"cheap-pruned: P(mu_cheap >= mu_cheap_L - {self.pr.delta_s:g}) = {pw:.3f} < "
                       f"{self.pr.p_dormant:g} after {node.n('cheap')} cheap episodes (cheap leader {lead})")
                self.archive.set_status(node.id, "dormant", why, DORMANT_TRIGGER, self.block)
                self.log("cheap_pruned", node.id, why)
            else:
                passed.append(node)
        return passed

    def sh_screen(self, nodes: list[Node], cap: float, keep_share: float = 0.0) -> list[Node]:
        """Successive halving on truncated episodes (the ``partial_screening`` ablation; proxy never validated)."""
        role, h = self.cfg.proxy_actor, self.env.proxy_month
        keep_final = max(self.cfg.sh_keep, math.ceil(len(nodes) * keep_share))
        alive, n_per = list(nodes), 2
        while len(alive) > keep_final:
            for node in alive:
                self.evaluate(node, role, n_per - len(node.partial[role]), "proxy", horizon=h, cap=cap)
            means = {n.id: float(np.mean([o.Y for o in n.partial[role]])) if n.partial[role] else -1.0 for n in alive}
            alive.sort(key=lambda n: means[n.id], reverse=True)
            keep = max(keep_final, len(alive) // 2)
            for rank, node in enumerate(alive[keep:], keep + 1):
                why = (f"proxy-pruned: month-{h} {role} proxy mean {means[node.id]:.1f} ranked {rank}/{len(alive)} "
                       f"after {len(node.partial[role])} truncated episodes (successive halving, proxy not validated)")
                self.archive.set_status(node.id, "dormant", why, DORMANT_TRIGGER, self.block)
                self.log("proxy_pruned", node.id, why)
            alive, n_per = alive[:keep], n_per * 2
        return alive

    # -- phases ---------------------------------------------------------------
    def roots(self) -> None:
        cfg = self.cfg
        count = len(ALL_FAMILIES) * cfg.roots_per_family  # same root budget with or without diversity
        fams = [self.root_families[j % len(self.root_families)] for j in range(count)]
        nodes = [x for x in (self.fresh(f) for f in fams) if x is not None]
        self.log("roots", None, f"{len(nodes)} root policies from families {sorted(set(fams))}")
        if cfg.screening == "partial" or cfg.cheap == "uncalibrated":
            survivors = self.screen(nodes, self.sel_budget, keep_share=0.25)
        else:
            survivors = nodes
        self.initial(survivors, self.sel_budget, purpose="root")

    def top_up(self, cap: float) -> None:
        self.initial([n for n in self.archive.by_status("active") if n.n() < self.pr.n0], cap)

    def generate(self, until: float, cap: float) -> None:
        """New candidates until spend on ``GEN_PURPOSES`` reaches ``until`` (reopen spend does not count)."""
        cfg = self.cfg
        made = 0
        room = self.gen_spent() < until and cap - self.spent >= self.pr.n0 * self.c_t
        while self.gen_spent() < until and cap - self.spent >= self.pr.n0 * self.c_t:
            batch = cfg.sh_batch if cfg.screening == "partial" else 1
            nodes = [x for x in (self.propose() for _ in range(batch)) if x is not None]
            if not nodes:
                break
            made += len(nodes)
            self.initial(self.screen(nodes, cap), cap)
        if room and not made:  # a stall: the block had budget for new candidates but generation produced none
            self.empty_gen_blocks += 1
            self.log("generation_stalled", None, "no new candidate this block (every proposal was a duplicate)")

    def propose(self) -> Node | None:
        cfg = self.cfg
        weights = dict(cfg.op_weights)
        if not cfg.specialization:
            weights["refine"] = weights.get("refine", 0.0) + weights.pop("specialize", 0.0)
        ops, ws = list(weights), list(weights.values())
        forced = None
        if self.stagnant:
            forced, self.stagnant = "wild", False
        for _attempt in range(6):
            op = forced or self.prng.choices(ops, ws)[0]
            forced = None
            prop = self.make_proposal(op)
            if prop is None:
                continue
            node = self.add(prop)
            if node is None:
                continue
            self.log("generate", node.id, prop.hypothesis, operator=prop.operator, parents=list(prop.parents))
            if cfg.reopen:
                for pid in prop.parents:
                    parent = self.archive[pid]
                    if parent.status == "dormant":
                        self.archive.set_status(pid, "active", f"reopened: new child hypothesis {node.id}", None,
                                                self.block)
                        self.evaluate(parent, "target", cfg.audit_episodes, "reopen", cap=self.sel_budget)
                        self.log("reopen", pid, f"new child hypothesis {node.id} built on dormant {pid}")
            return node
        return None

    def make_proposal(self, op: str) -> Proposal | None:
        if op == "new_family":
            return new_family(self.prng, self.stream, families=self.families)
        parent = self.pick_parent()
        if parent is None:  # no family has room under progressive widening: widen by a new family
            return new_family(self.prng, self.stream, families=self.families)
        if op == "refine":
            return refine(parent, parent.descriptors("target"), self.prng)
        if op == "specialize":
            return specialize(parent, self.prng, calendar=self.prng.random() < self.cfg.calendar_tests)
        if op == "wild":
            return wild(parent, self.prng)
        other = self.pick_parent(exclude=parent)
        return recombine(parent, other, self.prng) if other is not None else refine(
            parent, parent.descriptors("target"), self.prng)

    def room(self, family: str) -> bool:
        n_f = self.archive.family_episodes(family)
        return self.archive.family_children(family) < math.ceil((1 + n_f) ** self.cfg.widening_alpha)

    def pick_parent(self, exclude: Node | None = None) -> Node | None:
        """Thompson draw from the posteriors plus the family's recent development gain (potential)."""
        cands = [n for n in self.archive.by_status("active", "dormant")
                 if n.id in self.post and self.ncell.get(n.id, 0) >= self.pr.n0 and n is not exclude
                 and self.room(n.family)]
        if exclude is not None:
            cands = [c for c in cands if c.family != exclude.family] or cands
        if not cands:
            return None
        best, best_score = None, -math.inf
        for node in cands:
            p = self.post[node.id]
            gains = self.gains.get(node.family, [])[-3:]
            score = p.mean + p.sd * self.rng.standard_normal() + (max(0.0, float(np.mean(gains))) if gains else 0.0)
            if score > best_score:
                best, best_score = node, score
        return best

    def race(self, cap: float) -> None:
        slots = int((cap - self.spent + 1e-9) // self.c_t)
        keys = [n.id for n in self.archive.by_status("active") if self.ncell.get(n.id, 0) >= self.pr.n0]
        if slots <= 0 or not keys:
            return
        probs = stats.top_two_probs({k: self.post[k] for k in keys}, self.cfg.beta, self.rng)
        counts = self.rng.multinomial(slots, np.array([probs[k] for k in keys]))
        for k, c in zip(keys, counts):
            if c:
                self.evaluate(self.archive[k], "target", int(c), "race", cap=cap)

    def leader(self, post: dict[str, stats.Posterior], ncell: dict[str, int]) -> str | None:
        active = [n.id for n in self.archive.by_status("active") if n.id in post]
        ready = [k for k in active if ncell.get(k, 0) >= self.pr.n0] or active
        return max(ready, key=lambda k: post[k].mean) if ready else None

    def audit(self) -> None:
        if not self.cfg.reopen:
            return
        dormant = self.archive.by_status("dormant")
        if not dormant or self.prng.random() >= self.cfg.audit_q:
            return
        node = dormant[min(int(self.prng.random() * len(dormant)), len(dormant) - 1)]
        incl = self.cfg.audit_q / len(dormant)
        reason = node.dormancy_reason or ""
        if not self.evaluate(node, "target", self.cfg.audit_episodes, "audit", cap=self.sel_budget):
            return
        cells = self.archive.cells("target", at_block=self.block)
        post = stats.partial_pool(cells)
        lead = self.leader(post, {k: len(v[1]) for k, v in cells.items()})
        if lead is None or node.id not in post:
            return
        pw = stats.prob_within(post[node.id], post[lead], self.pr.delta_s)
        flag = pw >= self.pr.p_reactivate
        self.audits.append({"node": node.id, "block": self.block, "flag": bool(flag), "inclusion_prob": incl,
                            "p_within": pw, "reason": reason})
        why = (f"audit (inclusion prob {incl:.3f}): P(mu >= mu_L - {self.pr.delta_s:g}) = {pw:.3f} "
               f"{'>=' if flag else '<'} {self.pr.p_reactivate:g} after {node.n()} target episodes")
        self.log("audit", node.id, why, reactivated=bool(flag))
        if flag:
            self.archive.set_status(node.id, "active", f"reactivated by {why}", None, self.block)
            if reason.startswith("cheap-pruned") and self.cfg.cheap == "calibrated" and node.family not in self.revoked:
                self.revoked.add(node.family)
                self.log("authority_revoked", node.family, f"audited false rejection of cheap-pruned {node.id}: "
                                                           f"cheap pruning authority revoked for family {node.family}")

    def decision(self) -> None:
        """Block-boundary decisions on prefix-complete complete target episodes."""
        cfg, pr = self.cfg, self.pr
        cells = self.archive.cells("target", at_block=self.block)
        if not cells:
            return
        post = stats.partial_pool(cells)
        self.post, self.ncell = post, {k: len(v[1]) for k, v in cells.items()}
        lead = self.leader(post, self.ncell)
        if lead is None:
            return
        for node in self.archive.nodes.values():  # development potential: child-minus-parent gains
            if (node.id in post and node.parents and node.id not in self.gain_seen
                    and self.ncell[node.id] >= pr.n0 and node.parents[0] in post):
                self.gain_seen.add(node.id)
                self.gains[node.family].append(post[node.id].mean - post[node.parents[0]].mean)
        active = [n.id for n in self.archive.by_status("active") if n.id in post]
        dec = stats.decide({k: post[k] for k in active}, lead, pr)
        dormant = [k for k, d in dec.items() if d.action == "DORMANT"]
        if dormant:
            fits = stats.robust_fits(cells, rng=self.rng, n_boot=cfg.n_boot)
            fits = {name: {k: f[k] for k in active} for name, f in fits.items()}
            rob = stats.decision_is_robust({k: cells[k] for k in active}, pr, leader=lead, fits=fits)
            for k in dormant:
                if k in rob.dormancy_flips:
                    self.inconclusive += 1
                    self.log("dormancy_inconclusive", k, f"{dec[k].reason}; not acted on: {rob.explanation}")
                    continue
                self.archive.set_status(k, "dormant", dec[k].reason, DORMANT_TRIGGER, self.block)
                self.log("dormant", k, dec[k].reason)
        for node in self.archive.by_status("active"):
            meta = node.meta
            if not meta.get("specialization") or meta.get("accepted") or node.id not in post:
                continue
            base = meta.get("base")
            if base in post and self.ncell[node.id] >= pr.n0 and self.ncell[base] >= pr.n0:
                a, b = post[node.id], post[base]
                p = float(st.norm.sf((cfg.spec_delta - (a.mean - b.mean)) / math.sqrt(a.var + b.var)))
                meta["p_accept"] = p
                if p >= cfg.spec_p and not meta.get("diagnostic"):
                    meta["accepted"] = True
                    self.log("specialization_accepted", node.id, f"P(mu > mu_{base} + {cfg.spec_delta:g}) = {p:.3f} "
                                                                 f">= {cfg.spec_p:g} as complete policies")
        self.trace.append(post[lead].mean)
        k = cfg.stagnation_blocks
        self.stagnant = len(self.trace) > k and max(self.trace[-k:]) - self.trace[-k - 1] < pr.delta_s / 2
        if self.stagnant:
            self.log("stagnation", lead, f"leader posterior mean gained < {pr.delta_s / 2:g} over {k} blocks: "
                                         f"next generation slot is a contrarian (wild) hypothesis")
        if cfg.cheap == "calibrated":
            self.update_authority(post, lead)

    def update_authority(self, post: dict[str, stats.Posterior], lead: str) -> None:
        pr = self.pr
        both = [n for n in self.archive.nodes.values() if n.status != "retired" and n.n("cheap") >= 2
                and self.ncell.get(n.id, 0) >= 2]
        if len(both) < 3:
            return
        cal = stats.calibration({n.id: n.ys("cheap") for n in both}, {n.id: n.ys("target", self.block) for n in both},
                                n_boot=1000, rng=self.rng)
        cp = stats.partial_pool({n.id: (n.family, n.ys("cheap")) for n in both})
        cl = max(cp, key=lambda k: cp[k].mean)
        shadow = [k for k in cp if k != cl and k != lead
                  and stats.prob_within(cp[k], cp[cl], pr.delta_s) < pr.p_dormant
                  and stats.prob_within(post[k], post[lead], pr.delta_s) >= pr.p_reactivate]
        ok, reasons = stats.pruning_authority(cal, audited_false_rejections=len(shadow))
        self.last_cal = {"k": len(both), "pearson": cal.pearson, "p_rho_gt_0_5": cal.p_rho_gt_0_5,
                         "span_target": cal.span_target, "reliability_cheap": cal.reliability_cheap,
                         "reliability_target": cal.reliability_target, "shadow_false_rejections": shadow,
                         "authority": ok}
        if ok != self.authority:
            self.log("authority_granted" if ok else "authority_withdrawn", None,
                     "; ".join(reasons) + f"; retrospective audit on the calibration set: {len(shadow)} policies "
                                          f"cheap pruning would retire but target keeps {shadow}")
        self.authority = ok
        self.authority_ever = self.authority_ever or ok

    def freeze_and_confirm(self) -> SearchResult:
        cfg, pr = self.cfg, self.pr
        cells = self.archive.cells("target")
        post = stats.partial_pool(cells)
        ncell = {k: len(v[1]) for k, v in cells.items()}
        active = [n for n in self.archive.by_status("active") if n.id in post]
        eligible = [n for n in active if ncell[n.id] >= pr.n0
                    and (not n.meta.get("specialization") or n.meta.get("accepted"))]
        pool = eligible or [n for n in active if ncell[n.id] >= pr.n0] or active or \
            [self.archive[k] for k in post]
        ranked = sorted(pool, key=lambda n: post[n.id].mean, reverse=True)
        pbest = stats.prob_best({n.id: post[n.id] for n in ranked})
        finalists = ranked[:1] + [n for n in ranked[1:2] if pbest[n.id] >= pr.p_promote]
        selected = finalists[0]
        for f in finalists:
            self.archive.set_status(f.id, "frozen", None, None, self.block)
        pending = [n.id for n in active if n.meta.get("specialization") and not n.meta.get("accepted")]
        self.log("freeze", selected.id, f"finalists {[f.id for f in finalists]} by posterior mean "
                                        f"({', '.join(f'{f.id} {post[f.id].mean:.1f}, P(best) {pbest[f.id]:.2f}' for f in finalists)})"
                                        + (f"; pending specializations not eligible: {pending}" if pending else ""))
        self.sel_budget_spent = self.spent
        inc, new = self.archive.add(self.env.incumbent, "incumbent", (), "incumbent", "incumbent (comparator only)",
                                    self.block)
        arms = finalists + ([inc] if inc not in finalists else [])
        n_conf = int((self.budget - self.spent + 1e-9) // (self.c_t * len(arms)))
        confirmation: dict[str, Any] = {"n_per_arm": n_conf, "incumbent": inc.id}
        if n_conf >= 2:
            for arm in arms:
                self.evaluate(arm, "target", n_conf, "confirm", stream="confirm")
            conf = {a.id: a.meta["confirmation"] for a in arms}
            ys = conf[selected.id]
            estimate, kind = float(np.mean(ys)), "fresh"
            confirmation.update({"means": {k: float(np.mean(v)) for k, v in conf.items()},
                                 "sd": float(np.std(ys, ddof=1))})
            if inc not in finalists:
                alpha = 0.05 / len(finalists)
                claims = {f.id: stats.welch_lower_bound(conf[f.id], conf[inc.id], alpha) for f in finalists}
                confirmation["welch_lower_vs_incumbent"] = claims
                confirmation["claims"] = [k for k, lb in claims.items() if lb > 0]
            self.log("confirm", selected.id, f"fresh confirmation, {n_conf} target episodes per arm: selected mean "
                                             f"{estimate:.1f}; never used for selection")
        else:
            estimate, kind = post[selected.id].mean, "posterior"
            self.log("confirm", selected.id, "budget left too small for a confirmation batch; reporting the "
                                             "posterior mean instead")
        audit = None
        if self.audits:
            a = stats.audit_ipw([int(x["flag"]) for x in self.audits], [x["inclusion_prob"] for x in self.audits])
            audit = {"n": a.n_audited, "reactivated": a.raw_count, "ipw_rate": a.ipw_rate, "cp": [a.cp_low, a.cp_high]}
        rejected = [n.id for n in self.archive.by_status("dormant")]
        pp = self.by_purpose
        after_roots = self.sel_budget_spent - pp["root"] - pp["root_calibration"]
        new_spend = sum(pp[p] for p in GEN_PURPOSES)
        extra = {"blocks": self.block, "authority": self.authority, "authority_ever": self.authority_ever,
                 "generation_share": new_spend / after_roots if after_roots > 0 else float("nan"),
                 "stagnation_blocks": sum(1 for h in self.history if h["kind"] == "stagnation"),
                 "revoked_families": sorted(self.revoked), "audits": audit, "inconclusive_dormancies": self.inconclusive,
                 "calibration": self.last_cal, "root_families": self.root_families,
                 "generation_empty_blocks": self.empty_gen_blocks,
                 "specializations": sum(1 for n in self.archive.nodes.values() if n.meta.get("specialization")),
                 "specializations_accepted": sum(1 for n in self.archive.nodes.values() if n.meta.get("accepted")),
                 "cheap_pruned": sum(1 for n in self.archive.nodes.values()
                                     if (n.dormancy_reason or "").startswith("cheap-pruned")),
                 "proxy_pruned": sum(1 for n in self.archive.nodes.values()
                                     if (n.dormancy_reason or "").startswith("proxy-pruned"))}
        return self.result(selected, estimate, kind, [f.id for f in finalists], confirmation, rejected, extra)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

_BASELINES: dict[str, Callable[[_Run], SearchResult]] = {
    "best_of_n": _best_of_n, "refine_leader": _refine_leader, "racing": _racing}


def method_config(method: str, config: SearchConfig | None = None) -> SearchConfig:
    """The method's configuration: ``config`` (or defaults) with the ablation switches applied."""
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}; known: {list(METHODS)}")
    base = config or SearchConfig()
    return replace(base, **FULL_VARIANTS[method]) if method in FULL_VARIANTS else base


def run_search(method: str, env: SearchEnv, budget: float, rng: np.random.Generator,
               config: SearchConfig | None = None) -> SearchResult:
    """Run one search method on ``env`` within ``budget`` cost units.

    ``rng`` drives every random decision of the method (parent draws,
    allocation, audits). Passing equal generators to different methods and
    an env whose seeds depend only on (policy, launch) gives common random
    numbers across methods.
    """
    cfg = method_config(method, config)
    if method in _BASELINES:
        return _BASELINES[method](_Run(method, env, budget, rng, cfg))
    return _Full(method, env, budget, rng, cfg).search()
