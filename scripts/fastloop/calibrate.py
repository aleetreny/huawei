"""Calibration of the fast-race ladder (lab/protocol/fastloop-v2.md): simulated challengers against a champion.

Game model fitted on the 153 race Haiku games of 26 Oct: completed games Normal(mu, 4.5), early exits Normal(28.6, 11.2).
Run: uv run python scripts/fastloop/calibrate.py  (about a minute)
"""
import numpy as np
rng = np.random.default_rng(7)
ELIM_MU, ELIM_SD, COMP_SD = 28.6, 11.2, 4.5

def games(p, mu, n):
    done = rng.random(n) < p
    q = np.where(done, rng.normal(mu, COMP_SD, n), rng.normal(ELIM_MU, ELIM_SD, n))
    return np.clip(q, 0, 100), done

def post_draws(q, done, k=3000):
    n, c = len(q), int(done.sum())
    p = rng.beta(1 + c, 1 + n - c, k)
    if c:
        mu = rng.normal(q[done].mean(), 5.0 / np.sqrt(c), k)
    else:
        mu = rng.normal(61, 8, k)
    return p * mu + (1 - p) * ELIM_MU

def p_better(ch, champ):
    return float((post_draws(*ch) > post_draws(*champ)).mean())

def ladder_B(ch_true, champ_true, n_c=12, kill1=0.05, kill2=0.15, crown=0.75, sizes=(2, 4, 8)):
    cq, cd = games(*champ_true, n_c)
    q, d = games(*ch_true, sizes[-1])
    for i, n in enumerate(sizes):
        pb = p_better((q[:n], d[:n]), (cq, cd))
        if i == 0 and pb < kill1: return 'kill1', n
        if i == 1 and pb < kill2: return 'kill2', n
        if i == 2: return ('crown' if pb >= crown else 'runner'), n
    return 'runner', sizes[-1]

def ladder_A(ch_true, champ_true, n_c=12, d1=15, d2=6, m=1.0, sizes=(2, 4, 8)):
    cq, cd = games(*champ_true, n_c); C = cq.mean()
    q, d = games(*ch_true, sizes[-1])
    if (~d[:2]).all() or q[:2].mean() < C - d1: return 'kill1', 2
    if q[:4].mean() < C - d2 or (~d[:4]).sum() >= 2: return 'kill2', 4
    return ('crown' if q.mean() >= C + m and (~d).sum() <= 1 else 'runner'), 8

def report(name, fn, champ, chs, reps=3000, **kw):
    print(f"== {name} champion p={champ[0]} mu={champ[1]} true={champ[0]*champ[1]+(1-champ[0])*ELIM_MU:.1f} {kw}")
    for label, ch in chs:
        tm = ch[0]*ch[1]+(1-ch[0])*ELIM_MU
        res = [fn(ch, champ, **kw) for _ in range(reps)]
        crown = np.mean([r[0]=='crown' for r in res]); k1 = np.mean([r[0]=='kill1' for r in res]); k2=np.mean([r[0]=='kill2' for r in res])
        print(f"  {label:16s} true {tm:5.1f}  crown {crown:5.2f}  kill@2 {k1:5.2f}  kill@4 {k2:5.2f}  games {np.mean([r[1] for r in res]):4.1f}")

V3 = (0.95, 71.0); F1 = (0.88, 63.4)
CH = [('much worse', (0.5, 61)), ('worse', (0.85, 65)), ('slightly worse', (0.95, 68)), ('equal', (0.95, 71)),
      ('slightly better', (0.97, 73)), ('better', (0.98, 76))]
CHF = [('much worse', (0.5, 61)), ('slightly worse', (0.85, 61)), ('equal', (0.88, 63.4)), ('better p', (0.95, 64)), ('v3-like', (0.95, 71))]

def ladder_H(ch_true, champ_true, n_c=12, kill1=0.05, kill2=0.15, crown=0.6, extend=0.35, sizes=(2, 4, 8, 12)):
    cq, cd = games(*champ_true, n_c)
    q, d = games(*ch_true, sizes[-1])
    for i, n in enumerate(sizes):
        pb = p_better((q[:n], d[:n]), (cq, cd))
        if i == 0 and pb < kill1: return 'kill1', n
        if i == 1 and pb < kill2: return 'kill2', n
        if i == 2:
            if pb >= crown: return 'crown', n
            if pb < extend: return 'runner', n
        if i == 3: return ('crown' if pb >= crown else 'runner'), n
    return 'runner', sizes[-1]

report('H crown .6 extend .35', ladder_H, V3, CH, reps=1500)
report('H crown .6 extend .35, champion n=20', ladder_H, V3, CH, reps=1500, n_c=20)
report('H crown .6 extend .35', ladder_H, F1, CHF, reps=1500)
