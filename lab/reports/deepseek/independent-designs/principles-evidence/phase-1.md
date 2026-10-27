# Phase 1 — public rules and raw observations only

Recorded before reading the updated HALLAZGOS/ESTADO or simulator code for this task. Historical knowledge from earlier turns cannot be erased; this is a source-restricted re-analysis, not a blinded study. Base main 53025e1. Only public handbook, competition rules, the bank README as a locator, result metadata for selection and three raw player traces were used. No engine package or key was opened.

## Trace sample and limitations

- Good: ~/careerlab-data/huawei/runs/scre-19618e77-08e916-00000-a2/stream-0.jsonl; completed, Q 71.75. A raw tool stream, because the completed registry trajectory paths point to unavailable files; no completed local trajectory.jsonl was found. The stream contains the same player calls/results. Selected as an available completed high-score run, not representative of all runs.
- Dismissal A: ~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-19618e77-dff20f-00000-a1/events.jsonl; Q 18.76, month 24.
- Dismissal B: ~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-f74ba2d9-dff20f-00000-a1/events.jsonl; Q 14.98, month 24.

Parser written from the raw formats in /tmp/huawei_principles_traces.py; intermediate raw excerpts remain /tmp/huawei-principles-player-traces.json, outside Git. Counts of observed-state payloads: 178, 85, 85. Logs-tool calls: 0, 1, 0. No research-labelled option outcomes were used in this phase.

## My model

**What determines score?** Public competition scoring uses three career outcomes, document quality and per-survived-month tokens, with an early-exit cap. The raw terminal tool payload reports separate career components: level, wealth, wellbeing, skill, risk control and network; Output is absent as a direct terminal dimension. Therefore Output may be an enabling resource rather than a terminal objective. Salary and review bonuses link earlier promotions to later wealth. The good career achieves Q 71.75 at L5, so chasing the highest attainable title is not the only route to a useful score. These traces cannot establish all normalisation rules or a globally optimal allocation.

**Irreversible losses?** Death/dismissal terminates actions; a failed review cannot be repaired retroactively; lost promotion opportunities delay later income/career windows. A blow-up can undo progress and leaves less room before trust failure. Before a review, a growth stat near an apparently sufficient plateau is a fragile constraint, not spare currency. Selecting a reasonable life choice can nevertheless lose that constraint. A negative outcome can occur before the next quarterly repair opportunity.

**Information and timing?** observe gives precise visible stats, current time/level and actual offered choices; quarterly menus include numeric status_updates, costs and hidden-risk changes for some actions. take_action in these traces returns success/error, not an explanatory effect breakdown. A fresh observe gives the next state; events reports review/HR/warnings when emitted and can subsequently be empty. check_latest_logs returns action effects, notes and other entries, but costs a separate call. Narrative outcomes also appear in logs. A month-boundary stat difference can combine the choice, salary, review and promotion, so it is not automatically a clean action effect. Reviews are already present at the first observe of the review month in these traces. Completion also sets generic failed/alive flags terminally; ending_score.outcome distinguishes completion from elimination.

**What can be learned within a run?** Menu effect magnitudes; gains that fail to appear; health/relationship/delivery costs of one's own actions; whether provisional verbal interpretations were wrong; feedback about promotion success; sequences of HR changes. One can remember a small personal boundary such as “my predicted harmless refusal cost a relationship” without memorising a development event. Cannot infer unchosen counterfactual effects from one action, assume effects transfer to every new story, or isolate a story's hidden-risk change from a monthly aggregate without other assumptions. The good trace did not use logs at all: log use is possible, not established as necessary.

## Boundary observations that change the framing

- Dismissal A enters month 4 at Skill/Network/Output 9/3/3, the same values still present at month 5. One within-month choice changes Network 3→2. The first review does not promote. It returns to 9/3/3 before the next window, then a late story changes Output 3→2; again no promotion. This looks like a retention failure, not an inability to grow.
- Dismissal B enters the last preparation month at 7/3/3; a story raises Skill to 8, and the final story leaves Output 2. At first observe of the review month the panel is 8/3/2. The raw note explicitly applies the review rule and calls the chosen action harmless. Thus obedience to a mistaken simplification can create a decision error. The last pre-review Skill state is not 7 in this trace.
- Good career enters the preparation month at 8/3/3, then 9/3/3, and is promoted at the next first observe. It also has neutral/weak-sounding manager wording with promotion: grades/prose alone do not identify the missing requirement.
- Dismissal B later chooses a fast-delivery route while its latest HR remark is angry; its note cites the review marks rather than controlling the risk concern. Inference: priority execution is a distinct possible failure, even if isolated-option perception is good.

## Hypotheses to carry into phase 2 (not findings yet)

1. The task is a constrained control problem: learn from observed response, preserve a feasible career state, and spend known-effect quarterly actions as insurance. Full seven-sign prediction may be more work than deciding which downside is affordable.
2. A lagged risk gauge cannot support guaranteed safety between remarks without a bound on unseen disturbances. Guaranteed quarterly cleanup might reduce drift without classifying options, but cannot undo an intra-month shock.
3. Coarse narrative reviewer feedback should not automatically activate a growth mode. A human would track what changed after a prior near-success rather than assume the review names an accurate stat gap.
4. Conditional policy quality, perception and execution should be measured separately. A full consequence classifier may not be the cheapest useful representation.
5. Three-game means do not make low variance an independent objective; survival has value through actual career/efficiency payoffs. Best-of-cuts creates an option to explore after securing a valid baseline, subject to score-release delay.
