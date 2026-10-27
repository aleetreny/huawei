"""Build a policy folder from a base policy plus extra skill modules (T18 lab by period).

    uv run python scripts/secciones/compose.py --base <policy dir> --module review-clock [--module ...] \
        --name <name> --hypothesis "..." --predicted "..." --refutation "..."

Modules live in lab/policies-src/secciones/<module>/SKILL.md and become extra skills of the bundle.
The result goes to lab/policies-src/secciones/<name>/ (policy.json + bundle/).
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES = ROOT / "lab" / "policies-src" / "secciones"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--module", action="append", default=[])
    ap.add_argument("--name", required=True)
    ap.add_argument("--hypothesis", required=True)
    ap.add_argument("--predicted", required=True)
    ap.add_argument("--refutation", required=True)
    ap.add_argument("--change", default="")
    a = ap.parse_args()
    base = Path(a.base)
    base_meta = json.loads((base / "policy.json").read_text())
    out = MODULES / a.name
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(base / "bundle", out / "bundle")
    for m in a.module:
        dst = out / "bundle" / "skills" / m
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(MODULES / m / "SKILL.md", dst / "SKILL.md")
    manifest = json.loads((out / "bundle" / "manifest.json").read_text())
    manifest["name"] = a.name
    (out / "bundle" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    meta = {"family": "secciones", "name": a.name, "parents": [base_meta["name"]], "idea_origin": "T18 lab by period",
            "operator": "add module(s): " + ", ".join(a.module) if a.module else "copy",
            "hypothesis": a.hypothesis, "change": a.change or f"{base_meta['name']} plus skill module(s) {', '.join(a.module)}",
            "predicted_behaviour": a.predicted, "refutation": a.refutation, "skill_count": len(list((out / 'bundle' / 'skills').glob('*/SKILL.md')))}
    (out / "policy.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(out)


if __name__ == "__main__":
    main()
