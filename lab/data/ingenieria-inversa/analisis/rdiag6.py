import tl, riskseq, json, collections, tags, re
b=tl.Batch('b00-random-safe','b01-oracle-eps')
d=json.load(open('/home/user/rx/riskd.json'))
c=collections.Counter(); ex=collections.Counter()
TONE={'I had hopes':'warn','The room feels tense':'warn','HR marks the note':'warn','Your manager goes through':'neu','This half was neither':'neu','The feedback covers':'neu','Your manager closes':'praise','To be honest, I worried':'praise','The talk is shorter':'praise'}
for g in b.games():
    if g['outcome'] not in ('eliminated','completed'): continue
    r=tl.timeline(b,g)
    if r is None: continue
    R=0; lastobs=None; monthkeys=[]
    for s,e,a in r[1]:
        t=b.texts.get(s[5],'') if s[5] else ''
        h=tags.hr(t)
        if h is not None:
            if lastobs is not None and h<4 and lastobs<4:
                tone=next((v for kk,v in TONE.items() if kk in t),"-"); c[(s[0],s[4][4],tone,h-R)]+=1
                if s[0]==5 and h-R==1:
                    for k in monthkeys: ex[k]+=1
            if h<4: R=h
            lastobs=h; monthkeys=[]
            if 'Old landmines' in t: R=0
        elif 'Old landmines' in t: R=0
        k=riskseq.key(s,e); monthkeys.append((s[1],e['title'][:40] if s[1]=='e' else e['chosen'], s[0]))
        R=max(0,R+d.get(k,0))
for m in (3,4,5,6,7,10,11,12):
    print(m,[(k[1:],v) for k,v in sorted(c.items()) if k[0]==m])
print(ex.most_common(15))
