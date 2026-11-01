# Results panel

A single static page with the race leaderboard, how scores change over time, and the bot results. It also shows games from other machines (T11) once they are exported. Built by Leah on 26 Oct 2026, branch `leah/workspace`.

## Open it

```sh
git fetch origin                                   # race results (the closed race ended on origin/main)
uv run python scripts/panel/build.py               # writes lab/panel/data.js
python3 -m http.server 8795 --directory lab/panel  # then open http://localhost:8795
```

Opening `index.html` straight from disk also works in most browsers: the data is a plain `<script src="data.js">`, with no fetch call.

To refresh the local bot sweep, pass the folder of `harness.py` games:

```sh
uv run python scripts/panel/build.py --exploration ~/techarena-career-sim/exploration/runs
```

That summary goes to `lab/panel/data/exploration.json`, holding final scores only. The 346 MB of raw games stay out of Git.

## Follow a running game live

```sh
uv run python scripts/panel/live.py ~/careerlab-data/huawei-<origin>/runs/<job_id> "label shown on the page" &
python3 -m http.server 8795 --directory lab/panel  # then open http://localhost:8795/live.html
```

`live.py` re-reads the worker's transcript every 4 seconds and writes `lab/panel/live/game.json`. It stops by itself when the game ends. `live.html` shows:
- the month, level, review grades and the final score;
- Skill, Network, Output and Wealth after every decision, with review lines and promotion marks;
- Health and Dignity;
- the latest 12 decisions with the player's notes.

The committed `live/game.json` is the f3-lean-polish-v1 game of 27 Oct.

## What it shows

| Section | Chart | Source |
|---|---|---|
| Header | Leading manual's estimated score; tiles for AI games, completion rate, best single game, bot games | race registry, latest block decision |
| Leaderboard | Posterior mean ±1 sd per manual for any decision snapshot. Matteo's two manual runs are drawn as reference lines | `decisions.jsonl` (`block_decision` rows) |
| How the leader moved | The top-two manuals' estimates across snapshots | same |
| Evolution | Every scored AI game by finish time, coloured by model, with a best-so-far line | `evaluations.jsonl` |
| Where the points go | Average points earned out of each dimension's weight, completed games | `dims` in `evaluations.jsonl` |
| Still alive by month | Share of games still running, per model and for the race bots | `survival_months` |
| Bots | T10 energy-mix arms; Leah's 1,562-game local sweep (top 8 and baselines) | `lab/reports/energy-bots/README.md`; `data/exploration.json` |
| Other machines | One tile per origin in `lab/registry-origins/`, or the commands to produce one | T11 exports |
| All games | Sortable table of every scored game | all of the above |

The model chips and the purpose menu filter the tiles, the over-time chart, the points chart, the survival curves and the table together. The leaderboard always shows the decision as it was recorded.

Interrupted games are never scored (prereg-v1), so they don't appear. Every value is from the dev dataset with Claude standing in for DeepSeek. Treat them as development feedback, not predictions of the official score.

## What the data says (race at `b0f348f`, 26 Oct 14:07 UTC)

- **The leader is f3-feedback-reactive-v1 at 60.2 ±2.3**, ahead of f3-balance-recombined (58.9) and f3-lean (57.5).
- **About 40 points are missing in each completed game**, mostly in career level (13.8 of 30) and wealth (6.9 of 20). Health and dignity are almost full (14.8 of 15). Survival is solved; growth is not.
- **27 of the 51 eliminations happen at month 24–25**, the dismissal after two weak reviews. That is the cliff in the survival chart.
- **The strongest model scores higher, but not by much.** Completed games average 59.5 with Haiku, 61.2 with Sonnet and 62.6 with Opus.
- **The best single AI game is 73.1**: Matteo's m3-sustainable-career-v0-1 played by Sonnet. The same manual is dormant at 38 with Haiku, so it rewards a stronger reader.
- **Race bots that take the first story option never reach month 48.** In Leah's local sweep, the best quarterly plan (`q_health3_key`: Health recovery until full, then report materials, with a key project as the main action) averages 42.1 and completes 13 of 30 games.

## Files

- `scripts/panel/build.py`: reads committed results only, never the simulator; documented in its docstring.
- `lab/panel/index.html`: the page. Plain HTML, CSS and JavaScript, with no external libraries. Light and dark themes, responsive down to phone width.
- `lab/panel/data.js`: generated; commit it after rebuilding so teammates see the same snapshot.
- `lab/panel/data/exploration.json`: generated summary of the local bot sweep.

## Relevo

1. **Done.** The panel and its builder. I chose a static page over a server because anyone can open it from the repo, and the cloud can rebuild it without extra dependencies. The colours are the validated default palette: the four series pass the colourblind checks in light and dark mode. The two lighter series colours are backed by the legend, tooltips and the table view.
2. **Checked.** Rendered in the browser at desktop and phone width (375 px, no sideways scroll), light and dark. No console errors. Filters, the snapshot switcher, hover tooltips and table sorting were exercised.
3. **Limits.**
   - The race data is whatever `origin/cloud-lab-run` had when it was built (`b0f348f`).
   - The energy-bot numbers are parsed from the report's Markdown table, so a change in that table's format would hide the section.
   - The leaderboard has only three snapshots so far, all for the Haiku player.
4. **Next.**
   - After each cloud batch: `git fetch origin && uv run python scripts/panel/build.py`, then commit `lab/panel/data.js`.
   - Once Leah plays games under origin `leah` and exports them, they appear in *Other machines* and in the table.
