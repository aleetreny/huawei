"""Cut a Claude episode at a given month and record the state at every half-year review.

A short game ("cut at month M") stops the worker as soon as its own stream shows a
game state in month M or later. The result is ``truncated``: it carries no score and
never counts as completed or eliminated. Everything here reads only what the official
tools returned to the player (its stream) or to our own verifier (observe and
check_latest_logs on our own run); nothing reads the simulator's files.

Review snapshots: the half-year review is applied at the start of its month, before
that month's events, so the first state observed in a review month is the state the
review left (level after any promotion), and the last state observed in the month
before is the closest view of what the review judged.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

REVIEW_EVERY = 6
SNAP_KEYS = ("level", "skill", "network", "output", "health", "dignity", "wealth")
HR_TIERS = (  # calm -> angry, the five tones of the monthly HR remark
    ("doing all right", 0),
    ("isn't serious yet", 1),
    ("piled up", 2),
    ("on your own now", 3),
    ("about to go off", 4),
)
_MONTH = re.compile(r'"current_month"\s*:\s*(\d+)')
_GRADE = re.compile(r"Half-year performance bonus \(([SABCD])\)")
_LOG_MONTH = re.compile(r"^Month (\d+) \|")


def tool_result_texts(lines: Iterable[str]) -> Iterable[str]:
    """Text of every tool result in a stream-json transcript."""
    for line in lines:
        if '"tool_result"' not in line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        content = msg.get("message", {}).get("content", [])
        for block in content if isinstance(content, list) else []:
            if block.get("type") != "tool_result":
                continue
            text = block.get("content")
            if isinstance(text, list):
                text = "".join(b.get("text", "") for b in text if isinstance(b, dict))
            if isinstance(text, str):
                yield text


def max_month(lines: Iterable[str]) -> int:
    best = 0
    for text in tool_result_texts(lines):
        for found in _MONTH.finditer(text):
            best = max(best, int(found.group(1)))
    return best


class StreamWatcher:
    """Incremental reader of a growing stream file: reports the highest game month seen."""

    def __init__(self, path: Path):
        self.path = path
        self.offset = 0
        self.partial = ""
        self.month = 0

    def poll(self) -> int:
        if not self.path.exists():
            return self.month
        with self.path.open("r", encoding="utf-8", errors="replace") as fh:
            fh.seek(self.offset)
            chunk = fh.read()
            self.offset = fh.tell()
        if not chunk:
            return self.month
        data = self.partial + chunk
        lines = data.split("\n")
        self.partial = lines.pop()  # last piece may be an unfinished line
        self.month = max(self.month, max_month(lines))
        return self.month


def observed_states(lines: Iterable[str]) -> list[dict[str, Any]]:
    """Every game state the player observed, in order: {month, level, skill, ...}."""
    out = []
    for text in tool_result_texts(lines):
        if '"current_state"' not in text:
            continue
        try:
            obs = json.loads(text)
        except ValueError:
            continue
        state = obs.get("current_state") if isinstance(obs, dict) else None
        if not isinstance(state, dict) or "time" not in state:
            continue
        status = state.get("status") or {}
        level = status.get("level")
        row = {"month": int(state["time"].get("current_month") or 0)}
        for key in SNAP_KEYS:
            value = status.get(key)
            row[key] = int(str(value)[1:]) if key == "level" and value else value
        out.append(row)
    return out


def hr_tier(message: str) -> int | None:
    for marker, tier in HR_TIERS:
        if marker in message:
            return tier
    return None


def log_facts(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Grades, promotions, blow-ups and the HR tone per month, from check_latest_logs entries (oldest first)."""
    grades: list[str] = []
    blowups: list[int] = []
    hr: dict[int, int] = {}
    month = 1
    for entry in entries:
        msg = str(entry.get("message") or "")
        found = _LOG_MONTH.match(msg)
        if found:
            month = int(found.group(1))
        kind = entry.get("entry_type")
        if kind == "salary":
            grade = _GRADE.search(msg)
            if grade:
                grades.append(grade.group(1))
            tier = hr_tier(msg)
            if tier is not None:
                hr[month] = max(hr.get(month, 0), tier)
        elif kind == "warning" and "landmines" in msg:
            blowups.append(month)
    return {"grades": grades, "blowup_months": blowups, "hr_by_month": hr}


def review_snapshots(states: list[dict[str, Any]], facts: dict[str, Any], last_month: int) -> list[dict[str, Any]]:
    """One row per review reached: state before (last view in the previous month) and after (first view in the review month)."""
    rows = []
    grades = facts.get("grades") or []
    hr = facts.get("hr_by_month") or {}
    for k, review in enumerate(range(REVIEW_EVERY, last_month + 1, REVIEW_EVERY)):
        before = [s for s in states if s["month"] < review]
        after = [s for s in states if s["month"] == review]
        if not after:
            break
        pre, post = (before[-1] if before else None), after[0]
        rows.append({
            "review": k + 1,
            "month": review,
            "before": pre,
            "after": post,
            "promoted": bool(pre and post.get("level") and pre.get("level") and post["level"] > pre["level"]),
            "grade": grades[k] if k < len(grades) else None,
            "hr_tier_before": hr.get(review - 1),
        })
    return rows


def summarize(stream_paths: list[Path], log_entries: list[dict[str, Any]], last_month: int) -> dict[str, Any]:
    lines: list[str] = []
    for path in stream_paths:
        if path.exists():
            lines.extend(path.read_text(encoding="utf-8", errors="replace").splitlines())
    states = observed_states(lines)
    facts = log_facts(log_entries)
    return {
        "reviews": review_snapshots(states, facts, last_month),
        "final_state": states[-1] if states else None,
        "blowup_months": facts["blowup_months"],
        "hr_by_month": {str(k): v for k, v in sorted(facts["hr_by_month"].items())},
        "grades": facts["grades"],
    }
