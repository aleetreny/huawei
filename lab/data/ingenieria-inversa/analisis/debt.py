import sys, json, collections, math
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','b00-random-safe'); c=collections.Counter(); n=0
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; W=1.0; good=True
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        st=replica.obs_state(s[4],s[0]); st.wealth=W
        replica.decide_apply(rep,st,s,e)
        if s2[0]!=s[0]:
            t=b.texts.get(s2[5],'') if s2[5] else ''
            pre=st.wealth
            post=round(pre+replica.SALARY[st.level],1)
            if good and 'Half-year' not in t and 'Old landmines' not in t:
                c[(round(pre,1) if -3<pre<3 else ('<-3' if pre<0 else '>3'), 'Payday' in t)]+=1
            st2=st; info=rep.month_change(st2)
            W=st2.wealth
        else:
            W=st.wealth
        good = math.floor(W+1e-9)==s2[4][7]
        if not good: W=s2[4][7]+0.5
    n+=1
    if n>5000: break
for k in sorted(c, key=lambda x:(str(type(x[0])),x)): print(k,c[k])
