import gzip
import hashlib
import json

import pytest

from scripts.audit_promotion_observability import analyze


def record(sid, promoted, action="Deliver", health=8):
    before = {"current_state": {"session_id": sid, "status": {
        "level": "L1", "health": health, "skill": 8, "network": 3, "output": 3}},
        "current_event": {"title": "Public question"}, "choices": [{"choice": 1, "action": action}]}
    after = {"current_state": {"status": {"level": "L2" if promoted else "L1"}},
        "events": "Half-year performance bonus (C)"}
    return {"run": sid, "steps": [{"before": before, "after": after,
        "choice": {"choice": 1, "action": action}, "applied": True, "ambiguous": False}]}


def archive(tmp_path, records):
    batch = tmp_path / "input" / "batch"
    batch.mkdir(parents=True)
    path = batch / "public-trajectories.jsonl.gz"
    with gzip.open(path, "wt") as stream:
        for r in records:
            stream.write(json.dumps(r) + "\n")
    (batch / "archive-sha256.txt").write_text(hashlib.sha256(path.read_bytes()).hexdigest())
    return batch.parent


def test_same_observation_and_action_conflict_ignores_session_id(tmp_path):
    root = archive(tmp_path, [record("a", True), record("b", False)])
    output = tmp_path / "audit.json"
    analyze(root, output)
    result = json.loads(output.read_text())
    assert result["projections"]["full_observation_and_choice"]["conflicting_groups"] == 1


def test_different_actions_do_not_prove_same_action_conflict(tmp_path):
    root = archive(tmp_path, [record("a", True), record("b", False, action="Recover")])
    output = tmp_path / "audit.json"
    analyze(root, output)
    result = json.loads(output.read_text())["projections"]
    assert result["status_only"]["conflicting_groups"] == 1
    assert result["full_observation_and_choice"]["conflicting_groups"] == 0


def test_rejected_or_ambiguous_action_is_not_evidence(tmp_path):
    rejected = record("b", False)
    rejected["steps"][0]["applied"] = False
    ambiguous = record("c", False)
    ambiguous["steps"][0]["ambiguous"] = True
    root = archive(tmp_path, [record("a", True), rejected, ambiguous])
    output = tmp_path / "audit.json"
    analyze(root, output)
    result = json.loads(output.read_text())
    assert result["counts"]["excluded_unconfirmed_actions"] == 2
    assert result["projections"]["full_observation_and_choice"]["conflicting_groups"] == 0


def test_archive_integrity_is_checked(tmp_path):
    root = archive(tmp_path, [record("a", True)])
    (root / "batch" / "archive-sha256.txt").write_text("bad")
    with pytest.raises(ValueError, match="integrity"):
        analyze(root, tmp_path / "audit.json")
