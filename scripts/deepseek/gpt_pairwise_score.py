"""Score both representation arms, retaining every result and incomplete case."""
import collections, copy, json
from gpt_pairwise_probe import DATA, REPORT, prepare
from gpt_panel_forecast_score import R, realised, ROOT

def main():
 items,_=prepare();cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));counts=collections.defaultdict(collections.Counter);missing=[]
 for it in items:
  s=copy.deepcopy(it['observe']['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=it['observe']['current_state']['time']['current_month']
  fx={int(k):realised({'state':s},v['d']) for k,v in cat.nodes[it['node']]['choices'].items()};risk={k:cat.answer_risk(it['node'],k) for k in fx}
  safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and s['health']+fx[k]['health']>0]
  for arm in ('absolute','pairwise'):
   p=DATA/arm/it['id']/'result.json'
   if not p.exists():missing.append([it['id'],arm]);continue
   r=json.loads(p.read_text())
   if not r['done']:missing.append([it['id'],arm,'failed']);continue
   k=r['response']['recommended_choice'];c=counts[arm];c['n']+=1;c['positive_risk']+=risk[k]>0;c['avoidable_growth_loss']+=bool(safe and any(fx[k][g]<0 for g in R.GROWTH));c['health_zero']+=s['health']+fx[k]['health']<=0
 out={'scope':'Immediate catalog-based outcomes in 24 historical states, no full-career or DeepSeek transfer claim. Partial counts are not comparable until both arms complete.','arms':dict(counts),'pending':len(missing)}
 (REPORT/'pairwise-probe-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
