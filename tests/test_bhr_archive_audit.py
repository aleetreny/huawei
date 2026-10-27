"""Protect the offline audit against mixed archive schemas and settlement leakage."""
import gzip
import json

from scripts.audit_bhr_archives import analyze


def observation(network=4, level='L1', events=''):
    return {'current_state': {'status': {'skill': 3, 'network': network, 'output': 2, 'level': level},
                              'time': {'current_month': 5}}, 'events': events}


def write_archive(tmp_path, runs):
    path = tmp_path / 'public.jsonl.gz'
    with gzip.open(path, 'wt') as stream:
        for run in runs:
            stream.write(json.dumps(run) + '\n')
    return path


def test_promotion_comes_from_first_review_transition_not_run_flag(tmp_path):
    step = {'before': observation(), 'after': observation(level='L2', events='Half-year performance bonus'), 'applied': True}
    result, _ = analyze(write_archive(tmp_path, [{'run': 0, 'steps': [step]},
                                               {'run': 1, 'promoted': False, 'steps': [step]}]))
    assert result['counts']['promoted'] == 2
    assert result['counts']['review_message'] == 2


def test_review_settlement_loss_is_excluded_and_missing_reviews_retained(tmp_path):
    before_review = {'before': observation(), 'after': observation(network=3), 'applied': True}
    review = {'before': observation(network=3),
              'after': observation(network=1, events='Half-year performance bonus'), 'applied': True}
    result, rows = analyze(write_archive(tmp_path, [{'run': 0, 'steps': [before_review, review]},
                                                  {'run': 1, 'steps': []}]))
    assert result['counts']['non_review_net_output_loss_transitions'] == 1
    assert result['counts']['no_review_message'] == 1
    assert rows[0]['deficits'] == ['network']
    assert rows[0]['snapshot']['network'] == 3
    assert rows[0]['losses'][0]['step'] == 0
