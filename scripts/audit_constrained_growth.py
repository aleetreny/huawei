"""Replay safety-filter study decisions and independently verify the nominal constraints."""
from collections import Counter,defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.constrained_growth_study import select,excluded_reasons
from scripts.trust_risk_study import FrozenKnowledge
from scripts.second_review_search import remember


def audit(root):
    p=json.loads((root/"protocol.json").read_text())
    selector=select
    assert p["name"]=="safety-constrained-growth-v1"
    for file,hashfile in (("protocol.json","protocol-sha256.txt"),("public-trajectories.jsonl.gz","archive-sha256.txt")):
        if hashlib.sha256((root/file).read_bytes()).hexdigest()!=(root/hashfile).read_text().strip():raise ValueError("Integrity mismatch")
    for file,digest in p["dependencies"].items():
        if hashlib.sha256(Path(file).read_bytes()).hexdigest()!=digest:raise ValueError("Replay dependency changed")
    if hashlib.sha256((root/"design-input-diagnosis.json").read_bytes()).hexdigest()!=p["diagnosis_sha256"]:raise ValueError("Design diagnosis mismatch")
    for kind in ("effects","hazards"):
        if hashlib.sha256((root/f"frozen-{kind}.json").read_bytes()).hexdigest()!=p[f"{kind}_sha256"]:raise ValueError("Frozen model mismatch")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    with gzip.open(root/"public-trajectories.jsonl.gz","rt") as stream:records=[json.loads(line) for line in stream]
    assignments=json.loads((root/"assignments.json").read_text());by_run={r["run"]:r for r in records}
    if len(records)!=len(assignments) or len(by_run)!=len(records):raise ValueError("Duplicate or missing records")
    if sorted(a["position"] for a in assignments)!=list(range(len(p["schedule"]))):raise ValueError("Initial schedule coverage mismatch")
    generated=[];rng=random.Random(p["seed"])
    for _ in range(p["per_arm"]):
        block=list(p["arms"]);rng.shuffle(block);generated.extend(block)
    if generated!=p["schedule"]:raise ValueError("Random schedule mismatch")
    counts=defaultdict(Counter);override_trace=defaultdict(Counter);replayed=0;constraint_checks=0;unknown_common=0
    for a in assignments:
        index=a["position"];arm=a["arm"];r=by_run[index]
        if generated[index]!=arm or r["assignment"]!=a or a["when"]!="before new_game":raise ValueError("Assignment mismatch")
        counts[arm]["assigned"]+=1
        if r["outcome"] not in ("eliminated","twelve_month_window"):
            counts[arm]["interrupted"]+=1;continue
        if r["steps"][0]["before"]!=r["initial_observation"] or r["initial_observation"]["current_state"]["time"]["current_month"]>1:raise ValueError("Initial prefix missing")
        memory={"prior_explosions":0};rng_choice=random.Random(p["seed"]+index);previous=None;first=False;second=False;observations=[]
        for s in r["steps"]:
            if previous is not None and s["before"]!=previous:raise ValueError("History gap")
            previous=s["after"]
            if not s.get("applied") or s.get("ambiguous") or s.get("reply",{}).get("success") is not True or s["choice"] not in s["before"]["choices"]:raise ValueError("Unconfirmed/unoffered action")
            if s["before"]["current_state"]["time"]["current_month"]>12:raise ValueError("Action outside horizon")
            if s["prior_explosions_before"]!=memory["prior_explosions"]:raise ValueError("Incident memory mismatch")
            expected,reason,diagnostic=selector(s["before"],arm,k,memory,rng_choice,p["config"])
            if expected!=s["choice"] or reason!=s["reason"] or diagnostic!=s["diagnostic"]:raise ValueError(f"Policy replay mismatch: {index}")
            if arm=="constrained":
                common=next(c for c in s["before"]["choices"] if c["choice"]==diagnostic["common_choice"])
                # Separate assertions in addition to replaying the selector.
                status=s["before"]["current_state"]["status"]
                chosen_effect=k.effect(s["choice"]);common_effect=k.effect(common)
                for stat,floor in p["config"]["safety_floors"].items():
                    if max(0,floor-status[stat]-chosen_effect.get(stat,0))>max(0,floor-status[stat]-common_effect.get(stat,0)):raise ValueError("Nominal resource bound violated")
                if s["phase"]=="event" and memory["prior_explosions"] and k.hazard_rate(s["choice"])>k.hazard_rate(common):raise ValueError("Post-incident hazard bound violated")
                if s["choice"]!=common and not chosen_effect:raise ValueError("Unknown-effect alternative selected")
                constraint_checks+=1;unknown_common+=not common_effect
            if s["phase"]=="event" and diagnostic.get("growth_override"):
                override_trace[arm]["narrative_overrides"]+=1
                common=next(c for c in s["before"]["choices"] if c["choice"]==diagnostic["common_choice"])
                if memory["prior_explosions"] and k.hazard_rate(s["choice"])>k.hazard_rate(common):override_trace[arm]["higher_empirical_rate_after_incident"]+=1
            replayed+=1;remember(s["before"],s["choice"],s["after"],memory);memory["prior_explosions"]+="Old landmines" in s["after"].get("events","")
            b=s["before"]["current_state"];after=s["after"]["current_state"];lb=int(b["status"]["level"][1:]);la=int(after["status"]["level"][1:])
            first|=la>lb and after["time"]["current_month"]<=6;second|=lb==2 and la>=3 and after["time"]["current_month"]<=12
            observations.extend((s["before"],s["after"]))
        if previous!=r["final"]:raise ValueError("Final state differs from prefix")
        f=r["final"]["current_state"];flags=f["simulation_flags"];dead=flags.get("alive") is False or flags.get("failed") is True
        alive=not dead and f["time"]["current_month"]==13
        if alive!=(r["outcome"]=="twelve_month_window"):raise ValueError("Outcome mismatch")
        reached7=any(o["current_state"]["time"]["current_month"]==7 and o["current_state"]["simulation_flags"].get("alive") is not False and not o["current_state"]["simulation_flags"].get("failed") for o in observations)
        reason=flags.get("failure_reason") or "";row=counts[arm];row["resolved"]+=1
        for metric,answer in {"broke":dead and "Broke" in reason,"trust_death":dead and "Trust crisis" in reason,"health_death":dead and "Blackout" in reason,
            "first_promotion_by_6":first,"first_promoted_alive_at_7":first and reached7,"second_promotion_by_12":second,
            "second_promotion_and_alive":second and alive,"alive_through_12":alive}.items():row[metric]+=answer
    reported=json.loads((root/"results.json").read_text())
    for arm,c in counts.items():
        if reported["arms"][arm]["assigned"]!=c["assigned"]:raise ValueError("Denominator mismatch")
        for metric,v in reported["arms"][arm]["metrics"].items():
            if v["count"]!=c[metric]:raise ValueError("Reported outcome differs from public states")
    result={"verified":True,"assigned":len(assignments),"replayed_actions":replayed,"groups":{k:dict(v) for k,v in counts.items()},
        "narrative_override_trace":{k:dict(v) for k,v in override_trace.items()},
        "nominal_constraint_decisions_verified":constraint_checks,"common_unknown_effect_decisions":unknown_common,
        "scope":"Complete initial denominators, reproducible blocked assignment, past-only incident memory, every public action replayed and outcomes independently reconstructed"}
    (root/"independent-audit.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps({k:v for k,v in result.items() if k!="groups"},indent=2))


if __name__=="__main__":audit(Path(sys.argv[1]))
