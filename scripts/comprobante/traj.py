import json,sys,os,re,glob,ast
from collections import Counter,defaultdict
def load(d):
    ev=[json.loads(l) for l in open(os.path.join(d,'events.jsonl'))]
    calls={}; obs=[]; order=[]
    for e in ev:
        p=e.get('payload')
        if p is None: continue
        if 'delta' in p: continue
        if e['kind']=='tool_call':
            tc=p.get('tool_call',{})
            try: args=json.loads(tc.get('arguments') or '{}')
            except: args={}
            calls[tc.get('tool_call_id')]=(tc.get('name','').split('_')[-1] if 'take_action' not in tc.get('name','') else 'take_action',args)
            order.append(('call',tc.get('name'),args))
        elif e['kind']=='tool_result':
            s=p.get('result') or ''
            if not isinstance(s,str): s=json.dumps(s)
            if '"current_state"' not in s: continue
            j=None
            for cand in (s, ):
                try: j=json.loads(cand); break
                except Exception: pass
            if j is None:
                try:
                    inner=ast.literal_eval(s)
                    if isinstance(inner,dict) and 'result' in inner: j=json.loads(inner['result'])
                except Exception:
                    try:
                        i=s.index('{"current_state"'); k=s.rindex('}')
                        j=json.loads(s[i:k+1].encode().decode('unicode_escape')) 
                    except Exception: j=None
            if j: order.append(('obs',j))
    return order
def traj(d):
    order=load(d)
    months={}  # month -> dict
    lastobs=None; actions=[]
    pending=None
    for it in order:
        if it[0]=='obs':
            j=it[1]; st=j['current_state']['status']; t=j['current_state']['time']['current_month']
            ev=j.get('current_event') or {}; ch=j.get('choices') or []
            m=months.setdefault(t,{'month':t,'level':st['level'],'first':dict(st),'last':dict(st),'events':[],'quarter':False,'hr':None})
            m['last']=dict(st)
            evs=j.get('events')
            if evs: m['events'].append(evs if isinstance(evs,str) else json.dumps(evs,ensure_ascii=False))
            titles=[c.get('action','') for c in ch]
            if any('Energy' in str(c) or 'energy' in str(c) for c in ch) or 'Quarter' in ev.get('title','') or 'quarter' in ev.get('title','').lower():
                m['quarter']=True
            lastobs=(t,ev.get('title',''),titles)
        else:
            name,args=it[1],it[2]
            if 'take_action' in name and lastobs:
                t,title,titles=lastobs
                c=args.get('choice'); 
                act=titles[c-1] if isinstance(c,int) and 0<c<=len(titles) else str(c)
                # batched quarter: once the Energy menu's budget is spent, later numbers refer to the main-action menu
                if title.startswith('Quarterly energy'):
                    COST={'High-intensity work':2,'Skill learning':2,'Defuse legacy risk':2,'Network maintenance':1,'Mental recovery':1,'Health recovery':1,'Prepare report materials':1,'Reserve energy (no action)':0}
                    MAIN=['Apply for a key project','Report results to your manager','Fight for resources','Apply for rotation','Showcase results','Build a mentorship','Repair a key relationship','Lay low and reduce risk','No action']
                    spent=getattr(traj,'_qspent',0)
                    if spent>=3 or act=='Reserve energy (no action)' and spent>0 and False:
                        act=MAIN[c-1] if isinstance(c,int) and 0<c<=len(MAIN) else str(c)
                        title='Quarterly main action (batched)'
                    else:
                        spent+=COST.get(act,0)
                    traj._qspent=spent
                else:
                    traj._qspent=0
                actions.append((t,title,act,args.get('notes','')))
    return months,actions
if __name__=='__main__':
    for d in sys.argv[1:]:
        months,actions=traj(d)
        r=json.load(open(os.path.join(d,'result.json')))
        print('####',d[-30:],r.get('quantitative_score'))
        prev=None
        for t in sorted(months):
            m=months[t]; s=m['last']
            promo='' 
            if prev and m['level']!=prev: promo=' <== PROMO'
            prev=m['level']
            print(f"m{t:02d} {m['level']} S{s['skill']:3d} N{s['network']:2d} O{s['output']:2d} H{s['health']:2d} D{s['dignity']:2d} W{s['wealth']:5.1f}{promo}")
        print('-- quarterly/main actions:')
        for t,title,act,notes in actions:
            if any(k in act for k in ('Energy','learning','maintenance','report materials','High-intensity','Defuse','recovery','Apply for','Lay low','Repair','Report results')):
                print(f"  m{t:02d} {act[:70]}")
