"""Fake MCP servers for the obedience bank (T20): the official game tools replaying one bank item,
and a JiuwenSwarm-like `skill_tool`. Plain JSON-RPC over stdio (no framework: starts in milliseconds).

    python fake_mcp.py game  <item.json>   # server name career-emulator-engine (same five tools and signatures)
    python fake_mcp.py skills <item.json>  # server name jiuwen: skill_tool(skill_name, relative_file_path)

The item holds the recorded steps to serve (`steps`: observe payloads, the last one is the target),
the official log entries visible before each step (`logs_at`), the handbook and the Skill files.
`take_action` advances to the next recorded step whatever the choice (the prefix only builds a real
history); every call is appended to `record`, and the choice at the target ends the item.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MODE, ITEM = sys.argv[1], Path(sys.argv[2])
item = json.loads(ITEM.read_text())
RECORD = Path(item["record"])
SID = item.get("session_id", "")
pos_file = RECORD.with_suffix(".pos")

SID_DOC = ":param session_id: UUID4 hex session id returned by ``new_game``."
GAME_TOOLS = [
    {"name": "new_game", "description": "Start a new Career Emulator session.",
     "inputSchema": {"properties": {}, "type": "object"}},
    {"name": "observe", "description": f"Observe the current state and available choices for a session.\n\n{SID_DOC}",
     "inputSchema": {"properties": {"session_id": {"type": "string"}}, "required": ["session_id"], "type": "object"}},
    {"name": "take_action",
     "description": f"Apply one choice to a Career Emulator session.\n\n{SID_DOC}\n:param choice: One-based choice id from "
                    "``observe`` choices.\n:param notes: Agent note or reasoning retained in the player log.",
     "inputSchema": {"properties": {"session_id": {"type": "string"}, "choice": {"type": "integer"},
                                    "notes": {"type": "string"}},
                     "required": ["session_id", "choice", "notes"], "type": "object"}},
    {"name": "check_latest_logs",
     "description": f"Return the last log entries for a Career Emulator session.\n\n{SID_DOC}\n:param count: Number of "
                    "recent log entries to return.",
     "inputSchema": {"properties": {"session_id": {"type": "string"}, "count": {"default": 10, "type": "integer"}},
                     "required": ["session_id"], "type": "object"}},
    {"name": "show_employee_handbook", "description": "Show the employee handbook as Markdown.",
     "inputSchema": {"properties": {}, "type": "object"}},
]
SKILL_TOOLS = [
    {"name": "skill_tool",
     "description": "Use this tool to view the skill contents of a certain skill. On success it always includes an ASCII "
                    "directory_tree of the skill root and discovered_skill_names (relative paths of nested dirs that "
                    "contain SKILL.md). To load a nested skill, call again with relative_file_path (e.g. designer/SKILL.md).",
     "inputSchema": {"type": "object", "properties": {
         "skill_name": {"type": "string", "description": "Name of the skill"},
         "relative_file_path": {"type": "string", "description": "Optional. Views a specific file within the skill "
                                "directory at the relative_file_path. Leave blank to view the main SKILL.md file."}},
         "required": ["skill_name"]}},
]


def log(event: dict) -> None:
    with RECORD.open("a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def pos() -> int:
    return int(pos_file.read_text()) if pos_file.exists() else 0


def dump(x: object) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"))


def game_call(name: str, a: dict) -> str:
    steps = item["steps"]
    p = min(pos(), len(steps) - 1)
    if name == "new_game":
        log({"tool": "new_game"})
        return dump({"error": "Competition mode: only one game session is allowed."})
    if name == "show_employee_handbook":
        log({"tool": "show_employee_handbook"})
        return item["handbook"]
    if a.get("session_id") != SID:
        return dump({"error": f"Unknown session_id: {a.get('session_id')}"})
    if name == "observe":
        log({"tool": "observe", "pos": p})
        return dump(steps[p])
    if name == "check_latest_logs":
        count = int(a.get("count") or 10)
        log({"tool": "check_latest_logs", "pos": p, "count": count})
        entries = item["logs_at"][p][-max(1, count):]
        return dump({"session_id": SID, "log_file": f"/var/log/career/{SID}.log", "count": len(entries),
                     "entries": [{"session_id": SID, **e} for e in entries]})
    if name == "take_action":
        n = len(steps[p].get("choices") or [])
        try:
            choice = int(a.get("choice"))
        except (TypeError, ValueError):
            choice = -1
        if not 1 <= choice <= n:
            log({"tool": "take_action", "pos": p, "choice": a.get("choice"), "invalid": True})
            return dump({"success": False, "error": f"Invalid choice {a.get('choice')}; expected 1..{n}"})
        target = pos() >= len(steps) - 1
        log({"tool": "take_action", "pos": p, "choice": choice, "notes": str(a.get("notes") or "")[:1000], "target": target})
        pos_file.write_text(str(p + 1))
        return dump({"success": True, "error": None})
    raise KeyError(name)


def skill_call(name: str, a: dict) -> str:
    skill_name = str(a.get("skill_name") or "")
    rel = str(a.get("relative_file_path") or "") or "SKILL.md"
    log({"tool": "skill_tool", "skill": skill_name, "path": rel, "pos": pos()})
    files = item["skills"].get(skill_name)
    if files is None:
        return dump({"success": False, "error": f"Skill not found: {skill_name}"})
    if rel not in files:
        return dump({"success": False, "error": f"File not found: {rel}"})
    tree = f"{skill_name}/\n" + "\n".join(f"  {f}" for f in sorted(files))
    return dump({"skill_directory": f"/agent/skills/{skill_name}", "skill_content": files[rel],
                 "directory_tree": tree, "discovered_skill_names": []})


def main() -> None:
    tools, call, server = (GAME_TOOLS, game_call, "career-emulator-engine") if MODE == "game" else (SKILL_TOOLS, skill_call, "jiuwen")
    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        mid, method = msg.get("id"), msg.get("method")
        if mid is None:
            continue  # notification
        if method == "initialize":
            result = {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
                      "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": server, "version": "1.0"}}
        elif method == "tools/list":
            result = {"tools": tools}
        elif method == "tools/call":
            p = msg.get("params") or {}
            try:
                text = call(p.get("name"), p.get("arguments") or {})
                result = {"content": [{"type": "text", "text": text}], "isError": False}
            except Exception as exc:  # noqa: BLE001
                result = {"content": [{"type": "text", "text": f"Error calling tool {p.get('name')!r}: {exc}"}], "isError": True}
        elif method == "ping":
            result = {}
        else:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "not found"}}) + "\n")
            sys.stdout.flush()
            continue
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
