"""Read-only inventory for decision research; never imports or starts the game.

Only exported lab records and saved official replies are read. No causal effects
or policy rankings are estimated. Missing trajectories never become zero-valued
behaviour. Run with --help for explicit, portable trajectory mappings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"Expected objects: {path}")
    return rows


def decoded(value):
    return json.loads(value) if isinstance(value, str) else value


def trace_info(row: dict, runs_root: Path | None) -> dict:
    """Inspect the registered file, then inventory continuations without exporting text.

    runs_root is the directory containing job directories, supplied explicitly.
    Never guess a cloud pathname on the Mac or search engine/database directories.
    """
    if runs_root is None:
        return {"status": "not_checked"}
    filename = Path(row.get("trajectory_path") or "").name
    # Only these two public transcript formats are supported. No arbitrary paths.
    if filename not in {"stream-0.jsonl", "trajectory.jsonl"}:
        return {"status": "unsupported_path"}
    job_id = row["job_id"]
    if Path(job_id).name != job_id or job_id in {".", ".."}:
        raise ValueError("Unsafe job_id")
    primary = runs_root / job_id / filename
    if not primary.is_file():
        return {"status": "missing"}
    expected = row.get("trajectory_sha256")
    if not expected:
        return {"status": "unregistered_hash"}
    if sha256(primary) != expected:
        return {"status": "hash_mismatch"}
    streams = [primary]
    if filename == "stream-0.jsonl":
        streams = sorted(primary.parent.glob("stream-*.jsonl"), key=lambda p: int(p.stem.split("-")[1]))
    months: set[int] = set()
    observations = 0
    actions = 0
    try:
        for stream in streams:
            pending: dict[str, str] = {}
            for line in stream.read_text().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                obs = None
                if filename == "trajectory.jsonl":
                    if entry.get("kind") == "obs":
                        obs = entry.get("obs")
                    elif entry.get("kind") == "act":
                        actions += 1
                else:
                    content = (entry.get("message") or {}).get("content")
                    for block in content if isinstance(content, list) else []:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use":
                            pending[block["id"]] = block["name"].split("__")[-1]
                            actions += pending[block["id"]] == "take_action"
                        elif block.get("type") == "tool_result":
                            name = pending.pop(block.get("tool_use_id"), None)
                            if name != "observe":
                                continue
                            text = block.get("content")
                            if isinstance(text, list):
                                text = "".join(b.get("text", "") for b in text if isinstance(b, dict))
                            try:
                                candidate = json.loads(text)
                            except (ValueError, TypeError):
                                continue
                            if isinstance(candidate, dict):
                                # There should be a single observe result per entry.
                                # Count here, since a message may contain several results.
                                state = candidate.get("current_state") or {}
                                month = (state.get("time") or {}).get("current_month")
                                if isinstance(month, int) and isinstance(state.get("status"), dict):
                                    observations += 1
                                    months.add(month)
                if isinstance(obs, dict):
                    state = obs.get("current_state") or {}
                    month = (state.get("time") or {}).get("current_month")
                    if isinstance(month, int) and isinstance(state.get("status"), dict):
                        observations += 1
                        months.add(month)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return {"status": "malformed", "error_type": type(exc).__name__}
    return {
        "status": "primary_hash_verified",
        "observations": observations,
        "action_attempts": actions,
        "observed_months": len(months),
        "min_month": min(months) if months else None,
        "max_month": max(months) if months else None,
        "files": [{"name": p.name, "sha256": sha256(p), "registry_hash_covers_file": p == primary} for p in streams],
    }


def audit(export_dir: Path, runs_root: Path | None = None) -> dict:
    tables = {name: records(export_dir / f"{name}.jsonl") for name in ("evaluations", "jobs", "actors", "environments", "policies")}
    actors = {row["actor_id"]: row for row in tables["actors"]}
    environments = {row["env_id"] for row in tables["environments"]}
    policies = {row["policy_id"] for row in tables["policies"]}
    jobs = {row["job_id"]: row for row in tables["jobs"]}
    if len(jobs) != len(tables["jobs"]):
        raise ValueError("Duplicate job ids in jobs export")
    seen = set()
    resolved_slots = set()
    groups = defaultdict(list)
    traces = {}
    valid_rows = []
    for row in tables["evaluations"]:
        job_id = row["job_id"]
        if job_id in seen:
            raise ValueError(f"Duplicate evaluation: {job_id}")
        seen.add(job_id)
        job = jobs[job_id]
        actor = actors[row["actor_id"]]
        if row["env_id"] not in environments or row["policy_id"] not in policies:
            raise ValueError(f"Unknown environment or policy: {job_id}")
        for key in ("actor_id", "env_id", "policy_id", "purpose"):
            if job[key] != row[key]:
                raise ValueError(f"Job/evaluation mismatch: {job_id}/{key}")
        if row["outcome"] not in {"completed", "eliminated"}:
            continue
        if bool(row.get("completed")) != (row["outcome"] == "completed"):
            raise ValueError(f"Inconsistent terminal outcome: {job_id}")
        score = row.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 100:
            raise ValueError(f"Invalid terminal score: {job_id}")
        slot = tuple(job.get(key) for key in ("origin", "policy_id", "actor_id", "env_id", "purpose", "replicate"))
        if slot in resolved_slots:
            raise ValueError(f"Two scored attempts in one logical slot: {job_id}")
        resolved_slots.add(slot)
        valid_rows.append(row)
        key = (row["actor_id"], row["env_id"])
        groups[key].append(row)
        if actor["kind"] != "scripted":
            traces[job_id] = trace_info(row, runs_root)
    summaries = []
    for (aid, eid), rows in sorted(groups.items()):
        actor = actors[aid]
        cfg = decoded(actor["config"])
        summaries.append({
            "actor_id": aid, "env_id": eid, "kind": actor["kind"], "model": cfg.get("model"),
            "effort": cfg.get("effort"), "autocompact": cfg.get("autocompact"),
            "n": len(rows), "completed": sum(bool(r["completed"]) for r in rows),
            "policies": len({r["policy_id"] for r in rows}),
            "mean_Q_descriptive": round(sum(r["score"] for r in rows) / len(rows), 3),
        })
    job_status = Counter(j["status"] for j in tables["jobs"] if j["job_id"] not in seen)
    return {
        "scope": "Historical discovery audit; no causal estimates or selection decisions",
        "input_hashes": {name: sha256(export_dir / f"{name}.jsonl") for name in tables},
        "evaluations": len(tables["evaluations"]), "terminal": len(valid_rows),
        "outcomes": dict(sorted(Counter(r["outcome"] for r in tables["evaluations"]).items())),
        "jobs_without_evaluation_by_status": dict(sorted(job_status.items())),
        "actor_environment_summaries": summaries,
        "missing_job_metadata": {key: sum(j.get(key) is None for j in tables["jobs"]) for key in ("epoch", "block_id", "analysis_role", "assignment_probability")},
        "trace_status_counts_non_scripted_terminal": dict(sorted(Counter(t["status"] for t in traces.values()).items())),
        "traces": traces,
        "limitations": [
            "Terminal rows are retrospective discovery only, not prefix-complete selection or confirmation.",
            "Trace availability is machine-specific; never restrict causal comparisons to available traces.",
            "A registered hash authenticates the primary file only; continuation hashes are an audit snapshot.",
            "Observation counts do not establish complete state/action alignment, compliance, or randomisation.",
            "No historical assignment probabilities are inferred; cells with unknown epochs cannot support causal pooling.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-dir", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path, help="Explicit directory containing this export's job directories; omitted means not_checked")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.export_dir, args.runs_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("evaluations", "terminal", "outcomes", "trace_status_counts_non_scripted_terminal")}, sort_keys=True))


if __name__ == "__main__":
    main()
