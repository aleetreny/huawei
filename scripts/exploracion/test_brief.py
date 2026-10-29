"""Prueba del script con estado de ex-s1 (brief.py) sobre las partidas reales: se le pasan, en orden, las cifras que el
agente vería en cada observe (y las acciones del trimestre), y se comparan sus marcas de «lleno» con los techos de la
réplica (que nunca van al Skill). Investigación: comprueba que el script hace lo que dice.

    uv run python scripts/exploracion/test_brief.py
"""
import csv, gzip, collections, importlib.util, os, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingenieria-inversa"))
import replica as R  # noqa: E402
spec = importlib.util.spec_from_file_location("brief", ROOT / "lab/policies-src/exploracion/ex-s1/bundle/skills/career-rules/script/brief.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
sys.path.insert(0, str(ROOT / "scripts/exploracion"))
from calib_data import Row, hr_level  # noqa: E402

FAM = {"t13-read-v2", "t13-read-v3", "t13-read-v4", "t13-read-v5", "t13-read-v7", "cp-v3", "cp-v5a", "cp-v7", "cp-v8",
       "cp-v10", "cp-v11", "cp-v12"}
KEY = {"S": "skill", "N": "network", "O": "output"}


def main():
    rows = [Row(x) for x in csv.DictReader(gzip.open(ROOT / "lab/data/deepseek/decisiones.csv.gz", "rt"))]
    games = collections.OrderedDict()
    for r in rows:
        if r.manual in FAM:
            games.setdefault(r.partida, []).append(r)
    marks = collections.Counter()
    os.chdir(tempfile.mkdtemp())
    sample = []
    for gi, (g, rs) in enumerate(games.items()):
        sid = f"{gi:08d}"
        hr = 0
        i = 0
        while i < len(rs):
            r = rs[i]
            if isinstance(r.comentario_rrhh, str):
                h = hr_level(r.comentario_rrhh)
                hr = h if h is not None else hr
            lv = int(str(r.nivel).lstrip("L"))
            args = ["brief.py", sid, r.mes, lv, r.health, r.dignity, r.skill, r.network, r.output, r.wealth, hr]
            if r.tipo == "energia":
                en, mn = [], ""
                j = i
                while j < len(rs) and rs[j].tipo in ("energia", "accion") and rs[j].mes == r.mes:
                    if rs[j].tipo == "energia":
                        en.append(str(rs[j].eleccion))
                    else:
                        mn = str(rs[j].eleccion)
                    j += 1
                out = B.main([str(a) for a in args] + [f"q={','.join(en)}:{mn}"])
                i = j
            else:
                out = B.main([str(a) for a in args])
                i += 1
            st = B.load(sid)
            for s, v in st["full"].items():
                cap = R.cap(lv, KEY[s])
                marks["bien" if v >= cap else "falsa"] += 1
                if v < cap and len(sample) < 8:
                    sample.append((g, r.mes, lv, s, v, cap))
            if gi == 0 and r.mes in (3, 4, 6, 7, 24, 25) and r.tipo == "historia":
                print(f"  {g} m{r.mes} L{lv}: {out}")
    print("marcas de lleno (llamada a llamada):", dict(marks))
    for x in sample:
        print("  falsa:", x)


if __name__ == "__main__":
    main()
