"""Quota-free, public-tool exploration through month twelve.

Research bot approximation of the manual, not an LLM Skill evaluation. Public
action-effect lookup and coverage routing stay outside submission Skills.
"""
from __future__ import annotations
import argparse
import asyncio
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index, phase
from scripts.first_review_search import node_key

STATS = ("health", "dignity", "skill", "network", "output", "wealth")
UNSAFE = ("say nothing", "stay silent", "brush it off", "bluff", "backdate", "pretend",
    "inflate", "hide it", "fudge", "join in and laugh", "hint that", "vague hint",
    "deny knowing", "take the link", "industry gossip", "without opening", "let it slide", "keep quiet")
SAFE = ("clarify", "document", "verify", "confirm", "credit", "scope", "agree", "plan",
    "explain", "honest", "report", "fix", "schedule", "check", "discuss", "prioriti")


def records(path):
    if path.is_file():
        with gzip.open(path, "rt") as stream:
            for line in stream:
                yield json.loads(line)
    else:
        for file in sorted(path.glob("run-*.json")):
            yield json.loads(file.read_text())


class Knowledge:
    def __init__(self):
        self.effects = defaultdict(lambda: defaultdict(list))
        self.counts = Counter()
        self.questions = {}
        self.paths = defaultdict(set)

    def observe(self, obs):
        if not 7 <= month_index(obs) <= 12:
            return
        key = node_key(obs)
        self.questions.setdefault(key, {"id": key, "event": obs.get("current_event") or {},
            "choices": obs["choices"], "phase": phase(obs)})

    def applied(self, before, choice):
        self.observe(before)
        if 7 <= month_index(before) <= 12:
            self.counts[node_key(before), choice["choice"]] += 1

    def ingest(self, record):
        for entry in record.get("logs", {}).get("entries", []):
            text = entry.get("message", "")
            match = re.search(r"Chose #\d+: (.+)\n", text)
            if match:
                delta = {stat.lower(): int(number) for stat, number in re.findall(r"(Health|Dignity|Skill|Network|Output|Wealth) ([+-]\d+)", text)}
                for stat in STATS:
                    self.effects[match[1]][stat].append(delta.get(stat, 0))
        previous = {}
        for step in record["steps"]:
            if not step.get("applied") or step.get("ambiguous"):
                continue
            obs = step["before"]
            self.applied(obs, step["choice"])
            if phase(obs) == "event":
                title = obs["current_event"]["title"]
                if title in previous:
                    self.paths[previous[title]].add(node_key(obs))
                previous[title] = (node_key(obs), step["choice"]["choice"])

    def effect(self, choice):
        if "status_updates" in choice:
            return {k.lower(): v for k, v in choice["status_updates"].items()}
        return {k: sum(v) / len(v) for k, v in self.effects.get(choice["action"], {}).items()}

    def route(self, obs):
        key = node_key(obs)
        untried = [c for c in obs["choices"] if self.counts[key, c["choice"]] == 0]
        if untried:
            return untried
        title = (obs.get("current_event") or {}).get("title")
        distances = {k: 0 for k, q in self.questions.items() if q["event"].get("title") == title
            and any(self.counts[k, c["choice"]] == 0 for c in q["choices"])}
        for _ in range(len(self.questions)):
            changed = False
            for (start, _), ends in self.paths.items():
                d = 1 + min((distances.get(end, 999) for end in ends), default=999)
                if d < distances.get(start, 999):
                    distances[start] = d
                    changed = True
            if not changed:
                break
        ranked = [(min((distances.get(k, 999) for k in self.paths[key, c["choice"]]), default=999), c) for c in obs["choices"]]
        if min((d for d, _ in ranked), default=999) < 999:
            best = min(d for d, _ in ranked)
            return [c for d, c in ranked if d == best]
        return []

    def status(self):
        pairs = {(key, c["choice"]) for key, q in self.questions.items() for c in q["choices"]}
        tried = {p for p in pairs if self.counts[p] > 0}
        return {"questions_7_12": len(self.questions), "available_answers": len(pairs),
            "tried_answers": len(tried), "remaining_answers": len(pairs - tried),
            "missing": [{"question": k, "choice": n, "title": self.questions[k]["event"].get("title")} for k, n in sorted(pairs-tried)]}


def update_warnings(obs, memory):
    text = obs.get("events", "")
    if "HR partner" in text:
        memory["risk"] = 2 if any(w in text for w in ("frowning", "angry")) else (1 if "quietly" in text else 0)


def value(obs, choice, knowledge, memory, profile):
    status = obs["current_state"]["status"]
    eff = knowledge.effect(choice)
    level = int(status["level"][1:])
    # Explicit research hypotheses, not known promotion cutoffs or Skill text.
    targets = {"skill": 9 if level == 1 else (12 if profile != "broad" else 15),
        "network": 3 if level == 1 else (6 if profile != "broad" else 8),
        "output": 3 if level == 1 else (6 if profile != "broad" else 8)}
    score = 0.0
    for stat, target in targets.items():
        if phase(obs) in ("energy", "main_action") and (stat, status[stat], level) in memory.get("stalled", set()):
            continue
        weight = 1 if stat == "skill" else 3
        score += weight * (min(target, max(0, status[stat]+eff.get(stat, 0))) - min(target, status[stat]))
    health = status["health"] + eff.get("health", 0)
    dignity = status["dignity"] + eff.get("dignity", 0)
    score += 1.2 * (min(9, health) - min(9, status["health"]))
    score += .6 * (min(8, dignity) - min(8, status["dignity"]))
    score -= 50 * max(0, 3-health) + 15 * max(0, 2-dignity)
    risk_weight = 8 if memory.get("risk", 0) >= 1 else (2 if profile == "risk" else .5)
    score -= eff.get("hiddenrisk", 0) * risk_weight
    if choice["action"] == "Defuse legacy risk":
        score += 15 if memory.get("risk", 0) else (5 if profile == "risk" else 0)
    text = choice["action"].lower()
    if any(word in text for word in UNSAFE):
        score -= 15
    if not eff:
        score += .3 * sum(word in text for word in SAFE)
    return score / max(1, choice.get("energy_cost", 1))


def decide(obs, knowledge, memory, profile, mode, rng):
    update_warnings(obs, memory)
    knowledge.observe(obs)
    ph = phase(obs)
    choices = obs["choices"]
    if ph == "energy":
        left = (obs.get("current_event") or {}).get("remaining_energy", 3)
        choices = [c for c in choices if c.get("energy_cost", 0) <= left]
    if not choices:
        raise ValueError("No affordable public action")
    ranked = sorted(choices, key=lambda c: value(obs, c, knowledge, memory, profile), reverse=True)
    if month_index(obs) >= 7 and mode != "safe":
        # Exploration deliberately overrides the manual-inspired default.
        budget = 1 if mode == "one" else (3 if mode == "three" else 100)
        if memory.get("deviations", 0) < budget:
            targets = knowledge.route(obs)
            if targets:
                best_count = min(knowledge.counts[node_key(obs), c["choice"]] for c in targets)
                candidates = [c for c in targets if knowledge.counts[node_key(obs), c["choice"]] == best_count]
                chosen = rng.choice(candidates)
                memory["deviations"] = memory.get("deviations", 0)+1
                return chosen, "coverage_or_same_title_route"
    if ph == "energy" and memory.get("risk", 0) and memory.get("risk_resolved_quarter") != obs["current_state"]["time"]["current_quarter"]:
        cleanup = next((c for c in choices if c["action"] == "Defuse legacy risk"), None)
        if cleanup and obs["current_state"]["status"]["health"] >= 4:
            return cleanup, "respond_to_public_risk_warning"
    return ranked[0], "manual_inspired_gap_capacity_realised_gain"


def remember(before, choice, after, memory):
    b, a = before["current_state"]["status"], after["current_state"]["status"]
    if phase(before) in ("energy", "main_action") and b["level"] == a["level"] and month_index(before) == month_index(after):
        for stat in ("skill", "network", "output"):
            if choice.get("status_updates", {}).get(stat.capitalize(), 0) > 0 and a[stat] <= b[stat]:
                memory.setdefault("stalled", set()).add((stat, b[stat], int(b["level"][1:])))
    if choice["action"] == "Defuse legacy risk":
        memory["risk_resolved_quarter"] = before["current_state"]["time"]["current_quarter"]
        memory["risk"] = 0


async def episode(client, root, index, profile, mode, knowledge, seed):
    record = {"run": index, "arm": ["manual-inspired-research-bot", profile, mode], "steps": [],
        "choice_seed": seed, "outcome": "interrupted", "assignment": "adaptive coverage; no policy-effect estimate"}
    rng, memory = random.Random(seed), {}
    try:
        sid = await client.new_game()
        record["session_id"] = sid
        obs = await client.observe(sid)
        for step in range(300):
            if is_terminal(obs) or month_index(obs) > 12:
                record["outcome"] = "eliminated" if is_terminal(obs) else "twelve_month_window"
                break
            selected, reason = decide(obs, knowledge, memory, profile, mode, rng)
            eff = knowledge.effect(selected)
            result = await client.take_action(sid, selected["choice"], f"Public research: {reason}", obs)
            after = await client.observe(sid)
            record["steps"].append({"before": obs, "after": after, "choice": selected,
                "phase": phase(obs), "reason": reason, "expected_nominal_effect": eff,
                "risk_warning_before": memory.get("risk", 0),
                "reply": result.reply, "applied": result.applied, "ambiguous": result.ambiguous})
            if not result.applied or result.ambiguous:
                raise RuntimeError(f"Unconfirmed action: {result.reply}")
            knowledge.applied(obs, selected)
            remember(obs, selected, after, memory)
            obs = after
        else:
            raise RuntimeError("step cap")
        record["final"] = obs
        record["logs"] = await client.logs(sid, 100)
        # Counts already updated live; ingest only public effect samples and paths.
        saved_counts = knowledge.counts.copy()
        knowledge.ingest(record)
        knowledge.counts = saved_counts
    except Exception as exc:
        record["error"] = repr(exc)
    atomic_write_json(root / f"run-{index:05d}.json", record)
    return record


async def main(args):
    args.output.mkdir(parents=True, exist_ok=False)
    knowledge = Knowledge()
    sources = sorted(args.evidence.glob("*/public-trajectories.jsonl.gz")) + args.prior
    for source in sources:
        for record in records(source):
            knowledge.ingest(record)
    manual = args.manual.read_bytes()
    (args.output / "manual.md").write_bytes(manual)
    shutil.copyfile(__file__, args.output / "runner-source.py")
    atomic_write_json(args.output / "initial-effects.json", {k: {s: sum(v)/len(v) for s,v in eff.items()} for k,eff in knowledge.effects.items()})
    cfg = Settings(origin="matteotwelve", data_dir=args.output, lab_dir=args.output / "lab")
    atomic_write_json(args.output / "manifest.json", {"runs_cap": args.runs, "workers": args.workers,
        "seed": args.seed, "prior": [str(p) for p in args.prior], "manual_sha256": hashlib.sha256(manual).hexdigest(),
        "environment": ServerSpec("manifest", args.output, competition_mode=True).fingerprint(cfg),
        "actor": "local Python bot, no LLM", "scope": "fresh games months 1-12, coverage counted only in 7-12",
        "limits": "Manual-inspired approximation plus empirical effects, adaptive updates, no state clones or causal guarantees"})
    totals = Counter()
    queue = asyncio.Queue()
    for i in range(args.runs):
        queue.put_nowait(i)
    started = time.monotonic()
    async def worker(worker_id):
        while not queue.empty():
            i = queue.get_nowait()
            profile = ("balanced", "risk", "broad")[i % 3]
            mode = ("safe", "one", "three", "frontier")[(i//3) % 4]
            spec = ServerSpec(f"second-review-{i}", args.output / "servers" / str(i), competition_mode=True)
            try:
                async with GameClient(spec, cfg) as client:
                    if i == 0:
                        atomic_write_json(args.output / "handbook.json", await client.handbook())
                    r = await episode(client, args.output, i, profile, mode, knowledge, args.seed+i)
            except Exception as exc:
                r = {"run": i, "arm": ["manual-inspired-research-bot",profile,mode], "steps": [], "outcome": "interrupted", "error": repr(exc)}
                atomic_write_json(args.output / f"run-{i:05d}.json", r)
            totals[r["outcome"]] += 1
            status = {**knowledge.status(), "totals": dict(totals), "elapsed_seconds": round(time.monotonic()-started,1)}
            atomic_write_json(args.output / "coverage-status.json", status)
            if sum(totals.values()) % 12 == 0 or r.get("error"):
                print(json.dumps({k:v for k,v in status.items() if k != "missing"}, ensure_ascii=False), flush=True)
            queue.task_done()
    await asyncio.gather(*(worker(i) for i in range(args.workers)))
    print(json.dumps({"done": True, "totals": dict(totals), **{k:v for k,v in knowledge.status().items() if k != "missing"}}), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--evidence", type=Path, default=Path("lab/reports/first-review-search"))
    p.add_argument("--manual", type=Path, default=Path("lab/policies-src/matteo-first-review/promotion-readiness-v2/bundle/skills/promotion-readiness/SKILL.md"))
    p.add_argument("--prior", type=Path, nargs="*", default=[])
    p.add_argument("--runs", type=int, default=192)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--seed", type=int, default=420026)
    asyncio.run(main(p.parse_args()))
