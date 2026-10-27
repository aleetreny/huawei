import sys, json, time, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, game
cat=replica.Catalog(json.load(open('/home/user/rx/catalog_s.json')))
p=json.load(open('/home/user/rx/search_top.json'))[0][1]
base=planner.Planner(**p)
N=int(sys.argv[1]); n=int(sys.argv[2])
t=time.time(); b=[replica.Replica.score(game.play_game(cat, lambda g,d: g.policy_move(base,d), 7000+i).st) for i in range(N)]
print('base', round(statistics.mean(b),2), round(time.time()-t,1),'s')
ro=game.Rollout(base,n=n)
t=time.time(); r=[replica.Replica.score(game.play_game(cat, ro.choose, 7000+i).st) for i in range(N)]
print('rollout n=%d'%n, round(statistics.mean(r),2), round(time.time()-t,1),'s', 'paired diff', round(statistics.mean(x-y for x,y in zip(r,b)),2))
