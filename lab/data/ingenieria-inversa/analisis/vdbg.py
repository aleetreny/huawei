import sys, json, collections
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica
replica.DEBUG=collections.Counter()
res=replica.validate(replica.Catalog(json.load(open(sys.argv[1]))), sys.argv[2].split(','), verbose=False)
print({k:res[k] for k in ('games','steps','step_acc','promo_acc','score_mae')}, res['field_miss'])
for k,v in replica.DEBUG.most_common(int(sys.argv[3]) if len(sys.argv)>3 else 30): print(v,k)
