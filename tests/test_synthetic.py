"""SynthCareer: ground-truth properties (A, B, C), determinism, fast/MCP equivalence, MCP server."""

from __future__ import annotations

import json
import os
import random
import statistics as st
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from careerlab.mcp_client import fingerprint, is_terminal, phase
from careerlab.synthetic import game as g
from careerlab.synthetic.game import (DEFAULT_CONFIG, Engine, SynthConfig, SynthGame, fast_episode, throughput, truth)
from careerlab.synthetic.policy import (ACTORS, DESIGNED, FAMILIES, THETA_SPACE, PolicyActor, classify_option, complexity,
                                        crossover, feedback_codes, make_agent, mutate, normalize, random_theta,
                                        view_from_obs)

REPO = Path(__file__).resolve().parents[1]
OFFICIAL_TOOLS = {"new_game", "observe", "take_action", "check_latest_logs", "show_employee_handbook"}


def _paired(a: list[float], b: list[float]) -> tuple[float, float]:
    """Mean of a - b and its z statistic (seeds are shared, so the comparison is paired)."""
    d = [x - y for x, y in zip(a, b)]
    se = st.stdev(d) / len(d) ** 0.5
    return st.mean(d), st.mean(d) / se


def _q_at(out: g.EpisodeOutcome, month: int) -> float:
    """Score if the run were stopped at ``month`` (an earlier exit keeps its exit score)."""
    for row in out.monthly:
        if row["month"] == month:
            return row["q"]
    return out.Q


def _play_mcp(theta: dict, actor: str, seed: int, cfg: SynthConfig = DEFAULT_CONFIG) -> tuple[SynthGame, list[str]]:
    """Drive SynthGame through observe/take_action only, checking that the policy's view equals the engine's."""
    game = SynthGame(seed, cfg)
    agent = make_agent(theta, actor, seed)
    modes: list[str] = []
    while True:
        obs = game.observe()
        json.dumps(obs)  # JSON-serialisable, like the MCP payload
        view = view_from_obs(obs)
        assert view.key() == game.engine.view.key()
        if is_terminal(obs):
            return game, modes
        game.take_action(agent.choose(view), notes="test")
        if len(game.engine.history) > len(modes):
            modes.append(agent.policy.mode)


# ---------------------------------------------------------------------------
# (4) determinism and fast/MCP equivalence
# ---------------------------------------------------------------------------

def test_fast_episode_is_deterministic_and_seed_dependent():
    theta = DESIGNED["state_switch"]
    a = fast_episode(theta, "cheap_biased", 123)
    b = fast_episode(theta, "cheap_biased", 123)
    assert asdict(a) == asdict(b)
    others = [fast_episode(theta, "cheap_biased", s) for s in range(124, 130)]
    assert any(o.monthly != a.monthly for o in others)
    assert len(a.monthly) == a.T and a.tokens_proxy == a.steps * g.TOKENS_PER_STEP


@pytest.mark.parametrize("name", sorted(DESIGNED))
@pytest.mark.parametrize("actor", ["exact", "target", "cheap_capability", "cheap_biased", "eager"])
def test_fast_and_mcp_paths_agree_exactly(name, actor):
    theta = DESIGNED[name]
    for seed in (0, 1, 2):
        game, modes = _play_mcp(theta, actor, seed)
        slow = game.outcome()
        fast = fast_episode(theta, actor, seed)
        assert (fast.Q, fast.T, fast.completed, fast.failure_reason, fast.steps, fast.rejected) == \
               (slow.Q, slow.T, slow.completed, slow.failure_reason, slow.steps, slow.rejected)
        assert [{k: v for k, v in r.items() if k != "mode"} for r in fast.monthly] == \
               [{k: v for k, v in r.items() if k != "mode"} for r in slow.monthly]
        modes += [modes[-1]] * (len(fast.monthly) - len(modes))
        assert [r["mode"] for r in fast.monthly] == modes
        assert game.observe()["ending_score"]["quantitative_score"] == fast.Q


def test_random_families_agree_on_both_paths():
    rng = random.Random(3)
    for family in FAMILIES:
        theta = random_theta(rng, family)
        game, _ = _play_mcp(theta, "target", 77)
        assert game.outcome().Q == fast_episode(theta, "target", 77).Q


def test_common_random_numbers_across_policies():
    """Same seed, same start and same first month of events whatever the policy."""
    e1, e2 = Engine(5), Engine(5)
    assert (e1.health, e1.skill, e1.apt, e1.events) == (e2.health, e2.skill, e2.apt, e2.events)
    a = fast_episode(DESIGNED["no_invest"], "exact", 5)
    b = fast_episode(DESIGNED["early_invest"], "exact", 5)
    assert a.monthly[0]["month"] == b.monthly[0]["month"] == 1


# ---------------------------------------------------------------------------
# Observation schema and interface behaviour
# ---------------------------------------------------------------------------

def test_observation_schema_and_phases():
    game = SynthGame(11)
    seen: set[str] = set()
    steps = 0
    while not game.done:
        obs = game.observe()
        state = obs["current_state"]
        assert set(state) == {"time", "status", "simulation_flags", "session_id"}
        assert set(state["status"]) == {"health", "dignity", "skill", "network", "level", "duration_in_level",
                                        "output", "wealth", "energy"}
        assert 0 <= state["status"]["health"] <= 10 and 0 <= state["status"]["dignity"] <= 10
        assert len(state["session_id"]) == 32 and int(state["session_id"], 16) >= 0
        ph = phase(obs)
        seen.add(ph)
        if ph == "energy":
            ev = obs["current_event"]
            assert ev["energy_budget"] == 3 and "rules" in ev
            assert all("energy_cost" in c and "status_updates" in c for c in obs["choices"])
            dear = [c for c in obs["choices"] if c["energy_cost"] > ev["remaining_energy"]]
            if dear:  # unaffordable: rejected without advancing
                before = fingerprint(obs)
                reply = game.take_action(dear[0]["choice"], "too expensive")
                assert reply["success"] is False and "Insufficient energy" in reply["error"]
                assert fingerprint(game.observe()) == before
        elif ph == "main_action":
            assert obs["current_event"]["max_selections"] == 1
        reply = game.take_action(obs["choices"][-1]["choice"] if ph == "energy" else 1, "")
        assert reply == {"success": True, "error": None}
        steps += 1
    end = game.observe()
    assert {"event", "energy", "main_action"} <= seen
    score = end["ending_score"]
    assert set(score) == {"outcome", "survival_months", "completed", "quantitative_score",
                          "competition_partial_score", "dimensions"}
    assert [d["name"] for d in score["dimensions"]] == [n for n, _ in g.DIMENSIONS]
    assert abs(sum(d["weighted_score"] for d in score["dimensions"]) - score["quantitative_score"]) < 0.01
    assert score["competition_partial_score"] == round(score["quantitative_score"] * 0.7, 2)
    assert game.take_action(1, "")["success"] is False
    assert game.take_action(99, "")["success"] is False
    assert len(game.logs(5)["entries"]) == 5 and "SynthCareer" in game.handbook()


def test_story_option_texts_and_feedback_round_trip():
    for et in g.EVENT_TYPES:
        for style, text, _ in et.options:
            assert classify_option(text) == style, text
    for code, text in g.FIXED_TEXTS.items():
        assert feedback_codes(text) == [code]
    assert feedback_codes("\n".join(g.WARN_TEXTS + g.NOISE_TEXTS)) == [g.F_WARN] * 3 + [g.F_NOISE] * 3
    lines = [g.feedback_text(g.F_SALARY, (300, 250, 1)), g.feedback_text(g.F_GRADE_CODES[2], "B"),
             g.feedback_text(g.F_BONUS, 75), g.feedback_text(g.F_PROMOTED, "L2"),
             g.feedback_text(g.F_FAILED, "risk_incident")]
    assert feedback_codes("\n".join(lines)) == [g.F_SALARY, g.F_GRADE_CODES[2], g.F_BONUS, g.F_PROMOTED, g.F_FAILED]


def test_failures_and_survivorship_are_real():
    reasons = {fast_episode(DESIGNED[n], "target", s, record=False).failure_reason
               for n in ("no_invest", "calendar8", "overcommit", "steady_networker") for s in range(300)}
    assert {"out_of_depth", "risk_incident", "health_depleted", "insolvency", "skill_gap"} <= reasons


# ---------------------------------------------------------------------------
# (1) Problem B: late benefits
# ---------------------------------------------------------------------------

def test_B_early_investment_looks_worse_at_month_12_but_wins_at_48():
    seeds = range(600)
    inv = [fast_episode(DESIGNED["early_invest"], "target", s) for s in seeds]
    non = [fast_episode(DESIGNED["no_invest"], "target", s) for s in seeds]
    for month in (6, 12):
        diff, z = _paired([_q_at(o, month) for o in non], [_q_at(o, month) for o in inv])
        print(f"B: month {month} provisional Q, non-investor minus investor = {diff:.2f} (z={z:.1f})")
        assert diff > 0.5 and z > 4
    grade_points = {"S": 4, "A": 3, "B": 2, "C": 1, "D": 0}
    first = lambda outs: st.mean(grade_points[o.reviews[0]] for o in outs if o.reviews)  # noqa: E731
    assert first(inv) < first(non) - 1.0
    diff, z = _paired([o.Q for o in inv], [o.Q for o in non])
    print(f"B: month 48 Q, investor minus non-investor = {diff:.2f} (z={z:.1f})")
    assert diff > 10 and z > 10


# ---------------------------------------------------------------------------
# (2) Problem C: deceptive specialization
# ---------------------------------------------------------------------------

def test_C_state_switch_beats_calendar_but_survivor_data_flatter_the_calendar():
    seeds = range(2000)
    state = [fast_episode(DESIGNED["state_switch"], "target", s, record=False) for s in seeds]
    cal = [fast_episode(DESIGNED["calendar8"], "target", s, record=False) for s in seeds]
    diff, z = _paired([o.Q for o in state], [o.Q for o in cal])
    print(f"C: fresh games, state minus calendar Q = {diff:.2f} (z={z:.1f})")
    assert diff > 1.5 and z > 5
    y_diff, _ = _paired([o.Y for o in state], [o.Y for o in cal])
    assert y_diff > 1.5
    surv_state = st.mean(o.Q for o in state if o.completed)
    surv_cal = st.mean(o.Q for o in cal if o.completed)
    print(f"C: survivors only, calendar {surv_cal:.2f} vs state {surv_state:.2f}; completion "
          f"{st.mean(o.completed for o in cal):.2f} vs {st.mean(o.completed for o in state):.2f}")
    assert surv_cal >= surv_state
    assert st.mean(o.completed for o in cal) < st.mean(o.completed for o in state) - 0.1
    # Same story conditioning on the seeds where the calendar run survived (paired comparison).
    kept = [i for i, o in enumerate(cal) if o.completed]
    assert st.mean(cal[i].Q for i in kept) >= st.mean(state[i].Q for i in kept)


def test_C_calendar_mistiming_depends_on_latent_readiness():
    """The calendar rule is fine for fast learners and fatal for slow ones; the state rule adapts."""
    seeds = range(1500)
    apt = [Engine(s, record=False).apt for s in seeds]
    state = [fast_episode(DESIGNED["state_switch"], "target", s, record=False) for s in seeds]
    cal = [fast_episode(DESIGNED["calendar8"], "target", s, record=False) for s in seeds]
    slow = [i for i in range(len(apt)) if apt[i] == min(DEFAULT_CONFIG.aptitude_values)]
    fast = [i for i in range(len(apt)) if apt[i] == max(DEFAULT_CONFIG.aptitude_values)]
    assert st.mean(cal[i].completed for i in slow) < st.mean(state[i].completed for i in slow) - 0.25
    assert st.mean(cal[i].Q for i in fast) >= st.mean(state[i].Q for i in fast) - 0.5


# ---------------------------------------------------------------------------
# (3) Problem A: actor models
# ---------------------------------------------------------------------------

def test_A_cheap_biased_actor_reverses_a_designed_ranking():
    seeds = range(1000)
    def q(name: str, actor: str) -> list[float]:
        return [fast_episode(DESIGNED[name], actor, s, record=False).Q for s in seeds]
    diff_t, z_t = _paired(q("steady_networker", "target"), q("overcommit", "target"))
    diff_b, z_b = _paired(q("steady_networker", "cheap_biased"), q("overcommit", "cheap_biased"))
    print(f"A: steady minus overcommit, target {diff_t:.2f} (z={z_t:.1f}); cheap_biased {diff_b:.2f} (z={z_b:.1f})")
    assert diff_t > 1.5 and z_t > 4
    assert diff_b < -1.5 and z_b < -4


def test_actor_errors_grow_with_complexity():
    cap = ACTORS["cheap_capability"]
    assert cap.miss(1) < cap.miss(4) < cap.miss(7)
    assert ACTORS["exact"].miss(8) == 0.0 and ACTORS["target"].miss(8) < cap.miss(1)
    simple, complex_ = DESIGNED["steady_networker"], DESIGNED["overcommit"]
    assert complexity(simple) < complexity(complex_)
    seeds = range(600)
    loss = {n: st.mean(fast_episode(t, "target", s, record=False).Q - fast_episode(t, "cheap_capability", s, record=False).Q
                       for s in seeds) for n, t in (("simple", simple), ("complex", complex_))}
    assert loss["complex"] > loss["simple"] + 2.0


# ---------------------------------------------------------------------------
# Parameter space
# ---------------------------------------------------------------------------

def test_theta_space_operations():
    rng = random.Random(0)
    assert len([f for f in FAMILIES if f != "random"]) >= 5
    for family, spec in FAMILIES.items():
        for _ in range(20):
            t = random_theta(rng, family)
            assert t == normalize(t) and set(t) == set(THETA_SPACE)
            for k, v in spec.items():
                if isinstance(v, tuple):
                    assert v[0] <= t[k] <= v[1]
                elif isinstance(v, list):
                    assert t[k] in v
                else:
                    assert t[k] == v
    a, b = random_theta(rng, "state"), random_theta(rng, "grinder")
    for _ in range(20):
        m = mutate(a, rng, 0.2)
        assert m != a and m == normalize(m)
        c = crossover(a, b, rng)
        assert all(c[k] in (a[k], b[k]) for k in THETA_SPACE)
    assert complexity(normalize({"health_floor": 0, "dignity_floor": 0, "overtime_rule": "never",
                                 "risk_reaction": "ignore", "wealth_floor": -1, "assert_dignity": 0,
                                 "switch_rule": "none"})) == 0
    with pytest.raises(ValueError):
        normalize({"no_such_knob": 1})
    import numpy as np
    assert random_theta(np.random.default_rng(1), "calendar")["switch_rule"] == "calendar"


def test_truth_and_throughput():
    theta = DESIGNED["state_switch"]
    t = truth(theta, "exact", n=300, seed=2)
    assert 0 < t.mean_q < 100 and 0 < t.mean_y < 90
    q, y = truth(theta, "exact", n=300, seed=2)
    assert (q, y) == t
    eps = throughput(theta, "target", n=1000)
    print(f"fast path: {eps:.0f} episodes/s single core (record=False)")
    assert eps > 500


def test_short_games_via_config():
    cfg = replace(DEFAULT_CONFIG, months=6)
    out = fast_episode(DESIGNED["state_switch"], "target", 4, cfg)
    assert out.T <= 6 and (out.completed or out.failure_reason)
    assert SynthConfig.from_dict(json.loads(json.dumps(cfg.to_dict()))) == cfg


# ---------------------------------------------------------------------------
# MCP server over stdio
# ---------------------------------------------------------------------------

def _server_env(**extra: str) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO) + os.pathsep + env.get("PYTHONPATH", "")
    env["FASTMCP_LOG_LEVEL"] = "WARNING"
    env.update(extra)
    return env


async def test_stdio_server_exposes_official_tools_and_matches_fast_path(tmp_path):
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport

    theta, seed_base = DESIGNED["state_switch"], 7
    transport = StdioTransport(command=sys.executable, args=["-m", "careerlab.synthetic.server", "--months", "4"],
                               env=_server_env(CAREERLAB_SYNTH_SEED_BASE=str(seed_base)), cwd=str(REPO),
                               log_file=tmp_path / "server.log")
    async with Client(transport, timeout=30) as client:
        tools = {t.name for t in await client.list_tools()}
        assert tools == OFFICIAL_TOOLS
        handbook = (await client.call_tool("show_employee_handbook", {})).data
        assert "SynthCareer" in (handbook if isinstance(handbook, str) else handbook["result"])
        sid = (await client.call_tool("new_game", {})).data["session_id"]
        bad = (await client.call_tool("observe", {"session_id": "0" * 32})).data
        assert "error" in bad["current_state"]
        actor = PolicyActor(theta, "target", seed=seed_base)
        steps = 0
        while True:
            obs = (await client.call_tool("observe", {"session_id": sid})).data
            if is_terminal(obs):
                break
            decision = await actor.decide(obs, {})
            reply = (await client.call_tool("take_action", {"session_id": sid, "choice": decision.choice,
                                                            "notes": decision.notes})).data
            assert reply["success"] is True
            steps += 1
        logs = (await client.call_tool("check_latest_logs", {"session_id": sid, "count": 3})).data
        assert len(logs["entries"]) == 3
    fast = fast_episode(theta, "target", seed_base, replace(DEFAULT_CONFIG, months=4))
    assert obs["ending_score"]["quantitative_score"] == fast.Q
    assert obs["ending_score"]["survival_months"] == fast.T and steps == fast.steps


async def test_stdio_server_is_a_drop_in_for_the_lab_runner(tmp_path):
    """The lab's own GameClient + run_driven_episode play SynthCareer unchanged."""
    from careerlab.config import Settings
    from careerlab.episode import run_driven_episode
    from careerlab.mcp_client import GameClient, ServerSpec

    from careerlab.synthetic.server import write_launcher

    wrapper = write_launcher(tmp_path / "synth mcp")  # a space, like the iCloud repository path
    settings = Settings(data_dir=tmp_path / "data", lab_dir=tmp_path / "lab", runner_dir=tmp_path / "runner",
                        mcp_executable=str(wrapper), claude_executable="claude")
    spec = ServerSpec("synth", tmp_path / "srv", extra_env={
        "CAREERLAB_SYNTH_SEED_BASE": "21", "CAREERLAB_SYNTH_CONFIG": json.dumps({"months": 6}),
        "PYTHONPATH": str(REPO)})
    theta = DESIGNED["calendar8"]
    async with GameClient(spec, settings, call_timeout_s=30) as client:
        result = await run_driven_episode(client, PolicyActor(theta, "cheap_biased", seed=21), "synth-job", tmp_path / "run")
    fast = fast_episode(theta, "cheap_biased", 21, replace(DEFAULT_CONFIG, months=6))
    assert result.outcome == fast.outcome and result.quantitative_score == fast.Q
    assert result.survival_months == fast.T and result.steps == fast.steps


def test_sessions_persist_and_replay_across_server_processes(tmp_path):
    """Two stores on one root behave like two server processes on one CAREER_EMULATOR_DB."""
    from careerlab.synthetic.server import SessionStore

    cfg, theta = replace(DEFAULT_CONFIG, months=5), DESIGNED["state_switch"]
    a = SessionStore(seed_base=3, config=cfg, competition=True, state_dir=tmp_path)
    sid = a.new_game()["session_id"]
    assert "error" in a.new_game()
    b = SessionStore(state_dir=tmp_path)  # default config: the session header decides, not the process
    assert a.take_action(sid, 99, "invalid")["success"] is False
    agent, stores, steps = make_agent(theta, "target", 3), (a, b), 0
    while True:  # writers alternate; each store must see the other's calls
        mine, other = stores[steps % 2], stores[(steps + 1) % 2]
        obs = mine.get(sid).observe()
        assert fingerprint(obs) == fingerprint(other.get(sid).observe())
        if is_terminal(obs):
            break
        assert mine.take_action(sid, agent.choose(view_from_obs(obs)), f"step {steps}")["success"] is True
        steps += 1
    fast = fast_episode(theta, "target", 3, cfg)
    assert obs["ending_score"]["quantitative_score"] == fast.Q and steps == fast.steps
    c = SessionStore(state_dir=tmp_path)
    assert c.get(sid).logs(1000) == a.get(sid).logs(1000) and len(c.get(sid).logs(1000)["entries"]) == steps + 1
    assert c.get("../" + sid) is None and c.get("0" * 32) is None
    assert c.take_action("0" * 32, 1) is None and not (tmp_path / f"{'0' * 32}.jsonl").exists()
    d = SessionStore(seed_base=3, config=cfg, state_dir=tmp_path)  # the k-th game of a root plays seed base + k
    sid2 = d.new_game()["session_id"]
    assert sid2 != sid and d.get(sid2).seed == 4 and SessionStore(state_dir=tmp_path).get(sid2).seed == 4


async def test_claude_worker_flow_survives_a_second_server_process(tmp_path):
    """run_claude_episode's pattern: a worker server with the scrubbed env of mcp_config, then a verifier process."""
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport

    from careerlab.actors.claude_cli import GAME_SERVER, mcp_config
    from careerlab.config import Settings
    from careerlab.mcp_client import GameClient, ServerSpec
    from careerlab.synthetic.server import prepare_root, write_launcher

    settings = Settings(data_dir=tmp_path / "data", lab_dir=tmp_path / "lab", runner_dir=tmp_path / "runner",
                        mcp_executable=str(write_launcher(tmp_path / "synth-mcp")), claude_executable="claude")
    root, seed, theta = tmp_path / "game", 11, DESIGNED["feedback_switch"]
    prepare_root(root, seed_base=seed, config={"months": 3})
    server = mcp_config(settings, ServerSpec("claude-j", root, competition_mode=True))["mcpServers"][GAME_SERVER]
    assert not any(k.startswith("CAREERLAB_SYNTH") for k in server["env"])  # only the root carries the config
    actor, steps = PolicyActor(theta, "target", seed=seed), 0
    transport = StdioTransport(command=server["command"], args=server["args"], env=server["env"],
                               log_file=tmp_path / "worker.log")
    async with Client(transport, timeout=30) as worker:
        sid = (await worker.call_tool("new_game", {})).data["session_id"]
        assert "error" in (await worker.call_tool("new_game", {})).data  # competition mode
        for _ in range(4):
            obs = (await worker.call_tool("observe", {"session_id": sid})).data
            decision = await actor.decide(obs, {})
            await worker.call_tool("take_action", {"session_id": sid, "choice": decision.choice, "notes": decision.notes})
            steps += 1
        last = (await worker.call_tool("observe", {"session_id": sid})).data
    async with GameClient(ServerSpec("verify-j", root), settings, call_timeout_s=30) as client:  # as claude_cli does
        obs = await client.observe(sid)
        assert fingerprint(obs) == fingerprint(last)
        while not is_terminal(obs):
            decision = await actor.decide(obs, {})
            assert (await client.take_action(sid, decision.choice, decision.notes, before=obs)).applied
            steps += 1
            obs = await client.observe(sid)
        assert len((await client.logs(sid, 1000))["entries"]) == steps
    fast = fast_episode(theta, "target", seed, replace(DEFAULT_CONFIG, months=3))
    assert obs["ending_score"]["quantitative_score"] == fast.Q
    assert obs["ending_score"]["survival_months"] == fast.T and steps == fast.steps
    assert not (root / "career_emulator.sqlite3").exists()  # the official database path is never touched
