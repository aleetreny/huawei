"""Compare all original critical choices with fresh-context reads; no model calls."""
import collections,copy,hashlib,json
from pathlib import Path
from gpt_fresh_context import DATA,REPORT,ROOT
from gpt_decision_score import R,realised

def main():
    plan=json.loads((REPORT/'fresh-context-plan.json').read_text());p=DATA/'items.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['items_sha256'];items=json.loads(p.read_text())
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    rows=[];missing=[];models=collections.Counter()
    keys=('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk','health_zero_after','dignity_zero_after','wealth_cost_when_display_nonpositive')
    for it in items:
        p=DATA/f'sonnet-{it["id"]}'/'result.json'
        if not p.exists():missing.append(it['id']);continue
        res=json.loads(p.read_text());assert res['done'] and not res['invalid'] and not res['errors'] and res['skill_reads']>=1
        assert res['model_ids']==[plan['original_model']];models.update(res['model_ids'])
        assert json.loads((p.parent/'item.json').read_text())['steps']==[it['observe']]
        assert (p.parent/'system_prompt.md').read_bytes() and hashlib.sha256((p.parent/'system_prompt.md').read_bytes()).hexdigest()==plan['system_prompt_sha256']
        assert 'original_choice' not in (p.parent/'item.json').read_text()
        st=copy.deepcopy(it['observe']['current_state']['status']);st['level']=int(str(st['level']).removeprefix('L'));st['month']=it['observe']['current_state']['time']['current_month']
        opts=cat.nodes[it['node']]['choices'];fx={int(k):realised({'state':st},ch['d']) for k,ch in opts.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in opts}
        safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and st['health']+fx[k]['health']>0]
        for arm,k in (('original_career',it['original_choice']),('fresh_context',res['choice'])):
            assert k in fx;loss=any(fx[k][g]<0 for g in R.GROWTH)
            rows.append({'id':it['id'],'node':it['node'],'month':st['month'],'level':st['level'],'arm':arm,'choice':k,
                         'positive_risk':risk[k]>0,'growth_loss':loss,'avoidable_pre_review_loss':bool(loss and safe),'avoidable_positive_risk':bool(risk[k]>0 and safe),
                         'health_zero_after':st['health']+fx[k]['health']<=0,'dignity_zero_after':st['dignity']+fx[k]['dignity']<=0,
                         'wealth_cost_when_display_nonpositive':st['wealth']<=0 and fx[k]['wealth']<0})
    if missing:print(json.dumps({'pending':len(missing),'available':len(items)-len(missing)}));return
    arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(bool(r[k]) for r in rows if r['arm']==a) for k in keys}} for a in ('original_career','fresh_context')}
    pairs={it['id']:{} for it in items}
    for r in rows:pairs[r['id']][r['arm']]=r
    out={'meaning':'Same-model/Skill/system prompt,24original pre-review states. Original historical career choices compared with fresh current panel plus last3earlier accepted notes. Not a randomized career comparison. All critical turns, not only mistakes. Prior notes are fallible self-reports. No future gold or original target choice shown to actor. No Q prediction or DS-transfer claim.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'models':dict(models),'arms':arms,
         'same_choice':sum(v['original_career']['choice']==v['fresh_context']['choice'] for v in pairs.values()),
         'paired_changes':{k:{'improved':sum(v['original_career'][k] and not v['fresh_context'][k] for v in pairs.values()),'worsened':sum(not v['original_career'][k] and v['fresh_context'][k] for v in pairs.values())} for k in keys},
         'risk_admission_block':arms['fresh_context']['positive_risk']>arms['original_career']['positive_risk'],'rows':rows}
    (REPORT/'fresh-context-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
