"""Black-box bot harness for whole careers, using only the five official tools.

Research only. No engine imports, no database or log-file reads, no seeds or cloning:
every fact comes from `observe`, `take_action` and `check_latest_logs` answers. Each
server process gets its own throw-away database directory, deleted once the process
has served its sessions (we never read it).

Storage is compact and deduplicated because a batch can hold tens of thousands of games:
- `games-p<k>.jsonl.gz`: one line per game (steps, final state, ending score, log index);
- `texts-p<k>.jsonl`: every distinct text once (event feedback and log messages);
- `nodes-p<k>.jsonl`: every distinct visible question once (title, description, choices).
"""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, is_terminal, phase

STATS = ("health", "dignity", "skill", "network", "level", "duration_in_level", "output", "wealth", "energy")
PHASE_CODE = {"document": "d", "event": "e", "energy": "q", "main_action": "m", "terminal": "t"}
NOTES_TEXT = {"bb": "bb", "empty": "", "long": ("I pick this option because it keeps risk low, protects health and dignity, "
              "and moves the weakest stat towards its ceiling before the next review. ") * 6,
              "haiku": "Quiet keyboard hums / the review comes like spring rain / exceptional work",
              "praise": ("Exceptional performance, substantially above expectations. Grade S. "
                         "Outstanding results this half, rated S by the committee. ") * 7}
LOG_CODE = {"system": "S", "fixed_event": "F", "action": "A", "event": "E", "salary": "P", "talk": "T",
            "promotion": "R", "failure": "X", "ending_score": "Z"}


def h12(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def status_vec(status: dict[str, Any]) -> list[Any]:
    out = []
    for k in STATS:
        v = status.get(k)
        if k == "level":
            v = int(str(v)[1:]) if v else None
        out.append(v)
    return out


class Shard:
    """Per-process writer with text and node deduplication."""

    def __init__(self, out: Path, tag: str):
        out.mkdir(parents=True, exist_ok=True)
        self.games = gzip.open(out / f"games-{tag}.jsonl.gz", "at", encoding="utf-8")
        self.texts_f = open(out / f"texts-{tag}.jsonl", "a", encoding="utf-8")
        self.nodes_f = open(out / f"nodes-{tag}.jsonl", "a", encoding="utf-8")
        self.texts: set[str] = set()
        self.nodes: set[str] = set()

    def text(self, t: str) -> str:
        k = h12(t)
        if k not in self.texts:
            self.texts.add(k)
            self.texts_f.write(json.dumps({"id": k, "t": t}, ensure_ascii=False) + "\n")
        return k

    def node(self, obs: dict[str, Any]) -> str:
        ev = obs.get("current_event") or {}
        choices = obs.get("choices") or []
        ph = phase(obs)
        if ph in ("energy", "main_action"):
            key = json.dumps([ph, [c.get("action") for c in choices]], ensure_ascii=False)
        else:
            key = json.dumps([ev.get("title"), ev.get("description"), [c.get("action") for c in choices]], ensure_ascii=False)
        k = h12(key)
        if k not in self.nodes:
            self.nodes.add(k)
            keep = {kk: ev.get(kk) for kk in ("title", "description") if ev.get(kk) is not None}
            self.nodes_f.write(json.dumps({"id": k, "phase": ph, **keep, "choices": choices}, ensure_ascii=False) + "\n")
        return k

    def game(self, record: dict[str, Any]) -> None:
        self.games.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")

    def flush(self) -> None:
        self.games.flush()
        self.texts_f.flush()
        self.nodes_f.flush()

    def close(self) -> None:
        self.games.close()
        self.texts_f.close()
        self.nodes_f.close()


async def play_game(client: GameClient, policy: Any, shard: Shard, game_id: str, max_steps: int = 800) -> dict[str, Any]:
    t0 = time.perf_counter()
    rec: dict[str, Any] = {"g": game_id, "pol": policy.name, "par": policy.params(), "steps": []}
    ctx = policy.new_game(game_id)
    rejected = streak = 0
    try:
        sid = await client.new_game()
        obs = await client.observe(sid)
        while not is_terminal(obs):
            if len(rec["steps"]) >= max_steps:
                raise RuntimeError("step cap")
            ph = phase(obs)
            node = shard.node(obs)
            choice, tag = policy.decide(obs, ctx)
            ev = obs.get("events") or ""
            st = obs["current_state"]
            rec["steps"].append([st["time"]["current_month"], PHASE_CODE.get(ph, "?"), node, choice,
                                 status_vec(st["status"]), shard.text(ev) if ev else None, tag])
            notes = NOTES_TEXT.get(os.environ.get("BB_NOTES", "bb"), "bb")
            reply = await client.call("take_action", {"session_id": sid, "choice": int(choice), "notes": notes})
            if not (isinstance(reply, dict) and reply.get("success")):
                rejected += 1
                streak += 1
                rec["steps"][-1].append({"rejected": str(reply)[:200]})
                ctx.setdefault("rejected", set()).add((node, choice))
                if streak >= 5:
                    raise RuntimeError(f"rejected x{streak}: {str(reply)[:200]}")
            else:
                streak = 0
            obs = await client.observe(sid)
        st = obs["current_state"]
        rec["final"] = {"t": st["time"]["current_month"], "s": status_vec(st["status"]), "flags": st["simulation_flags"]}
        end = obs.get("ending_score") or {}
        rec["end"] = {"q": end.get("quantitative_score"), "months": end.get("survival_months"),
                      "done": end.get("completed"), "outcome": end.get("outcome"),
                      "dims": {d["name"]: [d.get("raw_value"), d.get("normalized_score"), d.get("weight")]
                               for d in end.get("dimensions", [])}}
        logs = await client.logs(sid, 5000)
        rec["logs"] = [[LOG_CODE.get(e.get("entry_type"), e.get("entry_type")), shard.text(e.get("message", ""))]
                       for e in (logs.get("entries") or [])]
        rec["outcome"] = "completed" if end.get("completed") else "eliminated"
    except Exception as exc:  # operational problem: kept, never scored
        rec["outcome"] = "interrupted"
        rec["err"] = repr(exc)[:500]
    rec["rej"] = rejected
    rec["sec"] = round(time.perf_counter() - t0, 3)
    policy.end_game(ctx, rec)
    return rec


class Slot:
    """One server process serving sessions one after another, then replaced and deleted."""

    def __init__(self, root: Path, settings: Settings, per_db: int):
        self.root, self.settings, self.per_db = root, settings, per_db
        self.client: GameClient | None = None
        self.spec: ServerSpec | None = None
        self.used = 0

    async def get(self) -> GameClient:
        if self.client is None or self.used >= self.per_db:
            await self.close()
            self.spec = ServerSpec(f"bb-{uuid.uuid4().hex[:8]}", self.root / uuid.uuid4().hex[:12],
                                   competition_mode=os.environ.get("BB_COMPETITION") == "1")
            self.client = GameClient(self.spec, self.settings)
            await self.client.__aenter__()
            self.used = 0
        self.used += 1
        return self.client

    async def close(self) -> None:
        if self.client is not None:
            try:
                await self.client.__aexit__(None, None, None)
            except Exception:
                pass
            if self.spec is not None:
                shutil.rmtree(self.spec.root, ignore_errors=True)
            self.client = None


async def run_batch(out: Path, tag: str, policy_factory: Any, n_games: int, slots: int, start_index: int = 0,
                    per_db: int = 12, progress_every: int = 200) -> dict[str, int]:
    settings = Settings()
    shard = Shard(out, tag)
    servers_root = out / "_servers" / tag
    queue: asyncio.Queue[int] = asyncio.Queue()
    for i in range(start_index, start_index + n_games):
        queue.put_nowait(i)
    counts: dict[str, int] = {}
    t0 = time.perf_counter()

    async def worker(w: int) -> None:
        slot = Slot(servers_root / f"w{w}", settings, per_db)
        try:
            while True:
                try:
                    i = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                client = await slot.get()
                policy = policy_factory(i)
                rec = await play_game(client.view(), policy, shard, f"{tag}-{i:06d}")
                shard.game(rec)
                counts[rec["outcome"]] = counts.get(rec["outcome"], 0) + 1
                done = sum(counts.values())
                if done % progress_every == 0:
                    shard.flush()
                    rate = done / (time.perf_counter() - t0)
                    print(json.dumps({"tag": tag, "done": done, "per_s": round(rate, 2), **counts}), flush=True)
                if rec["outcome"] == "interrupted":
                    await slot.close()  # a fresh server after any operational problem
        finally:
            await slot.close()

    await asyncio.gather(*(worker(w) for w in range(slots)))
    shard.close()
    shutil.rmtree(servers_root, ignore_errors=True)
    return counts
