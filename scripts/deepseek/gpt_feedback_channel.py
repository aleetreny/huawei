"""One-field HR intervention on saved inputs, with actual history held fixed.
Not a career replay: counterfactual memory is never carried into the actual next state.
"""
import copy,importlib.util,json,re,shlex,sys,hashlib
from pathlib import Path
from gpt_format_trace import ROOT,REPORT,DATA,records,node,R,sha

def visible_delta(o,fx):
    x=o['current_state']['status'];s=R.State(**{k:v for k,v in x.items() if k!='level'},level=int(str(x['level']).removeprefix('L')));before={k:getattr(s,k) for k in ('health','dignity','skill','network','output','wealth')};d=dict(fx)
    if d.get('wealth',0)<0:d['wealth']*=(s.level+1)//2
    R.apply_delta(s,d)
    return {k:getattr(s,k)-v for k,v in before.items()}

def audit(run,cat):
    root=DATA/run;rp=root/'output/score_report.json';report=json.loads(rp.read_text());script=Path(report['submission_dir'])/'skills/career-advisor/script/advisor.py';sp=importlib.util.spec_from_file_location('actual_advisor',script);adv=importlib.util.module_from_spec(sp);sp.loader.exec_module(adv)
    ep=next((root/'output').glob('events-*.jsonl'));rows,*_=records(ep);mems={};changes=[];compared=0
    for row in rows:
        m=re.search(r'CHOOSE\s+(\d+)',row['out'] or '')
        if not m:continue
        try:args=[x for x in shlex.split(row['command']) if 'sid=' in x and 'phase=' in x]
        except ValueError:continue
        if len(args)!=1:continue
        st,opts=adv.parse(args[0]);mem=mems.setdefault(st['sid'],adv.Memory(st['sid'],None));prior=copy.deepcopy(mem.d)
        original,_=adv.step(st,opts,mem);assert original==int(m[1]),'Original history no longer reproduces'
        public=row.get('public_hr')
        if not public or public['month']!=st['month'] or not row.get('accepted'):continue
        compared+=1;corrected=dict(st,hr=public['tier']);alt=adv.Memory('counterfactual',None);alt.d=prior;k,_=adv.step(corrected,opts,alt)
        if k==original:continue
        result={'month':st['month'],'phase':st['phase'],'level':st['level'],'passed_hr':st['hr'],'public_hr_tier':public['tier'],'old_choice':original,'new_choice':k}
        n=node(row['obs'])
        if st['phase']=='story' and n in cat.nodes and str(original) in cat.nodes[n]['choices'] and str(k) in cat.nodes[n]['choices']:
            for tag,c in [('old',original),('new',k)]:
                result[tag+'_risk_delta']=cat.answer_risk(n,c);delta=visible_delta(row['obs'],cat.nodes[n]['choices'][str(c)]['d']);result[tag+'_growth_loss']=any(delta.get(g,0)<0 for g in R.GROWTH)
        changes.append(result)
    sc=[c for c in changes if 'old_risk_delta' in c]
    return {'run':run,'report_sha256':sha(rp),'script_sha256':sha(script),'events_sha256':sha(ep),'comparable_accepted_decisions':compared,'changed':len(changes),'changed_stories_scored':len(sc),
            'old_positive_risk':sum(c['old_risk_delta']>0 for c in sc),'new_positive_risk':sum(c['new_risk_delta']>0 for c in sc),
            'old_growth_loss':sum(c['old_growth_loss'] for c in sc),'new_growth_loss':sum(c['new_growth_loss'] for c in sc),'changes':changes}

def main():
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));rs=[audit(x,cat) for x in ('sv1-g1','sv1-g2','sv3-g1','sv3-g2','sv3-g3')]
    r={'meaning':'One-step algorithm intervention: replace only passed HR ordinal with the contemporaneous public remark decoded by existing research parser. Same actual past memory, stats and option readings. Counterfactual history never propagated; no game Q forecast or inference about missed external outcomes. Unknown public feedback excluded. Quarter changes unscored.', 'script_sha256':sha(Path(__file__)),'parser_sha256':sha(ROOT/'scripts/deepseek/gpt_format_trace.py'),'catalog_sha256':sha(cp),'runs':rs}
    (REPORT/'feedback-channel-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k!='changes'} for r in rs],indent=2))
if __name__=='__main__':main()
