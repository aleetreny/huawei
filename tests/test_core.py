"""Core runner and registry tests with a fake game client (no game server)."""

import asyncio
import json
from pathlib import Path

import pytest

from careerlab.episode import Decision, run_driven_episode
from careerlab.mcp_client import ActionResult, CallStats, fingerprint
from careerlab.store import Registry


class FakeClient:
    """Three-step game; optionally loses one take_action reply after applying it."""

    def __init__(self, lose_reply_at: int | None = None, die: bool = False, vanish_at: int | None = None):
        self.stats = CallStats()
        self.t = 0
        self.lose_reply_at, self.die, self.vanish_at = lose_reply_at, die, vanish_at

    async def new_game(self) -> str:
        return "s" * 32

    def _obs(self) -> dict:
        state = {"time": {"current_month": self.t + 1}, "status": {"health": 5}, "simulation_flags": {"alive": True, "failed": False}}
        if self.t >= 3:
            state["simulation_flags"] = {"alive": not self.die, "failed": self.die, "failure_reason": "x" if self.die else None}
            return {"current_state": state, "choices": [], "ending_score": {"outcome": "eliminated" if self.die else "completed",
                    "survival_months": 3, "completed": not self.die, "quantitative_score": 42.0, "dimensions": []}}
        return {"current_state": state, "current_event": {"title": f"e{self.t}"}, "choices": [{"choice": 1}, {"choice": 2}]}

    async def observe(self, sid: str) -> dict:
        self.stats.add("observe", 0.001)
        if self.vanish_at is not None and self.t >= self.vanish_at:
            from careerlab.mcp_client import ToolError
            raise ToolError("observe failed: Unknown session_id")
        return self._obs()

    async def take_action(self, sid, choice, notes, before):
        self.stats.add("take_action", 0.001)
        if self.lose_reply_at == self.t:
            self.t += 1  # applied, but the reply is lost
            self.stats.ambiguous_actions += 1
            after = self._obs()
            return ActionResult(applied=fingerprint(after) != fingerprint(before), reply={"inferred": True}, attempts=1, ambiguous=True)
        self.t += 1
        return ActionResult(applied=True, reply={"success": True})


class FirstChoice:
    def config(self):
        return {"kind": "test"}

    async def decide(self, obs, memory):
        return Decision(obs["choices"][0]["choice"])


def run(client, tmp_path, job="j1"):
    return asyncio.run(run_driven_episode(client, FirstChoice(), job, tmp_path / job))


def test_completed_episode(tmp_path):
    res = run(FakeClient(), tmp_path)
    assert res.outcome == "completed" and res.quantitative_score == 42.0 and res.steps == 3
    assert json.loads((tmp_path / "j1" / "result.json").read_text())["outcome"] == "completed"


def test_game_failure_is_elimination_not_interruption(tmp_path):
    res = run(FakeClient(die=True), tmp_path)
    assert res.outcome == "eliminated" and res.quantitative_score == 42.0


def test_lost_reply_is_inferred_from_state_not_retried(tmp_path):
    client = FakeClient(lose_reply_at=1)
    res = run(client, tmp_path)
    assert res.outcome == "completed" and res.steps == 3 and client.t == 3  # no duplicate action


def test_vanished_session_is_interruption_without_score(tmp_path):
    res = run(FakeClient(vanish_at=2), tmp_path)
    assert res.outcome == "interrupted" and res.quantitative_score is None and "Unknown session" in res.interruption


def _registry(tmp_path) -> tuple[Registry, str, str, str]:
    reg = Registry(tmp_path / "reg.sqlite3")
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "scripted.json").write_text('{"rule_set": "uniform"}')
    pid = reg.register_policy(bundle, "fam", "p", [], "h", "c", "test")
    aid = reg.register_actor("scripted", {"name": "x"})
    eid = reg.register_environment({"environment": "test"})
    return reg, pid, aid, eid


def test_policy_identity_is_content_hash(tmp_path):
    reg, pid, _, _ = _registry(tmp_path)
    assert reg.verify_policy(pid)
    (tmp_path / "bundle" / "scripted.json").write_text('{"rule_set": "other"}')
    assert not reg.verify_policy(pid)  # edited bytes no longer match the registered id
    with pytest.raises(ValueError):
        reg.register_policy(tmp_path / "bundle", "fam", "q", ["missing-parent"], "h", "c", "test")


def test_enqueue_is_idempotent_and_ingest_never_scores_interruptions(tmp_path):
    reg, pid, aid, eid = _registry(tmp_path)
    jobs = reg.enqueue(pid, aid, eid, "pilot", 2) + reg.enqueue(pid, aid, eid, "pilot", 1)
    assert len(set(jobs)) == 3
    leased = reg.lease("me", 10)
    assert len(leased) == 3 and not reg.lease("other", 10)
    r1 = run(FakeClient(), tmp_path, jobs[0])
    r2 = run(FakeClient(vanish_at=1), tmp_path, jobs[1])
    reg.mark_running(jobs[0], 1, str(tmp_path / jobs[0]))
    assert reg.ingest(jobs[0], tmp_path / jobs[0]) == "completed"
    assert reg.ingest(jobs[1], tmp_path / jobs[1]) == "interrupted"
    assert reg.cell_scores(pid, aid) == [42.0]
    retry = reg.requeue_interrupted(jobs[1], "vanished session")
    assert retry.endswith("-a2")


def test_recover_ingests_finished_and_marks_dead_workers(tmp_path):
    reg, pid, aid, eid = _registry(tmp_path)
    done, dead, fresh = reg.enqueue(pid, aid, eid, "pilot", 3)
    reg.lease("ghost", 3)
    run(FakeClient(), tmp_path, done)
    reg.mark_running(done, 999999, str(tmp_path / done))   # result exists, process gone
    reg.mark_running(dead, 999999, str(tmp_path / dead))   # no result, process gone
    counts = reg.recover(lambda owner: False)
    assert counts == {"ingested": 1, "interrupted": 1, "still_running": 0, "released": 1}
    status = dict(reg.db.execute("SELECT job_id, status FROM jobs").fetchall())
    assert status[done] == "done" and status[dead] == "interrupted" and status[fresh] == "queued"


class _Server:
    """State machine behind a GameClient whose transport may drop replies."""

    def __init__(self, drop: str):
        self.t, self.drop, self.actions = 0, drop, 0

    async def call(self, tool, args=None, timeout_s=None):
        if tool == "observe":
            return {"current_state": {"time": {"current_month": self.t}}, "choices": [{"choice": 1}]}
        if tool == "take_action":
            if self.drop == "after-apply" and self.actions == 0:
                self.actions += 1
                self.t += 1
                raise TimeoutError("reply lost after the server applied the action")
            if self.drop == "before-apply" and self.actions == 0:
                self.actions += 1
                raise TimeoutError("request lost before the server saw it")
            self.t += 1
            return {"success": True, "error": None}
        raise AssertionError(tool)


@pytest.mark.parametrize("drop,expected_t,attempts", [("after-apply", 1, 1), ("before-apply", 1, 2)])
def test_take_action_observes_before_retrying(drop, expected_t, attempts):
    from careerlab.config import Settings
    from careerlab.mcp_client import GameClient, ServerSpec

    server = _Server(drop)
    client = GameClient(ServerSpec("x", Path("/tmp")), Settings())
    client.call = server.call  # type: ignore[method-assign]
    before = asyncio.run(client.observe("s"))
    result = asyncio.run(client.take_action("s", 1, "", before=before))
    assert result.applied and server.t == expected_t and result.attempts == attempts


def test_report_uses_protocol_outcome_and_counts_interruptions(tmp_path):
    from careerlab.report import cell_report

    reg, pid, aid, eid = _registry(tmp_path)
    jobs = reg.enqueue(pid, aid, eid, "screen", 3)
    reg.lease("me", 3)
    for j in jobs[:2]:
        run(FakeClient(), tmp_path, j)
        reg.ingest(j, tmp_path / j)
    run(FakeClient(vanish_at=1), tmp_path, jobs[2])
    reg.ingest(jobs[2], tmp_path / jobs[2])
    cell = cell_report(reg)["groups"][0]["cells"][0]
    # Q = 42 and completed without token counts: Y = 0.8*42 + 0.1*100 (imputed E for a completed run).
    assert cell["n"] == 2 and cell["interrupted_attempts"] == 1 and abs(cell["mean_Y"] - 43.6) < 1e-9


def test_bridge_refuses_non_local_servers(capsys):
    from careerlab.bridge import main

    assert main(["--url", "https://example.com/mcp", "new"]) == 2
    assert "only talks to a local" in capsys.readouterr().out


def test_live_owner_jobs_are_never_recovered_or_double_claimed(tmp_path):
    reg, pid, aid, eid = _registry(tmp_path)
    jobs = reg.enqueue(pid, aid, eid, "screen", 2)
    reg.lease("A", 2)
    counts = reg.recover(lambda owner: owner == "A")  # a second scheduler starting up while A is alive
    assert counts["still_running"] == 2 and counts["released"] == 0
    assert not reg.mark_running(jobs[0], 1, "x", owner="B")  # B cannot run A's job
    assert reg.mark_running(jobs[0], 1, "x", owner="A")
    assert not reg.mark_running(jobs[0], 1, "x", owner="A")  # and A cannot start it twice


def test_owner_alive_uses_local_pid(tmp_path):
    import os
    import socket

    from careerlab.config import Settings
    from careerlab.scheduler import Scheduler

    sched = Scheduler(Settings(data_dir=tmp_path), Registry(tmp_path / "r.sqlite3"))
    assert sched.owner_alive(f"{socket.gethostname()}:{os.getpid()}:abc")
    assert not sched.owner_alive(f"{socket.gethostname()}:999999:abc")


def test_export_import_round_trip(tmp_path):
    from careerlab.store import import_jsonl

    reg, pid, aid, eid = _registry(tmp_path)
    jobs = reg.enqueue(pid, aid, eid, "screen", 2)
    reg.lease("A", 2)
    run(FakeClient(), tmp_path, jobs[0])
    reg.ingest(jobs[0], tmp_path / jobs[0])
    reg.decide("block_decision", aid, {"x": 1}, "test")
    reg.export_jsonl(tmp_path / "export")
    other = Registry(tmp_path / "other.sqlite3")
    counts = import_jsonl(other, tmp_path / "export", tmp_path / "data", tmp_path / "lab")
    assert counts["evaluations"] == 1 and counts["jobs"] == 2
    statuses = dict(other.db.execute("SELECT job_id, status FROM jobs").fetchall())
    assert statuses[jobs[0]] == "done" and statuses[jobs[1]] == "queued"  # a lease from another machine is released
    assert other.cell_scores(pid, aid) == [42.0]
    import_jsonl(other, tmp_path / "export", tmp_path / "data", tmp_path / "lab")  # idempotent
    assert other.db.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0] == 1


def test_digest_pairs_actions_with_the_observation_before_them(tmp_path):
    from careerlab.digest import game_lines

    obs = {"current_state": {"time": {"current_month": 6}, "status": {"health": 7, "level": "L2"}},
           "current_event": {"title": "A choice"}, "choices": [{"choice": 1, "action": "Be honest"}, {"choice": 2, "action": "Bluff"}],
           "events": "[Half-year talk] Half-year performance bonus (C): +0.075"}
    stream = [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "a", "name": "mcp__career-emulator-engine__observe", "input": {}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "a", "content": [{"type": "text", "text": json.dumps(obs)}]}]}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "b", "name": "mcp__career-emulator-engine__take_action",
                                                       "input": {"choice": 1, "notes": "keep trust"}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "b", "content": '{"success":false,"error":"too costly"}'}]}},
    ]
    (tmp_path / "stream-0.jsonl").write_text("\n".join(json.dumps(e) for e in stream))
    lines, grades = game_lines(tmp_path)
    assert grades == ["C"]
    assert lines[0].startswith("  > [Half-year talk]")
    assert lines[1].startswith("- M6 [7/?/?/?/L2/?/?/?] A choice → [1] Be honest (declined: [2] Bluff)")
    assert "notes: keep trust" in lines[1] and "REJECTED: too costly" in lines[1]


def test_weekly_pace_spreads_the_seven_day_window_to_the_last_cutoff():
    from careerlab.scheduler import COMPETITION_END, weekly_allowance

    resets = COMPETITION_END + 16 * 3600  # the window that opened 26 Oct 16:00 UTC
    start = resets - 7 * 86400
    assert weekly_allowance(start, resets) == pytest.approx(0.10)
    assert weekly_allowance(COMPETITION_END, resets) == pytest.approx(0.90)
    assert weekly_allowance(resets, resets) == pytest.approx(0.90)
    assert 0.10 < weekly_allowance((start + COMPETITION_END) / 2, resets) < 0.90
    assert weekly_allowance(start, resets, {"initial": 1.0, "final": 1.0}) == 1.0


def test_latest_quota_reads_either_window(tmp_path):
    from careerlab.scheduler import latest_quota

    run = tmp_path / "job-1"
    run.mkdir()
    windows = {"five_hour": {"utilization": 0.4, "resetsAt": 10}, "seven_day": {"utilization": 0.2, "resetsAt": 20}}
    (run / "stream-0.jsonl").write_text(json.dumps({"type": "rate_limit_event", "rate_limit_info": {"unifiedWindows": windows}}) + "\n")
    assert latest_quota(tmp_path) == (0.4, 10.0)
    assert latest_quota(tmp_path, window="seven_day") == (0.2, 20.0)
