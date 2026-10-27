"""Score answer choices on the decision benchmark against the measured dev effects.

Each variant folder holds choices.json ({question id: chosen k}); the key (kept outside the
folders the answering agents can read) maps every question to its answers' measured effects.
The context given to every answerer: mid-career, all growth inputs below what the level needs,
Health and Dignity comfortable, calm HR remark. The value used to name a 'best' answer reflects
that context: growth inputs count fully, Health/Dignity/Wealth partly, three-month blow-up excess
is heavily penalised.

    python3 bench_score.py <bench dir> <key.json> A B C
"""

from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path


def value(e: dict) -> float:
    m = e["mean"]
    v = m.get("skill", 0) + m.get("network", 0) + m.get("output", 0)
    v += 0.4 * m.get("health", 0) + 0.4 * m.get("dignity", 0) + 0.3 * m.get("wealth", 0)
    return v - 25 * (e.get("blow3", 0) or 0)


def main() -> None:
    root = Path(sys.argv[1])
    key = json.loads(Path(sys.argv[2]).expanduser().read_text())
    rows = []
    # reference rows: uniform random choice and the best answer by measured effects
    ref = {"random": [], "best": []}
    for qid, q in key.items():
        effs = q["effects"]
        vals = {k: value(e) for k, e in effs.items()}
        ref["random"].append({k2: st.mean(effs[k].get("mean", {}).get(k2, 0) for k in effs) for k2 in ("skill", "network", "output", "health", "dignity")}
                             | {"blow3": st.mean(effs[k].get("blow3", 0) for k in effs), "value": st.mean(vals.values()),
                                "risky": st.mean(1.0 if effs[k].get("blow3", 0) >= 0.10 else 0.0 for k in effs), "best": 1 / len(effs)})
        kb = max(vals, key=vals.get)
        e = effs[kb]
        ref["best"].append({k2: e["mean"].get(k2, 0) for k2 in ("skill", "network", "output", "health", "dignity")}
                           | {"blow3": e.get("blow3", 0), "value": vals[kb], "risky": 1.0 if e.get("blow3", 0) >= 0.10 else 0.0, "best": 1.0})
    for variant in sys.argv[3:]:
        path = root / variant / "choices.json"
        if not path.exists():
            print(f"{variant}: no choices.json yet")
            continue
        choices = json.loads(path.read_text())
        out = []
        for qid, q in key.items():
            k = str(choices.get(qid, ""))
            effs = q["effects"]
            if k not in effs:
                continue
            vals = {kk: value(e) for kk, e in effs.items()}
            e = effs[k]
            out.append({k2: e["mean"].get(k2, 0) for k2 in ("skill", "network", "output", "health", "dignity")}
                       | {"blow3": e.get("blow3", 0), "value": vals[k], "risky": 1.0 if e.get("blow3", 0) >= 0.10 else 0.0,
                          "best": 1.0 if vals[k] == max(vals.values()) else 0.0})
        ref[variant] = out
    print(f"{'variant':8s} {'n':>4s} {'value':>6s} {'best%':>6s} {'risky%':>7s} {'blow3':>7s} {'skill':>6s} {'netw':>6s} {'outp':>6s} {'health':>7s} {'dign':>6s}")
    for name, out in ref.items():
        if not out:
            continue
        agg = {k: st.mean(r[k] for r in out) for k in out[0]}
        print(f"{name:8s} {len(out):4d} {agg['value']:6.2f} {agg['best']:6.0%} {agg['risky']:7.0%} {agg['blow3']:+7.3f} "
              f"{agg['skill']:+6.2f} {agg['network']:+6.2f} {agg['output']:+6.2f} {agg['health']:+7.2f} {agg['dignity']:+6.2f}")


if __name__ == "__main__":
    main()
