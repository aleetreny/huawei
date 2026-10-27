"""Run the obedience bank (T20) with Haiku through the Claude CLI, in the official Skill-delivery form.

    uv run python scripts/transmision/runbench.py assemble --bank bank.jsonl --sit sit.jsonl --out items.jsonl --k-long 18
    uv run python scripts/transmision/runbench.py run --items items.jsonl --variant <bundle dir|control> \
        --name <arm> --context month|long [--delivery official|inline] [--tags pre_review,...] [--limit N] [--slots 8]

Each item is served by `fake_mcp.py` (the five official tools, replaying recorded steps) and, in the
official delivery, a `skill_tool` server. The system prompt is the official IDENTITY.md (skill names and
the manifest instruction) plus JiuwenSwarm's skills section (`N. name: description`); the SKILL.md body
only reaches the model if it calls `skill_tool`. The user prompt is the official continuation prompt.
Results: ~/careerlab-data/transmision/runs/<arm>/<item>.json (choice, skill reads, log calls, tokens).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "transmision"))
CLAUDE = os.environ.get("CAREERLAB_CLAUDE_EXE", str(Path.home() / "claude-2.1.303/node_modules/.bin/claude"))
PY = sys.executable
PROMPTS = REPO / "careerlab" / "prompts"
SID = "5e1f0c2a9b7d4c3e8a6f1b2d3c4e5f60"
GAME = "career-emulator-engine"
GAME_TOOLS = [f"mcp__{GAME}__{t}" for t in ("new_game", "observe", "take_action", "check_latest_logs", "show_employee_handbook")]
SKILL_TOOL = "mcp__jiuwen__skill_tool"
HANDBOOK = DATA / "handbook.md"


# ----------------------------------------------------------------------------- assemble
def assemble(bank: Path, sit: Path, out: Path, k_long: int) -> None:
    """Attach to each bank item the recorded steps before it (same game) and the logs seen at each step."""
    items = [json.loads(line) for line in bank.open()]
    want: dict[str, set[int]] = {}
    for it in items:
        key = f"{it['batch']}:{it['game']}"
        lo = min(it["month_start"], max(0, it["i"] - k_long))
        want.setdefault(key, set()).update(range(lo, it["i"] + 1))
    steps: dict[tuple[str, int], dict[str, Any]] = {}
    logs: dict[str, list[dict[str, str]]] = {}
    for line in sit.open():
        if '"log_of"' in line[:20]:
            r = json.loads(line)
            if r["log_of"] in want:
                logs[r["log_of"]] = r["logs"]
            continue
        head = json.loads(line[: line.index(', "phase"')] + "}") if ', "phase"' in line else None
        if head is None:
            continue
        key = f"{head['batch']}:{head['game']}"
        if key in want and head["i"] in want[key]:
            r = json.loads(line)
            steps[(key, r["i"])] = {"observe": r["observe"], "log_upto": r["log_upto"]}
    with out.open("w") as f:
        for it in items:
            key = f"{it['batch']}:{it['game']}"
            lg = logs.get(key, [])
            lo = min(it["month_start"], max(0, it["i"] - k_long))
            seq = [steps[(key, j)] for j in range(lo, it["i"] + 1) if (key, j) in steps]
            it["serve"] = {"long_from": lo, "month_from": it["month_start"],
                           "observes": [s["observe"] for s in seq],
                           "logs_at": [lg[: s["log_upto"]][-30:] for s in seq]}
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"{len(items)} items -> {out}")


# ----------------------------------------------------------------------------- prompts
def load_variant(variant: str) -> tuple[str, list[tuple[str, str, dict[str, str]]]]:
    """(manifest instruction, [(skill name, description, {relative path: text})])."""
    if variant == "control":
        return "", []
    import yaml
    root = Path(variant)
    manifest = json.loads((root / "manifest.json").read_text()) if (root / "manifest.json").exists() else {}
    skills = []
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        fm = yaml.safe_load(text.split("---", 2)[1]) or {}
        files = {str(p.relative_to(skill_md.parent)): p.read_text(encoding="utf-8")
                 for p in skill_md.parent.rglob("*") if p.is_file()}
        skills.append((skill_md.parent.name, str(fm.get("description") or ""), files))
    return str(manifest.get("instruction") or "").strip(), skills


def system_prompt(instruction: str, skills: list[tuple[str, str, dict[str, str]]], delivery: str) -> str:
    template = (PROMPTS / "identity.md").read_text(encoding="utf-8")
    names = "- " + "\n- ".join(name for name, _, _ in skills) if skills else "- (none)"
    text = template.format(participant_skills=names, instruction=instruction or "(no extra strategy instructions provided)")
    if delivery == "inline":
        for name, _, files in skills:
            text += f"\n\n## Skill: {name}\n\n{files['SKILL.md']}"
        return text
    if not skills:
        return text + "\n\n# Skills\n\nNo skill was selected for this task. When skill information is available, read the relevant SKILL.md using read_file.\n"
    lines = "\n\n".join(f"{i}. {name}: {desc}" for i, (name, desc, _) in enumerate(skills))
    return (text + "\n\n# Skills\n\nRead the relevant SKILL.md using read_file before execution.\n\nAvailable skills:\n"
            + lines + "\nSelect the most relevant skill by reading its SKILL.md first.")


def continue_prompt(obs: dict[str, Any]) -> str:
    t = obs["current_state"]["time"]
    return (PROMPTS / "play_headless_continue.md").read_text(encoding="utf-8").format(
        session_id=SID, year=t["current_year"], month=t["current_month"])


# ----------------------------------------------------------------------------- one item
def env() -> dict[str, str]:
    keep = ("HOME", "PATH", "USER", "LOGNAME", "LANG", "TMPDIR", "SHELL")
    return {k: os.environ[k] for k in keep if k in os.environ}


async def run_item(it: dict[str, Any], arm_dir: Path, sp: str, skills: list, context: str, delivery: str,
                   model: str, timeout_s: float) -> dict[str, Any]:
    work = arm_dir / "work" / it["id"].replace(":", "_")
    work.mkdir(parents=True, exist_ok=True)
    for p in work.glob("*"):
        p.unlink()
    serve = it["serve"]
    start = 0 if context == "long" else serve["month_from"] - serve["long_from"]
    observes, logs_at = serve["observes"][start:], serve["logs_at"][start:]
    record = work / "record.jsonl"
    item = {"record": str(record), "session_id": SID, "steps": observes, "logs_at": logs_at,
            "handbook": HANDBOOK.read_text(encoding="utf-8"),
            "skills": {name: files for name, _, files in skills}}
    (work / "item.json").write_text(json.dumps(item, ensure_ascii=False))
    servers = {GAME: {"command": PY, "args": [str(HERE / "fake_mcp.py"), "game", str(work / "item.json")]}}
    tools = list(GAME_TOOLS)
    if delivery == "official" and skills:
        servers["jiuwen"] = {"command": PY, "args": [str(HERE / "fake_mcp.py"), "skills", str(work / "item.json")]}
        tools.append(SKILL_TOOL)
    (work / "mcp.json").write_text(json.dumps({"mcpServers": servers}))
    cmd = [CLAUDE, "-p", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", str(work / "mcp.json"),
           "--model", model, "--tools", "", "--allowedTools", ",".join(tools), "--output-format", "stream-json",
           "--verbose", "--no-session-persistence", "--system-prompt", sp, "--permission-mode", "dontAsk",
           continue_prompt(observes[0])]
    t0 = time.perf_counter()
    stream = work / "stream.jsonl"
    with stream.open("w") as out, (work / "stderr.log").open("w") as err:
        proc = await asyncio.create_subprocess_exec(*cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                                    cwd=str(work), env=env())
        done = False
        while time.perf_counter() - t0 < timeout_s:
            try:
                await asyncio.wait_for(proc.wait(), timeout=1.0)
                break
            except asyncio.TimeoutError:
                pass
            if record.exists() and '"target": true' in record.read_text():
                done = True
                break
        if proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=10)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
    events = [json.loads(x) for x in record.read_text().splitlines()] if record.exists() else []
    tgt = [e for e in events if e.get("tool") == "take_action" and e.get("target")]
    usage = {"input": 0, "cache_read": 0, "cache_create": 0, "output": 0}
    rate = None
    texts: list[str] = []
    for line in stream.read_text(errors="replace").splitlines():
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if msg.get("type") == "assistant":
            u = msg.get("message", {}).get("usage") or {}
            usage["input"] += u.get("input_tokens", 0)
            usage["cache_read"] += u.get("cache_read_input_tokens", 0)
            usage["cache_create"] += u.get("cache_creation_input_tokens", 0)
            usage["output"] += u.get("output_tokens", 0)
            for b in msg.get("message", {}).get("content", []):
                if b.get("type") == "text":
                    texts.append(b["text"][:400])
        elif msg.get("type") == "rate_limit_event":
            rate = msg.get("rate_limit_info", {}).get("unifiedWindows")
    res = {"id": it["id"], "choice": tgt[0]["choice"] if tgt else None, "notes": tgt[0].get("notes") if tgt else None,
           "done": bool(tgt), "skill_reads": [e for e in events if e.get("tool") == "skill_tool"],
           "log_calls": sum(1 for e in events if e.get("tool") == "check_latest_logs"),
           "handbook_calls": sum(1 for e in events if e.get("tool") == "show_employee_handbook"),
           "prefix_steps": len(observes) - 1, "seconds": round(time.perf_counter() - t0, 1), "usage": usage,
           "rate": rate, "texts": texts[-3:]}
    (arm_dir / f"{it['id'].replace(':', '_')}.json").write_text(json.dumps(res, ensure_ascii=False))
    for p in work.glob("*"):
        if p.name not in ("record.jsonl",):
            p.unlink()
    return res


def five_hour(arm_dir: Path) -> float | None:
    best = None
    for p in sorted(arm_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        try:
            r = json.loads(p.read_text()).get("rate") or {}
        except ValueError:
            continue
        u = (r.get("five_hour") or {}).get("utilization")
        if u is not None:
            best = u if best is None else max(best, u)
    return best


async def run(items_path: Path, variant: str, name: str, context: str, delivery: str, tags: list[str] | None,
              limit: int | None, slots: int, model: str, max_five_hour: float, ids_file: Path | None,
              split: str | None) -> None:
    items = [json.loads(line) for line in items_path.open()]
    if ids_file:
        keep = set(ids_file.read_text().split())
        items = [it for it in items if it["id"] in keep]
    if tags:
        items = [it for it in items if set(tags) & set(it["tags"])]
    if split == "dev":
        items = [it for it in items if not it["holdout"]]
    elif split == "holdout":
        items = [it for it in items if it["holdout"]]
    random.Random(11).shuffle(items)
    if limit:
        items = items[:limit]
    arm_dir = DATA / "runs" / name
    arm_dir.mkdir(parents=True, exist_ok=True)
    instruction, skills = load_variant(variant)
    sp = system_prompt(instruction, skills, delivery)
    (arm_dir / "system_prompt.md").write_text(sp)
    (arm_dir / "arm.json").write_text(json.dumps({"variant": variant, "context": context, "delivery": delivery,
                                                  "model": model, "claude": CLAUDE}, indent=1))
    todo = [it for it in items if not (arm_dir / f"{it['id'].replace(':', '_')}.json").exists()]
    print(f"{name}: {len(items)} items, {len(todo)} to run", flush=True)
    sem = asyncio.Semaphore(slots)
    timeout_s = 240 if context == "month" else 900
    n = 0

    async def one(it: dict[str, Any]) -> None:
        nonlocal n
        async with sem:
            while True:
                u = five_hour(arm_dir)
                if u is None or u < max_five_hour:
                    break
                print(f"five-hour {u:.2f} >= {max_five_hour}: waiting", flush=True)
                await asyncio.sleep(120)
            r = await run_item(it, arm_dir, sp, skills, context, delivery, model, timeout_s)
            n += 1
            if n % 20 == 0:
                print(f"  {n}/{len(todo)} last={r['choice']} {r['seconds']}s 5h={(r.get('rate') or {}).get('five_hour', {}).get('utilization')}",
                      flush=True)

    await asyncio.gather(*(one(it) for it in todo))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("assemble")
    p.add_argument("--bank", required=True)
    p.add_argument("--sit", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--k-long", type=int, default=18)
    p = sub.add_parser("run")
    p.add_argument("--items", required=True)
    p.add_argument("--variant", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--context", default="month", choices=("month", "long"))
    p.add_argument("--delivery", default="official", choices=("official", "inline"))
    p.add_argument("--tags")
    p.add_argument("--split", choices=("dev", "holdout"))
    p.add_argument("--ids")
    p.add_argument("--limit", type=int)
    p.add_argument("--slots", type=int, default=8)
    p.add_argument("--model", default="haiku")
    p.add_argument("--max-five-hour", type=float, default=0.65)
    a = ap.parse_args()
    if a.cmd == "assemble":
        assemble(Path(a.bank), Path(a.sit), Path(a.out), a.k_long)
    else:
        asyncio.run(run(Path(a.items), a.variant, a.name, a.context, a.delivery,
                        a.tags.split(",") if a.tags else None, a.limit, a.slots, a.model, a.max_five_hour,
                        Path(a.ids) if a.ids else None, a.split))


if __name__ == "__main__":
    main()
