import sys, json, collections, re
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
b=Batch('v02-validation','c01-greedy-real','b01-oracle-eps'); inc=collections.defaultdict(list)
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        if s2[0]==s[0] or e['d'].get('wealth',0): continue
        t=b.texts.get(s2[5],'') if s2[5] else ''
        if any(x in t for x in ('Half-year','Old landmines','Payday')): continue
        # previous steps in same month without wealth change? require displayed before == displayed of first step of month
        inc[(s[4][4], s[1])].append(s2[4][7]-s[4][7])
for k in sorted(inc): print(k, len(inc[k]), round(sum(inc[k])/len(inc[k]),3), collections.Counter(inc[k]).most_common(3))
