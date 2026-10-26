"""Append-only, conservative admission ledger for the limited competition key.

Reservations are estimates, NOT provider-enforced per-request billing limits.
Unknown actual costs keep the reservation and stop admission until reconciled.
Only the canonical cloud origin may spend this shared key.
"""
from __future__ import annotations

import json
import time
import uuid
from decimal import Decimal, ROUND_CEILING


ACCOUNT = "competition-key-2026"
PHASES = ("pilot", "selection", "confirmation", "reserve")


class BudgetClosed(RuntimeError):
    pass


def micros(value) -> int:
    if isinstance(value, bool):
        raise ValueError("money must be a finite nonnegative number")
    try:
        n = Decimal(str(value))
    except Exception as exc:
        raise ValueError("invalid monetary amount") from exc
    if not n.is_finite() or n < 0:
        raise ValueError("money must be finite and nonnegative")
    return int((n*1_000_000).to_integral_value(rounding=ROUND_CEILING))


class TargetBudget:
    def __init__(self, registry):
        self.reg = registry

    def configure(self, total=50, pilot=3, selection=15, confirmation=20, reserve=12):
        if self.reg.origin:
            raise BudgetClosed("the shared key has one canonical cloud ledger; other origins cannot configure it")
        limits = dict(zip(PHASES,map(micros,(pilot,selection,confirmation,reserve))))
        total = micros(total)
        if not 0 < total <= 50_000_000 or sum(limits.values()) != total:
            raise ValueError("phase limits must sum to a positive total no greater than the authorised USD 50")
        cfg = {"total":total,"limits":limits,"max_open":1}
        with self.reg.tx():
            old = self.reg.db.execute("SELECT config FROM target_budget_accounts WHERE account=?",(ACCOUNT,)).fetchone()
            if old and json.loads(old[0]) != cfg:
                raise BudgetClosed("existing budget cannot be reset/reconfigured; its spend and reserve must be preserved")
            self.reg.db.execute("INSERT OR IGNORE INTO target_budget_accounts VALUES (?,?,?)",(ACCOUNT,json.dumps(cfg),time.time()))
        return self.status()

    def _project(self):
        account = self.reg.db.execute("SELECT config FROM target_budget_accounts WHERE account=?",(ACCOUNT,)).fetchone()
        if account is None:
            raise BudgetClosed("target budget is not configured")
        cfg = json.loads(account[0])
        jobs = {}
        for row in self.reg.db.execute("SELECT * FROM target_budget_events WHERE account=? ORDER BY rowid",(ACCOUNT,)):
            data = json.loads(row["payload"])
            jid = row["job_id"]
            if row["kind"] == "reserved":
                jobs[jid] = {"job_id":jid,"phase":data["phase"],"reserved":data["amount"],"state":"reserved","cost":None}
            elif jid in jobs:
                state = jobs[jid]
                if row["kind"] in ("settled","reconciled"):
                    state.update(state="settled",cost=data["cost"],reason=data.get("why"),
                                 overage_acknowledged=row["kind"]=="reconciled")
                else:
                    state["state"] = row["kind"]
        used = {p:0 for p in PHASES}
        for j in jobs.values():
            if j["state"] != "cancelled":
                used[j["phase"]] += j["cost"] if j["state"]=="settled" else j["reserved"]
        unknown = [j["job_id"] for j in jobs.values() if j["state"]=="uncertain"]
        over = [j["job_id"] for j in jobs.values() if j["cost"] is not None and j["cost"]>j["reserved"] and not j.get("overage_acknowledged")]
        return cfg,jobs,used,unknown,over

    def _event(self, jid, kind, payload, unique=False):
        key = f"{ACCOUNT}:{jid}:{kind}" if unique else uuid.uuid4().hex
        self.reg.db.execute("INSERT INTO target_budget_events VALUES (?,?,?,?,?,?)",
                            (key,ACCOUNT,jid,kind,json.dumps(payload,sort_keys=True),time.time()))

    def status(self):
        cfg,jobs,used,unknown,over = self._project()
        return {"account":ACCOUNT,"total_usd":cfg["total"]/1e6,"committed_usd":sum(used.values())/1e6,
                "remaining_usd":(cfg["total"]-sum(used.values()))/1e6,
                "phase_remaining_usd":{p:(cfg["limits"][p]-used[p])/1e6 for p in PHASES},
                "open_jobs":[j["job_id"] for j in jobs.values() if j["state"] in ("reserved","started","uncertain")],
                "unknown_cost_jobs":unknown,"over_estimate_jobs":over,
                "paused":bool(unknown or over or sum(used.values())>cfg["total"]),
                "limit_type":"admission reservations, not a provider billing cap"}

    def charge(self,jid):
        return self._project()[1].get(jid)

    def reserve(self, jid: str, phase: str, usd):
        if self.reg.origin:
            raise BudgetClosed("only the canonical cloud can spend the competition key")
        amount = micros(usd)
        if phase not in PHASES or not amount:
            raise ValueError("a known phase and positive reservation are required")
        with self.reg.tx():
            cfg,jobs,used,unknown,over = self._project()
            job = self.reg.db.execute("SELECT j.origin,a.kind,a.config FROM jobs j JOIN actors a USING(actor_id) WHERE job_id=?",(jid,)).fetchone()
            if job is None or job["origin"] or job["kind"]!="jiuwenswarm-target" or json.loads(job["config"]).get("route")!="competition-key":
                raise BudgetClosed("reservation must belong to a canonical competition-key target job")
            if jid in jobs:
                old = jobs[jid]
                if old["reserved"] != amount or old["phase"] != phase or old["state"] != "reserved":
                    raise BudgetClosed("job already attempted or reservation differs; reconcile rather than retry billing")
                return old
            if unknown or over:
                raise BudgetClosed("unknown/over-estimate cost must be reconciled before more spend")
            if sum(j["state"] in ("reserved","started") for j in jobs.values()) >= cfg["max_open"]:
                raise BudgetClosed("one paid episode at a time until its actual cost is reconciled")
            if used[phase]+amount>cfg["limits"][phase] or sum(used.values())+amount>cfg["total"]:
                raise BudgetClosed("phase or total budget would be exceeded; reserve is protected")
            if phase!="reserve" and sum(used[p] for p in PHASES if p!="reserve")+amount>cfg["total"]-cfg["limits"]["reserve"]:
                raise BudgetClosed("the protected reserve would be consumed")
            self._event(jid,"reserved",{"phase":phase,"amount":amount},unique=True)
        return {"job_id":jid,"phase":phase,"reserved":amount,"state":"reserved","cost":None}

    def start(self, jid):
        with self.reg.tx():
            _,jobs,_,unknown,over = self._project()
            if unknown or over or jid not in jobs or jobs[jid]["state"]!="reserved":
                raise BudgetClosed("job has no fresh reservation or ledger is paused")
            self._event(jid,"started",{},unique=True)

    def settle(self, jid, actual_usd=None, why="runner receipt"):
        cost = None if actual_usd is None else micros(actual_usd)
        with self.reg.tx():
            _,jobs,_,_,_ = self._project()
            if jid not in jobs or jobs[jid]["state"] not in ("started","uncertain","settled"):
                raise BudgetClosed("cannot settle an unstarted reservation")
            if jobs[jid]["state"]=="settled":
                if jobs[jid]["cost"]==cost:
                    return
                raise BudgetClosed("different receipt: use explicit reconciliation")
            if jobs[jid]["state"]=="uncertain" and cost is None:
                return
            self._event(jid,"uncertain" if cost is None else "settled",{"cost":cost,"why":why},unique=cost is not None)

    def reconcile(self, jid, actual_usd, why):
        if not why or not why.strip():
            raise ValueError("a receipt/reconciliation rationale is required")
        cost = micros(actual_usd)
        with self.reg.tx():
            _,jobs,_,_,_ = self._project()
            if jid not in jobs or jobs[jid]["state"] in ("reserved","cancelled"):
                raise BudgetClosed("no attempted job to reconcile")
            # An over-estimate cannot be hidden by reinitialising: a verified receipt
            # may correct it, but the original amount remains in the event log.
            self._event(jid,"reconciled",{"cost":cost,"why":why})

    def cancel(self, jid, why):
        with self.reg.tx():
            _,jobs,_,_,_ = self._project()
            if jid not in jobs or jobs[jid]["state"]!="reserved":
                raise BudgetClosed("started/uncertain charges cannot be released as unused")
            self._event(jid,"cancelled",{"why":why})


def receipt_cost(usage: dict):
    """Only explicit actual monetary fields; token counts alone are not a bill."""
    for key in ("billed_cost_usd","cost_usd","total_cost_usd"):
        value = usage.get(key)
        if value is not None:
            micros(value)
            return float(value)
    return None
