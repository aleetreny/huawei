"""Exploratory, question-blind writer -> fresh reader, 8 cases x 2 budgets x 2 calls."""
import asyncio
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.run_note_cognitive_benchmark import request, prompt_for, SCHEMA
from scripts.diagnose_note_cognitive_errors import normalized_answer


def writer_prompt(case,skill,budget):
    return ('Create a factual checkpoint for continuing this Career Survival career. Do not use tools, read files, or contact services. '
        'You do not know the later factual question. Select what is worth remembering using the fixed Skill: past serious incidents, open commitments, '
        'latest review, observed investment payoff and next-step conditions. Distinguish observed results from advertised effects and expectations. '
        f'Put the entire memory in updated_note, at most {budget} Unicode characters. Other fields are not memory and will not reach the next reader. '
        'Use answer="unknown", evidence_ids=[], request_logs=false and any legally offered choice. No private reasoning.\n\nFIXED SKILL:\n'+skill+
        '\n\nPUBLIC PREFIX:\n'+json.dumps({'current':case['current'],'history':case['history']},ensure_ascii=False,separators=(',',':')))


async def run(source,root):
    root.mkdir(parents=True,exist_ok=False);(root/'responses').mkdir();(root/'empty-workspace').mkdir()
    (root/'response-schema.json').write_text(json.dumps(SCHEMA))
    cases=json.loads((source/'cases.json').read_text());chosen={}
    for c in sorted(cases,key=lambda c:c['id']):chosen.setdefault(c['category'],c)
    chosen=list(chosen.values());assert len(chosen)==8
    schedule=[{'case_id':c['id'],'budget':budget} for c in chosen for budget in (128,800)]
    random.Random(271029).shuffle(schedule)
    protocol={'name':'agent-written-checkpoint-exploratory-v1','model':'gpt-6-luna','reasoning_effort':'low','max_seconds_per_request':180,
        'max_requests':32,'created_at':datetime.now(timezone.utc).isoformat(),'schedule':schedule,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'parent_cases_sha256':hashlib.sha256((source/'cases.json').read_bytes()).hexdigest(),
        'selection':'First ID per category from completed fixed benchmark, not selected by errors; reused cases, exploratory not confirmation',
        'writer':'Question and gold withheld; only current/public prefix/Skill and budget; only updated_note crosses boundary',
        'overflow':'Record violation; enforce budget with prefix truncation and ellipsis before reader',
        'reader':'Fresh process; current plus actual generated note plus factual question; no history/recovery; CHECKPOINT citation explicitly available',
        'limits':['One writer/reader pair per case/budget, no precision or promotion guarantee','Semantic answer normalization is diagnostic, exact answer separately preserved',
                  'Not natural Jiuwen compression: a controlled loss of history with a generated checkpoint','Cannot pool this new note/citation procedure with the previous576 decisions']}
    (root/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    skill=(source/'frozen-skill.md').read_text();results=[];lookup={c['id']:c for c in chosen};stop=[]
    semaphore=asyncio.Semaphore(2)
    async def episode(index,item):
        async with semaphore:
            if stop:return
            c=lookup[item['case_id']];budget=item['budget']
            written=await request(root,protocol,index,writer_prompt(c,skill,budget),'writer')
            if written['error']:stop.append(written['error']);return
            original=written['answer']['updated_note']
            carried=original if len(original)<=budget else original[:budget-3]+'...'
            reader_case={**c,'checkpoint':{'id':'CHECKPOINT','text':carried}}
            read=await request(root,protocol,index,prompt_for(reader_case,'curated_checkpoint',skill),'reader')
            if read['error']:stop.append(read['error']);return
            a=read['answer'];ids=set(a['evidence_ids'])
            correct=str(a['answer']).strip().casefold()==c['answer'].casefold()
            semantic=normalized_answer(a['answer'],c['answer']).strip().casefold()==c['answer'].casefold()
            row={'position':index,**item,'category':c['category'],'gold':c['answer'],'question':c['question'],'writer':written,'reader':read,
                 'original_note_characters':len(original),'carried_note':carried,'budget_respected_by_writer':len(original)<=budget,
                 'exact_correct':correct,'diagnostic_normalized_correct':semantic,
                 'citation_contract_valid':ids<={'CURRENT','CHECKPOINT'},'supported_note_record_cited':'CHECKPOINT' in ids,
                 'legal_reader_choice':a['choice'] in {x['choice'] for x in c['current']['data']['choices']}}
            results.append(row)
            (root/'results.json').write_text(json.dumps({'complete':len(results)==16,'stop':stop,'results':sorted(results,key=lambda r:r['position'])},ensure_ascii=False,indent=2)+'\n')
    await asyncio.gather(*(episode(i,item) for i,item in enumerate(schedule)))
    usage=Counter()
    for row in results:
        for kind in ('writer','reader'):usage.update(row[kind]['usage'])
    summary={'complete':len(results)==16,'pairs':len(results),'requests':len(results)*2,'observed_usage':dict(usage),
        'by_budget':{str(b):{'n':sum(r['budget']==b for r in results),'exact_correct':sum(r['exact_correct'] for r in results if r['budget']==b),
                           'diagnostic_normalized_correct':sum(r['diagnostic_normalized_correct'] for r in results if r['budget']==b),
                           'writer_within_budget':sum(r['budget_respected_by_writer'] for r in results if r['budget']==b)} for b in (128,800)},'stop':stop}
    (root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':asyncio.run(run(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()))
