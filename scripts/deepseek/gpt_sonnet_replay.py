"""Diagnose the completed Sonnet reference using fixed actual stories, no model calls."""
import hashlib,json
from pathlib import Path
from gpt_native_replay import R,ROOT,REPORT,extract,simulate
from gpt_decision_score import realised
from gpt_public_action_alignment import align

def main():
    d=Path.home()/'careerlab-data/deepseek/gpt-sonnet-reference/run-1'
    p=d/'result.json';actual=json.loads(p.read_text())
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()))
    rows,_=extract(sorted(d.glob('stream-*.jsonl')))
    rows,alignment=align(rows,json.loads((d/'official-player-logs.json').read_text())['entries'])
    diagnostics=[]
    for row in rows:
        if row['phase'] not in ('event','document') or row['node'] not in cat.nodes:continue
        st=row['before'];options=cat.nodes[row['node']]['choices'];k=row['choice']
        fx={int(key):realised({'state':st},ch['d']) for key,ch in options.items()}
        risk={int(key):cat.answer_risk(row['node'],int(key)) for key in options}
        safe=[key for key in fx if risk[key]<=0 and all(fx[key][g]>=0 for g in R.GROWTH) and st['health']+fx[key]['health']>0]
        loss=any(fx[k][g]<0 for g in R.GROWTH)
        diagnostics.append({'month':st['month'],'level':st['level'],'positive_risk':risk[k]>0,
                            'growth_loss':loss,'avoidable_pre_review_loss':bool(st['month']%6==5 and loss and safe)})
    arms={a:[simulate(cat,rows,a,w,[]) for w in (0,.9)] for a in ('replay_actual','observed_quarter','main_aware_quarter','calm_quarter')}
    real=actual['quantitative_score'];baseline=arms['replay_actual'];qs=[r['Q'] for r in baseline if r['Q'] is not None]
    faithful=bool(qs) and min(qs)-.5<=real<=max(qs)+.5 and all(r['completed']==(actual['outcome']=='completed') for r in baseline)
    out={'meaning':'Fixed Sonnet story choices/path. Tests only quarter allocation against an observed path; different quarters could change subsequent model choices. No future story path passed to ranking, no whole-agent Q forecast. Interpret alternative arms only if actual quarter baseline reproduces outcome and Q within half a point. No hidden thresholds or event answers delivered as Skill.',
         'actual_Q':real,'baseline_fidelity_within_half_point_and_outcome':faithful,**alignment,'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'arms':arms,
         'story_diagnostics':{'n':len(diagnostics),**{key:sum(r[key] for r in diagnostics) for key in ('positive_risk','growth_loss','avoidable_pre_review_loss')},'rows':diagnostics}}
    (REPORT/'sonnet-quarter-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'actual_Q':real,'fidelity':faithful,'arms':{a:[{'Q':r['Q'],'L':r['level'],'failure':r['failure'],'censored':r['censored_original_path']} for r in rs] for a,rs in arms.items()}},indent=2))
if __name__=='__main__':main()
