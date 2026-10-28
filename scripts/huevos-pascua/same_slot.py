"""Respuestas con continuacion 'en el mismo mes': segun su plaza en el mes (1.a, 2.a, 3.a), llega la
continuacion?, se corta la historia?, vuelve a salir el titulo despues?

Uso: BB_DATA=<dir> python3 same_slot.py lote[,lote]
"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
from bbdata import Batch
cat = json.load(open(os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa', 'catalog_v2.json')))
N = cat['nodes']
b = Batch(*sys.argv[1].split(','))
tab = collections.Counter()
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    ev = [(s[0], s[2], s[3]) for s in g['steps'] if s[1] == 'e']
    last_month = g['steps'][-1][0]
    slot = []; cur = None; k = 0
    for m, n, c in ev:
        k = k + 1 if m == cur else 1; cur = m; slot.append(k)
    for i, (m, n, c) in enumerate(ev):
        ch = (N.get(n) or {}).get('choices', {}).get(str(c)) or {}
        if ch.get('when') != 'same': continue
        nx = ch['next']
        nxt_same = i + 1 < len(ev) and ev[i + 1][0] == m and ev[i + 1][1] == nx
        nxt_later = any(x[1] == nx for x in ev[i + 1:])
        title = N[n]['title']
        again = any(N.get(x[1], {}).get('title') == title and x[1] in cat['first_node'].values() for x in ev[i + 1:])
        tab[(slot[i], 'cont mismo mes' if nxt_same else ('cont despues' if nxt_later else 'sin cont'),
             'titulo repetido' if again else '-', 'vive>=+6m' if last_month >= m + 6 else 'muere pronto')] += 1
for k, v in sorted(tab.items()): print(v, k)
