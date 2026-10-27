"""Score obedience-bank arms (T20) against the replica's right answers.

    uv run python scripts/transmision/score.py --items items.jsonl --arms control,v1,... [--split dev|holdout|all] [--md]

Per rule (tag), for the items an arm answered:
- `ok`: the chosen option is a right answer: within `tol` of the best rollout value for event decisions
  (and closing), or in the rule's action set for quarterly decisions (Skill in L4, risk reduction);
- `regret`: best rollout value minus the chosen option's value (final-score points, replica);
- a rule-specific failure rate: pre_review loses a needed point; trigger reaches the explosion;
  early_ruin spends money while wealth is low; skill_l4 / hr_risk pick a non-rule action.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ingenieria-inversa"))
import replica as R  # noqa: E402

DATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "transmision"))
RULES = ("pre_review", "skill_l4", "hr_risk", "trigger", "early_ruin", "closing")
TOL_E, TOL_Q = 0.5, 0.15


def rule_of(it: dict[str, Any]) -> str | None:
    """Each item is scored under one rule (the most specific of its tags)."""
    tg = it["tags"]
    for r in ("trigger", "early_ruin", "pre_review", "closing", "hr_risk", "skill_l4"):
        if r in tg:
            if r == "skill_l4" and it["state"]["risk"] >= 2:
                continue
            return r
    return None


def right_set(it: dict[str, Any], rule: str) -> set[int]:
    q = {int(k): v for k, v in it["q"].items()}
    names = {int(k): f["name"] for k, f in it["fx"].items()}
    st = it["state"]
    if rule == "skill_l4":
        if it["phase"] == "q":
            ok = {k for k, n in names.items() if n == "Skill learning"}
            if st["health"] <= 3 or not ok:   # no room for the Health cost: recovery first
                ok = {k for k, n in names.items() if n == "Health recovery"}
            return ok
        return {k for k, n in names.items() if n == "Apply for rotation"}
    if rule == "hr_risk":
        want = "Defuse legacy risk" if it["phase"] == "q" else "Lay low and reduce risk"
        ok = {k for k, n in names.items() if n == want}
        if it["phase"] == "q" and (st["energy"] < 2 or not ok):
            ok = {k for k, n in names.items() if n in ("Health recovery", "Mental recovery", "Reserve energy (no action)")}
        return ok
    best = max(q.values())
    tol = TOL_E if it["phase"] == "e" else TOL_Q
    return {k for k, v in q.items() if v >= best - tol}


def decisive(it: dict[str, Any], rule: str) -> bool:
    if rule in ("skill_l4", "hr_risk"):
        return True
    q = list(it["q"].values())
    return (max(q) - min(q)) >= (2.0 if it["phase"] == "e" else 0.4) and len(right_set(it, rule)) < len(q)


def rule_fail(it: dict[str, Any], rule: str, k: int) -> bool:
    f = it["fx"][str(k)]
    st = it["state"]
    if rule == "pre_review":
        thr = R.THRESH[st["level"]]
        return any(f["d"].get(s, 0) < 0 and st[s] <= thr[i] for i, s in enumerate(R.GROWTH))
    if rule == "trigger":
        return st["risk"] + f["dr"] >= R.BLOW_AT
    if rule == "early_ruin":
        return f["d"].get("wealth", 0) < 0
    return k not in right_set(it, rule)


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    out = {}
    for line in path.open():
        it = json.loads(line)
        it.pop("serve", None)
        it["rule"] = rule_of(it)
        out[it["id"]] = it
    return out


def arm_results(name: str) -> dict[str, dict[str, Any]]:
    d = DATA / "runs" / name
    out = {}
    for p in d.glob("*.json"):
        if p.name in ("arm.json",):
            continue
        r = json.loads(p.read_text())
        out[r["id"]] = r
    return out


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    z = 1.96
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def score_arm(items: dict[str, dict[str, Any]], res: dict[str, dict[str, Any]], split: str,
              ids: set[str] | None = None) -> dict[str, dict[str, Any]]:
    table: dict[str, dict[str, Any]] = {}
    for iid, r in res.items():
        it = items.get(iid)
        if it is None or it["rule"] is None or (ids is not None and iid not in ids):
            continue
        if split == "dev" and it["holdout"] or split == "holdout" and not it["holdout"]:
            continue
        rule = it["rule"]
        if not decisive(it, rule):
            continue
        row = table.setdefault(rule, {"n": 0, "ok": 0, "fail": 0, "regret": 0.0, "none": 0, "reads": 0,
                                      "logs": 0, "tokens": 0})
        row["n"] += 1
        row["reads"] += int(bool(r.get("skill_reads")))
        row["logs"] += int(r.get("log_calls", 0) > 0)
        u = r.get("usage") or {}
        row["tokens"] += u.get("input", 0) + u.get("cache_read", 0) + u.get("cache_create", 0) + u.get("output", 0)
        k = r.get("choice")
        if k is None or str(k) not in it["q"]:
            row["none"] += 1
            row["fail"] += 1
            continue
        q = {int(a): v for a, v in it["q"].items()}
        row["ok"] += int(k in right_set(it, rule))
        row["fail"] += int(rule_fail(it, rule, k))
        row["regret"] += max(q.values()) - q[k]
    for row in table.values():
        n = max(1, row["n"])
        row["ok_rate"] = row["ok"] / n
        row["ok_ci"] = wilson(row["ok"], row["n"])
        row["fail_rate"] = row["fail"] / n
        row["regret_mean"] = row["regret"] / n
        row["read_rate"] = row["reads"] / n
        row["tokens_mean"] = row["tokens"] / n
    return table


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default=str(DATA / "items.jsonl"))
    ap.add_argument("--arms", required=True)
    ap.add_argument("--split", default="all", choices=("all", "dev", "holdout"))
    ap.add_argument("--common", action="store_true", help="only items every arm answered")
    a = ap.parse_args()
    items = load_items(Path(a.items))
    arms = a.arms.split(",")
    res = {arm: arm_results(arm) for arm in arms}
    ids = set.intersection(*(set(r) for r in res.values())) if a.common else None
    print(f"| arm | rule | n | right % (95 % CI) | rule failures % | regret (pts) | read Skill % | logs % | tokens |")
    print("|---|---|---:|---|---:|---:|---:|---:|---:|")
    for rule in RULES:
        for arm in arms:
            t = score_arm(items, res[arm], a.split, ids).get(rule)
            if not t:
                continue
            lo, hi = t["ok_ci"]
            print(f"| {arm} | {rule} | {t['n']} | {100*t['ok_rate']:.0f} ({100*lo:.0f}–{100*hi:.0f}) | "
                  f"{100*t['fail_rate']:.0f} | {t['regret_mean']:.2f} | {100*t['read_rate']:.0f} | "
                  f"{100*t['logs']/t['n']:.0f} | {t['tokens_mean']/1000:.0f}k |")


if __name__ == "__main__":
    main()
