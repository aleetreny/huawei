"""Append one reproducible historical exploration cycle; never launches games.

Example: uv run python scripts/explore_decisions.py --cycle 001
  --runs-root ~/careerlab-data/huawei/runs
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np

from careerlab.decision_models import bootstrap_difference, nested_predictions
from careerlab.decision_research import build_episode, ending_losses, extract_streams
from scripts.decision_research_audit import audit, decoded, records, sha256


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_jsonl(path, rows):
    content = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n" for row in rows)
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(content.encode(), mtime=0))
    else:
        path.write_text(content)


def analyse(episodes, spec):
    primary = [e for e in episodes if e["actor_id"] == spec["primary_actor_id"] and e["quality_for_prediction"]]
    cells = Counter(e["env_id"] for e in primary)
    # Avoid silently choosing an environment by its outcomes or mixing epochs.
    if len(cells) > 1:
        raise ValueError("Multiple primary-actor environments; freeze an environment restriction in the spec first")
    result = {"primary_actor": spec["primary_actor_id"], "primary_verified_quality_n": len(primary),
              "landmark_associations": {}, "models": [], "prediction_population": spec["prediction_population"]}
    predictions = []
    for month in spec["landmarks"]:
        key = str(month)
        rows = [e for e in primary if key in e["landmarks"]]
        tagged = [{**e, "promoted": (e["landmarks"][key]["level"] or 0) > 1} for e in rows]
        result["landmark_associations"][key] = {
            "n": len(rows), "missing_or_not_active": len(primary) - len(rows),
            "promotion": bootstrap_difference(tagged, "promoted", spec["seed"] + month),
            "feature_support": {},
        }
        for feature in spec["state_features"] + spec["behaviour_features"]:
            supported = [e for e in rows if feature in spec["state_features"] or e["landmarks"][key]["behaviour_prefix_complete"]]
            values = [e["landmarks"][key][feature] for e in supported if e["landmarks"][key].get(feature) is not None]
            result["landmark_associations"][key]["feature_support"][feature] = {
                "eligible": len(supported), "observed": len(values), "distinct_values": len(set(values)),
                "min": min(values, default=None), "max": max(values, default=None),
            }
        sets = {"state": spec["state_features"], "behaviour": spec["behaviour_features"],
                "state_and_behaviour": spec["state_features"] + spec["behaviour_features"]}
        for split in ("policy_id", "family"):
            for model_name in spec["models"] + ["state_on_behaviour_cohort"]:
                features = sets["state" if model_name == "state_on_behaviour_cohort" else model_name]
                cohort = rows if model_name == "state" else [e for e in rows if e["landmarks"][key]["behaviour_prefix_complete"]]
                X = [[e["landmarks"][key].get(f) for f in features] for e in cohort]
                fitted = nested_predictions(X, [e["Q"] for e in cohort], [e[split] for e in cohort], spec)
                entry = {"landmark": month, "split": split, "model": model_name, "features": features,
                         "cohort": "all_fresh_states" if model_name == "state" else "complete_behaviour_prefix", **fitted}
                if fitted["status"] == "ok":
                    for i, e in enumerate(cohort):
                        predictions.append({"job_id": e["job_id"], "policy_id": e["policy_id"], "family": e["family"],
                                            "landmark": month, "split": split, "model": model_name, "Q": e["Q"],
                                            "predicted_Q": fitted["prediction"][i], "baseline_Q": fitted["baseline_prediction"][i],
                                            "fold": fitted["fold_ids"][i]})
                    for field in ("prediction", "baseline_prediction", "fold_ids"):
                        entry.pop(field)
                result["models"].append(entry)
    completed = [e for e in primary if e["completed"] and e.get("ending_losses")]
    result["completed_score_gap"] = {
        "n": len(completed), "population": "Verified local primary actor completed games only; descriptive accounting",
        "mean_missing_Q": float(np.mean([100 - e["Q"] for e in completed])) if completed else None,
        "mean_loss_by_dimension": {d: float(np.mean([e["ending_losses"][d] for e in completed if d in e["ending_losses"]])) for d in sorted({d for e in completed for d in e["ending_losses"]})},
    }
    whole_behaviour = [e for e in primary if e["whole_game_behaviour_complete"]]
    result["whole_game_behaviour_support_descriptive_only"] = {
        "episodes_with_complete_behaviour": len(whole_behaviour),
        "main_actions_in_complete_episodes": sum(e["behaviour_whole_game_descriptive_only"]["prior_main_actions"] for e in whole_behaviour),
        "episodes_with_any_non_project_main_in_complete_episodes": sum((e["behaviour_whole_game_descriptive_only"]["growth_share"] or 0) < 1 for e in whole_behaviour),
        "story_transitions_same_month": sum(e["same_month_story_transitions"] for e in primary),
        "story_transitions_with_output_or_network_drop": sum(e["same_month_story_output_or_network_drop"] for e in primary),
    }
    return result, predictions


def render_tables(coverage, analysis):
    lines = ["# Tablas reproducibles del ciclo", "", "Exploración histórica. Ningún coeficiente ni diferencia identifica un efecto causal.", "",
             f"Terminales Claude elegibles: {coverage['eligible_terminal_claude']}; trazas extraídas: {coverage['extracted']}; actor primario con calidad: {analysis['primary_verified_quality_n']}.", "",
             "## Estado temprano y resultado posterior", "", "Población condicionada a seguir activo y tener una observación válida en ese mes.", "",
             "| Mes | Promovido | n | Completan | Q media |", "|---|---|---:|---:|---:|"]
    for month, entry in analysis["landmark_associations"].items():
        for group in entry["promotion"].get("groups", []):
            lines.append(f"| {month} | {'sí' if group['promoted'] else 'no'} | {group['n']} | {group['completed']} | {group['mean_Q']:.2f} |")
    lines += ["", "## Predicción de Q fuera de muestra", "", "Ridge con ajuste de penalización e imputación/escalado sólo dentro del entrenamiento. Error menor es mejor.", "",
              "| Mes | Grupo reservado | Modelo | n | RMSE | RMSE media de entrenamiento | MAE |", "|---|---|---|---:|---:|---:|---:|"]
    for m in analysis["models"]:
        if m["status"] == "ok":
            lines.append(f"| {m['landmark']} | {m['split']} | {m['model']} | {m['n']} | {m['rmse']:.2f} | {m['baseline_rmse']:.2f} | {m['mae']:.2f} |")
        else:
            lines.append(f"| {m['landmark']} | {m['split']} | {m['model']} | {m['n']} | {m['status']} | — | — |")
    lines += ["", "## Puntos ausentes entre carreras completadas del actor primario", "", f"n = {analysis['completed_score_gap']['n']}. Descomposición del score, no efectos de acciones.", "",
              "| Dimensión | Puntos Q ausentes, media |", "|---|---:|"]
    for d, value in analysis["completed_score_gap"]["mean_loss_by_dimension"].items():
        lines.append(f"| {d} | {value:.2f} |")
    lines += ["", "Los meses son puntos de análisis retrospectivo y no reglas de calendario para las Skills. Predicción interna no equivale a validación prospectiva ni a transferencia a DeepSeek."]
    return "\n".join(lines) + "\n"


def cycle_lineage(output: Path, episodes: list[dict], input_hashes: dict) -> dict:
    prior = sorted(p for p in output.parent.glob("[0-9][0-9][0-9]") if p.name < output.name and (p / "manifest.json").is_file())
    if not prior:
        return {"previous_cycle": None, "new_extracted_games": len(episodes), "reused_extracted_games": 0,
                "note": "First extraction here; these are historical games, not fresh confirmation."}
    previous = prior[-1]
    old = {r["job_id"]: r for r in records(previous / "episodes.jsonl")}
    new = {r["job_id"]: r for r in episodes}
    old_manifest = json.loads((previous / "manifest.json").read_text())
    return {"previous_cycle": previous.name, "previous_manifest_sha256": sha256(previous / "manifest.json"),
            "new_extracted_games": len(new.keys() - old.keys()), "reused_extracted_games": len(new.keys() & old.keys()),
            "removed_extracted_games": len(old.keys() - new.keys()),
            "changed_existing_episode_rows": sum(old[k] != new[k] for k in new.keys() & old.keys()),
            "same_export_hashes": old_manifest["input_hashes"] == input_hashes,
            "note": "Reanalysis of the same games is not additional independent evidence. New availability of an old trace is not a new launch."}


def run(export_dir: Path, runs_root: Path, spec_path: Path, output: Path) -> dict:
    if output.exists():
        raise ValueError(f"Immutable cycle already exists: {output}; choose a new cycle")
    spec = json.loads(spec_path.read_text())
    inventory = audit(export_dir, runs_root)
    policies = {r["policy_id"]: r for r in records(export_dir / "policies.jsonl")}
    actors = {r["actor_id"]: r for r in records(export_dir / "actors.jsonl")}
    jobs = {r["job_id"]: r for r in records(export_dir / "jobs.jsonl")}
    evaluations = records(export_dir / "evaluations.jsonl")
    episodes, action_rows, observation_rows = [], [], []
    coverage = {"excluded_by_purpose": dict(Counter(r["purpose"] for r in evaluations if r["purpose"] not in spec["allowed_purposes"])),
                "eligible_terminal_claude": 0, "extracted": 0, "trace_status": {}, "by_actor": {}}
    status_counts, actor_coverage = Counter(), defaultdict(Counter)
    manifests = {}
    for row in evaluations:
        if row["purpose"] not in spec["allowed_purposes"] or row["outcome"] not in {"completed", "eliminated"} or actors[row["actor_id"]]["kind"] != "claude-cli":
            continue
        coverage["eligible_terminal_claude"] += 1
        trace = inventory["traces"][row["job_id"]]
        status_counts[trace["status"]] += 1
        actor_coverage[row["actor_id"]]["eligible"] += 1
        if trace["status"] != "primary_hash_verified":
            continue
        run_dir = runs_root / row["job_id"]
        if Path(row["trajectory_path"]).name != "stream-0.jsonl":
            raise ValueError("Expected Claude stream transcript")
        paths = [run_dir / item["name"] for item in trace["files"]]
        actions, observations, diagnostics = extract_streams(paths)
        episode = build_episode(row, policies[row["policy_id"]], actions, observations, diagnostics, spec["landmarks"])
        episode["origin"] = jobs[row["job_id"]].get("origin") or "canonical"
        episode["epoch"] = jobs[row["job_id"]].get("epoch", "unknown")
        episode["ending_losses"] = ending_losses(run_dir / "result.json", row)
        manifests[row["job_id"]] = {"streams": trace["files"], "result_sha256": sha256(run_dir / "result.json") if (run_dir / "result.json").exists() else None}
        episodes.append(episode)
        actor_coverage[row["actor_id"]]["extracted"] += 1
        actor_coverage[row["actor_id"]]["quality_for_prediction"] += bool(episode["quality_for_prediction"])
        action_rows.extend({"job_id": row["job_id"], **r} for r in actions)
        observation_rows.extend({"job_id": row["job_id"], **r} for r in observations)
    coverage.update(extracted=len(episodes), trace_status=dict(status_counts), by_actor={key: dict(value) for key, value in actor_coverage.items()})
    analysis, predictions = analyse(episodes, spec)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".building-", dir=output.parent) as tmp:
        stage = Path(tmp)
        write_json(stage / "coverage.json", coverage)
        write_json(stage / "analysis.json", analysis)
        write_jsonl(stage / "episodes.jsonl", episodes)
        write_jsonl(stage / "predictions.jsonl", predictions)
        write_jsonl(stage / "actions.jsonl.gz", action_rows)
        write_jsonl(stage / "observations.jsonl.gz", observation_rows)
        (stage / "tables.md").write_text(render_tables(coverage, analysis))
        sources = [ROOT / "careerlab/decision_research.py", ROOT / "careerlab/decision_models.py", ROOT / "scripts/explore_decisions.py", ROOT / "scripts/decision_research_audit.py"]
        manifest = {"schema": 1, "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "spec": spec, "spec_sha256": sha256(spec_path), "input_hashes": inventory["input_hashes"],
                    "code_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in sources},
                    "trajectory_sources": manifests, "artifact_hashes": {p.name: sha256(p) for p in stage.iterdir()},
                    "lineage": cycle_lineage(output, episodes, inventory["input_hashes"]),
                    "limitations": inventory["limitations"] + ["Unknown epochs stay unknown; no causal pooling or target transfer claim.", "Historical internal validation may reflect earlier adaptive policy design; future confirmation remains separate."]}
        write_json(stage / "manifest.json", manifest)
        stage.rename(output)
    return {"output": str(output), "coverage": coverage, "primary_quality_n": analysis["primary_verified_quality_n"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True)
    parser.add_argument("--export-dir", type=Path, default=ROOT / "lab/registry")
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--spec", type=Path, default=ROOT / "research/careerlab/decision-research/exploration-v1.json")
    parser.add_argument("--output-root", type=Path, default=ROOT / "lab/reports/decision-research/cycles")
    args = parser.parse_args()
    if not re.fullmatch(r"\d{3}", args.cycle):
        parser.error("--cycle must have three digits, e.g. 001")
    print(json.dumps(run(args.export_dir, args.runs_root, args.spec, args.output_root / args.cycle), sort_keys=True))


if __name__ == "__main__":
    main()
