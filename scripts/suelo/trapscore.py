"""Score the trap bank (scripts/suelo/trapbank.py) for one or more arms: did the agent do what the floor
rules ask, by trap type? Research only.

Per trap type the measures are about the rule, not the replica's value of the option (for the L1 rescue
the replica without B30 cannot value it):
  l1_rescue / e   share of choices that add hidden risk (dr > 0); share that pick the lowest dr; share that
                  lower Network or Output when another option does not
  l1_rescue / q,m share of Defuse legacy risk (energy) and Lay low (main) when the HR remark is not friendly
  after_blow      share of choices that add risk; share picking the lowest dr
  all_risky       share picking the lowest dr; mean dr of the choice
  l1_prep         share lowering Network or Output when another option does not
Also: skill reads, log calls and note length per arm.

    SUELO_DATA=~/careerlab-data/suelo python3 scripts/suelo/trapscore.py --arms hk-c5,hk-suelo-v1
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
from pathlib import Path

DATA = Path(os.environ.get("SUELO_DATA", Path.home() / "careerlab-data" / "suelo"))


def load_items() -> dict[str, dict]:
    return {json.loads(x)["id"]: json.loads(x) for x in (DATA / "items.jsonl").open()}


def load_arm(name: str) -> dict[str, dict]:
    out = {}
    for f in (DATA / "runs" / name).glob("*_*.json"):
        r = json.loads(f.read_text())
        if str(r.get("done")) == "True" and r.get("choice") is not None:
            out[r["id"]] = r
    return out


def boot_diff(a: list[float], b: list[float], n: int = 4000) -> tuple[float, float]:
    rng = random.Random(1)
    d = [y - x for x, y in zip(a, b)]
    if not d:
        return (0.0, 0.0)
    ms = []
    for _ in range(n):
        s = [d[rng.randrange(len(d))] for _ in d]
        ms.append(sum(s) / len(s))
    ms.sort()
    return ms[int(0.025 * n)], ms[int(0.975 * n)]


def measures(it: dict, choice: int) -> dict[str, float]:
    fx = {int(k): v for k, v in it["fx"].items()}
    if choice not in fx:
        return {}
    drs = {k: v["dr"] for k, v in fx.items()}
    ch = fx[choice]
    out: dict[str, float] = {}
    ph = it["phase"]
    if ph == "e":
        out["adds risk"] = float(ch["dr"] > 0)
        out["lowest risk"] = float(ch["dr"] == min(drs.values()))
        out["dr of choice"] = float(ch["dr"])
        lose = lambda f: f["d"].get("network", 0) < 0 or f["d"].get("output", 0) < 0
        if any(not lose(f) for f in fx.values()):
            out["loses N/O avoidably"] = float(lose(ch))
    else:
        name = ch.get("name") or ""
        if ph == "q":
            out["Defuse"] = float(name.startswith("Defuse"))
            out["Output/Network energy"] = float(name.startswith("Prepare report") or name.startswith("Network maintenance"))
        else:
            out["Lay low"] = float(name.startswith("Lay low"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", required=True)
    a = ap.parse_args()
    items = load_items()
    arms = {n: load_arm(n) for n in a.arms.split(",")}
    common = set(items)
    for r in arms.values():
        common &= set(r)
    print(f"{len(common)} items answered by every arm")
    rows: dict[tuple[str, str, str], dict[str, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    meta: dict[str, dict[str, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for iid in sorted(common):
        it = items[iid]
        for arm, res in arms.items():
            r = res[iid]
            m = measures(it, int(r["choice"]))
            for t in it["tags"]:
                key = (t, it["phase"], arm)
                if it["phase"] in ("q", "m") and it["state"]["risk"] == 0 and t == "l1_rescue":
                    key = (t, it["phase"] + " (HR friendly)", arm)
                for k, v in m.items():
                    rows[key][k].append(v)
            meta[arm]["skill reads"].append(len(eval(str(r.get("skill_reads") or "[]"))))
            meta[arm]["log calls"].append(float(r.get("log_calls") or 0))
            meta[arm]["note chars"].append(len(str(r.get("notes") or "")))
    types = sorted({(t, p) for (t, p, _) in rows})
    for t, p in types:
        print(f"\n## {t} / {p}")
        keys = sorted({k for arm in arms for k in rows[(t, p, arm)]})
        hdr = "| measure | " + " | ".join(arms) + " |"
        print(hdr)
        print("|---|" + "---:|" * len(arms))
        for k in keys:
            cells = []
            for arm in arms:
                v = rows[(t, p, arm)].get(k, [])
                cells.append(f"{sum(v) / len(v):.0%} (n={len(v)})" if v and k != "dr of choice" else (f"{sum(v) / len(v):+.2f}" if v else "—"))
            print(f"| {k} | " + " | ".join(cells) + " |")
    print("\n## per arm")
    for arm, m in meta.items():
        print(arm, {k: round(sum(v) / len(v), 2) for k, v in m.items()})
    if len(arms) == 2:
        a1, a2 = list(arms)
        same = sum(int(arms[a1][i]["choice"]) == int(arms[a2][i]["choice"]) for i in common)
        print(f"\nsame choice {a1} vs {a2}: {same}/{len(common)} = {same / max(1, len(common)):.0%}")


if __name__ == "__main__":
    main()
