"""Merge batch catalogues; preserve provenance and mark unanswered branches."""
from collections import Counter
import json
from pathlib import Path
import sys


def catalog(root):
    questions = {}
    summaries = {}
    for batch in sorted(root.iterdir()):
        if not (batch / "questions.json").exists():
            continue
        summaries[batch.name] = json.loads((batch / "summary.json").read_text())
        for source in json.loads((batch / "questions.json").read_text()):
            key = source["id"]
            q = questions.setdefault(key, {"id": key, "event": source["event"], "phase": source["phase"],
                "choices": source["choices"], "seen": 0, "answers": {}, "batches": {}})
            q["seen"] += source["seen"]
            q["batches"][batch.name] = source["seen"]
            for number, ans in source["answers"].items():
                a = q["answers"].setdefault(number, {"action": ans["action"], "count": 0, "delta_counts": {}, "successors": {},
                    "delayed_same_title": {}, "episode_outcomes": {}, "promotion_episodes": 0, "examples": []})
                for field in ("count", "promotion_episodes"):
                    a[field] += ans[field]
                for field in ("delta_counts", "successors", "delayed_same_title", "episode_outcomes"):
                    a[field] = dict(Counter(a[field]) + Counter(ans[field]))
                a["examples"].extend({**x, "batch": batch.name} for x in ans["examples"][:1])
    ordered = sorted(questions.values(), key=lambda q: (q["phase"] != "event", q["event"].get("title", ""), q["id"]))
    for q in ordered:
        q["untried_choices"] = [c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    (root / "questions.json").write_text(json.dumps(ordered, ensure_ascii=False, indent=2))
    lines = ["# Observed question and answer catalogue", "", "Development evidence only. Each node identifies visible question text and options, not a complete hidden state. A recorded transition is temporal evidence. Same-title later stages are possible narrative chains, not matched counterfactuals. Delta averages include settlement, clipping, and delayed effects. Episode outcomes are associations, not action treatment effects.", "",
        "All raw before/after observations, alternatives and logs are preserved in the batch public-trajectories.jsonl.gz archives. Evidence IDs below use batch/run/step. Untried options are explicit. This does not enumerate unseen scenarios or the full six-month history tree.", ""]
    for q in ordered:
        lines += [f"## {q['event'].get('title', '?')} — {q['id']}", "", f"Phase: {q['phase']}; seen {q['seen']} times.", "", q["event"].get("description", ""), ""]
        for c in q["choices"]:
            a = q["answers"].get(str(c["choice"]))
            lines += [f"### Answer {c['choice']}: {c.get('action', '')}", ""]
            if a is None:
                lines += ["**Not tried.**", ""]
                continue
            means = Counter()
            for encoded, count in a["delta_counts"].items():
                for k, v in json.loads(encoded).items():
                    means[k] += v * count
            delta = ", ".join(f"{k} {v / a['count']:+.2f}" for k, v in sorted(means.items()) if v)
            lines += [f"Observed {a['count']} times. Mean immediate state change: {delta or 'no net mean change'}. These are mixed contexts.", "",
                "Later same-title questions: " + (", ".join(f"{k} ({v})" for k, v in sorted(a["delayed_same_title"].items())) or "none observed") + ".", "",
                "Examples: " + ", ".join(f"{x['batch']}/{x['run']}/{x['step']}" for x in a["examples"]) + ".", ""]
    (root / "catalogue.md").write_text("\n".join(lines))
    overview = {"batches": {k: v["groups"]["all"] for k, v in summaries.items()},
        "runs": sum(v["runs"] for v in summaries.values()), "nodes": len(ordered),
        "story_nodes": sum(q["phase"] == "event" for q in ordered),
        "available_answers": sum(len(q["choices"]) for q in ordered),
        "tried_answers": sum(len(q["answers"]) for q in ordered),
        "story_available_answers": sum(len(q["choices"]) for q in ordered if q["phase"] == "event"),
        "story_tried_answers": sum(len(q["answers"]) for q in ordered if q["phase"] == "event"),
        "untried": [{"question": q["id"], "title": q["event"].get("title"), "choices": q["untried_choices"]} for q in ordered if q["untried_choices"]]}
    (root / "overview.json").write_text(json.dumps(overview, indent=2))
    print(json.dumps(overview, indent=2))


if __name__ == "__main__":
    catalog(Path(sys.argv[1]))
