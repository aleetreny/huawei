"""Evaluaciones con explosion de riesgo en el semestre: que Output cuenta para ascender.

Para cada evaluacion (cambio de mes 6k -> 6k+1) toma los estados observados del semestre,
marca si hubo explosion ('Old landmines') y compara el Output visible antes de evaluar con el
Output maximo del semestre y con el de antes de la explosion.
"""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import replica as R
from bbdata import Batch, DATA, IDX

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
b = Batch(*batches)
tab = collections.Counter(); ex = []
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    st = g['steps']
    for i in range(len(st) - 1):
        s, n = st[i], st[i + 1]
        if s[0] == n[0] or s[0] % 6 != 0: continue
        m, L = s[0], s[4][IDX['level']]
        if L not in R.THRESH: continue
        thr = R.THRESH[L]
        promoted = n[4][IDX['level']] > L
        win = [x for x in st[:i + 1] if m - 5 <= x[0] <= m]
        blow_months = [x[0] for x in win if x[5] and 'Old landmines' in b.texts.get(x[5], '')]
        # explosion en el cambio de mes (llega con el texto del mes siguiente)
        blow_at_change = bool(n[5] and 'Old landmines' in b.texts.get(n[5], ''))
        outs = [x[4][IDX['output']] for x in win]
        last = s[4]  # estado antes de la ultima decision (aprox.)
        sk, nw, ou, dg = last[IDX['skill']], last[IDX['network']], last[IDX['output']], last[IDX['dignity']]
        if not blow_months: continue
        pre_blow = [x[4][IDX['output']] for x in win if x[0] < blow_months[0]]
        okS, okN = sk >= thr[0], nw >= thr[1]
        if not (okS and okN and dg >= 4): continue
        k = ('out_now_ok' if ou >= thr[2] else 'out_now_low',
             'max_ok' if max(outs) >= thr[2] else 'max_low',
             'preblow_ok' if pre_blow and max(pre_blow) >= thr[2] else 'preblow_low',
             'L%d' % L, 'promoted' if promoted else 'not')
        tab[k] += 1
        if ou < thr[2] and promoted and len(ex) < 8: ex.append((g['g'], m, blow_months, outs, thr))
for k, v in sorted(tab.items()): print(v, k)
for e in ex: print(e)
