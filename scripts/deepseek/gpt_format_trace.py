"""Audit saved DeepSeek script careers. Read own tool outputs/submission artifacts only.
Never imports the official engine, never calls a model or game tool. Narrative remains outside Git.
"""
from __future__ import annotations
import collections,hashlib,importlib.util,json,re,shlex,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/ingenieria-inversa'))
import replica as R
REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
DATA=Path.home()/'careerlab-data/formato/runs'
K=('health','dignity','skill','network','output','wealth')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def node(obs):
    ev=obs.get('current_event') or {}
    key=json.dumps([ev.get('title'),ev.get('description'),[c.get('action') for c in obs.get('choices') or []]],ensure_ascii=False)
    return hashlib.sha1(key.encode()).hexdigest()[:12]

def records(path):
    obs=None;latest_hr=None;rows=[];byid={};calls=collections.Counter();plain=0;sessions=set();action_rows={}
    for line in path.open():
        e=json.loads(line);p=e.get('payload') or {}
        if 'delta' in p:continue
        if e.get('kind')=='tool_call':
            c=p['tool_call'];name=c['name'].replace('mcp_career-emulator-engine_','');calls[name]+=1
            try:a=json.loads(c.get('arguments') or '{}')
            except ValueError:continue
            if name=='bash' and 'advisor.py' in a.get('command','') and 'sid=' in a['command']:
                row={'obs':obs,'public_hr':latest_hr,'command':a['command'],'out':None};rows.append(row);byid[c.get('tool_call_id')]=row
            elif name=='take_action':
                sessions.add(a.get('session_id'))
                available=[r for r in rows if r['obs'] is obs and 'choice' not in r and r['out'] is not None]
                if available:
                    available[-1]['choice']=a.get('choice');action_rows[c.get('tool_call_id')]=available[-1]
                else:plain+=1
        elif e.get('kind')=='tool_result':
            name=str(p.get('tool_name',''))
            if name.endswith('observe'):
                raw=p.get('raw_output') or {}
                try:o=json.loads(raw.get('result',''))
                except (ValueError,TypeError,AttributeError):continue
                if isinstance(o,dict) and 'current_state' in o:
                    obs=o;ev=o.get('events') or ''
                    tier=R.hr_level(ev) if isinstance(ev,str) else None
                    if tier is not None:latest_hr={'month':o['current_state']['time']['current_month'],'tier':tier}
            elif name=='bash' and p.get('tool_call_id') in byid:
                byid[p['tool_call_id']]['out']=str(p.get('result'))
            elif name.endswith('take_action') and p.get('tool_call_id') in action_rows:
                try:result=json.loads((p.get('raw_output') or {}).get('result',''))
                except (ValueError,TypeError,AttributeError):result={}
                action_rows[p['tool_call_id']]['accepted']=result.get('success') is True
    return rows,calls,plain,sessions

def audit(run,cat):
    d=DATA/run;rp=d/'output/score_report.json';report=json.loads(rp.read_text());events=sorted((d/'output').glob('events-*.jsonl'));assert len(events)==1
    script=Path(report['submission_dir'])/'skills/career-advisor/script/advisor.py'
    spec=importlib.util.spec_from_file_location('saved_advisor',script);adv=importlib.util.module_from_spec(spec);spec.loader.exec_module(adv)
    rows,calls,plain,sessions=records(events[0]);mems={};count=collections.Counter();conf={k:collections.Counter() for k in K+('risk',)};stages=collections.defaultdict(collections.Counter);details=[]
    for r in rows:
        m=re.search(r'CHOOSE\s+(\d+)',r['out'] or '')
        if not m:count['advisor_calls_without_printed_choice']+=1;continue
        try:
            tokens=shlex.split(r['command']);candidates=[t for t in tokens if 'sid=' in t and 'phase=' in t]
        except ValueError:candidates=[]
        if len(candidates)!=1:count['ambiguous_command_encoding']+=1;continue
        st,opts=adv.parse(candidates[0]);out=int(m[1]);count['advisor_printed_choice']+=1
        if r['public_hr'] and r['public_hr']['month']==st['month']:
            count['public_hr_comparable_rows']+=1;count['public_hr_input_mismatch']+=st['hr']!=r['public_hr']['tier'];count['public_hr_input_understated']+=st['hr'] is not None and st['hr']<r['public_hr']['tier']
        mem=mems.setdefault(st['sid'],adv.Memory(st['sid'],None))
        expected,_=adv.step(st,opts,mem);count['reproduced_advisor_choice']+=expected==out
        balance=mem.d.get('hr',0)+mem.d.get('risk_since',0)
        count['negative_raw_risk_balance_after_call']+=balance<0
        if st['phase']=='story' and out in opts:
            chosen_risk=opts[out][1]
            count['selected_claimed_cleanup_while_reported_risk_zero']+=chosen_risk<0 and max(0,min(4,balance-chosen_risk))==0
        if 'choice' in r:
            count['paired_actions']+=1;count['took_printed_choice']+=r['choice']==out;count['paired_accepted_actions']+=bool(r.get('accepted'))
        o=r['obs']
        if not o:count['missing_observation']+=1;continue
        s=o['current_state'];status=s['status'];actual={'month':s['time']['current_month'],'level':int(str(status['level']).removeprefix('L')),**{k:status[k] for k in K},'energy':status['energy']}
        mismatch=[k for k,v in actual.items() if st.get(k)!=v]
        count['state_copy_mismatch_rows']+=bool(mismatch)
        for k in mismatch:count['copy_mismatch_'+k]+=1
        if st['phase']!='story':continue
        ids={int(c['choice']) for c in o.get('choices') or []};count['story_option_coverage_mismatch']+=set(opts)!=ids
        nid=node(o)
        if nid not in cat.nodes:count['unmatched_story_nodes']+=1;continue
        count['matched_story_calls']+=1;stage='L1' if actual['level']==1 else 'higher';selected=r.get('choice',out);summary={'node':nid,'month':actual['month'],'level':actual['level'],'selected':selected,'state_copy_mismatch_fields':mismatch}
        for k,(fx,risk) in opts.items():
            ch=cat.nodes[nid]['choices'].get(str(k))
            if not ch:count['unmatched_option_ids']+=1;continue
            dr=cat.answer_risk(nid,k);sgn=(dr>0)-(dr<0)
            count['matched_options']+=1;count['options_with_double_visible_magnitude']+=any(abs(v)>1 for v in fx.values())
            for stat in K:
                true=ch['d'].get(stat,0);true=(true>0)-(true<0);guess=fx.get(stat,0);guess=(guess>0)-(guess<0);conf[stat][(true,guess)]+=1
            conf['risk'][(sgn,risk)]+=1
            if k==selected and r.get('accepted'):
                row=stages[stage];row['n']+=1;row['true_positive_risk']+=dr>0;row['positive_risk_missed']+=dr>0 and risk<=0;row['negative_risk_claim_on_true_positive']+=dr>0 and risk<0
                losses=[s for s in R.GROWTH if ch['d'].get(s,0)<0];miss=[s for s in losses if fx.get(s,0)>=0]
                row['growth_loss_choices']+=bool(losses);row['growth_loss_missed']+=bool(miss)
                summary.update(true_risk_delta=dr,predicted_risk=risk,true_growth_losses=losses,missed_growth_losses=miss)
        details.append(summary)
    accuracy={}
    for stat,c in conf.items():
        n=sum(c.values());up=sum(v for (t,g),v in c.items() if t>0);down=sum(v for (t,g),v in c.items() if t<0)
        accuracy[stat]={'n':n,'exact_sign_correct':sum(v for (t,g),v in c.items() if t==g),'positive_support':up,'positive_seen':c[(1,1)],'negative_support':down,'negative_seen':c[(-1,-1)]}
    memory_checks=[]
    for sid,mem in mems.items():
        mp=d/'advisor-state'/f'{sid}.json';saved=json.loads(mp.read_text()) if mp.exists() else None
        memory_checks.append({'sid_sha256':hashlib.sha256(sid.encode()).hexdigest(),'saved_exists':mp.exists(),'exact_dict_equal':saved==mem.d,'differing_top_keys':sorted(k for k in set(saved or {})|set(mem.d) if (saved or {}).get(k)!=mem.d.get(k))})
    ending=report.get('ending_score') or {}
    return {'run':run,'Q':ending.get('quantitative_score'),'completed':ending.get('completed'),'termination_reason':report.get('termination_reason'),'ending_dimensions':ending.get('dimensions'),'report_sha256':sha(rp),'events_sha256':sha(events[0]),'script_sha256':sha(script),'distinct_action_session_ids':len(sessions),'replayed_memory_ids':len(mems),'final_memory_checks':memory_checks,
            'tool_calls':dict(calls),'unpaired_or_single_choice_actions':plain,'counts':dict(count),'stages':{k:dict(v) for k,v in stages.items()},'accuracy':accuracy,'rows':details}

def main():
    cp=ROOT/'lab/data/ingenieria-inversa/catalog_v2.json';cat=R.Catalog(json.loads(cp.read_text()));runs=[audit(x,cat) for x in ('sv1-g1','sv1-g2','sv3-g1','sv3-g2','sv3-g3')]
    import gzip
    raw=json.dumps(runs,indent=1).encode();archive=REPORT/'format-trace-rows.json.gz';archive.write_bytes(gzip.compress(raw,mtime=0))
    out={'meaning':'Existing official DeepSeek careers, observational and selected posthoc. Fresh current menu paired by tool-call IDs, exact node hash, not title alone. Script replay uses actual submitted source and parsed observations only. Accuracy normalizes visible magnitudes only for reporting, never for replay. No new model/API calls; no attribution to external teams.',
         'script_sha256':sha(Path(__file__)),'catalog_sha256':sha(cp),'archive_sha256':sha(archive),'uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'runs':[{k:v for k,v in r.items() if k not in ('rows','accuracy','ending_dimensions')} for r in runs]}
    (REPORT/'format-trace-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{'run':r['run'],'Q':r['Q'],'sessions':r['distinct_action_session_ids'],'counts':r['counts'],'stages':r['stages']} for r in runs],indent=2))
if __name__=='__main__':main()
