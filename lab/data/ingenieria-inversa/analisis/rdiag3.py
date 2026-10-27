import tl, riskseq, json, collections, tags
b=tl.Batch('b00-random-safe','b01-oracle-eps')
d=json.load(open('/home/user/rx/riskd.json'))
feat_all=collections.Counter(); feat_bad=collections.Counter(); n=0
for g in b.games():
    if g['outcome'] not in ('eliminated','completed'): continue
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]; R=0; prev_ok=True; month_feats=set(); 
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        h=tags.hr(t)
        if h is not None:
            ok=(R==h) if h<4 else R>=4
            fs=month_feats
            for f in fs: feat_all[f]+=1
            if prev_ok and not ok and h==R+1:
                for f in fs: feat_bad[f]+=1
            prev_ok=ok
            if h<4: R=h  # resync
            month_feats=set(tags.tags(t))|{'m%3=='+str(s[0]%3)}
            month_feats|={'wneg' if s[4][7]<0 else 'wpos', 'L%d'%s[4][4], 'net0' if s[4][3]==0 else 'netpos', 'h<=2' if s[4][0]<=2 else 'h>2','dig<=3' if s[4][1]<=3 else 'dig>3'}
            if 'Old landmines' in t: R=0
        elif 'Old landmines' in t: R=0
        R=max(0,R+d.get(riskseq.key(s,e),0))
        if s[1]=='e' and any(c=='E' for c,_ in a): month_feats.add('completed_story')
    n+=1
for f in sorted(feat_all, key=lambda f: -feat_bad[f]/max(1,feat_all[f])):
    print(f, feat_bad[f], feat_all[f], round(feat_bad[f]/feat_all[f],3))
