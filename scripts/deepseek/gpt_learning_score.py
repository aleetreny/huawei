"""Score frozen experience-feedback decisions after collection; never call a model."""
import argparse,collections,copy,hashlib,json
from pathlib import Path
from gpt_learning_cases import DATA,REPORT,ROOT
from gpt_decision_score import R,realised

def main(holdout=False):
    name='learning-feedback-holdout' if holdout else 'learning-feedback'
    data=DATA.with_name(DATA.name+'-holdout') if holdout else DATA
    plan=json.loads((REPORT/f'{name}-plan.json').read_text())
    p=data/'items.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['input_sha256']
    items=json.loads(p.read_text());cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json'
    cat=R.Catalog(json.loads(cp.read_text()));rows=[];missing=[];models=collections.Counter()
    for it in items:
        o=it['observe'];st=copy.deepcopy(o['current_state']['status'])
        st['level']=int(str(st['level']).removeprefix('L'));st['month']=o['current_state']['time']['current_month']
        state={'state':st};choices=cat.nodes[it['node']]['choices']
        fx={int(k):realised(state,ch['d']) for k,ch in choices.items()}
        risk={int(k):cat.answer_risk(it['node'],int(k)) for k in choices}
        safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and st['health']+fx[k]['health']>0]
        for arm in plan['arms']:
            p=data/f'haiku-{it["id"]}-{arm}'/'result.json'
            if not p.exists():missing.append((it['id'],arm));continue
            res=json.loads(p.read_text());models.update(res.get('model_ids') or [])
            if not res['done'] or res['invalid'] or res['errors'] or res['skill_reads']<1:
                raise ValueError(f'Invalid transport: {p}')
            k=res['choice'];assert k in fx;loss=any(fx[k][g]<0 for g in R.GROWTH)
            rows.append({'id':it['id'],'arm':arm,'pre_review':it['pre_review'],'choice':k,
                         'positive_risk':risk[k]>0,'growth_loss':loss,
                         'avoidable_pre_review_loss':bool(it['pre_review'] and loss and safe),
                         'avoidable_positive_risk':bool(risk[k]>0 and safe)})
    if missing:print(json.dumps({'pending':len(missing),'available':len(rows)}));return
    keys=('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk')
    arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(bool(r[k]) for r in rows if r['arm']==a) for k in keys}} for a in plan['arms']}
    pairs={it['id']:{} for it in items}
    for r in rows:pairs[r['id']][r['arm']]=r
    out={'meaning':f'Paired one-step transfer, n={len(items)}, remaining targets={holdout}. Teachers/careers may overlap across studies; not independent corpus replication. Both arms have identical recorded history except the after panel. Gold only scores completed choices. No career Q, population efficacy or DeepSeek transfer inferred.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
         'models':dict(models),'arms':arms,'same_choice':sum(p['history_only']['choice']==p['observed_outcome']['choice'] for p in pairs.values()),
         'paired_changes':{k:{'improved':sum(p['history_only'][k] and not p['observed_outcome'][k] for p in pairs.values()),'worsened':sum(not p['history_only'][k] and p['observed_outcome'][k] for p in pairs.values())} for k in keys},
         'risk_admission_block':arms['observed_outcome']['positive_risk']>arms['history_only']['positive_risk'],'rows':rows}
    (REPORT/f'{name}-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--holdout',action='store_true');a=ap.parse_args();main(a.holdout)
