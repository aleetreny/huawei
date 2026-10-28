"""Linea Techo: diagnostico por evaluacion. Para cada politica, en cada ventana de evaluacion: cuantas partidas
llegan vivas, cuantas ascienden y, cuando no, que indicador falta y si ya faltaba al empezar el mes previo.
Tambien el ritmo de Skill por nivel (historias frente a trimestre) y el mes medio de cada ascenso.

    uv run python scripts/techo/diag.py --arms planner,base,caps --per exact --games 1000
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
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
import planner as P  # noqa: E402
import replica as R  # noqa: E402
import techobot as T  # noqa: E402

OPT = json.load(open(REPO / "lab/data/ingenieria-inversa/politica_optima.json"))["params"]


class SignPlanner(P.Planner):
    """El planificador ajustado valorando las historias solo con signos (+-1) y la marca de riesgo (x2), con ablaciones:
    capthr (techos en vez de umbrales), nocont (sin continuacion), norb (sin refuerzo del mes previo), nohd (sin valorar
    Health/Dignity), flat (mismo peso por debajo y por encima del umbral), lexq (trimestre de v4), noskhi (sin extra de
    Skill en L4+), signmag (signos exactos pero con magnitud)."""

    def __init__(self, per, abl: set[str], **p):
        pp = dict(p)
        if "norb" in abl:
            pp["review_boost"] = 1.0
        if "nocont" in abl:
            pp["w_cont"] = 0.0
        if "nohd" in abl:
            pp["w_h"], pp["w_d"] = 0.1, 0.1
        if "flat" in abl:
            pp["w_below"] = pp["w_above"] = 3.0
        if "noskhi" in abl:
            pp["w_skill_hi"] = 1.0
        if "dfloor4" in abl:
            pp["d_floor"] = 4
        if "hfloor4" in abl:
            pp["h_floor"] = 4
        if "riskhi" in abl:
            pp["risk_cost"] = 30.0   # casi estricto: una opcion marcada solo si no hay otra
        super().__init__(**pp)
        self.per, self.abl = per, abl

    def value(self, rep, st, fx, dr):
        if "capthr" not in self.abl:
            return super().value(rep, st, fx, dr)
        save = R.THRESH
        R.THRESH = {lv: (R.cap(lv, "skill"), R.cap(lv, "network"), R.cap(lv, "output")) for lv in range(1, 8)}
        try:
            return super().value(rep, st, fx, dr)
        finally:
            R.THRESH = save

    def _see(self, rep, node, k):
        if "signmag" in self.abl:
            d = rep.cat.nodes[node]["choices"][str(k)]["d"]
            r = rep.cat.answer_risk(node, k)
            return {a: float(b) for a, b in d.items()}, 2 * ((r > 0) - (r < 0))
        signs, rs = self.per.see(node, k)
        return {a: float(b) for a, b in signs.items()}, 2 * rs

    def story(self, rep, st, node):
        best, bv = 1, -1e18
        n = rep.cat.nodes[node]
        for kk, ch in n["choices"].items():
            k = int(kk)
            fx, dr = self._see(rep, node, k)
            v = self.value(rep, st, fx, dr)
            nxt = ch.get("next")
            if nxt and nxt in rep.cat.nodes and self.p["w_cont"] > 0:
                tmp = R.State(**{a: b for a, b in st.__dict__.items() if a not in ("out_hist", "grades")})
                R.apply_delta(tmp, {a: b for a, b in fx.items()})
                tmp.risk = max(0, tmp.risk + dr)
                cont = [self.value(rep, tmp, *self._see(rep, nxt, int(k2))) for k2 in rep.cat.nodes[nxt]["choices"]]
                if cont:
                    v += self.p["w_cont"] * max(cont)
            if v > bv:
                best, bv = k, v
        return best

    def energy(self, rep, st):
        if "lexq" not in self.abl or st.month >= 46:
            return super().energy(rep, st)
        if min(st.risk, 4) >= 1 and st.energy >= 3 and st.health > 4:
            return "Defuse legacy risk"
        if st.health <= 4 and st.energy >= 1:
            return "Health recovery"
        return {3: "Prepare report materials", 2: "Network maintenance", 1: "Prepare report materials"}.get(st.energy)

    def main(self, rep, st):
        if "lexq" not in self.abl or st.month >= 46:
            return super().main(rep, st)
        return "Lay low and reduce risk" if min(st.risk, 4) >= 2 else "Apply for a key project"


class Probe(R.Policy):
    """Envuelve una politica y anota el estado al empezar cada mes y lo que gana Skill en historias y trimestre."""

    def __init__(self, bot):
        self.bot, self.snap, self.rows = bot, {}, []
        self.skill_story = collections.Counter()
        self.skill_q = collections.Counter()
        self.months_in = collections.Counter()
        self._last = None

    def _see(self, st):
        m = st.month
        if m not in self.snap:
            self.snap[m] = (st.level, st.skill, st.network, st.output, st.dignity, st.blowups)
            self.months_in[st.level] += 1
            if m % 6 == 0 and (m - 1) in self.snap:
                lv0, s0, n0, o0, d0, b0 = self.snap[m - 1]
                if st.level == lv0:
                    thr = R.THRESH.get(lv0, R.THRESH[6])
                    now = [k for k, v, t in (("S", st.skill, thr[0]), ("N", st.network, thr[1]), ("O", st.output, thr[2])) if v < t]
                    before = [k for k, v, t in (("S", s0, thr[0]), ("N", n0, thr[1]), ("O", o0, thr[2])) if v < t]
                    self.rows.append({"month": m, "level": lv0, "promoted": False, "short": now, "short_before": before,
                                      "dignity_low": st.dignity < 4, "blew": st.blowups > b0})
                else:
                    self.rows.append({"month": m, "level": lv0, "promoted": True})

    def story(self, rep, st, node):
        self._see(st)
        s0 = st.skill
        k = self.bot.story(rep, st, node)
        self._pending = ("e", st.level, s0)
        return k

    def energy(self, rep, st):
        self._see(st)
        self._pending = ("q", st.level, st.skill)
        return self.bot.energy(rep, st)

    def main(self, rep, st):
        self._see(st)
        self._pending = ("q", st.level, st.skill)
        return self.bot.main(rep, st)


class Traced(R.Replica):
    pass


def _play(job):
    spec, per_mode, i, seed0 = job
    if spec == "planner":
        bot = P.Planner(**OPT)
    elif spec.startswith("sp"):
        per = T.Perception(per_mode, seed=50_000 + i)
        bot = SignPlanner(per, set(spec.split("+")[1:]), **OPT)
    else:
        per = T.Perception(per_mode, seed=50_000 + i)
        bot = T.V4Bot(per, seed=i, flags=T.parse_arm(spec))
    probe = Probe(bot)
    # ritmo de Skill: diferencia de Skill entre el inicio de meses consecutivos, por nivel
    st, trace = R.play(T.CAT, probe, random.Random(seed0 + i))
    probe._see(st) if st.alive else None
    gains = collections.defaultdict(list)
    ngains = collections.defaultdict(list)
    ms = sorted(probe.snap)
    for a, b in zip(ms, ms[1:]):
        lv = probe.snap[a][0]
        if probe.snap[b][0] == lv:
            gains[lv].append(probe.snap[b][1] - probe.snap[a][1])
            ngains[lv].append((probe.snap[b][2] - probe.snap[a][2], probe.snap[b][3] - probe.snap[a][3]))
    # Skill del trimestre: de la traza (acciones q/m con efecto skill)
    qskill = collections.Counter()
    for t in trace:
        if t[1] == "q":
            qskill[t[0]] += R.ENERGY_FX[t[2]][0].get("skill", 0)
        elif t[1] == "m":
            qskill[t[0]] += R.MAIN_FX[t[2]].get("skill", 0)
    qs_by_level = collections.Counter()
    for m, v in qskill.items():
        if m in probe.snap:
            qs_by_level[probe.snap[m][0]] += v
    return {"q": R.Replica.score(st), "level": st.level, "fail": st.failure or "ok", "rows": probe.rows,
            "gains": {k: v for k, v in gains.items()}, "ngains": dict(ngains), "qskill": dict(qs_by_level), "months_in": dict(probe.months_in),
            "promos": [m for m, kind, *rest in trace if kind == "r" and rest[0].get("promoted")]}


def report(name, out):
    n = len(out)
    q = np.array([o["q"] for o in out])
    lv = collections.Counter(o["level"] for o in out)
    fails = collections.Counter(o["fail"] for o in out)
    print(f"\n=== {name}: Q {q.mean():.2f} | L6+ {sum(v for k, v in lv.items() if k >= 6) / n:.0%} | {dict(fails)}")
    # ventanas
    by = collections.defaultdict(collections.Counter)
    for o in out:
        for r in o["rows"]:
            key = r["month"]
            by[key]["alive"] += 1
            if r["promoted"]:
                by[key]["promo"] += 1
                by[key][f"from L{r['level']}"] += 1
            else:
                why = "blew" if r["blew"] else ("dignity" if r["dignity_low"] and not r["short"] else
                      "lost in prep: " + "".join(sorted(set(r["short"]) - set(r["short_before"])))
                      if set(r["short"]) - set(r["short_before"]) else
                      "short before prep: " + "".join(r["short_before"]) if r["short_before"] else "other")
                by[key][f"L{r['level']} {why}"] += 1
    print("ventana  vivas  ascienden  | por que no (nivel, causa)")
    for m in sorted(by):
        c = by[m]
        rest = {k: v for k, v in c.most_common() if k not in ("alive", "promo") and not k.startswith("from")}
        top = ", ".join(f"{k}:{v}" for k, v in list(rest.items())[:5])
        print(f"m{m:<3d}   {c['alive']:5d}  {c['promo'] / max(1, c['alive']):8.0%}  | {top}")
    # ritmo de skill
    print("nivel  meses(media)  Skill/mes  de los cuales trimestre/mes   Network/mes  Output/mes")
    for lv_ in range(1, 7):
        g = [x for o in out for x in o["gains"].get(lv_, [])]
        ng = [x for o in out for x in o["ngains"].get(lv_, [])]
        months = [o["months_in"].get(lv_, 0) for o in out if o["months_in"].get(lv_, 0)]
        qs = sum(o["qskill"].get(lv_, 0) for o in out)
        tot_months = sum(months)
        if g:
            print(f"L{lv_}     {np.mean(months):5.1f}        {np.mean(g):5.2f}      {qs / max(1, tot_months):5.2f}"
                  f"               {np.mean([x[0] for x in ng]):5.2f}        {np.mean([x[1] for x in ng]):5.2f}")
    pm = collections.defaultdict(list)
    for o in out:
        for j, m in enumerate(o["promos"]):
            pm[j + 2].append(m)
    print("mes medio del ascenso a:", {f"L{k}": f"{np.mean(v):.1f} ({len(v) / n:.0%})" for k, v in sorted(pm.items())})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="planner,base")
    ap.add_argument("--per", default="exact")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    with ProcessPoolExecutor(a.workers) as ex:
        for spec in a.arms.split(","):
            out = list(ex.map(_play, [(spec, a.per, i, a.seed) for i in range(a.games)], chunksize=25))
            report(f"{spec} [{a.per if spec != 'planner' else 'exact fx'}]", out)


if __name__ == "__main__":
    main()
