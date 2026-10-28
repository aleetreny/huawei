"""Resume juicios de judge.py: nota media y dispersion por archivo y modelo, subnotas y condiciones de 0.

Uso: python3 scripts/calidad-skills/summary.py lab/reports/calidad-skills/data/j01-calibracion.jsonl [...]
"""
import sys, json, collections, statistics as S

rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.strip()]
by = collections.defaultdict(list)
for r in rows:
    by[(r['file'], r['model'])].append(r)
files = sorted({r['file'] for r in rows}, key=lambda f: -S.mean(r['score'] for r in rows if r['file'] == f and r.get('ok')))
models = sorted({r['model'] for r in rows})
SUB = ('findable', 'description', 'executable', 'near_limit', 'rules_match', 'horizon', 'robustness', 'clarity')
print('| Archivo | palabras | ' + ' | '.join(f'{m} (media ± dt, min–max)' for m in models) + ' | ceros |')
print('|---|---:|' + '---:|' * len(models) + '---|')
for f in files:
    cells = []; zeros = collections.Counter(); words = None
    for m in models:
        rs = [r for r in by[(f, m)] if r.get('ok')]
        if not rs: cells.append('—'); continue
        words = rs[0]['words']
        sc = [r['score'] for r in rs]
        cells.append(f"{S.mean(sc):.1f} ± {S.pstdev(sc):.1f} ({min(sc)}–{max(sc)})")
        for r in rs:
            for z in r.get('zero_conditions') or []: zeros[f"{m}:{z.get('type')}"] += 1
    short = f.replace('lab/policies-src/', '').replace('/bundle/skills/', ' → ').replace('/SKILL.md', '').replace('lab/reports/calidad-skills/', '')
    print(f"| {short} | {words} | " + ' | '.join(cells) + f" | {dict(zeros) or ''} |")
print()
print('Subnotas medias (todos los modelos):')
print('| Archivo | ' + ' | '.join(SUB) + ' |'); print('|---|' + '---:|' * len(SUB))
for f in files:
    rs = [r for r in rows if r['file'] == f and r.get('ok') and r.get('sub')]
    short = f.replace('lab/policies-src/', '').replace('/bundle/skills/', ' → ').replace('/SKILL.md', '').replace('lab/reports/calidad-skills/', '')
    print(f"| {short} | " + ' | '.join(f"{S.mean(float(r['sub'].get(k) or 0) for r in rs):.1f}" for k in SUB) + ' |')
bad = [r for r in rows if not r.get('ok')]
print(f'\nllamadas sin JSON valido: {len(bad)} de {len(rows)}')
