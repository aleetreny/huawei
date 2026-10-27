import tl, collections, re, math
b=tl.Batch('b00-random-safe','b01-oracle-eps')
c=collections.Counter(); n=0; ok=0; tot=0
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    W=1.0; out=r[1]; prevgood=True; previnfo=None
    for i,(s,e,a) in enumerate(out):
        disp=s[4][7]; good= math.floor(W+1e-9)==disp
        tot+=1; ok+=good
        if prevgood and not good and previnfo: c[(previnfo, round(disp-W,2))]+=1
        if not good: W=disp+0.5  # resync roughly
        prevgood=good
        W+=e['d'].get('wealth',0)
        t_next=b.texts.get(out[i+1][0][5],'') if i+1<len(out) and out[i+1][0][5] else ''
        info=[]
        for m in re.findall(r'Monthly base salary: \+([\d.]+)',t_next): W+=float(m); info.append('sal')
        for m in re.findall(r'performance bonus \((\w)\): \+([\d.]+)',t_next): W+=float(m[1]); info.append('bonus'+m[0])
        if 'Old landmines' in t_next: W-=2; info.append('boom')
        if e['d'].get('wealth'): info.append('dw%+g'%e['d']['wealth'])
        previnfo=(s[1],)+tuple(info)
    n+=1
    if n>3000: break
print(ok,tot)
for k,v in c.most_common(25): print(v,k)
