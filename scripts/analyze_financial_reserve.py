"""Archive reserve-study public trajectories and report full-start denominators."""
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import shutil
import statistics
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import month_index, is_terminal
from scripts.analyze_second_review import summarize_record
from scripts.analyze_trust_risk import wilson
from scripts.first_review_search import node_key

METRICS=("broke","trust_death","health_death","first_promotion_by_6","first_promoted_alive_at_7",
    "second_promotion_by_12","second_promotion_and_alive","alive_through_12")


def analyze(source,output):
    output.mkdir(parents=True,exist_ok=True)
    protocol=json.loads((source/"protocol.json").read_text())
    if hashlib.sha256((source/"protocol.json").read_bytes()).hexdigest()!=(source/"protocol-sha256.txt").read_text().strip():
        raise ValueError("Protocol integrity mismatch")
    records=[json.loads(p.read_text()) for p in sorted(source.glob("run-*.json"))]
    assignments=json.loads((source/"assignments.json").read_text())
    if len({a["position"] for a in assignments})!=len(assignments):
        raise ValueError("Duplicate assignment")
    by_run={r["run"]:r for r in records}
    rows=[]
    for a in assignments:
        index=a["position"]
        if protocol["schedule"][index]!=a["arm"]:
            raise ValueError("Frozen assignment mismatch")
        r=by_run[index]
        if r["assignment"]!=a:
            raise ValueError("Assignment journal mismatch")
        summary=summarize_record(r)
        reason=r.get("final",{}).get("current_state",{}).get("simulation_flags",{}).get("failure_reason") or ""
        resolved=r["outcome"] in ("eliminated","twelve_month_window")
        observations=([r["initial_observation"]] if r.get("initial_observation") else [])+[o for s in r["steps"] for o in (s["before"],s["after"])]
        first7=next((o for o in observations if month_index(o)==7 and not is_terminal(o)),None)
        overrides=[s for s in r["steps"] if s.get("diagnostic",{}).get("cash_override")]
        rows.append({"run":index,"arm":a["arm"],"resolved":resolved,"outcome":r["outcome"],
            **{k:summary[k] for k in METRICS if k in summary},"broke":"Broke" in reason,
            "trust_death":"Trust crisis" in reason,"health_death":"Blackout" in reason,
            "failure_reason":reason or None,"wealth_at_7":first7["current_state"]["status"]["wealth"] if first7 else None,
            "cash_overrides":len(overrides),"ever_cash_override":bool(overrides)})
    def aggregate(selected):
        done=[r for r in selected if r["resolved"]]
        n=len(selected);known=len(done);unknown=n-known
        wealth=[r["wealth_at_7"] for r in selected if r["wealth_at_7"] is not None]
        return {"assigned":n,"resolved":known,"interrupted":unknown,
            "metrics":{m:{"count":sum(r[m] for r in done),"resolved_n":known,
                "rate":sum(r[m] for r in done)/known if known else None,"wilson95":wilson(sum(r[m] for r in done),known),
                "assigned_rate_bounds":[sum(r[m] for r in done)/n,(sum(r[m] for r in done)+unknown)/n] if n else None} for m in METRICS},
            "wealth_at_7_conditional_on_reaching_7":{"n":len(wealth),"median":statistics.median(wealth) if wealth else None,
                "at_or_below_zero":sum(v<=0 for v in wealth)},
            "cash_override_episodes":sum(r["ever_cash_override"] for r in selected),"cash_override_actions":sum(r["cash_overrides"] for r in selected)}
    arms={arm:aggregate([r for r in rows if r["arm"]==arm]) for arm in ("baseline","reserve")}
    differences={}
    for metric in METRICS:
        off=arms["baseline"]["metrics"][metric];on=arms["reserve"]["metrics"][metric]
        if off["rate"] is None or on["rate"] is None:
            differences[metric]=None;continue
        p0,p1=off["rate"],on["rate"];lo0,hi0=off["wilson95"];lo1,hi1=on["wilson95"]
        d=p1-p0
        differences[metric]={"reserve_minus_baseline":d,"newcombe95":[d-math.sqrt((p1-lo1)**2+(hi0-p0)**2),d+math.sqrt((hi1-p1)**2+(p0-lo0)**2)]}
    archive=output/"public-trajectories.jsonl.gz"
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as stream:
            for r in records:stream.write((json.dumps(r,ensure_ascii=False)+"\n").encode())
    (output/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+"\n")
    for name in ("protocol.json","protocol-sha256.txt","assignments.json","status.json","frozen-effects.json","frozen-hazards.json","handbook.json"):
        if (source/name).exists():shutil.copyfile(source/name,output/name)
    shutil.copytree(source/"sources",output/"sources",dirs_exist_ok=True)
    old=json.loads(Path("lab/reports/trust-risk-study/extended-questions.json").read_text())
    old_keys={q["id"] for q in old};new={}
    for r in records:
        for s in r["steps"]:
            for o in (s["before"],s["after"]):
                if 7<=month_index(o)<=12 and o.get("choices") and not is_terminal(o) and node_key(o) not in old_keys:
                    new.setdefault(node_key(o),{"id":node_key(o),"event":o.get("current_event"),"choices":o["choices"],"answers":{}})
        for i,s in enumerate(r["steps"]):
            key=node_key(s["before"])
            if key in new and s.get("applied") and not s.get("ambiguous") and s.get("reply",{}).get("success") is True:
                new[key]["answers"].setdefault(str(s["choice"]["choice"]),{"run":r["run"],"step":i})
    for q in new.values():q["untried_choices"]=[c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    (output/"new-questions.json").write_text(json.dumps(list(new.values()),indent=2,ensure_ascii=False)+"\n")
    result={"assigned":len(rows),"target":len(protocol["schedule"]),"complete":len(rows)==len(protocol["schedule"]) and all(r["resolved"] for r in rows),
        "arms":arms,"differences":differences,"new_nodes_7_12":len(new),"rows":rows,
        "failure_labels":{arm:dict(Counter(r["failure_reason"] for r in rows if r["arm"]==arm and r["failure_reason"])) for arm in arms},
        "limits":protocol["limitations"]+["Wealth-at-month7 summaries condition on reaching month7 and are not the primary treatment effect",
            "Intervals for multiple secondary outcomes are exploratory and unadjusted","Interruptions remain unknown with assigned-denominator bounds"]}
    (output/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"complete":result["complete"],"assigned":len(rows),"arms":{a:{m:v["count"] for m,v in g["metrics"].items()} for a,g in arms.items()},"differences":differences,"new_nodes":len(new)},indent=2))


if __name__=="__main__":
    analyze(Path(sys.argv[1]),Path(sys.argv[2]))
