"""Four full Haiku careers, isolated official tools. Never imports a DeepSeek client.
Default freezes/inspects only; --run executes unfinished pilots with fail-closed quota guards.
"""
from __future__ import annotations
import argparse,asyncio,dataclasses,hashlib,json,os,signal,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from careerlab.actors.claude_cli import ClaudeWorkerConfig,cli_version,run_claude_episode
from careerlab.config import Settings
from gpt_decision_audit import processes
DATA=Path.home()/'careerlab-data/deepseek/gpt-native-pilot'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
BUNDLE=ROOT/'lab/policies-src/deepseek/native-craft-v1/bundle'
N=4

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quota():
    streams=list(DATA.glob('game-*/stream-*.jsonl'))+list((Path.home()/'careerlab-data/deepseek/gpt-decision-audit/runs').glob('*/*/attempt-*/stream.jsonl'))
    streams.sort(key=lambda p:p.stat().st_mtime,reverse=True)
    for p in streams:
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:rate=json.loads(line)['rate_limit_info'];w=rate.get('unifiedWindows') or {}
            except (ValueError,KeyError):continue
            if not all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):continue
            age=time.time()-p.stat().st_mtime
            allowed=age<3600 and all(float(w[k]['utilization'])<cap for k,cap in [('five_hour',.65),('seven_day',.45)])
            return {'allowed':allowed,'age_seconds':round(age),'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'source':str(p)}
    return {'allowed':False,'reason':'no recent measured quota'}

def freeze():
    DATA.mkdir(parents=True,exist_ok=True)
    cfg=ClaudeWorkerConfig('haiku',skills_mode='official',timeout_s=1800,cli_version=cli_version(Settings()))
    out={'n':N,'candidate':'native-craft-v1','actor':cfg.record(),'skill_sha256':sha(BUNDLE/'skills/career-craft/SKILL.md'),'manifest_sha256':sha(BUNDLE/'manifest.json'),
         'script_sha256':sha(Path(__file__)),'design':'Four independent unseeded official dev careers, no paired historical causal comparison. Screening only. Report every terminal score, operational interruptions separately. No optional replacement of low scores.',
         'sample_rationale':'n=4 can screen a large ~20-point route relative to historical 50–60 (SE~5 at SD10); too small to certify consistency or a narrow improvement. No blind claim from historical comparison.',
         'admission':'92 valid fresh native Haiku decisions, 4 positive-risk actions, 3 immediate dominated. This admits an end-to-end characterization, not an efficacy claim over current Skills.',
         'limits':{'five_hour':.65,'seven_day':.45,'max_processes':4,'concurrency':1,'max_new_games':N},'data':str(DATA)}
    p=REPORT/'native-pilot-plan.json'
    if p.exists():assert json.loads(p.read_text())==out,'Frozen plan changed; inspect before any call'
    else:p.write_text(json.dumps(out,indent=2)+'\n')
    return cfg

def summary():
    rows=[]
    for i in range(N):
        p=DATA/f'game-{i+1}'/'result.json'
        if not p.exists():continue
        r=json.loads(p.read_text());usage=r.get('actor_usage') or {}
        rows.append({k:r.get(k) for k in ('job_id','outcome','quantitative_score','survival_months','steps','rejected_actions','wall_seconds')}|{'source_sha256':sha(p),'models':usage.get('models'),'rate_limit_last':usage.get('rate_limit_last')})
    # Model usage and quota are numeric metadata; no game narrative copied.
    out={'n_requested':N,'n_finished_processes':len(rows),'rows':rows,'quota':quota(),'meaning':'Actual Haiku full-career scores; no DeepSeek transfer established. Operational interruptions have no imputed score.'}
    (REPORT/'native-pilot-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'}),flush=True)
    for r in rows:print(json.dumps({k:v for k,v in r.items() if k not in ('models','rate_limit_last')}),flush=True)

async def child(i):
    cfg=freeze();d=DATA/f'game-{i}'
    result=await run_claude_episode(Settings(),cfg,BUNDLE,f'native-craft-pilot-{i}',d)
    print(json.dumps({'game':i,'outcome':result.outcome,'Q':result.quantitative_score}),flush=True)

async def run():
    freeze()
    for i in range(1,N+1):
        d=DATA/f'game-{i}'
        if (d/'result.json').exists():continue
        if d.exists():raise RuntimeError(f'Unfinished game, do not restart or replace: {d}')
        q=quota();print('ADMISSION',json.dumps(q),flush=True)
        if not q['allowed'] or processes()>=4:break
        log=DATA/f'launcher-{i}.log'
        with log.open('w') as f:
            proc=await asyncio.create_subprocess_exec(sys.executable,str(Path(__file__).resolve()),'--child',str(i),stdout=f,stderr=f,start_new_session=True,cwd=ROOT)
            while proc.returncode is None:
                try:await asyncio.wait_for(proc.wait(),timeout=3)
                except asyncio.TimeoutError:pass
                q=quota()
                if proc.returncode is None and not q['allowed']:
                    os.killpg(proc.pid,signal.SIGTERM)
                    try:await asyncio.wait_for(proc.wait(),timeout=10)
                    except asyncio.TimeoutError:os.killpg(proc.pid,signal.SIGKILL);await proc.wait()
                    (DATA/f'quota-stop-{i}.json').write_text(json.dumps(q,indent=2))
                    print('QUOTA_STOP',json.dumps(q),flush=True);summary();return
        if proc.returncode!=0:print('TRANSPORT_STOP',i,proc.returncode,flush=True);break
        summary()
        result=json.loads((d/'result.json').read_text())
        if result['outcome']=='interrupted':break
    summary()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run',action='store_true');ap.add_argument('--child',type=int);a=ap.parse_args()
    if a.child:
        assert 1<=a.child<=N
        asyncio.run(child(a.child))
    elif a.run:asyncio.run(run())
    else:freeze();summary()
