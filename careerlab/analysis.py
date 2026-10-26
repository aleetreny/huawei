"""Actor-comparison analysis for Claude worker cells (problem A diagnostics).

Separates strategy quality (Y, completion, survival), execution (rejected actions,
extra sessions, non-game tool attempts, interruptions), speed and token use, per
actor configuration and per policy. Rank agreement between actors is reported
with the caveat that few shared policies cannot certify transfer.
"""

from __future__ import annotations

import json
import statistics as st
from collections import defaultdict
from pathlib import Path
from typing import Any

from careerlab import stats
from careerlab.store import Registry


def _actor_label(cfg: dict[str, Any]) -> str:
    label = cfg.get("model", cfg.get("name", "?"))
    if cfg.get("effort"):
        label += f"@{cfg['effort']}"
    if cfg.get("autocompact"):
        label += f"~{cfg['autocompact']}"
    if cfg.get("skills_mode") == "plugin":
        label += "#plugin"
    return label


def load_cells(reg: Registry, purposes: tuple[str, ...] = ("calibrate", "screen", "infra"), kind: str = "claude-cli") -> list[dict[str, Any]]:
    rows = reg.db.execute(
        "SELECT j.job_id, j.status, j.run_dir, j.purpose, p.name AS policy, p.family, a.config, e.outcome AS e_outcome, "
        "e.score AS e_score, e.survival_months AS e_months, e.steps AS e_steps, e.rejected_actions AS e_rejected, "
        "e.tokens AS e_usage, e.wall_s AS e_wall, e.interruption AS e_interruption FROM jobs j "
        "JOIN policies p USING(policy_id) JOIN actors a USING(actor_id) LEFT JOIN evaluations e USING(job_id) "
        "WHERE a.kind=? AND j.purpose IN (%s)" % ",".join("?" * len(purposes)),
        (kind, *purposes)).fetchall()
    out = []
    for r in rows:
        if r["run_dir"] and (Path(r["run_dir"]) / "result.json").exists():
            res = json.loads((Path(r["run_dir"]) / "result.json").read_text())
        elif r["e_outcome"]:  # imported from another machine: its run directory stayed there, the evaluation row did not
            res = {"outcome": r["e_outcome"], "quantitative_score": r["e_score"], "survival_months": r["e_months"],
                   "interruption": r["e_interruption"], "steps": r["e_steps"], "rejected_actions": r["e_rejected"] or 0,
                   "wall_seconds": r["e_wall"], "actor_usage": json.loads(r["e_usage"] or "{}")}
        else:
            continue
        usage = res.get("actor_usage") or {}
        tok = usage.get("tokens") or {}
        out.append({
            "job": r["job_id"], "policy": r["policy"], "family": r["family"], "actor": _actor_label(json.loads(r["config"])),
            "purpose": r["purpose"], "outcome": res["outcome"], "Q": res.get("quantitative_score"), "T": res.get("survival_months"),
            "failure": (res.get("failure_reason") or res.get("interruption") or "")[:40], "steps": res.get("steps"),
            "rejected": res.get("rejected_actions", 0), "extra_sessions": usage.get("extra_sessions", 0),
            "non_game": usage.get("non_game_tool_attempts", 0), "minutes": (res.get("wall_seconds") or 0) / 60,
            "cache_read_M": tok.get("cache_read_input_tokens", 0) / 1e6, "output_k": tok.get("output_tokens", 0) / 1e3,
            "usd_list": usage.get("cost_usd_list_price", 0.0),
        })
    return out


def summarise(cells: list[dict[str, Any]]) -> dict[str, Any]:
    by_actor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_cell: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for c in cells:
        by_actor[c["actor"]].append(c)
        by_cell[(c["actor"], c["policy"])].append(c)

    def y(c: dict[str, Any]) -> float:
        return stats.run_utility(c["Q"], c["T"], None, c["T"] == 48)

    actors = []
    for actor, cs in sorted(by_actor.items()):
        done = [c for c in cs if c["outcome"] != "interrupted"]
        actors.append({
            "actor": actor, "episodes": len(cs), "interrupted": len(cs) - len(done),
            "completion": round(sum(c["T"] == 48 for c in done) / max(len(done), 1), 2),
            "mean_Q": round(st.mean(c["Q"] for c in done), 1) if done else None,
            "mean_Y": round(st.mean(y(c) for c in done), 1) if done else None,
            "sd_Q": round(st.stdev(c["Q"] for c in done), 1) if len(done) > 1 else None,
            "mean_T": round(st.mean(c["T"] for c in done), 1) if done else None,
            "rejected_per_ep": round(st.mean(c["rejected"] for c in cs), 2),
            "extra_sessions": sum(c["extra_sessions"] for c in cs), "non_game_calls": sum(c["non_game"] for c in cs),
            "minutes_per_ep": round(st.mean(c["minutes"] for c in cs), 1),
            "minutes_per_month": round(sum(c["minutes"] for c in done) / max(sum(c["T"] for c in done), 1), 2),
            "cache_read_M_per_month": round(sum(c["cache_read_M"] for c in done) / max(sum(c["T"] for c in done), 1), 3),
            "usd_list_per_ep": round(st.mean(c["usd_list"] for c in cs), 2),
        })
    cells_tab = []
    for (actor, policy), cs in sorted(by_cell.items()):
        done = [c for c in cs if c["outcome"] != "interrupted"]
        cells_tab.append({"actor": actor, "policy": policy, "n": len(done),
                          "Q": [round(c["Q"], 1) for c in done], "T": [c["T"] for c in done],
                          "mean_Y": round(st.mean(y(c) for c in done), 1) if done else None,
                          "failures": [c["failure"] for c in done if c["T"] != 48]})
    # Rank agreement between actors on shared policies (descriptive only).
    means: dict[str, dict[str, float]] = defaultdict(dict)
    for row in cells_tab:
        if row["n"]:
            means[row["actor"]][row["policy"]] = row["mean_Y"]
    agreement = []
    names = sorted(means)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = sorted(set(means[a]) & set(means[b]))
            if len(shared) >= 3:
                ra = _ranks([means[a][p] for p in shared])
                rb = _ranks([means[b][p] for p in shared])
                agreement.append({"a": a, "b": b, "shared": len(shared), "same_top": shared[ra.index(max(ra))] == shared[rb.index(max(rb))],
                                  "spearman": round(_pearson(ra, rb), 2)})
    return {"actors": actors, "cells": cells_tab, "rank_agreement": agreement}


def _ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    for r, i in enumerate(order):
        ranks[i] = float(r + 1)
    return ranks


def _pearson(a: list[float], b: list[float]) -> float:
    ma, mb = st.mean(a), st.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else float("nan")


def markdown(summary: dict[str, Any]) -> str:
    lines = ["| Actor | eps | interrupted | completion | mean Q (sd) | mean Y | mean months | rejected/ep | min/ep | min/month | cache-read M/month | list-USD/ep |",
             "|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    for a in summary["actors"]:
        lines.append(f"| {a['actor']} | {a['episodes']} | {a['interrupted']} | {a['completion']} | {a['mean_Q']} ({a['sd_Q']}) | {a['mean_Y']} | {a['mean_T']} "
                     f"| {a['rejected_per_ep']} | {a['minutes_per_ep']} | {a['minutes_per_month']} | {a['cache_read_M_per_month']} | {a['usd_list_per_ep']} |")
    lines += ["", "| Actor | Policy | n | Q per episode | months | mean Y | early-exit causes |", "|---|---|---:|---|---|---:|---|"]
    for c in summary["cells"]:
        lines.append(f"| {c['actor']} | {c['policy']} | {c['n']} | {c['Q']} | {c['T']} | {c['mean_Y']} | {'; '.join(c['failures'])} |")
    if summary["rank_agreement"]:
        lines += ["", "| Actor A | Actor B | shared policies | same top | Spearman |", "|---|---|---:|---|---:|"]
        for r in summary["rank_agreement"]:
            lines.append(f"| {r['a']} | {r['b']} | {r['shared']} | {r['same_top']} | {r['spearman']} |")
    return "\n".join(lines)
