"""Shell bridge so native Claude Code subagents can play through Bash.

Native subagents of the orchestrator session cannot attach new MCP servers, but
they can run commands. Each command below makes one tool call to a long-lived
game server reached over HTTP and prints compact JSON. Only CareerLab's own
SynthCareer server is used this way: the documented interface for the real game
is stdio, and real-game LLM actors are closed by ``lab/gate.json``.

    uv run python -m careerlab.bridge --url http://127.0.0.1:PORT/mcp new
    uv run python -m careerlab.bridge --url ... observe --session S
    uv run python -m careerlab.bridge --url ... act --session S --choice 2 --notes "why"
    uv run python -m careerlab.bridge --url ... logs --session S --count 5
    uv run python -m careerlab.bridge --url ... handbook
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from fastmcp import Client


async def _call(url: str, tool: str, args: dict) -> object:
    async with Client(url, timeout=60) as client:
        result = await client.call_tool(tool, args, raise_on_error=False)
    if result.is_error:
        return {"error": "; ".join(getattr(c, "text", "") for c in result.content)}
    if result.data is not None:
        return result.data
    text = "\n".join(getattr(c, "text", "") for c in result.content)
    try:
        return json.loads(text)
    except ValueError:
        return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="careerlab.bridge")
    parser.add_argument("--url", default=os.environ.get("CAREERLAB_BRIDGE_URL", ""))
    parser.add_argument("--log", default=os.environ.get("CAREERLAB_BRIDGE_LOG", ""), help="append every call to this JSONL file")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("new")
    sub.add_parser("handbook")
    for name in ("observe", "logs", "act"):
        p = sub.add_parser(name)
        p.add_argument("--session", required=True)
        if name == "logs":
            p.add_argument("--count", type=int, default=5)
        if name == "act":
            p.add_argument("--choice", type=int, required=True)
            p.add_argument("--notes", default="")
    args = parser.parse_args(argv)
    if not args.url.startswith("http://127.0.0.1:"):
        print(json.dumps({"error": "bridge only talks to a local CareerLab synthetic server"}))
        return 2
    tool, call_args = {
        "new": ("new_game", {}),
        "handbook": ("show_employee_handbook", {}),
        "observe": ("observe", {"session_id": getattr(args, "session", "")}),
        "logs": ("check_latest_logs", {"session_id": getattr(args, "session", ""), "count": getattr(args, "count", 5)}),
        "act": ("take_action", {"session_id": getattr(args, "session", ""), "choice": getattr(args, "choice", 0), "notes": getattr(args, "notes", "")}),
    }[args.cmd]
    start = time.perf_counter()
    out = asyncio.run(_call(args.url, tool, call_args))
    if args.log:
        with Path(args.log).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"t": time.time(), "tool": tool, "args": call_args, "ms": round(1000 * (time.perf_counter() - start), 1),
                                     "result": out}, ensure_ascii=False) + "\n")
    print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
