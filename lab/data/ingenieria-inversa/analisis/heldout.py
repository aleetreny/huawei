import sys, json, random, hashlib, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, rules, game
cat=replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json')))
P=planner.Planner(**json.load(open('/home/user/rx/search2_top.json'))[1][1]); RB=rules.RuleBot()
half=lambda t: int(hashlib.md5(t.encode()).hexdigest(),16)%2
agree=collections.Counter(); tot=collections.Counter(); regret=collections.defaultdict(float)
for i in range(int(sys.argv[1])):
    g=game.Game(cat, random.Random(60000+i))
    while True:
        d=g.next()
        if d is None: break
        a=g.policy_move(P,d)
        if d[0]=='e':
            node=d[1]; t=cat.nodes[node]['title']; h=half(t)
            ch=cat.nodes[node]['choices']
            if len(ch)>1:
                b=RB.story(g.rep,g.st,node)
                vals={int(k):P.value(g.rep,g.st,c['d'],P._risk(g.rep,node,int(k))) for k,c in ch.items()}
                tot[h]+=1; agree[h]+=int(a==b); regret[h]+=vals[a]-vals[b]
        g.apply(a)
for h in (0,1): print('title half',h,'decisions',tot[h],'agreement',round(agree[h]/tot[h],3),'mean regret (planner value units)',round(regret[h]/tot[h],3))
