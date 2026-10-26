"""Report the isolated LLM block without scoring pending/interrupted slots as zero."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sys

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from careerlab.mcp_client import phase


def analyze(root, output):
    output.mkdir(parents=True, exist_ok=True)
    protocol = json.loads((root / "protocol.json").read_text())
    results = [json.loads(p.read_text()) for p in sorted((root / "runs").glob("*/result.json"))]
    groups = {}
    traces = []
    for r in results:
        arm = r["arm"]
        group = groups.setdefault(arm, {"attempted_slots": 0, "resolved": 0, "interrupted": 0,
            "promotion": 0, "alive_through_month_6": 0, "promotion_and_alive": 0})
        group["attempted_slots"] += 1
        if r["outcome"] == "interrupted":
            group["interrupted"] += 1
        else:
            group["resolved"] += 1
            for field in ("promotion", "alive_through_month_6", "promotion_and_alive"):
                group[field] += bool(r[field])
        run = root / "runs" / f"pair-{r['pair']:02d}-{arm}"
        events = [json.loads(line) for line in (run / "public-tools.jsonl").read_text().splitlines()]
        actions = [e for e in events if e["tool"] == "take_action"]
        applied = [e for e in actions if e.get("applied")]
        r["adherence"] = {"horizon_guard_blocks": sum(e.get("guard_blocked", False) for e in actions),
            "game_actions": len(applied), "non_game_tool_attempts": r["actor_usage"]["non_game_tool_attempts"],
            "quarterly_main_actions": Counter(e["args"]["choice"] for e in applied if phase(e["before"]) == "main_action"),
            "minimum_health": min((e["after"]["current_state"]["status"]["health"] for e in applied), default=None),
            "minimum_dignity": min((e["after"]["current_state"]["status"]["dignity"] for e in applied), default=None)}
        title = f"pair-{r['pair']:02d}-{arm}"
        traces += [f"## {title}", "", f"Outcome: {r['outcome']}; promotion {r.get('promotion')}; alive through month 6 {r.get('alive_through_month_6')}.", ""]
        for e in applied:
            obs = e["before"]
            chosen = next((c.get("action") for c in obs.get("choices", []) if c["choice"] == e["args"]["choice"]), "?")
            traces += [f"- M{obs['current_state']['time']['current_month']} {obs.get('current_event', {}).get('title')}: {chosen}. Notes: {e['args'].get('notes', '')}"]
        traces.append("")
        with gzip.open(output / f"{title}-public-tools.jsonl.gz", "wb") as archive:
            archive.write((run / "public-tools.jsonl").read_bytes())
        for name in ("verified-final.json", "verified-logs.json", "system_prompt.md"):
            if (run / name).exists():
                shutil.copyfile(run / name, output / f"{title}-{name}")
    complete = all(groups.get(arm, {}).get("resolved") == protocol["n_per_arm"] for arm in ("baseline", "candidate"))
    models = {arm: sorted({m for r in results if r["arm"] == arm for m in r["actor_usage"].get("models", {})}) for arm in ("baseline", "candidate")}
    outcome = {"block_complete": complete, "groups": groups, "resolved_models": models,
        "same_resolved_model": bool(models["baseline"]) and models["baseline"] == models["candidate"],
        "claim": "Exploratory counts only; no superiority or universal guarantee.",
        "raw_results": results}
    if complete:
        outcome["composite_difference"] = (groups["candidate"]["promotion_and_alive"] - groups["baseline"]["promotion_and_alive"]) / protocol["n_per_arm"]
        outcome["descriptive_ablation_signal"] = groups["candidate"]["promotion_and_alive"] > groups["baseline"]["promotion_and_alive"] and groups["candidate"]["alive_through_month_6"] >= groups["baseline"]["alive_through_month_6"]
    (output / "results.json").write_text(json.dumps(outcome, indent=2))
    (output / "decision-traces.md").write_text("# Autonomous actor decision traces\n\nThese are the actor's public action notes, not retrospective causal explanations.\n\n" + "\n".join(traces))
    shutil.copyfile(root / "protocol.json", output / "protocol.json")
    (output / "archive-sha256.txt").write_text("\n".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name for p in sorted(output.glob("*.gz"))) + "\n")
    print(json.dumps({k: v for k, v in outcome.items() if k != "raw_results"}, indent=2))


if __name__ == "__main__":
    analyze(Path(sys.argv[1]), Path(sys.argv[2]))
