# Speaker notes, extended (cut 3 video, mv-3)

Leah, 1 Nov 2026. Extended version of the speaker notes in Alejandro's 18-slide deck (claude.ai artifact). It keeps the same slides, the same order and the same five official questions, with more substance so the jury hears that we understand the game and the agent. Spoken text in English; delivery notes in *italics*.

**Length:** 1,263 spoken words: about **9 minutes at 140 words per minute**, 8.4 at 150, 9.7 at 130 (limit: 10 minutes). The time marks per slide are a guide. Read at a calm pace. If a rehearsal goes over 9:30, cut the last sentence of slide 14 and the provider sentence of slide 15. Every number comes from `ENCARGO.md` §4 or from the files it cites; every claim about the Skill matches `lab/policies-src/mejora/mv-3/bundle/` and `docs/entrega/cut3-mv3/`. The source of each claim is in the table at the end.

---

### 1 · Title (0:00–0:15)
Hi, we are Gradient Depression, a student team. We never played a single move of this game. We wrote the manual an AI reads before it lives a whole career. This is the story of that manual: what we tried, what broke, and what we learned.

*Calm and confident. Short pause after "a whole career".*

### 2 · The game (0:15–0:35)
Here is the game. An AI lives forty-eight months inside a company. Every month it faces three situations and picks an answer, without seeing what that answer will do. Every quarter it spends a small budget of energy. And every six months there is a performance review, where the right numbers mean a promotion.

### 3 · Three ways to lose (0:35–0:55)
There are three ways to lose. Never getting promoted, and being fired. Letting hidden trouble pile up until it explodes, twice. Or burning out. The hardest part: the AI never sees the hidden trouble. Its only clue is the tone of a monthly comment from HR. So from the very first month, this is a game about reading signals, not numbers.

*Emphasise "reading signals, not numbers": it is the thread of the whole video.*

### 4 · Our job (0:55–1:15)
The twist: we do not play. We write the manual, called a Skill, and the organisers run the AI with it three times. Eighty percent of the score is how those careers go. Ten percent is how much the AI has to read. Ten percent is how good the manual is as instructions. So every sentence we write has to earn its place.

### 5 · Question 1: how we designed it (1:15–1:45)
Question one: how did we think while designing it?

We started by studying the game from the outside. Using only the public tools and our own games, we built a practice copy that makes the same move as the real game ninety-nine times in a hundred. That gave us a lab to try ideas thousands of times for free. A lab, not a cheat sheet: nothing from it goes into the manual.

*Slow down on "a lab, not a cheat sheet".*

### 6 · The real problem (1:45–2:20)
The lab showed us that careers are decided at the reviews, by small story choices. Then we measured the model. It caught eighty-three percent of the risky answers, but only about half of the answers that would help it grow. That is the real bottleneck. So the manual does not hand out answers. It teaches the AI how to read one: what usually costs Network, what usually costs Output, and what usually buries a problem.

### 7 · Three questions every time (2:20–3:00)
Every decision runs through three questions. What will this answer change? What does my career need now? Which rule fits this moment?

Stories pass five ordered steps, from survive to grow. Quarters use a short list where the first matching line wins. And because the AI forgets, every note starts with a one-line diary: months to the next review, scores now, and best scores at this level. That line is its memory. All of it lives in one Skill: when we split the rules, the AI opened one and lost the rest.

*Point at the diagram while naming the three questions.*

### 8 · Question 2: what the logs taught us (3:00–3:20)
Question two: what did the logs teach us?

We submitted three times. The first manual scored sixty-four point seven five. The second dropped to forty-five point four four. The third is the one we present today, and we do not know its score yet. Every change came from reading what the AI actually did.

### 9 · Lesson 1: lost by one point (3:20–3:40)
Lesson one. Again and again, the AI missed a promotion by a single point, lost in the last story before the review. It was not a bad strategy, just one bad moment. So the manual now guards Network and Output in the two months before each review, and Skill too in the last month, remembers the best value it reached at this level, and repairs any loss at once.

### 10 · Lesson 2: nice answers that hide trouble (3:40–4:00)
Lesson two. Some answers sounded responsible: a quiet private chat, a fix done bit by bit, an anonymous report. In the logs, those were exactly the ones that exploded later. So the manual names them. Anything that might bury a problem is dropped, and when in doubt, an answer counts as risky.

### 11 · Lesson 3: reading too much (4:00–4:35)
Lesson three. The AI was reading far too much. At every step it re-reads the whole history, so the cost grows with the square of the number of steps. The fix was fewer turns: one reply with two calls, act and then look, and after the first quarter, a whole quarter in one reply. Reading dropped from about one point four million word pieces a month to about zero point six, and the efficiency score went from the sixties to the high nineties.

*Pause after "the square of the number of steps": it is the insight.*

### 12 · Lesson 4: one sentence (4:35–5:15)
Lesson four, the surprising one. In one career, the AI wrote its answers as text instead of acting, and the run was stopped. We added one sentence telling it never to do that. On paper, a fix. In real careers, worse: with that sentence, five of eleven careers ended early. Without it, seven of nine finished, averaging seventy point one, two at level six. Our guess, and it is only a guess: the sentence stopped the AI from thinking out loud. So we took it out. One sentence moved the whole result.

*The emotional peak of the video. Slow down, pause before "One sentence moved the whole result."*

### 13 · Lesson 5: quick tests fooled us (5:15–5:50)
Lesson five. Quick tests fooled us. Three times, a cheap test said a change was better, and full careers said it was worse. Our second submission came from exactly that: a bench of recorded situations told us to limit one reading rule, and two of three careers sank at the first level. So we built tests that replay the real start of a career, and in the end trusted only full careers.

### 14 · Question 3: why no scripts or extra files (5:50–6:30)
Question three: why no scripts or extra files?

The rules allowed small helper programs that use only what the game shows, and we built one. It had one excellent career, at level six, but three of its seven careers ended early, and it read about one point six times more. A helper can calculate, but it cannot read a situation for the AI, and reading is the real problem. So we kept one manual and nothing else: one thing to follow, one thing to check.

### 15 · Question 4: how general it is (6:30–7:15)
Question four: how general is it, and how would it adapt?

The manual uses only what the AI can see: HR's tone, the review talks, the menu of actions, the published calendar and its own notes. No event names, no secret answers, no hidden game numbers. What we only observed is marked as ours, and the AI trusts the game first. And it ran with different providers of the same model. The honest weak spot: about one career in four still falls, mostly at the start, where one lost point decides the first promotion.

### 16 · Question 5: agents and Skills (7:15–8:00)
Question five: what did we learn about agents and Skills?

A Skill is very good at changing how an agent works: its habits, its priorities, how much it reads. It is much weaker at changing what the agent understands. You can tell it to protect a score, but not make it see which answer will cost that score. And one sentence can shift a whole career. So a Skill gives an agent discipline and priorities, not understanding. And the only honest way to know what it does is to measure it for real.

*This is the thesis. Look at the camera, not the slide.*

### 17 · The journey (8:00–8:20)
So here is the journey. We studied the game from the outside and built a lab. We wrote a first manual and scored sixty-four point seven five. We cut the reading. We stumbled with the second version, and learned not to trust quick tests. And by comparing full careers, we arrived at mv-3.

### 18 · mv-3 (8:20–8:45)
mv-3 is the manual behind our best careers: seventy point one on average in its finished practice careers, two of them at level six, with less than half the reading of our first version, and no secret answers inside. All career scores here come from our own practice runs, except the two official scores. We are Gradient Depression. Thank you for watching.

*Smile. Two seconds of silence before stopping the recording.*

---

## Check against the sources

| Claim in the script | Source | Matches |
|---|---|---|
| 48 months, 3 situations a month, quarterly energy, review every 6 months | handbook (official docs); `ENCARGO.md` §3.1 | yes |
| Three ways to lose; HR tone is the only clue to hidden risk; two blow-ups end the run | `ENCARGO.md` §3.2; HALLAZGOS A3; mv-3 SKILL.md "Throughout" | yes |
| 80 % careers, 10 % reading (tokens), 10 % manual quality | competition-rules.rst; `ENCARGO.md` §1 | yes |
| Practice copy same move 99 times in 100; not used in the manual | HALLAZGOS B1 (99.3 % of steps); `ENCARGO.md` §3.1, §7 | yes |
| 83 % of risky answers; about half of growth answers (Skill 45 %, Output 49 %) | HALLAZGOS B17; `ENCARGO.md` §4 | yes |
| Five ordered story steps; first matching quarterly line wins | mv-3 SKILL.md, "Story decisions" 1–5 and "Quarterly phases: first matching line wins" | yes |
| Status line: Review in N, Now, Best (it also has Reviews here, not named in the script) | mv-3 SKILL.md, "Status line" | yes |
| One Skill because with several the agent opened one and lost rules | `ENCARGO.md` §5.1; HALLAZGOS B13 | yes |
| Official 64.75 and 45.44; third score unknown (rank not said: it was 13th after cut 1, 28th now) | `ENCARGO.md` §4; ESTADO 1 Nov | yes |
| Protect Network and Output two months before a review, Skill too in the last month; Best; repair at once | mv-3 manifest and SKILL.md step 4 (N = 2: Network and Output; N = 1: also Skill) | yes |
| Private, partial, anonymous answers dropped; "when in doubt, risky" | mv-3 manifest; SKILL.md "Hidden risk" | yes |
| Cost grows with the square of steps; one reply with two calls; whole quarter in one reply after the first quarter | HALLAZGOS C51–C53; mv-3 manifest, SKILL.md "Turn loop" 3; skills_design.md §3 | yes |
| 1.4 M → ~0.6 M tokens a month; efficiency from the sixties to the high nineties | v4 1.35–1.47 M (score ~64); mv-3 0.49–0.78 M (89–100, mean ~96 in completed) — `ENCARGO.md` §4 | yes |
| With the extra sentence 5 of 11 ended early; without, 7 of 9 finished, 70.1, two at L6 | mv-4: 6 completed + 5 not completed; mv-3: 7 of 9, mean 70.1, 77.78 and 74.12 at L6 — `ENCARGO.md` §4 | yes |
| Thinking-out-loud explanation is a hypothesis | `ENCARGO.md` §3.8 | yes (said as a guess) |
| Second submission: bench said the rule added risk beyond L1; two of three careers sank at L1 | `ENCARGO.md` §3.6 | yes |
| Helper script: one L6 career, 3 of 7 ended early, ~1.6× reading | `ENCARGO.md` §4; `docs/entrega/cut3-mv3/decision_report.md` §6 | yes |
| Uses only visible signals; observations marked "in our runs"; trust the game first | mv-3 SKILL.md "Published and ours" | yes |
| Different providers of the same model | `ENCARGO.md` §3.5, §5.4 | yes |
| About one career in four still falls, mostly at the start | Alejandro's slide 15; mv-3: 2 of 9 not completed, 1 at the first level | consistent (round wording, from the slide) |

| No scripts, no reference files; one Skill plus the manifest | docs/entrega/cut3-mv3/README.md and skills_design.md §2 | yes |
| The removed "never end a reply with text only" line is not in mv-3 | docs/entrega/cut3-mv3/README.md (changes since Cut 2); mv-3 manifest | yes |

Not said, on purpose (`ENCARGO.md` §7): event titles or game text, engine thresholds as rules, the replica as a source of rules, any claim about the official cut-3 score, Claude as a contributor.

**Small differences from Alejandro's notes:**
- slides 1, 6, 7, 11, 13–16 and 18 add detail;
- slide 13 adds the cut-2 example;
- slide 7 adds the five steps, which are in the Skill but not on the slide.

If a slide's text says otherwise, the slide wins: tell Alejandro.

---

## Cómo grabarlo en el Mac (Leah)

1. **Prepara la pantalla:**
   - Abre las diapositivas a pantalla completa (tecla `F` o el botón de pantalla completa) y comprueba que las flechas pasan de diapositiva.
   - Las notas **no** van en pantalla (la tecla `N` las enseña y saldrían en el vídeo): imprímelas o léelas en el móvil o en otra pantalla.
   - Activa **No molestar** (Centro de control → Concentración) y cierra el resto de apps.
2. **Si quieres salir en cámara** (el reglamento basta con una persona a cámara; las diapositivas son opcionales):
   - QuickTime Player → Archivo → Nueva grabación de película. Se abre la cámara.
   - Menú Visualización → **Flotar encima**.
   - Haz la ventana pequeña y ponla en una esquina de las diapositivas que no tape texto.
3. **Graba la pantalla con tu voz:**
   - Pulsa `Cmd + Shift + 5`.
   - Elige "Grabar toda la pantalla".
   - En **Opciones → Micrófono**, elige el micrófono (el del Mac o unos auriculares con micro; mejor en una habitación sin eco).
   - Pulsa **Grabar**, espera dos segundos y empieza.
   - Para parar, pulsa el botón de stop de la barra de menús. El vídeo se guarda en el Escritorio como `.mov`.
4. **Revísalo:**
   - Ábrelo y comprueba que se oye bien, que no salen las notas ni notificaciones, y que dura **menos de 10 minutos** (mejor 8–9).
   - Si te equivocas, es más fácil repetir la toma entera.
   - Para recortar el principio o el final: QuickTime → Edición → Recortar (`Cmd + T`).
5. **Conviértelo a `presentation.mp4`** en Terminal (`avconvert` viene con macOS):
   ```bash
   avconvert --preset Preset1920x1080 --source ~/Desktop/<nombre>.mov --output ~/Desktop/presentation.mp4
   ```
6. **Pásaselo a Alejandro.** Él reconstruye el ZIP del corte 3 con `scripts/entrega/build_cut.py ... --video <ruta>/presentation.mp4` (ENCARGO §8). El script comprueba la duración, y hay que subirlo antes de las **24:00 UK de hoy**.

**Consejos de voz:**
- Habla un poco más despacio de lo normal y haz una pausa al cambiar de pregunta.
- Lee de las notas, pero mira a la cámara en las frases marcadas (diapositivas 5, 12 y 16).
- Ensaya una vez en voz alta con cronómetro antes de grabar.
