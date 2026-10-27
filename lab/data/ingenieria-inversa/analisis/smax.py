import sys, json, collections, re
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v1.json'))); rep=replica.Replica(cat)
c=collections.Counter(); ex=[]
for bn in sys.argv[1].split(','):
  b=Batch(bn)
  for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; R=0
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        if i>0 and s[0]!=out[i-1][0][0] and 'Half-year talk' in t:
            ps,pe,_=out[i-1]; st=replica.obs_state(ps[4],ps[0]); replica.decide_apply(rep,st,ps,pe)
            gr=re.search(r'bonus \((\w)\)',t).group(1)
            caps=[st.skill>=replica.cap(st.level,'skill'),st.network>=replica.cap(st.level,'network'),st.output>=replica.cap(st.level,'output')]
            key=(st.level, sum(caps), st.dignity>=10, st.health>=9, R==0, gr)
            c[key]+=1
            if sum(caps)==3 and st.dignity>=10 and R==0 and len(ex)<10: ex.append((g['g'],s[0],st.level,st.skill,st.network,st.output,st.health,st.dignity,ps[4][5],gr))
        h=replica.hr_level(t)
        if h is not None and h<4: R=h
        if 'Old landmines' in t: R=0
        R=max(0,R+replica.step_risk(cat,s,e))
for k in sorted(c):
    if k[1]>=2: print(k,c[k])
for x in ex: print(x)
