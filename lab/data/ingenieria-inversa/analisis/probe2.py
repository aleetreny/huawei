import asyncio, json, sys, uuid, shutil, random
from pathlib import Path
sys.path.insert(0, "/home/user/huawei"); sys.path.insert(0,"/home/user/huawei/scripts/ingenieria-inversa")
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase
import policies
async def main():
    spec = ServerSpec("probe", Path("/home/user/rx/srv"+uuid.uuid4().hex[:6]))
    pol=policies.Base(int(sys.argv[1])); ctx=pol.new_game("x")
    async with GameClient(spec, Settings()) as c:
        sid = await c.new_game()
        while True:
            obs = await c.observe(sid)
            if is_terminal(obs): print("END",obs["current_state"]["simulation_flags"]); break
            m=obs["current_state"]["time"]["current_month"]
            ch,_=pol.decide(obs,ctx)
            if m>=int(sys.argv[2]):
                st=obs["current_state"]["status"]
                print(m, phase(obs), {k:st[k] for k in ("health","dignity","skill","network","output","level","duration_in_level","wealth")}, (obs.get("current_event") or {}).get("title","")[:30], "| EV:", (obs.get("events") or "").replace("\n"," ")[:160])
            if m>int(sys.argv[3]): break
            await c.call("take_action", {"session_id": sid, "choice": ch, "notes": ""})
        L=await c.logs(sid, 40)
        for e in L["entries"][-25:]: print("  LOG",e["entry_type"], e["message"][:110].replace("\n"," / "))
    shutil.rmtree(spec.root, ignore_errors=True)
asyncio.run(main())
