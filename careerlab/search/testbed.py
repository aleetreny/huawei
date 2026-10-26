"""Equal-budget simulation testbed: search methods against known ground truth on SynthCareer.

Each replication r gives every method the same environment (same actors,
costs and seeds) and the same decision generator, so the comparison uses
common random numbers across methods: an episode's seed depends only on
(replication, stream, actor role, policy hash, launch index), so two methods
that evaluate the same policy see the same games, while different policies
of one method play independent games, as they would in the real lab where
games cannot be seeded.

Metrics per run, all from SynthCareer's ground truth:

- true target mean Y of the selected policy (``n_truth`` games on the fixed
  truth seeds, cached per process);
- simple regret against the oracle's best policy and P(regret <= 2);
- false-rejection rate: share of the policies a method set aside by an
  elimination rule (dormant at the end, eliminated, cheap- or proxy-pruned)
  whose true Y is within ``delta_t`` of the selected policy's true Y. NaN for
  methods without an elimination rule (best_of_n, refine_leader);
- distinct behaviour families explored, budget share by actor and by
  confirmation, and the bias of the reported estimate (confirmation mean, or
  the in-sample mean when a method has no confirmation) minus the truth.

The oracle (``build_oracle``) is a long search with ~100x a method's budget
on noise-free-ish evaluations: (1) ``per_family`` fresh draws from every
behaviour family plus the designed policies, ``n_screen`` games each on
common seeds; (2) the ``top`` candidates re-evaluated on ``n_mid`` games;
(3) ``generations`` rounds of mutation and crossover around the ``elites``,
children screened on ``n_child`` games and the best re-evaluated on
``n_mid``; (4) the ``final`` best re-measured on the truth seeds with
``n_final`` games; the maximum is the oracle best. It is not a proof of the
global optimum: a method can beat it (negative regret), which the report
shows as is.

CLI: ``uv run python -m careerlab.search.testbed --R 30 --budget 4000 --out <dir>``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from dataclasses import asdict, dataclass, replace
from multiprocessing import get_context
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np
from scipy import stats as st

from careerlab import stats
from careerlab.search.archive import Outcome, theta_hash
from careerlab.search.methods import ABLATION_CHANGES, METHODS, SearchConfig, SearchResult, run_search
from careerlab.synthetic import game as g
from careerlab.synthetic.game import DEFAULT_CONFIG, DONE, ENERGY, MAIN, STORY, Engine, SynthConfig, fast_episode, truth
from careerlab.synthetic.policy import (DESIGNED, FAMILIES, crossover, default_theta, make_agent, mutate, normalize,
                                        random_theta)

ORACLE_SEED_BASE = 2_000_000_000  # oracle screening games; truth uses game.TRUTH_SEED_BASE
DEFAULT_ENV: dict[str, Any] = {"config": {}, "target": "target", "cheap": "cheap_biased", "c_target": 10.0,
                               "c_cheap": 1.0, "proxy_month": 12, "pending_long": 0.0}
NO_ELIMINATION = ("best_of_n", "refine_leader")


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def play(theta: dict[str, Any], actor: str, seed: int, cfg: SynthConfig = DEFAULT_CONFIG, record: bool = True,
         max_steps: int = 3000) -> Outcome:
    """One episode, decision for decision the same as ``fast_episode``, plus behaviour counts.

    Counts recovery choices (rest, Health/mental recovery, lay low, repair),
    Energy spent and invested (Skill learning, Network maintenance) and the
    first month the policy is in deliver mode, which the archive's
    descriptors need and ``EpisodeOutcome`` does not carry.
    """
    eng = Engine(seed, cfg, record)
    agent = make_agent(theta, actor, seed)
    view, policy, choose, apply = eng.view, agent.policy, agent.choose, eng.apply
    steps = rejected = decisions = recovery = energy = invest = invest_early = 0
    switch: int | None = None
    while eng.phase != DONE and steps < max_steps:
        phase, month, styles = view.phase, view.month, view.styles
        c = choose(view)
        if switch is None and policy.mode == "deliver":
            switch = month
        err = apply(c)
        steps += 1
        if err is not None:
            rejected += 1
            continue
        decisions += 1
        if phase == STORY:
            recovery += styles[c - 1] == g.REST
        elif phase == ENERGY and c != g.ENERGY_FINISH:
            a, cost = c - 1, g.ENERGY_COST[c - 1]
            energy += cost
            if a in (g.HEALTH_REC, g.MENTAL_REC):
                recovery += 1
            elif a in (g.SKILL_LEARNING, g.NETWORK_MAINT):
                invest += cost
                invest_early += cost if month <= 12 else 0
        elif phase == MAIN:
            recovery += c - 1 in (g.LAY_LOW, g.REPAIR)
    q = round(eng.score(), 2)
    return Outcome(Y=stats.run_utility(q, eng.month, completed=eng.completed), Q=q, T=eng.month,
                   completed=eng.completed, failure=eng.failure_reason, seed=seed, horizon=cfg.months,
                   monthly=tuple(row["q"] for row in eng.history) if record else (), switch_month=switch,
                   level=eng.level, promotions=len(eng.promotions), grades="".join(eng.reviews), skill=eng.skill,
                   network=eng.network, decisions=decisions, recovery=recovery, energy=energy, invest=invest,
                   invest_early=invest_early)


def _seed(*parts: Any) -> int:
    return int.from_bytes(hashlib.blake2b(":".join(map(str, parts)).encode(), digest_size=8).digest(), "big")


def synth_config(env_config: dict[str, Any]) -> SynthConfig:
    return SynthConfig.from_dict(env_config.get("config") or {}) if env_config.get("config") else DEFAULT_CONFIG


class SynthEnv:
    """SynthCareer evaluation environment with cost accounting by actor role.

    ``episodes`` plays policies with the role's actor model; a truncated
    episode (``horizon`` months) costs ``horizon / months`` of a complete
    one. With ``pending_long`` > 0, completed episodes come back one block
    late with that probability, which exercises prefix-complete inclusion.
    """

    def __init__(self, config: SynthConfig | None = None, *, replication: int = 0, seed: int = 0,
                 target: str = "target", cheap: str = "cheap_biased", c_target: float = 10.0, c_cheap: float = 1.0,
                 proxy_month: int = 12, pending_long: float = 0.0, incumbent: dict[str, Any] | None = None,
                 record: bool = True):
        self.cfg = config or DEFAULT_CONFIG
        self.actors = {"target": target, "cheap": cheap}
        self.c_target, self.c_cheap = float(c_target), float(c_cheap)
        self.proxy_month = int(proxy_month)
        self.pending_long = float(pending_long)
        self.replication, self.seed = replication, seed
        self.stream_seed = _seed("stream", seed, replication)
        self.incumbent = normalize(incumbent or default_theta())
        self.record = record
        self._proxy: dict[int, SynthConfig] = {}

    @classmethod
    def from_config(cls, env_config: dict[str, Any], replication: int = 0, seed: int = 0) -> "SynthEnv":
        e = {**DEFAULT_ENV, **env_config}
        return cls(synth_config(e), replication=replication, seed=seed, target=e["target"], cheap=e["cheap"],
                   c_target=e["c_target"], c_cheap=e["c_cheap"], proxy_month=e["proxy_month"],
                   pending_long=e["pending_long"])

    def cost(self, role: str, horizon: int | None = None) -> float:
        base = self.c_target if role == "target" else self.c_cheap
        return base * min(1.0, horizon / self.cfg.months) if horizon else base

    def episodes(self, theta: dict[str, Any], role: str, n: int, start: int = 1, horizon: int | None = None,
                 stream: str = "dev", block: int = 0) -> list[Outcome]:
        cfg = self.cfg
        if horizon and horizon < cfg.months:
            cfg = self._proxy.setdefault(horizon, replace(self.cfg, months=horizon))
        h = theta_hash(theta)
        out = []
        for launch in range(start, start + n):
            seed = _seed(self.seed, self.replication, stream, role, h, "partial" if horizon else "full", launch)
            o = play(theta, self.actors[role], seed, cfg, self.record)
            o.launch, o.block = launch, block
            late = self.pending_long and not horizon and o.completed and random.Random(seed).random() < self.pending_long
            o.resolved_block = block + 1 if late else block
            out.append(o)
        return out


# ---------------------------------------------------------------------------
# Ground truth and oracle
# ---------------------------------------------------------------------------

_TRUTH: dict[tuple[str, str, int, str], float] = {}


def _cfg_key(cfg: SynthConfig) -> str:
    return hashlib.sha256(json.dumps(cfg.to_dict(), sort_keys=True).encode()).hexdigest()[:12]


def true_y(theta: dict[str, Any], actor: str = "target", n: int = 2000, cfg: SynthConfig = DEFAULT_CONFIG) -> float:
    """Mean Y over ``n`` games on the fixed truth seeds (common across policies), cached per process."""
    key = (theta_hash(theta), actor, n, _cfg_key(cfg))
    if key not in _TRUTH:
        _TRUTH[key] = truth(theta, actor, n, 0, cfg).mean_y
    return _TRUTH[key]


@dataclass(frozen=True)
class OracleSettings:
    seed: int = 20261026
    per_family: int = 300
    n_screen: int = 60
    top: int = 60
    n_mid: int = 600
    generations: int = 8
    children: int = 64
    n_child: int = 300
    elites: int = 8
    final: int = 20
    n_final: int = 20000


def _oracle_eval(task: tuple[dict[str, Any], str, dict[str, Any], int]) -> float:
    theta, actor, cfg_dict, n = task
    cfg = SynthConfig.from_dict(cfg_dict) if cfg_dict else DEFAULT_CONFIG
    return sum(fast_episode(theta, actor, ORACLE_SEED_BASE + i, cfg, record=False).Y for i in range(n)) / n


def _truth_task(task: tuple[dict[str, Any], str, dict[str, Any], int]) -> float:
    theta, actor, cfg_dict, n = task
    return true_y(theta, actor, n, SynthConfig.from_dict(cfg_dict) if cfg_dict else DEFAULT_CONFIG)


def build_oracle(env_config: dict[str, Any], settings: OracleSettings = OracleSettings(),
                 mapper: Callable[..., Iterable[Any]] = map) -> dict[str, Any]:
    """Long search for the best target policy (see the module docstring); ``mapper`` may be ``Pool.map``."""
    e = {**DEFAULT_ENV, **env_config}
    actor, cfg_dict, s = e["target"], dict(e.get("config") or {}), settings
    rng = random.Random(f"oracle:{s.seed}")
    cands: dict[str, dict[str, Any]] = {}
    est: dict[str, tuple[float, int]] = {}
    episodes = 0

    def add(theta: dict[str, Any]) -> str | None:
        h = theta_hash(theta)
        if h in cands:
            return None
        cands[h] = normalize(theta)
        return h

    def evaluate(hashes: Sequence[str], n: int) -> None:
        nonlocal episodes
        hashes = list(hashes)
        for h, m in zip(hashes, mapper(_oracle_eval, [(cands[h], actor, cfg_dict, n) for h in hashes])):
            est[h] = (float(m), n)
        episodes += n * len(hashes)

    def ranked(min_n: int = 0) -> list[str]:
        return sorted((h for h in est if est[h][1] >= min_n), key=lambda h: est[h][0], reverse=True)

    for fam in FAMILIES:
        for _ in range(s.per_family):
            add(random_theta(rng, fam))
    for theta in (*DESIGNED.values(), default_theta()):
        add(theta)
    evaluate(list(cands), s.n_screen)
    evaluate(ranked()[: s.top], s.n_mid)
    for _ in range(s.generations):
        elite = ranked(s.n_mid)[: s.elites]
        kids = []
        for _ in range(s.children):
            a = cands[rng.choice(elite)]
            theta = (mutate(crossover(a, cands[rng.choice(elite)], rng), rng, 0.05) if rng.random() < 0.3
                     else mutate(a, rng, rng.choice((0.05, 0.1, 0.2))))
            h = add(theta)
            if h:
                kids.append(h)
        evaluate(kids, s.n_child)
        evaluate(sorted(kids, key=lambda h: est[h][0], reverse=True)[: s.elites], s.n_mid)
    final = ranked(s.n_mid)[: s.final]
    ys = [float(y) for y in mapper(_truth_task, [(cands[h], actor, cfg_dict, s.n_final) for h in final])]
    episodes += s.n_final * len(final)
    order = sorted(range(len(final)), key=lambda i: ys[i], reverse=True)
    top = [{"hash": final[i], "true_y": ys[i], "screen_y": est[final[i]][0], "theta": cands[final[i]]} for i in order]
    return {"best_y": top[0]["true_y"], "best_theta": top[0]["theta"], "best_hash": top[0]["hash"], "top": top,
            "settings": asdict(s), "candidates_evaluated": len(est), "episodes": episodes,
            "procedure": "family draws + designed policies screened on common seeds, top re-evaluated, "
                         f"{s.generations} generations of mutation/crossover around {s.elites} elites, final "
                         f"{s.final} re-measured with {s.n_final} truth-seed games; best = max"}


def oracle_key(env_config: dict[str, Any], settings: OracleSettings) -> str:
    e = {**DEFAULT_ENV, **env_config}
    blob = json.dumps({"config": e.get("config") or {}, "target": e["target"], "settings": asdict(settings)},
                      sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def run_metrics(res: SearchResult, env: SynthEnv, oracle_best: float, n_truth: int = 2000,
                n_truth_rejected: int = 500, protocol: stats.Protocol = stats.Protocol()) -> dict[str, Any]:
    """Ground-truth metrics of one search run (see the module docstring)."""
    actor, cfg = env.actors["target"], env.cfg
    y_sel = true_y(res.selected_theta, actor, n_truth, cfg)
    regret = oracle_best - y_sel
    t_rej = [true_y(res.archive[i].theta, actor, n_truth_rejected, cfg) for i in res.rejected]
    applicable = res.method not in NO_ELIMINATION and bool(t_rej)
    false = sum(t >= y_sel - protocol.delta_t for t in t_rej)
    strict = sum(t >= y_sel - protocol.delta_s for t in t_rej)
    spent = res.spent or 1.0
    x = res.extra
    return {
        "true_y": y_sel, "regret": regret, "within2": float(regret <= 2.0),
        "frr": false / len(t_rej) if applicable else float("nan"),
        "frr_strict": strict / len(t_rej) if applicable else float("nan"),
        "n_rejected": len(t_rej), "n_false_rejections": int(false),
        "families": res.families_explored, "n_policies": res.n_policies,
        "target_share": res.cost_by_actor.get("target", 0.0) / spent,
        "cheap_share": res.cost_by_actor.get("cheap", 0.0) / spent,
        "confirm_share": res.cost_by_purpose.get("confirm", 0.0) / spent,
        "spent": res.spent, "estimate": res.estimate, "estimate_kind": res.estimate_kind,
        "bias": res.estimate - y_sel, "selected_family": res.selected_family, "selected_theta": res.selected_theta,
        "authority": x.get("authority"), "authority_ever": x.get("authority_ever"),
        "cheap_pruned": x.get("cheap_pruned"), "proxy_pruned": x.get("proxy_pruned"),
        "audits": (x.get("audits") or {}).get("n", 0) if "audits" in x else None,
        "inconclusive": x.get("inconclusive_dormancies"),
        "specializations": x.get("specializations"), "specializations_accepted": x.get("specializations_accepted"),
        "claims": len(res.confirmation.get("claims", [])), "blocks": x.get("blocks"),
        "gen_share": x.get("generation_share", float("nan")), "stagnation_blocks": x.get("stagnation_blocks"),
        "gen_stalls": x.get("generation_empty_blocks"),
    }


def _replicate(task: tuple[Any, ...]) -> list[dict[str, Any]]:
    r, methods, budget, env_config, seed, n_truth, n_rej, oracle_best, cfg = task
    rows = []
    for m in methods:
        env = SynthEnv.from_config(env_config, replication=r, seed=seed)
        t0 = time.perf_counter()
        res = run_search(m, env, budget, np.random.default_rng([seed, r]), cfg)
        search_s = time.perf_counter() - t0
        row = run_metrics(res, env, oracle_best, n_truth, n_rej)
        rows.append({"method": m, "replication": r, "search_seconds": search_s,
                     "seconds": time.perf_counter() - t0, **row})
    return rows


def _mean_ci(values: Iterable[float], level: float = 0.95) -> dict[str, float]:
    v = np.array([x for x in values if x is not None and np.isfinite(x)], dtype=float)
    n = len(v)
    if n == 0:
        return {"mean": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    m = float(v.mean())
    if n == 1:
        return {"mean": m, "lo": float("nan"), "hi": float("nan"), "n": 1}
    half = float(st.t.ppf(0.5 + level / 2, n - 1) * v.std(ddof=1) / math.sqrt(n))
    return {"mean": m, "lo": m - half, "hi": m + half, "n": n}


def _wilson(k: float, n: int, level: float = 0.95) -> dict[str, float]:
    if n == 0:
        return {"mean": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    z = float(st.norm.ppf(0.5 + level / 2))
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return {"mean": p, "lo": max(0.0, centre - half), "hi": min(1.0, centre + half), "n": n}


SUMMARY_METRICS = ("true_y", "regret", "frr", "frr_strict", "families", "n_policies", "target_share", "cheap_share",
                   "confirm_share", "bias", "n_rejected", "seconds", "gen_share", "stagnation_blocks", "blocks",
                   "cheap_pruned", "proxy_pruned", "audits", "inconclusive", "specializations",
                   "specializations_accepted", "claims", "gen_stalls")


def aggregate(rows: list[dict[str, Any]], methods: Sequence[str], references: Sequence[str] = ("best_of_n", "full"),
              ) -> dict[str, Any]:
    """Per method: mean and 95% interval over replications; paired true-Y differences to the references."""
    by = {m: sorted((r for r in rows if r["method"] == m), key=lambda r: r["replication"]) for m in methods}
    out: dict[str, Any] = {}
    for m, rs in by.items():
        s = {k: _mean_ci(r[k] for r in rs) for k in SUMMARY_METRICS}
        s["within2"] = _wilson(sum(r["within2"] for r in rs), len(rs))
        s["authority_share"] = (float(np.mean([bool(r["authority_ever"]) for r in rs]))
                                if rs and rs[0].get("authority_ever") is not None else None)
        s["estimate_kind"] = sorted({r["estimate_kind"] for r in rs})
        for ref in references:
            if ref in by and ref != m:
                truth_ref = {r["replication"]: r["true_y"] for r in by[ref]}
                s[f"diff_vs_{ref}"] = _mean_ci(r["true_y"] - truth_ref[r["replication"]] for r in rs
                                               if r["replication"] in truth_ref)
        out[m] = s
    return out


def _fmt(s: dict[str, float], digits: int = 1, pct: bool = False) -> str:
    if not s or s.get("n", 0) == 0 or not np.isfinite(s["mean"]):
        return "n/a"
    k = 100.0 if pct else 1.0
    if not np.isfinite(s["lo"]):
        return f"{k * s['mean']:.{digits}f}"
    return f"{k * s['mean']:.{digits}f} [{k * s['lo']:.{digits}f}, {k * s['hi']:.{digits}f}]"


def markdown(results: dict[str, Any]) -> str:
    """Report table: means with 95% intervals over the R replications."""
    st_ = results["settings"]
    summ = results["summary"]
    o = results["oracle"]
    lines = [
        "# Synthetic method comparison (SynthCareer, known ground truth)",
        "",
        f"R = {st_['R']} replications per method, budget {st_['budget']:g} cost units (target episode "
        f"{st_['env']['c_target']:g}, cheap episode {st_['env']['c_cheap']:g}; cheap actor `{st_['env']['cheap']}`, "
        f"target actor `{st_['env']['target']}`), seed {st_['seed']}. Truth: mean Y over {st_['n_truth']} games on "
        f"fixed truth seeds ({st_['n_truth_rejected']} for rejected policies). Oracle best true Y = "
        f"{o['best_y']:.2f} ({o['candidates_evaluated']} candidates, {o['episodes']:,} episodes). Common random "
        f"numbers across methods. Wall time {results['wall_seconds']:.0f} s on {st_['workers']} workers.",
        "",
        "Cells: mean [95% interval over replications]; P(within 2) uses a Wilson interval; differences are paired "
        "by replication. Generation is emulated by parametric operators, so this tests allocation, selection and "
        "validation machinery under known mechanisms, not LLM-written policies or the real game.",
        "",
        "| method | true Y of selected | regret vs oracle | P(within 2) | false-rejection rate (delta_t) | "
        "families explored | target / cheap / confirm share (%) | estimate bias | Δ true Y vs best_of_n |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m, s in summ.items():
        share = (f"{100 * s['target_share']['mean']:.0f} / {100 * s['cheap_share']['mean']:.0f} / "
                 f"{100 * s['confirm_share']['mean']:.0f}")
        lines.append(f"| {m} | {_fmt(s['true_y'])} | {_fmt(s['regret'])} | {_fmt(s['within2'], 0, True)}% | "
                     f"{_fmt(s['frr'], 0, True)}{'%' if s['frr']['n'] else ''} | {_fmt(s['families'])} | {share} | "
                     f"{_fmt(s['bias'])} ({'/'.join(s['estimate_kind'])}) | {_fmt(s.get('diff_vs_best_of_n', {}))} |")
    ablations = [m for m in summ if m != "full" and "diff_vs_full" in summ[m] and m not in NO_ELIMINATION + ("racing",)]
    if ablations:
        lines += ["", "Ablations, paired by replication (ablation minus full; negative means the component helps):", "",
                  "| ablation | what changes | Δ true Y vs full | strict false-rejection rate (delta_s) | "
                  "policies evaluated | pruning authority ever granted |", "|---|---|---|---|---|---|"]
        for m in ablations:
            s = summ[m]
            auth = "n/a" if s["authority_share"] is None else f"{100 * s['authority_share']:.0f}% of runs"
            lines.append(f"| {m} | {ABLATION_CHANGES.get(m, '')} | {_fmt(s['diff_vs_full'])} | "
                         f"{_fmt(s['frr_strict'], 0, True)}"
                         f"{'%' if s['frr_strict']['n'] else ''} | {_fmt(s['n_policies'], 0)} | {auth} |")
        if "full" in summ:
            s = summ["full"]
            auth = "n/a" if s["authority_share"] is None else f"{100 * s['authority_share']:.0f}% of runs"
            lines.append(f"| (full itself) | | 0 | {_fmt(s['frr_strict'], 0, True)}"
                         f"{'%' if s['frr_strict']['n'] else ''}"
                         f" | {_fmt(s['n_policies'], 0)} | {auth} |")
    process = [m for m in summ if summ[m]["blocks"]["n"]]
    if process:
        lines += ["", "Process diagnostics of the CareerLab variants (means over replications):", "",
                  "| variant | blocks | generation share after roots, mean / min over runs (%) | blocks without a "
                  "new candidate | blocks flagged stagnant | cheap-pruned | "
                  "proxy-pruned | audits | dormancies held back as inconclusive | specializations accepted / proposed "
                  "| runs with a confirmed claim vs incumbent (%) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for m in process:
            s = summ[m]
            rs = [r for r in results["runs"] if r["method"] == m]
            claims = np.mean([r["claims"] > 0 for r in rs])
            gmin = min((r["gen_share"] for r in rs if r["gen_share"] is not None and np.isfinite(r["gen_share"])),
                       default=float("nan"))
            stalls = f"{s['gen_stalls']['mean']:.2f}" if s.get("gen_stalls", {}).get("n") else "n/a"
            lines.append(f"| {m} | {s['blocks']['mean']:.1f} | {100 * s['gen_share']['mean']:.0f} / {100 * gmin:.0f} | "
                         f"{stalls} | "
                         f"{s['stagnation_blocks']['mean']:.1f} | {s['cheap_pruned']['mean']:.1f} | "
                         f"{s['proxy_pruned']['mean']:.1f} | {s['audits']['mean']:.1f} | {s['inconclusive']['mean']:.1f} | "
                         f"{s['specializations_accepted']['mean']:.2f} / {s['specializations']['mean']:.1f} | "
                         f"{100 * claims:.0f} |")
    ref = results.get("reference_policies") or {}
    if ref:
        lines += ["", "Reference policies (true Y): " + ", ".join(f"{k} {v:.1f}" for k, v in ref.items()) + "."]
    lines += ["", "Oracle top 5 (true Y): " + ", ".join(f"{t['true_y']:.2f}" for t in o["top"][:5]) + ".", ""]
    return "\n".join(lines)


def run_comparison(methods: Sequence[str] = METHODS, R: int = 30, budget: float = 4000.0,
                   env_config: dict[str, Any] | None = None, seed: int = 0, *, workers: int | None = None,
                   out_dir: Path | None = None, oracle: dict[str, Any] | None = None,
                   oracle_settings: OracleSettings = OracleSettings(), oracle_cache: Path | None = None,
                   n_truth: int = 2000, n_truth_rejected: int = 500,
                   search_config: SearchConfig | None = None) -> dict[str, Any]:
    """Run every method R times at equal budget and summarise against ground truth.

    Replications run in parallel (one process per replication, all methods
    inside it, so truth evaluations of shared policies are cached). The
    oracle is cached in ``oracle_cache`` (default ``out_dir/oracle.json``)
    keyed by environment and oracle settings.
    """
    t0 = time.perf_counter()
    methods = list(methods)
    unknown = set(methods) - set(METHODS)
    if unknown:
        raise ValueError(f"unknown methods {sorted(unknown)}")
    env_config = {**DEFAULT_ENV, **(env_config or {})}
    workers = workers or max(1, min(R, (os.cpu_count() or 2) - 1))
    cache = oracle_cache or (out_dir / "oracle.json" if out_dir else None)
    key = oracle_key(env_config, oracle_settings)
    ctx = get_context("spawn")
    with ctx.Pool(workers) as pool:
        if oracle is None and cache and cache.exists():
            oracle = json.loads(cache.read_text()).get(key)
        if oracle is None:
            oracle = build_oracle(env_config, oracle_settings, pool.map)
            if cache:
                cache.parent.mkdir(parents=True, exist_ok=True)
                stored = json.loads(cache.read_text()) if cache.exists() else {}
                stored[key] = oracle
                cache.write_text(json.dumps(stored, indent=1))
        tasks = [(r, methods, budget, env_config, seed, n_truth, n_truth_rejected, oracle["best_y"], search_config)
                 for r in range(R)]
        rows = [row for chunk in pool.imap_unordered(_replicate, tasks) for row in chunk]
        names = [*DESIGNED, "incumbent"]
        thetas = [*DESIGNED.values(), default_theta()]
        cfg_dict = dict(env_config.get("config") or {})
        ref = pool.map(_truth_task, [(t, env_config["target"], cfg_dict, n_truth) for t in thetas])
    rows.sort(key=lambda r: (methods.index(r["method"]), r["replication"]))
    results = {
        "settings": {"methods": methods, "R": R, "budget": budget, "env": env_config, "seed": seed,
                     "n_truth": n_truth, "n_truth_rejected": n_truth_rejected, "workers": workers,
                     "search_config": asdict(search_config or SearchConfig()), "oracle_key": key},
        "oracle": oracle,
        "reference_policies": dict(zip(names, map(float, ref))),
        "summary": aggregate(rows, methods),
        "runs": rows,
        "wall_seconds": time.perf_counter() - t0,
    }
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "results.json").write_text(json.dumps(results, indent=1, default=_json_default))
        (out_dir / "results.md").write_text(markdown(results))
    return results


def _json_default(x: Any) -> Any:
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, set):
        return sorted(x)
    raise TypeError(f"not JSON serialisable: {type(x)}")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m careerlab.search.testbed", description=__doc__.split("\n")[0])
    ap.add_argument("--R", type=int, default=30, help="replications per method")
    ap.add_argument("--budget", type=float, default=4000.0, help="cost units per search")
    ap.add_argument("--out", type=Path, required=True, help="directory for results.json / results.md")
    ap.add_argument("--methods", default=",".join(METHODS), help="comma-separated subset of " + ",".join(METHODS))
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--cheap", default=DEFAULT_ENV["cheap"], help="cheap actor model name")
    ap.add_argument("--c-target", type=float, default=DEFAULT_ENV["c_target"])
    ap.add_argument("--c-cheap", type=float, default=DEFAULT_ENV["c_cheap"])
    ap.add_argument("--pending-long", type=float, default=0.0, help="share of completed episodes returned a block late")
    ap.add_argument("--n-truth", type=int, default=2000)
    ap.add_argument("--oracle-cache", type=Path, default=None)
    args = ap.parse_args(argv)
    env_config = {**DEFAULT_ENV, "cheap": args.cheap, "c_target": args.c_target, "c_cheap": args.c_cheap,
                  "pending_long": args.pending_long}
    results = run_comparison([m.strip() for m in args.methods.split(",") if m.strip()], args.R, args.budget,
                             env_config, args.seed, workers=args.workers, out_dir=args.out,
                             oracle_cache=args.oracle_cache, n_truth=args.n_truth)
    sys.stdout.write(markdown(results) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
