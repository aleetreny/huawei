"""Load black-box batches and parse the official log messages into structured records."""

from __future__ import annotations

import glob
import gzip
import json
import os
import re
from pathlib import Path
from typing import Any, Iterator

DATA = Path(os.environ.get("BB_DATA", Path.home() / "careerlab-data" / "ingenieria-inversa"))
STATS = ("health", "dignity", "skill", "network", "level", "duration_in_level", "output", "wealth", "energy")
IDX = {k: i for i, k in enumerate(STATS)}
DELTA_RE = re.compile(r"\b(Health|Dignity|Skill|Network|Output|Wealth|HiddenRisk)\s([+-]\d+(?:\.\d+)?)")


class Batch:
    def __init__(self, *names: str):
        self.dirs = [DATA / n for n in names]
        self.texts: dict[str, str] = {}
        self.nodes: dict[str, dict[str, Any]] = {}
        for d in self.dirs:
            for p in glob.glob(str(d / "texts-*.jsonl")):
                with open(p, encoding="utf-8") as f:
                    for line in f:
                        try:
                            r = json.loads(line)
                        except ValueError:
                            continue
                        self.texts[r["id"]] = r["t"]
            for p in glob.glob(str(d / "nodes-*.jsonl")):
                with open(p, encoding="utf-8") as f:
                    for line in f:
                        try:
                            r = json.loads(line)
                        except ValueError:
                            continue
                        self.nodes[r["id"]] = r

    def games(self) -> Iterator[dict[str, Any]]:
        from gzrobust import read_lines  # tolerates truncated gzip members (batches stopped mid-write)
        for d in self.dirs:
            for p in sorted(glob.glob(str(d / "games-*.jsonl.gz"))):
                for line in read_lines(p):
                    try:
                        yield json.loads(line)
                    except ValueError:
                        continue

    def log_entries(self, g: dict[str, Any]) -> list[tuple[str, str]]:
        return [(code, self.texts.get(tid, "")) for code, tid in g.get("logs", [])]


def deltas(text: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for k, v in DELTA_RE.findall(text):
        out[k.lower()] = out.get(k.lower(), 0) + float(v)
    return out


def parse_choice_entry(msg: str) -> dict[str, Any] | None:
    """'Month m | Title\\n<excerpt>\\nChose #k: <text>\\n<deltas>\\n...' -> structured."""
    m = re.match(r"Month (\d+) \| (.*?)\n(.*?)\nChose #(\d+): (.*?)\n(.*)", msg, re.S)
    if not m:
        return None
    month, title, excerpt, k, chosen, rest = m.groups()
    lines = rest.split("\n")
    delta_line = lines[0] if lines else ""
    cost = re.search(r"Energy cost: (\d+)", rest)
    return {"month": int(month), "title": title, "excerpt": excerpt, "k": int(k), "chosen": chosen,
            "d": deltas(delta_line), "delta_line": delta_line, "cost": int(cost.group(1)) if cost else None}


def grade_of(msg: str) -> str | None:
    m = re.search(r"Half-year performance bonus \(([SABCD])\)", msg)
    return m.group(1) if m else None


def promotion_of(msg: str) -> tuple[int, int] | None:
    m = re.search(r"moved from L(\d+) to L(\d+)", msg)
    return (int(m.group(1)), int(m.group(2))) if m else None
