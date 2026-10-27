"""Score stat labels against the exact effects, on the design half and on the reserved half of the events.

Inputs: answers.json (built with Alejandro's scripts/question-bank/build_answers.py), split.json
({design: [titles], eval: [titles]}, fixed before any variant was written) and any number of tag files:
either {key: {stat: -1|0|1}} (label.py) or {key: {up: [...], down: [...]}} (Alejandro's stat-tags.json).
"prior" is added automatically: each category's majority direction per stat, learnt on the design half.

Also writes every tag file in Alejandro's up/down format to --catbot-dir, ready for his catbot.py --tags.

    python3 scripts/leah/stat_perception/evaluate.py --answers A --split S --tags ale=X defs=Y ... --catbot-dir D
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

STATS = ["skill", "network", "output", "health", "dignity"]


def norm(t: dict) -> dict:
    if "up" in t or "down" in t:
        return {s: (1 if s in t.get("up", []) else -1 if s in t.get("down", []) else 0) for s in STATS}
    return {s: int(t.get(s, 0)) for s in STATS}


def truth(a: dict, s: str) -> int:
    v = a["d"].get(s, 0)
    return (v > 0) - (v < 0)


def prior(answers: list[dict], design: set) -> dict:
    by = defaultdict(lambda: defaultdict(Counter))
    for a in answers:
        if a["title"] in design:
            for s in STATS:
                by[a["cat"]][s][truth(a, s)] += 1
    rule = {c: {s: cnt.most_common(1)[0][0] for s, cnt in d.items()} for c, d in by.items()}
    return {f"{a['node']}:{a['choice']}": dict(rule.get(a["cat"], {s: 0 for s in STATS})) for a in answers}


def scores(answers: list[dict], tags: dict) -> dict:
    out = {}
    for s in STATS:
        tp_u = sum(1 for a in answers if truth(a, s) > 0 and tags[a["k"]][s] > 0)
        tp_d = sum(1 for a in answers if truth(a, s) < 0 and tags[a["k"]][s] < 0)
        n_u, n_d = sum(truth(a, s) > 0 for a in answers), sum(truth(a, s) < 0 for a in answers)
        p_u, p_d = sum(tags[a["k"]][s] > 0 for a in answers), sum(tags[a["k"]][s] < 0 for a in answers)
        acc = sum(tags[a["k"]][s] == truth(a, s) for a in answers) / len(answers)
        out[s] = {"up_recall": tp_u / max(n_u, 1), "up_precision": tp_u / max(p_u, 1),
                  "down_recall": tp_d / max(n_d, 1), "down_precision": tp_d / max(p_d, 1), "accuracy": acc}
    out["mean_accuracy"] = sum(out[s]["accuracy"] for s in STATS) / len(STATS)
    return out


def pairwise(answers: list[dict], tags: dict) -> dict:
    """Within one question, for each stat and pair of options whose true effects differ: does the labelling
    order them the same way (ties in the labels count half)? This is what a choice needs."""
    by = defaultdict(list)
    for a in answers:
        by[a["node"]].append(a)
    res = {}
    for s in STATS:
        good = n = 0
        for aa in by.values():
            for i in range(len(aa)):
                for j in range(i + 1, len(aa)):
                    ti, tj = aa[i]["d"].get(s, 0), aa[j]["d"].get(s, 0)
                    if ti == tj:
                        continue
                    li, lj = tags[aa[i]["k"]][s], tags[aa[j]["k"]][s]
                    n += 1
                    good += 1 if (li - lj) * (ti - tj) > 0 else 0.5 if li == lj else 0
        res[s] = good / max(n, 1)
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--split", required=True)
    ap.add_argument("--tags", nargs="+", required=True, help="name=path")
    ap.add_argument("--catbot-dir")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    A = json.load(open(Path(args.answers).expanduser()))
    for a in A:
        a["k"] = f"{a['node']}:{a['choice']}"
    split = json.load(open(Path(args.split).expanduser()))
    design = set(split["design"])
    if any(a["node"] in design for a in A):  # the committed split lists node ids, not titles
        design = {a["title"] for a in A if a["node"] in design}
    sets = {"prior": prior(A, design)}
    for spec in args.tags:
        name, path = spec.split("=", 1)
        raw = json.load(open(Path(path).expanduser()))
        sets[name] = {k: norm(v) for k, v in raw.items()}
    halves = {"design": [a for a in A if a["title"] in design], "eval": [a for a in A if a["title"] not in design]}
    report = {}
    print("Reserved half (eval), per stat: up recall / up precision | down recall / down precision | pairwise order")
    for name, tags in sets.items():
        missing = sum(a["k"] not in tags for a in A)
        for a in A:
            tags.setdefault(a["k"], {s: 0 for s in STATS})
        report[name] = {h: {"scores": scores(aa, tags), "pairwise": pairwise(aa, tags)} for h, aa in halves.items()}
        ev = report[name]["eval"]
        cells = "  ".join(f"{s[:4]} {ev['scores'][s]['up_recall']:.2f}/{ev['scores'][s]['up_precision']:.2f}|"
                          f"{ev['scores'][s]['down_recall']:.2f}/{ev['scores'][s]['down_precision']:.2f}|{ev['pairwise'][s]:.2f}"
                          for s in STATS)
        pw = sum(ev["pairwise"].values()) / len(STATS)
        print(f"{name:9s} acc {ev['scores']['mean_accuracy']:.3f} pair {pw:.3f}  {cells}" + (f"  (missing {missing})" if missing else ""))
        if args.catbot_dir:
            d = Path(args.catbot_dir).expanduser()
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{name}.json").write_text(json.dumps(
                {k: {"up": [s for s in STATS if v[s] > 0], "down": [s for s in STATS if v[s] < 0]} for k, v in tags.items()}))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
