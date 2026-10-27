import sys, json, collections, re, numpy as np
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','c01-greedy-real','v02-validation','c02-planner-real'); rows=[]
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; ms={}; R=0; blows=[]; Rm={}
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        if s[0] not in ms: ms[s[0]]=s[4]; Rm[s[0]]=R
        if i>0 and s[0]!=out[i-1][0][0] and 'Half-year talk' in t and out[i-1][0][4][4] in (4,5):
            ps,pe,_=out[i-1]; st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
            gr=re.search(r'bonus \((\w)\)',t).group(1)
            hist=[ms[m] for m in range(s[0]-6,s[0]) if m in ms]
            avg=np.mean([[h[2],h[3],h[6],h[1],h[0]] for h in hist],axis=0)
            nb=sum(1 for m in blows if m>=s[0]-6)
            rmax=max(Rm.get(m,0) for m in range(s[0]-6,s[0]))
            rep4=4*st.dignity+st.health-8*R-16*sum(1 for m in blows); rows.append(([ps[4][4],st.skill,st.network,st.output,st.dignity,st.health,ps[4][5],R,nb,rmax,rep4]+list(avg)+[st.output-hist[0][6],st.skill-hist[0][2],st.network-hist[0][3]], gr))
        h=replica.hr_level(t)
        if h is not None and h<4: R=h
        if 'Old landmines' in t: R=0; blows.append(s[0])
        R=max(0,R+replica.step_risk(cat,s,e))
X=np.array([r[0] for r in rows],float); y=np.array([r[1] for r in rows])
print(collections.Counter(y), len(y))
for name,cols in (('final+risk',[0,1,2,3,4,5,6,7,8,9]),('final+rep',[0,1,2,3,6,10]),('final+risk+rep',[0,1,2,3,4,5,6,7,8,9,10])):
    for mname,m in (('LR',LogisticRegression(max_iter=5000,C=10)),('GB',GradientBoostingClassifier())):
        print(name,mname, round(cross_val_score(m,X[:,cols],y,cv=5).mean(),3))
from sklearn.tree import DecisionTreeClassifier, export_text
names=['L','S','N','O','D','H','dur','R','nb','rmax','rep4']
m=(y=='A')|(y=='B')
for d in (2,3,4):
    t=DecisionTreeClassifier(max_depth=d,min_samples_leaf=10).fit(X[m][:,[0,1,2,3,6,10]],y[m])
    print('depth',d,round(t.score(X[m][:,[0,1,2,3,6,10]],y[m]),4))
print(export_text(t,feature_names=[names[i] for i in [0,1,2,3,6,10]]))
print('--- per level linear')
for L in (2,3,4,5,6):
    mm=m&(X[:,0]==L)
    if mm.sum()<50 or len(set(y[mm]))<2: continue
    Xl=X[mm][:,[1,2,3,10,6]]; yl=y[mm]
    lr=LogisticRegression(max_iter=20000,C=100).fit(Xl,yl)
    co=lr.coef_[0]; print('L',L,'n',mm.sum(),'acc',round(lr.score(Xl,yl),4),'coef S,N,O,rep4,dur',np.round(co/co[3],3),'int',round(lr.intercept_[0]/co[3],2))
