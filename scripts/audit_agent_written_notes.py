"""Replay question-blind writer/reader evidence and total native request counts."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.probe_agent_written_notes import writer_prompt
from scripts.run_note_cognitive_benchmark import prompt_for


def audit(base):
    root=base/'agent-written-v1';archive=root/'public-writer-reader.jsonl.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(root/'archive-sha256.txt').read_text().strip()
    with gzip.open(archive,'rt') as stream:
        header=json.loads(next(stream));pairs=[json.loads(line) for line in stream]
    cases={c['id']:c for c in header['cases']};threads=set();usage=Counter()
    def account(events,result=None):
        tid=next(e['thread_id'] for e in events if e['type']=='thread.started')
        assert tid not in threads;threads.add(tid)
        observed=next(e['usage'] for e in events if e['type']=='turn.completed')
        if result is not None:assert observed==result['usage'] and result['error'] is None and not result['tool_attempts']
        usage.update(observed)
    for r in pairs:
        assert header['protocol']['schedule'][r['position']]=={k:r[k] for k in ('case_id','budget')}
        c=cases[r['case_id']];writer=writer_prompt(c,header['skill'],r['budget'])
        assert c['question'] not in writer
        reader=prompt_for({**c,'checkpoint':{'id':'CHECKPOINT','text':r['carried_note']}},'curated_checkpoint',header['skill'])
        assert len(r['carried_note'])<=r['budget']
        for kind,prompt in (('writer',writer),('reader',reader)):
            assert hashlib.sha256(prompt.encode()).hexdigest()==r[kind]['prompt_sha256']
            account(r['native_events'][kind],r[kind])
    assert len(pairs)==16 and len(threads)==32
    writer_usage=dict(usage)
    with gzip.open(base/'cognition-v1/public-benchmark.jsonl.gz','rt') as stream:
        next(stream)
        for line in stream:
            r=json.loads(line)
            for events in r['native_events'].values():account(events)
    for f in (base/'cache-prefix-v1/responses').glob('*/events.json'):account(json.loads(f.read_text()))
    events=[json.loads(line) for line in (base/'cognition-v1/preflight/events.jsonl').read_text().splitlines()]
    account(events)
    assert len(threads)==719
    overall=json.loads((base/'cognition-v1/overall-work-audit.json').read_text())
    assert dict(usage)==overall['observed_usage']
    result={'writer_reader_pairs':16,'writer_reader_prompt_hashes':32,'writer_reader_usage':writer_usage,
            'all_work_unique_threads':len(threads),'all_work_usage':dict(usage),
            'limits':'Reconstruction of actual usage and supplied prompts, not a bill, backend routing receipt or universal cache expiry proof'}
    (root/'replay-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':audit(Path(sys.argv[1]))
