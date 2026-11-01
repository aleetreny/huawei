"""Build the data file for the results panel (lab/panel/index.html).

Reads only committed results, never the simulator:

- the race registry (``lab/registry/*.jsonl``) from a Git ref, by default
  ``origin/main`` (where the closed race ended), or from the working tree with ``--race-ref ''``;
- every other machine's export in ``lab/registry-origins/<origin>/`` (T11);
- the T10 energy-bot table in ``lab/reports/historico/energy-bots/README.md``;
- Matteo's two manual runs (``docs/experiments/manual-skills-v0*-summary.json`` on ``origin/Matteo``);
- optionally a folder of local scripted games (``--exploration``), summarised to
  ``lab/panel/data/exploration.json`` so the raw files never enter Git.

Writes ``lab/panel/data.js`` (``window.PANEL_DATA = {...}``). Usage:

    git fetch origin
    uv run python scripts/panel/build.py
    uv run python scripts/panel/build.py --exploration ~/techarena-career-sim/exploration/runs
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PANEL = REPO / "lab" / "panel"
WEIGHTS = {"level": 30, "wealth": 20, "resilience": 15, "skill": 15, "risk_control": 10, "network": 10}


def git_show(ref: str, path: str) -> str | None:
    try:
        return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def read(ref: str, path: str) -> str | None:
    """A file from a Git ref, or from the working tree when ref is ''."""
    if ref:
        return git_show(ref, path)
    p = REPO / path
    return p.read_text() if p.exists() else None


def jsonl(text: str | None) -> list[dict]:
    return [json.loads(line) for line in (text or "").splitlines() if line.strip()]


def actor_label(actor: dict) -> tuple[str, str]:
    """(model group, full label) for an actor record."""
    if actor["kind"] == "scripted":
        return "Bot", "Scripted bot"
    c = json.loads(actor["config"])
    if actor["kind"] == "jiuwenswarm-target":  # the official runner with the competition model
        return "DeepSeek", f"{c.get('model_name', 'DeepSeek')} (official runner)"
    model = (c.get("model") or "?").capitalize()
    extra = [x for x in (c.get("effort") and f"effort {c['effort']}", c.get("autocompact") and f"memory {c['autocompact']}") if x]
    return model, model + (f" ({', '.join(extra)})" if extra else "")


def registry_games(texts: dict[str, str | None], source: str) -> tuple[list[dict], dict, dict]:
    policies = {p["policy_id"]: p for p in jsonl(texts["policies"])}
    actors = {a["actor_id"]: a for a in jsonl(texts["actors"])}
    jobs = {j["job_id"]: j for j in jsonl(texts["jobs"])}
    games = []
    for e in jsonl(texts["evaluations"]):
        if e["outcome"] not in ("completed", "eliminated"):
            continue  # interruptions are never scored (prereg-v1)
        if source == "race" and jobs.get(e["job_id"], {}).get("origin"):
            continue  # imported from another machine: shown once, under its own origin
        pol, act = policies.get(e["policy_id"], {}), actors.get(e["actor_id"], {"kind": "?", "config": "{}"})
        group, label = actor_label(act)
        usage = json.loads(e.get("tokens") or "{}")
        games.append({
            "id": e["job_id"], "source": source, "origin": jobs.get(e["job_id"], {}).get("origin", "") or source,
            "policy": pol.get("name", e["policy_id"][:8]), "family": pol.get("family", "?"),
            "model": group, "actor": label, "purpose": e["purpose"], "outcome": e["outcome"],
            "score": e["score"], "months": e["survival_months"], "completed": bool(e["completed"]),
            "dims": json.loads(e.get("dims") or "{}"), "t": e["ingested_at"], "steps": e.get("steps"),
            "cost": usage.get("cost_usd_list_price"),
        })
    return games, policies, actors


def decisions(texts: dict[str, str | None], policies: dict, actors: dict) -> list[dict]:
    out = []
    for d in jsonl(texts["decisions"]):
        if d["kind"] != "block_decision":
            continue
        p = json.loads(d["payload"])
        out.append({"id": d["decision_id"], "t": d["at"], "actor": actor_label(actors[d["subject"]])[1] if d["subject"] in actors else d["subject"],
                    "rows": [{k: r.get(k) for k in ("policy", "posterior_mean", "posterior_sd", "p_best", "action", "n_prefix", "reason")}
                             for r in p.get("rows", [])]})
    return out


def policy_status(policies: dict) -> dict[str, str]:
    return {p["name"]: p.get("status", "active") for p in policies.values()}


def energy_bots(text: str | None) -> list[dict]:
    """Rows of the T10 results table: arm, completed, mean months, blackouts, mean Q."""
    rows = []
    for line in (text or "").splitlines():
        cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
        if len(cells) == 8 and re.fullmatch(r"\d+", cells[1] or "") and re.fullmatch(r"[\d.]+", cells[2]):
            rows.append({"arm": cells[0], "completed": int(cells[1]), "months": float(cells[2]), "blackouts": int(cells[3]),
                         "other": cells[4], "q": float(cells[5]), "n": 40})
    return rows


def matteo_runs(ref: str) -> list[dict]:
    out = []
    for v in ("v01", "v02"):
        text = git_show(ref, f"docs/experiments/manual-skills-{v}-summary.json")
        if text:
            d = json.loads(text)  # v0.1 and v0.2 summaries use different keys
            status = d.get("final_status") or d.get("final_visible_status") or {}
            out.append({"name": f"Matteo {d.get('candidate') or d.get('skill_version', v)}",
                        "score": d.get("score", d.get("quantitative_score")), "level": status.get("level"),
                        "months": d.get("completed_months", d.get("survival_months")),
                        "note": "manual run, strong model (Codex) choosing every move"})
    return out


def summarise_exploration(root: Path) -> dict:
    """Per-policy summary of local scripted games (harness.py JSON files); keeps only final scores."""
    games = []
    for f in sorted(glob.glob(str(root / "*" / "game_*.json"))):
        d = json.loads(Path(f).read_text())
        es = d["final_obs"].get("ending_score") or {}
        if "quantitative_score" not in es:
            continue
        reason = d["final_obs"]["current_state"]["simulation_flags"].get("failure_reason") or "Completed"
        games.append({"policy": Path(f).parent.name, "score": es["quantitative_score"], "months": es.get("survival_months", 0),
                      "completed": bool(es.get("completed")), "ending": reason.split("—")[0].strip(),
                      "level": d["final_obs"]["current_state"]["status"]["level"],
                      "dims": {x["name"]: x["normalized_score"] for x in es.get("dimensions", [])}})
    return {"source": str(root), "built": time.time(), "games": games}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--race-ref", default="origin/main", help="Git ref with the race registry (the closed race ended on main); '' = working tree")
    ap.add_argument("--matteo-ref", default="origin/Matteo")
    ap.add_argument("--exploration", help="folder of local harness.py games to summarise into lab/panel/data/exploration.json")
    args = ap.parse_args()

    ref = args.race_ref if (not args.race_ref or git_show(args.race_ref, "lab/registry/evaluations.jsonl")) else ""
    tables = ("policies", "actors", "jobs", "evaluations", "decisions")
    race = {t: read(ref, f"lab/registry/{t}.jsonl") for t in tables}
    games, policies, actors = registry_games(race, "race")
    blocks = decisions(race, policies, actors)

    origins = {}
    for folder in sorted((REPO / "lab" / "registry-origins").glob("*/")):
        texts = {t: (folder / f"{t}.jsonl").read_text() if (folder / f"{t}.jsonl").exists() else None for t in tables}
        texts["policies"] = (texts["policies"] or "") + (race["policies"] or "")
        texts["actors"] = (texts["actors"] or "") + (race["actors"] or "")
        og, *_ = registry_games(texts, folder.name)
        origins[folder.name] = og

    exploration_file = PANEL / "data" / "exploration.json"
    if args.exploration:
        exploration_file.parent.mkdir(parents=True, exist_ok=True)
        exploration_file.write_text(json.dumps(summarise_exploration(Path(args.exploration).expanduser())))
    exploration = json.loads(exploration_file.read_text()) if exploration_file.exists() else None

    data = {
        "built": time.time(), "race_ref": ref or "working tree",
        "race_commit": subprocess.run(["git", "rev-parse", "--short", ref or "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip(),
        "weights": WEIGHTS, "games": games, "blocks": blocks, "status": policy_status(policies),
        "origins": origins, "energy_bots": energy_bots(read(ref, "lab/reports/historico/energy-bots/README.md") or read(ref, "lab/reports/energy-bots/README.md")),
        "matteo": matteo_runs(args.matteo_ref), "exploration": exploration,
        "counts": dict(Counter(g["model"] for g in games)),
    }
    PANEL.mkdir(parents=True, exist_ok=True)
    (PANEL / "data.js").write_text("window.PANEL_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
    by = defaultdict(int)
    for g in games:
        by[g["model"]] += 1
    print(f"race {ref or 'working tree'}: {len(games)} scored games {dict(by)}, {len(blocks)} block decisions; "
          f"origins {{{', '.join(f'{k}: {len(v)}' for k, v in origins.items())}}}; energy arms {len(data['energy_bots'])}; "
          f"matteo {len(data['matteo'])}; exploration {len(exploration['games']) if exploration else 0}")


if __name__ == "__main__":
    main()
