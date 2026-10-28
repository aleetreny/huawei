"""Research-only joint-quarter intervention with saved readings and learned ceilings.
Planner simulates public menu deltas clipped only to observed ceilings and public wellbeing bounds.
It never uses the replica transition or true ceiling to rank plans.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math, random
from pathlib import Path
import gpt_incertidumbre as U
B=U.B
R=B.R

class Controller(U.Controller):
    def __init__(self,arm,seed,labels):
        super().__init__('hard_risk',seed,labels)
        self.joint=arm=='joint';self.pending_main=None
    def predict(self,st,a,phase):
        s=copy.copy(st)
        fx,cost=R.ENERGY_FX[a] if phase=='q' else (R.MAIN_FX[a],0)
        for k,x in fx.items():
            hi=10 if k in ('health','dignity') else self.cap(st,k) if k in R.GROWTH else float('inf')
            setattr(s,k,max(R.MINS.get(k,-float('inf')),min(hi,getattr(s,k)+x)))
        dr=R.ACTION_RISK.get(phase+'|'+a,0)
        s.risk=max(0,s.risk+dr);s.energy-=cost
        return s
    def plan(self,st):
        view=self.view(st); candidates=[]
        def visit(s,seq):
            for main in R.MAIN_FX:
                end=self.predict(s,main,'m')
                if end.health<=0:continue
                fx={k:getattr(end,k)-getattr(view,k) for k in B.K}
                # Same utility as the control, evaluated once on the combined plan.
                v=self._val(view,fx,end.risk-view.risk)
                candidates.append((v,len(seq),seq,main))
            for name,(_,cost) in R.ENERGY_FX.items():
                if cost<=0 or cost>s.energy:continue
                nxt=self.predict(s,name,'q')
                if nxt.health>0:visit(nxt,seq+(name,))
        visit(view,())
        return max(candidates)
    def energy(self,rep,st):
        if not self.joint:return super().energy(rep,st)
        self.sync(st)
        _,_,seq,main=self.plan(st);self.pending_main=main
        if not seq:return None
        a=seq[0]
        self.prev=('q',copy.copy(st),R.ENERGY_FX[a][0],{},'',R.ACTION_RISK.get('q|'+a,0))
        return a
    def main(self,rep,st):
        if not self.joint:return super().main(rep,st)
        self.sync(st)
        _,_,_,a=self.plan(st)
        self.prev=('m',copy.copy(st),R.MAIN_FX[a],{},'',R.ACTION_RISK.get('m|'+a,0))
        return a

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=400);ap.add_argument('--seed',type=int,default=202620270);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    catpath=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(catpath.read_text()))
    paths=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{r}-full.json' for r in (1,2)]
    labels=[json.loads(p.read_text()) for p in paths]
    out={'meta':{'games':a.games,'seed':a.seed,'design':'Fixed two arms; same story choices and utility; jointly enumerate quarter instead of greedy. Known menu deltas, learned ceilings, lagged HR. Conditional on frozen labels.',
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'catalog_sha256':hashlib.sha256(catpath.read_bytes()).hexdigest(),
      'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]},'arms':{}}
    for arm in ('greedy','joint'):
        rows=[]
        for i in range(a.games):
            bot=Controller(arm,a.seed+i,labels);st,trace=R.play(cat,bot,random.Random(a.seed+i))
            promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,
              'first_promotion':min(promo) if promo else None,'updates':bot.updates})
        out['arms'][arm]={'summary':B.summary(rows),'rows':rows}
        if arm=='joint':
            ds=[r['q']-b['q'] for r,b in zip(rows,out['arms']['greedy']['rows'])];m=sum(ds)/len(ds);se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds))
            out['arms'][arm]['delta_greedy']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1));print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
if __name__=='__main__':run()
