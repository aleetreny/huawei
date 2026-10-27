import tl, collections, re, math
b=tl.Batch('b00-random-safe','b01-oracle-eps')
c=collections.Counter(); n=0; bad=[]
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    W=1.0; out=r[1]
    for i,(s,e,a) in enumerate(out):
        disp=s[4][7]
        diff=round(disp-W,3)
        c[('floor' if math.floor(W+1e-9)==disp else 'no')]+=1
        continue_=1# round(W)==disp else ('floor' if math.floor(W)==disp else ('trunc' if int(W)==disp else 'none')))]+=1
        if math.floor(W+1e-9)!=disp and len(bad)<8: bad.append((g['g'],s[0],s[1],disp,round(W,3),e['title'][:30],e['delta_line'][:50]))
        # apply the decision and following logs
        W+=e['d'].get('wealth',0)
        t_next=b.texts.get(out[i+1][0][5],'') if i+1<len(out) and out[i+1][0][5] else ''
        for m in re.findall(r'Monthly base salary: \+([\d.]+)',t_next): W+=float(m)
        for m in re.findall(r'performance bonus \(\w\): \+([\d.]+)',t_next): W+=float(m)
        if 'Old landmines' in t_next: W-=2
    n+=1
    if n>3000: break
print(c); print(bad)
