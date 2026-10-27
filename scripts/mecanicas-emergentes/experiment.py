"""Isolated research interventions; no changes to the shared replica or production policies."""
from __future__ import annotations
import argparse
import collections
import copy
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts' / 'ingenieria-inversa'))
import replica as R
from planner import Planner

CATALOG = ROOT / 'lab/data/ingenieria-inversa/catalog_v1.json'
MANIFEST = ROOT / 'lab/data/ingenieria-inversa/c02-planner-real/manifest-0.json'


def base_params():
    return json.loads(MANIFEST.read_text())['kwargs']['arms'][0]['params']


class Intervention(Planner):
    def __init__(self, variant='base'):
        p = base_params()
        if variant in ('late_close', 'both'):
            p['end_from'] = 48
        super().__init__(**p)
        self.variant = variant

    def value(self, rep, st, fx, dr):
        if self.variant in ('risk_clip', 'both', 'joint_clip', 'bank_clip'):
            dr = max(-st.risk, dr)
        v = super().value(rep, st, fx, dr)
        if self.variant in ('bank', 'bank_clip') and st.level >= 4 and st.month < 46:
            # Treat growth retained across promotion as investment in the next level.
            v += 2.0 * (min(R.cap(st.level, 'skill'), st.skill + fx.get('skill', 0)) - st.skill)
        return v

    def quarter_plan(self, rep, st):
        best = (-float('inf'), [], 'No action')
        def search(cur, actions):
            nonlocal best
            for main in R.MAIN_FX:
                end = copy.copy(cur)
                rep.main_action(end, main)
                if not end.alive:
                    continue
                fx = {k:getattr(end,k)-getattr(st,k) for k in (*R.GROWTH, 'health', 'dignity')}
                v = self.value(rep, st, fx, end.risk-st.risk)
                candidate = (v, actions, main)
                if v > best[0] + 1e-9:
                    best = candidate
            for action, (_, cost) in R.ENERGY_FX.items():
                if cost <= 0 or cost > cur.energy:
                    continue
                nxt = copy.copy(cur)
                rep.energy_action(nxt, action)
                if nxt.alive and nxt.blowups == st.blowups:
                    search(nxt, actions + [action])
        search(copy.copy(st), [])
        return best

    def energy(self, rep, st):
        if self.variant in ('joint', 'joint_clip'):
            _, actions, _ = self.quarter_plan(rep, st)
            return actions[0] if actions else None
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.variant in ('joint', 'joint_clip'):
            tmp = copy.copy(st)
            tmp.energy = 0
            return self.quarter_plan(rep, tmp)[2]
        return super().main(rep, st)


def summarize(rows):
    q = [r['q'] for r in rows]
    return dict(n=len(q), mean=statistics.mean(q), se=statistics.stdev(q)/math.sqrt(len(q)) if len(q)>1 else 0,
                levels=dict(collections.Counter(r['level'] for r in rows)),
                outcomes=dict(collections.Counter(r['failure'] or 'completed' for r in rows)),
                promotions48=sum(r.get('promotions48', False) for r in rows))


def run_sim(args):
    cat = R.Catalog(json.loads(CATALOG.read_text()))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    manifest = dict(mode='replica', seed=args.seed, games_per_arm=args.games, variants=args.variants,
                    catalog_sha256=hashlib.sha256(CATALOG.read_bytes()).hexdigest(), params=base_params(),
                    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2))
    results = {}
    with (out/'games.jsonl').open('w') as f:
        for name in args.variants:
            rows=[]
            for i in range(args.games):
                st, trace = R.play(cat, Intervention(name), random.Random(args.seed+i))
                row=dict(variant=name, seed=args.seed+i, q=R.Replica.score(st), level=st.level,
                         skill=st.skill, wealth=st.wealth, health=st.health, dignity=st.dignity,
                         risk=st.risk, blowups=st.blowups, failure=st.failure,
                         promotions48=any(m==48 and ph=='r' and x[0].get('promoted') for m, ph, *x in trace))
                rows.append(row)
                f.write(json.dumps(row)+'\n')
            results[name]=summarize(rows)
            print(name, json.dumps(results[name]), flush=True)
    (out/'summary.json').write_text(json.dumps(results, indent=2))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--games', type=int, default=400)
    ap.add_argument('--seed', type=int, default=270000)
    ap.add_argument('--variants', nargs='+', default=['base','risk_clip','late_close','both'])
    ap.add_argument('--out', required=True)
    run_sim(ap.parse_args())

if __name__=='__main__':
    main()
