import json,sys,glob,collections,os
S=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 30
ds=sorted(glob.glob(S+'/runner/.career_sim_runner/career_emu/outputs/*/*'),key=os.path.getmtime)
f=glob.glob(ds[-1]+'/events-*.jsonl')
ev=[json.loads(l) for l in open(f[0])]
ev=[e for e in ev if 'payload' in e and 'delta' not in e['payload']]
c=collections.Counter(e['payload']['tool_call']['name'].replace('mcp_career-emulator-engine_','') for e in ev if e['kind']=='tool_call')
print(dict(c))
last_obs=None
for e in ev:
    p=e['payload']
    if e['kind']=='tool_result' and str(p.get('tool_name','')).endswith('observe'):
        try: last_obs=json.loads(p['raw_output']['result'])['current_state']
        except Exception: pass
if last_obs: print('LAST', last_obs['time'], last_obs['status'])
for e in ev[-n:]:
    p=e['payload']
    if e['kind']=='tool_call' and p['tool_call']['name'] in ('bash','mcp_career-emulator-engine_take_action','read_file','skill_tool','code'):
        print(p['tool_call']['name'][-12:], p['tool_call']['arguments'][:600])
    if e['kind']=='tool_result' and p.get('tool_name') in ('bash','code'):
        print('   ->', str(p.get('result'))[:300])
