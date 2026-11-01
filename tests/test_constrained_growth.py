import random
from copy import deepcopy

from scripts.constrained_growth_study import excluded_reasons,select
from scripts.balanced_growth_study import select as joint_select
from scripts.trust_risk_study import FrozenKnowledge
from tests.test_second_review_search import obs

CONFIG={"reserve_target":1,"reserve_weight":2,"growth_weight":24,
    "safety_floors":{"wealth":1,"health":4,"dignity":2}}


def event():
    o=obs(9,"L2",skill=12);o["current_state"]["status"].update(wealth=1,health=4,dignity=2,network=6,output=6)
    o["current_state"]["status"]["energy"]=0
    o["choices"]=[{"choice":1,"action":"Common"},{"choice":2,"action":"Grow"}]
    return o


def test_risk_filter_is_activated_only_after_prior_incident():
    o=event();k=FrozenKnowledge({"Common":{"skill":0},"Grow":{"skill":5}},
        {"Common":{"observations":100,"adverse_responses":0},"Grow":{"observations":100,"adverse_responses":20}})
    assert excluded_reasons(o,o["choices"][1],o["choices"][0],k,{},CONFIG)==[]
    assert excluded_reasons(o,o["choices"][1],o["choices"][0],k,{"prior_explosions":1},CONFIG)==["post_incident_hazard"]


def test_safety_filter_uses_deficits_relative_to_common_not_absolute_veto():
    o=event();common,grow=o["choices"]
    k=FrozenKnowledge({"Common":{"health":-1},"Grow":{"health":-1,"wealth":-1}}, {})
    assert excluded_reasons(o,grow,common,k,{},CONFIG)==["fragile_wealth"]
    assert excluded_reasons(o,common,common,k,{},CONFIG)==[]
    o["current_state"]["status"]["wealth"]=5
    assert excluded_reasons(o,grow,common,k,{},CONFIG)==[]


def test_filter_preserves_common_fallback_and_blocks_growth_that_spends_fragile_resources():
    o=event();k=FrozenKnowledge({"Common":{"skill":0},"Grow":{"skill":6,"wealth":-1}}, {})
    old,_,_=joint_select(o,"balanced",k,{},random.Random(0),CONFIG)
    new,_,d=select(o,"constrained",k,{},random.Random(0),CONFIG)
    assert old["choice"]==2 and new["choice"]==1
    assert d["filter_changed_choice"] and "fragile_wealth" in d["rejected"]["2"]


def test_unknown_alternatives_are_excluded_but_common_never_is():
    o=event();common,grow=o["choices"];k=FrozenKnowledge({}, {})
    assert excluded_reasons(o,grow,common,k,{},CONFIG)==["unknown_nominal_effect"]
    assert excluded_reasons(o,common,common,k,{},CONFIG)==[]


def test_growth_reward_cannot_buy_higher_empirical_exposure_after_incident():
    o=event();k=FrozenKnowledge({"Common":{"skill":0},"Grow":{"skill":6}},
        {"Common":{"observations":100,"adverse_responses":0},"Grow":{"observations":100,"adverse_responses":20}})
    old,_,_=joint_select(o,"balanced",k,{"prior_explosions":1},random.Random(0),CONFIG)
    new,_,d=select(o,"constrained",k,{"prior_explosions":1},random.Random(0),CONFIG)
    assert old["choice"]==2 and new["choice"]==1
    assert d["filter_changed_choice"] and "post_incident_hazard" in d["rejected"]["2"]


def test_fresh_reference_and_unconstrained_arms_match_the_frozen_parents():
    o=event();k=FrozenKnowledge({"Common":{"skill":0},"Grow":{"skill":6}}, {})
    for arm in ("control","balanced"):
        assert select(o,arm,k,deepcopy({}),random.Random(4),CONFIG)==joint_select(o,arm,k,deepcopy({}),random.Random(4),CONFIG)


def test_public_warning_cleanup_is_protected_even_if_other_nominal_options_look_better():
    o=event();o["current_state"]["status"]["energy"]=3;o["current_event"]["remaining_energy"]=3
    o["choices"]=[{"choice":1,"action":"Defuse legacy risk","energy_cost":2},
        {"choice":2,"action":"Grow","energy_cost":2,"status_updates":{"Skill":20}}]
    k=FrozenKnowledge({}, {})
    c,reason,_=select(o,"constrained",k,{"risk":2},random.Random(0),CONFIG)
    assert c["choice"]==1 and reason=="respond_to_public_risk_warning"
