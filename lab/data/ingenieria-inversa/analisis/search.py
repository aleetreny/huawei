import sys, json, random, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner
CAT=None
def init():
    global CAT; CAT=replica.Catalog(json.load(open('/home/user/rx/catalog_v1.json')))
SPACE=dict(w_below=(1,8),w_above=(0.1,1.5),w_skill_hi=(0.5,4),review_boost=(1,6),w_h=(0.1,1.5),w_d=(0.1,1.5),h_floor=(2,6),d_floor=(4,7),
           w_wealth=(0.1,2),risk_cost=(0,3),risk_cap=(2,4),w_cont=(0,1),end_from=(40,47),w_end=(0.3,3),low_n_risk=(0,1),defuse_at=(1,4),laylow_at=(2,4))
INTS={'h_floor','d_floor','risk_cap','end_from','low_n_risk','defuse_at','laylow_at'}
def sample(rng):
    p={}
    for k,(a,b) in SPACE.items():
        p[k]=rng.randint(a,b) if k in INTS else round(rng.uniform(a,b),2)
    return p
def evalp(args):
    p,n=args
    return replica.simulate(CAT,planner.Planner(**p),n,seed=1000)['mean'], p
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1])); N=int(sys.argv[2]); K=int(sys.argv[3])
    cands=[planner.DEFAULT]+[sample(rng) for _ in range(K)]
    with mp.Pool(int(sys.argv[4]),initializer=init) as pool:
        res=pool.map(evalp,[(p,N) for p in cands])
    res.sort(key=lambda x:-x[0])
    for m,p in res[:5]: print(m,json.dumps(p))
    json.dump(res[:10],open('/home/user/rx/search_top.json','w'))
