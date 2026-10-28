"""Score the matched one-step capacity diagnostic; no model calls and no bank rollout Q."""
import collections,copy,hashlib,json
from pathlib import Path
from gpt_capacity_probe import DATA,REPORT,ROOT
from gpt_decision_score import R,realised

def main():
    plan=json.loads((REPORT/'capacity-probe-plan.json').read_text());p=DATA/'items.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['items_sha256'];items=json.loads(p.read_text())
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));rows=[];missing=[];models=collections.Counter()
    for it in items:
        o=it['observe'];st=copy.deepcopy(o['current_state']['status']);st['level']=int(str(st['level']).removeprefix('L'));st['month']=o['current_state']['time']['current_month'];state={'state':st}
        choices=cat.nodes[it['node']]['choices'];fx={int(k):realised(state,ch['d']) for k,ch in choices.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in choices}
        safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and st['health']+fx[k]['health']>0]
        for model in plan['models']:
            p=DATA/f'{model}-{it["id"]}'/'result.json'
            if not p.exists():missing.append((it['id'],model));continue
            res=json.loads(p.read_text());models.update(res.get('model_ids') or [])
            if not res['done'] or res['invalid'] or res['errors'] or res['skill_reads']<1:raise ValueError(f'Invalid transport: {p}')
            k=res['choice'];assert k in fx
            loss=any(fx[k][g]<0 for g in R.GROWTH)
            rows.append({'id':it['id'],'model':model,'pre_review':it['pre_review'],'choice':k,'positive_risk':risk[k]>0,'growth_loss':loss,
                         'avoidable_pre_review_loss':bool(it['pre_review'] and loss and safe),'avoidable_positive_risk':bool(risk[k]>0 and safe),'safe_alternatives':safe})
    if missing:print(json.dumps({'pending':len(missing),'available':len(rows)}));return
    results={model:{'n':sum(r['model']==model for r in rows),**{key:sum(bool(r[key]) for r in rows if r['model']==model) for key in ('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk')}} for model in plan['models']}
    pairs={r['id']:{} for r in rows}
    for r in rows:pairs[r['id']][r['model']]=r
    out={'meaning':'12 current-panel L1 decisions, six pre-review, same Skill and no previous logs. Counts are diagnostic only; no game score, whole-career effect, strong-model superiority or DS transfer inferred. Gold is used only after choices. Startup cap exception may affect positive-gain comparisons; no positive-gain ranking endpoint used.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'models':dict(models),'arms':results,'same_choice':sum(v['haiku']['choice']==v['sonnet']['choice'] for v in pairs.values()),'rows':rows}
    (REPORT/'capacity-probe-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
