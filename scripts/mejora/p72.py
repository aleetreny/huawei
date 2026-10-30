"""Línea Mejora: media, P(Q>=72), derrotas y nota de versión simulada por brazo en la réplica calibrada (investigación).

    uv run python scripts/mejora/p72.py --games 3000 --arms "<spec>,<spec>" [--bot M.L1Bot]
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploracion"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D
import mbot as M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=3000)
    ap.add_argument("--arms", required=True)
    ap.add_argument("--bot", default="EndBot")
    ap.add_argument("--qual", type=float, default=75.0)
    a = ap.parse_args()
    out = D.run(a.arms.split(","), a.games, workers=16, botcls=getattr(M, a.bot), quiet=True)
    rng = np.random.default_rng(0)
    for spec, rows in out.items():
        q = np.array([r["q"] for r in rows]); ok = np.array([r["fail"] == "ok" for r in rows])
        idx = rng.integers(0, len(q), (100000, 3))
        A = 0.8 * q[idx].mean(1) + 0.1 * a.qual + 0.1 * np.where(ok[idx], 100, 50).mean(1)
        fails = {k: sum(r["fail"] == k for r in rows) / len(rows) for k in ("dismissed", "trust", "health")}
        print(f"{spec[-60:]:60s} Q {q.mean():5.2f}  P(Q>=72) {np.mean(q >= 72):5.1%}  L6 {np.mean([r['level'] >= 6 for r in rows]):4.1%}"
              f"  despidos {fails['dismissed']:4.1%} crisis {fails['trust']:4.1%} salud {fails['health']:4.1%}"
              f"  A media {A.mean():5.2f} P(A>=78) {np.mean(A >= 78):5.2%}", flush=True)


if __name__ == "__main__":
    main()
