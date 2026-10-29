"""Réplica calibrada: DeepSeek simulado con el modelo de elección ajustado a las partidas reales.

Historias: logit condicional (choice_model.py) sobre efectos verdaderos + lecturas de DeepSeek de cada
opción (una pasada de etiquetas al azar por encuentro, o la media). Trimestres: reglas de la familia v4/cp
(bot de techobot/cpbot), que DeepSeek obedece (B20).

    uv run python scripts/exploracion/dssim.py --arms base,qskill=4 --games 2000
Investigación: nada de esto va a un Skill.
"""
from __future__ import annotations
import argparse, json, random, sys, collections, math
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingenieria-inversa"))
sys.path.insert(0, str(ROOT / "scripts/techo"))
sys.path.insert(0, str(ROOT / "scripts/comprobante"))
sys.path.insert(0, str(ROOT / "scripts/exploracion"))
import replica as R  # noqa: E402
import techobot as T  # noqa: E402
import cpbot as C  # noqa: E402
import choice_model as CM  # noqa: E402

class B30Grade:
    """HALLAZGOS B30 (huevos-pascua): the third review in L1 is C only with hidden risk 0, else D."""

    def __init__(self, inner):
        self.inner = inner

    def grade(self, st, blow_now=False):
        if st.level == 1 and st.duration_in_level >= 17:
            return "C" if st.risk == 0 and not blow_now else "D"
        return self.inner.grade(st, blow_now)


if not isinstance(T.CAT.grade, B30Grade):
    T.CAT.grade = B30Grade(T.CAT.grade)

import gzip as _gz, re as _re
_ANS = {(a["node"], a["choice"]): a["text"] for a in json.load(_gz.open(ROOT / "lab/data/deepseek/otros/answers.json.gz", "rt"))}
_PRIV = _re.compile(r"\bprivate(ly)?\b|in private|aside|1:1|one-to-one|\bquiet(ly)?\b|\blater\b|after the meeting|afterwards|in writing", _re.I)
_HIDE = _re.compile(r"\bhide|\bdeny|cover up|conceal|anonym", _re.I)
_CONF = _re.compile(r"in the room|in public|publicly|openly|in the meeting|in front of|\brefuse|\bdecline|say no|firm|insist|push back", _re.I)


def text_kind(node, k):
    t = _ANS.get((node, k), "")
    if _HIDE.search(t):
        return "hide"
    if _PRIV.search(t):
        return "priv"
    if _CONF.search(t):
        return "conf"
    return ""


LABELS = {f: json.load(open(ROOT / "lab/data/deepseek/etiquetas" / f"{f}.json"))
          for f in ("ds-v1-r1-full", "ds-v1-r2-full", "ds-v3-r1-full", "ds-v3-r2-full")}
BETA = json.load(open(ROOT / "lab/data/exploracion/choice_beta.json"))


def option_labels(node: str, k: int) -> dict:
    return {f: L.get(f"{node}:{k}") for f, L in LABELS.items()}


class DSBot(C.CPBot):
    """Quarter rules of the cp/v4 family (flags as in cpbot); stories by the fitted choice model."""

    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags)
        f = flags or {}
        b = beta or (json.load(open(ROOT / f"lab/data/exploracion/choice_beta_{f['beta']}.json")) if f.get("beta") else BETA)
        self.names = b["names"]
        self.beta = np.array(b["beta"])
        self.cols = [CM.FEATS.index(n) for n in self.names]
        self.temp = float(f.get("temp", 1.0))
        self.labmode = f.get("lab", "mean")
        self.trace_dec = []

    def story_probs(self, rep, st, node):
        self._tick(st)
        n = self.n_to_review(st)
        stt = {k: getattr(st, k) for k in ("health", "dignity", "skill", "network", "output", "wealth")}
        ks, X = [], []
        for kk, ch in rep.cat.nodes[node]["choices"].items():
            k = int(kk)
            labs = option_labels(node, k)
            if self.labmode == "one":
                f = self.rng.choice(list(labs))
                lab = CM.mean_lab({f: labs[f]})
            else:
                lab = CM.mean_lab(labs)
            X.append(CM.features(stt, st.level, n, self.hr, ch["d"], rep.cat.answer_risk(node, k), lab))
            ks.append(k)
        X = np.array(X)
        z = (X[:, self.cols] @ self.beta) / self.temp
        z -= z.max()
        p = np.exp(z)
        p /= p.sum()
        return ks, p, X

    def story(self, rep, st, node):
        ks, p, X = self.story_probs(rep, st, node)
        i = int(self.rng.choices(range(len(ks)), weights=p)[0])
        if rep.cat.answer_risk(node, ks[i]) > 0:
            self.concerns += 1
        return ks[i]


_ARGS: dict = {}


def _init(a):
    _ARGS.update(a)


def _play(job):
    spec, i = job
    per = T.Perception("exact", seed=50_000 + i)
    flags = T.parse_arm(spec)
    bot = _ARGS.get("botcls", DSBot)(per, seed=i, flags=flags)
    st, trace = R.play(T.CAT, bot, random.Random(_ARGS["seed"] + i))
    promos = [m for m, kind, *rest in trace if kind == "r" and rest[0].get("promoted")]
    return {"q": R.Replica.score(st), "level": st.level, "fail": st.failure or "ok", "promos": promos,
            "skill": st.skill, "network": st.network, "output": st.output, "wealth": st.wealth,
            "blow": st.blowups, "month": st.month}


def summarize(name, rows):
    q = np.array([r["q"] for r in rows])
    ok = [r for r in rows if r["fail"] == "ok"]
    fails = collections.Counter(r["fail"] for r in rows)
    first = collections.Counter((r["promos"][0] if r["promos"] else 0) for r in rows)
    l5 = [next((m for j, m in enumerate(r["promos"]) if j == 3), None) for r in ok]
    l5m = np.mean([x for x in l5 if x]) if any(l5) else float("nan")
    lv = collections.Counter(r["level"] for r in ok)
    s = (f"{name:28s} Q {q.mean():5.2f}±{q.std(ddof=1)/math.sqrt(len(q)):.2f} | completas {len(ok)/len(rows):4.0%} Q {np.mean([r['q'] for r in ok]):5.2f}"
         f" | {dict(fails)} | 1er ascenso m6 {first[6]/len(rows):.0%} m12 {first[12]/len(rows):.0%} m18 {first[18]/len(rows):.0%} nunca {first[0]/len(rows):.0%}"
         f" | niveles completas {dict(sorted(lv.items()))} | L5 en mes {l5m:.1f} | explos/partida {np.mean([r['blow'] for r in rows]):.2f}")
    return s


def run(arms, games, seed=4242, workers=4, botcls=None, quiet=False):
    out = {}
    with ProcessPoolExecutor(workers, initializer=_init, initargs=({"seed": seed, "botcls": botcls or DSBot},)) as ex:
        for spec in arms:
            rows = list(ex.map(_play, [(spec, i) for i in range(games)], chunksize=25))
            out[spec] = rows
            if not quiet:
                print(summarize(spec, rows), flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="base")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    out = run(a.arms.split(","), a.games, a.seed)
    if a.json:
        json.dump(out, open(a.json, "w"))


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------------- intervenciones (cotas)
TRUTH_LAB = {}


def truth_lab(node, k):
    d = T.CAT.nodes[node]["choices"][str(k)]["d"]
    r = T.CAT.answer_risk(node, k)
    sg = lambda x: (x > 0) - (x < 0)
    return {**{s: sg(d.get(s, 0)) for s in ("health", "dignity", "skill", "network", "output", "wealth")}, "risk": sg(r)}


class XBot(DSBot):
    """DSBot + interventions (flags): perc=truth, capinfo, l1veto, nveto, hveto, rveto. Upper bounds unless noted."""

    def story(self, rep, st, node):
        self._tick(st)
        f = self.flags_x
        n = self.n_to_review(st)
        stt = {k: getattr(st, k) for k in ("health", "dignity", "skill", "network", "output", "wealth")}
        ks, X = [], []
        for kk, ch in rep.cat.nodes[node]["choices"].items():
            k = int(kk)
            if f.get("perc") == "truth":
                lab = {kx: float(v) for kx, v in truth_lab(node, k).items()}
            else:
                lab = CM.mean_lab(option_labels(node, k))
            if f.get("capinfo"):
                for s in R.GROWTH:
                    if getattr(st, s) >= R.cap(st.level, s) and lab.get(s, 0) > 0:
                        lab = dict(lab); lab[s] = 0.0
            d = dict(ch["d"])
            x = CM.features(stt, st.level, n, self.hr, d, rep.cat.answer_risk(node, k), lab)
            if f.get("capinfo"):
                for s in "SNO":
                    x[CM.FEATS.index("w" + s)] = 0.0
            X.append(x); ks.append(k)
        X = np.array(X)
        extra = np.zeros(len(ks))
        if f.get("donly") is not None and n <= int(f.get("donlyn", 1)) and st.level <= int(f.get("donlylv", 1)):
            pen = float(f["donly"]); bonus = float(f.get("nplus", 0))
            for j, k in enumerate(ks):
                lab = CM.mean_lab(option_labels(node, k))
                growth = max(lab.get("skill", 0), lab.get("network", 0), lab.get("output", 0))
                if lab.get("dignity", 0) > 0.5 and growth <= 0:
                    extra[j] -= pen
                if lab.get("network", 0) > 0.5 and lab.get("output", 0) >= 0:
                    extra[j] += bonus
        if f.get("privb") is not None and st.level == 1 and n == 1 and self.hr <= int(f.get("privhr", 1)) and self.concerns == 0:
            for j, k in enumerate(ks):
                kd = text_kind(node, k)
                if kd == "priv":
                    extra[j] += float(f["privb"])
                elif kd == "conf":
                    extra[j] -= float(f.get("confp", f["privb"]))
        beta = self.beta.copy()
        def mult(names, m):
            for nm in names:
                if nm in self.names:
                    beta[self.names.index(nm)] *= m
        if f.get("l1risk") is not None and st.level == 1 and n == 1 and self.hr <= 1:
            mult(["risk", "risky", "risk2", "LR+", "hr_risk", "hr_LR"], float(f["l1risk"]))
        if f.get("l1loss") is not None and st.level == 1 and n in (1, 2):
            mult(["lN", "lO", "LN-", "LO-", "N1_lossL", "N12_lossNO"], float(f["l1loss"]))
        if f.get("sk4") is not None and st.level >= 4:
            mult(["gS", "wS", "LS+"], float(f["sk4"]))
        if f.get("hcare") is not None and st.health <= int(f.get("hlow", 4)):
            mult(["dH", "LH", "lowH_dH"], float(f["hcare"]))
        if f.get("dcap") is not None and st.dignity >= int(f["dcap"]) and (f.get("dn") is None or n <= int(f["dn"])) \
                and (not f.get("dl1") or st.level == 1) and (not f.get("dhr") or self.hr <= 0):
            mult(["LD", "dD", "lowD_dD"], float(f.get("dmul", 0)))
        if f.get("hcapx") is not None and st.health >= int(f["hcapx"]):
            mult(["LH", "dH"], float(f.get("hmul", 0)))
        if f.get("allrisk") is not None:
            mult(["risk", "risky", "risk2", "LR+", "hr_risk", "hr_LR"], float(f["allrisk"]))
        z = (X[:, self.cols] @ beta + extra) / self.temp
        z -= z.max(); p = np.exp(z); p /= p.sum()
        allowed = np.ones(len(ks), bool)

        def veto(mask):
            nonlocal allowed
            m2 = allowed & ~mask
            if m2.any():
                allowed = m2
        effs = [rep.cat.nodes[node]["choices"][str(k)]["d"] for k in ks]
        risks = np.array([rep.cat.answer_risk(node, k) for k in ks])
        if f.get("hveto"):
            veto(np.array([st.health + e.get("health", 0) <= int(f["hveto"]) and e.get("health", 0) < 0 for e in effs]))
        if f.get("rveto"):
            veto(risks >= int(f["rveto"]))
        if f.get("l1veto") and st.level == 1 and n in ((1,) if f["l1veto"] == "1" or f["l1veto"] is True else (1, 2)):
            veto(np.array([e.get("network", 0) < 0 or e.get("output", 0) < 0 or (e.get("skill", 0) < 0 and st.skill + e.get("skill", 0) < R.THRESH[1][0]) for e in effs]))
        if f.get("l1lab") and st.level == 1 and n == 1 and (f.get("l1hr") is None or self.hr <= int(f["l1hr"])):
            # realistic: veto by one DeepSeek reading (random pass) of each option, keep risk <= l1r (by reading: any)
            labs1 = []
            for k in ks:
                L = option_labels(node, k); fsel = self.rng.choice([x for x in L if L[x]] or list(L))
                labs1.append(CM.lab_signs(L.get(fsel)))
            mask = np.array([lb.get("network", 0) < 0 or lb.get("output", 0) < 0 or lb.get("skill", 0) < 0 for lb in labs1])
            if f.get("l1r") is not None:
                lim = int(f["l1r"])
                mask = mask | np.array([risks[j] > lim for j in range(len(ks))])
            veto(mask)
        if f.get("l1veto2") and st.level == 1 and n == 1:
            lim = int(f["l1veto2"])
            m = np.array([e.get("network", 0) < 0 or e.get("output", 0) < 0 or (e.get("skill", 0) < 0 and st.skill + e.get("skill", 0) < R.THRESH[1][0]) for e in effs])
            ok = ~m & (risks <= lim)
            if ok.any():
                allowed = allowed & ok if (allowed & ok).any() else allowed
        if f.get("nveto") and n == 1 and st.level >= 2:
            veto(np.array([any(e.get(s, 0) < 0 for s in R.GROWTH) for e in effs]))
        p = np.where(allowed, p, 0); p /= p.sum()
        i = int(self.rng.choices(range(len(ks)), weights=p)[0])
        # re-check of the chosen option before sending it (detection q, false alarm fa), in review months
        rq = f.get("rq")
        if rq is not None and n in ((1,) if f.get("rqn", "1") == "1" else (1, 2)) and st.level <= int(f.get("rqlv", 1)):
            q, fa = float(rq), float(f.get("rfa", 0.0))
            tried = set()
            for _ in range(3):
                e = effs[i]
                loses = e.get("network", 0) < 0 or e.get("output", 0) < 0 or e.get("skill", 0) < 0
                if f.get("rqrisk") and risks[i] >= int(f["rqrisk"]):
                    loses = True
                flag = (self.rng.random() < q) if loses else (self.rng.random() < fa)
                if not flag:
                    break
                tried.add(i)
                rest = np.array([j not in tried for j in range(len(ks))]) & allowed
                if not rest.any():
                    break
                p2 = np.where(rest, p, 0)
                if p2.sum() <= 0:
                    p2 = rest.astype(float)
                p2 = p2 / p2.sum()
                i = int(self.rng.choices(range(len(ks)), weights=p2)[0])
        if risks[i] > 0:
            self.concerns += 1
        return ks[i]

    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        self.flags_x = dict(flags or {})


class QXBot(XBot):
    """XBot + quarter variants: qh=H (Health recovery first while Health <= H), defat=r (Defuse only from HR level r),
    layat=r (Lay low only from HR level r), q1txt (text version of q1out, without ceiling knowledge: at the starting
    level every Energy point left by the health and HR lines goes to Prepare report materials)."""

    def energy(self, rep, st):
        f = self.flags_x
        self._tick(st)
        if f.get("q1txt") and st.level == 1 and st.month < 46 and st.health > int(f.get("qh", 4)) and st.dignity > 4 \
                and not (self.hr != C.FRIENDLY and st.energy == 3):
            return "Prepare report materials" if st.energy >= 1 else None
        if f.get("qh") and st.month < 46 and st.health <= int(f["qh"]) and st.energy >= 1 and st.health < 10:
            return "Health recovery"
        if f.get("defat") is not None and st.month < 46:
            saved = self.hr
            if self.hr < int(f["defat"]):
                self.hr = 0
            try:
                return super().energy(rep, st)
            finally:
                self.hr = saved
        return super().energy(rep, st)

    def main(self, rep, st):
        f = self.flags_x
        self._tick(st)
        if f.get("layat") is not None and st.month < 46:
            saved = self.hr
            if self.hr < int(f["layat"]):
                self.hr = min(self.hr, 1)
            try:
                return super().main(rep, st)
            finally:
                self.hr = saved
        return super().main(rep, st)


class CapBot(QXBot):
    """QXBot + what a stateful in-run script can add to the quarter (C60): it records the state before and after each
    quarter (exact, from the observes) and the published effect of the actions taken; a stat that rose less than the
    published total is marked full at its current value for the rest of the level (anchored, B38). Flags:
    capdet (detect; 'truth' = know the ceilings, as an upper bound), and the planned Energy action on a full stat is
    redirected (Output -> Network -> Skill learning -> Health recovery)."""

    STAT = {"Prepare report materials": "output", "Network maintenance": "network", "Skill learning": "skill"}

    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        self.cap_mode = self.flags_x.get("capdet")
        self.full, self.full_lv = {}, None
        self.q_before, self.q_gain = None, {}

    def _resolve(self, st):
        if self.full_lv != st.level:
            self.full, self.full_lv = {}, st.level
            self.q_before = None
        if self.q_before is not None:
            for s, g in self.q_gain.items():
                if g > 0 and getattr(st, s) < self.q_before[s] + g:
                    self.full[s] = getattr(st, s)
            self.q_before, self.q_gain = None, {}
        for s in list(self.full):
            if getattr(st, s) < self.full[s]:
                del self.full[s]

    def is_full(self, st, s):
        if self.cap_mode == "truth":
            return getattr(st, s) >= R.cap(st.level, s)
        return s in self.full and getattr(st, s) >= self.full[s]

    def story(self, rep, st, node):
        if self.cap_mode:
            self._resolve(st)
        return super().story(rep, st, node)

    def energy(self, rep, st):
        if not self.cap_mode:
            return super().energy(rep, st)
        if st.energy == 3:
            self._resolve(st)
            self.q_before = {s: getattr(st, s) for s in R.GROWTH}
            self.q_gain = {}
        a = super().energy(rep, st)
        if a in self.STAT and st.month < 46 and self.is_full(st, self.STAT[a]):
            for alt in ("Prepare report materials", "Network maintenance", "Skill learning"):
                s = self.STAT[alt]
                cost = R.ENERGY_FX[alt][1]
                if cost <= st.energy and not self.is_full(st, s) and not (alt == "Skill learning" and st.health <= 6):
                    a = alt
                    break
            else:
                a = "Health recovery" if st.health < 10 else ("Mental recovery" if st.dignity < 10 else a)
        if a:
            for s, v in R.ENERGY_FX.get(a, ({}, 0))[0].items():
                if s in R.GROWTH:
                    self.q_gain[s] = self.q_gain.get(s, 0) + v
        return a

    def main(self, rep, st):
        a = super().main(rep, st)
        if self.cap_mode and a:
            for s, v in R.MAIN_FX.get(a, {}).items():
                if s in R.GROWTH:
                    self.q_gain[s] = self.q_gain.get(s, 0) + v
        return a
