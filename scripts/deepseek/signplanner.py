"""The tuned planner (politica_optima.json) valuing stories only from perceived signs (+-1) and the risk flag,
with ablations (capthr: caps instead of thresholds; lexq: t13-read-v4-like quarter; noskhi; nowealth).

    uv run python scripts/deepseek/signplanner.py 1500 2:1:,2:1:capthr,2:1:lexq [labels,...]
"""
import sys, json, random, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ingenieria-inversa'))
import groupbot as G
import planner as P
R = G.R
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from datapaths import deepseek_dir as _dsdir
params = json.load(open(Path(__file__).resolve().parents[2] / 'lab/data/ingenieria-inversa/politica_optima.json'))['params']
L = str(_dsdir() / 'labels') + '/'

class SignPlanner(P.Planner):
    """The tuned planner, but stories are valued only from perceived signs (+-1) and the risk flag."""
    def __init__(self, per, rmul=1.0, mag=1.0, capthr=False, lexq=False, **p):
        super().__init__(**p); self.per, self.rmul, self.mag, self.capthr, self.lexq = per, rmul, mag, capthr, lexq
    def value(self, rep, st, fx, dr):
        if not self.capthr:
            return super().value(rep, st, fx, dr)
        save = R.THRESH
        R.THRESH = {lv: (R.cap(lv, 'skill'), R.cap(lv, 'network'), R.cap(lv, 'output')) for lv in range(1, 8)}
        try:
            return super().value(rep, st, fx, dr)
        finally:
            R.THRESH = save
    def energy(self, rep, st):
        if not self.lexq: return super().energy(rep, st)
        if st.month >= 46: return super().energy(rep, st)
        if min(st.risk, 4) >= 2 and st.energy >= 3 and st.health > 4: return "Defuse legacy risk"
        if st.health <= 4 and st.energy >= 1: return "Health recovery"
        return {3: "Prepare report materials", 2: "Network maintenance", 1: "Prepare report materials"}.get(st.energy)
    def main(self, rep, st):
        if not self.lexq: return super().main(rep, st)
        if st.month >= 46: return super().main(rep, st)
        return "Lay low and reduce risk" if min(st.risk, 4) >= 2 else "Apply for a key project"
    def story(self, rep, st, node):
        best, bv = 1, -1e18
        for k in rep.cat.nodes[node]["choices"]:
            k = int(k)
            fx, sign = self.per.see(node, k)
            fx = {a: b * self.mag for a, b in fx.items()}
            dr = self.rmul * sign
            v = self.value(rep, st, fx, dr)
            if v > bv: best, bv = k, v
        return best

def mk(lab, rmul, mag, i, extra=''):
    sets = [json.load(open(L + f)) for f in lab.split('+')]
    pers = [G.Perception(s, 'signs', 'flag') for s in sets]
    per = pers[0] if len(pers) == 1 else G.Mixed(pers)
    if hasattr(per, 'rng'): per.rng = random.Random(i)
    pp = dict(params)
    if 'noskhi' in extra: pp['w_skill_hi'] = 1.0
    if 'nowealth' in extra: pp['w_wealth'] = 0.2
    return SignPlanner(per, rmul, mag, capthr='capthr' in extra, lexq='lexq' in extra, **pp)

def run(a):
    lab, rmul, mag, extra, i = a
    st, tr = R.play(G.CAT, mk(lab, rmul, mag, i, extra), random.Random(4242 + i))
    return R.Replica.score(st), st.level, st.failure or 'completed'

if __name__ == '__main__':
    n = int(sys.argv[1]); arms = [tuple((x + '::').split(':')[:3]) for x in sys.argv[2].split(',')]
    labs = sys.argv[3].split(',') if len(sys.argv) > 3 else ['truth-all.json', 'ds-v3-r1-full.json+ds-v3-r2-full.json']
    for lab in labs:
        for rmul, mag, extra in arms:
            with ProcessPoolExecutor(8) as ex:
                out = list(ex.map(run, [(lab, float(rmul), float(mag), extra, i) for i in range(n)], chunksize=25))
            s = np.array([o[0] for o in out]); f = collections.Counter(o[2] for o in out)
            done = [o[0] for o in out if o[2] == 'completed']
            l6 = sum(o[1] >= 6 for o in out) / n
            print(f"{lab[:8]:8s} risk x{rmul} {extra:18s} {s.mean():5.1f} ±{s.std(ddof=1)/np.sqrt(n):.2f} completed-mean {np.mean(done):5.1f} L6 {l6:4.0%} {dict(f)}", flush=True)
