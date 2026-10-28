"""Forecast observable after-panels rather than predicate labels. Default no calls."""
import argparse,asyncio,json,hashlib
from gpt_fresh_context import DATA as SOURCE,REPORT,quota as shared_quota
from gpt_fact_second_read import one,prepare as old_prepare,PROMPT
from gpt_decision_audit import processes
DATA=SOURCE.with_name('gpt-panel-forecast')
STATS=('health','dignity','skill','network','output','wealth')
TASK='''You are a forward predictor for a workplace game. For each offered action, predict the observable six-stat panel immediately after that action, before unrelated monthly or quarterly settlement. Start from the supplied current numbers. Account for both benefits and opportunity costs; a constructive act can still cost delivery or relationships. Do not substitute moral approval for a forecast. Give numeric after-values, not just direction labels. No hidden engine information is available: these are predictions, not facts. Then recommend one action using the unchanged participant policy below. Return JSON only.\n'''
def prepare():
 _,old=old_prepare();system=TASK+old[len(PROMPT):];p=SOURCE/'items.json';items=json.loads(p.read_text());assert len(items)==24
 DATA.mkdir(parents=True,exist_ok=True);plan={'n':24,'max_reads':24,'model':'sonnet','items_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'system_sha256':hashlib.sha256(system.encode()).hexdigest(),'scope':'All original critical states; numeric observable forward prediction instead of signs/factual flags. Original target choice hidden. Compare immediate chosen costs/risk and prediction error after collection. Gold only evaluator; no Q/DS claim. Any risk increase blocks admission. No games/API.','limits':{'five_hour':.65,'seven_day':.45,'processes':4}}
 f=REPORT/'panel-forecast-plan.json'
 if f.exists():assert json.loads(f.read_text())==plan
 else:f.write_text(json.dumps(plan,indent=2)+'\n')
 return items,system
def schema(it):
 ids=[c['choice'] for c in it['observe']['choices']];panel={'type':'object','properties':{k:{'type':'number'} for k in STATS},'required':list(STATS),'additionalProperties':False}
 return {'type':'object','properties':{'recommended_choice':{'type':'integer','enum':ids},'options':{'type':'array','items':{'type':'object','properties':{'choice':{'type':'integer','enum':ids},'after':panel},'required':['choice','after'],'additionalProperties':False}}},'required':['recommended_choice','options'],'additionalProperties':False}
def validate(it,r):
 ids={c['choice'] for c in it['observe']['choices']};assert len(r['options'])==len(ids) and {x['choice'] for x in r['options']}==ids
 assert r['recommended_choice'] in ids
 for x in r['options']:assert set(x['after'])==set(STATS) and all(isinstance(v,(int,float)) for v in x['after'].values())
async def run(limit):
 items,system=prepare();count=0
 for it in items:
  d=DATA/it['id']
  if d.exists():
   p=d/'result.json'
   if p.exists() and json.loads(p.read_text())['done']:continue
   raise RuntimeError('Inspect existing failed read; never replace')
  q=shared_quota(extra_roots=(DATA,))
  if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',q);return
  r=await one(it,system,data_root=DATA,model='sonnet',schema_override=schema(it),validator=validate);count+=1
  if not r['done']:raise RuntimeError('Forecast transport failure')
  if count>=limit:return
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--calls',type=int,default=0);a=p.parse_args()
 if a.calls:asyncio.run(run(a.calls))
 else:print({'n':len(prepare()[0]),'quota':shared_quota(extra_roots=(DATA,))})
