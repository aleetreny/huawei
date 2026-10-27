import random

from scripts.trust_risk_study import ARMS, FrozenKnowledge, eligible, selection
from scripts.second_review_search import remember
from tests.test_second_review_search import obs
from scripts.analyze_trust_risk import wilson, history


def energy(month=6,level="L2"):
    o=obs(month,level)
    o["current_event"]["remaining_energy"]=3
    o["choices"]=[{"choice":i,"action":name,"energy_cost":cost} for i,(name,cost) in enumerate([
        ("Defuse legacy risk",2),("Prepare report materials",1),("Health recovery",1)])]
    return o


def test_assignment_eligibility_does_not_depend_on_future_survival():
    assert eligible(energy())
    assert not eligible(energy(9))
    assert not eligible(energy(level="L1"))
    partial=energy();partial["current_event"]["remaining_energy"]=2
    assert not eligible(partial)


def test_factorial_contains_every_combination():
    assert len(ARMS)==8
    assert len({tuple(a.values()) for a in ARMS})==8


def test_equal_cost_plans_preserve_recovery_and_differ_only_in_package():
    plans={"cleanup":["Defuse legacy risk","Health recovery"],
        "growth":["Prepare report materials","Prepare report materials","Health recovery"]}
    k=FrozenKnowledge({},{})
    for arm in ARMS:
        memory={}
        choices=[]
        for _ in range(2 if arm["cleanup6"] else 3):
            c,_=selection(energy(),arm,memory,k,random.Random(0),plans)
            choices.append(c)
        assert sum(c["energy_cost"] for c in choices)==3
        assert sum(c["action"]=="Health recovery" for c in choices)==1


def test_cleanup_does_not_erase_public_incident_memory():
    before=energy();after=energy()
    memory={"prior_explosions":1}
    remember(before,{"action":"Defuse legacy risk"},after,memory)
    assert memory["prior_explosions"]==1
    assert memory["risk"]==0


def test_guard_uses_only_frozen_empirical_frequency():
    k=FrozenKnowledge({}, {"A":{"observations":6,"adverse_responses":2}})
    assert k.hazard_rate({"action":"A"})==.3
    assert k.hazard_rate({"action":"unseen"})==.25


def test_wilson_does_not_turn_zero_events_into_zero_uncertainty():
    interval=wilson(0,64)
    assert abs(interval[0])<1e-12
    assert interval[1]>.05
    assert wilson(0,0) is None


def test_history_retains_explosion_before_cleanup():
    first={"before":obs(5),"after":obs(6),"choice":{"action":"Act"}}
    first["after"]["events"]="Old landmines all go off at once"
    cleanup={"before":obs(6),"after":obs(6),"choice":{"action":"Defuse legacy risk"}}
    final={"current_state":{"simulation_flags":{"failure_reason":"Trust crisis"}}}
    result=history({"steps":[first,cleanup],"final":final})
    assert result["explosions"][0]["step"]==0
    assert result["cleanups"][0]["step"]==1
