"""Block-boundary decisions under the pre-registered protocol (prereg-v1 sections 3-6).

For one actor configuration, collect each policy's run utilities in launch
order, keep only the prefix-complete runs, fit the family-pooled posterior,
check robustness across noise models and apply the action rules. The result is
recorded as a registry decision with its explanation, so every dormancy,
promotion or repeat can be audited later.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from careerlab import stats
from careerlab.store import Registry


def collect(reg: Registry, actor_id: str, env_id: str | None = None) -> dict[str, dict[str, Any]]:
    """policy_id -> {name, family, launches: [(replicate, Y or None)]} for one actor (all purposes)."""
    query = ("SELECT j.policy_id, j.replicate, j.attempt, j.status, j.purpose, p.name, p.family, e.score, e.survival_months, e.completed, e.outcome "
             "FROM jobs j JOIN policies p USING(policy_id) LEFT JOIN evaluations e USING(job_id) WHERE j.actor_id=?")
    args: list[Any] = [actor_id]
    if env_id:
        query += " AND j.env_id=?"
        args.append(env_id)
    cells: dict[str, dict[str, Any]] = {}
    slots: dict[tuple[str, str, int], list[Any]] = defaultdict(list)
    for r in reg.db.execute(query, args).fetchall():
        cells.setdefault(r["policy_id"], {"name": r["name"], "family": r["family"]})
        slots[(r["policy_id"], r["purpose"], r["replicate"])].append(r)
    launches: dict[str, list[tuple[int, Any]]] = defaultdict(list)
    for (pid, purpose, replicate), attempts in sorted(slots.items()):
        latest = max(attempts, key=lambda a: a["attempt"])
        if latest["outcome"] in ("completed", "eliminated"):
            value: Any = stats.run_utility(latest["score"], latest["survival_months"], None, bool(latest["completed"]))
        elif latest["status"] == "interrupted" and str(latest["outcome"]) == "interrupted":
            value = None  # infrastructure censoring is handled by the alarm; the slot stays unresolved
        else:
            value = None  # queued, leased or running: pending
        launches[pid].append((len(launches[pid]) + 1, value))
    for pid, ls in launches.items():
        cells[pid]["launches"] = ls
        cells[pid]["prefix"] = stats.prefix_complete(ls)
    return cells


def block_decision(reg: Registry, actor_id: str, env_id: str | None = None, record: bool = True) -> dict[str, Any]:
    cells = collect(reg, actor_id, env_id)
    data = {pid: (c["family"], c["prefix"]) for pid, c in cells.items() if c["prefix"]}
    posts = stats.partial_pool(data)
    robust = stats.decision_is_robust(data)
    decisions = stats.decide(posts)
    pbest = stats.prob_best(posts)
    rows = []
    for pid, d in sorted(decisions.items(), key=lambda kv: -posts[kv[0]].mean):
        p = posts[pid]
        rows.append({"policy": cells[pid]["name"], "policy_id": pid, "n_prefix": len(cells[pid]["prefix"]),
                     "pending": sum(v is None for _, v in cells[pid]["launches"]), "posterior_mean": round(p.mean, 2),
                     "posterior_sd": round(p.sd, 2), "p_best": round(pbest[pid], 3), "action": d.action, "reason": d.reason})
    out = {"actor_id": actor_id, "env_id": env_id, "robust": robust.status == "robust",
           "robustness_note": robust.explanation, "rows": rows}
    if record:
        reg.decide("block_decision", actor_id, out, "prereg-v1 sections 3-6 applied to prefix-complete runs of this actor")
    return out


def markdown(out: dict[str, Any]) -> str:
    lines = [f"Actor `{out['actor_id']}` — robustness across noise models: {out['robust']} ({out['robustness_note']})", "",
             "| Policy | runs in prefix | pending | posterior Y (sd) | P(best) | action | reason |", "|---|---:|---:|---|---:|---|---|"]
    for r in out["rows"]:
        lines.append(f"| {r['policy']} | {r['n_prefix']} | {r['pending']} | {r['posterior_mean']} ({r['posterior_sd']}) | {r['p_best']} | **{r['action']}** | {r['reason']} |")
    return "\n".join(lines)
