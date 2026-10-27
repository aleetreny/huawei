import tl, collections, sys
b=tl.Batch(*sys.argv[1].split(','))
ST=["health","dignity","skill","network","output","wealth"]
res=collections.Counter(); ex={}
n=0
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    pre,out=r
    for k in range(len(out)-1):
        s,e,after=out[k]; s2=out[k+1][0]
        if s2[0]!=s[0]: continue  # same month only
        kinds=tuple(sorted(set(c for c,_ in after)))
        lv=s[4][4]
        diff=[]
        for st in ST:
            pred=s[4][tl.IDX[st]]+e["d"].get(st,0)
            diff.append(round(s2[4][tl.IDX[st]]-pred,2))
        key=(s[1],kinds,tuple(diff))
        res[key]+=1
        ex.setdefault(key,(g['g'],s,e['delta_line'],[(c,m[:120]) for c,m in after]))
    n+=1
    if n>=int(sys.argv[2]): break
for k,v in res.most_common(40): print(v,k, ex[k][2] if v<50 else '')
