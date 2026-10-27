"""Sequential integer hidden-risk fit: R = HR level (exact below 4), clip at 0, explosions reset."""
import tl, collections, tags, sys, json, random, os, numpy as np
def key(s,e):
    if s[1]=='e': return 'E|'+s[2]+'|'+str(s[3])
    return s[1]+'|'+e['chosen']
def load(batches):
    b=tl.Batch(*batches); G=[]
    for g in b.games():
        if g['outcome'] not in ('eliminated','completed'): continue
        r=tl.timeline(b,g)
        if r is None: continue
        seq=[]; out=r[1]
        for i,(s,e,a) in enumerate(out):
            t=b.texts.get(s[5],'') if s[5] else ''
            h=tags.hr(t)
            blow='Old landmines' in t
            if h is not None:
                if any(x in t for x in ('I had hopes','The room feels tense','HR marks the note')): seq.append(('K','REVIEW_WARN'))
                # month-start: explosion (if any) happens after the HR remark is computed
                seq.append(('O',h))
                if blow: seq.append(('B',0))
            elif blow:
                seq.append(('B',0))
            seq.append(('K',key(s,e)))
        fr=(g['final']['flags'].get('failure_reason') or '')
        y=g['end']['dims']['risk_control'][0]
        if fr.startswith('Trust crisis'): y=None
        G.append((seq,y))
    return G
def loss_game(seq,y,d,mode='reset',wfinal=1.0):
    R=0; n=0; L=0.0
    for typ,v in seq:
        if typ=='K': R=max(0,R+d.get(v,0))
        elif typ=='O':
            if v<4: L+=(R-v)**2
            elif R<4: L+=(4-R)**2
        else:
            n+=1
            if mode=='reset': R=0
    if y is not None: L+=wfinal*(R+5*n-y)**2
    return L
def fit(G,init,iters=10,vals=range(-3,4),mode='reset'):
    d=dict(init); idx=collections.defaultdict(list)
    for gi,(seq,y) in enumerate(G):
        for typ,v in seq:
            if typ=='K': idx[v].append(gi)
    for k in idx: idx[k]=sorted(set(idx[k]))
    err=np.array([loss_game(s,y,d,mode) for s,y in G])
    keys=list(idx)
    for it in range(iters):
        random.Random(it).shuffle(keys); ch=0
        for k in keys:
            gs=idx[k]; cur=d.get(k,0); best=(err[gs].sum(),cur)
            for v in vals:
                if v==cur: continue
                d[k]=v; e=sum(loss_game(G[g][0],G[g][1],d,mode) for g in gs)
                if e<best[0]-1e-9: best=(e,v)
            d[k]=best[1]
            if best[1]!=cur:
                ch+=1
                for g in gs: err[g]=loss_game(G[g][0],G[g][1],d,mode)
        print('iter',it,'changed',ch,'total loss',err.sum(),'games exact',np.mean(err==0).round(4),flush=True)
        if ch==0: break
    return d,err
if __name__=='__main__':
    G=load(sys.argv[1].split(','))
    sol=np.load('/home/user/rx/hrsol.npy'); keys=json.load(open('/home/user/rx/hrkeys.json'))
    init=json.load(open(os.environ.get('RISK_INIT','/home/user/rx/riskd.json'))); init['REVIEW_WARN']=1
    print('games',len(G))
    d,err=fit(G,init,mode=sys.argv[2] if len(sys.argv)>2 else 'reset')
    json.dump(d,open(os.environ.get('RISK_OUT','/home/user/rx/riskd.json'),'w'))
    print('value hist',collections.Counter(d.values()))
