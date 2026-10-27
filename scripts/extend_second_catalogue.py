"""Reconstruct extended coverage, keeping frozen mechanism outcomes separate."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import month_index, phase, is_terminal
from scripts.first_review_search import node_key


def extend(old_root,study_root,closure_source,additional_roots=()):
    dest=study_root/"catalogue-closure"
    dest.mkdir(parents=True,exist_ok=True)
    archive=dest/"public-trajectories.jsonl.gz"
    closure=[json.loads(p.read_text()) for p in sorted(closure_source.glob("run-*.json"))]
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as stream:
            for r in closure:
                stream.write((json.dumps(r,ensure_ascii=False)+"\n").encode())
    (dest/"archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+"\n")
    for name in ("manifest.json","manual.md","runner-source.py","coverage-status.json","initial-effects.json","handbook.json"):
        if (closure_source/name).exists():
            shutil.copyfile(closure_source/name,dest/name)
    old=json.loads((old_root/"questions.json").read_text())
    old_keys={q["id"] for q in old}
    questions={}
    provenance=[]
    count=0
    for root in (old_root,*additional_roots,study_root):
        for a in sorted(root.glob("*/public-trajectories.jsonl.gz")):
            expected=(a.parent/"archive-sha256.txt").read_text().split()[0]
            actual=hashlib.sha256(a.read_bytes()).hexdigest()
            if actual!=expected:
                raise ValueError("Source archive integrity mismatch")
            provenance.append({"path":str(a),"sha256":actual})
            with gzip.open(a,"rt") as stream:
                for line in stream:
                    r=json.loads(line);count+=1
                    for s in r["steps"]:
                        for obs in (s["before"],s["after"]):
                            if not 7<=month_index(obs)<=12 or not obs.get("choices") or is_terminal(obs):
                                continue
                            key=node_key(obs)
                            questions.setdefault(key,{"id":key,"phase":phase(obs),"event":obs.get("current_event"),"choices":obs["choices"],"answers":{}})
                    for index,s in enumerate(r["steps"]):
                        obs=s["before"]
                        if not 7<=month_index(obs)<=12 or not s.get("applied") or s.get("ambiguous") or s.get("reply",{}).get("success") is not True:
                            continue
                        key=node_key(obs)
                        questions[key]["answers"].setdefault(str(s["choice"]["choice"]),{
                            "archive":str(a),"run":r["run"],"step":index,"month":month_index(obs),"action":s["choice"]["action"]})
    for q in questions.values():
        q["untried_choices"]=[c["choice"] for c in q["choices"] if str(c["choice"]) not in q["answers"]]
    stories=[q for q in questions.values() if q["phase"]=="event"]
    result={"scope":"Every question offered in nonterminal public observations during months 7–12, including newly exposed continuations; not every hidden-state history",
        "source_records":count,"sources":provenance,"questions":len(questions),"story_questions":len(stories),
        "titles":len({q["event"]["title"] for q in stories}),"available_answers":sum(len(q["choices"]) for q in questions.values()),
        "witnessed_answers":sum(len(q["answers"]) for q in questions.values()),
        "story_available_answers":sum(len(q["choices"]) for q in stories),"story_witnessed_answers":sum(len(q["answers"]) for q in stories),
        "new_nodes":[q["id"] for q in questions.values() if q["id"] not in old_keys],
        "missing":[{"question":q["id"],"choices":q["untried_choices"]} for q in questions.values() if q["untried_choices"]],
        "closure_games":len(closure)}
    (study_root/"extended-questions.json").write_text(json.dumps(sorted(questions.values(),key=lambda q:q["id"]),indent=2,ensure_ascii=False)+"\n")
    (study_root/"extended-coverage-audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="sources"},indent=2))
    if result["missing"]:
        raise ValueError("Extended catalogue still has unwitnessed choices")


if __name__=="__main__":
    extend(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),tuple(Path(p) for p in sys.argv[4:]))
