"""Describe surviving first-year non-promoters from public histories only."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.analyze_second_review import summarize_record

TARGETS={"L1":{"skill":8,"network":3,"output":3},"L2":{"skill":18,"network":6,"output":6}}


def gaps(status):
    # Research description, not known engine promotion thresholds.
    targets=TARGETS.get(status["level"],{})
    return [stat for stat,target in targets.items() if status[stat]<target]


def diagnose(source,output):
    archive=source/"public-trajectories.jsonl.gz"
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=(source/"archive-sha256.txt").read_text().strip():
        raise ValueError("Archive integrity mismatch")
    effects=json.loads((source/"frozen-effects.json").read_text())
    groups=defaultdict(list)
    with gzip.open(archive,"rt") as stream:
        for line in stream:
            r=json.loads(line)
            if r["assignment"]["arm"]!="reserve" or r["outcome"]!="twelve_month_window":
                continue
            outcome=summarize_record(r)
            if outcome["second_promotion_by_12"]:
                continue
            group="missed_first" if not outcome["first_promotion_by_6"] else "stalled_L2"
            snapshots={}
            for month in (4,5,7,10,11):
                obs=next((s["before"] for s in r["steps"] if s["before"]["current_state"]["time"]["current_month"]==month),None)
                if obs:
                    status=obs["current_state"]["status"]
                    snapshots[str(month)]={"status":status,"proxy_gaps":gaps(status)}
            reviews=[]
            for index,s in enumerate(r["steps"]):
                if "Half-year performance bonus" not in s["after"].get("events",""):
                    continue
                b=s["before"]["current_state"]["status"]
                alternatives=[]
                for c in s["before"]["choices"]:
                    eff=effects.get(c["action"])
                    projected={**b,**{stat:max(0,b[stat]+(eff or {}).get(stat,0)) for stat in ("skill","network","output")}}
                    alternatives.append({"choice":c,"nominal_effect_known":eff is not None,"nominal_effect":eff,
                        "unclipped_nominal_projection":projected,"proxy_gaps":gaps(projected)})
                reviews.append({"step":index,"before_month":s["before"]["current_state"]["time"]["current_month"],
                    "before":b,"after":s["after"]["current_state"]["status"],"selected":s["choice"],
                    "alternatives":alternatives,"public_response":s["after"].get("events","")})
            groups[group].append({"run":r["run"],"final":r["final"]["current_state"],"snapshots":snapshots,"reviews":reviews})
    summaries={}
    for group,rows in groups.items():
        months={}
        for month in (4,5,7,10,11):
            selected=[r["snapshots"][str(month)] for r in rows if str(month) in r["snapshots"]]
            months[str(month)]={"n":len(selected),"proxy_gap_profiles":dict(Counter("+".join(s["proxy_gaps"]) or "none" for s in selected)),
                "statistics":{stat:dict(Counter(str(s["status"][stat]) for s in selected)) for stat in ("skill","network","output")}}
        boundary=Counter()
        for r in rows:
            review=next((x for x in r["reviews"] if x["before_month"]==(5 if group=="missed_first" else 11)),None)
            if review is None:continue
            boundary["reviews"]+=1
            boundary["before_last_choice_proxy_ready"]+=not gaps(review["before"])
            selected=next(x for x in review["alternatives"] if x["choice"]==review["selected"])
            boundary["chosen_known_nominal_projection_ready"]+=selected["nominal_effect_known"] and not selected["proxy_gaps"]
            boundary["some_known_nominal_alternative_ready"]+=any(x["nominal_effect_known"] and not x["proxy_gaps"] for x in review["alternatives"])
            boundary["some_nominal_effect_unknown"]+=any(not x["nominal_effect_known"] for x in review["alternatives"])
            boundary["pre_ready_but_no_known_projection_preserves_all"]+=not gaps(review["before"]) and all(x["nominal_effect_known"] and x["proxy_gaps"] for x in review["alternatives"])
        summaries[group]={"n":len(rows),"final_levels":dict(Counter(r["final"]["status"]["level"] for r in rows)),"months":months,"boundary_projection_audit":dict(boundary)}
    result={"source_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"selected":sum(len(v) for v in groups.values()),
        "summaries":summaries,"research_proxy_targets":TARGETS,"cases":dict(groups),
        "limits":["Selected survivors, not the full policy population or a causal comparison",
            "Proxy targets are private research hypotheses, not identified game gates",
            "Nominal alternative projections are not executed counterfactuals and omit clipping, review and delayed effects",
            "States before review differ from exact unobserved inputs used inside a bundled response"]}
    output.mkdir(parents=True,exist_ok=True)
    (output/"diagnosis.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"selected":result["selected"],"groups":{k:v["n"] for k,v in summaries.items()}},indent=2))


if __name__=="__main__":
    diagnose(Path(sys.argv[1]),Path(sys.argv[2]))
