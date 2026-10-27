"""Question bank: full 48-month scripted bots with randomised story choices.

Goal (Alejandro, 27 Oct): for every story question, is there an answer that pays off?
Can questions be grouped into categories an agent can recognise, each with its own
answer policy? What should the agent pursue at each stage of the career?

Only the five public tools are used. No Claude quota, no registry, nothing in the race.
Each episode is written as one compact JSON line (state before every decision, the
question key, the option chosen and whether it was a random draw), so choice effects
can be estimated with known assignment probabilities. Question texts go to a separate
dictionary file. Raw output stays under CAREERLAB_DATA (development-dataset text).

Story policy:
  --story random            every story option uniformly at random
  --story greedy --eps E    with prob. E uniform random, else the best option in --values
                            (a question key -> option scores file from analyse.py);
                            unknown questions are random. A category policy is the same
                            mechanism with values built from category ranks (categories.py).
Energy: each quarter draws one bundle (weights below); main action uniformly random.

    CAREERLAB_DATA=~/careerlab-data/question-bank nice -n 19 uv run python scripts/question-bank/run.py --batch explore --n 3000 --slots 4
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import random
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("CAREERLAB_DATA", str(Path.home() / "careerlab-data" / "question-bank"))

from careerlab.config import load_settings  # noqa: E402
from careerlab.mcp_client import is_terminal, month_index, phase  # noqa: E402
from careerlab.pool import ServerPool  # noqa: E402

HIGH, SKILL, NET, DEFUSE, MENTAL, HEALTH, REPORT, RESERVE = (
    "High-intensity work", "Skill learning", "Network maintenance", "Defuse legacy risk",
    "Mental recovery", "Health recovery", "Prepare report materials", "Reserve energy (no action)")
BUNDLES: dict[str, tuple[float, list[str]]] = {
    "defuse+health": (0.30, [DEFUSE, HEALTH]),
    "health+mental+report": (0.15, [HEALTH, MENTAL, REPORT]),
    "report+network+health": (0.15, [REPORT, NET, HEALTH]),
    "health+report+report": (0.15, [HEALTH, REPORT, REPORT]),
    "health+health+report": (0.10, [HEALTH, HEALTH, REPORT]),
    "skill+health": (0.075, [SKILL, HEALTH]),
    "high+health": (0.075, [HIGH, HEALTH]),
}
STATS = ("health", "dignity", "skill", "network", "output", "wealth", "duration_in_level")


def qkey(obs: dict[str, Any]) -> str:
    """Identity of the visible question (title, text and option labels), not of the hidden state."""
    ev = obs.get("current_event") or {}
    payload = [ev.get("title"), ev.get("description"), [c.get("action") for c in obs.get("choices") or []]]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()[:16]


def compact_state(obs: dict[str, Any]) -> list[Any]:
    st = obs["current_state"]["status"]
    return [st.get(k) for k in STATS] + [int(str(st.get("level", "L1")).lstrip("L") or 1)]


class Bot:
    def __init__(self, seed: int, story: str, eps: float, values: dict[str, list[float]], smart: bool = False):
        self.rng = random.Random(seed)
        self.story, self.eps, self.values, self.smart = story, eps, values, smart
        self.hr = 0  # last HR risk remark level seen (0 calm .. 4 angry)

    def story_choice(self, key: str, n: int) -> tuple[int, bool]:
        vals = self.values.get(key)
        if self.story == "random" or vals is None or len(vals) != n or self.rng.random() < self.eps:
            return self.rng.randrange(n), True
        best = max(vals)
        return self.rng.choice([i for i, v in enumerate(vals) if v == best]), False

    def bundle(self, health: int) -> str:
        """--smart: the known guardrails (Defuse on a risk remark, preventive Health) 75 % of
        quarters, a random bundle otherwise, so Energy effects stay measurable."""
        if self.smart and self.rng.random() < 0.75:
            if self.hr >= 2:
                return "defuse+health"
            if health <= 6:
                return "health+health+report"
            return self.rng.choice(["health+report+report", "report+network+health"])
        names = list(BUNDLES)
        return self.rng.choices(names, weights=[BUNDLES[n][0] for n in names])[0]

    def main_action(self, choices: list[dict[str, Any]]) -> dict[str, Any]:
        if self.smart and self.rng.random() < 0.5:
            want = "Lay low and reduce risk" if self.hr >= 3 else "Apply for a key project"
            for c in choices:
                if c.get("action") == want:
                    return c
        return self.rng.choice(choices)


async def play(client: Any, bot: Bot, questions: dict[str, Any]) -> dict[str, Any]:
    sid = await client.new_game()
    rows: list[list[Any]] = []
    energy_plan: list[str] = []
    bundle = None
    quarter_seen = None
    obs: dict[str, Any] = {}
    for _ in range(4000):
        obs = await client.observe(sid)
        if is_terminal(obs):
            break
        ph = phase(obs)
        choices = obs.get("choices") or []
        m = month_index(obs)
        ev_text = obs.get("events") or ""
        if "HR partner" in ev_text:
            seg = ev_text[ev_text.index("HR partner"):][:80]
            for lvl, word in enumerate(("smiling", "quietly", "frowning", "uneasy", "angry")):
                if word in seg:
                    bot.hr = lvl
        if ph == "energy":
            q = (m, obs["current_state"]["time"].get("current_quarter"))
            if q != quarter_seen:
                quarter_seen, bundle = q, bot.bundle(obs["current_state"]["status"]["health"])
                energy_plan = list(BUNDLES[bundle][1])
            left = (obs.get("current_event") or {}).get("remaining_energy", 0)
            by = {c.get("action"): c for c in choices}
            pick = None
            while energy_plan and pick is None:
                name = energy_plan.pop(0)
                c = by.get(name)
                if c and c.get("energy_cost", 0) <= left:
                    pick = c
            if pick is None:
                pick = by.get(RESERVE) or next(c for c in choices if c.get("energy_cost", 0) == 0)
            rows.append([m, "E", compact_state(obs), pick["action"], bundle, ev_text or None])
            choice = pick["choice"]
        elif ph == "main_action":
            pick = bot.main_action(choices)
            rows.append([m, "M", compact_state(obs), pick["action"], None, ev_text or None])
            choice = pick["choice"]
        elif ph == "event":
            key = qkey(obs)
            if key not in questions:
                ev = obs.get("current_event") or {}
                questions[key] = {"title": ev.get("title"), "description": ev.get("description"),
                                  "options": [c.get("action") for c in choices]}
            idx, rnd = bot.story_choice(key, len(choices))
            rows.append([m, "S", compact_state(obs), key, [idx, len(choices), int(rnd)], ev_text or None])
            choice = choices[idx]["choice"]
        else:
            rows.append([m, "D", compact_state(obs), None, None, ev_text or None])
            choice = choices[0]["choice"]
        res = await client.take_action(sid, choice, "", before=obs)
        if not res.applied:
            raise RuntimeError(f"rejected action: {res.reply}")
    flags = obs.get("current_state", {}).get("simulation_flags", {})
    return {"session": sid, "rows": rows, "final": compact_state(obs), "final_events": obs.get("events"),
            "failure": flags.get("failure_reason"), "score": obs.get("ending_score")}


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--slots", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=27_100_000)
    ap.add_argument("--story", choices=("random", "greedy"), default="random")
    ap.add_argument("--eps", type=float, default=1.0)
    ap.add_argument("--values", type=Path)
    ap.add_argument("--smart", action="store_true", help="guardrail Energy and main action (randomised part kept)")
    args = ap.parse_args()
    values = json.loads(args.values.read_text()) if args.values else {}
    s = load_settings()
    out = Path(os.environ["CAREERLAB_DATA"]) / args.batch
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps({**vars(args), "values": str(args.values), "bundles": BUNDLES,
                                                  "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=1))
    questions: dict[str, Any] = {}
    queue: asyncio.Queue[int] = asyncio.Queue()
    for r in range(args.n):
        queue.put_nowait(r)
    done = 0
    started = time.time()

    async def worker(w: int, pool: ServerPool) -> None:
        nonlocal done
        with (out / f"episodes-{w}.jsonl").open("a", encoding="utf-8") as fh:
            while True:
                try:
                    r = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                bot = Bot(args.seed0 + r, args.story, args.eps, values, args.smart)
                async with pool.lease() as client:
                    try:
                        ep = await play(client, bot, questions)
                    except Exception as exc:  # keep going; the episode is missing, never scored
                        print(f"episode {r}: {exc!r}", flush=True)
                        continue
                ep["run"], ep["seed"] = r, args.seed0 + r
                fh.write(json.dumps(ep, ensure_ascii=False, separators=(",", ":")) + "\n")
                fh.flush()
                done += 1
                if done % 100 == 0:
                    (out / "questions.json").write_text(json.dumps(questions, ensure_ascii=False))
                    print(f"{done} episodes, {len(questions)} questions, {time.time() - started:.0f}s", flush=True)

    async with ServerPool(s, s.servers_dir / args.batch, slots=args.slots) as pool:
        await asyncio.gather(*(worker(w, pool) for w in range(args.slots)))
    (out / "questions.json").write_text(json.dumps(questions, ensure_ascii=False))
    print(f"finished {done} episodes, {len(questions)} questions in {out}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
