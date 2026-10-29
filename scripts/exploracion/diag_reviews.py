"""Diagnóstico en la réplica calibrada: en cada evaluación perdida, qué indicador faltaba y por cuánto."""
import sys, random, collections, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D
R, T = D.R, D.T
import numpy as np


class Rec(D.XBot):
    pass


def run(spec, games, seed=4242):
    miss = collections.Counter(); short = collections.defaultdict(list); tot = collections.Counter()
    gap_by = collections.defaultdict(list)
    for i in range(games):
        bot = Rec(T.Perception("exact", seed=50000 + i), seed=i, flags=T.parse_arm(spec))
        rep_rng = random.Random(seed + i)
        # monkeypatch review to record
        orig = R.Replica.review
        recs = []
        def review(self, st, explosion_now=False, _o=orig):
            lv = st.level; t = R.THRESH.get(lv)
            snap = (lv, st.month, st.skill, st.network, st.output, st.dignity, st.risk)
            info = _o(self, st, explosion_now)
            recs.append((snap, info, t))
            return info
        R.Replica.review = review
        try:
            st, trace = R.play(T.CAT, bot, rep_rng)
        finally:
            R.Replica.review = orig
        for (lv, m, s, n, o, d, rk), info, t in recs:
            if not t: continue
            tot[lv] += 1
            if info["promoted"]: continue
            miss[lv] += 1
            why = []
            for nm, v, th in (("S", s, t[0]), ("N", n, t[1]), ("O", o, t[2])):
                if v < th:
                    why.append(nm); gap_by[(lv, nm)].append(th - v)
            if d < 4: why.append("D")
            if info["grade"] == "D": why.append("gradeD")
            short[lv].append("+".join(why) or "?")
    for lv in sorted(tot):
        c = collections.Counter(short[lv])
        print(f"L{lv}: evaluaciones {tot[lv]}, perdidas {miss[lv]} ({miss[lv]/tot[lv]:.0%}) causas {dict(c.most_common(8))}")
        for nm in "SNO":
            g = gap_by[(lv, nm)]
            if g: print(f"     falta {nm}: {len(g)} veces, mediana {np.median(g):.0f}, media {np.mean(g):.1f}")


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]))
