"""Independent reconstruction of month 7–12 answer coverage from public archives."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.mcp_client import month_index, phase
from scripts.first_review_search import node_key


def audit(root):
    questions=json.loads((root/"questions.json").read_text())
    required={(q["id"],c["choice"]) for q in questions for c in q["choices"]}
    stories={(q["id"],c["choice"]) for q in questions if q["phase"]=="event" for c in q["choices"]}
    offered,evidence,archives=set(),{},[]
    counts=Counter()
    for archive in sorted(root.glob("*/public-trajectories.jsonl.gz")):
        expected=(archive.parent/"archive-sha256.txt").read_text().split()[0]
        actual=hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual!=expected:
            raise ValueError(f"Archive integrity mismatch: {archive}")
        archives.append({"batch":archive.parent.name,"sha256":actual})
        with gzip.open(archive,"rt") as stream:
            for line in stream:
                r=json.loads(line)
                counts["records"]+=1
                for index,s in enumerate(r["steps"]):
                    if not 7<=month_index(s["before"])<=12:
                        continue
                    key=node_key(s["before"])
                    offered.update((key,c["choice"]) for c in s["before"]["choices"])
                    if s.get("applied") is not True or s.get("ambiguous") or s.get("reply",{}).get("success") is not True:
                        continue
                    choice=s["choice"]
                    if not any(c==choice for c in s["before"]["choices"]):
                        raise ValueError("Executed choice does not match offered choice")
                    pair=(key,choice["choice"])
                    evidence.setdefault(pair,{"batch":archive.parent.name,"run":r["run"],"step":index,
                        "month":month_index(s["before"]),"action":choice["action"]})
    if offered!=required:
        raise ValueError("Catalogue differs from reconstructed offered answers")
    result={"scope":"Every encountered public question/answer in action-before months 7–12, not all histories",
        "counts":dict(counts),"archives":archives,"required":len(required),"witnessed":len(required&set(evidence)),
        "story_required":len(stories),"story_witnessed":len(stories&set(evidence)),
        "complete":required<=set(evidence),
        "missing":[{"question":k,"choice":c} for k,c in sorted(required-set(evidence))],
        "witnesses":[{"question":k,"choice":c,**w} for (k,c),w in sorted(evidence.items())]}
    (root/"independent-coverage-audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("witnesses","archives","missing")},indent=2))
    return result


if __name__=="__main__":
    audit(Path(sys.argv[1]))
