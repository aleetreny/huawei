"""Linea Techo: cuando toma una opcion marcada como arriesgada el planificador de signos sin privilegios
(sp+capthr+lexq+hfloor4), y que gana con ella frente a la mejor opcion no marcada. Investigacion.

    uv run python scripts/techo/riskwhen.py --games 500
"""
from __future__ import annotations
import argparse, collections, random, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "scripts" / "ingenieria-inversa"))
import replica as R, techobot as T, diag as D

class Probe(D.SignPlanner):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.rows = []; self.month = None; self.hr = 0
    def story(self, rep, st, node):
        if st.month != self.month:
            self.month, self.hr = st.month, min(st.risk, 4)
        k = super().story(rep, st, node)
        seen = {int(kk): self._see(rep, node, int(kk)) for kk in rep.cat.nodes[node]["choices"]}
        fx, dr = seen[k]
        grow = lambda f: sum(1 for g in R.GROWTH if f.get(g, 0) > 0) - sum(1 for g in R.GROWTH if f.get(g, 0) < 0)
        safe = [v for kk, v in seen.items() if v[1] <= 0]
        best_safe = max((grow(f) for f, _ in safe), default=None)
        n = 6 - st.month % 6 if st.month % 6 else 6
        self.rows.append(dict(level=st.level, n=n, risk=st.risk, hr=self.hr, flagged=dr > 0, all_flagged=not safe,
                              gain=grow(fx), best_safe=best_safe, h=st.health, d=st.dignity, real=rep.cat.answer_risk(node, k)))
        return k

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--games", type=int, default=500); a = ap.parse_args()
    rows = []
    for i in range(a.games):
        per = T.Perception("exact", seed=50_000 + i)
        bot = Probe(per, {"capthr", "lexq", "hfloor4"}, **D.OPT)
        R.play(T.CAT, bot, random.Random(4242 + i)); rows += bot.rows
    fl = [r for r in rows if r["flagged"]]
    print(f"{len(rows)} decisiones, {len(fl)} marcadas elegidas ({len(fl)/len(rows):.1%}); forzadas {sum(r['all_flagged'] for r in fl)}")
    vol = [r for r in fl if not r["all_flagged"]]
    print(f"voluntarias: {len(vol)} ({len(vol)/a.games:.1f} por partida); riesgo real medio {np.mean([r['real'] for r in vol]):.2f}")
    print("por contador de riesgo vivo:", dict(sorted(collections.Counter(r["risk"] for r in vol).items())))
    print("por RR. HH. del mes:", dict(sorted(collections.Counter(r["hr"] for r in vol).items())))
    print("por nivel:", dict(sorted(collections.Counter(r["level"] for r in vol).items())))
    print("por N (meses hasta la evaluacion):", dict(sorted(collections.Counter(r["n"] for r in vol).items())))
    print("ventaja de crecimiento (elegida - mejor segura):", dict(sorted(collections.Counter(r["gain"] - r["best_safe"] for r in vol).items())))
    print("gain elegida:", dict(sorted(collections.Counter(r["gain"] for r in vol).items())), " best_safe:", dict(sorted(collections.Counter(r["best_safe"] for r in vol).items())))
    # oportunidades: decisiones con riesgo vivo 0, no forzadas, donde existia una marcada con mas crecimiento
    opp = [r for r in rows if not r["all_flagged"]]
    print("decisiones no forzadas con contador 0:", sum(1 for r in opp if r["risk"] == 0), "de", len(opp))

if __name__ == "__main__":
    main()
