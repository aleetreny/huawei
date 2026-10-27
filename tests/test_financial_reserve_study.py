import random
import hashlib
import json

from scripts.financial_reserve_study import reserve_term, select
from scripts.trust_risk_study import FrozenKnowledge
from tests.test_second_review_search import obs
from scripts.prepare_financial_calibration import prepare


CONFIG={"reserve_target":2,"reserve_weight":6}


def test_cash_term_values_replenishment_and_penalizes_depletion():
    assert reserve_term(1,-2)==-14
    assert reserve_term(1,1)==6
    assert reserve_term(4,1)==0
    assert reserve_term(4,-1)==-1


def test_reserve_guard_changes_costly_relationship_choice():
    o=obs(1)
    o["current_state"]["status"].update(network=1,wealth=1)
    o["choices"]=[{"choice":1,"action":"Buy support"},{"choice":2,"action":"Discuss scope"}]
    k=FrozenKnowledge({"Buy support":{"network":2,"wealth":-2}}, {})
    b,_,_=select(o,"baseline",k,{"prior_explosions":0},random.Random(0),CONFIG)
    c,_,d=select(o,"reserve",k,{"prior_explosions":0},random.Random(0),CONFIG)
    assert b["choice"]==1
    assert c["choice"]==2
    assert d["cash_override"]


def test_reserve_does_not_forbid_critical_health_spending():
    o=obs(1)
    o["current_state"]["status"].update(health=1,wealth=1)
    o["choices"]=[{"choice":1,"action":"Pay for recovery"},{"choice":2,"action":"Continue"}]
    k=FrozenKnowledge({"Pay for recovery":{"health":5,"wealth":-2}}, {})
    c,_,_=select(o,"reserve",k,{"prior_explosions":0},random.Random(0),CONFIG)
    assert c["choice"]==1


def test_both_arms_use_same_incident_guard_when_money_effects_zero():
    o=obs(1)
    o["current_state"]["status"]["wealth"]=1
    o["choices"]=[{"choice":1,"action":"A"},{"choice":2,"action":"B"}]
    k=FrozenKnowledge({}, {"A":{"observations":10,"adverse_responses":5},"B":{"observations":10,"adverse_responses":0}})
    for arm in ("baseline","reserve"):
        c,_,_=select(o,arm,k,{"prior_explosions":1},random.Random(0),CONFIG)
        assert c["choice"]==2


def test_without_financial_effect_no_override():
    o=obs(1)
    o["current_state"]["status"]["wealth"]=1
    k=FrozenKnowledge({}, {})
    _,_,d=select(o,"reserve",k,{"prior_explosions":0},random.Random(0),CONFIG)
    assert not d["cash_override"]


def test_calibration_creates_new_protocol_without_modifying_parent(tmp_path):
    parent=tmp_path/"parent";parent.mkdir()
    for kind in ("effects","hazards"):
        (parent/f"frozen-{kind}.json").write_text("{}")
    empty_sha=hashlib.sha256(b"{}").hexdigest()
    p={"dependencies":{},"effects_sha256":empty_sha,"hazards_sha256":empty_sha}
    original=json.dumps(p).encode()
    (parent/"protocol.json").write_bytes(original)
    digest=hashlib.sha256(original).hexdigest()
    (parent/"protocol-sha256.txt").write_text(digest)
    (parent/"results.json").write_text("{}")
    target=tmp_path/"calibration"
    prepare(target,parent,per_arm=2,seed=42)
    assert (parent/"protocol.json").read_bytes()==original
    new=json.loads((target/"protocol.json").read_text())
    assert new["config"]=={"reserve_target":1,"reserve_weight":2}
    assert new["schedule"].count("baseline")==new["schedule"].count("reserve")==2
    assert new["derived_after"]["results_sha256"]==empty_sha
