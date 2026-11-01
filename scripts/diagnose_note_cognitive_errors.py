"""Explicitly post-hoc format/provenance diagnostics; never replaces frozen scores."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import re
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.analyze_note_cognitive_benchmark import score


def normalized_answer(text,gold):
    text=str(text).strip()
    if str(gold).casefold() in ('yes','no','unknown'):
        match=re.match(r'^(yes|no|unknown)\b',text,re.I)
        return match.group(1).casefold() if match else text
    if re.fullmatch(r'[+-]?\d+(?:\.0+)?',str(gold)):
        match=re.match(r'^([+-]?\d+(?:\.0+)?)\b',text)
        return str(int(float(match.group(1)))) if match else text
    return text


def diagnose(root):
    with gzip.open(root/'public-benchmark.jsonl.gz','rt') as stream:
        header=json.loads(next(stream));responses=[json.loads(line) for line in stream]
    cases={c['id']:c for c in header['cases']};counts=defaultdict(Counter);witnesses=[]
    witness_positions={25,31,47,311,422}
    for r in responses:
        c=cases[r['case_id']];final=r['final'];original=final['answer'];changed=json.loads(json.dumps(final))
        changed['answer']['answer']=normalized_answer(original['answer'],c['answer'])
        if r['condition']=='curated_checkpoint':
            provenance=set(c['checkpoint']['sources'])
            changed['answer']['evidence_ids']=list(dict.fromkeys('CHECKPOINT' if source in provenance else source for source in original['evidence_ids']))
        measured=score(c,r['condition'],changed,r['recovered'])
        group=counts[r['condition']];group['n']+=1
        group['raw_answer_match_after_format_normalization']+=measured['raw_correct']
        group['supported_after_format_and_explicit_provenance_resolution']+=measured['supported_correct']
        if c['answer']!='unknown':
            group['known_n']+=1;group['known_answer_match_after_format_normalization']+=measured['raw_correct']
            group['known_supported_after_format_and_explicit_provenance_resolution']+=measured['supported_correct']
        if r['position'] in witness_positions:
            witnesses.append({'position':r['position'],'condition':r['condition'],'case_id':r['case_id'],
                              'question':c['question'],'gold':c['answer'],'answer':original,
                              'public_fact_checkpoint':c['checkpoint'],
                              'finding':'Analyst-selected witness: answer field disagrees with an explicit relevant fact in the same response note; inspect wording and sources, not a global contradiction rate.'})
    result={'post_hoc':True,'counts':{k:dict(v) for k,v in counts.items()},'selected_witnesses':witnesses,
        'normalization':'Leading yes/no/unknown or leading integer; only provenance IDs explicitly supplied in curated checkpoint mapped to CHECKPOINT; no gold substitution, no correction from response notes',
        'limits':['Frozen primary exact-answer/source scores remain unchanged','Post-hoc diagnostics are not independent confirmation of checkpoint superiority',
                  'Unknown versus not-reported wording can also contribute; semantic interpretation is bounded by original question',
                  'Five selected contradiction witnesses are not a population frequency']}
    (root/'posthoc-error-diagnostics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'post_hoc':True,'counts':result['counts'],'selected_witnesses':len(witnesses)},indent=2))


if __name__=='__main__':diagnose(Path(sys.argv[1]))
