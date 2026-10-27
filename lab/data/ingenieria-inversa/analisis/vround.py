import sys, json, collections, math
sys.path.insert(0,'/home/user/huawei/scripts/ingenieria-inversa')
import replica
mode=sys.argv[1]
if mode=='round':
    replica.DISPLAY=lambda w: math.floor(w+0.5+1e-9); replica.DISP_LO, replica.DISP_HI=-0.5,0.49
elif mode=='bankers':
    replica.DISPLAY=lambda w: round(w); replica.DISP_LO, replica.DISP_HI=-0.5,0.5
replica.DEBUG=collections.Counter()
res=replica.validate(replica.Catalog(json.load(open('/home/user/huawei/lab/data/ingenieria-inversa/catalog_v1.json'))), ['v02-validation'], verbose=False)
print(mode,{k:res[k] for k in ('step_acc','promo_acc','score_mae')}, res['field_miss'])
for k,v in replica.DEBUG.most_common(6): print(v,k)
