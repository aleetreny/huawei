"""Fit event sampling: per-title month window and weight (draws / exposure among eligible unused titles)."""
import sys, collections, json
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
b=Batch(*sys.argv[1].split(','))
games=[]
mn=collections.defaultdict(lambda:99); mx=collections.Counter(); cnt=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    seq=[]; seen=set()
    for s,e,a in r[1]:
        if s[1]!='e': continue
        t=e['title']
        if t not in seen:
            seen.add(t); seq.append((s[0],t)); mn[t]=min(mn[t],s[0]); mx[t]=max(mx[t],s[0]); cnt[t]+=1
    games.append(seq)
titles=list(cnt)
w={t:1.0 for t in titles}
for it in range(30):
    expo=collections.Counter()
    for seq in games:
        used=set()
        for m,t in seq:
            elig=[u for u in titles if mn[u]<=m<=mx[u] and u not in used]
            Z=sum(w[u] for u in elig)
            for u in elig: expo[u]+=w[u]/Z
            used.add(t)
    neww={t:cnt[t]/max(1e-9,expo[t])*w[t] for t in titles}
    s=sum(neww.values()); neww={t:v/s*len(titles) for t,v in neww.items()}
    delta=max(abs(neww[t]-w[t]) for t in titles); w=neww
    if delta<1e-3: break
print('iters',it,'titles',len(titles))
json.dump({'window':{t:[mn[t],mx[t]] for t in titles},'weight':w,'count':dict(cnt)},open(sys.argv[2],'w'))
ws=sorted(w.values()); print('weight min/med/max',round(ws[0],2),round(ws[len(ws)//2],2),round(ws[-1],2))
print('first-month distribution',sorted(collections.Counter(mn[t] for t in titles).items()))
