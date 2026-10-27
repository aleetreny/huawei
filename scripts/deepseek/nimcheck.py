"""Is NVIDIA NIM's free DeepSeek V4 Flash a stand-in for the competition route (OpenRouter, mostly Baidu fp8)?

The OpenRouter side is already paid for: two repeats of the perception labels (``perceive-v3`` r1 and r2,
403 questions) and two repeats of the obedience bank's control arm (``ds-control`` and ``ds-control-b``,
140 common items). NIM repeats the same calls with ``DS_BACKEND=nim``; the OpenRouter-versus-OpenRouter
agreement is the noise floor that the NIM-versus-OpenRouter agreement is compared with. No call here
uses the competition key.

    uv run python scripts/deepseek/nimcheck.py smoke                 # model list, one plain call, one tool call
    uv run python scripts/deepseek/nimcheck.py run [--part perceive|bench|all] [--limit N]
    uv run python scripts/deepseek/nimcheck.py compare [--json out.json]

``run`` and ``smoke`` set ``DS_BACKEND=nim`` themselves; ``compare`` reads files only. Runs resume: answered
questions and items are skipped. The decision rule is in ``lab/reports/deepseek/nim.md``.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

if len(sys.argv) > 1 and sys.argv[1] in ("smoke", "run"):
    os.environ["DS_BACKEND"] = "nim"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bench  # noqa: E402
import perceive  # noqa: E402
from ds import DATA, NIM_ENV, DeepSeek  # noqa: E402

VARIANT = "v3"
OR_ARMS = ("ds-control", "ds-control-b")
NIM_ARM = "nim-control"
IDS = DATA / "ids-nimcheck.txt"
FIELDS = ["type", *perceive.STATS, "risk"]


# ----------------------------------------------------------------------------- smoke
async def smoke() -> None:
    if not NIM_ENV.exists():
        raise SystemExit(f"missing {NIM_ENV}: API_BASE, API_KEY and MODEL_NAME of the NIM key (see nim.md)")
    ds = DeepSeek(concurrency=1)
    try:
        r = await ds._client.get(f"{ds._base}/models", headers={"Authorization": f"Bearer {ds._key}"})
        ids = [m.get("id") for m in (r.json().get("data") or [])] if r.status_code == 200 else []
        print(f"models endpoint: HTTP {r.status_code}; deepseek ids: {[i for i in ids if 'deepseek' in str(i)]}")
        print(f"configured MODEL_NAME: {ds.model} ({'listed' if ds.model in ids else 'NOT listed'})")
        t0 = time.perf_counter()
        msg = await ds.chat([{"role": "user", "content": "Reply with the single word: ready"}], tag="nim-smoke")
        print(f"plain call: {time.perf_counter() - t0:.1f}s, content={msg.get('content')!r:.60}, "
              f"reasoning chars={msg['_usage']['reasoning_chars']}, model={msg['_usage']['model']}")
        tool = {"type": "function", "function": {"name": "observe", "description": "Observe the game.",
                                                  "parameters": {"type": "object", "properties": {}}}}
        msg = await ds.chat([{"role": "user", "content": "Call the observe tool once."}], tag="nim-smoke", tools=[tool])
        print(f"tool call: {[c['function']['name'] for c in msg.get('tool_calls') or []] or 'NONE'}, "
              f"reasoning chars={msg['_usage']['reasoning_chars']}")
        if not msg["_usage"]["reasoning_chars"]:
            print("WARNING: no reasoning came back. OpenRouter serves this model with thinking on; set NIM_EXTRA "
                  "to the thinking flag of the NIM model card (default sent: chat_template_kwargs.thinking=true).")
    finally:
        await ds.close()


# ----------------------------------------------------------------------------- run
def bench_ids() -> list[str]:
    """Items both OpenRouter control repeats answered, in a fixed order."""
    sets = []
    for arm in OR_ARMS:
        sets.append({json.loads(p.read_text())["id"] for p in (bench.RUNS / arm).glob("*.json") if p.name != "arm.json"})
    return sorted(set.intersection(*sets))


async def run(part: str, limit: int | None) -> None:
    if part in ("perceive", "all"):
        nodes = sorted(p.stem for p in (DATA / "perceive" / f"{VARIANT}-r1").glob("*.json"))  # OpenRouter's questions
        for rep in (1, 2):
            await perceive.run(VARIANT, rep, "all", limit, 4, nodes)
    if part in ("bench", "all"):
        ids = bench_ids()
        IDS.write_text("\n".join(ids) + "\n")
        await bench.run("control", NIM_ARM, IDS, limit, 4)


# ----------------------------------------------------------------------------- compare
def agree(a: dict, b: dict, field: str) -> tuple[int, int]:
    keys = set(a) & set(b)
    if field == "type":
        same = sum(a[k].get("type") == b[k].get("type") for k in keys)
    else:
        same = sum(perceive.norm(a[k].get(field)) == perceive.norm(b[k].get(field)) for k in keys)
    return same, len(keys)


def pct(same: int, n: int) -> str:
    if not n:
        return "   -       "
    p = same / n
    return f"{100 * p:5.1f} ±{100 * 1.96 * math.sqrt(p * (1 - p) / n):3.1f}"


def compare_perceive(out: dict[str, Any]) -> None:
    runs = {f"OR{r}": perceive.load_run(VARIANT, r) for r in (1, 2)}
    runs.update({f"NIM{r}": perceive.load_run(VARIANT, r, "-nim") for r in (1, 2)})
    runs = {k: v for k, v in runs.items() if v}
    print(f"\n## Perception ({VARIANT}): options labelled " + ", ".join(f"{k}={len(v)}" for k, v in runs.items()))
    pairs = [("OR1", "OR2", "within OpenRouter"), ("NIM1", "NIM2", "within NIM")]
    cross = [(n, o) for n in ("NIM1", "NIM2") for o in ("OR1", "OR2")]
    print(f"{'field':8s} {'OR1-OR2':>12s} {'NIM1-NIM2':>12s} {'NIM-OR':>12s}  gap (NIM-OR minus OR-OR)")
    out["perceive"] = {}
    for f in FIELDS:
        row = {}
        for a, b, _ in pairs:
            if a in runs and b in runs:
                row[f"{a}-{b}"] = agree(runs[a], runs[b], f)
        cs = [agree(runs[n], runs[o], f) for n, o in cross if n in runs and o in runs]
        if cs:
            row["NIM-OR"] = (sum(s for s, _ in cs), sum(n for _, n in cs))
        gap = (row["NIM-OR"][0] / row["NIM-OR"][1] - row["OR1-OR2"][0] / row["OR1-OR2"][1]) \
            if "NIM-OR" in row and "OR1-OR2" in row and row["NIM-OR"][1] else None
        print(f"{f:8s} {pct(*row.get('OR1-OR2', (0, 0))):>12s} {pct(*row.get('NIM1-NIM2', (0, 0))):>12s} "
              f"{pct(*row.get('NIM-OR', (0, 0))):>12s}  {'' if gap is None else f'{100 * gap:+.1f}'}")
        out["perceive"][f] = {k: {"same": s, "n": n} for k, (s, n) in row.items()} | {"gap": gap}
    qs = perceive.questions()
    print("\naccuracy against the catalogue (risk binary accuracy; mean exact sign over the six stats):")
    out["accuracy"] = {}
    for name, lab in runs.items():
        sub = [q for q in qs if any((q["node"], ch) in lab for ch in q["truth"])]
        res = perceive.score_labels(sub, lab)
        stat = sum(v["exact"] for v in res["stats"].values()) / len(res["stats"])
        risk = res.get("risk", {}).get("binary_acc")
        out["accuracy"][name] = {"risk": risk, "stats": stat, "answers": res["answers"]}
        print(f"  {name:5s} risk {100 * (risk or 0):5.1f}%   stats {100 * stat:5.1f}%   ({res['answers']} options)")


def load_arm(arm: str) -> dict[str, dict[str, Any]]:
    d = bench.RUNS / arm
    return {r["id"]: r for r in (json.loads(p.read_text()) for p in d.glob("*.json") if p.name != "arm.json")} \
        if d.exists() else {}


def compare_bench(out: dict[str, Any]) -> None:
    arms = {a: load_arm(a) for a in (*OR_ARMS, NIM_ARM)}
    print("\n## Obedience bank, control arm: same choice on the same item")
    common = set.intersection(*(set(v) for v in arms.values() if v)) if all(arms.values()) else set()
    out["bench"] = {"common": len(common)}

    def same(a: str, b: str) -> tuple[int, int]:
        ks = [k for k in common if arms[a][k]["done"] and arms[b][k]["done"]]
        return sum(arms[a][k]["choice"] == arms[b][k]["choice"] for k in ks), len(ks)

    if not common:
        print(f"  items: {', '.join(f'{a}={len(v)}' for a, v in arms.items())}; NIM arm not run yet")
        return
    for a, b in (OR_ARMS, (NIM_ARM, OR_ARMS[0]), (NIM_ARM, OR_ARMS[1])):
        s, n = same(a, b)
        out["bench"][f"{a}~{b}"] = {"same": s, "n": n}
        print(f"  {a:13s} ~ {b:13s} {pct(s, n)}  (n={n})")
    print("\n  arm            done   calls/item  reasoning tok/item  output tok/item")
    for a, v in arms.items():
        rs = [v[k] for k in common]
        k = len(rs)
        print(f"  {a:13s} {100 * sum(r['done'] for r in rs) / k:5.1f}%  {sum(r['usage']['calls'] for r in rs) / k:9.1f}"
              f"  {sum(r['usage']['reasoning'] for r in rs) / k:17.0f}  {sum(r['usage']['output'] for r in rs) / k:14.0f}")
        out["bench"][a] = {"done": sum(r["done"] for r in rs) / k, "calls": sum(r["usage"]["calls"] for r in rs) / k}
    print("\n  regret per rule: TRANSMISION_DATA=~/careerlab-data/deepseek uv run python scripts/transmision/score.py "
          f"--items ~/careerlab-data/deepseek/items.jsonl --arms {','.join((*OR_ARMS, NIM_ARM))} --common")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("smoke")
    p = sub.add_parser("run")
    p.add_argument("--part", default="all", choices=("perceive", "bench", "all"))
    p.add_argument("--limit", type=int, help="only the first N questions / items (a quick look)")
    p = sub.add_parser("compare")
    p.add_argument("--json")
    a = ap.parse_args()
    if a.cmd == "smoke":
        asyncio.run(smoke())
    elif a.cmd == "run":
        asyncio.run(run(a.part, a.limit))
    else:
        out: dict[str, Any] = {}
        compare_perceive(out)
        compare_bench(out)
        if a.json:
            Path(a.json).expanduser().write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
