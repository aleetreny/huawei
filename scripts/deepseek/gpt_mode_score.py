"""Score only saved official-tool bot outputs, never internal server data."""
import json,gzip,math,statistics,hashlib
from pathlib import Path
from gpt_mode_audit import DATA,REPORT

def main():
 results={};pending={}
 for mode in ('dev','competition'):
  rows=[];partial=False
  for p in (DATA/mode).glob('games-*.jsonl.gz'):
   try:
    with gzip.open(p,'rt') as f:
     for line in f:rows.append(json.loads(line))
   except (EOFError,OSError):partial=True
  if len(rows)!=60 or partial:pending[mode]={'written_records':len(rows),'stream_incomplete':partial};continue
  manifest=json.loads((DATA/mode/'manifest.json').read_text());assert manifest['competition']==(mode=='competition') and manifest['args']['explore_below']==0
  valid=[r for r in rows if r.get('outcome') in ('completed','eliminated') and isinstance((r.get('end') or {}).get('q'),(int,float))];q=[r['end']['q'] for r in valid]
  results[mode]={'attempted':len(rows),'valid':len(q),'operational_failures':len(rows)-len(q),'mean':statistics.mean(q) if q else None,'se':statistics.stdev(q)/math.sqrt(len(q)) if len(q)>1 else None,'min':min(q) if q else None,'max':max(q) if q else None,'at_least75':sum(x>=75 for x in q),'completed':sum(r['outcome']=='completed' for r in valid),'policy_hash':hashlib.sha256(json.dumps(manifest['params'],sort_keys=True).encode()).hexdigest()}
 if pending:print(json.dumps({'pending':pending,'finished_modes':list(results)}));return
 assert results['dev']['policy_hash']==results['competition']['policy_hash']
 delta=results['competition']['mean']-results['dev']['mean'];se=math.hypot(results['competition']['se'],results['dev']['se'])
 out={'meaning':'Independent local mode samples, same Planner, not paired engine seeds. Pilot CI normal approximation, no small-shift equivalence claim. Interrupted runs never scored as zero; failures explicitly retained. No DeepSeek or competition-heldout score inference.','selection_warning':'Competition has operational missingness if failures>0; reported means/CI are conditional on valid games and cannot identify a mode effect without checking missingness.','modes':results,'competition_minus_dev':{'mean':delta,'ci95':[delta-1.96*se,delta+1.96*se]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'mode-audit-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
