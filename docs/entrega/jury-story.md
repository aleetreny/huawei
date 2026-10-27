# Jury story draft — the five official video questions

Working draft, 26 October 2026 (team-internal). It must be rewritten for the final version, using only results that exist at that time. Numbers marked *(preliminary)* come from Claude proxy workers on the dev game, not from the designated model. Replace them with target-actor results when available. The video must answer the five questions in this order, in English, in at most ten minutes, at normal playback speed.

## 1. How did we think while designing the Skills?

- **Treat Skills as policies to test, not prose to polish.** Every version of our Skills is a frozen, content-hashed policy with a written hypothesis, a predicted behaviour and a refutation criterion. We wrote ten deliberately different behaviour families before seeing any result: a minimal baseline, steady balance, invest early, feedback-reactive, visible delivery, relationship capital, commitment ledger, the same strategy as one Skill versus three, and a teammate's design.
- **Optimise the real objective.** Each run contributes 0.8 × quantitative score + 0.1 × token efficiency, and the efficiency term is capped at 50 if the run does not reach month 48. Survival to month 48 is therefore worth points in its own right, and concise Skills are cheaper on every turn.
- **Respect the rules by construction.** Decisions come only from the current run's state, text, choices and feedback. A linter rejects named-event answers, unpublished thresholds, calendar triggers and non-English text, and it checks every Skill against every event title we have ever observed.

## 2. What did earlier versions' logs show, and what did we change?

*(preliminary; Claude proxy workers, 1–4 runs per cell)*

- **The logs showed two ways to lose.** A run fails either through a second weak half-year review (always at month 24 in our runs, after grades such as C, C, D) or through a "trust crisis" after accumulated hidden risk. The run's own feedback announces both: "the half-year review fell short… the next one has to be better", followed by risk warnings.
- **The long, careful design (three Skills, about 1,300 words) lost in every proxy run.** The short, balanced and feedback-reactive designs completed all 48 months.
- **Changes we made from these traces:** a review-recovery mode with an explicit exit (back to normal after a solid review), a risk-defusing response to warnings, a subtraction of the long design, and a less defensive review-first variant. Each child keeps a link to its parent and the log evidence that motivated it.
- **What the comparison showed:** *(fill in from the block decisions)*, for example "the review-recovery child did / did not beat its parent at equal runs".

## 3. Why did we (not) use scripts or reference files?

- The submission runs as a single agent with the designated model. In our lab, the levers that mattered were behavioural: when to recover, when to deliver visibly, and how to react to feedback. Executable scripts would add attack surface and review risk without helping the model decide a story choice.
- *(Decide and state the final choice. The lab can measure a reference-file variant like any other policy.)*

## 4. How general and robust are the Skills if the settings change?

- **No fact specific to the dev dataset is encoded.** The modes trigger on the run's own feedback and visible trends, never on months or event titles. The linter enforces this.
- **We tested across actors.** The same Skills were played by different models: Haiku, Sonnet and Opus, at several effort and context settings. Rankings that hold across actors are more likely to survive a change of evaluator. Rankings that flip (Sonnet completed 0 of 6 runs, while Haiku and Opus agreed) told us which conclusions not to trust.
- **We tested late benefits and specialisation explicitly.** Policies are judged only on complete 48-month runs. A context switch must beat both "never switch" and "always switch", and a calendar version of a rule is a diagnostic, never shipped.

## 5. What did the competition teach us about agents and Skills?

- Skills are executable hypotheses. Their value depends on the actor that runs them: the same text produced bimodal outcomes that depended on the model and its effort setting.
- Evaluation design mattered more than generating many ideas. Episodes are stochastic and expensive, so we raced complete episodes with a pre-registered rule, kept losing ideas in a reversible archive and confirmed on fresh runs.
- **Our own contribution.** It is not a new search algorithm; the mechanisms (racing, partial pooling, archives, reflective prompt revision) are known. What we added:
  - an objective matched to the official score, including the early-exit cap;
  - a laboratory that measures the interface instead of assuming it (session retention, isolation, observe-before-retry);
  - an explicit treatment of actor bias, late benefits and spurious specialisation;
  - an audit trail that ties every Skill version to the evidence behind it.

## Evidence to collect before recording

- A lineage diagram with the dormant branches included (`lab/registry/policies.jsonl`, `decisions.jsonl`).
- The block decisions table with posteriors and P(best), and one reopened or audited branch.
- The actor-comparison table (problem A) and one example where the actor changed the ranking.
- Token use per month for the final version on the designated model (from the target pilot).
- Infrastructure facts that prevented false conclusions: the session-retention eviction, the duplicate-lease incident, and operator stops that were never scored.
