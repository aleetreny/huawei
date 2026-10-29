"""Research diagnostic: can earlier wellbeing preference explain high ending scores?
Not a submission: fixed level interventions and inherited research utility stay in the lab.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random
from pathlib import Path
import gpt_incertidumbre as U
from datapaths import deepseek_dir as _dsdir
B=U.B;R=B.R
class Controller(U.Controller):
    def __init__(self,arm,seed,labels):
        super().__init__('hard_risk',seed,labels);self.stop=int(arm[1:]) if arm!='control' else 99
    def _val(self,st,fx,risk_sign):
        v=super()._val(st,fx,risk_sign)
        if st.level>=self.stop:
            hd=sum(min(10,max(0,getattr(st,k)+fx.get(k,0)))-getattr(st,k) for k in ('health','dignity'))
            v+=5*hd
        return v

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=800);ap.add_argument('--seed',type=int,default=202630270);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    cp=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    paths=[_dsdir()/f'labels/ds-v3-r{r}-full.json' for r in (1,2)];labels=[json.loads(p.read_text()) for p in paths]
    out={'meta':{'games':a.games,'seed':a.seed,'design':'Fixed five arms, same seeds and saved labels; add 5x wellbeing preference at public levels L3/4/5/6. Diagnostic, not deployable threshold.',
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
      'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]},'arms':{}}
    for arm in ('control','L3','L4','L5','L6'):
        rows=[]
        for i in range(a.games):
            bot=Controller(arm,a.seed+i,labels);st,trace=R.play(cat,bot,random.Random(a.seed+i))
            promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,'health':st.health,'dignity':st.dignity,
              'wealth':st.wealth,'skill':st.skill,'network':st.network,'risk':st.risk,'blowups':st.blowups,
              'first_promotion':min(promo) if promo else None,'updates':bot.updates})
        summ=B.summary(rows);cc=[r['q'] for r in rows if r['failure'] is None]
        summ['completed_mean']=sum(cc)/len(cc) if cc else None;summ['Q75_rate']=sum(r['q']>=75 for r in rows)/len(rows)
        out['arms'][arm]={'summary':summ,'rows':rows}
        if arm!='control':
            ds=[r['q']-b['q'] for r,b in zip(rows,out['arms']['control']['rows'])];m=sum(ds)/len(ds);se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds))
            out['arms'][arm]['delta_control']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1));print(arm,json.dumps(summ),flush=True)
if __name__=='__main__':run()
