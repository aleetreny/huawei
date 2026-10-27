import sys, json, collections, statistics, random
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica
from bbdata import Batch
b=Batch(sys.argv[1]); real=[]; rl=collections.Counter(); rf=collections.Counter()
for g in b.games():
    if g['outcome'] not in ('completed','eliminated'): continue
    real.append(g['end']['q']); rl[g['final']['s'][4]]+=1; rf[(g['final']['flags'].get('failure_reason') or 'completed')[:12]]+=1
cat=replica.Catalog(json.load(open(sys.argv[2])))
sim=replica.simulate(cat, replica.Greedy(), int(sys.argv[3]), seed=99)
print('REAL n',len(real),'mean',round(statistics.mean(real),2),'levels',dict(sorted(rl.items())),dict(rf))
print('SIM ',sim)
