"""Causal post-action public-return learning screen, research replica only."""
import json,copy,random,hashlib,math
from pathlib import Path
from gpt_principios import ROOT,R,Controller,summary
from gpt_measured_ledger import MeasuredLedger,GROWTH
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
def public(st):return {k:getattr(st,k) for k in ('month','level',*GROWTH)}
class Learner(Controller):
 def __init__(self,*args):super().__init__(*args);self.pending=None;self.ledger=MeasuredLedger('replica-career');self.sequence=0;self.last_log_known=set()
 def sync(self,st):
  super().sync(st)
  if self.pending:
   before,cat,node,k,seq=self.pending;self.pending=None
   # This callback occurs only on the next decision, after the prior action committed.
   # Only the chosen action's logged nominal visible return is exposed, never alternatives.
   nominal={g:v for g,v in (cat.effect(node,k) or {}).items() if g in GROWTH}
   self.ledger.accept('replica-career',str(seq),before,public(st),nominal,True)
   if before['level']==st.level:
    for g in self.last_log_known-set(self.ledger.diminished):self.known.pop(g,None)
    self.known.update(self.ledger.diminished);self.last_log_known=set(self.ledger.diminished)
   else:self.last_log_known=set()
 def story(self,rep,st,node):
  k=super().story(rep,st,node);self.sequence+=1;self.pending=(public(st),rep.cat,node,k,self.sequence);return k

def main():
 paths=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)];labels=[json.loads(p.read_text()) for p in paths];cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));plan={'n':600,'seed':2026202900,'arms':['quarter_learning','quarter_plus_logged_story_returns'],'labels_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],'scope':'Chosen nominal visible effects revealed only at the next decision after action committed, simulating public logged feedback. Never unseen alternatives or true caps supplied. Same controller/readings; single-action month/role guard in MeasuredLedger. Replica mechanism screen, not live efficacy or DS prediction.'};p=REPORT/'return-learning-plan.json'
 if p.exists():assert json.loads(p.read_text())==plan
 else:p.write_text(json.dumps(plan,indent=2)+'\n')
 out={}
 for name,cls in [('quarter_learning',Controller),('quarter_plus_logged_story_returns',Learner)]:
  rows=[];learned=0
  for i in range(plan['n']):
   seed=plan['seed']+i;b=cls('observed',seed,labels);st,trace=R.play(cat,b,random.Random(seed));prom=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')];rows.append({'seed':seed,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(prom) if prom else None,'updates':b.updates});learned+=getattr(b,'ledger',None).counts['diminished_observations'] if isinstance(b,Learner) else 0
  out[name]={'summary':summary(rows),'diminished_observations':learned,'rows':rows}
 ds=[a['q']-b['q'] for a,b in zip(out['quarter_plus_logged_story_returns']['rows'],out['quarter_learning']['rows'])];mean=sum(ds)/len(ds);se=math.sqrt(sum((d-mean)**2 for d in ds)/(len(ds)-1)/len(ds));result={'meaning':plan['scope'],'arms':out,'delta':{'mean':mean,'ci95':[mean-1.96*se,mean+1.96*se]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'return-learning-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summaries':{a:{k:v for k,v in d.items() if k!='rows'} for a,d in out.items()},'delta':result['delta']},indent=2))
if __name__=='__main__':main()
