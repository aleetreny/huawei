"""Rebuild numerical evidence, keeping model counterfactuals separate from official observations."""
from __future__ import annotations
import argparse
import collections
import copy
import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path
from experiment import R, CATALOG, ROOT, Intervention


def stats(xs):
    xs=list(xs)
    if not xs:return {'n':0}
    m=statistics.mean(xs)
    se=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else 0
    return dict(n=len(xs),mean=m,se=se,ci95=[m-1.96*se,m+1.96*se])


def independent(a,b):
    x,y=stats(a),stats(b)
    d=x['mean']-y['mean']; se=math.hypot(x['se'],y['se'])
    return dict(difference=d,se=se,ci95=[d-1.96*se,d+1.96*se])


def finish_quarter(rep, start, name):
    st=copy.deepcopy(start); pol=Intervention(name); actions=[]
    for _ in range(4):
        a=pol.energy(rep,st)
        if a is None:break
        rep.energy_action(st,a);actions.append(a)
    a=pol.main(rep,st);rep.main_action(st,a);actions.append(a)
    return st, actions


def simulation_summary():
    result={}
    for folder in sorted((ROOT/'lab/reports/mecanicas-emergentes').glob('*/games.jsonl')):
        rows=[json.loads(x) for x in folder.read_text().splitlines()]
        if not rows or 'variant' not in rows[0]:continue
        groups=collections.defaultdict(dict)
        for row in rows:groups[row['variant']][row['seed']]=row
        if 'base' not in groups:continue
        base=groups['base']; arms={}
        for name,g in groups.items():
            paired=[g[s]['q']-base[s]['q'] for s in g if s in base]
            arms[name]={'score':stats(r['q'] for r in g.values()), 'paired_difference_vs_base':stats(paired),
                        'levels':dict(collections.Counter(r['level'] for r in g.values())),
                        'failures':dict(collections.Counter(r['failure'] or 'completed' for r in g.values()))}
        result[folder.parent.name]=arms
    return result


def official_summary(source, target):
    cat=R.Catalog(json.loads(CATALOG.read_text()));rep=R.Replica(cat)
    rows=[]; evidence=[]; bad=[]
    for path in sorted(source.glob('games-*.jsonl.gz')):
        with gzip.open(path,'rt') as f:
            for line in f:
                g=json.loads(line)
                name=g['par']['variant']
                if g['outcome']=='interrupted':
                    bad.append({'game':g['g'],'error':g.get('err')});continue
                row={'game':g['g'],'variant':name,'q':g['end']['q'],'level':g['final']['s'][4],
                     'completed':g['end']['done'],'outcome':g['end']['outcome'],'rejected':g['rej']}
                q0=g.get('probe',{}).get('quarter48')
                if q0:
                    start=R.State(**q0)
                    # Remaining energy is always the fresh quarterly budget at its first decision.
                    start.energy=3
                    ref,refa=finish_quarter(rep,start,'base')
                    opt,opta=finish_quarter(rep,start,'terminal_q')
                    chosen=ref if name=='base' else opt
                    settled = copy.deepcopy(chosen)
                    rep.month_change(settled)
                    official = g['final']['s']
                    nonwealth = [i for i in range(len(official)) if i != 7]
                    settlement_match = (g['final']['t'] == 49 and
                        all(settled.vis()[i] == official[i] for i in nonwealth) and
                        R.DISPLAY(settled.wealth) <= official[7] <= R.DISPLAY(settled.wealth + 0.9))
                    state_match=chosen.vis()==official
                    row.update(entry48=R.Replica.score(start),gain48=row['q']-R.Replica.score(start),
                               model_counterfactual_gain=R.Replica.score(opt)-R.Replica.score(ref),
                               official_minus_model=row['q']-R.Replica.score(chosen),state_match=state_match,
                               settlement_match=settlement_match, final_month=g['final']['t'],
                               salary=R.SALARY[chosen.level],
                               official_minus_settled_model=row['q']-R.Replica.score(settled),
                               health_final=g['final']['s'][0],dignity_final=g['final']['s'][1])
                    evidence.append({'game':g['g'],'variant':name,'start':q0,
                                     'baseline_actions':refa,'optimal_actions':opta,
                                     'baseline_model_final':ref.__dict__,'optimal_model_final':opt.__dict__,
                                     'official_final':g['final'],'official_score':g['end'],
                                     'last_actions':[s for s in g['steps'] if s[0]==48 and s[1] in ('q','m')]})
                rows.append(row)
    target.mkdir(exist_ok=True,parents=True)
    (target/'official-games.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    with gzip.open(target/'quarter-evidence.jsonl.gz','wt') as f:
        for r in evidence:f.write(json.dumps(r)+'\n')
    groups={n:[r for r in rows if r['variant']==n] for n in ['base','terminal_q']}
    reaching={n:[r for r in rs if 'entry48' in r] for n,rs in groups.items()}
    result={'interrupted':bad,'arms':{},'counterfactual_in_replica':stats(r['model_counterfactual_gain'] for r in rows if 'entry48' in r),
            'state_match_count':sum(r.get('state_match',False) for r in rows),
            'quarter_count':len(evidence),
            'settlement_match_count':sum(r.get('settlement_match',False) for r in rows),
            'settled_score_prediction_error':stats(r['official_minus_settled_model'] for r in rows if 'entry48' in r),
            'score_prediction_error':stats(r['official_minus_model'] for r in rows if 'entry48' in r)}
    for n,rs in groups.items():
        result['arms'][n]={'q_all':stats(r['q'] for r in rs),'gain48':stats(r['gain48'] for r in reaching[n]),
                           'completed':sum(r['completed'] for r in rs),'rejected':sum(r['rejected'] for r in rs),
                           'outcomes':dict(collections.Counter(str(r['outcome']) for r in rs))}
    if all(reaching.values()):
        result['adjusted_effect']=independent([r['gain48'] for r in reaching['terminal_q']], [r['gain48'] for r in reaching['base']])
        result['raw_effect']=independent([r['q'] for r in groups['terminal_q']], [r['q'] for r in groups['base']])
    contributions=collections.defaultdict(list)
    counts=collections.Counter()
    for item in evidence:
        b,o=item['baseline_model_final'],item['optimal_model_final']
        contributions['resilience'].append(.75*(o['health']+o['dignity']-b['health']-b['dignity']))
        contributions['network'].append((min(60,o['network'])-min(60,b['network']))/6)
        contributions['skill'].append((min(120,o['skill'])-min(120,b['skill']))/8)
        contributions['risk'].append(max(0,10-o['risk']-5*o['blowups'])-max(0,10-b['risk']-5*b['blowups']))
        counts['baseline_unused_energy']+=b['energy']>0
        counts['optimal_unused_energy']+=o['energy']>0
        counts['better_health_dignity']+=o['health']+o['dignity']>b['health']+b['dignity']
        counts['better_network']+=o['network']>b['network']
        counts['more_remaining_risk']+=o['risk']>b['risk']
    (target/'mechanism.json').write_text(json.dumps({'counts':dict(counts),
        'mean_model_score_contributions':{k:statistics.mean(v) for k,v in contributions.items()}},indent=2))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.iterdir()) if p.is_file()}
    (target/'raw-hashes.json').write_text(json.dumps({'source':str(source),'sha256':hashes},indent=2))
    (target/'manifest.json').write_bytes((source/'manifest.json').read_bytes())
    (target/'summary.json').write_text(json.dumps(result,indent=2))
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--official');a=ap.parse_args()
    report=ROOT/'lab/reports/mecanicas-emergentes'
    sim=simulation_summary();(report/'simulation-results.json').write_text(json.dumps(sim,indent=2))
    if a.official:
        print(json.dumps(official_summary(Path(a.official),report/'official-01'),indent=2))
    else:
        for name,arms in sim.items():
            print(name,{k:round(v['paired_difference_vs_base']['mean'],3) for k,v in arms.items()})

if __name__=='__main__':main()
