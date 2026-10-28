"""Analisis de un lote del explorador frente al catalogo v2 y a los lotes anteriores.

Uso: BB_DATA=~/careerlab-data/huevos-pascua python3 explore_report.py e01-explore
"""
import sys, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
from bbdata import Batch, parse_choice_entry, deltas, IDX
import tl

OLD = os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa')
cat = json.load(open(os.path.join(OLD, 'catalog_v2.json')))
N = cat['nodes']
b = Batch(*sys.argv[1].split(','))
games = list(b.games())
print('partidas', len(games), collections.Counter(g['outcome'] for g in games))
q = [g['end']['q'] for g in games if g['end'].get('q') is not None]
print('nota media', round(sum(q) / max(1, len(q)), 2), 'nivel final', collections.Counter(g['final']['s'][4] for g in games if g.get('final')))

# 1. cobertura y efectos de respuestas raras
obs = collections.defaultdict(collections.Counter)   # (node,k) -> delta_line counter
nxt = collections.defaultdict(collections.Counter)
new_nodes = collections.Counter(); level_in_month = []; codes = collections.Counter(); msgs = collections.Counter()
for g in games:
    r = tl.timeline(b, g)
    if r is None: continue
    out = r[1]
    for i, (s, e, a) in enumerate(out):
        if s[1] == 'e' and e:
            obs[(s[2], s[3])][e['delta_line']] += 1
            if s[2] not in N: new_nodes[(b.nodes.get(s[2], {}).get('title'), s[2])] += 1
            # siguiente paso de la misma historia
            for s2, e2, _ in out[i + 1:i + 8]:
                if s2[1] == 'e' and e2 and e2['title'] == e['title']:
                    nxt[(s[2], s[3])][s2[2]] += 1; break
        if i + 1 < len(out):
            s2 = out[i + 1][0]
            if s2[0] == s[0] and s2[4][IDX['level']] != s[4][IDX['level']]: level_in_month.append((g['g'], s[0]))
        for code, m in a:
            codes[code] += 1
            if code not in ('A', 'E', 'P', 'T'): msgs[(code, re.sub(r'\d+(\.\d+)?', '#', m[:80]))] += 1
print('cambios de nivel dentro de un mes', len(level_in_month))
print('preguntas nuevas (no estaban en el catalogo)', len(new_nodes)); [print('  ', v, k) for k, v in new_nodes.most_common(30)]
print('codigos de registro', codes)
old_msgs = set()
for code, m in msgs: pass
print('mensajes no de decision'); [print('  ', v, k) for k, v in msgs.most_common(40)]
rare_before = [(nid, int(k)) for nid, n in N.items() for k in range(1, n['n_choices'] + 1)
               if (n['choices'].get(str(k)) or {}).get('n', 0) < 30]
print('respuestas raras (<30) antes', len(rare_before), '; jugadas ahora', sum(1 for a in rare_before if obs.get(a)),
      '; con >=10 casos nuevos', sum(1 for a in rare_before if sum(obs.get(a, {}).values()) >= 10))
# efectos distintos del catalogo
diff = []
for (nid, k), c in obs.items():
    ch = (N.get(nid) or {}).get('choices', {}).get(str(k))
    lines = list(c)
    if ch is None:
        diff.append(('NUEVA', N.get(nid, {}).get('title') or b.nodes.get(nid, {}).get('title'), k, dict(c)))
    elif len(lines) > 1:
        diff.append(('VARIAS', N[nid]['title'], k, dict(c)))
    else:
        d = {kk: vv for kk, vv in deltas(lines[0]).items()}
        cd = {kk: vv for kk, vv in (ch.get('d') or {}).items() if vv}
        d = {kk: vv for kk, vv in d.items() if vv}
        if d != cd: diff.append(('DISTINTA', N[nid]['title'], k, lines[0], cd))
    if ch is not None and ch.get('next') and nxt.get((nid, k)) and set(nxt[(nid, k)]) != {ch['next']}:
        diff.append(('CONTINUACION', N[nid]['title'], k, dict(nxt[(nid, k)]), ch['next']))
print('respuestas con efecto o continuacion distinta/nueva', len(diff))
for d in diff[:60]: print('  ', d)
