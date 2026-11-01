"""Freeze an actual-experience learning diagnostic from our own public tool outputs.
Narrative never leaves careerlab-data; designers see only availability and hashes.
"""
import collections,hashlib,importlib.util,json,random,shlex
from pathlib import Path
from gpt_format_trace import DATA as SOURCES,ROOT,REPORT,records,node,sha
DATA=Path.home()/'careerlab-data/deepseek/gpt-learning-feedback'
G=('skill','network','output')

def prepare(holdout=False):
    pool={True:[],False:[]};sources={};seen=set()
    for path in sorted(SOURCES.glob('sv[13]-g*/output/events-*.jsonl')):
        report=json.loads((path.parent/'score_report.json').read_text());script=Path(report['submission_dir'])/'skills/career-advisor/script/advisor.py';sp=importlib.util.spec_from_file_location('history_reader',script);a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
        rows,*_=records(path)
        # Independently parsed tool panels are joined by canonical content, never object identity.
        ts=transitions_by_content(path);past=[];sources[str(path)]=sha(path)
        for index,row in enumerate(rows):
            if not row.get('accepted') or not row['obs']:continue
            o=row['obs'];s=o['current_state'];month=s['time']['current_month']
            try:parts=[t for t in shlex.split(row['command']) if 'sid=' in t and 'phase=' in t]
            except ValueError:continue
            if len(parts)!=1:continue
            st,opts=a.parse(parts[0])
            if st['phase']!='story' or str(s['status']['level'])!='L1' or month>11:continue
            title=o.get('current_event',{}).get('title');nid=node(o)
            eligible=[p for p in past if p['title']!=title]
            if eligible and nid not in seen:
                teacher=eligible[-1];seen.add(nid);pool[month%6==5].append({'id':nid,'node':nid,'observe':o,'pre_review':month%6==5,'source':str(path),'teacher':teacher})
            key=panelkey(o);tr=ts.get(key);choice=row['choice'];pred=opts.get(choice,({},0))[0]
            if tr:
                surprise=[k for k,d in tr['delta'].items() if d<0 and pred.get(k,0)>=0]
                if surprise:past.append({'title':title,'event':o['current_event'],'choices':o['choices'],'chosen':choice,'before':s['status'],'after':tr['after'],'own_prediction':opts.get(choice),'surprised_stats':surprise,'row_index':index,'month':month})
    rng=random.Random(2026102810);selected=[]
    for pre in (True,False):
        rows=sorted(pool[pre],key=lambda r:r['id']);rng.shuffle(rows);selected+=rows[:8]
    if len(selected)<12:raise ValueError(f'Insufficient contexts: pre={len(pool[True])},other={len(pool[False])}')
    rng.shuffle(selected)
    excluded=[r['id'] for r in selected]
    if holdout:
        selected=sorted([r for group in pool.values() for r in group if r['id'] not in excluded],key=lambda r:r['id'])
        random.Random(2026102811).shuffle(selected)
    data=DATA.with_name(DATA.name+'-holdout') if holdout else DATA
    data.mkdir(parents=True,exist_ok=True);p=data/'items.json';text=json.dumps(selected,ensure_ascii=False,indent=2)+'\n'
    if p.exists():assert p.read_text()==text,'Source or selection changed after freezing'
    else:p.write_text(text)
    plan={'n_items':len(selected),'n_calls_max':len(selected)*2,'arms':['history_only','observed_outcome'],'model':'haiku','source_sha256':sources,'input_sha256':sha(p),'seed':2026102810,
          'selection':[{'id':r['id'],'pre_review':r['pre_review'],'teacher_month':r['teacher']['month'],'teacher_row_index':r['teacher']['row_index'],'teacher_title_sha256':hashlib.sha256(r['teacher']['title'].encode()).hexdigest()} for r in selected],
          'meaning':'Actual earlier isolated story action with an unforeseen visible growth cost, followed by a different-title target in the same recorded career. Both arms see the past event, original choice, prediction and before panel. Only outcome arm sees the after panel. No true hidden risk, catalog effects, future events or fixed event answers taught. Actual history is provided, not forced counterfactual prefix actions. One-step learning diagnostic, not a career score.'}
    if holdout:
        plan.update({'exploratory_targets_excluded':excluded,'scope':'All remaining eligible target nodes in the same five-source corpus. No target overlap, but teachers and careers overlap: not independent corpus replication. Frozen before new calls, same arms and endpoints; no Q inference.','seed':2026102811})
    p=REPORT/('learning-feedback-holdout-plan.json' if holdout else 'learning-feedback-plan.json')
    if p.exists():assert json.loads(p.read_text())==plan,'Frozen plan changed'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({'n':len(selected),'available_pre':len(pool[True]),'available_other':len(pool[False]),'max_calls':plan['n_calls_max']}))
    return selected

def panelkey(o):return hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest()
def transitions_by_content(path):
    # Re-implement the small pairing with stable content keys, never Python object identity across parsers.
    obs=None;pending={};unseen=[];out={}
    for line in path.open():
        e=json.loads(line);p=e.get('payload') or {}
        if 'delta' in p:continue
        if e.get('kind')=='tool_call':
            c=p['tool_call'];name=c['name'].replace('mcp_career-emulator-engine_','')
            if name=='take_action':pending[c['tool_call_id']]={'before':obs}
        elif e.get('kind')=='tool_result':
            try:v=json.loads((p.get('raw_output') or {}).get('result',''))
            except (ValueError,TypeError,AttributeError):continue
            name=str(p.get('tool_name',''))
            if name.endswith('take_action') and p.get('tool_call_id') in pending:
                r=pending.pop(p['tool_call_id'])
                if isinstance(v,dict) and v.get('success'):unseen.append(r)
            elif name.endswith('observe') and isinstance(v,dict) and 'current_state' in v:
                if len(unseen)==1 and unseen[0]['before']:
                    b=unseen[0]['before'];x=b['current_state'];y=v['current_state']
                    if x['time']['current_month']==y['time']['current_month'] and x['status']['level']==y['status']['level'] and 'landmines' not in str(v.get('events') or '').lower():
                        out[panelkey(b)]={'after':y['status'],'delta':{k:y['status'][k]-x['status'][k] for k in G}}
                unseen=[];obs=v
    return out
if __name__=='__main__':prepare()
