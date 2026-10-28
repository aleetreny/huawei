"""Numeric audit of our own full-pilot tool outputs; no package/database inspection.
Rows explicitly distinguish isolated same-month consequences from settlement transitions.
Catalog effects remain research diagnostics and never enter the submitted Skill.
"""
from __future__ import annotations
import collections,copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
from careerlab.mcp_client import phase
import replica as R
DATA=Path.home()/'careerlab-data/deepseek/gpt-native-pilot'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
K=('health','dignity','skill','network','output','wealth','energy')

def decoded(block):
    x=block.get('content')
    if isinstance(x,list):x=''.join(b.get('text','') for b in x if isinstance(b,dict))
    if isinstance(x,dict):return x
    if not isinstance(x,str):return None
    try:return json.loads(x)
    except ValueError:return None

def snap(obs):
    s=obs['current_state'];d=s['status'];level=d['level']
    return {'month':s['time']['current_month'],'level':int(str(level).removeprefix('L')),**{k:d.get(k) for k in K}}

def node(obs):
    ev=obs.get('current_event') or {}
    key=json.dumps([ev.get('title'),ev.get('description'),[c.get('action') for c in obs.get('choices') or []]],ensure_ascii=False)
    return hashlib.sha1(key.encode()).hexdigest()[:12]

def extract(paths):
    pending={};seen=set();obs=None;rows=[];unobserved=None;logs=[];hr_by_month={}
    for path in paths:
        # A new CLI continuation has no prior tool IDs but continues the same game.
        for line in path.open(errors='replace'):
            try:m=json.loads(line)
            except ValueError:continue
            blocks=m.get('message',{}).get('content',[])
            if not isinstance(blocks,list):continue
            for b in blocks:
                if b.get('type')=='tool_use' and b.get('id') not in seen:
                    seen.add(b.get('id'));name=b.get('name','').split('__')[-1];args=b.get('input') or {}
                    pending[b.get('id')]={'name':name,'args':args}
                    if name=='take_action' and obs:
                        # Several actions without observing are not attributable to the stale menu.
                        row={'call_id_sha256':hashlib.sha256(str(b.get('id')).encode()).hexdigest(),'before':snap(obs),'phase':phase(obs),'choice':args.get('choice'),'node':node(obs),'stale_menu':unobserved is not None,'public_hr_tier':hr_by_month.get(snap(obs)['month'])}
                        opts=obs.get('choices') or [];selected=[c for c in opts if c.get('choice')==args.get('choice')]
                        # Only public quarterly action names are retained; event text stays outside Git.
                        if row['phase'] in ('energy','main_action'):row['quarter_action']=selected[0].get('action') if selected else None
                        rows.append(row);pending[b.get('id')]['row']=row
                        if unobserved is not None:unobserved['multiple_actions_before_observe']=True
                        unobserved=row
                elif b.get('type')=='tool_result':
                    call=pending.pop(b.get('tool_use_id'),{});o=decoded(b)
                    if not isinstance(o,dict):continue
                    if call.get('name')=='take_action' and call.get('row') is not None:
                        call['row']['accepted']=o.get('success') is True
                    if call.get('name')=='check_latest_logs':logs.extend(o.get('entries') or [])
                    if 'current_state' in o and isinstance(o['current_state'],dict) and 'status' in o['current_state']:
                        obs=o
                        tier=R.hr_level(o.get('events') or '')
                        if tier is not None:hr_by_month[snap(o)['month']]=tier
                        if unobserved:
                            after=snap(o);before=unobserved['before'];unobserved['after']=after
                            isolated=(before['month'],before['level'])==(after['month'],after['level']) and not unobserved.get('multiple_actions_before_observe') and not unobserved['stale_menu']
                            unobserved['isolated_same_month_level']=isolated
                            if isolated:unobserved['visible_delta']={k:after[k]-before[k] for k in K if isinstance(after[k],(int,float)) and isinstance(before[k],(int,float))}
                            unobserved=None
    return rows,logs

def audit():
    catpath=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(catpath.read_text()));allrows=[];games=[]
    for game in sorted(DATA.glob('game-*')):
        paths=sorted(game.glob('stream-*.jsonl'));rows,logs=extract(paths)
        counts=collections.Counter()
        for row in rows:
            counts['actions']+=1;counts['accepted']+=bool(row.get('accepted'));counts['isolated_observed_deltas']+=bool(row.get('isolated_same_month_level'))
            if row['phase']=='energy' and row.get('isolated_same_month_level') and row.get('quarter_action') not in ('Defuse legacy risk','Reserve energy (no action)'):
                counts['isolated_visible_energy_investments']+=1
                d=row.get('visible_delta') or {}
                no_gain=all(d.get(k,0)<=0 for k in K if k!='energy') and d.get('energy',0)<0
                row['no_positive_visible_return_energy_spent']=no_gain
                counts['energy_spent_no_positive_visible_return']+=no_gain
            if row['phase'] not in ('event','document') or row['stale_menu']:continue
            counts['stories']+=1;nd=cat.nodes.get(row['node']);choice=row['choice']
            if not nd or str(choice) not in nd['choices']:continue
            counts['catalog_matched_stories']+=1;dr=cat.answer_risk(row['node'],choice);row['catalog_risk_delta']=dr;counts['catalog_positive_risk']+=dr>0
            fx=nd['choices'][str(choice)]['d'];row['catalog_growth_losses']=[k for k in R.GROWTH if fx.get(k,0)<0]
            counts['catalog_growth_loss']+=bool(row['catalog_growth_losses'])
            counts['catalog_pre_review_growth_loss']+=bool(row['catalog_growth_losses']) and row['before']['month']%6==5
            if row.get('isolated_same_month_level') and row.get('accepted'):
                b=row['before'];s=R.State(**{k:v for k,v in b.items() if k!='level'}|{'level':b['level']})
                delta=copy.deepcopy(fx)
                if delta.get('wealth',0)<0:delta['wealth']*=(s.level+1)//2
                R.apply_delta(s,delta)
                checks={k:round(getattr(s,k)-b[k],6)==round(row['visible_delta'].get(k,0),6) for k in K if k!='energy'}
                row['replica_direct_delta_match']=checks
                row['startup_cap_exception_possible']=b['month']<=2
                counts['isolated_story_direct_predictions']+=1;counts['isolated_story_all_direct_visible_match']+=all(checks.values())
        allrows.extend({'game':game.name,**r} for r in rows)
        resultpath=game/'result.json';result=json.loads(resultpath.read_text()) if resultpath.exists() else {}
        from careerlab.truncate import log_facts
        logfile=game/'official-player-logs.json'
        if logfile.exists():logs=json.loads(logfile.read_text()).get('entries') or []
        facts=log_facts(logs)
        # Repeated log queries produce repeated entries: deduplicate each derived sequence by month.
        gates=[]
        for r in rows:
            b=r['before'];a=r.get('after') or {};review=a.get('month',0)
            if b['month']+1!=review or review%6 or not r.get('accepted') or r['stale_menu'] or r.get('multiple_actions_before_observe'):continue
            nd=cat.nodes.get(r['node'])
            if r['phase'] not in ('event','document') or not nd or str(r['choice']) not in nd['choices']:continue
            st=R.State(**b);fx=copy.deepcopy(nd['choices'][str(r['choice'])]['d'])
            if fx.get('wealth',0)<0:fx['wealth']*=(st.level+1)//2
            R.apply_delta(st,fx);th=R.THRESH.get(st.level,R.THRESH[6])
            gates.append({'review_month':review,'old_level':b['level'],'observed_after_level':a['level'],
                          'last_action_before_growth':{k:b[k] for k in R.GROWTH},
                          'predicted_after_last_action_growth':{k:getattr(st,k) for k in R.GROWTH},
                          'predicted_below_private_growth_gate':[k for k,t in zip(R.GROWTH,th) if getattr(st,k)<t],
                          'meaning':'Replica-derived after actual chosen last event, not a directly observed pre-review state; private gate only for research, no causal counterfactual.'})
        games.append({'game':game.name,'outcome':result.get('outcome','cancelled_before_start' if (game/'CANCELLED_BEFORE_START.json').exists() else 'running'),'Q':result.get('quantitative_score'),'counts':dict(counts),'review_gates_reconstructed':gates,
                      'blowup_months_observed_in_player_logs':sorted(set(facts['blowup_months'])),'hr_by_month_observed':facts['hr_by_month']|{str(r['before']['month']):r['public_hr_tier'] for r in rows if r.get('public_hr_tier') is not None},
                      'streams':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]})
    raw=json.dumps(allrows,indent=1).encode();archive=REPORT/'native-trace-rows.json.gz';archive.write_bytes(gzip.compress(raw,mtime=0))
    out={'meaning':'Public before/after evidence from the player; exact catalog predictions only research diagnostics. Month/level transitions and multiple actions excluded from isolated-delta checks. Direct-effect comparison does not simulate explosions or startup cap exceptions. No next-action causal claim from last pre-action panel. Running streams provisional.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(catpath.read_bytes()).hexdigest(),'games':games,
         'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(raw).hexdigest()}
    (REPORT/'native-trace-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'games':games},indent=2))
if __name__=='__main__':audit()
