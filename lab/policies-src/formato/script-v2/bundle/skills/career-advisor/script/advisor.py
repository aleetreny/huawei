#!/usr/bin/env python3
"""Career advisor: turns what the agent read this turn into one choice, the same way every time.

The agent reads the situation (its stats, the HR partner's tone, and how each story option is likely to
move each stat) and passes it here in one line. This script only does bookkeeping and arithmetic on that
line and on the stats it saw on earlier calls of the same game. It knows nothing about any event: it never
sees event titles or story text, only the agent's own reading of each option.

Usage (one line, quoted):
  python3 advisor.py "sid=<session_id> m=<month> H=<h> D=<d> S=<s> N=<n> O=<o> W=<w> L=<level> E=<energy>
                      hr=<0-4> phase=story | 1: S+ N+ | 2: O+ N- R+ | 3: H- O+ R-"
  phase=energy or phase=main for the quarterly menus (no options needed).

Option reading, per option: a stat letter (H Health, D Dignity, S Skill, N Network, O Output, W Wealth)
followed by + (rises), ++ (rises strongly), - (falls) or -- (falls strongly); R+ if the option may bury a
problem (hidden risk rises), R- if it clears one. Leave out what does not move.

Memory: one small JSON file per game (keyed by session id) in ./state next to this script. It holds the
stats seen on the previous call and the gains that stopped registering (a stat that "stalls"). Nothing
else is read or written.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STATS = ("health", "dignity", "skill", "network", "output", "wealth")
LETTER = {"H": "health", "D": "dignity", "S": "skill", "N": "network", "O": "output", "W": "wealth"}
GROWTH = ("skill", "network", "output")
UNKNOWN = 1e9
# Policy knobs (our own prudence settings, not game rules).
P = {"h_recover": 6, "h_floor": 2, "h_w": 0.5, "risk_base": 4.0, "risk_hr": 3.0, "risk_veto_hr": 1,
     "risk_veto": 20.0, "defuse_hr": 1, "laylow_hr": 1, "h_minus": 2.0,
     "guard": (5,), "guard_w": 6.0, "push_w": 0.0, "surprise_w": 0.0, "surprise_decay": 0.5,
     "story_detect": 0, "rminus_w": 1.0}

# Quarterly menus, as published in the employee handbook (signs) and the in-game menu text ("solid",
# "strongly" = 2). Energy cost per action is published. Menu order is the order the game lists them.
ENERGY = [  # (name, effect, cost, risk sign)
    ("High-intensity work", {"output": 1, "health": -1, "dignity": -1}, 2, 1),
    ("Skill learning", {"skill": 1, "health": -1}, 2, 0),
    ("Network maintenance", {"network": 1, "dignity": 1}, 1, 0),
    ("Defuse legacy risk", {}, 2, -1),
    ("Mental recovery", {"dignity": 2}, 1, 0),
    ("Health recovery", {"health": 2}, 1, 0),
    ("Prepare report materials", {"output": 1, "dignity": 1}, 1, 0),
    ("Reserve energy (no action)", {}, 0, 0),
]
MAIN = [
    ("Apply for a key project", {"output": 1, "skill": 1, "network": 1}, 0),
    ("Report results to your manager", {"output": 1, "network": 1, "dignity": 1}, 0),
    ("Fight for resources", {"output": 1, "network": 1}, 0),
    ("Apply for rotation", {"skill": 2, "network": 1}, 0),
    ("Showcase results", {"output": 1, "dignity": 1}, 0),
    ("Build a mentorship", {"skill": 1, "network": 1}, 0),
    ("Repair a key relationship", {"network": 1, "dignity": 1}, 0),
    ("Lay low and reduce risk", {"health": 1}, -1),
    ("No action", {}, 0),
]


# ----------------------------------------------------------------------------------------- parsing
def parse(line: str) -> tuple[dict, dict[int, tuple[dict, int]]]:
    head, *opts = line.split("|")
    kv = dict(re.findall(r"([A-Za-z]+)\s*=\s*([^\s|]+)", head))
    st = {"sid": kv.get("sid", "nosid"), "phase": kv.get("phase", "story").lower()}
    for key, name in (("m", "month"), ("L", "level"), ("E", "energy"), ("hr", "hr")):
        v = re.sub(r"[^0-9.\-]", "", kv.get(key, ""))
        st[name] = int(float(v)) if v else None
    for letter, name in LETTER.items():
        v = re.sub(r"[^0-9.\-]", "", kv.get(letter, ""))
        st[name] = float(v) if v else None
    options: dict[int, tuple[dict, int]] = {}
    for o in opts:
        m = re.match(r"\s*(\d+)\s*[:.)]?(.*)", o)
        if not m:
            continue
        fx, risk = {}, 0
        for tok, sign in re.findall(r"\b([HDSNOWR])\s*([+\-]{1,2})", m.group(2).upper()):
            size = len(sign) * (1 if sign[0] == "+" else -1)
            if tok == "R":
                risk = 1 if size > 0 else -1
            else:
                fx[LETTER[tok]] = fx.get(LETTER[tok], 0) + size
        options[int(m.group(1))] = (fx, risk)
    return st, options


# ----------------------------------------------------------------------------------------- memory
class Memory:
    def __init__(self, sid: str, root: Path | None = None) -> None:
        self.path = None
        self.d = {"caps": {}, "prev": None, "hr": 0, "hr_month": None, "risk_since": 0}
        if root is not None:
            safe = re.sub(r"[^A-Za-z0-9_-]", "", sid)[:64] or "nosid"
            self.path = root / f"{safe}.json"
            try:
                self.d.update(json.loads(self.path.read_text()))
            except (OSError, ValueError):
                pass

    def save(self) -> None:
        if self.path is None:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.d))
        except OSError:
            pass

    def cap(self, level: int, k: str) -> float:
        return self.d["caps"].get(f"{level}:{k}", UNKNOWN)


def learn(mem: Memory, st: dict) -> None:
    """Compare these stats with the last call: a published gain (quarterly action) that did not register
    means the stat has stalled at this level. Also refresh the risk estimate from the HR tone."""
    prev = mem.d.get("prev")
    if prev and prev.get("level") == st["level"] and prev.get("read") and P["story_detect"]:
        for k, x in prev["read"].items():  # a story gain you expected that did not move the stat
            if k in GROWTH and x > 0 and st.get(k) is not None and prev.get(k) is not None and st[k] <= prev[k]:
                key = f"{st['level']}:{k}"
                hits = mem.d.setdefault("stall_hits", {})
                hits[key] = hits.get(key, 0) + 1 if hits.get(key + "@") == st[k] else 1
                hits[key + "@"] = st[k]
                if hits[key] >= P["story_detect"]:
                    mem.d["caps"][key] = st[k]
    if prev and prev.get("level") == st["level"] and prev.get("expect"):
        for k, x in prev["expect"].items():
            if k in GROWTH and x > 0 and st.get(k) is not None and prev.get(k) is not None and st[k] < prev[k] + x:
                mem.d["caps"][f"{st['level']}:{k}"] = st[k]
    if st["hr"] is not None and st["month"] != mem.d.get("hr_month"):
        if mem.d.get("hr_month") is not None:  # HR worry rose more than the flagged picks explain
            expected = max(0, min(4, mem.d.get("hr", 0) + mem.d.get("risk_since", 0)))
            sur = mem.d.get("surprise", 0.0) * P["surprise_decay"] + max(0, min(4, st["hr"]) - expected)
            mem.d["surprise"] = sur
        mem.d["hr"], mem.d["hr_month"], mem.d["risk_since"] = max(0, min(4, st["hr"])), st["month"], 0
    elif st["hr"] is not None and st["hr"] > mem.d.get("hr", 0):
        mem.d["hr"] = min(4, st["hr"])


def risk_level(mem: Memory) -> int:
    return max(0, min(4, mem.d.get("hr", 0) + mem.d.get("risk_since", 0)))


# ----------------------------------------------------------------------------------------- valuation
def value(st: dict, mem: Memory, fx: dict, risk: int) -> float:
    lv, month = st["level"] or 1, st["month"] or 1
    pre_review = month % 6 in P["guard"]
    endgame = month >= 46
    v = 0.0
    at_cap = {k: (st[k] or 0) >= mem.cap(lv, k) for k in GROWTH}
    for k in GROWTH:
        x, cur, c = fx.get(k, 0), st[k] or 0, mem.cap(lv, k)
        gain = min(c, cur + x) - min(c, cur) if x > 0 else x
        w = 1.0 + 2.0 * max(0.0, (c - cur) / max(1.0, c))
        if k == "skill" and at_cap["network"] and at_cap["output"]:
            w += 2.0
        if pre_review and x < 0:
            w += P["guard_w"]
        if pre_review and x > 0 and c >= UNKNOWN:
            w += P["push_w"]
        if endgame:
            w = 0.0 if k == "output" else 0.3
        v += w * gain
    hx = fx.get("health", 0)
    h = min(10, (st["health"] or 0) + (hx * P["h_minus"] if hx < 0 else hx))
    d = min(10, (st["dignity"] or 0) + fx.get("dignity", 0))
    dh, dd = h - (st["health"] or 0), d - (st["dignity"] or 0)
    v += P["h_w"] * dh + 0.5 * dd
    if endgame:
        v += 0.8 * (dh + dd)
    if h <= P["h_floor"]:
        v -= 30
    if d < 5:  # below half of Dignity's published 0-10 range
        v -= 3 * (5 - d)
    wl = fx.get("wealth", 0)
    if wl < 0:
        wl *= (lv + 1) // 2
    v += 0.5 * wl
    hr = risk_level(mem)
    if risk >= 0:  # after unexplained HR worry, options that do not clear risk are less trusted
        v -= P["surprise_w"] * min(2.0, mem.d.get("surprise", 0.0))
    v -= risk * (P["risk_base"] + P["risk_hr"] * hr) * (P["rminus_w"] if risk < 0 else 1.0)
    if risk > 0 and hr >= P["risk_veto_hr"]:
        v -= P["risk_veto"]
    if endgame:
        v -= 3.0 * risk
    return v


# ----------------------------------------------------------------------------------------- decisions
def decide_story(st: dict, mem: Memory, options: dict[int, tuple[dict, int]]) -> int:
    best, bv = min(options) if options else 1, -1e18
    for k in sorted(options):
        fx, risk = options[k]
        v = value(st, mem, fx, risk)
        if v > bv:
            best, bv = k, v
    return best


def decide_energy(st: dict, mem: Memory) -> int:
    e, hr = st["energy"] or 0, risk_level(mem)
    names = [a[0] for a in ENERGY]
    if (st["health"] or 0) <= P["h_recover"] and e >= 1:
        return names.index("Health recovery") + 1
    if hr >= P["defuse_hr"] and e >= 2:
        return names.index("Defuse legacy risk") + 1
    if (st["month"] or 0) >= 46:
        if hr > 0 and e >= 2:
            return names.index("Defuse legacy risk") + 1
        if (st["health"] or 0) < 10 and e >= 1:
            return names.index("Health recovery") + 1
        if (st["dignity"] or 0) < 10 and e >= 1:
            return names.index("Mental recovery") + 1
    best, bv = None, 0.0
    for i, (name, fx, cost, risk) in enumerate(ENERGY):
        if name in ("High-intensity work", "Defuse legacy risk", "Reserve energy (no action)") or cost > e:
            continue
        v = value(st, mem, fx, 0) / cost
        if v > bv:
            best, bv = i + 1, v
    return best or names.index("Reserve energy (no action)") + 1


def decide_main(st: dict, mem: Memory) -> int:
    names = [a[0] for a in MAIN]
    hr = risk_level(mem)
    if hr >= P["laylow_hr"] or ((st["month"] or 0) >= 46 and hr > 0):
        return names.index("Lay low and reduce risk") + 1
    return max(range(len(MAIN)), key=lambda i: value(st, mem, MAIN[i][1], 0)) + 1


def plan_quarter(st: dict, mem: Memory) -> tuple[list[int], int, dict]:
    """The whole quarter at once: Energy picks one by one on the expected state, then the main action."""
    cur = dict(st)
    total: dict[str, float] = {}
    picks: list[int] = []
    for _ in range(4):
        k = decide_energy(cur, mem)
        name, fx, cost, risk = ENERGY[k - 1]
        picks.append(k)
        if cost == 0:
            break
        for s_, x in fx.items():
            if s_ in GROWTH and x > 0:
                x = max(0.0, min(mem.cap(cur["level"] or 1, s_), (cur[s_] or 0) + x) - (cur[s_] or 0))
            cur[s_] = (cur[s_] or 0) + x
            total[s_] = total.get(s_, 0) + x
        cur["energy"] = (cur["energy"] or 0) - cost
        mem.d["risk_since"] = mem.d.get("risk_since", 0) + risk
        if (cur["energy"] or 0) <= 0:
            picks.append(len(ENERGY))
            break
    m = decide_main(cur, mem)
    for s_, x in MAIN[m - 1][1].items():
        total[s_] = total.get(s_, 0) + x
    mem.d["risk_since"] = mem.d.get("risk_since", 0) + MAIN[m - 1][2]
    return picks, m, total


def track_best(mem: Memory, st: dict) -> None:
    best = mem.d.setdefault("best", {})
    for g in GROWTH:
        key = f"{st['level']}:{g}"
        if st.get(g) is not None:
            best[key] = max(best.get(key, -1e9), st[g])


def status_line(st: dict, mem: Memory) -> str:
    lv, m = st["level"] or 1, st["month"] or 1
    best = mem.d.get("best", {})
    stalled = [g[0].upper() for g in GROWTH if mem.cap(lv, g) < UNKNOWN]
    review_in = 6 - (m % 6) if m % 6 else 6
    now = " ".join(f"{g[0].upper()}{st[g]:g}" for g in GROWTH if st.get(g) is not None)
    bst = " ".join(f"{g[0].upper()}{best.get(f'{lv}:{g}', st.get(g) or 0):g}" for g in GROWTH)
    below = [g[0].upper() for g in GROWTH if st.get(g) is not None and st[g] < best.get(f"{lv}:{g}", st[g])]
    tail = f" | Below best: {''.join(below)}" if below else ""
    return f"Review in {review_in} | Now {now} | Best {bst} | Stalled: {', '.join(stalled) or 'none'}{tail}"


def step(st: dict, options: dict[int, tuple[dict, int]], mem: Memory) -> tuple[int, str]:
    """One decision: learn from the stats, choose, and remember what the choice should do."""
    learn(mem, st)
    track_best(mem, st)
    phase = st["phase"]
    if phase.startswith("stat"):
        mem.d["prev"] = {**{s: st[s] for s in STATS}, "level": st["level"], "month": st["month"], "expect": {}, "read": {}}
        return 0, "status"
    if phase.startswith("q"):
        picks, m, total = plan_quarter(st, mem)
        mem.d["prev"] = {**{s: st[s] for s in STATS}, "level": st["level"], "month": st["month"], "expect": total,
                         "read": {}}
        mem.d["plan"] = {"energy": picks, "main": m}
        return picks[0], "quarter"
    if phase.startswith("en"):
        k = decide_energy(st, mem)
        name, fx, risk = ENERGY[k - 1][0], ENERGY[k - 1][1], ENERGY[k - 1][3]
    elif phase.startswith("ma"):
        k = decide_main(st, mem)
        name, fx, risk = MAIN[k - 1][0], MAIN[k - 1][1], MAIN[k - 1][2]
    else:
        k = decide_story(st, mem, options)
        name, fx, risk = "", {}, options.get(k, ({}, 0))[1]
    mem.d["risk_since"] = mem.d.get("risk_since", 0) + risk
    mem.d["prev"] = {**{s: st[s] for s in STATS}, "level": st["level"], "month": st["month"], "expect": fx,
                     "read": options.get(k, ({}, 0))[0] if not name else {}}
    return k, name


def run(line: str, root: Path | None) -> str:
    st, options = parse(line)
    mem = Memory(st["sid"], root)
    k, name = step(st, options, mem)
    mem.save()
    if name == "status":
        return f"STATUS: {status_line(st, mem)} | HR {risk_level(mem)}"
    if name == "quarter":
        plan = mem.d["plan"]
        en = ", then ".join(f"{i} ({ENERGY[i - 1][0]})" for i in plan["energy"])
        mi = plan["main"]
        return (f"ENERGY, one pick per take_action in this order: {en}\n"
                f"MAIN: {mi} ({MAIN[mi - 1][0]})\n"
                f"STATUS: {status_line(st, mem)}")
    lv = st["level"] or 1
    stalled = [g[0].upper() for g in GROWTH if mem.cap(lv, g) < UNKNOWN]
    review_in = 6 - ((st["month"] or 1) % 6) if (st["month"] or 1) % 6 else 6
    label = f" ({name})" if name else ""
    return (f"CHOOSE {k}{label}\n"
            f"NOTE: Review in {review_in} | Stalled {''.join(stalled) or 'none'} | HR {risk_level(mem)} | advisor {k}")


def main() -> None:
    line = " ".join(sys.argv[1:]) or sys.stdin.read()
    print(run(line, Path(__file__).resolve().parent / "state"))


if __name__ == "__main__":
    main()
