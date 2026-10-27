import tl, collections, replay, sys
b=tl.Batch(*sys.argv[1].split(',')); c=collections.Counter(); ex={}; n=0
IX=replay.IX
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    out=r[1]
    for i in range(len(out)-1):
        s,e,after=out[i]; s2=out[i+1][0]
        if s2[0]==s[0]: continue
        kinds=''.join(sorted(set(cc for cc,_ in after)))
        evt=b.texts.get(s2[5],'') if s2[5] else ''
        if 'Old landmines' in evt: kinds+='B'
        warn=[m[:25] for cc,m in after if cc=='warning']
        pred=replay.apply(s[4],e['d'],s[4][4])
        promo=s2[4][4]-s[4][4]
        diff=tuple((k,round(s2[4][ix]-pred[ix],2)) for k,ix in IX.items() if k!='wealth' and abs(s2[4][ix]-pred[ix])>1e-6)
        key=(kinds,promo,diff,tuple(warn))
        c[key]+=1; ex.setdefault(key,(g['g'],s[0],s[4],e['title'][:25],e['delta_line']))
    n+=1
    if n>=int(sys.argv[2]): break
tot=sum(c.values()); good=sum(v for k,v in c.items() if not k[2])
print('month transitions match',good,'/',tot)
for k,v in c.most_common(40):
    if k[2]: print(v,k,ex[k])
