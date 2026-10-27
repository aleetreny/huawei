import tl, collections, sys
b=tl.Batch(*sys.argv[1].split(','))
stat=sys.argv[3]; L=int(sys.argv[4])
c=collections.Counter(); n=0
for g in b.games():
    r=tl.timeline(b,g)
    if r is None: continue
    for k in range(len(r[1])-1):
        s,e,after=r[1][k]; s2=r[1][k+1][0]
        if s2[0]!=s[0] or s[4][4]!=L or s[1]!='e': continue
        kinds=''.join(sorted(set(cc for cc,_ in after)))
        pre=s[4][tl.IDX[stat]]; d=e["d"].get(stat,0); post=s2[4][tl.IDX[stat]]
        c[(pre,d,kinds,post)]+=1
    n+=1
    if n>=int(sys.argv[2]): break
for k in sorted(c): 
    if c[k]>=3: print(k,c[k])
