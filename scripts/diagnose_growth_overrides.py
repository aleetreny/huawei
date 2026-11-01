"""Describe the 101 historical risk-increasing overrides using public archives only."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.trust_risk_study import FrozenKnowledge
from scripts.balanced_growth_study import bonus


def diagnose(source,output):
    archive=source/"public-trajectories.jsonl.gz"
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest==(source/"archive-sha256.txt").read_text().strip()
    k=FrozenKnowledge(json.loads((source/"frozen-effects.json").read_text()),json.loads((source/"frozen-hazards.json").read_text()))
    cases=[];titles=Counter();months=Counter();costs=Counter();immediate=Counter()
    with gzip.open(archive,"rt") as stream:
        for line in stream:
            r=json.loads(line)
            if r["assignment"]["arm"]!="balanced":continue
            for i,s in enumerate(r["steps"]):
                d=s["diagnostic"]
                if s["phase"]!="event" or not d["growth_override"] or not s["prior_explosions_before"]:continue
                common=next(c for c in s["before"]["choices"] if c["choice"]==d["common_choice"])
                chosen=s["choice"]
                if k.hazard_rate(chosen)<=k.hazard_rate(common):continue
                before=s["before"]["current_state"]["status"];after=s["after"]["current_state"]["status"]
                ce,be=k.effect(chosen),k.effect(common)
                losses=[stat for stat in ("wealth","health","dignity") if ce.get(stat,0)<be.get(stat,0)]
                costs.update(losses)
                event=s["before"]["current_event"];title=event["title"];month=s["before"]["current_state"]["time"]["current_month"]
                titles[title]+=1;months[month]+=1
                adverse=any(x in s["after"].get("events","") for x in ("Old landmines","Trust crisis"))
                immediate["adverse_reply"]+=adverse
                memory={"prior_explosions":s["prior_explosions_before"]}
                cases.append({"run":r["run"],"step":i,"month":month,"event":event,"status_before":before,
                    "chosen":chosen,"common_unexecuted":common,"chosen_nominal":ce,"common_nominal":be,
                    "chosen_hazard_lookup":k.hazard_rate(chosen),"common_hazard_lookup":k.hazard_rate(common),
                    "chosen_growth_bonus":bonus(s["before"],chosen,"balanced",k,memory),
                    "common_growth_bonus":bonus(s["before"],common,"balanced",k,memory),
                    "worse_nominal_resources":losses,"realized_status_delta":{key:after[key]-before[key] for key in ce if key in after and isinstance(after[key],(int,float))},
                    "reply_events":s["after"].get("events",""),"immediate_adverse":adverse,
                    "final_flags":r["final"]["current_state"]["simulation_flags"]})
    result={"archive_sha256":digest,"cases":cases,"count":len(cases),"unique_runs":len({c["run"] for c in cases}),
        "titles":dict(titles.most_common()),"months":dict(sorted(months.items())),"worse_nominal_resources":dict(costs),
        "immediate_adverse_responses":immediate["adverse_reply"],
        "limits":["Selected historical choices, not a randomized subset or estimate of causal harm", "Common alternative was never executed in the same state", "Hazards are smoothed historical associations, not true action risks", "No access to simulator internals"]}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({key:value for key,value in result.items() if key!="cases"},indent=2))


if __name__=="__main__":diagnose(Path(sys.argv[1]),Path(sys.argv[2]))
