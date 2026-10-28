"""Fixed observed story paths, alternative quarters. Research counterfactual, not an agent.
Does not rank using future stories. Baseline fidelity must be checked before interpreting changes.
"""
from __future__ import annotations
import collections,copy,hashlib,json,random,sys
from pathlib import Path
from gpt_principios import ROOT,R,Controller
DATA=Path.home()/'careerlab-data/deepseek/gpt-native-pilot'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
from gpt_native_trace import extract

class CalmQuarter(Controller):
    def energy(self,rep,st):
        self.sync(st)
        if self.hr>0 and st.energy>=2 and st.health>4:
            self.prev=('q',copy.copy(st),R.ENERGY_FX['Defuse legacy risk'][0],{},'',-1)
            return 'Defuse legacy risk'
        return super().energy(rep,st)
    def main(self,rep,st):
        self.sync(st)
        if self.hr>0:
            self.prev=('m',copy.copy(st),R.MAIN_FX['Lay low and reduce risk'],{},'',-1)
            return 'Lay low and reduce risk'
        return super().main(rep,st)

class MainAware(Controller):
    def sync(self,st):
        prev=self.prev
        super().sync(st)
        if not prev or prev[0]!='m':return
        _,old,fx,_,_,_=prev
        # Normal quarter closing advances one month; no review at that boundary.
        # Exclude public resource states that can cause persistent-condition growth penalties.
        if st.level!=old.level or st.month!=old.month+1 or st.month%6==0 or old.network<=0 or old.dignity<=1 or old.wealth<0:return
        for k in R.GROWTH:
            if fx.get(k,0)>0 and getattr(st,k)-getattr(old,k)<fx[k]:self.known[k]=getattr(st,k)

class ProposalGuard(MainAware):
    def __init__(self,*args,dominance=False):
        super().__init__(*args);self.dominance=dominance;self.switches=0;self.skipped_branching=0
    def propose(self,rep,st,node,native):
        nd=rep.cat.nodes[node]
        # Structural restriction of this research dataset: never invalidate recorded continuations.
        if any(ch.get('next') for ch in nd['choices'].values()):
            self.skipped_branching+=1;return native
        opts={}
        for kk in nd['choices']:
            k=int(kk);fx,risk,_,_=self.see(rep,st,node,k)
            rr=[lab[f'{node}:{k}'].get('risk','0') for lab in self.labels]
            risk=1 if any(str(r).startswith('+') for r in rr) else -1 if all(str(r).startswith('-') for r in rr) else 0
            delta={}
            for stat in ('health','dignity','skill','network','output','wealth'):
                cur=getattr(st,stat);x=fx.get(stat,0)
                if stat in R.GROWTH:
                    hi=max(cur,self.cap(st,stat));n=min(hi,cur+x) if x>0 else max(R.MINS[stat],cur+x)
                elif stat in ('health','dignity'):n=max(0,min(10,cur+x))
                else:n=cur+x*((st.level+1)//2 if x<0 else 1)
                delta[stat]=n-cur
            opts[k]=(fx,risk,delta)
        chosen=opts[native];allowed=[]
        if self.hr>=2 and chosen[1]>0:
            allowed=[k for k,v in opts.items() if v[1]<=0]
        if not allowed and self.dominance:
            allowed=[k for k,v in opts.items() if k!=native and v[1]<=chosen[1] and
                     all(v[2][a]>=chosen[2][a] for a in v[2]) and
                     (v[1]<chosen[1] or any(v[2][a]>chosen[2][a] for a in v[2]))]
        if not allowed:return native
        view=self.view(st);k=max(allowed,key=lambda k:self._val(view,opts[k][0],opts[k][1]))
        self.switches+=k!=native;return k

def simulate(cat,rows,arm,wealth_extra,labels):
    # Anchor after the documented startup cap exception, before any alternative quarter.
    start=next(r for r in rows if r['before']['month']==3 and r['node'] in cat.nodes)
    st=R.State(**start['before']);st.wealth+=wealth_extra;st.duration_in_level=3
    st.risk=start.get('public_hr_tier') or 0
    if st.risk>=4:raise ValueError('Ambiguous startup risk; do not guess')
    for m in (1,2,3):
        candidates=[r for r in rows if r['before']['month']==m]
        st.out_hist[m]=candidates[0]['before']['output'] if candidates else 0
    rep=R.Replica(cat,random.Random(0));by=collections.defaultdict(list)
    for r in rows:by[r['before']['month']].append(r)
    ctl=(ProposalGuard('hard_risk',0,labels,dominance=arm.endswith('dominance')) if arm.startswith('native_proposal') else {'main_aware_quarter':MainAware,'calm_quarter':CalmQuarter}.get(arm,Controller)('hard_risk',0,[]))
    promotions=[];spent=collections.Counter();stopped_at=None
    for m in range(3,49):
        rs=by.get(m,[]);stories=[r for r in rs if r['phase'] in ('event','document')]
        if not stories:
            stopped_at=m;break
        for r in stories:
            if r['stale_menu'] or r['node'] not in cat.nodes:raise ValueError('Unobserved or unknown story cannot be replayed')
            ctl.sync(st);choice=int(r['choice'])
            if isinstance(ctl,ProposalGuard):choice=ctl.propose(rep,st,r['node'],choice)
            rep.answer(st,r['node'],choice)
            if not st.alive:break
        if not st.alive:break
        if m%3==0:
            st.energy=3
            if arm=='replay_actual':
                for r in rs:
                    if r['phase']=='energy':
                        a=r['quarter_action'];cost=R.ENERGY_FX[a][1]
                        if cost>st.energy:raise ValueError('Stale quarter menu/action attribution')
                        rep.energy_action(st,a);spent[a]+=1
                mains=[r['quarter_action'] for r in rs if r['phase']=='main_action']
                if len(mains)!=1:raise ValueError('Missing or ambiguous main action')
                rep.main_action(st,mains[0]);spent[mains[0]]+=1
            else:
                while st.alive:
                    a=ctl.energy(rep,st)
                    if not a:break
                    rep.energy_action(st,a);spent[a]+=1
                if st.alive:
                    a=ctl.main(rep,st);rep.main_action(st,a);spent[a]+=1
        if not st.alive:break
        info=rep.month_change(st)
        if info.get('promoted'):promotions.append({'month':st.month,'level':st.level})
        if not st.alive:break
    complete=st.alive and st.month==49
    # A rescued but censored original path is not a completed counterfactual career.
    scored=complete or not st.alive
    return {'Q':R.Replica.score(st) if scored else None,'completed':complete,'alive':st.alive,'failure':st.failure,'month':st.month,'level':st.level,
            'skill':st.skill,'network':st.network,'output':st.output,'health':st.health,'dignity':st.dignity,'wealth':st.wealth,'risk':st.risk,'blowups':st.blowups,
            'promotions':promotions,'actions':dict(spent),'censored_original_path':stopped_at is not None,'learned':dict(ctl.known),'proposal_switches':getattr(ctl,'switches',0),'branching_guard_exclusions':getattr(ctl,'skipped_branching',0)}

def run():
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));games=[]
    lp=[Path.home()/f'careerlab-data/deepseek/labels/ds-v3-r{i}-full.json' for i in (1,2)];labels=[json.loads(p.read_text()) for p in lp]
    for d in sorted(DATA.glob('game-*')):
        p=d/'result.json'
        if not p.exists():continue
        actual=json.loads(p.read_text());rows,_=extract(sorted(d.glob('stream-*.jsonl')))
        if len([r for r in rows if r['before']['month']==3 and r['node'] in cat.nodes])==0:continue
        arms={a:[simulate(cat,rows,a,w,labels) for w in (0,.9)] for a in ('replay_actual','observed_quarter','main_aware_quarter','calm_quarter','native_proposal_risk','native_proposal_risk_and_dominance')}
        qs=[r['Q'] for r in arms['replay_actual'] if r['Q'] is not None];real=actual['quantitative_score']
        faithful=bool(qs) and min(qs)-.5<=real<=max(qs)+.5 and all(r['completed']==(actual['outcome']=='completed') for r in arms['replay_actual'])
        games.append({'game':d.name,'actual_Q':real,'baseline_fidelity_within_half_point_and_outcome':faithful,'arms':arms,'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    out={'meaning':'Exploratory fixed-story-path counterfactuals, not model behavior or a Q forecast. Native answers and future event path stay fixed; a different agent might choose differently. No future path is passed to quarter ranking. All pre-anchor actions unchanged. Starting displayed wealth spans +0..0.9. Censored rescued paths unscored. Baseline fidelity is an admission check, not full replica validation.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'labels_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in lp],'games':games}
    (REPORT/'native-quarter-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{'game':g['game'],'actual_Q':g['actual_Q'],'fidelity':g['baseline_fidelity_within_half_point_and_outcome'],'arms':{a:[{'Q':r['Q'],'L':r['level'],'failure':r['failure'],'censored':r['censored_original_path']} for r in rs] for a,rs in g['arms'].items()}} for g in games],indent=2))
if __name__=='__main__':run()
