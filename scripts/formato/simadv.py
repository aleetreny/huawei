"""Replica score of a Skill script (advisor.py) fed only what the agent can pass it (research, not Skill text).

Each decision builds the advisor's input from the visible state: the stats as the panel shows them, the
HR tone read at the start of the month (0 after a blow-up), and for story options the labels an agent gave
(DeepSeek label files, several passes mixed at random per encounter) or the exact signs (`exact` arm).
The advisor keeps its own memory per game, exactly as its state file would.

    uv run python scripts/formato/simadv.py --advisor lab/policies-src/formato/script-v1/bundle/skills/career-advisor/script/advisor.py \
        --labels ds=~/careerlab-data/deepseek/labels/ds-v3-r1-full.json+~/careerlab-data/deepseek/labels/ds-v3-r2-full.json --games 2000
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import math
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "deepseek"))
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
import groupbot as G  # noqa: E402
import replica as R  # noqa: E402
import rules  # noqa: E402

ADV = None
ARMS: dict = {}


def load_advisor(path: str):
    spec = importlib.util.spec_from_file_location("advisor", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class AdvisorPolicy(R.Policy):
    def __init__(self, adv, per, seed: int, hr_noise: float = 0.0) -> None:
        self.adv, self.per = adv, per
        self.mem = adv.Memory("sim", None)
        self.month, self.hr, self.nb = None, 0, 0
        self.rng = random.Random(seed)
        self.hr_noise = hr_noise
        if isinstance(per, G.Mixed):
            per.rng = random.Random(10_000 + seed)

    cheat = ""

    def _view(self, st: R.State, phase: str) -> dict:
        if "caps" in self.cheat:
            for k in R.GROWTH:
                self.mem.d["caps"][f"{st.level}:{k}"] = R.cap(st.level, k)
        if "risk" in self.cheat:
            self.month, self.hr = st.month, min(st.risk, 4)
            self.mem.d["hr_month"], self.mem.d["hr"], self.mem.d["risk_since"] = st.month, self.hr, 0
        if st.month != self.month:
            self.month, self.hr = st.month, min(st.risk, 4)
            if self.hr_noise and self.rng.random() < self.hr_noise:
                self.hr = max(0, min(4, self.hr + self.rng.choice((-1, 1))))
        if st.blowups > self.nb:
            self.nb, self.hr = st.blowups, 0
        return {"sid": "sim", "phase": phase, "month": st.month, "level": st.level, "energy": st.energy,
                "hr": self.hr, "health": st.health, "dignity": st.dignity, "skill": st.skill,
                "network": st.network, "output": st.output, "wealth": float(R.DISPLAY(st.wealth))}

    def story(self, rep, st, node):
        opts = {}
        for kk in rep.cat.nodes[node]["choices"]:
            k = int(kk)
            if self.per is None:
                r = rep.cat.answer_risk(node, k)
                d = rep.cat.nodes[node]["choices"][kk]["d"]
                fx = {s: float((v > 0) - (v < 0)) for s, v in d.items() if v}
                opts[k] = (fx, (r > 0) - (r < 0))
            else:
                fx, sign = self.per.see(node, k)
                opts[k] = ({s: float((v > 0) - (v < 0)) for s, v in fx.items() if v}, sign)
        k, _ = self.adv.step(self._view(st, "story"), opts, self.mem)
        return k

    def energy(self, rep, st):
        k, name = self.adv.step(self._view(st, "energy"), {}, self.mem)
        return None if name.startswith("Reserve") else name

    def main(self, rep, st):
        k, name = self.adv.step(self._view(st, "main"), {}, self.mem)
        return name


def _init(adv_path, arms, params=None):
    global ADV
    ADV = load_advisor(adv_path)
    ADV.P.update(params or {})
    ARMS.update(arms)


def _play(args):
    name, i, seed0, hr_noise = args
    per = ARMS[name]
    if name == "rulebot-exact":
        pol = rules.RuleBot()
    else:
        pol = AdvisorPolicy(ADV, per, i, hr_noise)
        pol.cheat = name.split("#", 1)[1] if "#" in name else ""
    st, _ = R.play(G.CAT, pol, random.Random(seed0 + i))
    return R.Replica.score(st), st.level, st.failure or "completed"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--advisor", required=True)
    ap.add_argument("--labels", action="append", default=[], help="name=path[+path]")
    ap.add_argument("--exact", action="store_true", help="arm with exact signs and exact risk sign")
    ap.add_argument("--rulebot", action="store_true", help="reference: 7-rule bot with exact caps and live risk")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--hr-noise", type=float, default=0.0)
    ap.add_argument("--params", default="{}", help="JSON overrides of the advisor's P knobs")
    a = ap.parse_args()
    arms = {}
    if a.rulebot:
        arms["rulebot-exact"] = None
    if a.exact:
        arms["advisor exact-signs"] = None
        arms["advisor exact-signs#caps"] = None
        arms["advisor exact-signs#risk"] = None
        arms["advisor exact-signs#caps+risk"] = None
    for spec in a.labels:
        name, paths = spec.split("=", 1)
        sets = [json.load(open(Path(p).expanduser())) for p in paths.split("+")]
        fxm, rm = (name.split("@", 1)[1].split(":") if "@" in name else ("signs", "flag"))
        pers = [G.Perception(lab, fxm, rm) for lab in sets]
        arms[f"advisor {name}"] = pers[0] if len(pers) == 1 else G.Mixed(pers)
    print(f"{a.games} games per arm, seeds {a.seed}+i")
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(a.advisor, arms, json.loads(a.params))) as ex:
        for name in arms:
            out = list(ex.map(_play, [(name, i, a.seed, a.hr_noise) for i in range(a.games)], chunksize=25))
            s = np.array([o[0] for o in out])
            lv = collections.Counter(o[1] for o in out)
            fails = collections.Counter(o[2] for o in out)
            print(f"  {name:28s} {s.mean():5.1f} ± {s.std(ddof=1) / math.sqrt(len(s)):.2f}  "
                  f"mean L {sum(k * v for k, v in lv.items()) / len(s):.2f}  {dict(fails)}", flush=True)


if __name__ == "__main__":
    main()
