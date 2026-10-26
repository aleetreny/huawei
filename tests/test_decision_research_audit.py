"""Safeguards against false sample sizes and fabricated behavioural data."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("decision_research_audit", Path(__file__).parents[1] / "scripts" / "decision_research_audit.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def write_export(root, evaluations, jobs=None):
    root.mkdir(exist_ok=True)
    if jobs is None:
        jobs = [{**{k: row[k] for k in ("job_id", "actor_id", "env_id", "policy_id", "purpose")}, "replicate": i, "origin": "", "status": "done"} for i, row in enumerate(evaluations)]
    tables = {"evaluations": evaluations, "jobs": jobs, "actors": [{"actor_id": "a", "kind": "claude-cli", "config": '{"model":"haiku"}'}], "environments": [{"env_id": "e"}], "policies": [{"policy_id": "p"}]}
    for name, rows in tables.items():
        (root / f"{name}.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))


def terminal(job_id="one", **kwargs):
    return {"job_id": job_id, "actor_id": "a", "env_id": "e", "policy_id": "p", "purpose": "screen", "outcome": "completed", "completed": 1, "score": 60, **kwargs}


def test_interrupted_and_pending_never_become_zero_scores(tmp_path):
    rows = [terminal(), terminal("bad", outcome="interrupted", completed=0, score=None)]
    write_export(tmp_path, rows)
    jobs = mod.records(tmp_path / "jobs.jsonl") + [{"job_id": "pending", "status": "running"}]
    write_export(tmp_path, rows, jobs)
    result = mod.audit(tmp_path)
    assert result["terminal"] == 1
    assert result["actor_environment_summaries"][0]["mean_Q_descriptive"] == 60
    assert result["jobs_without_evaluation_by_status"] == {"running": 1}
    assert result["trace_status_counts_non_scripted_terminal"] == {"not_checked": 1}


def test_duplicate_scored_attempts_in_same_slot_are_rejected(tmp_path):
    rows = [terminal(), terminal("replacement")]
    write_export(tmp_path, rows)
    jobs = mod.records(tmp_path / "jobs.jsonl")
    jobs[1]["replicate"] = 0
    write_export(tmp_path, rows, jobs)
    with pytest.raises(ValueError, match="Two scored attempts"):
        mod.audit(tmp_path)


@pytest.mark.parametrize("score", [None, float("nan"), float("inf"), -1, 101, True])
def test_invalid_terminal_scores_fail_closed(tmp_path, score):
    write_export(tmp_path, [terminal(score=score)])
    with pytest.raises(ValueError, match="Invalid terminal score"):
        mod.audit(tmp_path)


def test_missing_or_changed_trace_never_yields_behavioural_zeros(tmp_path):
    row = terminal(trajectory_path="old-host/one/stream-0.jsonl", trajectory_sha256="wrong")
    assert mod.trace_info(row, tmp_path) == {"status": "missing"}
    (tmp_path / "one").mkdir()
    (tmp_path / "one" / "stream-0.jsonl").write_text("{}\n")
    assert mod.trace_info(row, tmp_path) == {"status": "hash_mismatch"}


def test_only_official_observations_count_and_continuations_get_hashes(tmp_path):
    run = tmp_path / "one"
    run.mkdir()
    obs = {"current_state": {"time": {"current_month": 2}, "status": {"health": 5}}}
    content = [{"type": "tool_use", "id": "obs", "name": "mcp__game__observe"}, {"type": "tool_use", "id": "handbook", "name": "mcp__game__show_employee_handbook"}]
    rows = [{"message": {"content": content}}, {"message": {"content": [{"type": "tool_result", "tool_use_id": key, "content": json.dumps(obs)} for key in ("obs", "handbook")]}}]
    primary = run / "stream-0.jsonl"
    primary.write_text("".join(json.dumps(row) + "\n" for row in rows))
    (run / "stream-1.jsonl").write_text("{}\n")
    row = terminal(trajectory_path="/cloud/one/stream-0.jsonl", trajectory_sha256=hashlib.sha256(primary.read_bytes()).hexdigest())
    result = mod.trace_info(row, tmp_path)
    assert result["observations"] == 1
    assert result["min_month"] == 2
    assert len(result["files"]) == 2
    assert result["files"][1]["registry_hash_covers_file"] is False
    assert "health" not in json.dumps(result)


def test_duplicate_evaluation_is_rejected(tmp_path):
    write_export(tmp_path, [terminal()])
    with (tmp_path / "evaluations.jsonl").open("a") as out:
        out.write(json.dumps(terminal()) + "\n")
    with pytest.raises(ValueError, match="Duplicate evaluation"):
        mod.audit(tmp_path)


def test_inconsistent_terminal_outcome_is_rejected(tmp_path):
    write_export(tmp_path, [terminal(outcome="eliminated", completed=1)])
    with pytest.raises(ValueError, match="Inconsistent terminal outcome"):
        mod.audit(tmp_path)


def test_actor_configurations_remain_separate(tmp_path):
    write_export(tmp_path, [terminal(), terminal("two", actor_id="b", score=30)])
    actors = mod.records(tmp_path / "actors.jsonl") + [{"actor_id": "b", "kind": "claude-cli", "config": '{"model":"haiku","effort":"low"}'}]
    (tmp_path / "actors.jsonl").write_text("".join(json.dumps(row) + "\n" for row in actors))
    result = mod.audit(tmp_path)
    assert len(result["actor_environment_summaries"]) == 2
    assert {r["mean_Q_descriptive"] for r in result["actor_environment_summaries"]} == {30, 60}
