import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open(sys.argv[2])))
b=Batch(sys.argv[1]); bad=collections.Counter(); seen=collections.Counter(); mism=collections.Counter()
nobs={}
for nid,n in cat.nodes.items():
    for k,c in n['choices'].items(): nobs[f'E|{nid}|{k}']=c['n']
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    R=0; month_keys=[]
    for i,(s,e,a) in enumerate(r[1]):
        t=b.texts.get(s[5],'') if s[5] else ''
        h=replica.hr_level(t)
        if h is not None:
            if h<4 or R<4:
                d=(h-R) if h<4 else (4-R if R<4 else 0)
                mism[d]+=1
                for k in month_keys:
                    seen[k]+=1
                    if d!=0: bad[k]+=1
            if h<4: R=h
            month_keys=[]
        if 'Old landmines' in t: R=0
        k=replica.key(s,e); month_keys.append(k)
        R=max(0,R+replica.step_risk(cat,s,e))
print('monthly residual (obs-pred):',sorted(mism.items()))
rows=sorted(((bad[k]/seen[k],seen[k],k,nobs.get(k)) for k in seen if seen[k]>=4), reverse=True)[:15]
for x in rows: print(round(x[0],2),x[1],x[2][:40],'catalog n=',x[3], 'risk=',cat.risk.get(x[2],0))
