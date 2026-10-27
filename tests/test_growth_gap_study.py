import random

from scripts.growth_gap_study import bonus,select
from scripts.trust_risk_study import FrozenKnowledge
from scripts.financial_reserve_study import select as common_select
from tests.test_second_review_search import obs
from scripts.balanced_growth_study import readiness,bonus as joint_bonus

CONFIG={"reserve_target":1,"reserve_weight":2,"growth_weight":3}


def test_skill_bonus_keeps_rewarding_growth_above_old_L2_target():
    o=obs(9,"L2",skill=12)
    k=FrozenKnowledge({"Study":{"skill":2}}, {})
    assert bonus(o,{"action":"Study"},"skill",k,{})==6


def test_proxy_bonus_penalizes_crossing_below_readiness():
    o=obs(5);o["current_state"]["status"]["network"]=3
    k=FrozenKnowledge({"Trade":{"network":-1}}, {})
    assert bonus(o,{"action":"Trade"},"network",k,{})==-3


def test_stalled_positive_quarterly_gain_does_not_get_extra_bonus():
    o=obs(9,"L2",skill=12);o["current_event"]["remaining_energy"]=3
    k=FrozenKnowledge({"Study":{"skill":2}}, {})
    assert bonus(o,{"action":"Study"},"skill",k,{"stalled":{("skill",12,2)}})==0


def test_control_exactly_matches_common_reserve_policy():
    o=obs(5);o["current_state"]["status"]["wealth"]=1
    k=FrozenKnowledge({}, {})
    expected,_,_=common_select(o,"reserve",k,{"prior_explosions":0},random.Random(0),CONFIG)
    actual,_,_=select(o,"control",k,{"prior_explosions":0},random.Random(0),CONFIG)
    assert actual==expected


def test_explicit_risk_cleanup_is_preserved_in_all_arms():
    o=obs(9,"L2",skill=12);o["current_state"]["status"]["wealth"]=1
    o["current_event"]["remaining_energy"]=3
    o["choices"]=[{"choice":1,"action":"Defuse legacy risk","energy_cost":2},
        {"choice":2,"action":"Skill learning","energy_cost":2,"status_updates":{"Skill":9}}]
    k=FrozenKnowledge({}, {})
    for arm in ("control","skill","network","output"):
        c,reason,_=select(o,arm,k,{"prior_explosions":0,"risk":2},random.Random(0),CONFIG)
        assert c["choice"]==1 and reason=="respond_to_public_risk_warning"


def test_joint_readiness_caps_sufficient_dimensions():
    targets={"skill":18,"network":6,"output":6}
    assert readiness({"skill":9,"network":6,"output":6},targets)==.5
    assert readiness({"skill":9,"network":10,"output":10},targets)==.5


def test_joint_bonus_rewards_remaining_gap_and_penalizes_new_gap():
    o=obs(9,"L2",skill=12);o["current_state"]["status"].update(network=6,output=6)
    k=FrozenKnowledge({"Study":{"skill":3},"Distract":{"network":-2,"skill":1}}, {})
    assert joint_bonus(o,{"action":"Study"},"balanced",k,{})>0
    assert joint_bonus(o,{"action":"Distract"},"balanced",k,{})<0
