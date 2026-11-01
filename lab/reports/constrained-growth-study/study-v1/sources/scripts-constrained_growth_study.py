"""Prospective safety-constrained growth; public-tool bot with three fresh arms."""
from __future__ import annotations
import argparse
import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index, phase
from scripts.financial_reserve_study import select as common_select, reserve_term
from scripts.second_review_search import value, remember
from scripts.trust_risk_study import FrozenKnowledge

ARMS=("control","balanced","constrained")
TARGETS={"L1":{"skill":8,"network":3,"output":3},"L2":{"skill":18,"network":6,"output":6}}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def readiness(status,targets):
    result=1.0
    for stat,target in targets.items():
        result*=min(1,max(0,status[stat])/target)
    return result


def bonus(obs,choice,stat,k,memory,weight=24):
    status=obs["current_state"]["status"]
    targets=TARGETS.get(status["level"])
    if not targets:return 0.0
    projected=dict(status)
    for key in targets:
        delta=k.effect(choice).get(key,0)
        if phase(obs) in ("energy","main_action") and delta>0 and (key,status[key],int(status["level"][1:])) in memory.get("stalled",set()):
            delta=0
        projected[key]=max(0,status[key]+delta)
    return weight*(readiness(projected,targets)-readiness(status,targets))/max(1,choice.get("energy_cost",1))


def excluded_reasons(obs,choice,common,k,memory,config):
    # Relative nominal safeguards; none is claimed to be a game cutoff.
    if choice["choice"]==common["choice"]:return []
    if not k.effect(choice):return ["unknown_nominal_effect"]
    status=obs["current_state"]["status"];eff=k.effect(choice);base=k.effect(common)
    reasons=[]
    if phase(obs)=="event" and memory.get("prior_explosions",0)>0 and k.hazard_rate(choice)>k.hazard_rate(common):
        reasons.append("post_incident_hazard")
    for stat,floor in config["safety_floors"].items():
        deficit=max(0,floor-(status[stat]+eff.get(stat,0)))
        base_deficit=max(0,floor-(status[stat]+base.get(stat,0)))
        if deficit>base_deficit:reasons.append("fragile_"+stat)
    return reasons


def select(obs,arm,k,memory,rng,config):
    from scripts.balanced_growth_study import select as joint_select
    chosen,reason,diagnostic=joint_select(obs,"control" if arm=="control" else "balanced",k,memory,rng,config)
    if arm!="constrained" or phase(obs)=="document" or reason=="respond_to_public_risk_warning":
        return chosen,reason,diagnostic
    common=next(c for c in obs["choices"] if c["choice"]==diagnostic["common_choice"])
    choices=obs["choices"]
    if phase(obs)=="energy":
        left=(obs.get("current_event") or {}).get("remaining_energy",3)
        choices=[c for c in choices if c.get("energy_cost",0)<=left]
    rejected={str(c["choice"]):excluded_reasons(obs,c,common,k,memory,config) for c in choices}
    allowed=[c for c in choices if not rejected[str(c["choice"])]]
    def score(c):
        v=value(obs,c,k,memory,"balanced")
        if phase(obs)=="event":
            if memory.get("prior_explosions",0)>0:v-=40*k.hazard_rate(c)
            v+=reserve_term(obs["current_state"]["status"]["wealth"],k.effect(c).get("wealth",0),config["reserve_target"],config["reserve_weight"])
        return v+bonus(obs,c,"balanced",k,memory,config["growth_weight"])
    filtered=max(allowed,key=score)
    return filtered,"safety_filtered_growth",{"common_choice":common["choice"],"unconstrained_choice":chosen["choice"],
        "growth_override":filtered["choice"]!=common["choice"],"filter_changed_choice":filtered["choice"]!=chosen["choice"],
        "rejected":{key:reasons for key,reasons in rejected.items() if reasons},
        "bonus":bonus(obs,filtered,"balanced",k,memory,config["growth_weight"])}


def prepare(args):
    root=args.root;root.mkdir(parents=True,exist_ok=False)
    parent=args.parent
    inherited=json.loads((parent/"protocol.json").read_text())
    if sha(parent/"protocol.json")!=(parent/"protocol-sha256.txt").read_text().strip():
        raise ValueError("Parent protocol integrity mismatch")
    for kind in ("effects","hazards"):
        if sha(parent/f"frozen-{kind}.json")!=inherited[f"{kind}_sha256"]:
            raise ValueError("Parent model integrity mismatch")
        shutil.copyfile(parent/f"frozen-{kind}.json",root/f"frozen-{kind}.json")
    schedule=[];rng=random.Random(args.seed)
    for _ in range(args.per_arm):
        block=list(ARMS);rng.shuffle(block);schedule.extend(block)
    deps={}
    (root/"sources").mkdir()
    for p in (Path(__file__),Path("scripts/balanced_growth_study.py"),Path("scripts/financial_reserve_study.py"),Path("scripts/trust_risk_study.py"),Path("scripts/second_review_search.py"),Path("scripts/first_review_search.py"),Path("careerlab/mcp_client.py")):
        deps[str(p.resolve())]=sha(p);shutil.copyfile(p,root/"sources"/(p.parent.name+"-"+p.name))
    shutil.copyfile(args.derivation/"override-diagnosis.json",root/"design-input-diagnosis.json")
    cfg=Settings(origin="matteofilter",data_dir=root,lab_dir=root/"lab")
    protocol={"name":"safety-constrained-growth-v1","date":"2026-10-27","actor":"Python research bot; no LLM","arms":ARMS,
        "schedule":schedule,"per_arm":args.per_arm,"seed":args.seed,"dependencies":deps,
        "parent_results_sha256":sha(parent/"results.json"),"diagnosis_sha256":sha(args.derivation/"override-diagnosis.json"),"effects_sha256":sha(root/"frozen-effects.json"),"hazards_sha256":sha(root/"frozen-hazards.json"),
        "environment":ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg),
        "assignment":"Before new_game; permuted blocks of three, all starting games in denominator",
        "config":{"reserve_target":1,"reserve_weight":2,"growth_weight":24,"safety_floors":{"wealth":1,"health":4,"dignity":2}},"research_targets":TARGETS,
        "common":"Light financial reserve and persistent public incident guard from new game; same frozen effects and hazards; no exploration or online learning",
        "intervention":"Three arms: common light-reserve/incident controller; unchanged joint-readiness growth; same growth with a candidate filter before ranking. After an earlier public incident, do not select narrative candidates with a higher frozen empirical hazard frequency than the common action. Across decisions, do not deepen nominal shortfalls below research floors Wealth1/Health4/Dignity2 relative to that same common action. Unknown-effect alternatives are excluded; common action is always retained. Explicit-warning cleanup and document choices remain protected. This is one combined filter package, not separate causal estimates of its components.",
        "primary":"L2-to-L3 by month12 and alive at first month13 observation, on every initial assignment",
        "secondary":["First promotion by month6","First promotion and alive at month7","Second promotion by month12","Survival","Broke","Trust crisis","Blackout","Growth choice overrides"],
        "stop":"Fixed schedule; finish all games at death or first observation after month12; no outcome-based stopping or replacement",
        "analysis":"Preplanned contrasts: balanced minus control, constrained minus control, and constrained minus balanced, all metrics with Wilson95/Newcombe95 intervals, exploratory and unadjusted. Post-treatment survivor groups descriptive only. Do not adopt from a numeric primary increase accompanied by worse survival; inconclusive intervals do not establish equivalence or safety.",
        "limitations":["Targets are research hypotheses, not published or identified promotion cutoffs","Frozen lookup bot, not an agent reading the Skill",
            "Independent unseeded histories, not cloned state counterfactuals","Changing a priority can alter later states, warnings and choices",
            "Do not infer that a single observed final action caused a review failure",
            "Nominal safety constraints do not guarantee realized outcomes or survival; floor values are design settings, not identified engine thresholds","Technical interruptions stay unknown, never coded as failure"]}
    atomic_write_json(root/"protocol.json",protocol);(root/"protocol-sha256.txt").write_text(sha(root/"protocol.json")+"\n")
    print(json.dumps({"prepared":True,"target":len(schedule),"per_arm":args.per_arm}),flush=True)


async def episode(client,root,index,arm,k,p):
    assignment={"position":index,"arm":arm,"when":"before new_game"}
    r={"run":index,"assignment":assignment,"arm":["constrained-growth",arm],"steps":[],"outcome":"interrupted"}
    atomic_write_json(root/f"run-{index:05d}.json",r)
    memory={"prior_explosions":0};rng=random.Random(p["seed"]+index)
    try:
        sid=await client.new_game();r["session_id"]=sid
        obs=await client.observe(sid);r["initial_observation"]=obs
        for step in range(300):
            if is_terminal(obs) or month_index(obs)>12:
                r["outcome"]="eliminated" if is_terminal(obs) else "twelve_month_window";break
            c,reason,diagnostic=select(obs,arm,k,memory,rng,p["config"])
            result=await client.take_action(sid,c["choice"],f"Frozen constrained-growth research: {reason}",obs)
            after=await client.observe(sid)
            r["steps"].append({"before":obs,"after":after,"choice":c,"phase":phase(obs),"reason":reason,"diagnostic":diagnostic,
                "prior_explosions_before":memory["prior_explosions"],"reply":result.reply,"applied":result.applied,"ambiguous":result.ambiguous})
            if not result.applied or result.ambiguous:raise RuntimeError(f"Unconfirmed action: {result.reply}")
            remember(obs,c,after,memory);memory["prior_explosions"]+="Old landmines" in after.get("events","");obs=after
        else:raise RuntimeError("step cap")
        r["final"]=obs;r["logs"]=await client.logs(sid,100)
    except Exception as exc:r["error"]=repr(exc)
    atomic_write_json(root/f"run-{index:05d}.json",r);return r


async def run(args):
    root=args.root;p=json.loads((root/"protocol.json").read_text())
    if sha(root/"protocol.json")!=(root/"protocol-sha256.txt").read_text().strip():raise ValueError("Protocol changed")
    for file,digest in p["dependencies"].items():
        if sha(Path(file))!=digest:raise ValueError(f"Frozen dependency changed: {file}")
    for kind in ("effects","hazards"):
        if sha(root/f"frozen-{kind}.json")!=p[f"{kind}_sha256"]:raise ValueError("Frozen model changed")
    if list(root.glob("run-*.json")) or (root/"assignments.json").exists():raise ValueError("No restart or silent replacement")
    cfg=Settings(origin="matteofilter",data_dir=root,lab_dir=root/"lab")
    if ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg)!=p["environment"]:raise ValueError("Environment changed")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    assignments=[];next_index=0;outcomes=Counter()
    async def worker(worker_id):
        nonlocal next_index
        while next_index<len(p["schedule"]):
            index=next_index;next_index+=1;arm=p["schedule"][index]
            a={"position":index,"arm":arm,"when":"before new_game"};assignments.append(a);atomic_write_json(root/"assignments.json",assignments)
            atomic_write_json(root/f"run-{index:05d}.json",{"run":index,"assignment":a,"arm":["constrained-growth",arm],"steps":[],"outcome":"interrupted"})
            try:
                async with GameClient(ServerSpec(f"gap-{index}",root/"servers"/str(index),competition_mode=True),cfg) as client:
                    if index==0:atomic_write_json(root/"handbook.json",await client.handbook())
                    r=await episode(client,root,index,arm,k,p)
            except Exception as exc:
                r=json.loads((root/f"run-{index:05d}.json").read_text());r["infrastructure_error"]=repr(exc);atomic_write_json(root/f"run-{index:05d}.json",r)
            outcomes[r["outcome"]]+=1;atomic_write_json(root/"status.json",{"assigned":next_index,"target":len(p["schedule"]),"outcomes":dict(outcomes)})
            if sum(outcomes.values())%64==0 or r.get("error"):print(json.dumps({"finished":sum(outcomes.values()),"assigned":next_index,"outcomes":dict(outcomes)}),flush=True)
    await asyncio.gather(*(worker(i) for i in range(args.workers)))
    print(json.dumps({"done":True,"assigned":next_index,"outcomes":dict(outcomes)}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest="command",required=True)
    prep=sub.add_parser("prepare");prep.add_argument("--root",type=Path,required=True)
    prep.add_argument("--parent",type=Path,default=Path("lab/reports/financial-reserve-study/calibration-v1"))
    prep.add_argument("--derivation",type=Path,default=Path("lab/reports/constrained-growth-study"))
    prep.add_argument("--per-arm",type=int,default=192);prep.add_argument("--seed",type=int,default=810027)
    runner=sub.add_parser("run");runner.add_argument("--root",type=Path,required=True);runner.add_argument("--workers",type=int,default=4)
    args=p.parse_args();prepare(args) if args.command=="prepare" else asyncio.run(run(args))
