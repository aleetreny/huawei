import tl, collections, sys
b=tl.Batch(*sys.argv[1].split(','))
mx=collections.defaultdict(lambda: collections.Counter()); n=0
for g in b.games():
    for s in g["steps"]:
        lv=s[4][4]; key=(lv,s[0])
        for st in ("skill","network","output"):
            mx[(st,lv,s[0])][s[4][tl.IDX[st]]]+=1
    n+=1
    if n>=int(sys.argv[2]): break
for k in sorted(mx):
    c=mx[k]; vals=sorted(c)
    print(k, 'max',vals[-1], 'top:', [(v,c[v]) for v in vals[-4:]], 'n',sum(c.values()))
