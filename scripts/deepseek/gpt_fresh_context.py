"""Same-model fresh-context second thoughts on all critical turns of a real v4 career.
No game/DeepSeek calls. Default freezes own public source panels, never prints narratives.
"""
import argparse,asyncio,copy,hashlib,json,time
from pathlib import Path
from gpt_capacity_probe import ROOT,REPORT,BUNDLE,one
from gpt_native_trace import decoded,node
from gpt_decision_audit import processes
from careerlab.mcp_client import phase
SOURCE=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1'
DATA=SOURCE.parent.with_name('gpt-fresh-context')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prefix(it):
    return ('These are the last three notes from earlier accepted actions in this same career, in chronological order. They are historical self-reports, not verified predictions and not the current choice. Read the current Skill and current observation; do not infer unobserved future events.\n'+json.dumps(it['prior_notes'],ensure_ascii=False)+'\n\n')

def prepare():
    observations=[];pending={};seen=set();obs=None;notes=[];since_observe=False
    paths=sorted(SOURCE.glob('stream-*.jsonl'))
    for path in paths:
        for line in path.open():
            try:m=json.loads(line)
            except ValueError:continue
            blocks=m.get('message',{}).get('content',[])
            if not isinstance(blocks,list):continue
            for b in blocks:
                if b.get('type')=='tool_use' and b.get('id') not in seen:
                    seen.add(b.get('id'));name=b.get('name','').split('__')[-1];args=b.get('input') or {};case=None
                    if name=='take_action' and obs:
                        month=obs['current_state']['time']['current_month']
                        if phase(obs)=='event' and month%6==5:
                            assert not since_observe,'Ambiguous source menu'
                            case={'id':hashlib.sha256(str(b['id']).encode()).hexdigest()[:16],'node':node(obs),'observe':copy.deepcopy(obs),'original_choice':args['choice'],'prior_notes':copy.deepcopy(notes[-3:]),'pre_review':True}
                        since_observe=True
                    pending[b['id']]={'name':name,'args':args,'case':case}
                elif b.get('type')=='tool_result':
                    call=pending.pop(b.get('tool_use_id'),{});o=decoded(b)
                    if not isinstance(o,dict):continue
                    if call.get('name')=='take_action' and o.get('success') is True:
                        if call.get('case'):observations.append(call['case'])
                        if call['args'].get('notes'):notes.append(call['args']['notes'])
                    if 'current_state' in o and isinstance(o['current_state'],dict) and 'status' in o['current_state']:
                        obs=o;since_observe=False
    assert len(observations)==24 and len({it['id'] for it in observations})==24
    DATA.mkdir(parents=True,exist_ok=True);p=DATA/'items.json';text=json.dumps(observations,ensure_ascii=False,indent=2)+'\n'
    if p.exists():assert p.read_text()==text,'Source cases changed'
    else:p.write_text(text)
    source_plan=json.loads((REPORT/'sonnet-reference-plan.json').read_text())
    current={str(p.relative_to(BUNDLE)):sha(p) for p in sorted(BUNDLE.rglob('*')) if p.is_file()}
    assert current==source_plan['bundle_sha256'],'Skill changed since original career'
    plan={'n':24,'max_new_reads':24,'model_alias':'sonnet','original_model':'claude-sonnet-5-5','skill':'t13-read-v4 unchanged','items_sha256':sha(p),
          'source_sha256':{str(p):sha(p) for p in paths},'system_prompt_sha256':sha(SOURCE/'system_prompt.md'),'bundle_sha256':current,
          'prefix_sha256':[hashlib.sha256(prefix(it).encode()).hexdigest() for it in observations],
          'selection':[{'id':it['id'],'month':it['observe']['current_state']['time']['current_month'],'level':it['observe']['current_state']['status']['level']} for it in observations],
          'meaning':'All24accepted story decisions immediately before reviews in the completed Sonnet-v4 career. No gold-selected mistakes. Fresh same-model read with EXACT original system prompt/Skill, current original public panel and last3prior accepted notes; no original target choice/notes, no future history. Historical first choice versus fresh-context second thought, not randomized full-career efficacy. Baseline already completed at49.95. No new games/API, no claims of transfer toDS.',
          'endpoint':'Immediate risk and avoidable growth losses. Compare all24, not just errors. Risk increase blocks admission. No game score extrapolation.',
          'limits':{'five_hour':.65,'seven_day':.45,'max_claude_processes':4,'concurrency':1}}
    p=REPORT/'fresh-context-plan.json'
    if p.exists():assert json.loads(p.read_text())==plan,'Frozen plan changed'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    return observations

def quota():
    paths=list(DATA.glob('*/stream.jsonl'))+list((DATA.parent/'gpt-fact-second-read').glob('*/stream.jsonl'))+list((DATA.parent/'gpt-narrative-ablation').glob('*/stream.jsonl'))
    for p in sorted(paths,key=lambda p:p.stat().st_mtime,reverse=True):
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:w=json.loads(line)['rate_limit_info']['unifiedWindows']
            except (ValueError,KeyError):continue
            if all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):
                age=time.time()-p.stat().st_mtime
                return {'allowed':age<3600 and w['five_hour']['utilization']<.65 and w['seven_day']['utilization']<.45,'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'age_seconds':round(age)}
    return {'allowed':False,'reason':'No fresh quota'}

async def run(limit):
    items=prepare();count=0
    for it in items:
        d=DATA/f'sonnet-{it["id"]}'
        if d.exists():
            p=d/'result.json'
            if p.exists() and json.loads(p.read_text())['done']:continue
            raise RuntimeError('Unfinished read: inspect rather than replacing')
        q=quota()
        if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',json.dumps(q),flush=True);return
        r=await one(it,'sonnet',prefix=prefix(it),data_root=DATA,system_override=(SOURCE/'system_prompt.md').read_text());count+=1
        if not r['done'] or r['invalid'] or r['errors'] or r['skill_reads']<1:raise RuntimeError('Transport failure')
        if r['model_ids']!=['claude-sonnet-5-5']:raise RuntimeError('Model mismatch')
        if count>=limit:return
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--calls',type=int,default=0);a=ap.parse_args()
    if a.calls:asyncio.run(run(a.calls))
    else:print(json.dumps({'n':len(prepare()),'quota':quota()}))
