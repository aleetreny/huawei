"""Obedience bank with DeepSeek in the official Skill-delivery form (the DeepSeek twin of transmision/runbench.py).

The agent loop runs in-process against the DeepSeek key: the system prompt is the official IDENTITY.md
(skill names and the manifest instruction) plus JiuwenSwarm's skills section (``N. name: description``),
built by ``runbench.system_prompt``; the user prompt is the official continuation prompt. The model gets the
five official game tools and ``skill_tool`` (same names, descriptions and schemas as ``fake_mcp.py``); the
SKILL.md body only reaches it through ``skill_tool``. ``observe`` replays the recorded steps of the bank item
from the month start; ``take_action`` on the last step ends the item.

    uv run python scripts/deepseek/bench.py select --per-rule 40 --out ~/careerlab-data/deepseek/ids-ds1.txt
    uv run python scripts/deepseek/bench.py run --variant control|<bundle dir> --name ds-control --ids <file> [--limit N]
    TRANSMISION_DATA=~/careerlab-data/deepseek uv run python scripts/transmision/score.py \
        --items ~/careerlab-data/deepseek/items.jsonl --arms ds-control,ds-t13-final --common

Results: ~/careerlab-data/deepseek/runs/<arm>/<item>.json in the format score.py and fingerprint.py read.
``haiku`` writes Haiku's recorded choices for the same items as arms ``hk-<arm>`` for side-by-side scoring.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts" / "transmision"))
from ds import BACKEND, DATA, BudgetStop, DeepSeek  # noqa: E402
from runbench import SID, continue_prompt, load_variant, system_prompt  # noqa: E402

BANK = REPO / "lab" / "data" / "transmision"
ITEMS = DATA / "items.jsonl"
RUNS = DATA / "runs"
MAX_TURNS = 40

SID_DOC = ":param session_id: UUID4 hex session id returned by ``new_game``."
_GAME = [
    ("new_game", "Start a new Career Emulator session.", {"properties": {}, "type": "object"}),
    ("observe", f"Observe the current state and available choices for a session.\n\n{SID_DOC}",
     {"properties": {"session_id": {"type": "string"}}, "required": ["session_id"], "type": "object"}),
    ("take_action", f"Apply one choice to a Career Emulator session.\n\n{SID_DOC}\n:param choice: One-based choice id from "
     "``observe`` choices.\n:param notes: Agent note or reasoning retained in the player log.",
     {"properties": {"session_id": {"type": "string"}, "choice": {"type": "integer"}, "notes": {"type": "string"}},
      "required": ["session_id", "choice", "notes"], "type": "object"}),
    ("check_latest_logs", f"Return the last log entries for a Career Emulator session.\n\n{SID_DOC}\n:param count: Number of "
     "recent log entries to return.",
     {"properties": {"session_id": {"type": "string"}, "count": {"default": 10, "type": "integer"}},
      "required": ["session_id"], "type": "object"}),
    ("show_employee_handbook", "Show the employee handbook as Markdown.", {"properties": {}, "type": "object"}),
]
_SKILL = ("skill_tool", "Use this tool to view the skill contents of a certain skill. On success it always includes an ASCII "
          "directory_tree of the skill root and discovered_skill_names (relative paths of nested dirs that contain "
          "SKILL.md). To load a nested skill, call again with relative_file_path (e.g. designer/SKILL.md).",
          {"type": "object", "properties": {
              "skill_name": {"type": "string", "description": "Name of the skill"},
              "relative_file_path": {"type": "string", "description": "Optional. Views a specific file within the skill "
                                     "directory at the relative_file_path. Leave blank to view the main SKILL.md file."}},
           "required": ["skill_name"]})


def tools(with_skills: bool) -> list[dict[str, Any]]:
    defs = _GAME + ([_SKILL] if with_skills else [])
    return [{"type": "function", "function": {"name": n, "description": d, "parameters": p}} for n, d, p in defs]


def dump(x: object) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"))


class Game:
    """In-memory copy of fake_mcp.py's game and skill servers for one bank item."""

    def __init__(self, observes: list[dict[str, Any]], logs_at: list[list[dict[str, str]]], handbook: str,
                 skills: dict[str, dict[str, str]]) -> None:
        self.steps, self.logs_at, self.handbook, self.skills = observes, logs_at, handbook, skills
        self.pos = 0
        self.record: list[dict[str, Any]] = []
        self.target: dict[str, Any] | None = None

    def call(self, name: str, a: dict[str, Any]) -> str:
        p = min(self.pos, len(self.steps) - 1)
        if name == "skill_tool":
            skill = str(a.get("skill_name") or "")
            rel = str(a.get("relative_file_path") or "") or "SKILL.md"
            self.record.append({"tool": "skill_tool", "skill": skill, "path": rel, "pos": self.pos})
            files = self.skills.get(skill)
            if files is None:
                return dump({"success": False, "error": f"Skill not found: {skill}"})
            if rel not in files:
                return dump({"success": False, "error": f"File not found: {rel}"})
            tree = f"{skill}/\n" + "\n".join(f"  {f}" for f in sorted(files))
            return dump({"skill_directory": f"/agent/skills/{skill}", "skill_content": files[rel],
                         "directory_tree": tree, "discovered_skill_names": []})
        if name == "new_game":
            self.record.append({"tool": "new_game"})
            return dump({"error": "Competition mode: only one game session is allowed."})
        if name == "show_employee_handbook":
            self.record.append({"tool": "show_employee_handbook"})
            return self.handbook
        if name not in ("observe", "check_latest_logs", "take_action"):
            return dump({"error": f"Unknown tool: {name}"})
        if a.get("session_id") != SID:
            return dump({"error": f"Unknown session_id: {a.get('session_id')}"})
        if name == "observe":
            self.record.append({"tool": "observe", "pos": p})
            return dump(self.steps[p])
        if name == "check_latest_logs":
            try:
                count = int(a.get("count") or 10)
            except (TypeError, ValueError):
                count = 10
            self.record.append({"tool": "check_latest_logs", "pos": p, "count": count})
            entries = self.logs_at[p][-max(1, count):]
            return dump({"session_id": SID, "log_file": f"/var/log/career/{SID}.log", "count": len(entries),
                         "entries": [{"session_id": SID, **e} for e in entries]})
        n = len(self.steps[p].get("choices") or [])
        try:
            choice = int(a.get("choice"))
        except (TypeError, ValueError):
            choice = -1
        if not 1 <= choice <= n:
            self.record.append({"tool": "take_action", "pos": p, "choice": a.get("choice"), "invalid": True})
            return dump({"success": False, "error": f"Invalid choice {a.get('choice')}; expected 1..{n}"})
        is_target = self.pos >= len(self.steps) - 1
        ev = {"tool": "take_action", "pos": p, "choice": choice, "notes": str(a.get("notes") or "")[:1000],
              "target": is_target}
        self.record.append(ev)
        if is_target:
            self.target = ev
        self.pos = p + 1
        return dump({"success": True, "error": None})


async def run_item(ds: DeepSeek, it: dict[str, Any], sp: str, skills: list, arm: str) -> dict[str, Any]:
    serve = it["serve"]
    start = serve["month_from"] - serve["long_from"]
    observes, logs_at = serve["observes"][start:], serve["logs_at"][start:]
    game = Game(observes, logs_at, (BANK / "handbook.md").read_text(encoding="utf-8"),
                {name: files for name, _, files in skills})
    messages: list[dict[str, Any]] = [{"role": "system", "content": sp},
                                      {"role": "user", "content": continue_prompt(observes[0])}]
    usage = {"input": 0, "cache_read": 0, "cache_create": 0, "output": 0, "reasoning": 0, "cost": 0.0, "calls": 0}
    texts: list[str] = []
    nudges = 0
    t0 = time.perf_counter()
    for _ in range(MAX_TURNS):
        msg = await ds.chat(messages, tag=f"bench-{arm}", tools=tools(bool(skills)))
        u = msg["_usage"]
        cached = u.get("cached") or 0
        usage["input"] += (u.get("prompt") or 0) - cached
        usage["cache_read"] += cached
        usage["output"] += u.get("completion") or 0
        usage["reasoning"] += u.get("reasoning") or 0
        usage["cost"] += float(u.get("cost") or 0.0)
        usage["calls"] += 1
        calls = msg.get("tool_calls") or []
        am: dict[str, Any] = {"role": "assistant", "content": msg.get("content") or ""}
        if calls:
            am["tool_calls"] = calls
        if msg.get("reasoning_details"):
            am["reasoning_details"] = msg["reasoning_details"]
        elif msg.get("reasoning_content"):
            am["reasoning_content"] = msg["reasoning_content"]  # NIM: thinking goes back as DeepSeek's API expects
        messages.append(am)
        if msg.get("content"):
            texts.append(msg["content"][:400])
        if not calls:
            nudges += 1
            if nudges > 2:
                break
            messages.append({"role": "user", "content": continue_prompt(observes[min(game.pos, len(observes) - 1)])})
            continue
        for c in calls:
            fn = c.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except ValueError:
                args = {}
            out = game.call(str(fn.get("name")), args if isinstance(args, dict) else {})
            messages.append({"role": "tool", "tool_call_id": c.get("id"), "content": out})
            if game.target:
                break
        if game.target:
            break
    tgt = game.target
    return {"id": it["id"], "choice": tgt["choice"] if tgt else None, "notes": tgt.get("notes") if tgt else None,
            "done": bool(tgt), "skill_reads": [e for e in game.record if e.get("tool") == "skill_tool"],
            "log_calls": sum(1 for e in game.record if e.get("tool") == "check_latest_logs"),
            "handbook_calls": sum(1 for e in game.record if e.get("tool") == "show_employee_handbook"),
            "invalid": sum(1 for e in game.record if e.get("invalid")), "prefix_steps": len(observes) - 1,
            "seconds": round(time.perf_counter() - t0, 1), "usage": usage, "texts": texts[-3:],
            "tools": [e["tool"] for e in game.record]}


def load_items() -> dict[str, dict[str, Any]]:
    if not ITEMS.exists():
        DATA.mkdir(parents=True, exist_ok=True)
        with gzip.open(BANK / "bank-items.jsonl.gz", "rt") as src, ITEMS.open("w") as dst:
            for line in src:
                dst.write(line)
    return {json.loads(x)["id"]: json.loads(x) for x in ITEMS.open()}


async def run(variant: str, name: str, ids_file: Path, limit: int | None, slots: int) -> None:
    items = load_items()
    ids = ids_file.read_text().split()
    if limit:
        ids = ids[:limit]
    arm_dir = RUNS / name
    arm_dir.mkdir(parents=True, exist_ok=True)
    instruction, skills = load_variant(variant)
    sp = system_prompt(instruction, skills, "official")
    (arm_dir / "system_prompt.md").write_text(sp)
    (arm_dir / "arm.json").write_text(json.dumps({"variant": variant, "context": "month", "delivery": "official",
                                                  "model": "deepseek-v4-flash", "backend": BACKEND}, indent=1))
    todo = [i for i in ids if not (arm_dir / f"{i.replace(':', '_')}.json").exists()]
    print(f"{name}: {len(ids)} items, {len(todo)} to run", flush=True)
    ds = DeepSeek(concurrency=slots)
    n = 0

    async def one(iid: str) -> None:
        nonlocal n
        r = await run_item(ds, items[iid], sp, skills, name)
        (arm_dir / f"{iid.replace(':', '_')}.json").write_text(json.dumps(r, ensure_ascii=False))
        n += 1
        if n % 20 == 0:
            print(f"  {n}/{len(todo)} spent {ds.spent:.4f} USD", flush=True)

    sem = asyncio.Semaphore(slots)

    async def guarded(iid: str) -> None:
        async with sem:
            await one(iid)

    try:
        await asyncio.gather(*(guarded(i) for i in todo))
    except BudgetStop as exc:
        print(f"STOP: {exc}", flush=True)
    finally:
        await ds.close()
    print(f"{name}: done; line spend (logged) {ds.spent:.4f} USD", flush=True)


def select(per_rule: int, out: Path, seed: int) -> None:
    """``per_rule`` decisive V2 items per rule with Haiku control and t13-final (else t10-countdown) answers, plus G1."""
    from score import decisive, rule_of
    items = load_items()
    hk = json.load(gzip.open(BANK / "haiku-answers.json.gz", "rt"))
    v2 = (BANK / "ids-V2.txt").read_text().split()
    g1 = (BANK / "ids-G1.txt").read_text().split()
    rng = random.Random(seed)
    chosen: list[str] = []
    for rule in ("pre_review", "skill_l4", "hr_risk", "trigger", "early_ruin", "closing", "low_health", "general"):
        pool = [i for i in v2 if rule_of(items[i]) == rule and decisive(items[i], rule)
                and i in hk["control"] and (i in hk["t13-final"] or i in hk["t10-countdown"])]
        rng.shuffle(pool)
        chosen += pool[:per_rule]
        print(f"{rule}: {min(per_rule, len(pool))} of {len(pool)}")
    g1_ok = [i for i in g1 if i in hk["control"] and i in hk["t13-final"] and i not in chosen]
    print(f"G1: {len(g1_ok)} of {len(g1)} with both Haiku arms")
    out.write_text("\n".join(chosen + g1_ok) + "\n")
    print(f"{len(chosen) + len(g1_ok)} ids -> {out}")


def haiku(arms: list[str]) -> None:
    hk = json.load(gzip.open(BANK / "haiku-answers.json.gz", "rt"))
    for arm in arms:
        d = RUNS / f"hk-{arm}"
        d.mkdir(parents=True, exist_ok=True)
        for iid, r in hk[arm].items():
            rec = {"id": iid, "choice": r["choice"], "skill_reads": [1] * r.get("skill_reads", 0),
                   "log_calls": r.get("log_calls", 0), "usage": {}}
            (d / f"{iid.replace(':', '_')}.json").write_text(json.dumps(rec))
        print(f"hk-{arm}: {len(hk[arm])} answers")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--variant", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--ids", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--slots", type=int, default=8)
    p = sub.add_parser("select")
    p.add_argument("--per-rule", type=int, default=40)
    p.add_argument("--out", required=True)
    p.add_argument("--seed", type=int, default=3)
    p = sub.add_parser("haiku")
    p.add_argument("--arms", default="control,t13-final,t10-countdown")
    a = ap.parse_args()
    if a.cmd == "run":
        asyncio.run(run(a.variant, a.name, Path(a.ids).expanduser(), a.limit, a.slots))
    elif a.cmd == "select":
        select(a.per_rule, Path(a.out).expanduser(), a.seed)
    else:
        haiku(a.arms.split(","))


if __name__ == "__main__":
    main()
