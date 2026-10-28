"""Offline stalled-career recovery, fixed paired seeds; research only, not Skill code."""
import json,copy,random,math,hashlib,collections
from pathlib import Path
from gpt_principios import ROOT,R,Controller,summary
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
class Recovery(Controller):
 def __init__(self,*a):super().__init__(*a);self.review_month=0;self.review_level=1;self.misses=0;self.repairs=0
 def sync(self,st):
  if st.level!=self.review_level:self.misses=0;self.review_level=st.level
  if st.month!=self.review_month:
   if st.month%6==0 and st.level==self.level:self.misses+=1
   self.review_month=st.month
  super().sync(st)
 def energy(self,rep,st):
  self.sync(st)
  if self.misses>=2 and self.hr>0 and st.energy>=2 and st.health>4:
   a='Defuse legacy risk';self.prev=('q',copy.copy(st),R.ENERGY_FX[a][0],{},'',R.ACTION_RISK.get('q|'+a,0));self.repairs+=1;return a
  return super().energy(rep,st)
 def main(self,rep,st):
  self.sync(st)
  if self.misses>=2 and self.hr>0:
   a='Lay low and reduce risk';self.prev=('m',copy.copy(st),R.MAIN_FX[a],{},'',R.ACTION_RISK.get('m|'+a,0));self.repairs+=1;return a
  return super().main(rep,st)
def main():
 paths=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)];labels=[json.loads(p.read_text()) for p in paths];cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));plan={'n':600,'seed':2026102900,'arms':['observed','recovery'],'rule':'After two consecutive observed reviews without promotion, prioritise reducing non-best monthly HR feedback in quarters; health priority retained. Stories unchanged. Reset misses on promotion.','scope':'Research replica and frozen DS labels, not a Skill or Q forecast. No API. Same random seeds; path divergence possible. No private month/threshold rule delivered.','labels_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]};p=REPORT/'stall-recovery-plan.json'
 if p.exists():assert json.loads(p.read_text())==plan
 else:p.write_text(json.dumps(plan,indent=2)+'\n')
 out={}
 for arm,cls in [('observed',Controller),('recovery',Recovery)]:
  rows=[]
  for i in range(plan['n']):
   seed=plan['seed']+i;b=cls('observed',seed,labels);st,trace=R.play(cat,b,random.Random(seed));prom=[m for m,ph,*v in trace if ph=='r' and v[0].get('promoted')];rows.append({'seed':seed,'q':R.Replica.score(st),'failure':st.failure,'level':st.level,'first_promotion':min(prom) if prom else None,'updates':b.updates,'repairs':getattr(b,'repairs',0)})
  out[arm]={'summary':summary(rows),'repairs':sum(x['repairs'] for x in rows),'rows':rows}
 ds=[r['q']-b['q'] for r,b in zip(out['recovery']['rows'],out['observed']['rows'])];mean=sum(ds)/len(ds);se=math.sqrt(sum((d-mean)**2 for d in ds)/(len(ds)-1)/len(ds));result={'meaning':'Fixed offline recovery screen, not a model game or DS claim. Historical B30 motivated rule; no gold in story selection beyond existing frozen-label controller.','arms':out,'delta':{'mean':mean,'ci95':[mean-1.96*se,mean+1.96*se]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'stall-recovery-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summaries':{a:{k:v for k,v in d.items() if k!='rows'} for a,d in out.items()},'delta':result['delta']},indent=2))
if __name__=='__main__':main()
