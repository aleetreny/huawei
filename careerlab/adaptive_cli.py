"""Operational commands for the existing lab; no paid calls except `run` target."""
from __future__ import annotations

import getpass
import json
import math
import os
import time
from pathlib import Path

from careerlab.config import load_settings


def _print(value):
    print(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False))


def budget_command(args):
    from careerlab.budget import TargetBudget
    s=load_settings(); reg=s.registry(); budget=TargetBudget(reg)
    if args.action=="init":
        budget.configure(total=args.total_usd)
    elif args.action=="reconcile":
        if not args.job_id or args.actual_usd is None or not args.why:
            raise ValueError("reconcile needs --job-id, --actual-usd and --why (verified receipt)")
        budget.reconcile(args.job_id,args.actual_usd,args.why)
    elif args.action=="cancel":
        if not args.job_id or not args.why:
            raise ValueError("cancel needs an unstarted --job-id and --why")
        budget.cancel(args.job_id,args.why)
    _print(budget.status())
    return 0


def target_status(args):
    from careerlab.actors.official_runner import credential_status
    from careerlab.budget import BudgetClosed,TargetBudget
    s=load_settings(); result=credential_status(s)
    try: result["budget"]=TargetBudget(s.registry()).status()
    except BudgetClosed: result["budget"]={"configured":False}
    result["paid_calls_started"]=0
    _print(result)
    return 0 if result["configured"] else 2


def configure_target(args):
    from careerlab.actors.official_runner import credentials_path
    s=load_settings(); path=Path(args.env_file).expanduser().resolve() if args.env_file else credentials_path(s)
    if path.is_relative_to(s.repo_root.resolve()):
        raise ValueError("store credentials outside the repository, not in versioned project files")
    if path.exists():
        raise ValueError("credential file already exists; edit it privately rather than overwriting it")
    base=input("Official API_BASE from organiser: ").strip()
    model=input("Official MODEL_NAME [deepseek-v4-flash]: ").strip() or "deepseek-v4-flash"
    key=getpass.getpass("Competition API key (hidden): ").strip()
    if not base.startswith("https://") or model not in ("deepseek-v4-flash","deepseek/deepseek-v4-flash") or not key:
        raise ValueError("an HTTPS official base, designated model and nonempty key are required")
    if any("\n" in v or "\r" in v for v in (base,model,key)):
        raise ValueError("credential values must each occupy one line")
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"w") as out:
        out.write(f"API_BASE={base}\nAPI_KEY={key}\nMODEL_NAME={model}\n")
    _print({"configured":True,"env_file":str(path),"paid_calls_started":0,
            "next":"set CAREERLAB_TARGET_ENV to this path in the cloud runner environment"})
    return 0


def decision_command(args):
    from careerlab.decisions import block_decision,markdown
    s=load_settings(); reg=s.registry()
    jobs=None
    if args.batch:
        batch=json.loads(Path(args.batch).read_text())
        jobs=[j["job_id"] for j in batch["jobs"] if j["actor_id"]==args.actor_id and (not args.env_id or j["env_id"]==args.env_id)]
    result=block_decision(reg,args.actor_id,args.env_id,record=args.record,job_ids=jobs)
    print(markdown(result)) if args.markdown else _print(result)
    return 0


def resolve_alarm(args):
    s=load_settings(); reg=s.registry()
    through=args.through_at if args.through_at is not None else time.time()
    if not math.isfinite(through) or through<=0 or through>time.time() or not args.why.strip():
        raise ValueError("an actual past repair boundary and rationale are required")
    payload={"actor_id":args.actor_id,"env_id":args.env_id,"policy_id":args.policy_id,"through_at":through}
    reg.decide("alarm_resolved",args.policy_id,payload,args.why)
    _print(payload)
    return 0


def evidence_command(args):
    from careerlab.evidence import build_evidence
    s=load_settings(); reg=s.registry(); result=[]
    rows=reg.db.execute("SELECT e.*,j.run_dir,j.origin FROM evaluations e JOIN jobs j USING(job_id) WHERE j.origin=?"+
                        (" AND j.job_id=?" if args.job_id else ""),(reg.origin,args.job_id) if args.job_id else (reg.origin,)).fetchall()
    for row in rows:
        evidence=json.loads(row["evidence"]) if row["evidence"] else None
        if args.backfill:
            run=Path(row["run_dir"]) if row["run_dir"] else None
            if run and (run/"result.json").exists():
                evidence=build_evidence(json.loads((run/"result.json").read_text()),run)
                with reg.tx():
                    reg.db.execute("UPDATE evaluations SET evidence=? WHERE job_id=?",(json.dumps(evidence),row["job_id"]))
        result.append({"job_id":row["job_id"],"evidence":evidence})
    if args.out:
        Path(args.out).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    else:
        _print(result)
    return 0


def research_command(args):
    from careerlab.research import report,plan,freeze,confirmation_report,record_proposal
    s=load_settings(); reg=s.registry()
    if args.action=="report": result=report(reg,args.actor_id,args.env_id)
    elif args.action=="plan": result=plan(reg,args.actor_id,args.env_id,slots=args.slots,apply=args.apply)
    elif args.action=="freeze": result=freeze(reg,args.actor_id,args.env_id,args.policies,args.confirm_n,args.why)
    elif args.action=="confirm": result=confirmation_report(reg,args.freeze_id)
    else: result=record_proposal(reg,json.loads(Path(args.spec).read_text()))
    _print(result)
    return 0


def add_commands(sub):
    b=sub.add_parser("budget",help="single cloud admission ledger; never prints key values")
    b.add_argument("action",choices=["init","status","reconcile","cancel"])
    b.add_argument("--total-usd",type=float,default=50)
    b.add_argument("--job-id");b.add_argument("--actual-usd",type=float);b.add_argument("--why")
    b.set_defaults(fn=budget_command)
    sub.add_parser("target-status",help="read-only credential/budget preflight; no API requests").set_defaults(fn=target_status)
    c=sub.add_parser("target-configure",help="interactive hidden key entry into an untracked external file")
    c.add_argument("--env-file");c.set_defaults(fn=configure_target)
    d=sub.add_parser("decision",help="guarded comparison; target and exploratory scopes stay distinct")
    d.add_argument("--actor-id",required=True);d.add_argument("--env-id");d.add_argument("--batch")
    d.add_argument("--record",action="store_true");d.add_argument("--markdown",action="store_true");d.set_defaults(fn=decision_command)
    a=sub.add_parser("resolve-alarm",help="record a verified infrastructure repair boundary")
    for name in ("actor-id","env-id","policy-id","why"): a.add_argument("--"+name,required=True)
    a.add_argument("--through-at",type=float);a.set_defaults(fn=resolve_alarm)
    e=sub.add_parser("evidence",help="portable diagnostics from own transcripts, never game internals")
    e.add_argument("--job-id");e.add_argument("--out");e.add_argument("--backfill",action="store_true");e.set_defaults(fn=evidence_command)
    r=sub.add_parser("research",help="budget-aware plan, hypothesis archive and held-out confirmation")
    r.add_argument("action",choices=["report","plan","freeze","confirm","propose"])
    r.add_argument("--actor-id");r.add_argument("--env-id");r.add_argument("--slots",type=int,default=4)
    r.add_argument("--apply",action="store_true");r.add_argument("--policies",nargs="+")
    r.add_argument("--confirm-n",type=int,default=5);r.add_argument("--why",default="")
    r.add_argument("--freeze-id",type=int);r.add_argument("--spec");r.set_defaults(fn=research_command)
