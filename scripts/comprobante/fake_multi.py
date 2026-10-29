"""Fake OpenAI-compatible model that plays the official runner with SEVERAL tool calls per reply (0 USD).

Purpose: find out whether JiuwenSwarm executes two or more tool calls from one assistant message in order,
feeds every result back before the next model call, and whether an ``observe`` issued in the same reply as a
``take_action`` already shows the state after the action. Every request body is appended to a log so the exact
history growth per decision can be measured.

    python3 fake_multi.py PORT LOGFILE [MAX_DECISIONS]

Strategy: new_game -> observe -> then every reply is [take_action(choice), observe] in one message.
On the first quarterly Energy screen it sends [take_action, take_action, observe] (three calls) once.
Stops (replies "DONE") after MAX_DECISIONS take_actions or when the game ends.
"""
import json, re, sys, time, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(sys.argv[1]); LOG = Path(sys.argv[2]); MAXD = int(sys.argv[3]) if len(sys.argv) > 3 else 60
lock = threading.Lock(); state = {"n": 0, "decisions": 0, "triple_done": False, "sid": None}


def chunk(delta, finish=None, usage=None):
    d = {"id": "fake", "object": "chat.completion.chunk", "created": int(time.time()), "model": "deepseek-v4-flash",
         "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
    if usage:
        d["usage"] = usage
    return ("data: " + json.dumps(d) + "\n\n").encode()


def last_tool_results(msgs):
    """Tool results after the last assistant message, in order, as (name, parsed_or_text)."""
    i = len(msgs) - 1
    # JiuwenSwarm appends a per-call user message ("<system-reminder> ... runtime") after the tool results
    while i >= 0 and (msgs[i].get("role") == "tool" or (msgs[i].get("role") == "user" and str(msgs[i].get("content", "")).lstrip().startswith("<system-reminder>"))):
        i -= 1
    names = {}
    if i >= 0 and msgs[i].get("role") == "assistant":
        for tc in msgs[i].get("tool_calls") or []:
            names[tc.get("id")] = (tc.get("function") or {}).get("name", "")
    out = []
    for m in msgs[i + 1:]:
        if m.get("role") != "tool":
            continue
        c = m.get("content")
        if not isinstance(c, str):
            c = json.dumps(c)
        out.append((names.get(m.get("tool_call_id"), "?"), c))
    return out


def decide(msgs):
    """Return list of tool calls [(name, args)] or None for DONE."""
    tools_seen = [n for n, _ in last_tool_results(msgs)]
    # find session id anywhere
    if state["sid"] is None:
        for m in msgs:
            c = m.get("content")
            if isinstance(c, str):
                mm = re.search(r"session_id[\"']?\s*[:=]\s*[\"']?([0-9a-f]{32})", c)
                if mm:
                    state["sid"] = mm.group(1); break
    sid = state["sid"]
    if sid is None:
        if any(m.get("role") == "assistant" and any((tc.get("function") or {}).get("name", "").endswith("new_game") for tc in m.get("tool_calls") or []) for m in msgs):
            return None  # new_game called but no sid parsed: stop
        return [("mcp_career-emulator-engine_new_game", {})]
    results = last_tool_results(msgs)
    if not results:
        return [("mcp_career-emulator-engine_observe", {"session_id": sid})]
    name, text = results[-1]
    if not name.endswith("observe"):
        return [("mcp_career-emulator-engine_observe", {"session_id": sid})]
    if state["decisions"] >= MAXD:
        return None
    low = text.lower()
    if "game over" in low or '"alive":false' in low.replace('\\', '') or '"failed":true' in low.replace('\\', '') or "ending_score" in low:
        return None
    choices = re.findall(r'\\?"choice\\?":\s*(\d+)', text)
    if not choices:
        return None
    quarterly_energy = "energy" in low and "quarter" in low and ("skill learning" in low or "network maintenance" in low)
    if quarterly_energy:
        # Network maintenance costs 1: pick its id by matching the choice text
        m = re.search(r'\\?"choice\\?":\s*(\d+),\s*\\?"action\\?":\s*\\?"Network maintenance', text, re.I)
        c = int(m.group(1)) if m else int(choices[0])
        if not state["triple_done"]:
            state["triple_done"] = True
            state["decisions"] += 2
            return [("mcp_career-emulator-engine_take_action", {"session_id": sid, "choice": c, "notes": "probe q1"}),
                    ("mcp_career-emulator-engine_take_action", {"session_id": sid, "choice": c, "notes": "probe q2"}),
                    ("mcp_career-emulator-engine_observe", {"session_id": sid})]
        state["decisions"] += 1
        return [("mcp_career-emulator-engine_take_action", {"session_id": sid, "choice": c, "notes": "probe q"}),
                ("mcp_career-emulator-engine_observe", {"session_id": sid})]
    c = int(choices[0])
    state["decisions"] += 1
    return [("mcp_career-emulator-engine_take_action", {"session_id": sid, "choice": c, "notes": f"probe d{state['decisions']}"}),
            ("mcp_career-emulator-engine_observe", {"session_id": sid})]


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"data":[{"id":"deepseek-v4-flash","context_length":131072}]}')

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        with lock:
            n = state["n"]; state["n"] += 1
            calls = decide(body.get("messages", [])) if body.get("tools") else None
            with LOG.open("a") as f:
                f.write(json.dumps({"n": n, "ts": time.time(), "reply": calls, "body": body}) + "\n")
        usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        content = "" if calls else "DONE"
        if not body.get("stream"):
            msg = {"role": "assistant", "content": content}
            if calls:
                msg["tool_calls"] = [{"id": f"call_{n}_{i}", "type": "function", "function": {"name": nm, "arguments": json.dumps(a)}}
                                     for i, (nm, a) in enumerate(calls)]
            out = {"id": "fake", "object": "chat.completion", "model": "deepseek-v4-flash", "usage": usage,
                   "choices": [{"index": 0, "message": msg, "finish_reason": "tool_calls" if calls else "stop"}]}
            data = json.dumps(out).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(chunk({"role": "assistant", "content": ""}))
        if calls:
            for i, (nm, a) in enumerate(calls):
                self.wfile.write(chunk({"tool_calls": [{"index": i, "id": f"call_{n}_{i}", "type": "function",
                                                        "function": {"name": nm, "arguments": json.dumps(a)}}]}))
            self.wfile.write(chunk({}, "tool_calls", usage))
        else:
            self.wfile.write(chunk({"content": content}))
            self.wfile.write(chunk({}, "stop", usage))
        self.wfile.write(b"data: [DONE]\n\n")


ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
