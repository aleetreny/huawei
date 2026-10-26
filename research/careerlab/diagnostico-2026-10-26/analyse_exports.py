"""Offline descriptive audit of our exported registry, never the game or its DB.

Run from any directory: python3 <this file>. Writes summary.json beside itself.
No CareerLab imports, game tools, credentials or external libraries are used.
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REGISTRY = ROOT / "lab" / "registry"


def read(name):
    return [json.loads(line) for line in (REGISTRY / f"{name}.jsonl").read_text().splitlines() if line.strip()]


def unpack(value):
    return json.loads(value) if isinstance(value, str) else (value or {})


def mean(values):
    return st.mean(values) if values else None


def wilson(successes, n):
    if not n:
        return None
    z = 1.959963984540054
    p = successes / n
    centre = (p + z*z / (2*n)) / (1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [max(0.0, centre-half), min(1.0, centre+half)]


def describe(rows):
    q = [r["score"] for r in rows]
    wins = [r for r in rows if r["completed"]]
    losses = [r for r in rows if not r["completed"]]
    utilities = [0.8*r["score"] + (10 if r["completed"] else 5) for r in rows]
    dims = collections.defaultdict(list)
    for row in wins:
        for name, value in unpack(row["dims"]).items():
            dims[name].append(value)
    return {
        "n": len(rows), "completed": len(wins),
        "p_complete": len(wins)/len(rows) if rows else None,
        "completion_wilson95": wilson(len(wins), len(rows)),
        "q_mean": mean(q), "q_sd": st.stdev(q) if len(q)>1 else None,
        "q_completed": mean([r["score"] for r in wins]),
        "q_eliminated": mean([r["score"] for r in losses]),
        "proxy_y_mean": mean(utilities),
        "proxy_y_sd": st.stdev(utilities) if len(rows)>1 else None,
        "months_eliminated": dict(collections.Counter(str(r["survival_months"]) for r in losses)),
        "completed_dims_mean": {k: mean(v) for k,v in dims.items()},
        "rejected_actions": sum(r["rejected_actions"] for r in rows),
        "steps": sum(r["steps"] for r in rows),
        "wall_s_completed_median": st.median(r["wall_s"] for r in wins) if wins else None,
    }


def main():
    exported_evaluations, actors_list, policies_list, jobs, decisions = [read(x) for x in ("evaluations","actors","policies","jobs","decisions")]
    evaluations = [e for e in exported_evaluations if e["outcome"] in ("completed", "eliminated")]
    excluded = [e for e in exported_evaluations if e["outcome"] not in ("completed", "eliminated")]
    assert all(e["outcome"] == "interrupted" and e["score"] is None for e in excluded), "Unrecognised nonterminal result"
    actors = {a["actor_id"]: a for a in actors_list}
    policies = {p["policy_id"]: p for p in policies_list}
    jobs_by_id = {j["job_id"]: j for j in jobs}
    assert len(jobs_by_id) == len(jobs), "Exported job IDs are ambiguous across origins"
    assert len({e["job_id"] for e in evaluations}) == len(evaluations), "Duplicate terminal evaluations"
    assert all(e["job_id"] in jobs_by_id for e in evaluations), "Evaluation without exported job"
    assert all(0 <= e["score"] <= 100 for e in evaluations)
    assert all(e["outcome"] in ("completed", "eliminated") for e in evaluations)
    assert all(bool(e["completed"]) == (e["outcome"] == "completed") for e in evaluations)
    proxy = [e for e in evaluations if actors[e["actor_id"]]["kind"] == "claude-cli" and e["purpose"] != "infra"]
    race = [e for e in proxy if jobs_by_id[e["job_id"]]["origin"] == ""]
    haiku = [e for e in race if e["actor_id"] == "08e9167a965ed82c"]
    cells = collections.defaultdict(list)
    for e in proxy:
        cells[(jobs_by_id[e["job_id"]]["origin"], e["actor_id"], e["env_id"], e["policy_id"])].append(e)
    out = {
        "base_commit": "917565c",
        "scope": "Exported terminal results; descriptive analysis, not a selection or causal estimate. Actor/origin/environment cells stay separate.",
        "limitations": ["No event seeds or random assignment presumed", "Adaptive development data, not fresh confirmation", "Wilson intervals are descriptive at observed n, not anytime-valid", "Normalized dimensions are not action marginal returns", "List prices and tokens do not measure subscription quota"],
        "source_sha256": {n:hashlib.sha256((REGISTRY/f"{n}.jsonl").read_bytes()).hexdigest() for n in ("evaluations","actors","policies","jobs","decisions")},
        "counts": {"exported_evaluation_rows":len(exported_evaluations), "excluded_interrupted_unscored":len(excluded), "terminal_evaluations":len(evaluations), "claude_terminal_including_infra":sum(actors[e["actor_id"]]["kind"]=="claude-cli" for e in evaluations), "claude_terminal_excluding_infra":len(proxy), "race_origin_proxy":len(race), "scripted":sum(actors[e["actor_id"]]["kind"]=="scripted" for e in evaluations), "jobs":len(jobs)},
        "origins":dict(collections.Counter(jobs_by_id[e["job_id"]]["origin"] for e in proxy)),
        "race_proxy_all_actors":describe(race),
        "main_haiku_all_policies":describe(haiku),
        "actors":[], "cells":[],
    }
    for aid,a in actors.items():
        subset=[e for e in race if e["actor_id"]==aid]
        if subset:
            out["actors"].append({"actor_id":aid,"config":unpack(a["config"]), **describe(subset)})
    for (origin, aid, env, pid),rows in sorted(cells.items()):
        attempted=[j for j in jobs if j["origin"]==origin and j["actor_id"]==aid and j["env_id"]==env and j["policy_id"]==pid and j["purpose"]!="infra"]
        counts=collections.Counter(j["status"] for j in attempted)
        resolved=counts["done"]+counts["interrupted"]
        out["cells"].append({"origin":origin,"actor_id":aid,"env_id":env,"policy":policies[pid]["name"],"policy_id":pid,"family":policies[pid]["family"],"job_statuses":dict(counts),"interrupted_attempt_fraction":counts["interrupted"]/resolved if resolved else None, **describe(rows)})
    token_rows=[]
    for e in race:
        usage=unpack(e["tokens"])
        token=usage.get("tokens",{})
        total=sum(token.get(k,0) for k in ("input_tokens","output_tokens","cache_read_input_tokens","cache_creation_input_tokens"))
        if total:
            token_rows.append({"actor_id":e["actor_id"],"completed":bool(e["completed"]),"total":total,"cache_reads":token.get("cache_read_input_tokens",0),"per_month":total/e["survival_months"],"wall_s":e["wall_s"],"api_ms":usage.get("api_ms",0),"steps":e["steps"],"list_usd":usage.get("cost_usd_list_price",0)})
    out["usage"]={}
    for aid in {r["actor_id"] for r in token_rows}:
        rows=[r for r in token_rows if r["actor_id"]==aid and r["completed"]]
        if rows:
            out["usage"][aid]={"n_completed":len(rows),"median_tokens":st.median(r["total"] for r in rows),"median_tokens_per_month":st.median(r["per_month"] for r in rows),"cache_read_share":sum(r["cache_reads"] for r in rows)/sum(r["total"] for r in rows),"median_wall_s":st.median(r["wall_s"] for r in rows),"api_time_share":sum(r["api_ms"] for r in rows)/(1000*sum(r["wall_s"] for r in rows)),"median_steps":st.median(r["steps"] for r in rows),"median_list_usd":st.median(r["list_usd"] for r in rows)}
    haiku_cells=[c for c in out["cells"] if c["actor_id"]=="08e9167a965ed82c" and c["origin"]=="" and c["n"]>1]
    df=sum(c["n"]-1 for c in haiku_cells)
    sd=math.sqrt(sum((c["n"]-1)*c["proxy_y_sd"]**2 for c in haiku_cells)/df)
    coefficient=2*(st.NormalDist().inv_cdf(0.9)+st.NormalDist().inv_cdf(0.8))**2
    out["planning"]={"pooled_within_policy_haiku_proxy_y_sd":sd,"coefficient_alpha_one_sided_0_10_power_0_80":coefficient,"n_per_arm_for_delta4_y":math.ceil(coefficient*sd*sd/16),"caveat":"Normal approximation and pooled variance for planning only; this is not a stopping rule or a guarantee."}
    summary=out["main_haiku_all_policies"]
    if summary["q_completed"] is not None and summary["q_eliminated"] is not None:
        gap=summary["q_completed"]-summary["q_eliminated"]
        out["illustrative_sensitivity"]={"q_gap_completed_vs_eliminated":gap,"q_gain_if_completion_up_10pp_at_fixed_conditional_means":0.1*gap,"q_gain_if_completed_mean_up5_at_fixed_completion":5*summary["p_complete"],"caveat":"Algebraic scenario, not an intervention effect; pooled policies differ and prevented failures need not score like observed survivors."}
    out["trace_availability"]={"proxy_total":len(proxy),"recorded_path_exists_on_this_machine":sum(Path(e["trajectory_path"]).is_file() for e in proxy if e.get("trajectory_path")),"caveat":"Missing locally can mean the trace lives only in cloud or another machine; not proof of data loss."}
    blocks=[]
    for d in decisions:
        if d["kind"]=="block_decision":
            payload=unpack(d["payload"])
            rows=payload.get("rows",[])
            if rows: blocks.append({"id":d["decision_id"],"at":d["at"],"actor_id":payload.get("actor_id"),"robust":payload.get("robust"),"leader":rows[0]["policy"],"leader_mean_y":rows[0]["posterior_mean"],"leader_probability_best":rows[0]["p_best"]})
    out["recorded_blocks"]=blocks
    (HERE/"summary.json").write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({k:out[k] for k in ("counts","origins","main_haiku_all_policies","planning","illustrative_sensitivity","trace_availability","recorded_blocks")},indent=2))
    print("HAIKU CELLS")
    for c in sorted(haiku_cells,key=lambda c:-c["proxy_y_mean"]):
        print(c["policy"],"n",c["n"],"finished",c["completed"],"Q",round(c["q_mean"],2),"SD",round(c["q_sd"],2),"Y",round(c["proxy_y_mean"],2),"interrupt",c["interrupted_attempt_fraction"])
    print("USAGE",json.dumps(out["usage"]))


if __name__ == "__main__":
    main()
