import json

import pytest

from careerlab.mcp_client import ActionResult
from scripts.first_review_transfer import WindowBridge, classify, quota_reason, study_system


def observation(month=7, level="L2", failed=False):
    return {"current_state": {"time": {"current_month": month}, "status": {"level": level, "health": 5},
        "simulation_flags": {"alive": not failed, "failed": failed, "failure_reason": "test" if failed else None}}}


class Client:
    def __init__(self, obs):
        self.obs = obs
        self.calls = 0

    async def observe(self, sid):
        return self.obs

    async def take_action(self, sid, choice, notes, before):
        self.calls += 1
        return ActionResult(True, {"success": True})


@pytest.mark.asyncio
async def test_horizon_bridge_blocks_month_seven_before_official_mutation(tmp_path):
    client = Client(observation())
    result = await WindowBridge(client, tmp_path).take_action("sid", 1)
    assert not result["success"]
    assert client.calls == 0
    assert json.loads((tmp_path / "public-tools.jsonl").read_text())["guard_blocked"]


@pytest.mark.asyncio
async def test_bridge_preserves_window_action_and_journals_both_observations(tmp_path):
    client = Client(observation(month=6))
    result = await WindowBridge(client, tmp_path).take_action("sid", 1)
    assert result == {"success": True}
    assert client.calls == 1
    event = json.loads((tmp_path / "public-tools.jsonl").read_text())
    assert event["before"] == event["after"] == client.obs


def test_quota_blocks_current_window_but_not_expired_window():
    info = {"unifiedWindows": {"five_hour": {"utilization": .99, "resetsAt": 200}}}
    assert quota_reason(info, now=100)
    assert quota_reason(info, now=201) is None
    assert quota_reason({"isUsingOverage": True}, now=100)


def test_promotion_is_distinct_from_window_survival():
    result = classify(observation(6, "L2", True), {"entries": []})
    assert result["promotion"]
    assert not result["alive_through_month_6"]
    assert not result["promotion_and_alive"]
    assert classify(observation(5), {"entries": []})["outcome"] == "interrupted"


def test_scope_adaptation_is_shared_and_does_not_add_research_lookup(tmp_path):
    (tmp_path / "skills/example").mkdir(parents=True)
    (tmp_path / "manifest.json").write_text('{"instruction":""}')
    (tmp_path / "skills/example/SKILL.md").write_text("Protect dignity and deliver credited results.")
    system = study_system(tmp_path)
    assert "Protect dignity and deliver credited results." in system
    assert "current_month greater than 6" in system
    assert "finish one full career-emulator game" not in system
    assert "503" not in system and "frozen-effect-model" not in system
