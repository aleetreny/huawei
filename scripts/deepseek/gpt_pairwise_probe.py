"""Matched representation probe on saved observations; no game or DeepSeek calls."""
import argparse, asyncio, hashlib, json
from pathlib import Path
from gpt_panel_forecast import SOURCE, REPORT
from gpt_fact_second_read import one, prepare as policy_source, PROMPT
from gpt_decision_audit import processes
DATA = SOURCE.with_name('gpt-pairwise-probe')
TASKS = {
 'absolute': 'Evaluate each offered alternative separately: identify its concrete delivery and relationship costs and whether it leaves a problem unresolved. Then choose using the unchanged policy. Do not invent numeric effects.',
 'pairwise': 'Compare each pair of offered alternatives directly. What concrete delivery or relationship commitment does one sacrifice that the other preserves? Which leaves more of the problem unresolved? Do not infer danger just from private/public or now/later wording. Then choose using the unchanged policy. Do not invent numeric effects.',
}
def prepare():
 items = json.loads((SOURCE/'items.json').read_text())
 _, old = policy_source()
 policy = old[len(PROMPT):]
 systems = {a: t+' Keep the comparison concise. Return JSON with recommended_choice and analysis.\n'+policy for a,t in TASKS.items()}
 plan = {'n':len(items), 'max_calls':2*len(items), 'model':'sonnet', 'arms':list(TASKS), 'items_sha256':hashlib.sha256((SOURCE/'items.json').read_bytes()).hexdigest(), 'system_sha256':{a:hashlib.sha256(s.encode()).hexdigest() for a,s in systems.items()}, 'endpoint':'Immediate avoidable growth loss; increased positive risk blocks admission. All 24 pre-review states from one saved Sonnet career, not selected for gold errors. Same policy, schema, model, one call per arm. No proof of transfer to shared DeepSeek errors or career score. Alternating arm order. No retries of completed or failed trials.'}
 DATA.mkdir(parents=True,exist_ok=True)
 p=REPORT/'pairwise-probe-plan.json'
 if p.exists():assert json.loads(p.read_text())==plan
 else:p.write_text(json.dumps(plan,indent=2)+'\n')
 return items,systems
async def run(limit):
 items,systems=prepare();done=0
 for i,it in enumerate(items):
  for arm in (list(TASKS) if i%2==0 else list(TASKS)[::-1]):
   root=DATA/arm;root.mkdir(exist_ok=True);p=root/it['id']/'result.json'
   if p.exists():
    assert json.loads(p.read_text())['done'], 'Inspect failed result; no replacement'
    continue
   if processes()>=4:print('Concurrency admission stop');return
   ids=[c['choice'] for c in it['observe']['choices']]
   schema={'type':'object','properties':{'recommended_choice':{'type':'integer','enum':ids},'analysis':{'type':'string','maxLength':2200}},'required':['recommended_choice','analysis'],'additionalProperties':False}
   def validate(item,r):
    assert r['recommended_choice'] in ids and isinstance(r['analysis'],str) and len(r['analysis'])<=2200
   r=await one(it,systems[arm],data_root=root,model='sonnet',schema_override=schema,validator=validate)
   assert r['done'] and r['models']==['claude-sonnet-5-5'], 'Transport/model failure'
   done+=1
   for line in (root/it['id']/'stream.jsonl').read_text().splitlines():
    event=json.loads(line)
    if event.get('type')=='rate_limit_event':
     info=event.get('rate_limit_info',{})
     used=(info.get('unifiedWindows',{}).get('five_hour') or {}).get('utilization',0)
     if used>=.95 or info.get('status')=='rejected':
      print('Quota admission stop');return
   if done>=limit:return
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--calls',type=int,default=0);a=p.parse_args()
 if a.calls:asyncio.run(run(a.calls))
 else:print({'n':len(prepare()[0]),'calls':0})
