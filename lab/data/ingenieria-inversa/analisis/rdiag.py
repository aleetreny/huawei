import riskseq, json, numpy as np, collections
G=riskseq.load(['b00-random-safe','b01-oracle-eps'])
d=json.load(open('/home/user/rx/riskd.json'))
def shift(seq):
    # move each ('O',h) [and following B at month start] before the previous K token
    out=list(seq); i=0
    res=[]
    for tok in seq:
        if tok[0]=='O' and res and res[-1][0]=='K':
            last=res.pop(); res.append(tok); res.append(('_PENDING',last))
        elif tok[0]=='B' and res and res[-1][0]=='_PENDING':
            p=res.pop(); res.append(tok); res.append(p)
        else:
            res.append(tok)
    return [('K',t[1][1]) if t[0]=='_PENDING' else t for t in res]
for name,GG in (('orig',G),('hr_before_3rd',[(shift(s),y) for s,y in G])):
    errs=[riskseq.loss_game(s,y,d) for s,y in GG]
    print(name,'loss',sum(errs),'exact',np.mean(np.array(errs)==0))
