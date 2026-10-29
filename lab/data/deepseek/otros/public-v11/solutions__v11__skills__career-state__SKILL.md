---
name: career-state
description: A script that reads the game's own log and prints the exact state, what this pick is worth (MODE) and what the last pick cost; on quarter screens it prints the exact Energy and main action. Run it before every take_action.
---

# Career State

Run it before every take_action, as one bash call:

`python3 <skill_directory>/script/career.py brief --stats "m<month> L<level> H<health> D<dignity> S<skill> N<network> O<output> W<wealth> E<energy>" --log "<log_file>"`

- Use `brief` for story events and `quarter` for the Quarterly energy allocation and Quarterly main action screens.
- `<skill_directory>` is this skill's directory. `<log_file>` comes from check_latest_logs, called once right after new_game.
- Copy the numbers from the observe you just made, e.g. `--stats "m5 L1 H8 D10 S9 N3 O3 W2 E0"`.

## What it prints
- Line 1: month, level, each promotion stat against this level's limit once the limit is known (e.g. Output 2/3), Health, Dignity and the HR risk line.
- MODE: N normal, G guard, R recover or D danger, with one sentence on what this pick is worth.
- LAST PICK: what your previous pick cost, when it lowered Output or Network.
- REVIEW: once after each half-year review, what decided it.
- On quarter screens: ENERGY (choose now 'X' then ...) and MAIN ACTION. Follow them exactly, one action per take_action, and run it again after each.

If it prints CAREER ERROR or nothing, use the fallback rules in zeng-guofan.
