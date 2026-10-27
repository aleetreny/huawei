import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json')))
b=Batch('b01-oracle-eps','c01-greedy-real','v02-validation','h01-l6hunt','v03-validation','c02-planner-real')
resid_months=collections.Counter(); all_months=collections.Counter()
lagcount=collections.defaultdict(lambda: collections.Counter()); lagall=collections.defaultdict(lambda: collections.Counter())
sign=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    R=0; hist=collections.defaultdict(list)
    for s,e,a in r[1]:
        t=b.texts.get(s[5],'') if s[5] else ''
        h=replica.hr_level(t)
        if h is not None and s[0]>1:
            if h<4 and R<4:
                res=h-R; sign[res]+=1
                for k in range(1,7):
                    for key in set(hist[s[0]-k]):
                        lagall[k][key]+=1
                        if res!=0: lagcount[k][(key,res)]+=1
                all_months[0]+=1; resid_months[0]+=int(res!=0)
            if h<4: R=h
        if 'Old landmines' in t: R=0
        if any(x in t for x in replica.WARN_TONE) and h is None: pass
        R=max(0,R+replica.step_risk(cat,s,e))
        if s[1]=='e': hist[s[0]].append(replica.key(s,e))
print('monthly HR residual distribution',sorted(sign.items()), 'rate', round(resid_months[0]/all_months[0],4))
base=resid_months[0]/all_months[0]
for k in range(1,7):
    rows=[]
    for (key,res),c in lagcount[k].items():
        n=lagall[k][key]
        if n>=40 and c/n>0.25: rows.append((round(c/n,2),n,res,cat.nodes.get(key.split('|')[1],{}).get('title','')[:45],key.split('|')[2]))
    rows.sort(reverse=True)
    print('lag',k,'months: answers followed by residual >25% (base',round(base,3),'):',len(rows)); [print('   ',x) for x in rows[:6]]
