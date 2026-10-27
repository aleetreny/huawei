"""Fresh-process, structured Luna prefix probes; no live game calls or API keys."""
from __future__ import annotations
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time


SCHEMA = {'type':'object','additionalProperties':False,'properties':{
    'answer':{'type':'string'},'evidence_ids':{'type':'array','items':{'type':'string'}},
    'choice':{'type':'integer'},'updated_note':{'type':'string'},'request_logs':{'type':'boolean'}},
    'required':['answer','evidence_ids','choice','updated_note','request_logs']}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def prompt_for(case, condition, skill, recovery=None):
    payload={'current':case['current'],'question':case['question'],'checkpoint':None,'public_history':[],
             'logs_available_on_request':condition=='stale_recovery' and recovery is None}
    if condition=='full_history':
        payload['public_history']=case['history']
    elif condition=='curated_checkpoint':
        payload['checkpoint']=case['checkpoint']
    elif condition=='stale_recovery':
        payload['checkpoint']=case['stale_checkpoint']
    if recovery is not None:
        payload['previous_response']=recovery
        payload['public_history']=case['history']
    return ('You are evaluating a Career Survival public career prefix, not playing a live game. '
        'Use only the public evidence supplied below. Do not call tools, read files, browse, execute code, or contact any service. '
        'Historical statements have their original time; current observations override stale numeric values. '
        'Answer the factual question exactly in its requested format. Use "unknown" if the available evidence does not establish the answer; do not guess. '
        'Cite record IDs that support your answer. A curated checkpoint may be cited as CHECKPOINT; its source IDs are provenance. '
        'An old checkpoint is not necessarily current. If logs are available and needed, set request_logs=true; there is at most one recovery round. '
        'Select one legally offered current choice using the fixed Skill. This choice will not be executed. '
        'Write an updated factual checkpoint of at most 800 characters, separating observed facts from expectations. '
        'Return only the requested JSON, with no private reasoning.\n\nFIXED SKILL:\n'+skill+
        '\n\nPUBLIC EVIDENCE:\n'+json.dumps(payload,ensure_ascii=False,separators=(',',':')))


async def request(root, protocol, job, prompt, stage):
    directory=root/'responses'/f'{job:03d}-{stage}'
    directory.mkdir(parents=True,exist_ok=False)
    (directory/'prompt.txt').write_text(prompt)
    command=[shutil.which('codex'),'exec','--ignore-user-config','--ignore-rules','--ephemeral',
             '--skip-git-repo-check','--sandbox','read-only','--model',protocol['model'],
             '-c','model_reasoning_effort='+protocol['reasoning_effort'],'-c','project_doc_max_bytes=0',
             '-c','features.shell_tool=false','-c','features.multi_agent=false','--cd',str(root/'empty-workspace'),
             '--output-schema',str(root/'response-schema.json'),'--json','-']
    start=time.monotonic()
    proc=await asyncio.create_subprocess_exec(*command,stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,
        env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_API_KEY','ANTHROPIC_API_KEY'))})
    error=None
    try:
        stdout,stderr=await asyncio.wait_for(proc.communicate(prompt.encode()),protocol['max_seconds_per_request'])
    except asyncio.TimeoutError:
        proc.kill();stdout,stderr=await proc.communicate();error='request_timeout'
    events,answer,usage,tool_attempts=[],None,{},[]
    for line in stdout.decode(errors='replace').splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        kind=e.get('type','');item=e.get('item',{})
        if kind in ('turn.completed','turn.failed','thread.started','error'):
            events.append(e)
        if kind=='turn.completed':usage=e.get('usage',{})
        if kind=='item.completed' and item.get('type')=='agent_message':
            events.append(e)
            try:answer=json.loads(item['text'])
            except (ValueError,KeyError):pass
        if kind.startswith('item.') and item.get('type') not in ('agent_message','reasoning',None):
            tool_attempts.append({'event':kind,'item_type':item.get('type')})
    if proc.returncode!=0:error=error or 'cli_error'
    if answer is None:error=error or 'no_answer'
    if tool_attempts:error='unexpected_tool_use'
    result={'at':datetime.now(timezone.utc).isoformat(),'job':job,'stage':stage,'model_requested':protocol['model'],
            'elapsed_seconds':time.monotonic()-start,'exit_code':proc.returncode,'error':error,
            'usage':usage,'answer':answer,'tool_attempts':tool_attempts,'prompt_sha256':sha(directory/'prompt.txt'),
            'stderr_tail':stderr.decode(errors='replace')[-1500:]}
    (directory/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n')
    (directory/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


async def run(root):
    protocol=json.loads((root/'protocol.json').read_text())
    for name,key in (('cases.json','case_sha256'),('schedule.json','schedule_sha256'),('frozen-skill.md','skill_sha256')):
        assert sha(root/name)==protocol[key], f'Frozen {name} changed'
    assert not (root/'responses').exists(),'Do not silently resume or replace a benchmark'
    (root/'responses').mkdir();(root/'empty-workspace').mkdir()
    (root/'response-schema.json').write_text(json.dumps(SCHEMA))
    cases={c['id']:c for c in json.loads((root/'cases.json').read_text())}
    skill=(root/'frozen-skill.md').read_text()
    schedule=json.loads((root/'schedule.json').read_text())
    used={'input_tokens':0,'output_tokens':0,'cached_input_tokens':0,'reasoning_output_tokens':0,'requests':0}
    lock=asyncio.Lock();cursor=0;stop=[];completed=[]
    manifest={'runner_sha256':sha(Path(__file__)),'protocol_sha256':sha(root/'protocol.json'),
              'cli_version':(await asyncio.create_subprocess_exec('codex','--version',stdout=asyncio.subprocess.PIPE))}
    version=await manifest.pop('cli_version').communicate()
    manifest['cli_version']=version[0].decode().strip();manifest['started_at']=datetime.now(timezone.utc).isoformat()
    (root/'execution.json').write_text(json.dumps(manifest,indent=2)+'\n')
    async def account(r):
        async with lock:
            used['requests']+=1
            for k in ('input_tokens','output_tokens','cached_input_tokens','reasoning_output_tokens'):
                used[k]+=int(r['usage'].get(k) or 0)
            if r['error']:
                stop.append({'reason':r['error'],'job':r['job'],'stage':r['stage']})
            if used['input_tokens']>=protocol['max_total_input_tokens'] or used['output_tokens']+used['reasoning_output_tokens']>=protocol['max_total_output_tokens']:
                stop.append({'reason':'token_ceiling'})
            if used['requests']>=protocol['max_model_requests']:
                stop.append({'reason':'request_ceiling'})
    async def worker():
        nonlocal cursor
        while True:
            async with lock:
                if stop or cursor>=len(schedule):return
                index=cursor;cursor+=1
            item=schedule[index];case=cases[item['case_id']]
            first=await request(root,protocol,index,prompt_for(case,item['condition'],skill),'initial')
            await account(first)
            final=first
            if not first['error'] and item['condition']=='stale_recovery' and first['answer'].get('request_logs') and not stop:
                final=await request(root,protocol,index,prompt_for(case,item['condition'],skill,recovery=first['answer']),'recovery')
                await account(final)
            row={'position':index,**item,'first':first,'final':final,'recovered':final is not first}
            async with lock:
                completed.append(row)
                (root/'completed.json').write_text(json.dumps(sorted(completed,key=lambda x:x['position']),ensure_ascii=False,indent=2)+'\n')
                status={'completed':len(completed),'assigned':cursor,'target':len(schedule),'usage':used,'stop_reasons':stop}
                (root/'status.json').write_text(json.dumps(status,indent=2)+'\n')
                if len(completed)%12==0 or stop:print(json.dumps(status),flush=True)
    await asyncio.gather(*(worker() for _ in range(protocol['concurrency'])))
    print(json.dumps({'finished':len(completed)==len(schedule),'completed':len(completed),'usage':used,'stop':stop}),flush=True)


if __name__=='__main__':
    asyncio.run(run(Path(sys.argv[1]).resolve()))
