"""Programmatic client for the official Career Emulator MCP server.

Only the five official tools are called. Servers are started from the installed
``career-emulator-engine-mcp`` executable with documented options (transport,
host, port, competition mode) and the environment variables written by the
official participation runner (database path, log directory, event limits).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import socket
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from careerlab.config import OFFICIAL_ENGINE_ENV, Settings

OFFICIAL_TOOLS = ("new_game", "observe", "take_action", "check_latest_logs", "show_employee_handbook")


@dataclass
class ServerSpec:
    """One isolated game-server environment: its own database and log directory."""

    name: str
    root: Path
    transport: str = "stdio"  # "stdio" or "http" (streamable-http)
    port: int | None = None
    competition_mode: bool = False
    extra_env: dict[str, str] = field(default_factory=dict)

    @property
    def db_path(self) -> Path:
        return self.root / "career_emulator.sqlite3"

    @property
    def log_dir(self) -> Path:
        return self.root / "emulator_logs"

    def env(self) -> dict[str, str]:
        self.root.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env.update(OFFICIAL_ENGINE_ENV)
        env.update(
            CAREER_EMULATOR_DB=str(self.db_path),
            CAREER_EMULATOR_LOG_DIR=str(self.log_dir),
            FASTMCP_LOG_LEVEL="WARNING",
        )
        env.update(self.extra_env)
        return env

    def args(self) -> list[str]:
        args = ["--update", "skip", "--log-level", "WARNING"]
        if self.competition_mode:
            args.append("--competition")
        if self.transport == "http":
            args += ["--transport", "streamable-http", "--host", "127.0.0.1", "--port", str(self.port), "--path", "/mcp"]
        return args

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/mcp"

    def fingerprint(self, settings: Settings) -> dict[str, Any]:
        """Environment identity recorded with every evaluation."""
        from importlib.metadata import version

        return {
            "engine": version("career-emulator-engine"),
            "dataset": version("career-emulator-techarena"),
            "fastmcp": version("fastmcp"),
            "engine_env": dict(OFFICIAL_ENGINE_ENV),
            "split": "dev",
            "competition_mode": self.competition_mode,
        }


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class HttpServer:
    """A long-lived HTTP game server process for one ServerSpec."""

    def __init__(self, spec: ServerSpec, settings: Settings):
        if spec.transport != "http":
            raise ValueError("HttpServer needs an http ServerSpec")
        self.spec = spec
        self.settings = settings
        self.proc: subprocess.Popen[bytes] | None = None

    def start(self, timeout_s: float = 30.0) -> "HttpServer":
        if self.spec.port is None:
            self.spec.port = free_port()
        self.spec.root.mkdir(parents=True, exist_ok=True)
        log = open(self.spec.root / "server.log", "ab")
        self.proc = subprocess.Popen(
            [self.settings.mcp_executable, *self.spec.args()],
            env=self.spec.env(),
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError(f"MCP server {self.spec.name} exited with {self.proc.returncode}")
            try:
                with socket.create_connection(("127.0.0.1", self.spec.port), timeout=0.5):
                    return self
            except OSError:
                time.sleep(0.1)
        raise TimeoutError(f"MCP server {self.spec.name} did not open port {self.spec.port}")

    def stop(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def __enter__(self) -> "HttpServer":
        return self.start()

    def __exit__(self, *exc: object) -> None:
        self.stop()


class ToolError(RuntimeError):
    """The server answered with an MCP error result."""


@dataclass
class CallStats:
    calls: dict[str, int] = field(default_factory=dict)
    seconds: dict[str, float] = field(default_factory=dict)
    errors: int = 0
    ambiguous_actions: int = 0
    retried_actions: int = 0

    def add(self, tool: str, seconds: float) -> None:
        self.calls[tool] = self.calls.get(tool, 0) + 1
        self.seconds[tool] = self.seconds.get(tool, 0.0) + seconds


class GameClient:
    """Persistent MCP connection; one client may serve many sessions."""

    def __init__(self, spec: ServerSpec, settings: Settings, call_timeout_s: float = 60.0):
        self.spec = spec
        self.settings = settings
        self.call_timeout_s = call_timeout_s
        self.stats = CallStats()
        self._client: Client | None = None

    async def __aenter__(self) -> "GameClient":
        if self.spec.transport == "http":
            transport: Any = self.spec.url
        else:
            transport = StdioTransport(
                command=self.settings.mcp_executable,
                args=self.spec.args(),
                env=self.spec.env(),
                log_file=self.spec.root / "stdio-server.log",
            )
        self._client = Client(transport, timeout=self.call_timeout_s)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._client is not None:
            await self._client.__aexit__(*exc)

    def view(self) -> "GameClient":
        """A view sharing this connection but keeping its own per-episode statistics."""
        clone = object.__new__(GameClient)
        clone.__dict__.update(self.__dict__)
        clone.stats = CallStats()
        return clone

    async def call(self, tool: str, args: dict[str, Any] | None = None, timeout_s: float | None = None) -> Any:
        if tool not in OFFICIAL_TOOLS:
            raise ValueError(f"{tool} is not an official tool")
        assert self._client is not None, "client not connected"
        start = time.perf_counter()
        try:
            result = await self._client.call_tool(tool, args or {}, timeout=timeout_s or self.call_timeout_s, raise_on_error=False)
        finally:
            self.stats.add(tool, time.perf_counter() - start)
        if result.is_error:
            self.stats.errors += 1
            raise ToolError("; ".join(getattr(c, "text", str(c)) for c in result.content))
        if result.data is not None:
            data = result.data
            if isinstance(data, dict) and set(data) == {"result"} and tool == "show_employee_handbook":
                return data["result"]
            return data
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        try:
            return json.loads(text)
        except ValueError:
            return text

    async def new_game(self) -> str:
        return (await self.call("new_game"))["session_id"]

    async def observe(self, session_id: str) -> dict[str, Any]:
        obs = await self.call("observe", {"session_id": session_id})
        state = obs.get("current_state") if isinstance(obs, dict) else None
        if not isinstance(state, dict) or ("error" in state and "time" not in state):
            raise ToolError(f"observe failed: {str(obs)[:300]}")
        return obs

    async def logs(self, session_id: str, count: int = 10) -> dict[str, Any]:
        return await self.call("check_latest_logs", {"session_id": session_id, "count": count})

    async def handbook(self) -> str:
        return await self.call("show_employee_handbook")

    async def take_action(self, session_id: str, choice: int, notes: str, before: dict[str, Any]) -> "ActionResult":
        """Apply one choice; if the reply is ambiguous, observe before any retry.

        A lost reply does not prove the action was not applied. We compare the
        state fingerprint and the latest log entry with the pre-action values;
        only an unchanged state is retried, and only once.
        """
        args = {"session_id": session_id, "choice": int(choice), "notes": notes}
        before_fp = fingerprint(before)
        for attempt in (1, 2):
            try:
                reply = await self.call("take_action", args)
                return ActionResult(applied=bool(reply.get("success")), reply=reply, attempts=attempt)
            except (asyncio.TimeoutError, TimeoutError, ConnectionError, OSError, ToolError) as exc:
                self.stats.ambiguous_actions += 1
                after = await self.observe(session_id)
                if fingerprint(after) != before_fp:
                    return ActionResult(applied=True, reply={"success": True, "inferred": True, "error": repr(exc)}, attempts=attempt, ambiguous=True)
                if attempt == 1:
                    self.stats.retried_actions += 1
                    continue
                return ActionResult(applied=False, reply={"success": False, "error": repr(exc)}, attempts=attempt, ambiguous=True)
        raise AssertionError("unreachable")


@dataclass
class ActionResult:
    applied: bool
    reply: dict[str, Any]
    attempts: int = 1
    ambiguous: bool = False


# ---------------------------------------------------------------------------
# Observation helpers (structure as returned by the official observe tool)
# ---------------------------------------------------------------------------

def fingerprint(obs: dict[str, Any]) -> str:
    state = obs.get("current_state", {})
    event = obs.get("current_event") or {}
    key = {
        "time": state.get("time"),
        "status": state.get("status"),
        "flags": state.get("simulation_flags"),
        "title": event.get("title"),
        "description": event.get("description"),
        "remaining_energy": event.get("remaining_energy"),
        "choices": obs.get("choices"),
        "events": obs.get("events"),
    }
    return hashlib.sha256(json.dumps(key, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def is_terminal(obs: dict[str, Any]) -> bool:
    flags = obs.get("current_state", {}).get("simulation_flags", {})
    return bool(obs.get("ending_score")) or flags.get("alive") is False or flags.get("failed") is True


def month_index(obs: dict[str, Any]) -> int:
    """Months elapsed in the career clock, 1-based (year 1 month 1 -> 1)."""
    t = obs.get("current_state", {}).get("time", {})
    return int(t.get("current_month") or 0)


def phase(obs: dict[str, Any]) -> str:
    event = obs.get("current_event") or {}
    if "energy_budget" in event or "remaining_energy" in event:
        return "energy"
    if "max_selections" in event:
        return "main_action"
    if event.get("document"):
        return "document"
    if is_terminal(obs):
        return "terminal"
    return "event"
