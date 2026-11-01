"""Faithful segments: DeepSeek plays the start of an official game with the context JiuwenSwarm gives it.

Why. The bank (``scripts/deepseek/bench.py``) asks DeepSeek one month at a time with a fresh context: the Skill is
read a few turns before each decision, the system prompt is a short English stand-in, six tools instead of 52, and
no ``top_p``. In a real run the Skill is read once at month 0 and the critical decisions come 40–500 turns later.
This script reproduces the real request instead, and plays closed-loop against the official engine:

- system prompt: JiuwenSwarm's (``jiuwen_system.txt``, recorded with a fake model in the official runner) with the
  manual's skill name, description and manifest instruction filled in where JiuwenSwarm puts them;
- tools: the 52 JiuwenSwarm tools (``jiuwen_tools.json``); first user message, per-call ``<system-reminder>`` and
  continuation message as the runner sends them (``jiuwen_msgs.json``, ``careerlab/prompts/play_headless_continue.md``);
- sampling as JiuwenSwarm sends it: temperature 0.95, top_p 0.1, tool_choice auto, streamed;
- the model's reasoning goes back in the history as ``reasoning_content`` of every assistant message that carries
  tool calls, as openjiuwen's ``base_model_client._convert_messages_to_dict`` does (in the real runs the input grows
  per call by the visible output plus the reasoning; C51 had assumed it did not come back);
- tool results as JiuwenSwarm returns them: ``str({'result': <engine text>})`` for the game tools (byte-identical
  to the recorded runs), ``success=… data=… error=…`` for ``skill_tool`` and unknown tools;
- engine: the official MCP server (``career-emulator-engine-mcp``, competition mode), one per segment.

The segment stops at the first observation of month ``--stop-month`` (default 6: the first review has been applied),
at a level change, at game over, or after 20 continuations. ``TRAMOS_NO_REASONING=1`` drops the reasoning from the
history (the first pilot ran that way by mistake; it is kept as an ablation).

    uv run python scripts/tramos/fiel.py check                      # 0 USD: template and engine checks
    uv run python scripts/tramos/fiel.py run --arm v4=lab/policies-src/deepseek/t13-read-v4/bundle \
        --arm v4loop=lab/policies-src/mejora/v4-loop/bundle --per-arm 15 --parallel 12 --budget 1.2
    uv run python scripts/tramos/fiel.py summary

Credentials come from the runner's git-ignored ``.env`` (``CAREERLAB_TARGET_ENV``) and are never printed. Every
model call is logged to ``~/careerlab-data/tramos/calls.jsonl`` (no game text); each segment to
``~/careerlab-data/tramos/segments/<arm>-<n>.json``, its full message list to ``.../<arm>-<n>.messages.json.gz`` and
its engine database to ``~/careerlab-data/tramos/engines/<arm>-<n>/`` (kept so that the session can be resumed).
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import os
import random
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
from careerlab.config import Settings  # noqa: E402
from careerlab.mcp_client import ServerSpec, phase  # noqa: E402
from careerlab.target import read_env_file  # noqa: E402

ENV = Path(os.environ.get("CAREERLAB_TARGET_ENV", Path.home() / "huawei" / "local-runs" / "official-runner" / ".env"))
DATA = Path(os.environ.get("TRAMOS_DATA", Path.home() / "careerlab-data" / "tramos"))
CALLS = DATA / "calls.jsonl"
SEGMENTS = DATA / "segments"
SLOT = str(Path.home() / "careerlab-data" / "huawei-deepseek" / "target-slots" / "slot1")  # as in the real runs
PREFIX = "mcp_career-emulator-engine_"
GAME_TOOLS = ("new_game", "observe", "take_action", "check_latest_logs", "show_employee_handbook")
MAX_CONTINUATIONS = 20  # the runner's limit
NO_REASONING = os.environ.get("TRAMOS_NO_REASONING") == "1"  # ablation: drop the reasoning from the history
MAX_CALLS = 160
CONTINUE = (REPO / "careerlab" / "prompts" / "play_headless_continue.md").read_text(encoding="utf-8")
MSGS = json.loads((HERE / "jiuwen_msgs.json").read_text(encoding="utf-8"))
TOOLS = json.loads((HERE / "jiuwen_tools.json").read_text(encoding="utf-8"))
TEMPLATE = (HERE / "jiuwen_system.txt").read_text(encoding="utf-8")


class BudgetStop(RuntimeError):
    pass


# ----------------------------------------------------------------------------- the request JiuwenSwarm builds
def load_manual(bundle: Path) -> dict[str, Any]:
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    skills = []
    for skill_md in sorted((bundle / "skills").glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        front = yaml.safe_load(text.split("---", 2)[1]) or {}
        files = {str(p.relative_to(skill_md.parent)): p.read_text(encoding="utf-8")
                 for p in sorted(skill_md.parent.rglob("*")) if p.is_file()}
        skills.append({"name": skill_md.parent.name, "description": str(front.get("description") or ""), "files": files})
    return {"instruction": str(manifest.get("instruction") or "").strip(), "skills": skills}


def system_prompt(manual: dict[str, Any], slot: str = SLOT) -> str:
    names = "\n".join(f"- {s['name']}" for s in manual["skills"])
    listing = "\n".join(f"{i}. {s['name']}: {s['description']}" for i, s in enumerate(manual["skills"]))
    return (TEMPLATE.replace("{{SLOT}}", slot).replace("{{SKILL_NAMES}}", names)
            .replace("{{INSTRUCTION}}", manual["instruction"]).replace("{{SKILL_LIST}}", listing))


def wrap_user(content: str) -> str:
    """The runner's message envelope, with the current Shanghai time as JiuwenSwarm stamps it."""
    ts = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    head, rest = MSGS["first_user"].split("\n", 1)
    env = json.loads(rest)
    env["timestamp"], env["content"] = ts, content
    return head + "\n" + json.dumps(env, ensure_ascii=False)


def first_user() -> str:
    head, rest = MSGS["first_user"].split("\n", 1)
    return wrap_user(json.loads(rest)["content"])


def continue_user(sid: str, month: int) -> str:
    return wrap_user(CONTINUE.format(session_id=sid, year=(month - 1) // 12 + 1, month=month).rstrip("\n"))


# ----------------------------------------------------------------------------- model client (streamed, like JiuwenSwarm)
class Model:
    def __init__(self, budget: float) -> None:
        env = read_env_file(ENV)
        self._base, self._key, self.model = env["API_BASE"].rstrip("/"), env["API_KEY"], env["MODEL_NAME"]
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=30.0))
        self.budget = budget
        self.spent = 0.0
        DATA.mkdir(parents=True, exist_ok=True)

    async def close(self) -> None:
        await self._client.aclose()

    async def chat(self, messages: list[dict[str, Any]], tag: str) -> dict[str, Any]:
        if self.spent >= self.budget:
            raise BudgetStop(f"spent {self.spent:.3f} >= budget {self.budget}")
        body = {"model": self.model, "messages": messages, "tools": TOOLS, "stream": True,
                "stream_options": {"include_usage": True}, "temperature": 0.95, "tool_choice": "auto", "top_p": 0.1,
                "usage": {"include": True}}
        headers = {"Authorization": f"Bearer {self._key}", "Content-Type": "application/json"}
        err = ""
        for attempt in range(6):
            t0 = time.perf_counter()
            try:
                out = await self._stream(body, headers)
                if out is not None:
                    break
                err = "empty stream"
            except (httpx.HTTPError, ValueError) as exc:
                err = f"{type(exc).__name__}: {str(exc)[:160]}".replace(self._key, "<redacted>")
            print(f"  [{tag}] attempt {attempt + 1} failed: {err}", file=sys.stderr, flush=True)
            await asyncio.sleep(min(60, 3 * 2 ** attempt))
        else:
            raise RuntimeError(f"[{tag}] model call failed: {err}")
        u = out.pop("_usage") or {}
        ptd, ctd = u.get("prompt_tokens_details") or {}, u.get("completion_tokens_details") or {}
        rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tag": tag, "provider": out.pop("_provider"),
               "prompt": u.get("prompt_tokens"), "cached": ptd.get("cached_tokens"), "completion": u.get("completion_tokens"),
               "reasoning": ctd.get("reasoning_tokens"), "cost": u.get("cost"), "s": round(time.perf_counter() - t0, 2),
               "finish": out.get("finish"), "n_tools": len(out["tool_calls"]), "text": len(out["content"])}
        self.spent += float(rec["cost"] or 0.0)
        with CALLS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        out["_rec"] = rec
        return out

    async def _stream(self, body: dict[str, Any], headers: dict[str, str]) -> dict[str, Any] | None:
        content, reasoning, calls, usage, provider, finish = [], [], {}, None, None, None
        async with self._client.stream("POST", f"{self._base}/chat/completions", headers=headers, json=body) as r:
            if r.status_code != 200:
                raise ValueError(f"HTTP {r.status_code}: {(await r.aread())[:200]!r}")
            async for line in r.aiter_lines():
                if not line.startswith("data: ") or line == "data: [DONE]":
                    continue
                d = json.loads(line[6:])
                if d.get("error"):
                    raise ValueError(f"stream error: {str(d['error'])[:200]}")
                provider = d.get("provider") or provider
                usage = d.get("usage") or usage
                for ch in d.get("choices") or []:
                    delta = ch.get("delta") or {}
                    finish = ch.get("finish_reason") or finish
                    if delta.get("content"):
                        content.append(delta["content"])
                    if delta.get("reasoning"):
                        reasoning.append(delta["reasoning"])
                    for tc in delta.get("tool_calls") or []:
                        slot = calls.setdefault(tc.get("index", 0), {"id": "", "name": "", "arguments": ""})
                        slot["id"] = tc.get("id") or slot["id"]
                        fn = tc.get("function") or {}
                        slot["name"] += fn.get("name") or ""
                        slot["arguments"] += fn.get("arguments") or ""
        if usage is None and not content and not calls:
            return None
        tool_calls = [{"id": c["id"], "type": "function", "function": {"name": c["name"], "arguments": c["arguments"]}}
                      for _, c in sorted(calls.items())]
        return {"content": "".join(content), "reasoning": "".join(reasoning), "tool_calls": tool_calls,
                "finish": finish, "_usage": usage, "_provider": provider}


# ----------------------------------------------------------------------------- one segment
class Engine:
    """The official MCP server (competition mode, its own throw-away database) behind JiuwenSwarm's tool names."""

    def __init__(self, manual: dict[str, Any], root: Path | None = None) -> None:
        self.manual = manual
        self.keep = root is not None  # a kept database lets a later run resume the same session
        self.root = root or Path(tempfile.mkdtemp(prefix="tramo-"))
        self.spec = ServerSpec("tramo", self.root, competition_mode=True)
        self.client: Any = None

    async def __aenter__(self) -> "Engine":
        from fastmcp import Client
        from fastmcp.client.transports import StdioTransport
        settings = Settings()
        transport = StdioTransport(command=settings.mcp_executable, args=self.spec.args(), env=self.spec.env(),
                                   log_file=self.root / "server.log")
        self.client = Client(transport, timeout=120)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.client.__aexit__(*exc)
        if not self.keep:
            import shutil
            shutil.rmtree(self.root, ignore_errors=True)

    async def raw(self, tool: str, args: dict[str, Any]) -> str:
        r = await self.client.call_tool(tool, args, raise_on_error=False)
        return "\n".join(getattr(c, "text", "") for c in r.content)

    async def call(self, name: str, args: dict[str, Any]) -> str:
        if name.startswith(PREFIX) and name[len(PREFIX):] in GAME_TOOLS:
            tool = name[len(PREFIX):]
            keep = {"new_game": (), "show_employee_handbook": (), "observe": ("session_id",),
                    "take_action": ("session_id", "choice", "notes"), "check_latest_logs": ("session_id", "count")}[tool]
            return str({"result": await self.raw(tool, {k: v for k, v in args.items() if k in keep})})
        if name == "skill_tool":
            skill = next((s for s in self.manual["skills"] if s["name"] == args.get("skill_name")), None)
            rel = str(args.get("relative_file_path") or "") or "SKILL.md"
            if skill is None:
                return f"success=False data=None error={'Skill not found: ' + str(args.get('skill_name'))!r}"
            if rel not in skill["files"]:
                return f"success=False data=None error={'File not found: ' + rel!r}"
            tree = f"{skill['name']}/\n" + "\n".join(
                ("└── " if i == len(skill["files"]) - 1 else "├── ") + f for i, f in enumerate(sorted(skill["files"])))
            data = {"skill_directory": f"{SLOT}/home/.jiuwenswarm-instances/career_emu/agent/workspace/skills/{skill['name']}",
                    "skill_content": skill["files"][rel], "directory_tree": [tree], "directory_tree_truncated": False,
                    "discovered_skill_names": [], "discovered_skill_names_truncated": False}
            return f"success=True data={data!r} error=None"
        if any(t["function"]["name"] == name for t in TOOLS):  # a real JiuwenSwarm tool we do not emulate (rare: C70)
            return f"success=False data=None error={'Tool unavailable in this environment: ' + name!r}"
        return f"success=False data=None error={'Ability not found in resource_mgr: ' + name!r}"


def parse_result(text: str) -> dict[str, Any] | None:
    import ast
    try:
        inner = ast.literal_eval(text)["result"]
        return json.loads(inner)
    except (ValueError, SyntaxError, KeyError, TypeError):
        return None


async def segment(model: Model, arm: str, bundle: Path, n: int, stop_month: int) -> dict[str, Any]:
    manual = load_manual(bundle)
    tag = f"{arm}-{n:03d}"
    messages: list[dict[str, Any]] = [{"role": "system", "content": system_prompt(manual)},
                                      {"role": "user", "content": first_user()}]
    rec: dict[str, Any] = {"arm": arm, "bundle": str(bundle.relative_to(REPO)), "n": n, "t0": time.time(), "calls": [],
                           "decisions": [], "stop": None, "skill_reads": [], "odd_tools": [], "continuations": 0}
    sid, last_obs, month = "", None, 1
    async with Engine(manual, DATA / "engines" / tag) as engine:
        while rec["stop"] is None:
            if len(rec["calls"]) >= MAX_CALLS:
                rec["stop"] = "max_calls"
                break
            out = await model.chat(messages + [{"role": "user", "content": MSGS["reminder"]}], tag)
            r = out["_rec"]
            r["visible"] = out["content"][:300]
            rec["calls"].append(r)
            am: dict[str, Any] = {"role": "assistant", "content": out["content"]}
            if out["tool_calls"]:
                am["tool_calls"] = out["tool_calls"]
                if out["reasoning"] and not NO_REASONING:  # openjiuwen base_model_client: only with tool calls
                    am["reasoning_content"] = out["reasoning"]
            messages.append(am)
            if not out["tool_calls"]:
                rec["continuations"] += 1
                if rec["continuations"] > MAX_CONTINUATIONS:
                    rec["stop"] = "max_continuations"
                    break
                messages.append({"role": "user", "content": continue_user(sid or "unknown", month)})
                continue
            for tc in out["tool_calls"]:
                name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"] or "{}")
                    args = args if isinstance(args, dict) else {}
                except ValueError:
                    args = {}
                res = await engine.call(name, args)
                messages.append({"role": "tool", "content": res, "tool_call_id": tc["id"]})
                short = name[len(PREFIX):] if name.startswith(PREFIX) else name
                if short == "skill_tool":
                    rec["skill_reads"].append(month)
                elif short not in GAME_TOOLS:
                    rec["odd_tools"].append(name)
                if short == "new_game":
                    sid = (parse_result(res) or {}).get("session_id") or sid
                elif short == "observe":
                    obs = parse_result(res)
                    if not obs or "current_state" not in obs:
                        continue
                    last_obs = obs
                    st = obs["current_state"]
                    month = st["time"]["current_month"]
                    level = st["status"].get("level")
                    if not st["simulation_flags"].get("alive", True):
                        rec["stop"] = "game_over"
                    elif level != "L1":
                        rec["stop"] = "promoted"
                    elif month >= stop_month:
                        rec["stop"] = "month"
                elif short == "take_action" and last_obs:
                    ev = last_obs.get("current_event") or {}
                    rec["decisions"].append({"month": month, "title": ev.get("title"), "phase": phase(last_obs),
                                             "n_choices": len(last_obs.get("choices") or []), "choice": args.get("choice"),
                                             "notes": str(args.get("notes") or "")[:300],
                                             "status": last_obs["current_state"]["status"], "result": res[:200]})
        # what the harness (not the model) reads after the stop: the run's own log entries
        if sid:
            logs = parse_result(str({"result": await engine.raw("check_latest_logs", {"session_id": sid, "count": 200})}))
            rec["logs"] = (logs or {}).get("entries")
    rec["session_id"] = sid
    rec["final"] = last_obs["current_state"] if last_obs else None
    rec["seconds"] = round(time.time() - rec["t0"], 1)
    rec["cost"] = round(sum(float(c["cost"] or 0) for c in rec["calls"]), 5)
    SEGMENTS.mkdir(parents=True, exist_ok=True)
    (SEGMENTS / f"{tag}.json").write_text(json.dumps(rec, ensure_ascii=False))
    with gzip.open(SEGMENTS / f"{tag}.messages.json.gz", "wt", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False)
    return rec


async def run(arms: list[tuple[str, Path]], per_arm: int, parallel: int, budget: float, stop_month: int,
              start: int) -> None:
    model = Model(budget)
    jobs = [(arm, bundle, start + i) for i in range(per_arm) for arm, bundle in arms]  # interleaved by arm
    jobs = [j for j in jobs if not (SEGMENTS / f"{j[0]}-{j[2]:03d}.json").exists()]
    print(f"{len(jobs)} segments to run, budget {budget} USD", flush=True)
    sem = asyncio.Semaphore(parallel)
    done = 0

    async def one(arm: str, bundle: Path, n: int) -> None:
        nonlocal done
        async with sem:
            if model.spent >= budget * 0.97:
                return
            await asyncio.sleep(random.random() * 2)
            try:
                rec = await segment(model, arm, bundle, n, stop_month)
            except BudgetStop:
                print(f"  {arm}-{n:03d}: budget stop", flush=True)
                return
            except Exception as exc:  # operational problem: logged, never scored
                print(f"  {arm}-{n:03d}: ERROR {type(exc).__name__}: {str(exc)[:200]}", flush=True)
                return
            done += 1
            f = rec["final"] or {}
            st = f.get("status") or {}
            print(f"  {arm}-{n:03d}: {rec['stop']} m{(f.get('time') or {}).get('current_month')} {st.get('level')} "
                  f"S{st.get('skill')} N{st.get('network')} O{st.get('output')} H{st.get('health')} "
                  f"calls {len(rec['calls'])} {rec['cost']:.4f} USD {rec['seconds']:.0f}s | spent {model.spent:.3f}",
                  flush=True)

    try:
        await asyncio.gather(*(one(*j) for j in jobs))
    finally:
        await model.close()
    print(f"done: {done} segments, spent {model.spent:.4f} USD", flush=True)


# ----------------------------------------------------------------------------- checks (0 USD)
def check() -> None:
    rows = [json.loads(x) for x in open(Path.home() / "careerlab-data/comprobante/fake/multi2/requests.jsonl")]
    rows = [r.get("body", r) for r in rows if r.get("body", r).get("tools")]
    probe = {"instruction": "Probe instruction line.", "skills": [{"name": "career-probe", "files": {},
             "description": "Probe skill for the career game (runner mechanics test with a fake model; never submitted)."}]}
    slot = str(Path.home() / "careerlab-data/formato/slot-fake")
    print("system prompt identical to the recorded one:", system_prompt(probe, slot) == rows[-1]["messages"][0]["content"])
    print("tools identical:", TOOLS == rows[-1]["tools"])
    print("reminder identical:", MSGS["reminder"] == rows[-1]["messages"][-1]["content"])
    first = rows[-1]["messages"][1]["content"]
    print("first message identical but for the timestamp:", first_user()[:60] == first[:60] and len(first_user()) == len(first))

    async def engine_check() -> None:
        async with Engine(probe) as e:
            sid = (parse_result(await e.call(PREFIX + "new_game", {})) or {}).get("session_id")
            obs = await e.call(PREFIX + "observe", {"session_id": sid, "call_goal": "x"})
            import re
            old_sid = re.search(r"[0-9a-f]{32}", rows[-1]["messages"][3]["content"]).group()
            recorded = rows[-1]["messages"][5]["content"].replace(old_sid, sid)
            print("first observation identical to the recorded one:", obs == recorded)
            print("second new_game:", (await e.call(PREFIX + "new_game", {}))[:100])
            print("unknown tool:", await e.call("mcp_career-emlator-egine_take_ation", {}))
    asyncio.run(engine_check())


def export(out: Path) -> None:
    """Copy every batch under DATA (segments, messages, calls) to ``out``, with home paths replaced by ``~``."""
    home = str(Path.home())
    for batch in sorted(p for p in DATA.iterdir() if (p / "segments").is_dir()):
        dst = out / batch.name
        dst.mkdir(parents=True, exist_ok=True)
        for src in sorted((batch / "segments").iterdir()):
            opener = gzip.open if src.suffix == ".gz" else open
            with opener(src, "rt", encoding="utf-8") as f:
                text = f.read().replace(home, "~")
            with gzip.open(dst / (src.name if src.suffix == ".gz" else src.name + ".gz"), "wt", encoding="utf-8") as f:
                f.write(text)
        if (batch / "calls.jsonl").exists():
            with gzip.open(dst / "calls.jsonl.gz", "wt", encoding="utf-8") as f:
                f.write((batch / "calls.jsonl").read_text())
        print(f"{batch.name}: {len(list(dst.iterdir()))} files -> {dst}")


def summary() -> None:
    import collections
    by = collections.defaultdict(list)
    for p in sorted(SEGMENTS.glob("*.json")):
        r = json.loads(p.read_text())
        by[r["arm"]].append(r)
    for arm, rs in by.items():
        stops = collections.Counter(r["stop"] for r in rs)
        promoted = sum(1 for r in rs if r["stop"] == "promoted")
        cost = sum(r["cost"] for r in rs)
        calls = sum(len(r["calls"]) for r in rs)
        print(f"{arm}: n={len(rs)} promoted at 6: {promoted} ({promoted / len(rs):.0%}) stops {dict(stops)} "
              f"cost {cost:.3f} USD ({cost / len(rs):.4f}/seg), calls/seg {calls / len(rs):.1f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--arm", action="append", required=True, help="name=bundle_dir")
    p.add_argument("--per-arm", type=int, default=10)
    p.add_argument("--parallel", type=int, default=12)
    p.add_argument("--budget", type=float, required=True)
    p.add_argument("--stop-month", type=int, default=6)
    p.add_argument("--start", type=int, default=0)
    sub.add_parser("check")
    sub.add_parser("summary")
    p = sub.add_parser("export")
    p.add_argument("--out", default=str(REPO / "lab" / "data" / "deepseek" / "tramos"))
    a = ap.parse_args()
    if a.cmd == "run":
        arms = [(x.split("=", 1)[0], (REPO / x.split("=", 1)[1]).resolve()) for x in a.arm]
        asyncio.run(run(arms, a.per_arm, a.parallel, a.budget, a.stop_month, a.start))
    elif a.cmd == "check":
        check()
    elif a.cmd == "export":
        export(Path(a.out))
    else:
        summary()


if __name__ == "__main__":
    main()
