"""Independently verify assignment timing, delivered plans and public outcomes."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys


def audit(root):
    protocol=json.loads((root/"protocol.json").read_text())
    if hashlib.sha256((root/"protocol.json").read_bytes()).hexdigest()!=(root/"protocol-sha256.txt").read_text().strip():
        raise ValueError("Protocol integrity mismatch")
    archive=root/"public-trajectories.jsonl.gz"
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=(root/"archive-sha256.txt").read_text().strip():
        raise ValueError("Archive integrity mismatch")
    with gzip.open(archive,"rt") as stream:
        records=[json.loads(line) for line in stream]
    assignments=json.loads((root/"assignments.json").read_text())
    by_run={r["run"]:r for r in records}
    counts=defaultdict(Counter)
    checks=Counter()
    for pos,a in enumerate(assignments):
        if a["position"]!=pos or a["arm_index"]!=protocol["schedule"][pos]:
            raise ValueError("Random schedule mismatch")
        r=by_run[a["run"]]
        if r.get("assignment")!=a:
            raise ValueError("Assignment journal mismatch")
        matches=[i for i,s in enumerate(r["steps"]) if s["before"]["current_state"]==a["pre_state"]
            and s["phase"]=="energy" and (s["before"].get("current_event") or {}).get("remaining_energy")==3]
        if len(matches)!=1:
            raise ValueError("No unique public eligibility witness")
        index=matches[0]
        before=r["steps"][index]["before"]["current_state"]
        if before["time"]["current_month"]!=6 or before["status"]["level"]!="L2":
            raise ValueError("Ineligible assignment")
        if a["prior_explosions"]!=sum("Old landmines" in s["after"].get("events","") for s in r["steps"][:index]):
            raise ValueError("Incident count used future information or lost prior history")
        arm=protocol["arms"][a["arm_index"]]
        key="".join(str(int(arm[f])) for f in ("cleanup6","cleanup9","incident_guard"))
        row=counts[key]
        row["assigned"]+=1
        for s in r["steps"]:
            month=s["before"]["current_state"]["time"]["current_month"]
            if month>12:
                raise ValueError("Action outside horizon")
            if not s.get("applied") or s.get("ambiguous") or s.get("reply",{}).get("success") is not True:
                raise ValueError("Unconfirmed public action")
            if s["choice"] not in s["before"]["choices"]:
                raise ValueError("Choice not offered")
            if s.get("reason")=="persistent_incident_empirical_guard":
                if not arm["incident_guard"] or s["prior_explosions_before"]<1:
                    raise ValueError("Guard outside assigned condition")
        for month in (6,9):
            selected=[s for s in r["steps"] if s["before"]["current_state"]["time"]["current_month"]==month and s.get("reason")=="randomised_energy_plan"]
            actual=[s["choice"]["action"] for s in selected]
            plan=protocol["plans"]["cleanup" if arm[f"cleanup{month}"] else "growth"]
            if actual!=plan[:len(actual)] or len(actual)>len(plan):
                raise ValueError("Assigned plan not delivered")
            if actual==plan:
                if sum(s["choice"].get("energy_cost",0) for s in selected)!=3:
                    raise ValueError("Unequal-cost plan")
                checks[f"full_plan_{month}"]+=1
            if month==6 and actual!=plan:
                raise ValueError("Assigned game did not complete initial energy plan")
        if r["outcome"] not in ("eliminated","twelve_month_window"):
            row["interrupted"]+=1
            continue
        flags=r["final"]["current_state"]["simulation_flags"]
        failure=flags.get("failure_reason") or ""
        terminal=flags.get("alive") is False or flags.get("failed") is True
        alive=not terminal and r["final"]["current_state"]["time"]["current_month"]==13
        if (r["outcome"]=="twelve_month_window")!=alive:
            raise ValueError("Public outcome mismatch")
        promoted=any(s["before"]["current_state"]["status"]["level"]=="L2" and s["after"]["current_state"]["status"]["level"]=="L3"
            and s["after"]["current_state"]["time"]["current_month"]<=12 for s in r["steps"])
        row["resolved"]+=1
        row["trust_death"]+=terminal and "Trust crisis" in failure
        row["second_promotion"]+=promoted
        row["survived"]+=alive
        row["second_promotion_and_alive"]+=promoted and alive
    results=json.loads((root/"results.json").read_text())
    for key,c in counts.items():
        g=results["groups"][key]
        if g["assigned"]!=c["assigned"] or g["resolved"]!=c["resolved"]:
            raise ValueError("Report denominator mismatch")
        for metric in ("trust_death","second_promotion","second_promotion_and_alive","survived"):
            if g[metric]["count"]!=c[metric]:
                raise ValueError("Report outcome mismatch")
    result={"verified":True,"records":len(records),"assigned":len(assignments),"target":len(protocol["schedule"]),
        "groups":{k:dict(v) for k,v in counts.items()},"checks":dict(checks),
        "scope":"Random assignment precedes intervention, incident memory uses only past responses, assigned public energy plans and report outcomes agree with raw archive"}
    (root/"independent-audit.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="groups"},indent=2))


if __name__=="__main__":
    audit(Path(sys.argv[1]))
