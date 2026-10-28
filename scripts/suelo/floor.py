"""Suelo (floor) line: how often a v4-like player sinks a game in the replica, by cause, and what each
candidate rule does to that floor. Research only: nothing here is Skill text.

The player is the written-rule bot of scripts/deepseek/groupbot.py (LexBot, the replica twin of
t13-read-v4), with two readers:
  exact   sees the true sign of every stat change and of the hidden risk;
  noisy   a reader with DeepSeek's measured recall and false-alarm rates (lab/reports/deepseek/
          percepcion.md and categorizacion.md, reading v3), drawn again at every encounter.
The replica is patched with HALLAZGOS B30: at the third review in L1 (17 months in the level) the grade
is C, and the promotion goes through, only when the hidden risk is 0.

Arms are spec strings on top of the v4-like base (lex-strict + review-first-when-calm + L1 two-month
protection + repair + DeepSeek-like quarter + blind to ceilings):
  rescue   B30: after two reviews without promotion at the entry level, only risk-lowering options,
           Defuse + Lay low every quarter, and never lower a growth stat, until promoted
  pl1      at L1 never lower a growth stat in any month
  last     in the month before a review, the third story of the month (no later repair possible)
           puts the promotion before any risk; the first two keep the normal order
  blow     after a blow-up, only risk-lowering options when there are any (for the rest of the run)
  rvany    review first in the preparation month whatever the HR remark (v4 limits it to calm/quiet)
  sloss    forced growth loss near a review falls on Skill, not Network or Output

    python3 scripts/suelo/floor.py --games 2000 --arms base,base+rescue,base+rescue+pl1
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
sys.path.insert(0, str(REPO / "scripts" / "deepseek"))
import replica as R  # noqa: E402
import groupbot as G  # noqa: E402

CAT = G.CAT
K = G.K

# DeepSeek reading v3 (percepcion.md / categorizacion.md): recall of rises, recall of falls,
# false "+" on unchanged, false "-" on unchanged.
NOISE = {
    "health": (0.72, 0.51, 0.06, 0.10),
    "dignity": (0.79, 0.79, 0.22, 0.30),
    "skill": (0.78, 0.28, 0.01, 0.02),
    "network": (0.78, 0.79, 0.28, 0.15),
    "output": (0.47, 0.47, 0.07, 0.05),
    "wealth": (0.59, 0.45, 0.03, 0.02),
}
RISK_SEEN_1, RISK_SEEN_2, RISK_DOWN_SEEN, RISK_FALSE = 0.80, 0.92, 0.88, 0.10


class Exact:
    def see(self, node: str, k: int):
        r = CAT.answer_risk(node, k)
        return dict(CAT.nodes[node]["choices"][str(k)]["d"]), (r > 0) - (r < 0)

    def mag(self, node: str, k: int) -> int:
        """Perceived size of a risky option: 1 (mild) or 2 (serious)."""
        return 2 if CAT.answer_risk(node, k) >= 2 else 1


class Noisy:
    """DeepSeek-like reader: each encounter is a fresh reading with the measured error rates."""

    def __init__(self, seed: int = 0, scale: float = 1.0) -> None:
        self.rng = random.Random(seed)
        self.scale = scale  # 0 = exact, 1 = measured noise

    def see(self, node: str, k: int):
        d = CAT.nodes[node]["choices"][str(k)]["d"]
        fx = {}
        for s in K:
            x = d.get(s, 0)
            up, down, fp, fn = NOISE[s]
            if x > 0:
                fx[s] = 1.0 if self.rng.random() < 1 - self.scale * (1 - up) else 0.0
            elif x < 0:
                fx[s] = -1.0 if self.rng.random() < 1 - self.scale * (1 - down) else 0.0
            else:
                u = self.rng.random()
                fx[s] = 1.0 if u < self.scale * fp else (-1.0 if u < self.scale * (fp + fn) else 0.0)
        r = CAT.answer_risk(node, k)
        if r >= 2:
            sign = 1 if self.rng.random() < 1 - self.scale * (1 - RISK_SEEN_2) else 0
        elif r == 1:
            sign = 1 if self.rng.random() < 1 - self.scale * (1 - RISK_SEEN_1) else 0
        elif r < 0:
            sign = -1 if self.rng.random() < 1 - self.scale * (1 - RISK_DOWN_SEEN) else 0
        else:
            sign = 1 if self.rng.random() < self.scale * RISK_FALSE else 0
        return fx, sign

    def mag(self, node: str, k: int) -> int:
        r = CAT.answer_risk(node, k)
        if r >= 2:
            return 2 if self.rng.random() < 1 - self.scale * 0.1 else 1
        return 1 if self.rng.random() < 1 - self.scale * 0.1 else 2


class B30Grade:
    """Replica grade model + B30: third review in L1 is C only with hidden risk 0 (else D)."""

    def __init__(self, inner, on: bool = True) -> None:
        self.inner, self.on = inner, on

    def grade(self, st: R.State, blow_now: bool = False) -> str:
        if self.on and st.level == 1 and st.duration_in_level >= 17:
            return "C" if st.risk == 0 and not blow_now else "D"
        return self.inner.grade(st, blow_now)


class FloorBot(G.LexBot):
    def __init__(self, per, seed: int, spec: set[str]) -> None:
        dq = next((int(x[2:]) for x in spec if x.startswith("dq")), 1)
        ll = next((int(x[2:]) for x in spec if x.startswith("ll")), 2)
        super().__init__(per, seed=seed, risk_mode="survive" if "surv" in spec else "strict",
                         risk_first="alert" if ("blow" in spec or "rfalert" in spec) else "",
                         after_blowup="blow" in spec and "rfalert" not in spec, defuse_at=dq, laylow_at=ll,
                         review_first="" if "norvc" in spec else ("always" if "rvany" in spec else "calm"))
        self.hw = "hw" in spec
        self.rv_l1 = "rvl1" in spec
        self.mag = "mag" in spec
        self.window = 1
        self.protect_window = 1
        self.know_caps = False
        self.detect = False
        self.pw2_l1 = True
        self.repair = True
        self.quarter = "blind"
        self.protect_l1 = "pl1" in spec
        self.skill_first_loss = "sloss" in spec
        self.spec = spec
        self.slot_month, self.slot = None, 0
        self.stuck12 = False
        self.promo18 = False

    # ---- helpers
    def _rescue(self, st: R.State) -> bool:
        return "rescue" in self.spec and st.level == 1 and st.month >= 13

    def energy(self, rep, st):
        if self.hw and st.health <= 5 and st.energy >= 1 and st.month < 46:
            return "Health recovery"
        if self._rescue(st) and min(st.risk, 4) > 0 and st.energy >= 2 and not (st.health <= 4):
            return "Defuse legacy risk"
        if "blow" in self.spec and st.blowups > 0 and min(st.risk, 4) > 0 and st.energy >= 2 and st.health > 4:
            return "Defuse legacy risk"
        return super().energy(rep, st)

    def main(self, rep, st):
        if self._rescue(st) and min(st.risk, 4) > 0:
            return "Lay low and reduce risk"
        if "blow" in self.spec and st.blowups > 0 and min(st.risk, 4) > 0 and st.month < 46:
            return "Lay low and reduce risk"
        return super().main(rep, st)

    def story(self, rep, st, node):
        if self.slot_month != st.month:
            self.slot_month, self.slot = st.month, 0
        self.slot += 1
        if st.month == 13 and st.level == 1:
            self.stuck12 = True
        if st.month == 19 and st.level == 2 and self.stuck12:
            self.promo18 = True
        prep = st.month % 6 == 5
        if self._rescue(st):
            opts = []
            for kk in rep.cat.nodes[node]["choices"]:
                fx, sign = self.per.see(node, int(kk))
                opts.append((int(kk), {k: (v > 0) - (v < 0) for k, v in fx.items()}, sign))

            def keep(pool, bad):
                rest = [o for o in pool if not bad(o)]
                return rest or pool
            opts = keep(opts, lambda o: o[2] > 0)                       # never add risk
            if min(st.risk, 4) > 0:
                opts = keep(opts, lambda o: o[2] >= 0)                  # prefer lowering it
            opts = keep(opts, lambda o: any(o[1].get(k, 0) < 0 for k in R.GROWTH))
            opts = keep(opts, lambda o: (st.health <= 3 and o[1].get("health", 0) < 0) or (st.dignity <= 4 and o[1].get("dignity", 0) < 0))
            below = [k for k in R.GROWTH if getattr(st, k) < self.best.get(k, -99)]

            def score(o):
                sg = o[1]
                main = sum(2 if k in below else 1 for k in R.GROWTH if sg.get(k, 0) > 0)
                return (-o[2], main, sg.get("health", 0) + sg.get("dignity", 0), self.rng.random())
            for k in R.GROWTH:
                self.best[k] = max(self.best.get(k, -99), getattr(st, k))
            pick = max(opts, key=score)
            return pick[0]
        if self.mag and not self._rescue(st):
            node_opts = rep.cat.nodes[node]["choices"]
            seen = {int(kk): self.per.see(node, int(kk)) for kk in node_opts}
            if all(sg > 0 for _, sg in seen.values()) and len(seen) > 1:
                mags = {k: self.per.mag(node, k) for k in seen}
                lo = min(mags.values())
                safe = [k for k in seen if mags[k] == lo]
                if len(safe) < len(seen):
                    self._hw_seen, self._hw_safe = seen, set(safe)
                    try:
                        return self._story_restricted(rep, st, node)
                    finally:
                        self._hw_seen = None
        if self.hw:
            st_h = st.health
            if st_h <= 5:
                # drop options read as lowering Health unless every option does
                node_opts = rep.cat.nodes[node]["choices"]
                seen = {int(kk): self.per.see(node, int(kk)) for kk in node_opts}
                safe = [k for k, (fx, sg) in seen.items() if fx.get("health", 0) >= 0]
                if safe and len(safe) < len(seen):
                    self._hw_seen = seen
                    self._hw_safe = set(safe)
                    try:
                        return self._story_restricted(rep, st, node)
                    finally:
                        self._hw_seen = None
        if ("last" in self.spec or ("lastl1" in self.spec and st.level == 1)) and prep and self.slot >= 3:
            old = self.review_first
            self.review_first = "always"
            try:
                return super().story(rep, st, node)
            finally:
                self.review_first = old
        return super().story(rep, st, node)


    def _story_restricted(self, rep, st, node):
        """Run the normal story rule with the reader restricted to the Health-safe options."""
        per = self.per
        seen, safe = self._hw_seen, self._hw_safe

        class Sub:
            def see(self_, n, k):
                return seen[k]
        self.per = Sub()
        try:
            best, choices = None, rep.cat.nodes[node]["choices"]
            saved = dict(choices)
            for kk in list(choices):
                if int(kk) not in safe:
                    del choices[kk]
            try:
                best = super(FloorBot, self).story(rep, st, node) if not ("last" in self.spec and st.month % 6 == 5 and self.slot >= 3) else self._last(rep, st, node)
            finally:
                choices.clear(); choices.update(saved)
            return best
        finally:
            self.per = per

    def _last(self, rep, st, node):
        old = self.review_first
        self.review_first = "always"
        try:
            return super().story(rep, st, node)
        finally:
            self.review_first = old


DIAG = False
_ARMS: dict[str, dict] = {}


def _init(arms: dict[str, dict]) -> None:
    _ARMS.update(arms)
    CAT.grade = B30Grade(getattr(CAT.grade, "inner", CAT.grade), on=True)


REVIEWS: list = []
_orig_review = R.Replica.review


def _rec_review(self, st, explosion_now=False):
    t = R.THRESH.get(st.level)
    REVIEWS.append({"month": st.month, "level": st.level, "risk": st.risk, "dig": st.dignity,
                    "short": [k for k, v in zip(R.GROWTH, t) if getattr(st, k) < v] if t else [],
                    "blow": st.blowups})
    return _orig_review(self, st, explosion_now)


R.Replica.review = _rec_review


def _play(args):
    name, i, seed0 = args
    a = _ARMS[name]
    spec = set(a["spec"])
    per = Exact() if a["reader"] == "exact" else Noisy(seed=seed0 * 7 + i, scale=a.get("scale", 1.0))
    bot = FloorBot(per, i, spec)
    CAT.grade.on = "nob30" not in spec
    REVIEWS.clear()
    st, trace = R.play(CAT, bot, random.Random(seed0 + i))
    blow = st.blowups
    l1 = [r for r in REVIEWS if r["level"] == 1]
    return (R.Replica.score(st), st.level, st.failure or "completed", bot.stuck12, bot.promo18, blow, st.month, l1)


def run(arms: dict[str, dict], n: int, seed0: int, workers: int):
    out = {}
    with ProcessPoolExecutor(workers, initializer=_init, initargs=(arms,)) as ex:
        for name in arms:
            rows = list(ex.map(_play, [(name, i, seed0) for i in range(n)], chunksize=20))
            s = np.array([r[0] for r in rows])
            fails = collections.Counter(r[2] for r in rows)
            stuck = sum(r[3] for r in rows)
            resc = sum(r[4] for r in rows)
            low = float(np.mean(s < 40))
            l6 = np.mean([r[1] >= 6 for r in rows])
            lv = np.mean([r[1] for r in rows])
            print(f"{name:34s} {s.mean():5.2f} ±{s.std(ddof=1)/np.sqrt(n):.2f}  <40 {low:5.1%}  3-game sink {1-(1-low)**3:5.1%}"
                  f"  L1@13 {stuck/n:5.1%}  rescued@18 {resc}/{stuck}  Lmean {lv:.2f}  L6+ {l6:4.1%}"
                  f"  blowups/game {np.mean([r[5] for r in rows]):.2f}  {dict(fails)}", flush=True)
            out[name] = {"scores": s.tolist(), "fails": dict(fails), "stuck": stuck, "rescued": resc, "low": low}
            if DIAG:
                why = collections.Counter()
                for r in rows:
                    for rv in r[7]:
                        key = (rv["month"], "short:" + "+".join(rv["short"]) if rv["short"] else "at bar",
                               "risk0" if rv["risk"] == 0 else f"risk{min(rv['risk'],4)}", "dig<4" if rv["dig"] < 4 else "")
                        why[key] += 1
                for k, v in sorted(why.items()):
                    print("     ", k, v)
    return out


def parse(spec: str) -> dict:
    parts = spec.split("+")
    reader = "noisy"
    scale = 1.0
    rest = []
    for p in parts:
        if p in ("exact", "noisy"):
            reader = p
        elif p.startswith("scale"):
            scale = float(p[5:])
        elif p != "base":
            rest.append(p)
    return {"reader": reader, "scale": scale, "spec": rest}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="base,base+rescue")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="")
    ap.add_argument("--diag", action="store_true", help="why L1 reviews fail (stat short, risk, dignity)")
    a = ap.parse_args()
    global DIAG
    DIAG = a.diag
    arms = {s: parse(s) for s in a.arms.split(",")}
    print(f"{a.games} games per arm, seeds {a.seed}+i (paired across arms); B30 patch on unless 'nob30'")
    res = run(arms, a.games, a.seed, a.workers)
    if a.out:
        Path(a.out).write_text(json.dumps(res))


if __name__ == "__main__":
    main()
