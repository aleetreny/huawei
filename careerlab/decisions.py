"""Block-boundary decisions under the pre-registered protocol (prereg-v1 sections 3-6).

For one actor configuration, collect each policy's run utilities in launch
order, keep only the prefix-complete runs, fit the family-pooled posterior,
check robustness across noise models and apply the action rules. The result is
recorded as a registry decision with its explanation, so every dormancy,
promotion or repeat can be audited later.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from typing import Any

from careerlab import stats
from careerlab.store import Registry
from careerlab.decision_guard import (SELECTION_PURPOSES, actor_scope, check_batch, environment_scope,
                                     family_sensitivity, interruption_alarms)


def collect(reg: Registry, actor_id: str, env_id: str | None = None) -> dict[str, dict[str, Any]]:
    """policy_id -> {name, family, launches: [(replicate, Y or None)]} for one actor (all purposes)."""
    scope, _ = actor_scope(reg, actor_id)
    env_id = environment_scope(reg, actor_id, env_id)
    query = ("SELECT j.policy_id, j.replicate, j.attempt, j.status, j.purpose,j.created_at,p.name,p.family, "
             "e.score,e.survival_months,e.completed,e.outcome,e.tokens FROM jobs j JOIN policies p USING(policy_id) "
             "LEFT JOIN evaluations e USING(job_id) WHERE j.actor_id=? AND j.origin=? AND j.purpose IN (%s)" %
             ",".join("?"*len(SELECTION_PURPOSES)))
    args: list[Any] = [actor_id, reg.origin, *SELECTION_PURPOSES]
    if env_id:
        query += " AND j.env_id=?"
        args.append(env_id)
    cells: dict[str, dict[str, Any]] = {}
    slots: dict[tuple[str, str, int], list[Any]] = defaultdict(list)
    for r in reg.db.execute(query, args).fetchall():
        cells.setdefault(r["policy_id"], {"name": r["name"], "family": r["family"],"missing_usage":False})
        slots[(r["policy_id"], r["purpose"], r["replicate"])].append(r)
    launches: dict[str, list[tuple[int, Any]]] = defaultdict(list)
    for (pid, purpose, replicate), attempts in sorted(slots.items(), key=lambda item:(min(r["created_at"] for r in item[1]),item[0])):
        latest = max(attempts, key=lambda a: a["attempt"])
        if latest["outcome"] in ("completed", "eliminated"):
            usage = json.loads(latest["tokens"] or "{}")
            tokens = usage.get("total_tokens") if scope == "target" else None
            if scope == "target" and (not isinstance(tokens,(int,float)) or isinstance(tokens,bool) or not math.isfinite(tokens) or tokens<=0):
                cells[pid]["missing_usage"] = True
                value = None
            else:
                value = stats.run_utility(latest["score"], latest["survival_months"], tokens, bool(latest["completed"]))
        elif latest["status"] == "interrupted" and str(latest["outcome"]) == "interrupted":
            value = None  # infrastructure censoring is handled by the alarm; the slot stays unresolved
        else:
            value = None  # queued, leased or running: pending
        launches[pid].append((len(launches[pid]) + 1, value))
    for pid, ls in launches.items():
        cells[pid]["launches"] = ls
        cells[pid]["prefix"] = stats.prefix_complete(ls)
        cells[pid]["pending"] = sum(v is None for _,v in ls)
    return cells


def block_decision(reg: Registry, actor_id: str, env_id: str | None = None, record: bool = True,
                   job_ids: list[str] | None = None) -> dict[str, Any]:
    scope, cfg = actor_scope(reg, actor_id)
    env_id = environment_scope(reg, actor_id, env_id)
    cells = collect(reg, actor_id, env_id)
    data = {pid: (c["family"], c["prefix"]) for pid, c in cells.items() if c["prefix"]}
    posts = stats.partial_pool(data)
    robust = (stats.decision_is_robust(data) if data else
              stats.Robustness("inconclusive", {}, {}, "no resolved development episodes", False, []))
    decisions = stats.decide(posts)
    pbest = stats.prob_best(posts)
    blockers = check_batch(reg,actor_id,env_id,job_ids,cells)
    alarms = interruption_alarms(reg,actor_id,env_id)
    if alarms:
        blockers.append("unresolved interruption alarms")
    if any(c["missing_usage"] for c in cells.values()):
        blockers.append("target token counts missing; cannot impute official efficiency")
    if not robust.status == "robust":
        blockers.append("statistical robustness inconclusive")
    sensitivity = family_sensitivity(data)
    if not sensitivity["leader_stable"]:
        blockers.append("leader changes under family grouping sensitivity")
    rows = []
    for pid, d in sorted(decisions.items(), key=lambda kv: -posts[kv[0]].mean):
        p = posts[pid]
        action = "INCONCLUSIVE" if blockers else (d.action if scope == "target" else "EXPLORE_"+d.action)
        rows.append({"policy": cells[pid]["name"], "policy_id": pid, "n_prefix": len(cells[pid]["prefix"]),
                     "pending": sum(v is None for _, v in cells[pid]["launches"]), "posterior_mean": round(p.mean, 2),
                     "posterior_sd": round(p.sd, 2), "p_best": round(pbest[pid], 3), "action": action,
                     "suggested_action":d.action,"executable":not blockers and scope=="target",
                     "reason": "; ".join(blockers) if blockers else d.reason})
    out = {"actor_id": actor_id, "env_id": env_id, "robust": robust.status == "robust",
           "robustness_note": robust.explanation, "rows": rows,"schema_version":2,"scope":scope,
           "protocol":"operational-v2","purposes":list(SELECTION_PURPOSES),"batch_job_ids":job_ids,
           "blockers":blockers,"alarms":alarms,"family_sensitivity":sensitivity,
           "can_select":scope=="target" and not blockers}
    if record:
        reg.decide("block_decision", actor_id, out, "prereg-v1 sections 3-6 applied to prefix-complete runs of this actor")
    return out


def markdown(out: dict[str, Any]) -> str:
    lines = [f"Actor `{out['actor_id']}` — robustness across noise models: {out['robust']} ({out['robustness_note']})", "",
             "| Policy | runs in prefix | pending | posterior Y (sd) | P(best) | action | reason |", "|---|---:|---:|---|---:|---|---|"]
    for r in out["rows"]:
        lines.append(f"| {r['policy']} | {r['n_prefix']} | {r['pending']} | {r['posterior_mean']} ({r['posterior_sd']}) | {r['p_best']} | **{r['action']}** | {r['reason']} |")
    return "\n".join(lines)
