"""Describe pre-review drawdowns in existing public archives; never infer caps or replay choices."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def analyze(path):
    counts = Counter()
    witnesses = []
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            run = json.loads(line)
            counts['runs'] += 1
            # Identify public review output, never a hidden threshold.
            review = next((i for i, s in enumerate(run['steps'])
                           if 'Half-year performance bonus' in s['after'].get('events', '')), None)
            if review is None:
                counts['no_review_message'] += 1
                continue
            counts['review_message'] += 1
            review_step = run['steps'][review]
            promoted = (review_step['after']['current_state']['status']['level'] !=
                        review_step['before']['current_state']['status']['level'])
            counts['promoted'] += promoted
            best = {}
            losses = []
            for i, step in enumerate(run['steps'][:review + 1]):
                before = step['before']['current_state']
                for key in ('skill', 'network', 'output'):
                    best[key] = max(best.get(key, before['status'][key]), before['status'][key])
                if i == review:
                    break  # review-bearing transition mixes choice and automatic settlement
                after = step['after']['current_state']
                if not step.get('applied') or before['status']['level'] != after['status']['level']:
                    continue
                lost = [k for k in ('network', 'output') if after['status'][k] < before['status'][k]]
                if lost:
                    losses.append({'step': i, 'month': before['time']['current_month'],
                                   'stats': ','.join(lost), 'before': before['status'], 'after': after['status']})
            last = run['steps'][review]['before']['current_state']
            deficits = [k for k in ('network', 'output') if last['status'][k] < best[k]]
            group = 'promoted' if promoted else 'not_promoted'
            counts[group + '_review_n'] += 1
            counts[group + '_any_observed_net_output_loss'] += bool(losses)
            counts[group + '_last_snapshot_below_running_best'] += bool(deficits)
            counts[group + '_no_observed_net_output_loss'] += not losses
            counts['non_review_net_output_loss_transitions'] += len(losses)
            witnesses.append({'run': run['run'], 'promoted': promoted,
                              'review_transition': review, 'snapshot_month': last['time']['current_month'],
                              'snapshot': last['status'], 'running_best': best, 'deficits': deficits,
                              'losses': losses})
    assert counts['runs'] == counts['review_message'] + counts['no_review_message']
    assert counts['review_message'] == counts['promoted_review_n'] + counts['not_promoted_review_n']
    return {'source': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'counts': dict(counts)}, witnesses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('sources', nargs='+', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    results, rows = [], []
    for source in args.sources:
        result, witnesses = analyze(source)
        results.append(result)
        rows.extend({'source': str(source), **w} for w in witnesses)
    (args.output / 'results.json').write_text(json.dumps({'scope': 'Retrospective public-state description; no caps, readiness gold, counterfactuals or actor adherence identified.', 'collections': results}, indent=2) + '\n')
    with (args.output / 'witnesses.jsonl').open('w') as stream:
        for row in rows:
            stream.write(json.dumps(row) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
