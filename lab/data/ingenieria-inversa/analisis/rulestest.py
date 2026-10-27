import sys, json, copy, random, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, rules
BASE=dict(caps=copy.deepcopy(replica.CAPS), th=dict(replica.THRESH))
def scenario(name, cat):
    replica.CAPS.clear(); replica.CAPS.update(copy.deepcopy(BASE['caps'])); replica.THRESH.clear(); replica.THRESH.update(BASE['th']); replica.BLOW_AT=5
    if name=='caps-20': [c.update({k:max(1,round(v*0.8)) for k,v in c.items()}) for c in replica.CAPS.values()]
    if name=='caps+20': [c.update({k:round(v*1.2) for k,v in c.items()}) for c in replica.CAPS.values()]
    if name=='thr-20': replica.THRESH.update({l:tuple(max(1,round(x*0.8)) for x in t) for l,t in BASE['th'].items()})
    if name=='thr+20': replica.THRESH.update({l:tuple(round(x*1.2) for x in t) for l,t in BASE['th'].items()})
    if name=='draw20':
        rng=random.Random(5); smp=cat.d['sampler']; smp['weight']={t:w*rng.uniform(0.8,1.2) for t,w in smp['weight'].items()}
        smp['window']={t:[max(1,round(m0*rng.uniform(0.8,1.2))) if m0>1 else 1,m1] for t,(m0,m1) in smp['window'].items()}
    if name=='blow4': replica.BLOW_AT=4
    if name=='blow6': replica.BLOW_AT=6
def job(args):
    scen, off, n = args
    cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json')))
    scenario(scen, cat)
    on=[] if off=='ALL' else [r for r in rules.ALL if r!=off]
    return scen, off, replica.simulate(cat, rules.RuleBot(on), n, seed=777)['mean']
if __name__=='__main__':
    scens=sys.argv[1].split(','); n=int(sys.argv[2])
    jobs=[(s,o,n) for s in scens for o in (None,)+rules.ALL+('ALL',)]
    with mp.Pool(int(sys.argv[3])) as pool: res=pool.map(job,jobs)
    tab={}
    for s,o,m in res: tab[(s,o)]=m
    print('scenario | full | ' + ' | '.join('-'+r for r in rules.ALL) + ' | none')
    for s in scens:
        full=tab[(s,None)]
        print(s, '|', full, '|', ' | '.join(f"{tab[(s,r)]-full:+.2f}" for r in rules.ALL), '|', tab[(s,'ALL')])
