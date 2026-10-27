"""Frozen, quota-free reserve exploration with assignment before new_game."""
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
from scripts.second_review_search import decide, remember, value
from scripts.trust_risk_study import FrozenKnowledge


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reserve_term(wealth,delta,target=2,weight=6):
    # Private research heuristic, not a published safety cutoff or Skill rule.
    return weight*(min(target,wealth+delta)-min(target,wealth))-max(0,-delta)


def select(obs,arm,k,memory,rng,config):
    default,reason=decide(obs,k,memory,"balanced","safe",rng)
    if phase(obs)!="event":
        return default,reason,{"base_choice":default["choice"],"cash_override":False}
    def base(c):
        score=value(obs,c,k,memory,"balanced")
        if memory.get("prior_explosions",0)>0:
            score-=40*k.hazard_rate(c)
        return score
    baseline=max(obs["choices"],key=base)
    wealth=obs["current_state"]["status"]["wealth"]
    def cash(c):
        delta=k.effect(c).get("wealth",0)
        return reserve_term(wealth,delta,config["reserve_target"],config["reserve_weight"])
    chosen=max(obs["choices"],key=lambda c:base(c)+(cash(c) if arm=="reserve" else 0))
    return chosen,"reserve_aware_narrative" if arm=="reserve" else "common_incident_aware_narrative",{
        "base_choice":baseline["choice"],"cash_override":chosen["choice"]!=baseline["choice"],
        "wealth_before":wealth,"nominal_wealth_delta":k.effect(chosen).get("wealth",0),
        "base_nominal_wealth_delta":k.effect(baseline).get("wealth",0),
        "reserve_score_term":cash(chosen) if arm=="reserve" else 0}


def prepare(args):
    root=args.root
    root.mkdir(parents=True,exist_ok=False)
    source=args.model
    for name in ("effects","hazards"):
        shutil.copyfile(source/f"frozen-{name}.json",root/f"frozen-{name}.json")
    rng=random.Random(args.seed)
    schedule=[]
    for _ in range(args.per_arm):
        pair=["baseline","reserve"]
        rng.shuffle(pair)
        schedule.extend(pair)
    dependencies={}
    (root/"sources").mkdir()
    for p in (Path(__file__),Path("scripts/trust_risk_study.py"),Path("scripts/second_review_search.py"),Path("scripts/first_review_search.py"),Path("careerlab/mcp_client.py")):
        dependencies[str(p.resolve())]=sha(p)
        shutil.copyfile(p,root/"sources"/(p.parent.name+"-"+p.name))
    cfg=Settings(origin="matteocash",data_dir=root,lab_dir=root/"lab")
    protocol={"name":"financial-reserve-v1","date":"2026-10-27","actor":"Python research bot; no LLM",
        "per_arm":args.per_arm,"schedule":schedule,"seed":args.seed,"assignment":"Before new_game, permuted blocks of two; no eligibility or survivor filtering",
        "model_source":str(source.resolve()),"effects_sha256":sha(root/"frozen-effects.json"),"hazards_sha256":sha(root/"frozen-hazards.json"),
        "dependencies":dependencies,"environment":ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg),
        "common_policy":"Frozen balanced manual-inspired default, no exploration or model updates. Both arms retain public incident memory from the start; after an explosion apply the same empirical hazard penalty. State-dependent quarterly actions in both arms, no forced cleanup calendar.",
        "config":{"reserve_target":2,"reserve_weight":6},
        "intervention":"For narrative choices only, add 6*(min(2,Wealth+nominal_delta)-min(2,Wealth))-max(0,-nominal_delta). Nominal delta from the frozen public-log lookup. Other priorities unchanged.",
        "primary":"L2-to-L3 by month12 and alive at the first month13 observation, on all assigned new games",
        "secondary":["Broke failure","first promotion by month6","first promotion and alive at month7","second promotion by month12","survival","Trust crisis","Health failure","Wealth at first month7 observation","financial choice overrides"],
        "stop":"Fixed schedule, finish every assigned game at death or first observation after month12; never act in month13; no outcome-based early stopping",
        "analysis":"Arm counts, Wilson95 rate intervals and Newcombe95 differences reserve minus baseline; exploratory, no Skill superiority or universal guarantee",
        "technical":"Record every assigned slot including new_game failures. Interruptions remain unknown, not failure or success; do not replace or retry slots automatically",
        "limitations":["Independent unseeded histories, not identical-state counterfactuals","Reserve heuristic uses a lookup, not a general reasoning agent",
            "The numeric reserve target is a research setting, not an identified engine threshold","Public nominal changes can differ from net settlement",
            "Do not compare raw rates to the earlier month6-eligible study","No statement about consequences beyond month12"]}
    atomic_write_json(root/"protocol.json",protocol)
    (root/"protocol-sha256.txt").write_text(sha(root/"protocol.json")+"\n")
    print(json.dumps({"prepared":True,"assigned_slots":len(schedule),"per_arm":args.per_arm}),flush=True)


async def episode(client,root,index,arm,k,protocol):
    assignment={"position":index,"arm":arm,"when":"before new_game"}
    r={"run":index,"assignment":assignment,"arm":["financial-reserve",arm],"steps":[],"outcome":"interrupted"}
    atomic_write_json(root/f"run-{index:05d}.json",r)
    memory={"prior_explosions":0}
    rng=random.Random(protocol["seed"]+index)
    try:
        sid=await client.new_game()
        r["session_id"]=sid
        obs=await client.observe(sid)
        r["initial_observation"]=obs
        for i in range(300):
            if is_terminal(obs) or month_index(obs)>12:
                r["outcome"]="eliminated" if is_terminal(obs) else "twelve_month_window"
                break
            choice,reason,diagnostic=select(obs,arm,k,memory,rng,protocol["config"])
            result=await client.take_action(sid,choice["choice"],f"Frozen reserve research: {reason}",obs)
            after=await client.observe(sid)
            r["steps"].append({"before":obs,"after":after,"choice":choice,"phase":phase(obs),"reason":reason,
                "diagnostic":diagnostic,"prior_explosions_before":memory["prior_explosions"],
                "reply":result.reply,"applied":result.applied,"ambiguous":result.ambiguous})
            if not result.applied or result.ambiguous:
                raise RuntimeError(f"Unconfirmed public action: {result.reply}")
            remember(obs,choice,after,memory)
            memory["prior_explosions"]+="Old landmines" in after.get("events","")
            obs=after
        else:
            raise RuntimeError("step cap")
        r["final"]=obs
        r["logs"]=await client.logs(sid,100)
    except Exception as exc:
        r["error"]=repr(exc)
    atomic_write_json(root/f"run-{index:05d}.json",r)
    return r


async def run(args):
    root=args.root
    protocol=json.loads((root/"protocol.json").read_text())
    if sha(root/"protocol.json")!=(root/"protocol-sha256.txt").read_text().strip():
        raise ValueError("Frozen protocol changed")
    for file,expected in protocol["dependencies"].items():
        if sha(Path(file))!=expected:
            raise ValueError(f"Frozen dependency changed: {file}")
    for kind in ("effects","hazards"):
        if sha(root/f"frozen-{kind}.json")!=protocol[f"{kind}_sha256"]:
            raise ValueError("Frozen empirical model changed")
    if list(root.glob("run-*.json")) or (root/"assignments.json").exists():
        raise ValueError("Run already started; no silent restart or replacement")
    cfg=Settings(origin="matteocash",data_dir=root,lab_dir=root/"lab")
    if ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg)!=protocol["environment"]:
        raise ValueError("Environment changed")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    assignments=[]
    next_index=0
    outcomes=Counter()
    async def worker(worker_id):
        nonlocal next_index
        while next_index<len(protocol["schedule"]):
            index=next_index;next_index+=1
            arm=protocol["schedule"][index]
            assignment={"position":index,"arm":arm,"when":"before new_game"}
            assignments.append(assignment)
            atomic_write_json(root/"assignments.json",assignments)
            initial={"run":index,"assignment":assignment,"arm":["financial-reserve",arm],"steps":[],"outcome":"interrupted"}
            atomic_write_json(root/f"run-{index:05d}.json",initial)
            spec=ServerSpec(f"cash-{index}",root/"servers"/str(index),competition_mode=True)
            try:
                async with GameClient(spec,cfg) as client:
                    if index==0:
                        atomic_write_json(root/"handbook.json",await client.handbook())
                    r=await episode(client,root,index,arm,k,protocol)
            except Exception as exc:
                r=json.loads((root/f"run-{index:05d}.json").read_text())
                r["infrastructure_error"]=repr(exc)
                atomic_write_json(root/f"run-{index:05d}.json",r)
            outcomes[r["outcome"]]+=1
            atomic_write_json(root/"status.json",{"assigned":next_index,"target":len(protocol["schedule"]),"outcomes":dict(outcomes)})
            if sum(outcomes.values())%64==0 or r.get("error") or r.get("infrastructure_error"):
                print(json.dumps({"finished":sum(outcomes.values()),"assigned":next_index,"outcomes":dict(outcomes)}),flush=True)
    await asyncio.gather(*(worker(i) for i in range(args.workers)))
    print(json.dumps({"done":True,"assigned":next_index,"outcomes":dict(outcomes)}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    prep=sub.add_parser("prepare")
    prep.add_argument("--root",type=Path,required=True)
    prep.add_argument("--model",type=Path,default=Path("lab/reports/trust-risk-study/factorial-v1"))
    prep.add_argument("--per-arm",type=int,default=256)
    prep.add_argument("--seed",type=int,default=610027)
    runner=sub.add_parser("run")
    runner.add_argument("--root",type=Path,required=True)
    runner.add_argument("--workers",type=int,default=4)
    args=p.parse_args()
    prepare(args) if args.command=="prepare" else asyncio.run(run(args))
