# Speaker notes, final version (cut 3 video, mv-3)

Leah, 1 Nov 2026. Final script for Alejandro's 18-slide deck: shorter and easier to follow than the extended version ([speaker-notes-leah.md](speaker-notes-leah.md)), with the same facts. It still answers the five official questions in order. Every number comes from `ENCARGO.md` §4, and every claim about the Skill matches `lab/policies-src/mejora/mv-3/bundle/` and `docs/entrega/cut3-mv3/`; the source table is in the extended version, and the two differences are listed at the end.

*Italics are delivery notes, not to be read.* Length: 1,206 spoken words, about **8 min 35 s at 140 words per minute** (8.0 at 150, 9.3 at 130; limit 10). The times in brackets are where each slide should start.

---

### 1 · Title (0:00)
Hi, we are Gradient Depression. We never played a single move of this game. Our job was harder: to write the manual an AI reads before it lives an entire career. This is the story of that manual, and of what it taught us about AI.

*Calm, smiling. Pause after "an entire career".*

### 2 · The game (0:19)
Here is the game. An AI lives forty-eight months inside a company. It has visible scores: Skill, Network, Output, Health, Dignity and money. Every month it faces three situations and picks an answer, without seeing what that answer will change. Every quarter it spends a small budget of energy. And every six months comes a review: reach the bar, and you are promoted.

### 3 · Three ways to lose (0:46)
There are three ways to lose. Never get promoted, and you are fired. Let hidden trouble pile up, and it explodes; twice, and the career is over. Or burn out. And the AI never sees that hidden trouble. Its only clue is the tone of a monthly comment from HR.

So this is a game about reading signals, not numbers.

*Slow down on the last sentence: it is the thread of the whole video.*

### 4 · Our job (1:12)
And we do not play. We write the manual, called a Skill. The organisers run the AI with it three times. Eighty percent of the score is how those careers go. Ten percent is how much the AI has to read. Ten percent is how good the manual is. Every sentence has to earn its place.

### 5 · Question 1: design (1:36)
Question one: how did we design it?

First, we studied the game from the outside, using only the public tools and our own games. We built a practice copy that makes the same move as the real game ninety-nine times in a hundred. It became our lab: thousands of experiments, for free.

A lab, not a cheat sheet. Nothing from it goes into the manual.

### 6 · The real problem (2:04)
The lab told us where careers are won: at the reviews, decided by small story choices. Then we tested the model. It spotted eighty-three percent of the risky answers, but only about half of the answers that help it grow. That was the real bottleneck.

So our manual does not give answers. It teaches the AI how to read them: what usually costs Network, what usually costs Output, and what usually buries a problem.

### 7 · Three questions every time (2:36)
Every decision runs through three questions. What will this answer change? What does my career need right now? Which rule fits this moment?

Stories go through five ordered steps, from "survive" first to "grow" last. Quarters follow a short list where the first line that applies wins. And because the AI forgets, every note starts with one line of memory: months to the next review, scores now, and best scores at this level.

All of it lives in a single Skill. When we split it up, the AI read one part and lost the rest.

*Point at the three questions on the slide.*

### 8 · Question 2: the logs (3:16)
Question two: what did the logs teach us?

We submitted three times. Our first manual scored sixty-four point seven five. Our second fell to forty-five point four four. The third is mv-3, the one we present today; we do not know its score yet. Every change came from watching what the AI actually did.

### 9 · Lesson 1: lost by one point (3:39)
Lesson one. Again and again, the AI missed a promotion by a single point, lost in the last story before the review. So the manual now guards Network and Output in the two months before each review, and Skill too in the final month. It remembers its best scores, and repairs any loss at once.

### 10 · Lesson 2: nice answers, hidden trouble (4:03)
Lesson two. Some answers sounded responsible: a quiet private chat, a fix done bit by bit, an anonymous report. In the logs, those were exactly the ones that exploded later. Now the manual drops anything that might bury a problem. When in doubt, it is risky.

### 11 · Lesson 3: reading too much (4:23)
Lesson three. The AI was reading far too much. At every step it re-reads its whole history, so the cost grows with the square of the number of steps. The fix was fewer turns: act and look in a single reply, and after the first quarter, a whole quarter in one go.

Reading fell from about one point four million word pieces a month to about zero point six. Our efficiency score went from the sixties to the high nineties.

### 12 · Lesson 4: one sentence (4:57)
Lesson four, the one that surprised us most. In one career, the AI wrote its answer as text instead of acting, and the run was stopped. So we added one sentence telling it never to do that.

On paper, a fix. In real careers, a disaster: five of eleven ended early. Without that sentence, seven of nine finished, averaging seventy point one, and two reached level six.

Our guess, and it is only a guess: the sentence stopped the AI from thinking out loud. We took it out.

One sentence moved everything.

*The peak of the video. Slow down, pause, look at the camera on the last line.*

### 13 · Lesson 5: quick tests fooled us (5:36)
Lesson five. Quick tests fooled us. Three times, a cheap test said a change was better, and full careers said it was worse. Our second submission was one of them: two of its three careers sank at the very first level. So we built tests that replay the real start of a career, and in the end we trusted only full careers.

### 14 · Question 3: no scripts or extra files (6:03)
Question three: why no scripts or extra files?

They were allowed, as long as they use only what the game shows, and we tried one. It produced one brilliant career at level six. But three of its seven careers ended early, and it read about one point six times more.

A script can calculate. It cannot read a situation for the AI, and reading was our real problem. So: one manual, nothing else.

### 15 · Question 4: how general it is (6:34)
Question four: how general is it?

The manual uses only what the AI can see: HR's tone, the review talks, the menu of actions, the published calendar and its own notes. No event names. No secret answers. No hidden game numbers. Anything we only observed is marked as ours, and the AI trusts the game first. It also ran on different servers of the same model.

Its honest weak spot: about one career in four still falls, mostly at the start, where a single point decides the first promotion.

### 16 · Question 5: agents and Skills (7:12)
Question five: what did this teach us about agents and Skills?

A Skill is brilliant at changing how an agent works: its habits, its priorities, how much it reads. It is weak at changing what the agent understands. You can tell it to protect a score. You cannot make it see which answer costs that score. And a single sentence can change a whole career.

So a Skill gives an agent discipline, not understanding. And the only honest way to know what it does is to measure it, for real.

*The thesis. Look at the camera, not the slide.*

### 17 · The journey (7:51)
So that is our journey. We studied the game from the outside and built a lab. Our first manual scored sixty-four point seven five. We cut the reading. We stumbled, and learned to distrust quick tests. And by comparing full careers, we arrived at mv-3.

### 18 · mv-3 (8:10)
mv-3 is the manual behind our best careers: seventy point one on average in its finished practice careers, two of them at level six, with less than half the reading of our first version, and no secret answers inside. These career scores come from our own practice runs; only the two submission scores are official.

We are Gradient Depression. Thank you.

*Smile. Two seconds of silence before stopping.*

---

**Differences from the extended version** (same facts, shorter sentences):
- slide 2 introduces the six visible scores, so Network and Output are known before slide 6;
- "providers of the same model" became "servers of the same model";
- some details were dropped to save time: the cut-2 bench explanation (kept: two of three careers sank at the first level) and the late-review-talk safeguard.

Sources: same table as [speaker-notes-leah.md](speaker-notes-leah.md#check-against-the-sources). Recording guide: same file, last section.
