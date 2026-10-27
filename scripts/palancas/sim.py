"""Palancas: how much final score each in-run lever is worth in the replica (research only).

Nothing here is Skill content. The base player is the general-rule bot (`rules.RuleBot`, ~68 in the
replica), which sees what an agent can see: the effect of each option, the sign of its hidden risk,
the HR remark. Every lever is an option of one configurable bot, and all arms of an experiment play the
same seeds, so differences are paired game by game.

Levers (lab/reports/palancas/):
- caps: the ceiling of each stat at the current level. `exact` knows it, `blind` never does, `detect`
  learns it in-run when an announced gain does not fully register (kept for the whole level, as a note
  would keep it, or forgotten after `mem` months), `fixed` believes the dev ceilings whatever the game.
- warn: react to the money / isolation / dignity warnings (or to the visible condition itself).
- rep: arrive at a review with Dignity and Health high and risk low (M24), exact or as a general rule.
- risk: what the bot knows of hidden risk: `live` (exact, capped at 4), or the HR remark at the start of
  the month plus what it can count (`quarter`: the HiddenRisk numbers of the quarter menu; `sign`: the
  sign of each answer it picks).
- eps: share of story choices made at random (a noisier reader than the rule bot, closer to an LLM).

    python3 scripts/palancas/sim.py caps --games 10000
    python3 scripts/palancas/sim.py warn --games 10000
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import math
import os
import random
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ingenieria-inversa"))
os.environ.setdefault("BB_DATA", str(HERE.parents[1] / "lab" / "data" / "ingenieria-inversa"))

import replica as R  # noqa: E402
import rules  # noqa: E402

CATALOG = Path(os.environ["BB_DATA"]) / "catalog_v2.json"
BASE_CAPS = copy.deepcopy(R.CAPS)
BASE_THRESH = dict(R.THRESH)
UNKNOWN = 1e9


class LeverBot(rules.RuleBot):
    def __init__(self, caps: str = "exact", mem: int | None = None, warn: str | None = None, rep: str | None = None,
                 risk: str = "live", eps: float = 0.0, pdet: float = 1.0):
        super().__init__()
        self.caps_mode, self.mem, self.warn, self.rep, self.risk_mode, self.eps = caps, mem, warn, rep, risk, eps
        self.pdet = pdet   # chance of noticing a gain that did not register (Haiku in the cap bank: ~0.6)
        self.begin(0)

    # ------------------------------------------------------------------ per game
    def begin(self, seed: int) -> None:
        self.rng = random.Random(seed * 7919 + 17)
        self.rng_det = random.Random(seed * 104729 + 3)
        self.learned: dict[tuple[int, str], tuple[float, int]] = {}
        self.month = None
        self.est = 0
        self.nb = 0
        self.seen: collections.Counter = collections.Counter()

    def _tick(self, st: R.State) -> None:
        """What the agent reads at each decision: a new month brings the HR remark; a blow-up is announced."""
        if st.month != self.month:
            self.month = st.month
            self.est = min(st.risk, 4)
            for k, flag in (("money", st.neg_wealth_months >= 3), ("isolation", st.zero_net_months >= 3),
                            ("dignity", st.low_dig_months >= 3)):
                if flag:
                    self.seen[k] += 1
        if st.blowups > self.nb:
            self.nb, self.est = st.blowups, 0

    def _view(self, st: R.State) -> R.State:
        if self.risk_mode == "live":
            return st
        v = copy.copy(st)
        v.risk = self.est
        return v

    # ------------------------------------------------------------------ caps
    def cap(self, st: R.State, k: str) -> float:
        if self.caps_mode == "exact":
            return R.cap(st.level, k)
        if self.caps_mode == "fixed":
            return BASE_CAPS.get(st.level, BASE_CAPS[6]).get(k, UNKNOWN)
        if self.caps_mode in ("detect", "detect-q"):
            hit = self.learned.get((st.level, k))
            if hit and (self.mem is None or st.month - hit[1] < self.mem):
                return hit[0]
        return UNKNOWN

    def _learn(self, st: R.State, fx: dict[str, float], quarter: bool = False) -> None:
        """An announced gain that does not fully register shows the stat is at its ceiling (`detect-q`: only
        seen in the quarter phase, whose menu prints each action's status_updates)."""
        if self.caps_mode not in ("detect", "detect-q") or (self.caps_mode == "detect-q" and not quarter):
            return
        tmp = copy.copy(st)
        R.apply_delta(tmp, fx)
        for k in R.GROWTH:
            x = fx.get(k, 0)
            if x > 0 and getattr(tmp, k) < getattr(st, k) + x - 1e-9 and self.rng_det.random() < self.pdet:
                self.learned[(st.level, k)] = (getattr(tmp, k), st.month)

    # ------------------------------------------------------------------ levers in the value
    def _warn_flags(self, st: R.State) -> dict[str, bool]:
        if self.warn == "warning":   # react once the warning text has appeared (3rd month of the condition)
            return {"money": st.neg_wealth_months >= 3, "isolation": st.zero_net_months >= 3,
                    "dignity": st.low_dig_months >= 3}
        if self.warn == "condition":  # react to the visible condition itself
            return {"money": st.wealth < 0, "isolation": st.network <= 0, "dignity": st.dignity <= 1}
        return {}

    def _rep_active(self, st: R.State) -> bool:
        """Last quarter before a review (the quarter phase of month 3 of the semester and months 4-5)."""
        if not self.rep or st.month % 6 not in (3, 4, 5):
            return False
        if self.rep == "exact":   # M24 with a margin for the choices still to come
            return 4 * st.dignity + st.health < 22 + 8 * st.risk + 16 * st.blowups + 6
        return st.dignity < 10 or st.risk > 0   # general: Dignity full and HR remark friendly

    def _val(self, st: R.State, fx: dict[str, float], risk_sign: int) -> float:
        v = super()._val(st, fx, risk_sign)
        f = self._warn_flags(st)
        if f.get("money"):
            w = fx.get("wealth", 0)
            v += 6.0 * (w * ((st.level + 1) // 2) if w < 0 else w)
        if f.get("isolation"):
            v += 6.0 * fx.get("network", 0)
        if f.get("dignity"):
            v += 6.0 * fx.get("dignity", 0)
        if self._rep_active(st):
            v += 2.0 * min(fx.get("dignity", 0), 10 - st.dignity) + 0.5 * min(fx.get("health", 0), 10 - st.health)
            v -= 4.0 * max(0, risk_sign)
        return v

    # ------------------------------------------------------------------ decisions
    def story(self, rep: R.Replica, st: R.State, node: str) -> int:
        self._tick(st)
        u, pick = self.rng.random(), self.rng.random()
        choices = rep.cat.nodes[node]["choices"]
        if u < self.eps:
            keys = sorted(choices, key=int)
            k = int(keys[int(pick * len(keys))])
        else:
            k = super().story(rep, self._view(st), node)
        self._learn(st, choices[str(k)]["d"])
        if "sign" in self.risk_mode:
            r = rep.cat.answer_risk(node, k)
            self.est = max(0, self.est + (r > 0) - (r < 0))
        return k

    def energy(self, rep: R.Replica, st: R.State) -> str | None:
        self._tick(st)
        v = self._view(st)
        a = None
        if self._rep_active(v) and not (st.health <= 4 and "R7" in self.on):
            if v.risk > 0 and st.energy >= 2:
                a = "Defuse legacy risk"
            elif st.dignity < 10 and st.energy >= 1:
                a = "Mental recovery"
        f = self._warn_flags(st)
        if a is None and f.get("isolation") and st.energy >= 1:
            a = "Network maintenance"
        if a is None and f.get("dignity") and st.energy >= 1:
            a = "Mental recovery"
        if a is None:
            a = super().energy(rep, v)
        if a:
            self._learn(st, R.ENERGY_FX[a][0], quarter=True)
            if "quarter" in self.risk_mode:
                self.est = max(0, self.est + R.ACTION_RISK.get("q|" + a, 0))
        return a

    def main(self, rep: R.Replica, st: R.State) -> str:
        self._tick(st)
        a = super().main(rep, self._view(st))
        self._learn(st, R.MAIN_FX[a], quarter=True)
        if "quarter" in self.risk_mode:
            self.est = max(0, self.est + R.ACTION_RISK.get("m|" + a, 0))
        return a


# ----------------------------------------------------------------------------- scenarios and runs
def scenario(name: str, cat: R.Catalog) -> None:
    """Changed parameters, to check a lever does not rely on the dev values (as in rulestest.py)."""
    R.CAPS.clear()
    R.CAPS.update(copy.deepcopy(BASE_CAPS))
    R.THRESH.clear()
    R.THRESH.update(BASE_THRESH)
    R.BLOW_AT = 5
    if name.startswith("caps"):
        f = 1 + int(name[4:]) / 100
        for c in R.CAPS.values():
            c.update({k: max(1, round(v * f)) for k, v in c.items()})
    elif name.startswith("thr"):
        f = 1 + int(name[3:]) / 100
        R.THRESH.update({lv: tuple(max(1, round(x * f)) for x in t) for lv, t in BASE_THRESH.items()})
    elif name == "draw20":
        rng = random.Random(5)
        smp = cat.d["sampler"]
        smp["weight"] = {t: w * rng.uniform(0.8, 1.2) for t, w in smp["weight"].items()}
        smp["window"] = {t: [max(1, round(m0 * rng.uniform(0.8, 1.2))) if m0 > 1 else 1, m1]
                         for t, (m0, m1) in smp["window"].items()}


_CAT: dict[str, R.Catalog] = {}


def job(args: tuple[str, str, dict[str, Any], list[int]]) -> tuple[str, str, list[dict[str, Any]]]:
    scen, arm, opts, seeds = args
    if scen not in _CAT:
        _CAT.clear()
        _CAT[scen] = R.Catalog(json.loads(CATALOG.read_text()))
        scenario(scen, _CAT[scen])
    cat = _CAT[scen]
    bot = LeverBot(**opts)
    rows = []
    for s in seeds:
        bot.begin(s)
        st, trace = R.play(cat, bot, random.Random(s))
        tones = collections.Counter(x[2]["tone"] for x in trace if x[1] == "r")
        promos = [x[0] for x in trace if x[1] == "r" and x[2]["promoted"]]
        rows.append({"seed": s, "score": R.Replica.score(st), "fail": st.failure or "completed", "level": st.level,
                     "warn_talks": tones.get("warn", 0), "first_promo": promos[0] if promos else None,
                     "seen": dict(bot.seen), "blowups": st.blowups})
    return scen, arm, rows


def run(scens: list[str], arms: dict[str, dict[str, Any]], games: int, seed0: int, procs: int, chunk: int = 250):
    jobs = [(sc, a, o, list(range(seed0 + i, seed0 + min(games, i + chunk))))
            for sc in scens for a, o in arms.items() for i in range(0, games, chunk)]
    out: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    with Pool(procs) as pool:
        for sc, a, rows in pool.imap_unordered(job, jobs):
            out[(sc, a)].extend(rows)
    for v in out.values():
        v.sort(key=lambda r: r["seed"])
    return out


def paired(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> tuple[float, float]:
    d = [x["score"] - y["score"] for x, y in zip(a, b)]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / max(1, len(d) - 1))
    return m, sd / math.sqrt(len(d))


def report(res, scens: list[str], arms: list[str], ref: str, title: str) -> str:
    lines = [f"### {title}", "", f"Diferencia emparejada frente a `{ref}` (misma semilla), ± error típico.", "",
             "| Escenario | Brazo | Partidas | Nota media | Diferencia | L1 despedido | Crisis | Ruina | Aislado | Agotado/salud | Charlas de aviso por partida | L6+ |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for sc in scens:
        base = res[(sc, ref)]
        for a in arms:
            rows = res[(sc, a)]
            n = len(rows)
            mean = sum(r["score"] for r in rows) / n
            fails = collections.Counter(r["fail"] for r in rows)
            m, se = paired(rows, base)
            diff = "—" if a == ref else f"{m:+.2f} ± {se:.2f}"
            pct = lambda k: f"{100 * fails.get(k, 0) / n:.1f} %"
            lines.append(f"| {sc} | `{a}` | {n} | {mean:.2f} | {diff} | {pct('dismissed')} | {pct('trust')} | {pct('broke')} | "
                         f"{pct('isolated')} | {100 * (fails.get('health', 0) + fails.get('breakdown', 0)) / n:.1f} % | "
                         f"{sum(r['warn_talks'] for r in rows) / n:.2f} | {100 * sum(r['level'] >= 6 for r in rows) / n:.0f} % |")
    return "\n".join(lines)


EXPERIMENTS: dict[str, dict[str, Any]] = {
    "caps": {"ref": "blind", "scens": ["base", "caps+20", "caps-10", "thr-10"], "title": "Palanca 2: techos",
             "arms": {"blind": {"caps": "blind"}, "detect": {"caps": "detect"}, "detect-3m": {"caps": "detect", "mem": 3},
                      "detect-1m": {"caps": "detect", "mem": 1},
                      "detect-q": {"caps": "detect-q"}, "detect-q-60": {"caps": "detect-q", "pdet": 0.6},
                      "detect-60": {"caps": "detect", "pdet": 0.6}, "fixed-dev": {"caps": "fixed"}, "exact": {"caps": "exact"}}},
    "caps-noisy": {"ref": "blind", "scens": ["base", "caps+20"], "title": "Palanca 2: techos, jugador con ruido (30 % al azar)",
                   "arms": {"blind": {"caps": "blind", "eps": 0.3}, "detect": {"caps": "detect", "eps": 0.3},
                            "detect-1m": {"caps": "detect", "mem": 1, "eps": 0.3}, "exact": {"caps": "exact", "eps": 0.3}}},
    "warn": {"ref": "base", "scens": ["base"], "title": "Palanca 3: avisos con margen",
             "arms": {"base": {}, "warning": {"warn": "warning"}, "condition": {"warn": "condition"},
                      "base-noisy": {"eps": 0.3}, "warning-noisy": {"warn": "warning", "eps": 0.3},
                      "condition-noisy": {"warn": "condition", "eps": 0.3}}},
    "rep": {"ref": "base", "scens": ["base"], "title": "Palanca 4: reputación antes de la evaluación",
            "arms": {"base": {}, "general": {"rep": "general"}, "exact": {"rep": "exact"},
                     "base-noisy": {"eps": 0.3}, "general-noisy": {"rep": "general", "eps": 0.3},
                     "exact-noisy": {"rep": "exact", "eps": 0.3}}},
    "risk": {"ref": "live", "scens": ["base"], "title": "Palanca 5: el riesgo que ve el jugador",
             "arms": {"live": {}, "stale": {"risk": "stale"}, "quarter": {"risk": "quarter"}, "sign": {"risk": "sign"},
                      "sign+quarter": {"risk": "sign+quarter"}}},
    # what the status line in the note buys together: ceilings kept for the level and risky picks counted
    "notes": {"ref": "plain", "scens": ["base", "caps+20", "caps-10"], "title": "Palancas 1+2+5: la línea de estado en la nota",
              "arms": {"plain": {"caps": "detect", "mem": 1, "risk": "stale"},
                       "caps-only": {"caps": "detect", "risk": "stale"},
                       "risk-only": {"caps": "detect", "mem": 1, "risk": "sign+quarter"},
                       "status-line": {"caps": "detect", "risk": "sign+quarter"},
                       "status-line-q": {"caps": "detect-q", "risk": "sign+quarter"},
                       "plain-noisy": {"caps": "detect", "mem": 1, "risk": "stale", "eps": 0.3},
                       "status-line-noisy": {"caps": "detect", "risk": "sign+quarter", "eps": 0.3}}},
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("exp", choices=sorted(EXPERIMENTS))
    ap.add_argument("--games", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=777)
    ap.add_argument("--procs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--scens")
    ap.add_argument("--json", help="write per-game rows here")
    a = ap.parse_args()
    ex = EXPERIMENTS[a.exp]
    scens = a.scens.split(",") if a.scens else ex["scens"]
    res = run(scens, ex["arms"], a.games, a.seed, a.procs)
    # noisy arms are compared with the noisy base
    arms = list(ex["arms"])
    print(report(res, scens, [x for x in arms if "noisy" not in x], ex["ref"], ex["title"]))
    noisy = [x for x in arms if "noisy" in x]
    if noisy:
        print()
        print(report(res, scens, noisy, noisy[0], ex["title"] + " (jugador con ruido)"))
    if a.json:
        Path(a.json).write_text(json.dumps({f"{k[0]}|{k[1]}": v for k, v in res.items()}))


if __name__ == "__main__":
    main()
