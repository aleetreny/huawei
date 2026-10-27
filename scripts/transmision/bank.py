"""Obedience bank (T20): real situations from recorded bot games and the right answer per the replica.

Research only. Situations carry development-game text: they stay under ~/careerlab-data/transmision
(outside Git) and nothing from them goes into a Skill.

    python3 scripts/transmision/bank.py extract --batches c02-planner-real,v02-validation,b01-oracle-eps --out sit.jsonl
    python3 scripts/transmision/bank.py truth --sit sit.jsonl --out bank.jsonl --rollouts 48

`extract` replays each recorded game with the replica's hidden-state tracking (risk synced to the HR
remark, wealth interval, Output history, persistent-condition counters) and stores, for every candidate
step, the exact `observe` payload the player saw, the official log entries written so far, and the full
replica state. `truth` values every option of a situation with common-random-number rollouts in the
replica (the tuned stage planner plays the rest of the career) and tags the rule each situation tests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RE_DIR = HERE.parent / "ingenieria-inversa"
sys.path.insert(0, str(RE_DIR))
os.environ.setdefault("BB_DATA", str(HERE.parents[1] / "lab" / "data" / "ingenieria-inversa"))

import planner as P  # noqa: E402
import replica as R  # noqa: E402

DATA = Path(os.environ["BB_DATA"])
CATALOG = DATA / "catalog_v1.json"
LOG_TYPE = {"S": "system", "F": "fixed_event", "A": "action", "E": "event", "P": "salary", "T": "talk",
            "R": "promotion", "X": "failure", "Z": "ending_score"}
SID = "5e1f0c2a9b7d4c3e8a6f1b2d3c4e5f60"


def best_params() -> dict[str, Any]:
    top = json.loads((DATA / "search_top.json").read_text())
    return dict(top[0][1])


def holdout(title: str) -> bool:
    """Reserved titles (about 30 %): formulations are chosen on the others and checked here."""
    return int(hashlib.sha1(title.encode()).hexdigest(), 16) % 10 < 3


def observe_payload(s: list, node: dict[str, Any], events: str) -> dict[str, Any]:
    m = s[0]
    v = s[4]
    status = {"health": v[0], "dignity": v[1], "skill": v[2], "network": v[3], "level": f"L{v[4]}",
              "duration_in_level": v[5], "output": v[6], "wealth": v[7], "energy": v[8]}
    ev = {k: node[k] for k in ("title", "description") if node.get(k) is not None}
    return {"current_state": {"time": {"current_month": m, "current_quarter": (m - 1) // 3 + 1,
                                       "current_year": (m - 1) // 12 + 1},
                              "status": status,
                              "simulation_flags": {"alive": True, "failed": False, "failure_reason": None},
                              "session_id": SID, "available_choice_count": len(node.get("choices") or [])},
            "current_event": ev, "choices": node.get("choices") or [], "events": events or ""}


def state_dict(st: R.State) -> dict[str, Any]:
    d = dict(st.__dict__)
    d["out_hist"] = {str(k): v for k, v in st.out_hist.items()}
    return d


def state_from(d: dict[str, Any]) -> R.State:
    d = dict(d)
    d["out_hist"] = {int(k): v for k, v in d["out_hist"].items()}
    d["grades"] = list(d.get("grades") or [])
    return R.State(**d)


# ----------------------------------------------------------------------------- extract
def extract(batches: list[str], out_path: Path, max_games: int | None) -> None:
    import tl
    from bbdata import Batch
    cat = R.Catalog(json.loads(CATALOG.read_text()))
    rep = R.Replica(cat, random.Random(1))
    n_out = 0
    with out_path.open("w") as out_f:
        for batch in batches:
            b = Batch(batch)
            games = 0
            for g in b.games():
                if g["outcome"] not in ("eliminated", "completed"):
                    continue
                r = tl.timeline(b, g)
                if r is None:
                    continue
                games += 1
                if max_games and games > max_games:
                    break
                logs = b.log_entries(g)
                ci = [i for i, (c, msg) in enumerate(logs) if c in ("A", "F") and "Chose #" in msg]
                out = r[1]
                W, R_, nb = 1.0, 0, 0
                Wlo = Whi = 1.0
                out_hist: dict[int, float] = {}
                counters = (0, 0, 0)
                used: list[str] = []
                slot = 0
                month_start = 0
                for i, (s, e, a) in enumerate(out):
                    t = b.texts.get(s[5], "") if s[5] else ""
                    new_month = i == 0 or s[0] != out[i - 1][0][0]
                    if new_month:
                        out_hist.setdefault(s[0], s[4][6])
                        slot = 0
                        month_start = i
                    h = R.hr_level(t)
                    if h is not None and h < 4:
                        R_ = h
                    if "Old landmines" in t:
                        R_, nb = 0, nb + 1
                    st = R.obs_state(s[4], s[0])
                    W = (Wlo + Whi) / 2
                    st.wealth, st.risk, st.blowups, st.out_hist = W, R_, nb, dict(out_hist)
                    st.neg_wealth_months, st.zero_net_months, st.low_dig_months = counters
                    node = b.nodes.get(s[2], {})
                    title = node.get("title") or ""
                    if s[1] == "e" and title not in used:
                        used.append(title)
                    rec = {"id": f"{batch}:{g['g']}:{i}", "batch": batch, "game": g["g"], "i": i, "month": s[0],
                           "phase": s[1], "node": s[2], "title": title, "slot": slot, "month_start": month_start,
                           "recorded": s[3], "state": state_dict(st), "used": list(used),
                           "observe": observe_payload(s, node, t), "log_upto": ci[i] if i < len(ci) else len(logs)}
                    out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n_out += 1
                    # advance exactly as replica.validate does
                    R.decide_apply(rep, st, s, e)
                    if s[1] == "e":
                        slot += 1
                    nxt = out[i + 1][0] if i + 1 < len(out) else None
                    if nxt is not None and s[1] == "e" and nxt[1] == "q":
                        st.energy = 3
                    if nxt is not None and nxt[0] != s[0]:
                        rep.month_change(st)
                    R_ = st.risk
                    counters = (st.neg_wealth_months, st.zero_net_months, st.low_dig_months)
                    if nxt is not None:
                        obs = list(nxt[4])
                        dw = st.wealth - W
                        Wlo, Whi = max(Wlo + dw, obs[7] + R.DISP_LO), min(Whi + dw, obs[7] + R.DISP_HI)
                        if Wlo > Whi + 1e-9:
                            Wlo, Whi = obs[7] + R.DISP_LO, obs[7] + R.DISP_HI
                        W = (Wlo + Whi) / 2
                # games' logs, once per game, for check_latest_logs
                log_rec = {"log_of": f"{batch}:{g['g']}",
                           "logs": [{"entry_type": LOG_TYPE.get(c, "event"), "message": msg} for c, msg in logs]}
                out_f.write(json.dumps(log_rec, ensure_ascii=False) + "\n")
            print(f"{batch}: {games} games", file=sys.stderr)
    print(f"{n_out} steps -> {out_path}", file=sys.stderr)


# ----------------------------------------------------------------------------- rollouts
ENERGY_NAMES = list(R.ENERGY_FX)
MAIN_NAMES = list(R.MAIN_FX)


def option_names(sit: dict[str, Any]) -> list[tuple[int, str]]:
    return [(c["choice"], c["action"]) for c in sit["observe"]["choices"]]


def play_from(cat: R.Catalog, pol: P.Planner, st: R.State, sit: dict[str, Any], k: int, rng: random.Random,
              months: int = 48) -> R.State:
    """Take option k at the situation, then let the planner play the rest of the career."""
    rep = R.Replica(cat, rng)
    used = set(sit["used"])
    month = st.month
    pending: list[str] = []
    stage = sit["phase"]           # 'e' -> rest of the month's events, then quarter; 'q' -> energy; 'm' -> main
    slots = 3 - sit["slot"]
    names = dict(option_names(sit))
    if stage == "e":
        node = sit["node"]
        rep.answer(st, node, k)
        slots -= 1
        ch = cat.nodes[node]["choices"].get(str(k), {})
        if "next" in ch:
            if ch.get("when") == "same" and slots > 0:
                queue = [ch["next"]]
            else:
                pending.append(ch["next"])
                queue = []
        else:
            queue = []
    elif stage == "q":
        a = names[k]
        if a.startswith("Reserve"):
            stage = "m"
        else:
            rep.energy_action(st, a)
        queue = []
    else:
        rep.main_action(st, names[k] if not names[k].startswith("No") else "No action")
        queue = []
    first = True
    while month <= months and st.alive:
        if not first:
            queue, pending, slots = pending, [], 3
            stage = "e"
        if stage == "e":
            while slots > 0 and st.alive:
                if queue:
                    node = queue.pop(0)
                else:
                    t = R.draw_title(cat, st, used, rng)
                    if t is None:
                        break
                    used.add(t)
                    node = cat.d["first_node"][t]
                while st.alive:
                    n = cat.nodes.get(node)
                    if not n or not n["choices"]:
                        break
                    kk = pol.story(rep, st, node)
                    rep.answer(st, node, kk)
                    slots -= 1
                    ch = n["choices"].get(str(kk), {})
                    if "next" in ch:
                        if ch.get("when") == "same" and slots > 0:
                            node = ch["next"]
                            continue
                        pending.append(ch["next"])
                    break
            if not st.alive:
                break
            if month % 3 == 0:
                st.energy = 3
                stage = "q"
        if stage == "q" and month % 3 == 0:
            while st.alive:
                a = pol.energy(rep, st)
                if not a or R.ENERGY_FX.get(a, ({}, 9))[1] > st.energy:
                    break
                rep.energy_action(st, a)
            if not st.alive:
                break
            stage = "m"
        if stage == "m" and month % 3 == 0 and not (first and sit["phase"] == "m"):
            rep.main_action(st, pol.main(rep, st))
        first = False
        if month == months:
            break
        rep.month_change(st)
        month = st.month
    return st


_CAT: R.Catalog | None = None
_POL: P.Planner | None = None


def _init() -> None:
    global _CAT, _POL
    _CAT = R.Catalog(json.loads(CATALOG.read_text()))
    _POL = P.Planner(**best_params())


def value_options(sit: dict[str, Any], n: int) -> dict[str, Any]:
    assert _CAT is not None and _POL is not None
    q: dict[str, float] = {}
    fails: dict[str, float] = {}
    for k, _name in option_names(sit):
        tot, nf = 0.0, 0
        for j in range(n):
            st = state_from(sit["state"])
            end = play_from(_CAT, _POL, st, sit, k, random.Random(1000 + j))
            tot += R.Replica.score(end)
            nf += int(end.failure is not None)
        q[str(k)] = round(tot / n, 3)
        fails[str(k)] = round(nf / n, 3)
    return {"q": q, "fail": fails}


def option_fx(cat: R.Catalog, sit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Visible effect and hidden-risk change of each option (catalog for events, published table for quarters)."""
    fx: dict[str, dict[str, Any]] = {}
    for k, name in option_names(sit):
        if sit["phase"] == "e":
            d = dict(cat.effect(sit["node"], k) or {})
            dr = cat.answer_risk(sit["node"], k)
        elif sit["phase"] == "q":
            d, dr = dict(R.ENERGY_FX.get(name, ({}, 0))[0]), R.ACTION_RISK.get("q|" + name, 0)
        else:
            d, dr = dict(R.MAIN_FX.get(name, {})), R.ACTION_RISK.get("m|" + name, 0)
        fx[str(k)] = {"d": d, "dr": dr, "name": name}
    return fx


def tags(cat: R.Catalog, sit: dict[str, Any], fx: dict[str, dict[str, Any]]) -> list[str]:
    """Which key rule a situation tests (several may apply)."""
    st = sit["state"]
    lv, m, ph = st["level"], sit["month"], sit["phase"]
    out = []
    thr = R.THRESH.get(lv, R.THRESH[6])
    if ph == "e" and m % 6 == 5 and lv <= 3:
        # some option loses a growth point that is at or below its threshold
        for i, k in enumerate(R.GROWTH):
            if st[k] <= thr[i] + 1 and any(f["d"].get(k, 0) < 0 for f in fx.values()) \
                    and any(f["d"].get(k, 0) >= 0 for f in fx.values()):
                out.append("pre_review")
                break
    if lv in (4, 5) and ph in ("q", "m") and m < 45:
        out.append("skill_l4")
    if ph in ("q", "m") and st["risk"] >= 2 and m < 45:
        out.append("hr_risk")
    if ph == "e" and st["risk"] >= 2 and any(st["risk"] + f["dr"] >= R.BLOW_AT for f in fx.values()) \
            and any(st["risk"] + f["dr"] < R.BLOW_AT for f in fx.values()):
        out.append("trigger")
    if ph == "e" and lv <= 2 and st["wealth"] < 2.0 and any(f["d"].get("wealth", 0) < 0 for f in fx.values()):
        out.append("early_ruin")
    if m >= 45:
        out.append("closing")
    if st["health"] <= 3 and m < 45 and (ph in ("q",) or (ph == "e" and any(f["d"].get("health", 0) < 0 for f in fx.values())
                                                         and any(f["d"].get("health", 0) >= 0 for f in fx.values()))):
        out.append("low_health")
    if ph == "e" and m < 45:
        out.append("general")
    return out


def _truth_one(args: tuple[dict[str, Any], int]) -> dict[str, Any]:
    sit, n = args
    v = value_options(sit, n if sit["phase"] == "e" else max(4, n // 4))
    return {**sit, **v}


def truth(sit_path: Path, out_path: Path, n: int, per_tag: int, seed: int, only: str | None = None) -> None:
    cat = R.Catalog(json.loads(CATALOG.read_text()))
    cands: dict[str, list[dict[str, Any]]] = {}
    for line in sit_path.open():
        sit = json.loads(line)
        if "log_of" in sit:
            continue
        if sit["phase"] == "e":
            node = cat.nodes.get(sit["node"])
            if not node or len(node["choices"]) != len(sit["observe"]["choices"]):
                continue
            if any(c.get("n", 0) < 3 for c in node["choices"].values()):
                continue
        elif sit["phase"] == "q":
            if sit["state"]["energy"] < 1:
                continue
        fx = option_fx(cat, sit)
        tg = tags(cat, sit, fx)
        if not tg:
            continue
        sit["fx"], sit["tags"] = fx, tg
        sit["holdout"] = holdout(sit["title"]) if sit["phase"] == "e" else (hash(sit["game"]) % 10 < 3)
        for t in tg:
            if only and t != only:
                continue
            if t == "general" and not only:
                continue
            cands.setdefault(t, []).append(sit)
    rng = random.Random(seed)
    chosen: dict[str, dict[str, Any]] = {}
    for t, lst in sorted(cands.items()):
        rng.shuffle(lst)
        print(f"{t}: {len(lst)} candidates", file=sys.stderr)
        for sit in lst[:per_tag]:
            chosen[sit["id"]] = sit
    done: set[str] = set()
    if out_path.exists():
        done = {json.loads(line)["id"] for line in out_path.open()}
    todo = [(s, n) for s in chosen.values() if s["id"] not in done]
    print(f"valuing {len(todo)} situations x {n} rollouts", file=sys.stderr)
    with Pool(processes=max(1, (os.cpu_count() or 2)), initializer=_init) as pool, out_path.open("a") as f:
        for i, rec in enumerate(pool.imap_unordered(_truth_one, todo, chunksize=4)):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if i % 100 == 0:
                print(f"  {i}", file=sys.stderr, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("extract")
    p.add_argument("--batches", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--max-games", type=int)
    p = sub.add_parser("truth")
    p.add_argument("--sit", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--rollouts", type=int, default=48)
    p.add_argument("--per-tag", type=int, default=700)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--only-tag")
    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.batches.split(","), Path(a.out), a.max_games)
    else:
        truth(Path(a.sit), Path(a.out), a.rollouts, a.per_tag, a.seed, a.only_tag)


if __name__ == "__main__":
    main()
