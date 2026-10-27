"""Cold-read own completed historical session through official public tools only."""
import asyncio
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec


async def audit(run, out):
    out.mkdir(parents=True, exist_ok=False)
    result = json.loads((run/'result.json').read_text())
    assert result['outcome'] == 'completed' and result['session_id']
    config = json.loads((run/'mcp.json').read_text())['mcpServers']['career-emulator-engine']
    # Configuration is ours; no database/log file is opened or inspected.
    game_root = Path(config['env']['CAREER_EMULATOR_DB']).parent
    expected, subtypes, log_calls, timestamps = [], Counter(), 0, []
    stream = run/'stream-0.jsonl'
    for line in stream.read_text().splitlines():
        r = json.loads(line)
        if r.get('timestamp'):
            timestamps.append(r['timestamp'])
        if r.get('type') == 'system':
            subtypes[r.get('subtype', '')] += 1
        if r.get('type') == 'assistant':
            for b in r.get('message', {}).get('content', []):
                if b.get('type') != 'tool_use':
                    continue
                if b.get('name', '').endswith('take_action'):
                    expected.append(b.get('input', {}).get('notes', ''))
                if b.get('name', '').endswith('check_latest_logs'):
                    log_calls += 1
    spec = ServerSpec('historical-note-recovery', game_root, competition_mode=False)
    settings = Settings(origin='matteonotes')
    async with GameClient(spec, settings) as client:
        observation = await client.observe(result['session_id'])
        logs = await client.logs(result['session_id'], 1000)
    returned = [e['message'].split('\nNotes: ', 1)[1] for e in logs['entries'] if '\nNotes: ' in e['message']]
    matches = Counter(expected) & Counter(returned)
    data = {'retrieved_at': datetime.now(timezone.utc).isoformat(), 'historical_run': str(run),
            'stream_sha256': hashlib.sha256(stream.read_bytes()).hexdigest(), 'original_result': result,
            'original_tool_notes': expected, 'public_observation': observation, 'public_logs': logs,
            'original_timestamp_range_if_exposed': [timestamps[0], timestamps[-1]] if timestamps else None,
            'system_event_counts': dict(subtypes), 'player_log_requests': log_calls,
            'action_notes_sent': len(expected), 'notes_returned': len(returned), 'exact_multiset_matches': sum(matches.values()),
            'unmatched_expected_notes': list((Counter(expected)-Counter(returned)).elements()),
            'limits': ['Historical witness, not randomized memory efficacy trial',
                       'No compact_boundary in an archive does not prove no backend/context transformation',
                       'A cold client/server recovery is not a fresh model recall test',
                       'No fixed retention TTL inferred from one historical retrieval']}
    (out/'recovery.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: data[k] for k in ('action_notes_sent','notes_returned','exact_multiset_matches','system_event_counts','player_log_requests')}))


if __name__ == '__main__':
    asyncio.run(audit(Path(sys.argv[1]), Path(sys.argv[2])))
