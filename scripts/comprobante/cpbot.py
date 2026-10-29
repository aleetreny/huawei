"""Replica battery for cp-v9 candidate rules on top of techobot's V4Bot (exact/noisy perception)."""
import sys, random, collections, argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'techo')); sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ingenieria-inversa'))
import techobot as T
import replica as R
import numpy as np
FRIENDLY,QUIET=0,1
class CPBot(T.V4Bot):
    def __init__(self, per, seed=0, flags=None):
        super().__init__(per, seed, flags)
        f=flags or {}
        self.l5q=f.get('l5q','')          # 'out': 3x report + key project from L5; 'mix': learning+report+key project
        self.qlag=f.get('qlag','')        # 'prop': target the stat with least proportional growth since promotion (from qskill level)
        self.qoracle=bool(f.get('qoracle',False))  # target the stat with largest remaining fraction to the true threshold
        self.lockdown=bool(f.get('lockdown',False)) # after a blow-up: HR remark read one step worse for the rest of the run
        self.lockq=bool(f.get('lockq',False))       # after a blow-up: Defuse+Lay low every quarter only (stories unchanged)
        self.atpromo=None
        self.q1out=bool(f.get('q1out',False))   # level 1: Energy to Prepare report materials (x3), main action key project
        self.rfnarrow=int(f.get('rfnarrow',0))  # N=1 exception narrowed: loss-free options kept only if their risk <= this (replica risk units); 0 = wide (base)
        self.rf2=bool(f.get('rf2',False))   # review-first (step 4 before risk) also at N=2 when HR friendly, counter 0
        self.rf2l1=bool(f.get('rf2l1',False)) # same, only at level 1
        self.hpen=float(f.get('hpen',0))   # Grow: penalty per Health loss when Health below full
        self.hfrom=int(f.get('hfrom',8))
    def _tick(self, st):
        lv_before=self.lv
        super()._tick(st)
        if self.lv!=lv_before or self.atpromo is None:
            self.atpromo={k:max(1,getattr(st,k)) for k in R.GROWTH}
        if (self.lockdown or self.lockq) and st.blowups>=1 and self.hr<2:
            self._hr_true=self.hr
            self.hr=2 if self.lockdown else self.hr
    def _target(self, st):
        """which growth stat to buy this quarter"""
        if self.qoracle:
            th=R.THRESH.get(st.level,R.THRESH[6]); 
            fr={k:(th[i]-getattr(st,k))/max(1,th[i]) for i,k in enumerate(R.GROWTH)}
            fr={k:v for k,v in fr.items() if v>0}
            return max(fr,key=fr.get) if fr else 'skill'
        if self.qlag=='prop':
            g={k:getattr(st,k)/self.atpromo[k] for k in R.GROWTH if k not in self.stalled}
            if not g: return 'skill'
            return min(g,key=g.get)
        return None
    def story(self, rep, st, node):
        n=self.n_to_review(st)
        if self.rfnarrow and n==1 and self.hr in (0,1) and self.concerns==0:
            # emulate the narrow exception: a loss-free option with real risk above rfnarrow is NOT protected (looks like a plain risky option that also loses)
            orig_see=self.per.see
            cache={int(kk):orig_see(node,int(kk)) for kk in rep.cat.nodes[node]["choices"]}
            realrisk={int(kk):rep.cat.answer_risk(node,int(kk)) for kk in rep.cat.nodes[node]["choices"]}
            def see(nd,k):
                sg,rs=cache[k] if nd==node and k in cache else orig_see(nd,k)
                if nd==node and k in cache and rs>0 and realrisk[k]>self.rfnarrow and not any(sg[g]<0 for g in R.GROWTH):
                    sg=dict(sg); sg['output']=-1   # pretend it loses, so review_first drops it
                return sg,rs
            self.per.see=see
            try: return super().story(rep, st, node)
            finally: self.per.see=orig_see
        if (self.rf2 or (self.rf2l1 and st.level==1)) and n==2 and self.hr in (0,1) and self.concerns==0:
            # emulate review_first at N=2: drop options that lower a growth stat before the risk filter, if any remain
            orig_see=self.per.see
            cache={}
            for kk in rep.cat.nodes[node]["choices"]:
                cache[int(kk)]=orig_see(node,int(kk))
            safe=[k for k,(sg,rs) in cache.items() if not any(sg[g]<0 for g in R.GROWTH)]
            if safe and len(safe)<len(cache):
                def see(nd,k):
                    sg,rs=cache[k] if nd==node and k in cache else orig_see(nd,k)
                    if nd==node and k not in safe:
                        sg=dict(sg); sg['health']=-1; return sg, 3   # make it look risky and bad
                    return sg,rs
                self.per.see=see
                try: return super().story(rep, st, node)
                finally: self.per.see=orig_see
        if not self.hpen or st.health>self.hfrom:
            return super().story(rep, st, node)
        # count a Health loss like a growth loss: temporarily raise lossw effect by faking an extra negative growth sign
        orig_see=self.per.see
        def see(nd,k):
            signs,rs=orig_see(nd,k)
            if signs.get('health',0)<0:
                signs=dict(signs); 
                # mark as 'output' loss proxy only if output sign is 0 (so lossw counts it once)
                for key in ('output','network','skill'):
                    if signs[key]==0:
                        signs[key]=-1 if self.hpen>=1 else 0
                        break
            return signs,rs
        self.per.see=see
        try: return super().story(rep, st, node)
        finally: self.per.see=orig_see
    def energy(self, rep, st):
        self._tick(st)
        if st.energy==3: self._qstall_update(st)
        e=st.energy
        hr=self.hr
        if self.lockq and st.blowups>=1 and hr<2: hr=2
        if st.month>=46 or st.health<=4 or st.dignity<=4 or st.network<=0:
            return super().energy(rep,st)
        if hr!=FRIENDLY and e==3:
            return "Defuse legacy risk"
        if self.q1out and st.level==1 and e>=1:
            return "Prepare report materials" if st.output<R.cap(1,'output') else ("Network maintenance" if st.network<R.cap(1,'network') else "Health recovery" if st.health<10 else "Prepare report materials")
        if st.level>=self.qskill or (self.qoracle or self.qlag) and st.level>=4:
            tgt=self._target(st) if (self.qoracle or self.qlag) else None
            if tgt is None and self.l5q and st.level>=5:
                if self.l5q=='out':
                    return "Prepare report materials" if e>=1 else None
                if self.l5q=='mix':
                    if e>=2 and st.health>self.hguard: return "Skill learning"
                    return "Prepare report materials" if e>=1 else None
            if tgt=='skill' or (tgt is None):
                return super().energy(rep,st)
            if tgt=='output':
                return "Prepare report materials" if e>=1 else None
            if tgt=='network':
                return "Network maintenance" if e>=1 else None
        return super().energy(rep,st)
    def main(self, rep, st):
        self._tick(st)
        hr=self.hr
        if self.lockq and st.blowups>=1 and hr<2: hr=2
        if st.month>=46 or st.health<=4 or st.dignity<=4 or st.network<=0 or st.wealth<0:
            return super().main(rep,st)
        if hr not in (FRIENDLY,QUIET):
            return "Lay low and reduce risk"
        if (self.qoracle or self.qlag) and st.level>=4:
            tgt=self._target(st)
            return {'skill':"Apply for rotation",'output':"Apply for a key project",'network':"Build a mentorship"}[tgt]
        if self.l5q and st.level>=5:
            return "Apply for a key project"
        return super().main(rep,st)

_ARGS={}
def _init(a): _ARGS.update(a)
def _play(job):
    spec,i=job
    per=T.Perception(_ARGS['per'],seed=50_000+i,scale=_ARGS.get('scale',1.0))
    bot=CPBot(per,seed=i,flags=T.parse_arm(spec))
    st,trace=R.play(T.CAT,bot,random.Random(_ARGS['seed']+i))
    promos=[m for m,kind,*rest in trace if kind=='r' and rest[0].get('promoted')]
    return {"q":R.Replica.score(st),"level":st.level,"fail":st.failure or "ok","promos":promos,"skill":st.skill,"network":st.network,"output":st.output,"wealth":st.wealth,"blow":st.blowups,"month":st.month}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--arms',default='base'); ap.add_argument('--per',default='exact'); ap.add_argument('--games',type=int,default=1000); ap.add_argument('--seed',type=int,default=4242); ap.add_argument('--workers',type=int,default=4)
    a=ap.parse_args()
    for spec in a.arms.split(','):
        with ProcessPoolExecutor(a.workers,initializer=_init,initargs=({'per':a.per,'seed':a.seed},)) as ex:
            rows=list(ex.map(_play,[(spec,i) for i in range(a.games)],chunksize=25))
        blow=np.mean([r['blow'] for r in rows]); 
        print(T.summarize(f"{spec} [{a.per}]",rows)+f"\n{'':34s} blow-ups/game {blow:.3f}  mean N {np.mean([r['network'] for r in rows if r['fail']=='ok']):.1f}  mean O {np.mean([r['output'] for r in rows if r['fail']=='ok']):.1f}  mean W {np.mean([r['wealth'] for r in rows if r['fail']=='ok']):.1f}")
if __name__=='__main__': main()
