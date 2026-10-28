"""Score the frozen narrative ablation. No model calls or career-score extrapolation."""
import collections,copy,hashlib,json
from pathlib import Path
from gpt_narrative_cases import DATA,REPORT,ROOT,trial_id,mask
from gpt_decision_score import R,realised

def main():
    plan=json.loads((REPORT/'narrative-ablation-plan.json').read_text());p=DATA/'items.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['input_sha256']
    items=json.loads(p.read_text());cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    rows=[];missing=[];models=collections.Counter()
    keys=('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk')
    resources=('health_zero_after','dignity_zero_after','wealth_cost_when_display_nonpositive')
    for index,it in enumerate(items):
        context_id=it['id']+'-'+hashlib.sha256(json.dumps(it['observe'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]
        o=it['observe'];st=copy.deepcopy(o['current_state']['status']);st['level']=int(str(st['level']).removeprefix('L'));st['month']=o['current_state']['time']['current_month']
        opts=cat.nodes[it['node']]['choices'];fx={int(k):realised({'state':st},ch['d']) for k,ch in opts.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in opts}
        safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and st['health']+fx[k]['health']>0]
        for arm in plan['arms']:
            p=DATA/f'haiku-{trial_id(it,arm)}'/'result.json'
            if not p.exists():missing.append((it['id'],arm));continue
            res=json.loads(p.read_text());models.update(res.get('model_ids') or [])
            served=json.loads((p.parent/'item.json').read_text())['steps'][0]
            assert served==(mask(o) if arm=='options_only' else o),'Response not bound to intended panel'
            assert res['done'] and not res['invalid'] and not res['errors'] and res['skill_reads']>=1,p
            k=res['choice'];assert k in fx;loss=any(fx[k][g]<0 for g in R.GROWTH)
            rows.append({'id':context_id,'node':it['node'],'arm':arm,'pre_review':it['pre_review'],'choice':k,'positive_risk':risk[k]>0,'growth_loss':loss,
                         'avoidable_pre_review_loss':bool(it['pre_review'] and loss and safe),'avoidable_positive_risk':bool(risk[k]>0 and safe),
                         'health_zero_after':st['health']+fx[k]['health']<=0,'dignity_zero_after':st['dignity']+fx[k]['dignity']<=0,
                         'wealth_cost_when_display_nonpositive':st['wealth']<=0 and fx[k]['wealth']<0})
    if missing:print(json.dumps({'pending':len(missing),'available':len(rows)}));return
    arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(bool(r[k]) for r in rows if r['arm']==a) for k in keys+resources}} for a in plan['arms']}
    pairs={r['id']:{} for r in rows};assert len(pairs)==len(items)
    for r in rows:pairs[r['id']][r['arm']]=r
    out={'meaning':'Exploratory paired information ablation with unchanged v4. Masked arm has actual options/state/remarks but no narrative title/description. No whole-game Q, no DS transfer, no independent-source claim. Gold scored only after decisions.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
         'models':dict(models),'arms':arms,'same_choice':sum(v['full']['choice']==v['options_only']['choice'] for v in pairs.values()),
         'paired_changes':{k:{'improved':sum(v['full'][k] and not v['options_only'][k] for v in pairs.values()),'worsened':sum(not v['full'][k] and v['options_only'][k] for v in pairs.values())} for k in keys+resources},
         'risk_admission_block':arms['options_only']['positive_risk']>arms['full']['positive_risk'],'rows':rows}
    (REPORT/'narrative-ablation-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
