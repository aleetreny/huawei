"""Valor en el simulador de la mecanica 'el trimestre corta la historia y el titulo vuelve al bombo'.

play2 = replica.play + la regla medida (drop_rule.py): en un mes de trimestre, si la respuesta de la
ultima plaza tiene continuacion 'del mismo mes', la historia se descarta y su titulo puede volver a salir.
Brazos (mismas semillas):
  base      planificador optimo en el juego sin la regla (como hasta ahora)
  real      el mismo planificador en el juego con la regla
  aware     sabe que esa continuacion no llegara (no la cuenta)
  replay-w  ademas valora la repeticion del titulo con peso w
Uso: python3 replay_sim.py [partidas]
"""
import sys, os, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
import replica as R
import planner as P
from replica import State, Replica, ENERGY_FX

DATA = os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa')
cat = R.Catalog(json.load(open(os.path.join(DATA, 'catalog_v2.json'))))
OPT = {"w_below": 5.32, "w_above": 0.58, "w_skill_hi": 2.04, "review_boost": 4.57, "w_h": 0.69, "w_d": 1.46, "h_floor": 2,
       "d_floor": 4, "w_wealth": 1.69, "risk_cost": 2.07, "risk_cap": 3, "w_cont": 0.44, "end_from": 47, "w_end": 1.43,
       "low_n_risk": 1, "defuse_at": 2, "laylow_at": 3}
FIRST = set(cat.d['first_node'].values())


class Aware(P.Planner):
    def __init__(self, replay_w=0.0, **p):
        super().__init__(**p); self.replay_w = replay_w; self.slots = 3

    def story(self, rep, st, node):
        if not (st.month % 3 == 0 and self.slots == 1):
            return super().story(rep, st, node)
        best, bv = 1, -1e18
        for k, ch in rep.cat.nodes[node]["choices"].items():
            k = int(k); dr = self._risk(rep, node, k)
            v = self.value(rep, st, ch["d"], dr)
            nxt = ch.get("next")
            if nxt and ch.get("when") != "same" and nxt in rep.cat.nodes:
                tmp = R.State(**{kk: vv for kk, vv in st.__dict__.items() if kk not in ("out_hist", "grades")})
                R.apply_delta(tmp, ch["d"]); tmp.risk = max(0, tmp.risk + dr)
                cont = [self.value(rep, tmp, c2["d"], self._risk(rep, nxt, int(k2))) for k2, c2 in rep.cat.nodes[nxt]["choices"].items()]
                if cont: v += self.p["w_cont"] * max(cont)
            if nxt and ch.get("when") == "same" and node in FIRST and self.replay_w:
                v += self.replay_w * max(0.0, v)   # el titulo vuelve al bombo: otra ocasion de cobrar esta respuesta
            if v > bv: best, bv = k, v
        return best


def play2(cat, policy, rng, drop=True, months=48):
    rep = Replica(cat, rng); st = State(); st.out_hist[1] = st.output
    used, pending, replays, seen = set(), [], 0, set()
    for month in range(1, months + 1):
        queue, pending, slots = pending, [], 3
        while slots > 0 and st.alive:
            if queue:
                node, title = queue.pop(0)
            else:
                t = R.draw_title(cat, st, used, rng)
                if t is None: break
                used.add(t); title = t; node = cat.d["first_node"][t]
                if t in seen: replays += 1
                seen.add(t)
            while st.alive:
                n = cat.nodes.get(node)
                if not n or not n["choices"]: break
                if hasattr(policy, 'slots'): policy.slots = slots
                k = policy.story(rep, st, node)
                rep.answer(st, node, k); slots -= 1
                ch = n["choices"].get(str(k), {})
                if "next" in ch:
                    if ch.get("when") == "same" and slots > 0:
                        node = ch["next"]; continue
                    if drop and ch.get("when") == "same" and month % 3 == 0:
                        used.discard(title)      # la fase trimestral corta la historia
                    else:
                        pending.append((ch["next"], title))
                break
        if not st.alive: break
        if month % 3 == 0:
            st.energy = 3
            while st.alive:
                a = policy.energy(rep, st)
                if not a or ENERGY_FX.get(a, ({}, 9))[1] > st.energy: break
                rep.energy_action(st, a)
            if not st.alive: break
            rep.main_action(st, policy.main(rep, st))
        if month == months:
            if st.alive: rep.month_change(st)
            break
        rep.month_change(st)
        if not st.alive: break
    return st, replays


def arm(name, mk, drop, games, seed=11):
    sc, lv, rp, fail = [], collections.Counter(), [], collections.Counter()
    for i in range(games):
        st, r = play2(cat, mk(), random.Random(seed + i), drop=drop)
        sc.append(Replica.score(st)); lv[st.level] += 1; rp.append(r); fail[st.failure or 'ok'] += 1
    m = sum(sc) / games
    sd = (sum((x - m) ** 2 for x in sc) / (games - 1)) ** 0.5
    return name, round(m, 2), round(sd / games ** 0.5, 2), dict(sorted(lv.items())), round(sum(rp) / games, 2), dict(fail), sc


if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    arms = [('base (sin regla)', lambda: P.Planner(**OPT), False),
            ('real (con regla)', lambda: P.Planner(**OPT), True),
            ('aware', lambda: Aware(**OPT), True),
            ('replay-0.5', lambda: Aware(replay_w=0.5, **OPT), True),
            ('replay-1.0', lambda: Aware(replay_w=1.0, **OPT), True)]
    res = [arm(n, f, d, G) for n, f, d in arms]
    ref = res[1][6]
    for n, m, se, lv, rp, fl, sc in res:
        dif = [a - b for a, b in zip(sc, ref)]
        md = sum(dif) / G; sdd = (sum((x - md) ** 2 for x in dif) / (G - 1)) ** 0.5 / G ** 0.5
        print(f'{n:18s} nota {m} ±{se}  vs real {md:+.2f} ±{sdd:.2f}  niveles {lv}  repeticiones/partida {rp}  {fl}')
