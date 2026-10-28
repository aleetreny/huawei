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

CATALOG = ROOT / 'lab/data/ingenieria-inversa/catalog_v2.json'
MANIFEST = ROOT / 'lab/data/ingenieria-inversa/c02-planner-real/manifest-0.json'


def base_params():
    return json.loads((ROOT / 'lab/data/ingenieria-inversa/politica_optima.json').read_text())['params']


class Intervention(Planner):
    def __init__(self, variant='base'):
        p = base_params()
        if variant in ('late_close', 'both') or variant.startswith('skill'):
            p['end_from'] = 48
        super().__init__(**p)
        self.variant = variant
        self.final_decisions = 0

    def value(self, rep, st, fx, dr):
        if self.variant in ('risk_clip', 'both', 'joint_clip', 'bank_clip'):
            dr = max(-st.risk, dr)
        v = super().value(rep, st, fx, dr)
        if self.variant in ('bank', 'bank_clip') and st.level >= 4 and st.month < 46:
            # Treat growth retained across promotion as investment in the next level.
            v += 2.0 * (min(R.cap(st.level, 'skill'), st.skill + fx.get('skill', 0)) - st.skill)
        if self.variant.startswith('skill') and st.level >= 4 and st.month < 48:
            factor = float(self.variant[5:])
            cur = st.skill
            new = min(R.cap(st.level, 'skill'), cur + fx.get('skill', 0))
            t = R.THRESH.get(st.level, R.THRESH[6])[0]
            below = min(new, t) - min(cur, t)
            above = new - cur - below
            wb = self.p['w_below'] * (self.p['review_boost'] if st.month % 6 == 5 else 1)
            wa = self.p['w_above'] * self.p['w_skill_hi']
            v += (factor-1) * (wb * below + wa * above)
        return v

    def story(self, rep, st, node):
        if self.variant in ('terminal', 'terminal_myopic') and st.month == 48:
            self.final_decisions += 1
            best = (-float('inf'), None)
            for k, ch in rep.cat.nodes[node]['choices'].items():
                end = copy.deepcopy(st)
                rep.answer(end, node, int(k))
                if not end.alive:
                    v = -10000
                else:
                    v = R.Replica.score(end)
                    if self.variant == 'terminal':
                        end.energy = 3
                        v = self.quarter_plan(rep, end)[0]
                    if self.final_decisions < 3:
                        v -= 10 * max(0, 3 - end.health) + 10 * max(0, end.risk - 2)
                if v > best[0]:
                    best = (v, int(k))
            return best[1]
        if not self.variant.startswith('chain'):
            return super().story(rep, st, node)
        cost = float(self.variant[5:])
        def evaluate(state, nid, depth):
            best = (-float('inf'), None)
            for k, ch in rep.cat.nodes[nid]['choices'].items():
                dr = self._risk(rep, nid, int(k))
                v = self.value(rep, state, ch['d'], dr)
                nxt = ch.get('next')
                if nxt in rep.cat.nodes and depth > 0:
                    tmp = copy.deepcopy(state)
                    rep.answer(tmp, nid, int(k))
                    tmp.risk = max(0, state.risk + dr)
                    if ch.get('when') != 'same':
                        tmp.month += 1
                    if tmp.alive and tmp.month <= 48 and tmp.risk < R.BLOW_AT:
                        future, _ = evaluate(tmp, nxt, depth-1)
                        v += self.p['w_cont'] * (future - cost)
                if v > best[0]:
                    best = (v, int(k))
            return best
        return evaluate(st, node, 6)[1]

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
                v = (R.Replica.score(end) if self.variant.startswith('terminal') and st.month == 48
                     else self.value(rep, st, fx, end.risk-st.risk))
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
        if self.variant in ('joint', 'joint_clip') or (self.variant.startswith('terminal') and st.month == 48):
            _, actions, _ = self.quarter_plan(rep, st)
            return actions[0] if actions else None
        return super().energy(rep, st)

    def main(self, rep, st):
        if self.variant in ('joint', 'joint_clip') or (self.variant.startswith('terminal') and st.month == 48):
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
                    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    replica_sha256=hashlib.sha256(Path(R.__file__).read_bytes()).hexdigest(),
                    settle_completion=False)
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2))
    results = {}
    with (out/'games.jsonl').open('w') as f:
        for name in args.variants:
            rows=[]
            for i in range(args.games):
                # Preserve the pre-discovery scoring convention of these experiments.
                # The official test includes the real final settlement automatically.
                st, trace = R.play(cat, Intervention(name), random.Random(args.seed+i), settle_completion=False)
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
