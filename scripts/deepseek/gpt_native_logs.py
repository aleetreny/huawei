"""Fetch our completed pilot's player logs through the official log tool only.
No new_game, no actor/model call, no direct database or package inspection.
"""
import asyncio,json,collections,hashlib
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from careerlab.config import Settings
from careerlab.mcp_client import ServerSpec,GameClient
DATA=Path.home()/'careerlab-data/deepseek/gpt-native-pilot'
async def main():
    for d in sorted(DATA.glob('game-*')):
        p=d/'result.json';out=d/'official-player-logs.json'
        if not p.exists() or out.exists():continue
        r=json.loads(p.read_text())
        if not r.get('session_id'):continue
        async with GameClient(ServerSpec('own-native-logs-'+d.name,d/'game'),Settings()) as c:logs=await c.logs(r['session_id'],5000)
        out.write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
        es=logs.get('entries') or []
        print(json.dumps({'game':d.name,'entries':len(es),'types':dict(collections.Counter(e.get('entry_type') for e in es)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':asyncio.run(main())
