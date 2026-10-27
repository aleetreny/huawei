"""Per-decision trace of a Claude game stream (T20): month, phase title, chosen action, state, notes.

    python3 scripts/transmision/trace.py <run_dir> [--quarter]
"""
import json, sys
from pathlib import Path


def decisions(run_dir: Path):
    last = None
    for sp in sorted(run_dir.glob("stream-*.jsonl")):
        for line in sp.open():
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("type") == "user":
                c = m["message"]["content"]
                for b in c if isinstance(c, list) else []:
                    if b.get("type") != "tool_result":
                        continue
                    t = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"] if isinstance(x, dict))
                    try:
                        o = json.loads(t)
                    except ValueError:
                        continue
                    if isinstance(o, dict) and "current_state" in o and o.get("choices"):
                        last = o
            elif m.get("type") == "assistant":
                for b in m["message"]["content"]:
                    if b.get("type") == "tool_use" and b["name"].endswith("take_action") and last:
                        k = b["input"].get("choice")
                        ch = {c["choice"]: c["action"] for c in last["choices"]}
                        st = last["current_state"]["status"]
                        yield {"month": last["current_state"]["time"]["current_month"],
                               "title": (last.get("current_event") or {}).get("title", ""), "choice": k,
                               "action": ch.get(k, "?"), "state": st, "events": last.get("events", ""),
                               "notes": b["input"].get("notes", "")}


if __name__ == "__main__":
    q = "--quarter" in sys.argv
    for d in decisions(Path(sys.argv[1])):
        if q and not d["title"].startswith("Quarterly"):
            continue
        s = d["state"]
        print(d["month"], d["title"][:28], "->", d["action"][:40], f"H{s['health']} D{s['dignity']} S{s['skill']} N{s['network']} O{s['output']} {s['level']} W{s['wealth']}", "|", d["notes"][:110])
