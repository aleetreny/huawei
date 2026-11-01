"""Independent archive/inference accounting audit; runs with no CLI/model access."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.run_note_cognitive_benchmark import prompt_for


def audit(root):
    archive=root/'public-benchmark.jsonl.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(root/'archive-sha256.txt').read_text().strip()
    with gzip.open(archive,'rt') as stream:
        header=json.loads(next(stream));responses=[json.loads(line) for line in stream]
    cases={c['id']:c for c in header['cases']}
    schedule=json.loads((root/'schedule.json').read_text());summary=json.loads((root/'summary.json').read_text())
    seen=set();threads=set();requests=set();usage=Counter();raw=Counter();recovery_count=0
    for row in responses:
        pos=row['position'];assert pos not in seen;seen.add(pos)
        assert schedule[pos]=={k:row[k] for k in ('case_id','condition','replicate')}
        case=cases[row['case_id']]
        raw[row['condition']]+=str(row['final']['answer']['answer']).strip().casefold()==str(case['answer']).strip().casefold()
        if row['recovered']:
            assert row['condition']=='stale_recovery' and row['first']['answer']['request_logs']
            assert row['final']['stage']=='recovery';recovery_count+=1
        for result in (row['first'],row['final']):
            key=(pos,result['stage'])
            if key in requests:continue
            requests.add(key)
            rendered=prompt_for(case,row['condition'],header['skill'],recovery=row['first']['answer'] if result['stage']=='recovery' else None)
            assert hashlib.sha256(rendered.encode()).hexdigest()==result['prompt_sha256']
            events=row['native_events'][result['stage']]
            starts=[e['thread_id'] for e in events if e['type']=='thread.started']
            assert len(starts)==1 and starts[0] not in threads;threads.add(starts[0])
            reported=[e['usage'] for e in events if e['type']=='turn.completed']
            assert reported==[result['usage']]
            messages=[json.loads(e['item']['text']) for e in events if e['type']=='item.completed' and e['item']['type']=='agent_message' and e['item']['text'].lstrip().startswith('{')]
            assert messages[-1]==result['answer']
            assert result['error'] is None and not result['tool_attempts']
            for key,value in result['usage'].items():usage[key]+=int(value or 0)
    assert len(seen)==576 and len(requests)==576+recovery_count
    assert dict(usage)==summary['observed_usage']
    assert all(raw[c]==s['raw_correct'] for c,s in summary['conditions'].items())
    result={'verified_primary_decisions':len(seen),'verified_requests':len(requests),'unique_native_thread_ids':len(threads),
            'verified_prompt_hashes':len(requests),'recovery_requests':recovery_count,
            'observed_usage':dict(usage),'raw_answer_counts_reconstructed':dict(raw),
            'no_unexpected_tool_use':True,'no_model_call_errors':True,
            'limits':['Requested model/harness recorded; no separate backend model-resolution receipt',
                      'Fresh CLI threads and public task evidence do not establish absence of all hidden provider-side transformations',
                      'Raw answer reconstruction verifies accounting; semantic anchor judgments remain those of the fixed dataset']}
    (root/'independent-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':audit(Path(sys.argv[1]))
