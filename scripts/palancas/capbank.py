"""Cap bank (palanca 2): real quarterly situations where a stat has stopped rising, served after a resume.

Research only: the situations carry development-game text and stay under ~/careerlab-data/palancas.

Each item is one quarterly decision (an Energy action or the main action) from a recorded bot game, served
as the first turn of a new session (the official continuation prompt), so the only memory is the log:
`check_latest_logs` returns the recorded entries with the agent's earlier notes written in the arm's own
style (`t13`: the review countdown; `status`: the t16 status line with Now S/N/O and Caps). Kinds:
- `detect`: the previous quarterly action announced a gain on a stat that did not move; no note has the cap yet;
- `carry`: an earlier quarterly action of this level already showed the cap and the last note lists it;
- `nocap`: the previous quarterly action registered fully and nothing is capped (false-alarm check).

    python3 -I scripts/palancas/capbank.py build --sit ~/careerlab-data/palancas/sit-v02.jsonl --out ~/careerlab-data/palancas/caps-bank.jsonl
    python3 -I scripts/palancas/capbank.py serve --bank ~/careerlab-data/palancas/caps-bank.jsonl
    python3 -I scripts/palancas/capbank.py score --bank ~/careerlab-data/palancas/caps-bank.jsonl --arms caps-t13,caps-t16
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import os
import random
import re
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
os.environ.setdefault("BB_DATA", str(REPO / "lab" / "data" / "ingenieria-inversa"))
# scripts/transmision holds a select.py that shadows the standard module: load bank.py by path instead
_spec = importlib.util.spec_from_file_location("tbank", REPO / "scripts" / "transmision" / "bank.py")
tbank = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tbank)

import replica as R  # noqa: E402

OUT = Path.home() / "careerlab-data" / "palancas"
TDATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "transmision"))
GAINS = {**{a: fx for a, (fx, _c) in R.ENERGY_FX.items()}, **R.MAIN_FX}
SHORT = {"skill": "Skill", "network": "Network", "output": "Output"}


def review_in(month: int) -> int:
    return 6 if month % 6 == 0 else 6 - month % 6


def chosen_name(sit: dict[str, Any]) -> str | None:
    for c in sit["observe"]["choices"]:
        if c["choice"] == sit["recorded"]:
            return c["action"]
    return None


def caps_str(caps: list[str]) -> str:
    return ", ".join(SHORT[k] for k in caps) if caps else "none"


def note(style: str, sit: dict[str, Any], caps: list[str]) -> str:
    """The note an agent following the arm's Skill would have written at this step."""
    m = sit["month"]
    st = sit["state"]
    if sit["phase"] == "e":
        tail = ""
    else:
        tail = " | quarterly line" if style in ("status", "expect") else "quarterly line"
    if style in ("status", "expect"):
        line = f"Review in {review_in(m)} | Now S{st['skill']:g} N{st['network']:g} O{st['output']:g} | Caps: {caps_str(caps)}"
        if style == "expect" and sit["phase"] != "e":
            fx = GAINS.get(chosen_name(sit) or "", {})
            line += " | Expect " + " ".join(f"{k[0].upper()}{st[k] + max(0, fx.get(k, 0)):g}" for k in R.GROWTH)
        return line + tail
    return f"Review in {review_in(m)}" if sit["phase"] == "e" else tail


# ----------------------------------------------------------------------------- build
def load_games(paths: list[Path]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, str]]]]:
    games: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    logs: dict[str, list[dict[str, str]]] = {}
    for p in paths:
        for line in p.open():
            r = json.loads(line)
            if "log_of" in r:
                logs[r["log_of"]] = r["logs"]
                continue
            games[f"{r['batch']}:{r['game']}"].append(r)
    for v in games.values():
        v.sort(key=lambda r: r["i"])
    return games, logs


def candidates(steps: list[dict[str, Any]]) -> list[tuple[str, int, str | None, list[str]]]:
    """(kind, index, stat, caps in the last note) for every usable step of one game."""
    out = []
    seen: dict[int, list[str]] = collections.defaultdict(list)   # caps shown by quarterly actions, per level
    note_caps: list[list[str]] = []
    for i, s in enumerate(steps):
        lv = s["state"]["level"]
        note_caps.append(list(seen[lv]))
        if i == 0:
            continue
        p = steps[i - 1]
        if p["phase"] not in ("q", "m") or p["month"] != s["month"] or p["state"]["level"] != lv:
            continue
        a = chosen_name(p)
        fx = GAINS.get(a or "", {})
        stuck = [k for k in R.GROWTH if fx.get(k, 0) > 0 and s["state"][k] < p["state"][k] + fx[k] - 1e-9]
        full = all(s["state"][k] >= p["state"][k] + fx.get(k, 0) - 1e-9 for k in R.GROWTH if fx.get(k, 0) > 0)
        at_cap = [k for k in R.GROWTH if s["state"][k] >= R.cap(lv, k)]
        if s["phase"] in ("q", "m") and (s["phase"] == "m" or s["state"]["energy"] >= 1):
            fresh = [k for k in stuck if k not in seen[lv]]
            if fresh:
                out.append(("detect", i, fresh[0], list(seen[lv])))
            elif seen[lv] and all(k in at_cap for k in seen[lv]) and not stuck:
                out.append(("carry", i, seen[lv][0], list(seen[lv])))
            elif not seen[lv] and not at_cap and fx and full and any(fx.get(k, 0) > 0 for k in R.GROWTH):
                out.append(("nocap", i, None, []))
        for k in stuck:
            if k not in seen[lv]:
                seen[lv].append(k)
    return out


def _init() -> None:
    tbank._init()


def _value(args: tuple[dict[str, Any], int]) -> dict[str, Any]:
    sit, n = args
    return {**sit, **tbank.value_options(sit, n)}


def build(sit_paths: list[Path], out: Path, per_kind: int, rollouts: int, seed: int) -> None:
    games, logs = load_games(sit_paths)
    cat = R.Catalog(json.loads(tbank.CATALOG.read_text()))
    pool_by_kind: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for key, steps in games.items():
        for kind, i, stat, caps_prev in candidates(steps):
            s = dict(steps[i])
            lg = logs.get(key, [])
            ci = [j for j, e in enumerate(lg) if e["entry_type"] in ("action", "fixed_event") and "Chose #" in e["message"]]
            # notes of every earlier step of this game, in both styles (caps as an agent would have them then)
            caps_at = {}
            seen: dict[int, list[str]] = collections.defaultdict(list)
            for j, t in enumerate(steps[: i + 1]):
                caps_at[j] = list(seen[t["state"]["level"]])
                if j + 1 < len(steps):
                    n_ = steps[j + 1]
                    a = chosen_name(t) if t["phase"] in ("q", "m") else None
                    fx = GAINS.get(a or "", {})
                    if n_["state"]["level"] == t["state"]["level"]:
                        for k in R.GROWTH:
                            if fx.get(k, 0) > 0 and n_["state"][k] < t["state"][k] + fx[k] - 1e-9 and k not in seen[t["state"]["level"]]:
                                seen[t["state"]["level"]].append(k)
            s["notes_by_step"] = {style: {str(ci[j]): note(style, steps[j], caps_at[j]) for j in range(i) if j < len(ci)}
                                  for style in ("t13", "status", "expect")}
            s["logs_full"] = lg[: s["log_upto"]][-30:]
            s["log_offset"] = max(0, s["log_upto"] - 30)
            s["kind"], s["cap_stat"], s["caps_prev"] = kind, stat, caps_prev
            s["caps_true"] = [k for k in R.GROWTH if s["state"][k] >= R.cap(s["state"]["level"], k)]
            s["fx"] = tbank.option_fx(cat, s)
            s["tags"] = [kind]
            s["holdout"] = False
            pool_by_kind[kind].append(s)
    rng = random.Random(seed)
    chosen = []
    for kind, lst in sorted(pool_by_kind.items()):
        rng.shuffle(lst)
        by_game: set[str] = set()
        pick = []
        for s in lst:      # at most one item per game and kind, to spread the situations
            if s["game"] in by_game:
                continue
            by_game.add(s["game"])
            pick.append(s)
            if len(pick) >= per_kind:
                break
        print(f"{kind}: {len(lst)} candidates, {len(pick)} kept", file=sys.stderr)
        chosen += pick
    with Pool(max(1, (os.cpu_count() or 2) - 2), initializer=_init) as pool, out.open("w") as f:
        for rec in pool.imap_unordered(_value, [(s, rollouts) for s in chosen]):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"{len(chosen)} items -> {out}", file=sys.stderr)


# ----------------------------------------------------------------------------- serve
NOTE_RE = re.compile(r"\nNotes: .*\Z", re.S)


def serve(bank: Path) -> None:
    items = [json.loads(line) for line in bank.open()]
    for style in ("t13", "status", "expect"):
        path = OUT / f"items-caps-{style}.jsonl"
        with path.open("w") as f:
            for it in items:
                notes = it["notes_by_step"][style]
                logs = []
                for j, e in enumerate(it["logs_full"]):
                    msg = e["message"]
                    nt = notes.get(str(it["log_offset"] + j))
                    if nt is not None and "\nNotes: " in msg:
                        msg = NOTE_RE.sub("\nNotes: " + nt, msg)
                    logs.append({"entry_type": e["entry_type"], "message": msg})
                rec = {k: v for k, v in it.items() if k not in ("notes_by_step", "logs_full")}
                rec["serve"] = {"long_from": it["i"], "month_from": it["i"], "observes": [it["observe"]], "logs_at": [logs]}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{len(items)} items -> {path}")


# ----------------------------------------------------------------------------- score
def parse_caps(notes: str | None) -> list[str] | None:
    m = re.search(r"Caps:\s*([^|\n.;(]*)", notes or "")
    if not m:
        return None
    txt = m.group(1).lower()
    return [k for k in R.GROWTH if k in txt]


def capped_spend(it: dict[str, Any], k: int) -> bool:
    """The chosen action's growth gains all fall on stats at their ceiling (what the cap rule forbids)."""
    d = it["fx"][str(k)]["d"]
    up = [s for s in R.GROWTH if d.get(s, 0) > 0]
    return bool(up) and all(s in it["caps_true"] for s in up)


def known_spend(it: dict[str, Any], k: int) -> bool:
    """The chosen action raises a stat whose ceiling the history already showed, and no stat with room left."""
    known = set(it["caps_prev"]) | ({it["cap_stat"]} if it["cap_stat"] else set())
    d = it["fx"][str(k)]["d"]
    return (any(d.get(s, 0) > 0 and s in known for s in R.GROWTH)
            and not any(d.get(s, 0) > 0 and s not in it["caps_true"] for s in R.GROWTH))


def wasted(it: dict[str, Any], k: int) -> bool:
    """The chosen action raises a capped stat and gives nothing else that counts (no growth on another stat,
    no Health or Dignity below 10, no risk reduction)."""
    f = it["fx"][str(k)]
    d, st = f["d"], it["state"]
    if not any(d.get(s, 0) > 0 and s in it["caps_true"] for s in R.GROWTH):
        return False
    useful = (any(d.get(s, 0) > 0 and s not in it["caps_true"] for s in R.GROWTH)
              or (d.get("health", 0) > 0 and st["health"] < 10) or (d.get("dignity", 0) > 0 and st["dignity"] < 10)
              or f["dr"] < 0)
    return not useful


def score(bank: Path, arms: list[str]) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in bank.open()}
    print("| Brazo | Tipo | n | Apunta el techo bien % | Falsa alarma % | Gasta en un techo ya visto % | Gasta en cualquier techo % | Pérdida de nota (simulador) | Lee el registro % | Tokens |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for arm in arms:
        res = {}
        for p in (TDATA / "runs" / arm).glob("*.json"):
            if p.name != "arm.json":
                r = json.loads(p.read_text())
                res[r["id"]] = r
        for kind in ("detect", "carry", "nocap"):
            rows = [(items[i], r) for i, r in res.items() if i in items and items[i]["kind"] == kind]
            if not rows:
                continue
            n = len(rows)
            note_ok = false = known = spend = 0
            regret = 0.0
            logs = toks = 0
            for it, r in rows:
                caps = parse_caps(r.get("notes"))
                want = set(it["caps_prev"]) | ({it["cap_stat"]} if it["cap_stat"] else set())
                if caps is not None:
                    note_ok += int(want <= set(caps)) if want else int(not caps)
                    false += int(bool(set(caps) - set(it["caps_true"])))
                k = r.get("choice")
                if k is None or str(k) not in it["q"]:
                    regret += max(it["q"].values()) - min(it["q"].values())
                    continue
                known += int(known_spend(it, k))
                spend += int(capped_spend(it, k))
                regret += max(it["q"].values()) - it["q"][str(k)]
                logs += int(r.get("log_calls", 0) > 0)
                u = r.get("usage") or {}
                toks += sum(u.get(x, 0) for x in ("input", "cache_read", "cache_create", "output"))
            print(f"| {arm} | {kind} | {n} | {100 * note_ok / n:.0f} | {100 * false / n:.0f} | {100 * known / n:.0f} | {100 * spend / n:.0f} | "
                  f"{regret / n:.2f} | {100 * logs / n:.0f} | {toks / n / 1000:.0f}k |")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--sit", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--per-kind", type=int, default=50)
    p.add_argument("--rollouts", type=int, default=48)
    p.add_argument("--seed", type=int, default=3)
    p = sub.add_parser("serve")
    p.add_argument("--bank", required=True)
    p = sub.add_parser("score")
    p.add_argument("--bank", required=True)
    p.add_argument("--arms", required=True)
    a = ap.parse_args()
    if a.cmd == "build":
        build([Path(x) for x in a.sit.split(",")], Path(a.out), a.per_kind, a.rollouts, a.seed)
    elif a.cmd == "serve":
        serve(Path(a.bank))
    else:
        score(Path(a.bank), a.arms.split(","))


if __name__ == "__main__":
    main()
