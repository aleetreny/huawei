"""Quarter-end actions chosen per level and arm (T18): how Energy and main actions are spent at each level.

    uv run python scripts/secciones/alloc_by_level.py --batch final-periodos-v1
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from periods import rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    a = ap.parse_args()
    out = defaultdict(lambda: defaultdict(Counter))
    for r in rows(None, None, a.batch):
        run = next(Path.home().glob(f"careerlab-data/*/runs/{r['job']}"), None)
        if not run:
            continue
        pending, obs = {}, None
        for path in sorted(run.glob("stream-*.jsonl")):
            for line in path.read_text(errors="replace").splitlines():
                try:
                    m = json.loads(line)
                except ValueError:
                    continue
                content = (m.get("message") or {}).get("content")
                for b in content if isinstance(content, list) else []:
                    if b.get("type") == "tool_use":
                        pending[b["id"]] = b
                    elif b.get("type") == "tool_result":
                        use = pending.get(b.get("tool_use_id"), {})
                        t = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"])
                        if use.get("name", "").endswith("observe"):
                            try:
                                obs = json.loads(t)
                            except ValueError:
                                pass
                        elif use.get("name", "").endswith("take_action") and obs and "current_state" in obs:
                            ev = obs.get("current_event") or {}
                            if "remaining_energy" not in ev and "energy_budget" not in ev and "max_selections" not in ev:
                                continue
                            k = int(use.get("input", {}).get("choice", 0))
                            ch = obs.get("choices") or []
                            act = next((c.get("action", "") for c in ch if c.get("choice") == k), "?")
                            lv = obs["current_state"]["status"].get("level")
                            out[r["policy"]][lv][act] += 1
    for pol in sorted(out):
        print(f"## {pol}")
        for lv in sorted(out[pol]):
            c = out[pol][lv]
            tot = sum(c.values())
            print(f"  {lv} ({tot}): " + ", ".join(f"{k} {100 * v / tot:.0f}%" for k, v in c.most_common(6)) + f" | Skill learning {100 * c['Skill learning'] / tot:.0f}%, rotation {100 * c['Apply for rotation'] / tot:.0f}%")


if __name__ == "__main__":
    main()
