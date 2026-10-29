"""Where the DeepSeek data is: this Mac's ~/careerlab-data, or the copy in Git (lab/data/deepseek, NORMAS §1.6).

Scripts ask here instead of hard-coding ~/careerlab-data/deepseek:
- ``deepseek_dir()``: ``DEEPSEEK_DATA`` if set; else ~/careerlab-data/deepseek if it exists (Alejandro's Mac);
  else the Git copy unpacked once into ~/.cache/careerlab/deepseek with the original layout (runs/<arm>/,
  labels/, perceive/<variant>-r<rep>/, ids-*.txt, calls.jsonl, gpt-*/), so every old command works unchanged.
- ``games_dir()``: official DeepSeek games, ~/careerlab-data/huawei-deepseek/runs or lab/data/deepseek/partidas.
- ``proxies_dir()``: the free proxy labellers' answers (~/careerlab-data/proxies or its unpacked copy).
- ``open_text(path)``: opens a text file, gzip or not (the Git copy keeps large files as .gz).

    uv run python scripts/deepseek/datapaths.py materialize [--out DIR]   # unpack the Git copy
    DEEPSEEK_DATA=$(uv run python scripts/deepseek/datapaths.py where) uv run python scripts/transmision/score.py ...
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GIT = REPO / "lab" / "data" / "deepseek"
LOCAL = Path.home() / "careerlab-data"
CACHE = Path(os.environ.get("CAREERLAB_CACHE", Path.home() / ".cache" / "careerlab"))


def open_text(path: str | Path):
    p = Path(path)
    if not p.exists() and Path(str(p) + ".gz").exists():
        p = Path(str(p) + ".gz")
    return gzip.open(p, "rt", encoding="utf-8", errors="replace") if p.suffix == ".gz" else open(p, encoding="utf-8", errors="replace")


def _unpack(packed: Path, dst: Path) -> None:
    """A packed jsonl.gz (one line per original file) back to files."""
    with gzip.open(packed, "rt", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            out = dst / row["file"]
            out.parent.mkdir(parents=True, exist_ok=True)
            data = row["data"]
            out.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False), encoding="utf-8")


def materialize(out: Path | None = None, force: bool = False) -> Path:
    """Rebuild the ~/careerlab-data/deepseek layout from lab/data/deepseek."""
    out = out or CACHE / "deepseek"
    stamp = out / ".from-git"
    if stamp.exists() and not force:
        return out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for arm in sorted((GIT / "bancos").iterdir()):
        _unpack(arm / "resultados.jsonl.gz", out / "runs" / arm.name)
    for f in sorted((GIT / "etiquetas").glob("*.json")):
        (out / "labels").mkdir(exist_ok=True)
        shutil.copy(f, out / "labels" / f.name)
    for f in sorted((GIT / "etiquetas" / "lecturas").glob("*.jsonl.gz")):
        _unpack(f, out / "perceive" / f.name.removesuffix(".jsonl.gz"))
    for f in sorted((GIT / "ids").iterdir()):
        shutil.copy(f, out / f.name)
    for f in sorted((GIT / "llamadas").glob("*.gz")):
        with gzip.open(f, "rb") as src, open(out / f.name.removesuffix(".gz"), "wb") as dst:
            shutil.copyfileobj(src, dst)
    for f in sorted((GIT / "gpt-principios").glob("*.tar.gz")):
        with tarfile.open(f) as tar:
            tar.extractall(out, filter="data")
    for name in ("answers.json", "items-g1.jsonl"):
        src = GIT / "otros" / (name + ".gz")
        if src.exists():
            with gzip.open(src, "rb") as a, open(out / name, "wb") as b:
                shutil.copyfileobj(a, b)
    for f in sorted((GIT / "sustitutos").glob("*.jsonl.gz")):
        _unpack(f, out.parent / "proxies" / f.name.removesuffix(".jsonl.gz"))
    stamp.write_text("unpacked from lab/data/deepseek\n")
    return out


def deepseek_dir() -> Path:
    if os.environ.get("DEEPSEEK_DATA"):
        return Path(os.environ["DEEPSEEK_DATA"])
    if (LOCAL / "deepseek").exists():
        return LOCAL / "deepseek"
    return materialize()


def games_dir() -> Path:
    return LOCAL / "huawei-deepseek" / "runs" if (LOCAL / "huawei-deepseek" / "runs").exists() else GIT / "partidas"


def proxies_dir() -> Path:
    if (LOCAL / "proxies").exists():
        return LOCAL / "proxies"
    materialize()
    return CACHE / "proxies"


def labels(*names: str) -> list[Path]:
    return [deepseek_dir() / "labels" / n for n in names]


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("materialize")
    m.add_argument("--out", type=Path)
    sub.add_parser("where")
    a = ap.parse_args()
    if a.cmd == "materialize":
        print(materialize(a.out, force=True))
    else:
        print(deepseek_dir())


if __name__ == "__main__":
    main()
