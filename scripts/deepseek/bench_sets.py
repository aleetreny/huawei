"""Score DeepSeek bench arms on named item sets: q-loss (points of final score against the best answer),
picks that lower Network or Output when the best answer does not, and risky picks (research only).

    uv run python scripts/deepseek/bench_sets.py ~/careerlab-data/deepseek/ids-v9-sets.json ds-v4-full10 ds-v9
"""
import gzip
import json
import sys
from pathlib import Path
from datapaths import deepseek_dir as _dsdir

REPO = Path(__file__).resolve().parents[2]
RUNS = _dsdir() / "runs"
items = {json.loads(x)["id"]: json.loads(x) for x in gzip.open(REPO / "lab/data/transmision/bank-items.jsonl.gz", "rt")}


def choice(arm: str, iid: str) -> str | None:
    try:
        c = json.load(open(RUNS / arm / (iid.replace(":", "_") + ".json"))).get("choice")
    except (OSError, ValueError):
        return None
    return str(c) if c is not None else None


def main() -> None:
    sets, arms = json.load(open(sys.argv[1])), sys.argv[2:]
    for name, ids in sets.items():
        common = [i for i in ids if all(choice(a, i) for a in arms)]
        print(f"== {name}: {len(common)} of {len(ids)} items answered by every arm")
        for a in arms:
            loss = nolose = risky = best = 0
            for i in common:
                it, c = items[i], choice(a, i)
                q, fx = it["q"], it["fx"]
                b = max(q, key=q.get)
                loss += max(q.values()) - q.get(c, min(q.values()))
                best += c == b
                d = fx.get(c, {}).get("d", {})
                bd = fx[b]["d"]
                nolose += any(d.get(s, 0) < 0 and bd.get(s, 0) >= 0 for s in ("network", "output"))
                risky += fx.get(c, {}).get("dr", 0) > 0
            n = max(1, len(common))
            print(f"  {a:14s} q-loss {loss / n:5.2f}  best {best / n:4.0%}  N/O-losing picks {nolose:3d}  risky picks {risky:3d}")


if __name__ == "__main__":
    main()
