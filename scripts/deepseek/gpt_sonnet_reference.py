"""One preannounced Sonnet/v4 reference career via official game tools, Max account.
No model/API calls by default. --run admits exactly one new career; never replaces an outcome.
"""
import argparse,asyncio,dataclasses,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from careerlab.actors.claude_cli import ClaudeWorkerConfig,cli_version,run_claude_episode
from careerlab.config import Settings
from gpt_capacity_probe import quota
from gpt_decision_audit import processes
DATA=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
BUNDLE=ROOT/'lab/policies-src/deepseek/t13-read-v4/bundle'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze():
    cfg=ClaudeWorkerConfig('sonnet',skills_mode='official',timeout_s=1800,cli_version=cli_version(Settings()))
    plan={'n':1,'candidate':'t13-read-v4 unchanged','actor':cfg.record(),'bundle_sha256':{str(p.relative_to(BUNDLE)):sha(p) for p in sorted(BUNDLE.rglob('*')) if p.is_file()},'script_sha256':sha(Path(__file__)),
          'rationale':'Existential capacity reference only, not a powered difference/consistency trial. Twelve matched menus show one fewer avoidable pre-review growth loss, same risk count. Test whether a full career with the stronger reader exposes a different failure. No retry or outcome replacement. No claim of DS transfer.',
          'admission_limits':{'five_hour':.65,'seven_day':.45,'require_weekly_headroom_start_at_most':.40,'max_claude_processes':4},
          'scope':'Official game tools, isolated per-career server, CLI Skill-delivery emulation. Does not emulate all 52 Jiuwen tools. No new DS API. Do not interrupt a launched game for a weak score or a budget snapshot; no following game scheduled.'}
    p=REPORT/'sonnet-reference-plan.json'
    if p.exists():assert json.loads(p.read_text())==plan,'Frozen configuration drift'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    return cfg
async def run():
    cfg=freeze();d=DATA/'run-1'
    if d.exists():raise RuntimeError('Existing run: inspect it, never start another or replace it')
    q=quota();print('ADMISSION',json.dumps(q),flush=True)
    if not q['allowed'] or q['seven_day']>.40 or processes()>=4:raise RuntimeError('Insufficient fresh quota/process headroom')
    DATA.mkdir(parents=True,exist_ok=True)
    result=await run_claude_episode(Settings(),cfg,BUNDLE,'v4-sonnet-reference-1',d)
    r=dataclasses.asdict(result)
    out={'result':{k:r[k] for k in ('job_id','outcome','quantitative_score','survival_months','steps','rejected_actions','wall_seconds')},'result_sha256':sha(d/'result.json'),'models':(r.get('actor_usage') or {}).get('models'),'ending_score':r.get('ending_score'),'periods':r.get('periods'),
         'meaning':'One Sonnet capacity reference, not evidence of repeatability or DS performance. Operational interruption is unscored, never zero.'}
    (REPORT/'sonnet-reference-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['result']),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--run',action='store_true');a=ap.parse_args()
    if a.run:asyncio.run(run())
    else:freeze();print('Plan only; no game started')
