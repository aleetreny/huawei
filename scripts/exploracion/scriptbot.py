"""Script que decide las historias con las lecturas de DeepSeek (réplica calibrada), y el híbrido de Winfred.

Percepción 'ds': una pasada de etiquetas reales de DeepSeek al azar por opción y encuentro.
Brazos (flags):
  sp          SignPlanner de techo/diag.py (privilegiado: riesgo exacto y umbrales) sobre lecturas ds
  sp+capthr   … con techos en vez de umbrales
  hyb=0.7     híbrido: el script decide sólo si su elección se mantiene en >=70 % de 20 perturbaciones de la
              lectura; si no, decide DeepSeek (modelo calibrado)
Investigación, no texto de Skill.
"""
from __future__ import annotations
import sys, random, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "techo"))
import dssim as D
import diag as DG
import numpy as np
R, T, CM = D.R, D.T, D.CM

OPT = DG.OPT
LK = ("health", "dignity", "skill", "network", "output", "wealth")


class DSPer:
    """Perception from real DeepSeek label passes (one random pass per encounter)."""
    def __init__(self, seed):
        self.rng = random.Random(seed)

    def see(self, node, k):
        L = D.option_labels(node, k)
        keys = [f for f in L if L[f]]
        if not keys:
            return {s: 0 for s in LK}, 0
        lab = CM.lab_signs(L[self.rng.choice(keys)])
        return {s: int(lab.get(s, 0)) for s in LK}, int(lab.get("risk", 0))


def perturb(signs, rs, rng):
    out = {}
    for s, v in signs.items():
        if v != 0 and rng.random() < 0.3:
            v = 0
        elif v == 0 and rng.random() < 0.1:
            v = rng.choice((1, -1))
        out[s] = v
    if rs > 0 and rng.random() < 0.15:
        rs = 0
    elif rs <= 0 and rng.random() < 0.2:
        rs = 1
    return out, rs


class HybBot(D.XBot):
    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        f = self.flags_x
        abl = set(x for x in ("capthr", "nocont", "lexq", "flat") if f.get(x))
        self.sp = DG.SignPlanner(DSPer(seed + 777), abl, **OPT)
        self.mode = "sp" if f.get("sp") else ("hyb" if f.get("hyb") else "ds")
        self.thr = float(f.get("hyb", 0.7)) if f.get("hyb") else None
        self.prng = random.Random(seed + 99)
        self.stats = {"script": 0, "ds": 0}

    def story(self, rep, st, node):
        if self.mode == "ds":
            return super().story(rep, st, node)
        if self.mode == "sp":
            self._tick(st)
            return self.sp.story(rep, st, node)
        # hybrid: one reading, perturbed
        self._tick(st)
        ks = [int(k) for k in rep.cat.nodes[node]["choices"]]
        base = {k: self.sp.per.see(node, k) for k in ks}
        orig = self.sp.per.see
        votes = {}
        for i in range(20):
            pert = {k: perturb(*base[k], self.prng) for k in ks}
            self.sp.per.see = lambda nd, k, pert=pert: pert.get(k, orig(nd, k)) if nd == node else orig(nd, k)
            c = self.sp.story(rep, st, node)
            votes[c] = votes.get(c, 0) + 1
        self.sp.per.see = orig
        c, v = max(votes.items(), key=lambda x: x[1])
        if v / 20 >= self.thr:
            self.stats["script"] += 1
            if rep.cat.answer_risk(node, c) > 0:
                self.concerns += 1
            return c
        self.stats["ds"] += 1
        return super().story(rep, st, node)

    def energy(self, rep, st):
        if self.flags_x.get("spq"):
            return self.sp.energy(rep, st)
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.flags_x.get("spq"):
            return self.sp.main(rep, st)
        return super().main(rep, st)


class PlannerBot(R.Policy):
    """Reference: the tuned planner with exact effects (privileged)."""
    def __init__(self, per, seed=0, flags=None):
        import planner as P
        self.p = P.Planner(**OPT)
    def story(self, rep, st, node): return self.p.story(rep, st, node)
    def energy(self, rep, st): return self.p.energy(rep, st)
    def main(self, rep, st): return self.p.main(rep, st)


if __name__ == "__main__":
    which = sys.argv[3] if len(sys.argv) > 3 else "hyb"
    D.run(sys.argv[1].split(","), int(sys.argv[2]), botcls=PlannerBot if which == "planner" else HybBot)


class SwapBot(D.XBot):
    """DeepSeek (calibrated) everywhere except where the flags hand the decision to the exact planner:
    pl=1 (stories at L1), pl=23, pl=4, pl=5 (levels), plq (quarters), plrev (review months N<=2 only)."""
    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        import planner as P
        self.pp = P.Planner(**OPT)
        f = self.flags_x
        self.pl_levels = set(int(c) for c in str(f.get("pl", "")) if c.isdigit())
        self.plrev = bool(f.get("plrev"))

    def story(self, rep, st, node):
        n = self.n_to_review(st)
        if st.level in self.pl_levels and (not self.plrev or n in (1, 2)):
            self._tick(st)
            k = self.pp.story(rep, st, node)
            if rep.cat.answer_risk(node, k) > 0:
                self.concerns += 1
            return k
        return super().story(rep, st, node)

    def energy(self, rep, st):
        if self.flags_x.get("plq"):
            return self.pp.energy(rep, st)
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.flags_x.get("plq"):
            return self.pp.main(rep, st)
        return super().main(rep, st)
