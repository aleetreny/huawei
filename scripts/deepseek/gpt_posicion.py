"""Research-only positional sanity check. Never submit a fixed-index game policy.
Tests a possible dataset-order confound with identical observed quarterly control.
"""
import argparse,hashlib,json,random,math
from pathlib import Path
import gpt_principios as B
class Bot(B.Controller):
    def __init__(self,arm,seed):
        super().__init__('observed',seed,[]);self.position=arm
    def story(self,rep,st,node):
        self.sync(st);self.prev=None;keys=sorted(int(k) for k in rep.cat.nodes[node]['choices'])
        if self.position=='first':return keys[0]
        if self.position=='last':return keys[-1]
        rng=random.Random(f'{self.seed}/{st.month}/{node}')
        return rng.choice(keys)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=1000);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    cp=B.ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=B.R.Catalog(json.loads(cp.read_text()))
    out={'meta':{'seed':202680270,'n':a.games,'purpose':'diagnose option-order confound, not a compliant strategy or evidence about competitors',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()},'arms':{}}
    for arm in ('first','last','uniform'):
        rows=[]
        for i in range(a.games):
            seed=202680270+i;st,tr=B.R.play(cat,Bot(arm,seed),random.Random(seed));promo=[m for m,ph,*v in tr if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':seed,'q':B.R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(promo) if promo else None,'updates':0})
        out['arms'][arm]={'summary':B.summary(rows),'rows':rows};print(arm,json.dumps(out['arms'][arm]['summary']),flush=True)
        a.out.write_text(json.dumps(out,indent=1))
if __name__=='__main__':main()
