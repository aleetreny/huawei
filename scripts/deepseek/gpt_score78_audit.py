"""Audit saved mv evidence; no model calls, games, fitting, or official internals.

uv run --offline python scripts/deepseek/gpt_score78_audit.py > report.json
Only aggregate results leave this script. Predictive accuracy is not policy value.
"""
import collections
import csv
import gzip
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DS = ROOT / "lab/data/deepseek"
sys.path.insert(0, str(ROOT / "scripts/exploracion"))
import choice_model as CM


def norm(s):
    return re.sub(r"\W+", " ", str(s).lower()).strip()


def tone(s):
    for word, number in [("angry", 4), ("uneasy", 3), ("frowning", 2),
                         ("quietly", 1), ("smiling", 0)]:
        if word in s:
            return number
    return None


def accepted_calls(path):
    """Join non-delta calls/results by id, preserving exporter observation scope."""
    obs = None
    pending, result = {}, collections.defaultdict(list)
    for line in gzip.open(path, "rt"):
        event = json.loads(line)
        p = event.get("payload", {})
        if "delta" in p:
            continue
        if event["kind"] == "tool_call":
            call = p.get("tool_call", {})
            if not call.get("name", "").endswith("take_action"):
                continue
            try:
                args = json.loads(call.get("arguments", "{}"))
            except (ValueError, TypeError):
                args = {}
            if obs and (obs.get("current_state") or {}).get("status"):
                state = obs["current_state"]
                key = (str(state["time"]["current_month"]),
                       (obs.get("current_event") or {}).get("title", ""),
                       str(args.get("choice", "")), args.get("notes", ""))
                pending[call.get("tool_call_id")] = key
            obs = None
        if event["kind"] != "tool_result":
            continue
        raw = (p.get("raw_output") or {}).get("result")
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
        except (ValueError, TypeError):
            parsed = None
        if not isinstance(parsed, dict):
            continue
        if p.get("tool_name", "").endswith("observe"):
            obs = parsed
        elif p.get("tool_name", "").endswith("take_action"):
            key = pending.pop(p.get("tool_call_id"), None)
            if key:
                result[key].append(parsed.get("success"))
    return result


def main():
    catalog = json.loads((ROOT / "lab/data/ingenieria-inversa/catalog_v2.json").read_text())
    answers = json.load(gzip.open(DS / "otros/answers.json.gz", "rt"))
    texts = {(a["node"], str(a["choice"])): norm(a["text"]) for a in answers}
    titles = collections.defaultdict(list)
    for node_id, node in catalog["nodes"].items():
        titles[node["title"]].append(node_id)
    labels = {f: json.loads((DS / "etiquetas" / (f + ".json")).read_text())
              for f in ("ds-v1-r1-full", "ds-v1-r2-full", "ds-v3-r1-full", "ds-v3-r2-full")}
    models = {}
    for name in ("all", "v4fam"):
        path = ROOT / "lab/data/exploracion" / ("choice_beta" + ("_v4fam" if name == "v4fam" else "") + ".json")
        m = json.loads(path.read_text())
        models[name] = (m["beta"], [CM.FEATS.index(n) for n in m["names"]])
    raw = {p.parent.name: accepted_calls(p) for p in sorted((DS / "partidas").glob("mv-*__*/events.jsonl.gz"))}
    counts, aggregates, dominated = collections.Counter(), collections.defaultdict(collections.Counter), collections.Counter()
    dom_titles, dom_games = set(), set()
    dom_patterns = collections.Counter()
    dom_nodes = collections.Counter()
    for row in csv.DictReader(gzip.open(DS / "decisiones.csv.gz", "rt")):
        if row["manual"] not in ("mv-3", "mv-4") or row["tipo"] != "historia" or int(row["n_opciones"] or 0) < 2:
            continue
        counts["exported"] += 1
        key = (row["mes"], row["situacion"], row["eleccion"], row["nota"])
        statuses = raw[row["partida"]].get(key, [])
        counts["raw_unique_success" if statuses == [True] else "raw_other"] += 1
        ids = [n for n in titles[row["situacion"]]
               if len(catalog["nodes"][n]["choices"]) == int(row["n_opciones"])
               and row["texto_eleccion"] and texts.get((n, row["eleccion"])) == norm(row["texto_eleccion"])]
        if len(ids) != 1:
            counts["unmatched_catalog"] += 1
            continue
        counts["matched"] += 1
        if statuses != [True]:
            counts["matched_not_unique_success"] += 1
        nid = ids[0]
        node = catalog["nodes"][nid]
        keys = list(node["choices"])
        chosen = keys.index(row["eleccion"])
        state = {k: float(row[k]) for k in CM.LABK if k != "risk"}
        level, month = int(row["nivel"][1:]), int(row["mes"])
        n, hr = 6 - month % 6, tone(row["comentario_rrhh"])
        risks = [catalog["risk"].get(f"E|{nid}|{k}", 0) for k in keys]
        effects = [node["choices"][k]["d"] for k in keys]
        X = [CM.features(state, level, n, hr, d, risk,
                         CM.mean_lab({f: lab.get(f"{nid}:{k}") for f, lab in labels.items()}))
             for k, d, risk in zip(keys, effects, risks)]
        groups = ["all", row["manual"], row["partida"], "L" + str(level)]
        if n in (1, 2):
            groups.append("review_near")
        if level == 1 and n == 1:
            groups.append("L1_last_month")
        if hr is not None and hr >= 2:
            groups.append("hr_adverse")
        if min(risks) > 0:
            groups.append("all_options_risky")
        if statuses == [True]:
            groups.append("raw_verified")
        for model, (beta, cols) in models.items():
            logits = [sum(b * x[c] for b, c in zip(beta, cols)) for x in X]
            vals = [math.exp(z - max(logits)) for z in logits]
            probs = [v / sum(vals) for v in vals]
            for group in groups:
                acc = aggregates[model + "/" + group]
                acc["n"] += 1
                acc["top1_correct"] += logits.index(max(logits)) == chosen
                acc["nll_sum"] += -math.log(max(1e-12, probs[chosen]))
                acc["observed_positive_risk"] += risks[chosen] > 0
                acc["expected_positive_risk"] += sum(p for p, r in zip(probs, risks) if r > 0)
                acc["observed_NO_loss"] += any(effects[chosen].get(k, 0) < 0 for k in ("network", "output"))
                acc["expected_NO_loss"] += sum(p for p, d in zip(probs, effects) if any(d.get(k, 0) < 0 for k in ("network", "output")))
        chosen_d, chosen_r = effects[chosen], risks[chosen]
        better = [i for i, (d, r) in enumerate(zip(effects, risks))
                  if r <= chosen_r and all(d.get(k, 0) >= chosen_d.get(k, 0) for k in state)
                  and (r < chosen_r or any(d.get(k, 0) > chosen_d.get(k, 0) for k in state))]
        if better:
            dom_titles.add(node["title"]); dom_games.add(row["partida"])
            dom_nodes[nid] += 1
            dominated["records"] += 1
            dominated["chosen_risk_positive"] += chosen_r > 0
            dominated["chosen_already_risk_reducing"] += chosen_r < 0
            ch = node["choices"][keys[chosen]]
            same = [i for i in better if all(node["choices"][keys[i]].get(k) == ch.get(k) for k in ("next", "when"))]
            dominated["same_continuation"] += bool(same)
            dominated["near_review"] += n in (1, 2)
            dominated["raw_unique_success"] += statuses == [True]
            for i in same[:1]:
                st_chosen = CM.R.State(level=level, **state)
                st_alt = CM.R.State(level=level, **state)
                for st, delta in ((st_chosen, chosen_d), (st_alt, effects[i])):
                    adjusted = dict(delta)
                    if adjusted.get("wealth", 0) < 0:
                        adjusted["wealth"] *= (level + 1) // 2
                    CM.R.apply_delta(st, adjusted)
                retained = sorted(k for k in state if getattr(st_alt, k) > getattr(st_chosen, k))
                if risks[i] < chosen_r:
                    retained.append("risk_reduction_nominal")
                dominated["same_continuation_with_visible_or_nominal_risk_advantage"] += bool(retained)
                dom_patterns["+".join(retained) or "all_advantages_clipped"] += 1
    for result in aggregates.values():
        result["accuracy"] = result["top1_correct"] / result["n"]
        result["mean_nll"] = result["nll_sum"] / result["n"]
    dominated["distinct_titles"] = len(dom_titles)
    dominated["distinct_games"] = len(dom_games)
    dominated["largest_node_count"] = max(dom_nodes.values(), default=0)
    score = []
    for path in sorted((DS / "partidas").glob("mv-*__*/score_report.json")):
        r = json.loads(path.read_text()); e = r.get("ending_score") or {}
        if e.get("quantitative_score") is None:
            continue
        q = e["quantitative_score"]; months = e["survival_months"]
        tpm = r["token_usage"]["total_tokens"] / months
        eff = max(0, min(100, (3000000-tpm) / 25000))
        if months < 48:
            eff = min(50, eff)
        score.append({"run": path.parent.name, "Q": q, "E": eff, "tpm": tpm,
                      "completed": e["completed"], "auto_D80": .8*q+8+.1*eff})
    # Required frequency is sensitivity under the declared two-outcome model, not a forecast.
    sensitivity = []
    for d in (73, 80, 90, 100):
        for c in (74, 75, 77.78, 80):
            zero = .8*c + .1*d + 10
            pmax = (zero-78) / (.8*(c-28.02) + 5)
            sensitivity.append({"quality": d, "completed_Q": c, "score_at_zero_failures": zero,
                                "max_failure_probability": pmax if pmax >= 0 else None})
    assert counts["exported"] == counts["matched"] + counts["unmatched_catalog"]
    assert aggregates["all/all"]["n"] == counts["matched"]
    assert all(0 <= x["E"] <= 100 for x in score)
    best3 = sorted(score, key=lambda x: .8*x["Q"]+.1*x["E"], reverse=True)[:3]
    best3_general = {str(d): sum(.8*x["Q"]+.1*x["E"]+.1*d for x in best3)/3 for d in (73,80,90,100)}
    output = {"scope": "Saved traces only; fixed models, no refitting; model has privileged catalog features.",
              "coverage": counts, "local_dominance": dominated,
              "same_continuation_advantages": dom_patterns, "predictive": aggregates,
              "scores": score, "target78_Q_E100": {str(d):(78-.1*d-10)/.8 for d in (73,80,90,100)},
              "best_three_descriptive_only": {"runs": [x["run"] for x in best3], "automated_by_quality": best3_general},
              "scored_at_least72": sum(x["Q"] >= 72 for x in score),
              "failure_sensitivity_Q28_02_E50": sensitivity,
              "zero_failures_trials_one_sided95": {str(p): math.ceil(math.log(.05)/math.log(1-p)) for p in (.1,.05,.03)}}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
