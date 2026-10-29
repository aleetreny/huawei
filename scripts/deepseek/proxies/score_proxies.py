"""Compare proxy labellers (luna, qwen, haiku) with DeepSeek's two saved v3 readings on the same 60 events."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import perceive as P  # noqa: E402
import sys as _sys
_sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from datapaths import proxies_dir as _proxies_dir  # noqa: E402

# Usage (from the repo root): uv run python scripts/deepseek/proxies/score_proxies.py
# Data: ~/careerlab-data/proxies/<who>/respuesta-*.json, prompts and ids in ~/careerlab-data/proxies/luna/.

D = _proxies_dir()
ids = json.loads((D / "luna/ids.json").read_text())
truth = {q["node"]: q["truth"] for q in P.questions()}
ds = {r: P.load_run("v3", r) for r in (1, 2)}


def load(who):
    lab = {}
    for f in sorted((D / who).glob("respuesta-*.json")):
        txt = f.read_text()
        m = re.search(r"\{.*\}", txt, re.S)
        if not m:
            continue
        try:
            data = json.loads(m.group(0))
        except ValueError:
            continue
        for ev in data.get("events", []):
            node = ids.get(ev.get("id"))
            for o in ev.get("options", []):
                try:
                    lab[(node, int(o["choice"]))] = {k: str(v) for k, v in o.items() if k != "choice"}
                except (KeyError, TypeError, ValueError):
                    pass
    return lab


def agree(a, b, keys, s):
    ks = [k for k in keys if k in a and k in b]
    return sum(P.norm(a[k].get(s)) == P.norm(b[k].get(s)) for k in ks) / max(1, len(ks))


keys = [(n, c) for n in ids.values() for c in truth[n] if (n, c) in ds[1] and (n, c) in ds[2]]
print(f"{len(keys)} opciones de {len(ids)} situaciones\n")
print(f"{'':18s}" + "".join(f"{s:>9s}" for s in ("output", "network", "skill", "risk")))
print(f"{'DeepSeek-DeepSeek':18s}" + "".join(f"{100 * agree(ds[1], ds[2], keys, s):8.0f}%" for s in ("output", "network", "skill", "risk")))
labs = {w: load(w) for w in ("luna", "qwen", "haiku", "haiku45", "sonnet46", "sonnet5") if (D / w).exists()}
for w, lab in labs.items():
    if not lab:
        print(f"{w:18s} sin respuestas todavía")
        continue
    row = [(agree(lab, ds[1], keys, s) + agree(lab, ds[2], keys, s)) / 2 for s in ("output", "network", "skill", "risk")]
    print(f"{w + '-DeepSeek':18s}" + "".join(f"{100 * x:8.0f}%" for x in row) + f"   ({sum(k in lab for k in keys)} opciones)")

print("\nBajadas reales que no ve cada uno, y cuántas no ve tampoco DeepSeek (lectura 1):")
for s in ("output", "network"):
    downs = [k for k in keys if P.sign(truth[k[0]][k[1]]["d"].get(s, 0)) == "-"]
    dmiss = {k for k in downs if P.norm(ds[1][k].get(s)) != "-"}
    line = f"  {s}: {len(downs)} bajadas; DeepSeek no ve {len(dmiss)}"
    for w, lab in labs.items():
        got = [k for k in downs if k in lab]
        if not got:
            continue
        miss = {k for k in got if P.norm(lab[k].get(s)) != "-"}
        line += f" | {w} no ve {len(miss)}/{len(got)}, {len(miss & dmiss)} en común"
    print(line)
print("\nRiesgo: ve el riesgo real / falsa alarma")
for w, lab in [("deepseek", ds[1])] + list(labs.items()):
    up = [k for k in keys if k in lab and truth[k[0]][k[1]]["risk"] > 0]
    no = [k for k in keys if k in lab and truth[k[0]][k[1]]["risk"] <= 0]
    if up:
        print(f"  {w:9s} {100 * sum(P.norm(lab[k].get('risk')) == '+' for k in up) / len(up):3.0f}% / "
              f"{100 * sum(P.norm(lab[k].get('risk')) == '+' for k in no) / max(1, len(no)):3.0f}%")
