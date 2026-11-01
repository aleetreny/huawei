"""Public history reconstruction and frozen factorial summaries for trust study."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import month_index
from scripts.analyze_second_review import summarize_record
from scripts.trust_risk_study import arm_key


def wilson(k,n):
    if not n:
        return None
    z=1.959963984540054
    center=(k/n+z*z/(2*n))/(1+z*z/n)
    radius=z*math.sqrt((k/n)*(1-k/n)/n+z*z/(4*n*n))/(1+z*z/n)
    return [center-radius,center+radius]


def history(record):
    blasts=[]
    cleanups=[]
    warnings=[]
    for i,s in enumerate(record["steps"]):
        month=month_index(s["before"])
        text=s["after"].get("events","")
        if "Old landmines" in text:
            blasts.append({"step":i,"month":month,"choice":s["choice"],"reason":s.get("reason")})
        if s["choice"]["action"]=="Defuse legacy risk":
            cleanups.append({"step":i,"month":month})
        if "HR partner" in text:
            warnings.append({"step":i,"month":month,"text":text})
    failure=record.get("final",{}).get("current_state",{}).get("simulation_flags",{}).get("failure_reason")
    return {"explosions":blasts,"cleanups":cleanups,"warning_count":len(warnings),"failure_reason":failure,
        "last_step":record["steps"][-1] if record["steps"] else None}


def financial_audit(records):
    rows=[]
    for r in records:
        if not r.get("assignment"):
            continue
        reason=r.get("final",{}).get("current_state",{}).get("simulation_flags",{}).get("failure_reason") or ""
        if "Broke" not in reason:
            continue
        losses=[]
        for i,s in enumerate(r["steps"]):
            b,a=s["before"]["current_state"],s["after"]["current_state"]
            if a["status"]["wealth"]<b["status"]["wealth"]:
                losses.append({"step":i,"month":b["time"]["current_month"],"choice":s["choice"]["action"],
                    "before":b["status"]["wealth"],"after":a["status"]["wealth"]})
        rows.append({"run":r["run"],"wealth_at_assignment":r["assignment"]["pre_state"]["status"]["wealth"],
            "failure_month":r["final"]["current_state"]["time"]["current_month"],"losses":losses})
    return {"financial_deaths":len(rows),"wealth_at_assignment":dict(Counter(str(r["wealth_at_assignment"]) for r in rows)),
        "first_loss_month":dict(Counter(str(r["losses"][0]["month"]) if r["losses"] else "none" for r in rows)),
        "had_coffee_favour_spending":sum(any("buying coffees" in loss["choice"] for loss in r["losses"]) for r in rows),
        "coffee_first_loss_before_assignment":sum(any("buying coffees" in loss["choice"] and loss["month"]<=6 for loss in r["losses"]) for r in rows),
        "cases":rows,"limits":["Selected failures, not a treatment comparison", "Net visible wealth changes may include settlement; discretionary-loss attribution is descriptive"]}


def retrospective(evidence,output):
    selected=[]
    all_failures=Counter()
    sources=[]
    for archive in sorted(evidence.glob("*/public-trajectories.jsonl.gz")):
        expected=(archive.parent/"archive-sha256.txt").read_text().split()[0]
        actual=hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual!=expected:
            raise ValueError("Archive integrity mismatch")
        sources.append({"batch":archive.parent.name,"sha256":actual})
        with gzip.open(archive,"rt") as stream:
            for line in stream:
                r=json.loads(line)
                summary=summarize_record(r)
                h=history(r)
                if r["outcome"]=="eliminated":
                    all_failures[h["failure_reason"]]+=1
                if summary["second_promotion_by_12"] and r["outcome"]=="eliminated" and "Trust crisis" in (h["failure_reason"] or ""):
                    last=h["last_step"]
                    selected.append({"batch":archive.parent.name,"run":r["run"],
                        "explosions":h["explosions"],"cleanups":h["cleanups"],
                        "cleanup_after_first_explosion":bool(h["explosions"] and any(c["step"]>h["explosions"][0]["step"] for c in h["cleanups"])),
                        "fatal_choice":last["choice"],"fatal_phase":last["phase"],"fatal_reason":last.get("reason"),
                        "warning_memory_before_fatal_choice":last.get("risk_warning_before"),
                        "fatal_before":last["before"],"fatal_after":last["after"]})
    result={"sources":sources,"post_second_promotion_trust_deaths":len(selected),
        "normal_bot_final_choices":sum(r["fatal_reason"]!="coverage_or_same_title_route" for r in selected),
        "all_had_cleanup":all(r["cleanups"] for r in selected),
        "cleanup_month_patterns":[{"months":list(k),"n":v} for k,v in sorted(Counter(tuple(c["month"] for c in r["cleanups"]) for r in selected).items())],
        "cleanup_after_first_explosion":sum(r["cleanup_after_first_explosion"] for r in selected),
        "warning_memory_before_fatal_choice":dict(Counter(str(r["warning_memory_before_fatal_choice"]) for r in selected)),
        "all_original_failure_labels":dict(all_failures),"cases":selected,
        "limits":["Selected failures only; no causal effect of cleanup follows from these histories",
            "Bot warning memory can be stale and is not the true hidden risk",
            "Public explosion history does not expose the engine incident counter"]}
    output.mkdir(parents=True,exist_ok=True)
    (output/"retrospective.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("cases","sources","all_original_failure_labels")},indent=2))


def analyze(source,output):
    output.mkdir(parents=True,exist_ok=True)
    protocol=json.loads((source/"protocol.json").read_text())
    expected=(source/"protocol-sha256.txt").read_text().strip()
    if hashlib.sha256((source/"protocol.json").read_bytes()).hexdigest()!=expected:
        raise ValueError("Protocol hash mismatch")
    records=[json.loads(p.read_text()) for p in sorted(source.glob("run-*.json"))]
    (output.parent/"financial-failure-audit.json").write_text(json.dumps(financial_audit(records),indent=2,ensure_ascii=False)+"\n")
    assignments=json.loads((source/"assignments.json").read_text())
    by_run={r["run"]:r for r in records}
    if len({a["run"] for a in assignments})!=len(assignments):
        raise ValueError("Duplicate assignment")
    rows=[]
    mismatches=[]
    for pos,a in enumerate(assignments):
        if a["position"]!=pos or a["arm_index"]!=protocol["schedule"][pos]:
            raise ValueError("Assignment differs from frozen random schedule")
        r=by_run.get(a["run"])
        if not r or r.get("assignment")!=a:
            raise ValueError("Assignment journal and episode disagree")
        arm=protocol["arms"][a["arm_index"]]
        obs=a["pre_state"]
        if obs["time"]["current_month"]!=6 or obs["status"]["level"]!="L2":
            raise ValueError("Ineligible assignment")
        h=history(r)
        result=summarize_record(r)
        resolved=r["outcome"] in ("eliminated","twelve_month_window")
        row={"run":r["run"],"arm":arm_key(arm),"factors":arm,"prior_explosions":a["prior_explosions"],
            "resolved":resolved,"trust_death":bool(resolved and "Trust crisis" in (h["failure_reason"] or "")),
            "second_promotion":result["second_promotion_by_12"],"second_promotion_and_alive":result["second_promotion_and_alive"],
            "survived":result["alive_through_12"],"explosions":len(h["explosions"]),"failure_reason":h["failure_reason"]}
        for month in (6,9):
            expected_plan=protocol["plans"]["cleanup" if arm[f"cleanup{month}"] else "growth"]
            actual=[s["choice"]["action"] for s in r["steps"] if month_index(s["before"])==month and s.get("reason")=="randomised_energy_plan"]
            if actual!=expected_plan[:len(actual)] or len(actual)>len(expected_plan):
                mismatches.append({"run":r["run"],"month":month,"expected":expected_plan,"actual":actual})
            row[f"plan{month}_full"]=actual==expected_plan
            row[f"plan{month}_reached"]=bool(actual)
        rows.append(row)
    groups={}
    metrics=("trust_death","second_promotion","second_promotion_and_alive","survived")
    def aggregate(selected):
        done=[r for r in selected if r["resolved"]]
        return {"assigned":len(selected),"resolved":len(done),"interrupted":len(selected)-len(done),
            **{m:{"n":len(done),"count":sum(r[m] for r in done),"rate":sum(r[m] for r in done)/len(done) if done else None,
                "wilson95":wilson(sum(r[m] for r in done),len(done))} for m in metrics}}
    for index,arm in enumerate(protocol["arms"]):
        key=arm_key(arm)
        groups[key]={"factors":arm,**aggregate([r for r in rows if r["arm"]==key])}
    main_effects={}
    for factor in ("cleanup6","cleanup9","incident_guard"):
        off=aggregate([r for r in rows if not r["factors"][factor]])
        on=aggregate([r for r in rows if r["factors"][factor]])
        main_effects[factor]={"off":off,"on":on,"risk_differences_on_minus_off":{
            m:on[m]["rate"]-off[m]["rate"] if on[m]["rate"] is not None and off[m]["rate"] is not None else None for m in metrics}}
        intervals={}
        for m in metrics:
            if on[m]["rate"] is None or off[m]["rate"] is None:
                intervals[m]=None
                continue
            p1,p0=on[m]["rate"],off[m]["rate"]
            lo1,hi1=on[m]["wilson95"]
            lo0,hi0=off[m]["wilson95"]
            d=p1-p0
            intervals[m]=[d-math.sqrt((p1-lo1)**2+(hi0-p0)**2),d+math.sqrt((hi1-p1)**2+(p0-lo0)**2)]
        main_effects[factor]["newcombe95_risk_differences"]=intervals
    strata={}
    for prior in (False,True):
        selected=[r for r in rows if bool(r["prior_explosions"])==prior]
        strata[str(prior)]={"n":len(selected),"guard_off":aggregate([r for r in selected if not r["factors"]["incident_guard"]]),
            "guard_on":aggregate([r for r in selected if r["factors"]["incident_guard"]])}
    archive=output/"public-trajectories.jsonl.gz"
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as stream:
            for r in records:
                stream.write((json.dumps(r,ensure_ascii=False)+"\n").encode())
    (output/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+"\n")
    for name in ("protocol.json","protocol-sha256.txt","assignments.json","status.json","frozen-effects.json","frozen-hazards.json","handbook.json"):
        if (source/name).exists():
            shutil.copyfile(source/name,output/name)
    shutil.copytree(source/"sources",output/"sources",dirs_exist_ok=True)
    old_questions=json.loads(Path("lab/reports/second-review-search/questions.json").read_text())
    old_keys={q["id"] for q in old_questions}
    from scripts.first_review_search import node_key
    new_questions={}
    for r in records:
        for index,s in enumerate(r["steps"]):
            if not 7<=month_index(s["before"])<=12:
                continue
            key=node_key(s["before"])
            if key in old_keys:
                continue
            q=new_questions.setdefault(key,{"id":key,"event":s["before"].get("current_event"),"choices":s["before"]["choices"],"answers":{}})
            if s.get("applied") is True and not s.get("ambiguous") and s.get("reply",{}).get("success") is True:
                q["answers"].setdefault(str(s["choice"]["choice"]),{"run":r["run"],"step":index,"month":month_index(s["before"])})
    for q in new_questions.values():
        q["untried_choices"]=[c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    (output/"new-questions.json").write_text(json.dumps(list(new_questions.values()),indent=2,ensure_ascii=False)+"\n")
    result={"attempts":len(records),"assigned":len(rows),"target":len(protocol["schedule"]),
        "assignment_block_complete":len(rows)==len(protocol["schedule"]) and all(r["resolved"] for r in rows),
        "unassigned_outcomes":dict(Counter(r["outcome"] for r in records if not r.get("assignment"))),
        "groups":groups,"main_effects":main_effects,"pre_assignment_explosion_strata":strata,
        "plan_delivery":{"mismatches":mismatches,**{str(m):{"reached":sum(r[f"plan{m}_reached"] for r in rows),"full":sum(r[f"plan{m}_full"] for r in rows)} for m in (6,9)}},
        "new_question_nodes_vs_previous_catalogue":len(new_questions),
        "rows":rows,"limits":protocol["limitations"]+[
            "Intervals are descriptive exploratory rate intervals, not multiplicity-adjusted superiority tests",
            "No post-assignment survivor subgroup is used as the primary denominator",
            "Results apply to the frozen empirical research bot and eligible L2 population, not all new careers or reasoning agents"]}
    (output/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"attempts":len(records),"assigned":len(rows),"complete":result["assignment_block_complete"],
        "groups":{k:{m:v[m]["count"] for m in metrics} for k,v in groups.items()},
        "main_effects":{k:v["risk_differences_on_minus_off"] for k,v in main_effects.items()},"delivery":result["plan_delivery"]},indent=2))


if __name__=="__main__":
    if sys.argv[1]=="retrospective":
        retrospective(Path(sys.argv[2]),Path(sys.argv[3]))
    else:
        analyze(Path(sys.argv[1]),Path(sys.argv[2]))
