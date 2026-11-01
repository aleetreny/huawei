"""Build causal sidecar packets from own public history, never future target effects."""
import json,hashlib
from pathlib import Path
from gpt_measured_ledger import MeasuredLedger
from gpt_public_return_parser import parse_entry
from gpt_native_trace import extract
ROOT=Path(__file__).resolve().parents[2];REPORT=ROOT/'lab/reports/deepseek/gpt-principios';SOURCE=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1';DATA=SOURCE.parent.with_name('gpt-return-packets')
def packet(past,returns,current):
 assert len(past)==len(returns);ledger=MeasuredLedger('own-reference')
 for row,ret in zip(past,returns):
  assert row['choice']==ret['choice'] and row['before']['month']==ret['month']
  isolated=row.get('isolated_same_month_level',False)
  ledger.accept('own-reference',row['call_id_sha256'],row['before'],row.get('after') if isolated else None,ret['nominal_visible_changes'],isolated)
 diminished=dict(ledger.diminished) if ledger.level==current['level'] else {}
 # A currently observed value above the previous marker disproves that marker.
 diminished={k:v for k,v in diminished.items() if current[k]<=v}
 return {'role':current['level'],'observed_diminished_returns':diminished,'meaning':'Past isolated logged positive returns did not fully appear in observed growth. Provisional observations, not published limits or promises about current options. Reopen when growth resumes.'}
def main():
 rows,_=extract(sorted(SOURCE.glob('stream-*.jsonl')));rows=rows[1:];returns=[r for e in json.loads((SOURCE/'official-player-logs.json').read_text())['entries'] if (r:=parse_entry(e)) is not None];assert len(rows)==len(returns)==201
 targets=json.loads((SOURCE.parent.with_name('gpt-fresh-context')/'items.json').read_text());index={r['call_id_sha256'][:16]:i for i,r in enumerate(rows)};packets=[]
 for it in targets:
  i=index[it['id']];p=packet(rows[:i],returns[:i],rows[i]['before'])
  # Full future mutations cannot enter this explicit prefix-only interface.
  assert p==packet(list(rows[:i]),list(returns[:i]),dict(rows[i]['before']))
  packets.append({'id':it['id'],'observe':it['observe'],'prior_notes':it['prior_notes'],'packet':p,'past_action_count':i})
 DATA.mkdir(parents=True,exist_ok=True);out=DATA/'items.json';out.write_text(json.dumps(packets,ensure_ascii=False,indent=2)+'\n')
 report={'meaning':'24critical public panels plus past-return packets. Target effect and choice not stored or passed. Prefix-only function receives no future actions. No actor use/Q claim. Raw observations remain private.','n':len(packets),'nonempty_packets':sum(bool(p['packet']['observed_diminished_returns']) for p in packets),'items_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'selection':[{'id':p['id'],'past_action_count':p['past_action_count'],'packet':p['packet']} for p in packets],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'return-packets-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='selection'},indent=2))
if __name__=='__main__':main()
