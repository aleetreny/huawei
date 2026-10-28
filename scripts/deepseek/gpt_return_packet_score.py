"""Matched public-memory packet scoring; no model calls or game-Q extrapolation."""
import json,hashlib,copy,collections,re
from gpt_return_packet_probe import DATA,INPUT,REPORT,SOURCE,prefix
from gpt_fact_second_read import ROOT
from gpt_decision_score import R,realised

def main():
 plan=json.loads((REPORT/'return-packet-probe-plan.json').read_text());p=INPUT/'items.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==plan['input_sha256'];items=json.loads(p.read_text());source={x['id']:x for x in json.loads((SOURCE.parent.with_name('gpt-fresh-context')/'items.json').read_text())};cat=R.Catalog(json.loads((ROOT/'lab/data/ingenieria-inversa/catalog_v2.json').read_text()));rows=[];missing=[];models=collections.Counter();keys=('positive_risk','growth_loss','avoidable_loss','health_zero','depleted_wealth_cost')
 for it in items:
  o=it['observe'];s=copy.deepcopy(o['current_state']['status']);s['level']=int(str(s['level']).removeprefix('L'));s['month']=o['current_state']['time']['current_month'];node=source[it['id']]['node'];opts=cat.nodes[node]['choices'];fx={int(k):realised({'state':s},v['d']) for k,v in opts.items()};risk={int(k):cat.answer_risk(node,int(k)) for k in opts};safe=[k for k in fx if risk[k]<=0 and all(fx[k][g]>=0 for g in R.GROWTH) and s['health']+fx[k]['health']>0]
  for arm in plan['arms']:
   p=DATA/f'sonnet-{it["id"]}-{arm}'/'result.json'
   if not p.exists():missing.append((it['id'],arm));continue
   r=json.loads(p.read_text());assert r['done'] and not r['errors'] and not r['invalid'] and r['skill_reads']>=1;assert r['model_ids']==['claude-sonnet-5-5'];models.update(r['model_ids']);assert json.loads((p.parent/'item.json').read_text())['steps']==[o];assert (p.parent/'user_prompt.txt').read_text().startswith(prefix(it,arm));assert hashlib.sha256((p.parent/'system_prompt.md').read_bytes()).hexdigest()==plan['source_system_sha256'];k=r['choice'];loss=any(fx[k][g]<0 for g in R.GROWTH)
   events=[json.loads(line) for line in (p.parent/'record.jsonl').read_text().splitlines()];note=next(e.get('notes','') for e in events if e.get('target') and e.get('tool')=='take_action');field=re.search(r'\bStalled\s*:\s*([^|\n]*)',note,re.I);mapping={'skill':'S|Skill','network':'N|Network','output':'O|Output'};mentioned=bool(field and any(re.search(r'\b(?:'+mapping[g]+r')\b',field[1],re.I) for g in it['packet']['observed_diminished_returns']))
   rows.append({'id':it['id'],'arm':arm,'choice':k,'packet_nonempty':bool(it['packet']['observed_diminished_returns']),'note_mentions_packet_stat':mentioned,'positive_risk':risk[k]>0,'growth_loss':loss,'avoidable_loss':bool(loss and safe),'health_zero':s['health']+fx[k]['health']<=0,'depleted_wealth_cost':s['wealth']<=0 and fx[k]['wealth']<0})
 if missing:print({'pending':len(missing),'available_reads':len(rows)});return
 arms={a:{'n':sum(r['arm']==a for r in rows),**{k:sum(r[k] for r in rows if r['arm']==a) for k in keys}} for a in plan['arms']};pairs={it['id']:{} for it in items}
 for r in rows:pairs[r['id']][r['arm']]=r
 out={'meaning':'Same24public historical panels, matched fresh Sonnet-v4 reads, packet versus no packet with same common interpretation line and prior notes. No whole-career Q/DS transfer or Jiuwen script execution claim. Gold evaluator only.','models':dict(models),'arms':arms,'note_proxy':{a:sum(r['note_mentions_packet_stat'] for r in rows if r['arm']==a) for a in plan['arms']},'note_proxy_limit':'Mentions of a packet stat inside Stalled only, not proof of correct values or use in choice.','same_choice':sum(p['control']['choice']==p['measured_returns']['choice'] for p in pairs.values()),'risk_admission_block':arms['measured_returns']['positive_risk']>arms['control']['positive_risk'],'rows':rows,'script_sha256':hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest()};(REPORT/'return-packet-probe-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
