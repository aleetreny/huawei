import sys, json, collections, math
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v1.json'))); rep=replica.Replica(cat)
b=Batch('v02-validation','c01-greedy-real'); c=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g); out=r[1]
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        if s2[0]!=s[0] or s[1]!='e': continue
        d=s2[4][7]-s[4][7]
        if d<=-3:
            pred=cat.effect(s[2],s[3])
            c[(e['title'][:45],e['chosen'][:35],s[4][4],e['delta_line'][:40],'catalog',json.dumps(pred),'obs',d)]+=1
for k,v in c.most_common(15): print(v,k)
