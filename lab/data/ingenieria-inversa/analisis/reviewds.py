import tl, riskseq, replay, json, collections, tags, re, sys
TONE={'I had hopes':'warn','The room feels tense':'warn','HR marks the note':'warn','Your manager goes through':'neu','This half was neither':'neu','The feedback covers':'neu','Your manager closes':'praise','To be honest, I worried':'praise','The talk is shorter':'praise'}
def rows(batches, d):
    b=tl.Batch(*batches); out_rows=[]
    for g in b.games():
        if g['outcome'] not in ('eliminated','completed'): continue
        r=tl.timeline(b,g)
        if r is None: continue
        out=r[1]; R=0; nblow=0; grades=[]; promos=[]; sinceblow=99
        for i,(s,e,a) in enumerate(out):
            t=b.texts.get(s[5],'') if s[5] else ''
            h=tags.hr(t)
            if 'Half-year talk' in t and i>0:
                ps,pe,_=out[i-1]
                pre=replay.apply(ps[4],pe['d'],ps[4][4])
                tone=next((v for kk,v in TONE.items() if kk in t),'?')
                gm=re.search(r'bonus \((\w)\)',t)
                row=dict(g=g['g'],month=s[0],L=ps[4][4],dur=ps[4][5],H=pre[0],D=pre[1],S=pre[2],N=pre[3],O=pre[6],W=pre[7],R=R,
                         nblow=nblow,grade=gm.group(1) if gm else '?',tone=tone,promo=s[4][4]>ps[4][4],
                         prev=''.join(grades),blow_now='Old landmines' in t, hr=h, boom_recent=sinceblow)
                out_rows.append(row); grades.append(row['grade'])
                if 'I had hopes' in t or 'room feels tense' in t or 'HR marks the note' in t: R+=1
            if h is not None:
                if h<4: R=h
                sinceblow+=1
            if 'Old landmines' in t: R=0; nblow+=1; sinceblow=0
            R=max(0,R+d.get(riskseq.key(s,e),0))
    return out_rows
if __name__=='__main__':
    d=json.load(open('/home/user/rx/riskd.json'))
    rs=rows(sys.argv[1].split(','),d)
    json.dump(rs,open('/home/user/rx/reviews.json','w'))
    print(len(rs))
