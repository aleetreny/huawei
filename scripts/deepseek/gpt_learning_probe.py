"""Matched experience-feedback diagnostic. Actual earlier public outcomes, no hidden effects.
Default prepares only; --calls runs up to the frozen maximum through the existing isolated actor.
"""
import argparse,asyncio,copy,hashlib,json,time
from pathlib import Path
from gpt_learning_cases import prepare,DATA,REPORT,ROOT
from gpt_capacity_probe import one,BUNDLE
from gpt_decision_audit import processes

def quota():
    paths=list(DATA.glob('*/stream.jsonl'))+list((Path.home()/'careerlab-data/deepseek/gpt-capacity-probe').glob('*/stream.jsonl'))+list((Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1').glob('stream-*.jsonl'))
    for p in sorted(paths,key=lambda p:p.stat().st_mtime,reverse=True):
        for line in reversed(p.read_text(errors='replace').splitlines()):
            if '"rate_limit_event"' not in line:continue
            try:w=json.loads(line)['rate_limit_info']['unifiedWindows']
            except (ValueError,KeyError):continue
            if all((w.get(k) or {}).get('utilization') is not None for k in ('five_hour','seven_day')):
                age=time.time()-p.stat().st_mtime
                return {'allowed':age<3600 and w['five_hour']['utilization']<.65 and w['seven_day']['utilization']<.45,'five_hour':w['five_hour']['utilization'],'seven_day':w['seven_day']['utilization'],'age_seconds':round(age)}
    return {'allowed':False,'reason':'No fresh quota'}

def prefix(it,arm):
    t=it['teacher'];history={k:t[k] for k in ('event','choices','chosen','before','own_prediction')}
    if arm=='observed_outcome':history['after_observed']=t['after']
    return ('The following is a recorded EARLIER episode from this career, not the current menu. It is factual history, including a recorded prediction. '
            'Check that prediction against an observed outcome when one is supplied; preserve uncertainty when it is absent. Use any relevant lesson in the current decision. '
            'Do not write a new manual or memorize an answer. Read the current Skill and call observe to get the CURRENT menu.\n'
            +json.dumps(history,ensure_ascii=False)+'\n\n')

def freeze(holdout=False):
    rows=prepare(holdout);plan={'arms':['history_only','observed_outcome'],'n_calls_max':len(rows)*2,'model_alias':'haiku','bundle_sha256':{str(p.relative_to(BUNDLE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(BUNDLE.rglob('*')) if p.is_file()},
                       'prefix_sha256':{arm:[hashlib.sha256(prefix(it,arm).encode()).hexdigest() for it in rows] for arm in ('history_only','observed_outcome')},'limits':{'five_hour':.65,'seven_day':.45,'max_claude_processes':4,'concurrency':1},
                       'scope':'Same actual earlier history in both arms; only the after panel differs. No true engine labels, thresholds or hidden risk given. This is native belief revision across different event titles, not the numeric ceiling calibrator or another self-check of the same proposed answer.'}
    p=REPORT/('learning-feedback-holdout-transport-plan.json' if holdout else 'learning-feedback-transport-plan.json')
    if p.exists():assert json.loads(p.read_text())==plan,'Frozen prompts/bundle changed'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    return rows

async def run(calls,holdout=False):
    rows=freeze(holdout);count=0
    for i,it in enumerate(rows):
        for arm in (('history_only','observed_outcome') if i%2==0 else ('observed_outcome','history_only')):
            trial=copy.deepcopy(it);trial['id']=it['id']+'-'+arm;d=DATA/f'haiku-{trial["id"]}'
            if d.exists():
                r=d/'result.json'
                if r.exists() and json.loads(r.read_text())['done']:continue
                raise RuntimeError(f'Unfinished trial: {d}')
            q=quota()
            if not q['allowed'] or processes()>=4:print('ADMISSION_STOP',json.dumps(q),flush=True);return
            r=await one(trial,'haiku',prefix=prefix(it,arm),data_root=DATA);count+=1
            if not r['done'] or r['invalid'] or r['errors']:raise RuntimeError('Transport failure: inspect before retry')
            if count>=calls:return
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--calls',type=int,default=0);ap.add_argument('--holdout',action='store_true');a=ap.parse_args()
    if a.holdout:DATA=DATA.with_name(DATA.name+'-holdout')
    if a.calls:asyncio.run(run(a.calls,a.holdout))
    else:freeze(a.holdout);print(json.dumps(quota()))
