import tl, replay, tags, collections
b=tl.Batch('b00-random-safe','b01-oracle-eps')
c=collections.defaultdict(collections.Counter); fail=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; runs={'w':0,'n':0,'d':0}; 
    hist=[]
    for i in range(1,len(out)):
        s=out[i][0]; ps,pe,_=out[i-1]
        if s[0]==ps[0]: continue
        pre=replay.apply(ps[4],pe['d'],ps[4][4])
        t=b.texts.get(s[5],'') if s[5] else ''
        tg=set(tags.tags(t))
        # state at month advance = pre (approx)
        runs['w']=runs['w']+1 if pre[7]<0 else 0
        runs['n']=runs['n']+1 if pre[3]<=0 else 0
        runs['d']=runs['d']+1 if pre[1]<=1 else 0
        c['DEBT'][(min(runs['w'],6),'DEBT' in tg)]+=1
        c['ISOL'][(min(runs['n'],6),'ISOL' in tg)]+=1
        c['DIGNO'][(min(runs['d'],6),'DIGNO' in tg)]+=1
        c['SKILLB'][(s[0],ps[4][4],pre[2],'SKILLBEHIND' in tg)]+=1
    fr=(g['final']['flags'].get('failure_reason') or '')[:40]
    fail[(fr, 'w<0run%d'%runs['w'], 'n0run%d'%runs['n'], 'd<=1run%d'%runs['d'])]+=1
for k in ('DEBT','ISOL','DIGNO'):
    print(k, sorted(c[k].items()))
sk=c['SKILLB']; 
rows=collections.defaultdict(lambda:[0,0])
for (m,L,S,w),v in sk.items():
    rows[(m,L,S)][int(w)]+=v
print('SKILLBEHIND by month,L,skill (no,yes) where yes>0:')
for k in sorted(rows):
    if rows[k][1]>0: print(k,rows[k])
