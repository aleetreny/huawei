"""Modelo de elección de DeepSeek en las historias (logit condicional), ajustado a las decisiones reales.

Rasgos de cada opción (dentro de una decisión):
- efectos verdaderos del catálogo: ganancia útil de S/N/O (recortada al techo del nivel), pérdida de S/N/O,
  cambio de Health/Dignity/Wealth, riesgo verdadero;
- lecturas de DeepSeek (etiquetas ds-v*-full: signo por indicador y del riesgo, media de las pasadas);
- interacciones con el contexto (mes previo a la evaluación, RR. HH. no amable, Health baja).
Investigación: nada de esto va a un Skill.
"""
from __future__ import annotations
import gzip, json, sys, math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingenieria-inversa"))
import replica as R  # noqa: E402

G = ("skill", "network", "output")
LABK = ("health", "dignity", "skill", "network", "output", "wealth", "risk")
SIGN = {"+": 1, "-": -1, "0": 0}


def lab_signs(lab: dict | None) -> dict[str, float]:
    if not lab:
        return {}
    return {k: SIGN.get(str(lab.get(k, "0")), 0) for k in LABK}


def mean_lab(labs: dict) -> dict[str, float]:
    vals = [lab_signs(v) for v in labs.values() if v]
    if not vals:
        return {k: 0.0 for k in LABK}
    return {k: float(np.mean([v.get(k, 0) for v in vals])) for k in LABK}


FEATS = ["gS", "gN", "gO", "wS", "wN", "wO", "lS", "lN", "lO", "dH", "dD", "dW", "risk", "risky",
         "LS+", "LN+", "LO+", "LS-", "LN-", "LO-", "LH", "LD", "LW", "LR+", "LR-",
         "N1_loss", "N1_lossL", "N12_lossNO", "hr_risk", "hr_LR", "lowH_dH", "lowD_dD", "negW_dW",
         "risk2"]


def features(st: dict, level: int, N: int, hr: int | None, d: dict, risk: int, lab: dict[str, float]) -> list[float]:
    f = {}
    for k, s in zip(G, "SNO"):
        x = d.get(k, 0)
        cur = st[k]
        c = R.cap(level, k)
        useful = max(0.0, min(cur + x, max(c, cur)) - cur) if x > 0 else 0.0
        f["g" + s] = useful
        f["w" + s] = max(0.0, x) - useful        # gain wasted on the ceiling
        f["l" + s] = max(0.0, -x)
    f["dH"] = d.get("health", 0)
    f["dD"] = d.get("dignity", 0)
    f["dW"] = d.get("wealth", 0)
    f["risk"] = max(0, risk)
    f["risky"] = 1.0 if risk > 0 else 0.0
    f["risk2"] = 1.0 if risk >= 2 else 0.0
    for k, s in zip(G, "SNO"):
        f["L" + s + "+"] = max(0.0, lab.get(k, 0))
        f["L" + s + "-"] = max(0.0, -lab.get(k, 0))
    f["LH"] = lab.get("health", 0)
    f["LD"] = lab.get("dignity", 0)
    f["LW"] = lab.get("wealth", 0)
    f["LR+"] = max(0.0, lab.get("risk", 0))
    f["LR-"] = max(0.0, -lab.get("risk", 0))
    loss = f["lS"] + f["lN"] + f["lO"]
    f["N1_loss"] = loss if N == 1 else 0.0
    f["N1_lossL"] = (f["LS-"] + f["LN-"] + f["LO-"]) if N == 1 else 0.0
    f["N12_lossNO"] = (f["lN"] + f["lO"]) if N in (1, 2) else 0.0
    hrb = 1.0 if (hr or 0) > 0 else 0.0
    f["hr_risk"] = hrb * f["risk"]
    f["hr_LR"] = hrb * f["LR+"]
    f["lowH_dH"] = f["dH"] if st["health"] <= 4 else 0.0
    f["lowD_dD"] = f["dD"] if st["dignity"] <= 4 else 0.0
    f["negW_dW"] = f["dW"] if st["wealth"] <= 0 else 0.0
    return [f[k] for k in FEATS]


def load(manuals: set[str] | None = None, exclude: set[str] | None = None):
    rows = [json.loads(l) for l in gzip.open(Path.home() / "careerlab-data/exploracion/calib.jsonl.gz", "rt")]
    out = []
    for r in rows:
        if manuals and r["manual"] not in manuals:
            continue
        if exclude and r["manual"] in exclude:
            continue
        X = np.array([features(r["st"], r["nivel"], r["N"], r["hr"], o["d"], o["risk"], mean_lab(o["lab"])) for o in r["opts"]])
        ks = [o["k"] for o in r["opts"]]
        if r["choice"] not in ks:
            continue
        out.append((X, ks.index(r["choice"]), r))
    return out


def nll(beta, data, cols, l2=0.01):
    s = 0.0
    g = np.zeros_like(beta)
    for X, y, _ in data:
        Z = X[:, cols] @ beta
        Z = Z - Z.max()
        p = np.exp(Z); p /= p.sum()
        s -= math.log(p[y] + 1e-12)
        g -= X[y, cols] - p @ X[:, cols]
    s += l2 * beta @ beta
    g += 2 * l2 * beta
    return s, g


def fit(data, names):
    cols = [FEATS.index(n) for n in names]
    res = minimize(nll, np.zeros(len(cols)), args=(data, cols), jac=True, method="L-BFGS-B")
    return res.x, res.fun, cols


def evaluate(beta, cols, data):
    ll = acc = 0.0
    for X, y, _ in data:
        Z = X[:, cols] @ beta
        Z = Z - Z.max(); p = np.exp(Z); p /= p.sum()
        ll += math.log(p[y] + 1e-12)
        acc += float(np.argmax(p) == y)
    return ll / len(data), acc / len(data)


FAMILY = {"t13-read-v2", "t13-read-v3", "t13-read-v4", "t13-read-v5", "t13-read-v7", "cp-v3", "cp-v5a", "cp-v7",
          "cp-v8", "cp-v10", "cp-v11", "cp-v12"}

SETS = {
    "true": ["gS", "gN", "gO", "wS", "wN", "wO", "lS", "lN", "lO", "dH", "dD", "dW", "risk", "risky", "risk2"],
    "labels": ["LS+", "LN+", "LO+", "LS-", "LN-", "LO-", "LH", "LD", "LW", "LR+", "LR-"],
}
SETS["both"] = SETS["true"] + SETS["labels"]
SETS["both+ctx"] = SETS["both"] + ["N1_loss", "N1_lossL", "N12_lossNO", "hr_risk", "hr_LR", "lowH_dH", "lowD_dD", "negW_dW"]


def main():
    data = load(FAMILY)
    rng = np.random.default_rng(0)
    parts = sorted({r["partida"] for _, _, r in data})
    rng.shuffle(parts)
    test_p = set(parts[: len(parts) // 4])
    tr = [x for x in data if x[2]["partida"] not in test_p]
    te = [x for x in data if x[2]["partida"] in test_p]
    print(f"decisiones {len(data)} (train {len(tr)}, test {len(te)}), partidas {len(parts)}")
    base = np.mean([1 / len(X) for X, _, _ in te])
    print(f"azar: acierto {base:.3f}")
    for name, cols_names in SETS.items():
        b, f, cols = fit(tr, cols_names)
        ll, acc = evaluate(b, cols, te)
        lltr, acctr = evaluate(b, cols, tr)
        print(f"{name:10s} test ll {ll:.3f} acc {acc:.3f} | train ll {lltr:.3f} acc {acctr:.3f}")
    b, f, cols = fit(data, SETS["both+ctx"])
    for n, v in zip(SETS["both+ctx"], b):
        print(f"  {n:12s} {v:+.2f}")
    json.dump({"names": SETS["both+ctx"], "beta": b.tolist()}, open(ROOT / "lab/data/exploracion/choice_beta.json", "w"), indent=1)


if __name__ == "__main__":
    main()
