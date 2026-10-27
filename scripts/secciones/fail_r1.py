"""Why the first review did not promote: stat short at review, and whether it had been reached earlier (lost) or never.

    uv run python scripts/secciones/fail_r1.py [--purpose screen] [--cut 6]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from careerlab.truncate import observed_states
from periods import FLOORS, at_floor, rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purpose")
    ap.add_argument("--cut")
    ap.add_argument("--batch")
    a = ap.parse_args()
    by = defaultdict(Counter)
    for r in rows(a.purpose, a.cut, a.batch):
        rev = next((x for x in ((r["periods"] or {}).get("reviews") or []) if x["review"] == 1), None)
        if not rev:
            continue
        c = by[r["policy"]]
        c["n"] += 1
        if rev["promoted"]:
            c["promoted"] += 1
            continue
        if at_floor(rev):
            c["floor_not_promoted"] += 1
            dig = (rev["after"] or {}).get("dignity")
            c[f"  floor_not_promoted_dignity_{'low' if (dig or 10) <= 4 else 'ok'}"] += 1
            c[f"  floor_not_promoted_hr{rev.get('hr_tier_before')}"] += 1
            continue
        run_dir = Path(r["usage"] and "" or "")
        states = []
        job_dir = None
        for p in Path.home().glob(f"careerlab-data/*/runs/{r['job']}"):
            job_dir = p
        if job_dir:
            lines = []
            for s in sorted(job_dir.glob("stream-*.jsonl")):
                lines += s.read_text(errors="replace").splitlines()
            states = [s for s in observed_states(lines) if s["month"] < 6]
        snap = rev["after"]
        for k, f in zip(("skill", "network", "output"), FLOORS[1]):
            if (snap.get(k) or 0) < f:
                reached = any((s.get(k) or 0) >= f for s in states)
                c[f"short_{k}_{'lost' if reached else 'never'}"] += 1
                if reached:
                    last_ok = max(s["month"] for s in states if (s.get(k) or 0) >= f)
                    c[f"  lost_after_month_{last_ok}"] += 1
    for pol, c in sorted(by.items()):
        print(pol, json.dumps(dict(sorted(c.items()))))


if __name__ == "__main__":
    main()
