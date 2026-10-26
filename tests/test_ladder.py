"""Fast race (fastloop-v2): the ladder keeps, drops and crowns challengers by P(better than the champion)."""

import time

from careerlab import ladder
from careerlab.ladder import Cell, LadderConfig
from careerlab.scheduler import weekly_allowance
from careerlab.store import Registry

CFG = LadderConfig(draws=4000)


def _registry(tmp_path, names):
    reg = Registry(tmp_path / "r.sqlite3")
    aid = reg.register_actor("claude-cli", {"model": "haiku"})
    eid = reg.register_environment({"environment": "test"})
    ids = {}
    for name in names:
        bundle = tmp_path / name / "bundle"
        bundle.mkdir(parents=True)
        (bundle / "SKILL.md").write_text(name)
        ids[name] = reg.register_policy(bundle, "fam", name, [], f"idea of {name}", "c", "test")
    return reg, aid, eid, ids


def _play(reg, pid, aid, eid, games, purpose="screen"):
    """Finish queued jobs of a policy (or new ones) with the given (score, completed) results."""
    queued = [r[0] for r in reg.db.execute("SELECT job_id FROM jobs WHERE policy_id=? AND status='queued' ORDER BY created_at", (pid,))]
    while len(queued) < len(games):
        queued += reg.enqueue(pid, aid, eid, purpose, 1)
    for job, (score, done) in zip(queued, games):
        reg.db.execute("INSERT INTO evaluations (job_id, policy_id, actor_id, env_id, purpose, outcome, survival_months, completed, score, ingested_at) "
                       "VALUES (?,?,?,?,?,?,?,?,?,?)", (job, pid, aid, eid, purpose, "completed" if done else "eliminated", 48 if done else 24,
                                                         int(done), score, time.time()))
        reg.db.execute("UPDATE jobs SET status='done' WHERE job_id=?", (job,))


STRONG = [(71, True)] * 8
WEAK = [(30, False), (25, False)]


def _step(reg, state, now, in_flight=None):
    new, acts = ladder.step(state, ladder.load_cells(reg, state["actor_id"]), CFG, now, in_flight)
    ladder.apply(reg, new, acts)
    return new, acts


def test_p_better_tracks_completion_and_score():
    champ = Cell([62.0, 64.0, 30.0, 63.0, 61.0, 65.0, 28.0, 60.0], [True, True, False, True, True, True, False, True])
    assert ladder.p_better(Cell([71.0] * 4, [True] * 4), champ, CFG) > 0.8
    assert ladder.p_better(Cell([30.0, 25.0], [False, False]), champ, CFG) < 0.05
    assert ladder.p_better(Cell([71.0] * 4, [True] * 4), champ, CFG) == ladder.p_better(Cell([71.0] * 4, [True] * 4), champ, CFG)


def test_weak_challenger_leaves_after_two_games_and_its_queue_is_cancelled(tmp_path):
    reg, aid, eid, ids = _registry(tmp_path, ["champ", "weak"])
    _play(reg, ids["champ"], aid, eid, [(63, True)] * 7 + [(30, False)])
    state = ladder.new_state(reg, aid, CFG, 0.0)
    assert state["champion"] == ids["champ"]
    state = ladder.add(state, ids["weak"], "weak", "targeted", 1.0)
    state, acts = _step(reg, state, 2.0)
    assert [(a.kind, a.policy_id, a.n) for a in acts if a.kind == "enqueue"] == [("enqueue", ids["weak"], 2)]
    _play(reg, ids["weak"], aid, eid, WEAK)
    reg.enqueue(ids["weak"], aid, eid, "ladder", 3)  # stray queued jobs must be withdrawn when it leaves
    state, acts = _step(reg, state, 3.0)
    assert state["entries"][ids["weak"]]["status"] == "out"
    assert reg.db.execute("SELECT COUNT(*) FROM jobs WHERE policy_id=? AND status='queued'", (ids["weak"],)).fetchone()[0] == 0
    assert reg.db.execute("SELECT status FROM policies WHERE policy_id=?", (ids["weak"],)).fetchone()[0] == "retired"


def test_strong_challenger_climbs_and_is_crowned_and_old_variants_are_dropped(tmp_path):
    reg, aid, eid, ids = _registry(tmp_path, ["champ", "strong", "variant"])
    _play(reg, ids["champ"], aid, eid, [(63, True)] * 7 + [(30, False)])
    state = ladder.new_state(reg, aid, CFG, 0.0)
    state = ladder.add(state, ids["strong"], "strong", "external", 1.0, first=4)
    state = ladder.add(state, ids["variant"], "variant", "targeted", 1.5)
    state, acts = _step(reg, state, 2.0)
    assert ("enqueue", ids["strong"], 4) in [(a.kind, a.policy_id, a.n) for a in acts]
    _play(reg, ids["strong"], aid, eid, STRONG[:4])
    state, acts = _step(reg, state, 3.0)
    assert state["entries"][ids["strong"]]["rung"] == 2
    assert ("enqueue", ids["strong"], 4) in [(a.kind, a.policy_id, a.n) for a in acts]  # up to 8 games
    _play(reg, ids["strong"], aid, eid, STRONG[4:])
    state, acts = _step(reg, state, 4.0)
    assert state["champion"] == ids["strong"]
    assert state["entries"][ids["champ"]]["status"] == "runner_up"
    assert state["entries"][ids["variant"]]["status"] == "cancelled"  # built on the old champion, never played
    assert reg.db.execute("SELECT COUNT(*) FROM jobs WHERE policy_id=? AND status='queued'", (ids["variant"],)).fetchone()[0] == 0
    assert any(a.kind == "design" for a in acts)  # pipeline refills with variants of the new champion


def test_close_call_at_eight_games_plays_to_twelve(tmp_path):
    reg, aid, eid, ids = _registry(tmp_path, ["champ", "close"])
    _play(reg, ids["champ"], aid, eid, [(70, True)] * 8)
    state = ladder.new_state(reg, aid, CFG, 0.0)
    state = ladder.add(state, ids["close"], "close", "targeted", 1.0)
    _play(reg, ids["close"], aid, eid, [(70, True)] * 8)
    state, acts = _step(reg, state, 2.0)
    e = state["entries"][ids["close"]]
    assert e["status"] == "active" and e["rung"] == 3 and 0.35 <= e["p_better"] < 0.6
    assert ("enqueue", ids["close"], 4) in [(a.kind, a.policy_id, a.n) for a in acts]


def test_stuck_race_asks_for_bold_designs(tmp_path):
    names = ["champ"] + [f"w{i}" for i in range(6)]
    reg, aid, eid, ids = _registry(tmp_path, names)
    _play(reg, ids["champ"], aid, eid, [(70, True)] * 8)
    state = ladder.new_state(reg, aid, CFG, 0.0)
    for i in range(6):
        state = ladder.add(state, ids[f"w{i}"], f"w{i}", "targeted", 1.0 + i)
        _play(reg, ids[f"w{i}"], aid, eid, WEAK)
    state, acts = _step(reg, state, 10.0)
    assert state["bold_pending"] and [a.design for a in acts if a.kind == "design"][:2] == ["bold", "bold"]
    state = ladder.add(state, ids["champ"] if False else ids["w0"], "w0", "targeted", 11.0)  # idempotent: already on the ladder
    assert state["bold_pending"]


def test_champion_gets_control_games_as_challengers_play(tmp_path):
    reg, aid, eid, ids = _registry(tmp_path, ["champ", "a", "b"])
    _play(reg, ids["champ"], aid, eid, [(70, True)] * 8)
    state = ladder.new_state(reg, aid, CFG, 0.0)
    for name in ("a", "b"):
        state = ladder.add(state, ids[name], name, "targeted", 1.0)
        _play(reg, ids[name], aid, eid, [(70, True)] * 4)
    state, acts = _step(reg, state, 2.0)
    assert ("enqueue", ids["champ"], 1) in [(a.kind, a.policy_id, a.n) for a in acts]  # 8 challenger games -> 1 control game


def test_status_page_is_plain_spanish(tmp_path):
    reg, aid, eid, ids = _registry(tmp_path, ["champ", "a"])
    _play(reg, ids["champ"], aid, eid, [(70, True)] * 8)
    state = ladder.add(ladder.new_state(reg, aid, CFG, 0.0), ids["a"], "a", "bold", 1.0)
    page = ladder.report_es(state, CFG, 2.0)
    assert "## Campeón" in page and "idea valiente" in page and "70,0" in page
    assert "| a | bold |" in ladder.history_md(state, reg)


def test_continuous_scheduler_runs_the_highest_priority_job_queued_meanwhile(tmp_path, monkeypatch):
    import asyncio
    import json

    from careerlab import scheduler as sched_mod
    from careerlab.config import Settings

    settings = Settings(data_dir=tmp_path / "data", lab_dir=tmp_path / "lab")
    reg = Registry(settings.registry_path)
    aid = reg.register_actor("claude-cli", {"model": "haiku"})
    eid = reg.register_environment({"environment": "test"})
    bundle = tmp_path / "b"
    bundle.mkdir()
    (bundle / "SKILL.md").write_text("x")
    pid = reg.register_policy(bundle, "fam", "p", [], "h", "c", "test")
    reg.enqueue(pid, aid, eid, "screen", 2, priority=1.0)
    order, stop = [], tmp_path / "STOP"

    async def fake_episode(settings_, cfg, bundle_dir, job_id, run_dir):
        order.append(job_id)
        if len(order) == 1:  # a better job arrives while the first game is running
            reg.enqueue(pid, aid, eid, "ladder", 1, priority=50.0)
        await asyncio.sleep(0.01)
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "result.json").write_text(json.dumps({"job_id": job_id, "outcome": "completed", "quantitative_score": 60.0,
                                                          "survival_months": 48, "ending_score": {"completed": True, "dimensions": []}}))
        if len(order) == 3:
            stop.touch()

    monkeypatch.setattr(sched_mod, "run_claude_episode", fake_episode)
    s = sched_mod.Scheduler(settings, reg)
    counts = asyncio.run(s.run_claude_continuous(1, stop, poll_s=0.01))
    assert counts == {"completed": 3}
    assert order[1].startswith("ladd-")  # leased before the older, lower-priority screen job


def test_weekly_pace_knots_front_load_the_week():
    knots = {"knots": [[0, 0.10], [100, 0.45], [400, 0.90]]}
    assert weekly_allowance(-5, 1e9, knots) == 0.10
    assert abs(weekly_allowance(50, 1e9, knots) - 0.275) < 1e-9
    assert weekly_allowance(500, 1e9, knots) == 0.90
