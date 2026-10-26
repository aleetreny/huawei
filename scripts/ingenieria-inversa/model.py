"""Build the research effect model from black-box batches (never Skill content).

For every visible story question (node) and answer k:
- nominal stat changes from the official log line of that choice;
- the change in the HR partner's risk remark between the month of the choice and the next
  month, relative to the other answers of the same question (choices are randomised in the
  exploration batches, so this difference estimates the answer's hidden-risk push);
- which question follows in the same story (chains).
Also the highest month-start value of Skill, Network and Output seen at each level.

    python3 model.py --batches b00-random-safe --out ~/careerlab-data/ingenieria-inversa/models/m01.json
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any

from bbdata import IDX, Batch, parse_choice_entry

RISK_WORDS = (("smiling", 0), ("quietly", 1), ("frowning", 2), ("uneasy", 3), ("angry", 4))


def risk_level(text: str) -> int | None:
    m = re.search(r"An HR partner you get on with says,? (\w+)", text or "")
    if not m:
        return None
    word = m.group(1)
    for w, lv in RISK_WORDS:
        if word.startswith(w):
            return lv
    return None


def aligned(b: Batch, g: dict[str, Any]):
    st = [s for s in g["steps"] if s[1] in ("e", "q", "m")]
    ents = [parse_choice_entry(m) for c, m in b.log_entries(g) if c in ("A", "F")]
    ents = [e for e in ents if e]
    if len(st) != len(ents):
        return None
    return list(zip(st, ents))


def month_risk(b: Batch, g: dict[str, Any]) -> dict[int, int]:
    out: dict[int, int] = {}
    for s in g["steps"]:
        if s[5]:
            lv = risk_level(b.texts.get(s[5], ""))
            if lv is not None and s[0] not in out:
                out[s[0]] = lv
    return out


def build(batches: list[str], min_n: int = 1) -> dict[str, Any]:
    b = Batch(*batches)
    eff: dict[tuple[str, int], dict[str, Any]] = {}
    risk: dict[tuple[str, int], list[float]] = collections.defaultdict(list)
    blow: dict[tuple[str, int], list[int]] = collections.defaultdict(lambda: [0, 0])
    nxt: dict[tuple[str, int], collections.Counter] = collections.defaultdict(collections.Counter)
    ceil: dict[int, dict[str, int]] = collections.defaultdict(lambda: {"skill": 0, "network": 0, "output": 0})
    clamp: dict[tuple[int, str], collections.Counter] = collections.defaultdict(collections.Counter)
    games = 0
    for g in b.games():
        pairs = aligned(b, g)
        if pairs is None:
            continue
        games += 1
        mr = month_risk(b, g)
        seen_month = set()
        for s in g["steps"]:
            if s[0] not in seen_month:
                seen_month.add(s[0])
                lv = s[4][IDX["level"]]
                for k in ("skill", "network", "output"):
                    ceil[lv][k] = max(ceil[lv][k], s[4][IDX[k]])
        story = [(s, e) for s, e in pairs if s[1] == "e"]
        pos = {id(s): i for i, s in enumerate(g["steps"])}
        blow_idx = [i for i, s in enumerate(g["steps"]) if s[5] and "Old landmines" in b.texts.get(s[5], "")]
        last_month = g["final"]["t"] if g.get("final") else 0
        for s, _ in story:
            i = pos[id(s)]
            hit = any(j > i and g["steps"][j][0] <= s[0] + 3 for j in blow_idx)
            if hit or last_month >= s[0] + 3:
                blow[(s[2], s[3])][0] += 1
                blow[(s[2], s[3])][1] += int(hit)
        for s, e in story:
            i = pos[id(s)]
            if i + 1 < len(g["steps"]) and g["steps"][i + 1][0] == s[0]:
                after = g["steps"][i + 1][4]
                for k in ("skill", "network", "output"):
                    nom = e["d"].get(k, 0)
                    if nom > 0 and s[4][IDX[k]] + nom > after[IDX[k]] >= s[4][IDX[k]]:
                        clamp[(s[4][IDX["level"]], k)][after[IDX[k]]] += 1
        for i, (s, e) in enumerate(story):
            key = (s[2], s[3])
            r = eff.setdefault(key, {"n": 0, "sum": collections.Counter(), "sq": collections.Counter()})
            r["n"] += 1
            for stat, v in e["d"].items():
                r["sum"][stat] += v
                r["sq"][stat] += v * v
            m = s[0]
            if m in mr and m + 1 in mr:
                risk[key].append(mr[m + 1] - mr[m])
            title = b.nodes.get(s[2], {}).get("title")
            for s2, _ in story[i + 1:]:
                if b.nodes.get(s2[2], {}).get("title") == title:
                    nxt[key][s2[2]] += 1
                    break
    # relative risk push: answer mean minus mean over the question's answers
    by_node: dict[str, list[tuple[int, list[float]]]] = collections.defaultdict(list)
    for (node, k), v in risk.items():
        by_node[node].append((k, v))
    rel: dict[tuple[str, int], tuple[float, int]] = {}
    for node, lst in by_node.items():
        means = [sum(v) / len(v) for _, v in lst if v]
        if not means:
            continue
        base = sum(means) / len(means)
        for k, v in lst:
            if v:
                rel[(node, k)] = (sum(v) / len(v) - base, len(v))
    caps: dict[str, dict[str, int]] = {}
    for (lv, k), c in clamp.items():
        value, count = c.most_common(1)[0]
        if count >= 3 and count >= 0.6 * sum(c.values()):
            caps.setdefault(str(lv), {})[k] = value
    blow_rel: dict[tuple[str, int], tuple[float, int]] = {}
    by_node_b: dict[str, list[tuple[int, int, float]]] = collections.defaultdict(list)
    for (node, k), (n, h) in blow.items():
        if n >= 5:
            by_node_b[node].append((k, n, h / n))
    for node, lst in by_node_b.items():
        if len(lst) < 2:
            continue
        base = sum(r for _, _, r in lst) / len(lst)
        for k, n, r in lst:
            blow_rel[(node, k)] = (r - base, n)
    model: dict[str, Any] = {"batches": batches, "games": games, "nodes": {}, "ceil": caps,
                             "month_start_max": {str(k): v for k, v in sorted(ceil.items())}}
    for (node, k), r in eff.items():
        if r["n"] < min_n:
            continue
        n = r["n"]
        mean = {stat: round(sm / n, 3) for stat, sm in r["sum"].items()}
        entry = {"n": n, "mean": mean}
        if (node, k) in rel:
            entry["risk"] = round(rel[(node, k)][0], 3)
            entry["risk_n"] = rel[(node, k)][1]
        if (node, k) in blow_rel:
            entry["blow3"] = round(blow_rel[(node, k)][0], 3)
            entry["blow_n"] = blow_rel[(node, k)][1]
        if nxt[(node, k)]:
            entry["next"] = dict(nxt[(node, k)].most_common(5))
        model["nodes"].setdefault(node, {})[str(k)] = entry
    return model


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batches", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    model = build(args.batches.split(","))
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model))
    print(json.dumps({"games": model["games"], "nodes": len(model["nodes"]),
                      "answers": sum(len(v) for v in model["nodes"].values()), "ceil": model["ceil"]}))


if __name__ == "__main__":
    main()
