"""Historias que vuelven a salir desde su primera pregunta dentro de una misma partida.

Para cada repeticion: respuesta dada la primera vez, si su continuacion llego antes de la repeticion,
y meses entre ambas. Uso: BB_DATA=<dir> python3 repeats.py lote[,lote]
"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
from bbdata import Batch
cat = json.load(open(os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa', 'catalog_v2.json')))
N = cat['nodes']; first = set(cat['first_node'].values())
b = Batch(*sys.argv[1].split(','))
tot = collections.Counter(); kinds = collections.Counter(); gaps = collections.Counter(); games = 0; reps_by_ans = collections.Counter()
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    games += 1
    seq = [(s[0], s[2], s[3]) for s in g['steps'] if s[1] == 'e']
    seen = {}
    for i, (m, n, k) in enumerate(seq):
        if n not in first: continue
        if n in seen:
            m0, k0, i0 = seen[n]
            ch = (N.get(n) or {}).get('choices', {}).get(str(k0)) or {}
            nx = ch.get('next')
            got = nx is not None and any(x[1] == nx for x in seq[i0 + 1:i])
            kinds[('tenia continuacion' if nx else 'sin continuacion', 'llego' if got else 'no llego', ch.get('when'))] += 1
            gaps[min((m - m0) // 6 * 6, 30)] += 1
            reps_by_ans[(N.get(n, {}).get('title', '')[:50], k0)] += 1
            tot['rep'] += 1
        seen[n] = (m, k, i)
print('partidas', games, 'repeticiones', tot['rep'], 'por partida', round(tot['rep'] / max(1, games), 3))
print('tipo', kinds.most_common())
print('meses entre una y otra (bloques de 6)', sorted(gaps.items()))
print('respuesta dada la primera vez', reps_by_ans.most_common(12))
