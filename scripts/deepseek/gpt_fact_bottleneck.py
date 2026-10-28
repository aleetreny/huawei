"""Posthoc diagnosis only; gold never supplied to actors or turned into a candidate."""
import json,copy,hashlib
from pathlib import Path
from gpt_fact_career_score import DATA,FIRST,REPORT,ROOT,R,realised,select

def main():
 items=json.loads((FIRST/'items.json').read_text());cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));rows=[]
 for it in items:
  r=json.loads((DATA/it['id']/'result.json').read_text());assert r['done'];response=r['response'];flags={v['choice']:{f:v[f]['answer'] for f in ('time_diversion','relationship_rupture','unresolved_issue','personal_payment')} for v in response['options']}
  s=copy.deepcopy(it['observe']['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=it['observe']['current_state']['time']['current_month'];opts=cat.nodes[it['node']]['choices'];fx={int(k):realised({'state':s},v['d']) for k,v in opts.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in opts}
  safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and s['health']+fx[k]['health']>0];first=it['original_choice'];chosen,triggers=select(first,response,s['wealth']);fields=['time_diversion','relationship_rupture','unresolved_issue']+(['personal_payment'] if s['wealth']<=0 else [])
  if (safe and any(fx[first][g]<0 for g in R.GROWTH)) or chosen!=first:
   rows.append({'id':it['id'],'month':s['month'],'original':first,'recommendation':response['recommended_choice'],'gate':chosen,'original_true_growth_loss':any(fx[first][g]<0 for g in R.GROWTH),'original_flag_triggers':triggers,'true_safe_options':safe,'safe_option_flags':{str(k):flags[k] for k in safe},'recommended_flags':flags[response['recommended_choice']],'gate_added_risk':risk[chosen]>0 and risk[first]<=0,'recommended_passes_text_gate':all(flags[response['recommended_choice']][f]=='no' for f in fields)})
 out={'meaning':'Posthoc bottleneck attribution on saved replies, not a new rule, efficacy trial or proposal to use gold. Only numeric IDs/flags, no narrative.','rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'fact-bottleneck.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
