"""Frozen numeric-forecast constraint; no gold passed into selection."""
import json,copy,hashlib
from pathlib import Path
from gpt_panel_forecast import DATA,SOURCE,REPORT
from gpt_fact_second_read import ROOT
from gpt_decision_score import R,realised
G=('skill','network','output')
def choose(s,response):
 options={o['choice']:o['after'] for o in response['options']};first=response['recommended_choice']
 if all(options[first][g]>=s[g] for g in G):return first
 viable=[k for k,v in options.items() if all(v[g]>=s[g] for g in G) and v['health']>0 and v['dignity']>=s['dignity'] and v['wealth']>=s['wealth']]
 if not viable:return first
 return max(viable,key=lambda k:(min(options[k][g]-s[g] for g in G),sum(options[k][g]-s[g] for g in G),-k))
def main():
 assert (REPORT/'panel-constraint-plan.json').exists();items=json.loads((SOURCE/'items.json').read_text());cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));rows=[];changes=0
 for it in items:
  r=json.loads((DATA/it['id']/'result.json').read_text());assert r['done'];s=copy.deepcopy(it['observe']['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=it['observe']['current_state']['time']['current_month'];k=choose(s,r['response']);changes+=k!=r['response']['recommended_choice'];opts=cat.nodes[it['node']]['choices'];fx={int(c):realised({'state':s},v['d']) for c,v in opts.items()};risk={int(c):cat.answer_risk(it['node'],int(c)) for c in opts};safe=[c for c in fx if risk[c]<=0 and all(fx[c][g]>=0 for g in G) and s['health']+fx[c]['health']>0]
  for arm,c in (('original',it['original_choice']),('forecast',r['response']['recommended_choice']),('constraint',k)):
   loss=any(fx[c][g]<0 for g in G);rows.append({'id':it['id'],'arm':arm,'choice':c,'positive_risk':risk[c]>0,'growth_loss':loss,'avoidable_loss':bool(loss and safe),'health_zero':s['health']+fx[c]['health']<=0})
 keys=('positive_risk','growth_loss','avoidable_loss','health_zero');arms={a:{key:sum(x[key] for x in rows if x['arm']==a) for key in keys} for a in ('original','forecast','constraint')};out={'meaning':'Posthoc fixed selector on24historical states, no new model information. Gold only evaluator; no Q or DS claim. Choice-index tie break is only a research convention, not a validated strategy.','changes_from_forecast':changes,'arms':arms,'risk_admission_block':arms['constraint']['positive_risk']>arms['original']['positive_risk'],'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'panel-constraint-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
