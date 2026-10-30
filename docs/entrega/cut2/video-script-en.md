# Guion del vídeo del corte 2 (`mejora/mv-5r`)

Interno, no va en el ZIP. Es el texto para leer mientras se pasan las diapositivas: [presentación en claude.ai](https://claude.ai/artifact/JQE62TghzwYgvG2ZyoTnfy) (10 diapositivas, el mismo aspecto que la del corte 1; cada diapositiva lleva este mismo texto en sus notas).

**Cómo grabarlo.**
- En inglés, a velocidad normal, sin leer los títulos de las secciones. Pausa breve al cambiar de diapositiva.
- ~1.230 palabras: unos 8 minutos leyendo con calma (el límite es 10). Cada diapositiva responde a una de las 5 preguntas oficiales, en su orden (`competition-rules.rst`, «Video presentation»): «de dónde venimos» abre la pregunta 2 (la versión anterior es v4) y «a dónde vamos» cierra la 5 (dónde se queda corto un Skill).
- Todas las cifras son partidas locales con el programa oficial y el juego de desarrollo, no notas oficiales, salvo el 64,75 del corte 1. Fuentes: [informe de Mejora](../../../lab/reports/mejora/README.md) §7–§12 y HALLAZGOS C45, C49, C59, C63, C69, C70, C72, C74–C78, B31.
- Si se cambia algo del manual antes de entregar, revisar la diapositiva 4 y la 6.
- Guardar el vídeo como `presentation.mp4` y empaquetar con `scripts/entrega/build_cut.py` (pasos en [PREPARAR.md](PREPARAR.md)).

---

## Slide 1 — Cover

Hello again, we are Gradient Depression. In Cut 1 we submitted a Skill called t13-read-v4. This video presents its successor, mv-5r, by answering the five questions in order: how we designed it, what the logs showed, why no scripts, how robust it is, and what we learned about agents and Skills.

## Slide 2 — Q1: how we thought while designing

Question one: how did we think while designing the Skill? We do not play the game, DeepSeek does. And full games are slow and expensive, and one game says very little. So we test every idea from cheap to expensive. First, a replica of the game that we rebuilt from our own game outputs, where we can run thousands of careers for free. Second, a bank of real situations, answered again by DeepSeek with each candidate Skill. We learned to run it twice, because one pass is noisy. Third, short probes of the first turns, to check the reply format with different model providers. Only then, full games. And before each test, we write down the result that would make us drop the idea.

## Slide 3 — Q1: what mv-5r keeps and changes

So what is mv-5r? It is still one Skill. It keeps v4's judgement: story decisions follow five steps in order. Survive, avoid hidden risk, protect wellbeing, protect the review, and grow. The list of risky wording is the same, word for word. What changed is how the agent works. A turn loop: one reply per decision. A one-line status line that carries memory from turn to turn. A quarterly plan that changes with the level, with a brake when Health gets low. And, only at the starting level, a short list of hidden costs. In question two we explain each change with the logs that motivated it.

## Slide 4 — Q2: the earlier version (where we come from)

Question two: what did we find in the logs of an earlier version, and how did we change it? First, where we come from. Our first DeepSeek games on the official runner were all eliminated, with scores of 15, 19 and 43. Then t13-read-v4 gave us our first two complete careers, at about 72 and 70. That was our Cut 1 submission, and its official score was 64.75. When we looked at how that score is built, one part stood out. Ten percent of the score is token efficiency, and it is full only at 500 thousand tokens per game month or fewer. v4 used about 1.4 million, so it earned only about 64 of 100 there. So v4 is the earlier version, and we went back to its logs.

## Slide 5 — Q2: what the logs showed

In v4's logs we found four things worth improving. First, cost. v4 used about one and a half million tokens per game month. Each decision took several replies, and every reply sends the whole history again. So now one reply carries two calls, the action and the next observation, and the note is one line. That brings it to 300 to 500 thousand. Second, one wording of this loop broke with a model provider that does not reason privately: the agent narrated and sent the action alone. We kept the wording that worked with both providers, byte for byte, and it paired 18 replies out of 18. Third, one game stopped with no score, because the model wrote its tool call as plain text 21 times. One line in the manifest, never end a reply with text only, fixed it. Fourth, before the first review, DeepSeek followed our rule to protect Network and Output, but misread what an option costs. For example, it thought a polite refusal keeps Network. In the game, it does not. So we name these hidden costs, but only at the starting level: when we used them at every level, the agent took more risk before later reviews.

## Slide 6 — Q2: the result

The result. In its complete game, mv-5r used 460 thousand tokens per game month, about a third of v4. That moves the token efficiency score from about 64 to 100. The story play is v4's, and our games agree. Across the Skills of this family, 7 of 11 games were complete, with an average of 68. Our best game ever, 77.8, was the first career to reach level 6. mv-5r itself played three games: one complete at 69, and two dismissed at level 1. So we are honest about it: this version saves tokens; it does not yet play better than v4. These are local results on the development game, not official scores.

## Slide 7 — Q3: why no scripts

Question three: why no scripts? We did consider them. We built versions with scripts that keep memory of the current run, and we measured them in the replica, like any other idea. They changed the average by one or two points at most. The reason is simple: our losses come from misreading what an option will do, and a script reads the same text as the model. The memory we need fits in one status line. And in our logs, DeepSeek reads the Skill but does not reopen extra files, so every rule lives in one file. Even the token savings came from the reply format, not from code.

## Slide 8 — Q4: if the settings change

Question four: how general is it? The Skill names no event and has no fixed answers. It reacts to what the game shows: the HR remark, the review talks, and the stat changes after each choice. It reads the quarterly menus in the current run instead of having them written in. It uses the published six-month calendar, and if a review talk has not appeared yet, it keeps protecting. Everything we learned from our own games is marked as our observation, so the game's signals come first. Where can it break? A different review calendar would shift its countdown. It guesses option effects from their wording, and that guess can be wrong: about one game in four still collapses, mostly at the first promotion. And we tested the reply format with two providers, not with all of them.

## Slide 9 — Q5: what Skills add, and where they stop

Question five: what did we learn about agents and Skills? A Skill is very good at changing how an agent works. DeepSeek follows a quarterly plan, keeps a one-line memory, and the reply format alone cut its tokens by two thirds. It also makes the agent more careful: in 320 situations, our Skills cut the loss per decision by about a third, mostly by avoiding risk. But a Skill does not change what the agent sees. It can follow a rule and still misread an option. More text did not help: a Skill half as long chose the same. A rule written for one moment can change behaviour somewhere else. And measuring is hard: one pass of a test is noise, and one game is an anecdote.

## Slide 10 — Q5: what a Skill has not fixed yet (and what we do next)

The clearest example of where a Skill falls short is the first promotion, and it is also where we are going next. About one game in four still collapses, mostly because the career never leaves the starting level. When we studied the losses just before the first review, half of them had no clean alternative: every option cost a stat or added risk. A planner that sees the effect of every option averages 72.4 on the same game. So the gap is not more rules. It is avoiding collapses and reading options better. For the last cut, every new idea will go through the replica and two passes of the situation bank before we play a single game. That is our plan for the last cut. Thank you.

---

## De dónde sale cada cifra (para revisar, no para leer)

| Diapositiva | Cifra | Fuente |
|---|---|---|
| 4 | 15 · 19 · 43; 71,7 · 70,2 | vídeo del corte 1 (15,0 · 18,8 · 42,5); HALLAZGOS C3 |
| 4 | 64,75 | nota oficial del corte 1, HALLAZGOS C45 |
| 4, 6 | 500 mil → 100; 1,4 M → ~64 | `competition-rules.rst` (100 × (3 M − x) / 2,5 M); v4 1,35–1,47 M, Mejora §1 |
| 5 | 0 de 3 sondas; 18 de 18 | Mejora §6 y §10 (C69, C77) |
| 5 | 21 respuestas sin llamada; 0–2 por partida | Mejora §7 (C70): mv-4 1, 1, 1, 2, 2; mv-5r 0, 1, 0 |
| 5 | riesgo antes de evaluaciones posteriores | Mejora §9–§10 (C75, C77) |
| 6 | 460 mil por mes | mv-5r n.º 2, 461 mil (Mejora §11) |
| 6 | 7 de 11 completas, 68,2 | mv-3 (68,64 · 77,78 · 66,06), mv-4 (63,35 · 69,62 · 63,27), mv-5r (69,00); hundidas 37,06 · 18,98 · 22,65 · 24,51; la cortada de mv-3 no tiene nota |
| 7 | scripts ±1–2 | HALLAZGOS C63, C64 |
| 7 | no relee archivos de referencia | vídeo del corte 1, HALLAZGOS B10–B14 |
| 9 | 320 situaciones, 1,37 → 0,91 | Mejora §11 (C78) |
| 9 | la mitad de texto elige igual | `mv-s`, Mejora §11 (C78) |
| 10 | 1 de cada 4 | Mejora §8 y Relevo (~25 %) |
| 10 | la mitad sin alternativa limpia | mapa de pérdidas, Mejora §9 (C74): 6 de 11 con sólo +2 o ninguna |
| 10 | 72,4 | HALLAZGOS A5, B31 |
