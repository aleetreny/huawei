# Lessons for manual designers

Read this before writing any manual for the fast race. It says what is proven (keep it), what is promising, what already failed, and where points are still lost. The organiser adds one line per finished challenger after every new champion, and at least every three hours (scripts/fastloop/README.md). First written 26 Oct 2026, ~19:30 UTC, from the Claude-proxy evidence (Haiku unless marked); every claim carries its source.

**In one breath.** Keep G1–G5 below (risk cleanup on every risk signal, preventive Health recovery, an explicit weak-review plan, leaving the first level through visible Output, honest ownership in stories). The game is noisy: four games prove nothing (observed-growth-v3 went from 71.4 to 51.0 when four more were played). The open problems are the first promotion, which no manual controls reliably yet, and career level and wealth beyond the fifth level, which no LLM game has reached.

Notation: g = games; x/y = completed of played; Q = mean quantitative score. "Small n" means 4 or fewer. Source keys are at the end.

**Read first.**
- **Noise.** Within-policy SD of Y is about 16. Detecting a 4-point gain needs about 147 g per arm, so a 4-g screen only explores [DIAG].
- observed-growth-v3 fell from 4/4 (Q 71.4) to 5/8 (Q 51.0) once 4 fresh replicates came in (1/4, Q 30.7) [MG5].
- The top Haiku posteriors now cluster at 50–52 (decision #150) [CRS+].
- **Actors.** Haiku rankings do not carry over to opus~100k: Spearman 0.20; the F3 family went 2/6 against 4/4 for F1/P0 [FIND]. DeepSeek is untested. v3's race-actor screen is still running [CRS+].

## 1. Guardrails: keep in every manual

Seven race manuals completed at least two-thirds of 5 or more g: F1, F3, f3-lean, f3-balance-recombined, f1-review-risk, f2-convert-on-review and F7-three-skills. All seven contain G1, G2, G3 and G5, and so does v3 [policy texts; REG].

**G1. Defuse legacy risk after any risk signal, all career long.**
- Matteo's family (small n): v2 cut Defuse to 0–1 per career and got 2/4 trust crises. v3 Defused on any risk mention (13–15 per career) and had 0 in 8 g. v5, with the same rule, had 1/4 [MG2; MG3; MG5].
- Race, Haiku (observational): manuals with no Defuse rule (P0, p0-review-guard, f2-invest-early, value-conversion, M3) played 26 g, completed 6, and 13 ended with risk control at 0 (a trust-crisis proxy). Manuals with the rule: 151 g, 85 completed, 20 [REG].
- p0-review-guard got past month 24 in 3/3 g, then lost all three that way [REG].
- After a mild risk remark, Defuse cut blow-ups within 3 months from 10 % to 2 %. After a strong remark, from 20 % to 8 %. After a calm remark, no change (4 %). All 37 D grades came with a risk remark [B5].
- Keep it up to the end: 4 g reached month 48 and still ended at risk control 0 [REG]. Trigger it on signals, not the calendar: Leah's every-quarter Defuse never left L1 (n = 1) [LEAH].

**G2. Recover Health preventively.**
- Bots: every Energy mix without a Health point each quarter blacked out (40/40). The arm that recovered only when Health was low blacked out 36/40. The bots always take the first story option, a lab device [EB].
- observed-growth-v2 recovered "only on concrete need": 2/4 race g blacked out at month 9 [REG].
- A "lower half of the range" trigger was still too late with growth play. v4 blacked out from mid-range Health; one v3 replicate blacked out at month 12 [MG4; MG5].
- Do not over-recover. v1's losses spent Energy on Health that was already high [MG2]. Completed g lose only 0.4 of 15 resilience points [REG].

**G3. Have an explicit weak-review response.** After a C or D, or "falls short" feedback, until the next review: aim the main action at the named weakness, add visible Output, keep G1 and G2, and do not Lay low. Every observed first review was a C [DR; B3].
- f2-invest-early went 0/5 (Q 22.7). Adding a switch to visible delivery on the first weak review, plus risk states, gave 5/7 (Q 51.4) [REG].
- f3-opus-distilled replaced f3-lean's plan with "keep the key project": 2/4 (Q 38.4), both losses were month-24 dismissals. f3-lean itself went 5/5 (Q 56.7) [REG; CRS].
- 48 of 86 race-Haiku eliminations happened at month 24 [REG]. Each dismissal there followed four weak reviews in a row [CRS].
- F1's late-run caution caused 5 Lay-low actions, all at full Health; its weakest game took 4 of them [B5].
- Extra modes did not help: f1-review-risk went 5/7 (Q 48.3) against F1's 10/12 (Q 56.1) [REG].

**G4. Leave L1 through visible Output.**
- First promotion at review 1: Q 57.3, 12/14 completed. At review 2: Q 47.0, 7/11. Later: Q 22.0, 0/13. No game still at L1 got a B after its first review (0/47) [B3].
- Games still at L1 at month 12 completed 2/14, against 26/38 for promoted games. This is not causal [DEC].
- Output was at its run high at review 1 in 14/14 promoted g, against 12/24 of the others [B3].
- Skill stops rising within a level (9/9 of Matteo's episodes, 5/5 of Leah's games), so Skill learning at L1 is wasted [MG2; LEAH].
- All 3 Opus losses that went C, C, D, D chased Network as the "weakest" statistic [DR].
- Nothing forces the promotion: the same v3 text was promoted at the first window in 4/4 g, then in 0/4 [MG5].

**G5. Choose honest ownership in stories.** Own, finish and show your work; never hide problems, cut corners, overpromise or take undue credit.
- Stories drive growth. In months 1–24, the completed v1 career gained +44 Skill, +20 Network and +18 Output from stories, against about +0, +4 and +2 from Energy. Its 3 losses gained about 0 from stories (small n) [MG2].
- The causal evidence is indirect: Haiku picks the same option per event under every policy [B3].

## 2. Promising, not yet proven

- **R1:** after a C or D, Defuse plus Prepare report materials in the last Energy phase before the next review. Opus got a D in 0/7 such cases against 7/22 without it [DR]. Its child went 2/4 (Q 52.4), not above f3-lean (small n) [REG]. R1 is tied to the review cadence (see §5).
- f1-risk-signal, f1-core and f1-status-line are still being screened [CRS].
- Prepare report materials most quarters: Opus winners 8/8 against losers 2/6, but no split in Haiku games (65 % against 68 % of quarters) [DR; B3].
- Lift a statistic that is falling or named in feedback, not the smallest one [DR]. Its child f7-trend-marking went 1/4 (Q 35.8) [REG].
- v3's build and review quarters: v4 replaced them with a bottleneck rule, and 3/4 g never left L1 (small n) [MG4].
- Keep Wealth above zero: at least 3 exits were "Broke" (F4, o1, f3-balance-recombined on opus~100k) [CRS].

## 3. Tried and failed

Race Haiku [REG] unless marked.

| Idea and manual | Result | Likely reason |
|---|---|---|
| F2: build first, convert late | 0/5, Q 22.7, dormant | eliminated before the payoff [FIND] |
| F5: relationships first | 0/5, Q 30.5, dormant | 3/5 ended at risk control 0 |
| F4: Output first, high intensity | 2/5, Q 35.2 (Sonnet 0/2) | — |
| M3: 1,287 words in 3 Skills | 1/4, Q 36.5 | hedged prose with no decisive action (m3-subtracted policy.json) |
| F6: ledger kept in the notes | 3/6, Q 40.8 | — |
| f3-opus-distilled: 5 rules at once | 2/4, Q 38.4 | dropped the weak-review plan |
| F7 children: trend marks / delivery stories / promotion drive | 1/4, Q 35.8 / 2/4, Q 46.5 / 1/4, Q 48.1 | none beat the parent |
| f8: growth mode when calm | 4/7, Q 43.8 | — |
| o2: Health used as fuel | 1/4, Q 36.2 | — |
| o1: build the stat that blocks promotion | 4/7, Q 46.0 | — |
| value-conversion: pay, no Defuse rule | 2/7, Q 45.2 | 4/5 losses at risk control 0 |
| Leah's review-clock v1 / v2 / v3 | 1/4, Q 37.7 / 2/4, Q 45.4 / 2/4, Q 52.3 | — |
| observed-growth-v2: Defuse and Health only on need | Matteo cell 2/4 (2 trust crises); race 1/4, Q 30.6 (2 blackouts) [MG2] | broke G1 and G2 |
| v4: three changes at once | 1/4, Q 32.8; 3 stuck at L1 [MG4] | — |
| v5: pay preference plus strong grades | 1/4, Q 30.3 [MG5] | — |
| Energy mix alone (400 bots) | no mix avoided the first C [EB] | — |

## 4. Frontier

- The 131 completed LLM g still miss about 38.6 points: level 16.1, wealth 12.7, network 3.4, risk control 3.1, skill 2.9, resilience 0.4. In the 44 completed g with Q ≥ 65, the gaps are level 15.0, wealth 11.5 and everything else 4.8 [REG].
- **No registry game went past L5.** 89 of 268 LLM g reached it, and the 150 scripted floor games peaked at L3. L5 earns half the level dimension [REG].
- Opus at maximum effort with a growth mode lost the same points (level 16.2, wealth 12.8) [OC].
- The energy-bot README reports bots at "level 40–60" with Q up to 76. That would mean L6, above every LLM game, with a fixed key-project main action. The raw data are not in the repo, so it is **unverified** [EB]; the organiser is asked to check it. If true, the level frontier is reachable and the question is what those careers did differently.
- The best wealth score is 52.8 [REG]. Published salary is 0.3 a month at L1, 1.0 at L5 and 9.1 at L10 [DIAG], so the wealth gap is mostly a level gap.
- Late promotions are slow. v3's last promotion took about 18 months, with Output flat [V4P]. Leah's v1 reached L4 at month 30 and L5 at month 48 [LEAH1].
- Pushing harder (f8, o2, F4, promotion drive, v4, v5) cost survival without raising level or wealth (§3).
- v4 tried five things: push the input that rose least; skip a repeated Defuse after a mild remark; High-intensity work when Health is near full; pay-seeking stories; aim for strong grades. Result: 1/4 (Q 32.8); its one completed game reached L5 with wealth 42.1 [MG4; V4P].

## 5. Compliance reminders

- No event titles, no fixed answers to specific events, no specific months, and no unpublished thresholds or score weights written as rules. Describe general behaviour from the public docs and in-run feedback [FIND l.11; ESTADO §6; CMP].
- Published constants are fine: Health and Dignity 0–10, Energy 0–3, 48 months, L1–L10 [CMP]. State observations without numbers, for example "a statistic can stall at your level" [MG3].
- Never copy wording from digests or HR remarks, and never write "take the first option" [ESTADO §6; EB].
- Timing tied to the review cadence (R1, v3's quarters, o1) is waiting for a team decision under prereg-v1 §10. Prefer triggers based on feedback or state [DR; CRS].
- Write in English and keep it short.
  - Skills sit in the system prompt on every turn [DIAG].
  - Haiku already uses about 0.51 M cached tokens a month, against a 0.5 M full-mark line [CRS; FIND l.20].
  - The lab works to about 400 words; v3 has 542.
- Make one change per variant and fill in the hypothesis, predicted_behaviour and refutation fields. The driver runs `careerlab lint` with the known event titles; a manual that fails twice is rejected [ESTADO §6].

## Source keys

- **CRS:** `lab/reports/cloud-run-status.md`. **CRS+:** the same file at commit e17b598.
- **B3, B5:** `lab/reports/cloud-run-diagnostics/block{3,5}-generation.md`.
- **MG2, MG3:** `lab/reports/matteo-observed-growth-v{2,3}.md`.
- **MG4:** `lab/reports/matteo-observed-growth-v4.md`. **MG5:** branch `matteo/observed-growth-v5`, `lab/reports/matteo-observed-growth-v5.md` (pending merge into main).
- **V4P:** `lab/policies-src/matteo-feedback-growth/observed-growth-v4/policy.json`.
- **LEAH, LEAH1:** `research/leah/l1-review-clock-{v1-v3,first-read}.md`.
- **DR:** `lab/reports/teacher-digests/distilled-rules.md`.
- **EB:** `lab/reports/energy-bots/README.md`.
- **OC:** `lab/reports/opus-ceiling/README.md`.
- **DEC:** `lab/reports/decision-research/cycles/002/interpretation.md`.
- **DIAG:** branch `alejandro/diagnostico-estrategias` (PR #4), `research/careerlab/diagnostico-2026-10-26/findings.md`.
- **FIND:** `findings.md`.
- **CMP:** `careerlab/compliance.py`.
- **REG:** my tally of `lab/registry/evaluations.jsonl` (e17b598) and `lab/registry-origins/matteo/` (3d1bea6). The trust-crisis proxy is an elimination with the risk-control dimension at 0; it matches every exit that has a reported cause.
