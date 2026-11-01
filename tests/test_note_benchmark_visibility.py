"""Protect the benchmark from gold-label and unavailable-history leakage."""
import json

from scripts.run_note_cognitive_benchmark import prompt_for


def fixture_case():
    return {'question':'Which prior fact is supported?',
            'answer':'GOLD_LABEL_MUST_NOT_BE_SENT', 'future':'FUTURE_OUTCOME_MUST_NOT_BE_SENT',
            'current':{'id':'CURRENT','data':{'marker':'CURRENT_PUBLIC'}},
            'history':[{'id':'S000R','data':'HISTORY_ONLY_SENTINEL'}],
            'checkpoint':{'id':'CHECKPOINT','text':'CURATED_ONLY_SENTINEL'},
            'stale_checkpoint':{'id':'OLD_CHECKPOINT','text':'STALE_ONLY_SENTINEL'}}


def test_current_condition_cannot_leak_gold_history_or_checkpoint():
    rendered=prompt_for(fixture_case(),'current_only','FIXED_SKILL')
    assert 'CURRENT_PUBLIC' in rendered
    for value in ('GOLD_LABEL_MUST_NOT_BE_SENT','FUTURE_OUTCOME_MUST_NOT_BE_SENT',
                  'HISTORY_ONLY_SENTINEL','CURATED_ONLY_SENTINEL','STALE_ONLY_SENTINEL'):
        assert value not in rendered


def test_history_and_checkpoint_visibility_are_separate():
    history=prompt_for(fixture_case(),'full_history','FIXED_SKILL')
    curated=prompt_for(fixture_case(),'curated_checkpoint','FIXED_SKILL')
    assert 'HISTORY_ONLY_SENTINEL' in history and 'CURATED_ONLY_SENTINEL' not in history
    assert 'CURATED_ONLY_SENTINEL' in curated and 'HISTORY_ONLY_SENTINEL' not in curated
    for rendered in (history,curated):
        assert 'GOLD_LABEL_MUST_NOT_BE_SENT' not in rendered
        assert 'FUTURE_OUTCOME_MUST_NOT_BE_SENT' not in rendered


def test_recovery_exposes_logs_only_after_request_and_closes_request_channel():
    initial=prompt_for(fixture_case(),'stale_recovery','FIXED_SKILL')
    final=prompt_for(fixture_case(),'stale_recovery','FIXED_SKILL',recovery={'answer':'unknown','request_logs':True})
    first=json.loads(initial.split('PUBLIC EVIDENCE:\n')[1])
    second=json.loads(final.split('PUBLIC EVIDENCE:\n')[1])
    assert first['logs_available_on_request'] is True and first['public_history']==[]
    assert second['logs_available_on_request'] is False and second['public_history']
    assert 'STALE_ONLY_SENTINEL' in initial and 'HISTORY_ONLY_SENTINEL' not in initial
    assert 'HISTORY_ONLY_SENTINEL' in final


def test_memory_writer_does_not_see_later_question_or_gold():
    from scripts.probe_agent_written_notes import writer_prompt
    c=fixture_case()
    c['question']='FUTURE_QUIZ_MUST_NOT_BE_SENT'
    rendered=writer_prompt(c,'FIXED_SKILL',128)
    assert 'HISTORY_ONLY_SENTINEL' in rendered
    assert 'FUTURE_QUIZ_MUST_NOT_BE_SENT' not in rendered
    assert 'GOLD_LABEL_MUST_NOT_BE_SENT' not in rendered
