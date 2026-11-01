"""Single native-model pilot transport; only the five public game tools are exposed."""
import argparse
import asyncio
from dataclasses import asdict
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.config import Settings
from careerlab.episode import atomic_write_json,result_from_terminal
from careerlab.mcp_client import GameClient,ServerSpec,HttpServer,free_port,is_terminal
from careerlab.store import bundle_hash


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()


def prepare(root):
    root.mkdir(parents=True,exist_ok=False)
    source=Path('lab/policies-src/matteo-memory/champion-memory-v1/bundle')
    shutil.copytree(source,root/'bundle')
    settings=Settings(origin='matteoluna',data_dir=root,lab_dir=root/'lab')
    spec=ServerSpec('luna-memory-one',root/'server',transport='http',port=free_port(),competition_mode=True)
    p={'name':'luna-champion-memory-single-pilot-v1','created_at':now(),'actor':'native-subagent','model':'gpt-6-luna',
        'authorization':'Matteo explicitly chose GPT-6 Luna + Ale champion with memory; exactly one exploratory career',
        'parent':'targeted-1026-201334','parent_source_commit':'26e976f9acbe44761f77457d9314e69ea31c4934',
        'bundle_sha256':bundle_hash(root/'bundle'),'source_bundle_sha256':bundle_hash(source),
        'port':spec.port,'environment':spec.fingerprint(settings),
        'dependencies':{str(p.resolve()):sha(p) for p in (Path(__file__),Path('careerlab/mcp_client.py'),Path('careerlab/config.py'))},
        'harness':'Native Codex Luna, fresh-context child. Parent supplies frozen identity/skill only, no empirical lookup or advice. CLI bridge makes public MCP calls via local HTTP; take_action also observes and returns next observation.',
        'stop':'One new_game only, play until explicit ending; never replace a loss, no adaptive edits, no other run or resumption of Haiku4+4',
        'outcomes':['Ending score and survival','Observed promotions and review outcomes','Memory records in notes and factual accuracy','Tool/action counts and note length; model tokens only if actually exposed'],
        'limits':['One unseeded game, no same-actor control, no superiority or memory-causality claim','Different actor and harness from Haiku/DeepSeek','Native model token accounting may be unavailable; do not infer from note lengths']}
    atomic_write_json(root/'protocol.json',p);(root/'protocol-sha256.txt').write_text(sha(root/'protocol.json')+'\n')
    atomic_write_json(root/'status.json',{'status':'prepared','actions':0,'new_game_attempts':0})
    print(json.dumps({'prepared':True,'root':str(root),'bundle_sha256':p['bundle_sha256']}))


def load(root):
    p=json.loads((root/'protocol.json').read_text())
    assert sha(root/'protocol.json')==(root/'protocol-sha256.txt').read_text().strip(),'Protocol changed'
    assert bundle_hash(root/'bundle')==p['bundle_sha256'],'Bundle changed'
    for file,digest in p['dependencies'].items():assert sha(Path(file))==digest,'Transport changed'
    return p


def connection(root,p):
    return ServerSpec('luna-memory-one',root/'server',transport='http',port=p['port'],competition_mode=True),Settings(origin='matteoluna',data_dir=root,lab_dir=root/'lab')


async def call(root):
    p=load(root);request=json.load(sys.stdin);tool=request['tool'];status=json.loads((root/'status.json').read_text())
    if status.get('status') in ('completed','eliminated'):raise ValueError('Game is already over')
    allowed={'new_game','observe','take_action','check_latest_logs','show_employee_handbook'}
    if tool not in allowed:raise ValueError('Not a public game tool')
    spec,settings=connection(root,p);sid=status.get('session_id');args={}
    if tool=='new_game':
        if status['new_game_attempts']:raise ValueError('Exactly one new_game attempt is authorised')
        status['new_game_attempts']=1;status['status']='starting';atomic_write_json(root/'status.json',status)
    elif tool!='show_employee_handbook':
        if not sid:raise ValueError('No session created')
        args['session_id']=sid
    if tool=='take_action':args.update(choice=int(request['choice']),notes=str(request['notes']))
    if tool=='check_latest_logs':args['count']=int(request.get('count',8))
    entry={'timestamp':now(),'tool':tool,'args':args}
    with (root/'requests.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
    async with GameClient(spec,settings) as client:
        try:
            response=await client.call(tool,args);entry['response']=response
            if tool=='new_game':
                sid=response['session_id'];status['session_id']=sid;status['status']='playing'
                entry['observation']=await client.observe(sid)
            elif tool=='take_action':
                status['actions']+=1;status['rejected']=status.get('rejected',0)+int(not response.get('success'))
                entry['observation']=await client.observe(sid)
            elif tool=='observe':entry['observation']=response
            obs=entry.get('observation')
            if obs:
                status['last_state']=obs.get('current_state');status['last_observation']=obs
                if is_terminal(obs):
                    result=result_from_terminal('luna-memory-one',sid,obs);result.steps=status['actions'];result.rejected_actions=status.get('rejected',0)
                    atomic_write_json(root/'result.json',asdict(result));status['status']=result.outcome
                    entry['final_public_logs']=await client.logs(sid,1000)
        except Exception as exc:
            entry['error']=repr(exc)
            with (root/'trajectory.jsonl').open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
            atomic_write_json(root/'status.json',status);raise
    with (root/'trajectory.jsonl').open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
    status['updated_at']=now();atomic_write_json(root/'status.json',status)
    # Archive full terminal logs, but do not flood the model with them.
    shown={k:v for k,v in entry.items() if k not in ('timestamp','final_public_logs')}
    print(json.dumps(shown,ensure_ascii=False))


def serve(root):
    p=load(root);spec,settings=connection(root,p)
    with HttpServer(spec,settings) as server:
        atomic_write_json(root/'server-process.json',{'pid':server.proc.pid,'port':spec.port,'started_at':now()})
        print(json.dumps({'ready':True,'port':spec.port}),flush=True)
        server.proc.wait()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','serve','call']);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='prepare':prepare(args.root)
    elif args.command=='serve':serve(args.root)
    else:asyncio.run(call(args.root))
