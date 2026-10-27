import tl, collections, numpy as np, sys
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsqr
b=tl.Batch(*sys.argv[1].split(','))
rows=[]; 
keys={}
def key(s,e):
    if s[1]=='e': return ('E',s[2],s[3])
    return (s[1], e['chosen'])
for g in b.games():
    if g['outcome'] not in ('eliminated','completed'): continue
    nb=sum(1 for code,t in b.log_entries(g) if 'Old landmines' in t)
    if nb: continue
    R=g['end']['dims']['risk_control'][0]
    r=tl.timeline(b,g)
    if r is None: continue
    cnt=collections.Counter(key(s,e) for s,e,_ in r[1])
    rows.append((cnt,R,g))
    for k in cnt: keys.setdefault(k,len(keys))
print('games',len(rows),'params',len(keys))
A=lil_matrix((len(rows),len(keys))); y=np.zeros(len(rows))
for i,(cnt,R,g) in enumerate(rows):
    for k,v in cnt.items(): A[i,keys[k]]=v
    y[i]=R
sol=lsqr(A.tocsr(),y,damp=0.05)[0]
pred=A.tocsr()@sol
print('rmse',np.sqrt(np.mean((pred-y)**2)),'exact(rounded)',np.mean(np.round(pred)==y))
inv={v:k for k,v in keys.items()}
qa=[(k,sol[i]) for i,k in inv.items() if k[0]!='E']
for k,v in sorted(qa,key=lambda x:x[1]): print(k,round(v,2))
vals=np.array([sol[i] for i,k in inv.items() if k[0]=='E'])
print('story answer coef histogram', np.histogram(vals,bins=[-3,-1.5,-0.5,0.5,1.5,2.5,4])[0])
