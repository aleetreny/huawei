"""Linea Techo: bot de la replica que reproduce las reglas escritas de `calidad/v4-c5` (= t13-read-v4) con una
percepcion imperfecta, y palancas para medir que hace falta para llegar a L6 (investigacion, nada de esto es texto de Skill).

Percepcion de una opcion (lo que "lee" el agente antes de elegir):
  exact        signos exactos de cada indicador y del riesgo (cota superior)
  noisy        signos exactos degradados con las tasas de deteccion medidas en DeepSeek (HALLAZGOS B17, B18,
               mejora-nota): subidas de Skill vistas 78 %, bajadas de Output 47 %, bajadas de Network 79 %,
               riesgo positivo 86 %; el resto de signos 85 %; falsas alarmas 5 %
  haiku        etiquetas reales de Haiku (lab/reports/question-bank/stat-tags.json: up/down por indicador) y
               riesgo con la tasa de DeepSeek

Palancas (flags del bot):
  qskill=L     desde el nivel L, el trimestre va a Skill: Skill learning (si Health lo permite) + 1 punto, main Rotation
  sskill=L     desde el nivel L, en el paso Crecer, una subida de Skill cuenta doble
  qstall       estancamiento detectado comparando Now con los valores del ultimo trimestre (campo Q de la nota):
               un indicador que no ha subido en todo el trimestre se marca Stalled hasta que vuelva a subir
  caps         conoce los techos del nivel (cota superior de la deteccion de estancamiento)
  detect       deteccion de v4: una subida leida que no se registra marca Stalled (DeepSeek no lo hace)

    uv run python scripts/techo/techobot.py --arms base,qskill=4,qskill=3 --per noisy --games 2000
"""

from __future__ import annotations

import argparse
import collections
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

K = ["health", "dignity", "skill", "network", "output", "wealth"]
CAT = R.Catalog(json.load(open(RX / "catalog_v2.json")))

# tasas de deteccion (probabilidad de ver un signo que existe), por indicador y sentido
NOISY = {("skill", 1): 0.78, ("skill", -1): 0.70, ("output", 1): 0.60, ("output", -1): 0.47,
         ("network", 1): 0.85, ("network", -1): 0.79, ("health", 1): 0.85, ("health", -1): 0.85,
         ("dignity", 1): 0.75, ("dignity", -1): 0.75, ("wealth", 1): 0.9, ("wealth", -1): 0.9,
         ("risk", 1): 0.86, ("risk", -1): 0.5}
FALSE_ALARM = 0.05
FALSE_RISK = 0.10   # "marca R- de mas": una opcion neutra leida como que baja el riesgo
FALSE_RISKPLUS = 0.22  # opciones seguras leidas como arriesgadas (hacia-80 S5: 24 %; precision 71 %)


def sgn(x: float) -> int:
    return (x > 0) - (x < 0)


class Perception:
    def __init__(self, mode: str, seed: int = 0, scale: float = 1.0) -> None:
        self.mode, self.rng, self.scale = mode, random.Random(seed), scale
        self.cache: dict[tuple[str, int], tuple[dict[str, int], int]] = {}
        self.tags = None
        if mode == "haiku":
            self.tags = json.load(open(REPO / "lab/reports/question-bank/stat-tags.json"))

    def _noisy_sign(self, k: str, s: int) -> int:
        if s != 0:
            p = NOISY.get((k, s), 0.85)
            p = 1 - (1 - p) * self.scale   # scale < 1: mejor percepcion; > 1: peor
            return s if self.rng.random() < p else 0
        return self.rng.choice((1, -1)) if self.rng.random() < FALSE_ALARM * self.scale else 0

    def see(self, node: str, k: int) -> tuple[dict[str, int], int]:
        """(signos por indicador, signo del riesgo) tal como los lee el agente. Una lectura por encuentro."""
        d = CAT.nodes[node]["choices"][str(k)]["d"]
        r = CAT.answer_risk(node, k)
        exact = {s: sgn(d.get(s, 0)) for s in K}
        if self.mode == "exact":
            return exact, sgn(r)
        if self.mode == "haiku":
            t = self.tags.get(f"{node}:{k}")
            if t is not None:
                signs = {s: (1 if s in t["up"] else -1 if s in t["down"] else 0) for s in K}
            else:
                signs = {s: self._noisy_sign(s, exact[s]) for s in K}
            rs = self._noisy_sign("risk", sgn(r))
            if rs == 0 and r <= 0:
                u = self.rng.random()
                if u < FALSE_RISKPLUS:
                    rs = 1
                elif r == 0 and u < FALSE_RISKPLUS + FALSE_RISK:
                    rs = -1
            return signs, rs
        signs = {s: self._noisy_sign(s, exact[s]) for s in K}
        rs = self._noisy_sign("risk", sgn(r))
        if rs == 0 and r <= 0:
            u = self.rng.random()
            if u < FALSE_RISKPLUS * self.scale:
                rs = 1
            elif r == 0 and u < (FALSE_RISKPLUS + FALSE_RISK) * self.scale:
                rs = -1
        return signs, rs


FRIENDLY, QUIET = 0, 1


class V4Bot(R.Policy):
    """Las reglas de v4-c5 tal como estan escritas, sobre los signos percibidos."""

    def __init__(self, per: Perception, seed: int = 0, flags: dict | None = None) -> None:
        self.per, self.rng = per, random.Random(seed)
        f = dict(flags or {})
        self.qskill = int(f.get("qskill", 99))     # nivel desde el que el trimestre va a Skill
        self.sskill = int(f.get("sskill", 99))     # nivel desde el que Skill cuenta doble al crecer
        self.qstall = bool(f.get("qstall", False))
        self.caps = bool(f.get("caps", False))
        self.detect = bool(f.get("detect", False))
        self.hguard = int(f.get("hguard", 5))      # Skill learning solo con Health por encima de esto
        self.qmode = f.get("qmode", "v4")          # v4: informes, red, informes + proyecto clave (lo que hace DeepSeek)
        self.skill_only_stall = bool(f.get("sos", False))  # Skill tambien cuando solo uno de N/O esta estancado
        self.pfall = bool(f.get("pfall", False))   # tras un ascenso, el indicador que cayo cuenta doble hasta recuperarse
        self.q3l1 = bool(f.get("q3l1", False))     # C40: en L1 con RR. HH. "quiet", el trimestre va a crecer, no a Defuse
        self.fell: dict[str, float] = {}
        self.dprot = int(f.get("dprot", 4))      # bienestar: proteger Dignity desde este valor
        self.hprot = int(f.get("hprot", 4))      # bienestar: proteger Health desde este valor
        self.risktol = int(f.get("risktol", 0))  # aceptar una opcion arriesgada con RR. HH. amable y sin Concerns si crece >= N mas
        self.lossw = int(f.get("lossw", 1))      # cuanto resta cada indicador de crecimiento que baja
        self.pl1 = f.get("pl1", "")              # en L1 proteger S/N/O todos los meses: "safe" tras el filtro de riesgo,
                                                 # "first" antes (como la excepcion del mes previo, con RR. HH. amable)
        self.ndouble = int(f.get("ndouble", 0))  # hasta este nivel, una subida de Network cuenta doble al crecer
        self.rtn = int(f.get("rtn", 0))         # hasta este nivel, tolerar una marcada que suba Network (RR. HH. amable, sin Concerns)
        self.rtall = bool(f.get("rtall", False))
        self.rtlv = int(f.get("rtlv", 1))
        self.rt = f.get("rt", "")                # tolerancia tipo planificador: "safe0" = aceptar una marcada si crece y
                                                 # ninguna segura crece; "+all" tambien con N=1,2; "+lv2" solo desde L2
        self.prev: dict[str, float] | None = None
        self.lv = None
        self.best: dict[str, float] = {}
        self.stalled: set[str] = set()
        self.stall_at: dict[str, float] = {}
        self.qmark: dict[str, float] | None = None  # Now en el ultimo trimestre
        self.last_read: tuple[dict[str, float], dict[str, int]] | None = None
        self.concerns = 0
        self.month = None
        self.hr = 0           # comentario de RR. HH. al empezar el mes
        self.promos: list[int] = []

    # ------------------------------------------------------------ memoria (la linea de estado)
    def _tick(self, st: R.State) -> None:
        if st.month != self.month:
            self.month, self.concerns = st.month, 0
            self.hr = min(st.risk, 4)          # el comentario llega al empezar el mes
        if self.lv != st.level:
            if self.lv is not None:
                self.promos.append(st.month)
                if self.pfall and self.prev:
                    self.fell = {k: self.prev[k] for k in R.GROWTH if getattr(st, k) < self.prev[k]}
            self.lv, self.best, self.stalled, self.qmark, self.stall_at = st.level, {}, set(), None, {}
        for k in list(self.fell):
            if getattr(st, k) >= self.fell[k]:
                del self.fell[k]
        self.prev = {k: getattr(st, k) for k in R.GROWTH}
        for k in R.GROWTH:
            self.best[k] = max(self.best.get(k, -99), getattr(st, k))
        if self.caps:
            self.stalled = {k for k in R.GROWTH if getattr(st, k) >= R.cap(st.level, k)}
        if self.detect and self.last_read is not None:
            before, signs = self.last_read
            for k in R.GROWTH:
                if signs.get(k, 0) > 0 and getattr(st, k) <= before[k]:
                    self.stalled.add(k)
                    self.stall_at[k] = getattr(st, k)   # "Stalled: N at 3"
                elif getattr(st, k) > before[k]:
                    self.stalled.discard(k)
            self.last_read = None
        if self.detect:
            for k in list(self.stalled):   # la marca vale mientras el indicador siga en el valor en que se paro
                if k in self.stall_at and getattr(st, k) < self.stall_at[k]:
                    self.stalled.discard(k)

    @staticmethod
    def n_to_review(st: R.State) -> int:
        return 6 - st.month % 6 if st.month % 6 else 6

    # ------------------------------------------------------------ historias
    def story(self, rep, st, node):
        self._tick(st)
        opts = []
        for kk in rep.cat.nodes[node]["choices"]:
            signs, rs = self.per.see(node, int(kk))
            opts.append((int(kk), signs, rs))
        n = self.n_to_review(st)
        alert = self.hr != FRIENDLY or self.concerns >= 1

        def keep(pool, bad):
            rest = [o for o in pool if not bad(o)]
            return rest or pool
        # 1. sobrevivir
        opts = keep(opts, lambda o: st.health <= 1 and o[1]["health"] < 0)
        # 4 antes que 2 en el mes previo con RR. HH. tranquilo o quiet (excepcion de v3/v4)
        review_first = n == 1 and self.hr in (FRIENDLY, QUIET) and self.concerns == 0  # paso 2 con Concerns>=1 quita lo "leve"
        if self.pl1 == "first" and st.level == 1 and self.hr in (FRIENDLY, QUIET) and self.concerns == 0:
            review_first = True
        lowers_growth = lambda o: any(o[1][k] < 0 for k in R.GROWTH)
        lowers_no = lambda o: o[1]["network"] < 0 or o[1]["output"] < 0
        if review_first:
            opts = keep(opts, lowers_growth)
        # 2. riesgo (estricto: siempre fuera lo arriesgado; en alerta tambien lo "constructivo" se lee como arriesgado,
        #    que aqui ya esta en el signo)
        risky_pool = opts
        opts = keep(opts, lambda o: o[2] > 0)
        # 3. bienestar
        opts = keep(opts, lambda o: (st.health <= self.hprot and o[1]["health"] < 0) or (st.dignity <= self.dprot and o[1]["dignity"] < 0))
        opts = keep(opts, lambda o: st.wealth < 0 and o[1]["wealth"] < 0)
        if self.pl1 and st.level == 1:
            opts = keep(opts, lowers_growth)
        # 4. cerca de la evaluacion
        if n in (1, 2):
            opts = keep(opts, lowers_no)
            below = [k for k in ("network", "output") if getattr(st, k) < self.best.get(k, -99)]
            if below:
                opts = keep(opts, lambda o: not any(o[1][k] > 0 for k in below))
            if n == 1:
                opts = keep(opts, lowers_growth)
        # 5. crecer
        endgame = st.month >= 46 and n != 1
        grow = [k for k in R.GROWTH if k not in self.stalled] or list(R.GROWTH)

        def score(o):
            sg = o[1]
            if endgame:
                main = sg["health"] + sg["dignity"] - 2 * o[2]
            else:
                main = 0
                for k in grow:
                    if sg[k] > 0:
                        main += 2 if (k == "skill" and st.level >= self.sskill) or k in self.fell \
                            or (k == "network" and st.level <= self.ndouble) else 1
                main -= self.lossw * sum(1 for k in R.GROWTH if sg[k] < 0)
            return (main, -o[2], sg["health"] + sg["dignity"], sg["wealth"] >= 0, self.rng.random())
        pick = max(opts, key=score)
        if self.rt and not endgame and self.hr == FRIENDLY and self.concerns == 0 and (self.rtall or n not in (1, 2)) \
                and st.level >= self.rtlv and st.health > self.hprot and st.dignity > self.dprot:
            cand = [o for o in risky_pool if o[2] > 0 and not any(o[1][k] < 0 for k in R.GROWTH)]
            if cand:
                alt = max(cand, key=score)
                if score(alt)[0] >= 1 and score(pick)[0] <= 0:
                    pick = alt
        if self.rtn and st.level <= self.rtn and not endgame and self.hr == FRIENDLY and self.concerns == 0 \
                and (self.rtall or n not in (1, 2)) and st.health > self.hprot and st.dignity > self.dprot \
                and pick[1]["network"] <= 0:
            cand = [o for o in risky_pool if o[2] > 0 and o[1]["network"] > 0 and not any(o[1][k] < 0 for k in R.GROWTH)]
            if cand:
                pick = max(cand, key=score)
        if self.risktol and not endgame and self.hr == FRIENDLY and self.concerns == 0 and n not in (1, 2) \
                and st.health > self.hprot and st.dignity > self.dprot:
            # tolerancia: una opcion arriesgada que crece claramente mas, una vez al mes, con RR. HH. amable
            cand = [o for o in risky_pool if o[2] > 0 and not any(o[1][k] < 0 for k in R.GROWTH)]
            if cand:
                alt = max(cand, key=score)
                if score(alt)[0] >= score(pick)[0] + self.risktol:
                    pick = alt
        if pick[2] > 0:
            self.concerns += 1
        self.last_read = ({k: getattr(st, k) for k in R.GROWTH}, pick[1])
        return pick[0]

    # ------------------------------------------------------------ trimestre
    def _qstall_update(self, st: R.State) -> None:
        if self.qstall and self.qmark is not None:
            for k in R.GROWTH:
                if getattr(st, k) <= self.qmark[k]:
                    self.stalled.add(k)
                else:
                    self.stalled.discard(k)
        if st.energy == 3:
            self.qmark = {k: getattr(st, k) for k in R.GROWTH}

    def energy(self, rep, st):
        self._tick(st)
        if st.energy == 3:
            self._qstall_update(st)
        e = st.energy
        if st.month >= 46:   # ultimo trimestre
            if self.hr != FRIENDLY and e >= 2 and not getattr(self, "_defused", False):
                self._defused = True
                return "Defuse legacy risk"
            if st.health < 10 and e >= 1:
                return "Health recovery"
            if st.dignity < 10 and e >= 1:
                return "Mental recovery"
            return "Network maintenance" if e >= 1 else None
        # 2. cerca de un limite
        if st.health <= 4 and e >= 1:
            return "Health recovery"
        if st.dignity <= 4 and e >= 1:
            return "Mental recovery"
        if st.network <= 0 and e >= 1:
            return "Network maintenance"
        # 3. RR. HH.
        if self.hr != FRIENDLY and e == 3 and not (self.q3l1 and st.level == 1 and self.hr == QUIET):
            return "Defuse legacy risk"
        # 5/6. crecer
        skill_q = st.level >= self.qskill or (len({"network", "output"} & self.stalled) == 2) \
            or (self.skill_only_stall and ({"network", "output"} & self.stalled))
        if skill_q:
            if e >= 2 and st.health > self.hguard and "skill" not in self.stalled:
                return "Skill learning"
            if e >= 1:
                if "network" not in self.stalled and st.network <= st.output * 1.5:
                    return "Network maintenance"
                return "Prepare report materials" if "output" not in self.stalled else "Network maintenance"
            return None
        # lo que hace DeepSeek con v4: informes, red, informes
        order = [a for a in ("Prepare report materials", "Network maintenance", "Prepare report materials")
                 if not (a == "Prepare report materials" and "output" in self.stalled)
                 and not (a == "Network maintenance" and "network" in self.stalled)]
        if not order:
            return "Skill learning" if e >= 2 and st.health > self.hguard else ("Health recovery" if e >= 1 and st.health < 10 else None)
        idx = 3 - e
        return order[min(idx, len(order) - 1)] if e >= 1 else None

    def main(self, rep, st):
        self._tick(st)
        self._defused = False
        if st.month >= 46:
            return "Lay low and reduce risk" if self.hr != FRIENDLY else "Report results to your manager"
        if st.health <= 4 or st.dignity <= 4 or st.network <= 0 or st.wealth < 0:
            return "Repair a key relationship" if st.health > 4 else "Lay low and reduce risk"
        if self.hr not in (FRIENDLY, QUIET):
            return "Lay low and reduce risk"
        if st.level >= self.qskill or (len({"network", "output"} & self.stalled) == 2) \
                or (self.skill_only_stall and ({"network", "output"} & self.stalled)):
            return "Apply for rotation"
        stalled = self.stalled & set(R.GROWTH)
        if len(stalled) == 2:
            third = (set(R.GROWTH) - stalled).pop()
            return {"skill": "Apply for rotation", "network": "Build a mentorship", "output": "Showcase results"}[third]
        if len(stalled) == 3:
            return "Report results to your manager"
        return "Apply for a key project"


# ------------------------------------------------------------------------------- arnés
def parse_arm(spec: str) -> dict:
    flags = {}
    for tok in spec.split("+"):
        if tok in ("", "base"):
            continue
        if "=" in tok:
            k, v = tok.split("=", 1)
            flags[k] = v
        else:
            flags[tok] = True
    return flags


_ARGS: dict = {}


def _init(args: dict) -> None:
    _ARGS.update(args)


def _play(job: tuple[str, int]) -> dict:
    spec, i = job
    per = Perception(_ARGS["per"], seed=50_000 + i, scale=_ARGS.get("scale", 1.0))
    bot = V4Bot(per, seed=i, flags=parse_arm(spec))
    st, trace = R.play(CAT, bot, random.Random(_ARGS["seed"] + i))
    promos = [m for m, kind, *rest in trace if kind == "r" and rest[0].get("promoted")]
    return {"q": R.Replica.score(st), "level": st.level, "fail": st.failure or "ok", "promos": promos,
            "skill": st.skill, "network": st.network, "output": st.output, "wealth": st.wealth,
            "blow": st.blowups, "month": st.month}


def summarize(name: str, rows: list[dict]) -> str:
    q = np.array([r["q"] for r in rows])
    lv = collections.Counter(r["level"] for r in rows)
    fails = collections.Counter(r["fail"] for r in rows)
    ok = [r for r in rows if r["fail"] == "ok"]
    passed = [r for r in rows if r["promos"] and r["promos"][0] <= 12]  # salio de L1 a tiempo
    pm = collections.Counter(m for r in rows for m in r["promos"])
    l6 = sum(v for k, v in lv.items() if k >= 6) / len(rows)
    l6p = (sum(1 for r in passed if r["level"] >= 6) / len(passed)) if passed else float("nan")
    qp = np.mean([r["q"] for r in passed]) if passed else float("nan")
    sk = np.mean([r["skill"] for r in ok]) if ok else float("nan")
    windows = " ".join(f"m{m}:{pm.get(m, 0) / len(rows):.0%}" for m in (6, 12, 18, 24, 30, 36, 42, 48))
    return (f"{name:34s} Q {q.mean():5.2f}±{q.std(ddof=1) / np.sqrt(len(q)):.2f} | L6+ {l6:4.0%} | pasa L1 {len(passed) / len(rows):4.0%} "
            f"-> Q {qp:5.1f}, L6+ {l6p:4.0%} | Skill fin {sk:5.1f} | {dict(fails)}\n{'':34s} ascensos {windows}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="base")
    ap.add_argument("--per", default="noisy", choices=("exact", "noisy", "haiku"))
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    out = {}
    with ProcessPoolExecutor(a.workers, initializer=_init,
                             initargs=({"per": a.per, "seed": a.seed, "scale": a.scale},)) as ex:
        for spec in a.arms.split(","):
            rows = list(ex.map(_play, [(spec, i) for i in range(a.games)], chunksize=25))
            out[spec] = rows
            print(summarize(f"{spec} [{a.per}]", rows), flush=True)
    if a.json:
        json.dump(out, open(a.json, "w"))


if __name__ == "__main__":
    main()
