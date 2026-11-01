"""Matched Sonnet test of causal public-return packets; default prepares only."""
import argparse,asyncio,copy,json,hashlib
from gpt_return_packets import DATA as INPUT,REPORT,SOURCE
from gpt_fresh_context import prefix as history_prefix,quota as shared_quota
from gpt_capacity_probe import one
from gpt_decision_audit import processes
DATA=INPUT.with_name('gpt-return-packet-probe');FORECAST=INPUT.with_name('gpt-panel-forecast')
def prefix(it,arm):
 return history_prefix(it)+'A supplied helper packet records previous observed returns, not effects of the current options. Use supplied observations to maintain Stalled, following the same Skill.\nHelper packet: '+(json.dumps(it['packet']) if arm=='measured_returns' else 'not supplied')+'\n\n'
def prepare():
 p=INPUT/'items.json';items=json.loads(p.read_text());assert len(items)==24
 plan={'n':24,'max_reads':48,'model':'sonnet','arms':['control','measured_returns'],'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_system_sha256':hashlib.sha256((SOURCE/'system_prompt.md').read_bytes()).hexdigest(),'prefix_sha256':{a:[hashlib.sha256(prefix(it,a).encode()).hexdigest() for it in items] for a in ('control','measured_returns')},'scope':'Same24public original panels, last3prior notes, original system/Skill. Common interpretation line in both arms; only packet availability differs. Alternating order. No target effect/original choice shown. Primary avoidable growth loss; risk increase blocks admission. One source career, no game-Q/DS claims, no claim of Jiuwen script execution.','limits':{'five_hour':.65,'seven_day':.45,'processes':4,'concurrency':1}}
 DATA.mkdir(parents=True,exist_ok=True);f=REPORT/'return-packet-probe-plan.json'
 if f.exists():assert json.loads(f.read_text())==plan
 else:f.write_text(json.dumps(plan,indent=2)+'\n')
 return items
async def run(limit):
 items=prepare();count=0
 for i,it in enumerate(items):
  for arm in (('control','measured_returns') if i%2==0 else ('measured_returns','control')):
   trial=copy.deepcopy(it);trial['id']=it['id']+'-'+arm;d=DATA/f'sonnet-{trial["id"]}'
   if d.exists():
    p=d/'result.json'
    if p.exists() and json.loads(p.read_text())['done']:continue
    raise RuntimeError('Inspect failed/unfinished trial; never replace')
   q=shared_quota(extra_roots=(DATA,FORECAST))
   if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',q);return
   r=await one(trial,'sonnet',prefix=prefix(it,arm),data_root=DATA,system_override=(SOURCE/'system_prompt.md').read_text());count+=1
   if not r['done'] or r['errors'] or r['invalid'] or r['skill_reads']<1 or r['model_ids']!=['claude-sonnet-5-5']:raise RuntimeError('Transport/model mismatch')
   if count>=limit:return
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--calls',type=int,default=0);a=p.parse_args()
 if a.calls:asyncio.run(run(a.calls))
 else:print({'n':len(prepare()),'quota':shared_quota(extra_roots=(DATA,FORECAST))})
