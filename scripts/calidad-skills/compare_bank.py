"""Compara brazos del banco (runbench.py / bench.py): coincidencia de elecciones y perdida de nota por regla.

La perdida de una eleccion es la nota final media del simulador de la mejor opcion menos la de la elegida
(campo q de cada situacion). Intervalo bootstrap 95 % de la diferencia emparejada de perdida.
Uso: TRANSMISION_DATA=<dir> python3 compare_bank.py --a hk-v4 --b hk-c2 [--c hk-v4b]
"""
import argparse, json, os, random, collections
from pathlib import Path

DATA = Path(os.environ.get("TRANSMISION_DATA", Path.home() / "careerlab-data" / "calidad-skills" / "bank"))
RULE_ORDER = ("trigger", "early_ruin", "pre_review", "closing", "low_health", "hr_risk", "skill_l4", "general")


def rule_of(it):
    for r in RULE_ORDER:
        if r in it["tags"]:
            return r + "/" + it["phase"]
    return "?"


def arm(name):
    out = {}
    for f in (DATA / "runs" / name).glob("*_*.json"):
        r = json.loads(f.read_text())
        if r.get("done") and r.get("choice") is not None:
            out[r["id"]] = int(r["choice"])
    return out


def boot(xs, n=4000):
    rng = random.Random(1); m = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(n))
    return m[int(.025 * n)], m[int(.975 * n)]


ap = argparse.ArgumentParser(); ap.add_argument("--a", required=True); ap.add_argument("--b", required=True); ap.add_argument("--c")
a = ap.parse_args()
items = {}
for l in open(DATA / "items.jsonl"):
    it = json.loads(l); items[it["id"]] = it
A, B = arm(a.a), arm(a.b); C = arm(a.c) if a.c else {}
common = sorted(set(A) & set(B))
per = collections.defaultdict(lambda: {"n": 0, "same": 0, "lossA": [], "lossB": []})
for i in common:
    it = items[i]; q = {int(k): v for k, v in it["q"].items()}; best = max(q.values())
    p = per[rule_of(it)]; p["n"] += 1; p["same"] += int(A[i] == B[i])
    p["lossA"].append(best - q.get(A[i], min(q.values()))); p["lossB"].append(best - q.get(B[i], min(q.values())))
print(f"situaciones comunes: {len(common)}")
print(f"| Tipo | n | misma eleccion {a.a} vs {a.b} | perdida {a.a} | perdida {a.b} | diferencia (IC 95 %) |")
print("|---|---:|---:|---:|---:|---|")
tot = {"n": 0, "same": 0, "lossA": [], "lossB": []}
for r in sorted(per):
    p = per[r]
    for k in tot: tot[k] += p[k]
    d = [y - x for x, y in zip(p["lossA"], p["lossB"])]
    lo, hi = boot(d)
    print(f"| {r} | {p['n']} | {p['same'] / p['n']:.0%} | {sum(p['lossA']) / p['n']:.2f} | {sum(p['lossB']) / p['n']:.2f} | {sum(d) / len(d):+.2f} ({lo:+.2f}, {hi:+.2f}) |")
d = [y - x for x, y in zip(tot["lossA"], tot["lossB"])]; lo, hi = boot(d)
print(f"| **todas** | {tot['n']} | {tot['same'] / tot['n']:.0%} | {sum(tot['lossA']) / tot['n']:.2f} | {sum(tot['lossB']) / tot['n']:.2f} | {sum(d) / len(d):+.2f} ({lo:+.2f}, {hi:+.2f}) |")
if C:
    cc = sorted(set(A) & set(C))
    print(f"\nrepeticion {a.a} vs {a.c}: {sum(A[i] == C[i] for i in cc)}/{len(cc)} = {sum(A[i] == C[i] for i in cc) / max(1, len(cc)):.0%} misma eleccion")
