import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, tl
from bbdata import Batch
cat=replica.Catalog(json.load(open('cat_test.json')))
b=Batch('b00-random-safe','b01-oracle-eps')
ms=collections.Counter(); det=collections.defaultdict(lambda:[0,0]); detR=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; R=0
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        h=replica.hr_level(t)
        newmonth = i>0 and s[0]!=out[i-1][0][0]
        blow='Old landmines' in t
        if newmonth:
            Rm=R + (1 if any(x in t for x in replica.WARN_TONE) else 0)
            ms[(min(Rm,9), blow and h is not None)]+=1
        elif i>0:
            # mid-month explosion right after previous answer
            pk=replica.key(out[i-1][0],out[i-1][1])
            if out[i-1][0][1]=='e':
                det[(pk, min(Rprev_before,6))][0]+=1; det[(pk,min(Rprev_before,6))][1]+=int(blow)
                detR[(min(Rprev_before,6),blow)]+=1
        if h is not None and h<4: R=h
        if blow: R=0
        Rprev_before=R
        R=max(0,R+replica.step_risk(cat,s,e))
print('month-start explosion by tracked R:')
for k in sorted(ms): print(k,ms[k])
print('mid-month explosion after an answer by R before answer:')
for k in sorted(detR): print(k,detR[k])
json.dump({f'{k}|{rb}':v for (k,rb),v in det.items()}, open('/home/user/rx/det_raw.json','w'))
