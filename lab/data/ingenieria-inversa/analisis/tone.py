import sys, json, collections, re, numpy as np
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import cross_val_score
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json'))); rep=replica.Replica(cat)
rows=[]; y=[]
for bn in ('b00-random-safe','b01-oracle-eps','c01-greedy-real','v02-validation','h01-l6hunt','v03-validation'):
  b=Batch(bn)
  for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; R=0; nb=0; hist={}; neg=0; sem_risk=0; sem_out_loss=0; sem_net_loss=0; ms={}
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        if s[0] not in ms: ms[s[0]]=s[4]
        if i>0 and s[0]!=out[i-1][0][0] and 'Half-year talk' in t:
            ps,pe,_=out[i-1]; st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
            gr=re.search(r'bonus \((\w)\)',t).group(1)
            if gr=='C':
                tone='warn' if any(x in t for x in replica.WARN_TONE) else 'neu'
                first=ms.get(s[0]-6, ms.get(1))
                rows.append([st.level,s[0],st.skill,st.network,st.output,st.dignity,st.health,R,nb,sem_risk,sem_out_loss,sem_net_loss,
                             st.skill-first[2],st.network-first[3],st.output-first[6],st.dignity-first[1],st.health-first[0],int(st.wealth<0)])
                y.append(tone)
            sem_risk=0; sem_out_loss=0; sem_net_loss=0
        h=replica.hr_level(t)
        if h is not None and h<4: R=h
        if 'Old landmines' in t: R=0; nb+=1
        dr=replica.step_risk(cat,s,e); R=max(0,R+dr); sem_risk+=max(0,dr)
        sem_out_loss+=min(0,e['d'].get('output',0)); sem_net_loss+=min(0,e['d'].get('network',0))
names=['L','month','S','N','O','D','H','R','nblow','semRiskAdded','semOutLoss','semNetLoss','dS','dN','dO','dD','dH','Wneg']
X=np.array(rows,float); y=np.array(y)
print(collections.Counter(y), len(y))
for d in (2,3,4,6):
    print('depth',d, round(cross_val_score(DecisionTreeClassifier(max_depth=d,min_samples_leaf=20),X,y,cv=5).mean(),3))
clf=DecisionTreeClassifier(max_depth=3,min_samples_leaf=20).fit(X,y); print(export_text(clf,feature_names=names))
from sklearn.linear_model import LogisticRegression
for cols in ([5,7],[5,7,9],[5,7,6],[5,7,8,9,6],[5,7,9,10,11,6,8],list(range(18))):
    m=LogisticRegression(max_iter=5000,C=10)
    sc=cross_val_score(m,X[:,cols],y,cv=5).mean(); m.fit(X[:,cols],y)
    print([names[c] for c in cols], round(sc,3), 'coef', np.round(m.coef_[0]/abs(m.coef_[0][0]),2), 'int', round(m.intercept_[0]/abs(m.coef_[0][0]),2))
# exact table D x R
tab=collections.defaultdict(collections.Counter)
for row,t in zip(rows,y): tab[(int(row[5]),min(int(row[7]),4))][t]+=1
print('D,R -> warn share')
for D in range(0,11):
    print(D, ' '.join(f"R{R}:{tab[(D,R)]['warn']}/{sum(tab[(D,R)].values())}" for R in range(5)))
import itertools
D=X[:,5]; H=X[:,6]; R=X[:,7]; B=X[:,8]; yy=(y=='warn')
best=[]
for a,bh,c,t in itertools.product([1.0],[0,0.2,0.25,0.3,1/3,0.5],[1,1.5,2,2.5,3],[3,4,5,6]):
    for thr in np.arange(3,9,0.25):
        pred=(D+bh*H-c*R-t*B)<thr
        best.append((np.mean(pred==yy),bh,c,t,thr))
best.sort(reverse=True)
for x in best[:8]: print(x)
