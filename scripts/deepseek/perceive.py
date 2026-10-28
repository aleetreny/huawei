"""Perception test: what does DeepSeek see in each story option (type, direction of each stat, hidden risk)?

Each call shows DeepSeek one story question exactly as ``observe`` shows it (title, description, numbered
options) under a labelling prompt (``prompts/perceive-<variant>.md``) and asks, per option, for a type code,
the sign of the effect on six stats and the sign of the hidden-risk step. The answers are compared with
the exact catalogue of the engine line (``catalog_v2.json`` effects, ``riskd_v2.json`` risk steps).

    uv run python scripts/deepseek/perceive.py run --variant v1 --rep 1 --split dev --limit 5
    uv run python scripts/deepseek/perceive.py score --variant v1 [--rep 1] [--split dev|holdout|all]
    uv run python scripts/deepseek/perceive.py haiku            # same scores for Haiku's labels.json + stat-tags.json

Holdout titles (the bank's ``holdout`` flag) are kept out of design: score them only to check a choice.
Raw answers go to ~/careerlab-data/deepseek/perceive/<variant>-r<rep>/ (they can quote game text).
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import glob
import gzip
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
from ds import DATA, SUFFIX, BudgetStop, DeepSeek  # noqa: E402

RX = REPO / "lab" / "data" / "ingenieria-inversa"
STATS = ["health", "dignity", "skill", "network", "output", "wealth"]
CATS = ["FIX", "OWN", "HIDE", "ATTACK", "YIELD", "AVOID", "GUARD", "ESCALATE", "SELL", "PERSIST"]


# ----------------------------------------------------------------------------- questions and truth
def questions() -> list[dict[str, Any]]:
    """Every story question of the catalogue with its observe-like text and the exact truth per option."""
    cat = json.load(open(RX / "catalog_v2.json"))
    risk = json.load(open(RX / "riskd_v2.json"))
    texts: dict[str, Any] = {}
    for f in glob.glob(str(RX / "*" / "nodes-*.jsonl")):
        for line in open(f):
            try:
                n = json.loads(line)
            except ValueError:
                continue
            texts[n["id"]] = n
    bank = [json.loads(x) for x in gzip.open(REPO / "lab/data/transmision/bank-items.jsonl.gz", "rt")]
    holdout = {x["title"] for x in bank if x["holdout"]}
    out = []
    for nid, nd in cat["nodes"].items():
        t = texts.get(nid)
        if not t or t["phase"] != "event":
            continue
        truth = {int(ch): {"d": v["d"], "risk": risk.get(f"E|{nid}|{ch}", 0)} for ch, v in nd["choices"].items()}
        out.append({"node": nid, "title": nd["title"], "holdout": nd["title"] in holdout,
                    "event": {"current_event": {"title": t["title"], "description": t["description"]},
                              "choices": [{"choice": c["choice"], "action": c["action"]} for c in t["choices"]]},
                    "truth": truth})
    out.sort(key=lambda q: q["node"])
    return out


def pick(qs: list[dict[str, Any]], split: str) -> list[dict[str, Any]]:
    if split == "dev":
        return [q for q in qs if not q["holdout"]]
    if split == "holdout":
        return [q for q in qs if q["holdout"]]
    return qs


# ----------------------------------------------------------------------------- run
def parse(content: str) -> dict[int, dict[str, str]] | None:
    m = re.search(r"\{.*\}", content or "", re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
    except ValueError:
        return None
    rows = data.get("options") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return None
    out = {}
    for r in rows:
        try:
            out[int(r["choice"])] = {k: str(v).strip().upper() if k == "type" else str(v).strip() for k, v in r.items()
                                     if k != "choice"}
        except (KeyError, TypeError, ValueError):
            continue
    return out or None


async def run(variant: str, rep: int, split: str, limit: int | None, slots: int, nodes: list[str] | None) -> None:
    system = (HERE / "prompts" / f"perceive-{variant}.md").read_text(encoding="utf-8")
    qs = pick(questions(), split)
    if nodes:
        qs = [q for q in qs if q["node"] in set(nodes)]
    random.Random(5).shuffle(qs)
    if limit:
        qs = qs[:limit]
    out_dir = DATA / "perceive" / f"{variant}-r{rep}{SUFFIX}"
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = [q for q in qs if not (out_dir / f"{q['node']}.json").exists()]
    print(f"perceive {variant} r{rep} {split}: {len(qs)} questions, {len(todo)} to run", flush=True)
    ds = DeepSeek(concurrency=slots)
    done = 0

    async def one(q: dict[str, Any]) -> None:
        nonlocal done
        user = json.dumps(q["event"], ensure_ascii=False, indent=1)
        for attempt in range(2):
            msg = await ds.chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                                tag=f"perceive-{variant}-r{rep}")
            labels = parse(msg.get("content") or "")
            if labels:
                break
        rec = {"node": q["node"], "labels": labels, "content": msg.get("content"),
               "reasoning_chars": len(msg.get("reasoning") or ""), "usage": msg["_usage"]}
        (out_dir / f"{q['node']}.json").write_text(json.dumps(rec, ensure_ascii=False))
        done += 1
        if done % 25 == 0:
            print(f"  {done}/{len(todo)} spent {ds.spent:.4f} USD", flush=True)

    try:
        await asyncio.gather(*(one(q) for q in todo))
    except BudgetStop as exc:
        print(f"STOP: {exc}", flush=True)
    finally:
        await ds.close()
    print(f"done; line spend (logged) {ds.spent:.4f} USD", flush=True)


# ----------------------------------------------------------------------------- score
def sign(x: float) -> str:
    return "+" if x > 0 else "-" if x < 0 else "0"


def norm(v: str | None) -> str:
    v = (v or "0").strip()
    return "+" if v.startswith("+") or v.lower() in ("up", "rises") else "-" if v.startswith("-") or v.lower() in ("down", "falls") else "0"


def score_labels(qs: list[dict[str, Any]], lab: dict[tuple[str, int], dict[str, str]]) -> dict[str, Any]:
    """Per-stat recall of rises and falls, false alarms, risk detection, type distribution and risk by type."""
    st = {s: collections.Counter() for s in STATS}
    rk = collections.Counter()
    by_type: dict[str, list[int]] = collections.defaultdict(list)
    n = missing = 0
    for q in qs:
        for ch, t in q["truth"].items():
            p = lab.get((q["node"], ch))
            if p is None:
                missing += 1
                continue
            n += 1
            for s in STATS:
                true, guess = sign(t["d"].get(s, 0)), norm(p.get(s))
                st[s][(true, guess)] += 1
            r = t["risk"]
            g = norm(p.get("risk")) if "risk" in p else None
            if g is not None:
                rk[("up" if r > 0 else "down" if r < 0 else "zero", g)] += 1
                if r >= 2:
                    rk[("danger", g)] += 1
            if p.get("type"):
                by_type[p["type"]].append(r)
    res: dict[str, Any] = {"answers": n, "missing": missing, "stats": {}}
    for s in STATS:
        c = st[s]
        ups = sum(v for (t, _), v in c.items() if t == "+")
        downs = sum(v for (t, _), v in c.items() if t == "-")
        zeros = sum(v for (t, _), v in c.items() if t == "0")
        res["stats"][s] = {
            "n_up": ups, "n_down": downs,
            "up_recall": c[("+", "+")] / ups if ups else None,
            "down_recall": c[("-", "-")] / downs if downs else None,
            "false_up": c[("0", "+")] / zeros if zeros else None,
            "false_down": c[("0", "-")] / zeros if zeros else None,
            "wrong_direction": (c[("+", "-")] + c[("-", "+")]) / (ups + downs) if ups + downs else None,
            "exact": sum(v for (t, g), v in c.items() if t == g) / sum(c.values()) if c else None}
    if rk:
        up = sum(v for (t, _), v in rk.items() if t == "up")
        notup = sum(v for (t, _), v in rk.items() if t in ("zero", "down"))
        danger = sum(v for (t, _), v in rk.items() if t == "danger")
        down = sum(v for (t, _), v in rk.items() if t == "down")
        flagged = sum(v for (t, g), v in rk.items() if t != "danger" and g == "+")
        tp = rk[("up", "+")]
        res["risk"] = {"n_up": up, "up_recall": tp / up if up else None,
                       "danger_recall": rk[("danger", "+")] / danger if danger else None,
                       "precision": tp / flagged if flagged else None,
                       "false_alarm": (rk[("zero", "+")] + rk[("down", "+")]) / notup if notup else None,
                       "down_recall": rk[("down", "-")] / down if down else None,
                       "binary_acc": (tp + sum(v for (t, g), v in rk.items() if t in ("zero", "down") and g != "+")) / (up + notup)}
    res["types"] = {c: {"n": len(v), "mean_risk": sum(v) / len(v), "risky_share": sum(x > 0 for x in v) / len(v)}
                    for c, v in sorted(by_type.items(), key=lambda kv: -len(kv[1]))}
    return res


def load_run(variant: str, rep: int, suffix: str = "") -> dict[tuple[str, int], dict[str, str]]:
    lab = {}
    for p in (DATA / "perceive" / f"{variant}-r{rep}{suffix}").glob("*.json"):
        r = json.loads(p.read_text())
        for ch, v in (r.get("labels") or {}).items():
            lab[(r["node"], int(ch))] = v
    return lab


def haiku_labels() -> dict[tuple[str, int], dict[str, str]]:
    cats = json.load(open(REPO / "lab/reports/question-bank/labels.json"))
    tags = json.load(open(REPO / "lab/reports/question-bank/stat-tags.json"))
    lab = {}
    for key, c in cats.items():
        n, ch = key.split(":")
        t = tags.get(key, {})
        row = {"type": c}
        for s in STATS:
            row[s] = "+" if s in t.get("up", []) else "-" if s in t.get("down", []) else "0"
        lab[(n, int(ch))] = row
    return lab


def stability(a: dict, b: dict) -> dict[str, float]:
    keys = sorted(set(a) & set(b))
    if not keys:
        return {}
    out = {"n": len(keys), "type": sum(a[k].get("type") == b[k].get("type") for k in keys) / len(keys),
           "risk": sum(norm(a[k].get("risk")) == norm(b[k].get("risk")) for k in keys) / len(keys)}
    for s in STATS:
        out[s] = sum(norm(a[k].get(s)) == norm(b[k].get(s)) for k in keys) / len(keys)
    return out


def export(lab: dict[tuple[str, int], dict[str, str]], out: Path) -> None:
    """Labels in groupbot.py format: {"node:choice": {"group": type, <stat>: sign, "risk": sign}}."""
    rows = {}
    for (n, ch), v in lab.items():
        row = {"group": v.get("type", "?")}
        for s in STATS + ["risk"]:
            if s in v:
                row[s] = norm(v[s])
        rows[f"{n}:{ch}"] = row
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows))
    print(f"{len(rows)} labels -> {out}")


def fmt(x: float | None) -> str:
    return "  -  " if x is None else f"{100 * x:4.0f}%"


def show(name: str, res: dict[str, Any]) -> None:
    print(f"\n## {name}: {res['answers']} answers ({res['missing']} without a label)")
    print("stat     ups  rec_up  downs rec_dn  false+  false-  wrongdir  exact")
    for s, v in res["stats"].items():
        print(f"{s:8s} {v['n_up']:4d}  {fmt(v['up_recall'])}  {v['n_down']:4d}  {fmt(v['down_recall'])}  "
              f"{fmt(v['false_up'])}  {fmt(v['false_down'])}  {fmt(v['wrong_direction'])}  {fmt(v['exact'])}")
    if "risk" in res:
        r = res["risk"]
        print(f"risk: adds-risk recall {fmt(r['up_recall'])} (n={r['n_up']}), risk>=2 recall {fmt(r['danger_recall'])}, "
              f"precision {fmt(r['precision'])}, false alarm {fmt(r['false_alarm'])}, lowers-risk recall "
              f"{fmt(r['down_recall'])}, binary accuracy {fmt(r['binary_acc'])}")
    print("type      n  mean_risk  risky")
    for c, v in res["types"].items():
        print(f"{c:9s} {v['n']:4d}  {v['mean_risk']:+.2f}   {fmt(v['risky_share'])}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--variant", default="v1")
    p.add_argument("--rep", type=int, default=1)
    p.add_argument("--split", default="dev", choices=("dev", "holdout", "all"))
    p.add_argument("--limit", type=int)
    p.add_argument("--slots", type=int, default=8)
    p.add_argument("--nodes")
    p = sub.add_parser("score")
    p.add_argument("--variant", default="v1")
    p.add_argument("--rep", type=int, default=1)
    p.add_argument("--split", default="dev", choices=("dev", "holdout", "all"))
    p.add_argument("--json")
    p = sub.add_parser("export")
    p.add_argument("--variant", default="v1")
    p.add_argument("--rep", type=int, default=1)
    p.add_argument("--out", required=True)
    p = sub.add_parser("haiku")
    p.add_argument("--split", default="dev", choices=("dev", "holdout", "all"))
    p.add_argument("--out", help="also write Haiku's labels in groupbot format here")
    p.add_argument("--only-run", help="restrict to the questions labelled in this DeepSeek run, e.g. v1-r1")
    a = ap.parse_args()
    if a.cmd == "run":
        asyncio.run(run(a.variant, a.rep, a.split, a.limit, a.slots, a.nodes.split(",") if a.nodes else None))
    elif a.cmd == "score":
        qs = pick(questions(), a.split)
        lab = load_run(a.variant, a.rep)
        qs = [q for q in qs if any((q["node"], ch) in lab for ch in q["truth"])]
        res = score_labels(qs, lab)
        show(f"DeepSeek {a.variant} r{a.rep} ({a.split}, {len(qs)} questions)", res)
        other = load_run(a.variant, 2 if a.rep == 1 else 1)
        if other:
            print("\nstability against the other repeat:", {k: round(v, 3) for k, v in stability(lab, other).items()})
        hk = haiku_labels()
        print("type agreement with Haiku labels.json:",
              round(sum(lab[k].get("type") == hk[k]["type"] for k in lab if k in hk) / max(1, sum(k in hk for k in lab)), 3))
        if a.json:
            Path(a.json).write_text(json.dumps(res, indent=1))
    elif a.cmd == "export":
        export(load_run(a.variant, a.rep), Path(a.out).expanduser())
    else:
        if a.out:
            export(haiku_labels(), Path(a.out).expanduser())
        qs = pick(questions(), a.split)
        if a.only_run:
            v, r = a.only_run.rsplit("-r", 1)
            done = load_run(v, int(r))
            qs = [q for q in qs if any((q["node"], ch) in done for ch in q["truth"])]
        show(f"Haiku labels.json + stat-tags.json ({a.split}, {len(qs)} questions)", score_labels(qs, haiku_labels()))


if __name__ == "__main__":
    main()
