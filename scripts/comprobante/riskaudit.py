"""Per-decision risk audit of real games against the catalogue (research only)."""
import sys, json, collections, re
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'scripts'/'deepseek')); sys.path.insert(0,str(REPO/'scripts'/'ingenieria-inversa'))
import real_audit as A
import replica as R
sys.path.insert(0,str(Path(__file__).resolve().parent))
import traj as T
def my_decisions(path):
    order=T.load(str(Path(path).parent))
    obs=None
    for it in order:
        if it[0]=='obs': obs=it[1]
        elif 'take_action' in (it[1] or '') and obs:
            if len(obs.get('choices') or [])>1 and not (obs.get('current_event') or {}).get('title','').startswith('Quarterly'):
                yield obs, it[2].get('choice'), it[2].get('notes','') or ''
            obs=None
A.decisions=my_decisions
def fmt(d):
    return ' '.join(f"{k[0].upper()}{v:+g}" for k,v in d.items() if v)
mode=sys.argv[1]; paths=sys.argv[2:]
if mode=='detail':
    for p in paths:
        print('####',Path(p).parent.name)
        for st,opts,ch,best,val,note in A.rows(p):
            risks={k:r for k,(d,r) in opts.items()}
            if max(risks.values())<=0 and False: continue
            s=f"m{st.month:02d} L{st.level} | "
            s+=' || '.join(f"{'>>' if k==ch else '  '}{k}:{fmt(d)} R{r:+d} v{val[k]:.1f}" for k,(d,r) in sorted(opts.items()))
            print(s, '| note:', note[-60:].replace('\n',' '))
elif mode=='risky':
    # chosen risk>0 while an option with risk<=0 existed: what did the note say?
    rows=[]
    for p in paths:
        for st,opts,ch,best,val,note in A.rows(p):
            d,r=opts[ch]; minr=min(rr for _,rr in opts.values())
            if r>0 and minr<=0:
                rows.append((Path(p).parent.name[14:22],st.month,st.level,r,minr,[(k,fmt(dd),rr) for k,(dd,rr) in sorted(opts.items())],ch,note[-70:].replace('\n',' ')))
    print(len(rows),'risky picks with a safe alternative')
    for row in rows: print(row)
elif mode=='blowups':
    for p in paths:
        ev=[json.loads(l) for l in open(p)]
        n=0; months=[]
        for e in ev:
            pl=e.get('payload') or {}
            s=pl.get('result') or ''
            if isinstance(s,str) and 'landmines all go off' in s:
                m=re.search(r'"current_month":(\d+)',s)
                mm=int(m.group(1)) if m else -1
                if mm not in months: months.append(mm)
        print(Path(p).parent.name[14:22], 'blow-ups at months', months)
