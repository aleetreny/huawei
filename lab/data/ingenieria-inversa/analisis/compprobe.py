import asyncio, json, sys, uuid, shutil
from pathlib import Path
sys.path.insert(0, "/home/user/huawei")
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase
async def main(comp):
    spec = ServerSpec("cp", Path("/home/user/rx/srv"+uuid.uuid4().hex[:6]), competition_mode=comp)
    async with GameClient(spec, Settings()) as c:
        tools = await c._client.list_tools() if hasattr(c,'_client') else None
        sid = await c.new_game()
        obs = await c.observe(sid)
        out={'obs0':obs}
        r = await c.call("take_action", {"session_id": sid, "choice": 1, "notes": "x"})
        obs = await c.observe(sid); out['obs1']=obs; out['reply']=r
        logs = await c.logs(sid, 50); out['logs']=logs
        hb = await c.handbook(); out['handbook_len']=len(hb); out['handbook_head']=hb[:300]
        print(json.dumps(out, ensure_ascii=False)[:3000])
    shutil.rmtree(spec.root, ignore_errors=True)
asyncio.run(main(sys.argv[1]=='1'))
