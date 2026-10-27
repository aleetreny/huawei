"""Matched Haiku decision test, one recorded observation per trial. No DeepSeek client.
Narrative inputs, outputs and raw CLI streams stay outside Git. No new official games.
"""
from __future__ import annotations
import argparse,asyncio,collections,copy,gzip,hashlib,json,os,random,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/transmision'))
import runbench as RB
DATA=Path.home()/'careerlab-data/deepseek/gpt-decision-audit'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
ARMS={'native':'native-craft-v1','audit':'decisional-check-v1','repeat':'native-craft-v1'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
    bank=ROOT/'lab/data/transmision/bank-items.jsonl.gz'
    with gzip.open(bank,'rt') as f:items=[json.loads(l) for l in f]
    groups=collections.defaultdict(list)
    for it in items:
        if it['phase']=='e' and it['holdout']:groups[it['title']].append(it)
    rng=random.Random(2026102719);chosen=[]
    for title in sorted(groups):
        pool=sorted(groups[title],key=lambda x:x['id']);rng.shuffle(pool)
        a=pool[0];chosen.append(a)
        others=[it for it in pool[1:] if (it['month'],it['state']['level'])!=(a['month'],a['state']['level'])]
        if others:chosen.append(others[0])
    rng.shuffle(chosen)
    DATA.mkdir(parents=True,exist_ok=True)
    rows=[]
    for it in chosen:
        x=copy.deepcopy(it);x['serve']={'long_from':0,'month_from':0,'observes':[it['observe']], 'logs_at':[it['serve']['logs_at'][-1]]}
        rows.append(x)
    inp=DATA/'items.jsonl'
    if inp.exists():
        assert [json.loads(l)['id'] for l in inp.open()]==[r['id'] for r in rows],'Frozen selection changed'
    else:inp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    manifest={'seed':2026102719,'n_items':len(rows),'n_titles':len(groups),'bank_sha256':sha(bank),'input_sha256':sha(inp),
        'items':[{'id':r['id'],'title_sha256':hashlib.sha256(r['title'].encode()).hexdigest(),'month':r['month'],'level':r['state']['level']} for r in rows],
        'variants':{arm:{'path':name,'skill_sha256':sha(ROOT/'lab/policies-src/deepseek'/name/'bundle/skills/career-craft/SKILL.md')} for arm,name in ARMS.items()},
        'context':'one observed decision plus recorded prior logs; no forced-choice prefix transitions','model':'haiku','delivery':'official skill_tool emulation, not JiuwenSwarm target',
        'limits':{'max_five_hour':0.65,'max_weekly':0.45,'max_claude_processes':4},'repeat_ids':[r['id'] for r in rows[:24]]}
    frozen=REPORT/'decision-audit-selection.json'
    if frozen.exists():
        prior=json.loads(frozen.read_text())
        assert prior==manifest,'Selection or Skill changed after freezing; do not silently continue'
    else:frozen.write_text(json.dumps(manifest,indent=2)+'\n')
    print('Frozen selection',len(rows),'items',len(groups),'titles',flush=True)
    return rows

def processes():
    lines=subprocess.check_output(['ps','-axo','pid=,comm=,args='],text=True).splitlines();n=0
    for line in lines:
        parts=line.strip().split(None,2)
        if len(parts)<3:continue
        comm,args=Path(parts[1]).name,parts[2]
        if comm.startswith('claude') or (comm=='node' and 'claude' in args and '--output-format' in args):n+=1
    return n

def quota_status():
    latest=None
    for p in (DATA/'runs').glob('*/*/attempt-*/stream.jsonl'):
        stamp=p.stat().st_mtime
        for line in p.open(errors='replace'):
            if '"rate_limit_event"' not in line:continue
            try:d=json.loads(line).get('rate_limit_info',{})
            except ValueError:continue
            if latest is None or stamp>=latest[0]:latest=(stamp,d)
    if not latest:return {'allowed':None,'reason':'no fresh actor quota event yet'}
    d=latest[1];wins=d.get('unifiedWindows') or {};now=time.time()
    for key,limit in [('five_hour',.65),('seven_day',.45)]:
        w=wins.get(key) or {};u=w.get('utilization');reset=w.get('resetsAt')
        if u is not None and (not reset or now<float(reset)) and float(u)>=limit:
            return {'allowed':False,'reason':key,'utilization':u,'resetsAt':reset,'rate':d}
    # Unknown utilization does not silently authorize a large batch.
    known=all((wins.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day'))
    return {'allowed':True if known else None,'reason':'within caps' if known else 'missing window metrics','rate':d}

async def one(it,arm):
    name=ARMS[arm];bundle=ROOT/'lab/policies-src/deepseek'/name/'bundle'
    instruction,skills=RB.load_variant(str(bundle));sp=RB.system_prompt(instruction,skills,'official')
    base=DATA/'runs'/arm/it['id'].replace(':','_');base.mkdir(parents=True,exist_ok=True)
    work=base/f'attempt-{len(list(base.glob("attempt-*")))+1:02d}';work.mkdir()
    record=work/'record.jsonl'
    item={'record':str(record),'session_id':RB.SID,'steps':it['serve']['observes'],'logs_at':it['serve']['logs_at'],
        'handbook':(ROOT/'lab/data/transmision/handbook.md').read_text(),'skills':{n:f for n,_,f in skills}}
    (work/'item.json').write_text(json.dumps(item,ensure_ascii=False));(work/'system_prompt.md').write_text(sp)
    servers={RB.GAME:{'command':sys.executable,'args':[str(ROOT/'scripts/transmision/fake_mcp.py'),'game',str(work/'item.json')]},
             'jiuwen':{'command':sys.executable,'args':[str(ROOT/'scripts/transmision/fake_mcp.py'),'skills',str(work/'item.json')]}}
    (work/'mcp.json').write_text(json.dumps({'mcpServers':servers}))
    exe=shutil.which('claude');assert exe,'Claude CLI unavailable'
    cmd=[exe,'-p','--setting-sources','','--strict-mcp-config','--mcp-config',str(work/'mcp.json'),'--model','haiku','--tools','',
        '--allowedTools',','.join(RB.GAME_TOOLS+[RB.SKILL_TOOL]),'--output-format','stream-json','--verbose','--no-session-persistence',
        '--system-prompt',sp,'--permission-mode','dontAsk',RB.continue_prompt(it['observe'])]
    started=time.monotonic();target_seen=None
    with (work/'stream.jsonl').open('w') as out,(work/'stderr.log').open('w') as err:
        proc=await asyncio.create_subprocess_exec(*cmd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=work,env=RB.env())
        while proc.returncode is None and time.monotonic()-started<240:
            if record.exists() and '"target": true' in record.read_text():
                target_seen=target_seen or time.monotonic()
                if time.monotonic()-target_seen>1:break
            try:await asyncio.wait_for(proc.wait(),timeout=.25)
            except asyncio.TimeoutError:pass
        if proc.returncode is None:
            proc.terminate()
            try:await asyncio.wait_for(proc.wait(),timeout=10)
            except asyncio.TimeoutError:proc.kill();await proc.wait()
    events=[json.loads(l) for l in record.open()] if record.exists() else []
    tgt=[x for x in events if x.get('target') and x.get('tool')=='take_action'];usage=collections.Counter();errors=[];rates=[];models=set()
    for line in (work/'stream.jsonl').open(errors='replace'):
        try:d=json.loads(line)
        except ValueError:continue
        if d.get('type')=='assistant':
            if d.get('message',{}).get('model'):models.add(d['message']['model'])
            usage.update({k:v for k,v in (d.get('message',{}).get('usage') or {}).items() if isinstance(v,(int,float))})
        if d.get('type')=='rate_limit_event':rates.append(d.get('rate_limit_info',{}))
        if d.get('type')=='result' and d.get('is_error'):errors.append(str(d.get('result'))[:300])
    res={'id':it['id'],'arm':arm,'done':bool(tgt),'choice':tgt[0]['choice'] if tgt else None,'notes':tgt[0].get('notes') if tgt else None,
         'seconds':round(time.monotonic()-started,2),'model_ids':sorted(models),'exit_code':proc.returncode,'usage':dict(usage),'rate':rates[-1] if rates else None,'errors':errors,
         'skill_reads':sum(x.get('tool')=='skill_tool' for x in events),'invalid':sum(x.get('invalid',False) for x in events),'raw':str(work)}
    (base/'result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:res[k] for k in ('id','arm','done','choice','seconds','skill_reads','invalid')},ensure_ascii=False),flush=True)
    return res

async def run(calls):
    rows=prepare();todo=[]
    for i,it in enumerate(rows):
        for arm in (('native','audit') if i%2==0 else ('audit','native')):todo.append((it,arm))
    todo.extend((it,'repeat') for it in rows[:24]);count=0
    for it,arm in todo:
        target=DATA/'runs'/arm/it['id'].replace(':','_')/'result.json'
        if target.exists():
            if json.loads(target.read_text()).get('done'):continue
            raise RuntimeError(f'Unsuccessful existing result; inspect before retry: {target}')
        q=quota_status()
        if q['allowed'] is False or (q['allowed'] is None and any((DATA/'runs').glob('*/*/result.json'))):
            print('QUOTA_STOP',json.dumps(q),flush=True);break
        if processes()>=4:print('PROCESS_STOP four Claude processes already active',flush=True);break
        res=await one(it,arm);count+=1
        if not res['done'] or res['invalid'] or res['errors']:print('TRANSPORT_STOP inspect raw run before retry',flush=True);break
        if count>=calls:break
    print('Run ended',json.dumps({'new_calls':count,'quota':quota_status()}),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--calls',type=int,default=1);a=ap.parse_args();asyncio.run(run(a.calls))
