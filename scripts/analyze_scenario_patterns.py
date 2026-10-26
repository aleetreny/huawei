"""Summarise public six-month evidence without treating post-review state as causal inputs."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.first_review_search import node_key


def growth_ready(status):
    # Descriptive proxy inherited from earlier exploratory analysis, not a game formula.
    return status["skill"] >= 8 and status["network"] >= 3 and status["output"] >= 3


def analyze(root, output):
    mapping = json.loads((output / "taxonomy.json").read_text())["title_to_group"]
    questions = json.loads((root / "questions.json").read_text())
    titles = {q["event"]["title"] for q in questions if q["phase"] == "event"}
    if set(mapping) != titles:
        raise ValueError("Taxonomy must explicitly cover the exact current title set")
    group_counts = defaultdict(Counter)
    title_months = defaultdict(Counter)
    title_stages = Counter()
    for title in titles:
        group_counts[mapping[title]]["titles"] += 1
    for q in questions:
        if q["phase"] == "event":
            group = group_counts[mapping[q["event"]["title"]]]
            group["stages"] += 1
            group["answers"] += len(q["choices"])
            title_stages[q["event"]["title"]] += 1
    raw = Counter()
    failures = Counter()
    common_early_titles = None
    before_proxy = defaultdict(lambda: defaultdict(Counter))
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        for line in gzip.open(archive, "rt"):
            r = json.loads(line)
            raw["records"] += 1
            raw[r["outcome"]] += 1
            if r["outcome"] == "eliminated":
                failures[r["final"]["current_state"]["simulation_flags"].get("failure_reason", "unknown")] += 1
            raw["promotion"] += bool(r.get("promoted"))
            raw["promotion_and_alive"] += bool(r.get("promoted")) and r["outcome"] == "six_month_window"
            if r.get("promoted"):
                early = {s["before"]["current_event"]["title"] for s in r["steps"]
                         if s["phase"] == "event" and s["before"]["current_state"]["time"]["current_month"] < 6}
                common_early_titles = early if common_early_titles is None else common_early_titles & early
            for s in r["steps"]:
                if s["phase"] == "event":
                    obs = s["before"]
                    title_months[obs["current_event"]["title"]][obs["current_state"]["time"]["current_month"]] += 1
            if r["outcome"] != "interrupted":
                for month in (4, 5):
                    first = next((s["before"] for s in r["steps"] if s["before"]["current_state"]["time"]["current_month"] == month), None)
                    if first:
                        ready = growth_ready(first["current_state"]["status"])
                        prefix = f"{archive.parent.name}/month-{month}"
                        before_proxy[prefix]["ready" if ready else "gap"]["n"] += 1
                        before_proxy[prefix]["ready" if ready else "gap"]["promoted"] += bool(r.get("promoted"))
    only_after = sorted(t for t, months in title_months.items() if min(months) >= 6)
    for title in titles:
        group_counts[mapping[title]]["before_review_titles"] += title not in only_after
        group_counts[mapping[title]]["only_after_review_titles"] += title in only_after
    reviews = []
    for path in sorted(root.glob("*/reviews.json")):
        reviews.extend(dict(r, batch=path.parent.name) for r in json.loads(path.read_text()))
    clean_table = defaultdict(Counter)
    errors, clean_promotions, clean_n = [], 0, 0
    grades, clock = Counter(), Counter()
    for r in reviews:
        text = r["review_events"]
        grades[text.split("Half-year performance bonus (")[1].split(")")[0]] += 1
        clock[f"{r['before_time']['current_month']}->{r['after_time']['current_month']}"] += 1
        if any(word in text for word in ("Old landmines", "Trust crisis")):
            continue
        clean_n += 1
        clean_promotions += r["promoted"]
        status = r["after"]
        ready = growth_ready(status)
        label = ("growth_ready" if ready else "growth_gap") + ("/D>=2" if status["dignity"] >= 2 else "/D<2")
        clean_table[label]["n"] += 1
        clean_table[label]["promoted"] += r["promoted"]
        prediction = ready and status["dignity"] >= 2
        if prediction != r["promoted"]:
            errors.append(r)
    stalls = Counter()
    for path in root.glob("*/quarterly-effects.json"):
        for effect in json.loads(path.read_text()):
            if effect["level"] == "L1" and effect["advertised"] > 0 and effect["actual"] == 0:
                stalls[f"{effect['stat']}@{effect['before']}"] += 1
    stats = {"records": dict(raw), "failures": dict(failures), "groups": {g: dict(c) for g, c in sorted(group_counts.items())},
        "grouping_is_interpretive": True, "title_count": len(titles),
        "specific_early_story_titles_common_to_all_promotions": sorted(common_early_titles or []),
        "multistage_titles": sum(n > 1 for n in title_stages.values()),
        "only_observed_after_first_review": only_after, "title_month_counts": {t: dict(v) for t, v in sorted(title_months.items())},
        "review_count": len(reviews), "grades": dict(grades), "clock": dict(clock),
        "clean_review_count": clean_n, "clean_promotions": clean_promotions,
        "clean_post_transition_table": {k: dict(v) for k, v in sorted(clean_table.items())},
        "previous_separator_counterexamples": errors,
        "pre_review_proxy": {k: {g: dict(c) for g, c in v.items()} for k, v in sorted(before_proxy.items())},
        "unrealised_positive_quarterly_investments_L1": dict(stalls),
        "limits": ["Post-transition values are not exact review inputs", "Clear simultaneous risk messages excluded only for descriptive separator audit",
            "Pre-review groups are observational, not randomised readiness interventions", "Adaptive closure runs deliberately change state exposure",
            "Story occurrence may follow promotion rather than cause it", "No general-agent transfer result is available"]}
    (output / "statistics.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in stats.items() if k not in ("title_month_counts", "previous_separator_counterexamples", "pre_review_proxy")}, indent=2))


if __name__ == "__main__":
    analyze(Path(sys.argv[1]), Path(sys.argv[2]))
