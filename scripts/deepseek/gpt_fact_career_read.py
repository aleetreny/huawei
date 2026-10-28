"""Same evidence reader on all24real critical turns; default freezes without calls."""
import argparse,asyncio,hashlib,json
from gpt_fresh_context import DATA as SOURCE,REPORT,quota as shared_quota
from gpt_fact_second_read import prepare as critic_prepare,one
from gpt_decision_audit import processes
DATA=SOURCE.with_name('gpt-fact-career-read')
def quota():return shared_quota(extra_roots=(DATA,))
def prepare():
    _,system=critic_prepare();p=SOURCE/'items.json';items=json.loads(p.read_text());assert len(items)==24
    DATA.mkdir(parents=True,exist_ok=True)
    plan={'n':24,'max_reads':24,'model':'sonnet','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'system_sha256':hashlib.sha256(system.encode()).hexdigest(),
          'scope':'Same factual questions and gate as previous study; all24critical real-career turns, no selection by gold. Same model family as original career. Current panel only; critic never sees original target choice/notes. Historical comparison, not randomized career efficacy. Nonliteral evidence retained and falls back to first choice; never repaired/retried. Other transport errors stop. No games or DeepSeek.',
          'gate':'Reuse gpt_fact_second_score.select unchanged; risk increase blocks admission.', 'limits':{'five_hour':.65,'seven_day':.45,'processes':4}}
    f=REPORT/'fact-career-plan.json'
    if f.exists():assert json.loads(f.read_text())==plan
    else:f.write_text(json.dumps(plan,indent=2)+'\n')
    return items,system
async def run(limit):
    items,system=prepare();count=0
    for it in items:
        d=DATA/it['id']
        if d.exists():
            p=d/'result.json'
            if p.exists():
                r=json.loads(p.read_text())
                if r['done'] or (r['exit_code']==0 and r['error']=='Nonliteral evidence' and r['response']):continue
            raise RuntimeError('Inspect unfinished response, never replace')
        q=quota()
        if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',q);return
        r=await one(it,system,data_root=DATA,model='sonnet');count+=1
        if not r['done'] and not (r['exit_code']==0 and r['error']=='Nonliteral evidence' and r['response']):raise RuntimeError('Transport failure')
        if count>=limit:return
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--calls',type=int,default=0);a=p.parse_args()
    if a.calls:asyncio.run(run(a.calls))
    else:print({'n':len(prepare()[0]),'quota':quota()})
