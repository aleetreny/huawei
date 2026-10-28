"""Diagnose in-game versus standalone readings, including magnitude drift.
Own replica; saved labels only. Event-indexed maps are research data, never a submitted Skill.
"""
from __future__ import annotations
import argparse,collections,gzip,hashlib,json,math,random,shlex,sys
from pathlib import Path
from gpt_format_trace import records,node,DATA,ROOT,REPORT,sha
sys.path.insert(0,str(ROOT/'scripts/formato'))
import simadv as S

class Readings:
    def __init__(self,actual,fallback,full):self.actual,self.fallback,self.full=actual,fallback,full
    def see(self,n,k):
        if n not in self.actual or k not in self.actual[n]:return self.fallback.see(n,k)
        fx,r=self.actual[n][k]
        return ({s:v if self.full else (v>0)-(v<0) for s,v in fx.items()},r)

class Policy(S.AdvisorPolicy):
    def story(self,rep,st,n):
        opts={int(k):self.per.see(n,int(k)) for k in rep.cat.nodes[n]['choices']}
        return self.adv.step(self._view(st,'story'),opts,self.mem)[0]

def source(run):
    d=DATA/run;report=json.loads((d/'output/score_report.json').read_text());path=Path(report['submission_dir'])/'skills/career-advisor/script/advisor.py';adv=S.load_advisor(str(path));ep=next((d/'output').glob('events-*.jsonl'));rows,_,_,_=records(ep);mapping={};duplicates=0
    for row in rows:
        if not row['out'] or 'CHOOSE ' not in row['out'] or not row['obs'] or not row.get('accepted'):continue
        try:args=[t for t in shlex.split(row['command']) if 'sid=' in t and 'phase=' in t]
        except ValueError:continue
        if len(args)!=1:continue
        st,opts=adv.parse(args[0]);nid=node(row['obs'])
        if st['phase']!='story' or nid not in S.G.CAT.nodes:continue
        if set(opts)!={int(k) for k in S.G.CAT.nodes[nid]['choices']}:raise ValueError('Incomplete annotation; no oracle completion')
        if nid in mapping:
            duplicates+=1;continue
        mapping[nid]=opts
    return path,mapping,ep,duplicates

def summary(rows):
    qs=[r['q'] for r in rows];m=sum(qs)/len(qs);n=len(qs)
    return {'n':n,'mean':m,'se':math.sqrt(sum((q-m)**2 for q in qs)/(n-1)/n),'at_least_75':sum(q>=75 for q in qs),'completed':sum(r['failure'] is None for r in rows),'failures':dict(collections.Counter(r['failure'] or 'completed' for r in rows))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=400);ap.add_argument('--seed',type=int,default=202630280);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    lp=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)];labs=[json.loads(p.read_text()) for p in lp];out={};raw={}
    for run in ('sv1-g1','sv1-g2','sv3-g1','sv3-g2','sv3-g3'):
        path,mapping,ep,duplicates=source(run);out[run]={'nodes':len(mapping),'duplicate_occurrences_excluded':duplicates,'annotation_selection':'first acted occurrence per node','advisor_sha256':sha(path),'events_sha256':sha(ep),'arms':{}};raw[run]={}
        for arm in ('standalone','insitu_signs','insitu_full'):
            adv=S.load_advisor(str(path));rows=[]
            for i in range(a.games):
                mixed=S.G.Mixed([S.G.Perception(l,'signs','flag') for l in labs]);mixed.rng=random.Random(10_000+a.seed+i)
                per=Readings({} if arm=='standalone' else mapping,mixed,arm=='insitu_full');p=Policy(adv,per,a.seed+i)
                st,_=S.R.play(S.G.CAT,p,random.Random(a.seed+i));rows.append({'seed':a.seed+i,'q':S.R.Replica.score(st),'failure':st.failure,'level':st.level})
            raw[run][arm]=rows;out[run]['arms'][arm]={'summary':summary(rows)}
            if arm!='standalone':
                ds=[r['q']-b['q'] for r,b in zip(rows,raw[run]['standalone'])];m=sum(ds)/len(ds);se=math.sqrt(sum((x-m)**2 for x in ds)/(len(ds)-1)/len(ds));out[run]['arms'][arm]['paired_delta']={'mean':m,'ci95':[m-1.96*se,m+1.96*se]}
            print(run,arm,json.dumps(out[run]['arms'][arm]),flush=True)
    b=json.dumps(raw,indent=1).encode();archive=a.out.with_suffix('.json.gz');archive.write_bytes(gzip.compress(b,mtime=0))
    result={'meta':{'games_per_arm':a.games,'seed':a.seed,'script_sha256':sha(Path(__file__)),'labels_sha256':[sha(p) for p in lp],
                    'meaning':'Posthoc selected saved careers, new replica seeds. Replace annotations only on source-covered nodes; unseen nodes always use frozen DS baseline, never truth. Event-indexed annotations cannot be submitted. In-situ reading is frozen outside its original context: not an actor evaluation or proof of transfer. Full and sign arms differ only in magnitudes. Different source scripts must not be compared as randomized arms.'},'sources':out,'archive':{'file':archive.name,'sha256':sha(archive),'uncompressed_sha256':hashlib.sha256(b).hexdigest()}}
    a.out.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
