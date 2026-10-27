import sys, json, collections, math, re
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v1.json'))); rep=replica.Replica(cat)
b=Batch('v02-validation'); shown=0
for g in b.games():
    r=tl.timeline(b,g); out=r[1]
    lo=hi=1.0; hist=[]
    for i in range(len(out)-1):
        s,e,a=out[i]; s2=out[i+1][0]
        W=(lo+hi)/2
        st=replica.obs_state(s[4],s[0]); st.wealth=W; st.neg_wealth_months=-99
        replica.decide_apply(rep,st,s,e)
        if s2[0]!=s[0]: rep.month_change(st)
        dw=st.wealth-W
        sal=[m for c,m in a if c=='P']
        hist.append((s[0],s[1],s[4][4],'disp',s[4][7],'int',round(lo,2),round(hi,2),'dw',round(dw,3),'ans',e['d'].get('wealth',0),[x[:60].replace('\n',' ') for x in sal]))
        o=s2[4][7]
        if math.floor(st.wealth+1e-9)!=o and s2[0]!=s[0] and 'Half' not in (b.texts.get(s2[5],'') or ''):
            for h in hist[-8:]: print(h)
            print('  -> observed',o,'pred',st.wealth); print(); shown+=1; break
        lo,hi=max(lo+dw,o),min(hi+dw,o+0.99)
        if lo>hi: lo,hi=o,o+0.99
    if shown>=3: break
