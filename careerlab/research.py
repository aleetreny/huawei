"""Budget-aware experiment proposals, diagnostics and frozen confirmation.

The LLM organiser still writes hypotheses/Skills. This module controls what may
be tested next; it never edits a frozen evaluator or declares a perfect policy.
"""
from __future__ import annotations

import json
import math
import time
from collections import Counter,defaultdict

import numpy as np

from careerlab import stats
from careerlab.budget import BudgetClosed,TargetBudget
from careerlab.decision_guard import SELECTION_PURPOSES,actor_scope,environment_scope,family_sensitivity
from careerlab.decisions import collect
from careerlab.store import canonical_hash


def _rows(reg,actor_id,env_id,purposes=SELECTION_PURPOSES):
    return reg.db.execute("SELECT e.*,j.origin,p.name,p.family FROM evaluations e JOIN jobs j USING(job_id) "
        "JOIN policies p USING(policy_id) WHERE j.origin=? AND j.actor_id=? AND j.env_id=? "
        "AND j.purpose IN (%s) AND e.outcome IN ('completed','eliminated')" % ",".join("?"*len(purposes)),
        (reg.origin,actor_id,env_id,*purposes)).fetchall()


def report(reg,actor_id,env_id=None):
    if not actor_id:
        raise ValueError("--actor-id is required")
    scope,_=actor_scope(reg,actor_id)
    env_id=environment_scope(reg,actor_id,env_id)
    groups=defaultdict(list)
    for row in _rows(reg,actor_id,env_id): groups[row["policy_id"]].append(row)
    cells=collect(reg,actor_id,env_id)
    data={p:(c["family"],c["prefix"]) for p,c in cells.items() if c["prefix"]}
    rows=[]
    for pid,items in groups.items():
        wins=[r for r in items if r["completed"]]; n=len(items); p=len(wins)/n
        z=1.959963984540054; den=1+z*z/n
        centre=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
        utilities=[]
        for r in items:
            u=json.loads(r["tokens"] or "{}")
            tokens=u.get("total_tokens") if scope=="target" else None
            if scope=="target" and (not isinstance(tokens,(int,float)) or tokens<=0): continue
            utilities.append(stats.run_utility(r["score"],r["survival_months"],tokens,bool(r["completed"])))
        # Descriptive posterior predictive sensitivity. Jeffreys on completion
        # allows unseen losses after 4/4 wins; it is not the selection model.
        rng=np.random.default_rng(int(pid[:8],16))
        success=np.array([r["score"] for r in wins])
        failed=np.array([r["score"] for r in items if not r["completed"]])
        probs=rng.beta(len(wins)+0.5,n-len(wins)+0.5,4000)
        done=rng.random((4000,3))<probs[:,None]
        q_success=rng.choice(success,(4000,3)) if len(success) else rng.uniform(0,100,(4000,3))
        q_failure=rng.choice(failed,(4000,3)) if len(failed) else rng.uniform(0,100,(4000,3))
        predictive=np.mean(np.where(done,q_success,q_failure),axis=1)
        rows.append({"policy_id":pid,"name":items[0]["name"],"n":n,"completed":len(wins),
            "completion_wilson95":[max(0,centre-half),min(1,centre+half)],"mean_q":float(np.mean([r["score"] for r in items])),
            "mean_y":float(np.mean(utilities)) if utilities else None,
            "completed_q":float(np.mean(success)) if len(success) else None,
            "eliminated_q":float(np.mean(failed)) if len(failed) else None,
            "predictive_three_run_q_interval90":np.quantile(predictive,[0.05,0.95]).tolist(),
            "predictive_assumptions":"Jeffreys completion + empirical conditional Q; unobserved outcome uses Uniform(0,100), sensitivity only",
            "portable_trace_count":sum(bool(r["evidence"] and json.loads(r["evidence"]).get("trace_status")=="available") for r in items)})
    return {"actor_id":actor_id,"env_id":env_id,"scope":scope,"rows":sorted(rows,key=lambda r:-(r["mean_y"] or 0)),
            "family_sensitivity":family_sensitivity(data),"claims":"development estimates, not fresh confirmation or causal effects"}


def record_proposal(reg,spec):
    required=("parent_policy_id","hypothesis","changed_factor","predicted_behaviour","refutation","learning_goal")
    if any(not isinstance(spec.get(k),str) or not spec[k].strip() for k in required):
        raise ValueError("one named changed_factor, parent, hypothesis, prediction, refutation and learning_goal are required")
    if not reg.verify_policy(spec["parent_policy_id"]):
        raise ValueError("proposal parent must be a frozen verified policy")
    proposal=dict(spec);proposal["schema_version"]=1
    ident=canonical_hash(proposal)[:16]
    old=reg.db.execute("SELECT decision_id FROM decisions WHERE kind='experiment_proposed' AND subject=? AND origin=?",(ident,reg.origin)).fetchone()
    if old is None:
        reg.decide("experiment_proposed",ident,proposal,"one falsifiable mechanism; no game is launched by proposing it")
    return {"proposal_id":ident,"spec":proposal,"paid_calls_started":0}


def _proxy_order(reg):
    for r in reg.db.execute("SELECT payload FROM decisions WHERE kind='block_decision' AND origin=? ORDER BY decision_id DESC",(reg.origin,)):
        p=json.loads(r[0]); aid=p.get("actor_id")
        actor=reg.db.execute("SELECT kind FROM actors WHERE actor_id=?",(aid,)).fetchone()
        if actor and actor[0]=="claude-cli":
            return [x["policy_id"] for x in p.get("rows",[]) if x.get("policy_id")]
    return []


def plan(reg,actor_id,env_id=None,slots=4,apply=False):
    if not actor_id or not isinstance(slots,int) or not 1<=slots<=40:
        raise ValueError("an actor and 1–40 slots are required")
    scope,_=actor_scope(reg,actor_id)
    env_id=environment_scope(reg,actor_id,env_id)
    if not env_id:
        raise ValueError("an explicit registered --env-id is needed for the first plan")
    policies={r["policy_id"]:dict(r) for r in reg.db.execute("SELECT * FROM policies WHERE status='active'")}
    jobs=[dict(r) for r in reg.db.execute("SELECT * FROM jobs WHERE origin=? AND actor_id=? AND env_id=?",(reg.origin,actor_id,env_id))]
    pending=[j for j in jobs if j["status"] in ("queued","leased","running")]
    cells=collect(reg,actor_id,env_id)
    data={p:(c["family"],c["prefix"]) for p,c in cells.items() if c["prefix"]}
    posts=stats.partial_pool(data)
    ranked=sorted(posts,key=lambda p:-posts[p].mean)
    requested=[]; blockers=[]; stage="exploration"; budget_info=None; reservation=1.5
    if pending:
        blockers.append("finish the current queued/leased/running block before creating another")
    if scope=="target":
        if reg.origin: raise BudgetClosed("one canonical cloud owns the shared paid ledger")
        ledger=TargetBudget(reg)
        budget_info=ledger.status()
        if budget_info["paused"] or budget_info["open_jobs"]:
            blockers.append("reconcile or complete the current paid charge first")
        _,charges,_,_,_=ledger._project()
        measured=[j["cost"]/1e6 for j in charges.values() if j["state"]=="settled"]
        reservation=max([1.5]+[1.25*x for x in measured])
        pilot=[j for j in jobs if j["purpose"]=="pilot" and j["status"]=="done"]
        frozen=reg.db.execute("SELECT decision_id,payload FROM decisions WHERE kind='research_freeze' AND subject=? AND origin=? ORDER BY decision_id DESC LIMIT 1",(actor_id,reg.origin)).fetchone()
        if frozen and json.loads(frozen["payload"])["env_id"]==env_id:
            freeze_data=json.loads(frozen["payload"]); stage="confirmation"
            for pid in freeze_data["policies"]:
                existing=sum(j["purpose"]=="confirm" and j["policy_id"]==pid and j["status"]!="interrupted" for j in jobs)
                requested.extend((pid,"confirm") for _ in range(max(0,freeze_data["confirm_n"]-existing)))
        elif len(pilot)<2:
            stage="pilot"
            baseline=next((p for p,v in policies.items() if v["name"]=="p0-minimal-v1"),next(iter(policies),None))
            leaders=[p for p in _proxy_order(reg) if p in policies and p!=baseline]
            candidates=[baseline]+leaders[:1] if baseline else []
            for i in range(2-len(pilot)):
                if candidates: requested.append((candidates[(len(pilot)+i)%len(candidates)],"pilot"))
        else:
            stage="selection"
            # Keep at most four mechanisms, including a proxy-negative control;
            # the cheap actor never earns pruning authority by implication.
            candidates=list(dict.fromkeys(ranked[:2]+[p for p in _proxy_order(reg)[:2] if p in policies]))
            outside=[p for p in reversed(_proxy_order(reg)) if p in policies and p not in candidates]
            if outside and len(candidates)<4: candidates.append(outside[0])
            for pid in candidates[:4]:
                n=len(cells.get(pid,{}).get("prefix",[]))
                if n<4: requested.append((pid,"calibrate"))
            if not requested and posts:
                requested=[(stats.top_two_thompson(posts,rng=np.random.default_rng(i)),"screen") for i in range(slots)]
        capacity=max(0,int(budget_info["phase_remaining_usd"][stage]//reservation))
        requested=requested[:min(slots,capacity)]
        if not requested and not blockers:
            blockers.append("phase budget/comparison plan exhausted; freeze finalists or explicitly reconcile/reallocate within USD 50")
    else:
        unseen=[p for p in policies if p not in cells]
        # Two active hypotheses per block. Existing cells receive top-two
        # allocation; one new candidate gets at least 20% when available.
        novel_slots=max(1,math.ceil(0.2*slots)) if unseen else 0
        if unseen: requested += [(unseen[0],"screen")]*novel_slots
        active={p:posts[p] for p in ranked[:2]}
        if active:
            requested += [(stats.top_two_thompson(active,rng=np.random.default_rng(i)),"screen") for i in range(slots-len(requested))]
        elif unseen:
            requested=[(unseen[0],"screen")]*slots
    request_counts=Counter(requested)
    snapshot=canonical_hash({"jobs":[(j["job_id"],j["status"],j["updated_at"]) for j in jobs],"actor":actor_id,"env":env_id,"requests":requested,"stage":stage})[:16]
    out={"plan_id":snapshot,"actor_id":actor_id,"env_id":env_id,"scope":scope,"stage":stage,
         "requests":[{"policy_id":p,"purpose":purpose,"n":n} for (p,purpose),n in request_counts.items()],
         "blockers":blockers,"budget":budget_info,"reservation_usd":reservation,"applied":False,
         "interpretation":"budget-aware allocation heuristic; no optimality or superiority claim"}
    if apply and not blockers:
        old=reg.db.execute("SELECT payload FROM decisions WHERE kind='research_plan_applied' AND subject=? AND origin=?",(snapshot,reg.origin)).fetchone()
        if old: return {**json.loads(old[0]),"already_applied":True}
        ids=[]
        for request in out["requests"]:
            ids+=reg.enqueue(request["policy_id"],actor_id,env_id,request["purpose"],request["n"])
        out.update(applied=True,job_ids=ids)
        reg.decide("research_plan_applied",snapshot,out,"bounded block; full episodes, no mutation of evaluator or old policy")
    return out


def freeze(reg,actor_id,env_id,policies,confirm_n,why):
    if not actor_id or not env_id or not policies or not 1<=len(policies)<=3 or len(set(policies))!=len(policies) or not why.strip():
        raise ValueError("freeze needs actor, environment, 1–3 distinct policies and rationale")
    if not isinstance(confirm_n,int) or isinstance(confirm_n,bool) or not 2<=confirm_n<=40:
        raise ValueError("prestate 2–40 fresh confirmation episodes per finalist")
    if actor_scope(reg,actor_id)[0]!="target":
        raise ValueError("official confirmation requires the target actor; proxy results remain exploratory")
    environment_scope(reg,actor_id,env_id)
    if any(not reg.verify_policy(p) for p in policies): raise ValueError("finalists must have verified frozen bytes")
    existing=reg.db.execute("SELECT 1 FROM jobs WHERE origin=? AND actor_id=? AND env_id=? AND purpose='confirm'",(reg.origin,actor_id,env_id)).fetchone()
    if existing: raise ValueError("confirmation already exists; do not re-freeze after seeing held-out data")
    payload={"actor_id":actor_id,"env_id":env_id,"policies":policies,"confirm_n":confirm_n,
             "selection_job_ids":[r["job_id"] for r in _rows(reg,actor_id,env_id)],"frozen_at":time.time()}
    did=reg.decide("research_freeze",actor_id,payload,why)
    return {"freeze_id":did,**payload}


def confirmation_report(reg,freeze_id):
    saved=reg.db.execute("SELECT * FROM decisions WHERE decision_id=? AND kind='research_freeze' AND origin=?",(freeze_id,reg.origin)).fetchone()
    if saved is None: raise ValueError("unknown freeze")
    f=json.loads(saved["payload"])
    rows=_rows(reg,f["actor_id"],f["env_id"],("confirm",))
    results=[]; data={}; complete=True
    for pid in f["policies"]:
        if not reg.verify_policy(pid): raise ValueError("a frozen finalist was modified")
        items=[r for r in rows if r["policy_id"]==pid and r["ingested_at"]>=f["frozen_at"]]
        ys=[]
        for r in items:
            tokens=json.loads(r["tokens"] or "{}").get("total_tokens")
            if tokens is None: continue
            ys.append(stats.run_utility(r["score"],r["survival_months"],tokens,bool(r["completed"])))
        complete=complete and len(ys)==f["confirm_n"]
        data[pid]=ys
        results.append({"policy_id":pid,"n":len(ys),"mean_y":float(np.mean(ys)) if ys else None})
    claims=[]
    if complete and len(f["policies"])>1:
        baseline=f["policies"][0]; alpha=0.05/(len(f["policies"])-1)
        for pid in f["policies"][1:]:
            bound=stats.welch_lower_bound(data[pid],data[baseline],alpha=alpha)
            claims.append({"policy_id":pid,"baseline":baseline,"lower_bound_y":bound,"beats_by_delta4":bound>4})
    return {"freeze_id":freeze_id,"complete":complete,"rows":results if complete else [],"claims":claims,
            "status":"single planned confirmation look" if complete else "held-out results hidden until the predeclared complete set is resolved",
            "feeds_selection":False}
