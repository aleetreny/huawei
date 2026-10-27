import sys, json, collections, re
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json'))); rep=replica.Replica(cat)
b=Batch('b01-oracle-eps','b00-random-safe'); c=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    for i in range(1,len(out)):
        s=out[i][0]; ps,pe,_=out[i-1]
        t=b.texts.get(s[5],'') if s[5] else ''
        if s[0]==ps[0] or 'Half-year talk' not in t or 'Old landmines' in t or 'Payday' in t or 'nobody asks' in t: continue
        st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
        tone='warn' if any(x in t for x in replica.WARN_TONE) else ('praise' if any(x in t for x in replica.PRAISE_TONE) else 'neu')
        gm=re.search(r'bonus \((\w)\)',t).group(1)
        promo=s[4][4]>ps[4][4]; fast='climbed too fast' in t
        dd=s[4][1]-st.dignity
        if st.dignity>=9 and dd>=0: dd='cl'
        c[(tone,gm,promo,fast,'L%d'%ps[4][4],dd)]+=1
for k in sorted(c, key=str): print(k,c[k])
