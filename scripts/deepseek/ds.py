"""Cheap DeepSeek harness for the DeepSeek line: one chat-completion call at a time, logged and budgeted.

The competition key is an OpenRouter key. ``API_BASE``, ``API_KEY`` and ``MODEL_NAME`` are read from the
official runner's ``.env`` (git-ignored) and never printed or written anywhere. No provider, order or
routing preference is sent (the rules forbid it); temperature defaults to JiuwenSwarm's 0.95.

Every call appends one line to ``~/careerlab-data/deepseek/calls.jsonl``: time, tag, provider that served
it, prompt / cached / completion / reasoning tokens, cost in USD (OpenRouter's usage accounting) and
latency. No game text goes in that file.

Budget guard: the line's spend is the key's usage (``GET /key``, free) minus ``LINE_START_USAGE``. A call
is refused once the logged spend reaches ``DS_STOP_USD`` (default 3.0, the point where Alejandro is asked).

    uv run python scripts/deepseek/ds.py status      # key usage and the line's spend so far
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from careerlab.target import key_status, read_env_file  # noqa: E402

ENV = Path(os.environ.get("CAREERLAB_TARGET_ENV", REPO / "local-runs" / "official-runner" / ".env"))
DATA = Path(os.environ.get("DEEPSEEK_DATA", Path.home() / "careerlab-data" / "deepseek"))
CALLS = DATA / "calls.jsonl"
LINE_START_USAGE = 0.190530584  # key usage on 27 Oct 16:20 UTC, before this line's first call
STOP_USD = float(os.environ.get("DS_STOP_USD", "3.0"))
TEMPERATURE = 0.95  # JiuwenSwarm config.yaml, models.defaults


class BudgetStop(RuntimeError):
    pass


def logged_spend() -> float:
    if not CALLS.exists():
        return 0.0
    total = 0.0
    for line in CALLS.read_text().splitlines():
        try:
            total += float(json.loads(line).get("cost") or 0.0)
        except ValueError:
            continue
    return total


def line_spend() -> dict[str, float]:
    s = key_status(ENV)
    return {"key_usage": s["usage"], "line_spend": s["usage"] - LINE_START_USAGE, "remaining": s["limit_remaining"],
            "logged": logged_spend()}


class DeepSeek:
    """Async client. ``chat`` returns the assistant message dict plus ``_usage`` and ``_meta``."""

    def __init__(self, concurrency: int = 8, stop_usd: float = STOP_USD) -> None:
        env = read_env_file(ENV)
        self._base = env["API_BASE"].rstrip("/")
        self._key = env["API_KEY"]
        self.model = env["MODEL_NAME"]
        self._sem = asyncio.Semaphore(concurrency)
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(360.0, connect=30.0))
        self._spent = logged_spend()
        self.stop_usd = stop_usd
        DATA.mkdir(parents=True, exist_ok=True)

    @property
    def spent(self) -> float:
        return self._spent

    async def close(self) -> None:
        await self._client.aclose()

    async def chat(self, messages: list[dict[str, Any]], tag: str, tools: list[dict[str, Any]] | None = None,
                   temperature: float = TEMPERATURE, max_tokens: int | None = None,
                   response_format: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._spent >= self.stop_usd:
            raise BudgetStop(f"line spend {self._spent:.3f} USD >= stop {self.stop_usd} USD")
        body: dict[str, Any] = {"model": self.model, "messages": messages, "temperature": temperature,
                                "usage": {"include": True}}
        if tools:
            body["tools"] = tools
        if max_tokens:
            body["max_tokens"] = max_tokens
        if response_format:
            body["response_format"] = response_format
        headers = {"Authorization": f"Bearer {self._key}", "Content-Type": "application/json"}
        async with self._sem:
            for attempt in range(6):
                t0 = time.perf_counter()
                try:
                    r = await self._client.post(f"{self._base}/chat/completions", headers=headers, json=body)
                except httpx.HTTPError as exc:
                    err = type(exc).__name__
                else:
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("choices"):
                            break
                        err = f"no choices: {str(data.get('error'))[:200]}"
                    else:
                        err = f"HTTP {r.status_code}: {r.text[:200]}"
                err = err.replace(self._key, "<redacted>")
                print(f"  [{tag}] attempt {attempt + 1} failed: {err}", file=sys.stderr, flush=True)
                await asyncio.sleep(min(60, 3 * 2 ** attempt))
            else:
                raise RuntimeError(f"[{tag}] DeepSeek call failed after retries")
        dt = time.perf_counter() - t0
        u = data.get("usage") or {}
        ptd = u.get("prompt_tokens_details") or {}
        ctd = u.get("completion_tokens_details") or {}
        rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tag": tag, "id": data.get("id"),
               "model": data.get("model"), "provider": data.get("provider"),
               "prompt": u.get("prompt_tokens"), "cached": ptd.get("cached_tokens"),
               "completion": u.get("completion_tokens"), "reasoning": ctd.get("reasoning_tokens"),
               "cost": u.get("cost"), "s": round(dt, 2), "finish": data["choices"][0].get("finish_reason")}
        self._spent += float(rec["cost"] or 0.0)
        with CALLS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        msg = dict(data["choices"][0]["message"])
        msg["_usage"] = rec
        return msg


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps({k: round(v, 6) for k, v in line_spend().items()}))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
