"""Línea Mejora: mapa de pérdidas por evaluación en las partidas reales (investigación; nada de esto va a un Skill).

Para cada evaluación sin ascenso (meses 6, 12, … con la partida viva), reconstruye el estado con el que llegó
(estado previo de la última historia del mes anterior + su efecto verdadero con techos), qué indicador faltó frente
al umbral de la réplica, y clasifica cada historia de la ventana (los dos meses desde el último trimestre) que bajó
ese indicador:
  lectura    había una opción sin pérdida de S/N/O y sin riesgo (riesgo verdadero <= 0)
  excepcion  la única opción sin pérdida tenía riesgo +1 (lo que la excepción de mv-4 permite con RR. HH. amable o quiet)
  forzosa    toda opción sin pérdida tenía riesgo >= 2, o todas perdían algo
Si nadie bajó el indicador en la ventana, el déficit es «crecimiento» (no llegó) o «antes» (se perdió antes de la ventana).

    uv run python scripts/mejora/lossmap.py            # lee ~/careerlab-data/exploracion/calib.jsonl.gz (calib_data.py)
"""
from __future__ import annotations
import collections, gzip, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingenieria-inversa"))
import replica as R  # noqa: E402

CALIB = Path.home() / "careerlab-data/exploracion/calib.jsonl.gz"
GROW = ("skill", "network", "output")


def family(manual: str) -> str | None:
    if manual.startswith("mv-"):
        return "mv"
    if manual.startswith("cp-"):
        return "cp"
    if manual in ("t13-read-v3", "t13-read-v4", "t13-read-v5", "t13-read-v7"):
        return "v4"
    return None


def after(st: dict, d: dict, level: int) -> dict:
    s = R.State(health=st["health"], dignity=st["dignity"], skill=st["skill"], network=st["network"],
                output=st["output"], wealth=st["wealth"], level=level)
    R.apply_delta(s, d)
    return {k: getattr(s, k) for k in GROW}


def classify(row: dict, stat: str) -> str:
    th = R.THRESH[row["nivel"]]
    st = row["st"]
    alts = [o for o in row["opts"] if o["k"] != row["choice"]]
    # limpia: no baja el indicador que faltó y no deja ningún otro por debajo de su umbral
    clean = [o for o in alts if o["d"].get(stat, 0) >= 0 and all(
        st[s] + o["d"].get(s, 0) >= min(st[s], t) for s, t in zip(GROW, th))]
    if any(o["risk"] <= 0 for o in clean):
        return "lectura"
    if any(o["risk"] == 1 for o in clean):
        return "excepcion"
    return "forzosa"


def main() -> None:
    rows = [json.loads(l) for l in gzip.open(CALIB, "rt")]
    games = collections.defaultdict(list)
    for r in rows:
        if family(r["manual"]):
            games[r["partida"]].append(r)
    table = collections.Counter()
    by_fam_reviews = collections.Counter()
    detail = []
    for g, rs in games.items():
        fam = family(rs[0]["manual"])
        rs.sort(key=lambda r: (r["mes"]))
        bymonth = collections.defaultdict(list)
        for r in rs:
            bymonth[r["mes"]].append(r)
        last_m = max(bymonth)
        for rev in range(6, 49, 6):
            prev = bymonth.get(rev - 1)
            if not prev or rev > last_m + 1:
                continue
            lv = prev[-1]["nivel"]
            nxt = bymonth.get(rev) or bymonth.get(rev + 1)
            if not nxt:
                continue
            promoted = nxt[0]["nivel"] > lv
            by_fam_reviews[(fam, "evaluaciones")] += 1
            if promoted:
                by_fam_reviews[(fam, "ascensos")] += 1
                continue
            th = R.THRESH.get(lv)
            if not th:
                continue
            last = prev[-1]
            opt = next((o for o in last["opts"] if o["k"] == last["choice"]), None)
            end = after(last["st"], opt["d"] if opt else {}, lv)
            missing = [s for s, t in zip(GROW, th) if end[s] < t]
            if not missing:
                cause = "riesgo/nota" if lv == 1 and rev == 18 else "otro (Dignity, nota D)"
                table[(fam, lv, cause)] += 1
                detail.append((g, rev, lv, cause, end))
                continue
            window = [r for m in (rev - 2, rev - 1) for r in bymonth.get(m, [])]
            for s in missing:
                losses = []
                for r in window:
                    o = next((o for o in r["opts"] if o["k"] == r["choice"]), None)
                    if o and o["d"].get(s, 0) < 0:
                        losses.append(classify(r, s) + ("@N1" if r["mes"] == rev - 1 else "@N2")
                                      + ("/hr" + str(r["hr"]) if r["hr"] is not None else ""))
                if losses:
                    kinds = sorted(set(x.split("@")[0] for x in losses))
                    cause = "pérdida:" + "+".join(kinds)
                else:
                    start = window[0]["st"][s] if window else None
                    cause = "crecimiento" if start is not None and start < th[GROW.index(s)] else "antes"
                table[(fam, lv, f"{s[0].upper()} {cause}")] += 1
                detail.append((g, rev, lv, f"{s} {cause}", end, losses))
    print("== evaluaciones y ascensos por familia")
    for k in sorted(by_fam_reviews):
        print("  ", k, by_fam_reviews[k])
    print("== evaluaciones sin ascenso: indicador que faltó y causa (familia, nivel)")
    for k in sorted(table):
        print("  ", k, table[k])
    agg = collections.Counter()
    for (fam, lv, cause), n in table.items():
        band = "L1" if lv == 1 else "L2-3" if lv <= 3 else "L4+"
        c = cause.split(" ", 1)[-1]
        for k in ("lectura", "excepcion", "forzosa"):
            if k in c:
                agg[(fam, band, k)] += n
        if "pérdida" not in c:
            agg[(fam, band, c)] += n
    print("== agregado (una evaluación puede contar en varias causas)")
    for k in sorted(agg):
        print("  ", k, agg[k])
    print("== detalle")
    for d in detail:
        print("  ", d)


if __name__ == "__main__":
    main()
