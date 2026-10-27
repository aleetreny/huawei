import tl, collections, tags, sys, numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsqr
b=tl.Batch(*sys.argv[1].split(','))
def key(s,e):
    if s[1]=='e': return 'E|'+s[2]+'|'+str(s[3])
    return s[1]+'|'+e['chosen']
rows=[]; keys={}
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    # month start HR: the HR text appears in events of first step of month m (m>=2)
    hr={}; blow=set()
    for s,e,a in out:
        t=b.texts.get(s[5],'') if s[5] else ''
        h=tags.hr(t)
        if h is not None and s[0] not in hr: hr[s[0]]=h
        if 'Old landmines' in t: blow.add(s[0])
    bymonth=collections.defaultdict(list)
    for s,e,a in out: bymonth[s[0]].append(key(s,e))
    for m in bymonth:
        if m in hr and m+1 in hr and hr[m]<4 and hr[m+1]<4 and m not in blow and (m+1) not in blow:
            cnt=collections.Counter(bymonth[m])
            rows.append((cnt,hr[m+1]-hr[m],hr[m],hr[m+1]))
            for k in cnt: keys.setdefault(k,len(keys))
print('rows',len(rows),'keys',len(keys))
A=lil_matrix((len(rows),len(keys))); y=np.array([r[1] for r in rows],float)
for i,(cnt,dy,h0,h1) in enumerate(rows):
    for k,v in cnt.items(): A[i,keys[k]]=v
A=A.tocsr()
# exclude rows where clipping at 0 may have happened: h1==0
mask=np.array([r[3]>0 for r in rows])
sol=lsqr(A[mask],y[mask],damp=0.01)[0]
pred=A@sol
res=pred-y
print('rmse (h1>0 rows)',np.sqrt(np.mean(res[mask]**2)),'rounded exact',np.mean(np.round(pred[mask])==y[mask]))
inv={v:k for k,v in keys.items()}
print('coef hist',np.histogram(sol,bins=[-5,-2.5,-1.5,-0.5,0.5,1.5,2.5,5])[0])
for i in np.argsort(sol)[:5]: print(inv[i][:60],round(sol[i],2))
for i,k in inv.items():
    if not k.startswith('E|'): print(k,round(sol[i],2))
np.save('/home/user/rx/hrsol.npy',sol); import json; json.dump(keys,open('/home/user/rx/hrkeys.json','w'))
