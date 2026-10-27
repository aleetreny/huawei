import sys, json, pickle, statistics, random, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, valuefn
CATP='/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json'
P=json.load(open('/home/user/rx/search2_top.json'))[2][1]
def job(args):
    mix,start,n=args
    cat=replica.Catalog(json.load(open(CATP))); base=planner.Planner(**P)
    pol=base if mix is None else valuefn.ValuePolicy(pickle.load(open(sys.argv[1],'rb')),base,mix)
    return [replica.Replica.score(replica.play(cat,pol,random.Random(start+i))[0]) for i in range(n)]
if __name__=='__main__':
    mixes=[None]+[float(x) for x in sys.argv[2].split(',')]; N=int(sys.argv[3])
    jobs=[(m,600000+k*(N//4),N//4) for m in mixes for k in range(4)]
    with mp.Pool(4) as pool: res=pool.map(job,jobs)
    base=sum(res[0:4],[])
    for j,m in enumerate(mixes):
        r=sum(res[4*j:4*j+4],[]); d=[a-b for a,b in zip(r,base)]
        print('mix',m,'mean',round(statistics.mean(r),2),'paired diff vs planner',round(statistics.mean(d),2),'se',round(statistics.stdev(d)/len(d)**.5,2) if m is not None else '')
