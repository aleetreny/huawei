import sys, json, random, statistics, multiprocessing as mp, csv
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, game
P=json.load(open('/home/user/rx/search2_top.json'))[2][1]
def work(seed):
    cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json')))
    pol=planner.Planner(**P); rng=random.Random(seed); out=[]
    g=game.Game(cat, random.Random(seed))
    while True:
        d=g.next()
        if d is None: break
        if d[0]=='e' and rng.random()<0.05 and len(cat.nodes[d[1]]['choices'])>1:
            seeds=[rng.randrange(1<<30) for _ in range(24)]
            vals={}
            for k in cat.nodes[d[1]]['choices']:
                tot=[]
                for sd in seeds:
                    h=g.clone(sd); h.apply(int(k)); tot.append(h.finish(pol))
                vals[int(k)]=statistics.mean(tot)
            best=max(vals.values()); chosen=g.policy_move(pol,d)
            for k,v in vals.items():
                ch=cat.nodes[d[1]]['choices'][str(k)]
                out.append(dict(month=g.st.month,level=g.st.level,risk=g.st.risk,node=d[1],title=cat.nodes[d[1]]['title'],answer=k,
                                d=json.dumps(ch['d']),risk_delta=cat.answer_risk(d[1],k),exp_score=round(v,2),regret=round(best-v,2),policy_pick=int(k==chosen)))
        g.apply(g.policy_move(pol,d))
    return out
if __name__=='__main__':
    with mp.Pool(3) as pool: res=pool.map(work, range(int(sys.argv[1])))
    rows=[r for x in res for r in x]
    with open('/home/user/huawei/lab/data/ingenieria-inversa/answer_values.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    dec=[r for r in rows if r['policy_pick']]
    print('decision points',len(dec),'answers',len(rows))
    print('policy regret mean',round(statistics.mean(r['regret'] for r in dec),3),'share at best',round(sum(r['regret']<=0.01 for r in dec)/len(dec),3))
    allr=[r['regret'] for r in rows if not r['policy_pick']]
    print('regret of the other answers: mean',round(statistics.mean(allr),2),'median',round(statistics.median(allr),2),'max',max(allr))
    import collections
    byrisk=collections.defaultdict(list)
    for r in rows: byrisk[r['risk_delta']].append(r['regret'])
    for k in sorted(byrisk): print('answer risk',k,'mean regret',round(statistics.mean(byrisk[k]),2),'n',len(byrisk[k]))
