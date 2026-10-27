import sys, json, random, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner
from search import SPACE, INTS, sample
CAT=None
def init():
    global CAT; CAT=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v1.json')))
def run(args):
    p,n,seed=args; l6=0; sc=0
    for i in range(n):
        st,tr=replica.play(CAT,planner.Planner(**p),random.Random(seed+i))
        lv=1; m6=None
        for x in tr:
            if x[1]=='r' and x[2]['promoted']:
                lv+=1
                if lv==6: m6=x[0]
        l6+= (m6 is not None and m6<=42); sc+=replica.Replica.score(st)
    return l6/n, sc/n, p
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1])); N=int(sys.argv[2]); K=int(sys.argv[3])
    base=json.load(open('/home/user/rx/search_top.json'))[0][1]
    cands=[base]+[dict(sample(rng), end_from=48) for _ in range(K)]
    with mp.Pool(4,initializer=init) as pool: res=pool.map(run,[(p,N,7000) for p in cands])
    res.sort(key=lambda x:-x[0])
    for a,s,p in res[:6]: print(round(a,3),round(s,2),json.dumps(p))
    json.dump(res[:10],open('/home/user/rx/search6_top.json','w'))
