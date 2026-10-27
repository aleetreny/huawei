import sys, json, time, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, game
cat=replica.Catalog(json.load(open('/home/user/rx/catalog_s.json')))
p=json.load(open('/home/user/rx/search_top.json'))[0][1]
base=planner.Planner(**p)
N=int(sys.argv[1]); n=int(sys.argv[2]); margin=float(sys.argv[3])
ro=game.Rollout(base,n=n,margin=margin*n,kinds=('e',))
dev=[0,0]
orig=ro.choose
def ch(g,d):
    a=g.policy_move(base,d); b=orig(g,d)
    if d[0]=='e': dev[0]+=1; dev[1]+=int(a!=b)
    return b
res=[]
for i in range(N):
    b=replica.Replica.score(game.play_game(cat, lambda g,d: g.policy_move(base,d), 9000+i).st)
    r=replica.Replica.score(game.play_game(cat, ch, 9000+i).st)
    res.append(r-b); print(i, round(b,2), round(r,2), flush=True)
print('paired diff', round(statistics.mean(res),2), 'deviation rate', round(dev[1]/max(1,dev[0]),3))
