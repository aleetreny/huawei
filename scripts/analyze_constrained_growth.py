"""Archive the new cohort and report preplanned filter contrasts and delivery."""
from collections import Counter,defaultdict
import gzip
import json
import math
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.analyze_growth_gap import analyze
from scripts.analyze_financial_reserve import METRICS


def summarize(source,output):
    analyze(source,output)
    shutil.copyfile(source/"design-input-diagnosis.json",output/"design-input-diagnosis.json")
    r=json.loads((output/"results.json").read_text());delivery=defaultdict(Counter);by_phase=defaultdict(Counter)
    with gzip.open(output/"public-trajectories.jsonl.gz","rt") as stream:
        for line in stream:
            record=json.loads(line);arm=record["assignment"]["arm"]
            for step in record["steps"]:
                d=step["diagnostic"];g=delivery[arm];g["decisions"]+=1
                if d.get("growth_override"):g["growth_overrides"]+=1
                if d.get("filter_changed_choice"):
                    g["filter_changes"]+=1;by_phase[step["phase"]]["filter_changes"]+=1
                    unconstrained=str(d["unconstrained_choice"])
                    for reason in d["rejected"][unconstrained]:
                        g["changed_because_"+reason]+=1
                for reasons in d.get("rejected",{}).values():
                    for reason in reasons:g["candidate_rejections_"+reason]+=1
    contrasts={}
    for off,on in (("control","balanced"),("control","constrained"),("balanced","constrained")):
        contrast={}
        for metric in METRICS:
            a=r["arms"][off]["metrics"][metric];b=r["arms"][on]["metrics"][metric]
            if a["rate"] is None or b["rate"] is None:contrast[metric]=None;continue
            p0,p1=a["rate"],b["rate"];lo0,hi0=a["wilson95"];lo1,hi1=b["wilson95"];d=p1-p0
            contrast[metric]={"difference":d,"newcombe95":[d-math.sqrt((p1-lo1)**2+(hi0-p0)**2),d+math.sqrt((hi1-p1)**2+(p0-lo0)**2)]}
        contrasts[on+"_minus_"+off]=contrast
    r["planned_contrasts"]=contrasts;r["filter_delivery"]={a:dict(c) for a,c in delivery.items()}
    r["filter_changes_by_phase"]={phase:dict(c) for phase,c in by_phase.items()}
    r["limits"].append("Filter delivery and same-state rejected alternatives do not estimate the causal effect of an individual veto or its component")
    (output/"results.json").write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"planned_contrasts":{name:{m:c[m] for m in ("second_promotion_and_alive","alive_through_12","trust_death")} for name,c in contrasts.items()},"filter_delivery":r["filter_delivery"],"filter_changes_by_phase":r["filter_changes_by_phase"]},indent=2))


if __name__=="__main__":summarize(Path(sys.argv[1]),Path(sys.argv[2]))
