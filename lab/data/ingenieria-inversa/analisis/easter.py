import sys, json, collections, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
B=['b00-random-safe','b01-oracle-eps','c01-greedy-real','c02-planner-real','v02-validation','h01-l6hunt']
b=Batch(*B)
lv_title=collections.defaultdict(collections.Counter)     # title -> level counts (first step)
lv_total=collections.Counter()
state_title=collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
state_total=collections.defaultdict(collections.Counter)
big=[]; month_skill=collections.Counter(); chain_tot=collections.defaultdict(list)
def bins(v):
    return {'H':'lo' if v[0]<=3 else 'hi','D':'lo' if v[1]<=3 else 'hi','W':'neg' if v[7]<0 else ('rich' if v[7]>=20 else 'mid'),'dur':'long' if v[5]>=12 else 'short'}
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    seen=set(); ms=collections.defaultdict(float); cur=collections.defaultdict(lambda: collections.Counter())
    first_month_state={}
    for s,e,a in r[1]:
        if s[1]!='e': 
            ms[s[0]]+=e['d'].get('skill',0); continue
        t=e['title']
        ms[s[0]]+=e['d'].get('skill',0)
        for k,v in e['d'].items(): cur[t][k]+=v
        if any(c=='E' for c,_ in a): chain_tot[t].append(dict(cur[t])); cur[t]=collections.Counter()
        if t not in seen:
            seen.add(t); L=s[4][4]; lv_title[t][L]+=1; lv_total[L]+=1
            for k,v in bins(s[4]).items(): state_title[t][k][v]+=1; state_total[k][v]+=1
        tot=sum(abs(x) for x in e['d'].values())
        if tot>=8: big.append((tot,e['title'][:50],e['chosen'][:40],e['delta_line'],s[4][4]))
    for m,v in ms.items(): month_skill[min(int(v),12)]+=1
print('== titles only at high levels (never seen below L4)')
for t,c in sorted(lv_title.items(), key=lambda x:-sum(x[1].values())):
    if min(c)>=4: print(dict(sorted(c.items())), t[:70])
print('== titles first appearing at L2/L3 (not L1)', sum(1 for t,c in lv_title.items() if min(c) in (2,3)))
print('== level pools (distinct titles drawn per level):', {L:sum(1 for t,c in lv_title.items() if c.get(L)) for L in sorted(lv_total)})
print('== state-dependent titles (share in bin vs overall, bins with >=200 draws)')
for t,d in state_title.items():
    n=sum(d['H'].values())
    if n<150: continue
    for k,cc in d.items():
        for bn,cnt in cc.items():
            base=state_total[k][bn]/sum(state_total[k].values()); share=cnt/n
            if base>0.02 and (share>3*base or (share<base/5 and base>0.1)): print(t[:55],k,bn,'share',round(share,3),'base',round(base,3),'n',n)
print('== answers with total |effect| >= 8')
for x in sorted(set(big),reverse=True)[:15]: print(x)
print('== story totals (largest skill over a whole chain)')
best=sorted(((max(c.get('skill',0) for c in v),t) for t,v in chain_tot.items()),reverse=True)[:8]
for x in best: print(x)
print('== skill gained in a month (all decisions, nominal): distribution', sorted(month_skill.items()))
