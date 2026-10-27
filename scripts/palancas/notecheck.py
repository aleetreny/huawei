"""Check the status line Haiku writes in every note of a bank arm (palanca 1).

For every `take_action` of every item (the month's earlier steps and the target), compare the note with
the `observe` the model was shown at that step: is the line there, is `Review in N` right, are the `Now`
values right, what does `Risky this month` say, how long is the note.

    python3 -I scripts/palancas/notecheck.py --items ~/careerlab-data/palancas/bench/items.jsonl --arms g1-t16b-expect,g1-t17b-status
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
from pathlib import Path

DATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "palancas" / "bench"))
LINE = re.compile(r"Review in (\d+)\s*\|\s*Now S(-?\d+) N(-?\d+) O(-?\d+)")
RISKY = re.compile(r"Risky this month:\s*(\d+)")


def review_in(month: int) -> int:
    return 6 if month % 6 == 0 else 6 - month % 6


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--arms", required=True)
    a = ap.parse_args()
    items = {}
    for line in open(a.items):
        it = json.loads(line)
        items[it["id"]] = it
    print("| Brazo | Notas | Con la línea | `Review in N` bien | `Now` bien | `Risky this month` > 0 | Caracteres por nota (mediana) | Lee el registro por situación |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for arm in a.arms.split(","):
        d = DATA / "runs" / arm
        n = has = rev_ok = now_ok = risky = logs = items_n = 0
        lens: list[int] = []
        for wd in (d / "work").glob("*"):
            rec = wd / "record.jsonl"
            iid = None
            res = d / f"{wd.name}.json"
            if res.exists():
                iid = json.loads(res.read_text())["id"]
            if iid not in items or not rec.exists():
                continue
            it = items[iid]
            sv = it["serve"]
            obs = sv["observes"][sv["month_from"] - sv["long_from"]:]
            items_n += 1
            for e in map(json.loads, rec.read_text().splitlines()):
                if e.get("tool") == "check_latest_logs":
                    logs += 1
                if e.get("tool") != "take_action" or e.get("invalid"):
                    continue
                o = obs[min(e["pos"], len(obs) - 1)]["current_state"]
                note = e.get("notes") or ""
                n += 1
                lens.append(len(note))
                m = LINE.search(note)
                if not m:
                    continue
                has += 1
                rev_ok += int(int(m.group(1)) == review_in(o["time"]["current_month"]))
                s = o["status"]
                now_ok += int((int(m.group(2)), int(m.group(3)), int(m.group(4))) == (s["skill"], s["network"], s["output"]))
                r = RISKY.search(note)
                risky += int(bool(r) and int(r.group(1)) > 0)
        if not n:
            continue
        lens.sort()
        print(f"| {arm} | {n} | {100 * has / n:.0f} % | {100 * rev_ok / max(1, has):.0f} % | {100 * now_ok / max(1, has):.0f} % | "
              f"{100 * risky / max(1, has):.0f} % | {lens[len(lens) // 2]} | {logs / max(1, items_n):.2f} |")


if __name__ == "__main__":
    main()
