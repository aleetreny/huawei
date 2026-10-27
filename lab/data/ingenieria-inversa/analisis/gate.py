import sys, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import tl
from bbdata import Batch
b=Batch('b00-random-safe','b01-oracle-eps','c01-greedy-real','c02-planner-real','v02-validation','h01-l6hunt')
first=collections.defaultdict(collections.Counter)  # title -> (month bucket, level) counts
cell=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    seen=set()
    for s,e,a in r[1]:
        if s[1]!='e': continue
        t=e['title']
        mb=(s[0]-1)//6  # semester index
        key=(mb, min(s[4][4],4))
        cell[key]+=1
        if t not in seen:
            seen.add(t); first[t][key]+=1
early=[t for t,c in first.items() if sum(v for (mb,L),v in c.items() if mb==0)==0]
print('titles never drawn in semester 1:',len(early))
# for these titles: drawn by L1 players in later semesters? and by L2+ in semester 2?
rows=collections.Counter()
for t in early:
    for (mb,L),v in first[t].items(): rows[(mb,L)]+=v
for k in sorted(rows): print('semester',k[0]+1,'level',k[1],'draws of late titles',rows[k],'all event steps',cell[k], round(rows[k]/cell[k],4))
# minimum semester of each late title
mins=collections.Counter(min(mb for (mb,L) in first[t])+1 for t in early)
print('first semester seen for late titles:',sorted(mins.items()))
