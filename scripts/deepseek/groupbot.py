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


class GroupBot(rules.RuleBot):
    def __init__(self, per: Perception | None, seed: int = 0) -> None:
        super().__init__()
        self.per, self.rng = per, random.Random(seed)

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


_PER: dict[str, Perception | None] = {}


def _init(arms: dict[str, Perception | None]) -> None:
    _PER.update(arms)


def _play(args: tuple[str, int, int]) -> tuple[float, int, str]:
    name, i, seed0 = args
    st, _ = R.play(CAT, GroupBot(_PER[name], seed=i), random.Random(seed0 + i))
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
    ap.add_argument("--labels", action="append", default=[], help="name=path; repeatable")
    ap.add_argument("--arms", default="group:group", help="fx:risk pairs, comma-separated")
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
        name, path = spec.split("=", 1)
        labels = json.load(open(path))
        for pair in a.arms.split(","):
            fx, risk = pair.split(":")
            arms[f"{name} {fx}/{risk}"] = Perception(labels, fx, risk)
    if a.bank:
        bank(arms)
    else:
        print(f"{a.games} games per arm, seeds {a.seed}+i")
        games(arms, a.games, a.seed, a.workers)


if __name__ == "__main__":
    main()
