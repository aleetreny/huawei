"""Public-state witnesses for the native pilot's memory execution; no causal score."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))


def audit(root):
    archive=root/'public-trajectory.jsonl.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(root/'archive-sha256.txt').read_text().strip()
    with gzip.open(archive,'rt') as stream:r=json.loads(next(stream))
    steps=r['steps'];quarterly=[];prep=[];main=Counter()
    for i,s in enumerate(steps):
        if s['phase'] not in ('energy','main_action'):continue
        b=s['before']['current_state']['status'];a=s['after']['current_state']['status']
        row={'step':i,'month':s['before']['current_state']['time']['current_month'],'action':s['choice']['action'],
            'before':b,'after':a,'observed_delta':{key:a[key]-b[key] for key in ('health','dignity','skill','network','output','wealth')},'notes':s['notes']}
        quarterly.append(row)
        if s['choice']['action']=='Prepare report materials':prep.append(row)
        if s['phase']=='main_action':main[s['choice']['action']]+=1
    def witness(i):
        s=steps[i]
        return {'step':i,'month':s['before']['current_state']['time']['current_month'],
            'public_event':s['before'].get('current_event'),'choice':s['choice'],'notes':s['notes'],
            'before':s['before']['current_state']['status'],'after':s['after']['current_state']['status']}
    parent=Path('lab/reports/manual-memory/ale-champion-snapshot.md').read_bytes()
    candidate=(root/'frozen-bundle/skills/balanced-feedback/SKILL.md').read_bytes()
    assert candidate.startswith(parent),'Parent rules changed'
    output={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'all_parent_text_preserved':True,
        'nonempty_notes':sum(bool(s['notes'].strip()) for s in steps),
        'notes_with_explicit_memory_label':sum(s['notes'].startswith('Memory:') for s in steps),
        'report_preparation_actions':len(prep),'report_preparation_zero_visible_output_gain':sum(p['observed_delta']['output']==0 for p in prep),
        'main_action_counts':dict(main),'quarterly_choices':quarterly,
        'manual_reviewed_witnesses':[
            {'finding':'Actual payoff not recorded consistently: after report preparation gave no visible Output gain, next note still says no investments; another report preparation repeats the zero gain.',
             'steps':[witness(i) for i in (10,11,12)]},
            {'finding':'Open security fix retained: deferred fix with mitigations at step82 remains in subsequent notes; the recurring public event at step87 describes the attack and the model initiates response.',
             'steps':[witness(i) for i in (82,83,84,85,86,87,88)]},
            {'finding':'Review weakness retained, but later main choices remain defensive in several quarters. This is a policy/context trade-off, not proof that memory caused it.',
             'steps':[witness(i) for i in (23,38,50,62,74,86)]}],
        'observed_old_landmines_messages':sum('Old landmines' in s['after'].get('events','') for s in steps),
        'recovery_logs_requested_by_player':sum(json.loads(line)['tool']=='check_latest_logs' for line in (root/'trajectory.jsonl').read_text().splitlines()),
        'limits':['Post-hoc factual audit, not blinded and not a causal comparison','Memory-labelled prose is not evidence that every required field is correct',
            'Zero visible gain is not proof of no hidden or indirect benefit','No context reset was forced; restart recovery and reduced-context retention were not tested',
            'A story security incident differs from an official Old landmines/trust-crisis notification','No per-model token or monetary receipt exposed']}
    (root/'memory-audit.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({key:value for key,value in output.items() if key not in ('quarterly_choices','manual_reviewed_witnesses')},indent=2))


if __name__=='__main__':audit(Path(sys.argv[1]))
