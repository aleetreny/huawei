"""Configurable paths and settings.

Every location can be overridden with an environment variable so the same code
runs locally or in a cloud worker. Defaults keep bulky, frequently written data
(SQLite registries, game databases, trajectories) outside the repository: the
repository lives in iCloud Drive, which is unsafe for live SQLite files.
"""

from __future__ import annotations

import os
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


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    return Path(value).expanduser().resolve() if value else default


@dataclass(frozen=True)
class Settings:
    """Resolved laboratory settings."""

    repo_root: Path = REPO_ROOT
    data_dir: Path = field(default_factory=lambda: _env_path("CAREERLAB_DATA", Path.home() / "careerlab-data" / "huawei"))
    lab_dir: Path = field(default_factory=lambda: _env_path("CAREERLAB_LAB_DIR", REPO_ROOT / "lab"))
    runner_dir: Path = field(default_factory=lambda: _env_path("CAREERLAB_RUNNER_DIR", REPO_ROOT / "local-runs" / "official-runner"))
    mcp_executable: str = field(default_factory=lambda: os.environ.get("CAREERLAB_MCP_EXE", "") or _default_mcp_exe())
    claude_executable: str = field(default_factory=lambda: os.environ.get("CAREERLAB_CLAUDE_EXE", "") or (shutil.which("claude") or "claude"))

    @property
    def registry_path(self) -> Path:
        return self.data_dir / "registry.sqlite3"

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
