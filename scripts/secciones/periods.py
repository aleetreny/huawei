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


def at_floor(snap: dict | None, level: int) -> bool:
    """L1 promotion floor seen in the black-box study (Skill one under its stall point, Network and Output at theirs)."""
    if not snap or snap.get("level") != level or level != 1:
        return False
    return (snap.get("skill") or 0) >= 8 and (snap.get("network") or 0) >= 3 and (snap.get("output") or 0) >= 3


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def rows(purpose: str | None, actor_filter: str | None) -> list[dict]:
    s = load_settings()
    reg = s.registry()
    q = ("SELECT j.job_id, j.run_dir, p.name, a.config, e.outcome, e.score, e.survival_months FROM jobs j "
         "JOIN policies p USING(policy_id) JOIN actors a USING(actor_id) LEFT JOIN evaluations e USING(job_id) "
         "WHERE j.origin=? AND a.kind='claude-cli'")
    args = [s.origin]
    if purpose:
        q += " AND j.purpose=?"
        args.append(purpose)
    out = []
    for job_id, run_dir, name, cfg, outcome, score, months in reg.db.execute(q, args):
        cfg = json.loads(cfg)
        cut = cfg.get("stop_at_month")
        if actor_filter and str(cut) != actor_filter:
            continue
        res = {}
        if run_dir and (Path(run_dir) / "result.json").exists():
            res = json.loads((Path(run_dir) / "result.json").read_text())
        out.append({"job": job_id, "policy": name, "cut": cut, "outcome": outcome or "pending", "score": score,
                    "months": months, "periods": res.get("periods"), "usage": res.get("actor_usage")})
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
        floor1 = sum(1 for x in r1 if x and at_floor(x.get("before"), 1))
        floor_prom = sum(1 for x in r1 if x and at_floor(x.get("before"), 1) and x["promoted"])
        dead = sum(1 for g in played if g["outcome"] == "eliminated")
        blow = sum(len((g["periods"] or {}).get("blowup_months", [])) for g in played)
        lvl = [((g["periods"] or {}).get("final_state") or {}).get("level") for g in played]
        lvl = [v for v in lvl if v]
        done = [g for g in played if g["outcome"] in ("completed", "eliminated")]
        qs = [g["score"] for g in done if g["score"] is not None]
        mean_q = sum(qs) / len(qs) if qs else None
        se_q = (math.sqrt(sum((x - mean_q) ** 2 for x in qs) / (len(qs) - 1)) / math.sqrt(len(qs))) if len(qs) > 1 else None
        tok = [((g["usage"] or {}).get("tokens") or {}).get("cache_read_input_tokens", 0) for g in played]
        lo, hi = wilson(promoted1, n)
        table.append({"policy": pol, "cut": cut, "n": n, "pending": len(group) - n, "promoted_r1": promoted1,
                      "promoted_r1_ci": (round(lo, 2), round(hi, 2)), "floor_r1": floor1, "floor_promoted": floor_prom,
                      "eliminated": dead, "blowups": blow, "mean_level_end": round(sum(lvl) / len(lvl), 2) if lvl else None,
                      "completed": sum(g["outcome"] == "completed" for g in played), "mean_q": round(mean_q, 1) if mean_q else None,
                      "se_q": round(se_q, 1) if se_q else None, "cache_read_M": round(sum(tok) / max(n, 1) / 1e6, 2)})
    return table


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purpose")
    ap.add_argument("--cut", help="stop month of the actor; 'None' for full games")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = summarize(rows(a.purpose, a.cut))
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
