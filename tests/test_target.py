"""careerlab.target and the official-runner fixes, with mocks only: no network, no runner, no game, no spend."""

import asyncio
import io
import json
import os
import subprocess
import sys
import time
import urllib.error
from dataclasses import asdict
from pathlib import Path

import pytest

import careerlab.target as target
from careerlab.actors import official_runner as runner
from careerlab.config import Settings, check_origin
from careerlab.episode import EpisodeResult, atomic_write_json
from careerlab.store import Registry, bundle_hash

SECRET = "sk-or-v1-test-0123456789abcdef0123"
SKILL = "---\nname: steady\ndescription: Keep a steady balance across the whole career.\n---\n\nPlay steadily and note why.\n"
TARGET_ENV = {"environment": "real-dev", "runner": "test"}


def _bundle(root: Path, text: str = SKILL) -> Path:
    (root / "skills" / "steady").mkdir(parents=True)
    (root / "skills" / "steady" / "SKILL.md").write_text(text)
    (root / "manifest.json").write_text(json.dumps({"team": "Gradient Depression", "name": "t", "mode": "agent", "instruction": ""}))
    return root


def _policy(lab_dir: Path, name: str, parents: list[str], text: str = SKILL) -> Path:
    folder = lab_dir / "policies-src" / "fam" / name
    _bundle(folder / "bundle", text)
    (folder / "policy.json").write_text(json.dumps({"family": "fam", "name": name, "parents": parents,
                                                    "hypothesis": "h", "change": "c"}))
    return folder


@pytest.fixture
def lab(tmp_path, monkeypatch):
    lab_dir = tmp_path / "lab"
    lab_dir.mkdir()
    (lab_dir / "gate.json").write_text(json.dumps({"environments": {"real-dev": {"actors": {
        "jiuwenswarm-target": {"allowed": True, "routes": {"competition-key": {}}}}}}}))
    (tmp_path / "runner" / "career_sim_runner").mkdir(parents=True)
    env = tmp_path / "competition.env"
    env.write_text(f"API_BASE=https://openrouter.test/api/v1\nAPI_KEY={SECRET}\nMODEL_NAME=deepseek-v4-flash\n")
    settings = Settings(origin="deepseek", data_dir=tmp_path / "data", lab_dir=lab_dir, runner_dir=tmp_path / "runner").ensure()
    reg = Registry(settings.registry_path, origin="deepseek")
    pid = reg.register_policy(_bundle(lab_dir / "policies-src" / "fam" / "p-v1" / "bundle"), "fam", "p-v1", [], "h", "c", "test")
    monkeypatch.delenv("CAREERLAB_TARGET_ENV", raising=False)
    return settings, reg, pid, env


class FakeKey:
    """Key status returning the given usages in turn (the last one repeats)."""

    def __init__(self, *usages, limit=50.0):
        self.usages, self.limit, self.calls = list(usages), limit, 0

    def __call__(self, env_path, timeout_s=20.0):
        usage = self.usages[min(self.calls, len(self.usages) - 1)]
        self.calls += 1
        return {"usage": usage, "limit": self.limit, "limit_remaining": None if self.limit is None else self.limit - usage,
                "api_base": "https://openrouter.test/api/v1", "model_name": "deepseek-v4-flash"}


@pytest.fixture
def offline(lab, tmp_path, monkeypatch):
    """Slot preparation, dataset reload and runner checks replaced by fakes."""
    settings, reg, pid, env = lab
    slot = tmp_path / "slot"
    (slot / "runner").mkdir(parents=True)
    (slot / "home").mkdir()
    calls = {"prepare": 0, "reload": 0, "episodes": []}

    def fake_prepare(s, n):
        assert os.environ["CAREERLAB_TARGET_ENV"] == str(env)  # the slot gets the chosen key file
        calls["prepare"] += 1
        return slot

    def fake_reload(repo, home, log):
        calls["reload"] += 1
        log.write_text("reloaded")
        return 0

    monkeypatch.setattr(runner, "prepare_slot", fake_prepare)
    monkeypatch.setattr(runner, "reload_dev_dataset", fake_reload)
    monkeypatch.setattr(target, "check_slot", lambda root, solution: {
        "submission": {"ok": True, "checks": []}, "failures": [],
        "environment": {"ok": False, "checks": [{"name": "backend-reachable", "ok": False, "detail": "not running"}]}})
    monkeypatch.setattr(target, "target_environment", lambda root: dict(TARGET_ENV))
    return settings, reg, pid, env, calls


def fake_episode(calls, outcome="completed", score=61.5, tokens=123456, sleep_s=0.0, crash=None):
    async def run(settings, cfg, solution, job_id, run_dir, slot):
        calls["episodes"].append(job_id)
        assert (Path(solution) / "skills" / "steady" / "SKILL.md").read_text() == SKILL
        await asyncio.sleep(sleep_s)
        if crash:
            raise crash
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "play.log").write_text(f"oops {SECRET}\n")  # must be scrubbed afterwards
        played = outcome != "interrupted"
        result = EpisodeResult(job_id, "a" * 32, outcome, survival_months=48 if played else None,
                               quantitative_score=score if played else None,
                               ending_score={"completed": outcome == "completed", "quantitative_score": score, "dimensions": []} if played else None,
                               interruption=None if played else "boom",
                               actor_usage={"tokens": {"total_tokens": tokens}, "total_tokens": tokens})
        atomic_write_json(run_dir / "result.json", asdict(result))
        return result
    return run


def _decisions(reg):
    return [(r[0], json.loads(r[1])) for r in reg.db.execute("SELECT kind, payload FROM decisions ORDER BY decision_id")]


FAST = {"poll_s": 5.0, "settle_s": 0.001, "settle_max_s": 0.01}


# -- key status ------------------------------------------------------------------------------------------------

class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def test_key_status_reads_usage_and_never_returns_the_key(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text(f'export API_BASE="https://openrouter.test/api/v1/"\nAPI_KEY=\'{SECRET}\'\n# comment\n'
                   "MODEL_NAME=deepseek-v4-flash # designated model\n")
    seen = {}

    def fake_urlopen(request, timeout):
        seen.update(url=request.full_url, auth=request.get_header("Authorization"))
        return FakeResponse(json.dumps({"data": {"label": SECRET[:12] + "...", "usage": 1.25, "limit": 50,
                                                 "limit_remaining": 48.75}}).encode())

    monkeypatch.setattr(target.urllib.request, "urlopen", fake_urlopen)
    status = target.key_status(env)
    assert status == {"usage": 1.25, "limit": 50.0, "limit_remaining": 48.75,
                      "api_base": "https://openrouter.test/api/v1", "model_name": "deepseek-v4-flash"}
    assert seen == {"url": "https://openrouter.test/api/v1/key", "auth": f"Bearer {SECRET}"}
    assert SECRET[:12] not in json.dumps(status)  # not even OpenRouter's truncated label


def test_key_status_derives_remaining_credit(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text(f"API_BASE=https://openrouter.test/api/v1\nAPI_KEY={SECRET}\n")
    replies = iter([{"data": {"usage": 2.0, "limit": 50}}, {"data": {"usage": 2.0, "limit": None}}])
    monkeypatch.setattr(target.urllib.request, "urlopen", lambda request, timeout: FakeResponse(json.dumps(next(replies)).encode()))
    assert target.key_status(env)["limit_remaining"] == 48.0
    assert target.key_status(env)["limit_remaining"] is None


def test_key_status_errors_never_contain_the_key(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text(f"API_BASE=https://openrouter.test/api/v1\nAPI_KEY={SECRET}\n")

    def denied(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 401, f"bad key {SECRET}", {}, None)

    monkeypatch.setattr(target.urllib.request, "urlopen", denied)
    with pytest.raises(target.KeyStatusError) as err:
        target.key_status(env)
    assert "401" in str(err.value) and SECRET not in str(err.value) and err.value.__suppress_context__

    def unreachable(request, timeout):
        raise urllib.error.URLError(f"no route while sending {SECRET}")

    monkeypatch.setattr(target.urllib.request, "urlopen", unreachable)
    with pytest.raises(target.KeyStatusError) as err:
        target.key_status(env)
    assert SECRET not in str(err.value) and "<redacted>" in str(err.value)

    env.write_text(f"API_BASE=http://openrouter.test/api/v1\nAPI_KEY={SECRET}\n")
    with pytest.raises(target.KeyStatusError, match="https"):
        target.key_status(env)
    env.write_text("API_BASE=https://openrouter.test/api/v1\n")
    with pytest.raises(target.KeyStatusError, match="lacks"):
        target.key_status(env)


# -- policies and solutions ------------------------------------------------------------------------------------

def test_build_solution_copies_the_registered_bundle_byte_for_byte(lab):
    settings, reg, pid, env = lab
    bundle = Path(reg.db.execute("SELECT bundle_path FROM policies WHERE policy_id=?", (pid,)).fetchone()[0])
    (bundle / "skills" / "steady" / ".DS_Store").write_bytes(b"finder")  # not part of the hashed bundle
    out = settings.data_dir / "work"
    (out / "solution").mkdir(parents=True)
    (out / "solution" / "stale.txt").write_text("from an older build")
    solution = target.build_solution(settings, reg, pid, out)
    assert solution == out / "solution"
    files = sorted(str(p.relative_to(solution)) for p in solution.rglob("*") if p.is_file())
    assert files == sorted(["manifest.json", "skills/steady/SKILL.md", *target.PLAY_REQUIRED])
    for rel in ("manifest.json", "skills/steady/SKILL.md"):
        assert (solution / rel).read_bytes() == (bundle / rel).read_bytes()
    for rel in target.PLAY_REQUIRED:
        assert (solution / rel).read_text().startswith("# NOT FOR SUBMISSION")
    assert len(target.solution_sha256(solution)) == 64


def test_build_solution_refuses_changed_or_non_skill_bundles(lab, tmp_path):
    settings, reg, pid, env = lab
    bundle = Path(reg.db.execute("SELECT bundle_path FROM policies WHERE policy_id=?", (pid,)).fetchone()[0])
    scripted = tmp_path / "scripted"
    scripted.mkdir()
    (scripted / "scripted.json").write_text('{"rule_set": "first"}')
    sid = reg.register_policy(scripted, "scripted", "s", [], "h", "c", "test")
    with pytest.raises(ValueError, match="not a Skills bundle"):
        target.build_solution(settings, reg, sid, tmp_path / "w")
    (bundle / "skills" / "steady" / "SKILL.md").write_text(SKILL + "changed\n")
    with pytest.raises(ValueError, match="changed since registration"):
        target.build_solution(settings, reg, pid, tmp_path / "w")


def test_build_solution_finds_a_bundle_registered_from_another_checkout(lab, tmp_path):
    settings, reg, pid, env = lab
    reg.db.execute("UPDATE policies SET bundle_path=? WHERE policy_id=?",
                   ("/old/checkout/lab/policies-src/fam/p-v1/bundle", pid))
    assert (target.build_solution(settings, reg, pid, tmp_path / "w") / "manifest.json").is_file()


def test_register_policy_folder_registers_missing_ancestors_first(lab):
    settings, reg, pid, env = lab
    a = _policy(settings.lab_dir, "a-v1", [], SKILL + "Variant A.\n")
    _policy(settings.lab_dir, "b-v1", ["a-v1"], SKILL + "Variant B.\n")
    a_id = bundle_hash(a / "bundle")[:16]
    c = _policy(settings.lab_dir, "c-v1", ["b-v1", a_id], SKILL + "Variant C.\n")
    c_id = target.register_policy_folder(settings, reg, c)
    ids = {r[0]: r[1] for r in reg.db.execute("SELECT name, policy_id FROM policies")}
    parents = {r[0]: json.loads(r[1]) for r in reg.db.execute("SELECT name, parents FROM policies")}
    assert c_id == ids["c-v1"] == bundle_hash(c / "bundle")[:16] and ids["a-v1"] == a_id
    assert parents["c-v1"] == [ids["b-v1"], a_id] and parents["b-v1"] == [a_id] and parents["a-v1"] == []


def test_register_policy_folder_resolves_parents_named_by_id_and_refuses_unknown_ones(lab):
    settings, reg, pid, env = lab
    x = _policy(settings.lab_dir, "x-v1", [], SKILL + "Variant X.\n")
    x_id = bundle_hash(x / "bundle")[:16]
    y = _policy(settings.lab_dir, "y-v1", [x_id], SKILL + "Variant Y.\n")
    target.register_policy_folder(settings, reg, y)
    assert reg.db.execute("SELECT name FROM policies WHERE policy_id=?", (x_id,)).fetchone()[0] == "x-v1"
    z = _policy(settings.lab_dir, "z-v1", ["ghost-v9"], SKILL + "Variant Z.\n")
    with pytest.raises(ValueError, match="unknown parent 'ghost-v9'"):
        target.register_policy_folder(settings, reg, z)


def test_register_policy_folder_keeps_the_compliance_gate(lab):
    settings, reg, pid, env = lab
    bad = _policy(settings.lab_dir, "bad-v1", [], SKILL + "永远合作\n")
    with pytest.raises(ValueError, match="compliance errors"):
        target.register_policy_folder(settings, reg, bad)
    assert target.register_policy_folder(settings, reg, bad, allow_lint_errors=True)


# -- play_target ------------------------------------------------------------------------------------------------

def test_target_games_use_their_own_origin(lab, tmp_path):
    settings, reg, pid, env = lab
    assert check_origin("deepseek") == "deepseek"
    race = Registry(tmp_path / "race.sqlite3", origin="")
    with pytest.raises(ValueError, match="CAREERLAB_ORIGIN=deepseek"):
        target.play_target(settings, race, pid, env_path=env)
    env.write_text(f"API_BASE=https://openrouter.test/api/v1\nAPI_KEY={SECRET}\nMODEL_NAME=deepseek/deepseek-v4-pro\n")
    with pytest.raises(ValueError, match="designated"):
        target.play_target(settings, reg, pid, env_path=env)


def test_provider_qualified_model_name_is_accepted(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    env.write_text(f"API_BASE=https://openrouter.test/api/v1\nAPI_KEY={SECRET}\nMODEL_NAME=deepseek/deepseek-v4-flash\n")
    monkeypatch.setattr(target, "key_status", FakeKey(0.0))
    assert target.play_target(settings, reg, pid, dry_run=True, env_path=env, **FAST)[0]["would_start"]


def test_refuses_to_start_without_budget_headroom(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(32.5))  # 17.5 left - 15 reserve = 2.5 < 3 per game
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    out = target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert out[0]["started"] is False and out[0]["budget"]["headroom_usd"] == 2.5
    assert calls == {"prepare": 0, "reload": 0, "episodes": []}
    assert reg.db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0
    assert [k for k, _ in _decisions(reg)] == ["target_refused"]
    monkeypatch.setattr(target, "key_status", FakeKey(0.0, limit=None))  # a key without a limit cannot be guarded
    assert target.play_target(settings, reg, pid, env_path=env, **FAST)[0]["started"] is False


def test_one_game_is_a_job_with_exact_cost_and_a_decision(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(1.0, 1.0, 1.7, 1.85, 1.85))  # booking lags, then settles
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    [game] = target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert game["cost_usd"] == 0.85 and game["cost_settled"] and game["usage_before"] == 1.0
    assert game["outcome"] == "completed" and game["score"] == 61.5 and game["tokens"] == {"total_tokens": 123456}
    assert game["stopped"] is None and game["redacted_files"] == 1 and game["job_id"].startswith("deepseek-pilo-")
    assert calls["episodes"] == [game["job_id"]] and calls["prepare"] == 1 and calls["reload"] == 1
    job = reg.db.execute("SELECT status, actor_id, env_id FROM jobs").fetchone()
    assert job["status"] == "done"
    assert reg.db.execute("SELECT kind FROM actors WHERE actor_id=?", (job["actor_id"],)).fetchone()[0] == "jiuwenswarm-target"
    ev = reg.db.execute("SELECT outcome, score, tokens FROM evaluations").fetchone()
    assert ev["outcome"] == "completed" and ev["score"] == 61.5 and json.loads(ev["tokens"])["key_cost_usd"] == 0.85
    kinds = _decisions(reg)
    assert [k for k, _ in kinds] == ["enqueue", "target_game"] and kinds[1][1]["cost_usd"] == 0.85
    run_dir = Path(game["run_dir"])
    assert SECRET not in (run_dir / "play.log").read_text()
    assert SECRET not in json.dumps(game) and SECRET not in json.dumps(kinds)


def test_series_stops_after_a_game_above_the_cap(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0, 0.0, 3.5, 3.5))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    out = target.play_target(settings, reg, pid, games=3, env_path=env, **FAST)
    assert len(out) == 1 and len(calls["episodes"]) == 1 and "above the USD 3.00 cap" in out[0]["stopped"]


def test_series_continues_while_games_stay_under_the_cap(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    out = target.play_target(settings, reg, pid, games=2, env_path=env, **FAST)
    assert [g["cost_usd"] for g in out] == [0.5, 0.5] and len(set(calls["episodes"])) == 2


def test_series_stops_after_an_interrupted_game(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls, outcome="interrupted"))
    out = target.play_target(settings, reg, pid, games=2, env_path=env, **FAST)
    assert len(out) == 1 and out[0]["outcome"] == "interrupted" and out[0]["score"] is None
    assert out[0]["stopped"] == "game interrupted: boom"
    assert reg.db.execute("SELECT status FROM jobs").fetchone()[0] == "interrupted"


def test_watchdog_stops_a_game_that_overspends(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0, 0.0, 0.5, 4.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls, sleep_s=30))
    started = time.monotonic()
    out = target.play_target(settings, reg, pid, games=2, env_path=env, poll_s=0.01, settle_s=0.001, settle_max_s=0.01)
    assert time.monotonic() - started < 10
    [game] = out
    assert game["outcome"] == "interrupted" and "budget watchdog" in game["interruption"]
    assert game["watchdog_spend_usd"] == 4.0 and game["cost_usd"] == 4.0 and game["stopped"]


def test_a_crash_is_still_recorded_with_its_cost(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0, 0.0, 0.2, 0.2))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls, crash=RuntimeError("crash")))
    with pytest.raises(RuntimeError, match="crash"):
        target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert reg.db.execute("SELECT status FROM jobs").fetchone()[0] == "interrupted"
    kind, payload = _decisions(reg)[-1]
    assert kind == "target_game" and payload["cost_usd"] == 0.2 and payload["stopped"].startswith("aborted")


def test_one_target_game_at_a_time_and_queued_jobs_are_reused(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    aid = reg.register_actor("jiuwenswarm-target", runner.TargetConfig(route="competition-key").record())
    eid = reg.register_environment(dict(TARGET_ENV))
    [queued] = reg.enqueue(pid, aid, eid, "pilot", 1)
    [game] = target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert game["job_id"] == queued and reg.db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 1
    [stuck] = reg.enqueue(pid, aid, eid, "pilot", 1)
    reg.lease("someone:1:x", 1)
    reg.mark_running(stuck, 1, "/nowhere")
    with pytest.raises(RuntimeError, match="still leased or running"):
        target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert len(calls["episodes"]) == 1


def test_failed_runner_checks_refuse_the_game(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    monkeypatch.setattr(target, "check_slot", lambda root, solution: {"submission": {}, "environment": {},
                                                                       "failures": ["skill-frontmatter: missing name"]})
    [entry] = target.play_target(settings, reg, pid, env_path=env, **FAST)
    assert entry["started"] is False and entry["failures"] == ["skill-frontmatter: missing name"]
    assert calls["episodes"] == [] and reg.db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0


def test_dry_run_prepares_everything_but_plays_nothing(offline, monkeypatch):
    settings, reg, pid, env, calls = offline
    monkeypatch.setattr(target, "key_status", FakeKey(0.0))
    monkeypatch.setattr(runner, "run_target_episode", fake_episode(calls))
    [plan] = target.play_target(settings, reg, pid, games=2, dry_run=True, env_path=env, **FAST)
    assert plan["dry_run"] and plan["would_start"] and plan["budget"]["games_affordable"] == 11
    assert calls["prepare"] == 1 and calls["reload"] == 1 and calls["episodes"] == []
    assert reg.db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0
    assert [k for k, _ in _decisions(reg)] == ["target_dry_run"]
    assert (Path(plan["solution"]) / "skills" / "steady" / "SKILL.md").read_text() == SKILL
    assert plan["actor"]["route"] == "competition-key" and plan["environment"] == TARGET_ENV
    assert SECRET not in json.dumps(plan) and "CAREERLAB_TARGET_ENV" not in os.environ
    monkeypatch.setattr(target, "key_status", FakeKey(40.0))  # 10 left: the dry run still reports, but would not start
    [plan] = target.play_target(settings, reg, pid, dry_run=True, env_path=env, **FAST)
    assert plan["would_start"] is False and plan["budget"]["games_affordable"] == 0


# -- official runner fixes ----------------------------------------------------------------------------------------

def test_new_report_ignores_reports_from_earlier_games(tmp_path):
    root = tmp_path / "outputs"
    old = root / "Gradient Depression" / "20261026T100000Z" / "score_report.json"
    old.parent.mkdir(parents=True)
    old.write_text("{}")
    before = runner._reports(root)
    assert runner._new_report(root, before) is None
    os.utime(old, ns=(before[old] + 10**9, before[old] + 10**9))  # the same file rewritten counts as new
    assert runner._new_report(root, before) == old
    new = root / "Gradient Depression" / "20261026T120000Z" / "score_report.json"
    new.parent.mkdir()
    new.write_text("{}")
    os.utime(new, ns=(before[old] + 2 * 10**9, before[old] + 2 * 10**9))
    assert runner._new_report(root, before) == new
    assert runner._new_report(tmp_path / "missing", {}) is None


class FakeProc:
    pid, returncode = -1, 0

    async def wait(self):
        return 0


def _fake_slot(tmp_path, monkeypatch, play_writes=None):
    """A slot whose outputs already hold a completed earlier game; JiuwenSwarm and play are fakes."""
    root = tmp_path / "slot"
    outputs = root / "runner" / ".career_sim_runner" / "career_emu" / "outputs" / "Gradient Depression"
    (outputs / "20261026T100000Z").mkdir(parents=True)
    (outputs / "20261026T100000Z" / "score_report.json").write_text(json.dumps({
        "session_id": "0" * 32, "token_usage": {}, "events_log": None,
        "ending_score": {"completed": True, "quantitative_score": 77.0, "survival_months": 48}}))
    (root / "runner" / ".env").write_text("API_KEY=x\n")
    (root / "home").mkdir()
    spawned = []

    async def fake_spawn(*cmd, repo, home, log):
        spawned.append(cmd)
        if "play" in cmd and play_writes:
            play_writes(outputs)
        return FakeProc()

    async def no_stop(proc, grace_s=30.0):
        return None

    monkeypatch.setattr(runner, "prepare_slot", lambda settings, slot: root)
    monkeypatch.setattr(runner, "reload_dev_dataset", lambda repo, home, log: 0)
    monkeypatch.setattr(runner, "_ws_url", lambda repo, home: "ws://127.0.0.1:1")
    monkeypatch.setattr(runner, "_stop_stale_instance", lambda repo, home: spawned.append(("stop-stale",)))
    monkeypatch.setattr(runner, "_spawn", fake_spawn)
    monkeypatch.setattr(runner, "_stop", no_stop)
    return spawned


def _episode(tmp_path):
    settings = Settings(origin="deepseek", data_dir=tmp_path / "data")
    return asyncio.run(runner.run_target_episode(settings, runner.TargetConfig(route="competition-key"),
                                                 tmp_path / "solution", "job-1", tmp_path / "run", 0))


def test_episode_without_a_fresh_report_is_an_interruption_not_an_old_score(tmp_path, monkeypatch):
    spawned = _fake_slot(tmp_path, monkeypatch)
    result = _episode(tmp_path)
    assert result.outcome == "interrupted" and "no new score report" in result.interruption
    assert result.quantitative_score is None
    assert json.loads((tmp_path / "run" / "result.json").read_text())["outcome"] == "interrupted"
    assert [cmd[2] if len(cmd) > 2 else cmd[0] for cmd in spawned] == ["stop-stale", "jiuwenswarm-start", "python"]


def test_episode_scores_the_report_its_play_wrote(tmp_path, monkeypatch):
    session = "f" * 32

    def writes(outputs):
        d = outputs / "20261026T120000Z"
        d.mkdir()
        (d / "events.jsonl").write_text(json.dumps({"kind": "tool_result", "payload": {
            "raw_output": {"result": json.dumps({"session_id": session})}}}) + "\n")
        (d / "transcript.log").write_text(f"SESSION_ID={session}\n")
        (d / "score_report.json").write_text(json.dumps({
            "session_id": session, "play_exit_code": 0, "termination_reason": None,
            "token_usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12, "total_cost": 0.0},
            "ending_score": {"completed": False, "outcome": "fired", "quantitative_score": 55.0, "survival_months": 24,
                             "dimensions": []},
            "events_log": str(d / "events.jsonl"), "transcript_log": str(d / "transcript.log")}))

    _fake_slot(tmp_path, monkeypatch, writes)
    result = _episode(tmp_path)
    assert result.outcome == "eliminated" and result.quantitative_score == 55.0 and result.failure_reason == "fired"
    assert result.actor_usage["total_tokens"] == 12
    assert result.trajectory_path == str(tmp_path / "run" / "events.jsonl")
    assert (tmp_path / "run" / "transcript.log").is_file() and (tmp_path / "run" / "score_report.json").is_file()


def _report(tmp_path, session, events_text, score=None, events_path=None, name="a"):
    out = tmp_path / name / "out"
    out.mkdir(parents=True)
    (out / "events.jsonl").write_text(events_text)
    report = out / "score_report.json"
    report.write_text(json.dumps({"session_id": session, "token_usage": {}, "events_log": str(events_path or out / "events.jsonl"),
                                  "ending_score": score or {"completed": True, "quantitative_score": 60.0, "survival_months": 48}}))
    run = tmp_path / name / "run"
    run.mkdir()
    return report, run


def test_report_about_a_session_this_play_never_touched_is_not_scored(tmp_path):
    report, run = _report(tmp_path, "0" * 32, '{"kind": "tool_call", "payload": {}}\n')
    result = runner._from_report("j", report, run)
    assert result.outcome == "interrupted" and "never touched" in result.interruption and result.quantitative_score is None


def test_invalid_scores_and_foreign_files_are_rejected(tmp_path):
    session = "e" * 32
    report, run = _report(tmp_path, session, session, score={"completed": True, "quantitative_score": 150.0, "survival_months": 48})
    assert "invalid" in runner._from_report("j", report, run).interruption
    secret = tmp_path / ".env"
    secret.write_text(f"API_KEY={SECRET}\n{session}\n")
    report, run = _report(tmp_path, session, session, events_path=secret, name="b")
    result = runner._from_report("j", report, run)
    assert result.outcome == "interrupted" and not (run / "events.jsonl").exists()
    report, run = _report(tmp_path, session, session, name="c")
    assert runner._from_report("j", report, run).outcome == "completed" and (run / "events.jsonl").is_file()


def test_ws_url_needs_a_running_instance_with_an_open_port(tmp_path, monkeypatch):
    header = "INSTANCE     STATUS   PID     WORKSPACE                                PORTS\n" + "-" * 80 + "\n"
    listing = {"text": ""}
    opened = {"value": True}
    monkeypatch.setattr(runner.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, listing["text"], ""))
    monkeypatch.setattr(runner, "_port_open", lambda port, host="127.0.0.1": opened["value"])
    listing["text"] = header + "default      stopped  -       /h/.jiuwenswarm 19000/19001/19002/5173\n" \
                               "career_emu   stopped  -       /h/.jiuwenswarm-instances/career_emu 19092/20000/20001/6173\n"
    assert runner._ws_url(tmp_path, tmp_path) is None  # configured but stopped: --list still shows its ports
    listing["text"] = header + "career_emu   running  4242    /h/.jiuwenswarm-instances/career_emu 19092/20000/20001/6173\n"
    opened["value"] = False
    assert runner._ws_url(tmp_path, tmp_path) is None  # running, AgentServer not listening yet
    opened["value"] = True
    assert runner._ws_url(tmp_path, tmp_path) == "ws://127.0.0.1:19092"


def test_prepare_slot_never_waits_on_a_terminal_and_locks_the_key(tmp_path, monkeypatch):
    settings = Settings(origin="deepseek", data_dir=tmp_path / "data", runner_dir=tmp_path / "runner")
    root = runner.slot_dir(settings, 0)
    (root / "runner" / ".git").mkdir(parents=True)  # already cloned and synced
    key = tmp_path / "competition.env"
    key.write_text(f"API_KEY={SECRET}\n")
    monkeypatch.setenv("CAREERLAB_TARGET_ENV", str(key))
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", "/the/lab/venv")
    calls = []

    def fake_run(cmd, **kw):
        calls.append((cmd, kw))
        instance_env = runner.instance_env_path(root / "home")
        instance_env.parent.mkdir(parents=True, exist_ok=True)
        instance_env.write_text("API_KEY=copied\n")
        instance_env.chmod(0o644)
        return subprocess.CompletedProcess(cmd, 0 if len(calls) == 1 else 1, '{"summary": {}}', "")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.prepare_slot(settings, 0) == root
    [(cmd, kw)] = calls
    assert cmd[-1] == "setup" and kw["stdin"] is subprocess.DEVNULL
    assert kw["env"]["HOME"] == str(root / "home") and "UV_PROJECT_ENVIRONMENT" not in kw["env"]
    assert (root / "runner" / ".env").read_text() == key.read_text()
    assert (root / "runner" / ".env").stat().st_mode & 0o777 == 0o600
    assert runner.instance_env_path(root / "home").stat().st_mode & 0o777 == 0o600
    with pytest.raises(RuntimeError, match="setup.log"):
        runner.prepare_slot(settings, 0)


def test_hangup_and_terminate_become_interrupts_while_games_run():
    import signal

    saved = signal.getsignal(signal.SIGTERM), signal.getsignal(signal.SIGHUP)
    try:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)  # started under nohup
        with target._signals_as_interrupt():
            assert signal.getsignal(signal.SIGTERM) is signal.default_int_handler
            assert signal.getsignal(signal.SIGHUP) is signal.SIG_IGN
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        with target._signals_as_interrupt():
            assert signal.getsignal(signal.SIGHUP) is signal.default_int_handler
        assert signal.getsignal(signal.SIGTERM) == signal.getsignal(signal.SIGHUP) == signal.SIG_DFL
    finally:
        signal.signal(signal.SIGTERM, saved[0])
        signal.signal(signal.SIGHUP, saved[1])


def test_dataset_reload_matches_make_play(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(runner.subprocess, "run", lambda cmd, **kw: calls.append((cmd, kw)) or subprocess.CompletedProcess(cmd, 0))
    assert runner.reload_dev_dataset(tmp_path, tmp_path / "home", tmp_path / "dataset.log") == 0
    [(cmd, kw)] = calls
    assert cmd == ["uv", "run", "career-emulator-engine", "update", "--source", "distribution", "--split", "dev"]
    assert kw["stdin"] is subprocess.DEVNULL and kw["cwd"] == tmp_path


@pytest.mark.skipif(not hasattr(os, "killpg"), reason="process groups are POSIX only")
def test_stop_ends_the_whole_process_group(tmp_path):
    pid_file = tmp_path / "child.pid"

    async def scenario():
        proc = await runner._spawn("sh", "-c", f"sleep 60 & echo $! > '{pid_file}'; wait", repo=tmp_path, home=tmp_path,
                                   log=tmp_path / "log")
        for _ in range(100):
            if pid_file.exists() and pid_file.read_text().strip():
                break
            await asyncio.sleep(0.02)
        await runner._stop(proc, grace_s=5.0)
        return proc

    proc = asyncio.run(scenario())
    child = int(pid_file.read_text())
    assert proc.returncode is not None
    for _ in range(100):  # the orphaned sleep is reaped by init shortly after it dies
        try:
            os.kill(child, 0)
        except ProcessLookupError:
            break
        time.sleep(0.02)
    else:
        pytest.fail("the child of the stopped process is still alive")
