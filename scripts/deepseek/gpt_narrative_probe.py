"""Narrative ablation. Default prepares only; --calls runs frozen isolated decisions."""
import argparse,asyncio,copy,json,time
from pathlib import Path
from gpt_narrative_cases import DATA,REPORT,prepare,mask,trial_id
from gpt_capacity_probe import one
from gpt_decision_audit import processes

def quota():
    paths=list(DATA.glob('*/stream.jsonl'))+list((DATA.parent/'gpt-learning-feedback-holdout').glob('*/stream.jsonl'))
    for p in sorted(paths,key=lambda p:p.stat().st_mtime,reverse=True):
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:w=json.loads(line)['rate_limit_info']['unifiedWindows']
            except (ValueError,KeyError):continue
            if all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):
                age=time.time()-p.stat().st_mtime
                return {'allowed':age<3600 and w['five_hour']['utilization']<.65 and w['seven_day']['utilization']<.45,
                        'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'age_seconds':round(age)}
    return {'allowed':False,'reason':'Fresh quota unavailable'}

async def run(limit):
    items=prepare();count=0
    for i,it in enumerate(items):
        for arm in (('full','options_only') if i%2==0 else ('options_only','full')):
            trial=copy.deepcopy(it);trial['id']=trial_id(it,arm)
            if arm=='options_only':trial['observe']=mask(trial['observe'])
            d=DATA/f'haiku-{trial["id"]}'
            if d.exists():
                p=d/'result.json'
                if p.exists() and json.loads(p.read_text())['done']:continue
                raise RuntimeError(f'Inspect unfinished trial, do not replace: {d}')
            q=quota()
            if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',json.dumps(q),flush=True);return
            res=await one(trial,'haiku',data_root=DATA);count+=1
            if not res['done'] or res['invalid'] or res['errors'] or res['skill_reads']<1:raise RuntimeError('Transport failure')
            if count>=limit:return
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--calls',type=int,default=0);a=ap.parse_args()
    if a.calls:asyncio.run(run(a.calls))
    else:prepare();print(json.dumps(quota()))
