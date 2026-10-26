"""Analyse promotion-study trajectories: first-promotion factors and the event pool.

    python3 scripts/promotion-study/analyse.py [runs_dir] [out_dir]

Writes episodes.csv (one row per episode, first-semester features) and prints the
summaries. Event titles are used only for the pool/ordering analysis, never as Skill content.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

RUNS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "careerlab-data/promotion-study/runs"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "careerlab-data/promotion-study"

# Coarse, event-agnostic option categories from wording (lab device for analysis only).
KINDS = {
    "own": r"\b(lead|take (?:it )?on|own|step up|volunteer|fix|build|deliver|propose|agree|offer|draft|pair|help|run the|sign-off|plan)\b",
    "visible": r"\b(report|present|show|showcase|credit|visib|announce|demo|publicis|speak up|pitch)\b",
    "avoid": r"\b(say nothing|stay silent|ignore|leave it|decline|wait|skip|keep quiet|let it|put your head down|walk away|avoid|hold off)\b",
    "confront": r"\b(call (?:him|her|them) out|argue|hit back|blame|escalat|complain|confront|snap)\b",
    "shady": r"\b(hide|conceal|inflate|pretend|sit on|cover up|fudge|quietly change|backdate|bend|cut corners|skip the test)\b",
    "overwork": r"\b(work late|overnight|weekend|all-nighter|push through|cram|extra hours)\b",
}
KRX = {k: re.compile(v, re.I) for k, v in KINDS.items()}
PROMO = re.compile(r"Promotion notice: .*? moved from (L\d+) to (L\d+)")
GRADE = re.compile(r"Half-year performance bonus \(([SABCD])\)")
MAINS = ["Apply for a key project", "Report results to your manager", "Fight for resources", "Apply for rotation",
         "Showcase results", "Build a mentorship", "Repair a key relationship", "Lay low and reduce risk"]


def month_of(obs: dict) -> int:
    return int(((obs.get("current_state") or {}).get("time") or {}).get("current_month") or 0)


def parse(run: Path) -> tuple[dict, list[tuple[int, str, int, int]]] | None:
    tp = run / "trajectory.jsonl"
    if not (run / "result.json").exists() or not tp.exists():
        return None
    res = json.loads((run / "result.json").read_text())
    row: dict = {"job": run.name, "T": res.get("survival_months") or 0, "Q": res.get("quantitative_score"),
                 "outcome": res.get("outcome"), "failure": (res.get("failure_reason") or "")[:40]}
    feats = Counter()
    events_seen: list[tuple[int, str, int, int]] = []  # (month, title, n_choices, chosen)
    last_obs, last_events, mix = None, "", None
    promos: list[tuple[int, str]] = []
    grades: list[tuple[int, str]] = []
    pre_review = None
    hmin = 10.0
    for line in tp.open(encoding="utf-8", errors="replace"):
        rec = json.loads(line)
        k = rec.get("kind")
        if k == "new_game":
            mix = (rec.get("actor") or {}).get("mix")
        elif k == "obs":
            obs = rec.get("obs") or {}
            last_obs = obs
            mo = month_of(obs)
            st = (obs.get("current_state") or {}).get("status") or {}
            if mo <= 6 and st:
                hmin = min(hmin, float(st.get("health", 10)))
            ev = obs.get("events") or ""
            if ev and ev != last_events:
                for a, b in PROMO.findall(ev):
                    promos.append((mo, b))
                for g in GRADE.findall(ev):
                    grades.append((mo, g))
                if mo <= 6:
                    low = ev.lower()
                    feats["hr_risk"] += ("some risk" in low) or ("risk has" in low) or ("risks have" in low) or ("piled up" in low)
                    feats["hr_ok"] += "doing all right" in low
                    feats["hr_uneasy"] += ("uneasy" in low) or ("on your own" in low)
            last_events = ev
            title = (obs.get("current_event") or {}).get("title") or ""
            if mo == 6 and title == "Quarterly main action" and pre_review is None:
                pre_review = dict(st)
        elif k == "act" and last_obs is not None:
            mo = month_of(last_obs)
            ce = last_obs.get("current_event") or {}
            title = ce.get("title") or ""
            choices = last_obs.get("choices") or []
            chosen = next((c for c in choices if c.get("choice") == rec.get("choice")), None)
            text = (chosen or {}).get("action", "")
            if title == "Quarterly main action":
                if mo <= 6:
                    for m in MAINS:
                        if text.startswith(m):
                            feats["main_" + m.split()[0].lower() + "_" + m.split()[-1].lower()] += 1
            elif title == "Quarterly energy allocation" or title in ("New hire handbook",):
                pass
            elif choices:
                events_seen.append((mo, title, len(choices), int(rec.get("choice") or 0)))
                if mo <= 6:
                    feats["story_n"] += 1
                    feats["story_first"] += int(rec.get("choice") == 1)
                    for kname, rx in KRX.items():
                        feats["kind_" + kname] += bool(rx.search(text))
    row.update(mix=mix, hmin6=hmin, **feats)
    row["reached6"] = int(row["T"] >= 7 or any(m <= 7 for m, _ in promos))
    row["promo6"] = int(any(m <= 7 for m, _ in promos))
    row["promo12"] = int(any(m <= 13 for m, _ in promos))
    row["reached12"] = int(row["T"] >= 13 or row["promo12"])
    row["grade6"] = next((g for m, g in grades if m <= 7), None)
    for key in ("skill", "network", "output", "health", "dignity"):
        row["pre_" + key] = (pre_review or {}).get(key)
    return row, events_seen


def main() -> None:
    rows, pool = [], []
    for run in sorted(RUNS.glob("promo-*")):
        p = parse(run)
        if p:
            rows.append(p[0])
            pool += [(p[0]["job"],) + e for e in p[1]]
    df = pd.DataFrame(rows).fillna(0)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "episodes.csv", index=False)
    ev = pd.DataFrame(pool, columns=["job", "month", "title", "n_choices", "chosen"])
    ev.to_csv(OUT / "events.csv", index=False)

    print(f"episodes {len(df)}; reached first review {int(df.reached6.sum())}; promoted at first review {int(df.promo6.sum())}")
    print("outcomes:", df.failure.value_counts().head(6).to_dict())
    r6 = df[df.reached6 == 1]
    if len(r6):
        print(f"\nP(promo at first review | reached) = {r6.promo6.mean():.3f}  (n={len(r6)})")
        print("by Energy mix:", r6.groupby("mix").promo6.agg(["mean", "count"]).round(3).to_dict("index"))
        print("first grade:", r6.grade6.value_counts().to_dict())
        print("pre-review visible stats (promoted vs not):")
        print(r6.groupby("promo6")[["pre_skill", "pre_network", "pre_output", "pre_health", "pre_dignity", "hmin6"]].mean().round(2))
        feat = [c for c in r6.columns if c.startswith(("kind_", "main_", "hr_", "story_"))]
        print("\nfirst-semester features (mean, promoted vs not):")
        print(r6.groupby("promo6")[feat].mean().T.round(2))
        cap = (r6.pre_skill >= 9) & (r6.pre_network >= 3) & (r6.pre_output >= 3)
        print(f"\nat the L1 visible cap before review: n={int(cap.sum())}, P(promo)={r6[cap].promo6.mean():.3f}; "
              f"below cap: n={int((~cap).sum())}, P(promo)={r6[~cap].promo6.mean():.3f}")
        if r6.promo6.sum() >= 15:
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler
            X = r6[["pre_skill", "pre_network", "pre_output", "pre_health", "pre_dignity", "hmin6"] + feat].astype(float)
            Xs = StandardScaler().fit_transform(X)
            lr = LogisticRegression(C=0.3, max_iter=2000).fit(Xs, r6.promo6)
            coef = pd.Series(lr.coef_[0], index=X.columns).sort_values()
            print("\nlogistic regression on promo6 (standardised coefficients, L2-regularised):")
            print(pd.concat([coef.head(6), coef.tail(8)]).round(2))
            capped = r6[cap]
            if capped.promo6.sum() >= 10:
                Xc = StandardScaler().fit_transform(capped[feat + ["pre_health", "pre_dignity", "hmin6"]].astype(float))
                lc = LogisticRegression(C=0.3, max_iter=2000).fit(Xc, capped.promo6)
                cc = pd.Series(lc.coef_[0], index=feat + ["pre_health", "pre_dignity", "hmin6"]).sort_values()
                print("\nsame, only episodes at the visible cap (what separates them beyond stats):")
                print(pd.concat([cc.head(5), cc.tail(6)]).round(2))

    print(f"\nEVENT POOL: {ev.title.nunique()} distinct titles over {len(ev)} story decisions")
    first_month = ev.groupby(["job", "title"]).month.min().reset_index()
    span = first_month.groupby("title").month.agg(["min", "max", "count"])
    print("titles by earliest month seen (first 10):")
    print(span.sort_values(["min", "count"], ascending=[True, False]).head(10))
    per_job = ev.groupby("job").title.apply(lambda s: list(dict.fromkeys(s)))
    m1 = per_job.apply(lambda t: tuple(t[:3]))
    print(f"distinct opening sequences (first 3 titles): {m1.nunique()} over {len(m1)} episodes")
    repeats = ev.groupby(["job", "title"]).size()
    print(f"share of titles that come back within an episode (chains/follow-ups): {(repeats > 1).mean():.2f}")


if __name__ == "__main__":
    main()
