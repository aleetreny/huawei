"""Independent, isolated confirmation through the five official MCP tools. No engine internals."""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import multiprocessing as mp
import os
import random
import sys
from pathlib import Path
from importlib.metadata import version

from experiment import ROOT, CATALOG, Intervention, base_params, R
sys.path.insert(0, str(ROOT))
from replica_bot import ReplicaBot
import harness


class ProbeBot(ReplicaBot):
    name = 'emergentes'

    def __init__(self, seed, shared, variant):
        super().__init__(seed, shared=shared, policy='planner', params=base_params(), variant=variant)
        self.pol = Intervention(variant)

    def _state(self, obs, ctx):
        st = super()._state(obs, ctx)
        if st.month == 48:
            # Save the official visible state, plus the already established risk tracker.
            ctx.setdefault('entry48', dict(st.__dict__))
            ph = harness.phase(obs)
            if ph == 'energy':
                ctx.setdefault('quarter48', dict(st.__dict__))
        return st

    def end_game(self, ctx, rec):
        rec['probe'] = {k:ctx[k] for k in ('entry48','quarter48') if k in ctx}


def worker(k, args, assignments):
    os.nice(10)
    shared = ReplicaBot.load_shared(str(CATALOG))
    def factory(i):
        return ProbeBot(args.seed+i, shared, assignments[i])
    start = k*args.per_process
    print(json.dumps({'process':k, 'counts':asyncio.run(harness.run_batch(
        Path(args.out), f'p{k}', factory, args.per_process, args.slots,
        start_index=start, progress_every=50))}), flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--per-arm',type=int,default=400)
    ap.add_argument('--variants',nargs='+',default=['base','terminal_q'])
    ap.add_argument('--procs',type=int,default=2)
    ap.add_argument('--slots',type=int,default=3)
    ap.add_argument('--seed',type=int,default=901270)
    args=ap.parse_args()
    total=args.per_arm*len(args.variants)
    if total % args.procs:
        raise ValueError('total must be divisible by procs')
    args.per_process=total//args.procs
    out=Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    os.environ['CAREERLAB_ORIGIN']='emergentes'
    os.environ['BB_COMPETITION']='0'
    os.environ.pop('BB_NOTES',None)
    os.setpgrp()
    (out/'pgid.txt').write_text(str(os.getpgrp()))
    assignments=args.variants*args.per_arm
    random.Random(args.seed).shuffle(assignments)
    metadata=dict(args=vars(args), assignments=assignments, params=base_params(),
                  engine=version('career-emulator-engine'),dataset=version('career-emulator-techarena'),
                  catalog_sha256=hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  intervention_sha256=hashlib.sha256(Path(__file__).with_name('experiment.py').read_bytes()).hexdigest(),
                  interface='five official MCP tools; no game seeds, cloning or engine-internal reads')
    (out/'manifest.json').write_text(json.dumps(metadata, indent=2))
    ps=[mp.Process(target=worker,args=(k,args,assignments)) for k in range(args.procs)]
    for p in ps:p.start()
    for p in ps:p.join()
    if any(p.exitcode for p in ps):
        raise SystemExit('A worker failed; retain outputs as incomplete')

if __name__=='__main__':main()
