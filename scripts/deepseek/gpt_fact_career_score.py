"""Score independent second reads and the predeclared gate. No model/game calls."""
import collections,copy,hashlib,json
from pathlib import Path
from gpt_fact_career_read import DATA,SOURCE as FIRST,REPORT
from gpt_fact_second_read import ROOT,validate
from gpt_fact_second_score import select
from gpt_narrative_cases import trial_id
from gpt_decision_score import R,realised

def main():
    plan=json.loads((REPORT/'fact-career-plan.json').read_text());p=FIRST/'items.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['source_sha256']
    items=json.loads(p.read_text())
    assert len(items)==plan['n']
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    rows=[];missing=[];models=collections.Counter();changes=0;disagrees=0;yes_count=0;rejected=[]
    keys=('positive_risk','growth_loss','avoidable_pre_review_loss','avoidable_positive_risk','health_zero_after','dignity_zero_after','wealth_cost_when_display_nonpositive')
    for it in items:
        p=DATA/it['id']/'result.json'
        if not p.exists():missing.append(it['id']);continue
        critic=json.loads(p.read_text());first={'choice':it['original_choice']}
        assert critic['exit_code']==0 and critic['response'],p
        assert critic['done'] or critic['error']=='Nonliteral evidence',p
        assert critic['models']==['claude-sonnet-5-5']
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
    out={'meaning':'All24critical original Sonnet career decisions; same factual reader/gate, same model family. Critic sees current public panel and v4 inline, never original choice/notes. Historical comparison, not randomized career efficacy. Literal evidence is not proof of entailment or game effects. Invalid evidence retained/falls back. No game Q or DS transfer.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
         'critic_models':dict(models),'n_evidence_valid':len(items)-len(rejected),'rejected_evidence_fallback_to_first':rejected,'n_valid_literal_yes_flags':yes_count,'critic_disagreements':disagrees,'gate_changes':changes,'arms':arms,
         'paired_gate_changes':{k:{'improved':sum(v['first'][k] and not v['two_read_gate'][k] for v in pairs.values()),'worsened':sum(not v['first'][k] and v['two_read_gate'][k] for v in pairs.values())} for k in keys},
         'risk_admission_block':arms['two_read_gate']['positive_risk']>arms['first']['positive_risk'],'rows':rows}
    (REPORT/'fact-career-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
