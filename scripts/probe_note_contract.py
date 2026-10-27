"""Public-tool boundary and session-isolation probes; no model calls."""
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec

CASES = [('omitted', None), ('null', None), ('number', 123), ('boolean', True),
         ('array', ['fact']), ('object', {'fact': 'test'}), ('spaces', '  '),
         ('whitespace_edges', '  CONTRACT_EDGE  \n'), ('newline', '\n'),
         ('normal', 'CONTRACT_NORMAL'), ('empty', '')]


async def run(root, out):
    root.mkdir(parents=True, exist_ok=False)
    out.mkdir(parents=True, exist_ok=False)
    protocol = {'name': 'notes-contract-v1', 'at': datetime.now(timezone.utc).isoformat(),
                'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'cases': CASES, 'sessions': 2, 'competition_mode': False,
                'stop': 'Boundary probes only; sessions intentionally not completed, never included in promotion outcomes',
                'method': 'Same persistent server/client, two public sessions, invalid choice plus note types, observe after each call',
                'limits': 'Development multi-session test; does not claim competition permits multiple games'}
    (out/'protocol.json').write_text(json.dumps(protocol, indent=2)+'\n')
    settings = Settings(origin='matteonotes', data_dir=root)
    spec = ServerSpec('contract', root/'server', competition_mode=False)
    calls = []
    async with GameClient(spec, settings) as c:
        async def call(tool, args):
            row = {'tool': tool, 'args': args}
            calls.append(row)
            try:
                row['response'] = await c.call(tool, args)
                return row['response']
            except Exception as exc:
                row['error'] = repr(exc)
                return {'probe_error': repr(exc)}
        sids = [(await call('new_game', {}))['session_id'] for _ in range(2)]
        results = []
        for index, sid in enumerate(sids):
            before = await call('observe', {'session_id': sid})
            await call('take_action', {'session_id': sid, 'choice': before['choices'][0]['choice'], 'notes': f'CONTRACT_SESSION_{index}_DOCUMENT'})
            before = await call('observe', {'session_id': sid})
            invalid = await call('take_action', {'session_id': sid, 'choice': -999, 'notes': f'CONTRACT_SESSION_{index}_INVALID'})
            after = await call('observe', {'session_id': sid})
            invalid_state_unchanged = before == after
            rows = []
            for name, value in CASES:
                args = {'session_id': sid, 'choice': after['choices'][0]['choice']}
                if name != 'omitted':
                    args['notes'] = value
                reply = await call('take_action', args)
                next_obs = await call('observe', {'session_id': sid})
                rows.append({'case': name, 'reply': reply, 'observation_changed': after != next_obs})
                after = next_obs
            await call('take_action', {'session_id': sid, 'choice': after['choices'][0]['choice'], 'notes': f'CONTRACT_SESSION_{index}_VALID'})
            logs = await call('check_latest_logs', {'session_id': sid, 'count': 1000})
            text = json.dumps(logs, ensure_ascii=False)
            results.append({'session': index, 'invalid_choice_reply': invalid, 'invalid_choice_state_unchanged': invalid_state_unchanged,
                            'note_type_results': rows, 'public_logs': logs,
                            'own_valid_marker_present': f'CONTRACT_SESSION_{index}_VALID' in text,
                            'own_document_marker_present': f'CONTRACT_SESSION_{index}_DOCUMENT' in text,
                            'invalid_choice_marker_present': f'CONTRACT_SESSION_{index}_INVALID' in text,
                            'other_session_marker_present': f'CONTRACT_SESSION_{1-index}_' in text})
    (out/'results.json').write_text(json.dumps({'sessions': results, 'public_calls': calls}, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'sessions': [{k: v for k, v in r.items() if k not in ('public_logs','note_type_results')} for r in results], 'public_calls': len(calls)}))


if __name__ == '__main__':
    asyncio.run(run(Path(sys.argv[1]), Path(sys.argv[2])))
