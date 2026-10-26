"""Compact, readable digests of Claude worker games for trace-driven child generation.

A worker's stream-json transcript is about 1.6 MB per 48-month game. The digest
keeps what a policy author needs: the visible state before each decision, the
event, the option taken and the ones declined, the worker's notes and the
feedback the game printed (reviews, warnings, promotions). Everything comes from
the official tool replies the worker saw; nothing is read from the engine.
Digests are development material only: Skills derived from them must state
general behaviour and pass the compliance linter (no event titles or answers).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from careerlab.store import Registry

GRADE = re.compile(r"Half-year performance bonus \(([A-E][+-]?)\)")
STAT_KEYS = ("health", "dignity", "skill", "network", "level", "output", "wealth", "energy")


def _short(text: str, n: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1] + "…"


def _tool_text(content: Any) -> str:
    return content if isinstance(content, str) else "".join(c.get("text", "") for c in content if isinstance(c, dict))


def calls(run_dir: Path) -> list[tuple[str, dict[str, Any], str]]:
    """(tool, input, reply text) for every game tool call, across continuation streams in order."""
    out: list[tuple[str, dict[str, Any], str]] = []
    streams = sorted(run_dir.glob("stream-*.jsonl"), key=lambda p: int(p.stem.split("-")[1]))
    for stream in streams:
        pending: dict[str, tuple[str, dict[str, Any]]] = {}
        for line in stream.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            content = (event.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    pending[block["id"]] = (block["name"].split("__")[-1], block.get("input") or {})
                elif block.get("type") == "tool_result" and block.get("tool_use_id") in pending:
                    name, args = pending.pop(block["tool_use_id"])
                    out.append((name, args, _tool_text(block.get("content"))))
    return out


def game_lines(run_dir: Path) -> tuple[list[str], list[str]]:
    """Markdown lines for one game and its half-year grade sequence."""
    lines: list[str] = []
    grades: list[str] = []
    obs: dict[str, Any] = {}
    last_events = ""
    for name, args, reply in calls(run_dir):
        if name == "observe":
            try:
                obs = json.loads(reply)
            except json.JSONDecodeError:
                continue
            events = obs.get("events") or ""
            if events and events != last_events:
                grades += GRADE.findall(events)
                lines.append(f"  > {_short(events, 700)}")
            last_events = events
        elif name == "take_action" and obs:
            state = obs.get("current_state") or {}
            month = (state.get("time") or {}).get("current_month", "?")
            status = state.get("status") or {}
            stats = "/".join(str(status.get(k, "?")) for k in STAT_KEYS)
            event = obs.get("current_event") or {}
            choices = {c.get("choice"): c.get("action", "") for c in obs.get("choices") or []}
            picked = args.get("choice")
            line = f"- M{month} [{stats}] {_short(event.get('title', ''), 70)} → [{picked}] {_short(choices.get(picked, '?'), 110)}"
            if event.get("title") != "Quarterly energy allocation" and len(choices) > 1:
                declined = "; ".join(f"[{k}] {_short(v, 70)}" for k, v in choices.items() if k != picked)
                line += f" (declined: {declined})"
            if args.get("notes"):
                line += f" — notes: {_short(args['notes'], 200)}"
            try:
                result = json.loads(reply)
            except json.JSONDecodeError:
                result = {}
            if result.get("success") is False:
                line += f" — REJECTED: {_short(result.get('error'), 120)}"
            lines.append(line)
    return lines, grades


def digest(reg: Registry, model: str, out_dir: Path) -> list[dict[str, Any]]:
    """Write one digest per finished game of `model` plus an index; return the index rows."""
    rows = reg.db.execute(
        "SELECT j.job_id, j.run_dir, p.name AS policy, a.config, e.outcome, e.survival_months, e.score FROM evaluations e "
        "JOIN jobs j USING(job_id) JOIN actors a USING(actor_id) JOIN policies p USING(policy_id) "
        "WHERE a.kind='claude-cli' AND json_extract(a.config,'$.model')=? AND e.outcome IN ('completed','eliminated') "
        "ORDER BY e.score DESC", (model,)).fetchall()
    out_dir.mkdir(parents=True, exist_ok=True)
    index = []
    for r in rows:
        run_dir = Path(r["run_dir"]) if r["run_dir"] else None
        if run_dir is None or not run_dir.exists():  # imported games (other machines or origins) have no local run folder
            continue
        cfg = json.loads(r["config"])
        actor = cfg["model"] + (f"~{cfg['autocompact']}" if cfg.get("autocompact") else "")
        result = json.loads((run_dir / "result.json").read_text())
        dims = {d["name"]: d["normalized_score"] for d in (result.get("ending_score") or {}).get("dimensions", [])}
        lines, grades = game_lines(run_dir)
        head = [f"# {r['job_id']}", "",
                f"Policy `{r['policy']}`, actor `{actor}`: **{r['outcome']}**, {r['survival_months']} months, Q {r['score']:.2f}.",
                f"Ending dimensions (0–100): {json.dumps(dims)}. Failure: {(result.get('failure_reason') or '—').rstrip('.')}.",
                f"Half-year grades: {' '.join(grades) or '—'}.", "",
                f"State before each decision: [{'/'.join(STAT_KEYS)}]. `>` lines are game feedback, verbatim but shortened.", ""]
        (out_dir / f"{r['job_id']}.md").write_text("\n".join(head + lines) + "\n", encoding="utf-8")
        index.append({"job_id": r["job_id"], "policy": r["policy"], "actor": actor, "outcome": r["outcome"],
                      "months": r["survival_months"], "Q": round(r["score"], 2), "grades": " ".join(grades), **dims})
    table = ["| game | policy | actor | outcome | months | Q | half-year grades |", "|---|---|---|---|---:|---:|---|"]
    table += [f"| [{i['job_id']}]({i['job_id']}.md) | {i['policy']} | {i['actor']} | {i['outcome']} | {i['months']} | {i['Q']} | {i['grades']} |"
              for i in index]
    (out_dir / "index.md").write_text(f"# {model} game digests\n\n" + "\n".join(table) + "\n", encoding="utf-8")
    return index
