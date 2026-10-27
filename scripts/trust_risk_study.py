"""Public-tool, quota-free factorial exploration of second-window trust failures.

Frozen empirical bot. Random assignment at the first full month-six energy menu
after a first promotion. No engine internals, state clones, or gameplay LLMs.
"""
from __future__ import annotations
import argparse
import asyncio
from collections import Counter, defaultdict
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index, phase
from scripts.second_review_search import Knowledge, decide, remember, update_warnings, value

ARMS=[{"cleanup6":a,"cleanup9":b,"incident_guard":c} for a,b,c in itertools.product((False,True),repeat=3)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arm_key(arm):
    return "".join(str(int(arm[k])) for k in ("cleanup6","cleanup9","incident_guard"))


def archive_records(path):
    with gzip.open(path,"rt") as stream:
        for line in stream:
            yield json.loads(line)


def adverse(step):
    return any(w in step["after"].get("events","") for w in ("Old landmines","Trust crisis"))


def eligible(obs):
    return (not is_terminal(obs) and month_index(obs)==6 and phase(obs)=="energy"
        and obs["current_state"]["status"]["level"]=="L2"
        and (obs.get("current_event") or {}).get("remaining_energy")==3)


def prepare(args):
    root=args.root
    root.mkdir(parents=True,exist_ok=False)
    k=Knowledge()
    hazards=defaultdict(Counter)
    sources=[]
    for evidence_root in args.evidence:
        for archive in sorted(evidence_root.glob("*/public-trajectories.jsonl.gz")):
            expected=(archive.parent/"archive-sha256.txt").read_text().split()[0]
            if sha(archive)!=expected:
                raise ValueError(f"Archive hash mismatch: {archive}")
            sources.append({"path":str(archive.resolve()),"sha256":expected})
            for r in archive_records(archive):
                k.ingest(r)
                for s in r["steps"]:
                    if s["phase"]!="event" or not s.get("applied") or s.get("ambiguous"):
                        continue
                    action=s["choice"]["action"]
                    hazards[action]["observations"]+=1
                    hazards[action]["adverse_responses"]+=adverse(s)
    effects={action:{stat:sum(xs)/len(xs) for stat,xs in eff.items()} for action,eff in k.effects.items()}
    atomic_write_json(root/"frozen-effects.json",effects)
    atomic_write_json(root/"frozen-hazards.json",{a:dict(c) for a,c in hazards.items()})
    schedule=[]
    rng=random.Random(args.seed)
    for _ in range(args.per_arm):
        block=list(range(len(ARMS)))
        rng.shuffle(block)
        schedule.extend(block)
    dependency_files=[Path(__file__),Path("scripts/second_review_search.py"),Path("scripts/first_review_search.py"),Path("careerlab/mcp_client.py")]
    snapshots=root/"sources"
    snapshots.mkdir()
    dependencies={}
    for p in dependency_files:
        dependencies[str(p.resolve())]=sha(p)
        shutil.copyfile(p,snapshots/(p.parent.name+"-"+p.name))
    cfg=Settings(origin="matteotrust",data_dir=root,lab_dir=root/"lab")
    protocol={"name":"trust-risk-factorial-v1","date":"2026-10-27","actor":"Python bot; no LLM",
        "arms":ARMS,"per_arm":args.per_arm,"eligible_assignments":len(schedule),"attempt_cap":args.attempts,
        "choice_seed":args.seed,"schedule":schedule,"sources":sources,"dependencies":dependencies,
        "effects_sha256":sha(root/"frozen-effects.json"),"hazards_sha256":sha(root/"frozen-hazards.json"),
        "environment":ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg),
        "assignment":"Permuted blocks of eight assigned in order of reaching the first full month-six energy menu alive at L2; prefix independent of arm",
        "plans":{"cleanup":["Defuse legacy risk","Health recovery"],"growth":["Prepare report materials","Prepare report materials","Health recovery"]},
        "guard":"Only after at least one earlier public Old landmines response: subtract 40 * smoothed empirical adverse-response frequency from the base narrative score. It is a historical association, not an identified action risk.",
        "guard_rate":"(adverse_responses + 1)/(observations + 4); unseen action rate 1/4",
        "prefix":"Frozen balanced manual-inspired default, no exploration; no online model updates",
        "after_assignment":"Same frozen state-dependent narrative/main policy in every arm, except guard; force assigned full energy plan in months six and nine, then common default",
        "primary":"Terminal official Trust crisis by first observation of month13 among assigned games; never condition this denominator on post-assignment promotion or survival",
        "secondary":["L2-to-L3 by month12","L2-to-L3 and alive at first month13 observation","all-cause survival","public explosions","intervention delivery","technical interruptions"],
        "stop":"Complete scheduled assignments or attempt cap; finish all started episodes, no early stop for outcomes; no actions in month13",
        "analysis":"Counts and exploratory factorial main-effect differences; Wilson intervals for binary outcome rates; no universal guarantee or Skill superiority claim",
        "limitations":["Unseeded independent games, not cloned states","Cleanup substitutes two report actions; effect includes their opportunity cost",
            "Incident guard is an empirical lookup used by a research bot, not a transferable Skill or true risk oracle",
            "Post-assignment events and choices can differ as consequences of earlier state changes",
            "Missing/interrupted episodes are not coded as failures or successes"]}
    atomic_write_json(root/"protocol.json",protocol)
    (root/"protocol-sha256.txt").write_text(sha(root/"protocol.json")+"\n")
    print(json.dumps({"prepared":True,"assignments":len(schedule),"per_arm":args.per_arm,"sources":len(sources)}))


class FrozenKnowledge:
    def __init__(self,effects,hazards):
        self.effects=effects
        self.hazards=hazards

    def observe(self,obs):
        pass

    def effect(self,choice):
        if "status_updates" in choice:
            return {k.lower():v for k,v in choice["status_updates"].items()}
        return self.effects.get(choice["action"],{})

    def hazard_rate(self,choice):
        row=self.hazards.get(choice["action"],{})
        return (row.get("adverse_responses",0)+1)/(row.get("observations",0)+4)


def selection(obs,arm,memory,k,rng,plans):
    month=month_index(obs)
    if arm is not None and phase(obs)=="energy" and month in (6,9):
        plan=plans["cleanup" if arm[f"cleanup{month}"] else "growth"]
        index=memory.setdefault("plan_positions",{}).get(month,0)
        if index<len(plan):
            choice=next((c for c in obs["choices"] if c["action"]==plan[index]),None)
            if choice is None:
                raise ValueError(f"Assigned action unavailable: {plan[index]}")
            memory["plan_positions"][month]=index+1
            return choice,"randomised_energy_plan"
        finish=next((c for c in obs["choices"] if c.get("energy_cost",0)==0),None)
        if finish:
            return finish,"finish_randomised_energy_plan"
        raise ValueError("Extra energy decision after full assigned plan")
    if arm is not None and arm["incident_guard"] and memory.get("prior_explosions",0)>0 and phase(obs)=="event":
        update_warnings(obs,memory)
        chosen=max(obs["choices"],key=lambda c:value(obs,c,k,memory,"balanced")-40*k.hazard_rate(c))
        return chosen,"persistent_incident_empirical_guard"
    return decide(obs,k,memory,"balanced","safe",rng)


async def episode(client,root,index,k,protocol,assign):
    memory={"prior_explosions":0}
    rng=random.Random(protocol["choice_seed"]+index)
    r={"run":index,"arm":["unassigned-prefix"],"assignment":None,"steps":[],"outcome":"interrupted"}
    arm=None
    try:
        sid=await client.new_game()
        r["session_id"]=sid
        obs=await client.observe(sid)
        for i in range(300):
            if is_terminal(obs) or month_index(obs)>12:
                r["outcome"]="eliminated" if is_terminal(obs) else "twelve_month_window"
                break
            if arm is None and eligible(obs):
                assignment=assign(obs,memory,index)
                if assignment is None:
                    r["outcome"]="unassigned_after_schedule_full"
                    break
                arm=protocol["arms"][assignment["arm_index"]]
                r["assignment"]=assignment
                r["arm"]=["trust-factorial",arm_key(arm)]
                atomic_write_json(root/f"run-{index:05d}.json",r)
            if arm is None and month_index(obs)>6:
                r["outcome"]="ineligible_prefix"
                break
            choice,reason=selection(obs,arm,memory,k,rng,protocol["plans"])
            result=await client.take_action(sid,choice["choice"],f"Frozen public research: {reason}",obs)
            after=await client.observe(sid)
            r["steps"].append({"before":obs,"after":after,"choice":choice,"phase":phase(obs),"reason":reason,
                "prior_explosions_before":memory["prior_explosions"],"risk_warning_before":memory.get("risk",0),
                "guard_empirical_rate":k.hazard_rate(choice),"reply":result.reply,"applied":result.applied,"ambiguous":result.ambiguous})
            if not result.applied or result.ambiguous:
                raise RuntimeError(f"Unconfirmed action: {result.reply}")
            remember(obs,choice,after,memory)
            if "Old landmines" in after.get("events",""):
                memory["prior_explosions"]+=1
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
    for p,expected in protocol["dependencies"].items():
        if sha(Path(p))!=expected:
            raise ValueError(f"Frozen dependency changed: {p}")
    if list(root.glob("run-*.json")):
        raise ValueError("Study already started; no automatic restart or duplicate assignments")
    for name in ("effects","hazards"):
        if sha(root/f"frozen-{name}.json")!=protocol[f"{name}_sha256"]:
            raise ValueError("Frozen empirical model changed")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    cfg=Settings(origin="matteotrust",data_dir=root,lab_dir=root/"lab")
    if ServerSpec("manifest",root,competition_mode=True).fingerprint(cfg)!=protocol["environment"]:
        raise ValueError("Environment changed")
    assignments=[]
    outcomes=Counter()
    next_run=0
    def assign(obs,memory,index):
        position=len(assignments)
        if position>=len(protocol["schedule"]):
            return None
        assignment={"position":position,"arm_index":protocol["schedule"][position],"run":index,
            "pre_state":obs["current_state"],"prior_explosions":memory["prior_explosions"],
            "public_warning":memory.get("risk",0)}
        assignments.append(assignment)
        atomic_write_json(root/"assignments.json",assignments)
        return assignment
    async def worker(worker_id):
        nonlocal next_run
        while next_run<protocol["attempt_cap"] and len(assignments)<len(protocol["schedule"]):
            index=next_run;next_run+=1
            spec=ServerSpec(f"trust-{index}",root/"servers"/str(index),competition_mode=True)
            try:
                async with GameClient(spec,cfg) as client:
                    if index==0:
                        atomic_write_json(root/"handbook.json",await client.handbook())
                    r=await episode(client,root,index,k,protocol,assign)
            except Exception as exc:
                path=root/f"run-{index:05d}.json"
                r=json.loads(path.read_text()) if path.exists() else {"run":index,"assignment":None,"arm":["unassigned-prefix"],"steps":[],"outcome":"interrupted"}
                r["infrastructure_error"]=repr(exc)
                atomic_write_json(root/f"run-{index:05d}.json",r)
            outcomes[r["outcome"]]+=1
            atomic_write_json(root/"status.json",{"attempts_started":next_run,"assigned":len(assignments),"target":len(protocol["schedule"]),"outcomes":dict(outcomes)})
            if sum(outcomes.values())%64==0 or r.get("error"):
                print(json.dumps({"finished":sum(outcomes.values()),"assigned":len(assignments),"outcomes":dict(outcomes)}),flush=True)
    await asyncio.gather(*(worker(i) for i in range(args.workers)))
    print(json.dumps({"done":True,"assigned":len(assignments),"target":len(protocol["schedule"]),"outcomes":dict(outcomes)}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    prep=sub.add_parser("prepare")
    prep.add_argument("--root",type=Path,required=True)
    prep.add_argument("--evidence",type=Path,nargs="+",default=[Path("lab/reports/first-review-search"),Path("lab/reports/second-review-search")])
    prep.add_argument("--per-arm",type=int,default=64)
    prep.add_argument("--attempts",type=int,default=1024)
    prep.add_argument("--seed",type=int,default=510027)
    runner=sub.add_parser("run")
    runner.add_argument("--root",type=Path,required=True)
    runner.add_argument("--workers",type=int,default=4)
    args=p.parse_args()
    prepare(args) if args.command=="prepare" else asyncio.run(run(args))
