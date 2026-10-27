import sys, collections, json, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
d=json.load(open('/home/user/rx/sampler_v1.json'))
b=Batch('b01-oracle-eps','c01-greedy-real','v02-validation','h01-l6hunt')
L=collections.defaultdict(list); span=collections.defaultdict(list)
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    st=collections.Counter(); m0={}
    for s,e,a in r[1]:
        if s[1]!='e': continue
        t=e['title']; st[t]+=1; m0.setdefault(t,s[0])
        if any(c=='E' for c,_ in a): L[t].append(st[t]); span[t].append(s[0]-m0[t])
rows=[(round(d['weight'][t],2), round(statistics.mean(L[t]),2), round(statistics.mean(span[t]),2), t[:50]) for t in L if t in d['weight'] and len(L[t])>30]
import numpy as np
w=np.array([r[0] for r in rows]); l=np.array([r[1] for r in rows]); sp=np.array([r[2] for r in rows])
print('corr weight~steps',round(np.corrcoef(w,l)[0,1],3),'corr weight~month span',round(np.corrcoef(w,sp)[0,1],3))
for r in sorted(rows)[:8]: print(r)
for r in sorted(rows)[-5:]: print(r)
