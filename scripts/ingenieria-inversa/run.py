"""Launch one black-box bot batch: P processes, each driving S game servers.

    PYTHONPATH=. .venv/bin/python scripts/ingenieria-inversa/run.py \
        --batch b00-random-safe --policy random-safe --games 3000 --procs 4 --slots 3

Data go to ~/careerlab-data/ingenieria-inversa/<batch>/ (outside iCloud and outside Git).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import multiprocessing as mp
import os
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

import harness  # noqa: E402
import policies  # noqa: E402

DATA = Path(os.environ.get("BB_DATA", Path.home() / "careerlab-data" / "ingenieria-inversa"))


def policy_classes() -> dict[str, type]:
    found = {}
    for mod in (policies,):
        for obj in vars(mod).values():
            if isinstance(obj, type) and issubclass(obj, policies.Base) and obj is not policies.Base:
                found[obj.name] = obj
    try:
        import oracle  # noqa: F401  (optional, added once models exist)
        for obj in vars(oracle).values():
            if isinstance(obj, type) and issubclass(obj, policies.Base) and getattr(obj, "name", None):
                found[obj.name] = obj
    except ImportError:
        pass
    return found


def proc_main(k: int, args: argparse.Namespace, per: int, kwargs: dict) -> None:
    os.nice(args.nice)
    cls = policy_classes()[args.policy]
    shared = cls.load_shared(**kwargs) if hasattr(cls, "load_shared") else None

    arms = kwargs.pop("arms", None)

    def factory(i: int):
        kw = dict(kwargs)
        if arms:
            kw.update(arms[i % len(arms)])
            kw["arm"] = i % len(arms)
        return cls(args.seed + i, shared=shared, **kw) if shared is not None else cls(args.seed + i, **kw)

    counts = asyncio.run(harness.run_batch(DATA / args.batch, f"p{k}", factory, per, args.slots,
                                           start_index=args.offset + k * per))
    print(json.dumps({"proc": k, "finished": counts}), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--games", type=int, required=True)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--slots", type=int, default=3)
    ap.add_argument("--seed", type=int, default=1_000_000)
    ap.add_argument("--offset", type=int, default=0, help="first game index (to extend a batch)")
    ap.add_argument("--nice", type=int, default=10)
    ap.add_argument("--kw", default="{}", help="JSON keyword arguments for the policy")
    args = ap.parse_args()
    kwargs = json.loads(args.kw)
    out = DATA / args.batch
    out.mkdir(parents=True, exist_ok=True)
    os.setpgrp()  # one process group per batch: stop it with `kill -TERM -<pgid>` (see pgid.txt)
    (out / "pgid.txt").write_text(str(os.getpgrp()))
    per = -(-args.games // args.procs)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    manifest = {"args": vars(args), "kwargs": kwargs, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "commit": commit, "engine": version("career-emulator-engine"), "dataset": version("career-emulator-techarena"),
                "engine_env": "official runner values (careerlab.config.OFFICIAL_ENGINE_ENV)", "competition_mode": False,
                "interface": "five official MCP tools only; no seeds, cloning or internal reads"}
    (out / f"manifest-{args.offset}.json").write_text(json.dumps(manifest, indent=2))
    procs = [mp.Process(target=proc_main, args=(k, args, per, kwargs)) for k in range(args.procs)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(json.dumps({"batch": args.batch, "done": True}), flush=True)


if __name__ == "__main__":
    main()
