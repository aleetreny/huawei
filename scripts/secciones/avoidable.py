"""Lab diagnostic (never Skill content): were Haiku's Network/Output losses before a review avoidable?

Builds an option-effect catalog from a random-bot batch (announced effects in the official logs,
deterministic per answer, H12), then classifies every story decision Haiku took in the two months
before the first review at L1 in which the chosen answer cost Network or Output:
  safe-alternative   another answer kept Network and Output and added no hidden risk
  risky-alternative  another answer kept them but added hidden risk
  unavoidable        every answer cost Network or Output
  unknown            answer not in the catalog
Output: counts only.

    BB_DATA=~/careerlab-data/secciones-bots uv run python scripts/secciones/avoidable.py b00 --batch p1-base
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ingenieria-inversa"))
from bbdata import Batch, parse_choice_entry  # noqa: E402

from periods import rows  # noqa: E402


def catalog(batch: str) -> dict[tuple[str, str], dict[str, float]]:
    b = Batch(batch)
    cat: dict[tuple[str, str], dict[str, float]] = {}
    for g in b.games():
        for code, msg in b.log_entries(g):
            if code != "A":
                continue
            e = parse_choice_entry(msg)
            if e:
                cat.setdefault((e["title"], e["chosen"].strip()), e["d"])
    return cat


def decisions(run_dir: Path):
    pending, obs = {}, None
    for path in sorted(run_dir.glob("stream-*.jsonl")):
        for line in path.read_text(errors="replace").splitlines():
            try:
                m = json.loads(line)
            except ValueError:
                continue
            content = (m.get("message") or {}).get("content")
            for blk in content if isinstance(content, list) else []:
                if blk.get("type") == "tool_use":
                    pending[blk["id"]] = blk
                elif blk.get("type") == "tool_result":
                    use = pending.get(blk.get("tool_use_id"), {})
                    t = blk["content"] if isinstance(blk["content"], str) else "".join(x.get("text", "") for x in blk["content"])
                    if use.get("name", "").endswith("observe"):
                        try:
                            obs = json.loads(t)
                        except ValueError:
                            pass
                    elif use.get("name", "").endswith("take_action") and obs:
                        yield obs, int(use.get("input", {}).get("choice", 0))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bots")
    ap.add_argument("--batch", required=True)
    a = ap.parse_args()
    cat = catalog(a.bots)
    print("catalog answers:", len(cat))
    out = defaultdict(Counter)
    for r in rows(None, None, a.batch):
        run = next(Path.home().glob(f"careerlab-data/*/runs/{r['job']}"), None)
        if not run:
            continue
        for obs, k in decisions(run):
            st = obs["current_state"]
            month, status = st["time"]["current_month"], st["status"]
            ev = obs.get("current_event") or {}
            choices = obs.get("choices") or []
            if status.get("level") != "L1" or month not in (4, 5) or len(choices) < 2 or "energy_budget" in ev or "max_selections" in ev:
                continue
            title = ev.get("title", "")
            fx = [cat.get((title, c.get("action", "").strip())) for c in choices]
            mine = fx[k - 1] if 0 < k <= len(fx) else None
            c = out[r["policy"]]
            c["decisions"] += 1
            if mine is None:
                c["unknown"] += 1
                continue
            at_cap = {s for s, cap in (("network", 3), ("output", 3)) if (status.get(s) or 0) >= cap}
            lost = [s for s in ("network", "output") if mine.get(s, 0) < 0 and s in at_cap]
            if not lost:
                continue
            c["cost_capped_point"] += 1
            safe = risky = False
            for j, f in enumerate(fx):
                if j == k - 1 or f is None:
                    continue
                if all(f.get(s, 0) >= 0 for s in lost):
                    if f.get("hiddenrisk", 0) > 0:
                        risky = True
                    else:
                        safe = True
            c["safe_alternative" if safe else "risky_alternative" if risky else "unavoidable"] += 1
    for pol, c in sorted(out.items()):
        print(pol, json.dumps(dict(c)))


if __name__ == "__main__":
    main()
