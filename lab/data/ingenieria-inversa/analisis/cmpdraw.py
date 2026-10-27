import sys, json, collections, random, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open(sys.argv[2]))); p=json.load(open('/home/user/rx/h01kw.json'))['params']
smp=cat.d['sampler']; grp={t:w[0] for t,w in smp['window'].items()}
def summarize(games):  # games: list of list of (month,title) new draws
    n=len(games); per=collections.Counter(); bysem=collections.Counter(); tot=collections.Counter(); distinct=[]
    for seq in games:
        for m,t in seq: per[t]+=1; bysem[((m-1)//6, grp.get(t,'?'))]+=1; tot[(m-1)//6]+=1
        distinct.append(len(seq))
    return n, {t:v/n for t,v in per.items()}, {k:v/tot[k[0]] for k,v in bysem.items()}, statistics.mean(distinct)
real=[]
b=Batch(sys.argv[1])
for g in b.games():
    r=tl.timeline(b,g)
    if r is None or g['outcome']!='completed': continue
    seen=set(); seq=[]
    for s,e,a in r[1]:
        if s[1]=='e' and e['title'] not in seen: seen.add(e['title']); seq.append((s[0],e['title']))
    real.append(seq)
sim=[]; i=0
while len(sim)<len(real):
    st,tr=replica.play(cat,planner.Planner(**p),random.Random(50000+i)); i+=1
    if st.failure: continue
    seen=set(); seq=[]
    for x in tr:
        if x[1]=='e':
            t=cat.nodes[x[2]]['title']
            if t not in seen: seen.add(t); seq.append((x[0],t))
    sim.append(seq)
nr,pr,sr,dr=summarize(real); ns,ps,ss,ds=summarize(sim)
import numpy as np
T=sorted(set(pr)|set(ps)); a=np.array([pr.get(t,0) for t in T]); c=np.array([ps.get(t,0) for t in T])
print('completed games real',nr,'sim',ns)
print('distinct titles per game: real',round(dr,1),'sim',round(ds,1))
print('per-title draw rate per game: corr',round(np.corrcoef(a,c)[0,1],3),'mean abs diff',round(np.mean(np.abs(a-c)),3),'max abs diff',round(np.max(np.abs(a-c)),3))
print('share of draws by unlock block, per semester (real/sim):')
for sem in range(8):
    row=[]
    for g0 in (1,6,12,18,24,30):
        row.append(f"{g0}:{sr.get((sem,g0),0):.2f}/{ss.get((sem,g0),0):.2f}")
    print(' S%d'%(sem+1),' '.join(row))
