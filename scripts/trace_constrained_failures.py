"""Trace residual filter failures and pre-incident exposures; no causal attribution."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.trust_risk_study import FrozenKnowledge


def trace(root):
    archive=root/"public-trajectories.jsonl.gz"
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=(root/"archive-sha256.txt").read_text().strip():raise ValueError("Archive mismatch")
    k=FrozenKnowledge(json.loads((root/"frozen-effects.json").read_text()),json.loads((root/"frozen-hazards.json").read_text()))
    cases=[];exposures=Counter();per_death=Counter()
    with gzip.open(archive,"rt") as stream:
        for line in stream:
            r=json.loads(line)
            if r["assignment"]["arm"]!="constrained":continue
            flags=r["final"]["current_state"]["simulation_flags"]
            trust="Trust crisis" in (flags.get("failure_reason") or "")
            timeline=[]
            for i,s in enumerate(r["steps"]):
                d=s["diagnostic"];common=next(c for c in s["before"]["choices"] if c["choice"]==d["common_choice"])
                override=d["growth_override"]
                higher=s["phase"]=="event" and k.hazard_rate(s["choice"])>k.hazard_rate(common)
                if override and s["phase"]=="event":
                    key="before_first_incident" if not s["prior_explosions_before"] else "after_prior_incident"
                    exposures[key+"_overrides"]+=1
                    exposures[key+"_higher_empirical_hazard"]+=higher
                events=s["after"].get("events","")
                incident="Old landmines" in events;crisis="Trust crisis" in events
                if trust and (override or d.get("filter_changed_choice") or incident or crisis):
                    timeline.append({"step":i,"month":s["before"]["current_state"]["time"]["current_month"],
                        "phase":s["phase"],"event":s["before"].get("current_event"),"choice":s["choice"],
                        "common_unexecuted":common,"prior_incidents":s["prior_explosions_before"],
                        "growth_override":override,"filter_changed":d.get("filter_changed_choice",False),
                        "chosen_hazard_lookup":k.hazard_rate(s["choice"]),"common_hazard_lookup":k.hazard_rate(common),
                        "status_before":s["before"]["current_state"]["status"],"status_after":s["after"]["current_state"]["status"],"events":events})
            if trust:
                last=r["steps"][-1];d=last["diagnostic"]
                per_death["fatal_choice_matches_common"]+=not d["growth_override"]
                per_death["earlier_growth_overrides"]+=any(t["growth_override"] for t in timeline[:-1])
                per_death["prior_public_incident"]+=last["prior_explosions_before"]>0
                cases.append({"run":r["run"],"final_flags":flags,"timeline":timeline,
                    "fatal_step":len(r["steps"])-1,"fatal_choice_matches_common":not d["growth_override"]})
    result={"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"exposure_counts":dict(exposures),
        "trust_failures":len(cases),"trust_failure_profiles":dict(per_death),"cases":cases,
        "limits":["Actual public histories and unexecuted same-state baseline choices only", "An earlier override is not proof it caused a later crisis", "The filter only bounds selected empirical and nominal comparisons; it does not establish true risk"]}
    (root/"residual-failure-traces.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({key:value for key,value in result.items() if key!="cases"},indent=2))


if __name__=="__main__":trace(Path(sys.argv[1]))
