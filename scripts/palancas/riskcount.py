"""Does the model count its own risky story choices right? (palanca 5, `Risky this month`.)

For every note of an arm, the true count is the number of the month's earlier story choices (by the model,
in the same item) whose hidden risk is positive in the catalog. Story steps are matched to catalog nodes by
title and choice texts from the bot batches the bank items came from.

    python3 -I scripts/palancas/riskcount.py --items ~/careerlab-data/palancas/bench/items.jsonl --arms g1-t17b-status,g1-t18-status
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ingenieria-inversa"))
os.environ.setdefault("BB_DATA", str(HERE.parents[1] / "lab" / "data" / "ingenieria-inversa"))

import replica as R  # noqa: E402
from bbdata import Batch  # noqa: E402

DATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "palancas" / "bench"))
RISKY = re.compile(r"Risky this month:\s*(\d+)")


def key(title: str, choices: list) -> tuple:
    return (title, tuple((c.get("action") or c.get("text") or "") if isinstance(c, dict) else str(c) for c in choices))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--arms", required=True)
    a = ap.parse_args()
    items = {json.loads(line)["id"]: json.loads(line) for line in open(a.items)}
    cat = R.Catalog(json.loads((Path(os.environ["BB_DATA"]) / "catalog_v2.json").read_text()))
    nodes: dict[tuple, str] = {}
    for b in sorted({it["batch"] for it in items.values()}):
        for nid, n in Batch(b).nodes.items():
            nodes[key(n.get("title") or "", n.get("choices") or [])] = nid
    print("| Brazo | Notas con contador | Cuenta real > 0 | Haiku dice > 0 | Acierta el número | Con riesgo real, lo ve | Sin riesgo real, falsa alarma | Historias sin nodo |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for arm in a.arms.split(","):
        d = DATA / "runs" / arm
        n = real_pos = said_pos = exact = seen = false = unk = 0
        for wd in (d / "work").glob("*"):
            res = d / f"{wd.name}.json"
            rec = wd / "record.jsonl"
            if not res.exists() or not rec.exists():
                continue
            it = items.get(json.loads(res.read_text())["id"])
            if it is None:
                continue
            sv = it["serve"]
            obs = sv["observes"][sv["month_from"] - sv["long_from"]:]
            true = 0
            for e in map(json.loads, rec.read_text().splitlines()):
                if e.get("tool") != "take_action" or e.get("invalid"):
                    continue
                o = obs[min(e["pos"], len(obs) - 1)]
                m = RISKY.search(e.get("notes") or "")
                if m and o["current_event"].get("title") not in ("Quarterly energy allocation", "Quarterly main action"):
                    said = int(m.group(1))
                    n += 1
                    real_pos += int(true > 0)
                    said_pos += int(said > 0)
                    exact += int(said == true)
                    seen += int(true > 0 and said > 0)
                    false += int(true == 0 and said > 0)
                nid = nodes.get(key(o["current_event"].get("title") or "", o.get("choices") or []))
                if o["current_event"].get("title") in ("Quarterly energy allocation", "Quarterly main action"):
                    continue
                if nid is None:
                    unk += 1
                    continue
                true += int(cat.answer_risk(nid, int(e["choice"])) > 0)
        if n:
            print(f"| {arm} | {n} | {100 * real_pos / n:.0f} % | {100 * said_pos / n:.0f} % | {100 * exact / n:.0f} % | "
                  f"{100 * seen / max(1, real_pos):.0f} % (n={real_pos}) | {100 * false / max(1, n - real_pos):.0f} % | {unk} |")


if __name__ == "__main__":
    main()
