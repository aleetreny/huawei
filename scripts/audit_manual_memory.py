"""Offline memory inventory, public-note witness and conditional token arithmetic."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess


def sha(data):return hashlib.sha256(data).hexdigest()


def audit():
    root=Path('lab/reports/manual-memory');root.mkdir(parents=True,exist_ok=True)
    inventory=[]
    for name,path,kind in (
        ('F6','lab/policies-src/f6-commitment-ledger/f6-commitment-ledger-v1/bundle/skills/commitment-ledger/SKILL.md','Explicit full ledger in action notes; recovery from public logs'),
        ('Observed growth v1','lab/policies-src/matteo-feedback-growth/observed-growth-v1/bundle/skills/observed-growth/SKILL.md','Instruction to retain feedback, warnings, commitments and benefits; no fixed serialization'),
        ('Promotion readiness v2','lab/policies-src/matteo-first-review/promotion-readiness-v2/bundle/skills/promotion-readiness/SKILL.md','Compact action/payoff memory and open commitments; no explicit persistent storage protocol'),
        ('First-year draft','lab/reports/trust-risk-study/first-year-strategy-draft.md','Separates incident history, current warnings and open commitments; unvalidated prose draft'),
    ):
        data=Path(path).read_bytes();inventory.append({'manual':name,'path':path,'sha256':sha(data),'memory_description':kind})
    ref='26e976f9acbe44761f77457d9314e69ea31c4934'
    path='lab/policies-src/f3-feedback-reactive/targeted-1026-201334/bundle/skills/balanced-feedback/SKILL.md'
    champion=subprocess.check_output(['git','show',ref+':'+path]);(root/'ale-champion-snapshot.md').write_bytes(champion)
    inventory.append({'manual':'Ale champion targeted-1026-201334','source_commit':ref,'path':path,'sha256':sha(champion),
        'memory_description':'Risk state with step-down persistence, review plan and recent logs; no explicit incident-history ledger'})
    archive=Path('lab/reports/constrained-growth-study/study-v1/public-trajectories.jsonl.gz')
    assert sha(archive.read_bytes())==(archive.parent/'archive-sha256.txt').read_text().strip()
    with gzip.open(archive,'rt') as stream:r=json.loads(next(stream))
    expected=['Frozen constrained-growth research: '+s['reason'] for s in r['steps']]
    returned=[e['message'].split('Notes: ',1)[1] for e in r['logs']['entries'] if 'Notes: ' in e.get('message','')]
    assert len(returned)==50 and len(expected)==51 and all(n in expected for n in returned)
    unmatched=Counter(expected)-Counter(returned)
    witness={'archive':str(archive),'archive_sha256':sha(archive.read_bytes()),'run':r['run'],
        'actions':len(expected),'notes_returned':len(returned),'exact_known_note_matches':len(returned),
        'max_verified_note_characters':max(map(len,returned)),'unmatched_notes':dict(unmatched),
        'unmatched_choice':'Continue','limits':'Only already collected short notes. Does not verify long-ledger truncation, every action kind, small-count recovery or official-target context resets.'}
    scenarios=[]
    for extra in (40,60):
        n=200;reads=2;months=48
        output=extra*n;input_=extra*reads*n*(n-1)//2;total=input_+output
        scenarios.append({'extra_tokens_per_action':extra,'actions':n,'model_reads_per_later_action':reads,'months':months,
            'extra_output':output,'extra_input':input_,'extra_total':total,'extra_per_month':total/months,
            'weighted_token_score_loss_if_in_linear_region':.1*100*(total/months)/2500000})
    result={'inventory':inventory,'public_notes_witness':witness,'illustrative_full_history_scenarios':scenarios,
        'scenario_limits':['Not target-model tokenizer measurements or empirical usage forecasts','Extra tokens are relative to existing notes, not total note length',
            'Assumes each note is added at the end of an action and re-read twice on every later action; no compression or discarded history',
            'Prompt instruction, log-recovery calls, extra reasoning and serialization overhead omitted',
            'Score arithmetic uses the laboratory formula, only inside its linear region; clipping and early-exit caps can change the effect',
            'Dollar cost requires route-specific billed input/cache/output prices; no live tariff or spend estimate claimed']}
    (root/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'manuals':len(inventory),'witness':witness,'scenarios':scenarios},indent=2))


if __name__=='__main__':audit()
