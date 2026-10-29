"""Fake OpenAI-compatible chat server: logs every request and replies from a script (no real model)."""
import json, sys, time, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LOG = Path(sys.argv[2]); SCRIPT = Path(sys.argv[3])
lock = threading.Lock(); count = [0]


def chunk(delta, finish=None, usage=None):
    d = {"id": "fake", "object": "chat.completion.chunk", "created": int(time.time()), "model": "deepseek-v4-flash",
         "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
    if usage: d["usage"] = usage
    return ("data: " + json.dumps(d) + "\n\n").encode()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"data":[{"id":"deepseek-v4-flash","context_length":131072}]}')

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        with lock:
            n = count[0]
            if body.get("tools"): count[0] += 1
            else: n = 10**6
            with LOG.open("a") as f: f.write(json.dumps({"n": n, "path": self.path, "body": body}) + "\n")
        script = json.loads(SCRIPT.read_text()) if SCRIPT.exists() else []
        step = script[n] if n < len(script) else {"content": "DONE"}
        usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        if not body.get("stream"):
            msg = {"role": "assistant", "content": step.get("content", "")}
            if "tool" in step:
                msg["tool_calls"] = [{"id": f"call_{n}", "type": "function",
                                      "function": {"name": step["tool"], "arguments": json.dumps(step["args"])}}]
            out = {"id": "fake", "object": "chat.completion", "model": "deepseek-v4-flash", "usage": usage,
                   "choices": [{"index": 0, "message": msg, "finish_reason": "tool_calls" if "tool" in step else "stop"}]}
            data = json.dumps(out).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(chunk({"role": "assistant", "content": ""}))
        if "tool" in step:
            self.wfile.write(chunk({"tool_calls": [{"index": 0, "id": f"call_{n}", "type": "function",
                                                    "function": {"name": step["tool"], "arguments": json.dumps(step["args"])}}]}))
            self.wfile.write(chunk({}, "tool_calls", usage))
        else:
            self.wfile.write(chunk({"content": step.get("content", "DONE")}))
            self.wfile.write(chunk({}, "stop", usage))
        self.wfile.write(b"data: [DONE]\n\n")


ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
