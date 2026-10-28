"""Single measure for a categorisation: the replica score of a bot that sees each story option only through
the labels an agent gave it (the generalisation of question-bank/catbot.py to any grouping).

Labels file: {"node:choice": {"group": <code>, "health": "+|-|0", ..., "wealth": ..., "risk": "+|-|0"}}.
Perception of an option, per arm (energy and main action always follow the 7-rule bot, rules.py):
  fx    group        mean exact effect of the option's group, estimated on the OTHER half of the titles
        signs        the labelled sign of each stat, size 1
        group+signs  group mean, overridden by the labelled signs (catbot's "tags" mode)
        exact        the exact effect
  risk  group        +1 if the group's mean hidden-risk step (other half) is above RISK_CUT, else 0
        flag         the labelled risk sign (+1, 0, -1)
        exact        the sign of the exact step
Same seeds as catbot.py (4242 + game), same title halves (Random(7) over the sorted titles).

    uv run python scripts/deepseek/groupbot.py --labels L.json --arms group:group,signs:flag --games 1000
    uv run python scripts/deepseek/groupbot.py --bank --labels L.json --arms ...   # loss per bank decision instead

``--bank`` scores the bank's story decisions (events of ids-V2 and G1): the bot's pick under the same
valuation and the item's state, and the final-score loss against the best option (``q``), split by
design / holdout titles.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import json
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RX = REPO / "lab" / "data" / "ingenieria-inversa"
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
import replica as R  # noqa: E402
import rules  # noqa: E402

K = ["health", "dignity", "skill", "network", "output", "wealth"]
RISK_CUT = 0.3
CAT = R.Catalog(json.load(open(RX / "catalog_v2.json")))


def answers() -> list[dict]:
    out = []
    for nid, nd in CAT.nodes.items():
        for ch, v in nd["choices"].items():
            out.append({"node": nid, "choice": int(ch), "title": nd["title"], "d": v["d"],
                        "risk": CAT.answer_risk(nid, int(ch))})
    return out


A = answers()
TITLE = {a["node"]: a["title"] for a in A}
TITLES = sorted(set(TITLE.values()))
FOLD = {t: i % 2 for i, t in enumerate(random.Random(7).sample(TITLES, len(TITLES)))}


def sgn(v: str | None) -> int:
    v = (v or "0").strip()
    return 1 if v.startswith("+") else -1 if v.startswith("-") else 0


class Perception:
    def __init__(self, labels: dict[str, dict], fx: str, risk: str, default_group: str = "?") -> None:
        self.lab = {(k.split(":")[0], int(k.split(":")[1])): v for k, v in labels.items()}
        self.fx, self.risk = fx, risk
        self.means: dict[tuple[int, str], dict[str, float]] = {}
        self.rmean: dict[tuple[int, str], float] = {}
        groups = collections.defaultdict(lambda: collections.defaultdict(list))
        for a in A:
            g = (self.lab.get((a["node"], a["choice"])) or {}).get("group", default_group)
            groups[FOLD[a["title"]]][g].append(a)
        allg = {g for f in groups.values() for g in f}
        for f in (0, 1):
            other = groups[1 - f]
            pool_all = [a for g in other.values() for a in g]
            for g in allg:
                aa = other.get(g) or pool_all  # unseen group in the other half: overall mean
                self.means[(f, g)] = {k: float(np.mean([a["d"].get(k, 0) for a in aa])) for k in K}
                self.rmean[(f, g)] = float(np.mean([a["risk"] for a in aa]))
        self.default_group = default_group
        self.overall = {f: {k: float(np.mean([a["d"].get(k, 0) for a in A if FOLD[a["title"]] != f])) for k in K}
                        for f in (0, 1)}

    def see(self, node: str, k: int) -> tuple[dict[str, float], int]:
        lab = self.lab.get((node, k))
        f = FOLD.get(TITLE.get(node, ""), 0)
        if lab is None:  # unlabelled (held-out titles while designing): exact for every arm
            r = CAT.answer_risk(node, k)
            return dict(CAT.nodes[node]["choices"][str(k)]["d"]), (r > 0) - (r < 0)
        g = lab.get("group", self.default_group)
        d = CAT.nodes[node]["choices"][str(k)]["d"]
        if self.fx == "exact":
            fx = dict(d)
        elif self.fx == "signs":
            fx = {s: float(sgn(lab.get(s))) for s in K}
        elif self.fx == "group+signs":
            fx = dict(self.means[(f, g)])
            for s in K:
                x = sgn(lab.get(s))
                if x > 0:
                    fx[s] = max(fx.get(s, 0), 1.0)
                elif x < 0:
                    fx[s] = min(fx.get(s, 0), -1.0)
        else:
            fx = dict(self.means[(f, g)])
        if self.risk == "exact":
            r = CAT.answer_risk(node, k)
            sign = (r > 0) - (r < 0)
        elif self.risk == "flag":
            sign = sgn(lab.get("risk"))
        else:
            sign = 1 if self.rmean[(f, g)] > RISK_CUT else 0
        return fx, sign


class Mixed:
    """Several readings of the same options (repeats): each encounter uses one of them at random, as an
    agent that reads the option again every time it meets it."""

    def __init__(self, pers: list[Perception]) -> None:
        self.pers = pers
        self.rng = random.Random(0)

    def see(self, node: str, k: int) -> tuple[dict[str, float], int]:
        return self.rng.choice(self.pers).see(node, k)


class GroupBot(rules.RuleBot):
    def __init__(self, per: Perception | Mixed | None, seed: int = 0) -> None:
        super().__init__()
        self.per, self.rng = per, random.Random(seed)
        if isinstance(per, Mixed):
            per.rng = random.Random(10_000 + seed)

    def story(self, rep, st, node):
        if self.per is None:
            return super().story(rep, st, node)
        best, bv = None, -1e18
        for kk in rep.cat.nodes[node]["choices"]:
            k = int(kk)
            fx, sign = self.per.see(node, k)
            v = self._val(st, fx, sign) + 1e-6 * self.rng.random()
            if v > bv:
                best, bv = k, v
        return best


class LexBot(GroupBot):
    """The written group rule: discard, then prefer, using only the perceived signs and the visible context.

    1. Risk: discard options marked risky ("strict": always; "calm": only when the HR comment is not calm).
    2. Safety: discard options that lower Health when Health is low, or Dignity when Dignity is low.
    3. Review month: discard options that lower Skill, Network or Output.
    (A step that would discard every option is skipped.)
    4. Prefer the option that raises the most growth stats still below their ceiling, counting the one
       furthest below twice and each growth stat it lowers as minus one; at the end of the career, Health,
       Dignity and lower risk instead. Ties: lowers risk, then more Health + Dignity, then no money lost.
    """

    def __init__(self, per: Perception, seed: int = 0, risk_mode: str = "strict", risk_first: str = "",
                 after_blowup: bool = False, defuse_at: int = 2, laylow_at: int = 2, review_first: str = "") -> None:
        super().__init__(per, seed)
        self.review_first = review_first
        self.window = 1
        self.protect_window = 1
        self.know_caps = True        # False: the bot sees no ceiling, only what it detects in play
        self.detect = False          # story stall check: a perceived gain that did not move the stat
        self.protect_stalled = False # never lower a stalled stat before the review
        self.protect_l1 = False      # at the entry level, never lower a growth stat (any month)
        self.quarter = ""            # "blind": DeepSeek-like quarter (report, network, key project); "blind-l4": Skill from L4
        self.stalled, self.last, self.lv, self.best = set(), None, None, {}
        self.pw2_l1 = False          # at L1, also protect Network and Output two months before the review
        self.rv_l1 = False           # at L1 with no blow-up yet, promotion first in the review month at any risk
        self.skill_first_loss = False  # forced growth loss near a review: lose Skill, not Network or Output
        self.repair = False          # review close: if Network or Output fell under its best at the level, raise it back
        self.risk_mode, self.risk_first, self.after_blowup = risk_mode, risk_first, after_blowup
        self.defuse_at, self.laylow_at = defuse_at, laylow_at  # HR level (0-4) from which the quarter cleans risk

    def energy(self, rep, st):
        if not (st.health <= 4 and st.energy >= 1) and min(st.risk, 4) >= self.defuse_at and st.energy >= 3 \
                and st.month < 46:
            return "Defuse legacy risk"  # once per quarter, as the first action
        if self.quarter in ("blind", "blind-l4", "blind-l4b", "blind-l4c") and st.month < 46:
            if st.health <= 4 and st.energy >= 1:
                return "Health recovery"
            if self.quarter in ("blind-l4", "blind-l4b", "blind-l4c") and st.level >= 4:
                if self.quarter == "blind-l4c" and st.health <= 6 and st.energy >= 1:
                    return "Health recovery"
                if st.energy >= 2 and st.health > 4:
                    return "Skill learning"
                if self.quarter in ("blind-l4b", "blind-l4c"):
                    return "Prepare report materials" if st.energy >= 1 else None
                return "Network maintenance" if st.energy >= 1 else None
            if st.energy == 3:
                return "Prepare report materials"
            if st.energy == 2:
                return "Network maintenance"
            return "Prepare report materials" if st.energy >= 1 else None
        return super().energy(rep, st)

    def main(self, rep, st):
        if min(st.risk, 4) >= self.laylow_at and st.month < 46:
            return "Lay low and reduce risk"
        if self.quarter in ("blind", "blind-l4", "blind-l4b", "blind-l4c") and st.month < 46:
            return "Apply for rotation" if self.quarter == "blind-l4" and st.level >= 4 else "Apply for a key project"
        return super().main(rep, st)

    def story(self, rep, st, node):
        if self.lv != st.level:
            self.stalled, self.lv, self.best = set(), st.level, {}
        for k in R.GROWTH:
            self.best[k] = max(self.best.get(k, -99), getattr(st, k))
        if self.detect and self.last is not None:
            before, signs = self.last
            for k in R.GROWTH:
                if signs.get(k, 0) > 0 and getattr(st, k) <= before[k]:
                    self.stalled.add(k)
        opts = []
        for kk in rep.cat.nodes[node]["choices"]:
            fx, sign = self.per.see(node, int(kk))
            opts.append((int(kk), {k: (v > 0) - (v < 0) for k, v in fx.items()}, sign))
        calm = min(st.risk, 4) == 0

        def keep(pool, bad):
            rest = [o for o in pool if not bad(o)]
            return rest or pool
        prep = 6 - st.month % 6 <= self.window if st.month % 6 else False  # months to the review month
        protect = lambda o: any(o[1].get(k, 0) < 0 for k in R.GROWTH)
        if prep and self.review_first and (self.review_first == "always" or min(st.risk, 4) < 2
                                           or (self.rv_l1 and st.level == 1 and st.blowups == 0)):
            opts = keep(opts, protect)  # promotion first in the preparation month
        if self.risk_mode == "survive":  # never take an option that ends the run at once
            opts = keep(opts, lambda o: st.health + o[1].get("health", 0) * 1 <= 0)
        alert = not calm or (self.after_blowup and st.blowups > 0)
        if self.risk_first and (alert or self.risk_first == "always"):
            opts = keep(opts, lambda o: o[2] >= 0)  # only options that lower risk, when there are any
        if self.risk_mode in ("strict", "survive") or not calm:
            opts = keep(opts, lambda o: o[2] > 0)
        opts = keep(opts, lambda o: (st.health <= 3 and o[1].get("health", 0) < 0) or (st.dignity <= 4 and o[1].get("dignity", 0) < 0))
        if self.pw2_l1 and st.level == 1 and st.month % 6 and 6 - st.month % 6 == 2:
            opts = keep(opts, lambda o: o[1].get("network", 0) < 0 or o[1].get("output", 0) < 0)
        if self.skill_first_loss and st.month % 6 and 6 - st.month % 6 <= 2 and \
                all(any(o[1].get(k, 0) < 0 for k in R.GROWTH) for o in opts):
            # every option costs a growth stat: let the loss fall on Skill rather than Network or Output
            opts = keep(opts, lambda o: o[1].get("network", 0) < 0 or o[1].get("output", 0) < 0)
        if self.repair and st.month % 6 and 6 - st.month % 6 <= 2:
            below = [k for k in ("network", "output") if getattr(st, k) < self.best.get(k, -99)]
            if below:
                opts = keep(opts, lambda o: not any(o[1].get(k, 0) > 0 for k in below))
        if (st.month % 6 and 6 - st.month % 6 <= self.protect_window) or (self.protect_l1 and st.level == 1):
            opts = keep(opts, lambda o: any(o[1].get(k, 0) < 0 for k in R.GROWTH))
        if self.protect_stalled and self.stalled and st.month % 6 and 6 - st.month % 6 <= 2:
            opts = keep(opts, lambda o: any(o[1].get(k, 0) < 0 for k in self.stalled))
        lv = st.level
        if self.know_caps:
            room = {k: (R.cap(lv, k) - getattr(st, k)) / max(1.0, R.cap(lv, k)) for k in R.GROWTH}
        else:
            room = {k: (0.0 if k in self.stalled else 0.5) for k in R.GROWTH}
        far = max(room, key=room.get)
        endgame = st.month >= 46

        def score(o):
            sg = o[1]
            if endgame:
                main = sg.get("health", 0) + sg.get("dignity", 0) - 2 * o[2]
            else:
                main = sum((2 if k == far else 1) * (room[k] > 0) for k in R.GROWTH if sg.get(k, 0) > 0)
                main -= sum(1 for k in R.GROWTH if sg.get(k, 0) < 0)
            return (main, -o[2], sg.get("health", 0) + sg.get("dignity", 0), sg.get("wealth", 0) >= 0, self.rng.random())
        pick = max(opts, key=score)
        self.last = ({k: getattr(st, k) for k in R.GROWTH}, pick[1])
        return pick[0]


_PER: dict[str, Perception | None] = {}


def _init(arms: dict[str, Perception | None]) -> None:
    _PER.update(arms)


def _bot(name: str, i: int) -> GroupBot:
    """Lex specs: lex-<strict|calm|survive>[+rf-alert|+rf-always][+blow]."""
    per = _PER[name]
    if "/lex-" in name:
        spec = name.split("/lex-", 1)[1].split("+")
        rf = next((x[3:] for x in spec if x.startswith("rf-")), "")
        dq = next((int(x[2:]) for x in spec if x.startswith("dq")), 2)
        ll = next((int(x[2:]) for x in spec if x.startswith("ll")), 2)
        rv = "always" if "rv" in spec else ("calm" if any(x.startswith("rvc") for x in spec) else "")
        bot = LexBot(per, seed=i, risk_mode=spec[0], risk_first=rf, after_blowup="blow" in spec,
                     defuse_at=dq, laylow_at=ll, review_first=rv)
        bot.window = next((int(x[3:]) for x in spec if x.startswith("rvc") and x[3:]), 1)
        bot.protect_window = next((int(x[2:]) for x in spec if x.startswith("pw")), 1)
        bot.know_caps = "blind" not in spec
        bot.detect = "detect" in spec
        bot.protect_stalled = "ps" in spec
        bot.protect_l1 = "pl1" in spec
        bot.pw2_l1 = "lonetwo" in spec
        bot.repair = "rep" in spec
        bot.skill_first_loss = "sloss" in spec
        bot.rv_l1 = "rvlone" in spec
        bot.quarter = "blind-l4c" if "qb4c" in spec else "blind-l4b" if "qb4b" in spec else ("blind-l4" if "qb4" in spec else ("blind" if "qb" in spec else ""))
        return bot
    return GroupBot(per, seed=i)


def _play(args: tuple[str, int, int]) -> tuple[float, int, str]:
    name, i, seed0 = args
    st, _ = R.play(CAT, _bot(name, i), random.Random(seed0 + i))
    return R.Replica.score(st), st.level, st.failure or "completed"


def games(arms: dict[str, Perception | None], n: int, seed0: int, workers: int) -> dict[str, np.ndarray]:
    res = {}
    with ProcessPoolExecutor(workers, initializer=_init, initargs=(arms,)) as ex:
        for name in arms:
            out = list(ex.map(_play, [(name, i, seed0) for i in range(n)], chunksize=25))
            s = np.array([o[0] for o in out])
            lv = collections.Counter(o[1] for o in out)
            fails = collections.Counter(o[2] for o in out)
            res[name] = s
            print(f"  {name:28s} {s.mean():5.1f} ± {s.std(ddof=1) / np.sqrt(len(s)):.2f}  L6+ "
                  f"{sum(v for k, v in lv.items() if k >= 6) / len(s):4.0%}  {dict(fails)}", flush=True)
    return res


def bank(arms: dict[str, Perception | None]) -> None:
    """Loss per bank story decision: the bot's pick with the item's own state, against the best q."""
    items = [json.loads(x) for x in gzip.open(REPO / "lab/data/transmision/bank-items.jsonl.gz", "rt")]
    keep = set((REPO / "lab/data/transmision/ids-V2.txt").read_text().split()) | set(
        (REPO / "lab/data/transmision/ids-G1.txt").read_text().split())
    items = [it for it in items if it["phase"] == "e" and it["id"] in keep and it["node"] in CAT.nodes]
    print(f"  {len(items)} bank story decisions (V2 + G1)")
    for name, per in arms.items():
        loss = {False: [], True: []}
        for it in items:
            s = it["state"]
            st = R.State(**{k: s[k] for k in R.State.__dataclass_fields__ if k in s})
            bot = GroupBot(per)
            ks = [int(k) for k in it["q"]]
            best, bv = None, -1e18
            for k in ks:
                if str(k) not in CAT.nodes[it["node"]]["choices"]:
                    continue
                if per is None:
                    r = CAT.answer_risk(it["node"], k)
                    fx, sign = CAT.nodes[it["node"]]["choices"][str(k)]["d"], (r > 0) - (r < 0)
                else:
                    fx, sign = per.see(it["node"], k)
                v = bot._val(st, fx, sign)
                if v > bv:
                    best, bv = k, v
            if best is None:
                continue
            q = {int(a): v for a, v in it["q"].items()}
            loss[it["holdout"]].append(max(q.values()) - q[best])
        dv, ho = np.array(loss[False]), np.array(loss[True])
        print(f"  {name:28s} design {dv.mean():.2f} (n={len(dv)})  holdout {ho.mean():.2f} (n={len(ho)})", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", action="append", default=[], help="name=path[+path...] (repeats: one at random per encounter); repeatable")
    ap.add_argument("--arms", default="group:group", help="fx:risk[:lex-mode] specs, comma-separated; lex-mode strict|calm")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--oracle", action="store_true")
    ap.add_argument("--bank", action="store_true")
    a = ap.parse_args()
    arms: dict[str, Perception | None] = {}
    if a.oracle:
        arms["oracle (exact)"] = None
    for spec in a.labels:
        name, paths = spec.split("=", 1)
        sets = [json.load(open(p)) for p in paths.split("+")]
        for pair in a.arms.split(","):
            fx, risk, *lex = pair.split(":")
            pers = [Perception(lab, fx, risk) for lab in sets]
            arms[f"{name} {fx}/{risk}" + (f"/lex-{lex[0]}" if lex else "")] = pers[0] if len(pers) == 1 else Mixed(pers)
    if a.bank:
        bank(arms)
    else:
        print(f"{a.games} games per arm, seeds {a.seed}+i")
        games(arms, a.games, a.seed, a.workers)


if __name__ == "__main__":
    main()
