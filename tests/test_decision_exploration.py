"""Adversarial checks for temporal leakage, grouped validation and reserved data."""

import gzip
import json
from pathlib import Path

import numpy as np
import pytest

from careerlab.decision_models import grouped_folds, nested_predictions, ridge_fit, ridge_predict
from careerlab.decision_research import build_episode, extract_streams
from scripts.decision_research_audit import sha256
from scripts.explore_decisions import cycle_lineage, run


def call(name, key, **args):
    return {"message": {"content": [{"type": "tool_use", "name": "mcp__game__" + name, "id": key, "input": {"session_id": "s", **args}}]}}


def reply(key, value):
    return {"message": {"content": [{"type": "tool_result", "tool_use_id": key, "content": json.dumps(value)}]}}


def observation(month=1, level="L1", output=0):
    return {"current_state": {"session_id": "s", "time": {"current_month": month},
                              "status": {"level": level, "health": 5, "dignity": 5, "network": 1, "output": output},
                              "simulation_flags": {"alive": True}},
            "current_event": {"title": "Quarterly main action"},
            "choices": [{"choice": 1, "action": "Apply for a key project", "energy_cost": 0}]}


def transcript(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def test_observation_is_not_reused_after_an_action(tmp_path):
    path = transcript(tmp_path / "stream-0.jsonl", [call("observe", "o"), reply("o", observation()),
                       call("take_action", "a", choice=1), reply("a", {"success": True}),
                       call("take_action", "b", choice=1), reply("b", {"success": True})])
    actions, _, diagnostics = extract_streams([path])
    assert actions[0]["aligned"] is True
    assert actions[1]["aligned"] is False
    assert actions[1]["pre"] is None
    assert diagnostics["unaligned_action_calls"] == 1


def test_delayed_observation_cannot_become_fresh_after_intervening_action(tmp_path):
    path = transcript(tmp_path / "stream-0.jsonl", [call("observe", "early"), call("take_action", "a", choice=1),
                       reply("a", {"success": True}), reply("early", observation()), call("take_action", "b", choice=1), reply("b", {"success": True})])
    actions, _, diagnostics = extract_streams([path])
    assert not any(a["aligned"] for a in actions)
    assert diagnostics["stale_observation_result"] == 1


def test_session_mismatch_prevents_alignment(tmp_path):
    path = transcript(tmp_path / "stream-0.jsonl", [call("observe", "o"), reply("o", observation()),
                       call("take_action", "a", choice=1, session_id="wrong"), reply("a", {"success": True})])
    actions, _, diagnostics = extract_streams([path])
    assert actions[0]["pre"] is None
    assert diagnostics["session_mismatch"] == 1


def test_continuation_can_match_an_outstanding_call(tmp_path):
    one = transcript(tmp_path / "stream-0.jsonl", [call("observe", "o")])
    two = transcript(tmp_path / "stream-1.jsonl", [reply("o", observation()), call("take_action", "a", choice=1), reply("a", {"success": True})])
    actions, _, diagnostics = extract_streams([one, two])
    assert actions[0]["aligned"]
    assert diagnostics["unanswered_calls"] == 0


def test_landmark_has_no_future_behaviour_and_later_missing_states_do_not_select_it(tmp_path):
    rows = [call("observe", "o1"), reply("o1", observation()), call("take_action", "a1", choice=1), reply("a1", {"success": True}),
            call("observe", "o6"), reply("o6", observation(6, "L2", 4)), call("take_action", "a6", choice=1), reply("a6", {"success": True}),
            call("take_action", "unobserved", choice=1), reply("unobserved", {"success": True})]
    a, o, d = extract_streams([transcript(tmp_path / "stream-0.jsonl", rows)])
    e = {"job_id": "job", "actor_id": "actor", "env_id": "env", "policy_id": "policy", "purpose": "screen", "outcome": "completed", "completed": True, "score": 60, "survival_months": 48, "steps": 3}
    result = build_episode(e, {"name": "policy", "family": "f"}, a, o, d, [6])
    assert result["landmarks"]["6"]["prior_main_actions"] == 1
    assert result["landmarks"]["6"]["behaviour_prefix_complete"] is True
    assert result["quality_for_prediction"] is True
    assert result["whole_game_behaviour_complete"] is False


def test_rejected_action_does_not_enter_behaviour_counts(tmp_path):
    rows = [call("observe", "o1"), reply("o1", observation()), call("take_action", "a1", choice=1), reply("a1", {"success": False}),
            call("observe", "o6"), reply("o6", observation(6)), call("take_action", "a6", choice=1), reply("a6", {"success": True})]
    a, o, d = extract_streams([transcript(tmp_path / "stream-0.jsonl", rows)])
    e = {"job_id": "j", "actor_id": "a", "env_id": "e", "policy_id": "p", "purpose": "screen", "outcome": "completed", "completed": 1, "score": 60, "survival_months": 48, "steps": 2}
    result = build_episode(e, {"name": "p", "family": "f"}, a, o, d, [6])
    assert result["landmarks"]["6"]["prior_main_actions"] == 0
    assert result["landmarks"]["6"]["growth_share"] is None


def test_groups_never_overlap_between_train_and_test():
    groups = np.repeat(np.arange(9), [1, 2, 4, 2, 3, 1, 2, 5, 1])
    seen = []
    for train, test in grouped_folds(groups, 5, 26):
        assert set(groups[train]).isdisjoint(groups[test])
        seen.extend(test)
    assert sorted(seen) == list(range(len(groups)))


def test_preprocessing_uses_only_training_rows():
    fit = ridge_fit([[1, np.nan], [3, 8]], [10, 20], 1)
    assert fit["median"].tolist() == [2, 8]
    original = fit["mean"].copy()
    assert np.isfinite(ridge_predict(fit, [[1e9, np.nan]])).all()
    assert np.array_equal(fit["mean"], original)


def test_held_out_outcomes_cannot_influence_their_own_prediction_or_tuning():
    spec = {"minimum_games": 20, "minimum_groups": 5, "outer_folds": 5, "inner_folds": 3, "seed": 26, "ridge_alpha_grid": [0.1, 10]}
    rng = np.random.default_rng(26)
    X, y, groups = rng.normal(size=(40, 3)), rng.normal(size=40), np.repeat(np.arange(10), 4)
    first = nested_predictions(X, y, groups, spec)
    held = np.flatnonzero(np.array(first["fold_ids"]) == 0)
    y[held] += 1000
    second = nested_predictions(X, y, groups, spec)
    assert np.allclose(np.array(first["prediction"])[held], np.array(second["prediction"])[held])
    assert first["folds"][0]["alpha"] == second["folds"][0]["alpha"]


def test_end_to_end_excludes_reserved_data_and_refuses_overwrite(tmp_path):
    export, runs, output = tmp_path / "export", tmp_path / "runs", tmp_path / "cycle"
    export.mkdir()
    (runs / "job").mkdir(parents=True)
    stream = transcript(runs / "job" / "stream-0.jsonl", [call("observe", "o"), reply("o", observation()), call("take_action", "a", choice=1), reply("a", {"success": True}),
                        {"message": {"content": [{"type": "text", "text": "PRIVATE_MODEL_NOTES"}]}}])
    evaluation = {"job_id": "job", "actor_id": "actor", "env_id": "env", "policy_id": "policy", "purpose": "screen", "outcome": "completed", "completed": 1, "score": 60,
                  "survival_months": 48, "steps": 1, "trajectory_path": "cloud/job/stream-0.jsonl", "trajectory_sha256": sha256(stream)}
    reserved = {**evaluation, "job_id": "reserved", "purpose": "confirm", "score": 95}
    jobs = [{**{k: e[k] for k in ("job_id", "actor_id", "env_id", "policy_id", "purpose")}, "replicate": i, "origin": "", "status": "done"} for i, e in enumerate((evaluation, reserved))]
    tables = {"evaluations": [evaluation, reserved], "jobs": jobs, "actors": [{"actor_id": "actor", "kind": "claude-cli", "config": '{"model":"haiku"}'}],
              "environments": [{"env_id": "env"}], "policies": [{"policy_id": "policy", "name": "p", "family": "f"}]}
    for name, rows in tables.items():
        (export / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    spec_path = Path(__file__).parents[1] / "research/careerlab/decision-research/exploration-v1.json"
    result = run(export, runs, spec_path, output)
    assert result["coverage"]["eligible_terminal_claude"] == 1
    assert result["coverage"]["excluded_by_purpose"] == {"confirm": 1}
    assert len((output / "episodes.jsonl").read_text().splitlines()) == 1
    assert "PRIVATE_MODEL_NOTES" not in gzip.decompress((output / "actions.jsonl.gz").read_bytes()).decode()
    manifest = json.loads((output / "manifest.json").read_text())
    for name, digest in manifest["code_hashes"].items():
        assert sha256(output / "source" / name) == digest
    assert (output / "runtime.json").is_file()
    with pytest.raises(ValueError, match="Immutable cycle"):
        run(export, runs, spec_path, output)


def test_reanalysis_cannot_be_counted_as_new_games(tmp_path):
    first = tmp_path / "001"
    first.mkdir()
    (first / "episodes.jsonl").write_text('{"job_id":"same","Q":60}\n')
    (first / "manifest.json").write_text('{"input_hashes":{"evaluations":"hash"}}')
    lineage = cycle_lineage(tmp_path / "002", [{"job_id": "same", "Q": 60}], {"evaluations": "hash"})
    assert lineage["new_extracted_games"] == 0
    assert lineage["reused_extracted_games"] == 1
    assert lineage["changed_existing_episode_rows"] == 0
    assert lineage["same_export_hashes"]


def test_confirmation_purposes_remain_forbidden_even_if_added_to_spec(tmp_path):
    spec = tmp_path / "spec.json"
    spec.write_text('{"allowed_purposes":["screen","confirm"]}')
    with pytest.raises(ValueError, match="Reserved confirmation"):
        run(tmp_path / "missing_export", tmp_path / "runs", spec, tmp_path / "new_cycle")
