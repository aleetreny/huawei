#!/usr/bin/env python3
"""Run memory for the career-rules Skill: the agent passes a few numbers from the observe it just answered;
this script keeps the run's own record in one small file and prints a one-line briefing.

It uses only what the official tools returned in this run (the stats in observe, the HR remark as the agent
classified it, the quarterly actions the agent took) and the handbook's published action directions. It never
sees event text and knows nothing about any event. The record belongs to one run: a new session id starts it
from scratch, so nothing is carried from one run to the next.

Usage (from the agent's projects folder; one line):
  python3 ../skills/career-rules/script/brief.py <sid> <month> <level> <H> <D> <S> <N> <O> <W> <hr> [q=E,E,E:M] [b]

  sid      first 8 characters of the session_id from new_game
  month    current_month; level: the number of the level (L3 -> 3)
  H D S N O W   Health, Dignity, Skill, Network, Output, Wealth as observe showed them
  hr       the latest HR remark: 0 friendly, 1 quiet, 2 frowning, 3 uneasy or "on your own", 4 angry
  q=...    in a quarterly reply: the Energy choice numbers and the main-action number just sent (e.g. q=7,7,7:1)
  b        the events reported a blow-up of old risks this month

Prints one line, for example:
  Best S9 N3 O3 | full: N at 3 | Health 4: recover | quarter plan: Energy 7,7,7 then main 1
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

STATE = Path("career-brief-state.json")   # in the current working directory (the agent's projects folder)
GROWTH = ("S", "N", "O")
# Quarterly menus in the order the game lists them (the handbook's order), with the published directions.
ENERGY = {1: ("High-intensity work", "O", 2), 2: ("Skill learning", "S", 2), 3: ("Network maintenance", "N", 1),
          4: ("Defuse legacy risk", "", 2), 5: ("Mental recovery", "", 1), 6: ("Health recovery", "", 1),
          7: ("Prepare report materials", "O", 1), 8: ("Reserve energy", "", 0)}
MAIN = {1: ("Apply for a key project", "SNO"), 2: ("Report results to your manager", "NO"), 3: ("Fight for resources", "NO"),
        4: ("Apply for rotation", "SN"), 5: ("Showcase results", "O"), 6: ("Build a mentorship", "SN"),
        7: ("Repair a key relationship", "N"), 8: ("Lay low and reduce risk", ""), 9: ("No action", "")}
# Our own margins on the published 0-10 ranges (not game thresholds).
HEALTH_LOW, DIGNITY_LOW = 5, 4


def load(sid: str) -> dict:
    try:
        d = json.loads(STATE.read_text())
        if d.get("sid") == sid:
            return d
    except (OSError, ValueError):
        pass
    return {"sid": sid, "level": None, "since": 1, "best": {}, "full": {}, "pending": None, "hist": [], "blowups": 0}


def plan_quarter(d: dict, month: int, level: int, h: float, dg: float, now: dict, w: float, hr: int) -> str:
    """The Skill's quarterly lines, with stats the run has shown to be full skipped."""
    full = lambda s: s in d["full"] and now[s] >= d["full"][s]
    energy, left = [], 3
    stalled_start = level == 1 and month - d["since"] + 1 >= 12

    def add(n: int) -> None:
        nonlocal left
        energy.append(n)
        left -= ENERGY[n][2]

    if month >= 48:
        if hr > 0:
            add(4)
        while left >= 1 and (h < 10 or dg < 10):
            add(6 if h < 10 else 5)
            h, dg = (h + 2, dg) if energy[-1] == 6 else (h, dg + 2)
        while left >= 1:
            add(3)
        return f"Energy {','.join(map(str, energy))} then main {8 if hr > 0 else 2}"
    falling = len(d["hist"]) >= 3 and d["hist"][-1][1] < d["hist"][-2][1] < d["hist"][-3][1]
    h0 = h
    near = h0 <= DIGNITY_LOW or dg <= DIGNITY_LOW or w < 0 or now["N"] <= 0 or falling   # Quarterly line 2
    while left >= 1 and h <= HEALTH_LOW:          # Health 5 or below: recovery first with the Energy
        add(6)
        h += 2
    if near:
        if left >= 1 and dg <= DIGNITY_LOW:
            add(5)
        if left >= 1 and now["N"] <= 0:
            add(3)
    if hr >= 1 and left >= 2 and 4 not in energy:   # Quarterly line 3
        add(4)
    main = 8 if hr >= 2 or (stalled_start and hr >= 1) else None
    if near and main is None:
        main = 8 if h0 <= DIGNITY_LOW or falling else 7
    if level >= 4:
        if left >= 2 and h > HEALTH_LOW and not near and not full("S"):
            add(2)
        order = (3, 7) if now["N"] < d["best"].get("N", 0) and not full("N") else (7, 3)
        main = main or 4
    elif level >= 2:
        order = (3, 7, 3) if now["N"] < d["best"].get("N", 0) else (7, 3, 7)
        main = main or 1
    else:
        order = (7, 7, 7)
        main = main or 1
    for n in order:
        if left < 1:
            break
        stat = ENERGY[n][1]
        if full(stat):
            alt = [m for m in (7, 3) if not full(ENERGY[m][1])]
            n = alt[0] if alt else (6 if h < 10 else 5)
        add(n)
    while left >= 1:
        add(6 if h < 10 else (5 if dg < 10 else 3))
    return f"Energy {','.join(map(str, energy))} then main {main}"


def main(argv: list[str]) -> str:
    if len(argv) < 11:
        return "usage: brief.py sid month level H D S N O W hr [q=E,E,E:M] [b]"
    sid = argv[1][:8]
    month, level = int(float(argv[2])), int(float(str(argv[3]).lstrip("Ll")))
    h, dg, s, n, o, w = (float(x) for x in argv[4:10])
    hr = int(float(argv[10]))
    extra = argv[11:]
    blew = "b" in extra
    q = next((x[2:] for x in extra if x.startswith("q=")), None)
    now = {"S": s, "N": n, "O": o}
    d = load(sid)
    if d["level"] != level:                      # new run or a promotion: the level's record starts again
        d.update(level=level, since=month if d["level"] is not None else 1, best={}, full={}, pending=None)
    p = d["pending"]
    if p and month > p["month"]:                 # first call after a quarter: did each bought stat rise?
        if not blew:
            for stat, k in p["bought"].items():
                if now[stat] < p["before"][stat] + k:
                    d["full"][stat] = now[stat]
        d["pending"] = None
    for stat in list(d["full"]):                 # a stat that fell below its mark can rise again
        if now[stat] < d["full"][stat]:
            del d["full"][stat]
    for stat in GROWTH:
        d["best"][stat] = max(d["best"].get(stat, now[stat]), now[stat])
    if blew and d.get("blew_month") != month:   # count each blow-up once, however often it is reported
        d["blowups"] += 1
        d["blew_month"] = month
    if not d["hist"] or d["hist"][-1][0] != month:
        d["hist"] = (d["hist"] + [[month, h]])[-6:]
    if q:                                        # quarter just sent: remember what it should have raised
        bought: dict[str, int] = {}
        en, _, mn = q.partition(":")
        for x in [e for e in en.split(",") if e.strip()]:
            stat = ENERGY.get(int(x), ("", "", 0))[1]
            if stat:
                bought[stat] = bought.get(stat, 0) + 1
        for stat in MAIN.get(int(mn), ("", ""))[1] if mn.strip() else "":
            bought[stat] = bought.get(stat, 0) + 1
        d["pending"] = {"month": month, "before": now, "bought": bought}
    out = [f"Best S{d['best']['S']:g} N{d['best']['N']:g} O{d['best']['O']:g}"]
    under = [x for x in GROWTH if now[x] < d["best"][x]]
    if under:
        out.append("under Best: " + ",".join(under))
    if d["full"]:
        out.append("full: " + ", ".join(f"{x} at {v:g}" for x, v in d["full"].items()))
    if h <= 3:
        out.append(f"Health {h:g}: drop anything that lowers it")
    elif h <= HEALTH_LOW:
        out.append(f"Health {h:g}: recover")
    if level == 1 and month - d["since"] + 1 >= 12:
        out.append("stalled start: risk first")
    if d["blowups"]:
        out.append(f"blow-ups so far {d['blowups']}: a second ends the run")
    if month % 3 == 0 and not q:
        out.append("quarter plan: " + plan_quarter(d, month, level, h, dg, now, w, hr))
    STATE.write_text(json.dumps(d))
    return " | ".join(out)


if __name__ == "__main__":
    print(main(sys.argv))
