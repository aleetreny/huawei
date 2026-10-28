"""Offline uncertainty interventions over frozen saved label readings; never a submission.
No model/network client, credentials, or official engine package imports.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random
from pathlib import Path
import gpt_principios as B
R=B.R

class Controller(B.Controller):
    def __init__(self, arm, seed, labels):
        super().__init__('observed',seed,labels)
        self.variant=arm
        if arm != 'observed': self.arm='hard_risk'
    def see(self, rep, st, node, k):
        fx,risk,sg,group=super().see(rep,st,node,k)
        if self.variant in ('observed','hard_risk'):return fx,risk,sg,group
        rows=[lab[f'{node}:{k}'] for lab in self.labels]
        rs=[B.labelsign(r.get('risk','0')) for r in rows]
        # An unsafe reading in either replicate must be considered, without access to truth.
        risk=max(rs)
        if self.variant=='dual_pessimistic':
            fx={s:float(min(B.labelsign(r.get(s,'0')) for r in rows)) for s in B.K}
        elif self.variant=='dual_average':
            fx={s:sum(B.labelsign(r.get(s,'0')) for r in rows)/len(rows) for s in B.K}
        elif self.variant=='dual_loss':
            fx={s:float(min(B.labelsign(r.get(s,'0')) for r in rows)) if s in R.GROWTH else fx[s] for s in B.K}
        elif self.variant!='dual_risk':raise ValueError(self.variant)
        return fx,risk,sg,group

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=600);ap.add_argument('--seed',type=int,default=202610270)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    catpath=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json'
    cat=R.Catalog(json.loads(catpath.read_text()))
    paths=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{r}-full.json' for r in (1,2)]
    labels=[json.loads(p.read_text()) for p in paths]
    required={f'{n}:{k}' for n,nd in cat.nodes.items() for k in nd['choices']}
    assert all(required<=set(lab) for lab in labels)
    out={'meta':{'games':a.games,'seed':a.seed,'design':'Six prespecified arms, same seeds. Two fixed label files; simulation SE excludes uncertainty across new model readings.',
       'catalog_sha256':hashlib.sha256(catpath.read_bytes()).hexdigest(),
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'base_sha256':hashlib.sha256(Path(B.__file__).read_bytes()).hexdigest(),
       'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]},'arms':{}}
    for arm in ('observed','hard_risk','dual_risk','dual_average','dual_pessimistic','dual_loss'):
        rows=[]
        for i in range(a.games):
            bot=Controller(arm,a.seed+i,labels);st,trace=R.play(cat,bot,random.Random(a.seed+i))
            promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,
              'first_promotion':min(promo) if promo else None,'updates':bot.updates})
        out['arms'][arm]={'summary':B.summary(rows),'rows':rows}
        if arm!='observed':
            ds=[r['q']-b['q'] for r,b in zip(rows,out['arms']['observed']['rows'])];m=sum(ds)/len(ds)
            se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds))
            out['arms'][arm]['delta_observed']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1))
        print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
if __name__=='__main__':run()
