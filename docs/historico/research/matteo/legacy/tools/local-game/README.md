# Career Lab: local manual game

A browser interface for exploring the official TechArena Career Survival simulator. Read events, choose actions, track statistics, consult the employee handbook and review recent logs. Optional reasoning notes are recorded through the official action tool.

This is a team development tool, separate from the competition submission. It uses only the five official MCP tools and does not inspect engine internals or packaged datasets. No AI model or API key is used, so manual play consumes no competition API credit. Game text stays in its original English.

## Setup

Run from the repository root. Python 3.13 was used for verification.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tools/local-game/requirements.txt
career-emulator-engine update --source distribution --split dev
python tools/local-game/server.py
```

Open http://127.0.0.1:8765 in your browser. Click **Start your career** and choose an option. Use **Handbook** and **Activity log** to inspect public information and feedback. Stop the server with Ctrl+C.

On Windows, create the environment with `py -3.13 -m venv .venv` and activate it using `.venv\Scripts\Activate.ps1` in PowerShell; the remaining commands are the same.

The server binds only to the local computer. Leave its terminal running while playing. If port 8765 is already in use, stop the earlier instance first.

## Sessions and data

The browser stores the current session identifier in localStorage and resumes it after a page reload. The simulator manages the actual game state. Resume requires the same browser origin and the same simulator environment. **New game** switches the browser to a fresh session after confirmation; it does not delete earlier simulator sessions.

Simulator state and logs are managed by the installed engine and must not be committed. Do not copy the virtual environment, packaged datasets, API keys or game artifacts into this repository. Session identifiers are local to each developer's setup.

## Competition agent

This manual interface does not run JiuwenSwarm. For agent development and evaluation, follow the official participation repository and its exact JiuwenSwarm `0.2.4b3` dependency pin in single-agent mode. Do not treat this standalone environment as the agent evaluation setup.

## Verification

Verified locally: creating a session, loading statistics and choices, submitting the introductory Continue choice, opening the employee handbook and reading recent logs. A full 48-month playthrough has not been verified through this interface.
