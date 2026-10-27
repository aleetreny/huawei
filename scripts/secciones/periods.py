"""Period summary for T18 (lab by game period): one row per (policy, cut actor).

Reads this machine's registry and each run's result.json ("periods": review snapshots
written by careerlab.truncate). Prints a markdown table; --json for the raw rows.

    uv run python scripts/secciones/periods.py [--purpose screen] [--json]
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from careerlab.config import load_settings


FLOORS = {1: (8, 3, 3), 2: (18, 6, 5), 3: (35, 18, 14), 4: (90, 30, 22), 5: (130, 45, 32)}  # black-box study (H6, H14); lab only


def at_floor(review: dict | None) -> bool:
    """Skill, Network and Output at the promotion floor of the level held before the review.

    The review is applied at the start of its month, before any choice, so the first state of
    the review month carries exactly the Skill, Network and Output the review judged."""
    if not review or not review.get("before") or not review.get("after"):
        return False
    level, snap = review["before"].get("level"), review["after"]
    floor = FLOORS.get(level)
    return bool(floor) and all((snap.get(k) or 0) >= f for k, f in zip(("skill", "network", "output"), floor))


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


BATCHES = Path(__file__).resolve().parents[2] / "lab" / "reports" / "secciones" / "batches"


def batch_jobs(name: str) -> set[str]:
    """Job ids of one batch, or of several joined by commas."""
    out: set[str] = set()
    for part in name.split(","):
        data = json.loads((BATCHES / f"{part}.json").read_text())
        out |= {j for jobs in data["arms"].values() for j in jobs}
    return out


def rows(purpose: str | None, actor_filter: str | None, batch: str | None = None) -> list[dict]:
    s = load_settings()
    reg = s.registry()
    q = ("SELECT j.job_id, j.run_dir, p.name, a.config, e.outcome, e.score, e.survival_months, e.dims FROM jobs j "
         "JOIN policies p USING(policy_id) JOIN actors a USING(actor_id) LEFT JOIN evaluations e USING(job_id) "
         "WHERE j.origin=? AND a.kind='claude-cli'")
    args = [s.origin]
    if purpose:
        q += " AND j.purpose=?"
        args.append(purpose)
    out = []
    keep = batch_jobs(batch) if batch else None
    for job_id, run_dir, name, cfg, outcome, score, months, dims in reg.db.execute(q, args):
        if keep is not None and job_id not in keep:
            continue
        cfg = json.loads(cfg)
        cut = cfg.get("stop_at_month")
        if actor_filter and str(cut) != actor_filter:
            continue
        res = {}
        if run_dir and (Path(run_dir) / "result.json").exists():
            res = json.loads((Path(run_dir) / "result.json").read_text())
        out.append({"job": job_id, "policy": name, "cut": cut, "outcome": outcome or "pending", "score": score,
                    "months": months, "periods": res.get("periods"), "usage": res.get("actor_usage"),
                    "dims": json.loads(dims) if dims else None, "failure": res.get("failure_reason")})
    return out


def summarize(rs: list[dict]) -> list[dict]:
    by = defaultdict(list)
    for r in rs:
        by[(r["policy"], r["cut"])].append(r)
    table = []
    for (pol, cut), group in sorted(by.items(), key=lambda kv: (str(kv[0][1]), kv[0][0])):
        played = [g for g in group if g["outcome"] in ("truncated", "completed", "eliminated")]
        n = len(played)
        rev = lambda g, k: next((x for x in (g["periods"] or {}).get("reviews", []) if x["review"] == k), None)
        r1 = [rev(g, 1) for g in played]
        promoted1 = sum(1 for x in r1 if x and x["promoted"])
        floor1 = sum(1 for x in r1 if at_floor(x))
        floor_prom = sum(1 for x in r1 if at_floor(x) and x["promoted"])
        dead = sum(1 for g in played if g["outcome"] == "eliminated")
        blow = sum(len((g["periods"] or {}).get("blowup_months", [])) for g in played)
        lvl = [((g["periods"] or {}).get("final_state") or {}).get("level") for g in played]
        lvl = [v for v in lvl if v]
        done = [g for g in played if g["outcome"] in ("completed", "eliminated")]
        qs = [g["score"] for g in done if g["score"] is not None]
        mean_q = sum(qs) / len(qs) if qs else None
        se_q = (math.sqrt(sum((x - mean_q) ** 2 for x in qs) / (len(qs) - 1)) / math.sqrt(len(qs))) if len(qs) > 1 else None
        tok = [((g["usage"] or {}).get("tokens") or {}).get("cache_read_input_tokens", 0) for g in played]
        fin = [g for g in played if g["outcome"] == "completed" and g["dims"]]
        dim_means = {k: round(sum(g["dims"].get(k) or 0 for g in fin) / len(fin), 1) for k in (fin[0]["dims"] if fin else {})}
        lo, hi = wilson(promoted1, n)
        table.append({"policy": pol, "cut": cut, "n": n, "pending": len(group) - n, "promoted_r1": promoted1,
                      "promoted_r1_ci": (round(lo, 2), round(hi, 2)), "floor_r1": floor1, "floor_promoted": floor_prom,
                      "eliminated": dead, "blowups": blow, "mean_level_end": round(sum(lvl) / len(lvl), 2) if lvl else None,
                      "completed": sum(g["outcome"] == "completed" for g in played), "mean_q": round(mean_q, 1) if mean_q else None,
                      "se_q": round(se_q, 1) if se_q else None, "cache_read_M": round(sum(tok) / max(n, 1) / 1e6, 2),
                      "dims_completed": dim_means, "failures": sorted(str(g["failure"])[:30] for g in done if g["outcome"] == "eliminated")})
    return table


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purpose")
    ap.add_argument("--cut", help="stop month of the actor; 'None' for full games")
    ap.add_argument("--batch", help="only the jobs of lab/reports/historico/secciones/batches/<name>.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = summarize(rows(a.purpose, a.cut, a.batch))
    if a.json:
        print(json.dumps(t, indent=1))
        return
    print("| policy | cut | n (pending) | promoted R1 (95% CI) | at floor before R1 (promoted) | eliminated | blow-ups | mean level at end | completed | Q mean ± SE | cache-read M/game |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in t:
        n = max(r["n"], 1)
        print(f"| {r['policy']} | {r['cut']} | {r['n']} ({r['pending']}) | {r['promoted_r1']}/{r['n']} = {100*r['promoted_r1']/n:.0f}% {r['promoted_r1_ci']} | "
              f"{r['floor_r1']} ({r['floor_promoted']}) | {r['eliminated']} | {r['blowups']} | {r['mean_level_end']} | {r['completed']} | "
              f"{r['mean_q']} ± {r['se_q']} | {r['cache_read_M']} |")


if __name__ == "__main__":
    main()
