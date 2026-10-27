"""Summarise frozen growth-priority arms on all initially assigned games."""
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.analyze_second_review import summarize_record
from scripts.analyze_trust_risk import wilson
from scripts.analyze_financial_reserve import METRICS
from scripts.first_review_search import node_key
from careerlab.mcp_client import month_index,is_terminal


def analyze(source,output):
    output.mkdir(parents=True,exist_ok=True)
    p=json.loads((source/"protocol.json").read_text())
    if hashlib.sha256((source/"protocol.json").read_bytes()).hexdigest()!=(source/"protocol-sha256.txt").read_text().strip():raise ValueError("Protocol integrity mismatch")
    records=[json.loads(file.read_text()) for file in sorted(source.glob("run-*.json"))]
    assignments=json.loads((source/"assignments.json").read_text());by_run={r["run"]:r for r in records}
    rows=[]
    for a in assignments:
        i=a["position"];arm=a["arm"];r=by_run[i]
        if p["schedule"][i]!=arm or r["assignment"]!=a:raise ValueError("Assignment mismatch")
        summary=summarize_record(r);reason=r.get("final",{}).get("current_state",{}).get("simulation_flags",{}).get("failure_reason") or ""
        resolved=r["outcome"] in ("eliminated","twelve_month_window")
        alive=r["outcome"]=="twelve_month_window"
        snapshots={}
        for month in (5,11):
            o=next((s["before"] for s in r["steps"] if month_index(s["before"])==month),None)
            if o:snapshots[str(month)]=o["current_state"]["status"]
        rows.append({"run":i,"arm":arm,"resolved":resolved,**{m:summary[m] for m in METRICS if m in summary},
            "broke":"Broke" in reason,"trust_death":"Trust crisis" in reason,"health_death":"Blackout" in reason,
            "failure_reason":reason or None,"survived_without_first":alive and not summary["first_promotion_by_6"],
            "survived_stalled_L2":alive and summary["first_promotion_by_6"] and not summary["second_promotion_by_12"],
            "growth_overrides":sum(s.get("diagnostic",{}).get("growth_override",False) for s in r["steps"]),"snapshots":snapshots})
    groups={}
    for arm in p["arms"]:
        selected=[r for r in rows if r["arm"]==arm];done=[r for r in selected if r["resolved"]];n=len(selected);known=len(done)
        groups[arm]={"assigned":n,"resolved":known,"interrupted":n-known,
            "metrics":{m:{"count":sum(r[m] for r in done),"n":known,"rate":sum(r[m] for r in done)/known if known else None,
                "wilson95":wilson(sum(r[m] for r in done),known),"assigned_bounds":[sum(r[m] for r in done)/n,(sum(r[m] for r in done)+n-known)/n] if n else None} for m in METRICS},
            "survivor_partition":{"second_promoted":sum(r["second_promotion_and_alive"] for r in done),
                "missed_first":sum(r["survived_without_first"] for r in done),"stalled_L2":sum(r["survived_stalled_L2"] for r in done)},
            "growth_override_actions":sum(r["growth_overrides"] for r in selected)}
        profiles={}
        for month,level in ((5,"L1"),(11,"L2")):
            states=[r["snapshots"][str(month)] for r in selected if str(month) in r["snapshots"] and r["snapshots"][str(month)]["level"]==level]
            targets=p["research_targets"][level]
            profiles[f"month{month}/{level}"]={"n":len(states),"below_research_target":{stat:sum(s[stat]<target for s in states) for stat,target in targets.items()}}
        groups[arm]["post_assignment_intermediate_profiles"]=profiles
    contrasts={}
    for arm in p["arms"]:
        if arm=="control":continue
        contrast={}
        for m in METRICS:
            off=groups["control"]["metrics"][m];on=groups[arm]["metrics"][m]
            if off["rate"] is None or on["rate"] is None:contrast[m]=None;continue
            p0,p1=off["rate"],on["rate"];lo0,hi0=off["wilson95"];lo1,hi1=on["wilson95"];d=p1-p0
            contrast[m]={"difference":d,"newcombe95":[d-math.sqrt((p1-lo1)**2+(hi0-p0)**2),d+math.sqrt((hi1-p1)**2+(p0-lo0)**2)]}
        contrasts[arm]=contrast
    archive=output/"public-trajectories.jsonl.gz"
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as stream:
            for r in records:stream.write((json.dumps(r,ensure_ascii=False)+"\n").encode())
    (output/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+"\n")
    for name in ("protocol.json","protocol-sha256.txt","assignments.json","status.json","frozen-effects.json","frozen-hazards.json","handbook.json"):
        if (source/name).exists():shutil.copyfile(source/name,output/name)
    shutil.copytree(source/"sources",output/"sources",dirs_exist_ok=True)
    old={q["id"] for q in json.loads(Path("lab/reports/financial-reserve-study/extended-questions.json").read_text())};new={}
    for r in records:
        for s in r["steps"]:
            for o in (s["before"],s["after"]):
                if 7<=month_index(o)<=12 and o.get("choices") and not is_terminal(o) and node_key(o) not in old:
                    new.setdefault(node_key(o),{"id":node_key(o),"event":o.get("current_event"),"choices":o["choices"],"answers":{}})
        for index,s in enumerate(r["steps"]):
            key=node_key(s["before"])
            if key in new and s.get("applied") and not s.get("ambiguous") and s.get("reply",{}).get("success") is True:
                new[key]["answers"].setdefault(str(s["choice"]["choice"]),{"run":r["run"],"step":index})
    for q in new.values():q["untried_choices"]=[c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    (output/"new-questions.json").write_text(json.dumps(list(new.values()),indent=2,ensure_ascii=False)+"\n")
    result={"assigned":len(rows),"target":len(p["schedule"]),"complete":len(rows)==len(p["schedule"]) and all(r["resolved"] for r in rows),
        "arms":groups,"contrasts":contrasts,"rows":rows,"new_nodes_7_12":len(new),"limits":p["limitations"]+[
            "All contrasts and secondary intervals are exploratory and unadjusted for multiple comparisons",
            "Post-treatment survivor categories describe where paths stall, not conditional causal effects"]}
    (output/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"complete":result["complete"],"assigned":len(rows),"arms":{a:{m:v["count"] for m,v in g["metrics"].items()} for a,g in groups.items()},
        "primary_contrasts":{a:c["second_promotion_and_alive"] for a,c in contrasts.items()},"new_nodes":len(new)},indent=2))


def continuity(root):
    first=Path("lab/reports/first-review-search/questions.json");second=Path("lab/reports/financial-reserve-study/extended-questions.json")
    known={1:{q["id"] for q in json.loads(first.read_text())},2:{q["id"] for q in json.loads(second.read_text())}}
    novel={1:{},2:{}};sources=[]
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        actual=hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual!=(archive.parent/"archive-sha256.txt").read_text().split()[0]:raise ValueError("Archive integrity mismatch")
        n=0
        with gzip.open(archive,"rt") as stream:
            for line in stream:
                r=json.loads(line);n+=1
                for s in r["steps"]:
                    for o in (s["before"],s["after"]):
                        m=month_index(o)
                        if not 1<=m<=12 or not o.get("choices") or is_terminal(o):continue
                        window=1 if m<=6 else 2;key=node_key(o)
                        if key not in known[window]:novel[window][key]={"event":o.get("current_event"),"choices":o["choices"],"run":r["run"],"archive":str(archive)}
        sources.append({"archive":str(archive),"records":n,"sha256":actual})
    result={"reference_sha256":{"first_six":hashlib.sha256(first.read_bytes()).hexdigest(),"second_six":hashlib.sha256(second.read_bytes()).hexdigest()},
        "archives":sources,"new_first_six":novel[1],"new_second_six":novel[2]}
    (root/"catalogue-continuity-audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"new_first_six":len(novel[1]),"new_second_six":len(novel[2]),"records":sum(s["records"] for s in sources)}))


if __name__=="__main__":
    continuity(Path(sys.argv[2])) if sys.argv[1]=="catalogue" else analyze(Path(sys.argv[1]),Path(sys.argv[2]))
