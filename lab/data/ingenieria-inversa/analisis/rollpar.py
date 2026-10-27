import sys, json, statistics, multiprocessing as mp
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, game
def one(args):
    i,n,margin=args
    cat=replica.Catalog(json.load(open('/home/user/rx/catalog_s.json')))
    p=json.load(open('/home/user/rx/search_top.json'))[0][1]; base=planner.Planner(**p)
    ro=game.Rollout(base,n=n,margin=margin*n,kinds=('e',),seed=i)
    b=replica.Replica.score(game.play_game(cat, lambda g,d: g.policy_move(base,d), 20000+i).st)
    r=replica.Replica.score(game.play_game(cat, ro.choose, 20000+i).st)
    return b,r
if __name__=='__main__':
    N=int(sys.argv[1]); n=int(sys.argv[2]); m=float(sys.argv[3])
    with mp.Pool(int(sys.argv[4])) as pool: res=pool.map(one,[(i,n,m) for i in range(N)])
    d=[r-b for b,r in res]
    print('N',N,'base',round(statistics.mean(b for b,r in res),2),'rollout',round(statistics.mean(r for b,r in res),2),'diff',round(statistics.mean(d),2),'se',round(statistics.stdev(d)/len(d)**0.5,2))
