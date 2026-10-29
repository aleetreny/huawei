"""Offline first-principles interventions. Research only; never submission/Skill code.

Reads the team's replica and saved model labels, never a key, network client or official package.
No event text is written. Each career starts a fresh controller and fresh learning memory.
"""
from __future__ import annotations
import argparse, collections, copy, hashlib, json, math, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
import replica as R
import rules
from datapaths import deepseek_dir as _dsdir
K=('health','dignity','skill','network','output','wealth')
ARMS=('ideal_context','observed','true_risk','true_growth','true_all','loss_only','scheduled','blind_feedback','blind_scheduled','online')
def sign(x):return (x>0)-(x<0)
def labelsign(s):return 1 if str(s).startswith('+') else -1 if str(s).startswith('-') else 0
class Controller(rules.RuleBot):
    def __init__(self,arm,seed,labels):
        super().__init__();self.arm,self.seed,self.labels=arm,seed,labels
        self.month=0;self.level=0;self.hr=0;self.known={};self.prev=None
        self.cal=collections.defaultdict(lambda:[0.,0]);self.updates=0;self.defused=set()
    def cap(self,st,k):
        return R.cap(st.level,k) if self.arm in ('ideal_context','exact_caps','true_all_ideal') else self.known.get(k,1e6)
    def sync(self,st):
        if st.level!=self.level:self.known={};self.level=st.level
        if self.prev:
            kind,old,fx,sg,group,dr=self.prev
            if st.month==old.month and st.level==old.level:
                if kind=='q':
                    for k in R.GROWTH:
                        x=fx.get(k,0)
                        if x>0 and getattr(st,k)-getattr(old,k)<x:self.known[k]=getattr(st,k)
                if kind=='e' and self.arm=='online':
                    for k in K:
                        actual=sign(getattr(st,k)-getattr(old,k))
                        # Zero can be clipping; don't use it to label an unseen general mechanism.
                        if actual:
                            a=self.cal[(group,k,sg.get(k,0))];a[0]+=actual-sg.get(k,0);a[1]+=1;self.updates+=1
                if kind in ('q','m'):self.hr=max(0,self.hr+dr)
            self.prev=None
        if st.month!=self.month:self.hr=min(st.risk,4);self.month=st.month
    def view(self,st):
        s=copy.copy(st)
        if self.arm not in ('ideal_context','live_risk','true_all_ideal'):s.risk=self.hr
        return s
    def see(self,rep,st,node,k):
        idx=hashlib.sha256(f'{self.seed}|{st.month}|{node}'.encode()).digest()[0]%len(self.labels)
        row=self.labels[idx][f'{node}:{k}']
        fx={s:float(labelsign(row.get(s,'0'))) for s in K};risk=labelsign(row.get('risk','0'))
        sg=dict(fx);group=row.get('group','?')
        if self.arm=='online':
            for s in K:
                tot,n=self.cal[(group,s,sg[s])];fx[s]=max(-1,min(1,fx[s]+tot/(4+n)))
        if self.arm in ('true_growth','true_all','true_all_ideal','true_all_hard'):
            d=rep.cat.effect(node,k) or {}
            for s in (R.GROWTH if self.arm=='true_growth' else K):fx[s]=float(sign(d.get(s,0)))
        if self.arm in ('true_risk','true_all','true_all_ideal','true_all_hard'):risk=sign(rep.cat.answer_risk(node,k))
        if self.arm.startswith('blind_'):risk=0
        return fx,risk,sg,group
    def story(self,rep,st,node):
        self.sync(st);vst=self.view(st);best=None
        opts=[(int(kk),*self.see(rep,st,node,int(kk))) for kk in rep.cat.nodes[node]['choices']]
        if self.arm in ('hard_risk','true_all_hard','contract'):
            viable=[o for o in opts if st.health+o[1].get('health',0)>0]
            opts=viable or opts
            safer=[o for o in opts if o[2]<=0]
            opts=safer or opts
        for k,fx,risk,sg,group in opts:
            valued=dict(fx)
            if self.arm in ('loss_only','contract'):
                for s in R.GROWTH:valued[s]=min(0,valued.get(s,0))
            v=self._val(vst,valued,risk)
            # Shared reproducible tie-breaking without coupling to environmental RNG draws.
            tie=int.from_bytes(hashlib.sha256(f'{self.seed}|{st.month}|{node}|{k}'.encode()).digest()[:4],'big')/2**32
            row=(v,tie,k,fx,sg,group)
            if best is None or row[:2]>best[:2]:best=row
        _,_,k,fx,sg,group=best
        self.prev=('e',copy.copy(st),{},sg,group,0)
        return k
    def energy(self,rep,st):
        self.sync(st);s=self.view(st)
        if self.arm in ('scheduled','blind_scheduled'):
            if st.health<=4 and st.energy>=1:a='Health recovery'
            elif st.month not in self.defused and st.energy>=2:
                a='Defuse legacy risk';self.defused.add(st.month)
            else:
                # Maintenance is unconditional; remaining allocation uses known menu effects.
                s.risk=0;a=super().energy(rep,s)
        else:a=super().energy(rep,s)
        if a:self.prev=('q',copy.copy(st),R.ENERGY_FX[a][0],{},'',R.ACTION_RISK.get('q|'+a,0))
        return a
    def main(self,rep,st):
        self.sync(st)
        a='Lay low and reduce risk' if self.arm in ('scheduled','blind_scheduled') else super().main(rep,self.view(st))
        self.prev=('m',copy.copy(st),R.MAIN_FX[a],{},'',R.ACTION_RISK.get('m|'+a,0))
        return a

def summary(rows):
    q=[r['q'] for r in rows];m=sum(q)/len(q)
    return {'n':len(rows),'mean':m,'se':math.sqrt(sum((x-m)**2 for x in q)/(len(q)-1)/len(q)),
            'completion':sum(r['failure'] is None for r in rows)/len(rows),
            'promoted_by_first':sum(r['first_promotion'] is not None and r['first_promotion']<=6 for r in rows)/len(rows),
            'promoted_by_second':sum(r['first_promotion'] is not None and r['first_promotion']<=12 for r in rows)/len(rows),
            'failures':dict(collections.Counter(r['failure'] or 'completed' for r in rows)),
            'mean_feedback_updates':sum(r['updates'] for r in rows)/len(rows)}
def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=800);ap.add_argument('--seed',type=int,default=831000)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--arms',default=','.join(ARMS));a=ap.parse_args()
    cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()))
    paths=[_dsdir()/f'labels/ds-v3-r{r}-full.json' for r in (1,2)]
    labels=[json.loads(p.read_text()) for p in paths]
    required={f'{n}:{k}' for n,nd in cat.nodes.items() for k in nd['choices']}
    assert all(required<=set(lab) for lab in labels),'No oracle completion of missing labels allowed'
    out={'meta':{'games':a.games,'seed':a.seed,'arms':a.arms,'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
                 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 'catalog_sha256':hashlib.sha256((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_bytes()).hexdigest()},'arms':{}}
    for arm in a.arms.split(','):
        rows=[]
        for i in range(a.games):
            bot=Controller(arm,a.seed+i,labels);st,trace=R.play(cat,bot,random.Random(a.seed+i))
            promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,
                         'first_promotion':min(promo) if promo else None,'updates':bot.updates})
        out['arms'][arm]={'summary':summary(rows),'rows':rows}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1))
        print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
    if 'observed' in out['arms']:
        base=out['arms']['observed']['rows']
        for arm,dat in out['arms'].items():
            ds=[r['q']-b['q'] for r,b in zip(dat['rows'],base)];m=sum(ds)/len(ds)
            se=math.sqrt(sum((x-m)**2 for x in ds)/max(1,len(ds)-1)/len(ds))
            dat['delta_observed']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.write_text(json.dumps(out,indent=1))
if __name__=='__main__':run()
