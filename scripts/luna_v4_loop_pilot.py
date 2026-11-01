"""Two isolated native-Luna pilots; explicit ordered calls to public MCP tools only."""
import argparse
import asyncio
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json, result_from_terminal
from careerlab.mcp_client import GameClient, HttpServer, ServerSpec, is_terminal, month_index, phase
from careerlab.store import bundle_hash


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root):
    protocol = json.loads((root.parent / 'protocol.json').read_text())
    assert digest(root.parent / 'protocol.json') == (root.parent / 'protocol-sha256.txt').read_text().strip()
    assert bundle_hash(root.parent / 'bundle') == protocol['bundle_sha256']
    assert digest(Path(__file__).resolve()) == protocol['transport_sha256']
    return protocol


def connection(root, protocol):
    game = root.name
    settings = Settings(origin='matteoluna2', data_dir=root, lab_dir=root / 'lab')
    spec = ServerSpec(game, root / 'server', transport='http', port=protocol['ports'][game], competition_mode=True)
    return spec, settings


def serve(root):
    protocol = load(root)
    spec, settings = connection(root, protocol)
    with HttpServer(spec, settings) as server:
        atomic_write_json(root / 'server-process.json', {'pid': server.proc.pid, 'port': spec.port, 'started_at': now()})
        print(json.dumps({'ready': True, 'game': root.name, 'port': spec.port}), flush=True)
        server.proc.wait()


async def call(root):
    protocol = load(root)
    request = json.load(sys.stdin)
    calls = request.get('calls', [request])
    assert isinstance(calls, list) and 1 <= len(calls) <= 12
    allowed = {'new_game', 'observe', 'take_action', 'check_latest_logs', 'show_employee_handbook'}
    assert all(item.get('tool') in allowed for item in calls), 'Only the five public game tools'
    status = json.loads((root / 'status.json').read_text())
    assert status['status'] not in ('completed', 'eliminated'), 'Game is already terminal'
    status['batches'] += 1
    batch = status['batches']
    atomic_write_json(root / 'status.json', status)
    spec, settings = connection(root, protocol)
    output = []
    async with GameClient(spec, settings) as client:
        for index, item in enumerate(calls):
            tool = item['tool']
            args = {}
            if tool == 'new_game':
                assert not status['new_game_attempts'], 'Exactly one new_game per pilot'
                status['new_game_attempts'] = 1
                status['status'] = 'starting'
                atomic_write_json(root / 'status.json', status)
            elif tool != 'show_employee_handbook':
                assert status.get('session_id'), 'No game session'
                args['session_id'] = status['session_id']
            if tool == 'take_action':
                args.update(choice=int(item['choice']), notes=str(item.get('notes', '')))
            if tool == 'check_latest_logs':
                args['count'] = int(item.get('count', 8))
            entry = {'timestamp': now(), 'batch': batch, 'batch_size': len(calls), 'batch_index': index, 'tool': tool, 'args': args}
            with (root / 'requests.jsonl').open('a') as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + '\n')
            try:
                response = await client.call(tool, args)
                entry['response'] = response
                status['tool_calls'][tool] = status['tool_calls'].get(tool, 0) + 1
                if tool == 'new_game':
                    status['session_id'] = response['session_id']
                    status['status'] = 'playing'
                if tool == 'take_action':
                    status['actions'] += 1
                    status['rejected'] += int(not response.get('success'))
                if tool == 'observe':
                    previous = status.get('last_observation') or {}
                    previous_month = month_index(previous)
                    previous_phase = phase(previous)
                    status['last_observation'] = response
                    status['last_state'] = response.get('current_state')
                    status['month'] = month_index(response)
                    if previous_month and previous_phase in ('energy', 'main_action') and status['month'] > previous_month and previous_month % 3 == 0:
                        checkpoint = {'quarter_month': previous_month, 'observed_month': status['month'], 'state': status['last_state'], 'events': response.get('events'), 'actions': status['actions'], 'rejected': status['rejected'], 'timestamp': now()}
                        with (root / 'checkpoints.jsonl').open('a') as handle:
                            handle.write(json.dumps(checkpoint, ensure_ascii=False) + '\n')
                    if is_terminal(response):
                        result = result_from_terminal(root.name, status['session_id'], response)
                        result.steps = status['actions']
                        result.rejected_actions = status['rejected']
                        result.tool_calls = status['tool_calls']
                        result.trajectory_path = str(root / 'trajectory.jsonl')
                        atomic_write_json(root / 'result.json', asdict(result))
                        status['status'] = result.outcome
            except Exception as exc:
                entry['error'] = repr(exc)
                with (root / 'trajectory.jsonl').open('a') as handle:
                    handle.write(json.dumps(entry, ensure_ascii=False) + '\n')
                atomic_write_json(root / 'status.json', status)
                raise
            with (root / 'trajectory.jsonl').open('a') as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + '\n')
            status['updated_at'] = now()
            atomic_write_json(root / 'status.json', status)
            output.append({'tool': tool, 'response': response})
            if status['status'] in ('completed', 'eliminated'):
                break
    print(json.dumps({'batch': batch, 'results': output, 'status': status['status']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['serve', 'call'])
    parser.add_argument('--root', required=True, type=Path)
    options = parser.parse_args()
    if options.command == 'serve':
        serve(options.root)
    else:
        asyncio.run(call(options.root))
