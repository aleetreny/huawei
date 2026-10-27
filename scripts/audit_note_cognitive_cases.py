"""Reconstruct benchmark facts and temporal boundaries from public archives."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys


def audit(root):
    cases=json.loads((root/'cases.json').read_text())
    wanted={(c['archive'],c['line']) for c in cases};records={}
    for path in sorted({a for a,_ in wanted}):
        with gzip.open(path,'rt') as stream:
            for line_number,line in enumerate(stream):
                if (path,line_number) in wanted:records[(path,line_number)]=json.loads(line)
    checks=[]
    for c in cases:
        r=records[(c['archive'],c['line'])];steps=r['steps'];cut=c['cut'];j=c['source_step'];category=c['category']
        assert j<cut<=len(steps)
        assert c['current']['data']==steps[cut-1]['after']
        assert len(c['history'])==cut*3
        for index,s in enumerate(steps[:cut]):
            records3=c['history'][index*3:index*3+3]
            assert records3[0]['data']==s['before'] and records3[2]['data']==s['after']
            assert records3[1]['data']['choice']==s['choice']
        if category=='fresh_over_stale':
            assert str(c['current']['data']['current_state']['status']['health'])==c['answer']
            assert c['old_health']!=int(c['answer'])
            source_index=int(c['old_health_source'][1:4])
            assert steps[source_index]['before']['current_state']['status']['health']==c['old_health']
        elif category=='observed_payoff':
            before=steps[j]['before']['current_state']['status'];after=steps[j]['after']['current_state']['status']
            stat=next(s for s in ('Output','Skill','Network') if f'visible {s} change' in c['question'])
            assert str(after[stat.lower()]-before[stat.lower()])==c['answer']
            assert steps[j]['choice']['status_updates'][stat]>0
        elif category=='latest_review':
            grades=[g for s in steps[:cut] for g in re.findall(r'performance bonus \(([A-Z])\)',s['after'].get('events',''))]
            assert grades[-1]==c['answer']
        elif category=='incident_history':
            n=sum('Old landmines' in s['after'].get('events','') for s in steps[:cut])
            assert n==c['incident_count'] and ('yes' if n else 'no')==c['answer']
            assert 'Old landmines' not in c['current']['data'].get('events','')
        elif category in ('open_commitment','explicit_resolution'):
            description=steps[j]['before']['current_event']['description']
            assert c['matched_fragment'].casefold() in description.casefold()
            assert c['matched_fragment'].casefold() in c['checkpoint']['text'].casefold()
        elif category=='delayed_consequence':
            chosen=steps[j]['choice']['action']
            assert (chosen in c['question']) == (c['answer']=='yes')
            k=c['later_step'];assert k<cut
            assert steps[j]['before']['current_event']['title']==steps[k]['before']['current_event']['title']
            assert steps[j]['before']['current_event']['description']!=steps[k]['before']['current_event']['description']
        elif category=='unknown':
            assert c['answer']=='unknown'
        else:raise ValueError(category)
        checks.append({'id':c['id'],'category':category,'temporal_prefix_verified':True,'fact_reconstructed':True})
    assert len(cases)==48 and len({c['session_id'] for c in cases})==48
    a={c['family'] for c in cases if c['split']=='development'};b={c['family'] for c in cases if c['split']=='confirmation'}
    assert not a&b
    result={'cases_verified':48,'unique_source_careers':48,'family_split_disjoint':True,'checks':checks,
        'category_by_split':{s:dict(Counter(c['category'] for c in cases if c['split']==s)) for s in ('development','confirmation')},
        'case_sha256':hashlib.sha256((root/'cases.json').read_bytes()).hexdigest(),
        'limits':['Deterministic second pass and analyst review of semantic anchors, not an independent blinded human panel',
                  'Unknown hidden-parameter labels are public-information insufficiency judgments, not recovered hidden engine values']}
    (root/'case-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))


if __name__=='__main__':audit(Path(sys.argv[1]))
