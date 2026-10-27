"""Regression for the official month-49 settlement observed in completed black-box runs."""
import copy
import json
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/ingenieria-inversa'))
sys.path.insert(0, str(ROOT / 'scripts/mecanicas-emergentes'))
import replica as R
from game import Game
from experiment import CATALOG, Intervention


@pytest.fixture(scope='module')
def catalog():
    return R.Catalog(json.loads(CATALOG.read_text()))


def test_both_generators_settle_full_completion_once(catalog):
    completions = 0
    for seed in range(12):
        old, _ = R.play(catalog, Intervention('base'), random.Random(seed), settle_completion=False)
        new, _ = R.play(catalog, Intervention('base'), random.Random(seed))
        if old.alive:
            completions += 1
            assert old.month == 48 and new.month == 49
            assert new.wealth == pytest.approx(round(old.wealth + R.SALARY[old.level], 1))
            assert new.duration_in_level == old.duration_in_level + 1
        else:
            assert new == old
        g = Game(catalog, random.Random(seed))
        g.finish(Intervention('base'))
        assert g.st == new
        frozen = copy.deepcopy(g.st)
        assert g.next() is None and g.next() is None
        assert g.st == frozen
    assert completions > 0


def test_short_horizon_is_not_a_full_career_settlement(catalog):
    old, _ = R.play(catalog, Intervention('base'), random.Random(1), months=6, settle_completion=False)
    new, _ = R.play(catalog, Intervention('base'), random.Random(1), months=6)
    assert new == old
    assert new.month == 6
    g = Game(catalog, random.Random(1), months=6)
    g.finish(Intervention('base'))
    assert g.st == old


def test_already_eliminated_state_gets_no_completion_pay(catalog):
    g = Game(catalog, random.Random(1))
    g.st = R.State(month=48, level=6, wealth=40, health=0, alive=False, failure='health')
    old = copy.deepcopy(g.st)
    g._advance()
    assert g.st == old


def test_joint_terminal_plan_avoids_paying_twice_for_cleanup(catalog):
    rep=R.Replica(catalog)
    start=R.State(month=48,level=6,skill=145,network=54,output=38,
                  health=5,dignity=5,risk=1,wealth=40,energy=3)
    from analyze import finish_quarter
    baseline,_=finish_quarter(rep,start,'base')
    optimal,actions=finish_quarter(rep,start,'terminal_q')
    assert R.Replica.score(optimal)-R.Replica.score(baseline) == pytest.approx(3)
    assert optimal.risk == baseline.risk == 0
    assert optimal.alive and optimal.energy == 0
    assert 'Defuse legacy risk' not in actions
