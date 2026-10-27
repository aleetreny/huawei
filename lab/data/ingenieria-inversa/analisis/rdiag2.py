import riskseq, json, numpy as np, collections
G=riskseq.load(['b00-random-safe','b01-oracle-eps'])
d=json.load(open('/home/user/rx/riskd.json'))
pat=collections.Counter(); shown=0
for seq,y in G:
    R=0;n=0;trace=[];bad=False
    for typ,v in seq:
        if typ=='K':
            R=max(0,R+d.get(v,0)); trace.append(('k',d.get(v,0)))
        elif typ=='O':
            ok=(R==v) if v<4 else R>=4
            trace.append(('O',v,R,'' if ok else 'X'))
            if not ok:
                pat[(v,R)]+=1; bad=True
        else: n+=1; R=0; trace.append(('B',))
    if bad and shown<4:
        shown+=1; print(' '.join(str(t) for t in trace)[:1500]); print()
print(sorted(pat.items(),key=lambda x:-x[1])[:20])
