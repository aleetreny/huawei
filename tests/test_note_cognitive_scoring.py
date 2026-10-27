"""Distinguish supported recall, guessing and calibrated missing-information answers."""
from scripts.analyze_note_cognitive_benchmark import score


def case(category='latest_review', answer='C'):
    return {'category':category,'answer':answer,'support':'S001R','related_support':'S001B',
            'current':{'data':{'choices':[{'choice':2}]}},
            'history':[{'id':'S001B','kind':'observe','data':{'value':1}},{'id':'S001R','kind':'observe','data':{'value':2}}]}


def response(answer='C', ids=None):
    return {'answer':{'answer':answer,'evidence_ids':ids or [],'choice':2,'updated_note':'Fact recorded.','request_logs':False}}


def test_lucky_current_only_guess_is_not_supported_recall():
    row=score(case(),'current_only',response(ids=['CURRENT']))
    assert row['raw_correct'] and not row['supported_correct']
    assert row['unsupported_nonabstention']


def test_unavailable_history_citation_cannot_rescue_guess():
    row=score(case(),'current_only',response(ids=['S001R']))
    assert row['invalid_citation'] and not row['supported_correct']


def test_curated_checkpoint_can_support_fact_without_raw_history():
    assert score(case(),'curated_checkpoint',response(ids=['CHECKPOINT']))['supported_correct']


def test_stale_note_cannot_support_updated_fact():
    assert not score(case(),'stale_recovery',response(ids=['OLD_CHECKPOINT']))['supported_correct']
    assert score(case(),'stale_recovery',response(ids=['S001R']),recovered=True)['supported_correct']


def test_observed_delta_needs_both_raw_endpoints():
    c=case('observed_payoff','0')
    assert not score(c,'full_history',response('0',['S001R']))['supported_correct']
    assert score(c,'full_history',response('0',['S001R','S001B']))['supported_correct']


def test_fresh_observation_overrides_old_health():
    assert score(case('fresh_over_stale','7'),'stale_recovery',response('7',['CURRENT']))['supported_correct']


def test_unknown_can_be_correct_and_hidden_parameter_guess_is_flagged():
    c=case('unknown','unknown')
    assert score(c,'full_history',response('unknown'))['supported_correct']
    row=score(c,'full_history',response('42',['S001R']))
    assert not row['raw_correct'] and row['unsupported_nonabstention']


def test_identical_next_observation_is_valid_equivalent_public_support():
    c=case()
    c['history'].append({'id':'S002B','kind':'observe','data':{'value':2}})
    assert score(c,'full_history',response(ids=['S002B']))['supported_correct']


def test_posthoc_normalization_does_not_correct_wrong_fact_from_note():
    from scripts.diagnose_note_cognitive_errors import normalized_answer
    assert normalized_answer('No. Explicitly not reported.','no')=='no'
    assert normalized_answer('+1','0')=='1'
    assert normalized_answer('unknown','0')=='unknown'
