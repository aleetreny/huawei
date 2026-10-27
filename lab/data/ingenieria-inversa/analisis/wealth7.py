import tl, collections, re, math
b=tl.Batch('b00-random-safe','b01-oracle-eps')
n=0; ok=0; tot=0; firstbad=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    W=1.0; out=r[1]; bad=False; pend=0.0; prev=None
    for i,(s,e,a) in enumerate(out):
        t=b.texts.get(s[5],'') if s[5] else ''
        if i>0 and s[0]!=out[i-1][0][0]:
            W=round(W+pend,1); pend=0.0
        if 'Old landmines' in t: W-=2
        disp=s[4][7]; good= math.floor(W+1e-9)==disp
        tot+=1; ok+=good
        if not good and not bad:
            bad=True; firstbad[(prev, round(disp-W,2))]+=1
        W+=e['d'].get('wealth',0)
        for c,m in a:
            for x in re.findall(r'Monthly base salary: \+([\d.]+)',m): pend+=float(x)
            for x in re.findall(r'performance bonus \((\w)\): \+([\d.]+)',m): pend+=float(x[1])
        prev=(s[1],e['title'][:30],e['d'].get('wealth',0))
    n+=1
    if n>4000: break
print(ok,tot, round(ok/tot,4))
for k,v in firstbad.most_common(12): print(v,k)
