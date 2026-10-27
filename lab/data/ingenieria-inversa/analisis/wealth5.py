import tl, collections, re, math
b=tl.Batch('b00-random-safe','b01-oracle-eps')
n=0; ok=0; tot=0; firstbad=collections.Counter()
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    W=1.0; out=r[1]; bad=False; prev=None
    for i,(s,e,a) in enumerate(out):
        disp=s[4][7]; good= math.floor(W+1e-9)==disp
        tot+=1; ok+=good
        if not good and not bad:
            bad=True; firstbad[(prev, round(disp-W,2))]+=1
        W+=e['d'].get('wealth',0)
        info=[]
        for c,m in a:
            for x in re.findall(r'Monthly base salary: \+([\d.]+)',m): W+=float(x); info.append('sal')
            for x in re.findall(r'performance bonus \((\w)\): \+([\d.]+)',m): W+=float(x[1]); info.append('bonus'+x[0])
            if 'Old landmines' in m: W-=2; info.append('boom')
            if c=='E' and re.search(r'Wealth',m): info.append('E-wealth')
        prev=(s[1],tuple(info), e['d'].get('wealth',0))
    n+=1
    if n>3000: break
print(ok,tot, round(ok/tot,4))
for k,v in firstbad.most_common(15): print(v,k)
