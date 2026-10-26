from collections import Counter
import json
import gzip
import hashlib

import pytest

from careerlab.mcp_client import ActionResult
from scripts.close_known_frontier import Frontier, episode
from scripts.first_review_search import node_key
from scripts.audit_known_catalogue import audit


def observation(description="root"):
    return {"current_state": {"time": {"current_month": 6}, "status": {"level": "L1", "health": 5},
        "simulation_flags": {"alive": True, "failed": False}},
        "current_event": {"title": "Story", "description": description},
        "choices": [{"choice": 1, "action": "First"}, {"choice": 2, "action": "Second"}]}


def catalogue(obs):
    return [{"id": node_key(obs), "event": obs["current_event"], "choices": obs["choices"],
        "answers": {"1": {"count": 1, "delayed_same_title": {}}}}]


def test_target_is_untried_choice_and_requires_applied_evidence():
    obs = observation()
    f = Frontier(catalogue(obs))
    choice, reason = f.targeted(obs)
    assert choice["choice"] == 2
    assert not f.status()["frozen_catalogue_complete"]
    f.applied(obs, choice, 10, 4)
    assert f.status()["frozen_catalogue_complete"]
    assert f.status()["evidence"][0]["run"] == 10


def test_new_nodes_are_separate_from_frozen_target_denominator():
    obs = observation()
    f = Frontier(catalogue(obs))
    new = observation("previously unseen")
    f.applied(new, new["choices"][0], 11, 3)
    assert f.status()["frozen_available_pairs"] == 2
    assert f.status()["new_available_pairs"] == 2
    assert len(f.remaining()) == 1


def test_route_uses_same_title_continuation_not_random_next_story():
    root, later = observation(), observation("later")
    qs = catalogue(root) + catalogue(later)
    qs[0]["answers"]["2"] = {"count": 2, "delayed_same_title": {node_key(later): 2}}
    f = Frontier(qs)
    assert f.targeted(root)[0]["choice"] == 2
    assert f.targeted(root)[1] == "observed_same_title_route"


class RejectingClient:
    async def new_game(self):
        return "session"

    async def observe(self, sid):
        return observation()

    async def take_action(self, *args):
        return ActionResult(False, {"success": False})


@pytest.mark.asyncio
async def test_rejected_action_does_not_close_target(tmp_path):
    f = Frontier(catalogue(observation()))
    r = await episode(RejectingClient(), tmp_path, 0, "growth", {}, f, Counter(), 1)
    assert r["outcome"] == "interrupted"
    assert len(f.remaining()) == 1
    assert not f.evidence


def archived_example(tmp_path, applied=True):
    obs = observation()
    obs["choices"] = obs["choices"][:1]
    (tmp_path / "questions.json").write_text(json.dumps([{"id": node_key(obs), "phase": "event", "choices": obs["choices"]}]))
    batch = tmp_path / "batch"
    batch.mkdir()
    archive = batch / "public-trajectories.jsonl.gz"
    record = {"run": 0, "steps": [{"before": obs, "after": obs, "choice": obs["choices"][0],
        "applied": applied, "reply": {"success": applied}}]}
    with gzip.open(archive, "wt") as f:
        f.write(json.dumps(record) + "\n")
    (batch / "archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest())
    return archive


def test_independent_audit_requires_successful_in_window_witness(tmp_path):
    archived_example(tmp_path)
    result = audit(tmp_path, tmp_path / "audit.json")
    assert result["complete"] and result["witnessed_story_pairs"] == 1


def test_independent_audit_rejects_offered_but_unapplied_answer(tmp_path):
    archived_example(tmp_path, applied=False)
    with pytest.raises(RuntimeError, match="no successful witness"):
        audit(tmp_path, tmp_path / "audit.json")


def test_independent_audit_rejects_corrupt_evidence(tmp_path):
    archive = archived_example(tmp_path)
    archive.write_bytes(archive.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="Hash mismatch"):
        audit(tmp_path, tmp_path / "audit.json")
