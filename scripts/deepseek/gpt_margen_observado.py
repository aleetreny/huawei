"""Test risk stress pricing after removing privileged planner context.
Same RuleBot utility, learned ceilings, lagged HR and frozen label readings as recovered tests.
"""
import argparse,json,math,random,hashlib
from pathlib import Path
import gpt_principios as B
from datapaths import deepseek_dir as _dsdir
class Controller(B.Controller):
    def __init__(self,arm,seed,labels):
        super().__init__('hard_risk' if arm=='veto' else 'observed',seed,labels);self.stress=arm=='stress3'
    def _val(self,st,fx,risk_sign):
        return super()._val(st,fx,3 if self.stress and risk_sign>0 else risk_sign)
def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=2000);ap.add_argument('--seed',type=int,default=202670270);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    cp=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=B.R.Catalog(json.loads(cp.read_text()))
    paths=[_dsdir()/f'labels/ds-v3-r{r}-full.json' for r in (1,2)];labels=[json.loads(p.read_text()) for p in paths]
    out={'meta':{'games':a.games,'seed':a.seed,'context':'Learned ceilings, lagged HR, no thresholds used by controller. RuleBot, not privileged Planner. Known quarter action deltas. Frozen saved signs, not model execution.',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
     'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]},'arms':{}}
    for arm in ('observed','stress3','veto'):
        rows=[]
        for i in range(a.games):
            st,trace=B.R.play(cat,Controller(arm,a.seed+i,labels),random.Random(a.seed+i));promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':B.R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(promo) if promo else None,'updates':0})
        out['arms'][arm]={'summary':B.summary(rows),'rows':rows}
        if arm!='observed':
            ds=[r['q']-b['q'] for r,b in zip(rows,out['arms']['observed']['rows'])];m=sum(ds)/len(ds);se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds))
            out['arms'][arm]['delta_observed']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1));print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
if __name__=='__main__':run()
