"""Matched one-step Haiku/Sonnet capacity diagnostic, same frozen v4 Skill and menus.
A READY probe obtains fresh Max quota before admitting any game-menu calls. No DeepSeek client.
"""
from __future__ import annotations
import argparse,asyncio,copy,hashlib,json,random,shutil,subprocess,sys,time
from pathlib import Path
from gpt_format_trace import ROOT,DATA as SOURCES,records,node,sha
from gpt_decision_audit import processes
sys.path.insert(0,str(ROOT/'scripts/transmision'));import runbench as RB
DATA=Path.home()/'careerlab-data/deepseek/gpt-capacity-probe'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
BUNDLE=ROOT/'lab/policies-src/deepseek/t13-read-v4/bundle'

def prepare():
    pool={False:{},True:{}};sourcehashes={}
    for p in sorted(SOURCES.glob('sv[13]-g*/output/events-*.jsonl')):
        rows,*_=records(p);sourcehashes[str(p)]=sha(p)
        for r in rows:
            if not r.get('accepted') or not r['obs']:continue
            o=r['obs'];status=o['current_state']['status'];m=o['current_state']['time']['current_month']
            if str(status['level'])!='L1' or o.get('current_event',{}).get('document') or 'remaining_energy' in o.get('current_event',{}) or 'max_selections' in o.get('current_event',{}):continue
            if len(o.get('choices') or [])<2:continue
            n=node(o);pool[m%6==5].setdefault(n,o)
    rng=random.Random(2026102809);chosen=[]
    for pre in (True,False):
        keys=sorted(pool[pre]);rng.shuffle(keys)
        for n in keys:
            if n not in {r['node'] for r in chosen}:chosen.append({'id':n,'node':n,'observe':pool[pre][n],'pre_review':pre})
            if sum(x['pre_review']==pre for x in chosen)==6:break
    assert len(chosen)==12,'Expected six unique pre-review and six other menus'
    rng.shuffle(chosen);DATA.mkdir(parents=True,exist_ok=True);p=DATA/'items.json';content=json.dumps(chosen,ensure_ascii=False,indent=2)+'\n'
    if p.exists():assert p.read_text()==content,'Frozen cases drifted'
    else:p.write_text(content)
    plan={'n_items':12,'n_calls_max':25,'models':['haiku','sonnet'],'source_sha256':sourcehashes,'items_sha256':sha(p),'seed':2026102809,
          'selection':[{'id':r['id'],'pre_review':r['pre_review']} for r in chosen],
          'bundle_files_sha256':{str(p.relative_to(BUNDLE)):sha(p) for p in sorted(BUNDLE.rglob('*')) if p.is_file()},
          'meaning':'Capacity diagnostic, 12 L1 menus balanced by public pre-review timing, selected without effect labels. Both models fresh same Skill/current panel, no prior logs supplied. Not a full career, score or claim of DS transfer. Never promote from n12 alone.',
          'limits':{'five_hour':.65,'seven_day':.45,'max_claude_processes':4,'concurrency':1}}
    p=REPORT/'capacity-probe-plan.json'
    if p.exists():assert json.loads(p.read_text())==plan,'Plan drift'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    return chosen

def quota():
    paths=sorted(DATA.glob('*/stream.jsonl'),key=lambda p:p.stat().st_mtime,reverse=True)
    for p in paths:
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:d=json.loads(line)['rate_limit_info'];w=d.get('unifiedWindows') or {}
            except (ValueError,KeyError):continue
            if all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):
                age=time.time()-p.stat().st_mtime
                return {'allowed':age<3600 and w['five_hour']['utilization']<.65 and w['seven_day']['utilization']<.45,'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'age_seconds':round(age)}
    return {'allowed':False,'reason':'Fresh quota not known'}

async def one(it,model,probe=False,prefix='',data_root=None,system_override=None):
    d=(data_root or DATA)/('admission' if probe else f'{model}-{it["id"]}');d.mkdir(exist_ok=False);record=d/'record.jsonl'
    instruction,skills=RB.load_variant(str(BUNDLE));sp='Reply with READY only.' if probe else RB.system_prompt(instruction,skills,'official')
    if system_override is not None:sp=system_override
    config={'mcpServers':{}}
    if not probe:
        item={'record':str(record),'session_id':RB.SID,'steps':[it['observe']],'logs_at':[[]],'handbook':(ROOT/'lab/data/transmision/handbook.md').read_text(),'skills':{n:f for n,_,f in skills}}
        (d/'item.json').write_text(json.dumps(item,ensure_ascii=False))
        for server,mode in [(RB.GAME,'game'),('jiuwen','skills')]:config['mcpServers'][server]={'command':sys.executable,'args':[str(ROOT/'scripts/transmision/fake_mcp.py'),mode,str(d/'item.json')]}
    (d/'mcp.json').write_text(json.dumps(config));cmd=[shutil.which('claude'),'-p','--setting-sources','','--strict-mcp-config','--mcp-config',str(d/'mcp.json'),'--model',model,'--tools','','--output-format','stream-json','--verbose','--no-session-persistence','--system-prompt',sp,'--permission-mode','dontAsk']
    if not probe:
        index=cmd.index('--output-format')
        cmd[index:index]=['--allowedTools',','.join(RB.GAME_TOOLS+[RB.SKILL_TOOL])]
    user_prompt='Reply READY.' if probe else prefix+RB.continue_prompt(it['observe'])
    (d/'user_prompt.txt').write_text(user_prompt)
    (d/'system_prompt.md').write_text(sp)
    cmd+=[user_prompt]
    started=time.monotonic()
    with (d/'stream.jsonl').open('w') as f,(d/'stderr.log').open('w') as err:
        proc=await asyncio.create_subprocess_exec(*cmd,stdout=f,stderr=err,stdin=subprocess.DEVNULL,cwd=d,env=RB.env());seen=None
        while proc.returncode is None and time.monotonic()-started<180:
            if not probe and record.exists() and '"target": true' in record.read_text():
                seen=seen or time.monotonic()
                if time.monotonic()-seen>1:break
            try:await asyncio.wait_for(proc.wait(),timeout=.25)
            except asyncio.TimeoutError:pass
        if proc.returncode is None:
            proc.terminate()
            try:await asyncio.wait_for(proc.wait(),timeout=10)
            except asyncio.TimeoutError:proc.kill();await proc.wait()
    events=[json.loads(l) for l in record.open()] if record.exists() else [];targets=[e for e in events if e.get('target') and e.get('tool')=='take_action'];models=set();ready=False;errors=[]
    for l in (d/'stream.jsonl').read_text(errors='replace').splitlines():
        try:v=json.loads(l)
        except ValueError:continue
        if v.get('type')=='assistant':
            models.add(v.get('message',{}).get('model'))
            ready|=any(b.get('type')=='text' and 'READY' in b.get('text','') for b in v.get('message',{}).get('content',[]))
        if v.get('type')=='result' and v.get('is_error'):errors.append(str(v.get('result'))[:150])
    r={'id':it.get('id') if it else 'admission','model_alias':model,'model_ids':sorted(m for m in models if m),'done':ready if probe else bool(targets),'choice':targets[0]['choice'] if targets else None,'skill_reads':sum(e.get('tool')=='skill_tool' for e in events),'invalid':sum(bool(e.get('invalid')) for e in events),'seconds':round(time.monotonic()-started,2),'exit_code':proc.returncode,'errors':errors}
    (d/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);return r

async def run(limit,admit):
    rows=prepare();count=0
    if admit:
        assert not (DATA/'admission').exists(),'Inspect existing admission instead of repeating'
        if processes()>=4:raise RuntimeError('Four Claude processes already active')
        await one(None,'sonnet',True);print('QUOTA',json.dumps(quota()),flush=True);return
    for i,it in enumerate(rows):
        for model in (('haiku','sonnet') if i%2==0 else ('sonnet','haiku')):
            d=DATA/f'{model}-{it["id"]}'
            if d.exists():
                p=d/'result.json'
                if p.exists() and json.loads(p.read_text())['done']:continue
                raise RuntimeError(f'Unfinished trial; inspect, do not replace: {d}')
            q=quota()
            if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',json.dumps(q),flush=True);return
            r=await one(it,model);count+=1
            if not r['done'] or r['invalid'] or r['errors']:raise RuntimeError('Trial transport failure')
            if count>=limit:return
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--admit',action='store_true');ap.add_argument('--calls',type=int,default=0);a=ap.parse_args()
    if a.admit or a.calls:asyncio.run(run(a.calls,a.admit))
    else:prepare();print(json.dumps(quota()))
