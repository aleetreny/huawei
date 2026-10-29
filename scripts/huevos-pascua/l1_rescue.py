"""Evaluaciones en L1 por mes, tono del comentario de RR. HH. y si Skill/Network/Output llegaban al umbral.

Resultado (28 oct, 13 lotes): en los meses 6 y 12 la nota en L1 es siempre C; en el mes 18 (17 meses en
el nivel) es C, y se asciende, solo con el comentario 'smiling' (riesgo oculto 0); con cualquier otro
tono es D (168 de 168) y llega el despido. Uso: python3 scripts/huevos-pascua/l1_rescue.py
"""
import sys, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import tl
from bbdata import Batch, DATA, IDX

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
b = Batch(*batches)
tab = collections.defaultdict(collections.Counter); dig = collections.defaultdict(collections.Counter)
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    r = tl.timeline(b, g)
    if r is None: continue
    out = r[1]
    for i, (s, e, a) in enumerate(out):
        if s[0] % 6 != 5 or s[4][IDX['level']] != 1: continue
        nxt = out[i + 1][0] if i + 1 < len(out) else None
        if nxt is None or nxt[0] == s[0]: continue          # ultima decision antes de la evaluacion
        logs = ' '.join(m for ss, _, aa in out[max(0, i - 8):i + 2] if ss[0] in (s[0], s[0] + 1) for _, m in aa)
        gm = re.search(r'performance bonus \(([SABCD])\)', logs)
        hr = re.search(r'HR partner you get on with says,? (\w+)', logs)
        st = s[4]
        at_bar = st[IDX['skill']] >= 8 and st[IDX['network']] >= 3 and st[IDX['output']] >= 3
        key = (s[0] + 1, 'RRHH ' + (hr.group(1) if hr else '?'), 'en el umbral' if at_bar else 'por debajo')
        tab[key][(gm.group(1) if gm else '?', 'asciende' if nxt[4][IDX['level']] > 1 else 'no')] += 1
        if s[0] == 17: dig[st[IDX['dignity']]][gm.group(1) if gm else '?'] += 1
for k in sorted(tab): print(k, dict(tab[k]))
print('mes 18, nota por Dignity:', {k: dict(v) for k, v in sorted(dig.items())})
