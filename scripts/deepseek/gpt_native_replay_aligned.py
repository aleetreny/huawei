"""Correct old quarter attribution with accepted public logs; keep old output intact."""
import hashlib,json
from pathlib import Path
from gpt_native_replay import DATA,REPORT,ROOT,R,extract,simulate
from gpt_public_action_alignment import align

def main():
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));games=[]
    for d in sorted(DATA.glob('game-*')):
        p=d/'result.json'
        if not p.exists():continue
        actual=json.loads(p.read_text());rows,_=extract(sorted(d.glob('stream-*.jsonl')))
        rows,alignment=align(rows,json.loads((d/'official-player-logs.json').read_text())['entries'])
        arms={a:[simulate(cat,rows,a,w,[]) for w in (0,.9)] for a in ('replay_actual','observed_quarter','main_aware_quarter','calm_quarter')}
        qs=[r['Q'] for r in arms['replay_actual'] if r['Q'] is not None];real=actual['quantitative_score']
        faithful=bool(qs) and min(qs)-.5<=real<=max(qs)+.5 and all(r['completed']==(actual['outcome']=='completed') for r in arms['replay_actual'])
        games.append({'game':d.name,'actual_Q':real,'fidelity':faithful,**alignment,'arms':arms,'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    out={'meaning':'Correction of audit attribution only: actual public action logs replace stale prior quarterly menus. Original native-quarter-replay.json retained. Fixed actual story path/choices, no future stories in quarter ranking, no whole-agent Q inference. Alternative arms interpreted only if actual baseline reproduces outcome and Q within half a point.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'games':games}
    (REPORT/'native-quarter-replay-aligned.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{'game':g['game'],'real':g['actual_Q'],'fidelity':g['fidelity'],'repaired':g['stale_menu_quarter_attributions_repaired'],'arms':{a:[{'Q':r['Q'],'L':r['level'],'censored':r['censored_original_path']} for r in rs] for a,rs in g['arms'].items()}} for g in games],indent=2))
if __name__=='__main__':main()
