"""Pre-registered statistics for CareerLab decisions.

Every rule the planner uses to repeat, retire, promote or stop a policy lives
here so it can be audited and simulated before any real result is analysed.
Scores are on the run-utility scale ``Y`` in [0, 90] (80% live play plus 10%
token efficiency; the 10% document score is constant per version and left
out) unless a docstring says otherwise. Each function states the assumption it
relies on, and the robustness helpers report "inconclusive" instead of hiding
a decision that depends on one of them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
from scipy import stats as st
from scipy.optimize import brentq

Y_MAX = 90.0
HORIZON = 48
TOKENS_ZERO = 3_000_000.0  # tokens per month that score 0 on token efficiency
TOKENS_SPAN = 2_500_000.0  # linear span between 100 (500k) and 0 (3M)


# --------------------------------------------------------------------------- run utility


def token_efficiency(total_tokens: float, T: int, completed: bool | None = None) -> float:
    """Official token-efficiency term E in [0, 100] for one run.

    Assumes the competition rule: tokens per survived month mapped linearly
    from 500k (100) to 3M (0), capped at 50 for a run that ends before month
    48, and 0 without a survival length. ``completed`` overrides ``T >= 48``.
    """
    if T is None or T <= 0:
        return 0.0
    done = (T >= HORIZON) if completed is None else bool(completed)
    per_month = float(total_tokens) / T
    raw = min(100.0, max(0.0, 100.0 * (TOKENS_ZERO - per_month) / TOKENS_SPAN))
    return min(100.0 if done else 50.0, raw)


def run_utility(Q: float, T: int, total_tokens: float | None = None, completed: bool | None = None,
                e_completed: float = 100.0) -> float:
    """Run utility Y = 0.8 Q + 0.1 E in [0, 90].

    Without a token count (non-target development actors whose tokens say
    nothing about the target model) E is imputed: 50 for an early exit (the
    official cap) and ``e_completed`` for a completed run. That assumes the
    submitted agent stays under the 500k tokens/month line; pass a lower
    ``e_completed`` when it does not.
    """
    if T is None or T <= 0:
        e = 0.0
    elif total_tokens is None:
        done = (T >= HORIZON) if completed is None else bool(completed)
        e = float(e_completed) if done else 50.0
    else:
        e = token_efficiency(total_tokens, T, completed)
    return 0.8 * float(Q) + 0.1 * e


# --------------------------------------------------------------------------- launch-order prefix


@dataclass(frozen=True)
class Prefix:
    n_c: int  # largest k such that launches 1..k are all resolved
    values: list[float]  # values of launches 1..n_c, censored ones excluded
    n_censored: int  # resolved without a value inside the prefix (operational interruptions)
    n_held_back: int  # resolved values beyond the prefix, waiting for earlier launches


def prefix_summary(launches: Iterable[Sequence[Any]]) -> Prefix:
    """Launch-order prefix of resolved runs.

    Entries are ``(launch_index, value)`` or ``(launch_index, value, censored)``
    with 1-based indices; ``value is None`` and not censored means pending.
    Using only the complete prefix removes the bias of fast runs (often early
    eliminations) arriving first; it assumes launch order is independent of
    the outcome. A missing index counts as pending. Censored entries resolve
    their slot but contribute no value (they go to ``manski_bounds``).
    """
    slots: dict[int, tuple[Any, bool]] = {}
    for entry in launches:
        idx = int(entry[0])
        value = entry[1]
        censored = bool(entry[2]) if len(entry) > 2 else False
        if idx < 1 or idx in slots:
            raise ValueError(f"launch index {idx} is not a new positive index")
        if value is not None and isinstance(value, float) and math.isnan(value):
            value = None
        slots[idx] = (value, censored)
    n_c = 0
    while n_c + 1 in slots and (slots[n_c + 1][0] is not None or slots[n_c + 1][1]):
        n_c += 1
    inside = [slots[i] for i in range(1, n_c + 1)]
    values = [float(v) for v, c in inside if not c]
    held = sum(1 for i, (v, c) in slots.items() if i > n_c and (v is not None or c))
    return Prefix(n_c, values, sum(1 for _, c in inside if c), held)


def prefix_complete(launches: Iterable[Sequence[Any]]) -> list[float]:
    """Values with launch index <= n_c; pending runs never enter (see ``prefix_summary``)."""
    return prefix_summary(launches).values


# --------------------------------------------------------------------------- betting confidence sequence


def _plugin_moments(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Predictable mean and variance estimates (prior 1/2 and 1/4), aligned so index t-1 uses x_1..x_{t-1}."""
    t = np.arange(1, len(x) + 1)
    mu = (0.5 + np.cumsum(x)) / (t + 1)
    sig2 = (0.25 + np.cumsum((x - mu) ** 2)) / (t + 1)
    return np.concatenate([[0.5], mu[:-1]]), np.concatenate([[0.25], sig2[:-1]])


def hedged_capital_cs_path(x: Sequence[float], alpha: float = 0.05, c: float = 0.5, theta: float = 0.5,
                           grid: int = 2001, bounds: tuple[float, float] = (0.0, 1.0)) -> np.ndarray:
    """Running-intersection hedged-capital confidence sequence; row t-1 is (lo, hi) after t runs.

    Waudby-Smith & Ramdas (JRSS-B 2024), predictable plug-in lambda with
    truncation c. Assumes only that observations lie in ``bounds`` and have a
    constant conditional mean given the past (i.i.d. runs of one cell
    suffice); no normality, valid at every t simultaneously, so it can be
    checked after each run without inflating error. The hull of the grid set
    is widened by one grid step to stay conservative. NaN rows mean the set
    became empty (data incompatible with any constant mean).
    """
    lo_b, hi_b = map(float, bounds)
    x = (np.asarray(x, dtype=float) - lo_b) / (hi_b - lo_b)
    if x.size == 0:
        return np.empty((0, 2))
    if np.any(x < -1e-12) or np.any(x > 1 + 1e-12):
        raise ValueError("observations outside bounds")
    x = np.clip(x, 0.0, 1.0)
    t = np.arange(1, len(x) + 1)
    _, sig2_prev = _plugin_moments(x)
    lam = np.sqrt(2.0 * math.log(2.0 / alpha) / (sig2_prev * t * np.log1p(t)))
    m = np.linspace(0.0, 1.0, grid)
    with np.errstate(divide="ignore"):
        cap_plus = np.where(m > 0, c / m, np.inf)
        cap_minus = np.where(m < 1, c / (1.0 - m), np.inf)
    d = x[:, None] - m[None, :]
    log_kp = np.cumsum(np.log1p(np.minimum(lam[:, None], cap_plus[None, :]) * d), axis=0)
    log_km = np.cumsum(np.log1p(-np.minimum(lam[:, None], cap_minus[None, :]) * d), axis=0)
    log_k = np.maximum(math.log(theta) + log_kp, math.log(1.0 - theta) + log_km)
    inside = np.maximum.accumulate(log_k, axis=0) < math.log(1.0 / alpha)
    out = np.full((len(x), 2), np.nan)
    for i, row in enumerate(inside):
        idx = np.flatnonzero(row)
        if idx.size:
            out[i] = (m[max(idx[0] - 1, 0)], m[min(idx[-1] + 1, grid - 1)])
    return lo_b + out * (hi_b - lo_b)


def hedged_capital_cs(x: Sequence[float], alpha: float = 0.05, c: float = 0.5, theta: float = 0.5,
                      grid: int = 2001, bounds: tuple[float, float] = (0.0, 1.0)) -> tuple[float, float]:
    """(lo, hi) of the running-intersection CS after all observations (assumptions as in the path version)."""
    path = hedged_capital_cs_path(x, alpha, c, theta, grid, bounds)
    if len(path) == 0:
        return float(bounds[0]), float(bounds[1])
    return float(path[-1, 0]), float(path[-1, 1])


# --------------------------------------------------------------------------- paired e-process and e-BH


@dataclass(frozen=True)
class EProcess:
    wealth: np.ndarray  # K_t after each observation
    rejected_at: int | None  # first t (1-based) with K_t >= 1/alpha
    alpha: float
    m0: float

    @property
    def e_value(self) -> float:
        """Wealth at the last observation: an e-value when that is where sampling stopped."""
        return float(self.wealth[-1]) if len(self.wealth) else 1.0


def paired_z(y_a: Sequence[float], y_b: Sequence[float], delta: float = 0.0,
             y_range: float = Y_MAX) -> tuple[np.ndarray, float]:
    """Map paired differences to z in [0, 1] and the null boundary m0.

    H0: E[y_a - y_b] <= delta becomes E[z] <= m0. Pairs must share a block
    (same seed or same launch slot) so that the pairing removes shared noise;
    each pair is assumed independent of the others given the past.
    """
    d = np.asarray(y_a, dtype=float) - np.asarray(y_b, dtype=float)
    return (d + y_range) / (2.0 * y_range), (delta + y_range) / (2.0 * y_range)


def paired_eprocess(z: Sequence[float], m0: float, alpha: float = 0.05, c: float = 0.5) -> EProcess:
    """One-sided betting e-process for H0: E[z_t | past] <= m0, z in [0, 1].

    lambda_t is the predictable aGRAPA bet (mean gap over variance) clipped to
    [0, c/m0], so the wealth is a nonnegative supermartingale under H0 and
    Ville's inequality makes "reject when wealth >= 1/alpha" valid under
    continuous monitoring. Assumes bounded z and a mean that does not exceed
    m0 at any step under the null.
    """
    if not 0.0 < m0 < 1.0:
        raise ValueError("m0 must lie in (0, 1)")
    z = np.asarray(z, dtype=float)
    if np.any(z < -1e-12) or np.any(z > 1 + 1e-12):
        raise ValueError("z outside [0, 1]")
    mu_prev, sig2_prev = _plugin_moments(np.clip(z, 0.0, 1.0))
    gap = mu_prev - m0
    lam = np.clip(gap / (sig2_prev + gap**2), 0.0, c / m0)
    wealth = np.cumprod(1.0 + lam * (z - m0))
    hits = np.flatnonzero(wealth >= 1.0 / alpha)
    return EProcess(wealth, int(hits[0]) + 1 if hits.size else None, alpha, m0)


def ebh(e_values: Sequence[float], q: float = 0.10) -> list[int]:
    """e-BH (Wang & Ramdas 2022): indices rejected at FDR level q.

    Rejects the k* largest e-values with k* = max{k: k e_(k) / K >= 1/q}.
    Controls FDR at q K0/K under arbitrary dependence; assumes each null
    e-value has expectation at most 1.
    """
    e = np.asarray(e_values, dtype=float)
    K = len(e)
    if K == 0:
        return []
    order = np.argsort(-e, kind="stable")
    ks = np.arange(1, K + 1)
    ok = ks * e[order] / K >= 1.0 / q
    if not ok.any():
        return []
    return sorted(int(i) for i in order[: int(ks[ok].max())])


# --------------------------------------------------------------------------- partial pooling


@dataclass(frozen=True)
class Posterior:
    """Normal posterior for one policy's mean utility."""

    mean: float
    var: float
    n: int = 0
    family: str = ""
    ybar: float | None = None  # unpooled cell estimate
    prior_mean: float | None = None  # family mean the cell shrinks towards
    tau2: float | None = None  # between-policy variance in the family

    @property
    def sd(self) -> float:
        """Posterior standard deviation."""
        return math.sqrt(max(self.var, 0.0))


def _pooled_within_var(groups: Iterable[np.ndarray]) -> float | None:
    """Pooled within-cell variance, None without replicated cells."""
    groups = [g for g in groups if len(g) >= 2]
    df = sum(len(g) - 1 for g in groups)
    if df == 0:
        return None
    return float(sum(((g - g.mean()) ** 2).sum() for g in groups) / df)


def _dl(theta: np.ndarray, v: np.ndarray, floor: float) -> tuple[float, float, float]:
    """DerSimonian-Laird tau^2 (floored), random-effects mean and its variance."""
    k = len(theta)
    tau2 = floor
    if k >= 2:
        w = 1.0 / v
        tw = float((w * theta).sum() / w.sum())
        q = float((w * (theta - tw) ** 2).sum())
        denom = float(w.sum() - (w**2).sum() / w.sum())
        if denom > 0:
            tau2 = max(floor, (q - (k - 1)) / denom)
    W = 1.0 / (v + tau2)
    return float((W * theta).sum() / W.sum()), float(1.0 / W.sum()), float(tau2)


def _pool_estimates(est: Mapping[str, tuple[str, float, float, int]], empty: Mapping[str, str],
                    floor: float) -> dict[str, Posterior]:
    """Normal-normal shrinkage of cell estimates (family, theta, v, n) within each family.

    The posterior variance adds the uncertainty of the estimated family mean
    (Morris correction) so a cell is not overconfident when its family is
    small. Families without data borrow the all-cells fit.
    """
    out: dict[str, Posterior] = {}
    keys = list(est)
    if keys:
        g_mu, g_var, g_tau2 = _dl(np.array([est[p][1] for p in keys]), np.array([est[p][2] for p in keys]), floor)
    else:
        g_mu, g_var, g_tau2 = Y_MAX / 2, (Y_MAX / 4) ** 2, max(floor, (Y_MAX / 4) ** 2)
    hyper: dict[str, tuple[float, float, float]] = {}
    for fam in sorted({f for f, *_ in est.values()}):
        members = [p for p in keys if est[p][0] == fam]
        hyper[fam] = _dl(np.array([est[p][1] for p in members]), np.array([est[p][2] for p in members]), floor)
        mu, var_mu, tau2 = hyper[fam]
        for p in members:
            _, theta, v, n = est[p]
            b = v / (v + tau2)
            out[p] = Posterior(b * mu + (1 - b) * theta, (1 - b) * v + b * b * var_mu, n, fam, theta, mu, tau2)
    for p, fam in empty.items():
        mu, var_mu, tau2 = hyper.get(fam, (g_mu, g_var, g_tau2))
        out[p] = Posterior(mu, tau2 + var_mu, 0, fam, None, mu, tau2)
    return out


def _split_cells(cells: Mapping[str, tuple[str, Sequence[float]]]) -> tuple[dict[str, tuple[str, np.ndarray]], dict[str, str]]:
    """Cells with runs (as arrays) and empty cells (family only); empty cells get the family prior."""
    data = {p: (fam, np.asarray(ys, dtype=float)) for p, (fam, ys) in cells.items()}
    return {p: d for p, d in data.items() if len(d[1])}, {p: d[0] for p, d in data.items() if not len(d[1])}


def _family_scale(data: Mapping[str, tuple[str, np.ndarray]], fam: str, fallback: float) -> float:
    """Within-cell variance pooled over one family, assuming the family shares it; fallback without replication."""
    pooled = _pooled_within_var(ys for f, ys in data.values() if f == fam)
    return fallback if pooled is None else pooled


def partial_pool(cells: Mapping[str, tuple[str, Sequence[float]]], tau2_floor: float = 9.0,
                 sigma_default: float = 15.0, var_floor: float = 1.0) -> dict[str, Posterior]:
    """Normal-normal partial pooling of policy means within families.

    Assumes runs are i.i.d. normal within a cell with a variance shared by the
    family (pooled because cells of 4-10 runs give unstable variances), and
    policy means normal around a family mean with DerSimonian-Laird tau^2,
    floored at 9 (tau >= 3 Y-points) so a family never claims its members are
    identical. Without replicated cells the variance falls back to the global
    pool and then to ``sigma_default``^2.
    """
    data, empty = _split_cells(cells)
    global_var = _pooled_within_var(ys for _, ys in data.values())
    fallback = sigma_default**2 if global_var is None else global_var
    est = {}
    for p, (fam, ys) in data.items():
        s2 = max(var_floor, _family_scale(data, fam, fallback))
        est[p] = (fam, float(ys.mean()), s2 / len(ys), len(ys))
    return _pool_estimates(est, empty, tau2_floor)


def _t_em(groups: Sequence[np.ndarray], nu: float, iters: int = 200) -> tuple[np.ndarray, float | None]:
    """EM for per-cell locations with a shared Student-t scale (df-corrected), None scale without replication."""
    theta = np.array([float(np.median(g)) for g in groups])
    N, k = sum(len(g) for g in groups), len(groups)
    if N - k <= 0:
        return theta, None
    sigma2 = max(1e-6, float(sum(((g - th) ** 2).sum() for g, th in zip(groups, theta)) / (N - k)))
    for _ in range(iters):
        ws = [(nu + 1) / (nu + (g - th) ** 2 / sigma2) for g, th in zip(groups, theta)]
        new_theta = np.array([float((w * g).sum() / w.sum()) for w, g in zip(ws, groups)])
        new_sigma2 = max(1e-6, float(sum((w * (g - th) ** 2).sum() for w, g, th in zip(ws, groups, new_theta)) / (N - k)))
        done = np.allclose(new_theta, theta, atol=1e-9) and abs(new_sigma2 - sigma2) < 1e-9
        theta, sigma2 = new_theta, new_sigma2
        if done:
            break
    return theta, sigma2


def partial_pool_t(cells: Mapping[str, tuple[str, Sequence[float]]], nu: float = 4.0, tau2_floor: float = 9.0,
                   sigma_default: float = 15.0, var_floor: float = 1.0) -> dict[str, Posterior]:
    """Robustness refit with Student-t (nu=4) run noise instead of normal.

    Assumes heavy-tailed runs (rare windfalls or collapses) around each cell
    location with a family-shared scale; locations come from EM and their
    variance from the t Fisher information sigma^2 (nu+3)/((nu+1) n). Pooling
    across policies stays normal-normal.
    """
    data, empty = _split_cells(cells)
    all_theta, all_s2 = _t_em([ys for _, ys in data.values()], nu)
    default_scale = sigma_default**2 * (nu - 2) / nu  # t scale whose variance is sigma_default^2
    fallback = default_scale if all_s2 is None else all_s2
    est = {}
    for fam in sorted({f for f, _ in data.values()}):
        members = [p for p in data if data[p][0] == fam]
        theta, s2 = _t_em([data[p][1] for p in members], nu)
        s2 = max(var_floor * (nu - 2) / nu, fallback if s2 is None else s2)
        for p, th in zip(members, theta):
            n = len(data[p][1])
            est[p] = (fam, float(th), s2 * (nu + 3) / ((nu + 1) * n), n)
    return _pool_estimates(est, empty, tau2_floor)


def partial_pool_bb(cells: Mapping[str, tuple[str, Sequence[float]]], rng: np.random.Generator | None = None,
                    n_boot: int = 4000, tau2_floor: float = 9.0, sigma_default: float = 15.0,
                    var_floor: float = 1.0) -> dict[str, Posterior]:
    """Robustness refit with Bayesian-bootstrap cell means.

    Drops the shared-variance and normal-noise assumptions inside each cell:
    mean and variance of the cell mean come from Dirichlet(1) reweighting of
    its own runs. The Dirichlet variance is the plug-in s^2 (n-1)/(n(n+1)),
    only 60% of s^2/n at n=4, so it is rescaled by (n+1)/(n-1). Otherwise the
    refit is overconfident on small cells and retires them even under normal
    noise. Cells with fewer than two runs keep the normal-model variance,
    since one run carries no spread information.
    """
    rng = rng or np.random.default_rng(0)
    data, empty = _split_cells(cells)
    global_var = _pooled_within_var(ys for _, ys in data.values())
    fallback = sigma_default**2 if global_var is None else global_var
    est = {}
    for p, (fam, ys) in data.items():
        n = len(ys)
        if n >= 2:
            draws = rng.dirichlet(np.ones(n), size=n_boot) @ ys
            est[p] = (fam, float(draws.mean()), max(var_floor / n, float(draws.var(ddof=1)) * (n + 1) / (n - 1)), n)
        else:
            est[p] = (fam, float(ys.mean()), max(var_floor, _family_scale(data, fam, fallback)) / len(ys), len(ys))
    return _pool_estimates(est, empty, tau2_floor)


def robust_fits(cells: Mapping[str, tuple[str, Sequence[float]]], rng: np.random.Generator | None = None,
                nu: float = 4.0, n_boot: int = 4000) -> dict[str, dict[str, Posterior]]:
    """The main fit and the two pre-registered robustness refits, by name."""
    return {"normal": partial_pool(cells), "student_t": partial_pool_t(cells, nu=nu),
            "bayes_boot": partial_pool_bb(cells, rng=rng, n_boot=n_boot)}


# --------------------------------------------------------------------------- posterior comparisons


def prob_better(post_a: Posterior, post_b: Posterior) -> float:
    """P(mu_a > mu_b), treating the two normal posteriors as independent.

    Pooling makes them positively correlated through the family mean, so for
    two members of one family this slightly understates the separation.
    """
    sd = math.sqrt(post_a.var + post_b.var)
    if sd == 0:
        return float(post_a.mean > post_b.mean)
    return float(st.norm.cdf((post_a.mean - post_b.mean) / sd))


def prob_within(post_p: Posterior, post_leader: Posterior, delta: float) -> float:
    """P(mu_p >= mu_leader - delta) under independent normal posteriors."""
    sd = math.sqrt(post_p.var + post_leader.var)
    gap = post_p.mean - post_leader.mean + delta
    if sd == 0:
        return float(gap >= 0)
    return float(st.norm.cdf(gap / sd))


def prob_best(posteriors: Mapping[str, Posterior]) -> dict[str, float]:
    """P(each policy has the highest mean) under independent normal posteriors.

    Deterministic quadrature of pdf_i * prod_j cdf_j on a grid dense around
    every posterior, so tiny and wide posteriors are both resolved. Points
    below max_j(m_j - 8 s_j) are dropped: no policy can be best there.
    """
    keys = list(posteriors)
    if len(keys) <= 1:
        return {k: 1.0 for k in keys}
    m = np.array([posteriors[k].mean for k in keys], dtype=float)
    s = np.sqrt(np.maximum([posteriors[k].var for k in keys], 1e-12))
    lower = float((m - 8 * s).max())
    grid = np.unique(np.concatenate([mi + si * np.linspace(-8, 8, 321) for mi, si in zip(m, s)] + [[lower]]))
    grid = grid[grid >= lower]
    zz = (grid[None, :] - m[:, None]) / s[:, None]
    log_cdf = st.norm.logcdf(zz)
    integrand = st.norm.pdf(zz) / s[:, None] * np.exp(log_cdf.sum(axis=0)[None, :] - log_cdf)
    p = np.clip(np.trapezoid(integrand, grid, axis=1), 0.0, None)
    p = p / p.sum()
    return {k: float(v) for k, v in zip(keys, p)}


def top_two_probs(posteriors: Mapping[str, Posterior], beta: float = 0.5, rng: np.random.Generator | None = None,
                  cost: Mapping[str, float] | None = None, n_draws: int = 4000) -> dict[str, float]:
    """Top-two Thompson allocation probabilities, optionally divided by expected cost.

    Monte Carlo version of Russo's rule: the leader of one posterior draw with
    probability beta, otherwise the leader of a redraw conditioned to differ.
    Dividing by cost (then renormalising) spends budget where information is
    cheap; it assumes cost is known up to a constant and independent of the
    outcome.
    """
    rng = rng or np.random.default_rng()
    keys = list(posteriors)
    if len(keys) == 1:
        return {keys[0]: 1.0}
    m = np.array([posteriors[k].mean for k in keys])
    s = np.sqrt(np.maximum([posteriors[k].var for k in keys], 0.0))
    draws = m[None, :] + s[None, :] * rng.standard_normal((n_draws, len(keys)))
    best = draws.argmax(axis=1)
    counts = np.bincount(best, minlength=len(keys)).astype(float)
    pi = counts / n_draws
    alloc = beta * pi
    for i in np.flatnonzero(pi):
        if counts[i] < n_draws:
            challenger = counts / (n_draws - counts[i])
            challenger[i] = 0.0
        else:  # no draw ever beats i: use the per-draw runner-up instead
            masked = draws.copy()
            masked[:, i] = -np.inf
            challenger = np.bincount(masked.argmax(axis=1), minlength=len(keys)) / n_draws
        alloc += (1 - beta) * pi[i] * challenger
    if cost is not None:
        alloc = alloc / np.array([max(float(cost[k]), 1e-12) for k in keys])
    alloc = alloc / alloc.sum()
    return {k: float(v) for k, v in zip(keys, alloc)}


def top_two_thompson(posteriors: Mapping[str, Posterior], beta: float = 0.5, rng: np.random.Generator | None = None,
                     cost: Mapping[str, float] | None = None, n_draws: int = 4000) -> str:
    """Policy to sample next under (cost-weighted) top-two Thompson sampling (see ``top_two_probs``)."""
    rng = rng or np.random.default_rng()
    probs = top_two_probs(posteriors, beta, rng, cost, n_draws)
    keys = list(probs)
    return keys[int(rng.choice(len(keys), p=np.array([probs[k] for k in keys])))]


# --------------------------------------------------------------------------- sample size


def planning_sd(s: float, nu: int, q: float = 0.20) -> float:
    """Upper (1-q) confidence bound for sigma from a pilot SD s with nu df.

    Assumes normal runs so (nu s^2 / sigma^2) ~ chi2(nu); planning with it
    protects power against an optimistic pilot.
    """
    return float(s * math.sqrt(nu / st.chi2.ppf(q, nu)))


def required_n(sigma: float, delta: float, alpha: float = 0.10, power: float = 0.8, one_sided: bool = True) -> int:
    """Runs per arm for a two-sample z-test to detect a mean difference delta.

    n = (z_{1-a} + z_{power})^2 2 sigma^2 / delta^2, with a -> a/2 when
    two-sided. Assumes equal variances, equal allocation and approximate
    normality of the means.
    """
    za = st.norm.ppf(1 - (alpha if one_sided else alpha / 2))
    zb = st.norm.ppf(power)
    return int(math.ceil((za + zb) ** 2 * 2 * sigma**2 / delta**2 - 1e-9))


# --------------------------------------------------------------------------- censoring and survival


def manski_bounds(observed: Sequence[float], n_censored: int, lo: float = 0.0, hi: float = Y_MAX) -> tuple[float, float]:
    """Worst/best-case bounds on the mean when censored runs could score anything in [lo, hi].

    No assumption about why runs were censored (operational interruptions):
    the bounds hold whatever the missingness mechanism.
    """
    obs = np.asarray(observed, dtype=float)
    n = len(obs) + n_censored
    if n == 0:
        return float(lo), float(hi)
    total = float(obs.sum())
    return (total + n_censored * lo) / n, (total + n_censored * hi) / n


def decision_flips(observed_a: Sequence[float], n_censored_a: int, observed_b: Sequence[float], n_censored_b: int,
                   delta: float = 0.0, lo: float = 0.0, hi: float = Y_MAX) -> bool:
    """True when "mean_a - mean_b > delta" holds under one extreme imputation of censored runs but not the other.

    If it flips, censoring alone could change the decision, so it must wait
    for resolution or reruns rather than drop the interrupted runs.
    """
    a_lo, a_hi = manski_bounds(observed_a, n_censored_a, lo, hi)
    b_lo, b_hi = manski_bounds(observed_b, n_censored_b, lo, hi)
    return (a_lo - b_hi > delta) != (a_hi - b_lo > delta)


@dataclass(frozen=True)
class KaplanMeier:
    times: np.ndarray  # distinct event times
    survival: np.ndarray  # S(t) just after each event time
    at_risk: np.ndarray
    events: np.ndarray

    def at(self, t: float) -> float:
        """Right-continuous survival at time t."""
        idx = np.searchsorted(self.times, t, side="right")
        return 1.0 if idx == 0 else float(self.survival[idx - 1])


def kaplan_meier(times: Sequence[float], events: Sequence[int]) -> KaplanMeier:
    """Kaplan-Meier estimate of survival months (event 1 = eliminated, 0 = censored).

    Assumes censoring (completion at 48, interruptions) independent of the
    hazard; censored runs at an event time count as still at risk.
    """
    t = np.asarray(times, dtype=float)
    e = np.asarray(events, dtype=int)
    uniq = np.unique(t[e == 1])
    at_risk = np.array([(t >= u).sum() for u in uniq])
    d = np.array([((t == u) & (e == 1)).sum() for u in uniq])
    surv = np.cumprod(1.0 - d / at_risk) if len(uniq) else np.array([])
    return KaplanMeier(uniq, surv, at_risk, d)


def rmst(times: Sequence[float], events: Sequence[int], horizon: float = HORIZON) -> float:
    """Restricted mean survival time up to ``horizon`` (area under the KM curve).

    Uses the same independent-censoring assumption as ``kaplan_meier``; a
    curve that never drops gives ``horizon``.
    """
    km = kaplan_meier(times, events)
    area, prev, s = 0.0, 0.0, 1.0
    for tj, sj in zip(km.times, km.survival):
        if tj >= horizon:
            break
        area += s * (tj - prev)
        prev, s = float(tj), float(sj)
    return area + s * (horizon - prev)


# --------------------------------------------------------------------------- cheap-to-target calibration


@dataclass
class Calibration:
    policies: list[str]
    cheap_means: dict[str, float]
    target_means: dict[str, float]
    pearson_raw: float
    spearman_raw: float
    pearson: float  # disattenuated; NaN when a reliability is below rel_min (no information)
    spearman: float  # disattenuated (approximate: Pearson reliabilities applied to ranks); NaN as above
    pearson_interval: tuple[float, float]  # Bayesian bootstrap (draw reliabilities floored at rel_min); (-1, 1) without information
    spearman_interval: tuple[float, float]
    p_rho_gt_0_5: float  # posterior P(disattenuated Pearson > 0.5) from the same draws; NaN without information
    reliability_cheap: float  # 1 - noise / variance of the means, clipped to [0, 1]
    reliability_target: float
    top_k_recall: float
    regret: float  # mu_t(best by target) - mu_t(best by cheap) >= 0
    span_target: float  # range of noise-corrected (empirical-Bayes) target means
    k_top: int
    rel_min: float = 0.5
    informative_share: float = 1.0  # share of bootstrap draws with both reliabilities >= rel_min
    span_target_raw: float = float("nan")  # range of the observed target means, inflated by noise
    draws: dict[str, np.ndarray] = field(default_factory=dict, repr=False)


def _means_errors(data: Mapping[str, Sequence[float]], policies: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    """Policy means and their sampling variances s^2/n (pooled s^2 for single-run policies, assuming i.i.d. runs)."""
    groups = [np.asarray(data[p], dtype=float) for p in policies]
    pooled = _pooled_within_var(groups)
    if pooled is None:
        raise ValueError("calibration needs at least one policy with two or more runs on each side")
    means = np.array([g.mean() for g in groups])
    errs = np.array([(g.var(ddof=1) if len(g) >= 2 else pooled) / len(g) for g in groups])
    return means, errs


def _weighted_reliability(G: np.ndarray, x: np.ndarray, e: np.ndarray) -> np.ndarray:
    """Reliability 1 - noise / variance of the means per weight row (unclipped, can be negative)."""
    mx = G @ x
    vx = (G * (x[None, :] - mx[:, None]) ** 2).sum(1)
    unbias = 1.0 - (G**2).sum(1)  # reliability-weights correction, equals (k-1)/k for uniform weights
    with np.errstate(divide="ignore", invalid="ignore"):
        return 1.0 - (G @ e) / (vx / unbias)


def _weighted_corr(G: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Weighted Pearson correlation per weight row."""
    dx, dy = x[None, :] - (G @ x)[:, None], y[None, :] - (G @ y)[:, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        return (G * dx * dy).sum(1) / np.sqrt((G * dx * dx).sum(1) * (G * dy * dy).sum(1))


def _disattenuate(r: np.ndarray, rel_x: np.ndarray, rel_y: np.ndarray, rel_min: float) -> np.ndarray:
    """r / sqrt(rel_x rel_y) clipped to [-1, 1], each reliability floored at rel_min.

    The floor bounds the amplification at 1/rel_min. Below it the correction
    is under-applied, which pulls the value towards the raw correlation, the
    conservative direction for a "rho > 0.5" claim. An unbounded correction
    would turn noise into a perfect correlation whenever the means barely
    differ.
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.clip(r / np.sqrt(np.maximum(rel_x, rel_min) * np.maximum(rel_y, rel_min)), -1.0, 1.0)


def _interval(draws: np.ndarray, tail: float) -> tuple[float, float]:
    """Equal-tailed quantile interval of bootstrap draws."""
    return float(np.nanquantile(draws, tail)), float(np.nanquantile(draws, 1 - tail))


def calibration(cheap: Mapping[str, Sequence[float]], target: Mapping[str, Sequence[float]], k_top: int = 2,
                n_boot: int = 2000, rng: np.random.Generator | None = None, level: float = 0.95,
                rel_min: float = 0.5) -> Calibration:
    """How well cheap-actor policy means predict target-actor policy means.

    Correlations are corrected for attenuation by within-policy noise
    (Spearman 1904): reliability = 1 - mean(s^2/n) / var(means). Intervals
    and P(rho > 0.5) come from a Bayesian bootstrap over policies (Dirichlet
    weights), which assumes the calibrated policies are exchangeable draws
    from the population that pruning will act on. Rank correction is
    approximate. When either side's reliability is below ``rel_min`` the
    policy means are mostly noise and the correlation is not identified: the
    corrected estimates and P(rho > 0.5) are NaN, the intervals are (-1, 1),
    and ``pruning_authority`` refuses. Inside the bootstrap the draw
    reliabilities are floored at ``rel_min``, which bounds the correction.
    The target span is the range of empirical-Bayes means, shrunk towards
    their average by the moment estimate of between-policy variance, so
    noise alone gives a span near 0 instead of the range of noisy means.
    """
    rng = rng or np.random.default_rng(0)
    policies = sorted(p for p in cheap if p in target and len(cheap[p]) and len(target[p]))
    k = len(policies)
    if k < 3:
        raise ValueError("calibration needs at least three policies with data on both sides")
    xc, ec = _means_errors(cheap, policies)
    xt, et = _means_errors(target, policies)
    rc, rt = st.rankdata(xc), st.rankdata(xt)
    uniform = np.full((1, k), 1.0 / k)
    rel_c, rel_t = float(_weighted_reliability(uniform, xc, ec)[0]), float(_weighted_reliability(uniform, xt, et)[0])
    p_raw, s_raw = float(_weighted_corr(uniform, xc, xt)[0]), float(_weighted_corr(uniform, rc, rt)[0])
    informative = rel_c >= rel_min and rel_t >= rel_min
    p_dis, s_dis = (float(np.clip(r / math.sqrt(rel_c * rel_t), -1.0, 1.0)) if informative else float("nan")
                    for r in (p_raw, s_raw))
    G = rng.dirichlet(np.ones(k), size=n_boot)
    rc_d, rt_d = _weighted_reliability(G, xc, ec), _weighted_reliability(G, xt, et)
    p_draws = _disattenuate(_weighted_corr(G, xc, xt), rc_d, rt_d, rel_min)
    s_draws = _disattenuate(_weighted_corr(G, rc, rt), rc_d, rt_d, rel_min)
    tau2_t = max(0.0, float(xt.var(ddof=1) - et.mean()))  # moment estimate of between-policy target variance
    shrunk_t = xt.mean() + tau2_t / (tau2_t + et) * (xt - xt.mean()) if tau2_t > 0 else np.full(k, xt.mean())
    tail = (1 - level) / 2
    k_top = min(k_top, k)
    top_c = set(np.array(policies)[np.argsort(-xc, kind="stable")[:k_top]])
    top_t = set(np.array(policies)[np.argsort(-xt, kind="stable")[:k_top]])
    return Calibration(
        policies=policies,
        cheap_means=dict(zip(policies, map(float, xc))),
        target_means=dict(zip(policies, map(float, xt))),
        pearson_raw=p_raw, spearman_raw=s_raw, pearson=p_dis, spearman=s_dis,
        pearson_interval=_interval(p_draws, tail) if informative else (-1.0, 1.0),
        spearman_interval=_interval(s_draws, tail) if informative else (-1.0, 1.0),
        p_rho_gt_0_5=float(np.mean(p_draws > 0.5)) if informative else float("nan"),
        reliability_cheap=float(np.clip(rel_c, 0.0, 1.0)), reliability_target=float(np.clip(rel_t, 0.0, 1.0)),
        top_k_recall=len(top_c & top_t) / k_top,
        regret=float(xt.max() - xt[int(np.argmax(xc))]),
        span_target=float(shrunk_t.max() - shrunk_t.min()),
        k_top=k_top,
        rel_min=float(rel_min),
        informative_share=float(np.mean((rc_d >= rel_min) & (rt_d >= rel_min))),
        span_target_raw=float(xt.max() - xt.min()),
        draws={"pearson": p_draws, "spearman": s_draws},
    )


def pruning_authority(cal: Calibration, *, k_min: int = 8, span_min: float = 16.0, p_rho_gt_0_5_min: float = 0.8,
                      audited_false_rejections: int | None = None, max_false_rejections: int = 0) -> tuple[bool, list[str]]:
    """Whether cheap-actor results may retire policies without target-actor runs.

    Granted only when all of these hold. Enough policies were calibrated
    (k_min). Both sides' policy means are reliable (>= ``cal.rel_min``),
    because without between-policy signal the correlation carries no
    information. The noise-corrected target means span a useful range
    (span_min = 20 Q-points ~ 16 Y-points; a narrow range makes any
    correlation uninformative). P(rho > 0.5) is high. An audit has run and
    found no more than ``max_false_rejections``; no audit (None) means no
    authority.
    """
    rel_ok = cal.reliability_cheap >= cal.rel_min and cal.reliability_target >= cal.rel_min
    checks = [
        (len(cal.policies) >= k_min, f"k={len(cal.policies)} calibrated policies (need >= {k_min})"),
        (rel_ok, f"reliability cheap {cal.reliability_cheap:.2f} / target {cal.reliability_target:.2f} "
                 f"(need >= {cal.rel_min:g} each)"),
        (cal.span_target >= span_min, f"noise-corrected target span {cal.span_target:.1f} Y-points "
                                      f"(need >= {span_min:g}; raw {cal.span_target_raw:.1f})"),
        (cal.p_rho_gt_0_5 >= p_rho_gt_0_5_min,  # NaN (no information) fails
         f"P(rho > 0.5) = {cal.p_rho_gt_0_5:.3f} (need >= {p_rho_gt_0_5_min:g}; "
         f"{cal.informative_share:.0%} of draws reliable)" if rel_ok
         else f"P(rho > 0.5) undefined: no between-policy signal (need >= {p_rho_gt_0_5_min:g})"),
        (audited_false_rejections is not None and audited_false_rejections <= max_false_rejections,
         "no audit of pruned policies yet" if audited_false_rejections is None
         else f"{audited_false_rejections} audited false rejections (allowed {max_false_rejections})"),
    ]
    return all(ok for ok, _ in checks), [("PASS " if ok else "FAIL ") + why for ok, why in checks]


@dataclass(frozen=True)
class Audit:
    ipw_rate: float  # estimated false-rejection rate among all pruned policies
    raw_count: int
    n_audited: int
    cp_low: float  # Clopper-Pearson bounds on the raw audited proportion
    cp_high: float


def audit_ipw(flags: Sequence[int], inclusion_probs: Sequence[float], population: int | None = None,
              alpha: float = 0.05) -> Audit:
    """Inverse-probability-weighted false-rejection rate from a random audit of pruned policies.

    Assumes each pruned policy was audited independently with the known
    positive probability given; Horvitz-Thompson with ``population``,
    otherwise the Hajek ratio. Clopper-Pearson bounds use the raw
    (unweighted) audited count, which is exact but ignores the weights.
    """
    f = np.asarray(flags, dtype=float)
    pi = np.asarray(inclusion_probs, dtype=float)
    if len(f) != len(pi) or np.any(pi <= 0) or np.any(pi > 1):
        raise ValueError("need one inclusion probability in (0, 1] per audited policy")
    n, k = len(f), int(f.sum())
    if n == 0:
        return Audit(float("nan"), 0, 0, 0.0, 1.0)
    rate = float((f / pi).sum() / (population if population else (1.0 / pi).sum()))
    cp_low = 0.0 if k == 0 else float(st.beta.ppf(alpha / 2, k, n - k + 1))
    cp_high = 1.0 if k == n else float(st.beta.ppf(1 - alpha / 2, k + 1, n - k))
    return Audit(rate, k, n, cp_low, cp_high)


# --------------------------------------------------------------------------- group-sequential and Welch


def _upper_crossing(C: float, K: int, h: float = 0.01) -> float:
    """P(B(k/K) >= C for some k) for standard Brownian motion, by recursive grid integration."""
    sd = math.sqrt(1.0 / K)
    s = np.linspace(-10.0, C, int(round((C + 10.0) / h)) + 1)
    w = np.full(len(s), s[1] - s[0])
    w[[0, -1]] /= 2
    f = st.norm.pdf(s, scale=sd)
    cross = float(st.norm.sf(C, scale=sd))
    kernel = st.norm.pdf((s[:, None] - s[None, :]) / sd) / sd
    for _ in range(2, K + 1):
        cross += float((w * f * st.norm.sf((C - s) / sd)).sum())
        f = kernel @ (w * f)
    return cross


def obrien_fleming_z(n_looks: int = 3, alpha: float = 0.05) -> tuple[float, ...]:
    """Classical O'Brien-Fleming z boundaries for equally spaced looks.

    ``alpha`` is two-sided; the boundary is computed for the upper one-sided
    crossing at alpha/2 (0.025 by default), which gives 3.471, 2.454, 2.004
    for three looks (Jennison & Turnbull, table 2.3). Assumes the z statistic
    at look k has independent normal increments (B-value boundary constant C,
    z_k = C sqrt(K/k)).
    """
    C = brentq(lambda c: _upper_crossing(c, n_looks) - alpha / 2, 1.0, 6.0, xtol=1e-7)
    return tuple(float(C * math.sqrt(n_looks / k)) for k in range(1, n_looks + 1))


def welch_lower_bound(a: Sequence[float], b: Sequence[float], alpha: float = 0.05) -> float:
    """One-sided (1-alpha) lower confidence bound for mean(a) - mean(b), Welch-Satterthwaite df.

    Assumes independent samples with approximately normal means; unequal
    variances are allowed. Needs at least two runs per arm.
    """
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = math.sqrt(va + vb)
    if se == 0:
        return float(a.mean() - b.mean())
    df = (va + vb) ** 2 / (va**2 / (len(a) - 1) + vb**2 / (len(b) - 1))
    return float(a.mean() - b.mean() - st.t.ppf(1 - alpha, df) * se)


# --------------------------------------------------------------------------- submission value


def submission_ei(m: float, s: float, a_star: float) -> float:
    """Expected gain of the best score from submitting a version with score ~ N(m, s^2) over a_star.

    Stage 1 keeps a team's highest version score, so a submission only adds
    E[max(X, a*)] - a*. Assumes a normal predictive distribution for the
    version score (mean of three runs).
    """
    if s <= 0:
        return max(m - a_star, 0.0)
    z = (m - a_star) / s
    return float((m - a_star) * st.norm.cdf(z) + s * st.norm.pdf(z))


def expected_max_mc(prev: float | Sequence[float], mean: float, sd: float, n: int = 100_000,
                    rng: np.random.Generator | None = None) -> float:
    """Monte Carlo E[max(best previous score, X)], X ~ N(mean, sd^2); prev may be a list of known scores."""
    rng = rng or np.random.default_rng()
    best = float(np.max(prev)) if np.ndim(prev) else float(prev)
    return float(np.maximum(best, rng.normal(mean, sd, n)).mean())


# --------------------------------------------------------------------------- pre-registered action rules


@dataclass(frozen=True)
class Protocol:
    """Pre-registered thresholds (Y-points unless stated)."""

    delta_s: float = 4.0  # dormancy margin: retire when surely more than this below the leader
    delta_t: float = 8.0  # practically relevant difference; pair stops when SD(diff) <= delta_t / 2
    n0: int = 4  # minimum runs before a cell can be retired, promoted or stopped
    n_max_screen: int = 40  # runs per cell after which a screening comparison stops
    p_dormant: float = 0.05
    p_promote: float = 0.20
    p_stop: float = 0.95
    p_reactivate: float = 0.20  # a dormant cell comes back at P(mu >= mu_L - delta_s) >= this (prereg v1)


@dataclass(frozen=True)
class ActionDecision:
    policy: str
    action: str  # REPEAT | DORMANT | PROMOTE | STOP
    reason: str


def decide(cell_stats: Mapping[str, Posterior], leader: str | None = None,
           protocol: Protocol = Protocol()) -> dict[str, ActionDecision]:
    """Apply the pre-registered action rules to every cell; each decision carries its explanation.

    Order of precedence per cell:
      1. REPEAT while n < n0;
      2. DORMANT if n >= n0 and P(mu_p >= mu_L - delta_s) < p_dormant;
      3. STOP for the leader and its challenger (best other non-dormant cell)
         when P(mu_C > mu_L) >= p_stop or <= 1 - p_stop, SD(mu_C - mu_L) <=
         delta_t / 2, or both reached n_max_screen;
      4. PROMOTE if among the top two non-dormant posterior means with
         P(best) >= p_promote;
      5. STOP when the cell reached n_max_screen, otherwise REPEAT.
    Assumes normal, independent posteriors (e.g. from ``partial_pool``);
    ``leader`` defaults to the highest posterior mean.
    """
    if not cell_stats:
        return {}
    pr = protocol
    keys = list(cell_stats)
    leader = leader if leader is not None else max(keys, key=lambda k: cell_stats[k].mean)
    if leader not in cell_stats:
        raise ValueError(f"leader {leader!r} has no cell statistics")
    L = cell_stats[leader]
    p_best = prob_best(cell_stats)
    out: dict[str, ActionDecision] = {}
    for p in keys:
        post = cell_stats[p]
        if p == leader or post.n < pr.n0:
            continue
        pw = prob_within(post, L, pr.delta_s)
        if pw < pr.p_dormant:
            out[p] = ActionDecision(p, "DORMANT", f"DORMANT: n={post.n} >= n0={pr.n0} and P(mu >= mu_L - {pr.delta_s:g}) = "
                                    f"{pw:.3f} < {pr.p_dormant:g} (mean {post.mean:.1f} vs leader {leader} {L.mean:.1f})")
    ranked = sorted((p for p in keys if p not in out), key=lambda k: cell_stats[k].mean, reverse=True)
    top2 = ranked[:2]
    challenger = next((p for p in ranked if p != leader and cell_stats[p].n >= pr.n0), None)
    stop_reason = None
    if challenger is not None and L.n >= pr.n0:
        C = cell_stats[challenger]
        pcl, sd = prob_better(C, L), math.sqrt(C.var + L.var)
        pair = f"pair {challenger} vs leader {leader}"
        if pcl >= pr.p_stop:
            stop_reason = f"STOP: {pair}: P(mu_C > mu_L) = {pcl:.3f} >= {pr.p_stop:g}, challenger beats leader"
        elif pcl <= 1 - pr.p_stop + 1e-12:
            stop_reason = f"STOP: {pair}: P(mu_C > mu_L) = {pcl:.3f} <= {1 - pr.p_stop:.2f}, leader holds"
        elif sd <= pr.delta_t / 2:
            stop_reason = (f"STOP: {pair}: SD(mu_C - mu_L) = {sd:.2f} <= delta_t/2 = {pr.delta_t / 2:g}, difference "
                           f"{C.mean - L.mean:+.1f} known to within the relevant margin (P(C > L) = {pcl:.3f})")
        elif min(C.n, L.n) >= pr.n_max_screen:
            stop_reason = f"STOP: {pair}: both cells reached n_max={pr.n_max_screen} unresolved (P(C > L) = {pcl:.3f})"
    for p in keys:
        if p in out:
            continue
        post = cell_stats[p]
        if post.n < pr.n0:
            out[p] = ActionDecision(p, "REPEAT", f"REPEAT: n={post.n} < n0={pr.n0}")
        elif stop_reason and p in (leader, challenger):
            out[p] = ActionDecision(p, "STOP", stop_reason)
        elif p in top2 and p_best[p] >= pr.p_promote:
            out[p] = ActionDecision(p, "PROMOTE", f"PROMOTE: top-2 posterior mean {post.mean:.1f} with "
                                    f"P(best) = {p_best[p]:.3f} >= {pr.p_promote:g}")
        elif post.n >= pr.n_max_screen:
            out[p] = ActionDecision(p, "STOP", f"STOP: n={post.n} reached n_max={pr.n_max_screen} without promotion "
                                    f"(P(best) = {p_best[p]:.3f})")
        else:
            pw = 1.0 if p == leader else prob_within(post, L, pr.delta_s)
            out[p] = ActionDecision(p, "REPEAT", f"REPEAT: not separable yet (P(best) = {p_best[p]:.3f}, "
                                    f"P(mu >= mu_L - {pr.delta_s:g}) = {pw:.3f}, n={post.n})")
    return {p: out[p] for p in keys}


@dataclass(frozen=True)
class Robustness:
    status: str  # robust | inconclusive
    leaders: dict[str, str]  # argmax posterior mean per fit
    dormant: dict[str, list[str]]  # DORMANT cells per fit, from decide()
    explanation: str
    leader_flip: bool = False  # leaders differ and some fit separates its leader from another's
    dormancy_flips: list[str] = field(default_factory=list)  # retired by one fit, reactivated by another


def decision_is_robust(cells: Mapping[str, tuple[str, Sequence[float]]], protocol: Protocol = Protocol(),
                       leader: str | None = None, rng: np.random.Generator | None = None,
                       fits: Mapping[str, Mapping[str, Posterior]] | None = None) -> Robustness:
    """Flag 'inconclusive' when the leader or a dormancy decision flips between the normal, Student-t and Bayesian-bootstrap fits.

    A decision that depends on the noise model is not acted on: the cells get
    more runs instead. A flip has to cross the protocol's hysteresis band,
    because posteriors that differ by a hair always straddle some threshold
    and would make nearly every screening state inconclusive:

    - dormancy: one fit retires the cell (P(mu >= mu_L - delta_s) <
      p_dormant) while another would reactivate it (P >= p_reactivate);
    - leader: the fits name different leaders and one fit gives the other
      fit's leader P(beats its own leader) < p_reactivate. Near-ties that no
      fit separates leave both cells in play anyway, so they are reported but
      not flagged.

    Assumes all fits cover the same cells. Dormancy is anchored on each
    fit's own leader, or on ``leader`` (an incumbent) when given; the
    leaders compared are always each fit's highest posterior mean.
    """
    pr = protocol
    fits = fits if fits is not None else robust_fits(cells, rng=rng)
    leaders = {name: max(post, key=lambda k: post[k].mean) for name, post in fits.items()}
    dormant = {name: sorted(p for p, d in decide(post, leader, pr).items() if d.action == "DORMANT")
               for name, post in fits.items()}

    def within(name: str, p: str) -> float:
        post = fits[name]
        anchor = leader if leader is not None else leaders[name]
        return 1.0 if p == anchor else prob_within(post[p], post[anchor], pr.delta_s)

    problems, notes, flips = [], [], []
    for p in sorted({p for d in dormant.values() for p in d}):
        keep = {name: within(name, p) for name in fits if p not in dormant[name]}
        kept = {name: pw for name, pw in keep.items() if pw >= pr.p_reactivate}
        retire = ", ".join(f"{name} {within(name, p):.3f}" for name in fits if p in dormant[name])
        if kept:
            flips.append(p)
            problems.append(f"dormancy of {p} flips: P(mu >= mu_L - {pr.delta_s:g}) is {retire} (< {pr.p_dormant:g}) but "
                            + ", ".join(f"{name} {pw:.3f}" for name, pw in kept.items()) + f" (>= {pr.p_reactivate:g})")
        elif keep:
            notes.append(f"{p} dormant only in some fits, others inside the band ("
                         + ", ".join(f"{name} {pw:.3f}" for name, pw in keep.items()) + ")")
    leader_flip = False
    if len(set(leaders.values())) > 1:
        sep = {(f, other): prob_better(fits[f][leaders[f]], fits[f][other])
               for f in fits for other in dict.fromkeys(leaders.values()) if other != leaders[f]}
        detail = ", ".join(f"{k}={v}" for k, v in leaders.items()) + "; " + ", ".join(
            f"{f}: P({leaders[f]} > {other}) = {pv:.3f}" for (f, other), pv in sep.items())
        leader_flip = any(pv > 1 - pr.p_reactivate for pv in sep.values())
        (problems if leader_flip else notes).append(
            ("leader flips: " if leader_flip else "leader near-tie, not separated by any fit: ") + detail)
    if problems:
        return Robustness("inconclusive", leaders, dormant, "inconclusive: " + " | ".join(problems + notes),
                          leader_flip, flips)
    if notes:
        return Robustness("robust", leaders, dormant, "robust: fits differ only inside the hysteresis band: "
                          + " | ".join(notes), leader_flip, flips)
    return Robustness("robust", leaders, dormant,
                      f"robust: leader {next(iter(leaders.values()))} and dormant set {next(iter(dormant.values()))} "
                      f"agree across {', '.join(fits)}", leader_flip, flips)


# --------------------------------------------------------------------------- budget planner (playbook P34)


def budget_planner(sigma: float, tau: float, budget: int, ks: Sequence[int] = (2, 3, 4, 5, 6, 8),
                   delta: float = 4.0, n_min: int = 4, selection_share: float = 0.55, reps: int = 20000,
                   rng: np.random.Generator | None = None) -> list[dict[str, float]]:
    """How many candidate families a target budget can race.

    Assumes normal true means across families (SD ``tau``), normal episode noise
    (SD ``sigma``), equal allocation of the selection share of ``budget`` and
    choice by the sample mean. Returns, per K, the expected regret of the chosen
    family, the expected true mean of the chosen family relative to the family
    distribution (the quantity that trades breadth against precision) and the
    probability that it is within ``delta`` of the best raced family. K is
    infeasible when K * n_min episodes exceed the selection share (prereg
    dormancy minimum). Rerun with measured sigma and tau after the target pilot.
    """
    rng = rng or np.random.default_rng(0)
    out = []
    for k in ks:
        n = int(selection_share * budget // k)
        feasible = n >= n_min
        mu = rng.normal(0.0, tau, size=(reps, k))
        est = mu + rng.normal(0.0, sigma / math.sqrt(max(n, 1)), size=(reps, k))
        pick = mu[np.arange(reps), est.argmax(axis=1)]
        regret = mu.max(axis=1) - pick
        out.append({"K": k, "episodes_each": n, "feasible": feasible, "expected_regret": float(regret.mean()),
                    "expected_chosen_mean": float(pick.mean()),
                    "p_within_delta": float((regret <= delta).mean())})
    return out
