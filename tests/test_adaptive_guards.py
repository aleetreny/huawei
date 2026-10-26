import json
from pathlib import Path

import pytest

from careerlab import decisions, stats
from careerlab.actors.official_runner import TargetConfig
from careerlab.store import Registry


def setup_registry(tmp_path, target=False, origin=""):
    reg=Registry(tmp_path/"reg.sqlite3",origin=origin)
    bundle=tmp_path/"bundle"
    bundle.mkdir(exist_ok=True)
    (bundle/"scripted.json").write_text('{"rule_set":"uniform"}')
    pid=reg.register_policy(bundle,"family","policy",[],"hypothesis","one change","test")
    cfg=TargetConfig("competition-key").record() if target else {"model":"haiku","timeout_s":7200}
    aid=reg.register_actor("jiuwenswarm-target" if target else "claude-cli",cfg)
    eid=reg.register_environment({"test":"one"})
    return reg,pid,aid,eid


def ingest(reg,pid,aid,eid,tmp_path,score=60,purpose="screen",outcome="completed",usage=None):
    jid=reg.enqueue(pid,aid,eid,purpose,1)[0]
    d=tmp_path/jid; d.mkdir()
    result={"job_id":jid,"outcome":outcome,"quantitative_score":score,"survival_months":48 if outcome=="completed" else 24,
            "ending_score":{"completed":outcome=="completed"},"steps":1,"wall_seconds":1,"rejected_actions":0,
            "actor_usage":usage or {}}
    if outcome=="interrupted":
        result.update(quantitative_score=None,survival_months=None,interruption="test interruption")
    (d/"result.json").write_text(json.dumps(result))
    reg.ingest(jid,d)
    return jid


def test_development_excludes_confirmation_and_infra_and_is_exploratory(tmp_path):
    reg,p,a,e=setup_registry(tmp_path)
    jobs=[ingest(reg,p,a,e,tmp_path) for _ in range(4)]
    ingest(reg,p,a,e,tmp_path,score=100,purpose="confirm")
    ingest(reg,p,a,e,tmp_path,score=1,purpose="infra")
    result=decisions.block_decision(reg,a,job_ids=jobs,record=False)
    assert result["rows"][0]["n_prefix"]==4
    assert result["scope"]=="exploratory" and not result["can_select"]
    assert result["rows"][0]["action"].startswith("EXPLORE_")
    assert not result["rows"][0]["executable"]


def test_actual_target_tokens_and_missing_usage_are_not_imputed(tmp_path):
    reg,p,a,e=setup_registry(tmp_path,target=True)
    jobs=[ingest(reg,p,a,e,tmp_path,usage={"total_tokens":144_000_000}) for _ in range(4)]
    result=decisions.block_decision(reg,a,job_ids=jobs,record=False)
    assert result["rows"][0]["posterior_mean"]==48  # E=0 at three million/month
    assert result["can_select"]
    ingest(reg,p,a,e,tmp_path)
    result=decisions.block_decision(reg,a,record=False)
    assert not result["can_select"] and "missing" in " ".join(result["blockers"])


def test_inconclusive_robustness_never_emits_dormancy(tmp_path,monkeypatch):
    reg,p,a,e=setup_registry(tmp_path)
    jobs=[ingest(reg,p,a,e,tmp_path) for _ in range(4)]
    monkeypatch.setattr(stats,"decision_is_robust",lambda data:stats.Robustness("inconclusive",{},{},"flip",False,[]))
    monkeypatch.setattr(stats,"decide",lambda data:{p:stats.ActionDecision(p,"DORMANT","test suggestion")})
    result=decisions.block_decision(reg,a,job_ids=jobs,record=False)
    assert result["rows"][0]["action"]=="INCONCLUSIVE"
    assert result["rows"][0]["suggested_action"]=="DORMANT"


def test_pending_future_job_does_not_block_completed_explicit_batch(tmp_path):
    reg,p,a,e=setup_registry(tmp_path,target=True)
    jobs=[ingest(reg,p,a,e,tmp_path,usage={"total_tokens":10_000}) for _ in range(4)]
    future=reg.enqueue(p,a,e,"screen",1)[0]
    assert decisions.block_decision(reg,a,record=False)["blockers"]
    assert decisions.block_decision(reg,a,job_ids=jobs,record=False)["can_select"]
    assert not decisions.block_decision(reg,a,job_ids=[future],record=False)["can_select"]


def test_environment_mixing_and_interruptions_are_guarded(tmp_path):
    reg,p,a,e=setup_registry(tmp_path)
    jobs=[ingest(reg,p,a,e,tmp_path) for _ in range(4)]
    ingest(reg,p,a,e,tmp_path,outcome="interrupted")
    result=decisions.block_decision(reg,a,env_id=e,job_ids=jobs,record=False)
    assert any(x["kind"]=="interruption_rate" for x in result["alarms"])
    e2=reg.register_environment({"test":"two"}); reg.enqueue(p,a,e2,"screen",1)
    with pytest.raises(ValueError,match="multiple environments"):
        decisions.block_decision(reg,a,record=False)


def test_no_data_is_a_report_not_a_crash(tmp_path):
    reg,p,a,e=setup_registry(tmp_path)
    result=decisions.block_decision(reg,a,record=False)
    assert not result["rows"] and not result["can_select"]
