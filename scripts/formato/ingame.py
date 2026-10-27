"""What an official game of a script Skill did: advisor calls, obedience, and in-game reading accuracy.

Reads the runner's events log of one game, pairs every advisor call (bash) with the observation before it
and the take_action after it, and compares the agent's option codes with the replica catalogue (research
only: the catalogue never goes into a Skill).

    uv run python scripts/formato/ingame.py <events-*.jsonl> [more ...]
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CAT = json.load(open(REPO / "lab" / "data" / "ingenieria-inversa" / "catalog_v2.json"))
BY_TITLE: dict[tuple[str, int], list[str]] = collections.defaultdict(list)
for nid, nd in CAT["nodes"].items():
    BY_TITLE[(nd["title"], nd["n_choices"])].append(nid)
K = {"H": "health", "D": "dignity", "S": "skill", "N": "network", "O": "output", "W": "wealth"}


def risk_of(nid: str, k: str) -> int:
    return int(CAT["risk"].get(f"E|{nid}|{k}", 0))


def codes(block: str) -> tuple[dict[str, int], int]:
    fx, r = {}, 0
    for tok, sign in re.findall(r"\b([HDSNOWR])\s*([+\-]{1,2})", block.upper()):
        v = 1 if sign[0] == "+" else -1
        if tok == "R":
            r = v
        else:
            fx[K[tok]] = v
    return fx, r


def game(path: Path):
    ev = [json.loads(x) for x in open(path)]
    ev = [e for e in ev if "payload" in e and "delta" not in e["payload"]]
    obs, rows, pending = None, [], None
    calls = collections.Counter()
    for e in ev:
        p = e["payload"]
        if e["kind"] == "tool_call":
            name = p["tool_call"]["name"].replace("mcp_career-emulator-engine_", "")
            calls[name] += 1
            args = json.loads(p["tool_call"]["arguments"] or "{}")
            if name == "bash" and "advisor.py" in args.get("command", ""):
                pending = {"obs": obs, "line": args["command"], "out": None}
            elif name == "take_action":
                if pending and obs is pending["obs"]:
                    pending["took"] = args.get("choice")
                    rows.append(pending)
                elif obs and len(obs.get("choices", [])) > 1:
                    rows.append({"obs": obs, "line": None, "out": None, "took": args.get("choice")})
                pending = None
        elif e["kind"] == "tool_result":
            if str(p.get("tool_name", "")).endswith("observe"):
                try:
                    obs = json.loads(p["raw_output"]["result"])
                except Exception:
                    pass
            elif p.get("tool_name") == "bash" and pending is not None:
                pending["out"] = str(p.get("result"))
    return calls, rows


def main() -> None:
    tot = collections.Counter()
    conf = {s: collections.Counter() for s in list(K.values()) + ["risk"]}
    for f in sys.argv[1:]:
        calls, rows = game(Path(f))
        story = [r for r in rows if r["obs"] and r["obs"].get("current_event", {}).get("title", "").startswith("Quarterly") is False]
        n_adv = sum(1 for r in rows if r["line"])
        follow = sum(1 for r in rows if r["line"] and r["out"] and f"CHOOSE {r['took']}" in r["out"])
        print(f"{Path(f).parent.name}: calls {dict(calls)}; multi-choice decisions {len(rows)}, with advisor {n_adv}, "
              f"took the advisor's choice {follow}")
        for r in story:
            if not r["line"]:
                continue
            ce = r["obs"].get("current_event", {})
            nids = BY_TITLE.get((ce.get("title"), len(r["obs"].get("choices", []))), [])
            if len(nids) != 1:
                continue
            nid = nids[0]
            blocks = dict(re.findall(r"\|\s*(\d+)\s*:\s*([^|\"]*)", r["line"]))
            for k, ch in CAT["nodes"][nid]["choices"].items():
                if k not in blocks:
                    continue
                fx, rr = codes(blocks[k])
                for s in K.values():
                    t = ch["d"].get(s, 0)
                    t = (t > 0) - (t < 0)
                    conf[s][(t, fx.get(s, 0))] += 1
                tr = risk_of(nid, k)
                tr = (tr > 0) - (tr < 0)
                conf["risk"][(tr, rr)] += 1
                tot["options"] += 1
    print(f"options matched to the catalogue: {tot['options']}")
    for s, c in conf.items():
        up = c[(1, 1)] / max(1, sum(v for (t, _), v in c.items() if t == 1))
        dn = c[(-1, -1)] / max(1, sum(v for (t, _), v in c.items() if t == -1))
        fa = sum(v for (t, g), v in c.items() if t <= 0 and g == 1) / max(1, sum(v for (t, _), v in c.items() if t <= 0))
        print(f"  {s:8s} rises seen {up:4.0%}  falls seen {dn:4.0%}  false '+' {fa:4.0%}  (n={sum(c.values())})")


if __name__ == "__main__":
    main()
