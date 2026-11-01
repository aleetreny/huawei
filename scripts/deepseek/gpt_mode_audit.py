"""Independent local mode comparison via five official tools. No models. Default plan only."""
import argparse,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=Path.home()/'careerlab-data/deepseek/gpt-mode-audit';REPORT=ROOT/'lab/reports/deepseek/gpt-principios'
def main(run=False):
 plan={'n_per_mode':60,'modes':['dev','competition'],'policy':'Existing optimal Planner parameters through Explorer with explore_below=0; same in both arms. Unknown nodes retain existing fallback.','scope':'Independent random careers, not paired engine seeds. Pilot for difficulty/sample distribution differences, not power to exclude small shifts, not a Skill candidate or DS proof. Only five official tools, no package/database inspection. No API/model calls.','data':str(DATA)}
 p=REPORT/'mode-audit-plan.json'
 if p.exists():assert json.loads(p.read_text())==plan
 else:p.write_text(json.dumps(plan,indent=2)+'\n')
 if not run:return
 DATA.mkdir(parents=True,exist_ok=True)
 for mode in plan['modes']:
  if (DATA/mode).exists():raise RuntimeError('Existing mode data: inspect process/results before resuming')
  env=dict(os.environ);env['HP_DATA']=str(DATA);env.pop('BB_COMPETITION',None)
  args=[sys.executable,str(ROOT/'scripts/huevos-pascua/run_explore.py'),'--batch',mode,'--games','60','--procs','2','--slots','2','--seed','20261028','--explore-below','0']
  if mode=='competition':args.append('--competition')
  with (DATA/(mode+'-driver.log')).open('w') as out:subprocess.run(args,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT,check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',action='store_true');main(p.parse_args().run)
