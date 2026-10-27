"""Deterministic answer/support scoring and public, reproducible result archive."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import shutil
import statistics
import sys


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical(value):
    return str(value).strip().casefold()


def score(case, condition, response, recovered=False):
    answer=response.get('answer') or {}
    value=canonical(answer.get('answer',''))
    raw_match=value==canonical(case['answer'])
    ids=set(answer.get('evidence_ids') or [])
    history_present=condition=='full_history' or recovered
    available={'CURRENT'}
    if history_present:available.update(r['id'] for r in case['history'])
    if condition=='curated_checkpoint':available.add('CHECKPOINT')
    if condition=='stale_recovery':available.add('OLD_CHECKPOINT')
    valid_ids=ids<=available
    def equivalent_sources(source_id):
        original=next((r for r in case['history'] if r['id']==source_id),None)
        if original is None or original['kind']!='observe':return {source_id}
        return {r['id'] for r in case['history'] if r['kind']=='observe' and r['data']==original['data']}
    support=False
    if case['category']=='fresh_over_stale':
        support='CURRENT' in ids or (history_present and case['support'] in ids)
    if condition=='curated_checkpoint' and 'CHECKPOINT' in ids:
        support=True
    if history_present:
        if case['category']=='incident_history':
            if case['answer']=='yes':
                sources={r['id'] for r in case['history'] if r['kind']=='observe' and 'Old landmines' in r['data'].get('events','')}
                support=bool(sources&ids)
            else:
                support=bool(ids&available)
        elif case['category']=='observed_payoff':
            support=bool(ids&equivalent_sources(case['support'])) and bool(ids&equivalent_sources(case['related_support'])) and len(ids)>=2
        elif case['category']!='unknown':
            support=support or bool(equivalent_sources(case['support'])&ids)
    unknown=case['answer']=='unknown'
    supported=raw_match and valid_ids and (unknown or support)
    legal={c['choice'] for c in case['current']['data']['choices']}
    note=answer.get('updated_note','')
    answerable=unknown or case['category']=='fresh_over_stale' or history_present or condition=='curated_checkpoint'
    return {'raw_correct':raw_match,'supported_correct':supported,'is_unknown_case':unknown,
            'abstained':value=='unknown','available_evidence_sufficient':answerable,
            'calibrated_correct':supported if answerable else value=='unknown' and valid_ids,
            'unsupported_nonabstention':value!='unknown' and not (raw_match and valid_ids and support),
            'invalid_citation':not valid_ids,'legal_choice':answer.get('choice') in legal,
            'note_within_800':isinstance(note,str) and 0<len(note)<=800,
            'note_characters':len(note) if isinstance(note,str) else None,
            'choice':answer.get('choice'),'model_error':response.get('error'),
            'request_logs':bool(answer.get('request_logs'))}


def summarize(rows):
    out={'n':len(rows)}
    for key in ('raw_correct','supported_correct','calibrated_correct','abstained','unsupported_nonabstention',
                'invalid_citation','legal_choice','note_within_800','request_logs'):
        out[key]=sum(bool(r[key]) for r in rows)
    known=[r for r in rows if not r['is_unknown_case']]
    unknown=[r for r in rows if r['is_unknown_case']]
    out['known_facts']={'n':len(known),'raw_correct':sum(r['raw_correct'] for r in known),'supported_correct':sum(r['supported_correct'] for r in known)}
    out['unknown_facts']={'n':len(unknown),'correct_abstentions':sum(r['raw_correct'] for r in unknown)}
    return out


def bootstrap_contrast(rows,cases,a,b):
    per_case={}
    for cid,case in cases.items():
        if case['answer']=='unknown':continue
        av=[r['supported_correct'] for r in rows if r['case_id']==cid and r['condition']==a]
        bv=[r['supported_correct'] for r in rows if r['case_id']==cid and r['condition']==b]
        if len(av)==len(bv)==3:per_case[cid]=statistics.mean(av)-statistics.mean(bv)
    groups=defaultdict(list)
    for cid,d in per_case.items():groups[cases[cid]['family']].append(d)
    rng=random.Random(271028);draws=[];values=list(groups.values())
    for _ in range(5000):
        sampled=[d for group in rng.choices(values,k=len(values)) for d in group]
        draws.append(statistics.mean(sampled))
    draws.sort()
    return {'a':a,'b':b,'case_count':len(per_case),'family_clusters':len(groups),
            'difference':statistics.mean(per_case.values()),'exploratory_family_bootstrap_95':[draws[125],draws[4874]],
            'limits':'Purposive fixed sample; correlated replications; no population or promotion guarantee, unadjusted interval'}


def analyze(root,out):
    out.mkdir(parents=True,exist_ok=True)
    p=json.loads((root/'protocol.json').read_text())
    assert sha(root/'protocol.json')==(root/'protocol-sha256.txt').read_text().strip()
    for f,key in (('cases.json','case_sha256'),('schedule.json','schedule_sha256'),('frozen-skill.md','skill_sha256'),('scoring-frozen.json','scoring_sha256')):
        assert sha(root/f)==p[key]
    cases={c['id']:c for c in json.loads((root/'cases.json').read_text())}
    completed=json.loads((root/'completed.json').read_text());schedule=json.loads((root/'schedule.json').read_text())
    rows,initials,usage=[],[],Counter();requests=set();prompt_checks=0;max_character_prompt=0
    usage_by_condition=defaultdict(Counter);request_counts=Counter();request_latencies=defaultdict(list)
    from scripts.run_note_cognitive_benchmark import prompt_for
    skill=(root/'frozen-skill.md').read_text()
    for r in completed:
        assert schedule[r['position']]=={k:r[k] for k in ('case_id','condition','replicate')}
        case=cases[r['case_id']]
        for stage in ('first','final'):
            result=r[stage];key=(r['position'],result['stage'])
            if key in requests:continue
            requests.add(key)
            directory=root/'responses'/f"{r['position']:03d}-{result['stage']}"
            expected=prompt_for(case,r['condition'],skill,recovery=r['first']['answer'] if result['stage']=='recovery' else None)
            assert (directory/'prompt.txt').read_text()==expected
            assert sha(directory/'prompt.txt')==result['prompt_sha256']
            max_character_prompt=max(max_character_prompt,len(expected));prompt_checks+=1
            request_counts[r['condition']]+=1
            request_latencies[r['condition']].append(result['elapsed_seconds'])
            for k,v in result['usage'].items():
                usage[k]+=int(v or 0);usage_by_condition[r['condition']][k]+=int(v or 0)
        meta={k:r[k] for k in ('position','case_id','condition','replicate','recovered')}
        meta.update(category=case['category'],split=case['split'],family=case['family'])
        rows.append({**meta,**score(case,r['condition'],r['final'],r['recovered'])})
        initials.append({**meta,**score(case,r['condition'],r['first'],False)})
    summary={'complete':len(completed)==len(schedule),'completed':len(completed),'target':len(schedule),
             'model_requested':p['model'],'harness':p['route'],'requests':len(requests),'prompt_hash_checks':prompt_checks,
             'largest_prompt_characters':max_character_prompt,'observed_usage':dict(usage),
             'usage_by_condition':{c:dict(u) for c,u in usage_by_condition.items()},'request_counts_by_condition':dict(request_counts),
             'median_request_seconds':{c:statistics.median(v) for c,v in request_latencies.items()},
             'conditions':{c:summarize([r for r in rows if r['condition']==c]) for c in sorted({r['condition'] for r in rows})},
             'initial_stale':summarize([r for r in initials if r['condition']=='stale_recovery']),
             'by_category':{cat:{c:summarize([r for r in rows if r['category']==cat and r['condition']==c]) for c in sorted({r['condition'] for r in rows})} for cat in sorted({r['category'] for r in rows})},
             'by_split':{s:{c:summarize([r for r in rows if r['split']==s and r['condition']==c]) for c in sorted({r['condition'] for r in rows})} for s in ('development','confirmation')},
             'model_errors':sum(bool(r['model_error']) for r in rows),
             'limits':p['limits']}
    if summary['complete']:
        summary['contrasts']=[bootstrap_contrast(rows,cases,a,b) for a,b in (('curated_checkpoint','full_history'),('full_history','current_only'),('stale_recovery','full_history'))]
    paired=[]
    for cid in cases:
        for replicate in range(3):
            choices={r['condition']:r['choice'] for r in rows if r['case_id']==cid and r['replicate']==replicate}
            if len(choices)==4:paired.append(choices)
    summary['choice_changes_descriptive']={'paired_replicates':len(paired),
        'vs_current_only':{c:sum(r[c]!=r['current_only'] for r in paired) for c in ('full_history','curated_checkpoint','stale_recovery')},
        'limits':'Choice legality and variation only; no optimal-action gold or counterfactual game outcomes'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'scored-responses.json').write_text(json.dumps({'final':rows,'initial':initials},indent=2)+'\n')
    # Lossless public evidence + final answers/usage; no model reasoning or credentials.
    archive=out/'public-benchmark.jsonl.gz'
    with gzip.open(archive,'wt') as stream:
        stream.write(json.dumps({'kind':'header','protocol':p,'cases':list(cases.values()),'skill':skill,'scoring':json.loads((root/'scoring-frozen.json').read_text())},ensure_ascii=False)+'\n')
        for r in completed:
            events={}
            for result in (r['first'],r['final']):
                stage=result['stage']
                events[stage]=json.loads((root/'responses'/f"{r['position']:03d}-{stage}"/'events.json').read_text())
            stream.write(json.dumps({'kind':'response',**r,'native_events':events},ensure_ascii=False)+'\n')
    (out/'archive-sha256.txt').write_text(sha(archive)+'\n')
    for name in ('protocol.json','protocol-sha256.txt','schedule.json','execution.json','case-audit.json','scoring-frozen.json','frozen-skill.md','status.json'):
        shutil.copyfile(root/name,out/name)
    shutil.copytree(root/'sources',out/'sources',dirs_exist_ok=True)
    print(json.dumps({k:summary[k] for k in ('complete','completed','requests','observed_usage','conditions','model_errors')},indent=2))


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    analyze(Path(sys.argv[1]).resolve(),Path(sys.argv[2]))
