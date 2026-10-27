"""Analyse question-bank batches: per-question option effects with known assignment.

Reads <data>/<batch>/episodes-*.jsonl and questions.json written by run.py and writes
decisions.parquet-like JSONL plus bank.json (per question and option: counts, immediate
visible change, change in the HR risk remark, failure within 3 months, and the final
competition score adjusted for the state at decision time).

Only decisions drawn at random (flag r=1) are used for effect estimates, so within a
question the option is independent of the history and the comparison is causal for
that bot context (energy bundles and main actions drawn at random, stories as in the batch).

    python3 scripts/question-bank/analyse.py ~/careerlab-data/question-bank explore greedy1 --out <dir>
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

HR_LEVELS = [("smiling", 0), ("quietly", 1), ("frowning", 2), ("uneasy", 3), ("angry", 4)]
STAT = ["health", "dignity", "skill", "network", "output", "wealth", "dil", "level"]


def hr_level(text: str | None) -> int | None:
    if not text or "HR partner" not in text:
        return None
    seg = text[text.index("HR partner"):][:80]
    for word, lvl in HR_LEVELS:
        if word in seg:
            return lvl
    return None


def load(data: Path, batches: list[str]):
    questions: dict[str, dict] = {}
    episodes = []
    for b in batches:
        qf = data / b / "questions.json"
        if qf.exists():
            questions.update(json.loads(qf.read_text()))
        for f in sorted(glob.glob(str(data / b / "episodes-*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                e = json.loads(line)
                e["batch"] = b
                episodes.append(e)
    return questions, episodes


def episode_table(e: dict) -> tuple[list[dict], dict]:
    sc = e["score"] or {}
    dims = {d["name"]: d["normalized_score"] for d in sc.get("dimensions", [])}
    months = sc.get("survival_months") or e["final"][6]
    fail = (e.get("failure") or "")
    kind = ("completed" if sc.get("completed") else
            "trust" if fail.startswith("Trust") else "blackout" if fail.startswith("Blackout") else
            "broke" if fail.startswith("Broke") else "dismissed" if "dismiss" in fail.lower() or "review" in fail.lower() else
            "resign" if fail.startswith("You resign") else "other")
    ep = {"batch": e["batch"], "run": e["run"], "Y": sc.get("competition_partial_score"), "Q": sc.get("quantitative_score"),
          "months": months, "kind": kind, "final_level": e["final"][7], **{f"dim_{k}": v for k, v in dims.items()}}
    rows = e["rows"]
    # HR level reported in the events text of each month (first row of the month that carries it)
    hr_by_month: dict[int, int] = {}
    promo_months, review_months = [], []
    for r in rows:
        lvl = hr_level(r[5])
        if lvl is not None and r[0] not in hr_by_month:
            hr_by_month[r[0]] = lvl
        if r[5] and "Promotion notice" in r[5]:
            promo_months.append(r[0])
        if r[5] and "Half-year performance bonus" in r[5]:
            g = re.search(r"Half-year performance bonus \((\w)\)", r[5])
            review_months.append([r[0], g.group(1) if g else None])
    ep["promotions"] = promo_months
    ep["reviews"] = review_months
    out = []
    for i, r in enumerate(rows):
        m, kind_r, st = r[0], r[1], r[2]
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        after = nxt[2] if nxt is not None else e["final"]
        same_month = nxt is not None and nxt[0] == m
        d = {"m": m, "phase": kind_r, "state": st, "after": after, "same_month": same_month,
             "hr_now": hr_by_month.get(m), "hr_next": hr_by_month.get(m + 1),
             "fail_3m": int(ep["kind"] not in ("completed",) and months <= m + 3),
             "trust_6m": int(ep["kind"] == "trust" and months <= m + 6)}
        if kind_r == "S":
            d.update(q=r[3], idx=r[4][0], n=r[4][1], rnd=r[4][2])
        else:
            d.update(action=r[3], bundle=r[4])
        out.append(d)
    return out, ep


def features(d: dict) -> list[float]:
    st = d["state"]
    m = d["m"]
    hr = d["hr_now"] if d["hr_now"] is not None else 0
    f = [1.0, m / 48, (m / 48) ** 2]
    f += [st[0] / 10, st[1] / 10, min(st[2], 100) / 100, min(st[3], 100) / 100, min(st[4], 100) / 100, st[5] / 10, st[7] / 10]
    f += [float(st[0] <= 2), float(st[0] <= 4), float(st[1] <= 2), hr / 4, float(hr >= 3)]
    f += [x * m / 48 for x in f[3:10]]
    return f


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("data", type=Path)
    ap.add_argument("batches", nargs="+")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    questions, episodes = load(args.data, args.batches)
    decisions, eps = [], []
    for e in episodes:
        rows, ep = episode_table(e)
        eps.append(ep)
        for d in rows:
            d["ep"] = len(eps) - 1
            decisions.append(d)
    Y = np.array([eps[d["ep"]]["Y"] or 0.0 for d in decisions])
    X = np.array([features(d) for d in decisions])
    # baseline: value of the state at decision time, fitted on every decision of the pooled batches
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    base = X @ beta
    for d, y, b in zip(decisions, Y, base):
        d["Y"], d["adv"] = float(y), float(y - b)
    r2 = 1 - np.var(Y - base) / np.var(Y)
    print(f"{len(eps)} episodes, {len(decisions)} decisions; baseline R2 {r2:.3f}")

    # per question, per option
    bank: dict[str, dict] = {}
    groups: dict[str, dict[int, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for d in decisions:
        if d["phase"] == "S" and d["rnd"]:
            groups[d["q"]][d["idx"]].append(d)
    for q, opts in groups.items():
        meta = questions.get(q, {})
        n_opt = len(meta.get("options", [])) or (max(opts) + 1)
        entry = {"title": meta.get("title"), "description": meta.get("description"), "options": []}
        for i in range(n_opt):
            ds = opts.get(i, [])
            same = [x for x in ds if x["same_month"]]
            imm = (np.mean([np.array(x["after"][:6]) - np.array(x["state"][:6]) for x in same], axis=0).round(2).tolist()
                   if same else None)
            hr = [x["hr_next"] - x["hr_now"] for x in ds if x["hr_next"] is not None and x["hr_now"] is not None]
            adv = [x["adv"] for x in ds]
            entry["options"].append({
                "text": (meta.get("options") or [None] * n_opt)[i] if i < len(meta.get("options") or []) else None,
                "n": len(ds), "imm": imm, "n_imm": len(same),
                "hr_delta": round(float(np.mean(hr)), 3) if hr else None, "n_hr": len(hr),
                "fail_3m": round(float(np.mean([x["fail_3m"] for x in ds])), 3) if ds else None,
                "adv": round(float(np.mean(adv)), 2) if adv else None,
                "adv_se": round(float(np.std(adv, ddof=1) / np.sqrt(len(adv))), 2) if len(adv) > 1 else None,
                "Y": round(float(np.mean([x["Y"] for x in ds])), 2) if ds else None,
                "months": [x["m"] for x in ds],
            })
        entry["n"] = sum(o["n"] for o in entry["options"])
        bank[q] = entry
    (args.out / "bank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=0))
    (args.out / "episodes.json").write_text(json.dumps(eps))
    slim = [{k: v for k, v in d.items() if k not in ()} for d in decisions]
    with open(args.out / "decisions.jsonl", "w") as fh:
        for d in slim:
            fh.write(json.dumps(d, separators=(",", ":")) + "\n")
    print(f"{len(bank)} questions with random draws -> {args.out}")


if __name__ == "__main__":
    main()
