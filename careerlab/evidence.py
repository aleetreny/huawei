"""Portable diagnostics from our own tool transcripts, never engine internals.

Observations and correlations are evidence, not causal effects or event answers
to put in a submission. A missing trace is explicitly marked, never invented.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

GRADE = re.compile(r"Half-year performance bonus\s*\(([SABCD][+-]?)\)", re.I)
STATS = ("health","dignity","skill","network","output","wealth","level","energy")


def tool_calls(run_dir: Path):
    if any(run_dir.glob("stream-*.jsonl")):
        from careerlab.digest import calls
        yield from calls(run_dir)
    elif (run_dir/"trajectory.jsonl").exists():
        for line in (run_dir/"trajectory.jsonl").read_text().splitlines():
            row = json.loads(line)
            if row.get("kind")=="obs":
                yield "observe",{},json.dumps(row["obs"])
            elif row.get("kind")=="act":
                yield "take_action",{"choice":row["choice"],"notes":row.get("notes","")},json.dumps(row.get("reply") or {"success":row.get("applied")})
    elif (run_dir/"target-transcript.jsonl").exists():
        # Official runner transcript adapter: only public tool invocations/replies.
        pending={}
        for line in (run_dir/"target-transcript.jsonl").read_text().splitlines():
            row = json.loads(line)
            payload=row.get("payload") or {}
            node=payload.get("delta",payload)
            if row.get("kind")=="tool_call":
                call=node.get("tool_call") or {}
                args=call.get("arguments",{})
                args=json.loads(args) if isinstance(args,str) else args
                pending[str(call.get("id") or node.get("tool_call_id") or "")]=(call.get("name",""),args)
            elif row.get("kind")=="tool_result":
                key=str(payload.get("tool_call_id") or node.get("tool_call_id") or "")
                name,args=pending.pop(key,(payload.get("tool_name") or node.get("tool_name", ""),{}))
                raw=(payload.get("raw_output") or node.get("raw_output") or {}).get("result")
                if raw is not None:
                    yield name.split("__")[-1],args,raw if isinstance(raw,str) else json.dumps(raw)


def _decoded(reply):
    if isinstance(reply,dict):
        return reply
    try:
        value=json.loads(reply)
        return value if isinstance(value,dict) else {}
    except (ValueError,TypeError):
        return {}


def _phase(obs):
    title=str((obs.get("current_event") or {}).get("title","")).lower()
    return "energy" if "quarterly energy" in title else "main" if "quarterly main" in title else "story"


def build_evidence(result: dict[str,Any], run_dir: Path | None=None) -> dict[str,Any]:
    ending=result.get("ending_score") or {}
    evidence={"schema_version":1,"job_id":result["job_id"],"outcome":result["outcome"],
              "score":result.get("quantitative_score"),"survival_months":result.get("survival_months"),
              "completed":bool(ending.get("completed")),"failure_reason":result.get("failure_reason"),
              "interruption":result.get("interruption"),"dimensions":ending.get("dimensions",[]),
              "usage":result.get("actor_usage") or {},"trace_status":"unavailable","parse_error":None,
              "decisions":[],"reviews":[],"promotions":[],"probes":[],"action_counts":{},
              "limits":{"max_decisions":4000,"max_probes":24},"truncated":False,
              "interpretation":"descriptive own-run evidence; not causal effects or optimal event answers"}
    if run_dir is None or not run_dir.exists():
        return evidence
    obs, counts, seen_reviews, last_level = {},Counter(),set(),None
    probe_counts=Counter()
    try:
        for name,args,reply in tool_calls(run_dir):
            value=_decoded(reply)
            if name.endswith("observe") and value:
                obs=value
                evidence["trace_status"]="available"
                current=obs.get("current_state") or {}
                state={k:v for k,v in (current.get("status") or {}).items() if k in STATS}
                when=current.get("time") or {}
                timepoint={k:when.get(k) for k in ("current_year","current_month")}
                if evidence["decisions"]:
                    evidence["decisions"][-1]["observed_after"]=state
                level=state.get("level")
                if last_level is not None and level is not None and level!=last_level:
                    evidence["promotions"].append({**timepoint,"from":last_level,"to":level})
                last_level=level if level is not None else last_level
                feedback=str(obs.get("events") or "")
                for grade in GRADE.findall(feedback):
                    key=(*timepoint.values(),grade)
                    if key not in seen_reviews:
                        evidence["reviews"].append({**timepoint,"grade":grade,"level_observed":level,"feedback":feedback[:1500]})
                        seen_reviews.add(key)
                flags=current.get("simulation_flags") or {}
                evidence["failure_reason"]=flags.get("failure_reason") or evidence["failure_reason"]
                phase=_phase(obs)
                if obs.get("choices") and probe_counts[phase]<8 and len(evidence["probes"])<24:
                    evidence["probes"].append({"index":len(evidence["decisions"]),"phase":phase,"observation":obs})
                    probe_counts[phase]+=1
            elif name.endswith("take_action") and obs:
                if len(evidence["decisions"])>=4000:
                    evidence["truncated"]=True
                    break
                selected=next((c for c in obs.get("choices",[]) if c.get("choice")==args.get("choice")),{})
                phase=_phase(obs)
                action=str(selected.get("action") or selected.get("text") or "unknown")
                state=(obs.get("current_state") or {})
                counts[f"{phase}:{action}"]+=1
                evidence["decisions"].append({"index":len(evidence["decisions"]),"phase":phase,
                    "time":state.get("time") or {},"observed_before":{k:v for k,v in (state.get("status") or {}).items() if k in STATS},
                    "feedback":str(obs.get("events") or "")[:1500],"action":action,"choice":args.get("choice"),
                    "energy_cost":selected.get("energy_cost"),"notes":str(args.get("notes") or "")[:1000],
                    "success":value.get("success"),"observed_after":None})
    except (OSError,ValueError,KeyError,TypeError) as exc:
        evidence["parse_error"]=type(exc).__name__
        evidence["trace_status"]="partial" if evidence["decisions"] else "unreadable"
    evidence["action_counts"]=dict(counts)
    evidence["execution"]={"actions_observed":len(evidence["decisions"]),"actions_reported":result.get("steps",0),
                            "rejected_reported":result.get("rejected_actions",0),
                            "note_modes":dict(Counter(d["notes"].split(":",1)[0][:40] for d in evidence["decisions"] if d["notes"]))}
    return evidence


def mechanism_check(evidence: dict, expected: dict) -> dict:
    """Lab-only manipulation check; never removes a low score from evaluation."""
    counts=evidence.get("action_counts") or {}
    actual=sum(v for k,v in counts.items() if expected.get("action_contains","").lower() in k.lower())
    minimum=expected.get("min_occurrences",1)
    if not isinstance(minimum,int) or isinstance(minimum,bool) or minimum<1 or not expected.get("action_contains"):
        raise ValueError("an action fragment and positive minimum are required")
    return {"observed":actual,"expected_minimum":minimum,
            "status":"unavailable" if evidence.get("trace_status")!="available" else "observed" if actual>=minimum else "not_observed",
            "interpretation":"execution check only; keep every scored episode in intention-to-treat results"}
