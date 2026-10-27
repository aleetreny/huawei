"""Compare f3-lean-polish-v1 games (local transcripts) with f3-lean-v1 race games (saved digests).

Per game: score, tokens per month survived, turns, notes length, and the share of each
quarterly choice. Reads only worker transcripts, saved digests and the committed registry.

    uv run python scripts/leah/compare_polish.py ~/careerlab-data/huawei-leah/runs/leah-scre-679bb8b8-*
"""

from __future__ import annotations

import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

from careerlab.digest import calls

REPO = Path(__file__).resolve().parents[2]
LEAN = "cc098e54e25efc64"
CHOICE = re.compile(r"\] Quarterly (energy allocation|main action) → \[\d+\] ([^(—]+?)\s*(?:\(declined|—|$)")
NOTE = re.compile(r"— notes: (.*)$")


def tokens_per_month(usage: dict, months: int) -> tuple[int, int]:
    u = usage.get("tokens", {})
    total = sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    return round(total / max(months, 1)), int(usage.get("turns") or 0)


def lean_games() -> list[dict]:
    evals = {}
    for line in (REPO / "lab/registry/evaluations.jsonl").read_text().splitlines():
        e = json.loads(line)
        if e["policy_id"] == LEAN and e["actor_id"] == "08e9167a965ed82c" and e["outcome"] in ("completed", "eliminated"):
            evals[e["job_id"]] = e
    out = []
    for job, e in evals.items():
        digest = REPO / "lab/reports/teacher-digests/haiku-cloud" / f"{job}.md"
        energy, main, notes = Counter(), Counter(), []
        if digest.exists():
            for line in digest.read_text().splitlines():
                m = CHOICE.search(line)
                if m:
                    (energy if m.group(1).startswith("energy") else main)[m.group(2).strip()] += 1
                n = NOTE.search(line)
                if n:
                    notes.append(len(n.group(1)))
        tpm, turns = tokens_per_month(json.loads(e["tokens"] or "{}"), e["survival_months"])
        out.append({"job": job, "score": e["score"], "months": e["survival_months"], "tpm": tpm, "turns": turns,
                    "energy": energy, "main": main, "note_chars": st.median(notes) if notes else None, "digest": digest.exists()})
    return out


def local_game(run: Path) -> dict:
    energy, main, notes, obs_calls, actions = Counter(), Counter(), [], 0, 0
    obs = None
    for tool, args, reply in calls(run):
        if tool.endswith("observe"):
            obs_calls += 1
            try:
                obs = json.loads(reply)
            except ValueError:
                pass
        elif tool.endswith("take_action") and obs:
            actions += 1
            title = (obs.get("current_event") or {}).get("title", "")
            chosen = next((c for c in obs.get("choices", []) if c.get("choice") == args.get("choice")), {})
            label = chosen.get("action", "?")
            if title.startswith("Quarterly energy"):
                energy[label] += 1
            elif title.startswith("Quarterly main"):
                main[label] += 1
            if args.get("notes"):
                notes.append(min(len(" ".join(args["notes"].split())), 200))  # digests cap notes at 200 chars
    r = json.loads((run / "result.json").read_text())
    tpm, turns = tokens_per_month(r.get("actor_usage") or {}, r.get("survival_months") or 0)
    return {"job": run.name, "score": r.get("quantitative_score"), "months": r.get("survival_months"), "tpm": tpm, "turns": turns,
            "energy": energy, "main": main, "note_chars": st.median(notes) if notes else None,
            "observe_per_action": round(obs_calls / max(actions, 1), 2)}


def shares(games: list[dict], key: str) -> dict[str, float]:
    total = Counter()
    for g in games:
        total.update(g[key])
    n = sum(total.values()) or 1
    return {k: round(100 * v / n) for k, v in total.most_common()}


def summary(name: str, games: list[dict]) -> None:
    done = [g for g in games if g["months"] == 48]
    print(f"\n## {name}: {len(games)} games, {len(done)} completed")
    print(f"score mean {st.mean(g['score'] for g in games):.1f}; tokens/month median (completed) "
          f"{st.median(g['tpm'] for g in done) if done else '-'}; turns median {st.median(g['turns'] for g in games)}")
    print(f"note length median chars {st.median([g['note_chars'] for g in games if g['note_chars']])}")
    if "observe_per_action" in games[0]:
        print(f"observe calls per action {games[0]['observe_per_action']}")
    print("energy %:", shares(games, "energy"))
    print("main %:", shares(games, "main"))


if __name__ == "__main__":
    summary("f3-lean-v1 (race, Haiku 2.1.303)", lean_games())
    mine = [local_game(Path(p).expanduser()) for p in sys.argv[1:]]
    if mine:
        summary("f3-lean-polish-v1 (origin leah, Haiku 2.1.295)", mine)
