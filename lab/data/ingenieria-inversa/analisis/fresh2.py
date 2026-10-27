import asyncio, json, sys, uuid, shutil, random
from pathlib import Path
sys.path.insert(0, "/home/user/huawei")
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase
EFF=json.load(open("/home/user/rx/eff.json"))
def score(title, c, st):
    d=EFF.get(title+"||"+c["action"])
    if d is None: return 0
    v=d.get("network",0)+d.get("output",0)+d.get("skill",0)
    if st["health"]+d.get("health",0)<=2: v-=20
    if st["dignity"]+d.get("dignity",0)<=2: v-=20
    return v
async def game(c, rng):
    sid = await c.new_game(); traj=[]
    while True:
        obs = await c.observe(sid)
        if is_terminal(obs) or obs["current_state"]["time"]["current_month"]>int(sys.argv[3]): break
        st=obs["current_state"]["status"]; m=obs["current_state"]["time"]["current_month"]
        traj.append((m,st["level"],st["skill"],st["network"],st["output"]))
        ch=obs["choices"]; ph=phase(obs)
        if ph=="event":
            t=obs["current_event"]["title"]; best=max(ch,key=lambda x:score(t,x,st))
        elif ph=="energy":
            left=obs["current_event"].get("remaining_energy",0)
            opts=[x for x in ch if x.get("energy_cost",0)<=left]
            best=next((x for x in opts if x["action"]=="Health recovery"), None) if st["health"]<6 else next((x for x in opts if x["action"]=="Network maintenance"),None)
            best=best or [x for x in ch if x.get("energy_cost",0)==0][0]
        elif ph=="main_action":
            best=next(x for x in ch if x["action"]=="Apply for a key project")
        else: best=ch[0]
        await c.call("take_action", {"session_id": sid, "choice": best["choice"], "notes": ""})
    return traj
async def main(nserv, ngames):
    rng=random.Random(1)
    for sv in range(nserv):
        spec = ServerSpec("f", Path("/home/user/rx/srv"+uuid.uuid4().hex[:6]))
        async with GameClient(spec, Settings()) as c:
            for i in range(ngames):
                tr=await game(c,rng)
                over=[t for t in tr if t[1]=="L1" and (t[3]>3 or t[4]>3 or t[2]>9)]
                print("server",sv,"game",i,"overcap steps",len(over),"months",sorted(set(t[0] for t in over)),"max",max([t[3] for t in tr]), flush=True)
        shutil.rmtree(spec.root, ignore_errors=True)
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
