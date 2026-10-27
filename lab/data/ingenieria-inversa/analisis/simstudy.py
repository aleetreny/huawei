import sys, json, random, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica
cat=replica.Catalog(json.load(open('/home/user/rx/cat_test.json')))
pm=collections.defaultdict(list); comp=collections.defaultdict(list)
for i in range(300):
    st,tr=replica.play(cat,replica.Greedy(),random.Random(i))
    lv=1
    for x in tr:
        if x[1]=='r' and x[2]['promoted']: lv+=1; pm[lv].append(x[0])
    if st.failure is None:
        comp['level'].append(st.level*10*0.3); comp['wealth'].append(0.2*min(100,max(0,st.wealth)/80*100))
        comp['hd'].append(0.15*min(100,(st.health+st.dignity)*5)); comp['skill'].append(0.15*min(100,st.skill/1.2))
        comp['risk'].append(0.1*max(0,(10-st.risk-5*st.blowups)*10)); comp['net'].append(0.1*min(100,st.network/0.6))
        comp['S'].append(st.skill); comp['W'].append(st.wealth)
for lv in sorted(pm): print('reach L%d'%lv, len(pm[lv]), 'month dist', sorted(collections.Counter(pm[lv]).items()))
for k,v in comp.items(): print(k, round(sum(v)/len(v),2))
