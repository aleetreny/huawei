"""The first-promotion trap (L1) in the replica: why L1 reviews fail, and what reduces it.

Uses Alejandro's written-rule bot (scripts/deepseek/groupbot.py, LexBot) with a reading built from Leah's
Haiku stat labels (lab/reports/stat-perception/) and the blind categories of the question bank
(lab/reports/question-bank/labels.json); risk is judged by the category, as in catbot.py. DeepSeek's own
labels are not in the repo, so absolute scores differ from lab/reports/deepseek/; arms are compared on the
same seeds.

For every review taken at L1 it records which promotion condition failed (Skill, Network, Output below the
threshold, Dignity under 4, grade D) and, for every story in the two months before a review at L1 that cost
Network or Output, whether a safe alternative existed (no Network/Output loss and not risky by the exact
step): "avoidable" losses are perception, the rest are forced.

    .venv/bin/python scripts/stat-perception/l1_trap.py --games 2000 --arms base,cat2,...
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "deepseek"))
import groupbot as G  # noqa: E402

R = G.R
SP = REPO / "lab" / "reports" / "stat-perception"
CATS = json.load(open(REPO / "lab" / "reports" / "question-bank" / "labels.json"))
SIGN = {1: "+", -1: "-", 0: "0"}
# categories that, in the design half of the question bank, lower Network in about half their answers or more
NO_RISKY = {"ATTACK", "PERSIST", "SELL", "GUARD", "ESCALATE", "AVOID"}


def labels_from(tags_file: str) -> dict:
    tags = json.load(open(SP / tags_file))
    out = {}
    for k, cat in CATS.items():
        t = tags.get(k, {})
        out[k] = {"group": cat, **{s: SIGN[int(t.get(s, 0))] for s in ("health", "dignity", "skill", "network", "output")},
                  "wealth": "0"}
    return out


def perfect() -> dict:
    out = {}
    for a in G.A:
        k = f"{a['node']}:{a['choice']}"
        out[k] = {"group": CATS.get(k, "FIX"), **{s: SIGN[(a["d"].get(s, 0) > 0) - (a["d"].get(s, 0) < 0)] for s in G.K}}
    return out


class TrapBot(G.LexBot):
    """LexBot plus the trap experiments; records avoidable/forced Network-Output losses before L1 reviews."""

    def __init__(self, per, seed, cat_veto=0, no_first=False, two_reads=None, fill=False):
        super().__init__(per, seed=seed, risk_mode="strict", review_first="calm")
        self.fill = fill                 # quarter before an L1 review: Energy first to what Network/Output still lack
        self.quarter = "blind"           # DeepSeek-like quarter: report, network, key project
        self.pw2_l1 = True               # v4: protect Network and Output two months before the review at L1
        self.repair = True               # v4: raise back a stat under its best with the review close
        self.window = 1
        self.cat_veto = cat_veto         # >0: at L1, months before a review within this window, drop NO_RISKY categories
        self.no_first = no_first         # at L1 before a review: prefer options that raise Network or Output
        self.two_reads = two_reads       # a second Perception: an option counts as costly if either reading says so
        self.losses = collections.Counter()
        self.at_prep = {}                # Skill/Network/Output at the first story after each L1 quarter before a review

    def energy(self, rep, st):
        if self.fill and st.level == 1 and st.month % 6 == 3 and st.health > 3:
            # counting what the key project will add (Output +2, Network +1), fill what is still missing
            if st.network + 1 < R.cap(1, "network") and st.energy >= 1:
                return "Network maintenance"
            if st.output + 2 < R.cap(1, "output") and st.energy >= 1:
                return "Prepare report materials"
        return super().energy(rep, st)

    def story(self, rep, st, node):
        ks = [int(k) for k in rep.cat.nodes[node]["choices"]]
        months_to = 6 - st.month % 6 if st.month % 6 else 0
        near = st.level == 1 and 0 < months_to <= 2
        if near and months_to == 2 and st.month + 2 not in self.at_prep:
            self.at_prep[st.month + 2] = (st.skill, st.network, st.output)
        pool = ks
        if near and self.cat_veto and months_to <= self.cat_veto:
            rest = [k for k in ks if CATS.get(f"{node}:{k}", "FIX") not in NO_RISKY]
            pool = rest or ks
        if self.two_reads is not None and near:
            per1, per2 = self.per, self.two_reads

            class Both:
                def see(_, n, k):
                    fx, r = per1.see(n, k)
                    fx2, r2 = per2.see(n, k)
                    fx = dict(fx)
                    for s in ("network", "output", "skill"):
                        fx[s] = min(fx.get(s, 0), fx2.get(s, 0)) if min(fx.get(s, 0), fx2.get(s, 0)) < 0 else fx.get(s, 0)
                    return fx, max(r, r2)
            self.per = Both()
        if pool != ks:
            sub = dict(rep.cat.nodes[node])
            sub["choices"] = {str(k): rep.cat.nodes[node]["choices"][str(k)] for k in pool}
            orig, rep.cat.nodes[node] = rep.cat.nodes[node], sub
            try:
                pick = self._pick(rep, st, node)
            finally:
                rep.cat.nodes[node] = orig
        else:
            pick = self._pick(rep, st, node)
        if self.two_reads is not None and near:
            self.per = per1
        if near:
            d = rep.cat.nodes[node]["choices"][str(pick)]["d"]
            if d.get("network", 0) < 0 or d.get("output", 0) < 0:
                safe = [k for k in ks if rep.cat.nodes[node]["choices"][str(k)]["d"].get("network", 0) >= 0
                        and rep.cat.nodes[node]["choices"][str(k)]["d"].get("output", 0) >= 0
                        and rep.cat.answer_risk(node, k) <= 0]
                self.losses["avoidable" if safe else "forced"] += 1
        return pick

    def _pick(self, rep, st, node):
        if self.no_first and st.level == 1 and st.month % 6 and 6 - st.month % 6 <= 2:
            below = [k for k in ("network", "output") if getattr(st, k) < R.cap(1, k)]
            if below:
                opts = []
                for kk in rep.cat.nodes[node]["choices"]:
                    fx, sign = self.per.see(node, int(kk))
                    if sign <= 0 and any(fx.get(k, 0) > 0 for k in below) and not any(fx.get(k, 0) < 0 for k in ("network", "output")):
                        opts.append(int(kk))
                if opts:
                    return self.rng.choice(opts)
        return G.LexBot.story(self, rep, st, node)


_ARMS: dict = {}
REVIEWS: list = []


def _init(arms):
    _ARMS.update(arms)


def _play(args):
    name, i, seed0 = args
    per, kw = _ARMS[name]
    bot = TrapBot(per, seed=i, **kw)
    fails = []
    orig = R.Replica.review

    def review(self, st, explosion_now=False):
        lvl, s, n, o, dg = st.level, st.skill, st.network, st.output, st.dignity
        out = orig(self, st, explosion_now)
        if lvl == 1:
            t = R.THRESH[1]
            why = [x for x, bad in (("skill", s < t[0]), ("network", n < t[1]), ("output", o < t[2]),
                                    ("dignity", dg < 4), ("grade D", out["grade"] == "D")) if bad]
            fails.append((st.month, out["promoted"], why))
        return out
    R.Replica.review = review
    try:
        st, _ = R.play(G.CAT, bot, random.Random(seed0 + i))
    finally:
        R.Replica.review = orig
    return R.Replica.score(st), st.level, st.failure or "completed", fails, dict(bot.losses), bot.at_prep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--reading", default="tags-plain.json+tags-plain-rerun.json", help="tag files, + for repeated readings")
    ap.add_argument("--arms", default="base")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    reads = [G.Perception(labels_from(f), "signs", "group") for f in a.reading.split("+")]
    haiku = reads[0] if len(reads) == 1 else G.Mixed(reads)
    exact = G.Perception(perfect(), "signs", "group")
    second = G.Perception(labels_from("tags-defs3.json"), "signs", "group")
    vote = G.Perception(labels_from("tags-vote5c.json"), "signs", "group")
    menu = {
        "base": (haiku, {}),                                   # v4-like rules, Haiku reading
        "perfect": (exact, {}),                                # same rules, exact signs
        "cat1": (haiku, {"cat_veto": 1}),                       # + category veto in the month before the review
        "cat2": (haiku, {"cat_veto": 2}),                       # + category veto in the two months before
        "nofirst": (haiku, {"no_first": True}),                 # + prefer a safe Network/Output raise when below the bar
        "tworeads": (haiku, {"two_reads": second}),             # + an option is costly if either of two readings says so
        "vote": (vote, {}),                                     # reading = vote of five Haiku readings
        "cat2+tworeads": (haiku, {"cat_veto": 2, "two_reads": second}),
        "cat2+nofirst": (haiku, {"cat_veto": 2, "no_first": True}),
        "perfect+cat2": (exact, {"cat_veto": 2}),
        "fill": (haiku, {"fill": True}),                        # + quarter before an L1 review fills Network/Output first
        "fill+cat1": (haiku, {"fill": True, "cat_veto": 1}),
        "fill+vote": (vote, {"fill": True}),
        "perfect+fill": (exact, {"fill": True}),
    }
    arms = {n: menu[n] for n in a.arms.split(",")}
    rows = {}
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(arms,)) as ex:
        for name in arms:
            out = list(ex.map(_play, [(name, i, a.seed) for i in range(a.games)], chunksize=25))
            sc = np.array([o[0] for o in out])
            fails = collections.Counter(o[2] for o in out)
            stuck = sum(1 for o in out if o[1] == 1)
            why = collections.Counter()
            first = collections.Counter()
            for o in out:
                for m, promoted, w in o[3]:
                    if not promoted:
                        for x in w or ["(none)"]:
                            why[f"m{m}:{x}"] += 1
                        if m == 6:
                            first["missed m6"] += 1
            loss = collections.Counter()
            for o in out:
                loss.update(o[4])
            entry = collections.Counter()   # failed L1 reviews: were Network and Output at the bar when the window opened?
            for o in out:
                for m, promoted, w in o[3]:
                    if not promoted and m in (6, 12) and m in o[5]:
                        s0, n0, x0 = o[5][m]
                        t = R.THRESH[1]
                        entry["entered short" if (n0 < t[1] or x0 < t[2] or s0 < t[0]) else "entered at the bar"] += 1
            rows[name] = {"score": sc.mean(), "se": sc.std(ddof=1) / np.sqrt(len(sc)), "stuck_l1": stuck / len(sc),
                          "dismissed": fails["dismissed"], "trust": fails["trust"], "missed_m6": first["missed m6"] / len(sc),
                          "why_failed": dict(why), "no_losses": dict(loss), "entry": dict(entry)}
            r = rows[name]
            print(f"{name:15s} {r['score']:5.1f} ± {r['se']:.2f}  ends in L1 {r['stuck_l1']:5.1%}  dismissed {r['dismissed']:4d}  "
                  f"trust {r['trust']:4d}  missed m6 {r['missed_m6']:5.1%}  why {dict(why.most_common())}  N/O losses {dict(loss)}  failed m6/m12 reviews: {dict(entry)}", flush=True)
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=1, default=float))


if __name__ == "__main__":
    main()
