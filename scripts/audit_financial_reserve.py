"""Verify public outcomes, full-start assignment and replay frozen decisions."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.financial_reserve_study import select
from scripts.trust_risk_study import FrozenKnowledge
from scripts.second_review_search import remember


def audit(root):
    protocol=json.loads((root/"protocol.json").read_text())
    for file,hashfile in (("protocol.json","protocol-sha256.txt"),("public-trajectories.jsonl.gz","archive-sha256.txt")):
        if hashlib.sha256((root/file).read_bytes()).hexdigest()!=(root/hashfile).read_text().strip():
            raise ValueError("Integrity mismatch")
    for file,expected in protocol["dependencies"].items():
        if hashlib.sha256(Path(file).read_bytes()).hexdigest()!=expected:
            raise ValueError("Policy replay dependency changed")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    assignments=json.loads((root/"assignments.json").read_text())
    if len({a["position"] for a in assignments})!=len(assignments):
        raise ValueError("Duplicate assigned slot")
    with gzip.open(root/"public-trajectories.jsonl.gz","rt") as stream:
        records=[json.loads(line) for line in stream]
    by_run={r["run"]:r for r in records}
    generated=[]
    rng=random.Random(protocol["seed"])
    for _ in range(protocol["per_arm"]):
        pair=["baseline","reserve"];rng.shuffle(pair);generated.extend(pair)
    if generated!=protocol["schedule"]:
        raise ValueError("Random schedule not reproducible")
    counts=defaultdict(Counter);replayed=0
    for a in assignments:
        index=a["position"];arm=a["arm"]
        if generated[index]!=arm or a["when"]!="before new_game":
            raise ValueError("Assignment mismatch")
        r=by_run[index]
        if r["assignment"]!=a:
            raise ValueError("Assignment journal mismatch")
        counts[arm]["assigned"]+=1
        if r["outcome"] not in ("eliminated","twelve_month_window"):
            counts[arm]["interrupted"]+=1;continue
        if not r["steps"] or r["steps"][0]["before"]!=r["initial_observation"]:
            raise ValueError("Missing complete initial prefix")
        if r["initial_observation"]["current_state"]["time"]["current_month"]>1:
            raise ValueError("History starts too late")
        memory={"prior_explosions":0};choice_rng=random.Random(protocol["seed"]+index)
        observations=[];first=False;second=False
        previous=None
        for s in r["steps"]:
            if previous is not None and s["before"]!=previous:
                raise ValueError("Public history gap")
            previous=s["after"]
            if not s.get("applied") or s.get("ambiguous") or s.get("reply",{}).get("success") is not True:
                raise ValueError("Unconfirmed action")
            if s["choice"] not in s["before"]["choices"]:
                raise ValueError("Action was not offered")
            if s["before"]["current_state"]["time"]["current_month"]>12:
                raise ValueError("Action outside horizon")
            if s["prior_explosions_before"]!=memory["prior_explosions"]:
                raise ValueError("Incident memory differs from past public history")
            expected,reason,diagnostic=select(s["before"],arm,k,memory,choice_rng,protocol["config"])
            if expected!=s["choice"] or reason!=s["reason"] or diagnostic!=s["diagnostic"]:
                raise ValueError(f"Frozen policy replay mismatch: run {index}")
            replayed+=1
            remember(s["before"],s["choice"],s["after"],memory)
            memory["prior_explosions"]+="Old landmines" in s["after"].get("events","")
            b=s["before"]["current_state"];after=s["after"]["current_state"]
            lb,la=int(b["status"]["level"][1:]),int(after["status"]["level"][1:])
            first|=la>lb and after["time"]["current_month"]<=6
            second|=lb==2 and la>=3 and after["time"]["current_month"]<=12
            observations.extend((s["before"],s["after"]))
        final=r["final"]["current_state"];flags=final["simulation_flags"]
        dead=flags.get("alive") is False or flags.get("failed") is True
        alive=not dead and final["time"]["current_month"]==13
        if alive!=(r["outcome"]=="twelve_month_window"):
            raise ValueError("Public outcome differs from record")
        reason=flags.get("failure_reason") or ""
        reached7=any(o["current_state"]["time"]["current_month"]==7 and o["current_state"]["simulation_flags"].get("alive") is not False
            and not o["current_state"]["simulation_flags"].get("failed") for o in observations)
        row=counts[arm];row["resolved"]+=1
        for metric,answer in {"broke":dead and "Broke" in reason,"trust_death":dead and "Trust crisis" in reason,
            "health_death":dead and "Blackout" in reason,"first_promotion_by_6":first,
            "first_promoted_alive_at_7":first and reached7,"second_promotion_by_12":second,
            "second_promotion_and_alive":second and alive,"alive_through_12":alive}.items():row[metric]+=answer
    reported=json.loads((root/"results.json").read_text())
    for arm,c in counts.items():
        if reported["arms"][arm]["assigned"]!=c["assigned"]:
            raise ValueError("Assigned denominator mismatch")
        for metric,v in reported["arms"][arm]["metrics"].items():
            if v["count"]!=c[metric]:raise ValueError("Reported outcome differs from raw states")
    result={"verified":True,"assigned":len(assignments),"source_records":len(records),"replayed_actions":replayed,
        "groups":{k:dict(v) for k,v in counts.items()},"scope":"All initial assignments retained, every resolved public choice replayed under frozen policy, no future incident memory, outcomes reconstructed independently"}
    (root/"independent-audit.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="groups"},indent=2))


if __name__=="__main__":
    audit(Path(sys.argv[1]))
