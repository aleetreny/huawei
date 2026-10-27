# Recording script — t13-read-v4

Internal recording aid. About 8–9 minutes at 120–140 words per minute. The five numbered sections follow the required question order. This describes the frozen t13-read-v4 bundle, not the alternative script controller. Remove editorial headings when reading aloud. Do not treat this script as organiser approval.

## 1. How we thought while designing the Skills

Hello, we are Gradient Depression. Our submission is called t13-read-v4. It is a single English Skill that guides the designated DeepSeek agent through the career simulation. We did not train a new model. We designed and tested instructions for the existing model.

Our starting question was: how can an agent grow professionally without sacrificing the conditions that let it continue playing? We explored different approaches: balanced development, early investment, responding to feedback, relationships, and more structured memory. We treated these as hypotheses and compared their behaviour, including their failures.

The final approach combines three ideas. First, stories and quarterly planning need different decision procedures. Second, the agent should preserve professional progress when a review is approaching. Third, it needs a compact record of its own observations so that a good plan survives a long conversation.

At each turn, the agent observes the current situation, applies the procedure for the current phase, and takes an available action. For stories, it considers possible effects on wellbeing, money, professional capability, relationships, output and risk. It prioritises immediate survival, manages risk and wellbeing, protects progress near a review, and then seeks growth.

Quarterly planning has a separate ordered list. It first considers the end of the career, recovery needs and warning signals. It then responds to the latest review feedback and chooses useful investments. The first relevant condition determines the plan, subject to the available energy and action choices.

## 2. What the logs taught us, and what changed

Our most useful debugging finding was that the agent could rebuild its professional indicators during quarterly planning, then lose progress through story choices shortly before a review. A choice could sound responsible while taking time away from delivery or damaging a working relationship.

The response was not simply to tell the agent to work harder. In Matteo's observed-growth line we tracked the best values the agent had actually seen at its current level. The final version incorporates that idea. It records current and best observed Skill, Network and Output, pays particular attention before a review, and tries to repair lost ground.

We also saw a different failure: apparently constructive choices could still accumulate risk. In two earlier DeepSeek careers, version one ended with scores of 14.98 and 42.51. The traces showed that language such as a private fix, a partial resolution or postponing work could be read as safe even when the subsequent feedback became worse.

Another trace showed a quarterly instruction influencing a story decision. We therefore separated the two procedures explicitly, moved critical guidance into the main Skill and manifest, and strengthened the response to warning signals. Version three introduced a limited trade-off near a review: when feedback is reassuring, preserving professional progress may take priority over a mild concern, while concealment and serious shortcuts remain excluded. Version four added the best-observed values, the two-month preparation window and immediate repair guidance.

In local development tests using the designated DeepSeek model and the official runner, version four completed two careers with scores of 71.67 and 70.22. These are local development results, not official competition scores. A third career was interrupted by an infrastructure problem while still at level one, so we do not claim that the candidate reliably averages seventy.

## 3. Why this submission uses no scripts or reference files

The submitted bundle contains one Skill and a manifest instruction. It has no executable controller and no separate reference file.

Earlier experiments showed that placing a rule in a reference file did not guarantee that the agent would retrieve it at the right moment. We kept the decision-critical guidance together and used the manifest to reinforce phase separation and review preparation.

We also explored a script-based controller as a separate candidate. It achieved one very strong career, but another failed early and its additional tool calls increased token use. We selected the text-only candidate for this submission rather than treating the strongest individual result as proof of the best design.

The laboratory uses scripts to organise experiments and analyse outputs. Those research tools are separate from what we submit.

## 4. Generality, robustness and remaining limits

The agent does not receive a table of named events and fixed answers. It reads the current options and the feedback available in its own run. Its notes record current values, best observed values, the review countdown, provisional evidence that an expected gain did not appear, and its own concerns about recent choices.

These records have limits. An unobserved gain is not proof of a permanent ceiling. A count of concerns is not a measurement of hidden risk. Our best-value field is a memory of observations, not a supplied promotion threshold.

The design can respond to different event orders and changing outcomes, but we have not established robustness to every environment change. It uses the published review calendar and action structure. If those change, those parts need updating. Interpreting the consequences of unfamiliar options also remains a major weakness.

In particular, the model did not consistently maintain the provisional stalled field in our tests. We describe this as an intended mechanism with incomplete execution, not as a solved capability.

## 5. What we learned about agents and Skills

A Skill can give an agent priorities, a repeatable procedure, reminders and a compact memory format. It can reduce confusion between tasks and make decisions easier to inspect.

But following an instruction is different from understanding a consequence. An agent can correctly write that a review is near and still choose an option that harms the progress it meant to protect. Longer instructions or more memory do not automatically solve that problem, and extra rules can interfere with one another.

Our main lesson is to evaluate three things separately: whether the agent reads the Skill, whether it follows the procedure, and whether the resulting decision helps. We moved from broad advice towards a smaller set of explicit priorities, tested the actual target model, and retained the failures in our evaluation.

We see Skills as a way to organise an agent's reasoning and use of feedback. They do not replace judgement, reliable perception or honest measurement of uncertainty. Thank you.
