"""Muestra pasos y registro oficial de una partida entre dos meses. Uso: show_game.py <game_id> <mes_ini> <mes_fin> [lote]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import tl
from bbdata import Batch, DATA
gid, m0, m1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
batches = sys.argv[4].split(',') if len(sys.argv) > 4 else sorted(p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
for bn in batches:
    b = Batch(bn)
    for g in b.games():
        if g['g'] != gid: continue
        r = tl.timeline(b, g)
        print('==', bn, gid, g.get('pol'), g['end'].get('q'))
        for s, e, a in r[1]:
            if not (m0 <= s[0] <= m1): continue
            print(f"m{s[0]} {s[1]} st={s[4]} -> #{s[3]} {(e or {}).get('title','')[:50]} | {(e or {}).get('chosen','')[:60]} | {(e or {}).get('delta_line','')}")
            for code, m in a:
                if code not in ('A',): print('     ', code, m[:220].replace('\n', ' / '))
