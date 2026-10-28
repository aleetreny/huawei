"""Bot explorador para el juego real: politica optima, pero en cada pregunta elige la respuesta
menos observada (catalogo v2 + lo que ya eligio este proceso), salvo que haga explotar el riesgo
o lo lleve por encima de `risk_room`, deje Health a 1 o menos o cueste
Skill/Network/Output en el mes previo a una evaluacion. Sirve para jugar las ramas que los lotes anteriores casi nunca tocaron.

    PYTHONPATH=. .venv/bin/python scripts/huevos-pascua/run_explore.py --batch e01-explore --games 1200
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ingenieria-inversa"))
import replica  # noqa: E402
from replica_bot import ReplicaBot  # noqa: E402

PICKED: collections.Counter = collections.Counter()  # por proceso


class Explorer(ReplicaBot):
    name = "explorer"

    def __init__(self, seed: int, shared: dict[str, Any] | None = None, explore_below: int = 60, risk_room: int = 2, **kw: Any):
        super().__init__(seed, shared=shared, **kw)
        self.explore_below, self.risk_room = explore_below, risk_room
        self.p["risk_room"] = risk_room
        self.p["explore_below"] = explore_below

    def story(self, obs, choices, ctx):
        st = self._state(obs, ctx)
        ev = obs.get("current_event") or {}
        key = json.dumps([ev.get("title"), ev.get("description"), [c.get("action") for c in choices]], ensure_ascii=False)
        node = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
        n = self.cat.nodes.get(node)
        if n is None:  # pregunta nunca vista: se explora siempre
            k = min(choices, key=lambda c: PICKED[(node, c["choice"])])["choice"]
            PICKED[(node, k)] += 1
            return k, "x-new"
        def seen(k: int) -> int:
            c = n["choices"].get(str(k))
            return (c["n"] if c else 0) + PICKED[(node, k)]
        cand = []
        for c in choices:
            k = c["choice"]
            fx = (n["choices"].get(str(k)) or {}).get("d") or {}
            dr = self.cat.answer_risk(node, k)
            if st.risk + dr > self.risk_room or st.health + fx.get("health", 0) <= 1:
                continue
            if st.month % 6 == 5 and any(fx.get(s, 0) < 0 for s in ("skill", "network", "output")):
                continue  # mes previo a la evaluacion: no se pierde nada de lo que pide el ascenso
            cand.append((seen(k), k, dr))
        cand.sort()
        if cand and cand[0][0] < self.explore_below:
            k, dr = cand[0][1], cand[0][2]
            PICKED[(node, k)] += 1
            self._bump(ctx, dr)
            return k, "x"
        return super().story(obs, choices, ctx)
