"""Lanza un lote del bot explorador (solo las 5 herramientas oficiales, servidor local, sin modelo)."""
from __future__ import annotations

import argparse, asyncio, json, multiprocessing as mp, os, sys, time
from importlib.metadata import version
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "ingenieria-inversa")); sys.path.insert(0, str(HERE.parents[1]))
import harness  # noqa: E402
from explorer import Explorer  # noqa: E402

OUT = Path(os.environ.get("HP_DATA", Path.home() / "careerlab-data" / "huevos-pascua"))
CAT = HERE.parents[1] / "lab" / "data" / "ingenieria-inversa" / "catalog_v2.json"
OPT = {"w_below": 5.32, "w_above": 0.58, "w_skill_hi": 2.04, "review_boost": 4.57, "w_h": 0.69, "w_d": 1.46, "h_floor": 2,
       "d_floor": 4, "w_wealth": 1.69, "risk_cost": 2.07, "risk_cap": 3, "w_cont": 0.44, "end_from": 47, "w_end": 1.43,
       "low_n_risk": 1, "defuse_at": 2, "laylow_at": 3}


def proc_main(k, args, per):
    os.nice(10)
    if args.notes is not None:
        harness.NOTES_TEXT['custom'] = args.notes; os.environ['BB_NOTES'] = 'custom'
    if args.competition:
        os.environ['BB_COMPETITION'] = '1'
    shared = Explorer.load_shared(catalog=str(CAT))
    factory = lambda i: Explorer(args.seed + i, shared=shared, catalog=str(CAT), policy="planner", params=OPT,
                                 explore_below=args.explore_below, risk_room=args.risk_room)
    counts = asyncio.run(harness.run_batch(OUT / args.batch, f"p{k}", factory, per, args.slots, start_index=k * per))
    print(json.dumps({"proc": k, "finished": counts}), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True); ap.add_argument("--games", type=int, required=True)
    ap.add_argument("--procs", type=int, default=4); ap.add_argument("--slots", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7_100_000); ap.add_argument("--explore-below", type=int, default=60); ap.add_argument("--risk-room", type=int, default=2)
    ap.add_argument("--notes", default=None, help="texto fijo para el campo notes (sondeo de palabras clave)")
    ap.add_argument("--competition", action="store_true", help="servidor en modo --competition")
    args = ap.parse_args()
    out = OUT / args.batch; out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps({"args": vars(args), "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "engine": version("career-emulator-engine"), "dataset": version("career-emulator-techarena"), "params": OPT, "notes": args.notes, "competition": args.competition,
        "interface": "five official MCP tools only"}, indent=2))
    per = -(-args.games // args.procs)
    ps = [mp.Process(target=proc_main, args=(k, args, per)) for k in range(args.procs)]
    [p.start() for p in ps]; [p.join() for p in ps]
    print(json.dumps({"batch": args.batch, "done": True}), flush=True)
