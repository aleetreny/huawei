import sys, json, collections, math
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','b00-random-safe'); c=collections.Counter(); n=0; fails=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; W=1.0; good=True; runA=runB=0; ok=True
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        st=replica.obs_state(s[4],s[0]); st.wealth=W
        replica.decide_apply(rep,st,s,e)
        if s2[0]!=s[0]:
            t=b.texts.get(s2[5],'') if s2[5] else ''
            pre=st.wealth; post=round(pre+replica.SALARY[st.level],1)
            runA=runA+1 if pre<0 else 0
            runB=runB+1 if post<0 else 0
            if ok: c[('pre',min(runA,6),'Payday' in t)]+=1; c[('post',min(runB,6),'Payday' in t)]+=1
            st.neg_wealth_months=99 # avoid replica's own debt penalty
            info=rep.month_change(st); st.dignity=s2[4][1]
            W=st.wealth
        else: W=st.wealth
        if math.floor(W+1e-9)!=s2[4][7]: ok=False; W=s2[4][7]+0.5
    fr=(g['final']['flags'].get('failure_reason') or '')
    if fr.startswith('Broke') and ok: fails[('broke runA',runA,'runB',runB)]+=1
    n+=1
    if n>6000: break
for k in sorted(c): print(k,c[k])
print(fails)
