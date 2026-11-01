"""Record explicitly chosen manual actions and publish a local live snapshot.

This helper never selects actions or calls a model. Runtime files are local.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('command', choices=['new', 'step', 'observe'])
parser.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parents[2])
parser.add_argument('--version', default='v0.2-growth')
parser.add_argument('--label', default='Run 02 · Growth with a reserve')
parser.add_argument('--skills', type=Path)
args = parser.parse_args()
runtime = args.workspace.resolve() / '.career-lab'
runtime.mkdir(exist_ok=True)
active_path = runtime / 'active-manual.json'


def api(op, **data):
    req = urllib.request.Request('http://127.0.0.1:8765/api/' + op,
        data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)['data']


if args.command == 'new':
    sid = api('new')['session_id']
    run = runtime / 'runs' / sid
    run.mkdir(parents=True)
    meta = {'session_id': sid, 'run_dir': str(run), 'version': args.version,
            'run_label': args.label, 'actions': 0, 'history': [], 'decisions': []}
    if args.skills:
        meta['skill_sha256'] = {p.parent.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in args.skills.glob('*/SKILL.md')}
else:
    meta = json.loads(active_path.read_text())
    run = Path(meta['run_dir'])

sid = meta['session_id']
before = api('observe', session_id=sid)
record = {'observation_before': before}
if args.command == 'step':
    request = json.load(sys.stdin)
    choices = {c['choice']: c for c in before.get('choices', [])}
    if request['choice'] not in choices:
        raise SystemExit('Selected choice is not currently offered; no action sent.')
    result = api('action', session_id=sid, choice=request['choice'], notes=request['notes'])
    if isinstance(result, dict) and result.get('success') is False:
        raise SystemExit('Simulator rejected action; observe before retrying.')
    meta['actions'] += 1
    st = before['current_state']
    chosen = {'number': meta['actions'], 'month': st['time']['current_month'],
              'level': st['status']['level'], 'action': choices[request['choice']]['action'],
              'notes': request['notes']}
    meta['last_action'] = chosen
    meta['decisions'] = (meta['decisions'] + [chosen])[-8:]
    record.update(action=request, action_result=result)

obs = api('observe', session_id=sid)
logs = api('logs', session_id=sid)
record.update(observation=obs, logs=logs)
with (run / 'observations.jsonl').open('a') as f:
    f.write(json.dumps(record) + '\n')
state = obs['current_state']
meta['history'].append({'month': state['time']['current_month'], **state['status']})
ending = next((e['message'] for e in logs.get('entries', []) if e['entry_type'] == 'ending_score'), None)
reason = state.get('simulation_flags', {}).get('failure_reason') or ''
meta['status'] = ('completed' if 'Completed the 48-month simulation' in reason else 'eliminated') if not obs.get('choices') else 'running'
if ending:
    meta['ending_report'] = ending
    match = re.search(r'Quantitative score: ([\d.]+)', ending)
    if match:
        meta['quantitative_score'] = float(match[1])
meta['updated_at'] = datetime.now(timezone.utc).isoformat()
active_path.write_text(json.dumps(meta, indent=2))
snapshot = {k: v for k, v in meta.items() if k not in ('run_dir', 'skill_sha256')}
snapshot['observation'] = obs
temp = runtime / 'live.tmp'
temp.write_text(json.dumps(snapshot))
temp.replace(runtime / 'live.json')
event = obs.get('current_event')
if isinstance(event, dict) and 'rules' in event:
    event = {k: v for k, v in event.items() if k in ('title', 'remaining_energy')}
print(json.dumps({'month': state['time']['current_month'], 'status': state['status'],
    'flags': state['simulation_flags'], 'event': event,
    'choices': [{k:v for k,v in c.items() if k in ('choice','action','energy_cost','status_updates')}
                for c in obs.get('choices',[])], 'feedback': obs.get('events'),
    'outcome': [e['message'] for e in logs.get('entries', [])[-2:]
                if e['entry_type'] in ('event','ending_score','failure')]}, ensure_ascii=False))
