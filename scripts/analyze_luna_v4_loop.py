"""Audit two finished native-Luna pilots from their public MCP trajectories."""
import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import month_index, phase
from careerlab.store import bundle_hash


def analyze(root, out):
    protocol = json.loads((root / 'protocol.json').read_text())
    assert bundle_hash(root / 'bundle') == protocol['bundle_sha256']
    summaries = []
    for game in ('game-1', 'game-2'):
        directory = root / game
        result = json.loads((directory / 'result.json').read_text())
        entries = [json.loads(line) for line in (directory / 'trajectory.jsonl').read_text().splitlines()]
        assert result['outcome'] in ('completed', 'eliminated')
        assert sum(e['tool'] == 'new_game' for e in entries) == 1
        assert not any(e.get('error') for e in entries), 'Transport error requires explicit audit'
        notes = [e['args'].get('notes', '') for e in entries if e['tool'] == 'take_action']
        assert all(len(note) <= 1000 for note in notes)
        batches = collections.defaultdict(list)
        for entry in entries:
            batches[entry['batch']].append(entry)
        observation = None
        story_batches = paired_story_batches = quarter_batches = 0
        for batch in batches.values():
            tools = [e['tool'] for e in batch]
            if observation and phase(observation) == 'event' and 'take_action' in tools:
                story_batches += 1
                paired_story_batches += int(tools == ['take_action', 'observe'])
            elif observation and phase(observation) in ('energy', 'main_action') and 'take_action' in tools:
                quarter_batches += 1
            for entry in batch:
                if entry['tool'] == 'observe':
                    observation = entry['response']
        reviews = {}
        blowup_months = set()
        levels = []
        previous_level = None
        for entry in entries:
            if entry['tool'] != 'observe':
                continue
            obs = entry['response']
            month = month_index(obs)
            stats = obs.get('current_state', {}).get('status', {})
            current_level = stats.get('level')
            if current_level != previous_level:
                levels.append({'month': month, 'level': current_level})
                previous_level = current_level
            if 'Old landmines all go off at once' in str(obs.get('events', '')):
                blowup_months.add(month)
            grade = re.search(r'Half-year performance bonus \(([SABCD])\)', str(obs.get('events', '')))
            if grade:
                reviews[month] = grade.group(1)
        checkpoint_path = directory / 'checkpoints.jsonl'
        checkpoints = [json.loads(x) for x in checkpoint_path.read_text().splitlines()] if checkpoint_path.exists() else []
        summary = {'game': game, 'outcome': result['outcome'], 'score': result['quantitative_score'],
                   'survival_months': result['survival_months'], 'failure_reason': result['failure_reason'],
                   'final_stats': observation.get('current_state', {}).get('status'),
                   'actions': result['steps'], 'rejected_actions': result['rejected_actions'],
                   'new_game_attempts': 1, 'public_calls': dict(collections.Counter(e['tool'] for e in entries)),
                   'native_bridge_batches': len(batches), 'story_batches': story_batches,
                   'paired_story_batches': paired_story_batches, 'quarter_batches': quarter_batches,
                   'reviews': reviews, 'level_transitions': levels, 'public_blowup_months': sorted(blowup_months),
                   'note_field_coverage': {field: sum(field in note for note in notes) for field in ('Review in ', 'Now S', 'Best S', 'Stalled:', 'Concerns this month:')},
                   'note_chars_max': max(map(len, notes), default=0),
                   'note_chars_median': statistics.median(map(len, notes)) if notes else 0,
                   'public_trajectory_sha256': hashlib.sha256((directory / 'trajectory.jsonl').read_bytes()).hexdigest(),
                   'limits': protocol['limits']}
        (out / game).mkdir(parents=True, exist_ok=True)
        for name in ('result.json', 'status.json', 'checkpoints.jsonl'):
            path = directory / name
            if path.exists():
                if name == 'status.json':
                    status = json.loads(path.read_text())
                    status.pop('last_observation', None)
                    (out / game / name).write_text(json.dumps(status, indent=2, ensure_ascii=False))
                else:
                    (out / game / name).write_bytes(path.read_bytes())
        with gzip.GzipFile(filename=str(out / game / 'public-trajectory.jsonl.gz'), mode='wb', mtime=0) as handle:
            handle.write((directory / 'trajectory.jsonl').read_bytes())
        (out / game / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
        summaries.append(summary)
    combined = {'model_requested': protocol['model_requested'], 'new_games': 2, 'complete': True,
                'mean_score': statistics.mean(s['score'] for s in summaries),
                'completed_careers': sum(s['outcome'] == 'completed' for s in summaries),
                'games': summaries, 'limits': protocol['limits']}
    (out / 'summary.json').write_text(json.dumps(combined, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in combined.items() if k != 'games'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('out', type=Path)
    options = parser.parse_args()
    analyze(options.root, options.out)
