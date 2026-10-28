"""Score independent second reads and the predeclared gate. No model/game calls."""
import collections,copy,hashlib,json
from pathlib import Path
from gpt_fact_second_read import DATA,FIRST,REPORT,ROOT,validate
from gpt_narrative_cases import trial_id
from gpt_decision_score import R,realised

def select(first,response,wealth):
    options={r['choice']:r for r in response['options']};second=response['recommended_choice']
    fields=['time_diversion','relationship_rupture','unresolved_issue']
    if wealth<=0:fields.append('personal_payment')
    triggers=[f for f in fields if options[first][f]['answer']=='yes']
    safe=all(options[second][f]['answer']=='no' for f in fields)
    return (second if triggers and safe else first),triggers

def main():
    plan=json.loads((REPORT/'fact-second-read-plan.json').read_text());p=FIRST/'items.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['first_study_items_sha256']
    items=[it for it in json.loads(p.read_text()) if it['pre_review'] and it['id'] in plan['selection']]
    assert len(items)==plan['n']
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    rows=[];missing=[];models=collections.Counter();changes=0;disagrees=0;yes_count=0;rejected=[]
    keys=('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk','health_zero_after','dignity_zero_after','wealth_cost_when_display_nonpositive')
    for it in items:
        p=DATA/it['id']/'result.json';fp=FIRST/f'haiku-{trial_id(it,"full")}'/'result.json'
        if not p.exists() or not fp.exists():missing.append(it['id']);continue
        critic=json.loads(p.read_text());first=json.loads(fp.read_text())
        assert json.loads((fp.parent/'item.json').read_text())['steps'][0]==it['observe']
        assert critic['exit_code']==0 and critic['response'],p
        assert critic['done'] or critic['error']=='Nonliteral evidence',p
        assert first['done'] and not first['errors'] and not first['invalid'] and first['skill_reads']>=1,fp
        models.update(critic['models']);response=critic['response']
        if critic['done']:
            validate(it,response)
            yes_count+=sum(row[f]['answer']=='yes' for row in response['options'] for f in ('time_diversion','relationship_rupture','unresolved_issue','personal_payment'))
        else:rejected.append({'id':it['id'],'error':critic['error']})
        st=copy.deepcopy(it['observe']['current_state']['status']);st['level']=int(str(st['level']).removeprefix('L'));st['month']=it['observe']['current_state']['time']['current_month']
        f=first['choice'];second=response['recommended_choice']
        chosen,triggers=select(f,response,st['wealth']) if critic['done'] else (f,[])
        changes+=chosen!=f;disagrees+=second!=f
        opts=cat.nodes[it['node']]['choices'];fx={int(k):realised({'state':st},ch['d']) for k,ch in opts.items()};risk={int(k):cat.answer_risk(it['node'],int(k)) for k in opts}
        safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and st['health']+fx[k]['health']>0]
        for arm,k in (('first',f),('independent_read',second),('two_read_gate',chosen)):
            loss=any(fx[k][g]<0 for g in R.GROWTH)
            rows.append({'id':it['id'],'arm':arm,'choice':k,'positive_risk':risk[k]>0,'growth_loss':loss,
                         'avoidable_pre_review_loss':bool(loss and safe),'avoidable_positive_risk':bool(risk[k]>0 and safe),
                         'health_zero_after':st['health']+fx[k]['health']<=0,'dignity_zero_after':st['dignity']+fx[k]['dignity']<=0,
                         'wealth_cost_when_display_nonpositive':st['wealth']<=0 and fx[k]['wealth']<0,
                         'gate_triggers':triggers})
    if missing:print(json.dumps({'pending':len(missing),'available_pairs':len(items)-len(missing)}));return
    arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(bool(r[k]) for r in rows if r['arm']==a) for k in keys}} for a in ('first','independent_read','two_read_gate')}
    pairs={it['id']:{} for it in items}
    for r in rows:pairs[r['id']][r['arm']]=r
    out={'meaning':'Independent evidence-bound second read on16critical menus; first reader choice/notes withheld from critic. First reader is the cached full arm of narrative study, not selected by performance. Critic gets v4 inline and structured output, different task/delivery. No game-score/DS-transfer/population claim. Exact quote validation proves literal evidence presence, not entailment or actual stat effects. Gold used only in scoring.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
         'critic_models':dict(models),'n_evidence_valid':len(items)-len(rejected),'rejected_evidence_fallback_to_first':rejected,'n_valid_literal_yes_flags':yes_count,'critic_disagreements':disagrees,'gate_changes':changes,'arms':arms,
         'paired_gate_changes':{k:{'improved':sum(v['first'][k] and not v['two_read_gate'][k] for v in pairs.values()),'worsened':sum(not v['first'][k] and v['two_read_gate'][k] for v in pairs.values())} for k in keys},
         'risk_admission_block':arms['two_read_gate']['positive_risk']>arms['first']['positive_risk'],'rows':rows}
    (REPORT/'fact-second-read-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
