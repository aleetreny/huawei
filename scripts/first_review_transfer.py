"""Isolated, quota-limited LLM comparison over a six-month research horizon.

Only the official five game tools reach the game. The bridge journals public
responses and refuses actions beyond the study horizon. No research lookup,
catalogue, filesystem tools or central registry is available to the actor.
"""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from careerlab.actors.claude_cli import (
    ClaudeWorkerConfig, GAME_SERVER, GAME_TOOLS, StreamSummary, cli_version,
    load_bundle, parse_stream, render_system_prompt, worker_env,
)
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, month_index
from careerlab.store import bundle_hash

ORIGIN = "matteotransfer"
WINDOW = 6
QUOTA_CAP = .80
WEEK_CAP = .75
MODEL = "haiku"


def stamp():
    return datetime.now(timezone.utc).isoformat()


def settings(root):
    return Settings(origin=ORIGIN, data_dir=root, lab_dir=root / "lab",
        claude_executable="/Users/matteozabban/.local/bin/claude",
        mcp_executable=str(REPO / ".venv/bin/career-emulator-engine-mcp"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class WindowBridge:
    def __init__(self, client, run_dir):
        self.client, self.root = client, run_dir

    def record(self, tool, args, result, **extra):
        with (self.root / "public-tools.jsonl").open("a") as f:
            f.write(json.dumps({"at": stamp(), "tool": tool, "args": args, "result": result, **extra}, ensure_ascii=False) + "\n")

    async def new_game(self):
        if (self.root / "session.json").exists():
            return {"error": "A research session already exists; reuse its session_id."}
        sid = await self.client.new_game()
        result = {"session_id": sid}
        atomic_write_json(self.root / "session.json", result)
        self.record("new_game", {}, result)
        return result

    async def observe(self, session_id):
        obs = await self.client.observe(session_id)
        atomic_write_json(self.root / "last-observation.json", obs)
        self.record("observe", {"session_id": session_id}, obs)
        return obs

    async def take_action(self, session_id, choice, notes=""):
        before = await self.client.observe(session_id)
        args = {"session_id": session_id, "choice": choice, "notes": notes}
        if month_index(before) > WINDOW or is_terminal(before):
            reply = {"success": False, "error": "Research horizon reached. Stop this episode."}
            self.record("take_action", args, reply, guard_blocked=True, before=before)
            return reply
        result = await self.client.take_action(session_id, choice, notes, before)
        after = await self.client.observe(session_id)
        atomic_write_json(self.root / "last-observation.json", after)
        self.record("take_action", args, result.reply, before=before, after=after,
            applied=result.applied, ambiguous=result.ambiguous, attempts=result.attempts)
        return result.reply

    async def logs(self, session_id, count=10):
        result = await self.client.logs(session_id, count)
        self.record("check_latest_logs", {"session_id": session_id, "count": count}, result)
        return result

    async def handbook(self):
        result = await self.client.handbook()
        self.record("show_employee_handbook", {}, result)
        return result


async def serve(run_dir):
    from fastmcp import FastMCP
    spec = ServerSpec(run_dir.name, run_dir / "game", competition_mode=True)
    async with GameClient(spec, settings(run_dir.parent.parent)) as client:
        bridge = WindowBridge(client, run_dir)
        app = FastMCP("six-month-research")

        @app.tool()
        async def new_game() -> dict:
            """Start one Career Survival research session."""
            return await bridge.new_game()

        @app.tool()
        async def observe(session_id: str) -> dict:
            """Read the official observation for your current session."""
            return await bridge.observe(session_id)

        @app.tool()
        async def take_action(session_id: str, choice: int, notes: str = "") -> dict:
            """Choose an offered action while inside the research horizon."""
            return await bridge.take_action(session_id, choice, notes)

        @app.tool()
        async def check_latest_logs(session_id: str, count: int = 10) -> dict:
            """Read the latest official public log entries."""
            return await bridge.logs(session_id, count)

        @app.tool()
        async def show_employee_handbook() -> str:
            """Read the official employee handbook."""
            return await bridge.handbook()

        await app.run_async(transport="stdio", show_banner=False)


def study_system(bundle):
    instruction, skills = load_bundle(bundle)
    text = render_system_prompt(instruction, skills, "inline")
    text = text.replace("finish one full career-emulator game", "complete one six-month research window")
    text = text.replace("Do not stop or ask the user before the game ends. Decide autonomously until you see an ending signal.",
        "Continue autonomously until the research stopping condition below.")
    return text + "\n\n## Research stopping condition\n" + (
        "This experiment ends at the first observation with current_month greater than 6, "
        "or when the game explicitly ends early. Stop then, without another action. "
        "This research horizon replaces the full-career stopping condition in the task and Skill. "
        "Use only your assigned strategy and the five game tools. Do not request outside information.\n")


def prepare(root):
    root.mkdir(parents=True, exist_ok=True)
    if (root / "protocol.json").exists():
        raise FileExistsError("Protocol already frozen")
    source = {"baseline": REPO / "lab/policies-src/matteo-feedback-growth/observed-growth-v1/bundle",
              "candidate": REPO / "lab/policies-src/matteo-first-review/promotion-readiness-v1/bundle"}
    for arm, path in source.items():
        shutil.copytree(path, root / "policies" / arm)
        (root / "policies" / f"{arm}-system.md").write_text(study_system(root / "policies" / arm))
    rng = random.Random(310026)
    pairs = [rng.sample(["baseline", "candidate"], 2) for _ in range(4)]
    cfg = ClaudeWorkerConfig(model=MODEL, timeout_s=600, max_continues=1, cli_version=cli_version(settings(root)))
    protocol = {"frozen_at": stamp(), "origin": ORIGIN, "horizon_months": WINDOW,
        "purpose": "exploratory mechanism transfer; not prereg-v1 race selection or full-career scoring",
        "n_per_arm": 4, "pair_schedule": pairs, "schedule_seed": 310026,
        "pairing": "time-blocked independent sessions, not matched simulator seeds",
        "primary": "promoted at first review AND alive at first observation of month 7",
        "secondary": ["promotion", "alive_through_month_6", "adherence", "tokens", "technical_interruptions"],
        "actor": cfg.record(), "harness": "first_review_transfer.py; official tools via journaled horizon bridge",
        "script_sha256": sha(Path(__file__)),
        "policy_hashes": {arm: bundle_hash(root / "policies" / arm) for arm in source},
        "system_hashes": {arm: sha(root / "policies" / f"{arm}-system.md") for arm in source},
        "environment": ServerSpec("fingerprint", root / "unused", competition_mode=True).fingerprint(settings(root)),
        "budget": {"five_hour_cap": QUOTA_CAP, "seven_day_cap": WEEK_CAP, "max_episodes": 8,
                   "billing": "personal Claude subscription; no API key; paid overage must be off"},
        "inclusion": "resolve all four balanced pairs; keep interruptions, resume same session once, do not count interrupted runs as zero",
        "claims": "descriptive only; no superiority or universal-promotion claim with four episodes per arm",
        "next_stage": "If composite improves without lower survival, propose separate frozen ablations; no unbounded extension of this block."}
    atomic_write_json(root / "protocol.json", protocol)
    shutil.copyfile(__file__, root / "runner-source.py")
    atomic_write_json(root / "status.json", {"status": "prepared", "at": stamp()})
    print(json.dumps(protocol, indent=2))


def quota_reason(info, now=None):
    now = time.time() if now is None else now
    if info.get("isUsingOverage"):
        return "Paid overage active"
    for name, cap in (("five_hour", QUOTA_CAP), ("seven_day", WEEK_CAP)):
        window = info.get("unifiedWindows", {}).get(name, {})
        if window.get("resetsAt", 0) > now and window.get("utilization", 0) >= cap:
            return f"{name} utilization {window['utilization']}; reset {window['resetsAt']}"
    if info.get("status") == "rejected":
        return "Subscription rate limit rejected"
    return None


async def preflight(root):
    cfg = settings(root)
    args = [cfg.claude_executable, "-p", "Reply READY only.", "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', "--model", MODEL, "--tools", "", "--system-prompt", "Reply READY only.",
        "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--permission-mode", "dontAsk"]
    proc = await asyncio.create_subprocess_exec(*args, cwd=root, env=worker_env(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await asyncio.wait_for(proc.communicate(), 90)
    (root / "preflight-current.jsonl").write_bytes(out)
    (root / "preflight-current-stderr.log").write_bytes(err)
    limits = []
    for line in out.decode().splitlines():
        try:
            message = json.loads(line)
        except ValueError:
            continue
        if message.get("type") == "rate_limit_event":
            limits.append(message["rate_limit_info"])
    if limits and quota_reason(limits[-1]):
        return quota_reason(limits[-1]), limits
    if proc.returncode or not limits:
        return "Preflight failed or quota metadata unavailable", limits
    return quota_reason(limits[-1]), limits


def classify(final, logs):
    terminal = is_terminal(final)
    resolved = terminal or month_index(final) > WINDOW
    if not resolved:
        return {"outcome": "interrupted", "reason": "worker stopped before research horizon"}
    state = final["current_state"]
    promoted = any(e.get("entry_type") == "promotion" for e in logs.get("entries", [])) or int(state["status"]["level"][1:]) >= 2
    alive = not terminal and month_index(final) > WINDOW
    return {"outcome": "eliminated" if terminal else "window_complete", "promotion": promoted,
        "alive_through_month_6": alive, "promotion_and_alive": promoted and alive,
        "final_month": month_index(final), "final_status": state["status"],
        "failure": state.get("simulation_flags", {}).get("failure_reason")}


async def run_episode(root, arm, pair, protocol):
    run_dir = root / "runs" / f"pair-{pair:02d}-{arm}"
    run_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "result.json"
    if result_path.exists():
        prior = json.loads(result_path.read_text())
        if prior["outcome"] != "interrupted":
            return prior
    config = {"mcpServers": {GAME_SERVER: {"command": sys.executable,
        "args": [str(Path(__file__).resolve()), "serve", "--root", str(run_dir)],
        "env": {"PATH": worker_env().get("PATH", ""), "FASTMCP_LOG_LEVEL": "WARNING"}}}}
    atomic_write_json(run_dir / "mcp.json", config)
    system = (root / "policies" / f"{arm}-system.md").read_text()
    (run_dir / "system_prompt.md").write_text(system)
    cfg = settings(root)
    base = [cfg.claude_executable, "-p", "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", str(run_dir / "mcp.json"), "--model", MODEL, "--tools", "",
        "--allowedTools", ",".join(GAME_TOOLS), "--output-format", "stream-json", "--verbose",
        "--no-session-persistence", "--system-prompt", system, "--permission-mode", "dontAsk"]
    summary = StreamSummary()
    prior_streams = sorted(run_dir.glob("stream-*.jsonl"))
    for stream in prior_streams:
        parse_stream(stream, summary)
    if len(prior_streams) >= 2:
        return json.loads(result_path.read_text())
    started = time.monotonic()
    result = {"outcome": "interrupted", "reason": "no session"}
    for attempt in range(len(prior_streams), 2):
        session_path = run_dir / "session.json"
        prompt = ("Start a new Career Survival research session. Read the handbook, print SESSION_ID, and play with your assigned Skill. "
            "Observe after acting. Stop at an early game ending or the first observation with current_month greater than 6. "
            "Do not take any action after that observation. Print WINDOW_DONE with your final public state.")
        if session_path.exists():
            sid = json.loads(session_path.read_text())["session_id"]
            prompt = f"Continue research session {sid}, without creating a game. Observe and check logs to recover context. " + prompt.split("Observe after acting.")[1]
        stream = run_dir / f"stream-{attempt}.jsonl"
        with stream.open("w") as out, (run_dir / f"stderr-{attempt}.log").open("w") as err:
            proc = await asyncio.create_subprocess_exec(*base, prompt, cwd=run_dir, env=worker_env(), stdin=subprocess.DEVNULL, stdout=out, stderr=err)
            atomic_write_json(run_dir / "worker.json", {"pid": proc.pid, "started_at": stamp(), "attempt": attempt})
            try:
                await asyncio.wait_for(proc.wait(), 600)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                result = {"outcome": "interrupted", "reason": "worker timeout"}
        parse_stream(stream, summary)
        if not session_path.exists():
            break
        sid = json.loads(session_path.read_text())["session_id"]
        verify = ServerSpec(run_dir.name + "-verify", run_dir / "game", competition_mode=False)
        async with GameClient(verify, cfg) as client:
            final, logs = await client.observe(sid), await client.logs(sid, 100)
        atomic_write_json(run_dir / "verified-final.json", final)
        atomic_write_json(run_dir / "verified-logs.json", logs)
        result = classify(final, logs)
        result["session_id"] = sid
        if result["outcome"] != "interrupted":
            break
        if summary.rate_limits and quota_reason(summary.rate_limits[-1]):
            break
    result.update(arm=arm, pair=pair, wall_seconds=round(time.monotonic() - started, 2),
        policy_hash=protocol["policy_hashes"][arm], actor_usage=asdict(summary))
    if summary.non_game_tool_attempts or len(set(summary.session_ids)) > 1:
        result.update(outcome="interrupted", reason="actor isolation violation")
    atomic_write_json(result_path, result)
    print(json.dumps({k: result.get(k) for k in ("arm", "pair", "outcome", "promotion", "alive_through_month_6", "promotion_and_alive")}), flush=True)
    return result


async def run(root):
    protocol = json.loads((root / "protocol.json").read_text())
    if protocol["script_sha256"] != sha(Path(__file__)):
        raise RuntimeError("Runner changed after protocol freeze")
    if protocol["actor"]["cli_version"] != cli_version(settings(root)):
        raise RuntimeError("CLI version changed after protocol freeze")
    for arm, value in protocol["policy_hashes"].items():
        if bundle_hash(root / "policies" / arm) != value:
            raise RuntimeError("Frozen policy changed")
    reason, limits = await preflight(root)
    atomic_write_json(root / "preflight-quota.json", {"at": stamp(), "limits": limits, "blocked": reason})
    if reason:
        atomic_write_json(root / "status.json", {"status": "quota_blocked", "at": stamp(), "reason": reason})
        print(json.dumps({"status": "quota_blocked", "reason": reason}), flush=True)
        return
    results = []
    for pair, arms in enumerate(protocol["pair_schedule"]):
        atomic_write_json(root / "status.json", {"status": "running", "at": stamp(), "pair": pair})
        pair_results = await asyncio.gather(*(run_episode(root, arm, pair, protocol) for arm in arms))
        results.extend(pair_results)
        atomic_write_json(root / "results.json", results)
        if any(r["outcome"] == "interrupted" for r in pair_results):
            atomic_write_json(root / "status.json", {"status": "interruption_requires_review", "at": stamp(), "pair": pair})
            return
        for r in pair_results:
            rate = r["actor_usage"]["rate_limits"]
            if rate and quota_reason(rate[-1]):
                atomic_write_json(root / "status.json", {"status": "quota_blocked", "at": stamp(), "pair_completed": pair})
                return
    atomic_write_json(root / "status.json", {"status": "complete", "at": stamp(), "episodes": len(results)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "run", "serve"])
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.root.resolve())
    else:
        asyncio.run(serve(args.root.resolve()) if args.command == "serve" else run(args.root.resolve()))
