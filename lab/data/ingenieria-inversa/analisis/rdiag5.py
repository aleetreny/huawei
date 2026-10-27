import tl, riskseq, json, collections, tags, re
b=tl.Batch('b00-random-safe','b01-oracle-eps')
d=json.load(open('/home/user/rx/riskd.json'))
c=collections.Counter()
TONE={'I had hopes':'warn','The room feels tense':'warn','HR marks the note':'warn','Your manager goes through':'neu','This half was neither':'neu','The feedback covers':'neu','Your manager closes':'praise','To be honest, I worried':'praise','The talk is shorter':'praise'}
CUSH=('senior colleague','mentor texts','old hand','diligent peer','After standup')
for g in b.games():
    if g['outcome'] not in ('eliminated','completed'): continue
    r=tl.timeline(b,g)
    if r is None: continue
    R=0; pend=None
    for s,e,a in r[1]:
        t=b.texts.get(s[5],'') if s[5] else ''
        h=tags.hr(t)
        if h is not None:
            if pend is not None and h<4 and pend[-1]<4:
                c[pend[:-1]+(h-R,)]+=1
            pend=None
            if 'Half-year talk' in t and h<4:
                tone=next((v for k,v in TONE.items() if k in t),'?')
                cu=any(x in t for x in CUSH)
                gr=re.search(r'bonus \((\w)\)',t); gr=gr.group(1) if gr else '?'
                pend=(s[0],'L%d'%s[4][4],tone,'cush' if cu else '-',gr,h)
            if h<4: R=h
            if 'Old landmines' in t: R=0
        elif 'Old landmines' in t: R=0
        R=max(0,R+d.get(riskseq.key(s,e),0))
for k in sorted(c): 
    if c[k]>=5: print(k,c[k])
