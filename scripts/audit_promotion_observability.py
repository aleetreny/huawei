"""Search public pre-review observations for conflicting promotion outcomes.

Observational collisions diagnose an insufficient description, not a hidden
variable's identity or a causal effect. Never reads simulator storage.
"""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def without_session(value):
    if isinstance(value, dict):
        return {k: without_session(v) for k, v in value.items() if k != "session_id"}
    if isinstance(value, list):
        return [without_session(v) for v in value]
    return value


def projections(step):
    before = without_session(step["before"])
    status = before["current_state"]["status"]
    choice = step["choice"]
    return {
        "growth_indicators_only": {k: status[k] for k in ("skill", "network", "output")},
        "status_only": status,
        "status_and_choice": [status, choice],
        "status_question_and_choice": [status, before.get("current_event"), before.get("choices"), choice],
        "full_observation_and_choice": [before, choice],
    }


def analyze(root, output):
    groups = defaultdict(dict)
    counts = Counter()
    archives = []
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        expected = (archive.parent / "archive-sha256.txt").read_text().split()[0]
        actual = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Archive integrity mismatch: {archive}")
        archives.append({"batch": archive.parent.name, "sha256": actual})
        with gzip.open(archive, "rt") as stream:
            for line in stream:
                record = json.loads(line)
                for index, step in enumerate(record["steps"]):
                    text = step["after"].get("events", "")
                    if "Half-year performance bonus" not in text:
                        continue
                    counts["review_transitions"] += 1
                    if not step.get("applied") or step.get("ambiguous"):
                        counts["excluded_unconfirmed_actions"] += 1
                        continue
                    before = step["before"]["current_state"]["status"]
                    after = step["after"]["current_state"]["status"]
                    promoted = int(after["level"][1:]) > int(before["level"][1:])
                    witness = {"batch": archive.parent.name, "run": record["run"], "step": index,
                        "promoted": promoted, "before_status": before,
                        "choice": step["choice"], "review_events": text,
                        "history_sha256": digest(without_session(record["steps"][:index]))}
                    for name, projection in projections(step).items():
                        key = digest(projection)
                        group = groups[name].setdefault(key, {"outcomes": Counter(), "witnesses": {}})
                        label = "promoted" if promoted else "not_promoted"
                        group["outcomes"][label] += 1
                        group["witnesses"].setdefault(label, witness)
    summary = {}
    for name, indexed in groups.items():
        repeated = [g for g in indexed.values() if sum(g["outcomes"].values()) > 1]
        mixed = [(key, g) for key, g in indexed.items() if len(g["outcomes"]) > 1]
        mixed.sort(key=lambda item: (-sum(item[1]["outcomes"].values()), item[0]))
        summary[name] = {"distinct_groups": len(indexed), "repeated_groups": len(repeated),
            "conflicting_groups": len(mixed),
            "observations_in_conflicting_groups": sum(sum(g["outcomes"].values()) for _, g in mixed),
            "conflicts": [{"projection_sha256": k, "counts": dict(g["outcomes"]),
                "witnesses": g["witnesses"]} for k, g in mixed]}
    result = {"counts": dict(counts), "archives": archives, "projections": summary,
        "interpretation": [
            "Same public observation and chosen action can still have different earlier histories or random outcomes.",
            "A collision refutes a deterministic formula of that projection alone on this sample.",
            "Absence of collisions does not prove sufficient observability or universal promotion.",
            "No identical-state cloning, randomised intervention or causal identification is claimed.",
            "Promotion is measured by the immediate public level change, not a later window outcome."]}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"counts": result["counts"], "projections": {
        k: {a: b for a, b in v.items() if a != "conflicts"} for k, v in summary.items()}}, indent=2))


if __name__ == "__main__":
    analyze(Path(sys.argv[1]), Path(sys.argv[2]))
