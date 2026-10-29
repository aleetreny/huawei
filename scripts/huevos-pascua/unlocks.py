"""Busca eventos que solo aparecen si antes se eligio una respuesta concreta (desbloqueos ocultos).

Prueba de requisito: para cada titulo T y respuesta A (de otro titulo), P(A antes de T | T sale)
frente a P(A antes del mes de T) en partidas vivas en ese mes. Un requisito oculto daria ~1 frente a
algo menor. Tambien la prueba inversa (respuestas que impiden un titulo: P(A antes | T) ~ 0).
"""
import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
from bbdata import Batch, DATA

batches = sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
b = Batch(*batches)
title_of = {k: v.get('title') for k, v in b.nodes.items()}
rows = []
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    tm, am = {}, {}
    for s in g['steps']:
        if s[1] != 'e': continue
        tm.setdefault(title_of.get(s[2]), s[0]); am.setdefault((s[2], s[3]), s[0])
    rows.append((tm, am, g['steps'][-1][0]))
titles = sorted({t for tm, _, _ in rows for t in tm})
answers = sorted({a for _, am, _ in rows for a in am})
ti = {t: i for i, t in enumerate(titles)}; ai = {a: i for i, a in enumerate(answers)}
G = len(rows)
T = np.full((G, len(titles)), 99, np.int16); A = np.full((G, len(answers)), 99, np.int16); last = np.zeros(G, np.int16)
for gidx, (tm, am, l) in enumerate(rows):
    for t, m in tm.items(): T[gidx, ti[t]] = m
    for a, m in am.items(): A[gidx, ai[a]] = m
    last[gidx] = l
print('games', G, 'titles', len(titles), 'answers', len(answers))
an = (A < 99).sum(0)
res = []
for j, a in enumerate(answers):
    if an[j] < 20: continue
    Aj = A[:, j:j + 1]
    has_T = T < 99
    before = Aj < T                       # A elegida antes de que salga T
    cnt_T = has_T.sum(0)
    p_cond = (before & has_T).sum(0) / np.maximum(1, cnt_T)
    # base: partidas vivas al menos hasta la mediana del mes de T, A elegida antes de esa mediana
    for i, t in enumerate(titles):
        if title_of.get(a[0]) == t or cnt_T[i] < 30: continue
        med = int(np.median(T[has_T[:, i], i]))
        alive = last >= med
        base = ((A[alive, j] < med).sum()) / max(1, alive.sum())
        res.append((p_cond[i], base, cnt_T[i], t, title_of.get(a[0]), a[1], int(an[j])))
print('== posibles requisitos: P(A antes|T) >= 0.9 y base < 0.6')
for r in sorted(res, key=lambda r: r[1] - r[0]):
    if r[0] >= 0.9 and r[1] < 0.6: print(r)
print('== mayores diferencias P(A antes|T) - base')
for r in sorted(res, key=lambda r: r[1] - r[0])[:25]: print(round(r[0] - r[1], 3), r)
print('== posibles bloqueos: P(A antes|T) <= 0.01 y base > 0.1')
for r in sorted(res, key=lambda r: r[0] - r[1]):
    if r[0] <= 0.01 and r[1] > 0.1: print(r)
