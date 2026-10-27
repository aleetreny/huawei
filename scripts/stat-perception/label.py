"""Label every story answer with the direction it moves each stat, read from the wording only, with Haiku.

Follows Alejandro's question bank (branch alejandro/optimistic-gauss-edyw1j): his answers.json joins the
exact catalogue of main-1nddsg with his blind category labels. This script adds stat labels under
several "ways of seeing" (VARIANTS) so they can be compared on reserved events and in the replica.

Haiku sees one question at a time: the event description and its options, never the effects.
Output: tags-<variant>.json, {node:choice: {skill: -1|0|1, network: ..., output: ..., health: ..., dignity: ...}},
identifiers and codes only (no game text), so it can go into Git.

    python3 scripts/stat-perception/label.py --answers ~/careerlab-data/stat-perception/answers.json \\
        --variant defs --out lab/reports/stat-perception/tags-defs.json --slots 4
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import subprocess
import time
from collections import defaultdict
from pathlib import Path

STATS = ["skill", "network", "output", "health", "dignity"]

DEFS = """How the five stats work in this career game:
- Skill: your professional competence. UP when you handle the situation the rigorous, grown-up professional way: take ownership, fix it properly, quantify, document, put a process or checklist in place, set a clear quality bar, coach someone, learn or practise. DOWN when you skip the craft: a shortcut, letting someone else do the thinking, dodging the work.
- Output: your own visible delivery. UP when you ship, deliver, show a result or protect your own deadline. DOWN when the option takes time away from your own delivery (pausing work, investigations, rework, the slow thorough path, fixing someone else's problem, extra meetings) or delays shipping.
- Network: the goodwill of the people involved. UP when you help, include, give credit, mediate or handle it kindly in private. DOWN when you go against a person: block, refuse, report, correct or expose them, compete with them, keep away.
- Health: physical energy. UP with rest, limits on hours, handing work off. DOWN with overtime, extra load, stress.
- Dignity: self-respect and integrity. UP when you act on principle, are honest, stand your ground calmly, own it. DOWN when you lie, hide, grovel, give in against your values, gossip or get humiliated."""

CUES = """Checklist of cues (an option can match several):
Skill UP: owns or fixes the root cause | documents, writes it up | quantifies, brings data | sets a process, checklist, standard or plan | coaches, teaches, trains a deputy | holds a quality bar | learns, practises, studies.
Skill DOWN: shortcut, workaround, copy | hands the thinking to someone else | avoids the work.
Output UP: ships, delivers, finishes, demos a result | keeps own deadline | does the work now.
Output DOWN: pauses or delays shipping | spends own time on investigation, rework, someone else's problem, extra meetings | takes the slow thorough path.
Network UP: helps, includes, gives credit, mediates, apologises, private kind word.
Network DOWN: blocks, refuses, reports, corrects or exposes someone, competes, withdraws, sides against.
Health UP: rest, sleep, exercise, limits on hours, delegates.  Health DOWN: overtime, weekends, extra load, conflict stress.
Dignity UP: principled, honest, calm firmness, owns it.  Dignity DOWN: lies, hides, grovels, caves against values, gossip, humiliation."""

# Round 3: Output was the stat worth perceiving (replica) and the most mislabelled one. Rewritten from the
# design half's Output errors: Haiku read Output as "time spent", the game reads it as visible momentum.
DEFS2 = DEFS.replace(
    "- Output: your own visible delivery. UP when you ship, deliver, show a result or protect your own deadline. DOWN when the option takes time away from your own delivery (pausing work, investigations, rework, the slow thorough path, fixing someone else's problem, extra meetings) or delays shipping.",
    "- Output: your visible contribution and momentum at work. UP when you push your own work, results or standing forward: deliver, take more on, set a recovery plan with dates, keep focusing on the work, even promote yourself. DOWN when you disengage or step back: say nothing, swallow it, dodge responsibility, hand your work off, ask for a lighter load, rest instead of working, or get worn down. A short conversation, a review or a bit of help does not cost Output.")
assert DEFS2 != DEFS

FORMAT = """Answer with JSON only: {"<option number>": {"skill": s, "network": s, "output": s, "health": s, "dignity": s}, ...} for every option of every question, keyed "<question id>". Each s is 1 (goes up), -1 (goes down) or 0 (no clear change). Example shape: {"q1": {"1": {"skill": 1, "network": 0, "output": -1, "health": 0, "dignity": 1}, "2": {...}}}"""

VARIANTS = {
    # no explanation of the stats: only forces a judgement on every stat for every option
    "plain": "For each option, say which way choosing it moves each of the player's five stats: skill, network, output, health, dignity.",
    # what each stat means in this game, written from the design half of the events
    "defs": DEFS + "\n\nFor each option, say which way choosing it moves each stat.",
    # the same meanings as a checklist of concrete cues
    "cues": CUES + "\n\nFor each option, go through the checklist and say which way choosing it moves each stat.",
    # meanings plus an explicit comparison of the options of the same question
    "contrast": DEFS + "\n\nThe options of a question usually trade one stat for another. Compare them with each other first: for each stat, which option does most for it and which costs it. Then say which way choosing each option moves each stat.",
    # meanings plus a few words on what the option spends and earns before the signs
    "reason": DEFS + "\n\nFor each option, first think in a few words about what it spends (your time, your health, a relationship, your integrity) and what it earns, then say which way choosing it moves each stat. Put the reasoning in a field \"why\" (at most 12 words) next to the stats.",
    # defs with Output redefined as visible momentum (round 3)
    "defs2": DEFS2 + "\n\nFor each option, say which way choosing it moves each stat.",
    # one trade per option: the stat it mainly buys and the stat it mainly pays with (written as +1 / -1, rest 0)
    "trade": DEFS + "\n\nEvery option is a trade. For each option pick the ONE stat it mainly buys (+1) and the ONE stat it mainly pays with (-1); use none when there is no clear gain or no clear cost. Every other stat is 0.",
}


def questions(answers: list[dict]) -> list[dict]:
    by = defaultdict(list)
    for a in answers:
        by[a["node"]].append(a)
    out = []
    for node, aa in sorted(by.items()):
        aa.sort(key=lambda a: a["choice"])
        out.append({"node": node, "desc": aa[0]["desc"], "options": [(a["choice"], a["text"]) for a in aa]})
    return out


def prompt(batch: list[dict], instructions: str) -> str:
    parts = [instructions, "", FORMAT, ""]
    for i, q in enumerate(batch, 1):
        parts.append(f"### q{i}\nSituation: {q['desc']}")
        parts += [f"  {c}. {t}" for c, t in q["options"]]
        parts.append("")
    return "\n".join(parts)


def call(text: str, cwd: Path) -> tuple[dict, dict]:
    cmd = ["claude", "-p", "--model", "haiku", "--tools", "", "--strict-mcp-config", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json",
           "--system-prompt", "You annotate options of a workplace career game. Output JSON only, no prose."]
    for attempt in range(3):
        r = subprocess.run(cmd, input=text, capture_output=True, text=True, cwd=cwd, timeout=600)
        try:
            env = json.loads(r.stdout)
            body = env.get("result", "")
            body = body[body.index("{"): body.rindex("}") + 1]
            return json.loads(body), env
        except (ValueError, KeyError):
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"no JSON after 3 attempts: {r.stdout[:300]} {r.stderr[:300]}")


def sign(v) -> int:
    try:
        v = int(round(float(v)))
    except (TypeError, ValueError):
        return 0
    return (v > 0) - (v < 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--variant", required=True, choices=sorted(VARIANTS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch", type=int, default=20, help="questions per call")
    ap.add_argument("--slots", type=int, default=4)
    args = ap.parse_args()
    qs = questions(json.load(open(Path(args.answers).expanduser())))
    batches = [qs[i:i + args.batch] for i in range(0, len(qs), args.batch)]
    cwd = Path(args.answers).expanduser().parent / "empty"
    cwd.mkdir(exist_ok=True)
    tags, usage = {}, defaultdict(float)

    def run(batch):
        return batch, *call(prompt(batch, VARIANTS[args.variant]), cwd)

    with cf.ThreadPoolExecutor(args.slots) as ex:
        for batch, res, env in ex.map(run, batches):
            for i, q in enumerate(batch, 1):
                got = res.get(f"q{i}") or {}
                for c, _ in q["options"]:
                    o = got.get(str(c)) or {}
                    tags[f"{q['node']}:{c}"] = {s: sign(o.get(s)) for s in STATS}
            u = env.get("usage") or {}
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                usage[k] += u.get(k, 0) or 0
            usage["cost_usd"] += env.get("total_cost_usd") or 0
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(tags, indent=0, sort_keys=True))
    print(f"{args.variant}: {len(tags)} answers in {len(batches)} calls; usage {dict(usage)}")


if __name__ == "__main__":
    main()
