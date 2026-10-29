"""Línea Exploración: tabla de calibración (investigación; nada de esto va a un Skill).

Empareja cada decisión de historia de las partidas reales de DeepSeek (lab/data/deepseek/decisiones.csv.gz)
con su nodo del catálogo de la réplica (por título, número de opciones y texto de las opciones) y
guarda, por decisión, las opciones con su efecto verdadero, su riesgo verdadero y las lecturas de DeepSeek
(etiquetas ds-v*-full), además del contexto (mes, nivel, indicadores, comentario de RR. HH., Review in N).

    uv run python scripts/exploracion/calib_data.py   # -> ~/careerlab-data/exploracion/calib.jsonl.gz
"""
from __future__ import annotations
import gzip, json, re, sys, collections
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
DS = ROOT / "lab/data/deepseek"
OUT = Path.home() / "careerlab-data/exploracion"   # texto del juego: fuera de Git (se rehace con CPU, NORMAS §1.6)
sys.path.insert(0, str(ROOT / "scripts/ingenieria-inversa"))
import replica as R  # noqa: E402

CAT = json.load(open(ROOT / "lab/data/ingenieria-inversa/catalog_v2.json"))
ANS = json.load(gzip.open(DS / "otros/answers.json.gz", "rt"))
LABELS = {}
for f in ("ds-v1-r1-full", "ds-v1-r2-full", "ds-v3-r1-full", "ds-v3-r2-full"):
    LABELS[f] = json.load(open(DS / "etiquetas" / f"{f}.json"))

text_of = {(a["node"], a["choice"]): a["text"] for a in ANS}
by_title = collections.defaultdict(list)
for nid, n in CAT["nodes"].items():
    by_title[n["title"]].append(nid)


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


class Row:
    """Fila de decisiones.csv con los tipos que usa este script (antes pandas)."""
    INT = ("mes", "n_opciones", "eleccion")
    NUM = ("health", "dignity", "skill", "network", "output", "wealth")

    def __init__(self, x):
        self.x = x
        for k, v in x.items():
            if k in self.INT:
                v = int(float(v)) if v not in ("", None) else 0
            elif k in self.NUM or (k.startswith("d_") and k != "d_nivel"):
                v = float(v) if v not in ("", None) else 0.0
            elif v == "":
                v = None
            setattr(self, k, v)

    def __getitem__(self, k):
        return getattr(self, k)


def hr_level(t):
    return R.hr_level(t or "")


def main():
    allrows = list(csv.DictReader(gzip.open(DS / "decisiones.csv.gz", "rt")))
    games = collections.OrderedDict()
    for x in allrows:
        games.setdefault(x["partida"], []).append(x)
    rows = []
    stats = collections.Counter()
    for part, g in games.items():
        hr = None
        for x in g:
            r = Row(x)
            if isinstance(r.comentario_rrhh, str):
                h = hr_level(r.comentario_rrhh)
                if h is not None:
                    hr = h
            if r.tipo != "historia" or r.n_opciones < 2:
                continue
            stats["historias"] += 1
            node = r.nodo_catalogo if isinstance(r.nodo_catalogo, str) else None
            if node is None:
                cands = [nid for nid in by_title.get(r.situacion, []) if CAT["nodes"][nid]["n_choices"] == r.n_opciones
                         or len(CAT["nodes"][nid]["choices"]) == r.n_opciones]
                ct = norm(r.texto_eleccion)
                cands2 = [nid for nid in cands if norm(text_of.get((nid, int(r.eleccion)), "")) == ct]
                if len(cands2) == 1:
                    node = cands2[0]
                    stats["por_texto"] += 1
                elif len(cands2) > 1:
                    stats["ambiguo"] += 1
                else:
                    stats["sin_nodo"] += 1
            else:
                stats["por_csv"] += 1
            if node is None:
                continue
            n = CAT["nodes"][node]
            opts = []
            for k, ch in sorted(n["choices"].items(), key=lambda x: int(x[0])):
                lab = {f: LABELS[f].get(f"{node}:{k}") for f in LABELS}
                opts.append({"k": int(k), "d": ch["d"], "risk": CAT["risk"].get(f"E|{node}|{k}", 0),
                             "text": text_of.get((node, int(k)), ""), "lab": lab})
            m = int(r.mes)
            lv = int(str(r.nivel).lstrip("L"))
            rows.append({"partida": part, "manual": r.manual, "mes": m, "nivel": lv, "node": node, "title": r.situacion,
                         "choice": int(r.eleccion), "hr": hr, "N": 6 - m % 6 if m % 6 else 6,
                         "st": {k: r[k] for k in ("health", "dignity", "skill", "network", "output", "wealth")},
                         "obs_d": {k: r["d_" + k] for k in ("health", "dignity", "skill", "network", "output", "wealth")},
                         "opts": opts})
    OUT.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT / "calib.jsonl.gz", "wt") as f:
        for x in rows:
            f.write(json.dumps(x) + "\n")
    print(dict(stats), "->", len(rows))


if __name__ == "__main__":
    main()
