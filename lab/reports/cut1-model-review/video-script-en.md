# Three-minute presentation — simple English

Read the five sections in order. Do not read the headings aloud. Speak slowly and pause between sections.

## 1 — How we designed it

Hello, we are Gradient Depression.

We wrote one Skill: a set of instructions that helps DeepSeek play the career game.

We tried different ideas: keeping a good balance, learning more, building relationships, and reacting to feedback.

Our final Skill has two parts. One helps with story choices. The other plans how to use energy each quarter.

The main idea is simple: stay safe, stay healthy, and grow without losing the progress already made.

## 2 — What we found and changed

When we read the game logs, we saw a common problem. The agent built good results, but sometimes lost them just before a review.

So we added a short note. It records the current stats, the best stats seen at the current level, and how soon the next review will happen.

Before a review, the agent tries to protect those stats and recover lost progress.

We also saw that choices which sounded helpful could still lead to problems later. So we made the agent pay more attention to warnings.

We tested this version locally with DeepSeek and the official runner. Two games finished with scores of about seventy-two and seventy. A third stopped because of a technical problem while still at level one. We cannot promise the same scores every time.

## 3 — Why we did not include scripts

This version uses plain instructions, with no scripts or extra reference files.

We wanted the main rules to be easy to find in one place.

We also tried a version with a script. It had one very good game, but another failed early and it used more tokens. We chose the text-only version for this submission.

## 4 — How well it adapts

The Skill reads the current choices, stats and feedback. It does not use a list of fixed answers for named events.

It remembers what happened in the current game. It does not know the hidden promotion targets or the exact amount of hidden risk.

It can react when results change. But it can still misunderstand a choice, and it depends on the published game calendar.

## 5 — What we learned

Our biggest lesson is that following a rule is not the same as making a good choice.

The agent may know that a review is near, but still misunderstand what an option will do.

A Skill gives the agent a clear plan and helps it remember what matters. But more instructions do not always mean better results.

We need to check what the agent actually does, test more than one game, and be honest about what still fails.

Thank you.
