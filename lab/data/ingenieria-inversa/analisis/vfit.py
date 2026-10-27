import sys, json, time, multiprocessing as mp, numpy as np, pickle, statistics
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica, planner, valuefn
CATP='/home/user/huawei/lab/data/ingenieria-inversa/catalog_v2.json'
P=json.load(open('/home/user/rx/search2_top.json'))[2][1]
def gen(seed):
    cat=replica.Catalog(json.load(open(CATP))); return valuefn.generate(cat,P,int(sys.argv[1]),seed)
if __name__=='__main__':
    t=time.time()
    with mp.Pool(4) as pool: res=pool.map(gen,range(1,5))
    X=np.vstack([r[0] for r in res]); Y=np.concatenate([r[1] for r in res])
    print('samples',X.shape, 'gen s',round(time.time()-t))
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    Xtr,Xte,ytr,yte=train_test_split(X,Y,test_size=0.1,random_state=0)
    m=HistGradientBoostingRegressor(max_iter=400,learning_rate=0.08,max_leaf_nodes=63).fit(Xtr,ytr)
    pred=m.predict(Xte); print('value R2',round(1-np.sum((pred-yte)**2)/np.sum((yte-yte.mean())**2),3))
    pickle.dump(m,open('/home/user/rx/vmodel.pkl','wb'))
