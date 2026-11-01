# Presentation script, plain-language version — Gradient Depression, Cut 3 (`mv-3`)

Spoken script for the final deck ([presentacion-c.html](presentacion-c.html)). English, normal speed, one speaker, written for someone who has never seen our work. It still answers the five official questions in order (S5–S16); S1–S4 set the scene and S17–S18 wrap up, as the rules allow.
917 words: ~6:50 at a calm 135 words per minute, which suits a general audience; leave a short pause on each drawing. `[S3]` means "show slide 3".

| Block | Slides | Starts | Words |
|---|---|---|---|
| The game and our job | S1–S4 | 0:00 | 177 |
| Q1. How we designed it | S5–S7 | 1:20 | 158 |
| Q2. What went wrong, and what we changed | S8–S13 | 2:30 | 288 |
| Q3. Why no extra programs | S14 | 4:40 | 63 |
| Q4. How well it adapts | S15 | 5:05 | 67 |
| Q5. What we learned about AI manuals | S16 | 5:35 | 59 |
| Wrap-up | S17–S18 | 6:00 | 105 |
| **Total** | 18 | **~6:50** | **917** |

---

## The game and our job (0:00–1:20)

**[S1]**
Hi, we are Gradient Depression, a student team. This is the story of how we taught an AI to survive a career, and what we learned on the way.

**[S2]**
Here is the game. An AI lives forty-eight months in a company. Every month it faces three situations and picks an answer, without seeing what that answer will do. Every six months there is a performance review, and a good one means a promotion.

**[S3]**
There are three ways to lose. Never getting promoted, and being fired. Letting hidden trouble pile up until it explodes, twice. Or burning out. And the AI never sees the hidden trouble directly: its only clue is the tone of a monthly comment from HR.

**[S4]**
The twist: we do not play. We write the manual the AI reads before it starts, called a Skill. The organisers then run the AI with our manual three times. Most of the score is how well those careers go. A little is how much the AI has to read, and a little is how good the manual is.

## Q1. How did we think while designing the Skill? (1:20–2:30)

**[S5]**
So, question one: how did we design it?
First, we studied the game from the outside. Using only our own games, we built a practice copy that makes the same move as the real game ninety-nine times in a hundred. We used it to test ideas cheaply. Nothing from it goes into the manual.

**[S6]**
Then we found the real problem. The AI is good at spotting danger: it caught eighty-three percent of risky answers. But it caught only about half of the answers that would help it grow. So the manual teaches it how to read an answer, in plain words.

**[S7]**
The manual makes the AI ask three questions every time. What will this answer change? What does my career need right now? And which rule fits this moment? It also keeps a one-line diary in every note: how long until the next review, its scores now, and its best scores so far. That line is its memory.

## Q2. What did the logs show, and what did we change? (2:30–4:40)

**[S8]**
Question two: what did we learn from watching it play?
We submitted three times. The first scored sixty-four point seven five. The second dropped to forty-five point four four. The third is the version we are presenting now, and we do not know its score yet.

**[S9]**
Lesson one. In the logs, the AI often missed a promotion by a single point, lost just before the review. So the manual now tells it to guard its scores in the two months before each review.

**[S10]**
Lesson two. Some answers sounded responsible, like a quiet private chat or fixing things bit by bit. But they hid trouble that exploded later. So the manual tells it to avoid any answer that might bury a problem.

**[S11]**
Lesson three. The AI was reading far too much. At every step it re-reads everything that has happened so far, so the more steps, the faster the reading grows. We taught it to answer each situation in one go. Its reading dropped from about one point four million word pieces a month to about zero point six.

**[S12]**
Lesson four, the surprising one. In one career the AI kept writing its answers as text instead of acting, and the run was stopped. We added one sentence to fix that glitch. Careers got worse: with that sentence, five of eleven ended early. Without it, seven of nine finished, averaging seventy point one, and two reached level six. We think, but cannot prove, that the sentence stopped the AI from thinking out loud. So we left it out.

**[S13]**
Lesson five. Quick tests fooled us. Three times, a cheap test said a change was better, and full careers said it was worse. So in the end we trusted only full careers.

## Q3. Why no scripts or reference files? (4:40–5:05)

**[S14]**
Question three: why no extra programs or files?
We were allowed to add small helper programs, and we tried one. It had one excellent career, but three of its seven careers ended early, and it read one point six times more. The AI's real problem is reading the situations, and a helper cannot fix that. So we kept one manual and nothing else.

## Q4. How general and robust is it? (5:05–5:35)

**[S15]**
Question four: how well would it adapt?
The manual only uses things the AI can actually see: the tone of HR's comment, the review talks, the menu of actions, the calendar and its own notes. No secret answers, no hidden game numbers. So if the stories change, the same method still works. Its weak spot: about one career in four still falls, mostly at the very start.

## Q5. What do Skills add, and where do they fall short? (5:35–6:00)

**[S16]**
Question five: what did we learn about manuals for AI?
A manual is very good at changing how an AI works: its habits, its order, how much it reads. It is much weaker at changing what the AI understands. You can tell it to protect a score, but you cannot make it see which answer will cost that score.

## Wrap-up (6:00–6:50)

**[S17]**
So here is the whole journey. We started by studying the game and building a practice copy. We wrote a first manual and scored sixty-four point seven five. We cut the reading. We stumbled with the second version. Then we stopped trusting quick tests and compared full careers, and that led us to mv-3.

**[S18]**
mv-3 is the manual behind our best careers: seventy point one on average in its finished practice careers, less than half the reading of our first version, and no secret answers inside. All these career scores come from our own practice runs, except the two official scores. Thank you for watching.
