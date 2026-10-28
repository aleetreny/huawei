"""Ascenso segun Output visible y explosiones anteriores al semestre (todas las evaluaciones con S y N en regla)."""
import sys, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import replica as R
from bbdata import Batch, DATA, IDX

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
b = Batch(*batches)
tab = collections.Counter(); ex = collections.defaultdict(list)
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    st = g['steps']; blows = []
    for i in range(len(st) - 1):
        s, n = st[i], st[i + 1]
        if s[5] and 'Old landmines' in b.texts.get(s[5], '') and (i == 0 or st[i-1][5] != s[5]): blows.append(s[0])
        if s[0] == n[0] or s[0] % 6 != 5: continue
        m, L = s[0], s[4][IDX['level']]
        if L not in R.THRESH: continue
        thr = R.THRESH[L]
        nt = b.texts.get(n[5], '') if n[5] else ''
        gm = re.search(r'performance bonus \(([SABCD])\)', nt) or re.search(r'\b([SABCD]) grade', nt)
        grade = gm.group(1) if gm else '?'
        promoted = n[4][IDX['level']] > L
        last = s[4]
        sk, nw, ou, dg = last[IDX['skill']], last[IDX['network']], last[IDX['output']], last[IDX['dignity']]
        if not (sk >= thr[0] and nw >= thr[1] and dg >= 4): continue
        inwin = any(m - 5 <= x <= m + 1 for x in blows) or bool(n[5] and 'Old landmines' in b.texts.get(n[5], ''))
        before = [x for x in blows if x < m - 5]
        gap = (thr[2] - ou)
        k = ('blow_in_win' if inwin else ('blow_before' if before else 'no_blow'),
             'O_ok' if ou >= thr[2] else 'O_low', 'L%d' % L, grade, 'PROM' if promoted else 'no')
        tab[k] += 1
        if ou < thr[2] and promoted: ex[k].append((g['g'], m, before, ou, thr[2], [x[4][IDX['output']] for x in st[:i+1] if x[1]=='e' and x[0] > m-12]))
for k, v in sorted(tab.items()): print(v, k)
for k, v in ex.items():
    print(k, len(v))
    for e in v[:4]: print('   ', e)
