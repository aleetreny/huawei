"""Read-only audit of own official-MCP run artifacts, never engine internals or API.
Exports counts and visible numeric state only; narrative text stays outside Git.
"""
from __future__ import annotations
import argparse,ast,collections,hashlib,json,re
from pathlib import Path

def objects(value,depth=0):
    if depth>10:return
    if isinstance(value,str):
        if len(value)>1_000_000:return
        try:value=json.loads(value)
        except (ValueError,TypeError):
            try:value=ast.literal_eval(value)
            except (ValueError,SyntaxError):return
    if isinstance(value,dict):
        yield value
        for v in value.values():yield from objects(v,depth+1)
    elif isinstance(value,list):
        for v in value:yield from objects(v,depth+1)

def audit(run):
    path=run/'events.jsonl';calls=collections.Counter();success=fail=0;states=[];frames=[];seen=set();actions=0
    for line in path.open():
        record=json.loads(line);pl=record.get('payload',{});call=pl.get('tool_call')
        if isinstance(call,dict):
            cid=call.get('tool_call_id')
            if not cid or cid not in seen:
                if cid:seen.add(cid)
                calls[call.get('name','?')]+=1
                if 'take_action' in call.get('name',''):actions+=1
        if record.get('kind')=='frame_final':frames.append(actions)
        if record.get('kind')!='tool_result' or 'result' not in pl:continue
        nodes=list(objects(pl.get('raw_output') or pl['result']))
        if 'observe' in pl.get('tool_name',''):
            for node in nodes:
                st=node.get('current_state')
                if isinstance(st,dict):
                    states.append({'time':st.get('time'),'status':st.get('status'),'flags':st.get('simulation_flags')});break
        if 'take_action' in pl.get('tool_name',''):
            for node in nodes:
                if 'success' in node:
                    success+=int(node['success'] is True);fail+=int(node['success'] is False);break
    transcript=run/'transcript.log';txt=transcript.read_text(errors='replace') if transcript.exists() else ''
    monthly={}
    for st in states:
        month=st['time']['current_month'];monthly.setdefault(month,{'first':st});monthly[month]['last']=st
    return {'run_dir':str(run),'events_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'transcript_sha256':hashlib.sha256(transcript.read_bytes()).hexdigest() if transcript.exists() else None,
      'tool_calls':dict(calls),'successful_actions':success,'rejected_actions':fail,'observations':len(states),
      'frame_final_action_counts':frames,'last_observation':states[-1] if states else None,
      'visible_canned_refusal_count':txt.count('我还没学习如何回答这个问题'),
      'visible_chinese_character_count':len(re.findall('[\u4e00-\u9fff]',txt)),
      'monthly_observation_bounds':monthly,
      'limits':'First/last snapshots are before actions, not exact review gates. No causal attribution of final action from mixed settlement. No score imputed to interruption.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=audit(args.run_dir)
    base=Path.home()/'careerlab-data/huawei-deepseek/target-slots';languages={}
    for p in base.glob('slot*/home/.jiuwenswarm-instances/career_emu/config/config.yaml'):
        for line in p.open():
            if re.match(r'^preferred_language\s*:',line):languages[p.parents[4].name]=line.split(':',1)[1].strip()
    out['current_slot_language_preferences']=languages
    out['language_caveat']='Current configs are not frozen historical fingerprints. Chinese output and refusals are observed; language causation is untested.'
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('monthly_observation_bounds','frame_final_action_counts')},indent=2))
if __name__=='__main__':main()
