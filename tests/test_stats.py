"""Checks of the pre-registered statistics on synthetic data (no game involved)."""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import stats as st

from careerlab import stats as S
from careerlab.stats import Posterior, Protocol


# --------------------------------------------------------------------------- run utility and prefix


def test_run_utility_completed_and_cap():
    assert S.run_utility(50, 48, total_tokens=48 * 500_000) == pytest.approx(0.8 * 50 + 10)
    assert S.run_utility(50, 48, total_tokens=48 * 1_750_000) == pytest.approx(40 + 5)
    assert S.run_utility(50, 48, total_tokens=48 * 4_000_000) == pytest.approx(40)
    # Early exit: even zero tokens cannot beat the 50 cap.
    assert S.run_utility(30, 20, total_tokens=0) == pytest.approx(24 + 5)
    assert S.run_utility(30, 20, total_tokens=20 * 2_000_000) == pytest.approx(24 + 4)
    # Explicit completed flag overrides the month count.
    assert S.run_utility(30, 48, total_tokens=0, completed=False) == pytest.approx(24 + 5)


def test_run_utility_missing_tokens_and_bounds():
    assert S.run_utility(60, 48) == pytest.approx(48 + 10)
    assert S.run_utility(60, 48, e_completed=70) == pytest.approx(48 + 7)
    assert S.run_utility(60, 12) == pytest.approx(48 + 5)
    assert S.run_utility(60, 0, total_tokens=1000) == pytest.approx(48)  # no survival length -> E = 0
    assert S.run_utility(100, 48, total_tokens=0) == pytest.approx(90)
    assert S.run_utility(0, 1, total_tokens=10**9) == pytest.approx(0)


def test_prefix_complete_out_of_order():
    launches = [(3, 40.0), (1, 50.0), (5, 70.0), (2, None), (4, 30.0)]
    assert S.prefix_complete(launches) == [50.0]
    launches[3] = (2, 45.0)
    assert S.prefix_complete(launches) == [50.0, 45.0, 40.0, 30.0, 70.0]
    # Censored slot resolves the prefix but brings no value; a gap stops it.
    summary = S.prefix_summary([(1, 10.0), (2, None, True), (3, 20.0), (5, 99.0)])
    assert (summary.n_c, summary.values, summary.n_censored, summary.n_held_back) == (3, [10.0, 20.0], 1, 1)
    with pytest.raises(ValueError):
        S.prefix_complete([(1, 1.0), (1, 2.0)])


# --------------------------------------------------------------------------- confidence sequence


def _bimodal(rng, n):
    first = rng.random(n) < 0.6
    return np.where(first, rng.beta(2, 18, n), rng.beta(18, 3, n))


@pytest.mark.parametrize("name", ["beta", "bimodal"])
def test_hedged_cs_time_uniform_coverage(name):
    rng = np.random.default_rng(2026 if name == "beta" else 7)
    true_mean = 2 / 7 if name == "beta" else 0.6 * 0.1 + 0.4 * 18 / 21
    covered = 0
    for _ in range(400):
        x = rng.beta(2, 5, 60) if name == "beta" else _bimodal(rng, 60)
        path = S.hedged_capital_cs_path(x, alpha=0.05)
        covered += bool(np.all((path[:, 0] <= true_mean) & (true_mean <= path[:, 1])))
    assert covered / 400 >= 0.94, covered / 400


def test_hedged_cs_width_and_nesting():
    rng = np.random.default_rng(11)
    widths = []
    for _ in range(100):
        y = 90 * rng.beta(4, 4, 30)  # mean 45, SD 15 on the 0-90 scale
        lo, hi = S.hedged_capital_cs(y, bounds=(0, 90))
        widths.append(hi - lo)
    width = float(np.mean(widths))
    print(f"hedged CS mean width at n=30, SD 15: {width:.1f} Y-points")
    # Truncation c=0.5 binds for n < ~60, so the time-uniform CS is about twice the CLT width (10.7).
    assert 15 < width < 26
    path = S.hedged_capital_cs_path(y, bounds=(0, 90))
    assert np.all(np.diff(path[:, 0]) >= -1e-12) and np.all(np.diff(path[:, 1]) <= 1e-12)
    with pytest.raises(ValueError):
        S.hedged_capital_cs([0.2, 1.5])


# --------------------------------------------------------------------------- e-process and e-BH


def test_paired_eprocess_null_and_alternative():
    rng = np.random.default_rng(3)
    null_rejections = alt_rejections = 0
    for _ in range(300):
        base = rng.normal(45, 15, 80)
        a = np.clip(base + rng.normal(0, 10, 80), 0, 90)
        b = np.clip(base + rng.normal(0, 10, 80), 0, 90)
        z, m0 = S.paired_z(a, b, delta=0.0)
        null_rejections += S.paired_eprocess(z, m0).rejected_at is not None
        z, m0 = S.paired_z(np.clip(a + 10, 0, 90), b, delta=0.0)
        alt_rejections += S.paired_eprocess(z, m0).rejected_at is not None
    assert null_rejections / 300 <= 0.06
    assert alt_rejections / 300 >= 0.8
    ep = S.paired_eprocess(z, m0)
    assert ep.e_value == pytest.approx(ep.wealth[-1]) and np.all(ep.wealth > 0)


def test_ebh_example_and_fdr():
    assert S.ebh([100, 30, 0.5, 1, 25], q=0.1) == [0, 1, 4]
    assert S.ebh([1, 2, 3], q=0.1) == []
    rng = np.random.default_rng(5)
    K, K0, mu = 20, 12, 3.0
    fdp = []
    for _ in range(3000):
        x = rng.normal(0, 1, K)
        x[K0:] += mu
        e = np.exp(mu * x - mu**2 / 2)  # likelihood-ratio e-values, E[e] = 1 under the null
        rej = S.ebh(e, q=0.10)
        fdp.append(sum(1 for i in rej if i < K0) / max(len(rej), 1))
    assert np.mean(fdp) <= 0.10


# --------------------------------------------------------------------------- partial pooling and robustness


def test_partial_pool_shrinks_towards_family_mean():
    rng = np.random.default_rng(9)
    cells = {f"p{i}": ("fam", list(rng.normal(45, 15, 12))) for i in range(5)}
    cells["small_high"] = ("fam", [80.0, 75.0])
    cells["big_high"] = ("fam", list(rng.normal(78, 15, 40)))
    cells["empty"] = ("fam", [])
    post = S.partial_pool(cells)
    mu = post["small_high"].prior_mean
    small, big = post["small_high"], post["big_high"]
    assert mu < small.mean < small.ybar
    assert (small.ybar - small.mean) / (small.ybar - mu) > (big.ybar - big.mean) / (big.ybar - mu)
    assert post["empty"].n == 0 and post["empty"].mean == pytest.approx(mu)
    assert post["empty"].var > post["p0"].var
    assert all(p.tau2 >= 9.0 for p in post.values())


def test_partial_pool_families_are_separate():
    cells = {"a1": ("A", [20.0, 22, 18, 21]), "a2": ("A", [24.0, 19, 23, 20]),
             "b1": ("B", [70.0, 68, 72, 71]), "b2": ("B", [66.0, 74, 69, 70])}
    post = S.partial_pool(cells)
    assert post["a1"].prior_mean < 30 < post["b1"].prior_mean


def test_robust_fits_flag_outlier_driven_leader():
    rng = np.random.default_rng(1)
    outlier = {"A": ("f", [50.0, 51, 49, 50, 52, 48, 90, 90]), "B": ("f", [56.0, 54, 55, 57, 53, 55, 56, 54]),
               "C": ("f", [40.0, 42, 38, 41, 39, 40, 41, 39])}
    check = S.decision_is_robust(outlier, rng=rng)
    assert check.leaders["normal"] == "A" and check.leaders["student_t"] == "B"
    assert check.status == "inconclusive" and check.leader_flip and "leader flips" in check.explanation
    clean = {"A": ("f", list(rng.normal(60, 5, 10))), "B": ("f", list(rng.normal(45, 5, 10))),
             "C": ("f", list(rng.normal(30, 5, 10)))}
    assert S.decision_is_robust(clean, rng=rng).status == "robust"


def test_robustness_flags_collapse_driven_dormancy():
    base = [-3.0, 3, -2, 2, -1, 1, 0, 0, -1, 1] * 2
    cells = {"L": ("f", [55 + d for d in base]), "M": ("f", [52 + d for d in base]), "N": ("f", [50 + d for d in base]),
             "X": ("f", [54 + d for d in base[:7]] + [0.0, 0.0, 0.0])}  # competitive except three collapses
    check = S.decision_is_robust(cells, rng=np.random.default_rng(0))
    assert check.dormant["normal"] == ["X"] and "X" not in check.dormant["student_t"]
    assert check.status == "inconclusive" and check.dormancy_flips == ["X"] and not check.leader_flip
    assert "dormancy of X flips" in check.explanation


def test_robustness_hysteresis_band():
    L = Posterior(60, 4, n=10)
    retired = Posterior(50, 4, n=10)  # P(mu >= mu_L - 4) = Phi(-6 / sqrt 8) = 0.017 -> DORMANT
    in_band = Posterior(60 - 4 - st.norm.ppf(0.9) * math.sqrt(8), 4, n=10)  # P = 0.10: neither retire nor reactivate
    keeps = Posterior(54, 4, n=10)  # P = 0.24 >= 0.2: another fit would reactivate it
    check = S.decision_is_robust({}, fits={"normal": {"L": L, "P": retired}, "student_t": {"L": L, "P": in_band}})
    assert check.status == "robust" and check.dormant == {"normal": ["P"], "student_t": []}
    assert "inside the band" in check.explanation
    check = S.decision_is_robust({}, fits={"normal": {"L": L, "P": retired}, "student_t": {"L": L, "P": keeps}})
    assert check.status == "inconclusive" and check.dormancy_flips == ["P"]
    # Leaders that no fit separates are a near-tie, not a flip.
    tie = {"normal": {"A": Posterior(60, 9, n=10), "B": Posterior(59.5, 9, n=10)},
           "student_t": {"A": Posterior(59.5, 9, n=10), "B": Posterior(60, 9, n=10)}}
    check = S.decision_is_robust({}, fits=tie)
    assert check.leaders == {"normal": "A", "student_t": "B"} and check.status == "robust" and not check.leader_flip
    tie["student_t"]["A"] = Posterior(52, 9, n=10)  # P(B > A) = 0.97 under the t fit
    check = S.decision_is_robust({}, fits=tie)
    assert check.status == "inconclusive" and check.leader_flip


def test_bayes_boot_variance_matches_normal_model():
    rng = np.random.default_rng(42)
    for n in (2, 4, 8):
        ys = list(rng.normal(45, 15, n))
        normal = S.partial_pool({"a": ("f", ys)}, tau2_floor=1e9)["a"].var
        boot = S.partial_pool_bb({"a": ("f", ys)}, tau2_floor=1e9, rng=rng, n_boot=20_000)["a"].var
        assert boot / normal == pytest.approx(1.0, rel=0.05), n


def test_robustness_rarely_inconclusive_on_clean_close_cells():
    rng = np.random.default_rng(42)
    flagged = 0
    for r in range(200):
        true = rng.normal(45, 6, 6)
        cells = {f"p{i}": ("f", list(rng.normal(true[i], 15, int(rng.integers(4, 9))))) for i in range(6)}
        fits = S.robust_fits(cells, rng=np.random.default_rng(r), n_boot=1000)
        flagged += S.decision_is_robust(cells, fits=fits).status == "inconclusive"
    print(f"inconclusive on clean normal data: {flagged / 200:.3f}")
    assert flagged / 200 <= 0.25


# --------------------------------------------------------------------------- posterior comparisons and allocation


def test_prob_better_within_best():
    a, b = Posterior(60, 9), Posterior(57, 16)
    assert S.prob_better(a, b) == pytest.approx(st.norm.cdf(3 / 5))
    assert S.prob_within(b, a, 4) == pytest.approx(st.norm.cdf(1 / 5))
    pb = S.prob_best({"a": a, "b": b})
    assert pb["a"] == pytest.approx(st.norm.cdf(3 / 5), abs=1e-4)
    pb3 = S.prob_best({"x": Posterior(0, 1), "y": Posterior(0, 1), "z": Posterior(0, 1)})
    assert all(v == pytest.approx(1 / 3, abs=1e-4) for v in pb3.values())


def test_top_two_returns_valid_arms_and_respects_cost():
    rng = np.random.default_rng(4)
    posts = {"lead": Posterior(60, 4), "close": Posterior(58, 4), "far": Posterior(30, 4)}
    picks = [S.top_two_thompson(posts, rng=rng, n_draws=1000) for _ in range(300)]
    assert set(picks) <= set(posts)
    assert picks.count("far") == 0
    probs = S.top_two_probs(posts, rng=rng)
    assert probs["lead"] + probs["close"] == pytest.approx(1.0, abs=1e-3)
    cheap = S.top_two_probs(posts, rng=rng, cost={"lead": 10.0, "close": 1.0, "far": 1.0})
    assert cheap["close"] > probs["close"]
    dominant = S.top_two_probs({"a": Posterior(90, 0.01), "b": Posterior(0, 0.01)}, rng=rng)
    assert dominant["a"] == pytest.approx(0.5) and dominant["b"] == pytest.approx(0.5)


# --------------------------------------------------------------------------- sample size, censoring, survival


def test_required_n_and_planning_sd():
    assert S.required_n(15, 5) == 82
    assert S.required_n(15, 10) == 21
    assert S.required_n(15, 10, alpha=0.05, one_sided=False) == math.ceil((1.959964 + 0.841621) ** 2 * 450 / 100)
    assert S.planning_sd(15, 10) == pytest.approx(15 * math.sqrt(10 / st.chi2.ppf(0.2, 10)))
    assert S.planning_sd(15, 10) > 15


def test_manski_bounds_and_flips():
    assert S.manski_bounds([40, 50], 2) == pytest.approx((22.5, 67.5))
    assert S.manski_bounds([], 0) == (0.0, 90.0)
    assert not S.decision_flips([60] * 10, 0, [40] * 10, 1)
    assert S.decision_flips([50] * 4, 2, [48] * 4, 0)


def test_kaplan_meier_and_rmst():
    km = S.kaplan_meier([10, 20, 48, 48], [1, 1, 0, 0])
    assert list(km.survival) == pytest.approx([0.75, 0.5])
    assert km.at(5) == 1.0 and km.at(10) == 0.75 and km.at(30) == 0.5
    assert S.rmst([10, 20, 48, 48], [1, 1, 0, 0]) == pytest.approx(31.5)
    assert S.rmst([48, 48, 48], [0, 0, 0]) == pytest.approx(48)
    assert S.rmst([5, 30], [1, 0], horizon=10) == pytest.approx(5 + 5 * 0.5)


# --------------------------------------------------------------------------- calibration and audit


def test_calibration_recovers_correlation_and_authority():
    rng = np.random.default_rng(12)
    k = 12
    true_t = rng.normal(45, 10, k)
    true_c = 5 + 0.9 * true_t + rng.normal(0, 2, k)
    cheap = {f"p{i}": list(rng.normal(true_c[i], 15, 20)) for i in range(k)}
    target = {f"p{i}": list(rng.normal(true_t[i], 15, 20)) for i in range(k)}
    cal = S.calibration(cheap, target, n_boot=2000, rng=rng)
    truth = np.corrcoef(true_c, true_t)[0, 1]
    assert cal.pearson >= cal.pearson_raw
    assert cal.pearson > 0.8 and abs(cal.pearson - truth) < 0.15
    assert cal.pearson_interval[0] < cal.pearson <= cal.pearson_interval[1] + 1e-9
    assert min(cal.reliability_cheap, cal.reliability_target) >= cal.rel_min
    assert 16 < cal.span_target < cal.span_target_raw
    assert 0 <= cal.top_k_recall <= 1 and cal.regret >= 0
    granted, reasons = S.pruning_authority(cal, audited_false_rejections=0)
    assert granted, reasons
    granted, reasons = S.pruning_authority(cal)
    assert not granted and any("no audit" in r for r in reasons)
    granted, _ = S.pruning_authority(cal, k_min=20, audited_false_rejections=0)
    assert not granted


def _noise_calibration(seed, target_sd):
    """Cheap actor without between-policy signal; target policies differ by target_sd."""
    rng = np.random.default_rng(seed)
    true_t = rng.normal(45, target_sd, 12) if target_sd else np.full(12, 45.0)
    cheap = {f"p{i}": list(rng.normal(45, 15, 5)) for i in range(12)}
    target = {f"p{i}": list(rng.normal(true_t[i], 15, 5 if not target_sd else 20)) for i in range(12)}
    return S.calibration(cheap, target, n_boot=500, rng=rng)


@pytest.mark.parametrize("target_sd", [0.0, 10.0])
def test_calibration_without_signal_grants_no_authority(target_sd):
    cals = [_noise_calibration(seed, target_sd) for seed in range(40)]
    verdicts = [S.pruning_authority(cal, audited_false_rejections=0) for cal in cals]
    assert not any(granted for granted, _ in verdicts)  # the floored correction granted ~20% on pure noise
    no_info = [(cal, reasons) for cal, (_, reasons) in zip(cals, verdicts) if cal.reliability_cheap < cal.rel_min]
    assert len(no_info) >= 36  # cheap reliability >= 0.5 by chance is rare (about 5%)
    for cal, reasons in no_info:
        assert math.isnan(cal.pearson) and math.isnan(cal.p_rho_gt_0_5) and cal.pearson_interval == (-1.0, 1.0)
        assert any(r.startswith("FAIL reliability") for r in reasons)
    if not target_sd:  # pure noise: the noise-corrected span rarely reaches 16 although the raw range usually does
        assert all(c.span_target <= c.span_target_raw for c in cals)
        assert np.mean([c.span_target >= 16 for c in cals]) <= 0.2 < np.mean([c.span_target_raw >= 16 for c in cals])


def test_audit_ipw():
    audit = S.audit_ipw([1, 0, 0, 0], [0.5, 0.5, 0.25, 0.25])
    assert audit.ipw_rate == pytest.approx(2 / 12)
    assert audit.raw_count == 1 and audit.n_audited == 4
    assert audit.cp_low == pytest.approx(st.beta.ppf(0.025, 1, 4))
    assert audit.cp_high == pytest.approx(st.beta.ppf(0.975, 2, 3))
    assert S.audit_ipw([0, 0], [1, 1]).cp_low == 0.0


# --------------------------------------------------------------------------- group sequential, Welch, submission


def test_obrien_fleming_three_looks():
    assert S.obrien_fleming_z(3, 0.05) == pytest.approx((3.471, 2.454, 2.004), abs=2e-3)


def test_welch_lower_bound_matches_scipy():
    rng = np.random.default_rng(8)
    a, b = rng.normal(55, 15, 25), rng.normal(45, 8, 12)
    expected = st.ttest_ind(a, b, equal_var=False, alternative="greater").confidence_interval(0.95).low
    assert S.welch_lower_bound(a, b, 0.05) == pytest.approx(expected)


def test_submission_ei_matches_monte_carlo():
    rng = np.random.default_rng(6)
    ei = S.submission_ei(52.0, 6.0, 55.0)
    mc = S.expected_max_mc(55.0, 52.0, 6.0, n=400_000, rng=rng) - 55.0
    assert ei == pytest.approx(mc, abs=0.03)
    assert S.submission_ei(60, 0, 55) == 5 and S.submission_ei(50, 0, 55) == 0
    assert S.expected_max_mc([40.0, 55.0], 52.0, 6.0, rng=rng) > 55.0


# --------------------------------------------------------------------------- pre-registered action rules


def test_decide_designed_cases():
    cells = {
        "L": Posterior(60, 9, n=20),
        "C": Posterior(58, 16, n=6),  # close challenger, SD(diff)=5 > delta_t/2
        "A": Posterior(30, 4, n=10),  # far below the leader
        "B": Posterior(50, 16, n=2),  # too few runs
        "D": Posterior(52, 16, n=6),  # not separable, not top-2
    }
    out = S.decide(cells)
    assert {p: d.action for p, d in out.items()} == {"L": "PROMOTE", "C": "PROMOTE", "A": "DORMANT",
                                                     "B": "REPEAT", "D": "REPEAT"}
    assert all(d.reason.startswith(d.action) for d in out.values())


@pytest.mark.parametrize("challenger, var, n, fragment", [
    (63.0, 1.0, 10, "challenger beats leader"),
    (57.0, 1.0, 10, "leader holds"),
    (59.0, 4.0, 10, "SD(mu_C - mu_L)"),
    (59.0, 30.0, 40, "n_max"),
])
def test_decide_pair_stop_rules(challenger, var, n, fragment):
    out = S.decide({"L": Posterior(60, var, n=n), "C": Posterior(challenger, var, n=n)}, leader="L")
    assert out["L"].action == "STOP" and out["C"].action == "STOP"
    assert fragment in out["C"].reason


def test_decide_respects_incumbent_and_protocol():
    cells = {"inc": Posterior(55, 4, n=8), "new": Posterior(57, 4, n=8)}
    out = S.decide(cells, leader="inc", protocol=Protocol(delta_t=2.0))
    assert out["inc"].action == "PROMOTE" and out["new"].action == "PROMOTE"
    with pytest.raises(ValueError):
        S.decide(cells, leader="missing")
