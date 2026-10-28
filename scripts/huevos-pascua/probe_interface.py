"""Sondeo de la interfaz oficial: campos completos de observe, manual del juego y respuesta de
take_action a entradas fuera del menu. Solo las 5 herramientas oficiales, servidor local, sin modelo.
Uso: probe_interface.py <carpeta_de_salida>
"""
import asyncio, json, sys, uuid, shutil
from pathlib import Path
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

def keys(d, pre=''):
    out = []
    if isinstance(d, dict):
        for k, v in d.items():
            out.append(pre + k); out += keys(v, pre + k + '.')
    return out

async def main():
    root = OUT / ('srv-' + uuid.uuid4().hex[:8])
    spec = ServerSpec('probe', root)
    async with GameClient(spec, Settings()) as c:
        hb = await c.call('show_employee_handbook', {})
        (OUT / 'handbook.json').write_text(json.dumps(hb, ensure_ascii=False, indent=1))
        sid = await c.new_game()
        obs = await c.observe(sid)
        (OUT / 'observe0.json').write_text(json.dumps(obs, ensure_ascii=False, indent=1))
        print('observe keys:', keys(obs))
        r = await c.call('take_action', {'session_id': sid, 'choice': 1, 'notes': ''})
        print('continue ->', str(r)[:300])
        obs = await c.observe(sid)
        (OUT / 'observe1.json').write_text(json.dumps(obs, ensure_ascii=False, indent=1))
        print('observe1 keys:', keys(obs))
        n = len(obs.get('choices') or [])
        for ch in (0, -1, n + 1, 99, 10**9):
            try:
                r = await c.call('take_action', {'session_id': sid, 'choice': ch, 'notes': ''})
            except Exception as e:
                r = 'EXC ' + repr(e)[:200]
            print('choice', ch, '->', str(r)[:300])
        for bad in ({'session_id': sid, 'choice': '1', 'notes': ''}, {'session_id': sid, 'choice': 1.5, 'notes': ''},
                    {'session_id': sid, 'choice': 1, 'notes': '', 'extra': 'x'}, {'session_id': 'nope', 'choice': 1, 'notes': ''}):
            try:
                r = await c.call('take_action', bad)
            except Exception as e:
                r = 'EXC ' + repr(e)[:200]
            print('args', {k: v for k, v in bad.items() if k != 'session_id'}, '->', str(r)[:300])
        obs2 = await c.observe(sid)
        print('same state after bad inputs:', obs2.get('current_state') == obs.get('current_state'))
        logs = await c.logs(sid, 50)
        (OUT / 'logs.json').write_text(json.dumps(logs, ensure_ascii=False, indent=1))
        print('log keys', keys(logs)[:20])
    shutil.rmtree(root, ignore_errors=True)

asyncio.run(main())
