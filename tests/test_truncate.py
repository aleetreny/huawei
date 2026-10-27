"""Short games: cut at a month, review snapshots, and never scored."""

import asyncio
import json
from dataclasses import asdict

from careerlab.actors.claude_cli import ClaudeWorkerConfig, _wait_or_cut
from careerlab.episode import EpisodeResult
from careerlab.store import Registry, canonical_hash
from careerlab.truncate import StreamWatcher, log_facts, max_month, review_snapshots, summarize


def _obs_line(month: int, level: int = 1, skill: int = 5, network: int = 2, output: int = 1) -> str:
    obs = {"current_state": {"time": {"current_month": month},
                             "status": {"level": f"L{level}", "skill": skill, "network": network, "output": output,
                                        "health": 7, "dignity": 6, "wealth": 1}}}
    msg = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "x", "content": json.dumps(obs)}]}}
    return json.dumps(msg)


def test_max_month_reads_only_tool_results():
    noise = json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": '"current_month": 40'}]}})
    assert max_month([noise, _obs_line(3), _obs_line(5)]) == 5


def test_watcher_reads_incrementally_and_waits_for_whole_lines(tmp_path):
    stream = tmp_path / "s.jsonl"
    line = _obs_line(4)
    stream.write_text(line[:30])
    w = StreamWatcher(stream)
    assert w.poll() == 0
    with stream.open("a") as fh:
        fh.write(line[30:] + "\n" + _obs_line(6) + "\n")
    assert w.poll() == 6


def test_review_snapshots_promotion_grade_and_hr():
    states = [{"month": m, "level": lv, "skill": 9, "network": 3, "output": 3} for m, lv in [(4, 1), (5, 1), (6, 2), (6, 2)]]
    entries = [
        {"entry_type": "action", "message": "Month 5 | Something"},
        {"entry_type": "salary", "message": "Monthly base salary\n\nAn HR partner says quietly, there's some risk lately, but it isn't serious yet."},
        {"entry_type": "warning", "message": "Old landmines all go off at once"},
        {"entry_type": "salary", "message": "Half-year performance bonus (C): +0.075"},
    ]
    facts = log_facts(entries)
    assert facts["blowup_months"] == [5] and facts["grades"] == ["C"] and facts["hr_by_month"] == {5: 1}
    rows = review_snapshots(states, facts, 6)
    assert len(rows) == 1 and rows[0]["promoted"] and rows[0]["grade"] == "C" and rows[0]["hr_tier_before"] == 1
    assert rows[0]["before"]["month"] == 5 and rows[0]["after"]["level"] == 2


def test_summarize_ignores_reviews_not_reached(tmp_path):
    stream = tmp_path / "stream-0.jsonl"
    stream.write_text("\n".join(_obs_line(m) for m in range(1, 6)) + "\n")
    out = summarize([stream], [], 5)
    assert out["reviews"] == [] and out["final_state"]["month"] == 5


def test_full_game_actor_id_is_unchanged_and_cut_actor_differs():
    full = ClaudeWorkerConfig(model="haiku", cli_version="2.1.303 (Claude Code)")
    cut = ClaudeWorkerConfig(model="haiku", cli_version="2.1.303 (Claude Code)", stop_at_month=6)
    assert "stop_at_month" not in full.record()
    assert cut.record()["stop_at_month"] == 6
    assert canonical_hash(full.record()) != canonical_hash(cut.record())


def test_wait_or_cut_stops_the_worker_at_the_month(tmp_path):
    stream = tmp_path / "stream-0.jsonl"
    lines = "\n".join(_obs_line(m) for m in range(1, 8))
    script = f"import time\nopen({str(stream)!r}, 'w').write({lines!r} + '\\n')\ntime.sleep(60)\n"

    async def go():
        import sys

        from careerlab.actors.claude_cli import StreamSummary
        proc = await asyncio.create_subprocess_exec(sys.executable, "-c", script)
        summary = StreamSummary()
        await asyncio.wait_for(_wait_or_cut(proc, stream, 6, summary, poll_s=0.2), timeout=30)
        return proc.returncode, summary.errors

    code, errors = asyncio.run(go())
    assert code is not None and errors and errors[0].startswith("cut at month")


def test_truncated_games_are_stored_done_but_never_scored(tmp_path):
    reg = Registry(tmp_path / "reg.sqlite3")
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "scripted.json").write_text('{"rule_set": "uniform"}')
    pid = reg.register_policy(bundle, "fam", "p", [], "h", "c", "test")
    aid = reg.register_actor("scripted", {"name": "x"})
    eid = reg.register_environment({"environment": "test"})
    (job,) = reg.enqueue(pid, aid, eid, "pilot", 1)
    reg.lease("me", 1)
    run_dir = tmp_path / job
    run_dir.mkdir()
    result = EpisodeResult(job, "s" * 32, "truncated", quantitative_score=50.0)
    (run_dir / "result.json").write_text(json.dumps(asdict(result)))
    reg.mark_running(job, 1, str(run_dir))
    assert reg.ingest(job, run_dir) == "truncated"
    assert reg.cell_scores(pid, aid) == []
    row = reg.db.execute("SELECT status FROM jobs WHERE job_id=?", (job,)).fetchone()
    assert row[0] == "done"
    score = reg.db.execute("SELECT score FROM evaluations WHERE job_id=?", (job,)).fetchone()[0]
    assert score is None
