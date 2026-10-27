"""Configurable paths and settings.

Every location can be overridden with an environment variable so the same code
runs locally or in a cloud worker. Defaults keep bulky, frequently written data
(SQLite registries, game databases, trajectories) outside the repository: the
repository lives in iCloud Drive, which is unsafe for live SQLite files.

A machine other than the cloud race sets an *origin* (``CAREERLAB_ORIGIN`` or
``careerlab origin set <name>``, stored in the untracked ``.careerlab-origin``).
Its job ids, replicate numbers, data directory and registry export then belong
to that origin only, so its results can never overwrite the race's. No origin
means the canonical registry: the cloud race and its ``lab/registry/`` export.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Engine settings written by the official participation runner (career_sim_runner/setup.py
# at RAI-Internal/techarena-career-sim@00b084a8). Development runs must use the same values
# or they measure a different environment.
OFFICIAL_ENGINE_ENV = {
    "CAREER_EMULATOR_ACTIVE_LONG_CHAIN_LIMIT": "1",
    "CAREER_EMULATOR_MONTHLY_EVENT_LIMIT": "3",
    "CAREER_EMULATOR_MAX_NOTE_LENGTH": "1000",
}


ORIGIN_FILE = REPO_ROOT / ".careerlab-origin"
ORIGIN_RE = re.compile(r"^[a-z][a-z0-9]{1,15}$")


def check_origin(origin: str) -> str:
    """'' is the canonical registry; anything else is a short lower-case machine name such as 'leah'."""
    if origin and not ORIGIN_RE.match(origin):
        raise ValueError(f"origin {origin!r} must be 2-16 lower-case letters or digits, starting with a letter")
    return origin


def current_origin() -> str:
    value = os.environ.get("CAREERLAB_ORIGIN")
    if value is None and ORIGIN_FILE.exists():
        value = ORIGIN_FILE.read_text()
    return check_origin((value or "").strip())


def _default_data_dir() -> Path:
    origin = current_origin()
    return _env_path("CAREERLAB_DATA", Path.home() / "careerlab-data" / (f"huawei-{origin}" if origin else "huawei"))


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    return Path(value).expanduser().resolve() if value else default


@dataclass(frozen=True)
class Settings:
    """Resolved laboratory settings."""

    repo_root: Path = REPO_ROOT
    origin: str = field(default_factory=current_origin)
    data_dir: Path = field(default_factory=_default_data_dir)
    lab_dir: Path = field(default_factory=lambda: _env_path("CAREERLAB_LAB_DIR", REPO_ROOT / "lab"))
    runner_dir: Path = field(default_factory=lambda: _env_path("CAREERLAB_RUNNER_DIR", REPO_ROOT / "local-runs" / "official-runner"))
    mcp_executable: str = field(default_factory=lambda: os.environ.get("CAREERLAB_MCP_EXE", "") or _default_mcp_exe())
    claude_executable: str = field(default_factory=lambda: os.environ.get("CAREERLAB_CLAUDE_EXE", "") or (shutil.which("claude") or "claude"))

    @property
    def registry_path(self) -> Path:
        return self.data_dir / "registry.sqlite3"

    @property
    def registry_export_dir(self) -> Path:
        """Canonical export for the race; one folder per other origin, merged only by the organiser."""
        return self.lab_dir / "registry" if not self.origin else self.lab_dir / "registry-origins" / self.origin

    def registry(self):  # -> careerlab.store.Registry (imported here to avoid a cycle)
        from careerlab.store import Registry

        return Registry(self.registry_path, origin=self.origin)

    @property
    def runs_dir(self) -> Path:
        return self.data_dir / "runs"

    @property
    def servers_dir(self) -> Path:
        return self.data_dir / "servers"

    @property
    def policies_dir(self) -> Path:
        return self.lab_dir / "policies"

    def ensure(self) -> "Settings":
        for path in (self.data_dir, self.runs_dir, self.servers_dir, self.lab_dir, self.policies_dir):
            path.mkdir(parents=True, exist_ok=True)
        return self


def _default_mcp_exe() -> str:
    candidate = Path(sys.executable).parent / ("career-emulator-engine-mcp.exe" if os.name == "nt" else "career-emulator-engine-mcp")
    return str(candidate) if candidate.exists() else (shutil.which("career-emulator-engine-mcp") or "career-emulator-engine-mcp")


def load_settings() -> Settings:
    return Settings().ensure()
