"""Evaluación final de los candidatos en la réplica calibrada: media de partidas, reparto de hundimientos y
distribución de la nota de versión (0,8 × media de 3 partidas + 0,1 × calidad + 0,1 × fichas).

Brazos (historias = DeepSeek calibrado; trimestres = las reglas escritas de cada manual):
  cp-v12  CPBot qskill=4 (reglas de la familia; en L1-L3 el bot hace informes, red, informes como DeepSeek con v4)
  ex-v1   trimestre por tramos (L1 informes; L2-3 informe, red, informe + proyecto clave; L4+ Skill learning + informe
          + rotación), Health recovery desde 5, freno de salud en historias (hcare)
  ex-v3   ex-v1 + en el mes previo de L1 penalizar plantarse en público (confp)

    uv run python scripts/exploracion/final_eval.py --games 4000
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D
import qsearch as Q

EX1 = "ep=RRR.RNR.SLR.SLR+mp=KP.KP.ROT.ROT+qh=5"
ARMS = {"cp-v12": (D.QXBot, "qskill=4"),
        "ex-v1 (sólo trimestre)": (Q.PQBot, EX1),
        "ex-v1": (Q.PQBot, EX1 + "+hcare=2+hlow=5"),
        "ex-v3": (Q.PQBot, EX1 + "+hcare=2+hlow=5+privb=0+confp=2")}
QUAL = {"cp-v12": 69.5, "ex-v1 (sólo trimestre)": 75, "ex-v1": 75, "ex-v3": 75}   # media Opus/Sonnet (§6 del README)


def version_dist(rows, qual, tok_ok=98.0, n=200000, seed=0):
    q = np.array([r["q"] for r in rows]); ok = np.array([r["fail"] == "ok" for r in rows])
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(q), (n, 3))
    v = 0.8 * q[idx].mean(1) + 0.1 * qual + 0.1 * np.where(ok[idx], tok_ok, 50).mean(1)
    return v


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--games", type=int, default=4000); ap.add_argument("--temps", default="1,0.7")
    a = ap.parse_args()
    out = {}
    for temp in a.temps.split(","):
        for name, (cls, spec) in ARMS.items():
            s = spec + (f"+temp={temp}" if temp != "1" else "")
            rows = D.run([s], a.games, botcls=cls, quiet=True)[s]
            v = version_dist(rows, QUAL[name])
            q = np.array([r["q"] for r in rows])
            fails = {k: sum(1 for r in rows if r["fail"] == k) / len(rows) for k in ("dismissed", "health", "trust", "broke")}
            res = {"partida": round(q.mean(), 2), "ee": round(q.std(ddof=1) / np.sqrt(len(q)), 2),
                   "completas": round(float(np.mean([r["fail"] == "ok" for r in rows])), 3),
                   "media_completas": round(float(np.mean([r["q"] for r in rows if r["fail"] == "ok"])), 2),
                   "fallos": {k: round(x, 3) for k, x in fails.items()},
                   "version_media": round(float(v.mean()), 2),
                   **{f"P(v>{t})": round(float((v > t).mean()), 3) for t in (64.75, 68.17, 70, 72, 74, 76)}}
            out[f"{name} T={temp}"] = res
            print(f"{name:24s} T={temp}: {json.dumps(res, ensure_ascii=False)}", flush=True)
    json.dump(out, open(Path(__file__).resolve().parents[2] / "lab/reports/exploracion/data/final_eval.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
