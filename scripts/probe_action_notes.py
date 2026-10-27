"""Bounded public-MCP note-channel probes. No model calls or engine inspection."""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.actors.scripted import QuarterlyPlanner
from careerlab.config import Settings
from careerlab.episode import atomic_write_json
from careerlab.mcp_client import GameClient, HttpServer, ServerSpec, is_terminal, phase


def digest(data):
    return hashlib.sha256(data).hexdigest()


CASES = [("ascii", n) for n in (0, 1, 64, 999, 1000, 1001, 4096, 16000)] + [
    ("unicode", 1000), ("unicode", 1001), ("multiline", 1000), ("json", 1000)]


def note_for(run, step):
    kind, length = CASES[(step + run) % len(CASES)]
    prefix = f"NOTE_PROBE_r{run:02d}_s{step:03d}|"
    unit = {"ascii": "abcdefghij", "unicode": "è漢🙂e\u0301", "multiline": "line\n\titem\r\n", "json": '{"fact":"test","open":true}|'}[kind]
    text = (prefix + unit * (length + 1))[:max(0, length - 5)] + ("|END|" if length >= 5 else "x" * length)
    assert len(text) == length
    return {"kind": kind, "characters": length, "utf8_bytes": len(text.encode()), "text": text}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


async def run_one(root, run):
    records = []
    settings = Settings(origin="matteonotes", data_dir=root, lab_dir=root / "lab")
    spec = ServerSpec(f"notes-{run}", root / f"server{run}", transport="http", competition_mode=True)
    server = HttpServer(spec, settings)

    async def call(tool, args):
        row = {"at": datetime.now(timezone.utc).isoformat(), "tool": tool, "args": args}
        records.append(row)
        try:
            async with GameClient(spec, settings) as client:
                row["response"] = await client.call(tool, args)
            return row["response"]
        except Exception as exc:
            row["error"] = repr(exc)
            return {"probe_error": repr(exc)}

    result = {"run": run, "actions": [], "checkpoints": [], "technical_errors": []}
    try:
        server.start()
        sid = (await call("new_game", {}))["session_id"]
        result["session_id"] = sid
        obs = await call("observe", {"session_id": sid})
        actor, memory = QuarterlyPlanner(74000 + run, "risk"), {}
        for step in range(80):
            if is_terminal(obs):
                break
            decision = await actor.decide(obs, memory)
            case = note_for(run, step)
            reply = await call("take_action", {"session_id": sid, "choice": decision.choice, "notes": case["text"]})
            result["actions"].append({"step": step, "phase": phase(obs), "choice": decision.choice,
                                      "action": next(c.get("action") for c in obs["choices"] if c["choice"] == decision.choice),
                                      "case": case, "success": reply.get("success"), "reply": reply})
            obs = await call("observe", {"session_id": sid})
            if "current_state" not in obs:
                raise RuntimeError("observe unavailable; no blind action retry")
            if step in (0, 11, 23, 47, 79) or is_terminal(obs):
                checkpoint = {"after_step": step, "month": obs["current_state"]["time"]["current_month"], "logs": {}}
                for count in (0, 1, 2, 5, 10, 100, 1000):
                    checkpoint["logs"][str(count)] = await call("check_latest_logs", {"session_id": sid, "count": count})
                result["checkpoints"].append(checkpoint)
            if step == 11:
                before = await call("check_latest_logs", {"session_id": sid, "count": 1000})
                server.stop()
                server = HttpServer(spec, settings).start()
                after = await call("check_latest_logs", {"session_id": sid, "count": 1000})
                after_obs = await call("observe", {"session_id": sid})
                result["restart"] = {"logs_equal": before == after, "observation_equal": obs == after_obs,
                                     "before": before, "after": after}
                obs = after_obs
        result["ending"] = obs
        # Same game-server process, disjoint public session identity. Never inspect its DB.
        result["unknown_session_logs"] = await call("check_latest_logs", {"session_id": "0" * 32, "count": 10})
        result["technical_errors"] = [r for r in records if "error" in r]
    except Exception as exc:
        result["fatal_error"] = repr(exc)
    finally:
        server.stop()
        with gzip.open(root / f"run{run:02d}.json.gz", "wt") as stream:
            json.dump({"result": result, "public_calls": records}, stream, ensure_ascii=False)
    print(json.dumps({"run": run, "actions": len(result["actions"]), "restart": result.get("restart", {}).get("logs_equal"),
                      "fatal_error": result.get("fatal_error")}), flush=True)


async def execute(root):
    protocol = json.loads((root / "protocol.json").read_text())
    assert digest(Path(__file__).read_bytes()) == protocol["script_sha256"]
    semaphore = asyncio.Semaphore(3)
    async def bounded(run):
        async with semaphore:
            await run_one(root, run)
    await asyncio.gather(*(bounded(run) for run in range(protocol["runs"])))


def prepare(root):
    root.mkdir(parents=True, exist_ok=False)
    atomic_write_json(root / "protocol.json", {
        "name": "notes-channel-limits-v1", "runs": 12, "max_actions_per_run": 80,
        "created_at": datetime.now(timezone.utc).isoformat(), "script_sha256": digest(Path(__file__).read_bytes()),
        "actor": "quarterly-risk seeded 74000+run; never reads notes; not a promotion-strategy evaluation",
        "cases": CASES, "count_probes": [0, 1, 2, 5, 10, 100, 1000],
        "reconnect": "fresh MCP client on every call", "restart": "stop and restart own server after step11",
        "limits": ["Independent unseeded game scenarios; not paired causal text-effect test", "No LLM recall, learning or context-compaction measurement",
                   "Age measured in career steps/months, not wall-clock TTL", "No simulator files read; only public tool outputs"],
        "environment": ServerSpec("probe", root).fingerprint(Settings()),
        "dependencies": {str(p): digest(p.read_bytes()) for p in (Path("careerlab/mcp_client.py"), Path("careerlab/actors/scripted.py"))}})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["prepare", "run"])
    p.add_argument("root", type=Path)
    args = p.parse_args()
    if args.command == "prepare":
        prepare(args.root)
    else:
        asyncio.run(execute(args.root))
