"""Independent evidence-bound second read on frozen critical menus.
No first choice shown to critic; no new games/DeepSeek. Default freezes only.
"""
import argparse,asyncio,hashlib,json,shutil,sys,time
from pathlib import Path
from gpt_narrative_cases import ROOT,REPORT,BUNDLE,DATA as FIRST
from gpt_decision_audit import processes
sys.path.insert(0,str(ROOT/'scripts/transmision'));import runbench as RB
DATA=FIRST.with_name('gpt-fact-second-read')
FIELDS=('time_diversion','relationship_rupture','unresolved_issue','personal_payment')
PROMPT='''You are an independent second reader for a workplace career game. You have not seen another reader's choice. Examine each offered action as written, before recommending a choice.
For every action answer these concrete questions:
time_diversion: Does the action explicitly pause or delay delivery, redo or investigate work, take on extra work, learn, help with someone else's work, organise others, or hand away the player's credit?
relationship_rupture: Does the action explicitly decline someone's request, correct, accuse or report a person, exclude someone, or go over someone's head?
unresolved_issue: Does the action explicitly hide a known issue, postpone or partly fix it, use a private/unofficial workaround, or leave it unattended?
personal_payment: Does the action explicitly spend the player's own money or give up their payment?
Use yes/no/unclear. For yes, quote the smallest exact contiguous span of that action that establishes the fact. A merely plausible consequence or a fact only in the background is not enough for yes: use unclear. For no or unclear give an empty quote. Do not invent numeric game effects. These are reading facts, not claims that a hidden stat necessarily changes.
Then recommend one offered action using the installed policy reproduced below and the current public state. A recommendation does not change your evidence labels. Keep all narrative and quotes in this private response; do not write a new policy.
Return the requested JSON only.
'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
    items=[it for it in json.loads((FIRST/'items.json').read_text()) if it['pre_review']]
    assert len(items)==16
    instruction,skills=RB.load_variant(str(BUNDLE));policy=instruction+'\n\n'+'\n\n'.join(files['SKILL.md'] for _,_,files in skills)
    plan={'n':len(items),'max_cli_reads':len(items),'model_alias':'haiku','first_study_items_sha256':sha(FIRST/'items.json'),
          'selection':[it['id'] for it in items],'system_sha256':hashlib.sha256((PROMPT+policy).encode()).hexdigest(),
          'meaning':'Independent critic on the16pre-review menus of the frozen narrative study. Does not see first choice/notes. Exact action-text evidence or unclear. No gold to reader. Gate only after both collections: use critic recommendation if first choice has an explicit critical-cost flag and recommended option has no/never unclear on all growth/risk flags. Add payment guard only when current displayed wealth is nonpositive. No effect-size/power claim; no game-Q or DS transfer.',
          'gate':{'growth_flags':['time_diversion','relationship_rupture'],'risk_flag':'unresolved_issue','unknown_handling':'cannot establish safe replacement','replacement_requires_different_choice':True},
          'limits':{'five_hour':.65,'seven_day':.45,'max_claude_processes':4,'concurrency':1}}
    DATA.mkdir(parents=True,exist_ok=True);p=REPORT/'fact-second-read-plan.json'
    if p.exists():assert json.loads(p.read_text())==plan,'Frozen critic/gate changed'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    return items,PROMPT+policy

def quota():
    paths=list(DATA.glob('*/stream.jsonl'))+list(FIRST.glob('*/stream.jsonl'))
    for p in sorted(paths,key=lambda p:p.stat().st_mtime,reverse=True):
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:w=json.loads(line)['rate_limit_info']['unifiedWindows']
            except (ValueError,KeyError):continue
            if all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):
                age=time.time()-p.stat().st_mtime
                return {'allowed':age<3600 and w['five_hour']['utilization']<.65 and w['seven_day']['utilization']<.45,'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'age_seconds':round(age)}
    return {'allowed':False,'reason':'No fresh quota'}

def schema(it):
    flag={'type':'object','properties':{'answer':{'type':'string','enum':['yes','no','unclear']},'quote':{'type':'string'}},'required':['answer','quote'],'additionalProperties':False}
    ids=[c['choice'] for c in it['observe']['choices']]
    return {'type':'object','properties':{'recommended_choice':{'type':'integer','enum':ids},'options':{'type':'array','items':{'type':'object','properties':{'choice':{'type':'integer','enum':ids},**{k:flag for k in FIELDS}},'required':['choice',*FIELDS],'additionalProperties':False}}},'required':['recommended_choice','options'],'additionalProperties':False}

def validate(it,result):
    actions={c['choice']:c['action'] for c in it['observe']['choices']};opts=result['options']
    assert len(opts)==len(actions) and {r['choice'] for r in opts}==set(actions),'Option coverage'
    assert result['recommended_choice'] in actions
    for row in opts:
        for field in FIELDS:
            f=row[field];assert f['answer'] in ('yes','no','unclear')
            if f['answer']=='yes':assert f['quote'] and f['quote'] in actions[row['choice']],'Nonliteral evidence'
            else:assert f['quote']=='','Unexpected evidence for no/unclear'

async def one(it,system,data_root=None,model='haiku'):
    d=(data_root or DATA)/it['id'];d.mkdir(exist_ok=False);(d/'mcp.json').write_text('{"mcpServers":{}}')
    user=json.dumps(it['observe'],ensure_ascii=False);(d/'user_prompt.json').write_text(user);(d/'system_prompt.md').write_text(system)
    cmd=[shutil.which('claude'),'-p','--setting-sources','','--strict-mcp-config','--mcp-config',str(d/'mcp.json'),'--model',model,'--tools','','--output-format','stream-json','--verbose','--json-schema',json.dumps(schema(it)),'--no-session-persistence','--system-prompt',system,'--permission-mode','dontAsk',user]
    started=time.monotonic()
    with (d/'stream.jsonl').open('w') as out,(d/'stderr.log').open('w') as err:
        proc=await asyncio.create_subprocess_exec(*cmd,cwd=d,env=RB.env(),stdout=out,stderr=err,stdin=asyncio.subprocess.DEVNULL)
        try:await asyncio.wait_for(proc.wait(),180)
        except asyncio.TimeoutError:proc.terminate();await proc.wait()
    final=None;models=set()
    for line in (d/'stream.jsonl').read_text(errors='replace').splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        if e.get('type')=='assistant':models.add(e.get('message',{}).get('model'))
        if e.get('type')=='result':final=e
    result=final.get('structured_output') if final else None;valid=False;error=None
    try:
        assert proc.returncode==0 and final and not final.get('is_error') and result,'Incomplete structured response'
        validate(it,result);valid=True
    except (AssertionError,KeyError,TypeError) as e:error=str(e)
    record={'id':it['id'],'done':valid,'error':error,'exit_code':proc.returncode,'models':sorted(m for m in models if m),'seconds':round(time.monotonic()-started,2),'response':result}
    (d/'result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='response'}),flush=True)
    return record

async def run(limit):
    items,system=prepare();n=0
    for it in items:
        d=DATA/it['id']
        if d.exists():
            p=d/'result.json'
            if p.exists():
                old=json.loads(p.read_text())
                if old['done'] or (old['exit_code']==0 and old['error']=='Nonliteral evidence' and old['response']):continue
            raise RuntimeError('Inspect failed/unfinished response; never silently replace')
        q=quota()
        if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',json.dumps(q),flush=True);return
        r=await one(it,system);n+=1
        if not r['done'] and not (r['exit_code']==0 and r['error']=='Nonliteral evidence' and r['response']):raise RuntimeError('Critic transport/evidence failure')
        if n>=limit:return
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--calls',type=int,default=0);a=ap.parse_args()
    if a.calls:asyncio.run(run(a.calls))
    else:prepare();print(json.dumps(quota()))
