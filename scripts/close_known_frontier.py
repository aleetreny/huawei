"""Close a frozen public question/answer catalogue through fresh six-month games.

Only official tools are used. Target answers are research exploration choices,
never a submission policy. There are no engine imports, clones or DB reads.
"""
from __future__ import annotations
import argparse
import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index, phase
from scripts.first_review_search import choose, learn_effects, node_key, research_score


class Frontier:
    def __init__(self, catalogue):
        self.questions = {q["id"]: q for q in catalogue}
        self.initial_pairs = {(q["id"], c["choice"]) for q in catalogue for c in q["choices"]}
        self.covered = {(q["id"], int(n)) for q in catalogue for n, a in q["answers"].items() if a["count"] > 0}
        self.targets = self.initial_pairs - self.covered
        self.evidence = {}
        self.new_pairs = set()
        self.paths = {(q["id"], int(n)): list(a.get("delayed_same_title", {})) for q in catalogue for n, a in q["answers"].items()}

    def remaining(self):
        return self.targets - set(self.evidence)

    def distances(self, title):
        d = {q: 0 for q, _ in self.remaining() if self.questions[q]["event"].get("title") == title}
        for _ in range(len(self.questions)):
            changed = False
            for (q, c), following in self.paths.items():
                if self.questions[q]["event"].get("title") != title:
                    continue
                value = 1 + min((d.get(k, 999) for k in following), default=999)
                if value < d.get(q, 999):
                    d[q] = value
                    changed = True
            if not changed:
                break
        return d

    def targeted(self, obs):
        key = node_key(obs)
        available = [c for c in obs["choices"] if (key, c["choice"]) in self.remaining()]
        if available:
            return available[0], "frozen_untried_answer"
        distances = self.distances((obs.get("current_event") or {}).get("title"))
        if key not in distances:
            return None, None
        ranks = [(min((distances.get(k, 999) for k in self.paths.get((key, c["choice"]), [])), default=999), c) for c in obs["choices"]]
        distance, best = min(ranks, key=lambda item: item[0])
        return (best, "observed_same_title_route") if distance < 999 else (None, None)

    def applied(self, before, choice, run, step):
        pair = (node_key(before), choice["choice"])
        self.new_pairs.update((node_key(before), c["choice"]) for c in before["choices"] if (node_key(before), c["choice"]) not in self.initial_pairs)
        if pair in self.targets and pair not in self.evidence:
            self.evidence[pair] = {"run": run, "step": step, "month": month_index(before), "choice": choice}

    def status(self):
        return {"frozen_available_pairs": len(self.initial_pairs), "initially_tried_pairs": len(self.covered),
            "initial_targets": len(self.targets), "closed_targets": len(self.evidence),
            "remaining": [{"question": q, "choice": c, "title": self.questions[q]["event"].get("title")} for q, c in sorted(self.remaining())],
            "evidence": [{"question": q, "answer": c, **v} for (q, c), v in sorted(self.evidence.items())],
            "new_available_pairs": len(self.new_pairs), "frozen_catalogue_complete": not self.remaining()}


def decide(obs, cohort, rng, model, frontier, counts, allocations, memory):
    if phase(obs) == "event":
        target, reason = frontier.targeted(obs)
        if target:
            return target, reason
    energy = "recovery" if cohort in ("growth", "low-dignity") else "adaptive"
    if cohort == "low-dignity" and phase(obs) == "event" and month_index(obs) >= 3:
        status = obs["current_state"]["status"]
        def value(c):
            effects = model.get(c["action"], {})
            health = status["health"] + effects.get("health", 0)
            dignity = status["dignity"] + effects.get("dignity", 0)
            score = 2 * (abs(status["dignity"] - 1) - abs(dignity - 1))
            score += .5 * effects.get("health", 0) - 20 * max(0, 3 - health)
            score += .2 * sum(effects.get(k, 0) for k in ("skill", "network", "output"))
            if any(w in c["action"].lower() for w in ("deny", "hint that", "bluff", "fudge", "backdate", "take the link", "industry gossip")):
                score -= 15
            return score
        return max(obs["choices"], key=value), "controlled_low_dignity_exploration"
    return choose(obs, rng, "learned", energy, "project", allocations, counts, model, memory), "learned_survival_fallback"


async def episode(client, root, index, cohort, model, frontier, counts, seed):
    record = {"run": index, "choice_seed": seed, "arm": ["targeted-closure", cohort, "project"],
        "steps": [], "outcome": "interrupted", "assignment": "adaptive frozen-frontier closure; not a policy comparison"}
    rng = random.Random(seed)
    try:
        sid = await client.new_game()
        record["session_id"] = sid
        obs = await client.observe(sid)
        allocations, memory = {}, {}
        for step in range(150):
            if is_terminal(obs) or month_index(obs) > 6:
                record["outcome"] = "eliminated" if is_terminal(obs) else "six_month_window"
                break
            selected, reason = decide(obs, cohort, rng, model, frontier, counts, allocations, memory)
            result = await client.take_action(sid, selected["choice"], f"Research closure: {reason}", obs)
            after = await client.observe(sid)
            record["steps"].append({"before": obs, "after": after, "phase": phase(obs), "choice": selected,
                "reply": result.reply, "applied": result.applied, "ambiguous": result.ambiguous, "reason": reason})
            if not result.applied:
                raise RuntimeError(f"Rejected action: {result.reply}")
            counts[(node_key(obs), selected["choice"])] += 1
            frontier.applied(obs, selected, index, step)
            obs = after
        else:
            raise RuntimeError("step cap")
        record["final"] = obs
        record["promoted"] = int(obs["current_state"]["status"]["level"][1:]) >= 2
        record["logs"] = await client.logs(sid, 100)
    except Exception as exc:
        record["error"] = repr(exc)
    atomic_write_json(root / f"run-{index:05d}.json", record)
    return record


async def main(args):
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(args.catalogue, args.output / "input-catalogue.json")
    shutil.copyfile(__file__, args.output / "runner-source.py")
    frontier = Frontier(json.loads(args.catalogue.read_text()))
    model = learn_effects(args.training)
    atomic_write_json(args.output / "frozen-effect-model.json", model)
    cfg = Settings(origin="matteoclosure", data_dir=args.output, lab_dir=args.output / "lab")
    manifest = {"catalogue": str(args.catalogue), "input_sha256": hashlib.sha256(args.catalogue.read_bytes()).hexdigest(),
        "runs": args.runs, "workers": args.workers, "choice_seed": args.seed,
        "environment": ServerSpec("manifest", args.output, competition_mode=True).fingerprint(cfg),
        "initial_frontier": frontier.status(), "stop": "frozen targets closed, or run cap; all started games finish their six-month window"}
    atomic_write_json(args.output / "manifest.json", manifest)
    atomic_write_json(args.output / "coverage-status.json", frontier.status())
    counts, totals = Counter(), Counter()
    next_index = 0
    started = time.monotonic()
    async def worker(worker):
        nonlocal next_index
        while frontier.remaining() and next_index < args.runs:
            index = next_index
            next_index += 1
            # Once only retention remains, focus the cohort on dignity exposure.
            remaining_titles = {x["title"] for x in frontier.status()["remaining"]}
            cohort = "low-dignity" if remaining_titles == {"The company tries to keep you after you look elsewhere"} else ("growth", "low-dignity", "safe", "growth")[index % 4]
            spec = ServerSpec(f"closure-{index}", args.output / "servers" / str(index), competition_mode=True)
            async with GameClient(spec, cfg) as client:
                record = await episode(client, args.output, index, cohort, model, frontier, counts, args.seed + index)
            totals[record["outcome"]] += 1
            atomic_write_json(args.output / "coverage-status.json", {**frontier.status(), "totals": dict(totals), "elapsed_seconds": round(time.monotonic() - started, 1)})
            if sum(totals.values()) % 20 == 0 or record.get("error") or not frontier.remaining():
                print(json.dumps({"runs": sum(totals.values()), "remaining": frontier.status()["remaining"], "totals": totals, "error": record.get("error")}), flush=True)
    await asyncio.gather(*(worker(w) for w in range(args.workers)))
    print(json.dumps({"done": True, **frontier.status(), "totals": totals}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--training", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runs", type=int, default=1024)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=320026)
    asyncio.run(main(parser.parse_args()))
