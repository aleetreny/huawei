"""Create a new prospective calibration; never modify the first protocol."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from careerlab.episode import atomic_write_json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(root,parent,per_arm=256,seed=620027):
    root.mkdir(parents=True,exist_ok=False)
    original=json.loads((parent/"protocol.json").read_text())
    if sha(parent/"protocol.json")!=(parent/"protocol-sha256.txt").read_text().strip():
        raise ValueError("Parent protocol integrity mismatch")
    original["name"]="financial-reserve-calibration-v1"
    original["derived_after"]={"results_path":str((parent/"results.json").resolve()),"results_sha256":sha(parent/"results.json"),
        "reason":"First reserve improves survival but not the primary promotion-with-survival count; prospectively lower the target and weight, do not pool samples or claim a selected winner."}
    original["per_arm"]=per_arm
    original["seed"]=seed
    original["config"]={"reserve_target":1,"reserve_weight":2}
    original["intervention"]="For narrative choices only, add 2*(min(1,Wealth+nominal_delta)-min(1,Wealth))-max(0,-nominal_delta). Same common policy and frozen models as first study. These numbers are research heuristics."
    original["schedule"]=[]
    rng=random.Random(seed)
    for _ in range(per_arm):
        pair=["baseline","reserve"];rng.shuffle(pair);original["schedule"].extend(pair)
    original["dependencies"][str(Path(__file__).resolve())]=sha(Path(__file__))
    (root/"sources").mkdir()
    for file,expected in original["dependencies"].items():
        p=Path(file)
        if sha(p)!=expected:
            raise ValueError(f"Dependency changed: {p}")
        shutil.copyfile(p,root/"sources"/(p.parent.name+"-"+p.name))
    for name in ("effects","hazards"):
        p=parent/f"frozen-{name}.json"
        if sha(p)!=original[f"{name}_sha256"]:
            raise ValueError("Frozen model integrity mismatch")
        shutil.copyfile(p,root/p.name)
    atomic_write_json(root/"protocol.json",original)
    (root/"protocol-sha256.txt").write_text(sha(root/"protocol.json")+"\n")
    print(json.dumps({"prepared":True,"target":2*per_arm,"config":original["config"],"parent_unchanged":True}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--parent",type=Path,required=True)
    args=p.parse_args()
    prepare(args.root,args.parent)
