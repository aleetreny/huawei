"""Obedience report for the DeepSeek bank arms: per-rule score (transmision/score.py), fingerprint on the
general block, how often the agent opens each Skill file by month before the review, and self-agreement.

    uv run python scripts/deepseek/obedience.py --arms ds-control,ds-t13-final --haiku hk-control,hk-t13-final,hk-t10-countdown
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts" / "transmision"))
from ds import DATA  # noqa: E402

os.environ["TRANSMISION_DATA"] = str(DATA)
from score import arm_results, load_items  # noqa: E402

ITEMS = DATA / "items.jsonl"


def sh(*args: str) -> None:
    out = subprocess.run([sys.executable, *args], capture_output=True, text=True, env=os.environ)
    print(out.stdout.strip())
    if out.returncode:
        print(out.stderr[-2000:])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="ds-control,ds-t13-final")
    ap.add_argument("--haiku", default="hk-control,hk-t13-final,hk-t10-countdown")
    ap.add_argument("--ids", default=str(DATA / "ids-ds1.txt"))
    a = ap.parse_args()
    arms = a.arms.split(",")
    ids = set(Path(a.ids).read_text().split())
    items = load_items(ITEMS)
    print("## Per rule, DeepSeek arms on the items they share\n")
    sh(str(REPO / "scripts/transmision/score.py"), "--items", str(ITEMS), "--arms", ",".join(arms), "--common")
    for hk in a.haiku.split(","):
        print(f"\n## {hk} against ds-control on the items both answered\n")
        sh(str(REPO / "scripts/transmision/score.py"), "--items", str(ITEMS), "--arms", f"ds-control,{hk}", "--common")
    g1 = DATA / "items-g1.jsonl"
    g1_ids = set((REPO / "lab/data/transmision/ids-G1.txt").read_text().split())
    with g1.open("w") as f:
        for line in ITEMS.open():
            if json.loads(line)["id"] in g1_ids:
                f.write(line)
    print("\n## Fingerprint on the general block (G1), months 1-44\n")
    sh(str(REPO / "scripts/transmision/fingerprint.py"), "--items", str(g1), "--arms", ",".join(arms + a.haiku.split(",")))
    print("\n## Skill files opened, by the countdown N of t13-final (N = 1: month before a review)\n")
    for arm in arms:
        res = arm_results(arm)
        rows = collections.defaultdict(lambda: [0, 0, 0])
        for iid, r in res.items():
            if iid not in ids or iid not in items:
                continue
            m = items[iid]["month"]
            to_review = 6 - m % 6  # the manual's countdown: N = 1 in the month before a review month
            paths = {e["path"] for e in r.get("skill_reads") or []}
            row = rows[to_review]
            row[0] += 1
            row[1] += int("SKILL.md" in paths)
            row[2] += int(any(p != "SKILL.md" for p in paths))
        print(f"{arm}: " + "; ".join(f"N={k}: n={v[0]}, SKILL.md {100 * v[1] / v[0]:.0f} %, reference {100 * v[2] / v[0]:.0f} %"
                                    for k, v in sorted(rows.items())))


if __name__ == "__main__":
    main()
