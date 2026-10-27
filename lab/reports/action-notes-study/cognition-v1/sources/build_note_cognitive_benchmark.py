"""Build frozen public-prefix fact probes; gold never enters model prompts."""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import is_terminal

OPEN = [
    ('someone has to ask facilities', 'Has asking facilities for the extras already been reported as completed?', 'no'),
    ('promise to credit you in later docs', 'Has credit in the later documents already been reported as completed?', 'no'),
    ('still an unresolved risk', 'Is the project risk described as resolved at this briefing?', 'no'),
    ('still have not delivered', 'Has the dependent team delivered at this update?', 'no'),
    ('nothing is clearly signed off', 'Is clear sign-off already in place at this update?', 'no'),
    ('still have to decide whether the company should know', 'Has the decision about informing the company already been made?', 'no'),
]
CLOSED = [
    ('The remaining payment comes in', 'Has the remaining payment arrived?', 'yes'),
    ('she goes home', 'Has the ill colleague gone home?', 'yes'),
    ('They drop the slide and go with +12%', 'Has the manager replaced the inflated metric with +12%?', 'yes'),
    ('there is no second incident', 'Does this description report a second incident?', 'no'),
    ('You get Will out before', 'Was Will taken out before making the scene in front of the manager?', 'yes'),
    ('IT cannot recall it', 'Did IT succeed in recalling the email?', 'no'),
]
CATEGORIES = ('delayed_consequence', 'open_commitment', 'explicit_resolution', 'incident_history',
              'observed_payoff', 'latest_review', 'fresh_over_stale', 'unknown')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def observations(steps, cut):
    out = []
    for i, s in enumerate(steps[:cut]):
        out += [{'id': f'S{i:03d}B', 'kind': 'observe', 'data': s['before']},
                {'id': f'S{i:03d}A', 'kind': 'take_action', 'data': {'choice': s['choice'], 'success': s.get('applied', s.get('reply', {}).get('success', True))}},
                {'id': f'S{i:03d}R', 'kind': 'observe', 'data': s['after']}]
    return out


def candidates():
    pools = defaultdict(list)
    seen = set()
    paths = [Path('lab/reports/first-review-search/known-closure-2/public-trajectories.jsonl.gz'),
             Path('lab/reports/first-review-search/frontier/public-trajectories.jsonl.gz'),
             Path('lab/reports/second-review-search/closure/public-trajectories.jsonl.gz'),
             Path('lab/reports/second-review-search/exploration/public-trajectories.jsonl.gz'),
             Path('lab/reports/constrained-growth-study/study-v1/public-trajectories.jsonl.gz')]
    for archive in paths:
        with gzip.open(archive, 'rt') as stream:
            for line_index, line in enumerate(stream):
                r = json.loads(line)
                sid = r['session_id']
                if sid in seen:
                    continue
                seen.add(sid)
                steps = r['steps']
                def add(category, source_step, question, answer, fact, family, source_field='before', **extra):
                    if len(pools[category]) >= 1200 or sum(c['family']==family and (category!='latest_review' or c['answer']==str(answer)) for c in pools[category]) >= 120 or any(c['session_id']==sid and c['family']==family and (category!='latest_review' or c['answer']==str(answer)) for c in pools[category]):
                        return
                    cut = min(len(steps), source_step + 4)
                    if cut <= source_step or not steps[cut-1]['after'].get('choices') or is_terminal(steps[cut-1]['after']):
                        return
                    source_id = f'S{source_step:03d}' + ('B' if source_field == 'before' else 'R' if source_field == 'after' else 'A')
                    pools[category].append({'category': category, 'archive': str(archive), 'line': line_index,
                        'session_id': sid, 'source_step': source_step, 'cut': cut, 'question': question,
                        'answer': str(answer), 'fact': fact, 'family': family, 'support': source_id, **extra})
                prior = {}
                review = None
                for i, s in enumerate(steps):
                    e = s['before'].get('current_event') or {}
                    title, desc = e.get('title', ''), e.get('description', '')
                    if s['phase'] == 'event':
                        if title in prior and desc != prior[title][1]:
                            j, _ = prior[title]
                            if i-j >= 3 and steps[i]['after'].get('choices') and not is_terminal(steps[i]['after']):
                                actual = steps[j]['choice']['action']
                                alternatives = [c['action'] for c in steps[j]['before'].get('choices', []) if c['action'] != actual]
                                queried = actual if (i+line_index)%2 == 0 or not alternatives else alternatives[0]
                                previous_count=len(pools['delayed_consequence'])
                                add('delayed_consequence', j,
                                    f'At the earlier occurrence of {title!r}, did the recorded chosen action equal {queried!r}? Answer yes/no.',
                                    'yes' if queried == actual else 'no', f'At {title!r} the recorded action was {actual!r}.', title, 'action', later_step=i)
                                if len(pools['delayed_consequence'])>previous_count:
                                    pools['delayed_consequence'][-1]['cut'] = min(len(steps), i+1)
                        prior[title] = (i, desc)
                        for category, templates in (('open_commitment', OPEN), ('explicit_resolution', CLOSED)):
                            for fragment, q, answer in templates:
                                if fragment.casefold() in desc.casefold():
                                    add(category, i, f'According to the earlier public description of {title!r}: {q} Answer yes/no.', answer,
                                        f'Public description of {title!r}: {desc}', title, matched_fragment=fragment)
                    before, after = s['before']['current_state']['status'], s['after']['current_state']['status']
                    nominal = s['choice'].get('status_updates') or {}
                    if s['phase'] in ('energy', 'main_action'):
                        for stat in ('Output', 'Skill', 'Network'):
                            delta = after[stat.lower()] - before[stat.lower()]
                            if nominal.get(stat, 0) > 0 and delta != nominal[stat]:
                                action = s['choice']['action']
                                add('observed_payoff', i,
                                    f'What was the visible {stat} change across the earlier step {i} action {action!r}? Return the numeric delta as a string; unknown if unsupported.',
                                    delta, f'Step {i}: {action}; visible {stat} {before[stat.lower()]} -> {after[stat.lower()]}, observed delta {delta}; advertised {nominal[stat]}.',
                                    'payoff:'+action, 'after', related_support=f'S{i:03d}B')
                    grades = re.findall(r'performance bonus \(([A-Z])\)', s['after'].get('events', ''))
                    if grades:
                        grade = grades[-1]
                        add('latest_review', i,
                            'What is the grade in the latest public half-year performance bonus message before the current observation? Return the single letter, or unknown.',
                            grade, f'Latest half-year performance bonus grade at step {i}: {grade}.', 'latest_review', 'after', previous_grade=review)
                        review = grade
                    # A truly old checkpoint value contradicted by fresh observe, not a fabricated false note.
                    if i >= 4 and before['health'] != steps[i-4]['before']['current_state']['status']['health']:
                        cut = i
                        current = steps[cut-1]['after']
                        if current.get('choices') and not is_terminal(current):
                            old = steps[i-4]['before']['current_state']['status']['health']
                            previous_count=len(pools['fresh_over_stale'])
                            add('fresh_over_stale', i-1,
                                'What is Health in the current observation? Return the numeric value as a string; prefer fresh evidence over older notes.',
                                current['current_state']['status']['health'], f'Current Health: {current["current_state"]["status"]["health"]}.',
                                'current_health', 'after', old_health=old, old_health_source=f'S{i-4:03d}B')
                            if len(pools['fresh_over_stale'])>previous_count:
                                pools['fresh_over_stale'][-1]['cut'] = cut
                # History questions on a calm current response; grade/risk statements stay in past records.
                for cut in reversed(range(8, len(steps)+1)):
                    current = steps[cut-1]['after']
                    if not current.get('choices') or is_terminal(current) or 'Old landmines' in current.get('events', ''):
                        continue
                    incidents = [j for j, s in enumerate(steps[:cut]) if 'Old landmines' in s['after'].get('events', '')]
                    category = 'incident_history'
                    if len(pools[category]) < 240 and sum(c['answer']==('yes' if incidents else 'no') for c in pools[category]) < 120:
                        pools[category].append({'category':category,'archive':str(archive),'line':line_index,'session_id':sid,
                            'source_step':incidents[-1] if incidents else 0,'cut':cut,
                            'question':'Has an official public "Old landmines" message appeared anywhere earlier in this recorded career prefix? Answer yes/no; a calm current message is not historical evidence.',
                            'answer':'yes' if incidents else 'no','fact':f'Public Old landmines messages in the prefix: {len(incidents)}.',
                            'family':'incident_history','support':f'S{incidents[-1]:03d}R' if incidents else 'PREFIX_ABSENCE', 'incident_count':len(incidents)})
                    break
                if len(steps)>=8:
                    for idx, q in enumerate(('What is the exact hidden numeric first-promotion threshold?',
                        'What is the exact current hidden risk value?', 'What is the exact hidden probability of the next trust incident?',
                        'What is the exact hidden coefficient of Network in the performance formula?',
                        'What is the exact hidden coefficient of Skill in the performance formula?',
                        'What is the exact hidden coefficient of Output in the performance formula?')):
                        add('unknown', 3, q+' Return unknown if the public prefix does not disclose it.', 'unknown',
                            'No exact numeric value for this hidden parameter is disclosed by the public prefix.', 'unknown:'+str(idx), unknown_kind=idx)
    return pools


def build(out):
    out.mkdir(parents=True, exist_ok=False)
    pools = candidates()
    print('candidate counts', {k:len(v) for k,v in pools.items()}, flush=True)
    picked, used, family_counts = [], set(), Counter()
    # Reserve rare, explicit semantic witnesses before the abundant numeric/history cases.
    for category in ('open_commitment','explicit_resolution','delayed_consequence','observed_payoff','latest_review','incident_history','fresh_over_stale','unknown'):
        chosen = []
        ranked = sorted(pools[category], key=lambda c:(family_counts[c['family']], c['line'], c['source_step']))
        for c in ranked:
            if c['session_id'] in used:
                continue
            if category in ('open_commitment','explicit_resolution','delayed_consequence','unknown') and any(x['family']==c['family'] for x in chosen):
                continue
            if category=='observed_payoff' and sum(x['family']==c['family'] for x in chosen)>=3:
                continue
            if category=='latest_review' and sum(x['answer']==c['answer'] for x in chosen)>=3:
                continue
            if category=='incident_history' and sum(x['answer']==c['answer'] for x in chosen)>=3:
                continue
            chosen.append(c);used.add(c['session_id']);family_counts[c['family']]+=1
            if len(chosen)==6:
                break
        if len(chosen)!=6:
            raise ValueError(f'Insufficient independent witnesses for {category}: {len(chosen)}; do not fabricate cases')
        picked.extend(chosen)
    # Retrieve selected records only, from public archives. No ending or later steps enter cases.
    wanted = {(c['archive'],c['line']) for c in picked}
    records = {}
    for archive in sorted({a for a,_ in wanted}):
        with gzip.open(archive,'rt') as stream:
            for i,line in enumerate(stream):
                if (archive,i) in wanted:
                    records[(archive,i)] = json.loads(line)
    groups = defaultdict(list)
    for c in picked:
        groups[c['family']].append(c)
    split_rng=random.Random(271027)
    best=None
    for _ in range(4000):
        families=list(groups);split_rng.shuffle(families);selected=[];total=0;counts=Counter()
        for family in families:
            if total+len(groups[family])<=24:
                selected.append(family);total+=len(groups[family]);counts.update(c['category'] for c in groups[family])
        if total==24:
            score=sum(abs(counts[k]-3) for k in CATEGORIES)
            if best is None or score<best[0]:best=(score,selected)
    assert best is not None, 'Cannot create group-disjoint 24/24 split'
    development=set(best[1])
    cases = []
    for n,c in enumerate(picked):
        r = records[(c['archive'],c['line'])];steps=r['steps'];cut=c['cut'];current=steps[cut-1]['after']
        assert current.get('choices') and not is_terminal(current)
        history=observations(steps,cut)
        checkpoint={'id':'CHECKPOINT','saved_after_step':cut-1,'text':c['fact'],'sources':[c['support']]}
        if c['category']=='fresh_over_stale':
            oldtext=f'Health at the older observation: {c["old_health"]}.'
        elif c['category']=='latest_review' and c.get('previous_grade'):
            oldtext=f'Previously observed performance bonus grade: {c["previous_grade"]}.'
        else:
            oldtext='This older checkpoint contains no later outcome for the subject. Recheck public logs for updates.'
        stale={'id':'OLD_CHECKPOINT','saved_before_source_step':c['source_step'],'text':oldtext,'historical_not_current':True}
        if c['category']=='fresh_over_stale':
            checkpoint['text']=f'Health at the latest observation: {current["current_state"]["status"]["health"]}.'
        case={**c,'id':f'NC{n:02d}','split':'development' if c['family'] in development else 'confirmation',
              'current':{'id':'CURRENT','kind':'observe','data':current},'history':history,'checkpoint':checkpoint,'stale_checkpoint':stale,
              'source_archive_sha256':sha(Path(c['archive'])),'source_record_sha256':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest(),
              'note_age_actions':cut-1-c['source_step']}
        if len(json.dumps(checkpoint,ensure_ascii=False))>1000:
            # Keep the supporting description as a bounded verbatim excerpt around the matched phrase.
            fragment=c.get('matched_fragment','');text=c['fact'];at=text.casefold().find(fragment.casefold())
            checkpoint['text']=text[max(0,at-100):at+len(fragment)+180]
        assert len(json.dumps(checkpoint,ensure_ascii=False))<=1000
        cases.append(case)
    assert len({c['session_id'] for c in cases})==48
    (out/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    schedule=[{'case_id':c['id'],'condition':condition,'replicate':rep} for c in cases for condition in ('current_only','full_history','curated_checkpoint','stale_recovery') for rep in range(3)]
    random.Random(271026).shuffle(schedule)
    (out/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
    shutil.copyfile('lab/reports/memory-pilot/luna-v1/frozen-bundle/skills/balanced-feedback/SKILL.md',out/'frozen-skill.md')
    (out/'protocol.json').write_text(json.dumps({'name':'note-cognition-v1','model':'gpt-6-luna','route':'Codex CLI ChatGPT login; isolated ephemeral process per request',
        'cases':48,'conditions':4,'replicates':3,'primary_decisions':576,'max_model_requests':720,'max_total_input_tokens':24000000,'max_total_output_tokens':250000,
        'concurrency':4,'reasoning_effort':'low','max_seconds_per_request':180,'case_sha256':sha(out/'cases.json'),'schedule_sha256':sha(out/'schedule.json'),
        'skill_sha256':sha(out/'frozen-skill.md'),'builder_sha256':sha(Path(__file__)),
        'recovery':'stale condition may request one deterministic delivery of the prefix logs, then one final fresh-process response with the preceding prompt/answer plus supplied logs; simulated retrieval, not native MCP',
        'stop':'Fixed schedule or quota/route failure/token ceiling; never silently replace model errors; no outcome-based stopping or policy changes',
        'split':'24/24 by target fact family; one distinct source career per case; all cases fixed before any benchmark answer',
        'scoring':'Known-fact recovery with exact answer and valid public support; calibrated abstention separately. Choice legality only, no claimed optimal choices.',
        'limits':['Curated checkpoints test information availability, not quality of autonomous note writing','Historical pending/resolved statements do not establish present status at every later step',
                  'Offline prefix decisions are not counterfactual promotion outcomes','No natural compaction forced or Jiuwen timing measured','No provider cache TTL inferred from cache-hit counters',
                  'Incomplete stale checkpoints differ from explicitly obsolete health/review values; analyze separately','Confirmation category mix can differ due to family-disjoint split']},indent=2)+'\n')
    print(json.dumps({'cases':48,'splits':dict(Counter(c['split'] for c in cases)),'categories':dict(Counter(c['category'] for c in cases))}))


if __name__=='__main__':build(Path(sys.argv[1]))
