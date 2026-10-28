"""Vigila los repos públicos de otros participantes: commits nuevos, repos que aparecen o desaparecen
y notas nuevas en score_report.json. No ejecuta nada de esos repos; sólo git y lectura de JSON.

Uso: python3 -I scripts/fuentes-externas/vigilar.py
Lista de fuentes: lab/reports/fuentes-externas/fuentes.json. Estado (último commit visto y notas):
lab/reports/fuentes-externas/estado.json. Clones en ~/ext/ (fuera del repo).
"""
import json, os, subprocess, sys, time
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
    json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False)
    print("\n".join(news) if news else "sin cambios")


if __name__ == "__main__":
    main()
