"""Archive a completed native pilot from public responses; no new game calls."""
from collections import Counter
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import statistics
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.episode import result_from_terminal
from careerlab.mcp_client import is_terminal,phase
from careerlab.store import bundle_hash


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def analyze(source,output):
    output.mkdir(parents=True,exist_ok=True)
    p=json.loads((source/'protocol.json').read_text());assert sha(source/'protocol.json')==(source/'protocol-sha256.txt').read_text().strip()
    assert bundle_hash(source/'bundle')==p['bundle_sha256']
    raw=[json.loads(line) for line in (source/'trajectory.jsonl').read_text().splitlines()]
    assert sum(r['tool']=='new_game' for r in raw)==1
    last=None;steps=[];promotions=[];reviews=[];notes=[];calls=Counter();logs=None;first=None
    for record in raw:
        calls[record['tool']]+=1
        if 'error' in record:raise ValueError('Infrastructure error: review before interpreting outcome')
        tool=record['tool'];obs=record.get('observation')
        if tool=='new_game':
            assert obs;first=obs
            assert obs['current_state']['time']['current_month']==1
        if tool=='take_action':
            assert last is not None and obs is not None
            choice=next((c for c in last['choices'] if c['choice']==record['args']['choice']),None)
            success=record['response'].get('success') is True
            if success and choice is None:raise ValueError('Unobserved or unoffered action')
            notes.append(record['args']['notes'])
            steps.append({'before':last,'after':obs,'choice':choice or {'choice':record['args']['choice']},
                'notes':record['args']['notes'],'phase':phase(last),'reply':record['response'],'applied':success,'ambiguous':False})
            before=last['current_state'];after=obs['current_state'];b=before['status']['level'];a=after['status']['level']
            if a!=b:promotions.append({'month':after['time']['current_month'],'from':b,'to':a,'step':len(steps)-1})
            for grade in re.findall(r'performance bonus \(([A-Z])\)',obs.get('events','')):
                reviews.append({'month':after['time']['current_month'],'grade':grade})
        if obs:last=obs
        if record.get('final_public_logs'):logs=record['final_public_logs'];calls['observe_automatic_after_action_or_start']=sum(r['tool'] in ('take_action','new_game') for r in raw);calls['check_latest_logs_terminal_capture']+=1
    assert first is not None and last is not None and is_terminal(last),'Pilot is not terminal'
    independent=asdict(result_from_terminal('luna-memory-one',last['current_state']['session_id'],last))
    reported=json.loads((source/'result.json').read_text())
    for key in ('outcome','survival_months','quantitative_score','ending_score','failure_reason'):assert reported[key]==independent[key]
    trajectory={'run':0,'arm':['native-Luna','champion-memory-v1'],'actor':p['model'],'initial_observation':first,'steps':steps,
        'outcome':independent['outcome'],'final':last,'logs':logs,'protocol_sha256':sha(source/'protocol.json')}
    archive=output/'public-trajectory.jsonl.gz'
    with archive.open('wb') as file:
        with gzip.GzipFile(filename='',mode='wb',fileobj=file,mtime=0) as stream:stream.write((json.dumps(trajectory,ensure_ascii=False)+'\n').encode())
    (output/'archive-sha256.txt').write_text(sha(archive)+'\n')
    for name in ('protocol.json','protocol-sha256.txt','actor-launch.json','status.json','result.json','requests.jsonl','trajectory.jsonl'):
        shutil.copyfile(source/name,output/name)
    shutil.copytree(source/'bundle',output/'frozen-bundle',dirs_exist_ok=True)
    dependencies=output/'sources';dependencies.mkdir(exist_ok=True)
    for file,digest in p['dependencies'].items():
        path=Path(file);assert sha(path)==digest;shutil.copyfile(path,dependencies/(path.parent.name+'-'+path.name))
    result={'complete':True,'new_games':1,'model_requested':p['model'],'actor_harness':p['harness'],
        'outcome':independent['outcome'],'score':independent['quantitative_score'],'survival_months':independent['survival_months'],
        'failure_reason':independent['failure_reason'],'promotions':promotions,'review_grade_messages':reviews,
        'actions':len(steps),'rejected':sum(not s['applied'] for s in steps),'public_calls':dict(calls),
        'notes':{'characters_total':sum(map(len,notes)),'characters_median':statistics.median(map(len,notes)) if notes else None,
            'characters_max':max(map(len,notes),default=0),'words_total':sum(len(n.split()) for n in notes)},
        'final_status':last['current_state']['status'],'ending_score':last.get('ending_score'),
        'raw_public_trace_sha256':sha(source/'trajectory.jsonl'),'archive_sha256':sha(archive),
        'limits':['One exploratory game, no same-model baseline or causal memory comparison','Manual note presence is not proof of correct memory; semantic audit required',
            'No native-model token/currency receipt exposed; character/word counts are not billed tokens','Different native harness from Haiku or official DeepSeek; no pooled comparison',
            'Only requested model configuration is recorded; no separate backend-resolution receipt']}
    (output/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (output/'memory-notes.json').write_text(json.dumps([{'step':i,'month':s['before']['current_state']['time']['current_month'],'notes':s['notes']} for i,s in enumerate(steps)],indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key not in ('ending_score','actor_harness')},indent=2))


if __name__=='__main__':analyze(Path(sys.argv[1]),Path(sys.argv[2]))
