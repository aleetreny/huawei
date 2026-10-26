"""Black-box six-month research, using only the five public game tools.

No engine imports, database reads, state cloning, event seeds or model API.
Raw responses are retained outside the repo. Not a competition actor.
"""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index, phase


ENERGY = {
    "balanced": ["Prepare report materials", "Network maintenance", "Health recovery"],
    "reports": ["Prepare report materials"] * 3,
    "network": ["Network maintenance"] * 3,
    "recovery": ["Health recovery"] * 3,
    "risk": ["Defuse legacy risk", "Prepare report materials"],
    "skill": ["Skill learning", "Prepare report materials"],
    "overwork": ["High-intensity work", "Prepare report materials"],
    "mental": ["Mental recovery"] * 3,
    "skip": [],
}
MAIN = {"project": "Apply for a key project", "report": "Report results to your manager",
        "mentor": "Build a mentorship", "none": "No action",
        "resources": "Fight for resources", "rotation": "Apply for rotation",
        "showcase": "Showcase results", "repair": "Repair a key relationship", "low": "Lay low and reduce risk"}


def learn_effects(source):
    """Research-only empirical action model; never exported into a submitted Skill."""
    from collections import defaultdict
    samples = defaultdict(list)
    files = sorted(source.glob("run-*.json"))
    for path in files:
        r = json.loads(path.read_text())
        for entry in r.get("logs", {}).get("entries", []):
            message = entry.get("message", "")
            match = re.search(r"Chose #\d+: (.+)\n", message)
            if match:
                delta = {k.lower(): int(v) for k, v in re.findall(r"(Health|Dignity|Skill|Network|Output|Wealth) ([+-]\d+)", message)}
                samples[match.group(1)].append(delta)
    return {k: {stat: sum(d.get(stat, 0) for d in ds) / len(ds)
                for stat in ("health", "dignity", "skill", "network", "output", "wealth")}
            for k, ds in samples.items()}


def research_score(status, effects):
    # Lab hypotheses estimated in discovery, not published promotion thresholds.
    score = 0.0
    for stat, target, weight in (("skill", 9, 1), ("network", 3, 3), ("output", 3, 3), ("dignity", 7, .3)):
        before = status.get(stat, 0)
        after = max(0, before + effects.get(stat, 0))
        score += weight * (min(target, after) - min(target, before))
    health = status["health"] + effects.get("health", 0)
    score += .7 * (min(8, health) - min(8, status["health"]))
    score -= 100 * max(0, 1 - health) + 4 * max(0, 4 - health)
    return score


def node_key(obs):
    # Identity of visible question, not of the hidden game state.
    event = obs.get("current_event") or {}
    payload = [event.get("title"), event.get("description"), obs.get("choices")]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:20]


def choose(obs, rng, story, energy, main, allocations, counts, model=None, memory=None):
    choices = obs["choices"]
    ph = phase(obs)
    if memory is not None:
        feedback = obs.get("events", "")
        if "HR partner" in feedback:
            memory["risk"] = 2 if ("frowning" in feedback or "angry" in feedback) else (1 if "quietly" in feedback else 0)
    if ph in ("energy", "main_action") and (energy == "adaptive" if ph == "energy" else main == "adaptive"):
        status = obs["current_state"]["status"]
        left = (obs.get("current_event") or {}).get("remaining_energy", 3)
        options = [c for c in choices if c.get("energy_cost", 0) <= left]
        def value(c):
            eff = {k.lower(): v for k, v in c.get("status_updates", {}).items()}
            val = research_score(status, eff)
            if "HiddenRisk" in c.get("status_updates", {}):
                val += -c["status_updates"]["HiddenRisk"] * (5 if (memory or {}).get("risk", 0) >= 2 else .2)
            if c["action"] == "Defuse legacy risk":
                val += 14 if (memory or {}).get("risk", 0) >= 2 else 0
            return val / max(1, c.get("energy_cost", 1))
        best = max(options, key=value)
        if best["action"] == "Defuse legacy risk" and memory is not None:
            memory["risk"] = 0
        return best
    if ph == "energy":
        month = month_index(obs)
        index = allocations.get(month, 0)
        targets = ENERGY[energy]
        target = targets[index] if index < len(targets) else "__finish__"
        match = [c for c in choices if c.get("action", "").lower() == target.lower()]
        if not match:
            match = [c for c in choices if any(x in c.get("action", "").lower() for x in ("finish", "skip", "confirm", "end allocation"))]
        if not match:
            raise ValueError(f"Cannot identify energy action {target}: {choices}")
        allocations[month] = index + 1
        return match[0]
    if ph == "main_action":
        target = MAIN[main].lower()
        match = [c for c in choices if target in c.get("action", "").lower()]
        if not match:
            raise ValueError(f"Cannot identify main action {target}: {choices}")
        return match[0]
    if story == "first":
        return choices[0]
    if story == "coverage":
        key = node_key(obs)
        minimum = min(counts[(key, c["choice"])] for c in choices)
        return rng.choice([c for c in choices if counts[(key, c["choice"])] == minimum])
    if story == "learned":
        status = obs["current_state"]["status"]
        def value(c):
            effects = (model or {}).get(c["action"])
            if effects is None:
                return -1.0  # explicit fallback; no fabricated effects
            score = research_score(status, effects)
            text = c["action"].lower()
            # General text features intended to avoid hidden exposure, still unvalidated.
            if any(w in text for w in ("say nothing", "stay silent", "brush it off", "bluff", "backdate", "pretend", "inflate", "hide it", "fudge", "join in and laugh", "hint that", "vague hint", "deny knowing", "take the link", "industry gossip", "without opening", "let it slide", "keep quiet")):
                score -= 15
            return score
        return max(choices, key=value)
    return rng.choice(choices)


async def run_one(client, output, index, seed, arm, counts, model=None):
    rng = random.Random(seed)
    story, energy, main = arm
    record = {"run": index, "choice_seed": seed, "arm": list(arm),
              "assignment": "shuffled fixed arm schedule; independent unseeded game sessions",
              "steps": [], "outcome": "interrupted"}
    try:
        sid = await client.new_game()
        record["session_id"] = sid
        allocations = {}
        memory = {}
        obs = await client.observe(sid)
        for step in range(150):
            if is_terminal(obs) or month_index(obs) > 6:
                record["outcome"] = "eliminated" if is_terminal(obs) else "six_month_window"
                break
            choice = choose(obs, rng, story, energy, main, allocations, counts, model, memory)
            counts[(node_key(obs), choice["choice"])] += 1
            result = await client.take_action(sid, choice["choice"], "Isolated six-month black-box research", obs)
            after = await client.observe(sid)
            record["steps"].append({"before": obs, "phase": phase(obs), "choice": choice,
                                    "reply": result.reply, "applied": result.applied,
                                    "ambiguous": result.ambiguous, "after": after})
            if not result.applied:
                raise RuntimeError(f"Rejected action: {result.reply}")
            obs = after
        else:
            raise RuntimeError("step cap")
        record["final"] = obs
        record["logs"] = await client.logs(sid, 100)
        record["promoted"] = int(str(obs["current_state"]["status"]["level"])[1:]) >= 2
    except Exception as exc:
        record["error"] = repr(exc)
    (output / f"run-{index:05d}.json").write_text(json.dumps(record, ensure_ascii=False))
    return record


async def main(args):
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "runner-source.py").write_bytes(Path(__file__).read_bytes())
    # Keep infrastructure settings explicit, without creating default lab/registry dirs.
    settings = Settings()
    model = learn_effects(args.training) if args.training else None
    if model:
        (args.output / "frozen-effect-model.json").write_text(json.dumps(model, indent=2))
    arms = [(s, e, m) for s in args.story.split(",") for e in args.energy.split(",") for m in args.main.split(",")]
    jobs = [(i, arms[i % len(arms)]) for i in range(args.runs)]
    random.Random(args.seed).shuffle(jobs)
    queue = asyncio.Queue()
    for job in jobs:
        queue.put_nowait(job)
    counts, outcomes = Counter(), Counter()
    async def worker(worker_id):
        while not queue.empty():
            i, arm = queue.get_nowait()
            # Competition mode permits one new game per server process.
            spec = ServerSpec(f"first-review-{i}", args.output / "servers" / str(i), competition_mode=True)
            async with GameClient(spec, settings) as client:
              if i == jobs[0][0]:
                (args.output / "handbook.json").write_text(json.dumps(await client.handbook(), indent=2))
                (args.output / "manifest.json").write_text(json.dumps({**vars(args), "output": str(args.output), "training": str(args.training) if args.training else None,
                    "environment": spec.fingerprint(settings), "arms": arms,
                    "no_simulator_seed_or_clone": True}, indent=2))
              try:
                record = await run_one(client, args.output, i, args.seed + i, arm, counts, model)
              except Exception:
                raise
              else:
                outcomes[record["outcome"]] += 1
                outcomes["promoted"] += bool(record.get("promoted"))
                if sum(outcomes[k] for k in ("six_month_window", "eliminated", "interrupted")) % 20 == 0 or record.get("error"):
                    print(json.dumps({"worker": worker_id, "run": i, "arm": arm, "totals": outcomes,
                                      "error": record.get("error")}), flush=True)
                queue.task_done()
    await asyncio.gather(*(worker(i) for i in range(args.workers)))
    print(json.dumps({"done": True, "outcomes": outcomes}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runs", type=int, default=288)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=261026)
    parser.add_argument("--story", default="first,uniform,coverage")
    parser.add_argument("--energy", default=",".join(ENERGY))
    parser.add_argument("--main", default=",".join(MAIN))
    parser.add_argument("--training", type=Path)
    asyncio.run(main(parser.parse_args()))
