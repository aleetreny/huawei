"""Policy search: archive, operators, environment, every method and ablation, and the testbed driver."""

from __future__ import annotations

import json
import math
import random
from dataclasses import replace

import numpy as np
import pytest

from careerlab.search import archive as A
from careerlab.search import methods as M
from careerlab.search import operators as O
from careerlab.search import testbed as T
from careerlab.synthetic.game import DEFAULT_CONFIG, fast_episode
from careerlab.synthetic.policy import DESIGNED, default_theta, normalize, random_theta

SMALL_ORACLE = T.OracleSettings(per_family=6, n_screen=10, top=6, n_mid=20, generations=1, children=6, n_child=10,
                                elites=3, final=3, n_final=100)


def _node(theta: dict, family: str = "state", node_id: str = "n0000") -> A.Node:
    t = normalize(theta)
    return A.Node(node_id, t, A.theta_hash(t), family)


# ---------------------------------------------------------------------------
# environment
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("actor", ["target", "cheap_biased", "cheap_capability"])
def test_play_matches_fast_episode_and_counts_behaviour(actor):
    for name in ("state_switch", "overcommit", "steady_networker"):
        for seed in (0, 1, 2):
            o = T.play(DESIGNED[name], actor, seed)
            f = fast_episode(DESIGNED[name], actor, seed)
            assert (o.Q, o.T, o.completed, o.failure) == (f.Q, f.T, f.completed, f.failure_reason)
            assert o.Y == pytest.approx(f.Y)
            assert list(o.monthly) == [row["q"] for row in f.monthly]
            assert o.decisions == f.steps - f.rejected and o.promotions == len(f.promotions)
            assert 0 <= o.invest_early <= o.invest <= o.energy
            deliver = [row["month"] for row in f.monthly if row["mode"] == "deliver"]
            if o.switch_month is not None and deliver:
                assert o.switch_month <= deliver[0]


def test_truncated_config_is_the_prefix_of_a_full_game():
    cfg12 = replace(DEFAULT_CONFIG, months=12)
    for seed in range(4):
        full = T.play(DESIGNED["early_invest"], "target", seed)
        short = T.play(DESIGNED["early_invest"], "target", seed, cfg12)
        if full.T >= 12:
            assert short.Q == pytest.approx(full.monthly[11], abs=0.01) and short.completed
        else:
            assert (short.T, short.failure) == (full.T, full.failure)


def test_env_common_random_numbers_and_costs():
    th = DESIGNED["state_switch"]
    a, b = T.SynthEnv(replication=3), T.SynthEnv(replication=3)
    ea, eb = a.episodes(th, "target", 3), b.episodes(th, "target", 3)
    assert [o.Y for o in ea] == [o.Y for o in eb] and [o.launch for o in ea] == [1, 2, 3]
    assert [o.seed for o in a.episodes(th, "target", 2, start=2)] == [o.seed for o in ea[1:]]
    other = T.SynthEnv(replication=4).episodes(th, "target", 3)
    assert [o.seed for o in other] != [o.seed for o in ea]
    assert {o.seed for o in a.episodes(th, "cheap", 3)}.isdisjoint(o.seed for o in ea)
    assert {o.seed for o in a.episodes(DESIGNED["calendar8"], "target", 3)}.isdisjoint(o.seed for o in ea)
    assert a.cost("target") == 10 and a.cost("cheap") == 1 and a.cost("target", 12) == pytest.approx(2.5)
    assert all(o.T <= 12 and o.horizon == 12 for o in a.episodes(th, "target", 3, horizon=12))
    late = T.SynthEnv(pending_long=1.0).episodes(th, "target", 6, block=2)
    assert all(o.resolved_block == (3 if o.completed else 2) for o in late)


# ---------------------------------------------------------------------------
# archive
# ---------------------------------------------------------------------------

def test_archive_duplicates_status_lineage_and_prefix():
    arc = A.PolicyArchive()
    a, new_a = arc.add(DESIGNED["state_switch"], "state", hypothesis="root")
    b, new_b = arc.add(DESIGNED["calendar8"], "calendar")
    dup, new_dup = arc.add(dict(DESIGNED["state_switch"]), "state", operator="refine")
    assert new_a and new_b and not new_dup and dup is a and arc.duplicates == 1 and len(arc) == 2
    child, _ = arc.add(random_theta(random.Random(1), "random"), "state", parents=(a.id, b.id), operator="recombine")
    grand, _ = arc.add(random_theta(random.Random(2), "random"), "state", parents=(child.id,), operator="refine")
    assert arc.lineage(grand.id) == [child.id, a.id, b.id] and arc.children(a.id) == [child.id]
    assert arc.family_children("state") == 2
    bad, ok = arc.add({"not_a_parameter": 1}, "random")
    assert not ok and bad.status == "retired"
    with pytest.raises(ValueError):
        arc.set_status(bad.id, "active", "retirement is final")
    arc.set_status(b.id, "dormant", "DORMANT: test", "audit")
    assert (b.dormancy_reason, b.review_trigger) == ("DORMANT: test", "audit")
    arc.set_status(b.id, "active", "reactivated")
    assert b.dormancy_reason is None and b.review_trigger is None
    # prefix-complete: launch 2 is pending at block 0, so launches 2 and 3 are excluded
    for launch, resolved, y in ((1, 0, 10.0), (2, 1, 20.0), (3, 0, 30.0)):
        arc.record(a.id, "target", A.Outcome(Y=y, Q=y, T=48, completed=True, failure=None, seed=launch,
                                             launch=launch, resolved_block=resolved))
    arc.record(a.id, "target", A.Outcome(Y=99, Q=99, T=12, completed=True, failure=None, seed=9, horizon=12,
                                         launch=1), partial=True)
    assert a.ys("target", at_block=0) == [10.0] and a.ys("target", at_block=1) == [10.0, 20.0, 30.0]
    assert arc.cells("target", at_block=0) == {a.id: ("state", [10.0])} and a.ys() == [10.0, 20.0, 30.0]
    assert arc.summary()[0]["n_partial"] == 1


def test_descriptors_summarise_outcomes():
    env = T.SynthEnv()
    outs = env.episodes(DESIGNED["overcommit"], "target", 30)
    d = A.descriptors(outs)
    assert d["n"] == 30 and 0 <= d["completion"] <= 1 and 0 < d["rmst"] <= 48
    assert abs(sum(d["failures"].values()) - (1 - d["completion"])) < 1e-9
    assert 0 <= d["recovery_share"] <= 1 and 0 <= d["invest_early_share"] <= 1 and d["switch_share"] > 0
    assert set(d["km"]) == {12, 24, 36} and A.descriptors([]) == {"n": 0}


# ---------------------------------------------------------------------------
# operators
# ---------------------------------------------------------------------------

def test_refine_targets_the_dominant_failure():
    rng = random.Random(0)
    parent = _node({**DESIGNED["overcommit"], "health_floor": 2})
    p = O.refine(parent, {"n": 20, "failures": {"health_depleted": 0.5, "skill_gap": 0.1}}, rng)
    assert p.operator == "refine" and p.parents == (parent.id,) and "health_depleted" in p.hypothesis
    assert p.theta["health_floor"] > 2 and p.theta["overtime_rule"] == "if_healthy"
    p = O.refine(parent, {"n": 20, "failures": {"risk_incident": 0.4}}, rng)
    assert p.theta["risk_reaction"] in ("defuse", "lay_low") and p.theta["risk_warnings"] == 1
    p = O.refine(_node(DESIGNED["state_switch"]), {"n": 20, "failures": {}, "mean_level": 5.0}, rng)
    assert p.theta != DESIGNED["state_switch"]  # fine-tuning still changes something


def test_specialize_uses_observable_triggers_unless_calendar_is_tested():
    rng = random.Random(3)
    base = _node(DESIGNED["no_invest"], "grinder")
    for _ in range(30):
        p = O.specialize(base, rng)
        assert p.theta["switch_rule"] in ("state", "feedback") and p.meta["specialization"]
        assert not p.meta["diagnostic"] and p.theta["invest_build"] >= 0.7
    cal = O.specialize(base, rng, calendar=True)
    assert cal.theta["switch_rule"] == "calendar" and cal.meta["diagnostic"]
    already = _node(DESIGNED["state_switch"])
    assert all(O.specialize(already, rng).theta["switch_rule"] != "calendar" for _ in range(20))


def test_recombine_wild_new_family_and_shared_stream():
    rng = random.Random(5)
    a, b = _node(DESIGNED["state_switch"], node_id="n0001"), _node(DESIGNED["steady_networker"], node_id="n0002")
    p = O.recombine(a, b, rng)
    assert p.parents == ("n0001", "n0002") and p.meta["from_a"] and p.meta["from_b"]
    for k, v in p.theta.items():
        assert v in (a.theta[k], b.theta[k])
    w = O.wild(a, rng)
    assert sum(w.theta[k] != a.theta[k] for k in a.theta) >= 3 and "learning goal" in w.hypothesis
    s1, s2 = O.CandidateStream(7), O.CandidateStream(7)
    assert [s1.draw("state") for _ in range(3)] == [s2.draw("state") for _ in range(3)]
    assert s1.draw("builder") == s2.draw("builder") != O.CandidateStream(8).draw("builder")
    nf = O.new_family(rng, families=("cautious",))
    assert nf.family == "cautious" and nf.operator == "new_family" and not nf.parents


# ---------------------------------------------------------------------------
# methods
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def runs() -> dict[str, M.SearchResult]:
    return {m: M.run_search(m, T.SynthEnv(replication=1), 1600, np.random.default_rng([0, 1])) for m in M.METHODS}


def test_every_method_respects_the_budget_and_selects_an_evaluated_policy(runs):
    for m, res in runs.items():
        assert res.spent <= res.budget + 1e-9 and res.spent >= 0.9 * res.budget, m
        sel = res.archive[res.selected]
        assert sel.n("target") >= 4 and res.history and math.isfinite(res.estimate), m
        assert res.selected_theta == sel.theta and res.families_explored >= 1
        json.dumps(res.to_dict(with_archive=True), default=str)


def test_baselines_report_in_sample_and_full_reports_fresh_confirmation(runs):
    for m in ("best_of_n", "refine_leader", "racing"):
        assert runs[m].estimate_kind == "in_sample" and runs[m].cost_by_actor.keys() == {"target"}
    best = runs["best_of_n"]
    assert len({n.n() for n in best.archive.nodes.values()}) == 1 and not best.rejected
    for m in M.FULL_VARIANTS:
        res = runs[m]
        assert res.estimate_kind == "fresh" and res.confirmation["n_per_arm"] >= 2, m
        assert res.cost_by_purpose["confirm"] >= 0.14 * res.budget
        kinds = [h["kind"] for h in res.history]
        assert kinds.index("freeze") < kinds.index("confirm")
        assert all(res.archive[f].status == "frozen" for f in res.finalists)
        for node in res.archive.nodes.values():  # confirmation episodes never reach selection data
            assert len(node.meta.get("confirmation", [])) in (0, res.confirmation["n_per_arm"])


def test_dormancy_uses_complete_target_episodes_only(runs):
    for m in M.FULL_VARIANTS:
        for node in runs[m].archive.nodes.values():
            reason = node.dormancy_reason or ""
            if node.status == "dormant" and reason.startswith("DORMANT"):
                assert node.n("target") >= 4 and all(o.horizon == 48 for o in node.outcomes["target"]), m


def test_ablation_switches_change_what_they_should(runs):
    assert runs["target_only"].cost_by_actor.get("cheap", 0) == 0
    assert runs["partial_screening"].cost_by_purpose.get("proxy", 0) > 0
    assert runs["partial_screening"].cost_by_actor.get("cheap", 0) == 0
    assert runs["partial_screening"].extra["proxy_pruned"] > 0
    assert not {"audit", "reopen"} & {h["kind"] for h in runs["no_reopen"].history}
    assert runs["no_specialization"].extra["specializations"] == 0
    assert all(h.get("operator") != "specialize" for h in runs["no_specialization"].history)
    assert runs["no_calibration"].extra["authority"] and runs["no_calibration"].cost_by_purpose.get("calibration", 0) == 0
    assert runs["full"].cost_by_purpose.get("root_calibration", 0) > 0
    for m in M.FULL_VARIANTS:  # prereg: at least 20% of slots for new candidates
        assert runs[m].extra["generation_share"] >= 0.2, m
        assert runs[m].extra["generation_empty_blocks"] == 0, m
    for m, switches in M.FULL_VARIANTS.items():  # each ablation changes only its own switches
        cfg, full = M.method_config(m), M.method_config("full")
        assert {k for k in cfg.__dataclass_fields__ if getattr(cfg, k) != getattr(full, k)} == set(switches), m


def _roots(res: M.SearchResult) -> list[A.Node]:
    return [n for n in res.archive.nodes.values() if n.created_block == 0 and n.operator == "new_family"]


def test_no_diversity_narrows_only_the_root(runs):
    full, nodiv = runs["full"], runs["no_diversity"]
    assert full.extra["root_families"] == list(O.ALL_FAMILIES)
    (fam,) = nodiv.extra["root_families"]
    assert len(_roots(nodiv)) == len(_roots(full)) == 2 * len(O.ALL_FAMILIES)  # same root budget
    assert {n.family for n in _roots(nodiv)} == {fam} and {n.family for n in _roots(full)} == set(O.ALL_FAMILIES)


@pytest.mark.parametrize("method,replication,budget,cheap", [
    ("no_diversity", 0, 8000, "cheap_biased"),  # stalled in 12 of 31 blocks when the ablation also narrowed generation
    ("full", 25, 4000, "cheap_capability"),  # reopen episodes used to eat the generation quota (share 0.186)
])
def test_generation_never_stalls_and_keeps_its_prereg_share(method, replication, budget, cheap):
    env = T.SynthEnv.from_config({**T.DEFAULT_ENV, "cheap": cheap}, replication=replication, seed=0)
    res = M.run_search(method, env, budget, np.random.default_rng([0, replication]))
    assert res.extra["generation_share"] >= 0.25 and res.extra["generation_empty_blocks"] == 0
    generated = {h["block"] for h in res.history if h["kind"] == "generate"}
    assert set(range(1, res.extra["blocks"])) <= generated  # every block but the last, which may lack room
    late_new = [h for h in res.history if h.get("operator") == "new_family" and h["block"] > 0]
    assert late_new and res.families_explored == len(O.ALL_FAMILIES)  # new_family still widens beyond the root


def test_progressive_widening_bounds_children_per_family(runs):
    for m in M.FULL_VARIANTS:
        arc = runs[m].archive
        for fam in arc.families(evaluated_only=False):
            assert arc.family_children(fam) <= math.ceil((1 + arc.family_episodes(fam)) ** 0.5) + 1, (m, fam)


def test_confirmation_never_changes_the_selection():
    class Poisoned(T.SynthEnv):
        def episodes(self, theta, role, n, start=1, horizon=None, stream="dev", block=0):
            outs = super().episodes(theta, role, n, start, horizon, stream, block)
            if stream == "confirm":
                for o in outs:
                    o.Y = 0.0
            return outs

    a = M.run_search("target_only", T.SynthEnv(replication=2), 1200, np.random.default_rng(5))
    b = M.run_search("target_only", Poisoned(replication=2), 1200, np.random.default_rng(5))
    assert a.selected_theta == b.selected_theta and b.estimate == 0.0 < a.estimate


def test_prefix_complete_inclusion_waits_for_late_results():
    env = T.SynthEnv(replication=0, pending_long=1.0)
    res = M.run_search("target_only", env, 1000, np.random.default_rng(1))
    some = next(n for n in res.archive.nodes.values()
                if any(o.resolved_block > o.block for o in n.outcomes["target"]))
    first = min((o for o in some.outcomes["target"] if o.resolved_block > o.block), key=lambda o: o.launch)
    # at its own block boundary the late game and every later launch are excluded; one block later they count
    assert len(some.ys("target", at_block=first.block)) <= first.launch - 1
    assert len(some.ys("target", at_block=first.block + 1)) >= first.launch


def test_racing_confidence_sequence_rule_and_unknown_method():
    cfg = M.SearchConfig(race_rule="cs")
    res = M.run_search("racing", T.SynthEnv(), 1200, np.random.default_rng(0), cfg)
    assert res.spent <= 1200 and res.estimate_kind == "in_sample"
    with pytest.raises(ValueError):
        M.run_search("nope", T.SynthEnv(), 100, np.random.default_rng(0))
    assert M.method_config("no_reopen").reopen is False and M.method_config("full").reopen is True


def test_methods_are_deterministic_given_rng_and_env():
    a = M.run_search("full", T.SynthEnv(replication=4), 900, np.random.default_rng([0, 4]))
    b = M.run_search("full", T.SynthEnv(replication=4), 900, np.random.default_rng([0, 4]))
    assert a.selected_theta == b.selected_theta and a.estimate == b.estimate and a.history == b.history


# ---------------------------------------------------------------------------
# testbed driver
# ---------------------------------------------------------------------------

def test_oracle_and_metrics():
    oracle = T.build_oracle({}, SMALL_ORACLE)
    assert oracle["best_y"] == max(t["true_y"] for t in oracle["top"]) and len(oracle["top"]) == 3
    res = M.run_search("full", T.SynthEnv(replication=0), 900, np.random.default_rng(0))
    row = T.run_metrics(res, T.SynthEnv(), oracle["best_y"], n_truth=100, n_truth_rejected=50)
    assert row["regret"] == pytest.approx(oracle["best_y"] - row["true_y"])
    assert row["bias"] == pytest.approx(res.estimate - row["true_y"])
    assert 0 <= row["frr"] <= 1 and row["frr_strict"] <= row["frr"]
    assert row["target_share"] + row["cheap_share"] == pytest.approx(1.0)
    best = M.run_search("best_of_n", T.SynthEnv(), 400, np.random.default_rng(0))
    assert math.isnan(T.run_metrics(best, T.SynthEnv(), 60.0, 100, 50)["frr"])


def test_run_comparison_writes_json_and_markdown(tmp_path):
    out = T.run_comparison(["best_of_n", "full", "target_only"], R=2, budget=700, seed=3, workers=2, out_dir=tmp_path,
                           oracle_settings=SMALL_ORACLE, n_truth=100, n_truth_rejected=50)
    data = json.loads((tmp_path / "results.json").read_text())
    md = (tmp_path / "results.md").read_text()
    assert len(data["runs"]) == 6 and set(data["summary"]) == {"best_of_n", "full", "target_only"}
    assert "diff_vs_best_of_n" in data["summary"]["full"] and "| full |" in md and "Ablations" in md
    assert (tmp_path / "oracle.json").exists()
    again = T.run_comparison(["best_of_n"], R=1, budget=300, seed=3, workers=1, out_dir=tmp_path,
                             oracle_settings=SMALL_ORACLE, n_truth=50, n_truth_rejected=50)
    assert again["oracle"] == out["oracle"]  # cached


def test_cli_entry_point(tmp_path):
    key = T.oracle_key(T.DEFAULT_ENV, T.OracleSettings())
    fake = {"best_y": 60.0, "best_theta": default_theta(), "best_hash": "x", "top": [{"true_y": 60.0}],
            "settings": {}, "candidates_evaluated": 1, "episodes": 1, "procedure": "test stub"}
    cache = tmp_path / "oracle.json"
    cache.write_text(json.dumps({key: fake}))
    assert T.main(["--R", "1", "--budget", "300", "--out", str(tmp_path), "--methods", "best_of_n",
                   "--workers", "1", "--n-truth", "50", "--oracle-cache", str(cache)]) == 0
    assert json.loads((tmp_path / "results.json").read_text())["settings"]["R"] == 1
