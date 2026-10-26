#!/bin/sh
# Install the official participation runner at the commit CareerLab was built against.
# The runner pins JiuwenSwarm 0.2.4b3; never install another JiuwenSwarm version.
# Usage: sh scripts/setup_official_runner.sh   (honours CAREERLAB_RUNNER_DIR)
set -eu
REPO_URL="https://github.com/RAI-Internal/techarena-career-sim.git"
COMMIT="00b084a8"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${CAREERLAB_RUNNER_DIR:-$ROOT/local-runs/official-runner}"
if [ ! -d "$DEST/.git" ]; then
  git clone --quiet "$REPO_URL" "$DEST"
fi
git -C "$DEST" fetch --quiet origin
git -C "$DEST" checkout --quiet "$COMMIT"
(cd "$DEST" && uv sync --frozen)
echo "official runner ready at $DEST ($(git -C "$DEST" rev-parse --short HEAD))"
echo "next: cp $DEST/.env.example $DEST/.env, fill API_BASE/API_KEY/MODEL_NAME from the organiser email, then make setup"
