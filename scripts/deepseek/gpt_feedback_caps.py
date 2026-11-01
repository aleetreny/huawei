"""Learning a stalled gain from public consequences, with saved model expectations.
Research only. No model calls, official packages or data files. Private caps only diagnose errors.
"""
from __future__ import annotations
import argparse,collections,copy,gzip,hashlib,json,random,sys
from pathlib import Path
from gpt_principios import Controller,ROOT,R,summary,sign

class Learner(Controller):
    def __init__(self,seed,labels,required,truth=False):
        super().__init__('hard_risk',seed,labels);self.required=required;self.truth=truth
        self.evidence=collections.defaultdict(set);self.last_node=None;self.story_updates=0;self.false_updates=0;self.revoked=0
    def see(self,rep,st,node,k):
        fx,risk,sg,group=super().see(rep,st,node,k)
        if self.truth:
            d=rep.cat.effect(node,k) or {};fx={s:float(sign(d.get(s,0))) for s in fx};sg=dict(fx);risk=sign(rep.cat.answer_risk(node,k))
        return fx,risk,sg,group
    def sync(self,st):
        prev=self.prev;oldlevel=self.level
        super().sync(st)
        if st.level!=oldlevel:self.evidence.clear()
        if not self.required or not prev or prev[0]!='e':return
        _,old,_,sg,_,_=prev
        if (st.month,st.level)!=(old.month,old.level):return
        # Only same-month/level public changes; no true option delta or current risk is read.
        for k in R.GROWTH:
            delta=getattr(st,k)-getattr(old,k);cur=getattr(st,k)
            if delta>0:
                if k in self.known and cur>self.known[k]:self.known.pop(k);self.revoked+=1
                self.evidence={key:ids for key,ids in self.evidence.items() if key[0]!=k} | collections.defaultdict(set)
                self.evidence=collections.defaultdict(set,self.evidence)
            elif delta==0 and sg.get(k,0)>0:
                self.evidence[(k,cur)].add(self.last_node)
                if len(self.evidence[(k,cur)])>=self.required and self.known.get(k)!=cur:
                    self.known[k]=cur;self.story_updates+=1
                    # Ground truth is used only for reporting an erroneous inferred ceiling.
                    self.false_updates+=cur!=R.cap(st.level,k)
    def story(self,rep,st,node):
        k=super().story(rep,st,node);self.last_node=node;return k

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=600);ap.add_argument('--seed',type=int,default=202680270);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    lp=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)];labels=[json.loads(p.read_text()) for p in lp]
    out={'meta':{'games':a.games,'seed':a.seed,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'labels_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in lp],
                 'meaning':'Own replica, frozen expectations, not native model learning or game Q forecast. Same-month observed changes only. Actual caps never enter DS policy; false_updates uses caps only as an outcome metric.'},'arms':{}}
    allrows={}
    for name,required,truth in [('ds_baseline',0,False),('ds_one',1,False),('ds_two',2,False),('ds_three',3,False),('signs_baseline',0,True),('signs_two',2,True)]:
        rows=[]
        for i in range(a.games):
            bot=Learner(a.seed+i,labels,required,truth);st,tr=R.play(cat,bot,random.Random(a.seed+i));promo=[m for m,ph,*v in tr if ph=='r' and v[0].get('promoted')]
            rows.append({'seed':a.seed+i,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(promo) if promo else None,'updates':bot.story_updates,'false_updates':bot.false_updates,'revoked':bot.revoked})
        sm=summary(rows);sm['mean_false_updates']=sum(r['false_updates'] for r in rows)/len(rows);sm['mean_revoked']=sum(r['revoked'] for r in rows)/len(rows)
        out['arms'][name]={'summary':sm};allrows[name]=rows;print(name,json.dumps(sm),flush=True)
    for name,rows in allrows.items():
        base=allrows['signs_baseline' if name.startswith('signs') else 'ds_baseline'];ds=[r['q']-b['q'] for r,b in zip(rows,base)];m=sum(ds)/len(ds);se=(sum((d-m)**2 for d in ds)/(len(ds)-1)/len(ds))**.5
        out['arms'][name]['paired_delta']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
    raw=json.dumps(allrows,indent=1).encode();archive=a.out.with_suffix('.json.gz');archive.write_bytes(gzip.compress(raw,mtime=0));out['archive']={'file':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(raw).hexdigest()};a.out.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run()
