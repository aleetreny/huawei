"""Research information ceiling: same Planner, different story representations.
All arms use privileged current risk, caps and promotion thresholds. Not an agent forecast.
No lookahead to unseen future story nodes. Never include this in a Skill.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random
from pathlib import Path
import gpt_principios as B
import planner as P
R=B.R
class Controller(P.Planner):
    def __init__(self,arm,seed,labels,params):
        super().__init__(**params);self.arm,self.seed,self.labels=arm,seed,labels
    def story(self,rep,st,node):
        idx=hashlib.sha256(f'{self.seed}|{st.month}|{node}'.encode()).digest()[0]%len(self.labels)
        opts=[]
        for kk in rep.cat.nodes[node]['choices']:
            k=int(kk);truth=rep.cat.effect(node,k) or {};dr=rep.cat.answer_risk(node,k)
            row=self.labels[idx][f'{node}:{k}']
            if self.arm=='exact':fx=truth
            elif self.arm=='perfect_signs':fx={s:B.sign(truth.get(s,0)) for s in B.K};dr=B.sign(dr)
            else:
                fx={s:B.labelsign(row.get(s,'0')) for s in B.K}
                if self.arm=='predicted_magnitudes':fx={s:x*abs(truth.get(s,0)) for s,x in fx.items()}
                if self.arm!='predicted_true_risk':dr=B.labelsign(row.get('risk','0'))
            tie=int.from_bytes(hashlib.sha256(f'{self.seed}|{st.month}|{node}|{k}'.encode()).digest()[:4],'big')/2**32
            opts.append((self.value(rep,st,fx,dr),tie,k))
        return max(opts)[2]
def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=800);ap.add_argument('--seed',type=int,default=202640270);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    cp=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    pp=B.ROOT/'lab/data/ingenieria-inversa/politica_optima.json'
    params=json.loads(pp.read_text()) if pp.exists() else P.DEFAULT
    print('Planner params from',pp if pp.exists() else 'P.DEFAULT',flush=True)
    paths=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{r}-full.json' for r in (1,2)];labels=[json.loads(p.read_text()) for p in paths]
    out={'meta':{'games':a.games,'seed':a.seed,'context':'privileged true current risk/caps/thresholds, known menu effects. No next-node lookahead; conditional fixed two label files. Not model performance.',
     'params':params,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
     'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]},'arms':{}}
    for arm in ('exact','perfect_signs','predicted','predicted_true_risk','predicted_magnitudes'):
        rows=[]
        for i in range(a.games):
            st,trace=R.play(cat,Controller(arm,a.seed+i,labels,params),random.Random(a.seed+i))
            promo=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(promo) if promo else None,'updates':0})
        out['arms'][arm]={'summary':B.summary(rows),'rows':rows}
        if arm!='exact':
            ds=[r['q']-b['q'] for r,b in zip(rows,out['arms']['exact']['rows'])];m=sum(ds)/len(ds);se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds))
            out['arms'][arm]['delta_exact']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=1));print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
if __name__=='__main__':run()
