import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
B=['b00-random-safe','b01-oracle-eps','c01-greedy-real','v02-validation','h01-l6hunt','v03-validation']
b=Batch(*B)
first_variants=collections.defaultdict(set)
eff=collections.defaultdict(collections.Counter)
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    seen=set()
    for s,e,a in r[1]:
        if s[1]!='e': continue
        t=e['title']
        if t not in seen: seen.add(t); first_variants[t].add(s[2])
        eff[(s[2],s[3])][e['delta_line']]+=1
multi={t:v for t,v in first_variants.items() if len(v)>1}
print('(A) titles with more than one opening variant:',len(multi))
for t,v in list(multi.items())[:10]:
    print('  ',t[:60],[ (b.nodes[n].get('description') or '')[:70] for n in v])
var=[(k,c) for k,c in eff.items() if len(c)>1]
print('(C) answers with more than one effect line:',len(var),'of',len(eff))
for k,c in var[:8]: print('  ',b.nodes[k[0]].get('title','')[:40],k[1],dict(c.most_common(3)))
