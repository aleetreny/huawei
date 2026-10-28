"""Four-way research test of fictitious risk credit, using the actual delivered advisor.
Only own replica and frozen readings. Does not modify candidate files, run games or call models.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,math,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/formato'))
import simadv as S

def patch(adv,arm):
    value,step=adv.value,adv.step
    if arm in ('marginal','both'):
        def clipped_value(st,mem,fx,risk):
            effective=max(risk,-adv.risk_level(mem))
            return value(st,mem,fx,effective)
        adv.value=clipped_value
    if arm in ('floor','both','verified_only'):
        def bounded_step(st,opts,mem):
            result=step(st,opts,mem)
            if arm=='verified_only' and st.get('phase')=='story':
                claimed=opts.get(result[0],({},0))[1]
                if claimed<0:mem.d['risk_since']-=claimed
            mem.d['risk_since']=max(-mem.d.get('hr',0),mem.d.get('risk_since',0))
            return result
        adv.step=bounded_step
    return adv

def summarize(rows):
    qs=[r['q'] for r in rows];mean=sum(qs)/len(qs);n=len(qs)
    return {'n':n,'mean':mean,'se':math.sqrt(sum((q-mean)**2 for q in qs)/(n-1)/n),
            'completed':sum(r['failure'] is None for r in rows),'failure_counts':dict(__import__('collections').Counter(r['failure'] or 'completed' for r in rows)),
            'mean_level':sum(r['level'] for r in rows)/n}

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=800);ap.add_argument('--seed',type=int,default=202610280);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--arms',default='baseline,floor,marginal,both');a=ap.parse_args()
    path=ROOT/'lab/policies-src/formato/script-v1/bundle/skills/career-advisor/script/advisor.py'
    lp=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)]
    labs=[json.loads(p.read_text()) for p in lp];raw={};results={}
    for arm in a.arms.split(','):
        adv=patch(S.load_advisor(str(path)),arm)
        per=S.G.Mixed([S.G.Perception(lab,'signs','flag') for lab in labs]);rows=[]
        for i in range(a.games):
            pol=S.AdvisorPolicy(adv,per,a.seed+i);st,_=S.R.play(S.G.CAT,pol,random.Random(a.seed+i))
            rows.append({'seed':a.seed+i,'q':S.R.Replica.score(st),'failure':st.failure,'level':st.level,'blowups':st.blowups})
        raw[arm]=rows;results[arm]={'summary':summarize(rows)}
        if arm!='baseline':
            ds=[r['q']-b['q'] for r,b in zip(rows,raw['baseline'])];m=sum(ds)/len(ds);se=math.sqrt(sum((d-m)**2 for d in ds)/(len(ds)-1)/len(ds))
            results[arm]['paired_delta']={'mean':m,'se':se,'ci95':[m-1.96*se,m+1.96*se]}
        print(arm,json.dumps(results[arm]),flush=True)
    b=json.dumps(raw,indent=1).encode();archive=a.out.with_suffix('.json.gz');archive.write_bytes(gzip.compress(b,mtime=0))
    out={'meta':{'games':a.games,'seed':a.seed,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'advisor_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                 'label_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in lp],
                 'meaning':'Research replica conditioned on two frozen DS readings, as simadv. Four arms fixed before calls; no extra labels/caps/thresholds. Marginal effect floors risk decrease at currently estimated zero; tracking floor prevents storing risk below estimated zero. Not an actor score or proof of DS transfer.'},
         'arms':results,'archive':{'file':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(b).hexdigest()}}
    a.out.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run()
