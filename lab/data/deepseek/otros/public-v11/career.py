#!/usr/bin/env python3
"""career-state: what is true now, what this pick is worth, what the last pick cost.

Reads the game's own log file (the log_file that check_latest_logs returns) and
the visible stats the agent passes in. Two commands:

  python3 career.py brief   --stats "m5 L1 H8 D10 S9 N3 O3 W2 E0" --log <log_file>
  python3 career.py quarter --stats "m6 L1 H8 D10 S9 N3 O3 W2 E3" --log <log_file>

brief   before every story event: state line, MODE line, feedback lines.
quarter on the Energy and main-action screens: the exact action to take now.

Nothing here is an event answer or a hidden threshold. The script never sees the
options of the current event. Stat limits are found during the run: when a gain
shown in the log does not appear in the visible stats, that stat has reached
this level's limit.
"""
import argparse
import itertools
import json
import os
import re
import tempfile

STATE_NAME = "career_state.json"
PROMO = ("O", "N", "S")
NAMES = {"S": "Skill", "N": "Network", "O": "Output", "H": "Health", "D": "Dignity", "W": "Wealth"}
HR_STEPS = [("waiting for", 4), ("on your own", 3), ("piled up", 2), ("some risk", 1), ("all right", 0)]
HR_TEXT = {0: "doing all right", 1: "some risk lately", 2: "risks have piled up",
           3: "on your own now", 4: "what were you waiting for"}
RISK_LEFT = re.compile(r"risk (stays|remains|is still there)|still there|does not remove|not removed|"
                       r"reduces the risk|remaining risk|left open|buried", re.I)
DELTA = re.compile(r"\b(Skill|Network|Output|Health|Dignity|Wealth) ([+-]\d+)")
ENERGY = {"Health recovery": 1, "Mental recovery": 1, "Network maintenance": 1,
          "Prepare report materials": 1, "Skill learning": 2, "Defuse legacy risk": 2}
QUARTER_TITLES = ("quarterly energy allocation", "quarterly main action")


# ---------------------------------------------------------------- input

def parse_stats(text):
    """Read 'm5 L1 H8 D10 S9 N3 O3 W2 E3' or the observe JSON (lenient)."""
    st = {}
    text = text or ""
    if text.strip().startswith("{"):
        try:
            js = json.loads(text)
            cs = js.get("current_state", js)
            status = cs.get("status", cs)
            time = cs.get("time", {})
            st["m"] = int(time.get("current_month", status.get("current_month", 0)) or 0)
            st["L"] = int(re.sub(r"\D", "", str(status.get("level", "L0"))) or 0)
            for k, key in (("H", "health"), ("D", "dignity"), ("S", "skill"), ("N", "network"),
                           ("O", "output"), ("W", "wealth"), ("E", "energy")):
                if key in status:
                    st[k] = float(status[key]) if k == "W" else int(status[key])
            return st
        except Exception:
            pass
    for key, val in re.findall(r"\b([mLHDSNOWE])\s*[=:]?\s*(-?\d+(?:\.\d+)?)", text):
        if key not in st:
            st[key] = float(val) if key == "W" else int(float(val))
    return st


def parse_log(path):
    info = dict(level_by_month={}, hr=[], cuts=[], left=[], choices=[], grades=[], talk=None,
                promotions=[], blowups=[], last_month=0)
    if not path or not os.path.exists(path):
        return None
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    month, hdr = 0, None
    for i, ln in enumerate(lines):
        m = re.match(r"\[(\w+)\] Month (\d+) \| (.*)", ln)
        if m:
            hdr = (m.group(1), m.group(3).strip())
            month = int(m.group(2))
            info["last_month"] = max(info["last_month"], month)
            if m.group(1) == "event" and i + 1 < len(lines) and lines[i + 1].startswith("Outcome:"):
                if RISK_LEFT.search(lines[i + 1]):
                    info["left"].append(month)
            continue
        if ln.startswith("Chose #") and hdr:
            opt = ln.split(":", 1)[1].strip() if ":" in ln else ln
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            d = {k[0]: int(v) for k, v in DELTA.findall(nxt)}
            quarter = hdr[1].lower() in QUARTER_TITLES
            info["choices"].append(dict(month=month, kind=hdr[0], title=hdr[1], opt=opt, d=d, quarter=quarter, idx=i))
            if opt.startswith("Defuse legacy risk") or opt.startswith("Lay low"):
                info["cuts"].append(month)
            continue
        lm = re.match(r"\[salary\] Monthly base salary: .*\(L(\d+)\)", ln)
        if lm:
            info["level_by_month"][month] = int(lm.group(1))
        gm = re.match(r"\[salary\] Half-year performance bonus \((\w)\)", ln)
        if gm:
            info["grades"].append((month, gm.group(1), i))
        if ln.startswith("[talk]"):
            rest = [x.strip() for x in lines[i + 1:i + 4] if x.strip()]
            info["talk"] = (month, rest[0][:160] if rest else "")
        if ln.startswith("[promotion]"):
            pm = re.search(r"to L(\d+)", ln)
            info["promotions"].append(month)
            info["promoted_to"] = int(pm.group(1)) if pm else None
        if "HR partner" in ln:
            step = next((v for k, v in HR_STEPS if k in ln), None)
            if step is not None:
                info["hr"].append((month, step))
        if "go off at once" in ln or "Trust crisis" in ln:
            info["blowups"].append(month)
    return info


# ---------------------------------------------------------------- state

def state_path():
    for base in (os.getcwd(), tempfile.gettempdir()):
        p = os.path.join(base, STATE_NAME)
        try:
            with open(p, "a"):
                pass
            return p
        except Exception:
            continue
    return None


def load_state(p):
    try:
        with open(p) as f:
            s = json.load(f)
            if isinstance(s, dict):
                return s
    except Exception:
        pass
    return {}


def save_state(p, s):
    try:
        with open(p, "w") as f:
            json.dump(s, f)
    except Exception:
        pass


def update_limits(state, st, info):
    """Mark a stat as at its level limit when logged gains did not show up."""
    limits = state.setdefault("limits", {})
    peaks = state.setdefault("peaks", {})
    L = str(st.get("L", 0))
    lim = limits.setdefault(L, {})
    peak = peaks.setdefault(L, {})
    prev = state.get("prev")
    seen = state.get("seen_choices", 0)
    new = info["choices"][seen:] if info else []
    for k in PROMO:
        if k in st:
            peak[k] = max(peak.get(k, -999), st[k])
    if prev and str(prev.get("L")) == L and info is not None and len(info["choices"]) >= seen:
        for k in PROMO:
            if k not in st or k not in prev:
                continue
            gain = sum(c["d"].get(k, 0) for c in new)
            pos = sum(max(0, c["d"].get(k, 0)) for c in new)
            actual = st[k] - prev[k]
            if pos > 0 and actual < gain and st[k] >= peak.get(k, st[k]):
                lim[k] = st[k]
    for k in list(lim):
        if k in st and st[k] > lim[k]:
            del lim[k]          # it rose past the mark, so it was not the limit
    state["prev_old"], state["seen_old"] = prev, seen     # kept for the review summary
    state["prev"] = {k: st.get(k) for k in ("m", "L") + PROMO}
    if info is not None:
        state["seen_choices"] = len(info["choices"])
    return lim


def resolve_log(given, state, st):
    """Use the given log; otherwise the remembered one, unless it belongs to an older game."""
    log = given or state.get("log", "")
    if given or not log:
        return log
    stale = not os.path.exists(log)
    if not stale and st.get("m"):
        info = parse_log(log)
        stale = info is not None and info["last_month"] > st["m"] + 1
    if stale:
        folder = os.path.dirname(log)
        try:
            logs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".log")]
            if logs:
                return max(logs, key=os.path.getmtime)
        except Exception:
            pass
    return log


# ---------------------------------------------------------------- facts

def risk_now(info):
    if not info or not info["hr"]:
        return 0, None
    month, step = info["hr"][-1]
    return step, month


def months_since(lst, m):
    return m - max(lst) if lst else m


def at_limit(st, lim, k):
    return k in lim and k in st and st[k] >= lim[k]


def review_info(m, info=None):
    """Next review month, the month whose end it reads, and whether this is a pre-review month.

    The half-year talk can be logged before the last event that observe still labels
    month 5, 11, ...; once the talk for this window is in the log, the review is done.
    """
    nxt = ((m // 6) + 1) * 6 if m % 6 else m + 6
    pre = (m % 6) in (4, 5)
    if pre and info and info["grades"] and info["grades"][-1][0] >= nxt - 1:
        pre = False
        nxt += 6
    return nxt, nxt - 1, pre


def short_opt(opt, n=48):
    return opt if len(opt) <= n else opt[:n].rsplit(" ", 1)[0] + "..."


def fmt_delta(d):
    order = ("O", "N", "S", "H", "D", "W")
    return ", ".join("%s %+d" % (NAMES[k], d[k]) for k in order if d.get(k))


def last_pick(info):
    for c in reversed(info["choices"] if info else []):
        if not c["quarter"] and c["title"].lower() != "new hire handbook":
            return c
    return None


def costly_since(info, first_month, keys=("O", "N")):
    """Story picks from first_month on that lowered one of keys."""
    out = []
    for c in info["choices"] if info else []:
        if c["quarter"] or c["month"] < first_month:
            continue
        if any(c["d"].get(k, 0) < 0 for k in keys):
            out.append(c)
    return out


def stats_at_talk(state, info, lim, gidx):
    """Stats when the review ran: the last observed stats plus the picks logged before the talk."""
    prev, seen = state.get("prev_old"), state.get("seen_old")
    if not prev or seen is None:
        return None
    est = {}
    for k in PROMO:
        if prev.get(k) is None:
            return None
        v = prev[k]
        for c in info["choices"][seen:]:
            if c["idx"] < gidx:
                v += c["d"].get(k, 0)
                if k in lim:
                    v = min(v, lim[k])
        est[k] = v
    return est


# ---------------------------------------------------------------- planning (quarter)

def plan_final(st, r):
    """Month 48: every remaining point should buy final score (Output is not scored)."""
    H, D = st.get("H", 10), st.get("D", 10)
    H_after_main = min(10, H + 1)       # main action Lay low adds Health +1
    best = (-1, [])
    acts = ["Health recovery", "Mental recovery", "Network maintenance", "Defuse legacy risk"]
    for n in range(0, 4):
        for combo in itertools.combinations_with_replacement(acts, n):
            cost = sum(ENERGY[a] for a in combo)
            if cost > st.get("E", 3):
                continue
            h, d, v = H_after_main, D, 0.0
            for a in combo:
                if a == "Health recovery":
                    g = min(2, 10 - h); h += g; v += 0.75 * g
                elif a == "Mental recovery":
                    g = min(2, 10 - d); d += g; v += 0.75 * g
                elif a == "Network maintenance":
                    v += 0.17 + (0.75 if d < 10 else 0); d = min(10, d + 1)
                elif a == "Defuse legacy risk":
                    v += 1.0 if r >= 1 else 0.6
            if v > best[0] + 1e-9:
                best = (v, list(combo))
    return best[1] or ["Network maintenance"]


def plan_energy(st, info, lim, state):
    m, L = st.get("m", 0), st.get("L", 1)
    E = st.get("E", 3)
    H, D = st.get("H", 10), st.get("D", 10)
    r, _ = risk_now(info)
    cuts = info["cuts"] if info else []
    left_since_cut = bool(info) and any(x >= (max(cuts) if cuts else 0) for x in info["left"])
    since_cut = months_since(cuts, m)
    why = []
    if m >= 48:
        return plan_final(st, r), ["last quarter: points go to final Health, Dignity and risk (Output is not scored)"]
    steps = []
    if H <= 3:
        steps += ["Health recovery", "Health recovery"][:E]; why.append("Health %d is dangerous" % H)
    elif H <= 5:
        steps += ["Health recovery"][:E]; why.append("Health %d needs a buffer" % H)
    if D <= 4 and E - len(steps) >= 1:
        steps += ["Mental recovery"]; why.append("Dignity %d is low" % D)
    capped_all = all(at_limit(st, lim, k) for k in ("O", "N"))
    if L <= 1:
        # At L1 the next review is two months away and O/N must be at the limit first.
        defuse = r >= 2 or ((r >= 1 or left_since_cut) and capped_all)
    else:
        defuse = r >= 1 or left_since_cut or since_cut >= 9
    if m >= 43 and (r >= 1 or left_since_cut or since_cut >= 6):
        defuse = True
    if state.get("defused_q") == m:
        defuse = False
    used = sum(ENERGY[a] for a in steps)
    if defuse and E - used >= 2:
        steps.append("Defuse legacy risk")
        used += 2
        why.append("risk: HR says '%s'%s%s" % (HR_TEXT[r], ", an outcome said a risk remains" if left_since_cut else "",
                                             "" if r or left_since_cut else ", no risk cut for %d months" % since_cut))
    rem = E - used
    open_stats = [k for k in ("O", "N") if not at_limit(st, lim, k)]
    if open_stats:
        growth = state.get("growth", {})
        open_stats.sort(key=lambda k: (growth.get(k, 0), st.get(k, 0)))
        action = {"O": "Prepare report materials", "N": "Network maintenance"}
        i = 0
        while rem >= 1:
            steps.append(action[open_stats[i % len(open_stats)]] if i < 2 or len(open_stats) == 1
                         else action[open_stats[0]])
            rem -= 1
            i += 1
        why.append("still below this level's limit: " + ", ".join(NAMES[k] for k in open_stats))
    else:
        if rem >= 2 and L >= 3 and not at_limit(st, lim, "S") and H >= 6:
            steps.append("Skill learning"); rem -= 2
            why.append("Output and Network are at this level's limit, so Skill is the open stat")
        if rem >= 2 and "Defuse legacy risk" not in steps:
            steps.append("Defuse legacy risk"); rem -= 2
            why.append("nothing else can grow, so clear hidden risk")
        while rem >= 1:
            steps.append("Health recovery" if H < 10 else "Network maintenance"); rem -= 1
    return steps, why


def plan_main(st, info, lim):
    m, L, H = st.get("m", 0), st.get("L", 1), st.get("H", 10)
    r, _ = risk_now(info)
    if m >= 48:
        return "Lay low and reduce risk", "last quarter: lower final risk and add Health"
    if H <= 3:
        return "Lay low and reduce risk", "Health %d" % H
    if r >= 2:
        return "Lay low and reduce risk", "HR says '%s'" % HR_TEXT[r]
    if m >= 43 and r >= 1:
        return "Lay low and reduce risk", "close-out with some risk"
    if not at_limit(st, lim, "O"):
        return "Apply for a key project", "Output is still below this level's limit"
    if not at_limit(st, lim, "N"):
        return "Build a mentorship", "Network is still below this level's limit"
    if not at_limit(st, lim, "S") and L >= 3:
        return "Apply for rotation", "Output and Network at the limit; Skill decides the next promotion"
    if all(at_limit(st, lim, k) for k in PROMO):
        return "Lay low and reduce risk", "all promotion stats at this level's limit; lower risk instead"
    return "Apply for a key project", "default"


# ---------------------------------------------------------------- output

def state_line(st, lim, info):
    m, L = st.get("m", 0), st.get("L", 1)
    parts = []
    for k in PROMO:
        if k not in st:
            continue
        if k in lim:
            parts.append("%s %d/%d" % (NAMES[k], st[k], lim[k]))
        else:
            parts.append("%s %d" % (NAMES[k], st[k]))
    r, rmonth = risk_now(info)
    hr = "HR '%s'" % HR_TEXT[r] if info else "no log"
    return "m%d L%d | %s | Health %s Dignity %s | %s" % (m, L, ", ".join(parts), st.get("H", "?"), st.get("D", "?"), hr)


def mode_lines(st, lim, info):
    m, L, H = st.get("m", 0), st.get("L", 1), st.get("H", 10)
    r, _ = risk_now(info)
    nxt, check, pre = review_info(m, info)
    if r >= 2:
        return ["MODE D (DANGER): HR says '%s' and a second blow-up ends the career. Take the honest option "
                "that fixes the problem at its root, even if it costs Output." % HR_TEXT[r]]
    if pre and m < 48:
        short = [(k, lim[k] - st[k]) for k in ("O", "N", "S") if k in lim and k in st and st[k] < lim[k]]
        known = [k for k in ("O", "N") if k in lim]
        if short:
            need = ", ".join("%s %d/%d" % (NAMES[k], st[k], lim[k]) for k, _ in short)
            how = {"O": "delivers, finishes or makes your work visible", "N": "helps and works with people",
                   "S": "builds real skill (learn it, fix the root cause yourself)"}
            return ["MODE R (RECOVER): the m%d review reads your stats at the end of m%d and you are short: %s. "
                    "Among honest options take the one that %s." % (nxt, check, need,
                                                                     " or that ".join(how[k] for k, _ in short))]
        if known:
            return ["MODE G (GUARD): this pick decides the m%d review; %s at the limit with no buffer. Take the "
                    "honest option that keeps your work shipping and people with you; stopping or rolling back "
                    "work, a flat no, going over someone's head or time off costs them." % (
                        nxt, " and ".join(NAMES[k] for k in known) + (" are" if len(known) > 1 else " is"))]
        return ["MODE G (GUARD): this pick feeds the m%d review (stats at the end of m%d). Among honest options "
                "take the one that adds Output or Network, not one that costs them." % (nxt, check)]
    if m >= 43:
        return ["MODE N (NORMAL, close-out): keep what you built; prefer options that close problems and keep "
                "Health and Dignity. The last review still counts."]
    return ["MODE N (NORMAL): the next review reads the end of m%d. Small losses now are rebuilt at the "
            "quarter end; choose as Zeng would at your stage." % check]


def feedback_lines(st, lim, info, state):
    out = []
    if not info:
        return out
    m = st.get("m", 0)
    # Half-year review summary, once per review.
    if info["grades"]:
        gmonth, grade, gidx = info["grades"][-1]
        if state.get("reported_review") != gmonth:
            state["reported_review"] = gmonth
            promoted = any(abs(p - gmonth) <= 1 for p in info["promotions"])
            if promoted:
                new_level = info.get("promoted_to") or st.get("L", 0)
                msg = "REVIEW (m%d): grade %s, promoted to L%d. New level, new limits." % (gmonth + 1, grade, new_level)
                if new_level >= 4:
                    msg += " Skill has no limit from here and weighs on the next promotions: keep raising it."
                out.append(msg)
            else:
                msg = "REVIEW (m%d): grade %s, not promoted." % (gmonth + 1, grade)
                at_talk = stats_at_talk(state, info, lim, gidx)
                short = [k for k in PROMO if at_talk and k in lim and at_talk.get(k, 0) < lim[k]]
                if at_talk and short:
                    msg += " At the review: %s." % ", ".join("%s %d/%d" % (NAMES[k], at_talk[k], lim[k]) for k in short)
                    costly = [c for c in costly_since(info, gmonth - 1, short) if c["idx"] < gidx]
                    if costly:
                        msg += " It was lost by: %s." % "; ".join(
                            "'%s' (%s)" % (short_opt(c["opt"]), fmt_delta(c["d"])) for c in costly[-2:])
                elif at_talk and all(k in lim for k in ("O", "N")):
                    if st.get("L", 1) >= 4 and "S" not in lim:
                        msg += " Output and Network were at the limit; Skill has no limit here and decides it: raise Skill."
                    else:
                        msg += (" Output, Network and Skill were at the limit, so the limit is needed but not always "
                                "enough: keep them there and keep risk low.")
                msg += " Next window: the end of m%d." % min(gmonth + 6, 47)
                out.append(msg)
            if info.get("talk") and info["talk"][0] == gmonth:
                out.append("Manager said: " + info["talk"][1])
    # What the last story pick cost.
    c = last_pick(info)
    if c and state.get("reported_pick") != (c["month"], c["opt"]):
        state["reported_pick"] = (c["month"], c["opt"])
        loss = {k: v for k, v in c["d"].items() if k in ("O", "N") and v < 0}
        if loss:
            out.append("LAST PICK cost %s: '%s'." % (", ".join("%s %d" % (NAMES[k], -v) for k, v in loss.items()),
                                                   short_opt(c["opt"], 70)))
    if st.get("H", 10) <= 4:
        out.append("Health %d: an option that restores Health is fine now." % st["H"])
    return out


def quarter_lines(st, lim, info, state):
    m = st.get("m", 0)
    out = []
    E = st.get("E", 0)
    if E > 0:
        snap = state.get("q_snap")
        if not snap or snap.get("m") != m:
            if snap:
                state["growth"] = {k: st.get(k, 0) - snap.get(k, 0) for k in PROMO}
            state["q_snap"] = dict({k: st.get(k, 0) for k in PROMO}, m=m)
        done = [c["opt"] for c in (info["choices"] if info else [])
                if c["month"] == m and c["title"].lower() == "quarterly energy allocation"]
        if any(x.startswith("Defuse") for x in done):
            state["defused_q"] = m
        steps, why = plan_energy(st, info, lim, state)
        if steps:
            out.append("ENERGY (%d left): choose now '%s'%s" % (E, steps[0],
                       (" then " + ", ".join("'%s'" % x for x in steps[1:])) if steps[1:] else ""))
        if why:
            out.append("Why: " + "; ".join(why))
        ma, mwhy = plan_main(st, info, lim)
        out.append("MAIN ACTION after Energy: '%s' (%s)" % (ma, mwhy))
    else:
        ma, why = plan_main(st, info, lim)
        out.append("MAIN ACTION: '%s' (%s)" % (ma, why))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", default="brief")
    ap.add_argument("--stats", default="")
    ap.add_argument("--log", default="")
    ap.add_argument("--state-file", default="")
    ap.add_argument("--kind", default="")       # accepted for older call styles
    a = ap.parse_args()
    cmd = (a.kind or a.command).lower()
    sp = a.state_file or state_path()
    state = load_state(sp) if sp else {}
    st = parse_stats(a.stats)
    log = resolve_log(a.log, state, st)
    if log != state.get("log"):
        state = {"log": log}          # a new game: forget the old one
    info = parse_log(log)
    if not st.get("m") and info:
        st["m"] = info["last_month"]
    if not st.get("L") and info and info["level_by_month"]:
        st["L"] = info["level_by_month"][max(info["level_by_month"])]
    if str(state.get("level")) != str(st.get("L", 1)):
        state["level"] = st.get("L", 1)
        state["q_snap"] = None
    lim = update_limits(state, st, info)

    out = [state_line(st, lim, info)]
    if info is None:
        out.append("No log read: call check_latest_logs once and pass its log_file with --log.")
    if cmd.startswith(("quarter", "energy", "main")):
        out += quarter_lines(dict(st, E=0) if cmd.startswith("main") else st, lim, info, state)
        out += [x for x in feedback_lines(st, lim, info, state) if x.startswith(("REVIEW", "Manager"))]
    else:
        out += mode_lines(st, lim, info)
        out += feedback_lines(st, lim, info, state)
    if sp:
        save_state(sp, state)
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never break the game loop
        print("CAREER ERROR (%s): use the fallback rules in the zeng-guofan skill." % exc.__class__.__name__)
