"""Summarise a T20 game batch: mean score, completion, failures and level per arm, with standard errors.

    uv run python scripts/transmision/games.py --batch g1-full [--md]
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from careerlab.config import load_settings

BATCHES = Path(__file__).resolve().parents[2] / "lab" / "reports" / "transmision" / "batches"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    a = ap.parse_args()
    meta = json.loads((BATCHES / f"{a.batch}.json").read_text())
    reg = load_settings().registry()
    print(f"| Manual | Terminadas / jugadas | Nota Q media ± SE | Nota de las terminadas | Nivel final medio | Derrotas | Tokens por mes |")
    print("|---|---:|---:|---:|---:|---|---:|")
    rows = {}
    for arm, jobs in meta["arms"].items():
        evs = []
        for j in jobs:
            e = reg.db.execute("SELECT * FROM evaluations WHERE job_id=?", (j,)).fetchone()
            if e is not None and e["outcome"] in ("completed", "eliminated"):
                evs.append(e)
        if not evs:
            continue
        q = [e["score"] for e in evs if e["score"] is not None]
        m = sum(q) / len(q)
        se = math.sqrt(sum((x - m) ** 2 for x in q) / max(1, len(q) - 1) / len(q)) if len(q) > 1 else float("nan")
        done = [e for e in evs if e["completed"]]
        qd = [e["score"] for e in done]
        lv, fails, tpm = [], Counter(), []
        for e in evs:
            dims = json.loads(e["dims"] or "{}")
            if "level" in dims:
                lv.append(dims["level"] / 10)
            tok = json.loads(e["tokens"] or "{}") if isinstance(e["tokens"], str) else {}
            tot = sum(v for v in (tok.get("tokens") or {}).values()) if tok else 0
            if tot and e["survival_months"]:
                tpm.append(tot / e["survival_months"])
        # failure reasons from the run's result
        fails = Counter()
        for e in evs:
            if e["completed"]:
                continue
            try:
                res = json.loads((Path(e["trajectory_path"]).parent / "result.json").read_text())
                fails[(res.get("failure_reason") or res.get("outcome") or "?").split(" —")[0][:30]] += 1
            except Exception:  # noqa: BLE001
                fails["?"] += 1
        rows[arm] = (q, m, se)
        print(f"| {arm} | {len(done)}/{len(evs)} | {m:.1f} ± {se:.1f} | {sum(qd)/max(1,len(qd)):.1f} | "
              f"{sum(lv)/max(1,len(lv)):.2f} | {', '.join(f'{k} {v}' for k, v in fails.most_common())} | "
              f"{(sum(tpm)/len(tpm)/1000 if tpm else 0):.0f}k |")
    if len(rows) == 2:
        (a1, (q1, m1, s1)), (a2, (q2, m2, s2)) = rows.items()
        d = m2 - m1
        print(f"\nDiferencia {a2} − {a1}: {d:+.1f} ± {math.sqrt(s1**2 + s2**2):.1f} puntos")


if __name__ == "__main__":
    main()
