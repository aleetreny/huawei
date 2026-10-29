"""Busca cambios de level, duration_in_level o energy que no expliquen el calendario.

Para cada paso de evento compara el estado antes y despues (siguiente paso del mismo mes) y
cuenta tokens raros en las lineas de efecto del registro oficial.
"""
import sys, os, re, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'data', 'ingenieria-inversa'))
from bbdata import Batch, DATA, IDX, parse_choice_entry
import tl

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
b = Batch(*batches)
tok = collections.Counter(); odd = collections.Counter(); ex = {}
dur_odd = collections.Counter(); lvl_odd = collections.Counter(); en_odd = collections.Counter()
for g in b.games():
    st = g['steps']
    for i in range(len(st) - 1):
        s, n = st[i], st[i + 1]
        if s[0] != n[0]:
            continue  # cambio de mes: lo explica el calendario
        a, z = s[4], n[4]
        if None in (a[IDX['level']], z[IDX['level']]): continue
        key = (s[1], s[2], s[3])
        if z[IDX['level']] != a[IDX['level']]:
            lvl_odd[key] += 1; ex.setdefault(('L',) + key, (g['g'], s[0], a, z))
        if z[IDX['duration_in_level']] != a[IDX['duration_in_level']]:
            dur_odd[key] += 1; ex.setdefault(('D',) + key, (g['g'], s[0], a, z))
        if s[1] == 'e' and z[IDX['energy']] != a[IDX['energy']]:
            en_odd[key] += 1; ex.setdefault(('E',) + key, (g['g'], s[0], a, z))
    for code, m in b.log_entries(g):
        if code in ('A', 'F', 'E') and 'Chose #' in m:
            e = parse_choice_entry(m)
            if not e: continue
            for w in re.findall(r'\b([A-Z][A-Za-z]+)\s[+-]\d', e['delta_line']):
                tok[w] += 1
        elif code == 'E':
            for w in re.findall(r'\b([A-Z][A-Za-z]+)\s[+-]\d', m):
                odd[w] += 1
print('tokens in delta lines', tok)
print('tokens in E entries', odd)
print('level changes inside a month', sum(lvl_odd.values()), lvl_odd.most_common(10))
print('duration changes inside a month', sum(dur_odd.values()), dur_odd.most_common(10))
print('energy changes after events', sum(en_odd.values()), en_odd.most_common(10))
for k, v in list(ex.items())[:15]: print(k, v)
