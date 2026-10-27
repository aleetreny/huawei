"""Audit the completion boundary from official observations and logs, without replay assumptions."""
import collections
import gzip
import hashlib
import json
import math
import sys
from pathlib import Path
from experiment import ROOT, R
sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
from bbdata import parse_choice_entry


def audit(folder):
    texts={}
    for p in folder.glob('texts-*.jsonl'):
        for line in p.open():
            r=json.loads(line);texts[r['id']]=r['t']
    rows=[]
    for p in sorted(folder.glob('games-*.jsonl.gz')):
        with gzip.open(p,'rt') as f:
            while True:
                try:
                    line=f.readline()
                except (EOFError,OSError):
                    print(f'Historical truncated gzip: {p}; only complete records kept',file=sys.stderr)
                    break
                if not line:break
                try:g=json.loads(line)
                except json.JSONDecodeError:break
                if not g.get('end',{}).get('done'):continue
                last=g['steps'][-1]
                logs=[(code,texts[tid]) for code,tid in g['logs']]
                salary=[msg for code,msg in logs if msg.startswith('Monthly base salary:')]
                decisions=[parse_choice_entry(msg) for code,msg in logs if code in ('A','F') and 'Chose #' in msg]
                decision=decisions[-1]
                lv=last[4][4]
                raww=g['end']['dims']['wealth'][0]
                expected_salary=R.SALARY[lv]
                before_raw=raww-expected_salary-decision['d'].get('wealth',0)
                out=dict(batch=folder.name,game=g['g'],last_month=last[0],last_phase=last[1],
                         final_month=g['final']['t'],salary_payments=len(salary),level=lv,
                         last_salary_log=salary[-1].split('\n')[0],
                         final_wealth=raww,pre_action_displayed_wealth=last[4][7],
                         salary=expected_salary,
                         salary_consistent=math.floor(before_raw+1e-8)==last[4][7],
                         duration_increment=g['final']['s'][5]-last[4][5])
                rows.append(out)
    return rows


def main():
    rows=[]
    for name in ('v03-validation','d01-planner2','d02-planner2b','c02-planner-real'):
        d=ROOT/'lab/data/ingenieria-inversa'/name
        if d.exists():rows+=audit(d)
    out=ROOT/'lab/reports/mecanicas-emergentes/settlement'
    out.mkdir(exist_ok=True)
    (out/'games.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    res={}
    for name in sorted(set(r['batch'] for r in rows)):
        a=[r for r in rows if r['batch']==name]
        res[name]=dict(n=len(a),final49=sum(r['final_month']==49 for r in a),pay48=sum(r['salary_payments']==48 for r in a),
                       salary_consistent=sum(r['salary_consistent'] for r in a),duration_plus1=sum(r['duration_increment']==1 for r in a),
                       levels=dict(collections.Counter(r['level'] for r in a)))
    (out/'summary.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))

if __name__=='__main__':main()
