"""Independently witness every known answer in lossless public-tool archives."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.first_review_search import node_key


def audit(root, output):
    catalogue = json.loads((root / "questions.json").read_text())
    required = {(q["id"], c["choice"]) for q in catalogue for c in q["choices"]}
    story_required = {(q["id"], c["choice"]) for q in catalogue if q["phase"] == "event" for c in q["choices"]}
    evidence, archives, records, failures = {}, [], 0, []
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        expected = (archive.parent / "archive-sha256.txt").read_text().split()[0]
        actual = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Hash mismatch: {archive}")
        count = 0
        with gzip.open(archive, "rt") as stream:
            for line in stream:
                r = json.loads(line)
                count += 1
                records += 1
                for step, s in enumerate(r["steps"]):
                    before = s["before"]
                    pair = node_key(before), s["choice"]["choice"]
                    # An offered option or attempted/rejected action is not execution.
                    success = s.get("applied") is True and s.get("reply", {}).get("success") is True and not s.get("ambiguous", False)
                    within = 1 <= before["current_state"]["time"]["current_month"] <= 6
                    if pair in required and pair not in evidence and success and within:
                        evidence[pair] = {"question": pair[0], "answer": pair[1], "batch": archive.parent.name,
                            "run": r["run"], "step": step, "month": before["current_state"]["time"]["current_month"],
                            "action": s["choice"]["action"], "before": before["current_state"]["status"],
                            "after": s["after"]["current_state"]["status"], "reply": s["reply"]}
        archives.append({"batch": archive.parent.name, "records": count, "sha256": actual})
    missing = [{"question": q, "answer": c} for q, c in sorted(required - set(evidence))]
    result = {"complete": not missing, "scope": "Every displayed answer of every question encountered within the six-month catalogue; not all hidden-state histories",
        "catalogue_sha256": hashlib.sha256((root / "questions.json").read_bytes()).hexdigest(),
        "required_pairs": len(required), "witnessed_pairs": len(evidence),
        "required_story_pairs": len(story_required), "witnessed_story_pairs": len(story_required & set(evidence)),
        "records_checked": records, "archives": archives, "missing": missing,
        "witnesses": [evidence[k] for k in sorted(evidence)]}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in result.items() if k not in ("witnesses", "archives")}, indent=2))
    if missing:
        raise RuntimeError("Known catalogue has no successful witness for some answers")
    return result


if __name__ == "__main__":
    audit(Path(sys.argv[1]), Path(sys.argv[2]))
