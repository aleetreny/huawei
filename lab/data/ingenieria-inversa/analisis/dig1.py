import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps'); c=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        if s2[0]==s[0]: continue
        t=b.texts.get(s2[5],'') if s2[5] else ''
        if any(x in t for x in ('Half-year','Payday','Old landmines','nobody','self-respect')): continue
        st=replica.obs_state(s[4],s[0]); st.wealth=99; replica.decide_apply(rep,st,s,e)
        dd=s2[4][1]-st.dignity
        c[(dd, 'dig', st.dignity, 'H', st.health)]+=1 if dd else 0
for k,v in sorted(c.items(), key=lambda x:-x[1])[:20]: print(v,k)
