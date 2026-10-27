"""Integer hidden-risk fit with clipping at 0 and explosion handling, by coordinate descent."""
import tl, collections, sys, json, random
import numpy as np
def key(s,e):
    if s[1]=='e': return 'E|'+s[2]+'|'+str(s[3])
    return s[1]+'|'+e['chosen']
def load(batches, maxg=10**9):
    b=tl.Batch(*batches); G=[]
    for g in b.games():
        if g['outcome'] not in ('eliminated','completed'): continue
        fr=(g['final']['flags'].get('failure_reason') or '')
        if fr.startswith('Trust crisis'): continue
        r=tl.timeline(b,g)
        if r is None: continue
        seq=[]
        out=r[1]
        for i,(s,e,after) in enumerate(out):
            if i>0:
                t=b.texts.get(s[5],'') if s[5] else ''
                if 'Old landmines' in t: seq.append('BLOW')
                if out[i-1][0][0]!=s[0]: seq.append('MONTH')
            seq.append(key(s,e))
        nb=seq.count('BLOW')
        G.append((seq, g['end']['dims']['risk_control'][0], nb))
        if len(G)>=maxg: break
    return G
def sim(seq, d, mode, lo=0, hi=99, decay=0):
    R=0; n=0
    for k in seq:
        if k=='BLOW':
            n+=1
            if mode=='reset': R=0
            elif mode.startswith('minus'): R=max(lo,R-int(mode[5:]))
            continue
        if k=='MONTH':
            if decay: R=max(lo,R-decay)
            continue
        R=min(hi,max(lo,R+d.get(k,0)))
    return R+5*n
def fit(G, mode, iters=6, vals=range(-3,4), hi=99, decay=0, init=None):
    d=dict(init or {})
    idx=collections.defaultdict(list)
    for gi,(seq,y,nb) in enumerate(G):
        for k in set(seq):
            if k not in ('BLOW','MONTH'): idx[k].append(gi)
    err=np.array([(sim(seq,d,mode,hi=hi,decay=decay)-y)**2 for seq,y,nb in G],float)
    keys=list(idx); 
    for it in range(iters):
        random.Random(it).shuffle(keys); changed=0
        for k in keys:
            gs=idx[k]; cur=d.get(k,0); best=(err[gs].sum(),cur); 
            for v in vals:
                if v==cur: continue
                d[k]=v
                e=sum((sim(G[gi][0],d,mode,hi=hi,decay=decay)-G[gi][1])**2 for gi in gs)
                if e<best[0]-1e-9: best=(e,v)
            d[k]=best[1]
            if best[1]!=cur:
                changed+=1
                for gi in gs: err[gi]=(sim(G[gi][0],d,mode,hi=hi,decay=decay)-G[gi][1])**2
        exact=np.mean(err==0)
        print(mode,'iter',it,'changed',changed,'mse',err.mean().round(4),'exact',exact.round(4),flush=True)
        if changed==0: break
    return d,err
if __name__=='__main__':
    G=load(sys.argv[1].split(','))
    print('games',len(G), 'with blow', sum(1 for x in G if x[2]))
    for mode in sys.argv[2].split(','):
        d,err=fit(G,mode)
        json.dump(d,open(f'/home/user/rx/risk_{mode}.json','w'))
