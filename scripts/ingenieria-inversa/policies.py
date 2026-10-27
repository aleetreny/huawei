"""Bot policies for black-box research. None of this is Skill content.

A policy returns (choice index, tag) for each observation. Tags record why a choice was
made ('x' exploration, 'g' greedy, 'r' random, 'f' fixed rule), so analyses can keep
randomised decisions apart from steered ones.
"""

from __future__ import annotations

import random
from typing import Any

from careerlab.mcp_client import phase

HIGH, SKILL_L, NET_M, DEFUSE, MENTAL, HEALTH, REPORT, RESERVE = (
    "High-intensity work", "Skill learning", "Network maintenance", "Defuse legacy risk",
    "Mental recovery", "Health recovery", "Prepare report materials", "Reserve energy (no action)")
MAINS = ("Apply for a key project", "Report results to your manager", "Fight for resources", "Apply for rotation",
         "Showcase results", "Build a mentorship", "Repair a key relationship", "Lay low and reduce risk")


def by_action(choices: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {c.get("action", ""): c for c in choices}


def affordable(obs: dict[str, Any], choices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    left = (obs.get("current_event") or {}).get("remaining_energy", 0) or 0
    return [c for c in choices if (c.get("energy_cost") or 0) <= left]


def reserve_choice(choices: list[dict[str, Any]]) -> int:
    for c in choices:
        if (c.get("energy_cost") or 0) == 0 and "reserve" in c.get("action", "").lower():
            return c["choice"]
    return min(choices, key=lambda c: c.get("energy_cost") or 0)["choice"]


class Base:
    name = "base"

    def __init__(self, seed: int, **params: Any):
        self.rng = random.Random(seed)
        self.seed = seed
        self.p = params

    def params(self) -> dict[str, Any]:
        return {"seed": self.seed, **self.p}

    def new_game(self, game_id: str) -> dict[str, Any]:
        return {"spent": {}, "game": game_id}

    def end_game(self, ctx: dict[str, Any], rec: dict[str, Any]) -> None:
        pass

    def decide(self, obs: dict[str, Any], ctx: dict[str, Any]) -> tuple[int, str]:
        ph = phase(obs)
        choices = obs.get("choices") or []
        if ph == "document" or len(choices) == 1:
            return choices[0]["choice"], "f"
        if ph == "energy":
            return self.energy(obs, choices, ctx)
        if ph == "main_action":
            return self.main(obs, choices, ctx)
        return self.story(obs, choices, ctx)

    # --- default behaviours -------------------------------------------------
    def energy(self, obs, choices, ctx):
        """Survivable default: a Health point first if Health is not high, then Defuse, then reports."""
        st = obs["current_state"]["status"]
        month = obs["current_state"]["time"]["current_month"]
        spent = ctx["spent"].setdefault(month, [])
        ok = by_action(affordable(obs, choices))
        plan = [HEALTH, DEFUSE, REPORT] if st["health"] < 9 else [DEFUSE, REPORT, NET_M]
        for name in plan:
            if name in ok and name not in spent:
                spent.append(name)
                return ok[name]["choice"], "f"
        return reserve_choice(choices), "f"

    def main(self, obs, choices, ctx):
        ok = by_action(choices)
        return ok.get("Apply for a key project", choices[0])["choice"], "f"

    def story(self, obs, choices, ctx):
        return self.rng.choice(choices)["choice"], "r"


class RandomSafe(Base):
    """Uniform story choices; survivable Energy; main action uniform among the eight (or none)."""

    name = "random-safe"

    def main(self, obs, choices, ctx):
        return self.rng.choice(choices)["choice"], "r"


class RandomEnergy(Base):
    """Uniform story choices and uniformly random Energy spending (affordable), random main."""

    name = "random-all"

    def energy(self, obs, choices, ctx):
        return self.rng.choice(affordable(obs, choices))["choice"], "r"

    def main(self, obs, choices, ctx):
        return self.rng.choice(choices)["choice"], "r"
