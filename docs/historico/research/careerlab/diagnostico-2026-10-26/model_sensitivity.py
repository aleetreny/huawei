"""Offline sensitivity analysis of the team's statistical model, not gameplay.

Keeps the observed policy results fixed and varies only the family grouping.
This does not change the frozen protocol, the registry, or any decisions.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch

import numpy as np
from careerlab import decisions, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(name):
    return [json.loads(x) for x in (ROOT / "lab" / "registry" / f"{name}.jsonl").read_text().splitlines() if x.strip()]


def main():
    policies = {p["policy_id"]:p for p in read("policies")}
    jobs = read("jobs")
    evaluations = {e["job_id"]:e for e in read("evaluations")}
    slots = defaultdict(list)
    for j in jobs:
        if j["actor_id"] == "08e9167a965ed82c" and j["origin"] == "":
            slots[(j["policy_id"],j["purpose"],j["replicate"])].append(j)
    launches = defaultdict(list)
    for (pid,purpose,replicate), attempts in sorted(slots.items()):
        latest = max(attempts,key=lambda j:j["attempt"])
        e = evaluations.get(latest["job_id"])
        value = None
        if e and e["outcome"] in ("completed","eliminated"):
            value = stats.run_utility(e["score"],e["survival_months"],None,bool(e["completed"]))
        launches[pid].append((len(launches[pid])+1,value))
    observed = {pid:(policies[pid]["family"],stats.prefix_complete(values)) for pid,values in launches.items()}
    observed = {pid:cell for pid,cell in observed.items() if cell[1]}
    groupings = {
        "registered_families":observed,
        "one_common_family":{pid:("common",ys) for pid,(_,ys) in observed.items()},
        "one_family_per_policy":{pid:(pid,ys) for pid,(_,ys) in observed.items()},
    }
    results = {}
    for label,data in groupings.items():
        post = stats.partial_pool(data)
        actions = stats.decide(post)
        ranked = sorted(post,key=lambda pid:-post[pid].mean)
        results[label] = {
            "top5":[{"policy":policies[pid]["name"],"mean_y":post[pid].mean,"sd_y":post[pid].sd,"n":post[pid].n,"action":actions[pid].action} for pid in ranked[:5]],
            "dormant":[policies[pid]["name"] for pid,a in actions.items() if a.action=="DORMANT"],
        }
    # Reuse the collapse/outlier example from tests/test_stats.py, with no registry.
    residuals = [-3.0,3,-2,2,-1,1,0,0,-1,1]*2
    probe = {"L":("f",[55+d for d in residuals]),"M":("f",[52+d for d in residuals]),
             "N":("f",[50+d for d in residuals]),"X":("f",[54+d for d in residuals[:7]]+[0.0,0.0,0.0])}
    collected = {pid:{"name":pid,"family":family,"prefix":ys,"launches":list(enumerate(ys,1))} for pid,(family,ys) in probe.items()}
    original_robustness = stats.decision_is_robust
    with patch("careerlab.decisions.collect",return_value=collected), patch("careerlab.decisions.stats.decision_is_robust",side_effect=lambda d:original_robustness(d,rng=np.random.default_rng(0))):
        decision = decisions.block_decision(None,"offline-guard-probe",record=False)
    probe_actions={r["policy"]:r["action"] for r in decision["rows"]}
    assert decision["robust"] is False and probe_actions["X"] == "DORMANT"
    out={"base_commit":"917565c","caveat":"Same observed data; alternate groupings are sensitivity analyses, not replacement selection rules. They do not identify which model is true.","haiku_policy_count":len(observed),"results":results,
         "guard_reproduction":{"input":"Existing collapse/outlier example from tests/test_stats.py; collect mocked only to avoid storage; robustness uses real computation with seed 0.","robust":decision["robust"],"actions":probe_actions,"note":decision["robustness_note"],"registry_written":False}}
    (HERE/"model-sensitivity.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
