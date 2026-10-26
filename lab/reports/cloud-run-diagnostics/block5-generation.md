# Block 5 generation: F1 reliability children and the stall slot

Source: the 86 cloud Haiku digests (decision #142) and F1's Opus digests. A **risk remark** is a non-reassuring monthly HR remark; a **strong** one says "piled up" or worse.

## 1. Coverage

F1 completed 7 of 8 Haiku runs; its exit (month 24) has no digest, nor does f1-review-risk's. All 6 F1-family digests completed (Q 54.8–68.1), so exit routes come from near-misses, the 86-game data and F1's two Opus losses (both trust crises).

## 2. F1 against the failed children

The failed children (f7-trend-marking, f7-delivery-stories, f7-promotion-drive, f3-opus-distilled, f8, o2, l1) have 31 digests.

| | F1 (4) | Failed (31) |
|---|---|---|
| Completed | 4 | 12 (11 dismissed, 7 trust crises, 1 blackout) |
| Promoted at review 1 | 4 | 11 |
| Games with a blow-up | 3 | 22 |
| Months with a strong remark | 11% | 19% |

F1 leaves Level 1 early. Its exposure is blow-ups: 3 of 4 games had one, and a second blow-up is a trust crisis.

## 3. Where a weaker reader executes F1 wrongly

**a. Risk is read by strength, not presence.** F1 took Defuse legacy risk after 11 of 22 risk remarks (5 of 9 strong) and in 0 of the 6 phases after its 3 blow-ups, but in 16 of 42 phases after a calm remark.

**b. Defuse helps only when a signal is present** (all 86 digests):

| Remark before the phase | Blow-up within 3 months, no Defuse | With Defuse |
|---|---|---|
| Mild | 9/93 (10%) | 2/110 (2%) |
| Strong | 10/51 (20%) | 13/154 (8%) |
| Calm | 15/354 (4%) | 11/246 (4%) |

All 37 D grades came with a risk remark in the review month; 60 of 75 A grades came with a calm one. After a first blow-up, games that later had a trust crisis took Defuse in both of the next two phases in 2 of 13 cases; the others did so in 12 of 31.

**c. F1 contradicts itself.** Its late-run caution appears in 11% of notes, mostly from mid-run on. It caused all 5 of F1's Lay-low main actions, each at full Health, against F1's own Lay-low guard. The weakest F1 game (19618e77-00005: Q 57.1, C C C C, three at Level 2) took 4 of them.

**d. Most labels go unused.** Watch appears in 1% of notes, Fine in 0%, and the Output-after-a-C rule in 1%. Skill learning and High-intensity work appear in 0 of 64 phases. At 486 words, F1 exceeds the 400-word cap.

## 4. New policies: a nested ladder

Each rung changes one thing.

| Policy | Words | Change against the rung below |
|---|---:|---|
| `f1-core-v1` | 284 | F1 without its unexecuted or contradictory text (P20) |
| `f1-risk-signal-v1` | 315 | Any non-reassuring risk feedback, or a blow-up since the last phase, puts Defuse right after Act recovery |
| `f1-status-line-v1` | 326 | The same rules as a status line, then need, then option (P22) |

**f1-core-v1 (§3c, d)** drops "Across the run" with its late-run caution. Prediction: no Lay low at full Health; key-project share and completion at least the parent's.

**f1-risk-signal-v1 (§3a, b)** has a pure feedback trigger, with no review cadence (unlike R1). It has no REVIEW mode, main-action switch or story ban (unlike f1-review-risk). Prediction: Defuse after at least 80% of signals (parent 50%); fewer strong months and blow-ups; no D grade and no trust crisis.

**f1-status-line-v1 (stall slot)**, `idea_origin` "playbook:P22 (stagnation rule, decision #142)". Its parents are F1 and f3-lean, but it takes only F3's named risk state, as a slot. It leaves out F3's Escalating mode and weak-review plan, which opus~100k plays badly.

Why P22: it fits the playbook symptom "the cheap actor ignores instructions", and §3 shows rules that exist but are skipped or reordered. P20 is already rung 1. P21 would drop the balance that transfers across actors, and it resembles f7-promotion-drive (45.2). P25 needs other actors' runs, not new text.

Learning goal: does a slot line raise rule agreement for a small model at no token cost, against rung 2's prose? Transfer needs opus~100k or DeepSeek cells (P26).

## Not chosen; caveats

Not chosen: a review mode (f1-review-risk, 53.1), story-filter edits, a promotion drive, Defuse timed to reviews, and "skip Defuse when calm" (F3 games link pre-review Defuse to better grades).

Caveats: samples are small, Haiku picks the same option in an event under every policy, and the remark–grade link may be reverse causal.

## Compliance

`careerlab lint`: no findings. `lint.py` (169 digest titles): 0 errors. `pytest tests/test_compliance.py`: 97 passed. The Skills contain no numbers, months, review cadence, quoted game text or late-run wording.
