import gzip
import hashlib
import json
import pytest

from scripts.second_review_search import Knowledge, remember, value
from scripts.analyze_second_review import summarize_record
from scripts.audit_second_review import audit
from scripts.first_review_search import node_key


def obs(month, level="L1", skill=9):
    return {"current_state": {"time": {"current_month": month, "current_quarter": (month+2)//3},
        "status": {"health": 8,"dignity":8,"skill":skill,"network":3,"output":3,"level":level,"energy":3},
        "simulation_flags": {"alive":True,"failed":False}},
        "current_event": {"title":"Question"},"choices":[{"choice":1,"action":"Do it"}],"events":""}


def step(before, after):
    return {"before":before,"after":after,"choice":{"choice":1,"action":"Do it"},
        "applied":True,"ambiguous":False,"reply":{"success":True},"phase":"event"}


def test_coverage_is_only_second_window():
    k=Knowledge()
    k.applied(obs(6),{"choice":1})
    k.applied(obs(7),{"choice":1})
    assert k.status()["questions_7_12"]==1
    assert sum(k.counts.values())==1


def test_delayed_first_promotion_is_not_second_promotion():
    r={"run":0,"arm":[],"outcome":"twelve_month_window",
        "steps":[step(obs(6),obs(7)),step(obs(11),obs(12,"L2"))],"final":obs(13,"L2")}
    result=summarize_record(r)
    assert result["reached_7"]
    assert not result["first_promoted_alive_at_7"]
    assert not result["second_promotion_by_12"]


def test_second_promotion_and_survival_are_distinct():
    r={"run":0,"arm":[],"outcome":"eliminated",
        "steps":[step(obs(5),obs(6,"L2")),step(obs(7,"L2"),obs(8,"L2")),
                 step(obs(11,"L2"),obs(12,"L3"))],"final":obs(12,"L3")}
    result=summarize_record(r)
    assert result["first_promoted_alive_at_7"]
    assert result["second_promotion_by_12"]
    assert not result["second_promotion_and_alive"]


def test_stall_memory_requires_same_level_and_clock():
    before,after=obs(9,"L2"),obs(10,"L2")
    before["current_event"]["remaining_energy"]=3
    c={"action":"Study","status_updates":{"Skill":1}}
    memory={}
    remember(before,c,after,memory)
    assert not memory.get("stalled")
    after=obs(9,"L2")
    remember(before,c,after,memory)
    assert ("skill",9,2) in memory["stalled"]


def test_nominal_effect_model_counts_missing_stats_as_zero():
    k=Knowledge()
    k.ingest({"steps":[],"logs":{"entries":[
        {"message":"Chose #1: Work\nSkill +2"},
        {"message":"Chose #1: Work\nHealth +2"}]}})
    assert k.effect({"action":"Work"})["skill"]==1
    assert k.effect({"action":"Work"})["health"]==1


def test_independent_audit_does_not_count_prefix_execution(tmp_path):
    before=obs(7)
    question={"id":node_key(before),"phase":"event","choices":before["choices"]}
    (tmp_path/"questions.json").write_text(json.dumps([question]))
    batch=tmp_path/"batch"
    batch.mkdir()
    archive=batch/"public-trajectories.jsonl.gz"
    prefix=step(obs(6),obs(7))
    rejected=step(before,obs(8))
    rejected["applied"]=False
    with gzip.open(archive,"wt") as stream:
        stream.write(json.dumps({"run":0,"steps":[prefix,rejected]})+"\n")
    (batch/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest())
    result=audit(tmp_path)
    assert result["required"]==1
    assert result["witnessed"]==0
    assert not result["complete"]


def test_independent_audit_rejects_catalogue_drift(tmp_path):
    (tmp_path/"questions.json").write_text("[]")
    batch=tmp_path/"batch"
    batch.mkdir()
    archive=batch/"public-trajectories.jsonl.gz"
    with gzip.open(archive,"wt") as stream:
        stream.write(json.dumps({"run":0,"steps":[step(obs(7),obs(8))]})+"\n")
    (batch/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest())
    with pytest.raises(ValueError,match="Catalogue differs"):
        audit(tmp_path)
