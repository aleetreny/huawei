"""Export auditable questions, observed branches and review evidence from public responses."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.first_review_search import node_key


def analyze(source, output):
    output.mkdir(parents=True, exist_ok=True)
    runs = [json.loads(p.read_text()) for p in sorted(source.glob("run-*.json"))]
    questions, edges, reviews, effects = {}, Counter(), [], []
    arms = defaultdict(Counter)
    failures = Counter()
    support_table = Counter()
    maxima = defaultdict(lambda: float("-inf"))
    for r in runs:
        steps = r["steps"]
        review = next((s for s in steps if "Half-year performance bonus" in s["after"].get("events", "")), None)
        outcome = r["outcome"]
        final = r.get("final", {}).get("current_state", {})
        promoted = bool(r.get("promoted"))
        for group in ("all", "story:" + r["arm"][0], "energy:" + r["arm"][1], "main:" + r["arm"][2], "arm:" + "/".join(r["arm"])):
            arms[group][outcome] += 1
            arms[group]["promotion"] += promoted
            arms[group]["review"] += review is not None
            arms[group]["alive_promoted"] += promoted and outcome == "six_month_window"
        if outcome == "eliminated":
            failures[final.get("simulation_flags", {}).get("failure_reason", "unknown")] += 1
        if review:
            text = review["after"]["events"]
            support = any(w in text for w in ("put in a good word", "gave the boss the context", "talked them down", "argued for context"))
            support_table[(support, promoted)] += 1
            row = {"run": r["run"], "arm": r["arm"], "before_time": review["before"]["current_state"]["time"],
                   "after_time": review["after"]["current_state"]["time"],
                   "before": review["before"]["current_state"]["status"], "after": review["after"]["current_state"]["status"],
                   "choice": review["choice"], "review_events": text, "promoted": promoted, "support_text": support,
                   "outcome": outcome, "final": final}
            reviews.append(row)
        previous_by_title = {}
        for i, s in enumerate(steps):
            before, after = s["before"], s["after"]
            key = node_key(before)
            event = before.get("current_event") or {}
            q = questions.setdefault(key, {"id": key, "event": event, "phase": s["phase"],
                "choices": before.get("choices"), "seen": 0, "answers": {}, "first_evidence": [r["run"], i]})
            q["seen"] += 1
            b = before["current_state"]["status"]
            a = after["current_state"]["status"]
            delta = {k: a[k] - v for k, v in b.items() if isinstance(v, (int, float)) and isinstance(a.get(k), (int, float))}
            choice_id = str(s["choice"]["choice"])
            ans = q["answers"].setdefault(choice_id, {"action": s["choice"]["action"], "count": 0, "delta_counts": {}, "successors": {}, "examples": [],
                "episode_outcomes": {}, "delayed_same_title": {}, "promotion_episodes": 0})
            ans["count"] += 1
            ans["episode_outcomes"][outcome] = ans["episode_outcomes"].get(outcome, 0) + 1
            ans["promotion_episodes"] += promoted
            later = next((z for z in steps[i + 1:] if z["before"].get("current_event", {}).get("title") == event.get("title")), None)
            if later and s["phase"] == "event":
                lk = node_key(later["before"])
                ans["delayed_same_title"][lk] = ans["delayed_same_title"].get(lk, 0) + 1
            dk = json.dumps(delta, sort_keys=True)
            ans["delta_counts"][dk] = ans["delta_counts"].get(dk, 0) + 1
            next_key = node_key(after)
            ans["successors"][next_key] = ans["successors"].get(next_key, 0) + 1
            if len(ans["examples"]) < 3:
                ans["examples"].append({"run": r["run"], "step": i, "before": b, "after": a,
                                        "month": before["current_state"]["time"]["current_month"]})
            edges[(key, choice_id, next_key, "observed_next_question")] += 1
            title = event.get("title")
            if s["phase"] == "event" and title in previous_by_title:
                prev_key, prev_choice = previous_by_title[title]
                edges[(prev_key, prev_choice, key, "same_title_later_possible_chain")] += 1
            if s["phase"] == "event":
                previous_by_title[title] = (key, choice_id)
            if b.get("level") == "L1":
                for k in ("skill", "network", "output"):
                    maxima[k] = max(maxima[k], b[k])
            if s["phase"] in ("energy", "main_action") and b.get("level") == a.get("level"):
                for stat, advertised in s["choice"].get("status_updates", {}).items():
                    if advertised > 0 and stat.lower() in delta:
                        effects.append({"run": r["run"], "step": i, "action": s["choice"]["action"], "level": b["level"],
                            "stat": stat, "before": b[stat.lower()], "advertised": advertised, "actual": delta[stat.lower()]})
    # Include unanswered alternatives explicitly: catalogue coverage is not state-tree coverage.
    for q in questions.values():
        q["untried_choices"] = [c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    summary = {"source": str(source), "runs": len(runs), "groups": {k: dict(v) for k, v in sorted(arms.items())},
        "failures": dict(failures), "question_nodes": len(questions),
        "story_nodes": sum(q["phase"] == "event" for q in questions.values()),
        "available_question_answers": sum(len(q["choices"]) for q in questions.values()),
        "tried_question_answers": sum(len(q["answers"]) for q in questions.values()),
        "story_available_answers": sum(len(q["choices"]) for q in questions.values() if q["phase"] == "event"),
        "story_tried_answers": sum(len(q["answers"]) for q in questions.values() if q["phase"] == "event"),
        "support_by_promotion": [{"support_text": s, "promotion": p, "count": n} for (s, p), n in sorted(support_table.items())],
        "observed_L1_maxima": dict(maxima),
        "limits": ["Unseeded sessions: no identical-state counterfactuals", "Visible question identity is not hidden-state identity",
                   "Edges record temporal succession, not proven causation", "Promotion is distinct from survival and performance grade",
                   "Effects at clock boundaries can include automatic settlement", "Coverage is empirical, not exhaustive"]}
    for name, obj in (("summary", summary), ("reviews", reviews), ("questions", list(questions.values())), ("quarterly-effects", effects)):
        (output / (name + ".json")).write_text(json.dumps(obj, indent=2, ensure_ascii=False))
    with (output / "observed-edges.csv").open("w") as f:
        writer = csv.writer(f)
        writer.writerow(["from_question", "answer", "to_question", "evidence_type", "count"])
        writer.writerows((*k, v) for k, v in sorted(edges.items()))
    # Lossless public-tool evidence, compact enough for the private research repo.
    archive = output / "public-trajectories.jsonl.gz"
    with gzip.open(archive, "wt", encoding="utf-8") as f:
        for r in runs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (output / "archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + "  " + archive.name + "\n")
    if (source / "manifest.json").exists():
        (output / "manifest.json").write_bytes((source / "manifest.json").read_bytes())
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    analyze(args.source, args.output)
