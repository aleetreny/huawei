"""Read-only audit of paid mv traces and empirical catalog; no API or simulator calls.
Run from any cwd: python3 scripts/deepseek/gpt_mv_evidence.py > report.json
Outputs aggregates only (no event wording). Catalog outcomes are research evidence,
not observable information for a submitted Skill or full-career counterfactuals.
"""
import collections, csv, gzip, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DS = ROOT / "lab/data/deepseek"
cat = json.loads((ROOT / "lab/data/ingenieria-inversa/catalog_v2.json").read_text())
answers = json.load(gzip.open(DS / "otros/answers.json.gz", "rt"))
texts = {(a["node"], str(a["choice"])): a["text"] for a in answers}
bytitle = collections.defaultdict(list)
for nid, node in cat["nodes"].items():
    bytitle[node["title"]].append(nid)
def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()
def hr(s):
    for word, value in [("angry",4),("uneasy",3),("frowning",2),("quietly",1),("smiling",0)]:
        if word in s: return value
    return None
stats = collections.defaultdict(collections.Counter)
pergame = collections.defaultdict(collections.Counter)
casegames = collections.defaultdict(set)
coverage = collections.Counter()
for row in csv.DictReader(gzip.open(DS / "decisiones.csv.gz", "rt")):
    if row["manual"] not in ("mv-3", "mv-4") or row["tipo"] != "historia" or int(row["n_opciones"] or 0)<2:
        continue
    coverage["stories"] += 1
    key = row["eleccion"]
    if not key or not row["texto_eleccion"]:
        coverage["invalid_or_missing_choice"] += 1
        continue
    candidates = [nid for nid in bytitle[row["situacion"]] if len(cat["nodes"][nid]["choices"])==int(row["n_opciones"]) and norm(texts.get((nid,key),""))==norm(row["texto_eleccion"])]
    if len(candidates)!=1:
        coverage["unmatched_or_ambiguous"] += 1
        continue
    nid=candidates[0]; node=cat["nodes"][nid]
    # replica.build serializes only nonzero risks; missing entries mean zero.
    coverage["matched"] += 1
    opts={k:(ch["d"],cat["risk"].get(f"E|{nid}|{k}",0)) for k,ch in node["choices"].items()}
    d,risk=opts[key]
    health=float(row["health"])
    safe=[d2 for d2,r2 in opts.values() if r2<=0 and health+d2.get("health",0)>0]
    near=int(row["mes"])%6 in (4,5)
    tone=hr(row["comentario_rrhh"])
    lose_no=any(d.get(k,0)<0 for k in ("network","output"))
    minrisk=min(r2 for d2,r2 in opts.values())
    dominated=any(r2<=risk and all(d2.get(k,0)>=d.get(k,0) for k in ("health","dignity","skill","network","output","wealth")) and (r2<risk or any(d2.get(k,0)>d.get(k,0) for k in ("health","dignity","skill","network","output","wealth"))) for d2,r2 in opts.values())
    measures={"all_options_risky":minrisk>0,"all_risky_selected_above_min":minrisk>0 and risk>minrisk,"locally_dominated_raw_effects":dominated,"n":1,"risk_positive":risk>0,"risk_at_least_2":risk>=2,
      "positive_risk_with_nonpositive_alternative":risk>0 and bool(safe),
      "NO_loss":lose_no,
      "NO_loss_with_safe_NO_preserving_alternative":lose_no and any(all(d2.get(k,0)>=0 for k in ("network","output")) for d2 in safe),
      "health_loss_when_health_le3":health<=3 and d.get("health",0)<0}
    groups=["all", row["manual"], row["nivel"], "review_near" if near else "review_far"]
    if tone is not None:groups.append("hr_adverse" if tone>=2 else "hr_mild")
    if near:groups.append("near_"+row["nivel"])
    for group in groups:
        stats[group].update({k:int(v) for k,v in measures.items()})
    pergame[row["partida"]].update({k:int(v) for k,v in measures.items()})
    if tone is not None and tone>=2 and risk>0 and safe:
        casegames[nid].add(row["partida"])
scored=[]
for path in sorted((DS/"partidas").glob("mv-*__*/score_report.json")):
    report=json.loads(path.read_text()); e=report.get("ending_score") or {}
    if e.get("quantitative_score") is None:continue
    n=e["survival_months"];t=report["token_usage"]["total_tokens"]
    eff=max(0,min(100,100*(3000000-t/n)/2500000))
    if n<48:eff=min(eff,50)
    scored.append({"run":path.parent.name,"Q":e["quantitative_score"],"completed":e["completed"],"E":eff,
      "dimensions":{d["name"]:d["weighted_score"] for d in e["dimensions"]}})
mean=lambda xs:sum(xs)/len(xs)
complete=[s for s in scored if s["completed"]]
qbar=mean([s["Q"] for s in scored]); ebar=mean([s["E"] for s in scored])
print(json.dumps({"coverage":dict(coverage),"groups":dict(stats),"pergame":dict(pergame),
 "adverse_risk_cases_distinct_nodes":len(casegames),"adverse_risk_nodes_in_multiple_games":sum(len(v)>1 for v in casegames.values()),
 "scored":scored,"summary":{"n":len(scored),"Q":qbar,"E":ebar,"version_if_D73":.8*qbar+7.3+.1*ebar,
 "completed_Q":mean([s["Q"] for s in complete]),"completed_dimensions":{k:mean([s["dimensions"][k] for s in complete]) for k in complete[0]["dimensions"]},
 "target_Q_if_E100":{str(d):(76-.1*d-10)/.8 for d in [70,73,80,90,100]}}},indent=2))
