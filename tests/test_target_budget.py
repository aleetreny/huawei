from concurrent.futures import ThreadPoolExecutor

import pytest

from careerlab.budget import BudgetClosed, TargetBudget, micros, receipt_cost
from careerlab.store import Registry, import_jsonl
from test_adaptive_guards import setup_registry


def jobs_and_budget(tmp_path,n=3):
    reg,p,a,e=setup_registry(tmp_path,target=True)
    jobs=reg.enqueue(p,a,e,"pilot",n)
    b=TargetBudget(reg); b.configure()
    return reg,jobs,b


def test_unknown_cost_keeps_money_and_stops_further_admission(tmp_path):
    reg,j,b=jobs_and_budget(tmp_path)
    b.reserve(j[0],"pilot",1.5); b.reserve(j[0],"pilot",1.5)
    b.start(j[0]); b.settle(j[0])
    assert b.status()["paused"] and b.status()["committed_usd"]==1.5
    with pytest.raises(BudgetClosed): b.reserve(j[1],"pilot",1.5)
    with pytest.raises(BudgetClosed): b.cancel(j[0],"not free")
    b.reconcile(j[0],0.6,"verified provider receipt")
    b.reserve(j[1],"pilot",1.5)
    assert b.status()["committed_usd"]==2.1
    with pytest.raises(BudgetClosed): b.start(j[0])


def test_actual_overage_is_kept_and_requires_acknowledgement(tmp_path):
    reg,j,b=jobs_and_budget(tmp_path)
    b.reserve(j[0],"pilot",1); b.start(j[0]); b.settle(j[0],1.4)
    assert b.status()["paused"] and b.status()["committed_usd"]==1.4
    b.reconcile(j[0],1.4,"verified charge; future reservations increased")
    assert not b.status()["paused"]
    with pytest.raises(BudgetClosed): b.reserve(j[1],"pilot",2)
    with pytest.raises(BudgetClosed): b.configure(total=50,pilot=10,selection=8)


def test_concurrent_admission_allows_one_paid_episode(tmp_path):
    reg,j,b=jobs_and_budget(tmp_path)
    def reserve(jid):
        other=Registry(reg.path)
        try:
            TargetBudget(other).reserve(jid,"pilot",1)
            return True
        except BudgetClosed:
            return False
        finally: other.db.close()
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(reserve,j[:2]))==[False,True]


def test_ledger_survives_export_import_and_cannot_be_reset(tmp_path):
    reg,j,b=jobs_and_budget(tmp_path)
    b.reserve(j[0],"pilot",1.5); b.start(j[0]); b.settle(j[0],0.8)
    out=tmp_path/"export"; reg.export_jsonl(out)
    cloud=Registry(tmp_path/"new"/"reg.sqlite3")
    import_jsonl(cloud,out,tmp_path,tmp_path)
    copy=TargetBudget(cloud); copy.configure()
    assert copy.status()["committed_usd"]==0.8
    import_jsonl(cloud,out,tmp_path,tmp_path)
    assert copy.status()["committed_usd"]==0.8
    with pytest.raises(BudgetClosed): copy.reserve(j[0],"pilot",1.5)
    other=Registry(tmp_path/"other.sqlite3",origin="other")
    with pytest.raises(BudgetClosed): TargetBudget(other).configure()


@pytest.mark.parametrize("bad",[-1,float("nan"),float("inf"),True])
def test_invalid_money_is_rejected(bad):
    with pytest.raises(ValueError): micros(bad)


def test_no_token_based_guess_of_paid_cost():
    assert receipt_cost({"total_tokens":99_000_000}) is None
    assert receipt_cost({"billed_cost_usd":0.6})==0.6
