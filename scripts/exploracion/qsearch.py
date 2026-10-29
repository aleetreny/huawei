"""Búsqueda del reparto trimestral por tramos de nivel en la réplica calibrada (historias = DeepSeek calibrado).

Política paramétrica por tramo (L1, L2-3, L4, L5+): plan de energía (3 puntos) y acción principal; reglas fijas
antes: último trimestre (cierre), salud baja (recuperar si Health <= qh), RR. HH. (Defuse con cualquier tono que
no sea el amable; Lay low con frowning o peor). Opcional: saltar el indicador que ya está en su tope (caps=truth).
Investigación: nada de esto va a un Skill tal cual.
"""
from __future__ import annotations
import sys, json, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D
R = D.R

EPLANS = {"RRR": ["Prepare report materials"] * 3, "RNR": ["Prepare report materials", "Network maintenance", "Prepare report materials"],
          "NNN": ["Network maintenance"] * 3, "RNN": ["Prepare report materials", "Network maintenance", "Network maintenance"],
          "SLR": ["Skill learning", "Prepare report materials"], "SLN": ["Skill learning", "Network maintenance"]}
MAINS = {"KP": "Apply for a key project", "ROT": "Apply for rotation", "MEN": "Build a mentorship", "REP": "Report results to your manager"}
STAT_OF = {"Prepare report materials": "output", "Network maintenance": "network", "Skill learning": "skill"}
FALLBACK = {"output": "Network maintenance", "network": "Prepare report materials", "skill": "Prepare report materials"}


def band(level):
    return 0 if level == 1 else 1 if level <= 3 else 2 if level == 4 else 3


class PQBot(D.XBot):
    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        f = self.flags_x
        self.ep = f.get("ep", "RNR.RNR.SLN.SLN").split(".")
        self.mp = f.get("mp", "KP.KP.ROT.ROT").split(".")
        self.qh = int(f.get("qh", 4))
        self.capsk = f.get("caps") == "truth"
        self.qi = 0

    def energy(self, rep, st):
        self._tick(st)
        e = st.energy
        if e == 3:
            self.qi = 0
        if st.month >= 46:
            return super().energy(rep, st)
        if st.health <= self.qh and e >= 1 and st.health < 10:
            return "Health recovery"
        if st.dignity <= 4 and e >= 1:
            return "Mental recovery"
        if st.network <= 0 and e >= 1:
            return "Network maintenance"
        if self.hr != D.C.FRIENDLY and e == 3:
            return "Defuse legacy risk"
        plan = EPLANS[self.ep[band(st.level)]]
        while self.qi < len(plan):
            a = plan[self.qi]; self.qi += 1
            cost = R.ENERGY_FX[a][1]
            if cost > e:
                continue
            if a == "Skill learning" and st.health <= self.qh + 1:
                a = "Prepare report materials"
            if self.capsk and getattr(st, STAT_OF[a]) >= R.cap(st.level, STAT_OF[a]):
                alt = FALLBACK[STAT_OF[a]]
                if getattr(st, STAT_OF[alt]) >= R.cap(st.level, STAT_OF[alt]):
                    alt = "Skill learning" if e >= 2 and st.health > self.qh + 1 and st.skill < R.cap(st.level, "skill") else ("Health recovery" if st.health < 10 else "Mental recovery")
                a = alt
            if R.ENERGY_FX[a][1] <= e:
                return a
        if e >= 1:
            return "Health recovery" if st.health < 10 else ("Mental recovery" if st.dignity < 10 else "Network maintenance")
        return None

    def main(self, rep, st):
        self._tick(st)
        if st.month >= 46:
            return super().main(rep, st)
        if st.health <= 4 or st.dignity <= 4 or st.network <= 0 or st.wealth < 0:
            return "Repair a key relationship" if st.health > 4 else "Lay low and reduce risk"
        if self.hr not in (D.C.FRIENDLY, D.C.QUIET):
            return "Lay low and reduce risk"
        return MAINS[self.mp[band(st.level)]]


def score(spec, games, seed):
    out = D.run([spec], games, seed=seed, botcls=PQBot, quiet=True)[spec]
    import numpy as np
    return float(np.mean([r["q"] for r in out])), out


def search(games=1500, seed=777, base_extra="beta=v4fam+qh=5"):
    ep = ["RRR", "RNR", "SLN", "SLN"]; mp = ["KP", "KP", "ROT", "ROT"]
    best = None
    for rnd in range(2):
        for b in range(4):
            res = []
            for e, m in itertools.product(EPLANS, MAINS):
                ep2, mp2 = list(ep), list(mp)
                ep2[b], mp2[b] = e, m
                spec = f"{base_extra}+ep={'.'.join(ep2)}+mp={'.'.join(mp2)}"
                q, _ = score(spec, games, seed)
                res.append((q, e, m))
            res.sort(reverse=True)
            ep[b], mp[b] = res[0][1], res[0][2]
            print(f"ronda {rnd} tramo {b}: mejor {res[0][1]}/{res[0][2]} {res[0][0]:.2f}; siguientes {[(round(x[0],2),x[1],x[2]) for x in res[1:4]]}; actual peor {res[-1][0]:.2f}", flush=True)
        best = (ep, mp)
    print("FINAL", ".".join(ep), ".".join(mp))


if __name__ == "__main__":
    search()
