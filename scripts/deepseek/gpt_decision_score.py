"""Score the frozen Haiku decision trial with v2 effects; no narrative output in Git.
Cluster intervals by title. Saved bank Q estimates and old fx risk values are not used.
"""
from __future__ import annotations
import argparse,collections,copy,dataclasses,gzip,hashlib,json,random,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
import replica as R
DATA=Path.home()/'careerlab-data/deepseek/gpt-decision-audit'
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
K=('health','dignity','skill','network','output','wealth')

def boot(title_rows,key,iterations=5000):
    # Equal title weighting, averaging contexts first; titles, not repeated contexts, are units.
    vals=[sum(x[key] for x in rows)/len(rows) for rows in title_rows.values()]
    rng=random.Random(271019);samples=sorted(sum(rng.choices(vals,k=len(vals)))/len(vals) for _ in range(iterations))
    return {'mean':sum(vals)/len(vals),'ci95':[samples[int(.025*iterations)],samples[int(.975*iterations)]],'n_titles':len(vals)}

def realised(it,fx):
    names={f.name for f in dataclasses.fields(R.State)}
    s=R.State(**{k:copy.deepcopy(v) for k,v in it['state'].items() if k in names})
    before={k:getattr(s,k) for k in K}
    delta=dict(fx)
    if delta.get('wealth',0)<0:delta['wealth']*=(s.level+1)//2
    R.apply_delta(s,delta)
    return {k:getattr(s,k)-before[k] for k in K}

def score(it,result,cat):
    if not result.get('done') or result.get('choice') is None:return None
    choice=int(result['choice']);node=it['node'];opts={int(k):v for k,v in cat.nodes[node]['choices'].items()}
    if choice not in opts:raise ValueError(f'Choice outside v2 catalog {it["id"]}')
    fx={k:realised(it,v['d']) for k,v in opts.items()};risk={k:cat.answer_risk(node,k) for k in opts}
    selected=fx[choice];dr=risk[choice]
    dominated=any(all(fx[k][s]>=selected[s] for s in K) and risk[k]<=dr and
                  (any(fx[k][s]>selected[s] for s in K) or risk[k]<dr) for k in opts if k!=choice)
    note=result.get('notes') or '';m=re.search(r'Draft\s+(\d+)\s*\|\s*Final\s+(\d+)',note,re.I)
    return {'positive_risk':int(dr>0),'risk_delta':dr,'avoidable_positive_risk':int(dr>0 and any(v<=0 for v in risk.values())),
            'dominated':int(dominated),'growth_loss':int(any(selected[k]<0 for k in R.GROWTH)),
            'pre_review_growth_loss':int(it['month']%6==5 and any(selected[k]<0 for k in R.GROWTH)),
            'audit_record':int(bool(m)),'revised':int(bool(m) and m[1]!=m[2]),'record_matches_action':int(bool(m) and int(m[2])==choice),
            **{k+'_delta':selected[k] for k in K}}

def run(partial):
    selection=json.loads((REPORT/'decision-audit-selection.json').read_text());items={r['id']:r for r in map(json.loads,(DATA/'items.jsonl').open())}
    assert hashlib.sha256((DATA/'items.jsonl').read_bytes()).hexdigest()==selection['input_sha256']
    catpath=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(catpath.read_text()))
    allrows=[];missing=[];models=collections.Counter();totals=collections.defaultdict(collections.Counter)
    for meta in selection['items']:
        iid=meta['id'];it=items[iid]
        for arm in ['native','audit']+(['repeat'] if iid in selection['repeat_ids'] else []):
            p=DATA/'runs'/arm/iid.replace(':','_')/'result.json'
            if not p.exists():missing.append((iid,arm));continue
            result=json.loads(p.read_text());sc=score(it,result,cat)
            if sc is None:missing.append((iid,arm));continue
            totals[arm].update(result.get('usage') or {})
            models.update(result.get('model_ids') or [])
            if not result.get('model_ids'):
                fallback_models=set()
                for line in (Path(result['raw'])/'stream.jsonl').open():
                    try:d=json.loads(line)
                    except ValueError:continue
                    if d.get('type')=='assistant' and d.get('message',{}).get('model'):fallback_models.add(d['message']['model'])
                models.update(fallback_models)
            allrows.append({'id':iid,'title_sha256':meta['title_sha256'],'arm':arm,'choice':result['choice'],**sc})
    if missing and not partial:raise SystemExit(f'{len(missing)} trials missing; no final comparison written')
    lookup={(r['id'],r['arm']):r for r in allrows};paired=collections.defaultdict(list);noise=collections.defaultdict(list)
    keys=['positive_risk','risk_delta','avoidable_positive_risk','dominated','growth_loss','pre_review_growth_loss']+[k+'_delta' for k in K]
    for meta in selection['items']:
        iid=meta['id'];a=lookup.get((iid,'native'));b=lookup.get((iid,'audit'));c=lookup.get((iid,'repeat'))
        if a and b:paired[meta['title_sha256']].append({k:b[k]-a[k] for k in keys}|{'same_choice':int(a['choice']==b['choice'])})
        if a and c:noise[meta['title_sha256']].append({k:c[k]-a[k] for k in keys}|{'same_choice':int(a['choice']==c['choice'])})
    out={'meta':{'selection_sha256':hashlib.sha256((REPORT/'decision-audit-selection.json').read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'catalog_sha256':hashlib.sha256(catpath.read_bytes()).hexdigest(),
        'complete':not missing,'n_missing':len(missing),'models':dict(models),
        'trial_stopping':'CLI terminated after target decision was recorded; emitted token totals omit the final CLI result and are not settled billing or full-career efficiency','meaning':'one-step Haiku decision test; visible deltas include bounds and scaled wealth losses, exclude risk explosions/settlement. Pre-review loss is joint incidence over all sampled decisions. Not a full-game score or evidence of DeepSeek transfer'},
        'arms':{},'audit_minus_native':{k:boot(paired,k) for k in keys+['same_choice']} if paired else {},
        'repeat_minus_native':{k:boot(noise,k) for k in keys+['same_choice']} if noise else {},'stream_reported_tokens':dict(totals)}
    for arm in ('native','audit','repeat'):
        rows=[r for r in allrows if r['arm']==arm]
        out['arms'][arm]={'n':len(rows),**({k:sum(r[k] for r in rows)/len(rows) for k in keys+['audit_record','revised','record_matches_action']} if rows else {})}
    if not partial:
        archive=REPORT/'decision-audit-rows.json.gz';raw=json.dumps(allrows,indent=1).encode();archive.write_bytes(gzip.compress(raw,mtime=0))
        out['raw_archive']={'file':archive.name,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(raw).hexdigest()}
        (REPORT/'decision-audit-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--partial',action='store_true');a=ap.parse_args();run(a.partial)
