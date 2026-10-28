"""Vigila los repos públicos de otros participantes: commits nuevos, repos que aparecen o desaparecen
y notas nuevas en score_report.json. No ejecuta nada de esos repos; sólo git y lectura de JSON.

Uso: python3 -I scripts/fuentes-externas/vigilar.py
Lista de fuentes: lab/reports/fuentes-externas/fuentes.json. Estado (último commit visto y notas):
lab/reports/fuentes-externas/estado.json. Clones en ~/ext/ (fuera del repo).
"""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "lab" / "reports" / "fuentes-externas" / "fuentes.json"
STATE = ROOT / "lab" / "reports" / "fuentes-externas" / "estado.json"
EXT = Path.home() / "ext"
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_LFS_SKIP_SMUDGE="1")


def head(url):
    r = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True, env=ENV, timeout=120)
    return r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else None


def scores(d):
    out = []
    files = [os.path.join(r, n) for r, ds, fs in os.walk(d) if "/.git" not in r for n in fs
             if n.startswith("score_report") and n.endswith(".json")]  # os.walk entra en carpetas ocultas (.career_sim_runner)
    for f in files:
        try:
            r = json.load(open(f))
        except Exception:
            continue
        e = r.get("ending_score") or {}
        dims = {x.get("name"): x.get("raw_value") for x in e.get("dimensions", [])}
        out.append({"archivo": os.path.relpath(f, d), "q": e.get("quantitative_score"), "meses": e.get("survival_months"),
                    "nivel": dims.get("level"), "fichas": (r.get("token_usage") or {}).get("total_tokens")})
    return sorted(out, key=lambda x: x["archivo"])


def clasificacion(url):
    """Lee la clasificación oficial (Hydro devuelve JSON con Accept: application/json).
    Sólo guarda nombre de equipo, puesto y notas: el udict trae correos e IPs que no deben ir al repo."""
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    head_, *rows = d["rows"]
    cols = [c.get("value") for c in head_]
    out = []
    for r in rows:
        u = d["udict"].get(str(r[1].get("raw")), {})
        notas = {cols[i]: c.get("value") for i, c in enumerate(r) if i >= 2}
        nombre = re.sub(r"[\w.+-]+@[\w.-]+", "(correo)", u.get("displayName") or "")  # hay equipos con el correo por nombre
        out.append({"equipo": nombre, "puesto": r[0].get("value"), **notas})
    return out


def main():
    src = json.load(open(SRC))
    state = json.load(open(STATE)) if STATE.exists() else {}
    EXT.mkdir(exist_ok=True)
    news = []
    for rep in src["repos"]:
        url = rep["url"]; key = url.split("github.com/")[-1].lower()
        old = state.get(key, {})
        sha = head(url)
        rec = {"sha": sha, "visto": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "scores": old.get("scores", [])}
        if sha is None:
            if old.get("sha"):
                news.append(f"{key}: ha dejado de ser público")
        elif sha != old.get("sha"):
            d = EXT / key.replace("/", "_")
            subprocess.run(["rm", "-rf", str(d)])
            subprocess.run(["git", "clone", "-q", "--depth", "1", url, str(d)], env=ENV, timeout=900)
            sc = scores(d)
            nuevos = [s for s in sc if s not in old.get("scores", [])]
            rec["scores"] = sc
            news.append(f"{key}: commit nuevo {sha[:7]} (antes {str(old.get('sha'))[:7]}); {len(nuevos)} notas nuevas")
            for s in nuevos:
                news.append(f"    {s}")
        state[key] = rec
    for pg in src.get("paginas", []):
        if "scoreboard" not in pg["url"]:
            continue
        try:
            tabla = clasificacion(pg["url"])
        except Exception as e:
            news.append(f"clasificación: no se pudo leer ({e})")
            continue
        old = {(r["equipo"], r["puesto"]): r for r in state.get("clasificacion", [])}
        con_nota = [r for r in tabla if any(v not in ("—", "0", "", None) for k, v in r.items() if k not in ("equipo", "puesto"))]
        cambios = [r for r in con_nota if old.get((r["equipo"], r["puesto"])) != r]
        if cambios:
            news.append(f"clasificación: {len(con_nota)} de {len(tabla)} equipos con nota; {len(cambios)} filas nuevas o cambiadas")
            for r in sorted(con_nota, key=lambda r: -float(r.get("Score") or 0))[:15]:
                news.append(f"    {r}")
            news += [f"    nosotros: {r}" for r in tabla if r["equipo"] == "Gradient Depression"]
        state["clasificacion"] = tabla
    json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False)
    print("\n".join(news) if news else "sin cambios")


if __name__ == "__main__":
    main()
