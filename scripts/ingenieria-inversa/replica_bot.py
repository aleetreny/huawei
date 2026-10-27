"""Real-game bot that plays a replica policy: converts each observation into a replica State.

Hidden risk is tracked as the replica does (answer risks from the catalog, synced to the HR remark),
so the same policy can be compared in the real game and in the replica."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any

from careerlab.mcp_client import phase

import replica
from policies import Base, affordable, by_action, reserve_choice


class ReplicaBot(Base):
    name = "replica-greedy"

    @staticmethod
    def load_shared(catalog: str, **_: Any) -> dict[str, Any]:
        return {"cat": replica.Catalog(json.loads(Path(catalog).read_text()))}

    def __init__(self, seed: int, shared: dict[str, Any] | None = None, catalog: str | None = None,
                 risk_cap: int = 3, **params: Any):
        super().__init__(seed, risk_cap=risk_cap, **params)
        self.cat = shared["cat"]
        self.rep = replica.Replica(self.cat, random.Random(seed))
        self.pol = replica.Greedy(risk_cap=risk_cap)

    def new_game(self, game_id: str) -> dict[str, Any]:
        return {"spent": {}, "game": game_id, "R": 0, "nb": 0, "last_key": None}

    def _state(self, obs: dict[str, Any], ctx: dict[str, Any]) -> replica.State:
        stt = obs["current_state"]["status"]
        month = obs["current_state"]["time"]["current_month"]
        ev = obs.get("events") or ""
        h = replica.hr_level(ev)
        if h is not None and h < 4:
            ctx["R"] = h
        if "Old landmines" in ev:
            ctx["R"], ctx["nb"] = 0, ctx["nb"] + 1
        st = replica.State(health=stt["health"], dignity=stt["dignity"], skill=stt["skill"], network=stt["network"],
                           level=int(str(stt["level"])[1:]), duration_in_level=stt["duration_in_level"],
                           output=stt["output"], wealth=float(stt["wealth"]), energy=stt["energy"], month=month)
        st.risk, st.blowups = ctx["R"], ctx["nb"]
        return st

    def _bump(self, ctx: dict[str, Any], dr: int) -> None:
        ctx["R"] = max(0, ctx["R"] + dr)
        if ctx["R"] >= replica.BLOW_AT:
            ctx["R"] = 0

    def story(self, obs, choices, ctx):
        st = self._state(obs, ctx)
        ev = obs.get("current_event") or {}
        key = json.dumps([ev.get("title"), ev.get("description"), [c.get("action") for c in choices]], ensure_ascii=False)
        node = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
        if node not in self.cat.nodes:
            return self.rng.choice(choices)["choice"], "u"
        k = self.pol.story(self.rep, st, node)
        valid = {c["choice"] for c in choices}
        if k not in valid:
            k = self.rng.choice(choices)["choice"]
        self._bump(ctx, self.cat.answer_risk(node, k))
        return k, "g"

    def energy(self, obs, choices, ctx):
        st = self._state(obs, ctx)
        st.energy = (obs.get("current_event") or {}).get("remaining_energy", st.energy) or 0
        a = self.pol.energy(self.rep, st)
        ok = by_action(affordable(obs, choices))
        if a and a in ok:
            self._bump(ctx, replica.ACTION_RISK.get("q|" + a, 0))
            return ok[a]["choice"], "g"
        return reserve_choice(choices), "g"

    def main(self, obs, choices, ctx):
        st = self._state(obs, ctx)
        a = self.pol.main(self.rep, st)
        ok = by_action(choices)
        if a in ok:
            self._bump(ctx, replica.ACTION_RISK.get("m|" + a, 0))
            return ok[a]["choice"], "g"
        return ok.get("No action", choices[0])["choice"], "g"
