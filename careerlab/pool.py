"""Server pool with database rotation.

A game database retains only about 20 sessions (see findings.md), so each server
process serves at most ``sessions_per_db`` sessions and is then replaced by a new
process with a fresh database directory. Replacements start in the background
while the old process drains, hiding the ~1.4 s start-up cost.
"""

from __future__ import annotations

import asyncio
import itertools
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncIterator

from careerlab.config import Settings
from careerlab.mcp_client import GameClient, ServerSpec

_ids = itertools.count()


@dataclass
class Slot:
    spec: ServerSpec
    client: GameClient
    created: int = 0
    active: int = 0
    retired: bool = False
    closed: asyncio.Event = field(default_factory=asyncio.Event)


class ServerPool:
    def __init__(self, settings: Settings, root: Path, slots: int = 8, per_slot: int = 1,
                 sessions_per_db: int = 12, competition_mode: bool = False):
        if sessions_per_db > 18:
            raise ValueError("sessions_per_db must stay well below the ~20-session retention limit")
        self.settings, self.root = settings, root
        self.n_slots, self.per_slot, self.sessions_per_db = slots, per_slot, sessions_per_db
        self.competition_mode = competition_mode
        self.slots: list[Slot] = []
        self._cond = asyncio.Condition()
        self._tasks: set[asyncio.Task[None]] = set()
        self.started_processes = 0

    async def _spawn(self) -> Slot:
        spec = ServerSpec(f"pool-{next(_ids)}-{uuid.uuid4().hex[:6]}", self.root / uuid.uuid4().hex[:12],
                          transport="stdio", competition_mode=self.competition_mode)
        client = GameClient(spec, self.settings)
        await client.__aenter__()
        self.started_processes += 1
        return Slot(spec, client)

    async def __aenter__(self) -> "ServerPool":
        self.slots = list(await asyncio.gather(*(self._spawn() for _ in range(self.n_slots))))
        return self

    async def __aexit__(self, *exc: object) -> None:
        for task in list(self._tasks):
            await task
        await asyncio.gather(*(s.client.__aexit__(None, None, None) for s in self.slots), return_exceptions=True)

    def _replace_in_background(self, old: Slot) -> None:
        async def run() -> None:
            new = await self._spawn()
            async with self._cond:
                self.slots[self.slots.index(old)] = new
                self._cond.notify_all()
            while old.active:
                await asyncio.sleep(0.05)
            await old.client.__aexit__(None, None, None)
        task = asyncio.create_task(run())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    @asynccontextmanager
    async def lease(self) -> AsyncIterator[GameClient]:
        """Reserve capacity for one new session; yields a per-episode client view."""
        async with self._cond:
            while True:
                free = [s for s in self.slots if not s.retired and s.active < self.per_slot and s.created < self.sessions_per_db]
                if free:
                    slot = min(free, key=lambda s: s.active)
                    break
                await self._cond.wait()
            slot.active += 1
            slot.created += 1
            if slot.created >= self.sessions_per_db:
                slot.retired = True
                self._replace_in_background(slot)
        try:
            view = slot.client.view()
            view.db_root = str(slot.spec.root)  # type: ignore[attr-defined]
            yield view
        finally:
            async with self._cond:
                slot.active -= 1
                self._cond.notify_all()
