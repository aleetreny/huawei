"""Deterministic, non-LLM development actors.

They exist to test the infrastructure, to provide floor baselines with complete
per-episode records, and to probe quarterly planning that only uses effects the
game publishes in the current observation (energy_cost / status_updates). They
never read event identifiers and contain no event-specific answers.
"""

from __future__ import annotations

import random
from typing import Any

from careerlab.episode import Decision
from careerlab.mcp_client import phase


class UniformActor:
    """Uniform choice among listed options (replicates the teammate's random driver design)."""

    name = "uniform"

    def __init__(self, seed: int, affordable_only: bool = False):
        self.seed = seed
        self.affordable_only = affordable_only
        self.rng = random.Random(seed)

    def config(self) -> dict[str, Any]:
        return {"kind": "scripted", "name": self.name, "seed": self.seed, "affordable_only": self.affordable_only}

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision:
        choices = obs.get("choices") or []
        if self.affordable_only and phase(obs) == "energy":
            left = (obs.get("current_event") or {}).get("remaining_energy", 0)
            choices = [c for c in choices if c.get("energy_cost", 0) <= left] or choices
        return Decision(self.rng.choice(choices)["choice"], notes="uniform")


def _stat(obs: dict[str, Any], key: str) -> float:
    return float(obs.get("current_state", {}).get("status", {}).get(key, 0) or 0)


class QuarterlyPlanner:
    """Uniform story choices; rule-based quarterly allocation from published effects.

    ``mode`` selects a behaviour family for the quarterly phase only:
    - "wellbeing": restore the weaker of Health/Dignity first, then grow.
    - "growth": favour Skill/Output/Network, recover only when low.
    - "risk": defuse hidden risk whenever the run's own feedback mentions risk.
    Stat bands are lab parameters for comparing behaviours, not game thresholds.
    """

    def __init__(self, seed: int, mode: str = "wellbeing", low: float = 4.0):
        self.seed, self.mode, self.low = seed, mode, low
        self.rng = random.Random(seed)
        self.name = f"quarterly-{mode}"

    def config(self) -> dict[str, Any]:
        return {"kind": "scripted", "name": self.name, "seed": self.seed, "mode": self.mode, "low": self.low}

    async def decide(self, obs: dict[str, Any], memory: dict[str, Any]) -> Decision:
        choices = obs.get("choices") or []
        events_text = (obs.get("events") or "").lower()
        if "risk" in events_text or "landmine" in events_text:
            memory["risk_flag_month"] = obs.get("current_state", {}).get("time", {}).get("current_month")
        ph = phase(obs)
        if ph == "energy":
            return Decision(self._energy(obs, choices, memory), notes=f"{self.name} energy")
        if ph == "main_action":
            return Decision(self._main(obs, choices, memory), notes=f"{self.name} main")
        return Decision(self.rng.choice(choices)["choice"], notes="uniform story choice")

    def _gain(self, choice: dict[str, Any], key: str) -> float:
        return float((choice.get("status_updates") or {}).get(key, 0))

    def _energy(self, obs: dict[str, Any], choices: list[dict[str, Any]], memory: dict[str, Any]) -> int:
        left = (obs.get("current_event") or {}).get("remaining_energy", 0)
        options = [c for c in choices if c.get("energy_cost", 0) <= left]
        health, dignity = _stat(obs, "health"), _stat(obs, "dignity")
        def best(key: str, sign: float = 1.0) -> dict[str, Any] | None:
            ranked = sorted((c for c in options if sign * self._gain(c, key) > 0), key=lambda c: -sign * self._gain(c, key) / max(c.get("energy_cost", 1), 1))
            return ranked[0] if ranked else None
        picks: list[dict[str, Any] | None] = []
        if self.mode == "risk" and memory.get("risk_flag_month") is not None:
            picks.append(best("HiddenRisk", -1.0))
        if min(health, dignity) <= self.low or self.mode == "wellbeing":
            picks.append(best("Health") if health <= dignity else best("Dignity"))
        if self.mode == "growth":
            picks += [best("Skill"), best("Output"), best("Network")]
        else:
            picks += [best("Network"), best("Output")]
        for pick in picks:
            if pick is not None and pick.get("energy_cost", 0) > 0:
                if not (self._gain(pick, "Health") < 0 and health <= self.low):
                    return pick["choice"]
        reserve = [c for c in options if c.get("energy_cost", 0) == 0]
        return (reserve or options or choices)[0]["choice"]

    def _main(self, obs: dict[str, Any], choices: list[dict[str, Any]], memory: dict[str, Any]) -> int:
        health, dignity = _stat(obs, "health"), _stat(obs, "dignity")
        if self.mode == "risk" and memory.pop("risk_flag_month", None) is not None:
            key = "HiddenRisk"
            ranked = sorted(choices, key=lambda c: self._gain(c, key))
            return ranked[0]["choice"]
        if health <= self.low:
            ranked = sorted(choices, key=lambda c: -self._gain(c, "Health"))
            return ranked[0]["choice"]
        weights = {"growth": {"Skill": 1.0, "Output": 1.0, "Network": 0.7, "Dignity": 0.3},
                   "wellbeing": {"Dignity": 1.0 if dignity <= self.low else 0.4, "Network": 0.8, "Output": 0.6, "Skill": 0.6},
                   "risk": {"Output": 0.8, "Network": 0.8, "Skill": 0.6, "Dignity": 0.5}}[self.mode]
        ranked = sorted(choices, key=lambda c: -sum(w * self._gain(c, k) for k, w in weights.items()))
        return ranked[0]["choice"]


def make_scripted(name: str, seed: int) -> Any:
    if name == "uniform":
        return UniformActor(seed)
    if name == "uniform-affordable":
        actor = UniformActor(seed, affordable_only=True)
        actor.name = name
        return actor
    if name.startswith("quarterly-"):
        return QuarterlyPlanner(seed, mode=name.split("-", 1)[1])
    raise ValueError(f"unknown scripted actor {name}")
