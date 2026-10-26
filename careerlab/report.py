"""Per-cell report under the pre-registered protocol (lab/protocol/prereg-v1.md)."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from careerlab import stats
from careerlab.store import Registry


def cell_report(reg: Registry, purpose: str | None = None, all_origins: bool = False) -> dict[str, Any]:
    """Y per episode, pooled posteriors per actor/epoch, anytime-valid intervals, survival and alarms."""
    query = ("SELECT e.*, p.name, p.family, a.kind AS actor_kind, json_extract(a.config,'$.name') AS actor_name "
             "FROM evaluations e JOIN policies p USING(policy_id) JOIN actors a USING(actor_id) JOIN jobs j USING(job_id) WHERE 1=1")
    args: list[Any] = []
    if not all_origins:
        query += " AND j.origin=?"
        args.append(reg.origin)
    if purpose:
        query += " AND e.purpose=?"
        args.append(purpose)
    rows = reg.db.execute(query + " ORDER BY e.launch_index", args).fetchall()
    groups: dict[tuple[str, str], dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        groups[(r["actor_id"], r["env_id"])][r["policy_id"]].append(r)
    out: dict[str, Any] = {"protocol": "careerlab-prereg-v1", "groups": []}
    for (actor_id, env_id), cells in groups.items():
        ys: dict[str, tuple[str, list[float]]] = {}
        table = []
        for pid, evs in cells.items():
            done = [e for e in evs if e["outcome"] in ("completed", "eliminated")]
            tokens = [json.loads(e["tokens"] or "{}").get("total_tokens") for e in done]
            y = [stats.run_utility(e["score"], e["survival_months"], t, bool(e["completed"])) for e, t in zip(done, tokens)]
            ys[pid] = (evs[0]["family"], y)
            interrupted, operator_stops = reg.db.execute(
                "SELECT COUNT(*), SUM(COALESCE(note,'') LIKE 'operator:%') FROM jobs WHERE policy_id=? AND actor_id=? AND env_id=? AND status='interrupted'"
                + (" AND purpose=?" if purpose else ""), (pid, actor_id, env_id, *([purpose] if purpose else []))).fetchone()
            operator_stops = operator_stops or 0
            times = [e["survival_months"] for e in done]
            events = [0 if e["completed"] else 1 for e in done]
            cs = stats.hedged_capital_cs([v / stats.Y_MAX for v in y]) if len(y) >= 2 else (0.0, 1.0)
            table.append({"policy": evs[0]["name"], "policy_id": pid, "family": evs[0]["family"], "n": len(done),
                          "interrupted_attempts": interrupted, "operator_stops": operator_stops, "resumed": sum(e["resumed"] for e in done),
                          "mean_Q": round(sum(e["score"] for e in done) / max(len(done), 1), 2),
                          "mean_Y": round(sum(y) / max(len(y), 1), 2),
                          "Y_anytime_95": [round(cs[0] * stats.Y_MAX, 1), round(cs[1] * stats.Y_MAX, 1)],
                          "completion": round(sum(e["completed"] for e in done) / max(len(done), 1), 3),
                          "rmst_48": round(stats.rmst(times, events), 2) if times else None})
        post = stats.partial_pool(ys)
        pbest = stats.prob_best(post)
        for row in table:
            p = post[row["policy_id"]]
            row.update(posterior_mean=round(p.mean, 2), posterior_sd=round(p.sd, 2), p_best=round(pbest[row["policy_id"]], 3))
        # Operator stops (quota throttling, incident clean-up) are independent of outcomes and excluded from the alarm.
        def _rate(r: dict[str, Any]) -> float:
            failures = r["interrupted_attempts"] - r["operator_stops"]
            return failures / (r["n"] + failures) if r["n"] + failures else 0.0
        alarms = [f"{r['policy']}: infrastructure interruption rate {_rate(r):.0%}" for r in table if _rate(r) > 0.10]
        actor = reg.db.execute("SELECT kind, config FROM actors WHERE actor_id=?", (actor_id,)).fetchone()
        out["groups"].append({"actor_id": actor_id, "actor_kind": actor["kind"], "env_id": env_id,
                              "cells": sorted(table, key=lambda r: -r["posterior_mean"]), "alarms": alarms})
    return out


def markdown(report: dict[str, Any]) -> str:
    lines = [f"Protocol {report['protocol']}. Y = 0.8 Q + 0.1 E (E imputed for non-target actors). Posteriors pool within family per actor and environment.", ""]
    for g in report["groups"]:
        lines += [f"### Actor {g['actor_kind']} `{g['actor_id']}` · environment `{g['env_id']}`", "",
                  "| Policy | n | interrupted (operator) | mean Q | mean Y | posterior Y (sd) | P(best) | anytime 95% Y | completion | RMST48 |",
                  "|---|---:|---:|---:|---:|---|---:|---|---:|---:|"]
        for r in g["cells"]:
            lines.append(f"| {r['policy']} | {r['n']} | {r['interrupted_attempts']} ({r['operator_stops']}) | {r['mean_Q']} | {r['mean_Y']} | {r['posterior_mean']} ({r['posterior_sd']}) "
                         f"| {r['p_best']} | {r['Y_anytime_95'][0]}–{r['Y_anytime_95'][1]} | {r['completion']} | {r['rmst_48']} |")
        lines += ["", "Alarms: " + ("; ".join(g["alarms"]) if g["alarms"] else "none"), ""]
    return "\n".join(lines)
