"""Why the written-rule bot misses promotions: for each review it does not pass, which of Skill, Network,
Output or Dignity was short at the review, and whether it was already short at the start of the
preparation month or was lost during it.

    uv run python scripts/deepseek/promo.py --labels A.json+B.json --arm signs:flag:strict --games 2000
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import groupbot as G  # noqa: E402

R = G.R


class Probe:
    def __init__(self, bot):
        self.bot, self.snap, self.rows = bot, {}, []

    def __getattr__(self, k):
        return getattr(self.bot, k)

    def story(self, rep, st, node):
        m = st.month
        if m not in self.snap:
            self.snap[m] = (st.level, st.skill, st.network, st.output, st.dignity, st.blowups)
            if m % 6 == 0 and (m - 1) in self.snap and (m - 1) % 6 == 5:
                lv0, s0, n0, o0, d0, b0 = self.snap[m - 1]
                lv1 = st.level
                if lv1 == lv0:
                    thr = R.THRESH[lv0]
                    short_now = [k for k, v, t in (("S", st.skill, thr[0]), ("N", st.network, thr[1]), ("O", st.output, thr[2])) if v < t]
                    short_before = [k for k, v, t in (("S", s0, thr[0]), ("N", n0, thr[1]), ("O", o0, thr[2])) if v < t]
                    self.rows.append({"month": m, "level": lv0, "short_at_review": short_now,
                                      "short_at_prep_start": short_before, "dignity_low": st.dignity < 4,
                                      "blew": st.blowups > b0})
                else:
                    self.rows.append({"month": m, "level": lv0, "promoted": True})
        return self.bot.story(rep, st, node)

    def energy(self, rep, st):
        return self.bot.energy(rep, st)

    def main(self, rep, st):
        return self.bot.main(rep, st)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--arm", default="signs:flag:strict")
    ap.add_argument("--games", type=int, default=1000)
    a = ap.parse_args()
    sets = [json.load(open(p)) for p in a.labels.split("+")]
    fx, risk, *lex = a.arm.split(":")
    pers = [G.Perception(lab, fx, risk) for lab in sets]
    per = pers[0] if len(pers) == 1 else G.Mixed(pers)
    name = f"x {fx}/{risk}" + (f"/lex-{lex[0]}" if lex else "")
    G._PER[name] = per
    rows, outcomes = [], collections.Counter()
    for i in range(a.games):
        probe = Probe(G._bot(name, i))
        st, _ = R.play(G.CAT, probe, random.Random(4242 + i))
        rows += [dict(r, game=i) for r in probe.rows]
        outcomes[(st.failure or "completed", st.level if st.failure == "dismissed" else None)] += 1
    print("outcomes (failure, level if dismissed):", dict(outcomes.most_common(10)))
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        key = (r["level"], r["month"])
        if r.get("promoted"):
            by[key]["promoted"] += 1
        else:
            why = "blew up" if r["blew"] else ("dignity" if r["dignity_low"] and not r["short_at_review"] else
                  "lost in prep month: " + "".join(sorted(set(r["short_at_review"]) - set(r["short_at_prep_start"])))
                  if set(r["short_at_review"]) - set(r["short_at_prep_start"]) else
                  "short before prep: " + "".join(r["short_at_prep_start"]) if r["short_at_prep_start"] else "other")
            by[key][why] += 1
    for key in sorted(by):
        if key[0] <= 2 and key[1] <= 24:
            print(f"L{key[0]} review m{key[1]}:", dict(by[key].most_common(8)))


if __name__ == "__main__":
    main()
