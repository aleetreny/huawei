"""Trimestre planificado por script (réplica calibrada): techos conocidos (cota) o detectados en partida.

Detección (lo que un script del Skill puede hacer con lo que devuelve el juego): el menú del trimestre publica
el efecto exacto de cada acción; si tras una acción el indicador sube menos de lo anunciado, su valor actual es
el tope de ese nivel (se guarda el valor; vale hasta el siguiente ascenso). Investigación, no texto de Skill.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D
R, T = D.R, D.T

GAIN_E = {"output": ("Prepare report materials", 1), "network": ("Network maintenance", 1), "skill": ("Skill learning", 2)}


class QBot(D.XBot):
    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        f = self.flags_x
        self.capq = f.get("capq", "")          # '' (cp rules), 'truth', 'detect'
        self.order = f.get("qorder", "ons")    # priority among growth stats at L1-L3
        self.skfrom = int(f.get("skfrom", 4))  # from this level Skill first
        self.hmin = int(f.get("hmin", 4))
        self.known_cap = {}                    # stat -> value seen as the top at this level
        self.cap_lv = None
        self.pending = None                    # (stat, before, expected gain)
        self.mainpref = f.get("mainq", "kp")   # 'kp' key project default; 'tgt' main action that hits the target

    # ----- detection
    def _cap_tick(self, st):
        if self.cap_lv != st.level:
            self.cap_lv, self.known_cap = st.level, {}
        if self.pending:
            for s, before, gain in self.pending:
                now = getattr(st, s)
                if now < before + gain:
                    self.known_cap[s] = now
            self.pending = None

    def capped(self, st, s):
        if self.capq == "truth":
            return getattr(st, s) >= R.cap(st.level, s)
        if self.capq == "detect":
            return s in self.known_cap and getattr(st, s) >= self.known_cap[s]
        return False

    def energy(self, rep, st):
        if not self.capq:
            return super().energy(rep, st)
        self._tick(st)
        self._cap_tick(st)
        e = st.energy
        if st.month >= 46:
            return super().energy(rep, st)
        if st.health <= self.hmin and e >= 1:
            return "Health recovery"
        if st.dignity <= 4 and e >= 1:
            return "Mental recovery"
        if st.network <= 0 and e >= 1:
            return "Network maintenance"
        if self.hr != D.C.FRIENDLY and e == 3:
            return "Defuse legacy risk"
        order = list(self.order_for(st))
        for s in order:
            if self.capped(st, s):
                continue
            name, cost = GAIN_E[s]
            if cost > e:
                continue
            if s == "skill" and st.health <= self.hmin + 1:
                continue
            fx = R.ENERGY_FX[name][0]
            self.pending = [(k, getattr(st, k), v) for k, v in fx.items() if k in R.GROWTH]
            return name
        if e >= 1 and st.health < 10:
            return "Health recovery"
        if e >= 1 and st.dignity < 10:
            return "Mental recovery"
        return None

    def order_for(self, st):
        if st.level >= self.skfrom:
            return ("skill", "output", "network")
        return {"ons": ("output", "network", "skill"), "nos": ("network", "output", "skill"),
                "son": ("skill", "output", "network")}[self.order]

    def main(self, rep, st):
        if not self.capq:
            return super().main(rep, st)
        self._tick(st)
        self._cap_tick(st)
        if st.month >= 46:
            return super().main(rep, st)
        if st.health <= 4 or st.dignity <= 4 or st.network <= 0 or st.wealth < 0:
            return "Repair a key relationship" if st.health > 4 else "Lay low and reduce risk"
        if self.hr not in (D.C.FRIENDLY, D.C.QUIET):
            return "Lay low and reduce risk"
        open_ = [s for s in ("skill", "network", "output") if not self.capped(st, s)]
        if st.level >= self.skfrom and "skill" in open_:
            name = "Apply for rotation" if self.mainpref == "tgt" or "output" not in open_ else "Apply for a key project"
            if self.flags_x.get("l4rot"):
                name = "Apply for rotation"
        elif not open_:
            name = "Report results to your manager"
        elif self.mainpref == "tgt" and len(open_) == 1:
            name = {"skill": "Apply for rotation", "network": "Build a mentorship", "output": "Showcase results"}[open_[0]]
        else:
            name = "Apply for a key project"
        fx = R.MAIN_FX[name]
        self.pending = [(k, getattr(st, k), v) for k, v in fx.items() if k in R.GROWTH]
        return name


if __name__ == "__main__":
    D.run(sys.argv[1].split(","), int(sys.argv[2]) if len(sys.argv) > 2 else 2000, botcls=QBot)
