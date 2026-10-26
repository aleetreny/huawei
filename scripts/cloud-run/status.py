"""Write lab/reports/cloud-run-status.md from the registry (cloud lab run, 26-27 Oct 2026)."""

import json
import os
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from careerlab import analysis, decisions
from careerlab.config import load_settings
from careerlab.scheduler import latest_quota, weekly_allowance
from careerlab.store import Registry

SP = Path(os.environ.get("CLOUD_RUN_DIR", Path.home() / "careerlab-data" / "huawei" / "cloud-run"))  # logs, next.md, teacher.md, relevo.md
HAIKU, OPUSC = "08e9167a965ed82c", "eaaedd84f8f22e6d"
BY = "cloud-lab-run"


def utc(ts: float | None) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%d %b %H:%M UTC") if ts else "n/a"


def main() -> None:
    s = load_settings()
    reg = Registry(s.registry_path)
    out = [f"# CareerLab cloud run — status", "",
           f"Generated {utc(time.time())} in the Claude Code cloud container, branch `cloud-lab-run`. "
           "All scores are Claude-proxy results on the dev split (`real-dev`), not official scores and not the target actor "
           "(deepseek-v4-flash in JiuwenSwarm). Under prereg-v1 section 8 they cannot prune or select by themselves.", ""]

    jobs = {r[0]: r[1] for r in reg.db.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")}
    new_evals = sum(1 for r in reg.db.execute("SELECT j.run_dir FROM evaluations e JOIN jobs j USING(job_id) WHERE j.run_dir IS NOT NULL")
                    if (Path(r[0]) / "result.json").exists())
    batches = sorted((json.loads(p.read_text()) for p in (SP / "logs").glob("batch-*.done.json")), key=lambda b: b["batch"])
    util, resets = latest_quota(s.runs_dir)
    week, week_resets = latest_quota(s.runs_dir, window="seven_day")
    pace = json.loads((s.data_dir / "quota_cap.json").read_text()).get("weekly_pace") if (s.data_dir / "quota_cap.json").exists() else None
    allow = weekly_allowance(time.time(), week_resets, pace) if week_resets and time.time() < week_resets else None
    cap = json.loads((s.data_dir / "quota_cap.json").read_text()).get("max_five_hour") if (s.data_dir / "quota_cap.json").exists() else None
    out += ["## At a glance", "",
            f"- Jobs in the registry: {', '.join(f'{k} {v}' for k, v in sorted(jobs.items()))}.",
            f"- Episodes finished in this container: {new_evals}. Batches completed: {len(batches)}"
            + (f" (last at {batches[-1]['finished_utc']})." if batches else "."),
            f"- Five-hour quota (`careerlab.scheduler.latest_quota`): utilisation **{util if util is None else f'{util:.2f}'}**, "
            f"window resets {utc(resets)}; governor cap {cap}. The window is shared with every session on the account.",
            f"- Seven-day quota: utilisation **{week if week is None else f'{week:.2f}'}**, window resets {utc(week_resets)}; "
            f"weekly allowance now **{allow if allow is None else f'{allow:.3f}'}** (`weekly_allowance`: straight line from 0.10 at the window start "
            "to 0.90 at 2 Nov 00:00 UTC, about 0.126 a day). New episodes wait while either window is over its limit.",
            "- Claude CLI pinned to 2.1.303 (the version frozen in the registry's actor records; the container ships 2.1.310), "
            "so new runs land in the existing Haiku (`08e9167a965ed82c`) and opus~100k (`eaaedd84f8f22e6d`) cells.", ""]

    ceil = reg.db.execute("SELECT j.status, e.outcome, e.score, e.survival_months FROM jobs j JOIN policies p USING(policy_id) "
                          "LEFT JOIN evaluations e USING(job_id) WHERE p.family='ceiling' ORDER BY j.replicate, j.attempt").fetchall()
    games = [f"Q {r['score']:.1f}/T {r['survival_months']}" for r in ceil if r["outcome"] in ("completed", "eliminated")]
    out.insert(len(out) - 1, f"- **T13 Opus ceiling** (`claude-cli:opus@max~100k`, 2-slot lane, see `lab/reports/opus-ceiling/README.md`): "
               + (f"jobs {', '.join(f'{k} {v}' for k, v in sorted(__import__('collections').Counter(r['status'] for r in ceil).items()))}; "
                  f"finished games: {', '.join(games) or 'none yet'}." if ceil else "policy not registered yet; predictions pre-stated in the README."))
    rows = reg.db.execute("SELECT decision_id, at, payload FROM decisions WHERE kind='block_decision' AND subject=? ORDER BY decision_id",
                          (HAIKU,)).fetchall()
    hist = [(r["decision_id"], r["at"], json.loads(r["payload"])) for r in rows]
    out += ["## Latest pre-registered block decision (Haiku actor)", ""]
    if hist:
        did, at, payload = hist[-1]
        if payload.get("robust") is None:  # recorded before the display fix: the note holds the Robustness repr
            m = re.search(r"status='(\w+)'.*explanation=(['\"])(.*?)\2, leader_flip", payload.get("robustness_note", ""))
            if m:
                payload = {**payload, "robust": m.group(1) == "robust", "robustness_note": m.group(3)}
        out += [f"Registry decision #{did}, recorded {utc(at)} (`careerlab.decisions.block_decision`, record=True).", "",
                decisions.markdown(payload), ""]
        lead = [(d, a, p["rows"][0]["policy"], p["rows"][0]["posterior_mean"]) for d, a, p in hist if p.get("rows")]
        out += ["Leader history (stall trigger: leader posterior mean not improved by 2 Y-points over 3 decisions):", "",
                "| Decision | Time | Leader | Posterior Y |", "|---:|---|---|---:|"]
        out += [f"| #{d} | {utc(a)} | {name} | {m} |" for d, a, name, m in lead]
        if len(lead) >= 4:
            gain = lead[-1][3] - lead[-4][3]
            out += ["", f"Gain over the last three decisions: {gain:+.2f} → stall trigger **{'fires' if gain < 2 else 'does not fire'}**."]
        out.append("")

    out += ["## Progressive widening (Haiku cell)", "",
            "| Family | terminal Haiku episodes N_f | cap ⌈(1+N_f)^0.5⌉ | children so far |", "|---|---:|---:|---:|"]
    fams = reg.db.execute(
        "SELECT p.family, SUM(e.outcome IN ('completed','eliminated')) AS n FROM evaluations e JOIN policies p USING(policy_id) "
        "WHERE e.actor_id=? GROUP BY p.family ORDER BY n DESC", (HAIKU,)).fetchall()
    for f in fams:
        kids = reg.db.execute("SELECT COUNT(*) FROM policies WHERE family=? AND parents!='[]'", (f["family"],)).fetchone()[0]
        out.append(f"| {f['family']} | {f['n']} | {math.ceil((1 + f['n']) ** 0.5)} | {kids} |")
    out.append("")

    kids = reg.db.execute("SELECT * FROM policies WHERE created_by=? ORDER BY created_at", (BY,)).fetchall()
    out += ["## Children created in this cloud run", ""]
    if not kids:
        out += ["None yet.", ""]
    for k in kids:
        meta = json.loads(k["meta"] or "{}")
        sc = reg.db.execute("SELECT score, survival_months FROM evaluations WHERE policy_id=? AND actor_id=? AND outcome IN ('completed','eliminated')",
                            (k["policy_id"], HAIKU)).fetchall()
        res = ", ".join(f"Q {r[0]:.1f}/T {r[1]}" for r in sc) or "no finished runs yet"
        out += [f"### {k['name']} (`{k['policy_id']}`, family {k['family']})", "",
                f"- Parents: {', '.join(meta.get('parents', []))}; operator: {meta.get('operator', '?')}; idea origin: {meta.get('idea_origin', 'trace diagnostics')}.",
                f"- Hypothesis: {k['hypothesis']}", f"- Haiku runs so far: {res}.", ""]

    teach = SP / "teacher.md"
    out += ["## Teacher distillation", "", teach.read_text().strip() if teach.exists() else "(not started)", ""]
    dist = [k for k in kids if "teacher distillation" in (json.loads(k["meta"] or "{}").get("idea_origin") or "")]
    if dist:
        out += ["| Distilled child | Haiku runs finished | Q per run | pending |", "|---|---:|---|---:|"]
        for k in dist:
            sc = reg.db.execute("SELECT score FROM evaluations WHERE policy_id=? AND actor_id=? AND outcome IN ('completed','eliminated')",
                                (k["policy_id"], HAIKU)).fetchall()
            pend = reg.db.execute("SELECT COUNT(*) FROM jobs WHERE policy_id=? AND status IN ('queued','leased','running')", (k["policy_id"],)).fetchone()[0]
            out.append(f"| {k['name']} | {len(sc)} | {', '.join(f'{r[0]:.1f}' for r in sc) or '—'} | {pend} |")
        out.append("")

    opus = decisions.block_decision(reg, OPUSC, record=False)
    hrows = {r["policy"]: r for r in hist[-1][2]["rows"]} if hist else {}
    out += ["## Problem A check: Haiku vs opus~100k on shared policies", "",
            "opus~100k decision computed with the same rule but **not recorded** (only the Haiku decision is the block decision).", "",
            "| Policy | Haiku posterior Y (n) | opus~100k posterior Y (n) | opus~100k pending |", "|---|---|---|---:|"]
    for r in opus["rows"]:
        h = hrows.get(r["policy"])
        out.append(f"| {r['policy']} | {f'{h['posterior_mean']} ({h['n_prefix']})' if h else '—'} | {r['posterior_mean']} ({r['n_prefix']}) | {r['pending']} |")
    shared = [r for r in opus["rows"] if r["policy"] in hrows and r["n_prefix"]]
    if len(shared) >= 3:
        hr = analysis._ranks([hrows[r["policy"]]["posterior_mean"] for r in shared])
        orank = analysis._ranks([r["posterior_mean"] for r in shared])
        rho = analysis._pearson(hr, orank)
        top_h = max(shared, key=lambda r: hrows[r["policy"]]["posterior_mean"])["policy"]
        top_o = max(shared, key=lambda r: r["posterior_mean"])["policy"]
        out += ["", f"Shared policies with opus~100k data: {len(shared)}. Spearman of posterior means {rho:.2f}; "
                f"top policy Haiku `{top_h}`, opus~100k `{top_o}` ({'agree' if top_h == top_o else 'disagree'}). "
                "Descriptive only: with this few shared policies and 2–4 runs per cell, agreement cannot certify transfer "
                "(pruning authority needs ≥ 8 shared policies spanning ≥ 16 Y-points)."]
    out.append("")

    out += ["## Actor comparison (all Claude-proxy episodes, `careerlab.analysis`)", "",
            "Imported episodes from the Mac have no local `result.json`; their rows come from the registry evaluation "
            "(early-exit causes are blank for them).", "",
            analysis.markdown(analysis.summarise(analysis.load_cells(reg))), ""]

    nxt = SP / "next.md"
    out += ["## What is next", "", nxt.read_text().strip() if nxt.exists() else "(not written yet)", ""]
    relevo = SP / "relevo.md"
    out += ["## Relevo (hand-off)", "", relevo.read_text().strip() if relevo.exists() else "(not written yet)", ""]
    path = s.lab_dir / "reports" / "cloud-run-status.md"
    path.write_text("\n".join(out))
    print(path)


if __name__ == "__main__":
    main()
