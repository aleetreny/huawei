import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json')))
b=Batch('b00-random-safe','b01-oracle-eps')
c=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; R=0
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        h=replica.hr_level(t); blow='Old landmines' in t
        newmonth = i>0 and s[0]!=out[i-1][0][0]
        if i>0 and not newmonth:
            c[(min(R,8), blow, out[i-1][0][1])]+=1
        if newmonth:
            pass
        if h is not None and h<4: R=h
        if blow: R=0
        R=max(0,R+replica.step_risk(cat,s,e))
for k in sorted(c): print(k,c[k])
