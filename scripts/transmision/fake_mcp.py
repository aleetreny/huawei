"""Fake MCP servers for the obedience bank (T20): the official game tools replaying one bank item,
and a JiuwenSwarm-like `skill_tool`.

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

from fastmcp import FastMCP

MODE, ITEM = sys.argv[1], Path(sys.argv[2])
item = json.loads(ITEM.read_text())
RECORD = Path(item["record"])
SID = item["session_id"]
pos_file = RECORD.with_suffix(".pos")


def log(event: dict) -> None:
    with RECORD.open("a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def pos() -> int:
    return int(pos_file.read_text()) if pos_file.exists() else 0


def dump(x: object) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"))


if MODE == "game":
    mcp = FastMCP("career-emulator-engine")

    @mcp.tool()
    def new_game() -> str:
        """Start a new Career Emulator session."""
        log({"tool": "new_game"})
        return dump({"error": "Competition mode: only one game session is allowed."})

    @mcp.tool()
    def observe(session_id: str) -> str:
        """Observe the current state and available choices for a session.

        :param session_id: UUID4 hex session id returned by ``new_game``.
        """
        p = pos()
        log({"tool": "observe", "pos": p})
        if session_id != SID:
            return dump({"error": f"Unknown session_id: {session_id}"})
        return dump(item["steps"][min(p, len(item["steps"]) - 1)])

    @mcp.tool()
    def take_action(session_id: str, choice: int, notes: str) -> str:
        """Apply one choice to a Career Emulator session.

        :param session_id: UUID4 hex session id returned by ``new_game``.
        :param choice: One-based choice id from ``observe`` choices.
        :param notes: Agent note or reasoning retained in the player log.
        """
        p = pos()
        n = len(item["steps"][min(p, len(item["steps"]) - 1)].get("choices") or [])
        if session_id != SID:
            return dump({"success": False, "error": f"Unknown session_id: {session_id}"})
        if not 1 <= int(choice) <= n:
            log({"tool": "take_action", "pos": p, "choice": choice, "invalid": True})
            return dump({"success": False, "error": f"Invalid choice {choice}; expected 1..{n}"})
        target = p >= len(item["steps"]) - 1
        log({"tool": "take_action", "pos": p, "choice": int(choice), "notes": notes[:1000], "target": target})
        pos_file.write_text(str(p + 1))
        return dump({"success": True, "error": None})

    @mcp.tool()
    def check_latest_logs(session_id: str, count: int = 10) -> str:
        """Return the last log entries for a Career Emulator session.

        :param session_id: UUID4 hex session id returned by ``new_game``.
        :param count: Number of recent log entries to return.
        """
        p = min(pos(), len(item["steps"]) - 1)
        log({"tool": "check_latest_logs", "pos": p, "count": count})
        entries = item["logs_at"][p][-max(1, int(count)):]
        return dump({"session_id": SID, "log_file": f"/var/log/career/{SID}.log", "count": len(entries),
                     "entries": [{"session_id": SID, **e} for e in entries]})

    @mcp.tool()
    def show_employee_handbook() -> str:
        """Show the employee handbook as Markdown."""
        log({"tool": "show_employee_handbook"})
        return item["handbook"]

else:
    mcp = FastMCP("jiuwen")

    @mcp.tool()
    def skill_tool(skill_name: str, relative_file_path: str = "") -> str:
        """Use this tool to view the skill contents of a certain skill. On success it always includes an ASCII directory_tree of the skill root and discovered_skill_names (relative paths of nested dirs that contain SKILL.md). To load a nested skill, call again with relative_file_path (e.g. designer/SKILL.md).

        :param skill_name: Name of the skill
        :param relative_file_path: Optional. Views a specific file within the skill directory at the relative_file_path. Leave blank to view the main SKILL.md file.
        """
        rel = relative_file_path or "SKILL.md"
        log({"tool": "skill_tool", "skill": skill_name, "path": rel, "pos": pos()})
        files = item["skills"].get(skill_name)
        if files is None:
            return dump({"success": False, "error": f"Skill not found: {skill_name}"})
        if rel not in files:
            return dump({"success": False, "error": f"File not found: {rel}"})
        tree = f"{skill_name}/\n" + "\n".join(f"  {f}" for f in sorted(files))
        return dump({"skill_directory": f"/agent/skills/{skill_name}", "skill_content": files[rel],
                     "directory_tree": tree, "discovered_skill_names": []})

if __name__ == "__main__":
    mcp.run(show_banner=False)
