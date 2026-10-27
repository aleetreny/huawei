import sys, json, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner
def run(args):
    p,seed,n=args
    cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json')))
    return replica.simulate(cat,planner.Planner(**p),n,seed=seed)
if __name__=='__main__':
    cands=[('prev_best(c02)',json.load(open('search_top.json'))[0][1]),('h01',json.load(open('h01kw.json'))['params'])]+[('s2_%d'%i,x[1]) for i,x in enumerate(json.load(open('search2_top.json'))[:6])]
    jobs=[(p,900000+k*250,250) for name,p in cands for k in range(4)]
    with mp.Pool(4) as pool: res=pool.map(run,jobs)
    for j,(name,p) in enumerate(cands):
        rs=res[4*j:4*j+4]; m=sum(r['mean'] for r in rs)/4
        lv=sum(r['levels'].get(6,0)+r['levels'].get(7,0) for r in rs)/1000; tr=sum(r['outcomes'].get('trust',0) for r in rs)/1000
        print(name, round(m,2), 'L6+',round(lv,3),'trust',tr)
