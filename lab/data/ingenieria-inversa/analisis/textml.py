import sys, json, collections, numpy as np, hashlib
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
from bbdata import Batch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.model_selection import GroupKFold
cat=json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json'))
b=Batch('b01-oracle-eps','h01-l6hunt')  # node texts
rows=[]
for nid,n in cat['nodes'].items():
    meta=b.nodes.get(nid)
    if not meta: continue
    acts={c['choice']:c.get('action','') for c in meta.get('choices') or []}
    for k,ch in n['choices'].items():
        txt=acts.get(int(k))
        if not txt: continue
        rows.append((n['title'], txt, ch['d'], cat['risk'].get(f'E|{nid}|{k}',0)))
print('answers with text',len(rows))
texts=[r[1] for r in rows]; groups=[r[0] for r in rows]
vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True)
Xt=vec.fit_transform(texts)
gkf=GroupKFold(n_splits=5)
def cv_reg(yv):
    pred=np.zeros(len(yv))
    for tr,te in gkf.split(Xt,yv,groups):
        m=Ridge(alpha=1.0).fit(Xt[tr],yv[tr]); pred[te]=m.predict(Xt[te])
    return 1-np.sum((pred-yv)**2)/np.sum((yv-yv.mean())**2), np.corrcoef(pred,yv)[0,1]
for stat in ('skill','network','output','dignity','health','wealth'):
    yv=np.array([r[2].get(stat,0) for r in rows],float)
    r2,c=cv_reg(yv); print(f'{stat:8s} held-out-title R2 {r2:.2f} corr {c:.2f}')
yr=np.array([r[3] for r in rows],float); r2,c=cv_reg(yr); print(f'risk     held-out-title R2 {r2:.2f} corr {c:.2f}')
# risky (>0) vs not classification
yb=(yr>0).astype(int); acc=[]
for tr,te in gkf.split(Xt,yb,groups):
    m=LogisticRegression(max_iter=3000,C=3).fit(Xt[tr],yb[tr]); acc.append(np.mean(m.predict(Xt[te])==yb[te]))
print('risky-or-not accuracy on held-out titles',round(np.mean(acc),3),'base rate',round(1-yb.mean(),3))
m=Ridge(alpha=1.0).fit(Xt,yr); fn=np.array(vec.get_feature_names_out()); co=m.coef_
print('words raising hidden risk:',list(fn[np.argsort(-co)[:30]]))
print('words lowering hidden risk:',list(fn[np.argsort(co)[:30]]))
