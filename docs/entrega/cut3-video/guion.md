# Presentation script — Gradient Depression, Cut 3 (`mv-3`)

Spoken script for `presentation.mp4`. English, normal speed, one speaker. Target about 8:30, never over 9:30 (the limit is 10:00).
Timings assume about 145 words per minute (8:45 in all; 9:05 at a slower 140). `[S3]` means "show slide 3". Sentences in *italics* can be cut if the take runs long (about 5 seconds).

| Block | Slides | Starts | Length | Words |
|---|---|---|---|---|
| Opening: who we are, the task | S1–S2 | 0:00 | 0:40 | 98 |
| Q1. How we thought while designing | S3–S5 | 0:40 | 1:47 | 259 |
| Q2. From the logs to the changes | S6–S10 | 2:27 | 3:10 | 459 |
| Q3. Why no scripts or reference files | S11 | 5:37 | 0:44 | 106 |
| Q4. Generality and robustness | S12 | 6:21 | 1:11 | 171 |
| Q5. Agents and Skills | S13 | 7:32 | 0:52 | 126 |
| Closing: why mv-3 | S14 | 8:24 | 0:19 | 47 |
| **Total** | 14 | | **~8:45** | **1,266** |

---

## Opening (0:00–0:40)

**[S1]**
Hello. We are Gradient Depression. Our final submission for Career Survival is one Skill, called mv-3. We answer the five questions in order, and along the way we explain why this is the version we submitted.

**[S2]**
The task in brief. A DeepSeek agent lives a forty-eight-month career. Each month it answers three stories with hidden effects. Each quarter it spends Energy. Every six months, a review can promote it. It loses by never being promoted, by hidden risk blowing up, or by burning out. Its only gauge of hidden risk is the tone of a monthly HR remark.

## Q1. How did we think while designing the Skills? (0:40–2:27)

**[S3]**
Question one: how did we think while designing?
We started from why careers fail, and found failures at three layers. So every decision rests on three questions. What does this option probably change? What does the career need now? Which rule applies in this phase?

The first question is the hardest. In isolated tests, DeepSeek spotted eighty-three percent of risky options, but only about half of the options that raise Skill or Output. So the story section opens with a reading guide: in general words, what tends to move each stat and hidden risk. No event names, no answers.

**[S4]**
The second question is priorities, in a fixed order: stay in the run, win the next review, then grow. Every story goes through five ordered steps: survive, drop risk, protect wellbeing, protect the review, and only then grow. Quarterly phases are a short list where the first matching line wins, with a plan per level and a Health brake.

The third question is scope, because a rule that helps before a review can hurt elsewhere. Every note starts with a status line: months to the next review, Skill, Network and Output now, the best values held at this level, and reviews received here. "Review in N" is a switch: the review rules apply only when N is one or two. The line is also the agent's memory.

**[S5]**
We use one Skill, because with several, the agent opened one and missed rules in another. And since it reads the Skill early and then works from context, the manifest repeats the essentials.

## Q2. What did the logs show, and what did we change? (2:27–5:37)

**[S6]**
Question two: what did the logs show, and what did we change?
Our path first. Cut one, t13-read-v4, scored sixty-four point seven five officially, thirteenth of thirty-four. Cut two, mv-5r, scored forty-five point four four. Cut three is mv-3; we do not know its score yet.

**[S7]**
Three findings shaped the story rules.
One: early careers lost promotions by one point of Network or Output, in the last story before a review. So we added the "Best" value: protect Network and Output in the two months before a review, and repair any loss at once.
Two: responsible-sounding options, like a private talk or a phased fix, carried hidden risk the model missed. That became a list of risky wording, and a strict mode when the HR remark is not friendly.
Three: the notes showed the agent obeyed the review rule but misread costs: it believed a polite refusal kept Network. In our runs, it did not. So the Skill names those costs: Network falls when someone is let down, even politely; Output falls when your time goes to someone else's work.

**[S8]**
The fourth finding was tokens: cut one used about one point four million per game month. Every call resends the whole history, so cost grows faster than the number of replies. We moved to one reply per decision, with two tool calls, take_action then observe; DeepSeek only did it when the Skill showed the literal shape of that reply. mv-3 uses half a million to zero point eight million per month: on average, less than half.

**[S9]**
Our most honest example. One mv-3 career was stopped by the runner after twenty-one replies carried no tool call. The obvious fix was one manifest line: never end a reply with text only; put the decision in the call, not in prose. That line is the only difference in mv-4. It treated the symptom, but in full careers mv-4 ended early five times in eleven, while mv-3 completed seven of nine, averaging seventy point one, two at the sixth level. Our unproven hypothesis: the line removed the short written reasoning the model needs when its provider does not reason privately.

**[S10]**
The main lesson: cheap tests misled us more than once. For cut two, a bank of recorded situations said the hidden-cost text added risk at later levels, so we kept it to the starting level; two of three careers then collapsed there. On the last day, a rebuild of our cut-one rules won in replays of the first months and with our quality reviewers; in five full careers, three were dismissed at the starting level. *A bolder variant did not climb higher, and some of its careers blew up.* Full careers never misled us, so we submitted the Skill of our best careers.

## Q3. Why no scripts or reference files? (5:37–6:21)

**[S11]**
Question three: why no scripts and no reference files?
Scripts using only data from the current run were allowed, and we tried them. A teammate's advisor script had one excellent career at the sixth level, but three of its seven careers ended early, and complete ones used about one point six times more tokens. In our research replica, a script that kept state added nothing. What fails is reading the options, and a script cannot read them better than the model that feeds it. Reference files had a delivery problem: the agent did not reopen supporting files. So everything lives in one Skill and the manifest.

## Q4. How general and robust is it? (6:21–7:32)

**[S12]**
Question four: how general and robust is it?
The Skill holds no event titles, no fixed answers and no hidden thresholds. Every rule rests on what the agent can see: the HR remark, the review talks, the effects shown in the quarterly menu, and its own notes. The only calendar is the published one, a review every six months, and if a review talk comes late, the Skill keeps protecting until it appears. Our own observations are marked as such, and the game's signals come first, so if wording or order changes, the same procedure applies. The turn loop held with two model providers, one that reasons privately and one that does not.
The limits are real. Perception: about one career in four still collapses, mostly at the starting level, where the third review was won by only one of the eleven careers that reached it, and hidden risk, not missing stats, was the reason. The countdown assumes a six-month cycle. And some providers sometimes write a tool call as text.

## Q5. What do Skills add for an agent, and where do they fall short? (7:32–8:24)

**[S13]**
Question five: agents and Skills.
Skills are very good at changing how an agent works. The reply format alone cut tokens to less than half, and concrete quarterly directions were followed far more often than general goals.
They are weak at changing what an agent perceives. "Protect Output before a review" is obeyed, but it cannot make the model see which option costs Output.
Rules also leak: one earlier manual changed about one in five unrelated story choices, so scope must be written in, as a switch the agent computes.
And one sentence can change how the model plays, as mv-4 showed. A Skill has to be measured in the real loop, over whole careers.
Our conclusion: Skills give an agent priorities and discipline, not understanding.

## Closing (8:24–8:45)

**[S14]**
So we submitted mv-3: the best record in complete careers, less than half the tokens of our first cut, and rules built only on what the agent can see. Apart from the two official cut scores, every score here comes from our own development runs. Thank you.

---

## Notas de grabación (en español)

- Ritmo: a 145 palabras por minuto dura ~8:45. Si una toma pasa de 9:15, quitar la frase en *cursiva* de S10 y repetir más suelto; el límite del reglamento es 10:00 a velocidad normal (no acelerar el vídeo).
- Pronunciación: «t13-read-v4» = *tee-thirteen read vee-four*; «mv-3» = *em-vee three*; «mv-5r» = *em-vee five-ar*; «take_action» = *take action*.
- Decir los números como están en el guion. No añadir cifras que no estén aquí ni en la hoja de comprobación.
- No improvisar sobre el juego: nada de títulos de eventos, texto del juego, umbrales («the bar is…») ni el paquete del motor.
- Cambiar de diapositiva cuando aparece `[Sn]`, al empezar la frase siguiente.
