"""Compact trace of one short game: month, phase, S/N/O/H/D before each action, the choice and the player's note.

    uv run python scripts/secciones/trace.py <run_dir> [--from-month 3]
Output contains game text: keep it out of manuals and of the repo.
"""
import json
import sys
from pathlib import Path

run = Path(sys.argv[1])
start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
pending = {}
state = None
for path in sorted(run.glob("stream-*.jsonl")):
    for line in path.read_text(errors="replace").splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        for b in (m.get("message") or {}).get("content", []) if isinstance((m.get("message") or {}).get("content"), list) else []:
            if b.get("type") == "tool_use":
                pending[b["id"]] = b
            elif b.get("type") == "tool_result":
                use = pending.get(b.get("tool_use_id"), {})
                t = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"])
                if use.get("name", "").endswith("observe"):
                    try:
                        o = json.loads(t)
                    except ValueError:
                        continue
                    st = o["current_state"]["status"]
                    mo = o["current_state"]["time"]["current_month"]
                    ev = o.get("current_event") or {}
                    state = (mo, f"{st['level']} S{st['skill']} N{st['network']} O{st['output']} H{st['health']} D{st['dignity']} W{st['wealth']}",
                             ev.get("title", "")[:50], [c.get("action", "")[:60] for c in o.get("choices") or []], (o.get("events") or "")[:160])
                elif use.get("name", "").endswith("take_action") and state and state[0] >= start:
                    inp = use.get("input", {})
                    print(f"m{state[0]} {state[1]} | {state[2]}")
                    if state[4]:
                        print(f"    events: {state[4]}")
                    print(f"    -> #{inp.get('choice')} of {len(state[3])}: {state[3][inp.get('choice', 1) - 1] if state[3] and 0 < inp.get('choice', 0) <= len(state[3]) else ''}")
                    print(f"    note: {str(inp.get('notes', ''))[:200]}")
