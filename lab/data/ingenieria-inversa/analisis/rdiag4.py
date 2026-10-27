import tl, riskseq, json, collections, tags
b=tl.Batch('b00-random-safe','b01-oracle-eps')
d=json.load(open('/home/user/rx/riskd.json'))
allc=collections.Counter(); bad=collections.Counter()
for g in b.games():
    if g['outcome'] not in ('eliminated','completed'): continue
    r=tl.timeline(b,g)
    if r is None: continue
    R=0; prev=None
    for s,e,a in r[1]:
        t=b.texts.get(s[5],'') if s[5] else ''
        h=tags.hr(t)
        if h is not None:
            if prev is not None and h<4:
                key=(prev[0],prev[1])
                allc[key]+=1
                if h==R+1: bad[key]+=1
            if h<4: R=h
            prev=(s[0]-1, s[4][4]) # jump happened during previous month
            if 'Old landmines' in t: R=0
        elif 'Old landmines' in t: R=0
        R=max(0,R+d.get(riskseq.key(s,e),0))
for k in sorted(allc):
    if allc[k]>50: print(k, bad[k], allc[k], round(bad[k]/allc[k],3))
