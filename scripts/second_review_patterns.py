"""Descriptive second-review patterns; no inferred universal cutoffs."""
from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path
import sys


def patterns(root):
    reviews=json.loads((root/"reviews.json").read_text())
    outcomes=json.loads((root/"outcomes.json").read_text())
    second=[r for r in reviews if r["before_month"]>6]
    l2=[r for r in second if r["before"]["level"]=="L2"]
    growth=[r for r in l2 if r["promoted"]]
    friction=[r for r in growth if "You climbed too fast" in r["review_events"]]
    clean=[r for r in l2 if not any(w in r["review_events"] for w in ("Old landmines","Trust crisis"))]
    growth_ranges={}
    for label,selected in (("all_L2_promotions",growth),("without_explicit_simultaneous_explosion",[r for r in clean if r["promoted"]])):
        growth_ranges[label]={"n":len(selected),"post_state_ranges":{
            k:{"min":min(r["after"][k] for r in selected),"max":max(r["after"][k] for r in selected)}
            for k in ("health","dignity","skill","network","output")} if selected else {}}
    allocations=Counter()
    stalls=Counter()
    deaths_after_promotion=Counter()
    pre11=defaultdict(Counter)
    review_index={(r["batch"],r["run"]):r for r in second}
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        with gzip.open(archive,"rt") as stream:
            for line in stream:
                r=json.loads(line)
                rev=review_index.get((archive.parent.name,r["run"]))
                entry=next((s["before"] for s in r["steps"] if s["before"]["current_state"]["time"]["current_month"]==11),None)
                if entry:
                    state=entry["current_state"]["status"]
                    if state["level"]=="L2":
                        for stat in ("skill","network","output","health","dignity"):
                            key=f"{stat}={state[stat]}"
                            pre11[key]["n"]+=1
                            pre11[key]["promoted"]+=bool(rev and rev["promoted"])
                if rev and rev["before"]["level"]=="L2" and rev["promoted"] and r["outcome"]=="eliminated":
                    deaths_after_promotion[r["final"]["current_state"]["simulation_flags"].get("failure_reason","unknown")]+=1
                for s in r["steps"]:
                    b,a=s["before"]["current_state"],s["after"]["current_state"]
                    month=b["time"]["current_month"]
                    if s["phase"] in ("energy","main_action") and month in (6,9):
                        allocations[f"month-{month}/{s['phase']}"]+=1
                    if s["phase"] not in ("energy","main_action") or b["status"]["level"]!=a["status"]["level"]:
                        continue
                    if not 7<=month<=12:
                        continue
                    for stat,nominal in s["choice"].get("status_updates",{}).items():
                        k=stat.lower()
                        if k in ("skill","network","output") and nominal>0 and a["status"][k]==b["status"][k]:
                            stalls[f"{b['status']['level']}/{k}@{b['status'][k]}"]+=1
    with (root/"same-title-chains.csv").open() as stream:
        chain_rows=list(csv.DictReader(stream))
    crossing=[r for r in chain_rows if int(r["from_month"])<=6]
    result={"second_reviews":len(second),"L2_second_reviews":len(l2),"L2_to_L3_promotions":len(growth),
        "grade_and_promotion":[{"grade":g,"promoted":p,"n":n} for (g,p),n in sorted(Counter((r["grade"],r["promoted"]) for r in l2).items())],
        "social_friction_notice":len(friction),"network_changes_with_friction":dict(Counter(str(r["after"]["network"]-r["before"]["network"]) for r in friction)),
        "post_transition_descriptive_ranges":growth_ranges,
        "promoted_then_died_failure_reasons":dict(deaths_after_promotion),
        "quarterly_actions_before_second_review":dict(allocations),
        "positive_nominal_zero_net_investments":dict(stalls),
        "start_month11_observational_groups":{k:dict(v) for k,v in sorted(pre11.items())},
        "same_title_crossing_from_first_six":{"distinct_edges":len(crossing),"observations":sum(int(r["count"]) for r in crossing)},
        "limits":["Post-review values mix action, review, settlement, promotion friction and other consequences",
            "Minima and maxima are observed ranges, not identified thresholds",
            "Start-month-11 groups and mixed adaptive cohorts are not causal estimates",
            "Same-title recurrence is temporal evidence, not proof of a specific causal chain",
            "Survival to month13 does not resolve obligations beyond the research window"]}
    (root/"patterns.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("start_month11_observational_groups","positive_nominal_zero_net_investments")},indent=2))


if __name__=="__main__":
    patterns(Path(sys.argv[1]))
