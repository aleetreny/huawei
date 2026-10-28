"""Within-menu information collisions in saved factual representations, no model calls."""
import json,hashlib,copy,collections
from pathlib import Path
from gpt_fact_career_score import DATA,FIRST,REPORT,ROOT,R,realised
FIELDS=('time_diversion','relationship_rupture','unresolved_issue','personal_payment')
def main():
 items=json.loads((FIRST/'items.json').read_text());cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));collisions=[];menus=set()
 for it in items:
  reply=json.loads((DATA/it['id']/'result.json').read_text());assert reply['done'];s=copy.deepcopy(it['observe']['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=it['observe']['current_state']['time']['current_month'];groups=collections.defaultdict(list)
  for row in reply['response']['options']:
   k=row['choice'];fx=realised({'state':s},cat.nodes[it['node']]['choices'][str(k)]['d']);risk=cat.answer_risk(it['node'],k)
   groups[tuple(row[f]['answer'] for f in FIELDS)].append({'choice':k,'positive_risk':risk>0,'growth_loss':any(fx[g]<0 for g in R.GROWTH)})
  for flags,rows in groups.items():
   if len(rows)>1 and len({(r['positive_risk'],r['growth_loss']) for r in rows})>1:
    menus.add(it['id']);collisions.append({'id':it['id'],'flags':dict(zip(FIELDS,flags)),'options':rows})
 out={'meaning':'Posthoc within-menu collisions: same public state and identical saved four-predicate answers, different gold risk/growth-loss outcomes. Shows these particular observed predicate vectors alone are insufficient; not a bound on richer text/state policies, perfect factual annotation, career Q or DeepSeek. No answer map delivered as Skill.', 'n_menus':len(items),'menus_with_collisions':len(menus),'colliding_groups':len(collisions),'rows':collisions,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(REPORT/'fact-sufficiency.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
