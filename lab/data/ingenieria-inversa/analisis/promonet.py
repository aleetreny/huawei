import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('catalog_v1.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','c01-greedy-real'); c=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    for i in range(1,len(out)):
        s=out[i][0]; ps,pe,_=out[i-1]
        t=b.texts.get(s[5],'') if s[5] else ''
        if s[0]==ps[0] or s[4][4]<=ps[4][4] or 'Old landmines' in t or 'nobody' in t: continue
        st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
        fast='climbed too fast' in t
        c[(ps[4][4],fast,"dur",ps[4][5],"tone",next((x for x in replica.PRAISE_TONE if x in t),"other"),s[4][3]-st.network)]+=1 if ps[4][4]>=4 else 0
for k in sorted(c): print(k,c[k])
