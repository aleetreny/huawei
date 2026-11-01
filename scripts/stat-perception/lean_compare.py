"""Compare two bank arms (runbench.py results) on what grows the history and on the choices.

For each arm: situations answered, mean output tokens per situation (what the model writes), median note
length, mean input tokens (cache read + created + fresh), Skill reads; then the share of situations where
both arms picked the same option, split by bank rule (pre_review against the rest).

    python3 scripts/stat-perception/lean_compare.py --a v4-bank --b lean-bank [--items ~/careerlab-data/transmision/bank-items.jsonl]
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

DATA = Path.home() / "careerlab-data" / "transmision"


def load(arm: str) -> dict[str, dict]:
    out = {}
    for p in (DATA / "runs" / arm).glob("*.json"):
        if p.name == "arm.json":
            continue
        r = json.loads(p.read_text())
        if "id" in r:
            out[r["id"]] = r
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--items", default=str(DATA / "bank-items.jsonl"))
    args = ap.parse_args()
    A, B = load(args.a), load(args.b)
    tags = {}
    for line in open(Path(args.items).expanduser()):
        it = json.loads(line)
        if it["id"] in A or it["id"] in B:
            tags[it["id"]] = "pre_review" if "pre_review" in it["tags"] else "other"
    common = sorted(set(A) & set(B))
    print(f"{len(common)} situations answered by both arms")
    print("| arm | output tokens / situation | median note chars | input tokens / situation | Skill reads / situation |")
    print("|---|---:|---:|---:|---:|")
    for name, R in ((args.a, A), (args.b, B)):
        rows = [R[i] for i in common]
        out = [(r.get("usage") or {}).get("output", 0) for r in rows]
        inp = [sum((r.get("usage") or {}).get(k, 0) for k in ("input", "cache_read", "cache_create")) for r in rows]
        notes = [len(r.get("notes") or "") for r in rows]
        reads = [len(r.get("skill_reads") or []) for r in rows]
        print(f"| {name} | {statistics.mean(out):.0f} | {statistics.median(notes):.0f} | {statistics.mean(inp) / 1000:.0f}k | {statistics.mean(reads):.2f} |")
    for grp in ("pre_review", "other"):
        ids = [i for i in common if tags.get(i) == grp]
        same = sum(A[i].get("choice") == B[i].get("choice") for i in ids)
        print(f"same choice, {grp}: {same}/{len(ids)} ({100 * same / max(len(ids), 1):.0f} %)")


if __name__ == "__main__":
    main()
