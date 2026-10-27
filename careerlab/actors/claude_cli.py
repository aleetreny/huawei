"""Claude Code headless worker that plays one episode through MCP tools itself.

The worker mirrors the official JiuwenSwarm run: the official identity prompt
(skill names + manifest instruction) as system prompt, the official task prompt,
the five game tools as its only tools, and the official continuation prompt if
it stops before the game ends. Each episode gets its own game server process
and database (competition mode: one session). User plugins, hooks, skills,
CLAUDE.md and other MCP servers are excluded so the configuration is frozen.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.episode import EpisodeResult, atomic_write_json, result_from_terminal
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal
from careerlab.truncate import StreamWatcher, summarize

PROMPTS = Path(__file__).resolve().parents[1] / "prompts"
GAME_SERVER = "career-emulator-engine"
GAME_TOOLS = [f"mcp__{GAME_SERVER}__{t}" for t in ("new_game", "observe", "take_action", "check_latest_logs", "show_employee_handbook")]


@dataclass(frozen=True)
class ClaudeWorkerConfig:
    model: str                      # alias ("haiku", "sonnet", "opus") or full id
    effort: str | None = None       # low | medium | high | xhigh | max ; None = CLI default
    skills_mode: str = "inline"     # inline: SKILL.md bodies appended to the system prompt; plugin: real Skill tool
    autocompact: str | None = None  # e.g. "100k" for a compact-context variant
    max_continues: int = 3          # official runner re-prompts a stopped agent to continue
    timeout_s: float = 7200.0
    cli_version: str = ""
    stop_at_month: int | None = None  # short game: stop the worker once it sees this month (result "truncated")

    def record(self) -> dict[str, Any]:
        fields = asdict(self)
        if fields["stop_at_month"] is None:  # keep the full-game actor id unchanged
            del fields["stop_at_month"]
        return {"kind": "claude-cli", **fields, "prompts": "official-runner@00b084a8", "tools": GAME_TOOLS,
                "isolation": "--setting-sources '' --strict-mcp-config --tools '' (or Skill) --no-session-persistence; scrubbed env",
                "game_server": "per-episode stdio, --competition, fresh CAREER_EMULATOR_DB, official engine env"}


def cli_version(settings: Settings) -> str:
    out = subprocess.run([settings.claude_executable, "--version"], capture_output=True, text=True, timeout=30)
    return out.stdout.strip()


def load_bundle(bundle_dir: Path) -> tuple[str, list[tuple[str, str]]]:
    """Return (manifest instruction, [(skill name, SKILL.md text)]) from a policy bundle."""
    manifest = json.loads((bundle_dir / "manifest.json").read_text())
    skills = []
    for skill_md in sorted((bundle_dir / "skills").glob("*/SKILL.md")):
        skills.append((skill_md.parent.name, skill_md.read_text(encoding="utf-8")))
    return str(manifest.get("instruction") or "").strip(), skills


def render_system_prompt(instruction: str, skills: list[tuple[str, str]], skills_mode: str) -> str:
    template = (PROMPTS / "identity.md").read_text(encoding="utf-8")
    names = "- " + "\n- ".join(name for name, _ in skills) if skills else "- (none)"
    text = template.format(participant_skills=names, instruction=instruction or "(no extra strategy instructions provided)")
    if skills_mode == "inline":
        for name, body in skills:
            text += f"\n\n## Skill: {name}\n\n{body}"
    return text


def build_plugin(run_dir: Path, skills: list[tuple[str, str]]) -> Path:
    plugin = run_dir / "policy-plugin"
    (plugin / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "policy", "version": "0.0.0"}))
    for name, body in skills:
        (plugin / "skills" / name).mkdir(parents=True, exist_ok=True)
        (plugin / "skills" / name / "SKILL.md").write_text(body, encoding="utf-8")
    return plugin


def worker_env() -> dict[str, str]:
    """Minimal environment for a worker process.

    The desktop app exports CLAUDE_CODE_* / CLAUDE_EFFORT / MCP_* variables; some of
    them (for example CLAUDE_CODE_EFFORT_LEVEL) take precedence over CLI flags, so
    inheriting them would silently change the frozen actor configuration.
    """
    keep = ("HOME", "PATH", "USER", "LOGNAME", "LANG", "TMPDIR", "SHELL")
    return {k: os.environ[k] for k in keep if k in os.environ}


def mcp_config(settings: Settings, spec: ServerSpec) -> dict[str, Any]:
    env = {k: v for k, v in spec.env().items() if k.startswith(("CAREER_EMULATOR", "FASTMCP"))}
    env["PATH"] = os.environ.get("PATH", "")
    return {"mcpServers": {GAME_SERVER: {"command": settings.mcp_executable, "args": spec.args(), "env": env}}}


@dataclass
class StreamSummary:
    session_ids: list[str] = field(default_factory=list)
    tool_calls: dict[str, int] = field(default_factory=dict)
    rejected_actions: int = 0
    non_game_tool_attempts: int = 0
    usage: dict[str, float] = field(default_factory=dict)
    cost_usd_list_price: float = 0.0
    turns: int = 0
    api_ms: float = 0.0
    rate_limits: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    models: dict[str, Any] = field(default_factory=dict)


def parse_stream(path: Path, summary: StreamSummary) -> None:
    pending: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        kind = msg.get("type")
        if kind == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    summary.tool_calls[name] = summary.tool_calls.get(name, 0) + 1
                    pending[block.get("id")] = name
                    if name not in GAME_TOOLS:
                        summary.non_game_tool_attempts += 1
        elif kind == "user":
            content = msg.get("message", {}).get("content", [])
            for block in content if isinstance(content, list) else []:
                if block.get("type") != "tool_result":
                    continue
                name = pending.get(block.get("tool_use_id"), "")
                text = block.get("content")
                text = text if isinstance(text, str) else json.dumps(text)
                if name.endswith("new_game"):
                    found = re.search(r'"session_id"\s*:\s*"([0-9a-f]{32})"', text)
                    if found:
                        summary.session_ids.append(found.group(1))
                if name.endswith("take_action") and '"success":false' in text.replace(" ", ""):
                    summary.rejected_actions += 1
        elif kind == "rate_limit_event":
            summary.rate_limits.append(msg.get("rate_limit_info", {}))
        elif kind == "result":
            summary.turns += int(msg.get("num_turns") or 0)
            summary.api_ms += float(msg.get("duration_api_ms") or 0)
            summary.cost_usd_list_price += float(msg.get("total_cost_usd") or 0)
            for key in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                summary.usage[key] = summary.usage.get(key, 0) + float((msg.get("usage") or {}).get(key) or 0)
            for model, info in (msg.get("modelUsage") or {}).items():
                summary.models[model] = info
            if msg.get("is_error"):
                summary.errors.append(str(msg.get("result"))[:300])


async def run_claude_episode(settings: Settings, cfg: ClaudeWorkerConfig, bundle_dir: Path, job_id: str,
                             run_dir: Path, game_root: Path | None = None,
                             mcp_override: dict[str, Any] | None = None) -> EpisodeResult:
    """Run one complete episode; the planner verifies the end state with its own client."""
    run_dir.mkdir(parents=True, exist_ok=True)
    spec = ServerSpec(f"claude-{job_id}", game_root or (run_dir / "game"), transport="stdio", competition_mode=True)
    instruction, skills = load_bundle(bundle_dir)
    system_prompt = render_system_prompt(instruction, skills, cfg.skills_mode)
    (run_dir / "system_prompt.md").write_text(system_prompt, encoding="utf-8")
    config = mcp_override or mcp_config(settings, spec)
    (run_dir / "mcp.json").write_text(json.dumps(config, indent=1))
    atomic_write_json(run_dir / "actor.json", cfg.record())
    base = [settings.claude_executable, "-p", "--setting-sources", "", "--strict-mcp-config",
            "--mcp-config", str(run_dir / "mcp.json"), "--model", cfg.model,
            "--tools", "Skill" if cfg.skills_mode == "plugin" else "",
            "--allowedTools", ",".join(GAME_TOOLS + (["Skill"] if cfg.skills_mode == "plugin" else [])),
            "--output-format", "stream-json", "--verbose", "--no-session-persistence",
            "--system-prompt", system_prompt, "--permission-mode", "dontAsk"]
    if cfg.effort:
        base += ["--effort", cfg.effort]
    if cfg.autocompact:
        base += ["--autocompact", cfg.autocompact]
    if cfg.skills_mode == "plugin":
        base += ["--plugin-dir", str(build_plugin(run_dir, skills))]
    summary = StreamSummary()
    started = time.perf_counter()
    result: EpisodeResult | None = None
    session_id: str | None = None
    prompt = (PROMPTS / "play_headless.md").read_text(encoding="utf-8")
    for attempt in range(cfg.max_continues + 1):
        stream = run_dir / f"stream-{attempt}.jsonl"
        with stream.open("w") as out, (run_dir / f"stderr-{attempt}.log").open("w") as err:
            proc = await asyncio.create_subprocess_exec(*base, prompt, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                                        cwd=str(run_dir), env=worker_env())
            (run_dir / "worker.pid").write_text(str(proc.pid))
            try:
                await asyncio.wait_for(_wait_or_cut(proc, stream, cfg.stop_at_month, summary),
                                       timeout=max(cfg.timeout_s - (time.perf_counter() - started), 1))
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                summary.errors.append("timeout")
        parse_stream(stream, summary)
        if summary.session_ids:
            session_id = summary.session_ids[0]
        if session_id is None:
            result = EpisodeResult(job_id, None, "interrupted", interruption="worker never created a game session")
            break
        verifier = ServerSpec(f"verify-{job_id}", spec.root, transport="stdio")  # same database, no competition lock
        async with GameClient(verifier, settings) as client:
            obs = await client.observe(session_id)
        if is_terminal(obs):
            result = result_from_terminal(job_id, session_id, obs)
            break
        month = int(obs.get("current_state", {}).get("time", {}).get("current_month") or 0)
        if cfg.stop_at_month and month >= cfg.stop_at_month:
            result = EpisodeResult(job_id, session_id, "truncated", survival_months=None)
            break
        if "timeout" in summary.errors:
            result = EpisodeResult(job_id, session_id, "interrupted", interruption="worker timeout")
            break
        t = obs.get("current_state", {}).get("time", {})
        prompt = (PROMPTS / "play_headless_continue.md").read_text(encoding="utf-8").format(
            session_id=session_id, year=t.get("current_year"), month=t.get("current_month"))
    if result is None:
        result = EpisodeResult(job_id, session_id, "interrupted", interruption=f"game not finished after {cfg.max_continues} continuations")
    result.wall_seconds = round(time.perf_counter() - started, 2)
    result.tool_calls = summary.tool_calls
    result.rejected_actions = summary.rejected_actions
    result.steps = summary.tool_calls.get(f"mcp__{GAME_SERVER}__take_action", 0)
    result.actor_usage = {"tokens": summary.usage, "cost_usd_list_price": round(summary.cost_usd_list_price, 4),
                          "turns": summary.turns, "api_ms": summary.api_ms, "models": summary.models,
                          "extra_sessions": max(len(set(summary.session_ids)) - 1, 0),
                          "non_game_tool_attempts": summary.non_game_tool_attempts,
                          "rate_limit_first": summary.rate_limits[0] if summary.rate_limits else None,
                          "rate_limit_last": summary.rate_limits[-1] if summary.rate_limits else None,
                          "errors": summary.errors[:10]}
    result.trajectory_path = str(run_dir / "stream-0.jsonl")
    if session_id is not None and result.outcome != "interrupted":
        result.periods = await _periods(settings, spec, session_id, run_dir, obs)
    atomic_write_json(run_dir / "result.json", asdict(result))
    return result


async def _wait_or_cut(proc: asyncio.subprocess.Process, stream: Path, stop_at_month: int | None,
                       summary: StreamSummary, poll_s: float = 2.0) -> None:
    """Wait for the worker; with `stop_at_month`, stop it as soon as its stream shows that month."""
    if not stop_at_month:
        await proc.wait()
        return
    watcher = StreamWatcher(stream)
    while proc.returncode is None:
        try:
            await asyncio.wait_for(proc.wait(), timeout=poll_s)
        except asyncio.TimeoutError:
            pass
        if proc.returncode is None and watcher.poll() >= stop_at_month:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=20)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
            summary.errors.append(f"cut at month {watcher.month}")


async def _periods(settings: Settings, spec: ServerSpec, session_id: str, run_dir: Path,
                   obs: dict[str, Any]) -> dict[str, Any] | None:
    """Review snapshots from the player's own stream plus our verifier's log read (never scored)."""
    try:
        verifier = ServerSpec(f"logs-{spec.name}", spec.root, transport="stdio")
        async with GameClient(verifier, settings) as client:
            logs = await client.logs(session_id, 5000)
        month = int(obs.get("current_state", {}).get("time", {}).get("current_month") or 0)
        return summarize(sorted(run_dir.glob("stream-*.jsonl")), list(logs.get("entries") or []), month)
    except Exception as exc:  # evidence only; never fails the episode
        return {"error": repr(exc)[:300]}
