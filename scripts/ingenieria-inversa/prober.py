"""Easter-egg prober (matteo/easter-eggs): the oracle, but it forces the answers the earlier batches almost never took.

Earlier bots (b00-v03, ~6,300 games) chose some answers fewer than 30 times and 20 follow-up answers never.
If a hidden path exists (a chain that only opens on an unusual answer), it sits there. This bot plays like the
oracle to stay alive and reach late stages, but at a target story it takes the least-explored answer:
catalog count plus how often this process has already forced it. Stories missing from the catalog are new
content and get the same rotation. Tag 'p' marks a forced answer.

mode: "never"  -> only answers never seen before
      "career" -> never-seen answers plus every rare answer of career-path stories (promotion, management, VP...)
      "rare"   -> every answer seen fewer than `rare_n` times
Research bot only; nothing here is Skill material.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from typing import Any

from oracle import Oracle

CATALOG = Path(__file__).resolve().parents[2] / "lab/data/ingenieria-inversa/catalog_v2.json"
CAREER = re.compile(r"promot|ladder|management|individual contributor|VP|director|senior leader|panel|"
                    r"title|stepping up|leave|recruit|offer|covenant|new office|new bet|reshape the job|"
                    r"keep you|restructure|lead", re.I)


class Prober(Oracle):
    name = "prober"

    @staticmethod
    def load_shared(model: str, mode: str = "career", rare_n: int = 30, **_: Any) -> dict[str, Any]:
        sh = Oracle.load_shared(model)
        cat = json.loads(CATALOG.read_text())["nodes"]
        targets: dict[str, dict[int, int]] = {}
        for nid, v in cat.items():
            seen = {int(k): e.get("n", 0) for k, e in (v.get("choices") or {}).items()}
            nc = v.get("n_choices") or len(seen)
            counts = {c: seen.get(c, 0) for c in range(1, nc + 1)}
            never = any(n == 0 for n in counts.values())
            rare = any(n < rare_n for n in counts.values())
            career = bool(CAREER.search(v.get("title") or ""))
            if (mode == "never" and never) or (mode == "career" and (never or (career and rare))) or (mode == "rare" and rare):
                targets[nid] = counts
        sh["targets"] = targets
        sh["known"] = set(cat)
        sh["forced"] = collections.Counter()
        return sh

    def __init__(self, seed: int, shared: dict[str, Any] | None = None, mode: str = "career", rare_n: int = 30,
                 **params: Any):
        super().__init__(seed, shared=shared, mode=mode, rare_n=rare_n, **params)

    def story(self, obs, choices, ctx):
        node = self._node_id(obs)
        tg = self.sh.get("targets", {})
        forced = self.sh["forced"]
        if node in tg or node not in self.sh.get("known", ()):
            base = tg.get(node, {})
            pick = min(choices, key=lambda c: (base.get(c["choice"], 0) + 50 * forced[(node, c["choice"])],
                                               self.rng.random()))
            forced[(node, pick["choice"])] += 1
            ctx.setdefault("forced", []).append([obs["current_state"]["time"]["current_month"], node, pick["choice"]])
            return pick["choice"], "p"
        return super().story(obs, choices, ctx)
