"""Analyze archived public note probes; no game or model calls."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sys


def analyze(root, out):
    out.mkdir(parents=True, exist_ok=True)
    totals = Counter()
    cases = defaultdict(Counter)
    missing = Counter()
    runs, witnesses, ages = [], [], []
    for path in sorted(root.glob("run*.json.gz")):
        with gzip.open(path, "rt") as stream:
            data = json.load(stream)
        r = data["result"]
        assert not r.get("fatal_error"), r.get("fatal_error")
        totals["games"] += 1
        totals["actions"] += len(r["actions"])
        totals["public_calls"] += len(data["public_calls"])
        totals["rejected"] += sum(a["success"] is not True for a in r["actions"])
        totals["tool_errors"] += len(r["technical_errors"])
        totals["restart_logs_equal"] += r["restart"]["logs_equal"]
        totals["restart_observation_equal"] += r["restart"]["observation_equal"]
        totals["unknown_session_rejected"] += "Unknown session_id" in str(r["unknown_session_logs"])
        last = r["checkpoints"][-1]["logs"]["1000"]["entries"]
        last_text = "\n".join(e["message"] for e in last)
        action_rows = []
        for a in r["actions"]:
            case = a["case"]
            key = f"{case['kind']}:{case['characters']}"
            cases[key]["attempted"] += 1
            cases[key]["accepted"] += a["success"] is True
            if case["characters"] < 64:
                cases[key]["non_unique_or_empty"] += 1
                continue
            tag = f"NOTE_PROBE_r{r['run']:02d}_s{a['step']:03d}|"
            matched = [e["message"] for e in last if tag in e["message"]]
            actual = matched[0].split("\nNotes: ", 1)[-1] if matched else None
            expected = case["text"] if len(case["text"]) <= 1000 else case["text"][:997] + "..."
            outcome = "missing" if actual is None else "exact" if actual == case["text"] else "truncated_as_prefix997_plus_ellipsis" if actual == expected else "other_transformation"
            cases[key][outcome] += 1
            if outcome == "missing":
                missing[f"{a['phase']}:{a['action']}"] += 1
            if actual is not None:
                assert len(matched) == 1
                ages.append(len(r["actions"]) - 1 - a["step"])
            if outcome == "other_transformation":
                witnesses.append({"run": r["run"], "step": a["step"], "outcome": outcome, "expected": expected, "actual": actual})
            action_rows.append({"step": a["step"], "phase": a["phase"], "action": a["action"], "case": key,
                                "returned_characters": len(actual) if actual is not None else None, "outcome": outcome})
        for cp in r["checkpoints"]:
            full = cp["logs"]["1000"]["entries"]
            for count, logs in cp["logs"].items():
                entries = logs.get("entries", [])
                totals["log_count_checks"] += 1
                totals["suffix_order_matches"] += entries == full[-max(1, int(count)):]
            latest_noted = [e for e in full if "\nNotes: " in e["message"]]
            if latest_noted:
                totals["latest_note_checks"] += 1
                for count in (1, 2, 5, 10):
                    totals[f"latest_note_recovered_count{count}"] += latest_noted[-1] in cp["logs"][str(count)]["entries"]
        assert not any(f"NOTE_PROBE_r{other:02d}_" in last_text for other in range(12) if other != r["run"])
        totals["no_other_run_marker"] += 1
        runs.append({"run": r["run"], "actions": len(r["actions"]), "month": r["ending"]["current_state"]["time"]["current_month"],
                     "terminal": bool(r["ending"].get("ending_score")), "log_entries": len(last), "action_audit": action_rows})
        shutil.copyfile(path, out / path.name)
    summary = {"totals": dict(totals), "cases": {k: dict(v) for k, v in cases.items()}, "missing_by_action": dict(missing),
               "max_verified_note_age_in_later_actions": max(ages), "month_range": [min(r['month'] for r in runs), max(r['month'] for r in runs)],
               "unexpected_transformations": witnesses, "runs": runs,
               "limitations": ["No LLM learning or compaction measured", "No timed expiry claim", "Short/empty notes not uniquely attributable",
                               "Independent games; no causal promotion or note-semantics claim", "Latest note checks concern any recorded note, not necessarily a full ledger"]}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    shutil.copyfile(root / "protocol.json", out / "protocol.json")
    (out / "archive-sha256.json").write_text(json.dumps({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('run*.gz'))}, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != 'runs'}, indent=2))


if __name__ == "__main__":
    analyze(Path(sys.argv[1]), Path(sys.argv[2]))
