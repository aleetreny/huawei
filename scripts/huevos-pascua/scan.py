"""Escaneo global de los lotes de bots en busca de mecanicas raras (huevos de Pascua).

Solo lee lo que devolvieron las herramientas oficiales en nuestras partidas (lab/data/ingenieria-inversa).
"""
import sys, os, json, glob, collections, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'data', 'ingenieria-inversa'))
from bbdata import Batch, promotion_of, DATA

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
print('batches', batches)
b = Batch(*batches)
print('nodes', len(b.nodes), 'texts', len(b.texts))
phase_nodes = collections.Counter(n['phase'] for n in b.nodes.values())
print('node phases', phase_nodes)
for n in b.nodes.values():
    if n['phase'] in ('energy', 'main_action', 'document', 'terminal'):
        print('  ', n['phase'], n['id'], n.get('title'), [c.get('action') for c in n['choices']])

flags = collections.Counter(); outcomes = collections.Counter(); codes = collections.Counter()
sysmsg = collections.Counter(); fixed = collections.Counter(); promo = collections.Counter(); fail = collections.Counter()
other = collections.Counter(); ngames = 0; jumps = []; lvl_at = collections.Counter()
for g in b.games():
    ngames += 1
    outcomes[g.get('outcome')] += 1
    fl = (g.get('final') or {}).get('flags')
    if fl is not None:
        flags[json.dumps(fl, sort_keys=True)[:300]] += 1
    prev = None
    for s in g['steps']:
        L = s[4][4]
        if prev is not None and L is not None and prev is not None and L - prev not in (0, 1):
            jumps.append((g['g'], s[0], prev, L))
        if L is not None: prev = L
    for code, t in b.log_entries(g):
        codes[code] += 1
        head = re.sub(r'\d+(\.\d+)?', '#', t[:90])
        if code == 'S': sysmsg[head] += 1
        elif code == 'F': fixed[head] += 1
        elif code == 'R':
            promo[head] += 1
            p = promotion_of(t)
            if p and p[1] - p[0] != 1: jumps.append((g['g'], 'log', t[:120]))
        elif code == 'X': fail[head] += 1
        elif code not in ('A', 'E', 'P', 'T', 'Z'): other[(code, head)] += 1
print('games', ngames, outcomes)
print('log codes', codes)
print('== flags (final)'); [print(v, k) for k, v in flags.most_common(30)]
print('== system msgs'); [print(v, k) for k, v in sysmsg.most_common(60)]
print('== fixed events'); [print(v, k) for k, v in fixed.most_common(60)]
print('== promotion msgs'); [print(v, k) for k, v in promo.most_common(30)]
print('== failure msgs'); [print(v, k) for k, v in fail.most_common(30)]
print('== other codes'); [print(v, k) for k, v in other.most_common(30)]
print('== level jumps != +1', len(jumps)); [print(j) for j in jumps[:30]]
