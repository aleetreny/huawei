"""Isolation and concurrency checks that use only the five official tools.

We never open the game database to prove anything: each check creates sessions
through ``new_game`` and asks other server processes or sessions to ``observe``
them. A session visible from another process means shared storage.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec, ToolError, fingerprint


async def _visible(client: GameClient, session_id: str) -> tuple[bool, str]:
    try:
        obs = await client.observe(session_id)
    except ToolError as exc:
        return False, str(exc)[:200]
    if isinstance(obs, dict) and obs.get("current_state", {}).get("session_id") == session_id:
        return True, "observed"
    return False, str(obs)[:200]


async def check_isolation(settings: Settings, root: Path | None = None) -> dict[str, Any]:
    root = root or Path(tempfile.mkdtemp(prefix="isolation-", dir=settings.servers_dir))
    report: dict[str, Any] = {"root": str(root)}

    # T1/T2: separate database paths vs the same database path, two processes each.
    # stdio only: the docs describe development clients over standard input/output.
    a = ServerSpec("iso-a", root / "a")
    b = ServerSpec("iso-b", root / "b")
    shared_1 = ServerSpec("iso-s1", root / "shared")
    shared_2 = ServerSpec("iso-s2", root / "shared")
    async with GameClient(a, settings) as ca, GameClient(b, settings) as cb, \
            GameClient(shared_1, settings) as c1, GameClient(shared_2, settings) as c2:
        sid_a = await ca.new_game()
        report["T1_separate_db_visible_from_other_process"] = await _visible(cb, sid_a)
        sid_s = await c1.new_game()
        report["T2_same_db_visible_from_other_process"] = await _visible(c2, sid_s)

        # T3: two sessions on one server do not affect each other.
        x, y = await ca.new_game(), await ca.new_game()
        y_before = fingerprint(await ca.observe(y))
        for _ in range(6):
            obs = await ca.observe(x)
            await ca.take_action(x, obs["choices"][0]["choice"], "isolation check", before=obs)
        y_after = fingerprint(await ca.observe(y))
        report["T3_actions_on_one_session_leave_other_unchanged"] = y_before == y_after
        report["T3_distinct_session_ids"] = len({sid_a, x, y}) == 3

        # T4: concurrent calls on one connection, different sessions.
        sids = [await ca.new_game() for _ in range(8)]
        results = await asyncio.gather(*(ca.observe(s) for s in sids))
        report["T4_concurrent_observe_returns_own_session"] = all(
            r["current_state"]["session_id"] == s for r, s in zip(results, sids)
        )

    # T5: competition mode allows a single new game per server process.
    comp = ServerSpec("iso-comp", root / "comp", transport="stdio", competition_mode=True)
    async with GameClient(comp, settings) as cc:
        first = await cc.call("new_game")
        try:
            second = await cc.call("new_game")
            report["T5_competition_mode_second_new_game"] = {"first": first, "second": second}
        except ToolError as exc:
            report["T5_competition_mode_second_new_game"] = f"rejected: {str(exc)[:160]}"

    # T6: default storage without CAREER_EMULATOR_DB, two processes in different working
    # directories. Informational: our runners always set an explicit database path.
    d1, d2 = root / "cwd1", root / "cwd2"
    d1.mkdir(parents=True, exist_ok=True)
    d2.mkdir(parents=True, exist_ok=True)
    report["T6_default_db_shared_across_cwds"] = await _default_db_probe(settings, d1, d2)
    return report


async def _default_db_probe(settings: Settings, d1: Path, d2: Path) -> Any:
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport

    base_env = {k: v for k, v in os.environ.items() if not k.startswith("CAREER_EMULATOR_DB")}

    def transport(cwd: Path) -> StdioTransport:
        return StdioTransport(command=settings.mcp_executable, args=["--update", "skip", "--log-level", "WARNING"],
                              env=base_env, cwd=str(cwd), log_file=cwd / "server.log")

    async with Client(transport(d1)) as p1, Client(transport(d2)) as p2:
        sid = (await p1.call_tool("new_game", {})).data["session_id"]
        res = await p2.call_tool("observe", {"session_id": sid}, raise_on_error=False)
        visible = (not res.is_error) and isinstance(res.data, dict) and res.data.get("current_state", {}).get("session_id") == sid
        created_files = sorted(str(p.relative_to(d1)) for p in d1.rglob("*") if p.is_file() and p.name != "server.log")
        return {"visible_from_other_cwd": visible, "files_created_in_cwd": created_files[:10]}


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
