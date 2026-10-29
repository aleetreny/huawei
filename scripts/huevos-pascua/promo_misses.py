"""Evaluaciones en las que la regla de ascenso (M12) falla, con su contexto.

Si existiera una combinacion oculta que adelanta un ascenso, apareceria aqui como
'ascenso no previsto' con algun evento o accion repetido en los meses anteriores.
Uso: python3 promo_misses.py [lote,lote,...]   (por defecto, todos)
"""
import sys, os, re, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import replica as R
import tl
from bbdata import Batch, DATA

batches = sys.argv[1].split(',') if len(sys.argv) > 1 else sorted(
    p.name for p in DATA.iterdir() if p.is_dir() and list(p.glob('games-*.jsonl.gz')))
CAT = os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa', 'catalog_v2.json')
cat = R.Catalog(json.load(open(CAT)))
b = Batch(*batches)
rep = R.Replica(cat, random.Random(1))
cases = []; conf = collections.Counter(); hist_all = collections.Counter(); hist_miss = collections.Counter()
n_rev = 0
for g in b.games():
    if g['outcome'] not in ('eliminated', 'completed'): continue
    r = tl.timeline(b, g)
    if r is None: continue
    out = r[1]
    Wlo = Whi = 1.0; Rk, nb = 0, 0; out_hist = {}; counters = (0, 0, 0); recent = []
    for i, (s, e, a) in enumerate(out):
        t = b.texts.get(s[5], '') if s[5] else ''
        if i == 0 or s[0] != out[i - 1][0][0]: out_hist.setdefault(s[0], s[4][6])
        h = R.hr_level(t)
        if h is not None and h < 4: Rk = h
        if 'Old landmines' in t: Rk, nb = 0, nb + 1
        st = R.obs_state(s[4], s[0]); W = (Wlo + Whi) / 2
        st.wealth, st.risk, st.blowups, st.out_hist = W, Rk, nb, dict(out_hist)
        st.neg_wealth_months, st.zero_net_months, st.low_dig_months = counters
        R.decide_apply(rep, st, s, e)
        e = e or {}
        lab = (s[1], e.get('title') if s[1] == 'e' else e.get('chosen'), s[3] if s[1] == 'e' else '')
        recent.append((s[0], lab))
        nxt = out[i + 1][0] if i + 1 < len(out) else None
        if nxt is not None and s[1] == 'e' and nxt[1] == 'q': st.energy = 3
        if nxt is not None and nxt[0] != s[0]:
            pre = dict(level=st.level, skill=st.skill, network=st.network, output=st.output, dignity=st.dignity,
                       health=st.health, dur=st.duration_in_level, risk=st.risk, blow=st.blowups)
            info = rep.month_change(st)
            if 'promoted' in info:
                n_rev += 1
                actual = nxt[4][4] > s[4][4]
                conf[(info['promoted'], actual)] += 1
                win = [lab for m, lab in recent if m > s[0] - 6]
                for lb in set(win): hist_all[lb] += 1
                if info['promoted'] != actual:
                    for lb in set(win): hist_miss[lb] += 1
                    nt = b.texts.get(nxt[5], '') if nxt[5] else ''
                    logs_after = ' '.join(m for ss, _, aa in out[max(0, i - 8):i + 2] if ss[0] in (s[0], s[0] + 1) for _, m in aa)
                    gm = re.search(r'performance bonus \(([SABCD])\)', logs_after)
                    cases.append(dict(g=g['g'], pol=g.get('pol'), month=s[0], pred=info['promoted'], real=actual,
                                      grade=info.get('grade'), real_grade=gm.group(1) if gm else None,
                                      blow_after_review='Old landmines' in logs_after, pre=pre,
                                      thr=R.THRESH.get(pre['level']), after=nxt[4], talk=nt[:300]))
        Rk = st.risk; counters = (st.neg_wealth_months, st.zero_net_months, st.low_dig_months)
        if nxt is not None:
            obs = list(nxt[4]); dw = st.wealth - W
            Wlo, Whi = max(Wlo + dw, obs[7] + R.DISP_LO), min(Whi + dw, obs[7] + R.DISP_HI)
            if Wlo > Whi + 1e-9: Wlo, Whi = obs[7] + R.DISP_LO, obs[7] + R.DISP_HI
print('reviews', n_rev, {f'pred={k[0]} real={k[1]}': v for k, v in conf.items()})
print('== casos que fallan')
for c in cases: print(json.dumps(c, ensure_ascii=False))
print('== decisiones sobrerrepresentadas en los 6 meses previos a un fallo (lift, n_fallo, n_total)')
nm = len(cases)
rows = []
for lb, k in hist_miss.items():
    tot = hist_all[lb]
    if k >= 2: rows.append((k / nm / (tot / n_rev), k, tot, lb))
for x in sorted(rows, reverse=True)[:25]: print(round(x[0], 1), x[1], x[2], x[3])
print('== clasificacion')
cl = collections.Counter()
for c in cases:
    if c['blow_after_review']: k = 'explosion justo despues de evaluar (la replica la aplica antes)'
    elif c['grade'] != c['real_grade']: k = 'nota mal prevista: replica %s, real %s' % (c['grade'], c['real_grade'])
    else: k = 'otro'
    cl[(k, c['pred'], c['real'])] += 1
for k, v in cl.most_common(): print(v, k)
for c in cases:
    if not c['blow_after_review'] and c['grade'] == c['real_grade']: print('OTRO', json.dumps(c, ensure_ascii=False)[:400])
