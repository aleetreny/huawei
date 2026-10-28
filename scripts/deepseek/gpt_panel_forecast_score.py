"""Score forward predictions and decisions separately; no model or game calls."""
import json,hashlib,copy,collections
from gpt_panel_forecast import DATA,SOURCE,REPORT,STATS,validate
from gpt_decision_score import R,realised
from gpt_fact_second_read import ROOT

def main():
 plan=json.loads((REPORT/'panel-forecast-plan.json').read_text());p=SOURCE/'items.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['items_sha256'];items=json.loads(p.read_text());cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));rows=[];errors=[];missing=[];models=collections.Counter()
 for it in items:
  p=DATA/it['id']/'result.json'
  if not p.exists():missing.append(it['id']);continue
  r=json.loads(p.read_text());assert r['done'] and not r['error'];assert r['models']==['claude-sonnet-5-5'];models.update(r['models']);validate(it,r['response'])
  s=copy.deepcopy(it['observe']['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=it['observe']['current_state']['time']['current_month'];opts=cat.nodes[it['node']]['choices'];fx={int(k):realised({'state':s},v['d']) for k,v in opts.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in opts};safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and s['health']+fx[k]['health']>0]
  for pred in r['response']['options']:
   k=pred['choice']
   for stat in STATS:
    truth=s[stat]+fx[k][stat];delta=pred['after'][stat]-s[stat];actual=fx[k][stat]
    errors.append({'stat':stat,'absolute_error':abs(pred['after'][stat]-truth),'sign_correct':((delta>0)-(delta<0))==((actual>0)-(actual<0))})
  for arm,k in (('original',it['original_choice']),('forecast_reader',r['response']['recommended_choice'])):
   loss=any(fx[k][g]<0 for g in R.GROWTH);rows.append({'id':it['id'],'arm':arm,'choice':k,'positive_risk':risk[k]>0,'growth_loss':loss,'avoidable_pre_review_loss':bool(loss and safe),'health_zero_after':s['health']+fx[k]['health']<=0,'wealth_cost_when_display_nonpositive':s['wealth']<=0 and fx[k]['wealth']<0})
 if missing:print({'pending':len(missing),'complete':len(items)-len(missing)});return
 keys=('positive_risk','growth_loss','avoidable_pre_review_loss','health_zero_after','wealth_cost_when_display_nonpositive');arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(r[k] for r in rows if r['arm']==a) for k in keys}} for a in ('original','forecast_reader')}
 metrics={stat:{'n':sum(e['stat']==stat for e in errors),'mae':sum(e['absolute_error'] for e in errors if e['stat']==stat)/sum(e['stat']==stat for e in errors),'sign_accuracy':sum(e['sign_correct'] for e in errors if e['stat']==stat)/sum(e['stat']==stat for e in errors)} for stat in STATS}
 out={'meaning':'All24historical critical states. Numeric after-panel forecasts scored against own replica direct effects, not observed counterfactual outcomes. Displayed wealth is truncated; its MAE is conditional on displayed baseline. No Q/DS claim; source one career. Gold only after decisions.','models':dict(models),'arms':arms,'prediction_metrics':metrics,'risk_admission_block':arms['forecast_reader']['positive_risk']>arms['original']['positive_risk'],'rows':rows,'script_sha256':hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest()};(REPORT/'panel-forecast-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
