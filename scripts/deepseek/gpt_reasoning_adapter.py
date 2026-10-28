"""Pure request-kwargs tests of public Jiuwen helpers. No client initialization/network."""
import importlib.util,sys,types,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'local-runs/official-runner/.venv/lib/python3.14/site-packages/jiuwenswarm/common'
def main():
 for name in ('jiuwenswarm','jiuwenswarm.common'):
  package=types.ModuleType(name);package.__path__=[];sys.modules[name]=package
 modules={};hashes={}
 for short in ('reasoning_config','reasoning_injector'):
  path=BASE/(short+'.py');name='jiuwenswarm.common.'+short;spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);modules[short]=m;hashes[short]=hashlib.sha256(path.read_bytes()).hexdigest()
 fn=modules['reasoning_injector'].build_reasoning_model_request_kwargs;rows=[]
 for base,model in [('https://openrouter.ai/api/v1','deepseek/deepseek-v4-flash'),('https://openrouter.ai/api/v1','deepseek-v4-flash'),('https://api.deepseek.com','deepseek-v4-flash')]:
  for level in (None,'off','high'):
   cfg={'temperature':.95}
   if level is not None:cfg['reasoning_level']=level
   out=fn(model_client_config={'client_provider':'openai','api_base':base,'model_name':model},model_config_obj=cfg,model_name=model)
   if 'openrouter' in base:assert 'reasoning_effort' not in out and 'extra_body' not in out
   if 'api.deepseek.com' in base and level=='high':assert out['reasoning_effort']=='high' and out['extra_body']['thinking']['type']=='enabled'
   rows.append({'base':base,'model':model,'requested_internal_level':level,'kwargs':out})
 result={'meaning':'Current installed public helper only. OpenRouter hostname is unrecognized by this injector even with unprefixed model. Does not prove the full live request, provider default, or historical model reasoning mode. Official-host positive control verifies injection. No API/client/env accessed.','source_sha256':hashes,'rows':rows}
 p=ROOT/'lab/reports/deepseek/gpt-principios/reasoning-adapter.json';p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'cases':len(rows),'openrouter_cases_without_injection':6,'official_positive_control':True}))
if __name__=='__main__':main()
