"""Public measured-return memory prototype. No game constants, event lookup or model calls."""
import json,hashlib,collections
from pathlib import Path
GROWTH=('skill','network','output')
class MeasuredLedger:
 def __init__(self,session):self.session=session;self.seen={};self.level=None;self.diminished={};self.counts=collections.Counter()
 def accept(self,session,action_id,before,after,nominal,isolated):
  if session!=self.session:raise ValueError('Session mismatch')
  payload=json.dumps([before,after,nominal,isolated],sort_keys=True)
  if action_id in self.seen:
   if self.seen[action_id]!=payload:raise ValueError('Action identity reused with different evidence')
   self.counts['duplicate_ignored']+=1;return
  self.seen[action_id]=payload
  if before['level']!=self.level:self.level=before['level'];self.diminished={}
  if not after or not isolated or (before['month'],before['level'])!=(after['month'],after['level']):self.counts['ambiguous_rejected']+=1;return
  if any(after[k]-before[k]<0 and nominal.get(k,0)>=0 for k in GROWTH):self.counts['unexpected_loss_rejected']+=1;return
  self.counts['isolated_accepted']+=1
  for k in GROWTH:
   if k in self.diminished and after[k]>self.diminished[k]:del self.diminished[k];self.counts['reopened']+=1
   if nominal.get(k,0)>0 and after[k]-before[k]<nominal[k]:self.diminished[k]=after[k];self.counts['diminished_observations']+=1

def main():
 from gpt_native_trace import extract
 from gpt_public_return_parser import parse_entry
 root=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1';rows,_=extract(sorted(root.glob('stream-*.jsonl')));rows=rows[1:];entries=json.loads((root/'official-player-logs.json').read_text())['entries'];returns=[r for e in entries if (r:=parse_entry(e)) is not None];assert len(rows)==len(returns)==201
 ledger=MeasuredLedger('own-reference');facts=[]
 for row,ret in zip(rows,returns):
  assert row['choice']==ret['choice'] and row['before']['month']==ret['month'];before=dict(ledger.diminished)
  ledger.accept('own-reference',row['call_id_sha256'],row['before'],row.get('after'),ret['nominal_visible_changes'],row.get('isolated_same_month_level',False))
  if before!=ledger.diminished:facts.append({'month':row['before']['month'],'level':row['before']['level'],'diminished':dict(ledger.diminished)})
 # Independent fail-closed invariants, not game examples.
 b={'month':1,'level':1,'skill':1,'network':1,'output':1};a=dict(b,skill=2);l=MeasuredLedger('a');l.accept('a','x',b,a,{'skill':1},True);l.accept('a','x',b,a,{'skill':1},True);assert l.counts['isolated_accepted']==1
 try:l.accept('b','x',b,a,{},True);raise AssertionError('Session guard failed')
 except ValueError:pass
 try:l.accept('a','x',b,a,{},True);raise AssertionError('Identity guard failed')
 except ValueError:pass
 l.accept('a','y',a,a,{'skill':1},True);assert l.diminished['skill']==2
 l.accept('a','z',a,dict(a,skill=3),{'skill':1},True);assert 'skill' not in l.diminished
 out={'meaning':'Research prototype learned only from own public logged nominal returns and isolated observed panels. No true caps or hidden risk read. Diminished return is provisional, not an engine rule or score guarantee. Batched/settlement transitions and unexpected losses excluded. No actor use or policy efficacy tested.','counts':dict(ledger.counts),'unique_actions':len(ledger.seen),'state_changes':facts,'guards_passed':['deduplication','cross_session_rejection','conflicting_identity_rejection','diminished_observation','reopening'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 p=Path(__file__).resolve().parents[2]/'lab/reports/deepseek/gpt-principios/measured-ledger-audit.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='state_changes'},indent=2))
if __name__=='__main__':main()
