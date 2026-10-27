import asyncio, json, sys, uuid, shutil, random
from pathlib import Path
sys.path.insert(0, "/home/user/huawei")
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase
async def game(c, rng):
    sid = await c.new_game(); over=[]
    while True:
        obs = await c.observe(sid)
        if is_terminal(obs) or obs["current_state"]["time"]["current_month"]>int(sys.argv[4]): break
        st=obs["current_state"]["status"]
        if st["level"]=="L1" and (st["network"]>3 or st["output"]>3 or st["skill"]>9):
            over.append((obs["current_state"]["time"]["current_month"], st["skill"],st["network"],st["output"]))
        ch=obs["choices"]
        await c.call("take_action", {"session_id": sid, "choice": rng.choice(ch)["choice"], "notes": ""})
    return over
async def main(nserv, ngames):
    rng=random.Random(int(sys.argv[3]))
    for sv in range(nserv):
        spec = ServerSpec("f", Path("/home/user/rx/srv"+uuid.uuid4().hex[:6]))
        async with GameClient(spec, Settings()) as c:
            res=[]
            for i in range(ngames):
                o=await game(c,rng); res.append(o[-3:] if o else 0)
            print("server",sv,res, flush=True)
        shutil.rmtree(spec.root, ignore_errors=True)
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
