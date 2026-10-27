import riskint, sys, numpy as np
G=riskint.load(['b00-random-safe'])
G0=[x for x in G if x[2]==0]
print('noblow',len(G0))
for hi in (99,):
  for decay in (0,):
    d,err=riskint.fit(G0,'reset',iters=8,hi=hi,decay=decay)
# check also linear (no clip) by lo=-99
import riskint as r
def sim_noclip(seq,d):
    return sum(d.get(k,0) for k in seq if k not in('BLOW','MONTH'))
print('if no clipping same d exact:', np.mean([sim_noclip(s,d)==y for s,y,n in G0]))
