---
name: career-play
description: Plays one complete Career Survival game from its start to its ending. Use for every observe and take_action decision in the run.
---

# Career play

Play the whole 48-month game carefully, one decision at a time, using only information this run has returned.

1. Call `observe` and read the current state, the event, every listed choice and any feedback text.
2. Choose the option you judge best for this career, then call `take_action` with its `choice` number and a short note giving your reason.
3. In a quarterly phase, an option whose `energy_cost` exceeds `remaining_energy` is rejected; choose an affordable option, or the listed option that ends the phase.
4. If `take_action` reports `success` as false, observe again before choosing.
5. Repeat until the observation contains `ending_score`. Never start a second game.
