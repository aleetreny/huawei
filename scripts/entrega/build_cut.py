"""Build and check one submission ZIP (solution/ with manifest, README, video, design/ and skills/).

The Skills and the manifest are copied byte for byte from the policy bundle, so the ZIP holds exactly what was
tested. Before zipping it runs the checks that make a version invalid or wasted (docs/entrega/README.md):
- `careerlab lint` on the policy (no errors);
- the official validator (`python -m career_sim_runner validate`; it does not contact JiuwenSwarm);
- every deliverable in English: no CJK, Cyrillic or Spanish-only characters, no `TODO` markers left;
- the design documents name every submitted Skill and the policy, and quote no catalogue event title;
- the video exists, is not empty and lasts at most ten minutes (ffprobe or macOS mdls);
- the content (all files but the video) is not identical to an earlier package, which would not be scored again.

    uv run python scripts/entrega/build_cut.py --policy lab/policies-src/<family>/<name> --cut cut2 \
        --design docs/entrega/cut2-<name> --video <presentation.mp4> [--readme <README.md>] [--out DIR]

Writes <out>/<cut>/solution/, <out>/<cut>/gradient-depression-<name>-<cut>.zip and <out>/<cut>/package.json.
Default out: ~/careerlab-data/entrega. Exit 0 only when every check passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNNER = Path.home() / "huawei" / "local-runs" / "official-runner"
CATALOG = REPO / "lab" / "data" / "ingenieria-inversa" / "catalog_v2.json"
NON_ENGLISH = re.compile(r"[Ѐ-ӿ぀-ヿ㐀-鿿가-힯¿¡ñÑ]")


def content_hash(solution: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in solution.rglob("*") if x.is_file() and x.name != "presentation.mp4"):
        h.update(str(p.relative_to(solution)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def video_seconds(video: Path) -> float | None:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                             capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        pass
    try:  # macOS without ffprobe: Spotlight metadata
        out = subprocess.run(["mdls", "-raw", "-name", "kMDItemDurationSeconds", str(video)],
                             capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", required=True, type=Path, help="lab/policies-src/<family>/<name> (with bundle/)")
    ap.add_argument("--cut", required=True)
    ap.add_argument("--design", required=True, type=Path, help="folder with skills_design.md and decision_report.md")
    ap.add_argument("--video", type=Path)
    ap.add_argument("--readme", type=Path, help="default: README.md in the design folder")
    ap.add_argument("--out", type=Path, default=Path.home() / "careerlab-data" / "entrega")
    a = ap.parse_args()
    bundle, name = a.policy / "bundle", a.policy.name
    out = a.out / a.cut
    solution = out / "solution"
    problems: list[str] = []

    lint = subprocess.run(["uv", "run", "careerlab", "lint", str(a.policy)], cwd=REPO, capture_output=True, text=True)
    if lint.returncode != 0 or re.search(r"^ERROR", lint.stdout, re.M):
        problems.append("careerlab lint reports errors:\n" + lint.stdout[-1500:])

    if solution.exists():
        shutil.rmtree(solution)
    solution.mkdir(parents=True)
    shutil.copytree(bundle / "skills", solution / "skills")
    shutil.copyfile(bundle / "manifest.json", solution / "manifest.json")
    (solution / "design").mkdir()
    for doc in ("skills_design.md", "decision_report.md"):
        if not (a.design / doc).exists():
            problems.append(f"missing {a.design / doc}")
        else:
            shutil.copyfile(a.design / doc, solution / "design" / doc)
    readme = a.readme or a.design / "README.md"
    if readme.exists():
        shutil.copyfile(readme, solution / "README.md")
    else:
        problems.append(f"missing README ({readme})")
    if a.video and a.video.exists() and a.video.stat().st_size > 0:
        shutil.copyfile(a.video, solution / "presentation.mp4")
        secs = video_seconds(a.video)
        if secs is not None and secs > 600:
            problems.append(f"video lasts {secs / 60:.1f} min (maximum 10)")
    else:
        problems.append("no presentation.mp4 (required in every final ZIP)")

    manifest = json.loads((solution / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("mode") != "agent":
        problems.append(f"manifest mode is {manifest.get('mode')!r}, must be 'agent'")
    if not manifest.get("team") or "your team" in str(manifest.get("team")).lower():
        problems.append("manifest team name is blank or a placeholder")

    texts = {str(p.relative_to(solution)): p.read_text(encoding="utf-8", errors="replace")
             for p in solution.rglob("*") if p.is_file() and p.suffix in (".md", ".json")}
    for path, t in texts.items():
        if NON_ENGLISH.search(t):
            problems.append(f"{path}: non-English characters ({NON_ENGLISH.search(t).group(0)!r})")
        if re.search(r"\bTODO\b", t):
            problems.append(f"{path}: TODO marker left")
    skills = sorted(p.parent.name for p in (solution / "skills").glob("*/SKILL.md"))
    design = "\n".join(t for p, t in texts.items() if p.startswith("design/"))
    for s in skills:
        if s not in design:
            problems.append(f"design documents never name the submitted Skill {s!r}")
    if name not in design:
        problems.append(f"design documents never name the submitted version {name!r}")
    titles = {n["title"] for n in json.loads(CATALOG.read_text())["nodes"].values() if len(n["title"]) > 25}
    for path, t in texts.items():
        hit = next((x for x in titles if x in t), None)
        if hit:
            problems.append(f"{path}: quotes an event title ({hit[:40]}…)")

    check = subprocess.run(["uv", "run", "python", "-m", "career_sim_runner", "validate", "--submission", str(solution)],
                           cwd=RUNNER, capture_output=True, text=True)
    if check.returncode != 0:
        problems.append("official validator failed:\n" + (check.stdout + check.stderr)[-1500:])

    digest = content_hash(solution)
    for old in sorted(a.out.glob("*/package.json")):
        prev = json.loads(old.read_text())
        if prev.get("content_sha256") == digest and old.parent != out:
            problems.append(f"content identical to {old.parent.name} ({prev.get('policy')}): it would not be scored again")
    for old in sorted(a.out.glob("*/solution")):
        if old != solution and content_hash(old) == digest:
            problems.append(f"content identical to {old.parent.name}/solution: it would not be scored again")

    zip_path = out / f"gradient-depression-{name}-{a.cut}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(solution.rglob("*")):
            z.write(p, Path("solution") / p.relative_to(solution))
    record = {"policy": name, "policy_dir": str(a.policy), "cut": a.cut, "content_sha256": digest,
              "skills": skills, "video": str(a.video) if a.video else None, "zip": str(zip_path),
              "zip_bytes": zip_path.stat().st_size, "validator_exit": check.returncode,
              "validator_tail": (check.stdout + check.stderr)[-800:], "problems": problems}
    (out / "package.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "validator_tail"}, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
