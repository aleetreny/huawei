# Tarea para ChatGPT: diseños independientes del manual

Para que alguien de fuera piense distinto. Pega el texto de abajo en ChatGPT y **adjunta tres archivos** del repo:
- `lab/data/transmision/handbook.md`: el manual público del juego;
- `local-runs/official-runner/docs/competition-rules.rst`, o copia sus secciones *Document design quality* y *Permitted and prohibited content*;
- `lab/policies-src/transmision/t13-final/bundle/skills/career-rules/SKILL.md`: nuestro mejor manual. Adjúntalo sólo para la parte 3, después de que haya hecho las partes 1 y 2.

Lo que devuelva se prueba en nuestro banco de situaciones con DeepSeek, frente a nuestros manuales, en las mismas situaciones.

---

You are helping a team in a competition where a small language model (DeepSeek V4 Flash) plays a 48-month text career simulation by following "Skills": Markdown instruction files we write. We do not play; the model reads our Skill and decides. I want **your own, independent designs**. Think differently from us.

**The game (public rules are in the attached handbook).**
- Each month the agent answers 3 story events. Each event offers 2–4 options, and their effects are hidden until chosen.
- Every 3 months it spends 3 Energy on actions and picks one main action. The handbook lists these with their stat effects.
- Every 6 months there is a review that can promote it.
- Visible stats: Health, Dignity (both 0–10), Skill, Network, Output, Wealth, Level.
- A run fails on Health at zero, long-empty wallet, long isolation, dignity collapse, a second "blow-up" of hidden risk, or staying at the first level too long.
- The final score is out of 100 and weights level reached, wealth, health and dignity, skill, risk control and network.

**What we have learned (general facts, safe to use as principles):**
1. Promotion needs Skill, Network and Output all high enough for the level at the moment of the review. At the lowest level there is no slack: losing one point of Network or Output just before a review often costs the promotion. Each level has a ceiling per stat, and gains above it are wasted. The agent can detect a ceiling in-run when an announced gain does not move the stat.
2. Hidden risk accumulates from answers that hide, deny, take shortcuts, cave in to please, gossip, attack in public, or handle things privately or half-way. A monthly HR remark is the only visible gauge (friendly → quiet → frowning → uneasy → angry). A second blow-up ends the run.
3. The model reads risk fairly well, but it often **cannot tell which option raises Skill or Output**. That perception gap is where most points are lost.
4. Rules about quarterly Energy and main actions are obeyed well. Rules about story choices are obeyed only partly, and they **leak**: they change about 1 in 5 other story choices even when they do not apply, and that lowered scores sharply. A self-computed switch that the agent writes in its note before every story choice (for example `Review in N`) kept one story rule confined to its month.
5. Every action carries a free-text `notes` field (up to 1,000 characters). It is kept in the game log and survives context compression. Using it as a running status line (ceilings seen, risky picks since the last calm HR remark) looks valuable in simulation.

**Hard constraints (from the competition rules; breaking them can invalidate the entry):**
- No event titles, no fixed answers to named events, no specific month numbers as triggers, and no hidden thresholds, formulas or probabilities presented as known rules. Only general principles tied to signals the agent sees in the run.
- English only. Each SKILL.md starts with YAML front matter (`name`, `description`).
- One agent, no sub-agents.
- Keep it short: the model pays tokens on every call, and token efficiency is 10 % of the score.

**Your tasks**
1. **Three radically different designs** for the Skill set, each built on a different idea of how to make a weak model play well. Examples of directions, which you do not have to use: a decision procedure the agent fills per option; a "persona" or "values" framing instead of rules; a state machine driven only by the notes field; a minimal design that trusts the model; something else. For each design:
   - the complete SKILL.md file(s), at most about 600 words in total;
   - the one-sentence hypothesis of why it should work;
   - what result would show it is wrong.
2. **The perception gap.** Write the best short "how to read an option" guide you can (at most 150 words, general, no event content) that helps a model tell whether an option will raise or lower Skill, Network, Output, Health, Dignity, Wealth and hidden risk, from the option's wording alone.
3. **Critique our manual** (attached last): what a rubric reviewer would mark down, what may break the content rules, and what you would remove.

Be concrete and opinionated. Do not hedge between all options; tell me which of your three designs you would submit and why.
