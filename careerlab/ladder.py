"""Fast race (protocol fastloop-v2, 26 Oct 2026): one champion, challengers climb a short ladder.

A game's expected score is p * mu + (1 - p) * ELIM_MEAN: p is the completion rate
(Beta posterior), mu the mean score of completed games (Normal posterior) and
ELIM_MEAN the mean score of an early exit in the race. After 2 and 4 games a
challenger stays only while P(better than the champion) is at least 0.05 and 0.15;
at 8 games it becomes champion at P >= 0.60, leaves below 0.35 and otherwise plays
4 more; at 12 games it becomes champion at P >= 0.60 or leaves. The thresholds were
calibrated by simulation on the 153 race Haiku games (lab/protocol/fastloop-v2.md).

The rest is bookkeeping: the champion keeps a few control games, queued games of a
challenger that left are cancelled, and the pipeline asks for new designs
(variants of the champion, bold ones when the race is stuck). `step` is pure;
`apply` writes the registry and the state file; the driver in scripts/fastloop/
runs them in a loop.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from careerlab.store import Registry

KINDS = ("initial", "targeted", "stretch", "bold", "external")
KIND_ES = {"initial": "inicial", "targeted": "variante", "stretch": "variante ambiciosa", "bold": "idea valiente",
           "external": "del equipo"}
PENDING = ("queued", "leased", "running")


@dataclass(frozen=True)
class LadderConfig:
    rungs: tuple[int, ...] = (2, 4, 8, 12)  # games a challenger has played when it is judged
    keep: tuple[float, ...] = (0.05, 0.15)  # minimum P(better) to stay after 2 and after 4 games
    crown: float = 0.60  # P(better) that makes a challenger with 8 or 12 games the champion
    extend: float = 0.35  # below this at 8 games it leaves; between extend and crown it plays to 12
    elim_mean: float = 28.6  # mean score of the 75 race Haiku games that ended early
    comp_sd: float = 5.0  # spread of one completed game around its manual's mean
    prior_mu: float = 61.0  # mean completed-game score in the race, used before a manual completes a game
    prior_mu_sd: float = 8.0
    champion_min: int = 8
    champion_max: int = 24
    champion_every: int = 5  # one control game for the champion per this many challenger games
    pipeline: int = 4  # challengers to keep in play (active plus designs in flight)
    stuck_after: int = 6  # challengers finished without a crown before a bold round
    stuck_hours: float = 3.0  # or this long without a crown, once at least 3 challengers finished
    draws: int = 20000


@dataclass
class Cell:
    """Race games of one manual with the race actor: terminal scores in launch order and pending jobs."""
    scores: list[float] = field(default_factory=list)
    completed: list[bool] = field(default_factory=list)
    pending: int = 0

    @property
    def n(self) -> int:
        return len(self.scores)

    @property
    def mean(self) -> float | None:
        return sum(self.scores) / len(self.scores) if self.scores else None


@dataclass
class Action:
    kind: str  # enqueue | cancel | crown | leave | design
    policy_id: str | None = None
    n: int = 0
    priority: float = 0.0
    status: str | None = None
    design: str | None = None
    why: str = ""


# -- statistics ---------------------------------------------------------------

def _rng(*parts: Any) -> np.random.Generator:
    seed = int(hashlib.sha256(json.dumps(parts, default=str).encode()).hexdigest()[:12], 16)
    return np.random.default_rng(seed)


def score_draws(cell: Cell, cfg: LadderConfig, rng: np.random.Generator) -> np.ndarray:
    """Posterior draws of a manual's expected game score."""
    n, c = cell.n, sum(cell.completed)
    p = rng.beta(1 + c, 1 + n - c, cfg.draws)
    if c:
        done = [s for s, ok in zip(cell.scores, cell.completed) if ok]
        mu = rng.normal(sum(done) / c, cfg.comp_sd / math.sqrt(c), cfg.draws)
    else:
        mu = rng.normal(cfg.prior_mu, cfg.prior_mu_sd, cfg.draws)
    return p * mu + (1 - p) * cfg.elim_mean


def p_better(challenger: Cell, champion: Cell, cfg: LadderConfig) -> float:
    """P(challenger's expected score > champion's); deterministic for the same data."""
    rng = _rng(challenger.scores, challenger.completed, champion.scores, champion.completed)
    return float((score_draws(challenger, cfg, rng) > score_draws(champion, cfg, rng)).mean())


def expected_score(cell: Cell, cfg: LadderConfig) -> float:
    return float(score_draws(cell, cfg, _rng("mean", cell.scores, cell.completed)).mean())


# -- registry access ----------------------------------------------------------

def load_cells(reg: Registry, actor_id: str) -> dict[str, Cell]:
    """Every manual's games with one actor in this registry's origin (all purposes)."""
    cells: dict[str, Cell] = {}
    rows = reg.db.execute(
        "SELECT j.policy_id, j.status, e.outcome, e.score, e.completed FROM jobs j LEFT JOIN evaluations e USING(job_id) "
        "WHERE j.actor_id=? AND j.origin=? ORDER BY j.created_at, j.replicate, j.attempt", (actor_id, reg.origin)).fetchall()
    for r in rows:
        cell = cells.setdefault(r["policy_id"], Cell())
        if r["outcome"] in ("completed", "eliminated") and r["score"] is not None:
            cell.scores.append(float(r["score"]))
            cell.completed.append(bool(r["completed"]))
        elif r["status"] in PENDING:
            cell.pending += 1
    return cells


def policy_names(reg: Registry) -> dict[str, str]:
    return {r[0]: r[1] for r in reg.db.execute("SELECT policy_id, name FROM policies")}


def resolve_policy(reg: Registry, ref: str) -> str:
    row = reg.db.execute("SELECT policy_id FROM policies WHERE policy_id=? OR name=? ORDER BY created_at DESC", (ref, ref)).fetchone()
    if row is None:
        raise ValueError(f"unknown policy {ref!r}")
    return row[0]


# -- state ----------------------------------------------------------------------

def new_state(reg: Registry, actor_id: str, cfg: LadderConfig, now: float, champion: str | None = None) -> dict[str, Any]:
    """Start the ladder: the champion is given, or the manual with the best expected score among those with 8+ games."""
    cells = load_cells(reg, actor_id)
    names = policy_names(reg)
    if champion is None:
        ranked = sorted((expected_score(c, cfg), pid) for pid, c in cells.items() if c.n >= cfg.champion_min)
        if not ranked:
            raise ValueError(f"no manual has {cfg.champion_min} games with actor {actor_id}")
        champion = ranked[-1][1]
    env = reg.db.execute("SELECT env_id FROM jobs WHERE policy_id=? AND actor_id=? ORDER BY created_at DESC",
                         (champion, actor_id)).fetchone()
    if env is None:
        raise ValueError("the champion has never played with this actor")
    cell = cells.get(champion, Cell())
    state = {"version": 1, "actor_id": actor_id, "env_id": env[0], "champion": champion, "crowned_at": now,
             "games_at_crown": 0, "finished_since_crown": 0, "stuck_at": None, "bold_pending": False,
             "entries": {}, "events": [], "updated": now}
    state["entries"][champion] = _entry(champion, names.get(champion, champion), "initial", champion, now, 2)
    state["entries"][champion].update(status="champion", games=cell.n, mean=cell.mean, completed=sum(cell.completed))
    _event(state, now, "champion", champion, names.get(champion, champion), cell, None, "initial champion: best expected score with 8+ games")
    return state


def _entry(pid: str, name: str, kind: str, base: str, now: float, first: int, note: str = "") -> dict[str, Any]:
    return {"policy_id": pid, "name": name, "kind": kind, "base": base, "status": "active", "rung": 0, "first": first,
            "entered": now, "decided": None, "games": 0, "mean": None, "completed": 0, "p_better": None, "note": note}


def _event(state: dict[str, Any], now: float, what: str, pid: str, name: str, cell: Cell | None, pb: float | None, why: str) -> None:
    state["events"].append({"at": now, "event": what, "policy_id": pid, "name": name,
                            "games": cell.n if cell else 0, "mean": round(cell.mean, 2) if cell and cell.mean is not None else None,
                            "completed": sum(cell.completed) if cell else 0, "p_better": None if pb is None else round(pb, 3), "why": why})


def add(state: dict[str, Any], pid: str, name: str, kind: str, now: float, first: int = 2, note: str = "") -> dict[str, Any]:
    """Put a registered manual on the ladder (idempotent). `first` is 4 for outside manuals with strong evidence."""
    if kind not in KINDS[1:]:
        raise ValueError(f"kind must be one of {KINDS[1:]}")
    if first not in (2, 4):
        raise ValueError("a challenger starts with 2 games, or 4 when it brings strong evidence from elsewhere")
    s = copy.deepcopy(state)
    if pid in s["entries"]:
        return s
    s["entries"][pid] = _entry(pid, name, kind, s["champion"], now, first, note)
    _event(s, now, "enter", pid, name, None, None, f"{kind} challenger, first {first} games" + (f"; {note}" if note else ""))
    return s


def load_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n")
    os.replace(tmp, path)


# -- the decision step ----------------------------------------------------------

def _priority(stage: int, kind: str) -> float:
    return 10.0 + 10.0 * stage + (2.0 if stage == 0 and kind in ("bold", "external") else 0.0)


def step(state: dict[str, Any], cells: dict[str, Cell], cfg: LadderConfig, now: float, in_flight: list[str] | None = None
         ) -> tuple[dict[str, Any], list[Action]]:
    """One pass over the ladder. Pure: returns the new state and the actions to apply."""
    s = copy.deepcopy(state)
    in_flight = in_flight or []
    acts: list[Action] = []
    entries = s["entries"]

    def cell(pid: str) -> Cell:
        return cells.get(pid, Cell())

    def leave(pid: str, status: str, pb: float | None, why: str) -> None:
        e = entries[pid]
        e.update(status=status, decided=now)
        s["finished_since_crown"] += 1
        acts.append(Action("leave", pid, status=status, why=why))
        if cell(pid).pending:
            acts.append(Action("cancel", pid, why=f"{e['name']} left the ladder"))
        _event(s, now, status, pid, e["name"], cell(pid), pb, why)

    def crown(pid: str, pb: float, why: str) -> None:
        old = s["champion"]
        entries[old].update(status="runner_up", decided=now)
        entries[pid].update(status="champion", decided=now)
        acts.append(Action("crown", pid, why=why))
        _event(s, now, "champion", pid, entries[pid]["name"], cell(pid), pb, why)
        s.update(champion=pid, crowned_at=now, finished_since_crown=0, stuck_at=None, bold_pending=False)
        s["games_at_crown"] = _challenger_games(s, cells)  # after the swap, so the new champion's games are not counted
        for other, e in entries.items():  # variants of the old champion that have not played yet are dropped
            if e["status"] == "active" and e["base"] == old and e["kind"] in ("targeted", "stretch") and cell(other).n == 0:
                e.update(status="cancelled", decided=now)
                if cell(other).pending:
                    acts.append(Action("cancel", other, why=f"variant of the old champion {entries[old]['name']}, not started"))
                _event(s, now, "cancelled", other, e["name"], cell(other), None, "variant of a champion that lost its title, not started")

    active = sorted((pid for pid, e in entries.items() if e["status"] == "active"), key=lambda p: entries[p]["entered"])
    for pid in active:
        e = entries[pid]
        while e["status"] == "active":
            target = e["first"] if e["rung"] == 0 else cfg.rungs[e["rung"]]
            stage = cfg.rungs.index(target)
            c = cell(pid)
            e.update(games=c.n, mean=c.mean, completed=sum(c.completed))
            if c.n < target:
                missing = target - c.n - c.pending
                if missing > 0:
                    acts.append(Action("enqueue", pid, n=missing, priority=_priority(stage, e["kind"]),
                                       why=f"{e['name']}: {target} games for rung {stage + 1}"))
                break
            champ = cell(s["champion"])
            pb = p_better(c, champ, cfg)
            e["p_better"] = round(pb, 3)
            vs = f"P(better than {entries[s['champion']]['name']}) = {pb:.2f} after {c.n} games, mean {c.mean:.1f}, {sum(c.completed)}/{c.n} completed"
            if stage < len(cfg.keep):
                if pb < cfg.keep[stage]:
                    leave(pid, "out", pb, f"{vs} < {cfg.keep[stage]}")
                else:
                    e["rung"] = stage + 1
            elif stage == len(cfg.rungs) - 2:
                if pb >= cfg.crown:
                    crown(pid, pb, f"{vs} >= {cfg.crown}")
                elif pb < cfg.extend:
                    leave(pid, "runner_up", pb, f"{vs} < {cfg.extend}")
                else:
                    e["rung"] = stage + 1
            else:
                if pb >= cfg.crown:
                    crown(pid, pb, f"{vs} >= {cfg.crown}")
                else:
                    leave(pid, "runner_up", pb, f"{vs} < {cfg.crown}")

    # control games keep the champion's estimate fresh as challengers play
    champ_id = s["champion"]
    c = cell(champ_id)
    entries[champ_id].update(games=c.n, mean=c.mean, completed=sum(c.completed))
    extra = (_challenger_games(s, cells) - s["games_at_crown"]) // cfg.champion_every
    target = min(cfg.champion_max, max(cfg.champion_min, cfg.champion_min + extra))
    if target - c.n - c.pending > 0:
        acts.append(Action("enqueue", champ_id, n=target - c.n - c.pending, priority=25.0,
                           why=f"champion control games ({target} wanted)"))

    # stuck: too many challengers finished, or too long, without a new champion
    finished = s["finished_since_crown"]
    stuck = finished >= cfg.stuck_after or (finished >= 3 and now - s["crowned_at"] >= cfg.stuck_hours * 3600)
    if stuck and not s["bold_pending"] and s["stuck_at"] is None:
        s.update(stuck_at=now, bold_pending=True)
        _event(s, now, "stuck", champ_id, entries[champ_id]["name"], c, None,
               f"{finished} challengers finished without a new champion; bold round requested")
    if s["bold_pending"] and any(e["kind"] == "bold" and e["entered"] >= (s["stuck_at"] or now) for e in entries.values()):
        s.update(bold_pending=False, stuck_at=None, finished_since_crown=0)

    # designs: keep the pipeline full
    live = [e for e in entries.values() if e["status"] == "active"]
    need = cfg.pipeline - len(live) - len(in_flight)
    kinds_live = [e["kind"] for e in live] + list(in_flight)
    while need > 0:
        if s["bold_pending"] and kinds_live.count("bold") < 2:
            kind = "bold"
        elif "stretch" not in kinds_live:
            kind = "stretch"
        else:
            kind = "targeted"
        acts.append(Action("design", design=kind, why=f"pipeline {cfg.pipeline}, {len(live)} active, {len(in_flight)} in design"))
        kinds_live.append(kind)
        need -= 1
    s["updated"] = now
    return s, acts


def _challenger_games(s: dict[str, Any], cells: dict[str, Cell]) -> int:
    return sum(cells.get(pid, Cell()).n for pid, e in s["entries"].items() if pid != s["champion"])


# -- applying a step ----------------------------------------------------------------

def apply(reg: Registry, state: dict[str, Any], actions: list[Action]) -> list[dict[str, Any]]:
    """Write a step's actions to the registry; returns the design requests for the driver."""
    designs = []
    actor, env = state["actor_id"], state["env_id"]
    for a in actions:
        if a.kind == "enqueue":
            jobs = reg.enqueue(a.policy_id, actor, env, "ladder", a.n, priority=a.priority)
            reg.decide("ladder_enqueue", a.policy_id, {"n": a.n, "priority": a.priority, "jobs": jobs}, a.why)
        elif a.kind == "cancel":
            jobs = reg.cancel_queued(a.policy_id, actor, a.why)
            reg.decide("ladder_cancel", a.policy_id, {"jobs": jobs}, a.why)
        elif a.kind == "crown":
            reg.decide("ladder_crown", a.policy_id, {"champion": a.policy_id}, a.why)
        elif a.kind == "leave":
            reg.set_policy_status(a.policy_id, "retired", f"fast race: {a.status}; {a.why}")
        elif a.kind == "design":
            designs.append(asdict(a))
    return designs


def run_step(reg: Registry, state_path: Path, cfg: LadderConfig | None = None, apply_changes: bool = False,
             in_flight: list[str] | None = None, now: float | None = None) -> tuple[dict[str, Any], list[Action]]:
    cfg = cfg or LadderConfig()
    state = load_state(state_path)
    new, actions = step(state, load_cells(reg, state["actor_id"]), cfg, now or time.time(), in_flight)
    if apply_changes:
        apply(reg, new, actions)
        save_state(state_path, new)
    return new, actions


# -- reports ------------------------------------------------------------------------

def _hm(ts: float | None) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%d %b %H:%M") if ts else "—"


def _num(x: float | None, digits: int = 1) -> str:
    return "—" if x is None else f"{x:.{digits}f}".replace(".", ",")


def _next_es(e: dict[str, Any], cfg: LadderConfig) -> str:
    if e["status"] != "active":
        return "—"
    target = e["first"] if e["rung"] == 0 else cfg.rungs[e["rung"]]
    return f"jugar hasta {target}"


def report_es(state: dict[str, Any], cfg: LadderConfig, now: float) -> str:
    """Plain-Spanish status page for the team (lab/reports/carrera-rapida.md)."""
    e = state["entries"]
    ch = e[state["champion"]]
    lines = ["# Carrera rápida: estado", "", f"Actualizado: {_hm(now)} UTC. Cómo funciona: [lab/fastloop/README.md](../fastloop/README.md).", "",
             "## Campeón", "",
             f"**{ch['name']}**: nota media {_num(ch['mean'])} en {ch['games']} partidas, terminó {ch['completed']} de {ch['games']}. "
             f"Campeón desde el {_hm(state['crowned_at'])} UTC.", "",
             "## Aspirantes en juego", ""]
    live = [x for x in e.values() if x["status"] == "active"]
    if live:
        lines += ["| Manual | Tipo | Partidas | Nota media | Terminadas | Prob. de ser mejor | Siguiente paso |", "|---|---|---:|---:|---:|---:|---|"]
        for x in sorted(live, key=lambda x: x["entered"]):
            pb = "—" if x["p_better"] is None else f"{round(100 * x['p_better'])} %"
            lines.append(f"| {x['name']} | {KIND_ES[x['kind']]} | {x['games']} | {_num(x['mean'])} | {x['completed']} de {x['games']} | {pb} | {_next_es(x, cfg)} |")
    else:
        lines.append("Ninguno ahora mismo; el sistema está diseñando los siguientes.")
    what = {"champion": "pasa a campeón", "out": "descartado", "runner_up": "se queda a las puertas (no supera al campeón)",
            "cancelled": "cancelado (era variante del campeón anterior)", "enter": "entra en la carrera", "stuck": "atasco: toca ronda de ideas valientes"}
    lines += ["", "## Últimas decisiones", ""]
    for ev in reversed(state["events"][-15:]):
        detail = ""
        if ev["games"]:
            detail = f" ({ev['games']} partidas, media {_num(ev['mean'])}, {ev['completed']} terminadas"
            detail += f"; prob. de ser mejor {round(100 * ev['p_better'])} %)" if ev["p_better"] is not None else ")"
        lines.append(f"- {_hm(ev['at'])}: **{ev['name']}** {what.get(ev['event'], ev['event'])}{detail}.")
    finished = state["finished_since_crown"]
    lines += ["", "## ¿Atascados?", ""]
    if state["bold_pending"]:
        lines.append(f"Sí: {finished} aspirantes descartados sin nuevo campeón. La siguiente tanda son ideas valientes.")
    else:
        lines.append(f"No. Desde el último campeón se han descartado {finished} aspirantes; la ronda de ideas valientes salta con {cfg.stuck_after} "
                     f"(o tras {cfg.stuck_hours:g} horas sin campeón nuevo).")
    return "\n".join(lines) + "\n"


def history_md(state: dict[str, Any], reg: Registry) -> str:
    """Every manual that went through the ladder and what happened, for designers (English)."""
    hyp = {r[0]: r[1] for r in reg.db.execute("SELECT policy_id, hypothesis FROM policies")}
    lines = ["# Fast race history", "", "Generated by `careerlab ladder status --write`. Read it before designing: do not repeat an idea that already failed "
             "unless you change what made it fail.", "",
             "| Manual | Kind | Built on | Games | Mean | Completed | Result | Idea |", "|---|---|---|---:|---:|---:|---|---|"]
    names = {pid: x["name"] for pid, x in state["entries"].items()}
    for pid, x in sorted(state["entries"].items(), key=lambda kv: kv[1]["entered"]):
        idea = " ".join((hyp.get(pid) or "").split())
        idea = idea if len(idea) <= 220 else idea[:219] + "…"
        lines.append(f"| {x['name']} | {x['kind']} | {names.get(x['base'], x['base'])} | {x['games']} | {_num(x['mean'])} | "
                     f"{x['completed']} | {x['status']} | {idea} |")
    return "\n".join(lines) + "\n"
