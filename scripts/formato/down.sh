#!/bin/bash
S=$1; cd "$S/runner"; export HOME="$S/home"
uv run jiuwenswarm-start --stop career_emu < /dev/null > /dev/null 2>&1 || uv run jiuwenswarm-stop career_emu < /dev/null >/dev/null 2>&1
pkill -f "$S/runner/.venv" 2>/dev/null; true
