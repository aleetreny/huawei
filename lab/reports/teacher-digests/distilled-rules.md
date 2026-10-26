# Opus teacher distillation: rules for F3 children

Source: the 14 Opus digests in `opus/` (8 completed = W, 6 eliminated = L; policies F1, P0, M3; never F3). Energy and main-action tallies cover months 1–24 (a window every game reaches); review-level tests use every review.

**Caveat.** Opus's wins mix its own capability with the policy it played. What we test is whether a rule written for a weaker reader helps Haiku now and DeepSeek (the target model) later.

## Per-game tallies

Quarters with PR (Prepare report materials), NW/BM (Network maintenance or Build a mentorship) and DF (Defuse legacy risk); KP×2 = Apply for a key project in both quarters after the first C; pre-DF = reviews after a C/D preceded by Defuse in the last Energy phase; D-noDF = Ds after a C/D without it.

| game | pol | actor | out | grades ≤M30 | PR | NW/BM | DF | KP×2 | pre-DF | D-noDF |
|---|---|---|---|---|---|---|---|---|---|---|
| 19618e77-eaaedd-00000 | F1 | opus~100k | W | CBBBB | 6/8 | 2/8 | 4/8 | yes | 0 | 0 |
| 19618e77-eaaedd-00001 | F1 | opus~100k | W | CBBBB | 6/8 | 2/8 | 4/8 | yes | 0 | 0 |
| ed78f44c-eaaedd-00001 | P0 | opus~100k | W | CCBBB | 8/8 | 2/8 | 3/8 | yes | 2 | 0 |
| ed78f44c-a10402-00000 | P0 | opus | W | CCBBB | 6/8 | 2/8 | 1/8 | yes | 1 | 0 |
| ed78f44c-eaaedd-00000 | P0 | opus~100k | W | CBBBB | 7/8 | 3/8 | 1/8 | yes | 0 | 0 |
| 3207e8f5-eaaedd-00001 | M3 | opus~100k | W | CCCCB | 7/8 | 5/8 | 3/8 | yes | 2 | 0 |
| 19618e77-d92292-00000 | F1 | opus | W | CCBBB | 8/8 | 3/8 | 2/8 | yes | 1 | 0 |
| 3207e8f5-a10402-00000 | M3 | opus | W | CCDBB | 6/8 | 5/8 | 2/8 | no | 0 | 1 |
| 19618e77-a10402-00000 | F1 | opus | L trust | CBBB | 3/7 | 3/7 | 5/7 | no | 1 | 0 |
| 19618e77-a10402-00001 | F1 | opus | L trust | CCBB | 6/8 | 4/8 | 3/8 | no | 0 | 0 |
| 3207e8f5-a10402-00001 | M3 | opus | L trust | CBB | 4/6 | 2/6 | 3/6 | no | 0 | 0 |
| ed78f44c-d92292-00000 | P0 | opus | L capab. | CCDD | 4/7 | 5/7 | 2/7 | no | 0 | 2 |
| 3207e8f5-d92292-00000 | M3 | opus | L capab. | CCDD | 4/7 | 5/7 | 2/7 | yes | 0 | 2 |
| 3207e8f5-eaaedd-00000 | M3 | opus~100k | L capab. | CCDD | 6/7 | 6/7 | 1/7 | no | 0 | 2 |

Pooled quarter shares, W vs L: PR 84% vs 64%; NW/BM 38% vs 60%; DF 31% vs 38%; Health recovery 38% vs 48%.

## Findings (months 1–30)

**Recovery from the first C.** All 14 games opened with C. The second review was B in 3/8 W and 2/6 L: no difference at that step. Apply for a key project stayed the main action in both following quarters in 7/8 W vs 1/6 L; losers switched to Build a mentorship ("network weakest"), Report results or Lay low. Prepare report materials in both quarters: 5/8 W, 3/6 L. Story style did not change.

**Energy.** Winners kept one point for Prepare report materials almost every quarter, alongside recovery or Defuse (Defuse+PR, Health+PR+PR). Losers filled the 1-point slots with Network maintenance or Health recovery more often. Unused Energy was rare in both.

**Risk and HR warnings.** The monthly HR remark is a visible five-step gauge: "doing all right", "some risk", "risks have piled up", "you're on your own now", "what were you waiting for? … about to go off". Opus defused in the first Energy phase after "piled up" or worse in 14/18 W vs 11/15 L phases (top two steps: 5/9 vs 7/10), and almost never after a reassuring quarter (0/23 vs 1/16). Lay low was similarly rare in both. **The response to warnings does not separate the groups; its timing relative to reviews does (R1).**

**Story style.** Option [1] (usually the bounded, honest or private one) was taken in 81% of W and 82% of L story decisions; keyword tallies of chosen vs declined options (public, secretive, blaming, honest, bounded, private) agree within 2 points. Teacher-wide, not a winner trait: no rule (the lean's "disclose, fix or close" line covers it).

**Before C C D D** (3 L). (a) Still L1 at the first D, while all 5 W with C C were L2 by their second review. (b) Network-chasing in 71–86% of quarters, the top three of all games. (c) No Defuse in the last Energy phase before any of their six Ds (R1). (d) The HR remark reached "on your own" or "angry" within the half-year before every D (7/7 to month 30); D comments cite "recent incidents… work got dropped", "slips, friction" or "warning signs on risk". In 3/7 it was mild at the last Energy phase and spiked afterwards.

**Before trust crises** (3 L, all seed group a10402, actor opus; risk_control 0). Two had a visible blow-up ("Old landmines all go off at once") 1–2 months earlier; in both the next HR remark was reassuring, then "angry", and Opus had just taken a formal escalation in a story (named letter, formal investigation). Of 3 W surviving a blow-up, 2 took Lay low next and 1 escalated openly. The third crisis has no visible first blow-up.

## Distilled rules

**R1, pre-review Defuse after a weak review (strongest).**
(a) The latest review was C or D, and this is the second Energy phase since that review, the last before the next one.
(b) Take Defuse legacy risk + Prepare report materials, whatever the signal state.
(c) Next review after a C/D: D in 0/7 cases with this Defuse vs 7/22 without. At a third review after C C, 4/4 that defused avoided D (W: ed78f44c-eaaedd-00001, ed78f44c-a10402-00000, 3207e8f5-eaaedd-00001, 19618e77-d92292-00000) and 4/4 that did not got D (W 3207e8f5-a10402-00000; the three capability L), within every seed group and within P0 and M3 (F1 has no case without it). D after a weak review without it: 1/8 W, 3/6 L. Defuse in the *first* phase after the weak review does not protect (6/12 still D).
(d) Refuted if Haiku executes it and a D still follows a C/D, or the D rate after weak reviews is not below f3-lean's.

**R2, results every quarter.**
(a) Any Energy phase.
(b) At least one point goes to Prepare report materials.
(c) PR in ≥3 of 4 quarters: 8/8 W, 2/6 L (exceptions 19618e77-a10402-00001, 3207e8f5-eaaedd-00000). PR alone in the pre-review phase did not prevent D (6/18); the contrast may partly reflect losers' forced recovery spending.
(d) Refuted if Haiku's PR share rises over f3-lean's but reviews after the opening C are not better.

**R3, judge statistics by trend, not size.**
(a) Choosing what to lift in a quarterly phase.
(b) Lift a statistic that is falling or named in feedback. Network maintenance and Build a mentorship are used only when Network falls or feedback names relationships.
(c) NW/BM in ≥2/3 of quarters: 0/8 W, 3/6 L, exactly the C C D D games, whose notes say "Network is the weakest" although Network runs on a smaller scale than Skill. Contradicts f3-lean's "lift the weakest statistic".
(d) Refuted if relationship feedback or Network warnings rise and score falls vs f3-lean.

**R4, keep the key project through weak reviews.**
(a) Any quarterly main action, including after a C or D (Lay low still applies when Escalating outside a weak review plan).
(b) Apply for a key project; Repair a key relationship only if the feedback names relationships.
(c) Key project in both quarters after the first C: 7/8 W, 1/6 L. Weak outcome link: next review after a C/D was D in 2/12 all-key-project half-years vs 2/8 with Report results or mentorship; the eliminated Sonnet F3 run got a D after switching to Build a mentorship. Contradicts f3-lean's factor mapping.
(d) Refuted if grades after a C are worse than f3-lean's.

**R5, a blow-up means Escalating.**
(a) Buried problems blow up, or HR says they are about to go off.
(b) Escalating at once; a reassuring remark does not shorten the quiet quarter; no formal complaints or open escalations in stories.
(c) Formal escalation within two months of a visible blow-up: 2/2 L (19618e77-a10402-00001, 3207e8f5-a10402-00001, both then blew up again) vs 1/3 W (19618e77-d92292-00000). Thin (n=5).
(d) Refuted if trust-crisis exits or risk_control do not improve vs f3-lean, or if Haiku never meets a blow-up (then uninformative).

## Strongest rule: R1

R1 has the most consistent outcome-linked contrast (0/7 vs 7/22; 4/4 vs 4/4 at the decisive third review, in every seed group) and a visible mechanism: D reviews cite incidents and risk, and the HR gauge rose between the last Energy phase and the review. It targets the most common Opus exit (3/6 losses; also the eliminated Sonnet F3 run), and a weaker model can execute it: one fixed Energy choice on a published cadence. R2's game split is larger (8/8 vs 2/6) but threshold-dependent with no review-level outcome link; R4's (7/8 vs 1/6) is likely partly reverse-causal. Screen risk: Haiku under F3 already defused 11–18 times per run, so R1 may be saturated for Haiku; the policy treats that as uninformative, not a refutation.

## Confounds

- **Actor = seed group.** Every eaaedd game is opus~100k (5/6 won); a10402 (2/5) and d92292 (1/3) are opus.
- **Policy.** M3 games chase Network more (R3). In P0 games Opus sometimes sent a main-action number to the open Energy menu, losing 3–8 recorded main actions in two winners (intent taken from notes).
- **Small n.** 8 vs 6 games, 7 relevant Ds, 5 visible blow-ups.
- **Reactive behaviour.** Losers had lower Health and higher risk, so part of their Energy was forced.

## Children

Nested f3-lean ⊂ `f3-distilled-prereview-defuse-v1` (lean + R1, 278 words) ⊂ `f3-opus-distilled-v1` (lean + R1–R5, 340 words), both in `lab/policies-src/f3-feedback-reactive/`; the R1 line is identical in both.

## Compliance review point (orchestrator, before any submission use)

R1 is triggered by visible feedback (a C or D). Its timing, however, is "the second Energy phase after it, the last before the next review", which is anchored to the published review cadence. The linter accepts it, and no month or unpublished number appears. Prereg-v1 §10 keeps calendar-triggered variants as diagnostic arms only, so the team should decide whether this cadence-relative timing counts as one before a policy containing R1 is submitted. If the team decides it does, R1's screen result is diagnostic, and a submittable version would need a state- or feedback-based condition instead.
