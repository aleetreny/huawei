"""Que decide si una continuacion 'del mismo mes' que no cabe pasa al mes siguiente o se descarta.

Para cada respuesta con continuacion en el mismo mes elegida en la ultima plaza del mes, cuenta
cuantas otras continuaciones quedan pendientes para el mes siguiente (respuestas del mismo mes con
continuacion 'next') y mira si la suya llega el mes siguiente o se pierde.
Uso: BB_DATA=<dir> python3 drop_rule.py lote[,lote]
"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
from bbdata import Batch
cat = json.load(open(os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa', 'catalog_v2.json')))
N = cat['nodes']
b = Batch(*sys.argv[1].split(','))
tab = collections.Counter(); first_in_next = collections.Counter(); per = collections.defaultdict(collections.Counter); bym = collections.defaultdict(collections.Counter)
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    ev = [(s[0], s[2], s[3]) for s in g['steps'] if s[1] == 'e']
    last = g['steps'][-1][0]
    bymonth = collections.defaultdict(list)
    for i, x in enumerate(ev): bymonth[x[0]].append(i)
    for m, idx in bymonth.items():
        if m + 1 > last or not bymonth.get(m + 1): continue
        i = idx[-1]; n, c = ev[i][1], ev[i][2]
        ch = (N.get(n) or {}).get('choices', {}).get(str(c)) or {}
        if ch.get('when') != 'same': continue
        others = 0
        for j in idx[:-1]:
            chj = (N.get(ev[j][1]) or {}).get('choices', {}).get(str(ev[j][2])) or {}
            if chj.get('when') == 'next': others += 1
        nxt_nodes = [ev[j][1] for j in bymonth[m + 1]]
        carried = ch['next'] in nxt_nodes
        tab[(others, 'pasa al mes siguiente' if carried else 'se descarta')] += 1
        if carried: first_in_next[nxt_nodes.index(ch['next'])] += 1
        per[(N[n]['title'][:55], n, c)][carried] += 1
        bym[m][carried] += 1
for k, v in sorted(tab.items()): print(v, k)
print('plaza que ocupa en el mes siguiente cuando pasa', sorted(first_in_next.items()))
print('== por respuesta: veces que pasa / que se descarta')
mixed = 0
for k, v in sorted(per.items(), key=lambda x: -sum(x[1].values())):
    if v[True] and v[False]: mixed += 1
print('respuestas', len(per), 'mixtas', mixed)
for k, v in sorted(per.items(), key=lambda x: -sum(x[1].values()))[:40]: print(v[True], v[False], k)
print('== por mes: pasa / se descarta')
for m in sorted(bym): print(m, bym[m][True], bym[m][False], round(bym[m][False] / max(1, sum(bym[m].values())), 2))
