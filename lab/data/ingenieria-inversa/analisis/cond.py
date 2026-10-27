import sys, collections, json
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
d=json.load(open('/home/user/rx/sampler_v1.json'))
b=Batch('b01-oracle-eps','c01-greedy-real','c02-planner-real','v02-validation','h01-l6hunt')
feat=lambda v,m:{'L>=4':v[4]>=4,'L>=5':v[4]>=5,'dur>=12':v[5]>=12,'dur>=7':v[5]>=7,'W>=10':v[7]>=10,'W>=20':v[7]>=20,'H>=7':v[0]>=7,'D>=8':v[1]>=8,'N>=30':v[3]>=30,'S>=90':v[2]>=90}
base=collections.defaultdict(lambda: collections.Counter()); tit=collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    seen=set()
    for s,e,a in r[1]:
        if s[1]!='e' or s[0]<30: continue
        t=e['title']
        f=feat(s[4],s[0])
        newdraw = t not in seen
        seen.add(t)
        if not newdraw: continue
        for k,v in f.items():
            base[k][v]+=1; tit[t][k][v]+=1
print('feature: overall share True among new draws (months>=30)')
for k in base: print(' ',k, round(base[k][True]/sum(base[k].values()),3))
rows=[]
for t,fk in tit.items():
    n=sum(fk['L>=4'].values())
    if n<100: continue
    devs={k:round(fk[k][True]/n - base[k][True]/sum(base[k].values()),3) for k in fk}
    k,v=max(devs.items(), key=lambda x:abs(x[1]))
    rows.append((abs(v),k,v,n,round(d['weight'][t],2),d['window'][t][0],t[:55]))
for x in sorted(rows,reverse=True)[:20]: print(x)
