"""Saved decisions versus a state-aware heuristic. Diagnostic utility is never game Q."""
import collections,copy,dataclasses,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
import replica as R
from planner import Planner
DATA=Path.home()/'careerlab-data/deepseek/gpt-decision-audit'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'

def run():
    catpath=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json'
    cat=R.Catalog(json.loads(catpath.read_text()));p=Planner(w_cont=0)
    groups=collections.defaultdict(list);fields={f.name for f in dataclasses.fields(R.State)}
    for it in map(json.loads,(DATA/'items.jsonl').open()):
        s=R.State(**{k:copy.deepcopy(v) for k,v in it['state'].items() if k in fields})
        # Fix hidden risk to zero in every context: visible-state sensitivity only.
        s.risk=0
        vals={int(k):p.value(None,s,v['d'],cat.answer_risk(it['node'],int(k))) for k,v in cat.nodes[it['node']]['choices'].items()}
        best=max(vals.values());opts={k for k,v in vals.items() if abs(v-best)<1e-9}
        r=json.loads((DATA/'runs/native'/it['id'].replace(':','_')/'result.json').read_text())
        groups[it['title']].append({'id':it['id'],'node':it['node'],'choice':r['choice'],'best':opts,'gap':best-vals[r['choice']], 'level':s.level,'month':s.month})
    pairs=[v for v in groups.values() if len(v)==2 and v[0]['node']==v[1]['node']]
    incompatible=[v for v in pairs if not v[0]['best']&v[1]['best']]
    out={'meaning':'Exploratory diagnostic, not game score/regret. Heuristic uses exact catalog effects and private caps/thresholds, hidden current risk fixed at zero, no continuation. Cannot establish native choice wrong or promise Skill transfer.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(catpath.read_bytes()).hexdigest(),
         'paired_titles_same_node':len(pairs),'native_changed':sum(v[0]['choice']!=v[1]['choice'] for v in pairs),
         'heuristic_optimal_sets_disjoint':len(incompatible),'native_changed_when_disjoint':sum(v[0]['choice']!=v[1]['choice'] for v in incompatible),
         'same_node_distinct_level':sum(v[0]['level']!=v[1]['level'] for v in pairs),
         'rows':[{'title_sha256':hashlib.sha256(t.encode()).hexdigest(),'contexts':[{**r,'best':sorted(r['best'])} for r in rs]} for t,rs in groups.items()]}
    (REPORT/'context-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':run()
