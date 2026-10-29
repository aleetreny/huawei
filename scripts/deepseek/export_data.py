"""Copy the DeepSeek data that only lived on Alejandro's Mac (~/careerlab-data) into lab/data/deepseek/.

Team decision of 29 Oct (NORMAS §1.6): the repo is private, so official DeepSeek games, DeepSeek bench runs,
perception labels and the data the DeepSeek reports cite go to Git, game text included. The script is
idempotent: it rebuilds lab/data/deepseek/ from ~/careerlab-data and rewrites the two summary tables.

Every text file passes a filter that blanks anything shaped like a key or an authorisation header and
replaces the home path with "~". Never copied: *.env files (keys), the official runner checkouts (software,
re-installable with scripts/setup_official_runner.sh), items.jsonl (rebuilt from the bank by bench.py),
the cut-1 ZIP and video (copied outside the Mac instead).

    uv run python scripts/deepseek/export_data.py            # rebuild lab/data/deepseek
    uv run python scripts/deepseek/export_data.py --check    # only list what would be copied
"""

from __future__ import annotations

import argparse
import collections
import csv
import gzip
import io
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = Path.home() / "careerlab-data"
OUT = REPO / "lab" / "data" / "deepseek"
HOME = str(Path.home())
CATALOG = REPO / "lab" / "data" / "ingenieria-inversa" / "catalog_v2.json"
MAX_BYTES = 50 * 1024 * 1024

SECRET = re.compile(
    r"sk-or-v1-[0-9a-fA-F]{16,}|sk-or-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9_-]{24,}|nvapi-[A-Za-z0-9_-]{16,}"
    r"|(Authorization\"?\s*[:=]\s*\"?Bearer\s+)[A-Za-z0-9._~+/=-]{8,}"
    r"|((?:api_key|apikey|API_KEY)\"?'?\s*[:=]\s*[\"']?)[A-Za-z0-9._-]{16,}")

# Official games whose run folder kept no events.jsonl (cut by our watchdog or a port clash): the raw output
# of the official runner stayed in the slot. Matched by slot, start time, last month and level (28-29 Oct).
RAW_FOR_RUN = {
    "deepseek-pilo-0b43b18e-dff20f-00000-a1": "huawei-deepseek/target-slots/slot0/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T182853Z",
    "deepseek-pilo-4bdd76ad-dff20f-00000-a1": "huawei-deepseek/target-slots/slot0/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T185312Z",
    "deepseek-pilo-f78c8b88-dff20f-00001-a1": "huawei-deepseek/target-slots/slot1/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T195611Z",
    "deepseek-pilo-0b43b18e-dff20f-00002-a1": "huawei-deepseek/target-slots/slot2/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T183307Z",
}
# Script-format games (line Formato): tag -> (manual, slot); sv4 was stopped at months 8-9 and only the slot kept it.
FORMATO = {"sv1": "script-v1", "sv2": "script-v2", "sv3": "script-v3", "sv4": "script-v4"}
RAW_FOR_FORMATO = {
    "sv4-g1": "formato/slot-a/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T220541Z",
    "sv4-g2": "formato/slot-b/runner/.career_sim_runner/career_emu/outputs/Gradient Depression/20261027T220431Z",
}
FAKE = "formato/slot-fake/runner/.career_sim_runner/career_emu/outputs/gradient-depression"


def clean(text: str) -> str:
    text = SECRET.sub(lambda m: (m.group(1) or m.group(2) or "") + "<redacted>", text)
    return text.replace(HOME, "~").replace(Path.home().name, "<user>")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def put(dst: Path, text: str, gz: bool = False) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = clean(text).encode("utf-8")
    if gz:
        dst = dst.with_name(dst.name + ".gz")
        with open(dst, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as f:
            f.write(data)
    else:
        dst.write_bytes(data)
    if dst.stat().st_size > MAX_BYTES:
        raise SystemExit(f"{dst} is over 50 MB: split it")


def put_file(src: Path, dst: Path, gz_over: int = 200_000) -> None:
    if src.exists():
        put(dst, read_text(src), gz=src.stat().st_size > gz_over)


def pack_dir(src: Path, dst: Path) -> int:
    """Many small JSON files -> one jsonl.gz, one line per file: {"file": name, "data": parsed JSON or text}."""
    lines = []
    for f in sorted(src.rglob("*")):
        if not f.is_file():
            continue
        t = read_text(f)
        try:
            data = json.loads(t)
        except ValueError:
            data = t
        lines.append(json.dumps({"file": str(f.relative_to(src)), "data": data}, ensure_ascii=False))
    put(dst, "\n".join(lines) + "\n", gz=True)
    return len(lines)


def tar_dir(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dst, "w:gz", compresslevel=9) as tar:
        for f in sorted(src.rglob("*")):
            if f.is_file() and not f.name.endswith(".env"):
                data = clean(read_text(f)).encode("utf-8")
                info = tarfile.TarInfo(f"{src.name}/{f.relative_to(src)}")
                info.size, info.mtime = len(data), 0
                tar.addfile(info, io.BytesIO(data))
    if dst.stat().st_size > MAX_BYTES:
        raise SystemExit(f"{dst} is over 50 MB: split it")


# ----------------------------------------------------------------------------- games
def policy_names() -> dict[str, str]:
    db = SRC / "huawei-deepseek" / "registry.sqlite3"
    with sqlite3.connect(db) as c:
        return {pid[:8]: name for pid, name in c.execute("select policy_id, name from policies")}


def runner_of(slot: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(slot / "runner"), "rev-parse", "--short=8", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def games() -> list[dict]:
    """One dict per official game: id, manual, source files."""
    names, out = policy_names(), []
    for d in sorted((SRC / "huawei-deepseek" / "runs").glob("deepseek-pilo-*")):
        pid, n = d.name.split("-")[2], d.name.split("-")[4]
        actor = json.loads(read_text(d / "actor.json")) if (d / "actor.json").exists() else {}
        raw = SRC / RAW_FOR_RUN[d.name] if d.name in RAW_FOR_RUN else None
        out.append({
            "id": f"{names.get(pid, pid)}__{pid}-{n}", "manual": names.get(pid, pid), "line": "deepseek",
            "events": d / "events.jsonl" if (d / "events.jsonl").exists() else next(raw.glob("events-*.jsonl"), None) if raw else None,
            "transcript": d / "transcript.log" if (d / "transcript.log").exists() else next(raw.glob("transcript-*.log"), None) if raw else None,
            "score": d / "score_report.json" if (d / "score_report.json").exists() else (raw / "score_report.json" if raw and (raw / "score_report.json").exists() else None),
            "extra": [d / x for x in ("actor.json", "result.json", "dataset.log", "play.log", "jiuwen.log")],
            "runner": actor.get("runner_commit", ""), "jiuwenswarm": actor.get("jiuwenswarm", ""),
            "model": actor.get("model_name", ""), "source": f"huawei-deepseek/runs/{d.name}" + (f" + {RAW_FOR_RUN[d.name]}" if raw else ""),
        })
    for d in sorted((SRC / "formato" / "runs").iterdir()):
        raw = SRC / RAW_FOR_FORMATO[d.name] if d.name in RAW_FOR_FORMATO else d / "output"
        slot = SRC / "formato" / ("slot-a" if d.name == "sv4-g1" else "slot-b" if d.name == "sv4-g2" else "slot-a")
        out.append({
            "id": f"{FORMATO[d.name[:3]]}__{d.name}", "manual": FORMATO[d.name[:3]], "line": "formato",
            "events": next(raw.glob("events-*.jsonl"), None), "transcript": next(raw.glob("transcript-*.log"), None),
            "score": raw / "score_report.json" if (raw / "score_report.json").exists() else None,
            "extra": [d / "play.log", d / "cost.txt"], "advisor": d / "advisor-state",
            "runner": runner_of(slot), "jiuwenswarm": "0.2.4b3", "model": "deepseek-v4-flash",
            "source": f"formato/runs/{d.name}" + (f" + {RAW_FOR_FORMATO[d.name]}" if d.name in RAW_FOR_FORMATO else ""),
        })
    return out


def usage_lines(jiuwen: Path | None) -> list[tuple[str, int, int, float]]:
    """Per LLM call from the runtime log: (UTC time, input tokens, output tokens, cost)."""
    if not jiuwen or not jiuwen.exists():
        return []
    rows = []
    pat = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+).*llm_usage chunk.*?'input_tokens': (\d+), 'output_tokens': (\d+).*?'input_cost': ([\d.e-]+), 'output_cost': ([\d.e-]+)")
    for line in read_text(jiuwen).splitlines():
        m = pat.search(line)
        if m:
            rows.append((m.group(1).replace(" ", "T"), int(m.group(2)), int(m.group(3)), float(m.group(4)) + float(m.group(5))))
    return rows


HR = re.compile(r"(An HR partner[^\n]*?(?:\.|$)(?:[^\n]*?\.)?)")


def decisions(g: dict, cat_by_title: dict) -> list[dict]:
    if not g["events"]:
        return []
    usage = usage_lines(next((x for x in g["extra"] if x.name == "jiuwen.log"), None))
    obs, rows, hr = None, [], ""
    for line in open(g["events"], encoding="utf-8", errors="replace"):
        e = json.loads(line)
        p = e.get("payload", {})
        if "delta" in p:
            continue
        if e["kind"] == "tool_result" and str(p.get("tool_name", "")).endswith("observe"):
            try:
                new = json.loads(p["raw_output"]["result"])
            except (KeyError, ValueError, TypeError):
                continue
            m = HR.search(new.get("events") or "")
            if m:
                hr = " ".join(m.group(1).split())
            if rows and rows[-1].get("_after") is None:
                rows[-1]["_after"] = new.get("current_state", {}).get("status", {})
            obs = new
        elif e["kind"] == "tool_call" and p.get("tool_call", {}).get("name", "").endswith("take_action") and obs:
            a = json.loads(p["tool_call"].get("arguments") or "{}")
            ce, st = obs.get("current_event", {}), obs.get("current_state", {})
            title = ce.get("title", "")
            kind = "energia" if title.startswith("Quarterly energy") else "accion" if title.startswith("Quarterly main") else "historia"
            ch = a.get("choice")
            text = next((c.get("action", "") for c in obs.get("choices", []) if c.get("choice") == ch), "")
            nodes = cat_by_title.get((title, len(obs.get("choices", []))), []) if kind == "historia" else []
            ts = e.get("ts", "")[:23]
            call = max((u for u in usage if u[0] <= ts), default=None, key=lambda u: u[0])
            rows.append({
                "partida": g["id"], "manual": g["manual"], "mes": st.get("time", {}).get("current_month"),
                "tipo": kind, "situacion": title, "nodo_catalogo": nodes[0] if len(nodes) == 1 else "",
                "n_opciones": len(obs.get("choices", [])), "eleccion": ch, "texto_eleccion": text,
                "comentario_rrhh": hr, "nota": a.get("notes", ""),
                "fichas_entrada_llamada": call[1] if call else "", "fichas_salida_llamada": call[2] if call else "",
                "coste_llamada": round(call[3], 6) if call else "",
                "_before": st.get("status", {}), "_after": None,
            })
            obs = None
    keys = ("health", "dignity", "skill", "network", "output", "wealth")
    for r in rows:
        b, a = r.pop("_before"), r.pop("_after") or {}
        r["nivel"] = b.get("level", "")
        for k in keys:
            r[k] = b.get(k, "")
            r["d_" + k] = (a[k] - b[k]) if a and isinstance(a.get(k), (int, float)) and isinstance(b.get(k), (int, float)) else ""
        r["d_nivel"] = "" if not a else (a.get("level") != b.get("level"))
    return rows


def game_summary(g: dict, dec: list[dict]) -> dict:
    score = json.loads(read_text(g["score"])) if g["score"] else {}
    end = score.get("ending_score", {})
    dims = {d["name"]: d.get("raw_value") for d in end.get("dimensions", [])}
    tu = score.get("token_usage", {})
    usage = usage_lines(next((x for x in g["extra"] if x.name == "jiuwen.log"), None))
    play = next((x for x in g["extra"] if x.name == "play.log"), None)
    pt = read_text(play) if play and play.exists() else ""
    months = re.findall(r"Month (\d+) ·", pt)
    levels = re.findall(r"^ (L\d+) ", pt, re.M)
    if not months and dec:
        months = [str(dec[-1]["mes"])]
    cost_txt = next((x for x in g["extra"] if x.name == "cost.txt"), None)
    return {
        "partida": g["id"], "manual": g["manual"], "linea": g["line"], "modelo": g["model"],
        "runner": g["runner"], "jiuwenswarm": g["jiuwenswarm"],
        "nota": end.get("quantitative_score", ""), "completada": end.get("completed", ""),
        "meses": int(months[-1]) if months else "",
        "nivel": f"L{int(dims['level'])}" if dims.get("level") else (levels[-1] if levels else (dec[-1]["nivel"] if dec else "")),
        "explosiones": pt.count("landmines"), "skill": dims.get("skill", ""), "network": dims.get("network", ""),
        "dinero": dims.get("wealth", ""), "salud_dignidad": dims.get("resilience", ""), "riesgo": dims.get("risk_control", ""),
        "fichas_entrada": tu.get("input_tokens") or (sum(u[1] for u in usage) if usage else ""),
        "fichas_salida": tu.get("output_tokens") or (sum(u[2] for u in usage) if usage else ""),
        "coste_usd": tu.get("total_cost") if tu.get("total_cost") is not None else (round(sum(u[3] for u in usage), 4) if usage else ""),
        "coste_fuente": "score_report" if tu.get("total_cost") is not None else ("jiuwen.log" if usage else ("cost.txt" if cost_txt and cost_txt.exists() else "")),
        "fin": (score.get("termination_reason") or ("completada" if end.get("completed") else "eliminada" if end else "cortada o sin informe")),
        "decisiones": len(dec), "origen": g["source"],
    }


def copy_game(g: dict, dst: Path) -> None:
    if g["score"]:
        put(dst / "score_report.json", read_text(g["score"]))
    if g["events"]:
        put(dst / "events.jsonl", read_text(g["events"]), gz=True)
    if g["transcript"]:
        put(dst / "transcript.log", read_text(g["transcript"]), gz=True)
    for x in g["extra"]:
        put_file(x, dst / x.name)
    adv = g.get("advisor")
    if adv and adv.exists():
        for f in adv.iterdir():
            put_file(f, dst / "advisor-state" / f.name)


# ----------------------------------------------------------------------------- everything else
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    gs = games()
    if a.check:
        for g in gs:
            print(g["id"], "events" if g["events"] else "-", "score" if g["score"] else "-", g["source"])
        return
    for sub in ("partidas", "bancos", "etiquetas", "ids", "llamadas", "registros", "gpt-principios", "sustitutos", "programa", "otros"):
        shutil.rmtree(OUT / sub, ignore_errors=True)
    cat = json.loads(read_text(CATALOG))
    by_title = collections.defaultdict(list)
    for nid, nd in cat["nodes"].items():
        by_title[(nd["title"], nd["n_choices"])].append(nid)
    summaries, all_dec = [], []
    for g in gs:
        copy_game(g, OUT / "partidas" / g["id"])
        dec = decisions(g, by_title)
        all_dec += dec
        summaries.append(game_summary(g, dec))
    with open(OUT / "partidas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summaries[0]))
        w.writeheader()
        w.writerows(summaries)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(all_dec[0]))
    w.writeheader()
    w.writerows(all_dec)
    put(OUT / "decisiones.csv", buf.getvalue(), gz=True)

    ds = SRC / "deepseek"
    for arm in sorted((ds / "runs").iterdir()):
        n = pack_dir(arm, OUT / "bancos" / arm.name / "resultados.jsonl")
        print(f"bancos/{arm.name}: {n} files")
    for f in sorted((ds / "labels").glob("*.json")):
        put_file(f, OUT / "etiquetas" / f.name, gz_over=10**9)
    for v in sorted((ds / "perceive").iterdir()):
        pack_dir(v, OUT / "etiquetas" / "lecturas" / f"{v.name}.jsonl")
    for f in sorted(ds.glob("ids-*")) + [ds / "obedience-ds1.txt"]:
        put_file(f, OUT / "ids" / f.name, gz_over=10**9)
    for f in ("calls.jsonl", "calls-nim.jsonl"):
        put_file(ds / f, OUT / "llamadas" / f, gz_over=0)
    for f in sorted(ds.glob("*.log")) + sorted(ds.glob("official-*")) + sorted((ds / "games").glob("*")):
        put_file(f, OUT / "registros" / f.name, gz_over=100_000)
    for d in sorted(ds.glob("gpt-*")):
        tar_dir(d, OUT / "gpt-principios" / f"{d.name}.tar.gz")
    for d in sorted((SRC / "proxies").iterdir()):
        if d.is_dir():
            pack_dir(d, OUT / "sustitutos" / f"{d.name}.jsonl")
    for f in ("obs_seq.txt", "tools.json", "fake.log", "fake_llm.py", "peek.py"):
        put_file(SRC / "formato" / f, OUT / "programa" / f)
    for d in sorted((SRC / FAKE).iterdir()):
        for f in d.iterdir():
            put_file(f, OUT / "programa" / "modelo-falso" / d.name / f.name)
    put_file(ds / "answers.json", OUT / "otros" / "answers.json", gz_over=0)
    put_file(ds / "items-g1.jsonl", OUT / "otros" / "items-g1.jsonl", gz_over=0)
    for f in sorted((ds / "public-v11").iterdir()):
        put_file(f, OUT / "otros" / "public-v11" / f.name)
    print(f"{len(gs)} games, {len(all_dec)} decisions -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
