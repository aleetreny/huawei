"""Freeze a narrative ablation using only our previously observed public panels.
No model calls, effect labels or narrative output to designers. Not a Skill.
"""
import copy,hashlib,inspect,json,random
from pathlib import Path
from gpt_capacity_probe import ROOT,REPORT,BUNDLE
from gpt_format_trace import DATA as FORMATO,records,node,sha
from gpt_native_trace import decoded
DATA=Path.home()/'careerlab-data/deepseek/gpt-narrative-ablation'

def mask(o):
    out=copy.deepcopy(o)
    out['current_event']['title']='Story'
    out['current_event']['description']='Narrative withheld in this diagnostic. Choose among the offered actions.'
    return out

def trial_id(it,arm):
    """Reuse a legacy response only if its actual served panel matches this case."""
    legacy=it['id']+'-'+arm;d=DATA/f'haiku-{legacy}'
    expected=mask(it['observe']) if arm=='options_only' else it['observe']
    if not d.exists():return legacy
    p=d/'item.json'
    if p.exists() and json.loads(p.read_text())['steps'][0]==expected:return legacy
    suffix=hashlib.sha256(json.dumps(expected,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]
    return legacy+'-context-'+suffix

def observations(path):
    for line in path.open():
        try:m=json.loads(line)
        except ValueError:continue
        blocks=m.get('message',{}).get('content',[])
        if not isinstance(blocks,list):continue
        for b in blocks:
            if b.get('type')=='tool_result':
                o=decoded(b)
                if isinstance(o,dict) and 'current_state' in o and 'choices' in o:yield o

def prepare():
    pool={True:{},False:{}};hashes={}
    def add(o):
        status=o['current_state']['status'];m=o['current_state']['time']['current_month'];ev=o.get('current_event') or {}
        if str(status['level'])!='L1' or m>11 or ev.get('document') or 'remaining_energy' in ev or 'max_selections' in ev:return
        if len(o.get('choices') or [])<2:return
        pool[m%6==5].setdefault(node(o),o)
    for p in sorted(FORMATO.glob('sv[13]-g*/output/events-*.jsonl')):
        hashes[str(p)]=sha(p);rows,*_=records(p)
        for r in rows:
            if r.get('accepted') and r.get('obs'):add(r['obs'])
    base=Path.home()/'careerlab-data/deepseek'
    paths=sorted((base/'gpt-native-pilot').glob('game-*/stream-*.jsonl'))+sorted((base/'gpt-sonnet-reference/run-1').glob('stream-*.jsonl'))
    for p in paths:
        hashes[str(p)]=sha(p)
        for o in observations(p):add(o)
    rng=random.Random(2026102812);items=[]
    for pre,maximum in ((True,16),(False,16)):
        keys=sorted(pool[pre]);rng.shuffle(keys)
        for n in keys[:maximum]:items.append({'id':n,'node':n,'pre_review':pre,'observe':pool[pre][n]})
    assert len(items)>=24,'Too few eligible menus'
    rng.shuffle(items);DATA.mkdir(parents=True,exist_ok=True);p=DATA/'items.json';content=json.dumps(items,ensure_ascii=False,indent=2)+'\n'
    if p.exists():assert p.read_text()==content,'Frozen items changed'
    else:p.write_text(content)
    plan={'n_items':len(items),'n_calls_max':len(items)*2,'arms':['full','options_only'],'seed':2026102812,'input_sha256':sha(p),'source_sha256':hashes,
          'available':{str(k):len(v) for k,v in pool.items()},'selection':[{'id':it['id'],'pre_review':it['pre_review']} for it in items],
          'bundle_sha256':{str(p.relative_to(BUNDLE)):sha(p) for p in sorted(BUNDLE.rglob('*')) if p.is_file()},
          'meaning':'Information ablation, unchanged v4/Haiku. Same public state/options/events; mask only title and description. No previous logs. Selection without gold. Primary avoidable pre-review growth loss, risk increase blocks admission. Secondary total growth loss/resource safety. Exploratory bank, not game Q or DS transfer. May reuse menus from earlier studies; no independent-corpus claim.',
          'mask_sha256':hashlib.sha256(inspect.getsource(mask).encode()).hexdigest(),
          'masked_panels_sha256':[hashlib.sha256(json.dumps(mask(it['observe']),sort_keys=True,ensure_ascii=False).encode()).hexdigest() for it in items],
          'limits':{'five_hour':.65,'seven_day':.45,'max_claude_processes':4,'concurrency':1}}
    p=REPORT/'narrative-ablation-plan.json'
    if p.exists():assert json.loads(p.read_text())==plan,'Plan changed'
    else:p.write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({'n':len(items),'pre_review':sum(x['pre_review'] for x in items),'max_calls':len(items)*2,'available':plan['available']}))
    return items
if __name__=='__main__':prepare()
