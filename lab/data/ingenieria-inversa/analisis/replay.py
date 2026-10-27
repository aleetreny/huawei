"""One-step replay validator: predict state after each decision from the recorded state before it."""
import tl, collections, sys, json
CAPS={1:{'skill':9,'network':3,'output':3},2:{'skill':21,'network':7,'output':6},3:{'skill':42,'network':21,'output':16},
      4:{'skill':108,'network':36,'output':26},5:{'skill':154,'network':54,'output':38},6:{'skill':999,'network':72,'output':54}}
MINS={'health':0,'dignity':0,'skill':1,'network':0,'output':-1}
IX={'health':0,'dignity':1,'skill':2,'network':3,'output':6,'wealth':7}
def apply(v, d, lv):
    v=list(v)
    if 'skill' in d and v[IX['skill']]+d['skill']<1:
        d=dict(d); d['dignity']=d.get('dignity',0)-1; d['output']=d.get('output',0)-1
    for k,x in d.items():
        if k not in IX: continue
        i=IX[k]; nv=v[i]+x
        if k in ('health','dignity'): nv=min(10,nv)
        if k in CAPS.get(lv,{}): 
            cap=CAPS[lv][k]
            if x>0: nv=min(nv, max(cap, v[i]))
        if k in MINS: nv=max(MINS[k],nv)
        v[i]=round(nv,3)
    return v
if __name__=='__main__':
    b=tl.Batch(*sys.argv[1].split(',')); N=int(sys.argv[2])
    c=collections.Counter(); ex={}
    n=0
    for g in b.games():
        r=tl.timeline(b,g)
        if r is None: continue
        out=r[1]
        for i in range(len(out)-1):
            s,e,after=out[i]; s2=out[i+1][0]
            kinds=''.join(sorted(set(cc for cc,_ in after)))
            if s2[0]!=s[0]: continue   # month change handled later
            if any(k in kinds for k in ('X','R','T')): continue
            pred=apply(s[4], e['d'], s[4][4])
            evt=b.texts.get(s2[5],'') if s2[5] else ''
            if 'Old landmines' in evt:
                kinds+='B'
                pred[IX['output']]=0; pred[IX['dignity']]=max(0,pred[IX['dignity']]-2); pred[IX['wealth']]=round(pred[IX['wealth']]-2,3)
            diff=tuple((k,round(s2[4][ix]-pred[ix],2)) for k,ix in IX.items() if abs(s2[4][ix]-pred[ix])>(1.01 if k=='wealth' else 1e-6))
            key=(s[1],kinds,diff)
            c[key]+=1; ex.setdefault(key,(g['g'],s[0],s[4],e['title'][:30],e['delta_line'],[(cc,m[:80]) for cc,m in after]))
        n+=1
        if n>=N: break
    tot=sum(c.values()); good=sum(v for k,v in c.items() if not k[2])
    print('match',good,'/',tot)
    for k,v in c.most_common(25):
        if k[2]: print(v,k,ex[k])
