"""Does DeepSeek obey the one-reply-per-decision loop under the real JiuwenSwarm prompt? (~0.002 USD per call)

Rebuilds the exact request the official runner sends (system prompt captured by the Formato line with the
IDENTITY block swapped for the manual under test, the 52 tool schemas, the runner's first user message, the
per-call runtime reminder) and replays a short synthetic history: skill_tool -> new_game -> observe (real
observe results recorded in an official t13-read-v4 game). Then it lets DeepSeek reply for K turns, executing
its calls against the recorded observe sequence (the recorded game's own choices are replayed, so the state
shown is coherent only for mechanics, not for judging the decision). Records per turn: tool calls, visible
text length, reasoning tokens, note length.

    CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env uv run python scripts/comprobante/turnprobe.py \
        --bundle lab/policies-src/comprobante/cp-v1/bundle --turns 6 --out ~/careerlab-data/comprobante/turnprobe-cp1.json
"""
from __future__ import annotations

import argparse, ast, asyncio, json, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "deepseek"))
from ds import DeepSeek  # noqa: E402

FORMATO = Path.home() / "careerlab-data" / "formato"
TRACE = Path.home() / "careerlab-data" / "huawei-deepseek" / "runs" / "deepseek-pilo-f78c8b88-dff20f-00000-a1" / "events.jsonl"
REMINDER = ("<system-reminder>\nThe following context is automatically attached for this model call only.\nIt may or may not be "
            "relevant to your tasks. Do not respond to it unless it highly relevant to your task.\n\n<prompt-attachment type=\"runtime\">\n"
            "# 运行时状态\n\n- 当前模型：deepseek-v4-flash\n- 可用模型：deepseek-v4-flash\n- 当前模式：智能体模式\n- 当前语言：cn\n- 当前渠道：web\n"
            "</prompt-attachment>\n</system-reminder>")
PFX = "mcp_career-emulator-engine_"


def first_user() -> str:
    return ('你收到一条消息：\n{"source": "web", "timezone": "Asia/Shanghai", "timestamp": "' + time.strftime("%Y-%m-%d %H:%M:%S") +
            '", "preferred_response_language": "zh", "content": "## Current task\\nStart a new Career Survival Agent game. Play according to '
            'the rules in IDENTITY.md and the installed skills.\\n\\n### Recommended first steps\\n1. Call `show_employee_handbook` once to learn '
            'the rules.\\n2. Call `new_game` and print `SESSION_ID=<session_id>`.\\n3. Then loop with the core rules: `observe` → decide → '
            '`take_action` until the game ends.\\n4. When the game ends, print the full `ending_score` payload, then output `DONE`.", '
            '"files_updated_by_user": "{}", "type": "user input"}')


def load_trace():
    rows = [json.loads(l) for l in TRACE.open()]
    rows = [r for r in rows if "payload" in r and r["payload"].get("delta_kind")]
    calls = {r["payload"]["delta"]["tool_call"]["tool_call_id"]: r["payload"]["delta"]["tool_call"] for r in rows if r["kind"] == "tool_call"}
    out = []
    for r in rows:
        if r["kind"] != "tool_result":
            continue
        d = r["payload"]["delta"]
        tid = d.get("tool_call_id") or d.get("tool_call", {}).get("tool_call_id")
        tc = calls.get(tid, {})
        s = d.get("result") if isinstance(d.get("result"), str) else json.dumps(d.get("result"))
        out.append((tc.get("name", ""), tc.get("arguments", ""), s))
    return out


def system_prompt(bundle: Path) -> str:
    sp = (FORMATO / "system_prompt.txt").read_text()
    man = json.loads((bundle / "manifest.json").read_text())
    skill_dirs = sorted(p for p in (bundle / "skills").iterdir() if p.is_dir())
    name = skill_dirs[0].name
    text = (skill_dirs[0] / "SKILL.md").read_text()
    import yaml
    desc = yaml.safe_load(text.split("---", 2)[1])["description"]
    sp = sp.replace("- career-probe", f"- {name}").replace("Probe instruction line.", man["instruction"])
    sp = sp.replace("0. career-probe: Probe skill for the career game.", f"0. {name}: {desc}")
    sp = sp.replace("career-probe", name)
    return sp, name, text


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--turns", type=int, default=6)
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", type=int, default=0, help="how many recorded decisions to replay before DeepSeek takes over")
    ap.add_argument("--stop-usd", type=float, default=0.5)
    ap.add_argument("--paired", action="store_true", help="replay the recorded decisions as [take_action, observe] pairs")
    a = ap.parse_args()
    bundle = Path(a.bundle)
    sp, name, skill_text = system_prompt(bundle)
    tools = json.loads((FORMATO / "tools.json").read_text())
    trace = load_trace()
    sid = re.search(r'"session_id":"([0-9a-f]{32})"', [s for n, _, s in trace if n.endswith("new_game")][0]).group(1)
    handbook = [s for n, _, s in trace if n.endswith("show_employee_handbook")][0]
    observes = [(args, s) for n, args, s in trace if n.endswith("observe")]
    skill_result = ("success=True data={'skill_directory': '/agent/workspace/skills/" + name + "', 'skill_content': " + repr(skill_text) +
                    ", 'directory_tree': ['" + name + "/\\n└── SKILL.md'], 'directory_tree_truncated': False, 'discovered_skill_names': [], "
                    "'discovered_skill_names_truncated': False} error=None")
    msgs = [{"role": "system", "content": sp}, {"role": "user", "content": first_user()}]
    k = 0

    def call(nm, args):
        nonlocal k
        k += 1
        return {"id": f"call_{k:04d}", "type": "function", "function": {"name": nm, "arguments": json.dumps(args)}}

    def add(calls, results):
        msgs.append({"role": "assistant", "content": "", "tool_calls": calls})
        for c, r in zip(calls, results):
            msgs.append({"role": "tool", "tool_call_id": c["id"], "content": r})

    add([call("skill_tool", {"skill_name": name})], [skill_result])
    add([call(PFX + "show_employee_handbook", {})], [handbook])
    add([call(PFX + "new_game", {})], ["{'result': '{\"session_id\":\"" + sid + "\"}'}"])
    pos = 0
    add([call(PFX + "observe", {"session_id": sid})], [observes[pos][1]])
    # replay recorded decisions first (take_action with the recorded choice, then observe), as the real game did
    rec_actions = [(json.loads(args), s) for n, args, s in trace if n.endswith("take_action")]
    for i in range(a.start):
        act, res = rec_actions[i]
        if a.paired:  # history as if the model had already been pairing the two calls
            pos += 1
            add([call(PFX + "take_action", act), call(PFX + "observe", {"session_id": sid})], [res, observes[pos][1]])
        else:
            add([call(PFX + "take_action", act)], [res])
            pos += 1
            add([call(PFX + "observe", {"session_id": sid})], [observes[pos][1]])
    ds = DeepSeek(concurrency=1, stop_usd=a.stop_usd)
    log = []
    try:
        for t in range(a.turns):
            req = msgs + [{"role": "user", "content": REMINDER}]
            msg = await ds.chat(req, tag="turnprobe", tools=tools)
            calls = msg.get("tool_calls") or []
            u = msg["_usage"]
            names = [c["function"]["name"].replace(PFX, "") for c in calls]
            notes = [json.loads(c["function"]["arguments"] or "{}").get("notes") for c in calls if c["function"]["name"].endswith("take_action")]
            entry = {"turn": t, "calls": names, "content_chars": len(msg.get("content") or ""), "content": (msg.get("content") or "")[:300],
                     "reasoning_tokens": u.get("reasoning"), "completion": u.get("completion"), "prompt": u.get("prompt"),
                     "cost": u.get("cost"), "notes": notes, "pos": pos}
            log.append(entry)
            print(json.dumps(entry, ensure_ascii=False), flush=True)
            if not calls:
                msgs.append({"role": "assistant", "content": msg.get("content") or ""})
                break
            results = []
            for c in calls:
                nm = c["function"]["name"]
                if nm.endswith("take_action"):
                    pos += 1
                    results.append("{'result': '{\"success\":true,\"error\":null}'}")
                elif nm.endswith("observe"):
                    results.append(observes[min(pos, len(observes) - 1)][1])
                elif nm.endswith("check_latest_logs"):
                    results.append("{'result': '{\"session_id\":\"" + sid + "\",\"count\":0,\"entries\":[]}'}")
                elif nm == "skill_tool":
                    results.append(skill_result)
                else:
                    results.append("{'result': 'ok'}")
            msgs.append({"role": "assistant", "content": msg.get("content") or "", "tool_calls": calls})
            for c, r in zip(calls, results):
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": r})
    finally:
        await ds.close()
    Path(a.out).expanduser().write_text(json.dumps({"bundle": str(bundle), "spent": ds.spent, "log": log}, ensure_ascii=False, indent=1))
    print(f"spent {ds.spent:.4f} USD")


if __name__ == "__main__":
    asyncio.run(main())
