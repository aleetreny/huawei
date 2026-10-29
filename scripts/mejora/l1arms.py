"""Línea Mejora: batería de brazos en la réplica calibrada (investigación; nada de esto va a un Skill).

    uv run python scripts/mejora/l1arms.py --games 2000 --arms "beta=v4fam,beta=v4fam+l1risk=0.3"
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploracion"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dssim as D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=2000)
    ap.add_argument("--arms", required=True)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--bot", default="QXBot")
    a = ap.parse_args()
    if a.bot == "PQBot":
        import qsearch as Q
        cls = Q.PQBot
    elif a.bot.startswith("M."):
        import mbot as M
        cls = getattr(M, a.bot[2:])
    else:
        cls = getattr(D, a.bot)
    D.run(a.arms.split(","), a.games, workers=a.workers, botcls=cls)


if __name__ == "__main__":
    main()
