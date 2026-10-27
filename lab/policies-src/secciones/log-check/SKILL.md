---
name: log-check
description: Uses check_latest_logs to see the exact effect each answer had, to spot capped stats and to learn which kinds of answers cost Network or Output in this run. Use after story choices in the months before a review, and whenever a stat moved unexpectedly.
---

# Read the log, learn the run

`check_latest_logs` lists each recent choice with the stat change it announced, before caps. The same kind of answer tends to have the same kind of effect all run, so the log teaches you what each kind of answer costs.

## When to read it
- After each story choice while a review is one or two months away, call `check_latest_logs` with a small count (about 3).
- After any choice that left a stat lower than you expected.

## What to take from it
- **Cap.** If the log announced a gain but the stat did not rise, that stat is at its cap for this level. Stop spending answers or Energy on it and keep it from falling.
- **Cost pattern.** If an answer cost Network or Output, note in a few words what kind of answer it was (for example: challenged someone in public, took on side work, went over someone's head). Until the review, avoid answers of that kind when an honest alternative exists.
- **Repair.** If a point was lost, the next answers should win it back: Network by helping and collaborating, Output by delivering your own work.

Keep a short running summary of these lessons in your notes, for example `caps: N,O | avoid: public challenge, side work`.
