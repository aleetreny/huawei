"""Do general answer traits predict an answer's effects on questions never seen in training?

Inputs: the research model (per-answer effects measured in dev) and trait labels (tags + integrity)
given to each answer text by a separate labelling pass. Fits a ridge regression from traits to each
effect, with folds grouped by event title, so every prediction comes from a model that never saw
that story. Writes the out-of-fold predictions as a model file the "principles" bot can play with.

    .venv/bin/python semantics.py --model m04.json --labels labels/out-*.jsonl --out principles-m04.json
"""

from __future__ import annotations

import argparse
import glob
import json
import random
from collections import defaultdict
from pathlib import Path

import numpy as np

from bbdata import Batch

TAGS = ["OWN", "TRANSPARENT", "PROCESS", "QUALITY", "CONFIDENTIAL", "HELP", "COLLABORATE", "ESCALATE", "BOUNDARY",
        "VISIBILITY", "SHORTCUT", "CONCEAL", "DECEIVE", "GOSSIP", "CONFRONT", "PASSIVE", "OVERWORK", "APPEASE",
        "LEARN", "SELF_CARE"]
TARGETS = ["skill", "network", "output", "health", "dignity", "wealth", "risk", "blow3"]


def features(tags: list[str], integrity: int) -> list[float]:
    return [1.0] + [1.0 if t in tags else 0.0 for t in TAGS] + [float(integrity)]


def ridge(X: np.ndarray, y: np.ndarray, lam: float = 1.0) -> np.ndarray:
    pen = lam * np.eye(X.shape[1])
    pen[0, 0] = 0.0
    return np.linalg.solve(X.T @ X + pen, X.T @ y)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--batches", default="b00-random-safe,b01-oracle-eps10")
    args = ap.parse_args()
    model = json.loads(Path(args.model).expanduser().read_text())
    labels = {}
    for p in glob.glob(str(Path(args.labels).expanduser())):
        for line in open(p):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            labels[(r["node"], int(r["k"]))] = (r.get("tags", []), int(r.get("integrity", 0)))
    b = Batch(*args.batches.split(","))
    rows = []
    for node, opts in model["nodes"].items():
        title = b.nodes.get(node, {}).get("title", node)
        for k, e in opts.items():
            lab = labels.get((node, int(k)))
            if not lab:
                continue
            y = {t: e["mean"].get(t, 0.0) for t in TARGETS[:6]}
            y["risk"] = e.get("risk") if e.get("risk_n", 0) >= 3 else None
            y["blow3"] = e.get("blow3") if e.get("blow_n", 0) >= 10 else None
            rows.append({"node": node, "k": int(k), "title": title, "x": features(*lab), "y": y, "n": e["n"], "tags": lab[0], "integrity": lab[1]})
    titles = sorted({r["title"] for r in rows})
    random.Random(7).shuffle(titles)
    fold_of = {t: i % args.folds for i, t in enumerate(titles)}
    pred = defaultdict(dict)
    report = {}
    for target in TARGETS:
        use = [r for r in rows if r["y"][target] is not None]
        X = np.array([r["x"] for r in use])
        y = np.array([r["y"][target] for r in use])
        w = np.sqrt(np.minimum(np.array([r["n"] for r in use], dtype=float), 50.0))
        oof = np.zeros(len(use))
        for f in range(args.folds):
            tr = np.array([fold_of[r["title"]] != f for r in use])
            te = ~tr
            beta = ridge(X[tr] * w[tr, None], y[tr] * w[tr])
            oof[te] = X[te] @ beta
        ss_res = float(np.sum(w * (y - oof) ** 2))
        ss_tot = float(np.sum(w * (y - np.average(y, weights=w)) ** 2))
        corr = float(np.corrcoef(y, oof)[0, 1])
        beta_all = ridge(X * w[:, None], y * w)
        report[target] = {"n": len(use), "r2_heldout_titles": round(1 - ss_res / ss_tot, 3), "corr": round(corr, 3),
                          "coef": {name: round(float(c), 3) for name, c in zip(["intercept"] + TAGS + ["integrity"], beta_all)}}
        for r, p in zip(use, oof):
            pred[r["node"]][str(r["k"])] = pred[r["node"]].get(str(r["k"]), {}) | {target: round(float(p), 3)}
    # within-question decision test: does the trait model pick the same best answer as the measured effects?
    out_nodes = {}
    for node, opts in pred.items():
        out_nodes[node] = {}
        for k, p in opts.items():
            mean = {t: p[t] for t in TARGETS[:6] if t in p}
            e = {"n": 50, "mean": mean}
            if "risk" in p:
                e["risk"], e["risk_n"] = p["risk"], 50
            if "blow3" in p:
                e["blow3"], e["blow_n"] = p["blow3"], 50
            nxt = model["nodes"].get(node, {}).get(k, {}).get("next")
            if nxt:
                e["next"] = nxt
            out_nodes[node][k] = e
    out = {"source": "out-of-fold trait predictions (titles held out)", "ceil": model.get("ceil", {}), "nodes": out_nodes,
           "report": report}
    Path(args.out).expanduser().write_text(json.dumps(out))
    print(json.dumps({t: {k: v for k, v in r.items() if k != "coef"} for t, r in report.items()}, indent=1))
    print("coefficients (all data):")
    for t, r in report.items():
        top = sorted(r["coef"].items(), key=lambda kv: -abs(kv[1]))[:8]
        print(f"  {t:8s}", ", ".join(f"{k} {v:+.2f}" for k, v in top))


if __name__ == "__main__":
    main()
