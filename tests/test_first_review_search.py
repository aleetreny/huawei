"""Research harness boundaries: window, rejected actions and empirical coverage."""
import json
import random
from collections import Counter
from pathlib import Path

import pytest

from careerlab.mcp_client import ActionResult
from scripts.analyze_first_review import analyze
from scripts.first_review_search import choose, node_key, run_one


def observation(month, level="L1", title="Question", choices=None, events=""):
    return {"current_state": {"time": {"current_month": month}, "status": {"level": level, "health": 5, "skill": 9, "network": 3, "output": 3},
                              "simulation_flags": {"alive": True, "failed": False}},
            "current_event": {"title": title}, "choices": choices or [{"choice": 1, "action": "Explain"}, {"choice": 2, "action": "Wait"}], "events": events}


class WindowClient:
    def __init__(self, reject=False):
        self.index = 0
        self.reject = reject
        self.observations = [observation(5), observation(6, "L2", events="Half-year performance bonus (C): +0.075"), observation(7, "L2")]

    async def new_game(self):
        return "session"

    async def observe(self, sid):
        return self.observations[self.index]

    async def take_action(self, sid, choice, notes, before):
        if not self.reject:
            self.index += 1
        return ActionResult(not self.reject, {"success": not self.reject})

    async def logs(self, sid, count):
        return {"entries": []}


@pytest.mark.asyncio
async def test_window_retains_review_and_stops_before_month_seven_action(tmp_path):
    client = WindowClient()
    record = await run_one(client, tmp_path, 0, 1, ("first", "balanced", "project"), Counter())
    assert record["outcome"] == "six_month_window"
    assert record["promoted"] is True
    assert len(record["steps"]) == 2
    assert record["steps"][0]["before"]["current_state"]["time"]["current_month"] == 5
    analyze(tmp_path, tmp_path / "analysis")
    summary = json.loads((tmp_path / "analysis/summary.json").read_text())
    assert summary["groups"]["all"]["review"] == 1
    questions = json.loads((tmp_path / "analysis/questions.json").read_text())
    assert questions[0]["untried_choices"] == [2]


@pytest.mark.asyncio
async def test_rejection_is_interruption_not_failed_game_or_zero_promotion(tmp_path):
    record = await run_one(WindowClient(reject=True), tmp_path, 0, 1, ("first", "balanced", "project"), Counter())
    assert record["outcome"] == "interrupted"
    assert "Rejected action" in record["error"]
    assert "promoted" not in record


def test_skip_main_action_uses_public_label():
    obs = observation(3, choices=[{"choice": 9, "action": "No action"}])
    obs["current_event"]["max_selections"] = 1
    assert choose(obs, random.Random(1), "first", "balanced", "none", {}, Counter())["choice"] == 9


def test_reserving_energy_uses_observed_public_label():
    obs = observation(3, choices=[{"choice": 8, "action": "Reserve energy (no action)", "energy_cost": 0}])
    obs["current_event"]["remaining_energy"] = 3
    assert choose(obs, random.Random(1), "coverage", "skip", "none", {}, Counter())["choice"] == 8


def test_visible_question_key_deliberately_does_not_claim_state_identity():
    left, right = observation(3), observation(5)
    right["current_state"]["status"]["health"] = 1
    assert node_key(left) == node_key(right)


def test_frontier_prioritizes_untried_answer_over_a_known_chain():
    obs = observation(2)
    key = node_key(obs)
    counts = Counter({(key, 1): 10})
    model = {"distances": {"later": 0}, "paths": {(key, 1): ["later"]}}
    assert choose(obs, random.Random(1), "frontier", "recovery", "project", {}, counts, model)["choice"] == 2


def test_frontier_follows_observed_same_title_chain_when_answers_tried():
    obs = observation(2)
    key = node_key(obs)
    counts = Counter({(key, 1): 10, (key, 2): 10})
    model = {"distances": {"later": 0}, "paths": {(key, 2): ["later"]}}
    assert choose(obs, random.Random(1), "frontier", "recovery", "project", {}, counts, model)["choice"] == 2
