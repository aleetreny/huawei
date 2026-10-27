import asyncio, json, sys, uuid, shutil, random
from pathlib import Path
sys.path.insert(0, "/home/user/huawei")
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase
async def main():
    spec = ServerSpec("probe", Path("/home/user/rx/srv"+uuid.uuid4().hex[:6]))
    async with GameClient(spec, Settings()) as c:
        sid = await c.new_game()
        out=[]
        for i in range(40):
            obs = await c.observe(sid)
            out.append(obs)
            if is_terminal(obs): break
            ch = obs["choices"]
            r = await c.call("take_action", {"session_id": sid, "choice": ch[0]["choice"], "notes": ""})
            out.append({"REPLY": r})
        logs = await c.logs(sid, 200)
        out.append({"LOGS": logs})
    json.dump(out, open("/home/user/rx/probe.json","w"), indent=1, ensure_ascii=False)
    shutil.rmtree(spec.root, ignore_errors=True)
asyncio.run(main())
