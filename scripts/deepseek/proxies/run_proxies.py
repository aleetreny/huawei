"""Label the three saved prompt batches with local Qwen (oMLX on :8000) or a Claude model through the CLI.

    python3 -I scripts/deepseek/proxies/run_proxies.py qwen
    python3 -I scripts/deepseek/proxies/run_proxies.py sonnet5 claude-sonnet-5

Answers go to ~/careerlab-data/proxies/<who>/respuesta-<n>.json; batches already answered are skipped.
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
import sys as _sys
_sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from datapaths import proxies_dir as _proxies_dir  # noqa: E402

D = _proxies_dir()
who = sys.argv[1]
model = sys.argv[2] if len(sys.argv) > 2 else "haiku"
out = D / who
out.mkdir(parents=True, exist_ok=True)

for b in (1, 2, 3):
    dst = out / f"respuesta-{b}.json"
    if dst.exists() and dst.stat().st_size > 100:
        continue
    prompt = (D / "luna" / f"prompt-{b}.txt").read_text()
    t0 = time.time()
    if who == "qwen":
        key = json.loads((Path.home() / ".omlx/settings.json").read_text())["auth"]["api_key"]
        body = {"model": "Qwen3.6-35B-A3B-4bit", "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7, "max_tokens": 32000}
        req = urllib.request.Request("http://127.0.0.1:8000/v1/chat/completions", data=json.dumps(body).encode(),
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        text = json.load(urllib.request.urlopen(req, timeout=3600))["choices"][0]["message"]["content"]
    else:
        text = subprocess.run(["claude", "-p", "--model", model, "--output-format", "text"], input=prompt,
                              capture_output=True, text=True, timeout=1800).stdout
    dst.write_text(text)
    print(f"{who} batch {b}: {len(text)} chars in {time.time() - t0:.0f}s", flush=True)
