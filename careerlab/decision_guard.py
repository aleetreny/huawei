"""Operational checks around the frozen statistical model (no gameplay)."""
from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

SELECTION_PURPOSES = ("pilot", "screen", "calibrate", "audit")


def actor_scope(reg, actor_id: str) -> tuple[str, dict]:
    row = reg.db.execute("SELECT kind,config FROM actors WHERE actor_id=?", (actor_id,)).fetchone()
    if row is None:
        raise ValueError("unknown actor")
    cfg = json.loads(row["config"])
    target = (row["kind"] == "jiuwenswarm-target" and cfg.get("route") == "competition-key"
              and cfg.get("model_name") == "deepseek-v4-flash" and cfg.get("mode") == "agent"
              and cfg.get("jiuwenswarm") == "0.2.4b3")
    return ("target" if target else "exploratory"), cfg


def environment_scope(reg, actor_id: str, env_id: str | None, purposes=SELECTION_PURPOSES) -> str | None:
    rows = reg.db.execute(
        "SELECT DISTINCT env_id FROM jobs WHERE actor_id=? AND origin=? AND purpose IN (%s)" % ",".join("?"*len(purposes)),
        (actor_id, reg.origin, *purposes)).fetchall()
    ids = {r[0] for r in rows}
    if env_id is None and len(ids) > 1:
        raise ValueError("multiple environments: pass env_id explicitly; cells cannot be pooled")
    return env_id or next(iter(ids), None)


def check_batch(reg, actor_id: str, env_id: str | None, job_ids: list[str] | None, cells: dict) -> list[str]:
    if job_ids is None:
        return ["unresolved launches; provide the completed batch job_ids"] if any(c["pending"] for c in cells.values()) else []
    if not job_ids or len(set(job_ids)) != len(job_ids):
        return ["batch must contain distinct job ids"]
    errors = []
    for jid in job_ids:
        row = reg.db.execute("SELECT * FROM jobs WHERE job_id=?", (jid,)).fetchone()
        if (row is None or row["origin"] != reg.origin or row["actor_id"] != actor_id
                or row["env_id"] != env_id or row["purpose"] not in SELECTION_PURPOSES):
            errors.append("batch job outside actor/environment/origin/development scope")
            continue
        latest = reg.db.execute(
            "SELECT j.status,e.outcome FROM jobs j LEFT JOIN evaluations e USING(job_id) "
            "WHERE j.origin=? AND j.policy_id=? AND j.actor_id=? AND j.env_id=? AND j.purpose=? AND j.replicate=? "
            "ORDER BY j.attempt DESC LIMIT 1",
            (reg.origin,row["policy_id"],actor_id,env_id,row["purpose"],row["replicate"])).fetchone()
        if latest["outcome"] not in ("completed", "eliminated"):
            errors.append("batch has unresolved/interrupted slots; finish or replace them before deciding")
    return sorted(set(errors))


def interruption_alarms(reg, actor_id: str, env_id: str | None) -> list[dict[str, Any]]:
    """All attempts count; a documented repair can close an old alarm window."""
    resolved = {}
    for row in reg.db.execute("SELECT payload FROM decisions WHERE kind='alarm_resolved' AND origin=?", (reg.origin,)):
        p = json.loads(row[0])
        if p.get("actor_id") == actor_id and p.get("env_id") == env_id:
            resolved[p["policy_id"]] = max(resolved.get(p["policy_id"],0),p["through_at"])
    groups = defaultdict(list)
    for row in reg.db.execute(
            "SELECT j.policy_id,j.updated_at,j.status,e.wall_s,e.completed FROM jobs j LEFT JOIN evaluations e USING(job_id) "
            "WHERE j.origin=? AND j.actor_id=? AND j.env_id=? AND j.purpose IN (%s)" % ",".join("?"*len(SELECTION_PURPOSES)),
            (reg.origin,actor_id,env_id,*SELECTION_PURPOSES)):
        if row["updated_at"] > resolved.get(row["policy_id"],0) and row["status"] in ("done","interrupted"):
            groups[row["policy_id"]].append(row)
    rates, alarms = {}, []
    for pid, rows in groups.items():
        n_int = sum(r["status"] == "interrupted" for r in rows)
        rate = n_int/len(rows)
        rates[pid] = rate
        if rate > 0.10:
            alarms.append({"policy_id":pid,"kind":"interruption_rate","interrupted":n_int,"attempts":len(rows),"rate":rate})
        completed = sorted(r["wall_s"] for r in rows if r["completed"] and r["wall_s"])
        if completed:
            median = (completed[(len(completed)-1)//2]+completed[len(completed)//2])/2
            if any(r["status"]=="interrupted" and (r["wall_s"] or 0)>median for r in rows):
                alarms.append({"policy_id":pid,"kind":"long_episode_interruption"})
    if len(rates)>1 and max(rates.values())>0 and (min(rates.values())==0 or max(rates.values())>2*min(rates.values())):
        alarms.append({"kind":"interruption_rate_ratio","rates":rates})
    return alarms


def family_sensitivity(data: dict) -> dict:
    from careerlab import stats
    views = {"registered":data,"singletons":{p:(p,ys) for p,(_,ys) in data.items()},
             "common":{p:("common",ys) for p,(_,ys) in data.items()}}
    summaries = {}
    for name, cells in views.items():
        posts = stats.partial_pool(cells)
        ranked = sorted(posts,key=lambda p:-posts[p].mean)
        summaries[name] = {"leader":ranked[0] if ranked else None,
                           "top": [{"policy_id":p,"mean":posts[p].mean,"sd":posts[p].sd} for p in ranked[:2]]}
    return {"leader_stable":len({v["leader"] for v in summaries.values()})<=1,"views":summaries,
            "interpretation":"sensitivity to grouping, not evidence that any grouping is true"}
