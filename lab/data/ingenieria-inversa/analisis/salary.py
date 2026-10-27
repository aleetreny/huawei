import sys, json, collections, re
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
K=4
b=Batch('v02-validation','c01-greedy-real'); inc=collections.defaultdict(list)
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; first={}
    for s,e,a in out:
        first.setdefault(s[0],(s,e))
    months=sorted(first)
    # stretch of months where no step had wealth delta, no review, no blowup
    clean={}
    for s,e,a in out:
        t=b.texts.get(s[5],'') if s[5] else ''
        bad= e['d'].get('wealth',0)!=0 or 'Half-year' in t or 'Old landmines' in t or 'Payday' in t
        clean[s[0]]=clean.get(s[0],True) and not bad
    for m in months:
        if m+K in first and all(clean.get(x,False) for x in range(m,m+K)):
            L={first[x][0][4][4] for x in range(m,m+K+1)}
            if len(L)==1:
                inc[L.pop()].append((first[m+K][0][4][7]-first[m][0][4][7])/K)
for L in sorted(inc): print(L, len(inc[L]), round(sum(inc[L])/len(inc[L]),3))
