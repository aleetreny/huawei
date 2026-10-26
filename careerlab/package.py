"""Build a submission directory from a registered policy and validate it with the official runner.

The Skills and manifest are copied byte for byte from the frozen policy bundle,
so the submitted version is exactly the evaluated one (same content hash). The
design documents and the video are team-authored inputs; this tool only checks
that they exist and records what was packaged.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from careerlab.config import Settings
from careerlab.store import Registry, bundle_hash


def package(settings: Settings, reg: Registry, policy_id: str, out_dir: Path, design_dir: Path,
            video: Path | None, readme: Path | None = None) -> dict[str, Any]:
    row = reg.db.execute("SELECT * FROM policies WHERE policy_id=?", (policy_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown policy {policy_id}")
    bundle = Path(row["bundle_path"])
    if bundle_hash(bundle)[:16] != policy_id:
        raise ValueError("bundle bytes changed since registration; register a new version instead")
    solution = out_dir / "solution"
    if solution.exists():
        shutil.rmtree(solution)
    solution.mkdir(parents=True)
    shutil.copytree(bundle / "skills", solution / "skills")
    shutil.copyfile(bundle / "manifest.json", solution / "manifest.json")
    (solution / "design").mkdir()
    for name in ("skills_design.md", "decision_report.md"):
        src = design_dir / name
        if not src.exists():
            raise FileNotFoundError(f"missing team-authored {src}")
        shutil.copyfile(src, solution / "design" / name)
    if readme and readme.exists():
        shutil.copyfile(readme, solution / "README.md")
    else:
        meta = json.loads(row["meta"] or "{}")
        skills = sorted(p.parent.name for p in (solution / "skills").glob("*/SKILL.md"))
        (solution / "README.md").write_text(
            f"# Gradient Depression — {row['name']}\n\nSkills: {', '.join(skills)}.\n\n{meta.get('hypothesis', '')}\n", encoding="utf-8")
    if video and video.exists():
        shutil.copyfile(video, solution / "presentation.mp4")
    check = subprocess.run(["uv", "run", "python", "-m", "career_sim_runner", "validate", "--submission", str(solution)],
                           cwd=settings.runner_dir, capture_output=True, text=True)
    digest = hashlib.sha256()
    for path in sorted(p for p in solution.rglob("*") if p.is_file() and p.name != "presentation.mp4"):
        digest.update(str(path.relative_to(solution)).encode() + b"\0" + path.read_bytes() + b"\0")
    record = {"policy_id": policy_id, "policy": row["name"], "solution": str(solution), "content_sha256": digest.hexdigest(),
              "validator_exit": check.returncode, "validator_tail": (check.stdout + check.stderr)[-1500:],
              "video_included": (solution / "presentation.mp4").exists()}
    reg.decide("submission_candidate", policy_id, record, "packaged for a cutoff; content hash excludes the video")
    return record
