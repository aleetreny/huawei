import sys, json, collections, re, numpy as np
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
cat=replica.Catalog(json.load(open('catalog_v1.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','c01-greedy-real'); rows=[]
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; ms={}
    for i,(s,e,a) in enumerate(out):
        if s[0] not in ms: ms[s[0]]=s[4]
        t=b.texts.get(s[5],'') if s[5] else ''
        if i>0 and s[0]!=out[i-1][0][0] and 'Half-year talk' in t and out[i-1][0][4][4]==4:
            ps,pe,_=out[i-1]; st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
            gr=re.search(r'bonus \((\w)\)',t).group(1)
            hist=[ms[m] for m in range(s[0]-6,s[0]) if m in ms]
            avg=np.mean([[h[2],h[3],h[6]] for h in hist],axis=0)
            rows.append(([st.skill,st.network,st.output,st.dignity,st.health,ps[4][5]]+list(avg)+[min(h[6] for h in hist)], gr))
X=np.array([r[0] for r in rows]); y=np.array([r[1] for r in rows]); m=np.isin(y,['A','B']); X=X[m]; y=y[m]
for name,cols in (('final S,N,O,D,H,dur',[0,1,2,3,4,5]),('avg S,N,O',[6,7,8]),('final O only',[2]),('avg O only',[8]),('final+avg',list(range(10)))):
    sc=cross_val_score(LogisticRegression(max_iter=5000,C=10),X[:,cols],y,cv=5).mean()
    print(name, round(sc,3))
print(collections.Counter(y))
