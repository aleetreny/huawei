"""Línea Mejora: bots de la réplica calibrada con una regla de L1 de detección imperfecta (investigación; nada
de esto va a un Skill).

L1Bot = PQBot (trimestre por tramos de qsearch) + veto en el nivel inicial, en los meses con Review in N <= l1vn,
con RR. HH. amable o quiet: descarta las opciones que bajan Network u Output, pero cada pérdida sólo se ve con
probabilidad l1det y una opción sin pérdida se marca por error con probabilidad l1fa. Las opciones con riesgo
verdadero > l1vr no se rescatan (si sólo queda eso, decide el modelo de elección como siempre).

    uv run python scripts/mejora/l1arms.py --bot M.L1Bot --arms "beta=v4fam+l1v=1+l1det=0.5"
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploracion"))
import dssim as D  # noqa: E402
import qsearch as Q  # noqa: E402
R = D.R


class L1Bot(Q.PQBot):
    def story_probs_x(self, rep, st, node):
        return None

    def story(self, rep, st, node):
        f = self.flags_x
        n = self.n_to_review(st)
        if not f.get("l1v") or st.level != 1 or n > int(f.get("l1vn", 1)) or self.hr > int(f.get("l1hr", 1)):
            return super().story(rep, st, node)
        det, fa, lim = float(f.get("l1det", 1.0)), float(f.get("l1fa", 0.0)), int(f.get("l1vr", 1))
        ks = [int(k) for k in rep.cat.nodes[node]["choices"]]
        effs = {k: rep.cat.nodes[node]["choices"][str(k)]["d"] for k in ks}
        risks = {k: rep.cat.answer_risk(node, k) for k in ks}
        flagged = set()
        for k in ks:
            e = effs[k]
            loses = e.get("network", 0) < 0 or e.get("output", 0) < 0 or (
                e.get("skill", 0) < 0 and st.skill + e.get("skill", 0) < R.THRESH[1][0])
            if (loses and self.rng.random() < det) or (not loses and self.rng.random() < fa):
                flagged.add(k)
        keep = [k for k in ks if k not in flagged and risks[k] <= lim]
        if not keep or len(keep) == len(ks):
            return super().story(rep, st, node)
        # elige entre las que quedan con el modelo de elección (mismas probabilidades relativas)
        ks2, p, _X = self.story_probs(rep, st, node)
        w = np.array([p[i] if ks2[i] in keep else 0.0 for i in range(len(ks2))])
        if w.sum() <= 0:
            return super().story(rep, st, node)
        i = int(self.rng.choices(range(len(ks2)), weights=w / w.sum())[0])
        if risks[ks2[i]] > 0:
            self.concerns += 1
        return ks2[i]


class QL1Bot(L1Bot):
    """L1Bot + umbral de Health recovery propio del nivel inicial (qh1) antes de la primera evaluación."""

    def energy(self, rep, st):
        f = self.flags_x
        if f.get("qh1") is not None and st.level == 1:
            saved = self.qh
            self.qh = int(f["qh1"])
            try:
                return super().energy(rep, st)
            finally:
                self.qh = saved
        return super().energy(rep, st)


class CountBot(L1Bot):
    """L1Bot que cuenta, en el nivel inicial con Review in 1, cuántas elecciones bajan Network u Output (tasa del banco)."""

    def story(self, rep, st, node):
        k = super().story(rep, st, node)
        if st.level == 1 and self.n_to_review(st) == 1:
            e = rep.cat.nodes[node]["choices"][str(k)]["d"]
            self.cnt[0] += 1
            self.cnt[1] += e.get("network", 0) < 0 or e.get("output", 0) < 0
        return k

    def __init__(self, per, seed=0, flags=None, beta=None):
        super().__init__(per, seed, flags, beta)
        self.cnt = [0, 0]


def loss_rate(spec, games=1500, seed=4242):
    import random as _r
    tot = [0, 0]
    for i in range(games):
        per = D.T.Perception("exact", seed=50_000 + i)
        bot = CountBot(per, seed=i, flags=D.T.parse_arm(spec))
        R.play(D.T.CAT, bot, _r.Random(seed + i))
        tot[0] += bot.cnt[0]; tot[1] += bot.cnt[1]
    return tot[1] / max(1, tot[0]), tot[0]


if __name__ == "__main__":
    B = "beta=v4fam+ep=RRR.RNR.SLR.SLR+mp=KP.KP.ROT.ROT+qh=5+hcare=2+hlow=5"
    for extra in ("", "+l1v=1+l1det=0.3", "+l1v=1+l1det=0.5", "+l1v=1+l1det=0.7", "+l1v=1+l1det=1"):
        print(extra or "base", loss_rate(B + extra))


class EndBot(QL1Bot):
    """QL1Bot + endhd: en el último trimestre, Health y Mental recovery hasta el tope antes que Defuse (cada punto de
    Health o Dignity vale 0,75 de nota final; Defuse, 2 de energía por 1 punto de riesgo = 1 de nota)."""

    def energy(self, rep, st):
        if self.flags_x.get("endhd") and st.month >= 46:
            self._tick(st)
            e = st.energy
            if st.health < 10 and e >= 1:
                return "Health recovery"
            if st.dignity < 10 and e >= 1:
                return "Mental recovery"
            if self.hr != D.C.FRIENDLY and e >= 2:
                return "Defuse legacy risk"
            return "Network maintenance" if e >= 1 else None
        return super().energy(rep, st)
