"""Extract public logged nominal returns. No event lookup, thresholds or engine access."""
import re,json,hashlib,collections
from pathlib import Path
STATS={k:k.lower() for k in ('Health','Dignity','Skill','Network','Output','Wealth')}
PATTERN=re.compile(r'\b(Health|Dignity|Skill|Network|Output|Wealth)\s*([+−-]\s*\d+(?:\.\d+)?)\b',re.I)
def parse_entry(entry):
 text=entry.get('message','');chosen=re.search(r'^Chose #(\d+):[^\n]*\n',text,re.M)
 if not chosen:return None
 month=re.search(r'^Month (\d+)\s*\|',text)
 if not month:return None
 body=text[chosen.end():].split('Notes:',1)[0];values={};conflicts=[]
 for stat,number in PATTERN.findall(body):
  key=stat.lower();value=float(number.replace(' ','').replace('−','-'))
  if key in values and values[key]!=value:conflicts.append(key)
  values[key]=value
 return {'month':int(month[1]),'choice':int(chosen[1]),'nominal_visible_changes':values,'conflicts':conflicts,'kind':entry.get('entry_type')}
def main():
 root=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1';p=root/'official-player-logs.json';entries=json.loads(p.read_text())['entries'];rows=[r for e in entries if (r:=parse_entry(e)) is not None]
 assert len(rows)==201
 assert all(not r['conflicts'] for r in rows)
 assert parse_entry({'message':'Month 1 | synthetic\nChose #1: example\nOutput +1\nNotes: Network -9','entry_type':'action'})['nominal_visible_changes']=={'output':1.0}
 report={'meaning':'Nominal visible returns extracted from our public player log. Not measured actual state deltas or hidden risk, not evidence of caps or policy efficacy. Notes excluded so predictions cannot masquerade as returns. Onboarding without Chose is excluded. No narrative retained.', 'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'n_entries':len(entries),'accepted_choice_records':len(rows),'records_with_visible_returns':sum(bool(r['nominal_visible_changes']) for r in rows),'kind_counts':dict(collections.Counter(r['kind'] for r in rows)),'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out=Path(__file__).resolve().parents[2]/'lab/reports/deepseek/gpt-principios/public-return-parser.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
