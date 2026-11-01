# Catálogo de preguntas por etapa (dev 1.0.8, 12885 partidas de bots)

Material de investigación. **No se copia a ninguna Skill ni se pasa a diseñadores.**

Columnas de cada respuesta: efecto fijo anunciado; `riesgo` = cambio relativo del comentario de RR. HH.; `expl3` = exceso de probabilidad de explosión en 3 meses frente a las demás respuestas; `→` = paso siguiente.

## An intern accidentally emails a rant about the manager

Aparece 4580 veces (primer paso): L1 57%, L2 13%, L3 11%, L4 13%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `d0e4a10f3649` (4907 veces): Intern Quinn accidentally sends "Chris changes his mind like a rollercoaster" to the whole 200-person department. Two minutes later Quinn is in tears at your desk: "What do I do? I can't recall it." Chris is on the thread and has already read it.
- 1. Go with Quinn to apologise to Chris in person straight away — network +2, dignity +1, health -1; riesgo -0.38; expl3 -0.21; → `22432e97c716` (n=1161)
- 2. Suggest sending a follow-up claiming the account was hacked — dignity -2; riesgo +0.91; expl3 +0.40; → `735ffae103c9` (n=376)
- 3. Stay out of it and leave Quinn to deal with it — network -2; riesgo -0.19; expl3 +0.06 (n=442)
- 4. Call IT first and ask whether the email can still be recalled — skill +2, dignity +2; riesgo -0.34; expl3 -0.25; → `1b60e9026be0` (n=1951)

**Paso** `22432e97c716` (2957 veces): Chris is silent for ten minutes, then says it must not happen again. Quinn gets a warning and keeps the internship.
- 1. Help Quinn write a proper wash-up — network +3, dignity +2, skill +1; riesgo -0.04; expl3 -0.05 (n=1681)
- 2. Step back and stay out — sin cambios; riesgo +0.04; expl3 +0.05 (n=554)

**Paso** `1b60e9026be0` (2433 veces): IT cannot recall it, but they suggest you go and apologise. You take Quinn to see Chris.
- 1. Go ahead with the apology — network +2, dignity +2; riesgo -0.65; expl3 -0.30; → `22432e97c716` (n=1500)
- 2. Go with the fake-hack story instead — sin cambios; riesgo +0.65; expl3 +0.30; → `735ffae103c9` (n=192)

**Paso** `735ffae103c9` (453 veces): IT shows the account was not hacked. You and Quinn are both investigated.
- 1. Admit you suggested the cover story — dignity +1, output -1; riesgo +0.20; expl3 +0.01 (n=267)
- 2. Blame Quinn — dignity -3, network -3; riesgo -0.20; expl3 -0.01 (n=180)

## The client praises a feature you did not build

Aparece 4578 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `586fc69e28b6` (4612 veces): In the Cedar Retail project review, the client’s procurement director says: “This real-time stock sync can forecast next week’s bestsellers. That’s ahead of the market.” What you actually shipped is next-day (T+1) batch sync, and forecasting is on next year’s roadmap. Kim, the product manager, catch
- 1. Say in the room that what is live is next-day sync, and forecasting is a later proposal — dignity +2, skill +1, network -1, output -1; riesgo -0.50; expl3 -0.06; → `f919cb29457e` (n=571)
- 2. Keep quiet in the room and clarify in writing after the meeting — dignity +1, skill +1; riesgo -0.82; expl3 -0.34 (n=2216)
- 3. Stay silent and let the review pass — output +2, network +2, dignity -2; riesgo +1.32; expl3 +0.40; → `762ff298d9d1` (n=956)

**Paso** `762ff298d9d1` (765 veces): The remaining payment comes in. Two months later the client finds there is no forecasting, and sends a solicitor’s letter alleging misrepresentation and asking for the money back.
- 1. Produce the review recording and the scope pack in your defence — dignity +1, output -2; riesgo -0.07; expl3 -0.23 (n=199)
- 2. Go along with sales and accept “poor communication” as the explanation — dignity -2, network +1; riesgo +0.07; expl3 +0.23 (n=555)

**Paso** `f919cb29457e` (510 veces): The client is taken aback and asks for a contract annex stating that forecasting is not part of this phase. The remaining payment is delayed. Kim says you do not know how to talk to clients.
- 1. Help sales revise the annex and push a phase-two forecasting proof of concept — skill +2, output +1, network +1, health -1; riesgo +0.01; expl3 -0.03 (n=258)
- 2. Stick to the accurate scope and stay out of the wrangling with sales — dignity +2, output -1, network -2; riesgo -0.01; expl3 +0.03 (n=225)

## A project you wanted going to someone else

Aparece 4544 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `82d4b8110ef5` (4680 veces): You are running a live project that needs your full attention. The timetable is tight, and you own the fallout if it goes wrong. Your manager has just started a new project you have wanted for a while, with a new framework and external visibility, but the slot went to your teammate Owen. Your manage
- 1. Accept the plan and give the live project your full attention — output +2, dignity +1, skill -1; riesgo -0.68; expl3 -0.12 (n=1219)
- 2. Ask your manager if you can join the new project part-time — network +1, output -1, skill +1, health -1; riesgo +0.35; expl3 +0.23; → `16b81625d0ab` (n=550)
- 3. Approach Owen privately: you supply the technical design, they stay the lead — network +2, skill +1, dignity -1; riesgo +0.33; expl3 -0.12; → `2fa0e56e4058` (n=1976)

**Paso** `2fa0e56e4058` (2328 veces): Owen agrees on the surface (“let's do it together”), but in updates outside the team they mostly put their own name on the work. Your manager praises Owen in the channel for “pushing the new direction hard”. You need to decide what to do next.
- 1. Clarify your actual contribution and what you want with your manager — dignity +2, network -1, output +1, skill +1; riesgo +0.23; expl3 -0.07 (n=1311)
- 2. Drop it and go back to focusing on the live project — output +2, health +1, network -2; riesgo -0.23; expl3 +0.07 (n=388)

**Paso** `16b81625d0ab` (467 veces): After some hesitation, your manager agrees you can spend 20% of your week on the new project, as long as the live work does not slip. Two weeks later the live project hits an integration blocker, and Owen also needs you at the new framework's review.
- 1. Prioritise the live project, pause the new work, and tell your manager — output +2, dignity +1, network -1; riesgo -0.57; expl3 -0.19 (n=238)
- 2. Carry both, working weekends to do it — skill +2, health -3, output +1; riesgo +0.57; expl3 +0.19 (n=203)

## After dinner, karaoke with someone on the promotion panel

Aparece 4519 veces (primer paso): L1 58%, L2 13%, L3 11%, L4 14%, L5 4%, L6 0%; meses 1–48 (mediana 7).

**Paso** `c146648a91af` (4625 veces): The Lynx team dinner is over. Helen, the HR business partner, who sits on the promotion committee, suggests going on to karaoke. You have a headache and want to go home. Nine people have already signed up in the channel, and only you and Lee have not. Helen tags you: “Come on — no work talk, just si
- 1. Go to the karaoke bar, keep your drinking in check, and join in — network +3, health -2; riesgo -0.04; expl3 -0.05; → `ca620a2683a8` (n=1422)
- 2. Decline politely and make sure you are sharp at the morning stand-up — health +2, output +1, dignity +1; riesgo +0.04; expl3 -0.06 (n=1719)
- 3. Show your face for half an hour, then leave — network +1, health -1, dignity +1; riesgo +0.00; expl3 +0.11; → `968e25fb5d70` (n=562)

**Paso** `ca620a2683a8` (1582 veces): You sing two songs. Helen says you are down to earth. At 1am she asks privately whether you are interested in Polaris — you cannot tell if it is drink talking.
- 1. Show interest and ask how to prepare for promotion — network +2, output +1; riesgo -0.07; expl3 -0.10 (n=949)
- 2. Talk about the project and leave promotion out, so it does not look transactional — network +2, skill +1, dignity +1; riesgo +0.07; expl3 +0.10 (n=226)

**Paso** `968e25fb5d70` (486 veces): You put in an appearance and leave. Helen texts: “Sensible to get some rest.” Someone on the team mutters that you do not mix.
- 1. Bring breakfast in the next day for the people who stayed — network +2, wealth -1; riesgo +0.03; expl3 +0.03 (n=247)
- 2. Offer no explanation and let your work speak for itself — output +2, network -1; riesgo -0.03; expl3 -0.03 (n=233)

## A colleague keeps @channel-ing questions already answered in the docs

Aparece 4513 veces (primer paso): L1 57%, L2 13%, L3 11%, L4 14%, L5 6%, L6 0%; meses 1–48 (mediana 7).

**Paso** `989377c65575` (4513 veces): In the main project channel, new joiner Tessa @channels questions several times a day that are clearly in the docs or a thirty-second search away. Plenty of people are tired of the pings. This time it's a question answered on the first page of the wiki.
- 1. DM her a doc link and suggest checking the wiki or asking the owner before using @channel — network +2, skill +1, dignity +1; riesgo -0.23; expl3 -0.22 (n=2552)
- 2. Call Tessa out in the channel: "Could you read the docs before asking?" — network -2, dignity -1; riesgo +0.49; expl3 +0.17 (n=560)
- 3. Ignore it like everyone else and leave the question hanging — network -1; riesgo -0.26; expl3 +0.04 (n=537)

## One umbrella, a downpour, and Jordan at going-home time

Aparece 4509 veces (primer paso): L1 56%, L2 14%, L3 10%, L4 15%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `bd24f8d08a0b` (4603 veces): A release ran late and you are finally leaving. Rain is hammering the glass and the Met Office has an amber warning out. In your drawer is a single folding umbrella you picked up from a hotel on a previous trip. Jordan, a teammate, has just stood up too, with no umbrella, and is staring towards the 
- 1. Offer to share the umbrella and walk to the station together — network +2, health -1, dignity +1; riesgo -0.03; expl3 -0.11; → `fbbc5dc173d9` (n=1305)
- 2. Lend Jordan the umbrella and make a dash through the rain for a cab — network +3, health -2, dignity +2, wealth -1; riesgo +0.04; expl3 +0.10 (n=419)
- 3. Suggest sharing a cab and splitting the fare — network +1, wealth -1, dignity +1; riesgo -0.01; expl3 -0.16 (n=1598)
- 4. Say the umbrella only covers one, so you will each make your own way — network -2; riesgo -0.00; expl3 +0.16 (n=386)

**Paso** `fbbc5dc173d9` (1378 veces): The umbrella is small and your shoulders still get wet. On the way Jordan talks about your manager squeezing the timetable lately, and they sound low. At the station they hesitate: “Want to grab a bowl of something hot near mine? On me.” The rain is getting heavier.
- 1. Accept, and listen to how the project is going — network +3, health -1, wealth +1; riesgo -0.02; expl3 -0.09 (n=773)
- 2. Decline and catch the last train home — network +1, health +1, dignity +1; riesgo +0.02; expl3 +0.09 (n=279)

## A former colleague at a competitor fishes for intel

Aparece 4508 veces (primer paso): L1 55%, L2 14%, L3 11%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `9ef86d653154` (4540 veces): Former colleague Felix has moved to Helios. He once referred you into this job. Over dinner he asks, "Has Lynx locked the team merger yet? What's the Polaris budget?" His contract forbids him from fishing for commercial information from people who still work here.
- 1. Refuse, and keep the chat to personal matters — dignity +2, network -1; riesgo -1.13; expl3 -0.38 (n=2330)
- 2. Share non-confidential industry gossip — network +1, dignity -1; riesgo +0.46; expl3 +0.10; → `d0bc6fbafd8a` (n=653)
- 3. Tell him about the draft merger plan, as a way of repaying the favour — network +2, dignity -3; riesgo +0.67; expl3 +0.27; → `49c605f69076` (n=681)

**Paso** `d0bc6fbafd8a` (585 veces): Felix pieces the merger together from other sources anyway. Helios goes after your clients with precisely targeted price cuts.
- 1. Tell compliance you may have overstepped the line — dignity +1, network -2; riesgo -0.79; expl3 -0.20 (n=282)
- 2. Stay silent — sin cambios; riesgo +0.79; expl3 +0.20 (n=269)

**Paso** `49c605f69076` (527 veces): InfoSec opens an investigation. Your call records with Felix are pulled.
- 1. Cooperate with the investigation — dignity +1, output -2; riesgo -0.89; expl3 -0.29 (n=274)
- 2. Deny it — dignity -3; riesgo +0.89; expl3 +0.29 (n=231)

## A dinner that is really a fishing trip for team gossip

Aparece 4507 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `0a9e3caf4970` (4528 veces): Sonya in Finance, who you barely speak to, takes you to dinner. After the third drink she starts: “I hear Lynx might be merged? Will your manager change? Who on your team might leave?” Her husband is a recruiter and posts on LinkedIn. What you actually know: there is a draft merger plan, not yet dec
- 1. Say you do not know, every time, and change the subject — dignity +2; riesgo -0.86; expl3 -0.32 (n=2541)
- 2. Keep to what is public, but hint that the team may change — network +1; riesgo +0.20; expl3 +0.02; → `300820081fbe` (n=559)
- 3. Tell her about the draft merger plan and that Leo may be moved — network +2, dignity -2; riesgo +0.66; expl3 +0.30; → `db4956f47d81` (n=569)

**Paso** `300820081fbe` (481 veces): Sonya is satisfied. A week later a recruiter contacts Leo. Your manager starts asking where it came from.
- 1. Admit you gave her a vague outline over dinner — dignity +1, network -2; riesgo -0.87; expl3 -0.21 (n=265)
- 2. Deny it — dignity -2; riesgo +0.87; expl3 +0.21 (n=209)

**Paso** `db4956f47d81` (423 veces): Leo is pulled in early and takes it badly. Your manager finds your name in the chat history.
- 1. Apologise and accept the reprimand — dignity +1, output -1; riesgo +0.01; expl3 -0.04 (n=214)
- 2. Say Sonya tricked it out of you — network -3, dignity -2; riesgo -0.01; expl3 +0.04 (n=200)

## Dismissed in a team meeting as "just engineering work"

Aparece 4496 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `b3cb36a36e7d` (4716 veces): In the weekly team meeting you present this quarter's reliability and performance work. Your manager listens and says, mildly, “This is basically just engineering work. If it runs, that's enough. It won't add much business value. Everyone knows that.” A few colleagues look at their screens and the r
- 1. Politely challenge that framing on the spot, with data and business impact — dignity +2, skill +2, network +1; riesgo +0.53; expl3 +0.20; → `b76a593aac7d` (n=629)
- 2. Let it go in the meeting and speak to your manager afterwards — dignity -1, network +1, output +1, health -1; riesgo -0.24; expl3 -0.02; → `150dfc3384c1` (n=712)
- 3. Let it pass in the room, then privately encourage colleagues and spell out what the work achieved — network +2, dignity +1, skill +1; riesgo -0.29; expl3 -0.18; → `d827bc6044d9` (n=2440)

**Paso** `d827bc6044d9` (2854 veces): You do not push back in the meeting. Afterwards you take a few colleagues for coffee and spell out the project's value and their part in it, and morale lifts. Your manager does not raise it again, and does not correct the remark in public either. You need to decide whether to take the point further.
- 1. Use the next meeting's pre-read to put business value in a summary your manager will see — skill +2, output +1, dignity +1; riesgo -0.48; expl3 -0.17 (n=1744)
- 2. Keep encouraging colleagues privately and do not raise it with your manager again — network +3, dignity +1; riesgo +0.48; expl3 +0.17 (n=334)

**Paso** `150dfc3384c1` (613 veces): Afterwards you book fifteen minutes with your manager and show how the work maps to business metrics. They soften: “Next time, put the business value on page one.” You still sense the rest of the team thinks engineering work does not count. You need to decide whether to fight for the team's visibili
- 1. Push to get your work into team OKRs or the quarterly highlights — output +2, network +2, skill +1, health -1; riesgo +0.07; expl3 -0.05 (n=371)
- 2. Keep to your own patch and stop speaking for the team — output +1, network -1, health +1; riesgo -0.07; expl3 +0.05 (n=227)

**Paso** `b76a593aac7d` (557 veces): You list SLA gains, a lower incident rate and fewer client complaints. Your manager pauses: “I have seen the data. Time is tight in the meeting. Next time, frame the update in business language.” Someone messages you afterwards: “Glad someone finally said it.” That afternoon your manager calls you i
- 1. Reframe updates in business language, but keep the technical value in the write-up — skill +2, output +1, network +1, dignity +1; riesgo -0.50; expl3 -0.21 (n=331)
- 2. Keep speaking up for engineering value in public and accept the political friction — dignity +2, network +2, output -1; riesgo +0.50; expl3 +0.21 (n=206)

## Raising a technical objection on another team's API design

Aparece 4496 veces (primer paso): L1 56%, L2 14%, L3 11%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `2df0b2cd5662` (4672 veces): While reviewing a downstream API design from a neighbouring team, your own load tests flag a likely bottleneck: at peak, once QPS doubles, tail latency could jump from 50ms to around 800ms and threaten your SLA. Their design has already passed their internal review. The owner is a well-regarded seni
- 1. Comment publicly on the shared design doc, with the load-test data attached — skill +2, output +1, network -2; riesgo -0.49; expl3 -0.12; → `5b47e404352f` (n=2828)
- 2. Take their owner aside for a 1:1 and walk through the load-test results privately — network +2, skill -1, output -1; riesgo +0.49; expl3 +0.12; → `688b3634ff34` (n=909)

**Paso** `5b47e404352f` (3146 veces): Both teams see your comment. Their owner replies: "Thanks for the data — there is a risk, but the timetable is tight. Let's ship as designed and watch it in a canary." Your manager also tags you: "Be careful how you raise things in public. They have a reputation to protect." You need to decide wheth
- 1. Insist on a pre-launch fix and attach a complete proposed patch — skill +2, output +1, network -1; riesgo -0.59; expl3 -0.06 (n=1626)
- 2. Accept the canary plan and add monitoring and a rollback playbook — network +2, skill -1, output -1; riesgo +0.59; expl3 +0.06 (n=817)

**Paso** `688b3634ff34` (849 veces): Their owner thanks you for the private heads-up, admits it was an oversight, and is willing to change the design. They add, offhand: "Let's keep this between us — no need to air it in the channel, or it will look as if our review missed it." You need to decide whether to share the finding with the w
- 1. Agree the fix in the 1:1, then record the problem and the decision in the design doc — network +2, skill -1, output -1; riesgo +0.61; expl3 +0.20 (n=285)
- 2. Anonymise it as a "performance review lesson" and share it with both teams — skill +2, output +2, network -2; riesgo -0.61; expl3 -0.20 (n=475)

## Vaping at the neighbouring desk

Aparece 4494 veces (primer paso): L1 57%, L2 14%, L3 11%, L4 15%, L5 4%, L6 0%; meses 1–48 (mediana 7).

**Paso** `8fad09397a68` (4494 veces): After lunch, Robin at the next desk is vaping again. The cloud hangs over the open plan. The office rule is no vaping inside. You were hoping to concentrate this afternoon.
- 1. Smile and quietly remind him vaping inside isn't allowed and the shelter is downstairs — dignity +1, network +1, skill +1; riesgo -0.50; expl3 -0.27 (n=2512)
- 2. Frown and put up with it without saying anything — health -1, dignity -1; riesgo +0.20; expl3 +0.14 (n=552)
- 3. Post a snide note in the channel: "some people might show a bit of consideration" — network -2, dignity -1; riesgo +0.31; expl3 +0.13 (n=540)

## How blunt to be in a code-review comment

Aparece 4489 veces (primer paso): L1 56%, L2 14%, L3 11%, L4 14%, L5 4%, L6 1%; meses 1–48 (mediana 7).

**Paso** `55ea7ab10ab8` (4489 veces): Priya, who has just joined, opens her first merge request. The design is clearly wrong. You can write in the review that this will blow up in production, or you can ask questions until she sees it herself. The team's culture is fairly direct, and HR has just started talking about psychological safet
- 1. Name the problem directly and mark it as must-fix — skill +1, dignity +1, network -1; riesgo -0.30; expl3 -0.00 (n=964)
- 2. Use questions so she spots the issue herself — skill +1, network +2, output -1; riesgo -0.25; expl3 -0.09 (n=1821)
- 3. Approve it, and explain on Slack afterwards — network +1, dignity -1; riesgo +0.55; expl3 +0.09 (n=835)

## A metrics problem, ten minutes before the briefing

Aparece 4485 veces (primer paso): L1 56%, L2 14%, L3 10%, L4 15%, L5 4%, L6 0%; meses 1–48 (mediana 7).

**Paso** `fe69155b8239` (4669 veces): The department’s quarterly review starts in ten minutes. You have just checked the Nebula Growth dashboard. Slide 7 of your manager’s pack says “MAU up 38% month on month”, but that figure mixes trial accounts in with paying users. The external definition counts paying MAU only, which gives +12%. Th
- 1. Quietly point out the definition problem now and suggest correcting it in the room — dignity +2, skill +1; riesgo -0.76; expl3 -0.33; → `e4d9556b8ea5` (n=2687)
- 2. Hold off for now and email privately after the meeting — dignity +1, network +1; riesgo +0.13; expl3 +0.13 (n=531)
- 3. Say nothing and let the briefing run — network +2, dignity -2; riesgo +0.63; expl3 +0.20 (n=535)

**Paso** `e4d9556b8ea5` (3054 veces): Your manager’s face tightens. They drop the slide and go with +12%. The VP asks why it is lower than the figure in last week’s comms. Afterwards your manager says: “Check this a day ahead next time.”
- 1. Offer to follow up with the VP on how the metric is defined — skill +2, dignity +2, network +1, health -1; riesgo +0.03; expl3 -0.00 (n=1394)
- 2. Leave it there so your manager is not made to look small — network +1; riesgo -0.03; expl3 +0.00 (n=897)

## Who picks up the bill at a client lunch

Aparece 4484 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `d5435f95e2de` (4484 veces): You have taken a client out for a work lunch. As it winds down they say, "Let me get this," and make a move for the bill. This is ordinary client entertaining, so your side is meant to pay. How do you handle the moment?
- 1. Having already paid quietly at the desk, say, "This one's on us. You can host next time" — network +2, dignity +1, skill +1; riesgo -0.27; expl3 -0.24 (n=2551)
- 2. Wrestle over the bill at the table until it gets awkward — dignity -1; riesgo -0.17; expl3 +0.07 (n=541)
- 3. Go along with it and let the client pay — network -1, dignity -1; riesgo +0.44; expl3 +0.17 (n=527)

## A chatty, skiving colleague eating into your time

Aparece 4483 veces (primer paso): L1 56%, L2 14%, L3 11%, L4 14%, L5 4%, L6 0%; meses 1–48 (mediana 7).

**Paso** `74d9a35755c8` (4652 veces): Luke, a teammate, has taken to hovering at your desk for half-hour chats: gossip, moaning, memes. You can tell their own workload is light and they mostly want someone to skive with. You have a critical module due for QA today and have already been interrupted three times. You need to decide how to 
- 1. Tell them directly but politely that you need to focus today and to come back later — dignity +2, output +1, network -1, health +1; riesgo -0.32; expl3 -0.06; → `87419cb48b1b` (n=558)
- 2. Put headphones on, look busy, and give them the cold shoulder — output +1, network -2; riesgo -0.02; expl3 +0.07 (n=432)
- 3. Chat for a few minutes, then steer back to work and mention today's deadline — network +1, health -1; riesgo -0.21; expl3 -0.23; → `286812cbad17` (n=2350)
- 4. Tell your manager that Luke keeps breaking your concentration — output +2, network -3, dignity +1; riesgo +0.55; expl3 +0.22 (n=376)

**Paso** `286812cbad17` (2802 veces): Luke takes a hint, but in the afternoon they bring snacks and want to "eat and chat". Today's QA deadline is still closing in.
- 1. Turn down the snack session firmly and suggest lunch another day — dignity +1, output +2, health +1; riesgo -0.35; expl3 -0.16 (n=1841)
- 2. Give in, chat for a quarter of an hour, and catch up in the evening — network +2, output -1, health -2; riesgo +0.35; expl3 +0.16 (n=180)

**Paso** `87419cb48b1b` (510 veces): Luke pauses, says "fair enough", and leaves you alone that day. Over the next few days, though, they tell others at the tea point that "someone has gone rather chilly". You need to decide whether to repair the relationship.
- 1. Spend ten minutes with them at lunch explaining the boundary and that you mean no ill will — network +2, dignity +1; riesgo +0.07; expl3 -0.07 (n=327)
- 2. Offer no explanation and keep focusing on the work — output +2, network -1, dignity +1; riesgo -0.07; expl3 +0.07 (n=173)

## A collaborator shifts the blame in a meeting

Aparece 4482 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `96938b0a0a7b` (4672 veces): You and Chloe share delivery on a client project. In the weekly meeting the client complains about repeated API changes and thin test coverage. Chloe speaks first: “The API design was mainly theirs. I worked to the version they gave me. Testing was held up on their team too.” In fact the changes cam
- 1. Walk through the timeline and the email trail, and set out who owned what — dignity +2, skill +1, network -1; riesgo -0.45; expl3 -0.23; → `a584dd5abf77` (n=2149)
- 2. Take some of the blame for now to steady the client, and leave Chloe for later — network +1, dignity -2, output +1; riesgo +0.59; expl3 +0.25; → `eb3949a16468` (n=509)
- 3. Hit back in the room: Chloe did not provide the integration environment on time — dignity +1, network -3, output -1; riesgo +0.35; expl3 +0.09; → `6f83d26ea9d8` (n=394)
- 4. Stay silent and ask your manager to unpick it — dignity -1, output -1; riesgo -0.49; expl3 -0.11; → `fe17b4acc2cc` (n=707)

**Paso** `a584dd5abf77` (2557 veces): The emails show the client and your manager exactly how the changes came about. Chloe looks grim. Afterwards your manager tells you and Chloe to “sort it between yourselves”. The client wants a joint improvement plan this week.
- 1. Draft a joint improvement plan, copy your manager, and invite Chloe to co-author it — output +2, network +1, skill +1, dignity +1; riesgo -0.12; expl3 -0.14 (n=1623)
- 2. Write only your own part and make clear where it ends — dignity +2, output +1, network -2; riesgo +0.12; expl3 +0.14 (n=204)

**Paso** `fe17b4acc2cc` (625 veces): Your manager papers over it, but the client is not satisfied. Your manager asks why you did not explain in the room.
- 1. Reply to the email at once with the facts, and take ownership of the fixes — skill +1, output +1, dignity +1, health -1; riesgo -0.04; expl3 -0.14 (n=440)
- 2. Excuse it as "not the moment to speak" — network -2, dignity -2, output -1; riesgo +0.04; expl3 +0.14 (n=181)

**Paso** `eb3949a16468` (454 veces): The client eases off, seeing you as someone who will own it. Afterwards Chloe says, "Cheers — lunch on me next time." Your manager privately reminds you to "watch how you communicate next time".
- 1. Fill your manager in on the facts so you do not become the permanent fall guy — dignity +1; riesgo -0.30; expl3 -0.27 (n=238)
- 2. Swallow it and do not pursue it — network +1, dignity -3; riesgo +0.30; expl3 +0.27 (n=172)

**Paso** `6f83d26ea9d8` (345 veces): You and Chloe air each other's failings in the meeting. The client frowns. Your manager cuts in: "Solve the problem first — don't bicker." Afterwards they speak to each of you separately.
- 1. Apologise to your manager and submit a plan for working together better — network +1, output +1, dignity -1, skill +1; riesgo +0.05; expl3 -0.05 (n=184)
- 2. Insist Chloe shifted the blame first and ask your manager for a fair ruling — dignity +1, network -2, output -1; riesgo -0.05; expl3 +0.05 (n=159)

## Whether to invest in a CI automation suite

Aparece 4482 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 15%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `6e91406739d1` (4650 veces): Your team still lacks a proper automated-test CI pipeline. Every release depends on senior engineers manually reviewing critical paths. Your manager wants you to lead the platform work. Headcount has just doubled from five to ten. New joiners' PRs have piled up, review pressure has spiked, and relea
- 1. Spend two weeks building a full CI automation suite — skill +3, output -2, network -1; riesgo -0.72; expl3 -0.17; → `ab5f34d4cbe1` (n=2566)
- 2. Keep manual review and let new joiners follow the existing process — output +2, network +1, skill -1, health -2; riesgo +0.72; expl3 +0.17 (n=1197)

**Paso** `ab5f34d4cbe1` (2831 veces): CI goes live and the team's merge speed improves markedly. New joiners find the configuration harder than expected, though, and the last two PRs sat blocked for hours. A senior colleague suggests loosening the gates so people can get used to the workflow, then tightening them later. You need to deci
- 1. Keep the strict gates and make the team meet the higher bar — skill +2, output -1, network -2; riesgo -1.10; expl3 +0.00 (n=605)
- 2. Loosen the thresholds so the team can ease into the CI workflow — network +2, output +1, skill -1; riesgo +1.10; expl3 -0.00 (n=1597)

## Forgetting to water the office plants on your rota

Aparece 4481 veces (primer paso): L1 56%, L2 13%, L3 10%, L4 14%, L5 6%, L6 0%; meses 1–48 (mediana 7).

**Paso** `9a1fc53ea201` (4481 veces): Facilities has you on the rota to water the communal plants this week. You got busy and forgot. On Wednesday, Facilities pings you: the plants are almost dead.
- 1. Water them today and set a calendar reminder — dignity +1, network +1; riesgo -0.04; expl3 -0.00 (n=865)
- 2. Apologise and ask a colleague to cover this once — network +1; riesgo -0.06; expl3 -0.12 (n=2239)
- 3. Treat it as too small to matter — network -1, dignity -1; riesgo +0.09; expl3 +0.12 (n=519)

## The colleague who buys coffee is collecting favours for a lead vote

Aparece 4477 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 13%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `0eb42f1c2467` (4584 veces): Harvey brings the team coffees from Pret every day and never takes money. You notice a notebook: “Favours ledger: Chris +2, Ethan +1…” The team is about to pick an acting lead, and Harvey is standing. Today he hands you a larger coffee: “Put in a word for me at the review tonight?”
- 1. Refuse to campaign. In the review, stick to the facts — dignity +2, network -2; riesgo -0.16; expl3 +0.10 (n=418)
- 2. Agree to talk him up, in return for later support — network +2, dignity -2; riesgo +0.57; expl3 -0.07; → `df176d515a61` (n=1351)
- 3. Warn your manager privately that someone is trading favours for support — dignity +1, network -3, skill +1; riesgo -0.14; expl3 +0.10 (n=423)
- 4. Start buying coffees yourself and join the favours game — wealth -2, network +1, dignity -1; riesgo -0.27; expl3 -0.12 (n=1486)

**Paso** `df176d515a61` (1428 veces): Harvey is named acting lead and puts you on weekend on-call.
- 1. Take the on-call and keep the relationship — network +1, health -2, dignity -1; riesgo +0.03; expl3 -0.06 (n=802)
- 2. Refuse and draw a line — dignity +2, network -2; riesgo -0.03; expl3 +0.06 (n=323)

## A manager-free channel shares a screenshot of your boss

Aparece 4473 veces (primer paso): L1 58%, L2 13%, L3 10%, L4 13%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `601bc0a5175e` (4477 veces): In the Lynx late-night Slack channel, where no managers are allowed, someone posts a screenshot of Chris tearing into people: "If you can't even do this, what bonus do you think you deserve?" The next message: "Thoughts? Should we reply as a group?" You're in the channel. Passing a copy to HR, a sta
- 1. Ask them to stop spreading it, keep the evidence the target needs, and raise it through a grievance or staff rep — dignity +2, network +1; riesgo -0.51; expl3 -0.30 (n=2315)
- 2. Join in and have a moan — network +2, dignity -1; riesgo +1.26; expl3 +0.42; → `1fe4d614ba24` (n=414)
- 3. Leave the channel and stay out of it — dignity +1, network -2; riesgo -0.64; expl3 -0.05 (n=412)
- 4. Message Chris privately about team morale, without saying how you know — dignity +1, skill +1; riesgo -0.10; expl3 -0.07 (n=482)

**Paso** `1fe4d614ba24` (328 veces): You joined the mockery aimed at Chris himself, and the thread, with the screenshot and the jokes, was forwarded into channels that have nothing to do with the complaint. IT traces the chain. Handing the screenshot to HR, a representative, a union or a solicitor for the complaint is not part of what 
- 1. Own up that you joined in — dignity +1, network -2; riesgo -0.35; expl3 -0.20 (n=155)
- 2. Deny it — dignity -3; riesgo +0.35; expl3 +0.20 (n=162)

## A newly hired VP talks to you alone for ten minutes on day one

Aparece 4470 veces (primer paso): L1 57%, L2 13%, L3 11%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `e79bb72a3d10` (4649 veces): Hale, a newly hired group VP, tours the Lynx floor, stops at your desk and asks how the payments circuit breaker works. You talk for ten minutes. Afterwards colleagues mutter about whether your manager is being replaced and whether you are about to shoot up the ladder. Tara turns polite and distant.
- 1. Brief Chris on Hale's questions and your answers — network +2, dignity +2; riesgo -0.39; expl3 -0.09 (n=653)
- 2. Don't make a fuss, and keep delivering as normal — output +2, dignity +1; riesgo -0.57; expl3 -0.30; → `e895c77e599a` (n=2521)
- 3. Quietly take Hale's team out to lunch to build on the impression — network +1, dignity -1; riesgo +0.96; expl3 +0.39; → `a955c62d2667` (n=545)

**Paso** `e895c77e599a` (2902 veces): Two weeks later Hale does not follow up one-to-one. The gossip cools. Chris is back to normal.
- 1. Let your project results strengthen your position — output +2, skill +1; riesgo -0.08; expl3 -0.13 (n=1905)
- 2. Moan that it was a nine-day wonder — network -2, dignity -1; riesgo +0.08; expl3 +0.13 (n=238)

**Paso** `a955c62d2667` (453 veces): The lunch lands. Chris finds out and warns you not to go over his head. Hale does not seek you out again either.
- 1. Apologise to Chris — network +1; riesgo -0.04; expl3 -0.20 (n=242)
- 2. Keep going round him — network -3; riesgo +0.04; expl3 +0.20 (n=206)

## Escape room: your manager is slowing you down, a quiet colleague is flying

Aparece 4466 veces (primer paso): L1 56%, L2 14%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `c0119ebd042a` (4473 veces): Company escape room: The 1948 Files. Chris, your manager, insists on directing and is all over the place, retrying the same wrong codes. Quinn, usually quiet in testing, has just solved three puzzles in a row. Fifteen minutes left, one lock from the exit, and Chris is about to guess again.
- 1. Ask Quinn to take the lock, and tell Chris: “You keep the big picture” — network +2, skill +1, dignity +1; riesgo -0.21; expl3 -0.25 (n=2520)
- 2. Say outright that Chris’s approach is wrong — dignity +2, network -3; riesgo -0.15; expl3 +0.07 (n=532)
- 3. Follow Chris’s guesses so he is not made to look small — network +1, dignity -2; riesgo +0.36; expl3 +0.17; → `ed337e5b57b4` (n=541)

**Paso** `ed337e5b57b4` (465 veces): You run out of time and finish last. The venue ranks you bottom. Chris says he was “not on it today.”
- 1. In the debrief, name Quinn’s contribution — network +2, skill +1, dignity +1; riesgo -0.09; expl3 -0.03 (n=234)
- 2. Say nothing — sin cambios; riesgo +0.09; expl3 +0.03 (n=226)

## Forced ranking: scoring a colleague who is also a friend

Aparece 4466 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `1f27ca8a00ca` (4620 veces): It is time for year-end 360 reviews, and the department uses a forced A/B/C split (20% / 60% / 20%). You have to rate Ethan, a friend who has babysat for you and trains with you. But he carried about 30% of the blame for a Lynx Wallet incident this year, and his output has been ordinary. An A for hi
- 1. Give him a fair B and write clear points for improvement — dignity +2, skill +1, network -2; riesgo -0.37; expl3 -0.17; → `9d6837da9d35` (n=1818)
- 2. Give him an A, taking the slot from a colleague you know less well — network +2, dignity -2; riesgo +0.92; expl3 +0.18; → `b526a7bdc370` (n=587)
- 3. Give him a C, because the incident has to show in the rating — dignity +1, network -3; riesgo -0.43; expl3 +0.09; → `0e28adfafed4` (n=445)
- 4. Recuse yourself and ask your manager to have someone else rate Ethan — dignity +1; riesgo -0.12; expl3 -0.10 (n=871)

**Paso** `9d6837da9d35` (2187 veces): Ethan’s bonus is in the normal range. Privately he says he understands. In calibration your manager uses your comments and asks him to write up the incident.
- 1. Help Ethan rework the write-up and keep the friendship — network +2, skill +1, output +1; riesgo -0.12; expl3 -0.14 (n=1367)
- 2. Keep your distance and stay strictly professional — dignity +1; riesgo +0.12; expl3 +0.14 (n=192)

**Paso** `b526a7bdc370` (472 veces): The colleague who lost the slot raises it with HR. HR look at the evidence and ask whether you rated him as a favour.
- 1. Admit the rating was too generous — dignity +1, network -1; riesgo -0.18; expl3 -0.28 (n=306)
- 2. Insist Ethan deserved an A — network -2, dignity -2; riesgo +0.18; expl3 +0.28 (n=150)

**Paso** `0e28adfafed4` (390 veces): Ethan’s bonus is roughly halved. He blocks you for three months. Some people on the team call you tough.
- 1. Try to explain the constraints of the rating system — network +1; riesgo +0.05; expl3 -0.01 (n=195)
- 2. Accept that the friendship is over — dignity +1, network -2; riesgo -0.05; expl3 +0.01 (n=192)

## Another department’s major incident: do you volunteer?

Aparece 4465 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `0adf8ea56cf9` (4531 veces): The payments clearing centre had a P0 incident last night: a ledger service, unrelated to Halcyon Tech, is posting rubbish. Platform Engineering owns it, and your Lynx Payments team is not in the firing line. The platform director tags every payments tech lead in the leadership channel: “If you know
- 1. Volunteer for the incident team — network +3, skill +2, health -3, output -2, dignity +1; riesgo -0.06; expl3 -0.07; → `d674ff2c9f08` (n=1144)
- 2. Offer two hours of remote Q&A in the channel, but do not join on site — skill +1, network +1, dignity +1; riesgo +0.00; expl3 -0.11 (n=1938)
- 3. Stay quiet and stick to your own work — output +2, network -2; riesgo +0.06; expl3 +0.17 (n=578)

**Paso** `d674ff2c9f08` (1059 veces): It takes seven straight days to restore the ledger. The CEO praises the payments team for showing up. The membership-benefits proposal slips and the client complains.
- 1. Ask your manager for extra people on the benefits proposal in return — dignity +2, output +1, network +3; riesgo -0.06; expl3 +0.02 (n=692)
- 2. Work late to catch up on the proposal yourself, without asking for anything — output +2, health -3; riesgo +0.06; expl3 -0.02 (n=164)

## Whether to join a cross-team architecture review — and how hard to push

Aparece 4462 veces (primer paso): L1 55%, L2 13%, L3 11%, L4 15%, L5 4%, L6 1%; meses 1–48 (mediana 7).

**Paso** `a6ec66a39db6` (4643 veces): The department tech committee is holding a cross-team architecture review next week, covering next-quarter rebuilds of several core services. Reviewers get a vote and share responsibility for the outcome later. You have been invited as a cross-team reviewer (you have a lot of experience with API per
- 1. Accept, read the docs properly, and prepare comments — skill +2, network +3, output -2, health -1; riesgo +0.01; expl3 -0.08; → `bf15b3541d28` (n=2635)
- 2. Decline and keep the time for your own team's delivery — output +2, skill -1, network -2, health +1; riesgo -0.01; expl3 +0.08 (n=1076)

**Paso** `bf15b3541d28` (2961 veces): You go in deep and raise a core objection to one design: they plan to introduce a framework that has not been used at scale inside the company, which carries a maintenance risk. Their owner disagrees in the meeting, fairly bluntly. The chair suggests you carry on the discussion afterwards. You need 
- 1. Write a full risk assessment and submit it formally to the tech committee — skill +2, network -1, output -1, dignity +1; riesgo -0.88; expl3 -0.04 (n=827)
- 2. Defer to their judgement and file your comments as an appendix — network +2, output +1, skill -1; riesgo +0.88; expl3 +0.04 (n=1396)

## A colleague hogging the printer

Aparece 4460 veces (primer paso): L1 57%, L2 14%, L3 11%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `3b7f405b90f7` (4460 veces): You need a short meeting pack printed now. Quentin is using the shared printer for a hundred-odd pages of personal material, checking each page as it comes out, with no sign of letting anyone in. You are short of time.
- 1. Explain politely that you have something urgent and ask to jump in for two pages — dignity +1, network +1, output +1; riesgo -0.32; expl3 -0.21 (n=2535)
- 2. Walk over, cancel his job and print yours first — output +1, network -2, dignity -1; riesgo +0.53; expl3 +0.19 (n=537)
- 3. Wait in silence while the meeting starts without you — output -1, dignity -1, health -1; riesgo -0.21; expl3 +0.01 (n=558)

## Going for a valuable certification that takes months

Aparece 4455 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `25a609bfc7e1` (4455 veces): There is a well-regarded certification in the industry that would help your career, but preparing for it would take months of evenings and weekends. The exam fee is not cheap either. You are not sure whether to start now.
- 1. Set a steady revision plan over several months, broken into daily tasks you can finish — skill +2, dignity +1, health -1; riesgo -0.23; expl3 -0.18 (n=2256)
- 2. Sign up, then study in fits and starts, and cram at the last minute — health -1, wealth -1; riesgo +0.44; expl3 +0.19 (n=543)
- 3. Drop the idea because it looks too hard — health +1, skill -1, dignity -1; riesgo -0.21; expl3 -0.00 (n=822)

## A request to swap on-call over a peak trading bank holiday

Aparece 4454 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `72e498369fda` (4454 veces): The bank-holiday on-call rota is out. Owen has a family matter and wants to swap with you. That would put you on cover for the three highest-risk days of the break in a row, during peak trading, when alerts are much more likely. Taking it would really help the team, and Owen would owe you. But three
- 1. Take the consecutive shifts and cover the three peak-trading days — network +1, output +1, health -2, dignity +1; riesgo -0.07; expl3 -0.10 (n=2687)
- 2. Decline the swap and ask your manager to rebalance by the rules — health +2, network -1, output -1; riesgo +0.07; expl3 +0.10 (n=932)

## An engagement survey that asks for your staff ID

Aparece 4452 veces (primer paso): L1 58%, L2 13%, L3 9%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `7ada24db9b30` (4601 veces): The annual engagement survey says answers are confidential. The portal asks for your staff ID and an SMS code, which may only be there to stop someone submitting twice. The page does not say whether anyone can later trace an answer back to you. You have a long list on Chris, your manager: goalposts 
- 1. Fill it in honestly, with examples and no swearing — dignity +2; riesgo +1.06; expl3 +0.35; → `b3f7d30c02d4` (n=549)
- 2. Score everything as blandly positive — network +1, dignity -2; riesgo -0.82; expl3 -0.10 (n=758)
- 3. Set out the moving goalposts, the credit-taking and the weekend messages as plain facts, without insults — dignity +1, skill +1; riesgo -0.24; expl3 -0.24; → `79970c0e0631` (n=2392)

**Paso** `79970c0e0631` (2880 veces): HR pass on “please set dates more clearly” to Chris. He tries two weeks of stand-ups to fix it.
- 1. Acknowledge the improvement in the meeting so that it sticks — network +2, output +1, dignity +1; riesgo -0.04; expl3 -0.07 (n=1637)
- 2. Wait and see — sin cambios; riesgo +0.04; expl3 +0.07 (n=456)

**Paso** `b3f7d30c02d4` (445 veces): A month later Chris books a 1:1: “Someone said you’ve got an issue with me.” He does not know if it came from the survey.
- 1. Tell him face to face what you actually need — dignity +2, health -1; riesgo -0.03; expl3 -0.07 (n=219)
- 2. Deny it and say it may be a misunderstanding — sin cambios; riesgo +0.03; expl3 +0.07 (n=222)

## A senior puts their name on an intern’s work

Aparece 4442 veces (primer paso): L1 57%, L2 13%, L3 10%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `2aec8a18e126` (4625 veces): During an Aurora reporting sprint, senior engineer Rowan puts the SQL work and visualisation templates of Quinn, the intern, into the weekly update under his own name. Quinn is listed as having “assisted”. Quinn comes to you in tears, too scared to take on Rowan, who trained with your manager. The r
- 1. Name Quinn’s specific contribution in the meeting that finalises the slides — dignity +2, network -2, skill +1; riesgo -0.51; expl3 -0.09; → `29693d725de0` (n=399)
- 2. Ask Rowan privately to correct the credit — dignity +1; riesgo -0.42; expl3 -0.29; → `ce19f6fbc898` (n=2557)
- 3. Tell Quinn to take it to your manager themselves — network -1; riesgo +0.13; expl3 +0.10 (n=412)
- 4. Stay out of it to avoid annoying Rowan — network +1, dignity -3; riesgo +0.80; expl3 +0.28 (n=374)

**Paso** `ce19f6fbc898` (2922 veces): Rowan says “it’s team output, we don’t divide it,” and refuses to change it. Quinn looks at you, disappointed.
- 1. Send the weekly update and the git history to your manager — dignity +2, skill +1, network -1; riesgo -0.46; expl3 -0.05 (n=1705)
- 2. Drop it — dignity -2; riesgo +0.46; expl3 +0.05 (n=497)

**Paso** `29693d725de0` (364 veces): Rowan turns on you in the room. Your manager tells you to “sort it afterwards.” Quinn’s name is added. Rowan freezes you out.
- 1. Walk your manager through the facts and ask for a fair rating — dignity +2; riesgo +0.03; expl3 -0.02 (n=162)
- 2. Take on some of Rowan’s work to thaw the relationship — network +2, output -1, health -1, dignity -1; riesgo -0.03; expl3 +0.02 (n=177)

## The person next to you wears very strong perfume

Aparece 4441 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `dd42ec7d098d` (4441 veces): Your new neighbour wears very heavy perfume. A morning of it has given you a headache. She clearly loves it, and even asks, "Nice, isn't it?" Saying no might hurt her feelings, but putting up with it is miserable.
- 1. Tell her gently that strong scent gives you headaches, and ask if she could wear less — dignity +1, network +1, health +1; riesgo -0.45; expl3 -0.24 (n=2517)
- 2. Praise it insincerely and keep sitting there with a headache — health -1, dignity -1; riesgo +0.22; expl3 +0.12 (n=553)
- 3. Turn to other colleagues and moan that she "stinks the place out" — network -2, dignity -1; riesgo +0.23; expl3 +0.12 (n=521)

## Choosing a path for a legacy service hitting its limits

Aparece 4433 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `19b8d4428dfd` (4433 veces): A core order service you own has been live for three years and is reaching its performance limit. Monitoring shows QPS already at 80% of the original design limit, and in another quarter or two normal growth will probably overwhelm it. Your manager has given you three months to propose a path, witho
- 1. Rewrite on a modern framework as a three-to-five-year foundation — skill +1, output -1, health -2; riesgo +0.06; expl3 +0.13 (n=530)
- 2. Refactor in stages on the current architecture — skill +2, output +1, health -1; riesgo -0.01; expl3 -0.18 (n=2411)
- 3. Ship the smallest performance patches and ride out this cycle — output +1, skill -1, health +1; riesgo -0.04; expl3 +0.05 (n=653)

## An unpublished restructure, and a friend about to buy a flat

Aparece 4433 veces (primer paso): L1 57%, L2 13%, L3 11%, L4 14%, L5 4%, L6 1%; meses 1–48 (mediana 7).

**Paso** `9cba42517174` (4458 veces): You were copied on a restricted leadership note: a draft Q2 reorganisation. Lynx may be folded into Falcon Recs, with about 15% fewer roles. Nothing has been announced. Over dinner last night your friend and colleague Sienna said she wants to put in an offer on a flat, with the deposit already saved
- 1. Hint that things may move soon and she should be careful, without naming the document — network +2; riesgo +0.76; expl3 +0.05; → `24cd954dc776` (n=715)
- 2. Say you cannot comment on internal plans or promise that any role is safe, so she must weigh the risk herself — dignity +1; riesgo -1.13; expl3 -0.38 (n=2370)
- 3. Tell her privately what is planned and ask her to keep it strictly confidential — network +3, dignity -2; riesgo +0.37; expl3 +0.33; → `0896936dad40` (n=527)

**Paso** `24cd954dc776` (606 veces): Sienna holds off signing. Two weeks later the change is announced and she thanks you. Your manager senses a leak and starts checking who knew.
- 1. Go to your manager and admit you dropped a vague hint — dignity +2, network -1; riesgo -1.09; expl3 -0.20 (n=324)
- 2. Stay silent — dignity -1; riesgo +1.09; expl3 +0.20 (n=265)

**Paso** `0896936dad40` (385 veces): Sienna does not buy. She tells her husband, who “anonymously” discusses it in an industry group chat. The story reaches HR.
- 1. Tell HR the truth about how the leak spread — dignity +1, network -3, output -1; riesgo -0.44; expl3 -0.23 (n=197)
- 2. Deny it was you — dignity -3, network -2; riesgo +0.44; expl3 +0.23 (n=185)

## Named on a department award you did not work on

Aparece 4432 veces (primer paso): L1 55%, L2 13%, L3 11%, L4 15%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `f36455cc968e` (4584 veces): Submissions for the department’s annual Breakthrough Award close tonight. Your manager sends you the Aurora data-platform pack to look over. You have been on Lynx Payments the whole time. The team next door delivered Aurora, and you only turned up to the kick-off. Your manager messages: “I’ve added 
- 1. Ask that the pack name only those who did the work, or limit your line to the kick-off — dignity +2, network -2; riesgo -0.42; expl3 +0.02; → `4ab0a079865b` (n=535)
- 2. Sign it quietly and treat it as a favour from your manager — network +2, wealth +1, dignity -2; riesgo +0.65; expl3 -0.01; → `181910e6b114` (n=2134)
- 3. Suggest submitting Lynx Payments instead, with you as the lead author — output +1, dignity +1, skill +1, network -1; riesgo -0.23; expl3 -0.02 (n=991)

**Paso** `181910e6b114` (2541 veces): Aurora wins. You are named at the awards. Three months later internal audit picks the pack for a spot check and asks you to describe exactly what you contributed to the platform.
- 1. Admit you were not part of the core work — dignity +2, wealth -1, network -1; riesgo -0.45; expl3 -0.40 (n=1592)
- 2. Invent a contribution that matches your manager’s story — dignity -3, wealth +1; riesgo +0.45; expl3 +0.40 (n=238)

**Paso** `4ab0a079865b` (463 veces): Your manager is put out: “Fine. Aurora is one name short.” He calls you ungrateful. Aurora goes on to win.
- 1. Put your head down and let next quarter’s delivery speak — output +2, dignity +1, skill +1; riesgo +0.06; expl3 -0.00 (n=268)
- 2. Ask HR anonymously whether naming people who did not contribute is allowed — dignity +2, network -2; riesgo -0.06; expl3 +0.00 (n=188)

## You overhear an unpublished project naming you

Aparece 4430 veces (primer paso): L1 57%, L2 14%, L3 11%, L4 13%, L5 4%, L6 1%; meses 1–48 (mediana 7).

**Paso** `bf4b670138f3` (4437 veces): In the fifteenth-floor kitchen, platform director Harper and Miles, a fellow manager, drop their voices: “Polaris starts in Q3. On the Lynx side we’ll have… lead the tech.” The word you half-catch in the gap is your surname. The project has not been announced. If Miles realises you were listening, i
- 1. Walk in as if you have just come for water and say hello as normal — network +1, dignity +1; riesgo -0.49; expl3 -0.26 (n=2416)
- 2. Leave quietly and act as if you heard nothing — dignity +2; riesgo -0.60; expl3 -0.07 (n=610)
- 3. Stay in the corner and listen to the rest — skill +1, dignity -1; riesgo +1.09; expl3 +0.33; → `3b488977854a` (n=556)

**Paso** `3b488977854a` (456 veces): You hear budget and competitor detail. Miles turns: “Who’s there?”
- 1. Step out and say you were just passing, without admitting you listened — network -2; riesgo +0.10; expl3 +0.12 (n=191)
- 2. Step out, say you heard your name, and ask whether this is a normal process — dignity +2; riesgo -0.10; expl3 -0.12 (n=243)

## A leaver asks you to keep work files off the company systems

Aparece 4414 veces (primer paso): L1 57%, L2 14%, L3 11%, L4 14%, L5 4%, L6 1%; meses 1–48 (mediana 7).

**Paso** `1511245e8c5e` (4423 veces): One evening Felix, who is leaving for a competitor, sends you a link to 8GB of files in cloud storage: “Three years of project scripts and client-contact notes. I wiped the company drive — keep this for me, and don’t upload it here.” Some of the files are scanned client contracts marked Internal. Yo
- 1. Refuse the files and tell him to use the proper handover — dignity +2, network -1; riesgo -0.53; expl3 -0.06 (n=554)
- 2. Take the link without opening it, and plan to delete it later — network +1, dignity -1; riesgo +1.06; expl3 +0.34; → `3972f45b76ab` (n=515)
- 3. Take it and report it to Information Security — dignity +2, network -1, skill +1; riesgo -0.53; expl3 -0.28 (n=2493)

**Paso** `3972f45b76ab` (458 veces): Three months later competitor Halcyon Tech quotes your clients with unusual precision. InfoSec is checking access logs. Felix once logged into a drive you hold.
- 1. Come forward and say you received a link you had not yet deleted — dignity +1, network -2, output -1; riesgo -0.40; expl3 -0.31 (n=210)
- 2. Deny knowing anything — network -1, dignity -4; riesgo +0.40; expl3 +0.31 (n=210)

## The gym after work, or staying late to get ahead

Aparece 4413 veces (primer paso): L1 56%, L2 15%, L3 11%, L4 13%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `ae90bae63391` (4413 veces): You started going to the gym after work and have kept it up. You feel better and have more energy. Tonight there is a non-urgent piece of work that would make tomorrow easier if you finished it. You can only do one: the gym or staying late.
- 1. Go to the gym as planned and get the work done efficiently tomorrow — health +2, dignity +1, output -1; riesgo -0.23; expl3 +0.00 (n=665)
- 2. Skip the gym, stay late, and clear the work tonight — output +1, health -1; riesgo -0.37; expl3 -0.20 (n=2348)
- 3. Try to do both: gym first, then stay up late to finish the work — output +1, health -2; riesgo +0.60; expl3 +0.20 (n=529)

## Choosing a stack for a new module

Aparece 4412 veces (primer paso): L1 56%, L2 13%, L3 10%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `8f418a6facbe` (4412 veces): You need to pick a stack for a new module. You could write the team's mature stack in your sleep, and it would almost certainly deliver on time. There is also a more modern framework with an active community that fits better in the long term. But neither you nor the team has used it in production, s
- 1. Adopt the new framework and use this low-risk module to build experience — skill +3, output -1, health -1; riesgo +0.58; expl3 +0.19 (n=763)
- 2. Stick with the mature stack and put reliable delivery first — output +2, health +1, skill -1; riesgo -0.58; expl3 -0.19 (n=2793)

## A colleague's late handovers keep pushing back your work

Aparece 4411 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `dd70cf8fec5c` (4411 veces): Your work cannot start until your colleague Will hands his over. He always delivers at the last minute. This time it arrives on the afternoon of the deadline, so you are stuck working late. He shrugs, "It was only a bit late."
- 1. Agree a handover time with him, and bring in the project schedule if it needs writing down — skill +1, dignity +1, output +1; riesgo -0.54; expl3 -0.29 (n=2497)
- 2. Work late to cover it and say nothing — output +1, health -2, dignity -1; riesgo +0.23; expl3 +0.15 (n=531)
- 3. Call him out in the main channel as always holding things up — network -2, dignity -1; riesgo +0.32; expl3 +0.14 (n=522)

## Thanking a colleague from the next team who went out of their way

Aparece 4409 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `615eebee3ab7` (4409 veces): Last week a nasty bug in a barely maintained legacy submodule had you stuck for two days. Chris, a senior engineer on the next team, sat at your desk for a whole afternoon and helped you find and fix it. Nobody required them to spend that long. It is Friday, and you want to say thank you. You could 
- 1. Take them out for lunch privately, straight away — network +2, wealth -2, dignity -1, output -1, health -1; riesgo -0.41; expl3 +0.09 (n=548)
- 2. Write a formal recognition note and copy their manager — network +3, dignity +2, skill +1, output -1, health +1; riesgo -0.54; expl3 -0.14 (n=2055)
- 3. Do nothing special for now and help them next time they need it — network +1, output +1, health +1; riesgo +0.95; expl3 +0.06 (n=944)

## Late-night work messages and the manager's reaction

Aparece 4408 veces (primer paso): L1 58%, L2 13%, L3 10%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `13b41a44f8c9` (4506 veces): Colleague Tara posts "today's progress" and "tomorrow's plan" in the channel every night at 11pm. Your manager, Chris, is often first to react. You are never online at that hour. In the weekly meeting Chris said "we need to respond promptly". Tonight Tara @channels a question about an API field.
- 1. Reply at once to look professional — network +2, output +1, health -2, dignity -1; riesgo -0.08; expl3 -0.10 (n=1190)
- 2. Reply in the morning and spell out your working hours — dignity +2, health +1, network -1; riesgo -0.13; expl3 -0.15; → `344ab51bb479` (n=1332)
- 3. Suggest to your manager privately that important items go by email — skill +1, dignity +1; riesgo +0.18; expl3 +0.02 (n=662)
- 4. Copy Tara and start sending late-night updates yourself — network +1, health -3, dignity -2; riesgo +0.03; expl3 +0.23 (n=440)

**Paso** `344ab51bb479` (1675 veces): Chris says, "In principle that's fine, but we can't slip client deadlines."
- 1. Set up an on-call rota, with no replies on days you are not on call — skill +2, dignity +2, health +1, network +1; riesgo -0.06; expl3 -0.10 (n=1004)
- 2. Keep to your hours anyway, whatever the reaction — dignity +1, health +1; riesgo +0.06; expl3 +0.10 (n=157)

## Hosting an important client visit

Aparece 4408 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 14%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `1a36d76efe7f` (4408 veces): An important client's head of engineering is visiting next week. Facilities has left the final plan to you, since you own the technical side of the partnership and will run the demo. There are three options. (A) Use the standard BD budget, drinks within policy included, for a working dinner at a nea
- 1. A: Working dinner at a business restaurant, staying two hours — network +3, output +1, health -2; riesgo -0.00; expl3 +0.02 (n=637)
- 2. B: Working lunch in the office café, then an afternoon demo covering everything in one go — network +1, output +2, health +1, skill +1, dignity -1; riesgo -0.12; expl3 -0.15 (n=2354)
- 3. C: Fully remote demo, no in-person visit — output +1, health +2, network -2, dignity -1, skill -1; riesgo +0.13; expl3 +0.14 (n=543)

## Lunch with the team, or keep the break to yourself

Aparece 4393 veces (primer paso): L1 56%, L2 13%, L3 10%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `3d24b299375e` (4571 veces): At noon the team usually heads to a café near the office to swap project gossip and guesses about what your manager is thinking. It is where people pick up the unofficial news. For the past few months you have eaten at your desk or gone for a walk instead. You get a real break and are sharper in the
- 1. Switch to lunching with colleagues at least three days a week — network +3, health -1; riesgo -0.04; expl3 -0.09; → `6b0f78038f1f` (n=2008)
- 2. Keep skipping the café, and let a strong afternoon prove the point — health +2, output +2, network -2, dignity +1; riesgo +0.02; expl3 +0.07; → `1a6085e46de5` (n=687)
- 3. Compromise: Tuesdays and Thursdays with the team, the break to yourself the rest — network +2, health +1, dignity +1; riesgo +0.02; expl3 +0.02; → `9fde1c3e54a1` (n=965)

**Paso** `6b0f78038f1f` (2430 veces): At your third lunch you overhear people discussing who will get places on next quarter’s flagship project. Someone floats your name. Someone else says “we never see them.” You need to decide how often to keep going.
- 1. Keep lunching with the team every day — network +3, health -2, output -1; riesgo +0.03; expl3 +0.11 (n=249)
- 2. Drop back to Tuesdays and Thursdays once you have the key information — network +2, health +1, dignity +1, output +1; riesgo -0.03; expl3 -0.11 (n=1475)

**Paso** `9fde1c3e54a1` (876 veces): After a month of lunching with the team twice a week, your manager stops talking about “mixing in”. Over lunch you learn Warren’s project is being folded into your module, so you have time to prepare.
- 1. Keep to the current pattern — network +2, health +1, output +1, dignity +1; riesgo -0.18; expl3 -0.11 (n=601)
- 2. Go to more lunches to stay more visible — network +3, health -1; riesgo +0.18; expl3 +0.11 (n=226)

**Paso** `1a6085e46de5` (644 veces): Your delivery stays solid, but in a review Warren says you “don’t really know the team’s pain points”. Missing lunch has left you out of the loop.
- 1. Start joining lunch occasionally, specifically to catch up — network +2, output +1; riesgo +0.08; expl3 -0.06 (n=363)
- 2. Keep skipping the café, and book 1:1s with the people who matter — network +1, output +2, dignity +1, health +1; riesgo -0.08; expl3 +0.06 (n=249)

## Health check returning the wrong status

Aparece 4387 veces (primer paso): L1 58%, L2 13%, L3 9%, L4 15%, L5 5%, L6 0%; meses 1–48 (mediana 7).

**Paso** `8b573078a5b5` (4387 veces): Your load-balancer health-check endpoint returns 200, but the body says status is degraded, so traffic still hits unhealthy instances.
- 1. Fix the endpoint now and check the other services — skill +2, output +1, health -1; riesgo -0.88; expl3 -0.31 (n=2460)
- 2. Fix this service only — output +1, skill +1; riesgo +0.25; expl3 +0.07 (n=552)
- 3. Leave it for on-call — network -1, dignity -1; riesgo +0.63; expl3 +0.25 (n=534)

## A colleague's clutter takes over the aisle

Aparece 4377 veces (primer paso): L1 56%, L2 13%, L3 11%, L4 15%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `c5255c36c7ac` (4377 veces): Leon, who sits next to you, hoards things. Boxes, parcels and gym kit are all over the floor and have slowly taken over the shared aisle between you. You have to turn sideways to get past, and it is a trip hazard. He doesn't seem to see a problem.
- 1. Tell him the aisle is too tight and suggest sorting the clutter together — dignity +1, network +1, skill +1; riesgo -0.26; expl3 -0.21 (n=2491)
- 2. Squeeze past every day and say nothing — health -1, dignity -1; riesgo -0.20; expl3 +0.07 (n=548)
- 3. While he is away, pile all of it onto his desk — network -2, dignity -1; riesgo +0.47; expl3 +0.14 (n=476)

## A colleague keeps helping themselves to your snacks

Aparece 4375 veces (primer paso): L1 57%, L2 14%, L3 10%, L4 14%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `57cfacff9564` (4375 veces): You keep a few snacks in your drawer. Colleague Mia "just grabs a handful" every day, never brings her own, and has never returned the favour. Today she grins, "Yours are the best." It isn't much, but it is starting to grate.
- 1. Joke: "Bring some next time and we can swap", and leave it there — dignity +1, network +1, skill +1; riesgo -0.29; expl3 -0.22 (n=2479)
- 2. Keep sharing, because you don't like to say anything — network +1, dignity -1, wealth -1; riesgo -0.28; expl3 +0.05 (n=509)
- 3. Lock the snacks away and stop sharing, without explaining — dignity +1, network -1; riesgo +0.57; expl3 +0.17 (n=539)

## One conference place, and a question about Jo

Aparece 4356 veces (primer paso): L1 62%, L2 14%, L3 9%, L4 11%, L5 4%, L6 0%; meses 1–48 (mediana 6).

**Paso** `b4e949afe460` (4356 veces): The team has one place at an industry conference. It is a good trip with plenty of visibility, and word is it will go to you or Jo. Your manager catches you in the kitchen and asks, as if in passing, 'How has Jo been lately? Do you think she's the right person to represent the team?' You can tell th
- 1. Give Jo fair credit for her strengths and say she would be a good fit — network +2, dignity +2, output -1; riesgo -0.30; expl3 -0.16; → `f2ae5b8d98cb` (n=960)
- 2. Praise Jo, and briefly add your own recent relevant work — output +1, network -1, skill +1; riesgo -0.15; expl3 -0.23; → `3346fbd482a3` (n=1691)
- 3. Say you each have strengths, and suggest choosing whoever fits the brief best — dignity +1, skill +1; riesgo -0.04; expl3 -0.02; → `d205454b1b10` (n=507)
- 4. Hint at gaps in Jo's recent work — output +1, network -3, dignity -2; riesgo +0.49; expl3 +0.41; → `270e81bd6397` (n=417)

**Paso** `3346fbd482a3` (2272 veces): Your manager listens and says, 'Noted.' The list comes out and you are going. Jo takes the day off and is noticeably cooler with you afterwards. When you get back, your manager wants you to give the team a 30-minute talk on the conference.
- 1. Thank Jo in the talk for her earlier groundwork, then go and speak to her afterwards — network +2, dignity +2, output +1, skill +1; riesgo -0.38; expl3 -0.23 (n=1425)
- 2. Keep the talk on what you got out of it and reinforce your manager's good impression — output +2, network -2, dignity -1; riesgo +0.38; expl3 +0.23 (n=221)

**Paso** `f2ae5b8d98cb` (1001 veces): Your manager nods and says no more. Two days later the list is out: Jo is going. She thanks you in front of the team for 'putting in a word'. A week later she shares client leads from the conference, and your manager praises her in the team channel. You have to decide how you feel about it and what 
- 1. Congratulate her and ask what she got out of it — network +3, skill +1, dignity +1; riesgo -0.46; expl3 -0.17 (n=702)
- 2. Congratulate her in public, then tell your manager privately you want the next one — output +1, dignity -1; riesgo +0.46; expl3 +0.17 (n=206)

**Paso** `d205454b1b10` (516 veces): Your manager asks you each to write a one-page case for attending, and a director will decide. You both get to work on it. The atmosphere is awkward but still civil.
- 1. Keep the one-pager to business value and what you would bring back, without knocking Jo — skill +2, dignity +2, output +1, health -1; riesgo -0.28; expl3 -0.15; → `d8560ce9b512` (n=265)
- 2. Compare the two of you in the one-pager and imply you are the better fit — output +2, network -2, dignity -1; riesgo +0.28; expl3 +0.15; → `d8560ce9b512` (n=197)

**Paso** `d8560ce9b512` (458 veces): The director reads both one-pagers and picks whoever fits the brief better. If you go, Jo will only half accept it. If you don't, you still need to handle it well.
- 1. If you go, offer to take turns next time. If not, help Jo get ready — network +2, dignity +2, output +1; riesgo -0.03; expl3 -0.11 (n=243)
- 2. Take the win or the loss and put nothing more into the relationship — output +1, network -1; riesgo +0.03; expl3 +0.11 (n=164)

**Paso** `270e81bd6397` (342 veces): Your manager's face gives nothing away. They only say, 'I'll think about it.' The list comes out and you are still going. But Jo has heard from someone else that you spoke badly of her in the kitchen, and the team's relationship with you drops sharply.
- 1. Go to Jo, clarify or apologise, and try to repair it — network +1, dignity -1, health -1; riesgo +0.04; expl3 -0.21 (n=191)
- 2. Offer no explanation and focus on the trip — output +2, network -3; riesgo -0.04; expl3 +0.21 (n=148)

## In-house kernel versus an open-source stack

Aparece 4346 veces (primer paso): L1 61%, L2 15%, L3 10%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `1b2dba28e4f1` (4346 veces): The company is setting up a new real-time compute platform, and your manager has put you in charge of the technology choice for your part of it. There are two options. You can build the kernel in-house, which fits the business but means a long build and a painful go-live. Or you can adopt a well-kno
- 1. Argue for an in-house kernel as a long-term technical asset — skill +2, dignity +1, output -1; riesgo -0.09; expl3 +0.08; → `e09fb7b3f3c2` (n=1099)
- 2. Adopt the open-source stack and aim for fast delivery — output +2, skill -1; riesgo +0.09; expl3 -0.08; → `724082d3e27e` (n=2454)

**Paso** `724082d3e27e` (3291 veces): The platform goes live on the open-source stack on time and the business is pleased. Then a routine security scan flags a problem: this version has an undisclosed candidate CVE, and details are already circulating among a few people internally. If it can be triggered in production, it would hit your
- 1. Tell security and rush out a fallback from scratch — dignity +2, skill +1, output -2, network -1; riesgo -1.08; expl3 -0.16 (n=997)
- 2. Sit on the report and bet it will not be triggered soon — output +1, wealth +1, dignity -1; riesgo +1.08; expl3 +0.16; → `5b304c0c74aa` (n=1662)

**Paso** `5b304c0c74aa` (1786 veces): Three weeks later security has traced the internal reports back to your team and invited you to a 'compliance conversation'. Beforehand your manager briefs you: 'Don't take all of it. Blame the misjudgement on the vendor or the upstream community so the team can close this.' In the room, the complia
- 1. Use your manager's line and blame the upstream community — dignity -2, network -1, wealth +1; riesgo +0.59; expl3 +0.13 (n=251)
- 2. Admit you got the assessment wrong and accept whatever sanction is appropriate — dignity -3, wealth -1; riesgo -0.59; expl3 -0.13 (n=1246)

**Paso** `e09fb7b3f3c2` (1151 veces): Two months into the in-house build you are badly behind and keep missing milestones. At the quarterly review your manager puts you on the spot in front of everyone: 'This was your call. The business can't wait. Project X's core modules are already close to your design. Have a look at them, hit the m
- 1. Quietly borrow the open-source kernel, rebrand it, and hit the milestone — output +1, skill -1, dignity -2; riesgo +0.57; expl3 +0.23; → `724082d3e27e` (n=408)
- 2. Keep the work original, ask for a delay, and write the risk into the update — skill +1, dignity +1, output -1, network -1; riesgo -0.57; expl3 -0.23 (n=585)

## In-house senior architect certification over the weekend

Aparece 4329 veces (primer paso): L1 56%, L2 13%, L3 10%, L4 15%, L5 5%, L6 1%; meses 1–48 (mediana 7).

**Paso** `6268bfe7fb13` (4329 veces): The tech committee is running an in-house senior architect certification this Saturday and Sunday, on your own time. It is optional, and the company covers the fee. Meanwhile, an internal tooling project of yours is due next Tuesday as planned. If you put in extra hours this weekend, you could ship 
- 1. Sign up for the certification and spend both days learning properly — skill +3, network +1, output -1, health -1; riesgo +0.04; expl3 -0.04 (n=1064)
- 2. Work through the weekend to deliver the project on Monday morning — output +2, network +1, skill -1, health -2; riesgo -0.07; expl3 -0.11 (n=1827)
- 3. Stick to the family weekend and pick work up next week as planned — health +2, dignity +1, skill -1, output -1, network -1; riesgo +0.04; expl3 +0.15 (n=590)

## The client adds three things 'while we're here'

Aparece 4328 veces (primer paso): L1 62%, L2 15%, L3 9%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `a17faeec0f07` (4328 veces): Close to delivery, at a regular meeting, the client 'mentions in passing' three new requirements: 'These shouldn't be hard. Just do them at the same time.' In fact the change is a big one. It would squeeze the current plan and hurt quality. Their tone is casual, as if it is obviously included. Every
- 1. Neither accept nor refuse in the meeting, and promise an impact assessment and proposal afterwards — skill +2, dignity +1, network +1; riesgo -0.29; expl3 -0.32; → `805cf4026a03` (n=2385)
- 2. Afraid of annoying them, agree to all of it on the spot — network +1, output -1, health -1; riesgo +0.22; expl3 +0.23; → `3d62ca15fbb5` (n=561)
- 3. Refuse there and then: 'It's not in the contract. We can't do it' — dignity +1, network -2; riesgo +0.07; expl3 +0.09; → `8b6248c5eb13` (n=593)

**Paso** `805cf4026a03` (3086 veces): You assessed it properly afterwards. One of the three is small, but the other two would push the date back a long way. You have a table of impact, cost and schedule ready. The client is chasing for an answer.
- 1. Talk numbers: do the small one for free, and put the other two through change control with plan trade-offs — skill +2, output +2, network +1, dignity +1; riesgo -0.53; expl3 -0.26 (n=1997)
- 2. Still dreading the conversation after the assessment, cram all of it into the current plan — output -1, health -2; riesgo +0.53; expl3 +0.26 (n=314)

**Paso** `8b6248c5eb13` (507 veces): A flat no in front of everyone made the client look small. The atmosphere soured, and they think you are 'inflexible and not commercial'. Afterwards they complain to your manager. The request could have been handled more gently.
- 1. Go to the client, smooth things over, explain where the line is, and offer a workable change proposal — network +2, skill +1, dignity +1, health -1; riesgo -0.24; expl3 -0.10 (n=276)
- 2. Stand firm: 'I wasn't wrong. The contract is the contract' — network -1, dignity +1; riesgo +0.24; expl3 +0.10 (n=227)

**Paso** `3d62ca15fbb5` (443 veces): You agreed to all of it. The client is pleased for now, the plan is wrecked, and quality on the original features is starting to slip. Encouraged, the client keeps 'mentioning in passing' more work, and the scope creep has no end in sight.
- 1. Stop it now: tell the client and your manager where things stand, and reset scope and change control — skill +1, dignity +1, output +1, health -1; riesgo -0.58; expl3 -0.23 (n=226)
- 2. Keep taking whatever comes, and have the team work late to carry it — health -2, output -1, network -1; riesgo +0.58; expl3 +0.23 (n=213)

## Pushed on stage at the Christmas party

Aparece 4291 veces (primer paso): L1 62%, L2 14%, L3 10%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 6).

**Paso** `d05ff804187a` (4291 veces): The Christmas party is in full swing. The host spots you, and your table, colleagues and manager included, starts chanting for you to get up and do something to “get the room going.” You have nothing prepared and this is not your sort of thing, but every eye is on you and someone is already holding 
- 1. Take it in good humour: a quick gag or a bit of audience interaction, just enough to lift the room — network +2, dignity +1, health -1; riesgo -0.16; expl3 +0.01; → `bd04d6e787f9` (n=599)
- 2. Smile and say, ‘Thanks, but not tonight’ — network +1, dignity +1, skill +1; riesgo -0.08; expl3 -0.23; → `447e2772ea5a` (n=2336)
- 3. Shut it down flat with “I’m not doing that”, and let the room go quiet — dignity -1, network -2; riesgo +0.24; expl3 +0.22; → `b8cd3e61c27b` (n=581)

**Paso** `447e2772ea5a` (3011 veces): You stay off the stage and at your table, chatting and clapping along. You are still very much part of the evening. Then the table turns on Jordan, a new joiner who hates this sort of thing, and they go bright red.
- 1. Get Jordan off the hook: steer the attention elsewhere and give them a way out — network +2, dignity +1, skill +1; riesgo -0.06; expl3 -0.08 (n=1761)
- 2. Leave them to deal with it — sin cambios; riesgo +0.06; expl3 +0.08 (n=500)

**Paso** `bd04d6e787f9` (529 veces): You get up and run a quick game for the whole room. It goes down better than you expected. People are laughing, and your manager gives you a thumbs-up. Afterwards the host tries to keep you up there for the next part.
- 1. Quit while you are ahead: hand the stage back and return to your table — network +1, dignity +1, health +1; riesgo +0.01; expl3 -0.02 (n=291)
- 2. Ride the moment and keep hosting, even as you start to run out of steam — dignity -1, health -1; riesgo -0.01; expl3 +0.02 (n=233)

**Paso** `b8cd3e61c27b` (513 veces): You refuse bluntly. The host has to paper over an awkward few seconds. The people who were winding you up look silly, and your manager marks you down as “not really a team person.” There was a more graceful way to say no.
- 1. Recover by joining a later group game to show you are still part of things — network +1, dignity +1, health -1; riesgo -0.16; expl3 -0.13 (n=282)
- 2. Sit the rest of the night out with a face like thunder, speaking to nobody — network -2, dignity -1; riesgo +0.16; expl3 +0.13 (n=227)

## Pitching against a cheaper rival

Aparece 4283 veces (primer paso): L1 61%, L2 15%, L3 10%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `43cde09e9d6e` (4283 veces): The company is bidding for a major client project, and you are leading the pitch. Your main rival is known for undercutting on price. The panel is a mix of technical people and procurement, so they care about both the solution and the quote. You have heard the rival will almost certainly lead with “
- 1. Play to your strengths: use technical depth and total cost of ownership to justify the higher price — skill +2, output +1, network +1, health -1; riesgo -0.35; expl3 -0.30; → `207aa5bc82c1` (n=2359)
- 2. Slash the price at the last minute to match them, and skate through the actual pitch — output -1, skill -1; riesgo +0.33; expl3 +0.23; → `642bb20be594` (n=587)
- 3. Take a swipe at the rival: imply their tech is weak and they have botched jobs before — network -1, dignity -1; riesgo +0.01; expl3 +0.07; → `c9ee8f93505b` (n=582)

**Paso** `207aa5bc82c1` (3002 veces): You walk through a solid technical design and a cost-of-ownership model that explains the price. The technical panellists nod along. Procurement still stares at the number: “You’re well above the other bid. How do we sell this to our leadership?”
- 1. Offer staged payments plus a measurable ROI model procurement can repeat upstairs — skill +2, output +2, network +1, dignity +1; riesgo -0.45; expl3 -0.18 (n=1985)
- 2. Keep talking technology and dodge the pricing question — skill +1, output -1; riesgo +0.45; expl3 +0.18 (n=274)

**Paso** `c9ee8f93505b` (512 veces): You run the rival down in the pitch. One of the panellists turns out to know them, and the room cools: “We asked for your proposal, not a review of someone else’s.” You look small, and it costs you marks.
- 1. Pull it back immediately and return to what your own proposal actually delivers — skill +1, dignity +1, output +1, network +1; riesgo -0.42; expl3 -0.10 (n=285)
- 2. Keep going on about their past failures — network -2, dignity -2; riesgo +0.42; expl3 +0.10 (n=222)

**Paso** `642bb20be594` (476 veces): You cut the price to almost nothing, and the pitch itself is thin. If you win, the team inherits a rushed, loss-making job. If you lose, you have still taught the client to expect a price you cannot live with. Your manager is uneasy about the tactic.
- 1. Stop cutting and steer the contest back onto value — skill +1, dignity +1, output +1; riesgo -0.26; expl3 -0.22 (n=255)
- 2. Keep betting everything on price: win the deal now and worry later — output -1, health -1, dignity -1; riesgo +0.26; expl3 +0.22 (n=220)

## A live demo blows up in front of the client

Aparece 4279 veces (primer paso): L1 62%, L2 14%, L3 9%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `606ffe5fc95e` (4279 veces): You are at the client's offices demonstrating a new feature. At the key checkout step the system throws an error and the page freezes. Their decision-makers sit opposite you, waiting to see it work. You know the demo environment is flaky, but the room has already gone cold.
- 1. Say plainly it's a demo-environment glitch, and switch to a fallback or recording to show the core value — skill +2, dignity +1, output +1, network +1; riesgo -0.45; expl3 -0.32; → `ba8c41707c24` (n=2390)
- 2. Keep hitting refresh as it gets messier, without switching plan — dignity -1, output -1; riesgo +0.04; expl3 +0.09; → `1d60300df07b` (n=585)
- 3. In a panic, say it is a problem on the client's network — network -1, dignity -1; riesgo +0.41; expl3 +0.23; → `40890a450f1c` (n=531)

**Paso** `ba8c41707c24` (3077 veces): You switch to the fallback without fuss, finish the core flow, and use it to talk through the system's fault-tolerance. The client even thinks you were well prepared. After the demo their engineering lead asks you privately what caused the error.
- 1. Give the root cause straight, and promise a write-up of the investigation and fix afterwards — skill +2, output +1, network +1, dignity +1; riesgo -0.49; expl3 -0.21 (n=2016)
- 2. Fudge it: 'Small issue, doesn't affect anything' — sin cambios; riesgo +0.49; expl3 +0.21 (n=301)

**Paso** `1d60300df07b` (508 veces): You keep retrying. Five or six minutes of dead air pass, the client's people start looking at their phones, and the room turns icy. A colleague slides you a note: 'Talk about something else first.' The demo has lost all momentum.
- 1. Change tack at once: skip the broken step, talk about overall value, and demo it afterwards — skill +1, dignity +1, output +1, health -1; riesgo -0.18; expl3 -0.09 (n=274)
- 2. Keep hammering at the bug until time runs out — output -2, dignity -1, network -1; riesgo +0.18; expl3 +0.09 (n=231)

**Paso** `40890a450f1c` (441 veces): You blame 'the client's network'. Their IT team tests it on the spot and the network is fine, so the lie is exposed. The client's expression changes: 'If it's the product, say so. Don't spin us.' Trust has taken a knock.
- 1. Admit at once that you got that wrong, apologise properly, and get back to the demo — dignity +1, skill +1, network +1, health -1; riesgo -0.31; expl3 -0.26 (n=245)
- 2. Keep doubling down with another excuse — network -2, dignity -2; riesgo +0.31; expl3 +0.26 (n=195)

## Client makes an inappropriate joke at dinner

Aparece 4275 veces (primer paso): L1 62%, L2 14%, L3 9%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 6).

**Paso** `bc47083fd307` (4275 veces): You are at a client dinner. After a few drinks, one of their senior people starts making jokes that cross a line — pointed, sexual remarks aimed at Chloe, a woman on your side of the table. Her laugh is tight and she looks trapped. They are an important account. Everyone else is pretending it is ban
- 1. Change the subject without a scene, pull the talk back to the work, and give Chloe a way out — skill +2, dignity +1, network +1; riesgo -0.06; expl3 -0.33; → `67b294bc6e4f` (n=2399)
- 2. Join in and laugh along, to keep the ‘atmosphere’ — dignity -2; riesgo +0.15; expl3 +0.37; → `0ff722c16925` (n=546)
- 3. Say firmly that the remark is not on, and bring the talk back to the work — dignity +1, network -1; riesgo -0.09; expl3 -0.04; → `5204148abfa9` (n=590)

**Paso** `67b294bc6e4f` (3050 veces): You steer the conversation onto the project and give Chloe an easy exit — a ‘call she needs to take.’ The client does not clock that you defused it, and the table settles. Afterwards Chloe thanks you privately. You still have to decide whether the company should know this client has a problem with b
- 1. Brief your manager privately and factually, ask Chloe what support she wants, and raise it with the account lead — skill +1, dignity +1, network +1; riesgo -0.16; expl3 -0.14 (n=2047)
- 2. Decide it was handled and there is no need to raise it — network +1; riesgo +0.16; expl3 +0.14 (n=278)

**Paso** `5204148abfa9` (536 veces): You stop the remark without a scene and bring the talk back to the work. The client looks uncomfortable. Chloe is glad someone drew a line. Nobody asks her to repair the relationship. That job belongs to the account lead.
- 1. Leave the client relationship with the account lead, and ask Chloe only what support she wants — skill +1, network +1, dignity +1, health -1; riesgo -0.24; expl3 -0.10 (n=264)
- 2. Decide you were in the right, and make no effort to repair it — network -1, dignity +1; riesgo +0.24; expl3 +0.10 (n=268)

**Paso** `0ff722c16925` (442 veces): You laugh along to keep the client sweet. To everyone watching, that is taking part. Chloe is finished with you and will not work with you if she can help it. It gets round the team that you have no line when a deal is on the table. Your manager hears, and starts to doubt your judgement. Whatever go
- 1. Own it: apologise properly to Chloe and admit you were out of order — dignity +1, network +1, health -1; riesgo -0.14; expl3 -0.10 (n=221)
- 2. Brush it off as ‘just dinner banter’ and insist you did nothing wrong — network -2, dignity -2; riesgo +0.14; expl3 +0.10 (n=220)

## Telling the client the project will be late

Aparece 4264 veces (primer paso): L1 62%, L2 15%, L3 9%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 6).

**Paso** `77660e585b81` (4264 veces): An upstream dependency has failed on a project you own. You now know you will be a week late, and the original delivery date is three days away. The client cares a lot about this one and has even put their own name behind it internally. You need to decide how to tell them.
- 1. Tell them at once, with a cause analysis, a recovery plan and a new timetable — skill +2, dignity +1, network +1, output +1, health -1; riesgo -0.40; expl3 -0.37; → `58898ba74773` (n=2358)
- 2. Wait until delivery day in case you still make it — output -1, dignity -1; riesgo +0.27; expl3 +0.15; → `9eb8dd3309ae` (n=601)
- 3. Report 'on time', then quietly work late and try to catch up — output -1, health -2, dignity -1; riesgo +0.13; expl3 +0.22; → `efc2085cd900` (n=559)

**Paso** `58898ba74773` (2995 veces): You were straight with them early. The client is not pleased, but respects that you were professional and took responsibility: 'At least you didn't hide it. I can explain that internally.' Then they push: could you ship a usable core first and the rest next week?
- 1. Check what is feasible, then offer phased delivery: the core first, the rest after — skill +2, output +2, network +1, dignity +1; riesgo -0.59; expl3 -0.24 (n=1978)
- 2. To keep them happy, promise both the core and the full version by the original date — output +1, health -2; riesgo +0.59; expl3 +0.24 (n=293)

**Paso** `9eb8dd3309ae` (507 veces): The gamble failed, and you only told them on delivery day that it would be late. The client is furious: 'Why didn't you say? I can't explain this upstairs.' They want an explanation from the company. Your manager is pulled in.
- 1. Apologise in person at once, present a detailed recovery plan, and fix how you communicate — dignity +1, skill +1, network +1, health -1; riesgo -0.55; expl3 -0.20 (n=280)
- 2. Explain why you were a victim of this too — network -2, dignity -2; riesgo +0.55; expl3 +0.20 (n=221)

**Paso** `efc2085cd900` (424 veces): You reported 'on time', then forced it through overnight. The version you shipped is rough and keeps failing once live. The client discovers that you hid the delay and delivered a poor product, and is beyond angry. You have ended up with the worst of both.
- 1. Tell the whole story, pull the broken version, and set a delivery plan that will actually hold — dignity +1, skill +1, output -1, health -1; riesgo -0.51; expl3 -0.25 (n=214)
- 2. Keep patching it and play down how bad it was — network -2, dignity -2; riesgo +0.51; expl3 +0.25 (n=204)

## A colleague who keeps handing you his work

Aparece 4257 veces (primer paso): L1 62%, L2 15%, L3 9%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `90c39716bd3e` (4257 veces): Dave on your team is very good at 'finding help'. One day it is two slides to rewrite, the next a script to run, and it is always 'you're better at this, it'll take minutes'. At first you were happy to help. Then you noticed more and more of his actual job coming your way as a matter of course, whil
- 1. Help this time, and be clear: next time he drafts it first and you review — network +1, dignity +1, skill +1; riesgo -0.17; expl3 -0.26; → `aaeb00b0e947` (n=2398)
- 2. Decline gently: 'I'm swamped. You start it and I'll jump in if you're stuck' — dignity +1, output +1, network -1; riesgo -0.17; expl3 +0.05; → `c32cb98e49bf` (n=561)
- 3. Quietly take it on again so as not to sour the relationship — output -1, health -1, dignity -1; riesgo +0.34; expl3 +0.21; → `c1069c37da9f` (n=550)

**Paso** `aaeb00b0e947` (3065 veces): You helped and said your piece. Dave agreed, then 'forgot' the next time and dumped the work on you again. In front of your manager he breezily called it 'something we always do together', blurring who did what. You realise a spoken agreement means nothing to him.
- 1. Record what you help with in messages and ticket notes so credit is traceable, and reset the split — skill +2, dignity +1, output +1; riesgo -0.18; expl3 -0.16 (n=2034)
- 2. Leave it. It's less hassle to keep helping — output -1, dignity -1, health -1; riesgo +0.18; expl3 +0.16 (n=304)

**Paso** `c32cb98e49bf` (520 veces): Dave was put out by the gentle no that day, but then did the work himself. A week later he hits something that really is beyond him and hesitates to ask you. You hear about it.
- 1. Tell him, 'If you're really stuck, come to me', and help without doing it for him — network +2, skill +1, dignity +1; riesgo -0.03; expl3 -0.01 (n=278)
- 2. Keep your distance. You are done being used as spare capacity — network -1, dignity +1; riesgo +0.03; expl3 +0.01 (n=237)

**Paso** `c1069c37da9f` (452 veces): You took the lot again. At the month-end review your own work is unfinished and your manager pulls you up on it, while Dave is praised for 'on-time delivery' of work you produced. The unfairness and the performance pressure hit you at the same time.
- 1. Give your manager the facts on how the work was really split, and redraw the line — dignity +1, skill +1, output +1, network -1, health -1; riesgo -0.20; expl3 -0.09 (n=238)
- 2. Swallow it. A falling-out is not worth it — dignity -2, output -1, health -1; riesgo +0.20; expl3 +0.09 (n=209)

## Remote client keeps sending the work back

Aparece 4249 veces (primer paso): L1 63%, L2 15%, L3 9%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `396f026fa76e` (4249 veces): You are working with a remote client entirely over video and chat. After the first delivery they say on a call, “This isn’t what I wanted.” Your chat history shows they had informally agreed to that direction. Reworking it will be expensive, and the team is already grumbling. Their tone on the call 
- 1. Skip the blame game: work out the mismatch and propose prototypes or visual specs before building more — skill +2, network +1, output +1, dignity +1; riesgo -0.25; expl3 -0.26; → `6b61efeefb32` (n=2327)
- 2. Pull up the chat log and argue that they already confirmed it — dignity +1, network -2; riesgo +0.14; expl3 +0.12; → `6e016db0f86a` (n=594)
- 3. Rework the lot without question, doing whatever they say — output -1, health -1; riesgo +0.12; expl3 +0.14; → `ac44790efd45` (n=557)

**Paso** `6b61efeefb32` (3021 veces): You suggest that from now on every requirement goes through a rough prototype and written sign-off. The client agrees: “That would actually make this much clearer.” You also agree a sensible scope for the first rework. The team still worries that endless changes will wreck the timeline and morale.
- 1. Build sign-off and a change log into the process to protect both the client and the team — skill +2, output +2, network +1, dignity +1; riesgo -0.42; expl3 -0.16 (n=2003)
- 2. Fix how you communicate, ignore the timeline, and just work longer hours — output +1, health -2; riesgo +0.42; expl3 +0.16 (n=267)

**Paso** `6e016db0f86a` (509 veces): You wave the chat log to prove you were right. The client is left looking small, and even though they were in the wrong they snap: “This partnership isn’t a courtroom.” Everything after that is spiky. You won the point and lost the relationship.
- 1. Cool things down: move from ‘who was wrong’ to ‘how we get this right’, and propose better sign-off — network +2, skill +1, dignity +1, health -1; riesgo -0.33; expl3 -0.09 (n=262)
- 2. Insist you did nothing wrong, and wait for them to blink first — network -2, dignity -1; riesgo +0.33; expl3 +0.09 (n=243)

**Paso** `ac44790efd45` (479 veces): You rework the lot without pinning down what went wrong. Their spoken requests stay vague, and version two is sent back as well. The team is exhausted, so are you, and the real problem is still there: nothing is clearly signed off.
- 1. Stop the blind rework and put a proper sign-off in place before going further — skill +2, dignity +1, output +1, health -1; riesgo -0.62; expl3 -0.24 (n=253)
- 2. Keep reworking on demand, exactly as they say — output -2, health -2, network -1; riesgo +0.62; expl3 +0.24 (n=218)

## A colleague who comes in ill

Aparece 4232 veces (primer paso): L1 62%, L2 14%, L3 10%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `d8263f1dd1b7` (4232 veces): Faye at the next desk has a heavy cold. She is coughing constantly and has almost lost her voice, but she is still in: 'The milestone's tight, I can't drop the ball.' The whole open-plan floor can hear every cough, and two people have started sneezing. She sees it as doing her duty, but there is a r
- 1. Check in privately, ask her to go home, and offer to cover the urgent part — network +2, dignity +1, output +1, health -1, skill +1; riesgo +0.06; expl3 -0.17; → `0f346d6e4d3e` (n=2279)
- 2. Tell your manager her coming in ill is a health risk, and suggest sick leave while the team covers — skill +1, dignity +1, network -1; riesgo -0.24; expl3 -0.02; → `927ed56a73ab` (n=638)
- 3. Put on a mask, move away from the noise and the germs, and say nothing — health -1, network -1, dignity -1; riesgo +0.18; expl3 +0.18; → `8060da8ac6e7` (n=549)

**Paso** `0f346d6e4d3e` (2900 veces): Faye is touched but still hesitates: 'I feel bad, you've got your own work.' You take the most urgent part and she goes home. Now your own schedule is packed, the milestone is close, and you are feeling the strain.
- 1. Tell your manager you are covering Faye for now, and ask for a realistic plan — output +1, dignity +1, network +1, skill +1; riesgo -0.36; expl3 -0.22 (n=1875)
- 2. Carry all of it without telling anyone, and work late to catch up — output +1, health -2, dignity -1; riesgo +0.36; expl3 +0.22 (n=286)

**Paso** `927ed56a73ab` (610 veces): Your manager takes the suggestion and sends Faye home on sick leave. The floor is quieter and people relax. Faye later hears that you raised it and feels a bit hurt, calling it 'a bit ungenerous'. You were thinking of everyone's health, but she never heard that part.
- 1. Explain privately, ask how she is, and help her hand over what cannot wait — network +2, dignity +1, skill +1; riesgo -0.04; expl3 +0.01 (n=352)
- 2. Leave it. You did nothing wrong and there is no need to explain — dignity +1, network -1; riesgo +0.04; expl3 -0.01 (n=246)

**Paso** `8060da8ac6e7` (472 veces): You kept your distance and said nothing. Within a week three more people on the team are ill. In the review afterwards your manager says, 'If someone had said something, we could have sent her home.' You think back to keeping quiet, and regret it.
- 1. Learn from it and propose a simple team rule: if you're ill, stay off, and the team covers — skill +1, dignity +1, network +1, output +1; riesgo -0.28; expl3 -0.11 (n=246)
- 2. Be glad you didn't catch it, and leave it there — network -1, dignity -1; riesgo +0.28; expl3 +0.11 (n=219)

## A milestone briefing for the execs

Aparece 4229 veces (primer paso): L1 62%, L2 15%, L3 9%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `36a72de95b64` (4229 veces): At the company's quarterly leadership review, you have to report on a milestone for a project you own. The execs are short of time and only want conclusions and risks. They have no interest in process. There is still an unresolved risk on the project, and progress is only 'broadly on track'. You hav
- 1. Lead with the conclusion: key results first, then the risk and the plan to deal with it — skill +2, dignity +1, output +1; riesgo -0.39; expl3 -0.25; → `54e5c54d627f` (n=2377)
- 2. Give only the good news: hide the risk and stick to highlights throughout — output +1, dignity -1; riesgo +0.34; expl3 +0.23; → `2fcf4c1df6d3` (n=563)
- 3. Walk through the process in detail, still not reaching the point ten minutes in — skill -1, output -1, dignity -1; riesgo +0.04; expl3 +0.01; → `2609a7ac9b1c` (n=538)

**Paso** `54e5c54d627f` (3039 veces): You opened with the results, then one slide on the risk and the plan already in place. An exec presses: 'What's the worst this risk does? What do you need?' This is a chance to show you have it under control.
- 1. Answer with a quantified worst case and a clear request for resources — skill +2, output +2, network +1, dignity +1; riesgo -0.40; expl3 -0.19 (n=2033)
- 2. Stay vague with 'shouldn't be too bad', offering no real assessment — skill -1, dignity -1; riesgo +0.40; expl3 +0.19 (n=276)

**Paso** `2609a7ac9b1c` (487 veces): You got lost in the process. The execs checked their watches several times, then cut in: 'What's the conclusion? Is there a risk?' You did not get to the point in the time you had, and the briefing went down badly.
- 1. Stop at once and give the conclusion, the risk and your request in three sentences — skill +1, dignity +1, output +1; riesgo +0.03; expl3 -0.02 (n=261)
- 2. Keep reading the pack at your own pace — skill -1, output -1, dignity -1, network -1; riesgo -0.03; expl3 +0.02 (n=222)

**Paso** `2fcf4c1df6d3` (472 veces): You only talked about highlights, and the execs came away impressed on the day. Two months later the risk materialises, the damage spreads, and leadership digs out the briefing notes: 'Why was there not a word about risk?' You are on the back foot.
- 1. Run a review, own the bad call, and show the fix already in place — dignity +1, skill +1, health -1; riesgo -0.52; expl3 -0.15 (n=250)
- 2. Argue that 'nobody could have seen this then' — dignity -2, network -2; riesgo +0.52; expl3 +0.15 (n=216)

## Seated with a senior leader at the Christmas party

Aparece 4222 veces (primer paso): L1 62%, L2 14%, L3 10%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 6).

**Paso** `21c9b9147fa9` (4222 veces): The Christmas party seating plan puts you, though you are not senior, on a table with a director you almost never see. A chance like this is rare, and easy to get wrong. After the opening small talk the table goes quiet, and they are looking round the group.
- 1. Open with something light: an industry anecdote, or an honest take on the evening — skill +2, network +1, dignity +1; riesgo -0.01; expl3 -0.24; → `df0f7ea33696` (n=2344)
- 2. Seize the moment and lay the praise on thick so they remember you — network -1, dignity -1; riesgo +0.16; expl3 +0.22; → `1c1fe0a733df` (n=585)
- 3. Freeze, eat, and say almost nothing all night — network -1, dignity -1; riesgo -0.15; expl3 +0.02; → `e344277cc05c` (n=531)

**Paso** `df0f7ea33696` (3020 veces): Your opener is well judged. The table warms up, they pick up the thread, and they ask in passing what you work on. It is a chance to be noticed, but it is only a passing question, time is short, and this is the wrong setting for a pitch.
- 1. Say in a couple of sentences what you do and why it matters, then stop without taking over the table — skill +2, network +2, dignity +1, output +1; riesgo -0.35; expl3 -0.18 (n=1956)
- 2. Treat it as a long status update, and sneak in a request while you are at it — network -1, dignity -1; riesgo +0.35; expl3 +0.18 (n=318)

**Paso** `1c1fe0a733df` (525 veces): The praise comes across as oily. They smile politely and change the subject, and people at the table wince on your behalf. Laying it on this thick has had the opposite effect to the one you wanted.
- 1. Stop, and go back to ordinary, honest conversation — skill +1, network +1, dignity +1; riesgo -0.20; expl3 -0.12 (n=282)
- 2. Keep finding new ways to compliment them — network -2, dignity -2; riesgo +0.20; expl3 +0.12 (n=240)

**Paso** `e344277cc05c` (491 veces): You are too tense to speak, and you spend a rare evening at that table staring at your plate. They have no impression of you at all, and the table files you as someone who cannot open up. The chance was in front of you and you did not take it.
- 1. Catch them before people leave and introduce yourself briefly, enough to leave a decent impression — skill +1, network +1, dignity +1, health -1; riesgo +0.05; expl3 -0.03 (n=266)
- 2. Stay silent until it is over, and miss the whole evening — network -1, dignity -1; riesgo -0.05; expl3 +0.03 (n=221)

## A new colleague with no sense of privacy

Aparece 4215 veces (primer paso): L1 61%, L2 15%, L3 10%, L4 11%, L5 3%, L6 0%; meses 1–48 (mediana 7).

**Paso** `939537b6c800` (4215 veces): Lou has just joined and is over-familiar from the start. Within days she has asked whether you own or rent, whether you are seeing anyone and how you get on with your manager. At lunch she also presses you on 'who on the team doesn't get on'. She means no harm and just doesn't seem to know where the
- 1. Laugh it off and gently draw a line: 'Let's not go there. Talk about something else?' — dignity +1, network +1, skill +1; riesgo -0.13; expl3 -0.24; → `bf16e66fcb1f` (n=2379)
- 2. Be blunt: 'That's private. Please don't ask' — dignity +1, network -1; riesgo -0.03; expl3 +0.05; → `0d17bad6dec1` (n=565)
- 3. Answer each question, not wanting to embarrass a new colleague — dignity -1, health -1; riesgo +0.16; expl3 +0.19; → `1c06b932cd1a` (n=515)

**Paso** `bf16e66fcb1f` (3039 veces): Lou picks up on it, looks a bit embarrassed and stops. You move the conversation on to work and hobbies, and things feel normal again. A couple of days later she is asking about 'team gossip' again. She really does not seem to know where the line is.
- 1. Kindly suggest she gossips less and focuses on the work while she's new, for her own sake — network +2, skill +1, dignity +1; riesgo -0.05; expl3 -0.05 (n=1774)
- 2. Keep deflecting without spelling it out, and stay out of it — dignity +1; riesgo +0.05; expl3 +0.05 (n=523)

**Paso** `0d17bad6dec1` (520 veces): One sentence stops Lou in her tracks. She goes red, barely speaks to you for days, and tells other people you are 'quite fierce'. You held the line, but a new colleague was rattled and her settling in took a knock.
- 1. Find a moment to soften it: you just don't discuss your private life, and it wasn't personal — network +2, dignity +1, skill +1; riesgo -0.28; expl3 -0.12 (n=289)
- 2. Don't soften it. The boundary matters more than her feelings — dignity +1, network -1; riesgo +0.28; expl3 +0.12 (n=228)

**Paso** `1c06b932cd1a` (421 veces): You answered reluctantly, and Lou then chatted about your private life in the kitchen. Now it is out, you are on the back foot and wish you had drawn the line at the start.
- 1. Talk to Lou: ask her not to pass it on, and set the line from now on — dignity +1, skill +1, health -1; riesgo -0.32; expl3 -0.12 (n=217)
- 2. Call her out for gossiping, in the team channel or in front of people — network -2, dignity -1; riesgo +0.32; expl3 +0.12 (n=203)

## Christmas-party rehearsals eating your evenings

Aparece 4189 veces (primer paso): L1 63%, L2 15%, L3 9%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 5).

**Paso** `5a3fa16ce834` (4189 veces): The department is putting on an optional group number at the Christmas party. The organiser has booked evening rehearsals — an hour or two after work, most weekdays, for a fortnight. Your actual job is busy and your personal plans are a mess. It is voluntary. A lot of people are going, and your mana
- 1. Show up, and work with the organiser on a tighter rehearsal plan so the day job still fits — network +2, skill +1, dignity +1, health -1; riesgo -0.07; expl3 -0.28; → `566765c9f14b` (n=2343)
- 2. Attend every rehearsal and let the day job pile up — network +1, output -1, health -1; riesgo +0.27; expl3 +0.21; → `9e81d578e317` (n=548)
- 3. Skip a lot of sessions — “I’m not here to dance when there’s real work” — network -2; riesgo -0.20; expl3 +0.07; → `9080e113a19c` (n=541)

**Paso** `566765c9f14b` (2971 veces): You suggest splitting into small-group practice plus a few full run-throughs. It saves a lot of time, people stop staying late every night, and the organiser is grateful. Close to the party they have a family problem and ask whether you can take the last rehearsals and the on-the-night logistics.
- 1. Step up, run the last rehearsals and the night itself, and get the number on stage cleanly — skill +2, network +2, dignity +1, output +1, health -1; riesgo -0.14; expl3 -0.08 (n=1815)
- 2. Decline the lead: “I’ll keep rehearsing, but I’m not running the thing” — sin cambios; riesgo +0.14; expl3 +0.08 (n=423)

**Paso** `9080e113a19c` (503 veces): You miss so many sessions that the number cannot come together. The organiser is stuck, and the people who are showing up mutter that you are not a team player and you are holding them back. Close to the night, the piece is weaker because of the gaps you left.
- 1. Change tack, find time to catch up, and fill the hole you left — network +1, dignity +1, health -1; riesgo -0.31; expl3 -0.14 (n=273)
- 2. Stick to “the job matters more than dancing” and keep missing it — network -2, dignity -1; riesgo +0.31; expl3 +0.14 (n=220)

**Paso** `9e81d578e317` (467 veces): You stay late every night so you are not the weak link. Your actual work stacks up, and two month-end deliveries go wrong enough that your manager names you. A polished dance number does not make up for it. You can see you got the balance wrong.
- 1. Reorder your priorities: catch up on the work and put a limit on rehearsals — output +1, skill +1, dignity +1, health -1; riesgo -0.27; expl3 -0.18 (n=226)
- 2. Keep putting rehearsals first and let the work wait — output -2, dignity -2; riesgo +0.27; expl3 +0.18 (n=236)

## The office war over windows and heating

Aparece 4188 veces (primer paso): L1 60%, L2 15%, L3 9%, L4 11%, L5 4%, L6 0%; meses 1–48 (mediana 7).

**Paso** `77488149beeb` (4188 veces): The temperature in your corner of the open-plan office is a running sore. Hugh always feels hot and throws the windows open as soon as he arrives. Maya always feels cold, so she shuts them and turns the radiator up. It can go back and forth several times a day. Today they snap at each other in front
- 1. Propose a middle temperature, plus a small extra for each: a desk fan, a draught screen — skill +1, network +2, dignity +1; riesgo +0.04; expl3 -0.18; → `296dab11327d` (n=2255)
- 2. Make the call: set the temperature most people like, and tell them both to stop — dignity +1, network -1; riesgo -0.01; expl3 +0.10; → `78e43c634ee6` (n=570)
- 3. Keep your head down and work. It's not your problem — network -1, dignity -1; riesgo -0.04; expl3 +0.08; → `2bc01b1638f2` (n=607)

**Paso** `296dab11327d` (2910 veces): You set out what each of them needs and suggest a fixed middle temperature, a small screen to keep the draught off Maya, and a desk fan for Hugh. Both feel looked after, and most of the heat goes out of the row. To make it happen, someone has to ask facilities for the extras.
- 1. Take the lead with facilities and get the extras in — output +1, network +1, dignity +1, health -1, skill +1; riesgo -0.14; expl3 -0.06 (n=1742)
- 2. You had the idea. They can chase it themselves — network +1; riesgo +0.14; expl3 +0.06 (n=431)

**Paso** `2bc01b1638f2` (572 veces): You kept your head down. The two of them dug in further and ended up asking your manager to referee. Your manager frowns: 'You can't sort out something this small?' Everyone who could have stepped in and didn't, you included, now looks as if it is nothing to do with them. The atmosphere is awkward f
- 1. Step in late with a middle option so both of them have a way out — network +1, dignity +1, skill +1; riesgo -0.34; expl3 -0.15 (n=330)
- 2. Stay out of it. It's still not your problem — network -2, dignity -1; riesgo +0.34; expl3 +0.15 (n=239)

**Paso** `78e43c634ee6` (526 veces): You made the call and the row stopped. Maya, who lost out, feels hard done by, thinks you sided with the majority, and is cooler with you afterwards. Shutting the argument down did nothing for the person in the minority.
- 1. Talk to Maya privately and find her a way to keep warm, to soften the blunt call — network +2, dignity +1, skill +1; riesgo -0.34; expl3 -0.13 (n=279)
- 2. Majority rules. Nobody needs extra looking after — network -1; riesgo +0.34; expl3 +0.13 (n=240)

## A drunk colleague at the Christmas party

Aparece 4167 veces (primer paso): L1 62%, L2 16%, L3 9%, L4 10%, L5 3%, L6 0%; meses 1–48 (mediana 6).

**Paso** `75649c2a9f1c` (4167 veces): A few rounds into the Christmas party, Will, usually quiet, is loudly tearing into the department and is close to marching off to ‘have it out’ with your manager. Nobody else can get through to him. He is a decent person having a bad night. If this continues he will hate himself in the morning, and 
- 1. Steer him out, half-coaxing, half-supporting, and get him home with someone to look after him — network +2, dignity +1, health -1; riesgo -0.13; expl3 -0.21; → `bc7c1522a743` (n=2229)
- 2. Stay and watch, joining the crowd treating it as entertainment — network -1, dignity -1; riesgo +0.28; expl3 +0.21; → `3e82cb4c3196` (n=553)
- 3. Get well away so none of it lands on you, and leave him to it — network -1, dignity -1; riesgo -0.15; expl3 -0.01; → `01baf664974a` (n=632)

**Paso** `bc7c1522a743` (2865 veces): You get Will out before he does it in front of your manager. He is sick in the cab and, before he blacks out, mumbles a thanks. The next day he is mortified, and asks privately whether he made a scene and whether anyone senior saw.
- 1. Tell him the truth: it never reached your manager, and suggest he watch his drinking next time — network +2, dignity +1, skill +1; riesgo -0.36; expl3 -0.15 (n=1897)
- 2. Turn it into a story and tell it round the office in full colour — network -2, dignity -1; riesgo +0.36; expl3 +0.15 (n=239)

**Paso** `01baf664974a` (591 veces): You keep well clear. Will still unravels in public. Afterwards people know who was near him, who helped, and who vanished. People notice that you treated it as not your problem, and it quietly costs you.
- 1. Check in afterwards and help him limit the damage — network +1, dignity +1; riesgo +0.01; expl3 -0.05 (n=354)
- 2. Be glad you stayed out of it, and leave it there — network -1, dignity -1; riesgo -0.01; expl3 +0.05 (n=226)

**Paso** `3e82cb4c3196` (484 veces): You stay for the show. Will fully unravels in front of your manager, becomes office comedy the next day, and gets a formal conversation about it. He later finds out you were right there watching and did not pull him back, and he is gutted. You have lost someone who could have become a friend.
- 1. Apologise to Will, and put in a fair word for him with your manager — network +1, dignity +1, health -1; riesgo -0.28; expl3 -0.14 (n=244)
- 2. Shrug it off — you didn’t pour the drinks — network -2, dignity -1; riesgo +0.28; expl3 +0.14 (n=237)

## You overhear a redundancy list that includes a friend

Aparece 3069 veces (primer paso): L1 22%, L2 24%, L3 19%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `a75bc0f22588` (3135 veces): From a toilet cubicle you hear a VP and the HR director discussing the Q2 redundancy list: “…Ethan is in the consultation pool after the Lynx Wallet incident, package would be a standard redundancy…” Ethan is your tennis partner and helped you move last week. They wash their hands and leave, unaware
- 1. Tell no one and act as if you never heard it — dignity +2; riesgo -0.74; expl3 -0.31 (n=1090)
- 2. Hint that Ethan should keep his head down and not resign in a hurry — network +2; riesgo +1.12; expl3 -0.18; → `5d4b22fb4497` (n=348)
- 3. Tell him he is on the list and what the package looks like — network +3, dignity -2; riesgo -0.11; expl3 +0.64; → `b74621ceb19e` (n=768)
- 4. Tell Ethan only about the published redundancy process and support channels, and nothing you overheard — dignity +1, network +1; riesgo -0.26; expl3 -0.14 (n=141)

**Paso** `5d4b22fb4497` (442 veces): Ethan guesses you know and presses for detail. HR starts looking into who knew early.
- 1. Admit you overheard, but say you did not name the list — dignity +1, network -1; riesgo -0.94; expl3 -0.02 (n=108)
- 2. Help Ethan understand the consultation and how to prepare for it — network +2, dignity -1; riesgo +0.94; expl3 +0.02 (n=151)

**Paso** `b74621ceb19e` (255 veces): Ethan screenshots your messages about the package. It leaks. You are called into a meeting with compliance.
- 1. Cooperate and explain exactly how it got out — dignity +1, output -1; riesgo -1.28; expl3 +0.00 (n=231)
- 2. Deny you told him — dignity -3; riesgo +1.28; expl3 +0.00 (n=23)

## Burnout, and the urge to coast

Aparece 3028 veces (primer paso): L1 22%, L2 25%, L3 19%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `e15d3d102237` (3028 veces): You are exhausted, and one thought keeps coming back: pack it in and just coast. It is a classic sign of burnout, and decisions made on impulse now are the ones people regret. How do you deal with it?
- 1. Take it seriously: a few days' annual leave, a saner pace, and a workload talk with your manager if needed — health +1, dignity +1, skill +1; riesgo -0.35; expl3 -0.20 (n=1901)
- 2. Bottle it, pretend you are fine, and keep running on empty — health -2, output -1; riesgo +0.36; expl3 +0.09 (n=173)
- 3. Give in to the urge to coast and start phoning the work in — output -2, dignity -1; riesgo -0.01; expl3 +0.11 (n=177)

## Palpitations after weeks of overtime: whether to stop

Aparece 3018 veces (primer paso): L1 22%, L2 24%, L3 19%, L4 25%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `0de905fc3c15` (3082 veces): Two weeks of late nights. Tonight your heart races, your chest feels tight, and your hands shake. These are clear warning signs, but the task is almost done.
- 1. Stop now, rest, see a doctor if needed, and work at a steadier pace from tomorrow — health +2, output -1; riesgo -0.81; expl3 -0.07 (n=1730)
- 2. Drink some water, wait it out, and grind through to the end — output +1, health -2; riesgo +0.81; expl3 +0.07; → `5af41f10eca7` (n=522)

**Paso** `5af41f10eca7` (857 veces): You finish by pushing through, but the palpitations keep coming back over the next few days. You start to feel rattled.
- 1. Get checked straight away and make yourself keep a proper sleep routine — health +2, output -1; riesgo -0.24; expl3 -0.42 (n=291)
- 2. Tell yourself you are just tired and keep going round the clock — health -3; riesgo +0.24; expl3 +0.42 (n=70)

## Anonymous feedback — do you own up?

Aparece 3013 veces (primer paso): L1 22%, L2 24%, L3 20%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `652995a4e87d` (3191 veces): In the quarterly anonymous team survey you left specific suggestions about your manager's style, including some criticism. Afterwards they tell the team that 'anonymous feedback is cowardly — if there's a problem you should say it to my face'. A few days later they take you aside: 'I don't know who 
- 1. Own it, walk through the feedback in person, and offer constructive suggestions — dignity +3, skill +2, network +1; riesgo -0.13; expl3 -0.11; → `872c2542242f` (n=2112)
- 2. Deny it, suggest other possible sources, and protect the anonymity — dignity -2, network -1; riesgo +0.13; expl3 +0.11; → `807f005a6adb` (n=257)

**Paso** `872c2542242f` (2398 veces): Your manager praises you for raising it face to face, then gets defensive about the substance. They explain why those decisions were reasonable, and hint that 'you're only seeing a slice'.
- 1. Stand by what you observed, admit your view is partial, and suggest more openness about how decisions are made — skill +2, dignity +2, network +1; riesgo -0.90; expl3 -0.31 (n=1575)
- 2. Ease off, admit you may have lacked some information, and say you still rate their management overall — network +2, dignity -1; riesgo +0.90; expl3 +0.31 (n=137)

**Paso** `807f005a6adb` (217 veces): Your manager appears to accept the denial, but their expression says otherwise. Later, chances that would have been yours go to other people. The explanation is that 'others need more stretch'.
- 1. Find a better moment and admit you denied it to protect how anonymous feedback is meant to work — dignity +1, network +1; riesgo -0.55; expl3 -0.16 (n=128)
- 2. Live with it, let the work speak, and trust time to clear the misunderstanding — output +2, network -1; riesgo +0.55; expl3 +0.16 (n=82)

## Your idea is pitched first by someone else

Aparece 2996 veces (primer paso): L1 21%, L2 25%, L3 19%, L4 27%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `f017a8240772` (3189 veces): In a team brainstorm you suggest a design, but it gets little attention. Two weeks later a colleague pitches almost the same idea in a wider meeting, with some of the same wording. A VP likes it and asks them to lead it. You cannot tell whether they got there independently or borrowed yours. Either 
- 1. Speak to them privately afterwards, mention the discussion two weeks ago, and check where the idea came from — dignity +2, network +1; riesgo +0.17; expl3 +0.18; → `6b00dbae7557` (n=261)
- 2. Share your earlier thinking with the team, without directly challenging their claim to the idea — skill +1, network +1, dignity +1; riesgo -0.17; expl3 -0.18; → `2afc19f6340b` (n=2107)

**Paso** `2afc19f6340b` (2322 veces): Now the team knows the history. People start calling it 'your idea'. The colleague is offended and says in a meeting they understand you had thought in a similar direction, but they developed their proposal independently and took it to delivery.
- 1. Publicly recognise their independent development and delivery, and make clear you never questioned that — network +2, dignity +2, skill +1; riesgo -0.60; expl3 -0.18 (n=1529)
- 2. Leave it. Let the team decide who contributed what — network -1, dignity -1; riesgo +0.60; expl3 +0.18 (n=133)

**Paso** `6b00dbae7557` (212 veces): They say they do remember the chat, thought it was just thinking out loud, and had not realised how close it was to what they had in mind. They promise to credit you in later docs. The VP's impression of who proposed it will be hard to undo.
- 1. Accept the promise. Credit in the docs is enough — network +2, dignity +1; riesgo -0.00; expl3 -0.11 (n=128)
- 2. Ask them to say at the next update that the idea originally came from you — dignity +2, network +1; riesgo +0.00; expl3 +0.11 (n=77)

## Peer review finds a serious bug in a friend's code

Aparece 2992 veces (primer paso): L1 21%, L2 24%, L3 18%, L4 27%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `46b115f9aa63` (2992 veces): Craig, a colleague you get on well with, has an SQL injection risk in his merge request. He messages privately: “Merge it for now — I'll buy dinner tonight and fix it after.”
- 1. Block the review and require a fix before merge — dignity +2, skill +1, network -1; riesgo -1.25; expl3 -0.21 (n=1658)
- 2. Merge it and help him fix it this evening — network +1, dignity -1; riesgo +1.10; expl3 -0.03 (n=428)
- 3. Comment but do not block — dignity -1; riesgo +0.15; expl3 +0.23 (n=168)

## How intensely to mentor a new intern

Aparece 2990 veces (primer paso): L1 21%, L2 24%, L3 20%, L4 24%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `7520ec2f8620` (2990 veces): An intern, Alex, joined your team this week and, under company policy, is automatically assigned to you as mentor. The first two weeks matter most for onboarding. Alex is sharp but has no domain background and will need a lot of questions answered to get up to speed. Intensive mentoring (an hour of 
- 1. Mentor intensively so they can work independently within two weeks — skill +1, network +3, output -2, health -2; riesgo -0.43; expl3 -0.04 (n=1582)
- 2. Keep a light touch, let them explore, and stay focused on your own work — output +2, skill +1, network -2, health +1; riesgo +0.43; expl3 +0.04 (n=638)

## Whether to share the method you have kept to yourself

Aparece 2990 veces (primer paso): L1 21%, L2 24%, L3 20%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `1fd3c946c998` (3136 veces): The internal tech forum is calling for posts. You have a method for payments circuit breaking and graceful degradation that you have never shared, and it is what makes you hard to replace on the team. Publishing it would probably get a reaction from the CTO and help your promotion case, but colleagu
- 1. Publish the full version and build a personal brand — skill +2, network +3, output +1, dignity +2; riesgo -0.26; expl3 -0.10; → `0d67061a569f` (n=1828)
- 2. Post a cut-down version and keep the core parameters back — skill +1, network +1; riesgo +0.55; expl3 +0.06 (n=284)
- 3. Don't share it, and keep it to yourself — output +2, network -2; riesgo -0.29; expl3 +0.04 (n=172)

**Paso** `0d67061a569f` (2214 veces): The post takes off. Lauren uses the write-up to improve the system, and your manager asks you to standardise it across the team.
- 1. Lead training for the whole group and step up as the technical expert — skill +3, network +2, output +1, health -1; riesgo -0.31; expl3 -0.13 (n=1418)
- 2. Worry about being replaced and start holding things back again — network -1, dignity -1; riesgo +0.31; expl3 +0.13 (n=93)

## Do you say the code was AI-generated?

Aparece 2987 veces (primer paso): L1 21%, L2 25%, L3 19%, L4 26%, L5 7%, L6 1%; meses 6–48 (mediana 16).

**Paso** `73dc25a030ab` (3181 veces): You used an AI assistant to generate the core of a complex algorithm, edited it, and opened a pull request. The team has no rule on whether AI contributions need to be flagged. In review a colleague admires how clever the code is — and you realise they have no idea a model wrote the first draft.
- 1. Note in the PR that it was AI-assisted, and explain what you changed — dignity +2, skill +1, network +1; riesgo -0.40; expl3 -0.13; → `14eca1b3be70` (n=2072)
- 2. Say nothing extra, and let it read as ordinary engineering — dignity -1; riesgo +0.40; expl3 +0.13; → `76bf24f2cab8` (n=269)

**Paso** `14eca1b3be70` (2387 veces): Your candour sparks a team discussion about labelling AI-written code. Your manager asks you to lead on drafting a guideline.
- 1. Take it on and push for a team standard on being open about AI use — skill +2, network +2, output -1; riesgo +0.01; expl3 -0.01 (n=1154)
- 2. Suggest a more experienced colleague lead it, and stay involved — network +1, skill -1, output +1; riesgo -0.01; expl3 +0.01 (n=538)

**Paso** `76bf24f2cab8` (172 veces): Later the team finds bugs nobody had spotted in AI-generated code elsewhere, and starts checking which changes were labelled. Your pull request is dug out of the history.
- 1. Go to your manager, admit you did not label it, and say you should have thought it through — dignity +1, network -1; riesgo -0.49; expl3 -0.30 (n=98)
- 2. Wait to be asked, then stress that there was no clear rule at the time — dignity -1; riesgo +0.49; expl3 +0.30 (n=69)

## Neck pain with a deadline — whether to keep the physio appointment

Aparece 2984 veces (primer paso): L1 22%, L2 26%, L3 17%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 15).

**Paso** `71251431c1fc` (3153 veces): A stretch of late nights has left your neck aching and your right hand tingling. Physio is booked for tomorrow afternoon, which is also when a delivery checkpoint falls.
- 1. Keep the physio appointment and shift delivery by half a day — health +2; riesgo -0.14; expl3 -0.03 (n=249)
- 2. Move the appointment to the weekend and push through delivery first — health -1; riesgo -0.18; expl3 -0.11; → `fce9f15f4099` (n=1888)
- 3. Stick on a heat patch, tough it out, and leave physio for later — output +1, health -2; riesgo +0.32; expl3 +0.14 (n=173)

**Paso** `fce9f15f4099` (2257 veces): Delivery goes smoothly. At the weekend you get to physio, and while you are at it you buy a neck support and a sit-stand desk.
- 1. Use it as a prompt to change your habits, and set a timer to stand up — health +2, skill +1; riesgo -0.47; expl3 -0.09 (n=1496)
- 2. Once you feel better, go back to sitting all day — health -1; riesgo +0.47; expl3 +0.09 (n=96)

## Emergency hotfix — do you skip the process?

Aparece 2975 veces (primer paso): L1 22%, L2 24%, L3 19%, L4 27%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `97d36c58735f` (3146 veces): Production has a critical fault and needs an immediate hotfix. The standard path of code review, staging checks and a confirmed rollback would take about two hours. A client is in the middle of a live promotional stream, and every minute of downtime is a serious loss. The operations lead hints you c
- 1. Stick to the full process, and turn on a degraded mode to limit the impact on the client — skill +2, dignity +2, output -1; riesgo -1.31; expl3 -0.14; → `d70b2d6f0af7` (n=1812)
- 2. Ship on a shortened path while the team prepares a rollback and completes the review within an hour — output +2, skill +1, dignity -1; riesgo +1.31; expl3 +0.14; → `50a1ad6c7aee` (n=507)

**Paso** `d70b2d6f0af7` (2111 veces): The full process takes three hours. The client's live event is badly hit. The sales VP asks openly whether engineering's response time matches what the business needs. The wash-up shows the degraded mode did not fully cover the missing function.
- 1. In the wash-up, admit the process was too rigid, and propose a graded response for future emergencies — skill +2, dignity +1, network +1; riesgo -0.28; expl3 -0.11 (n=1390)
- 2. Stress quality first, and point out that a hotfix introducing a new fault would have cost more — dignity +2, network -2; riesgo +0.28; expl3 +0.11 (n=129)

**Paso** `50a1ad6c7aee` (459 veces): The hotfix goes out in time and the live event carries on. When the process is completed afterwards, it finds an edge case the fix missed. The rollback is ready, so there is no second incident. The CTO asks you privately what would have happened if the rollback had failed.
- 1. Admit the risk, and propose a pre-authorised emergency path that sets out when the process can be shortened — skill +2, dignity +1, network +1; riesgo +0.01; expl3 -0.28 (n=278)
- 2. Stress that this success shows the team's skill with incidents, and argue for keeping the current flexibility — output +1, dignity -1; riesgo -0.01; expl3 +0.28 (n=78)

## You notice promotions going to the people who play politics

Aparece 2974 veces (primer paso): L1 22%, L2 25%, L3 20%, L4 26%, L5 7%, L6 1%; meses 6–48 (mediana 16).

**Paso** `27004c40b56c` (3195 veces): You have watched this for three years. The fastest riser is Harvey: average technically, but he never misses karaoke, five-a-side or the pub after work. Your technical scores have topped the team for years, yet your promotion still lags. Chris says they also look at “the whole picture”.
- 1. Make more effort socially, without crossing your own lines — network +3, health -2, dignity -1; riesgo -0.29; expl3 -0.20; → `63f37880930a` (n=811)
- 2. Refuse to play along and double down on technical output — skill +3, output +3, network -2, dignity +2; riesgo -0.36; expl3 -0.18; → `c29bd1377046` (n=1266)
- 3. Tell Helen, the HR business partner, that the promotion criteria are too vague — dignity +2, network -1; riesgo +0.41; expl3 +0.15 (n=141)
- 4. Start looking elsewhere and ease off here — output -1, skill +1; riesgo +0.24; expl3 +0.24 (n=125)

**Paso** `c29bd1377046` (2218 veces): The CTO sees your talk at a tech conference and moves you into architecture, bypassing Chris's reporting line.
- 1. Take the move — skill +3, network +2, output +2, dignity +2; riesgo -0.06; expl3 -0.03 (n=1358)
- 2. Stay on the Lynx team — output +2; riesgo +0.06; expl3 +0.03 (n=211)

**Paso** `63f37880930a` (993 veces): Six months on, Harvey is promoted again. You get a tick for "collaboration" and are still behind.
- 1. Keep working the relationships — health -2, dignity -2; riesgo +0.29; expl3 +0.07 (n=41)
- 2. Go back to the technical path — skill +2, output +2, dignity +1; riesgo -0.29; expl3 -0.07; → `c29bd1377046` (n=643)

## Caffeine dependence and a broken sleep pattern

Aparece 2971 veces (primer paso): L1 21%, L2 25%, L3 18%, L4 26%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `7f809673d971` (2973 veces): You rely more and more on coffee and energy drinks. They get you through the day, then you cannot sleep, and the cycle repeats. Your focus and mood are both getting worse.
- 1. Reset: limit caffeine, keep a regular sleep routine and recover gradually — health +2, skill +1; riesgo -0.57; expl3 -0.11 (n=1941)
- 2. Keep relying on caffeine and finish what is in front of you first — output +1, health -2; riesgo +0.57; expl3 +0.11; → `9178d6ce5688` (n=271)

**Paso** `9178d6ce5688` (203 veces): Caffeine carries you for a while and you get the work done. Then you keep nodding off during the day and cannot sleep at all at night.
- 1. Finally cut out caffeine and get back to regular sleeping hours — health +2, output -1; riesgo -0.76; expl3 -0.15 (n=120)
- 2. Increase the dose and keep pushing — health -2; riesgo +0.76; expl3 +0.15 (n=75)

## Where personal use of work kit stops

Aparece 2970 veces (primer paso): L1 22%, L2 24%, L3 19%, L4 25%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `cacdaf5c484e` (3126 veces): The company issues a high-spec workstation and a 4K display. Policy allows 'limited personal use' without saying exactly where the limit is. You have started using the work kit for a personal open-source project that does not compete with the business, and at weekends it soaks up a fair amount of co
- 1. Stop using work kit for the personal project immediately, and move it onto your own machines — dignity +2, skill +1, wealth -1; riesgo +0.12; expl3 +0.01; → `721fa2282e6e` (n=944)
- 2. Ask your manager and compliance whether the current use sits inside policy, and get it in writing — dignity +2, network +1, output -1; riesgo -0.12; expl3 -0.01; → `275f67d8928c` (n=1371)

**Paso** `275f67d8928c` (1579 veces): Compliance confirm the current use sits inside 'limited personal use', and advise you to 'significantly reduce weekend usage to avoid perception issues'. The written confirmation is reassuring, and it also means the use is now on a formal record.
- 1. Cut weekend use as advised, and move most of the development onto personal kit in your own time — dignity +2, network +1; riesgo -0.68; expl3 -0.18 (n=1026)
- 2. Keep using it, but avoid commit times colleagues can see, and stay quiet about it — output +1, dignity -1; riesgo +0.68; expl3 +0.18 (n=111)

**Paso** `721fa2282e6e` (1025 veces): The personal project slows down. Colleagues notice how careful you are, and it quietly counts in your favour in the team. Someone in HR mentions in passing that they are reviewing personal use of kit, and that your approach is worth a look.
- 1. Join the review and share how you keep work and personal kit separate — network +2, dignity +2, output -1; riesgo +0.18; expl3 +0.04 (n=228)
- 2. Keep your head down. You don't need to preach about a personal choice — dignity +1; riesgo -0.18; expl3 -0.04 (n=547)

## Whether to warn that the sprint is overcommitted

Aparece 2970 veces (primer paso): L1 22%, L2 24%, L3 19%, L4 26%, L5 7%, L6 1%; meses 6–48 (mediana 16).

**Paso** `850b7ff65ee4` (2970 veces): In sprint planning, Product brings in far more story points than the team can handle. Your manager looks at you: “Can we do it?” Everyone else stays quiet.
- 1. Use the numbers to show the team is over capacity, and suggest cutting scope — skill +2, dignity +2, output +1; riesgo -0.62; expl3 -0.19 (n=1828)
- 2. Nod and take it on — output -1, network +1, health -2; riesgo +0.55; expl3 +0.09 (n=199)
- 3. Raise it privately with your manager after the meeting — network +1; riesgo +0.07; expl3 +0.10 (n=202)

## A former colleague asks you for internal company material

Aparece 2967 veces (primer paso): L1 22%, L2 23%, L3 19%, L4 25%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `a58cc54807be` (2967 veces): A former colleague gets in touch, very friendly, and asks a "small favour": send them some internal material or data. "You've got it to hand. It's not a big deal." The material is company property and covered by confidentiality. What do you do?
- 1. Decline, explain it is confidential company property that can't go outside, and keep things civil — dignity +1, skill +1; riesgo -0.81; expl3 -0.31 (n=1875)
- 2. Send the internal material because you feel you can't say no — dignity -1; riesgo +0.18; expl3 +0.23 (n=174)
- 3. Send it, plus extra they didn't ask for, to look generous — dignity -2, network -1; riesgo +0.62; expl3 +0.09 (n=159)

## Dependency upgrade breaks the build

Aparece 2961 veces (primer paso): L1 22%, L2 24%, L3 18%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `d8c4685218df` (2961 veces): Dependabot auto-upgrades a transitive dependency and main goes red. You suspect a breaking patch.
- 1. Revert immediately, pin the version, and find the cause — skill +2, output -1, dignity +1; riesgo -0.94; expl3 -0.19 (n=1615)
- 2. Hack the code to match the new version — skill +2, output +1, health -2; riesgo +0.54; expl3 -0.06 (n=403)
- 3. Disable Dependabot — skill -1; riesgo +0.40; expl3 +0.26 (n=192)

## How thorough to be in code review as the team grows

Aparece 2960 veces (primer paso): L1 23%, L2 23%, L3 18%, L4 27%, L5 8%, L6 0%; meses 6–48 (mediana 16).

**Paso** `bb5ccb9743b4` (3026 veces): Since the team expanded, the weekly review queue has jumped from five or six PRs to more than thirty. As technical owner, you are the named reviewer on most of the critical modules. Each PR now takes 30–40 minutes; one or two hours a day disappear into review. A new colleague's PR is in your queue: 
- 1. Review line by line and list every improvement — skill +2, network +1, output -2, health -2; riesgo -1.04; expl3 -0.07; → `f998abcab2f4` (n=1110)
- 2. Focus on core logic and risk, and leave the nits to the author — output +2, network +2, skill -1, health +1; riesgo +1.04; expl3 +0.07 (n=1150)

**Paso** `f998abcab2f4` (1445 veces): You leave more than thirty comments. The new colleague starts by working through them carefully, but after the third round they message you privately: should they run everything against your bar themselves before opening a PR? Your manager has noticed their PRs are merging more slowly and books a 1:
- 1. Turn the standard into a team code-review checklist and roll it out — skill +2, network -1, output +1, health -1; riesgo -0.73; expl3 -0.10 (n=796)
- 2. Go easier on this new colleague until they have found their feet — network +2, output +1, skill -1, health +1; riesgo +0.73; expl3 +0.10 (n=139)

## Grey-area items on a travel expense claim

Aparece 2945 veces (primer paso): L1 21%, L2 23%, L3 20%, L4 27%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `a14372106c74` (3124 veces): You have just finished a week on a client site and are putting the expenses together. A few items sit in a grey area: 1) coffees you bought the client as a gift (no VAT receipt, only a till slip); 2) a late dinner you ordered for yourself after overtime (policy covers a 'working meal'; late dinners 
- 1. Claim only the flights and hotels, which are clearly within policy, and drop every grey item — dignity +2, wealth -1; riesgo -0.72; expl3 -0.21; → `84e404ca743c` (n=2045)
- 2. Claim as usual, taking colleagues' advice that 'everyone does this, it's fine' — wealth +1, dignity -1; riesgo +0.72; expl3 +0.21; → `ad0a82ef8777` (n=274)

**Paso** `84e404ca743c` (2353 veces): Finance clears your claim quickly. Colleagues notice the total is well below what people usually claim and rib you over lunch: 'A bit too honest, aren't you? You've left money on the table.'
- 1. Say it is your own choice, and remind people what the policy actually allows — dignity +2, network -1; riesgo -0.23; expl3 -0.02 (n=527)
- 2. Smile it off. Keep your own standard without commenting on anyone else's — network +1, dignity +1; riesgo +0.23; expl3 +0.02 (n=1168)

**Paso** `ad0a82ef8777` (188 veces): The claim goes through. Next month a spot audit flags your late-dinner line as 'possible non-compliance'. Finance asks you to explain or repay.
- 1. Repay it, admit you should have been stricter, and promise to stick to the policy — dignity +1, wealth -1; riesgo -0.32; expl3 -0.31 (n=104)
- 2. Say you followed team custom, and suggest Finance stop chasing individuals and set a clear rule — network -1, dignity -1; riesgo +0.32; expl3 +0.31 (n=75)

## A job spec from the big tech firm you have always wanted to join

Aparece 2943 veces (primer paso): L1 22%, L2 26%, L3 19%, L4 24%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `bb11438fdc75` (2943 veces): You come across a role that closely matches yours at a company you have always wanted to work for. Reading the spec, you feel envious and a bit anxious, because you are not there yet. What do you do with that feeling?
- 1. Use the spec as a yardstick and close the gaps in your current role until you could get it — skill +2, dignity +1, output +1; riesgo -0.10; expl3 -0.15 (n=1872)
- 2. Spend the days daydreaming about leaving, refreshing job boards, and letting the day job drift — output -1, health -1; riesgo +0.33; expl3 +0.19 (n=176)
- 3. Envy it and do nothing, telling yourself you would never get there anyway — dignity -1; riesgo -0.22; expl3 -0.03 (n=163)

## A recruiter rings — do you take the call?

Aparece 2920 veces (primer paso): L1 22%, L2 25%, L3 18%, L4 26%, L5 8%, L6 1%; meses 6–48 (mediana 16).

**Paso** `bd1bc7fd3328` (2920 veces): A withheld number during work hours: a recruiter, wanting to talk about "a decent opportunity." You are not itching to leave, but it never hurts to know what the market looks like. How do you handle the call?
- 1. Arrange a time after work to hear them out, without disruption or commitment — network +1, skill +1, dignity +1; riesgo -0.17; expl3 -0.14 (n=1828)
- 2. Talk it through at your desk, loud enough that colleagues overhear — dignity -1; riesgo +0.40; expl3 +0.14 (n=151)
- 3. Hang up and block them, since even talking feels disloyal — network -1; riesgo -0.23; expl3 +0.00 (n=154)

## A junior asks to pair on your state machine

Aparece 2902 veces (primer paso): L1 22%, L2 24%, L3 20%, L4 25%, L5 9%, L6 1%; meses 6–48 (mediana 16).

**Paso** `49f5cda30810` (2902 veces): Intern Alex asks for two hours this afternoon to pair, so he can understand a state machine you wrote. You have a bug that needs to be fixed by four.
- 1. Reschedule: pair first, then fix the bug — network +3, skill +1, output -1, health -1; riesgo +0.04; expl3 +0.08 (n=176)
- 2. Point him at the docs and comments and let him work through it — output +1, skill +1, network -1; riesgo +0.01; expl3 -0.03 (n=292)
- 3. Pair for an hour and do the rest asynchronously — network +2, skill +1, health -1; riesgo -0.05; expl3 -0.06 (n=1692)

## Mentoring a graduate who breaks things

Aparece 2710 veces (primer paso): L1 25%, L2 30%, L3 18%, L4 21%, L5 6%, L6 1%; meses 6–48 (mediana 13).

**Paso** `ada84185618b` (2710 veces): The department has taken on a new batch of interns. Your manager gives you Sam, who has the flashiest university and the biggest ego, and hints that mentoring is an unofficial requirement for a top rating this year. You hear Sam nearly caused trouble in another team by merging unreviewed code, and m
- 1. Take it on and set out clearly how the mentoring will work — network +1, skill +1; riesgo +0.38; expl3 +0.12; → `626e71b5e7d5` (n=553)
- 2. Decline, citing your current workload — network -1, dignity +1; riesgo -0.38; expl3 -0.12; → `9f1b3214cac8` (n=1490)

**Paso** `626e71b5e7d5` (2382 veces): You have been mentoring Sam for barely two weeks when they skip your code review and merge lightly tested code into the pre-production branch. Staging is down all night and several neighbouring teams are blocked. At the next morning's standup your manager asks, stony-faced, 'Who is going to answer f
- 1. Take the main responsibility and say your oversight as mentor failed — dignity +2, output -1, network +1; riesgo -0.13; expl3 -0.15; → `b065278afba1` (n=1551)
- 2. Say in the room that the whole fault is Sam's — network -2, dignity -1; riesgo +0.13; expl3 +0.15 (n=182)

**Paso** `b065278afba1` (2105 veces): You took responsibility in public and Sam is hugely grateful. That afternoon your manager pulls you into a meeting room: 'We're already over our incident quota. Group wants a named person on the accountability report. If you keep this on yourself, the team can't carry it. I suggest you sign the draf
- 1. Sign the draft and put the main fault on Sam — wealth +1, network +1, dignity -2; riesgo -0.06; expl3 -0.06 (n=1393)
- 2. Rewrite it to match what happened: who skipped review, and which check in the process failed — dignity +1, network -1, output -1; riesgo +0.06; expl3 +0.06 (n=82)

**Paso** `9f1b3214cac8` (1958 veces): After you declined, Sam was given to Chris in the next team. Three months later Chris is seconded elsewhere, and Sam is behind on a client deliverable. Your manager calls you into a meeting room: 'You're the only person in the department who knows this area. You'll have to take over Sam's mentoring 
- 1. Take Sam on and help clear the backlog — health -2, skill +1, output +1, network +1; riesgo -0.58; expl3 -0.15; → `626e71b5e7d5` (n=1289)
- 2. Refuse again and say you do not have the capacity — network -2, dignity +1, output -1; riesgo +0.58; expl3 +0.15 (n=129)

## The company tries to keep you after you look elsewhere

Aparece 2704 veces (primer paso): L1 26%, L2 30%, L3 17%, L4 20%, L5 7%, L6 1%; meses 6–48 (mediana 13).

**Paso** `8e3aff4f9b76` (2704 veces): You have been unhappy and have quietly thought about looking for another job, and it has started to show in how you talk. Your manager notices, takes it seriously and comes back with a retention package: a rise, a project, even a hint that you would be first in line at the next promotion round. Your
- 1. Go back to why you wanted to leave, and only stay if the package actually fixes that — skill +1, dignity +1, network +1; riesgo -0.53; expl3 -0.24; → `6d5fb9c2f294` (n=1634)
- 2. Let the rise decide it, and drop the idea of leaving on the spot — wealth +1, dignity -1; riesgo +0.18; expl3 +0.02; → `92782979ad4e` (n=221)
- 3. Say you will stay, and keep looking on the quiet — wealth +1, network -1; riesgo +0.35; expl3 +0.22; → `463563d349a8` (n=157)

**Paso** `6d5fb9c2f294` (2247 veces): You think hard about why you wanted out. Was it money, growth, or a clash with how your manager works? Once that is clear, the question is whether this package fixes the thing you care about. Your manager is sincere and willing to listen.
- 1. Tell them what is really bothering you, agree a fix, then stay with a clear head — dignity +2, network +1, skill +1; riesgo -0.28; expl3 -0.11 (n=1470)
- 2. Feel too awkward to be honest, take the rise and leave the real problem unsolved — wealth +1, dignity -1; riesgo +0.28; expl3 +0.11 (n=100)

**Paso** `92782979ad4e` (178 veces): The rise puts an end to the idea of leaving. What actually bothered you, such as having no room to grow, is still there. A few months later the dissatisfaction is back. More awkwardly, the team has a rough idea that you nearly left and were bought back.
- 1. Face the real issue: discuss your career path with your manager so that staying changes something — skill +1, network +1, dignity +1, output +1; riesgo -0.28; expl3 -0.10 (n=114)
- 2. Muddle on, and let your attitude sour — dignity -2, output -1, health -1; riesgo +0.28; expl3 +0.10 (n=59)

**Paso** `463563d349a8` (104 veces): You take the rise and keep looking. It shows. Your manager finds out you are still interviewing, trust collapses, and the project and the promotion hint are withdrawn. You keep the money you were already given. You are still here, in a worse position.
- 1. Stop sitting on the fence, commit, and win trust back by being consistent — dignity +1, network +1, output +1, health -1; riesgo -0.80; expl3 -0.31 (n=67)
- 2. Keep both options vaguely alive, one more day at a time — network -2, dignity -2; riesgo +0.80; expl3 +0.31 (n=35)

## A merge conflict wrecks release day

Aparece 2599 veces (primer paso): L1 26%, L2 28%, L3 18%, L4 21%, L5 6%, L6 1%; meses 6–48 (mediana 13).

**Paso** `51a246f17b72` (2599 veces): On release day you are merging the release branch. After a long session resolving conflicts, you accidentally pull in untested feature-branch code. CI is green because a flaky test skipped one check.
- 1. Halt the release as soon as you notice and roll the merge back — skill +2, dignity +1, output -1; riesgo -1.09; expl3 -0.23; → `3387abd67dfe` (n=1433)
- 2. Carry on with the release and gamble that the code path will not be hit — output +1; riesgo +0.48; expl3 +0.31; → `df3b77834e73` (n=202)
- 3. Quietly hotfix the wrongly merged files out — dignity -1; riesgo +0.61; expl3 -0.08; → `a3e5e635212d` (n=337)

**Paso** `3387abd67dfe` (2214 veces): The release slips a day. Your manager asks why.
- 1. Hold a review and add a release checklist — skill +2, network +1, dignity +1; riesgo -0.12; expl3 -0.11 (n=1469)
- 2. Just say the merge went wrong — sin cambios; riesgo +0.12; expl3 +0.11 (n=138)

**Paso** `a3e5e635212d` (332 veces): The hotfix introduces a new conflict. CI goes red.
- 1. Stop the release completely and roll the merge back — skill +1; riesgo -0.31; expl3 -0.30; → `3387abd67dfe` (n=224)
- 2. Force the hotfix through — output -1; riesgo +0.31; expl3 +0.30 (n=50)

**Paso** `df3b77834e73` (126 veces): Production hits an unexpected UI crash.
- 1. Roll back immediately and take responsibility — dignity +1, health -1; riesgo -0.52; expl3 -0.20 (n=88)
- 2. Make sure everyone knows whose feature it was — network -2; riesgo +0.52; expl3 +0.20 (n=32)

## The pay rise did not come through — coast in protest?

Aparece 2254 veces (primer paso): L1 5%, L2 11%, L3 30%, L4 39%, L5 14%, L6 1%; meses 12–48 (mediana 23).

**Paso** `f140d5344d9f` (2254 veces): Your request for a pay rise got nowhere this time. Your manager only said 'let's see'. You feel deflated, and your energy for the work drops. What next?
- 1. Hold your nerve, keep delivering, build your case for next time, and agree a date to revisit it — skill +1, output +1, dignity +1; riesgo -1.02; expl3 -0.16 (n=1455)
- 2. Protest by coasting and drag your feet on everything you can — output -1, dignity -1; riesgo +0.51; expl3 +0.07 (n=57)
- 3. In a huff, tell the whole office 'I'll walk', with no actual plan — network -2, dignity -1; riesgo +0.51; expl3 +0.09 (n=40)

## You notice a remote colleague is often offline

Aparece 2254 veces (primer paso): L1 6%, L2 10%, L3 30%, L4 38%, L5 13%, L6 2%; meses 12–48 (mediana 23).

**Paso** `3f7c2f0d5bfb` (2394 veces): While working remotely you notice a colleague you get on with is often offline in working hours, with Slack showing them away for more than three hours, yet their output has not obviously dropped. The team is meant to be outcomes-led, and you also know they are looking after a sick relative.
- 1. Check in privately: ask how they are, and whether they need help or a change to the arrangement — network +2, dignity +1; riesgo -0.62; expl3 -0.14; → `9a31f8d9f452` (n=1575)
- 2. Leave it and trust that managing by outcomes will sort it out — network -1; riesgo +0.62; expl3 +0.14; → `2a24299330d4` (n=87)

**Paso** `9a31f8d9f452` (1897 veces): They admit they are caring for family, and that they are already thinking about leaving. Their exit would leave a hole on a key project.
- 1. Help them ask your manager for flexible working, and try to keep them in the team — network +2, skill +1, dignity +2; riesgo -0.80; expl3 -0.16 (n=1240)
- 2. Tell them to decide in their own time, and stay out of it — network +1; riesgo +0.80; expl3 +0.16 (n=55)

**Paso** `2a24299330d4` (76 veces): Your manager reviews the remote-working data, spots the unusual away time, and asks whether you knew.
- 1. Say you had noticed they were stretched, and suggest the manager speak to them directly — dignity +1, network -1; riesgo -0.37; expl3 +0.07 (n=20)
- 2. Say you did not know, and offer nothing further — network +1, dignity -1; riesgo +0.37; expl3 -0.07 (n=52)

## A Glassdoor post about the company is doing the rounds

Aparece 2250 veces (primer paso): L1 6%, L2 8%, L3 28%, L4 42%, L5 15%, L6 2%; meses 12–48 (mediana 24).

**Paso** `14a55d5bc427` (2250 veces): A tell-all post about the company is spreading fast on Glassdoor, and only half of it is true. People in the team channel are forwarding it and stirring things up, and they ask what you think.
- 1. Don't spread it or take sides, and pay attention only to facts that affect you — dignity +1; riesgo -1.24; expl3 -0.20 (n=1480)
- 2. Forward it eagerly to every chat, adding your own embellishments — network -1; riesgo +0.73; expl3 +0.09 (n=48)
- 3. Leave an anonymous comment adding more detail — dignity -1; riesgo +0.50; expl3 +0.11 (n=58)

## Team morale is on the floor — should you step up?

Aparece 2248 veces (primer paso): L1 6%, L2 10%, L3 29%, L4 40%, L5 13%, L6 2%; meses 12–48 (mediana 23).

**Paso** `d12cb1323b3a` (2248 veces): After the turmoil, the team is scattered and morale is low. Nobody has much energy for the work, and the gloom is spreading. You are not the manager, but your attitude still rubs off on the people around you.
- 1. Keep up your own pace, and privately give nearby colleagues some encouragement and a calmer view of things — network +2, dignity +1, output +1; riesgo -0.53; expl3 -0.17 (n=1455)
- 2. Join the gloom, pile into the complaining, and make the pessimism louder — output -1, network -1; riesgo +0.51; expl3 +0.20 (n=48)
- 3. Treat it as none of your business, look after yourself, and ignore the team's mood — network -1; riesgo +0.01; expl3 -0.03 (n=62)

## A dependent team is late — do you escalate in the open?

Aparece 2237 veces (primer paso): L1 6%, L2 8%, L3 29%, L4 42%, L5 13%, L6 2%; meses 12–48 (mediana 23).

**Paso** `018d96935057` (2368 veces): A critical piece of work your project depends on, owned by a sister team, is already two weeks late. Their tech lead says privately they 'need another week' but will not update the official plan. The risk to your project is about to show in an update to senior management. You can keep coordinating q
- 1. Escalate the risk to senior leadership and ask for a firm delivery commitment — dignity +2, network -2, output +1; riesgo -0.93; expl3 -0.08; → `c399a11d5d5d` (n=990)
- 2. Keep coordinating privately, give them another week's buffer, and prepare a stopgap — network +2, skill +1, output -1; riesgo +0.93; expl3 +0.08; → `6d386680bb54` (n=632)

**Paso** `c399a11d5d5d` (1004 veces): Once senior managers are involved, the other team is held to a hard deadline. Their tech lead tells you privately that 'there will be no more informal flexibility after this'. The working atmosphere sours.
- 1. Go to their tech lead, explain the escalation was about project risk, and try to repair the relationship — network +1, dignity +2; riesgo +0.71; expl3 +0.03 (n=423)
- 2. Accept the new way of working: formalise every dependency and drop the informal chasing — skill +2, network -1; riesgo -0.71; expl3 -0.03 (n=395)

**Paso** `6d386680bb54` (942 veces): A week later they still have not delivered, and your stopgap cannot fully cover the gap. In the project update your risk warning looks late. A VP asks why you are only saying so now.
- 1. Own your misjudgement of the risk, and ask for a more formal way of tracking cross-team dependencies — dignity +2, skill +2, network -1; riesgo -0.38; expl3 -0.27 (n=493)
- 2. Point to the other team's history of slipping, and stress you could only judge what you could see — network -2, dignity -1; riesgo +0.38; expl3 +0.27 (n=24)

## Balancing a promising idea against delivery pressure

Aparece 2236 veces (primer paso): L1 6%, L2 10%, L3 29%, L4 41%, L5 13%, L6 1%; meses 12–48 (mediana 23).

**Paso** `77275d2f0b94` (2333 veces): You have spotted a new technical approach that could make the system much more efficient, but checking whether it works would take two to three weeks. The current sprint is already full, and your manager is clear that 'delivery commitments are non-negotiable'. You could explore it in your own time, 
- 1. Ask for 20% of the sprint to explore, and commit to dropping it if there is no breakthrough in two weeks — skill +2, dignity +2, output -1, network +1; riesgo -0.40; expl3 -0.05; → `9b0e720933d0` (n=559)
- 2. Explore in your own time, and only ask for formal resource once you have early results — skill +1, health -2, output +1; riesgo +0.40; expl3 +0.05; → `ad52a153fc57` (n=1093)

**Paso** `ad52a153fc57` (952 veces): Three months of evenings produce a breakthrough and a solid case for the efficiency gain. When you ask your manager for formal resource, a colleague in the same sprint proposes a similar optimisation: it uses the current tech, ships sooner and gains less.
- 1. Compare the two on depth and long-term return, and argue yours is worth the bigger investment — skill +2, dignity +2, network -1; riesgo +0.41; expl3 +0.07 (n=40)
- 2. Back the quicker option, and get your work put on the roadmap for later — network +2, dignity +1, skill +1; riesgo -0.41; expl3 -0.07 (n=826)

**Paso** `9b0e720933d0` (915 veces): The request is approved. Some of the team are unhappy: their work is also queued, so why do you get time? Two weeks later the idea is technically viable, but the implementation is more complex than expected and needs more time.
- 1. Be open about the extra complexity, and ask the team to decide whether it is worth continuing — dignity +2, skill +2, network +1, output -1; riesgo -1.17; expl3 -0.27 (n=415)
- 2. Promise to finish the implementation yourself, without team time, in return for permission to keep going — skill +2, health -2, output -1; riesgo +1.17; expl3 +0.27 (n=21)

## You find out a peer got a bigger increase

Aparece 2225 veces (primer paso): L1 6%, L2 10%, L3 31%, L4 40%, L5 13%, L6 1%; meses 12–48 (mediana 23).

**Paso** `8ee638c2e75c` (2225 veces): Pay-review outcomes are out. You learn privately that a peer at the same level got a larger increase. It sits badly, and you start to wonder whether you have been short-changed.
- 1. Compare contributions, find what you can improve, and if needed ask your manager how the assessment was done — skill +1, dignity +1, output +1; riesgo -0.64; expl3 -0.13 (n=1420)
- 2. Stew in jealousy, take against that colleague, and compete with them behind their back — network -1, dignity -1; riesgo +0.46; expl3 +0.00 (n=59)
- 3. Ask around what everyone got and spread the comparison to whoever will listen — network -2, dignity -1; riesgo +0.18; expl3 +0.13 (n=57)

## Your manager gives you a rise — with a lot more work attached

Aparece 2211 veces (primer paso): L1 5%, L2 9%, L3 29%, L4 41%, L5 14%, L6 2%; meses 12–48 (mediana 24).

**Paso** `15bda0715899` (2211 veces): Your manager offers you a rise, then adds, 'Now that the pay is up, you can take on these extra bits of the business as well.' The increase is real, and so is the extra load. The two may not balance.
- 1. Weigh the extra work against the increase, take what is fair, and say so if it would overload you — skill +1, dignity +1, output +1; riesgo -0.42; expl3 -0.03 (n=561)
- 2. Get carried away by the rise and accept every new piece of work without counting the load — output +1, health -2; riesgo +0.08; expl3 -0.05 (n=938)
- 3. Take the rise but quietly dodge the extra work — network -1, dignity -1; riesgo +0.33; expl3 +0.08 (n=48)

## Your manager blames 'the climate' to keep your increase down

Aparece 2207 veces (primer paso): L1 6%, L2 9%, L3 30%, L4 41%, L5 14%, L6 1%; meses 12–48 (mediana 24).

**Paso** `944fa5bf9273` (2207 veces): In the pay-review conversation you name a figure and your manager waves it off: 'The climate is grim this year. The whole company is tightening its belt — that increase isn't realistic.' The wider economy is being used as cover to talk you down.
- 1. Acknowledge the climate, then bring the conversation back to your actual contribution and market rates — skill +1, dignity +1, output +1; riesgo -0.30; expl3 -0.07 (n=1403)
- 2. Lose heart at 'the climate' and cut your ask to something tiny — wealth -1, dignity -1; riesgo -0.27; expl3 +0.07 (n=61)
- 3. Get heated and snap that the climate is nothing to do with you, and the conversation turns into a row — network -1, dignity -1; riesgo +0.57; expl3 -0.00 (n=64)

## Whether to volunteer as lunch-and-learn speaker

Aparece 2206 veces (primer paso): L1 6%, L2 10%, L3 30%, L4 40%, L5 14%, L6 1%; meses 12–48 (mediana 24).

**Paso** `8b9bf5486c95` (2206 veces): The team's lunch-and-learn needs a speaker for the next slot. The topic is callback idempotency, which you have just worked on. Signing up means about 40 minutes of slides, and this week's calendar is already full.
- 1. Volunteer to speak — skill +2, network +2, output -1, health -1; riesgo +0.11; expl3 -0.03 (n=161)
- 2. Suggest that Priya, who knows this area well, gives the talk — network +2, skill +1, dignity +1; riesgo +0.13; expl3 +0.01 (n=1119)
- 3. Don't sign up. Stay on delivery — output +2, network -1; riesgo -0.25; expl3 +0.02 (n=266)

## Whether to tell your manager about a health problem

Aparece 2204 veces (primer paso): L1 5%, L2 10%, L3 28%, L4 41%, L5 14%, L6 2%; meses 12–48 (mediana 24).

**Paso** `785d8f808711` (2214 veces): A follow-up appointment confirms a health problem that needs a course of treatment and will sap your energy. You cannot decide whether to tell your manager. If you say something, you worry you will be treated differently and kept off important work. If you say nothing, you worry about pushing throug
- 1. Tell your manager, tactfully, that you need a lighter load for a while and will keep quality up — health +2, dignity +1, output -1; riesgo -1.35; expl3 -0.15 (n=1378)
- 2. Tell nobody. Treat it quietly and push through — health -1, output +1; riesgo +1.35; expl3 +0.15; → `f5141bfadc00` (n=155)

**Paso** `f5141bfadc00` (160 veces): You hide it and push through, and for a while the work gets done. Then, on a critical piece of work, you run out of steam, and people start to speculate.
- 1. Come clean now and adjust the plan — health +1, dignity +1, output -1; riesgo -0.51; expl3 -0.20 (n=37)
- 2. Keep hiding it and gamble that nobody notices — health -2, dignity -1; riesgo +0.51; expl3 +0.20 (n=65)

## Your first reaction to finding out a newer hire is paid more

Aparece 2202 veces (primer paso): L1 6%, L2 10%, L3 31%, L4 40%, L5 13%, L6 1%; meses 12–48 (mediana 23).

**Paso** `46685c440d04` (2202 veces): You find out by accident that a newly hired colleague in the same role, with less experience, is paid more than you. It rankles. What is your first move?
- 1. Collect yourself, gather your results, and ask your manager for a pay review at the right moment — skill +1, dignity +1, output +1; riesgo -0.68; expl3 -0.12 (n=1426)
- 2. Start coasting in protest and stop doing the work properly — output -1, dignity -1; riesgo +0.12; expl3 -0.01 (n=50)
- 3. Complain round the team about how unfair the company is, and spread the discontent — network -2, dignity -1; riesgo +0.56; expl3 +0.14 (n=43)

## Christmas at home clashing with the on-call rota

Aparece 2195 veces (primer paso): L1 5%, L2 10%, L3 30%, L4 40%, L5 13%, L6 2%; meses 12–48 (mediana 24).

**Paso** `4a1527dd4a1d` (2195 veces): You are on the Christmas on-call rota, which clashes with going home for the break. It is the only time in the year your older relatives really get together.
- 1. Negotiate a fair swap with a colleague, and offer to cover them later — network +1, dignity +1, health +1; riesgo -0.19; expl3 -0.05 (n=1165)
- 2. Quietly accept the shift and skip going home — output +1, dignity -1, health -1; riesgo -0.32; expl3 -0.08 (n=306)
- 3. Skip the on-call shift without warning anyone — network -2; riesgo +0.51; expl3 +0.14 (n=50)

## Pay-review percentages are out — dwell on the ranking?

Aparece 2192 veces (primer paso): L1 6%, L2 9%, L3 29%, L4 42%, L5 13%, L6 1%; meses 12–48 (mediana 24).

**Paso** `0d4638eb2f6b` (2192 veces): Somehow everyone's pay-review percentage has been shared around the team, or a colleague has turned the figures into a comparison table. Yours is in the middle, neither top nor bottom. Looking at the table feels a bit awkward.
- 1. Look once, put it away, and spend your energy getting better so your next review is stronger — skill +1, dignity +1; riesgo -0.52; expl3 -0.12 (n=1413)
- 2. Keep staring at the ranking, feel more aggrieved each time, and let it hit your mood and your work — output -1, health -1; riesgo +0.37; expl3 +0.10 (n=62)
- 3. Take the comparison table to your manager and demand an explanation of every difference — network -1, dignity -1; riesgo +0.15; expl3 +0.02 (n=40)

## Cost-cutting hits perks — join the complaining?

Aparece 2189 veces (primer paso): L1 6%, L2 8%, L3 31%, L4 41%, L5 12%, L6 1%; meses 12–48 (mediana 23).

**Paso** `758728710c9c` (2189 veces): The company is talking about 'efficiency' and has cut some perks, tightened expenses, and shrunk the budget for team socials. The kitchen is full of moaning, and someone starts calling the company tight. You are not thrilled either.
- 1. Accept the company is under pressure, focus on making yourself more valuable, and stay out of the griping — dignity +1, skill +1; riesgo -0.87; expl3 -0.07 (n=1380)
- 2. Lead the public complaining and stir people into having a go at the company — network -1, dignity -1; riesgo +0.76; expl3 +0.05 (n=53)
- 3. Protest by coasting: the perks have gone, so you do less work — output -1, dignity -1; riesgo +0.10; expl3 +0.02 (n=48)

## At the demo, your manager praises Product and not engineering

Aparece 2186 veces (primer paso): L1 6%, L2 9%, L3 29%, L4 42%, L5 13%, L6 2%; meses 12–48 (mediana 24).

**Paso** `d389f5a4418e` (2186 veces): At the sprint demo, your manager says the product design was excellent and does not mention the late nights engineering put in. The client is on the call.
- 1. After the demo, email the client (cc'd) with the technical highlights — output +1, dignity +1, network -1; riesgo -0.09; expl3 +0.02 (n=999)
- 2. Jump in on the call to explain how engineering built it — dignity +1, network -1, skill +1; riesgo +0.20; expl3 +0.01 (n=158)
- 3. Say nothing — dignity -1, output -1; riesgo -0.11; expl3 -0.03 (n=341)

## Should you leave the company a bad Glassdoor review?

Aparece 2183 veces (primer paso): L1 6%, L2 10%, L3 28%, L4 41%, L5 14%, L6 1%; meses 12–48 (mediana 23).

**Paso** `a89cf738e92b` (2183 veces): You have a stack of grievances and fancy leaving a low score and a rant on Glassdoor, as a warning for the next person and a chance to get it off your chest.
- 1. If you write, stick to facts: no exaggeration, no confidential detail, no personal attacks — dignity +1; riesgo +0.41; expl3 -0.03 (n=51)
- 2. Write a long, emotional recap of every grievance, including unverified claims — dignity -1; riesgo +0.77; expl3 +0.20 (n=62)
- 3. Hold off, and use the frustration to decide properly whether to stay or go — dignity +1, health +1; riesgo -1.17; expl3 -0.17 (n=1408)

## Annual bonus cut and paid in instalments

Aparece 2173 veces (primer paso): L1 6%, L2 10%, L3 29%, L4 40%, L5 14%, L6 2%; meses 12–48 (mediana 24).

**Paso** `fdefc81be72f` (2173 veces): The company announces that the annual bonus, which your contract describes as discretionary, is being reduced and paid over several quarters, citing 'cash-flow management'. A contractual sum could not be cut like this without your agreement. As it is, your expected pay takes a hit, and the move says
- 1. Take it as a warning: look hard at the company's prospects and adjust your own plans — network +1; riesgo -0.80; expl3 -0.13 (n=1408)
- 2. Complain in public and lead the moaning — dignity -1, network -1; riesgo +0.49; expl3 +0.07 (n=50)
- 3. Tell yourself at least they are still paying it, and try not to think about it — sin cambios; riesgo +0.31; expl3 +0.06 (n=45)

## A colleague rushed to hospital: a warning for you

Aparece 2170 veces (primer paso): L1 6%, L2 10%, L3 30%, L4 39%, L5 14%, L6 1%; meses 12–48 (mediana 23).

**Paso** `8cd89c9101bc` (2170 veces): A colleague around your age, who also works late as a habit, is rushed into hospital. The news hits the team hard. Your stomach drops, because you have been living the same way.
- 1. Rebuild your sleep and exercise routine, and start actively managing your health — health +2, skill +1; riesgo -0.70; expl3 -0.07 (n=1270)
- 2. Feel shaken for a bit, then get busy and forget — health -1; riesgo +0.61; expl3 +0.13 (n=47)
- 3. Use the moment to start a team conversation about cutting pointless overtime — network +1, dignity +1, health +1; riesgo +0.09; expl3 -0.06 (n=167)

## The new manager from outside wants you to inform on the team

Aparece 2169 veces (primer paso): L1 5%, L2 10%, L3 29%, L4 40%, L5 14%, L6 1%; meses 12–48 (mediana 24).

**Paso** `7299fe171a1b` (2169 veces): The manager hired from outside wants a quick picture of the team and takes you aside: 'You've been here. Tell me how people really are and who has issues. I'll remember you for it.' It could be a chance to be useful. It could also be a trap that makes you the informant.
- 1. Give a fair picture of the team and the work, without informing on anyone or running them down — dignity +1, network +1, skill +1; riesgo -0.34; expl3 -0.06 (n=984)
- 2. Embellish complaints about colleagues to please the new manager — network -2, dignity -2; riesgo +1.05; expl3 +0.16 (n=52)
- 3. Refuse outright and brusquely, even to give a normal briefing — network -1; riesgo -0.72; expl3 -0.10 (n=448)

## Colleagues want you to join a group pay demand

Aparece 2169 veces (primer paso): L1 5%, L2 9%, L3 29%, L4 43%, L5 12%, L6 1%; meses 12–48 (mediana 23).

**Paso** `6e13acf42332` (2169 veces): A few colleagues unhappy with pay have organised and want to go to your manager together to 'push for an across-the-board increase'. They want you in: 'There's strength in numbers — come on.' You worry your manager will treat a group conversation as trouble. That would be his own reading. No rule sa
- 1. Back a written case through a staff representative, and do not corner anyone — skill +1, dignity +1; riesgo -0.48; expl3 -0.09 (n=1276)
- 2. Decline the group pressure and make your own pay-review case on your contribution — skill +1, dignity +1; riesgo -0.27; expl3 +0.02 (n=35)
- 3. Join in, and block the doorway so your manager cannot leave until you have an answer — network -1, dignity -1; riesgo +1.23; expl3 +0.21 (n=37)
- 4. Want to join but fear the blowback, so half-agree and then pull out at the last minute — network -1, dignity -1; riesgo -0.48; expl3 -0.14 (n=147)

## Funding and listing rumours — bet on the share options?

Aparece 2168 veces (primer paso): L1 6%, L2 10%, L3 30%, L4 40%, L5 13%, L6 2%; meses 12–48 (mediana 23).

**Paso** `07c8e918cda5` (2168 veces): Word is the company is raising money or heading for a listing. People talk as if the share options will make them rich, and they tell you to 'hang on a few more years for the options — don't leave'. The rumours are hard to pin down and a payout looks a long way off. You are not sure you should hang 
- 1. Count the share options as a possible bonus and decide on the fundamentals of the job — skill +1, dignity +1; riesgo -0.52; expl3 -0.14 (n=1375)
- 2. Turn down a better offer in front of you and stay put for options that have been over-promised — dignity -1; riesgo +0.52; expl3 +0.13 (n=43)
- 3. Ignore the options entirely, count only cash, and leave as soon as something better comes up — sin cambios; riesgo -0.00; expl3 +0.01 (n=58)

## Whether to volunteer as organiser of the annual team offsite

Aparece 2162 veces (primer paso): L1 6%, L2 9%, L3 31%, L4 39%, L5 14%, L6 1%; meses 12–48 (mediana 24).

**Paso** `6a1d1ec95b66` (2162 veces): This year's department offsite needs an internal organiser from each team: surveying preferences, choosing the format (outdoors, a meal, board games), liaising with HR and facilities, and hosting on the day. It has nothing to do with OKRs, but it shapes two days for more than eighty people, and it i
- 1. Volunteer as organiser — network +3, skill +1, output -2, health -2; riesgo +0.05; expl3 -0.00 (n=470)
- 2. Do not volunteer, and save your energy for the scheduled project — output +3, network -2, skill -1, health +1; riesgo -0.05; expl3 +0.00 (n=1047)

## You think the project bonus split is unfair

Aparece 2146 veces (primer paso): L1 5%, L2 10%, L3 29%, L4 40%, L5 14%, L6 1%; meses 12–48 (mediana 23).

**Paso** `a51bfd3b129a` (2146 veces): A project closes and bonuses go out. You did most of the work, yet your share is roughly the same as people who barely showed up. The colleague who ran the split clearly favoured some over others. It feels unfair.
- 1. Raise your actual contribution with whoever ran the split or your manager, and ask for a fairer adjustment — skill +1, dignity +1, output +1; riesgo -0.67; expl3 -0.07 (n=1305)
- 2. Swallow it, say nothing, and go cold on the project from here — dignity -1, output -1; riesgo +0.02; expl3 -0.11 (n=146)
- 3. Lose your temper and threaten to coast on the next project, saying nobody should count on you — output -1, network -1; riesgo +0.64; expl3 +0.18 (n=51)

## The new manager's first team meeting: make an impression?

Aparece 2142 veces (primer paso): L1 5%, L2 9%, L3 30%, L4 40%, L5 14%, L6 1%; meses 12–48 (mediana 24).

**Paso** `c4c50e3cc4c6` (2142 veces): The manager hired from outside is holding their first team meeting, and this is when they start to size everyone up. You wonder whether to push yourself forward and make a good first impression.
- 1. Come prepared and give a clear, professional update on your work and thinking, without hogging the floor — skill +1, output +1, dignity +1, network +1; riesgo -0.24; expl3 -0.07 (n=1367)
- 2. Talk over people, overstate your role, and put colleagues down to make yourself look good — network -2, dignity -1; riesgo +0.63; expl3 +0.05 (n=55)
- 3. Keep your head down and say nothing all meeting, terrified of saying the wrong thing — dignity -1, network -1; riesgo -0.39; expl3 +0.01 (n=49)

## An undeclared relationship that looks like a conflict of interest

Aparece 1975 veces (primer paso): L1 2%, L2 3%, L3 17%, L4 57%, L5 19%, L6 2%; meses 18–48 (mediana 29).

**Paso** `7f4fb6deb62e` (2083 veces): Late at night in the office you catch a department lead in a clearly intimate moment with someone who reports to them — well beyond a normal working relationship. That manager is currently reviewing the report's promotion pack, and has just changed their reporting line 'to develop them more closely'
- 1. Raise it anonymously with HR as a conflict-of-interest risk and ask them to look into it — dignity +2, network -2; riesgo -0.38; expl3 -0.27; → `d00919181ae0` (n=536)
- 2. Say nothing. It is their private life, and you have no hard evidence — network +1, dignity -1; riesgo +0.38; expl3 +0.27; → `f0ff4ae34269` (n=883)

**Paso** `f0ff4ae34269` (848 veces): Three months later that report is promoted. Other candidates feel the process was unfair and cannot say so. In an exit interview, one of them mentions 'an undeclared conflict in the promotion review'. HR traces it back and asks whether you knew.
- 1. Admit what you saw, and explain you were not sure at the time whether you should report it — dignity +1, network -1; riesgo +0.84; expl3 -0.30 (n=105)
- 2. Deny knowing anything. Insist you never saw anything unusual — dignity -3, network +1; riesgo -0.84; expl3 +0.30 (n=597)

**Paso** `d00919181ae0` (844 veces): HR opens an investigation and confirms the relationship from other sources. The manager is asked to declare it, denies it, then traces the original report back to you. They start telling the team someone 'went behind their back'. The atmosphere turns suspicious.
- 1. If confronted, own it and explain you raised a conflict of interest and meant nothing personal by it — dignity +2, network -1; riesgo +0.48; expl3 -0.30 (n=435)
- 2. Stay anonymous and carry on as normal in the team — network -1, dignity -1; riesgo -0.48; expl3 +0.30 (n=7)

## Invited to shadow a senior planning meeting

Aparece 1814 veces (primer paso): L1 3%, L2 2%, L3 18%, L4 57%, L5 19%, L6 2%; meses 18–48 (mediana 29).

**Paso** `b1effdb77fbb` (1889 veces): As part of your development plan, the CTO invites you to shadow the quarterly executive strategy meeting. In the room you hear sensitive discussion about other departments, including possible restructuring and redundancies in a friend's team. The CTO makes clear it is strictly confidential. Afterwar
- 1. Keep it confidential. Tell them you cannot discuss anything from the meeting — dignity +2, network -2; riesgo -1.27; expl3 -0.13; → `1f8f614bb21c` (n=444)
- 2. Hint they have reason to pay attention, without specifics, and suggest they talk to their own manager — network +1, dignity -1; riesgo +1.27; expl3 +0.13; → `f819346123f7` (n=836)

**Paso** `f819346123f7` (773 veces): Your friend over-reads the hint, spreads anxiety through their team, and even starts looking for other jobs. The CTO hears that details of the meeting have leaked and starts tracing the source.
- 1. Go to the CTO, admit you shared no detail but may have hinted too strongly, and take responsibility — dignity +2, network -1; riesgo +0.91; expl3 -0.34 (n=618)
- 2. Deny passing anything on, and suggest their anxiety may have come from somewhere else — dignity -2, network -1; riesgo -0.91; expl3 +0.34 (n=35)

**Paso** `1f8f614bb21c` (766 veces): Your friend feels shut out: 'So you're at a level we don't get to now.' Three months later their team is restructured. They feel they could have prepared if they had known earlier, and the friendship cracks.
- 1. Explain that confidentiality is a professional duty. You care about them, but you still cannot share — dignity +2, network +1; riesgo -0.46; expl3 -0.11 (n=357)
- 2. Don't explain. Accept that work relationships sometimes need this distance — network -2; riesgo +0.46; expl3 +0.11 (n=10)

## Asking for remote work or a steadier role for family reasons

Aparece 1805 veces (primer paso): L1 2%, L2 3%, L3 18%, L4 56%, L5 20%, L6 2%; meses 18–48 (mediana 29).

**Paso** `ab9a3b9e678c` (1805 veces): Your family needs more of you. You are thinking of asking to work remotely or to move to a steadier, less intense role, but you worry it will look like a lack of ambition and hurt your promotion chances.
- 1. Be clear about the trade-off: make a formal request and commit to keeping your work up to standard — health +2, dignity +1, output -1; riesgo -0.32; expl3 -0.03 (n=205)
- 2. Make a vague request, because you want the easier setup but fear looking unambitious — dignity -1; riesgo +0.62; expl3 +0.08 (n=551)
- 3. Say nothing and keep grinding as you are — health -2, dignity -1; riesgo -0.30; expl3 -0.05 (n=467)

## Pushed to sign a settlement agreement on the spot

Aparece 1805 veces (primer paso): L1 2%, L2 2%, L3 18%, L4 55%, L5 21%, L6 2%; meses 18–48 (mediana 29).

**Paso** `c6a8b64ee0da` (1805 veces): HR puts a settlement agreement in front of you and wants it signed today. Sign it and you waive claims you might otherwise bring. They say: 'Just get it done — better for everyone.' It is not binding unless you have had time to read it and taken independent legal advice.
- 1. Ask for time, take independent legal advice, and only sign a settlement you agree with — dignity +2, wealth +1; riesgo -0.69; expl3 -0.07 (n=1146)
- 2. Sign the settlement today to get it over with, because you are tired of being chased — wealth -2, dignity -1; riesgo +0.16; expl3 +0.02 (n=31)
- 3. Lose your temper, tear up the paper and walk out — dignity +1, network -1; riesgo +0.54; expl3 +0.04 (n=51)

## A new manager is hired in, and you start again on trust

Aparece 1794 veces (primer paso): L1 8%, L2 10%, L3 34%, L4 36%, L5 12%, L6 1%; meses 12–48 (mediana 22).

**Paso** `e2d9e95cfaa3` (1794 veces): A new manager is hired in over your team, with a strong background and a style nothing like the last one. They do not know you yet. Some people are already sucking up to them; others are watching coldly. You start from nothing, and they will control your reviews and your prospects. What is your firs
- 1. Lead with the work: explain clearly what you are doing and ask what they expect, without grovelling or bristling — skill +1, output +1, network +1, dignity +1; riesgo -0.63; expl3 -0.15; → `bb0dd5f0ea00` (n=1152)
- 2. Rush to pick their side and lay the flattery on — dignity -1; riesgo +0.26; expl3 +0.00; → `08ef8a7b4de6` (n=37)
- 3. Watch them coldly, resist, and talk about how much better the last one was — network -1, output -1; riesgo +0.38; expl3 +0.14; → `7e8baea12fb0` (n=48)

**Paso** `bb0dd5f0ea00` (1654 veces): A clear update and solid delivery make a good first impression, and they start taking your views seriously. Then they ask for something the last manager never would. People mutter in private that it is change for change’s sake.
- 1. Judge the new request on its merits, deliver it well, and add something useful — skill +2, output +1, network +1, dignity +1; riesgo -0.34; expl3 -0.05 (n=1072)
- 2. Join the private muttering that the old way was better — network -1, dignity -1; riesgo +0.34; expl3 +0.05 (n=43)

**Paso** `7e8baea12fb0` (48 veces): You resist, and you keep talking about the last manager. The new one notices you are not cooperating and gives the important work to people who will go along with the changes. You have pushed yourself to the edge of the new team.
- 1. Drop the prejudice, adapt, and win trust back by delivering — skill +1, output +1, network +1, dignity +1, health -1; riesgo +0.40 (n=36)
- 2. Keep resisting and work against them — network -2, output -1; riesgo -0.40 (n=9)

**Paso** `08ef8a7b4de6` (35 veces): The heavy flattery gets a polite response, but they have already clocked it. What they care about is people who deliver. Colleagues find it embarrassing too. Grovelling has not got you a solid relationship or anyone’s respect.
- 1. Change tack: let your ability and delivery rebuild how they see you — skill +2, output +1, dignity +1, network +1; riesgo +0.05 (n=27)
- 2. Keep spending your energy on flattery — network -2, dignity -1, output -1; riesgo -0.05 (n=7)

## Should you put serious time into an emerging technology?

Aparece 1794 veces (primer paso): L1 3%, L2 3%, L3 18%, L4 57%, L5 18%, L6 2%; meses 18–48 (mediana 29).

**Paso** `55be54a078f2` (1794 veces): An emerging technology is gathering pace in the industry and looks likely to become mainstream. Learning it properly would take a fair amount of your own time, and it will not help the work on your desk in the short run. Do you learn it, or leave it?
- 1. Treat it as an investment: make a plan, learn it properly, and look for chances to practise — skill +2, dignity +1, health -1; riesgo -0.62; expl3 -0.05 (n=1076)
- 2. Skip it as too much hassle and tell yourself you'll pick it up if you ever need it — skill -1; riesgo +0.32; expl3 +0.03 (n=63)
- 3. Bookmark tutorials and sign up for a course so you look like you're learning, but never do the work — sin cambios; riesgo +0.30; expl3 +0.02 (n=62)

## The company asks for a 'voluntary' pay cut to get through a hard patch

Aparece 1787 veces (primer paso): L1 3%, L2 2%, L3 18%, L4 57%, L5 19%, L6 2%; meses 18–48 (mediana 29).

**Paso** `989090f05b39` (1787 veces): Leadership asks staff to agree a temporary pay cut to see the company through. Nothing changes unless you agree in writing. They also hint that those who step up first will be remembered. You do not want to look disloyal, and you do not want to give up pay with no prospect of getting it back.
- 1. Offer to share some of the load if you get a written agreement and a clear route back — dignity +1, wealth -1; riesgo -0.83; expl3 -0.14 (n=522)
- 2. Be first to volunteer a steep cut, no questions asked, to look loyal — network +1, wealth -2; riesgo +0.46; expl3 -0.03 (n=648)
- 3. Refuse publicly and have a go at leadership — dignity +1, network -2; riesgo +0.37; expl3 +0.16 (n=34)

## School run clashing with overtime

Aparece 1778 veces (primer paso): L1 3%, L2 2%, L3 19%, L4 56%, L5 18%, L6 2%; meses 18–48 (mediana 29).

**Paso** `f4e37dc9c0e9` (1778 veces): Your child has just started school. Pick-ups and being there for your child both take time, and this project is busy. At this company, staying late has become the norm, and family time and work are clashing.
- 1. Share the load at home, agree some flexibility with the team, and make a formal flexible-working request for the school run — health +1, network +1, output -1; riesgo -0.32; expl3 -0.12 (n=430)
- 2. Throw yourself into the project and put family time on hold — output +1, dignity -1, health -1; riesgo -0.39; expl3 -0.06 (n=723)
- 3. Try to do everything perfectly at home and at work, and run yourself into the ground — health -2; riesgo +0.70; expl3 +0.19 (n=28)

## Load-test results clash with what product expected

Aparece 1764 veces (primer paso): L1 5%, L2 12%, L3 33%, L4 38%, L5 10%, L6 1%; meses 12–48 (mediana 22).

**Paso** `9a769ee2a9cf` (1764 veces): The load test you ran shows the system can only take 60% of the expected QPS. The product owner insists the last demo was fine, so your method must be wrong. The go-live deadline does not move.
- 1. Invite product to review the scripts and scenarios with you — skill +2, network +1, dignity +1; riesgo -0.52; expl3 -0.18; → `84192d5a7b02` (n=1146)
- 2. Stand by the numbers and ask to cut scope or slip the date — dignity +2, output -1, network -1; riesgo -0.67; expl3 -0.05; → `8c81681b83e4` (n=46)
- 3. Tweak the test parameters until they 'pass', as product asked — output +1, dignity -2; riesgo +1.19; expl3 +0.23; → `6377deb5cab5` (n=43)

**Paso** `84192d5a7b02` (1613 veces): You find the demo used an ideal path with an extremely high cache-hit rate.
- 1. Retest and issue a realistic capacity report — skill +2, output +1, network +1; riesgo -0.56; expl3 -0.05 (n=1074)
- 2. Compromise: ship, but with rate limits — skill +1, dignity +1, output +1; riesgo +0.56; expl3 +0.05 (n=35)

**Paso** `8c81681b83e4` (48 veces): Your manager supports a one-week slip. The client is mildly unhappy.
- 1. Work late and optimise to 80% of target capacity — output +2, health -2, skill +1; riesgo -0.64; expl3 -0.19 (n=34)
- 2. Keep the delay — dignity +1, network +1, output -1; riesgo +0.64; expl3 +0.19 (n=11)

**Paso** `6377deb5cab5` (30 veces): On launch day the system wobbles at peak. The client complains.
- 1. After the incident, admit you were pressured into fudging the load test — dignity +1, network -1; riesgo -0.33; expl3 -0.23 (n=6)
- 2. Call it unexpected traffic — dignity -1; riesgo +0.33; expl3 +0.23 (n=18)

## You survive a round of cuts and inherit the work

Aparece 1763 veces (primer paso): L1 5%, L2 10%, L3 32%, L4 38%, L5 14%, L6 1%; meses 12–48 (mediana 23).

**Paso** `80d596434dd5` (1763 veces): You survive a round of redundancies. Several colleagues are gone, and your manager asks you to cover the urgent part of their work for a short while and to come back with what should wait. Your pay has not changed. Until that conversation happens, you are carrying more. How do you handle it?
- 1. Prioritise the new work, discuss resources and limits with your manager, and push for support or something in return — skill +1, dignity +1, network +1, output +1; riesgo -0.49; expl3 -0.13; → `9c3a2272f29c` (n=1167)
- 2. Take the lot in silence and carry it at any cost — output +1, health -2, dignity -1; riesgo +0.04; expl3 +0.10; → `0085f55f8dd0` (n=33)
- 3. Push back by coasting: the more that arrives, the more you half-do it — output -1, dignity -1; riesgo +0.45; expl3 +0.04; → `d6bc318b4981` (n=39)

**Paso** `9c3a2272f29c` (1628 veces): You go through the extra work with your manager: what you can carry, what needs more people or time, and why covering at this level should come with something in return. They like how organised you are and that you have taken it on, give you some support, and note your contribution. Covering becomes
- 1. Cover the critical work well, and turn “stepping up” into a case for promotion and a rise — skill +2, output +2, network +1, dignity +1, health -1; riesgo -0.37; expl3 -0.11 (n=1094)
- 2. Ease off after the conversation, and do not deliver what you promised — output -1, dignity -1; riesgo +0.37; expl3 +0.11 (n=32)

**Paso** `0085f55f8dd0` (37 veces): You take the lot without a word and keep going like that for months. Your body starts to complain. Your manager assumes you are fine, offers no extra help or anything in return, and treats this as the new normal. Carrying it all is wearing down your health and your position to negotiate.
- 1. Stop in time, and negotiate a sustainable workload and a fair return — dignity +1, network +1, health +1; riesgo -0.03 (n=22)
- 2. Keep carrying until your health goes — health -2, output -1; riesgo +0.03 (n=7)

**Paso** `d6bc318b4981` (31 veces): You coast in protest at the overload, and the more that piles up, the more you half-do it. During a short-staffed, critical stretch you drop something. You survived the cuts, but because of how you have just performed, you are now a likely name for the next round.
- 1. Get your head straight, focus on the critical work, and steady your position — output +1, skill +1, dignity +1, health -1; riesgo -1.28; expl3 -0.16 (n=21)
- 2. Keep coasting — output -2, dignity -2; riesgo +1.28; expl3 +0.16 (n=7)

## Mentoring an intern as a first taste of management

Aparece 1760 veces (primer paso): L1 2%, L2 2%, L3 18%, L4 57%, L5 19%, L6 2%; meses 18–48 (mediana 29).

**Paso** `ac3127970b24` (1760 veces): Your manager asks you to mentor a new intern. It will split your attention between teaching, checking in and covering for them, but it is also your first chance to try managing someone. How do you handle it?
- 1. Mentor them properly: plan, give feedback, and treat it as practice for leading people — skill +1, network +1, dignity +1; riesgo -0.58; expl3 -0.03 (n=1023)
- 2. Treat it as a distraction from your own work, phone it in and leave them to it — network -1, dignity -1; riesgo +0.36; expl3 +0.09 (n=33)
- 3. Use them as free labour: odd jobs only, no real teaching — network -1, dignity -1; riesgo +0.22; expl3 -0.06 (n=138)

## A security hole that would be expensive to fix

Aparece 1759 veces (primer paso): L1 6%, L2 10%, L3 34%, L4 38%, L5 12%, L6 1%; meses 12–48 (mediana 22).

**Paso** `73fd0f35b02d` (1759 veces): In a routine review you find a potential security hole: under certain conditions, an attacker could reach another user's data. Fixing it means rebuilding the core authorisation module. That touches much of the system, needs a long round of testing, and will probably delay a release that is about to 
- 1. Block the release until the hole is fully fixed and has passed a security audit — skill +2, dignity +2, output -2, network -1; riesgo -0.97; expl3 -0.18; → `806a7a11d21f` (n=959)
- 2. Accept a later fix, but put temporary mitigations and monitoring in first — output +1, skill +1; riesgo +0.97; expl3 +0.18; → `baa67f453b26` (n=280)

**Paso** `806a7a11d21f` (1361 veces): The release slips two weeks. Sales complain about lost deals. At the exec meeting the CEO asks whether a medium-severity issue is worth several million pounds of revenue. The CISO backs you in the meeting, then tells you privately that they held the line this time but want a more balanced answer fro
- 1. Start a shift-left process, so similar issues are found much earlier — skill +2, network +1, output -1; riesgo -0.67; expl3 -0.09 (n=883)
- 2. Soften your stance, and promise to be more 'pragmatic' in balancing security against the business — network +1, dignity -1; riesgo +0.67; expl3 +0.09 (n=48)

**Paso** `baa67f453b26` (346 veces): The release ships on time, and the temporary mitigations hold. Two weeks later monitoring shows access patterns that look like an attack, and the hole may already be in criminal hands. Security responds and confirms that a small amount of customer data was accessed improperly.
- 1. Open a full incident response: notify every affected customer and report it to the regulator — dignity +2, output -2, network +1; riesgo -0.62; expl3 -0.21 (n=86)
- 2. Scope the real impact, and recommend notifying only customers you can confirm were affected — output +1, network -1; riesgo +0.62; expl3 +0.21 (n=176)

## Communicating a breaking change on a public API

Aparece 1753 veces (primer paso): L1 6%, L2 10%, L3 31%, L4 39%, L5 12%, L6 1%; meses 12–48 (mediana 23).

**Paso** `0d41ef234c09` (1753 veces): Your v3 API drops two v2 fields, which is a breaking change. Of the three downstream teams, one has refused to upgrade for a long time. The contract SLA requires 90 days' notice.
- 1. Follow the 90-day process and publish a deprecation notice — dignity +2, skill +1, network +1, output -1; riesgo -0.68; expl3 -0.16; → `b17ec9623cc5` (n=756)
- 2. Privately agree a longer compatibility layer with the reluctant team — network +2, skill +1; riesgo +0.47; expl3 -0.08; → `596b77b5116b` (n=410)
- 3. Switch v2 off and force them to upgrade — output +1, network -3, dignity -1; riesgo +0.21; expl3 +0.24; → `b863327870ac` (n=41)

**Paso** `b17ec9623cc5` (1106 veces): The reluctant team still stalls, then asks you for more time two weeks before the deadline.
- 1. Hold the deadline but offer a migration script and support — skill +2, dignity +1, network +1; riesgo -0.55; expl3 -0.08 (n=707)
- 2. Slip another 30 days — network +1, dignity -1; riesgo +0.55; expl3 +0.08 (n=31)

**Paso** `596b77b5116b` (564 veces): The compatibility layer raises your maintenance cost, and your module's bug rate climbs.
- 1. Put a sunset date for the compatibility layer into the OKRs — skill +1, output +1; riesgo -1.05; expl3 -0.05 (n=379)
- 2. Maintain it indefinitely — health -1, output -1; riesgo +1.05; expl3 +0.05 (n=23)

**Paso** `b863327870ac` (29 veces): Their production system starts throwing errors, and the client complains to your manager.
- 1. Restore v2 in a hurry and review how you communicated — skill +1, dignity +1, network -1; riesgo -0.19; expl3 -0.11 (n=11)
- 2. Insist they brought it on themselves — network -3, dignity -2; riesgo +0.19; expl3 +0.11 (n=18)

## The new manager quietly moves you out of the inner circle

Aparece 1752 veces (primer paso): L1 2%, L2 1%, L3 19%, L4 55%, L5 20%, L6 2%; meses 18–48 (mediana 29).

**Paso** `f4b3d2e1b543` (1752 veces): You notice you have been quietly dropped from the core decision-making channel. A few important meetings no longer include you. Nobody has said it out loud.
- 1. Ask your manager where you stand and what is expected of you — network +1, dignity +1; riesgo -0.48; expl3 -0.08 (n=166)
- 2. Make your work so solid they cannot ignore you — skill +1, output +1, health -1; riesgo -0.47; expl3 -0.07 (n=947)
- 3. Nurse the grievance, quietly check out and complain in private — dignity -1, output -1; riesgo +0.94; expl3 +0.15 (n=36)

## A database migration window clashes with peak trading

Aparece 1740 veces (primer paso): L1 7%, L2 11%, L3 33%, L4 36%, L5 12%, L6 1%; meses 12–48 (mediana 22).

**Paso** `b8bb70d839d4` (1740 veces): You are leading the membership database migration from MySQL 5.7 to 8.0, scheduled for Sunday 02:00–06:00. On Friday, product announces that a peak trading period has been brought forward to Monday midnight. Chris, the DBA, says: 'The rollback script is not fully tested. Going ahead is a big risk.'
- 1. Ask to delay the migration and protect peak trading first — dignity +1, output -1, network +1; riesgo -0.81; expl3 -0.20; → `2a4b6d5ebdb1` (n=215)
- 2. Cut testing short and go ahead as planned — output +2, health -2, skill +1; riesgo +0.72; expl3 +0.29; → `7fc9c29f1065` (n=40)
- 3. Propose dual-write with a two-week canary cutover — skill +2, network +1; riesgo +0.10; expl3 -0.10; → `cc05a015912b` (n=964)

**Paso** `cc05a015912b` (1208 veces): Dual-write means building a sync-and-check tool this week, which pushes out a request from the rewards centre.
- 1. Take it on and ask your manager to drop the other work — skill +2, network +2, output +1, health -1; riesgo -0.14; expl3 -0.02 (n=804)
- 2. Refuse to build the tool, and force a straight choice between delaying and rushing — dignity -1, skill -1; riesgo +0.14; expl3 +0.02; → `2a4b6d5ebdb1` (n=121)

**Paso** `2a4b6d5ebdb1` (551 veces): Product accepts the delay. Architecture reminds you that 5.7 support ends at the end of the month.
- 1. Commit to a fixed 72-hour migration plan straight after peak trading — skill +1, output +1, dignity +1; riesgo -0.56; expl3 -0.32 (n=309)
- 2. Cite safety and push it back another month — network -1, output -1; riesgo +0.56; expl3 +0.32 (n=17)

**Paso** `7fc9c29f1065` (33 veces): At 03:40 on Sunday, replica lag spikes after cutover. Twenty hours remain before peak trading.
- 1. Roll back immediately, following the playbook — skill +1, dignity +1, output -1; riesgo -0.56; expl3 -0.28 (n=14)
- 2. Stay up all night fixing it, without rolling back — health -3, output +2; riesgo +0.56; expl3 +0.28 (n=15)

## Your company is acquired and the culture flips

Aparece 1734 veces (primer paso): L1 6%, L2 10%, L3 33%, L4 39%, L5 12%, L6 1%; meses 12–48 (mediana 22).

**Paso** `8640a52844d2` (1734 veces): A larger company buys yours, and reporting lines, processes and culture all have to fall in line with theirs. Everything you knew is changing. Some people are already leaving, and others are watching anxiously. The new owner’s rules and pace still feel foreign. With this much changing, where do you 
- 1. Learn how the new organisation works and where the openings are, adapt, and find where you still add value — skill +1, network +1, dignity +1, output +1; riesgo -0.36; expl3 -0.16; → `857dc2b16712` (n=810)
- 2. Cling to the old culture, resist the new rules, and keep saying how much better it used to be — network -1, output -1; riesgo +0.44; expl3 +0.28; → `4437b842d1d8` (n=52)
- 3. Play the chaos, commit to nobody, and wait to see who wins — network -1; riesgo -0.08; expl3 -0.12; → `3b2d6186a1e4` (n=353)

**Paso** `857dc2b16712` (1268 veces): You learn the new rules, find the people who matter on the buyer’s side, and come across as open and capable, so they mark you down as someone they can rely on during the integration. They offer you a piece of cross-team work, which means acting as a bridge between two cultures. That is not easy.
- 1. Take the bridging role, get both sides working together, and build credibility with both companies — skill +2, network +2, output +1, health -1; riesgo -0.16; expl3 -0.05 (n=761)
- 2. Duck the responsibility and push the cross-team work onto someone else — network -1, dignity -1, output -1; riesgo +0.16; expl3 +0.05 (n=26)

**Paso** `3b2d6186a1e4` (356 veces): You wait and commit to nobody. Once the integration settles you have neither joined the new organisation nor stayed with the old camp, and neither side counts you as one of theirs.
- 1. Pick a direction, join the new organisation properly, and rebuild the trust you let slide — skill +1, network +1, dignity +1, output +1; riesgo -0.65; expl3 -0.08 (n=314)
- 2. Keep sitting on the fence and coasting — network -2, dignity -1; riesgo +0.65; expl3 +0.08 (n=15)

**Paso** `4437b842d1d8` (47 veces): You cling to the old culture and keep resisting. The new leadership sees you as hard to integrate and unwilling to change. You miss out on what the deal could have offered and become a candidate for the next round of cuts.
- 1. Face facts, let go of the old ways, and get behind the new organisation — skill +1, network +1, dignity +1, health -1; riesgo -0.26; expl3 -0.15 (n=30)
- 2. Keep looking backwards and resisting to the end — network -2, output -1; riesgo +0.26; expl3 +0.15 (n=15)

## Abnormal health-check results: push through or see a doctor

Aparece 1732 veces (primer paso): L1 6%, L2 9%, L3 33%, L4 40%, L5 11%, L6 1%; meses 12–48 (mediana 22).

**Paso** `57bc60dd65d8` (1732 veces): The company health-check results are in, and several of yours are flagged: abnormal liver function, a thyroid nodule recommended for further biopsy, and an ECG noting occasional extra beats. The doctor has written, 'See a specialist promptly; avoid late nights and high stress.' These two weeks are t
- 1. Take leave now for specialist tests and hand over your work cleanly — health +2, output -1, network +1; riesgo -0.85; expl3 -0.34; → `033caaadb176` (n=1115)
- 2. Push through this delivery and book the follow-up for the end of the month — output +1, health -2; riesgo +0.23; expl3 -0.04; → `c733fe736423` (n=46)
- 3. Decide health checks always scare people, and ignore it — health -2; riesgo +0.61; expl3 +0.38; → `50d9bc1b5a7b` (n=47)

**Paso** `033caaadb176` (1588 veces): You tell your manager about the results. There is no fuss, and Priya covers for you. Follow-up tests show the nodule is benign and the extra beats are linked to late nights and caffeine. The doctor gives you a plan and stresses sleep. You are relieved, and you also take it as your body's first warni
- 1. Reset how you work: fixed hours, with the high-intensity work spread out — health +2, skill +1; riesgo -0.77; expl3 -0.15 (n=1052)
- 2. Nothing serious showed up, so you fall back into late-night sprints — output +1, health -2; riesgo +0.77; expl3 +0.15 (n=40)

**Paso** `50d9bc1b5a7b` (43 veces): You shove the report in a drawer and keep working long weeks. Three months later, late at night on overtime, you get a violent bout of palpitations and tingling hands. A colleague takes you to A&E. The doctor is blunt: 'Keep this up and next time it will not be a warning.' Lying on the trolley, you 
- 1. Take the scare seriously: stop work for a full course of treatment and rest — health +2, wealth -1, output -2; riesgo -0.41; expl3 -0.18 (n=20)
- 2. Once discharged, decide you are fine and dive into the next high-pressure programme — health -3; riesgo +0.41; expl3 +0.18 (n=16)

**Paso** `c733fe736423` (39 veces): You deliver on time and the quarter looks excellent. At the end-of-month follow-up, the biopsy is another two weeks' wait. Meanwhile you get palpitations and fatigue, and your family starts pushing you to take it seriously. You can put it off again or stop the damage now.
- 1. Get treatment now, and tell the team you need some time to adjust — health +2, dignity +1, output -1; riesgo -0.88; expl3 -0.09 (n=12)
- 2. Keep putting off the follow-up as one project follows another — output +1, health -2; riesgo +0.88; expl3 +0.09 (n=20)

## Your annual bonus falls short, and you go to your manager

Aparece 1724 veces (primer paso): L1 5%, L2 11%, L3 31%, L4 40%, L5 11%, L6 1%; meses 12–48 (mediana 22).

**Paso** `933432539f49` (1724 veces): Your annual bonus comes in well below what you expected, after a year of graft and a rating that should have meant more. You are hurt and you have questions. Storm in, or get the facts first?
- 1. Check your rating, the bonus rules and last year’s figures, then book a conversation about how it was calculated — skill +1, dignity +1, health +1; riesgo -0.56; expl3 -0.14; → `ec527ccbc4a8` (n=1121)
- 2. Storm into the office and demand to know why it is so low — network -1, dignity -1; riesgo -0.18; expl3 +0.02; → `f83bdf70ef64` (n=43)
- 3. Say nothing to their face, and snipe about the company in the team channel — network -2, dignity -1; riesgo +0.74; expl3 +0.11; → `e265df4c26ea` (n=26)

**Paso** `ec527ccbc4a8` (1614 veces): You get the rules straight, then talk it through calmly. Your manager explains this year’s calculation, and along the way you find a place where your contribution really was undervalued. The conversation stays civil. What matters now is what you ask for next.
- 1. Show with facts what was undervalued, and push for a correction or a catch-up in next year’s rating or pay review — wealth +1, skill +1, network +1, dignity +1; riesgo -0.16; expl3 -0.04 (n=1014)
- 2. Hear the explanation, feel too awkward to push, and let it go — dignity -1; riesgo +0.16; expl3 +0.04 (n=82)

**Paso** `f83bdf70ef64` (40 veces): You go in hot. Your manager is left looking small, and the conversation turns into a clash of tempers. Even if you have a point, your manner puts them on the defensive about their authority, and they stop trying to help. Now the argument is about your temper.
- 1. Realise your manner was wrong, cool things down, and bring the conversation back to the facts — dignity +1, network +1; riesgo -0.09 (n=32)
- 2. Get more heated, until neither of you will budge — network -2, dignity -1; riesgo +0.09 (n=7)

**Paso** `e265df4c26ea` (25 veces): You skip the conversation and snipe in the channel. It reaches your manager quickly. You get no bonus correction, and you pick up a reputation for complaining behind people’s backs. A pay question that could have been sorted out has become a problem about you.
- 1. Limit the damage: take the posts down, apologise, and raise it through the proper channel — dignity +1, network +1; riesgo -1.59 (n=13)
- 2. Keep complaining in public and make it bigger — network -2, dignity -2; riesgo +1.59 (n=7)

## Admitting you are not coping, and asking for help

Aparece 1722 veces (primer paso): L1 5%, L2 11%, L3 36%, L4 36%, L5 11%, L6 1%; meses 12–48 (mediana 21).

**Paso** `3a8aea444ceb` (1722 veces): After three months of a high-pressure project you are not sleeping, you cannot concentrate, and your temper is going. Last week you lost it with a colleague in the morning meeting over a design disagreement, and you have been kicking yourself since. The Employee Assistance Programme counsellor sugge
- 1. Follow the sick-leave procedure, and privately agree the support and return-to-work plan you need — health +2, wealth -1; riesgo -0.67; expl3 -0.28; → `9dda33820227` (n=1136)
- 2. Grit it out, try exercise and meditation, and deal with it after the project — health -2, output +1; riesgo +0.67; expl3 +0.28; → `f874c81e497c` (n=67)

**Paso** `9dda33820227` (1609 veces): When you come back, colleagues have covered your work and the plan has been moved around your absence. Meanwhile, someone who gritted it out to the end was admitted to hospital with acute anxiety. You can talk about what happened, or keep the details private.
- 1. If you want to, talk about the leave, and suggest the team builds a workload and support check into how it works — network +2, dignity +2; riesgo -0.18; expl3 -0.01 (n=1035)
- 2. Keep it quiet, and prove yourself again through delivery — output +2, network -1; riesgo +0.18; expl3 +0.01 (n=70)

**Paso** `f874c81e497c` (52 veces): The project goes live. After the drinks, your body gives a louder warning: a tight chest, palpitations and a trip to A&E. The doctor says it is a physical reaction to long-running anxiety and that you need to stop. Your manager visits with news: the company wants to make you Tech Lead, if you can sh
- 1. Be honest about your health, ask to delay the promotion, and request a move onto a steadier product — health +2, dignity +2, wealth -1, network +1; riesgo +0.62; expl3 -0.41 (n=19)
- 2. Promise to get back on form, take the promotion, and keep the counselling from the team — wealth +2, network +1, health -2; riesgo -0.62; expl3 +0.41 (n=30)

## You bring an outside offer back to negotiate pay

Aparece 1715 veces (primer paso): L1 6%, L2 10%, L3 33%, L4 38%, L5 12%, L6 1%; meses 12–48 (mediana 23).

**Paso** `85daedc9b56c` (1715 veces): You have a real offer from another company, paying more. You are not set on leaving, and would prefer to use it as leverage for the rise you think you are owed here. Bringing an offer into a pay conversation can help or hurt you, depending on how you use it.
- 1. Be straight: you want to stay, here is what the market pays, and would they review your pay — skill +1, dignity +1, network +1; riesgo -0.93; expl3 -0.26; → `07f7c3477a61` (n=1082)
- 2. Use the offer as an ultimatum: “Match this number or I go today” — network -1, dignity -1; riesgo +0.66; expl3 +0.06; → `78d7cfb4cd70` (n=41)
- 3. Inflate the offer and quote your manager a much higher number — dignity -2; riesgo +0.27; expl3 +0.20; → `6675f6eb93a2` (n=38)

**Paso** `07f7c3477a61` (1594 veces): You say you want to stay and set out what the market pays. Your manager does not hear it as a threat, takes a proper look, and is willing to fight for a rise, though the process will take some time. You are working on it together.
- 1. Give them time, be clear about wanting to stay and about your ask, and aim for a deal that suits both sides — wealth +1, skill +1, network +1, dignity +1; riesgo -0.41; expl3 -0.06 (n=1003)
- 2. Lose patience halfway and switch to a threat — network -1, dignity -1; riesgo +0.41; expl3 +0.06 (n=51)

**Paso** `78d7cfb4cd70` (35 veces): You issue an ultimatum, and your manager is backed into a corner. Even if they give in on the spot to keep you, they now see you as someone who negotiates by threat and has one foot out of the door. From now on you get less trust and fewer chances. You might win a number and lose a relationship.
- 1. Soften, and steer the conversation back to a negotiation about what you are worth — dignity +1, network +1; riesgo -1.77 (n=31)
- 2. Hold firm, and force them to name a number — wealth +1, network -2; riesgo +1.77 (n=3)

**Paso** `6675f6eb93a2` (33 veces): The offer is real, but the number you quoted is not. If they get suspicious, one question, “Can I see the details?”, ends it. If the inflated number is exposed, you miss the rise and people start to doubt your basic honesty, which is far worse than leaving your pay where it is.
- 1. Drop the lie in time, and make your case on what you have delivered and real market rates — dignity +1, skill +1; riesgo +0.14 (n=23)
- 2. Keep the story going and try to make the lie hold — dignity -2, network -2; riesgo -0.14 (n=8)

## A colleague accidentally posts internal architecture online

Aparece 1714 veces (primer paso): L1 5%, L2 10%, L3 34%, L4 39%, L5 11%, L6 1%; meses 12–48 (mediana 22).

**Paso** `a7aefe689dfe` (1714 veces): Browsing GitHub, you find that a colleague has posted an architecture diagram of an internal system in a public technical thread. Names have been removed, but anyone who knows the company would recognise it. It is clearly an accident: they were in a hurry to get help with a hard problem. Report it, 
- 1. Help them take the post down, then report the accidental disclosure to security and say it was a mistake — dignity +1, network -2, skill +1; riesgo -0.65; expl3 +0.03; → `278bead05620` (n=53)
- 2. Message them privately to take it down now, on the understanding that it goes no further — network +2, dignity +1, skill +1; riesgo +0.65; expl3 -0.03; → `f0e348bd43db` (n=1163)

**Paso** `f0e348bd43db` (1601 veces): They are grateful, take the post down, and become more careful about information security. Three months later someone else makes a worse mistake of the same kind: a log snippet containing sensitive customer data, picked up by an external crawler. Security's investigation finds that you knew about th
- 1. Admit you handled it badly, accept the company's sanction, and propose a 'good-faith warning' route for first minor incidents — dignity +1, network +1; riesgo -0.60; expl3 -0.22 (n=1072)
- 2. Argue that the two incidents differed in severity, and that your call was reasonable in context — network -3, dignity -2; riesgo +0.60; expl3 +0.22 (n=53)

**Paso** `278bead05620` (65 veces): Security investigates and judges the leak containable. Your colleague is hurt to find out you reported it, and tells the people they are close to that you shopped them. Helping them take the post down and then reporting the accident was the normal security step.
- 1. Explain to the team how the report worked, and that security rules are not optional — dignity +2, network -1, skill +1; riesgo -0.41; expl3 -0.08 (n=36)
- 2. Say nothing, and trust that time will show you made the right call — network -2; riesgo +0.41; expl3 +0.08 (n=16)

## A toxic team culture: stay or leave?

Aparece 1394 veces (primer paso): L1 3%, L2 2%, L3 21%, L4 53%, L5 18%, L6 2%; meses 18–48 (mediana 29).

**Paso** `2eacb385fd54` (1394 veces): A newly hired VP is pushing an aggressive 'high-performance' culture: public humiliation for anyone who misses their numbers, briefings that reward stitching colleagues up, and a quiet rank-and-yank. The mood in engineering sours fast, and several people are showing signs of depression. One colleagu
- 1. Join a few senior colleagues in a named letter to HR and the CEO about the culture — dignity +2, network +1, wealth -1; riesgo +0.48; expl3 -0.17; → `845e73bb76dc` (n=453)
- 2. Keep your head down, and quietly help people who are being hurt to transfer internally — network +2, dignity -1; riesgo -0.48; expl3 +0.17; → `817595b70dcd` (n=490)

**Paso** `845e73bb76dc` (742 veces): The VP hears about the letter. In an all-hands they say, without naming names, that anyone who cannot handle tough competition is free to leave. HR then sits you down. The CEO hired this VP personally, the company is fully behind the change, and are you willing to 'get with the programme'?
- 1. Stand your ground, and ask HR to open a formal investigation into the culture — dignity +3, network -2; riesgo -0.59; → `e7f2a966b4c7` (n=9)
- 2. Go along with a transfer for now, and start looking for jobs elsewhere — network -1, dignity -1; riesgo +0.59 (n=407)

**Paso** `817595b70dcd` (542 veces): You get two colleagues into healthier teams. The VP sees your 'little group' as a clique. In a one-to-one, they say they have heard you are helping people leave the team. If that is your attitude, you might as well join the department you have been sending people to, and free up the headcount for pe
- 1. Take the 'suggestion' and transfer to the team you had already been helping people into — network +1, skill -1, dignity -1; riesgo -0.75; expl3 +0.23 (n=424)
- 2. Refuse to be pushed into a transfer, and say you acted out of duty to your colleagues — dignity +2, network -1; riesgo +0.75; expl3 -0.23; → `df3a5694d7b3` (n=24)

**Paso** `e7f2a966b4c7` (140 veces): A formal investigation gets going, slowly. Meanwhile the VP pushes the policy harder. Two more people leave, including someone you had been developing for two years. Three months later the finding is that the VP's management style has 'room to improve' but did not breach policy. The VP is told to wa
- 1. Accept the finding, and say openly that you will keep watching whether the culture improves — dignity +2, network +1;  (n=1)
- 2. Lose faith in the investigation and resign — dignity +1, network +2, wealth -1; riesgo +0.00 (n=1)

**Paso** `df3a5694d7b3` (95 veces): The VP is furious. They start targeting you in public, handing you work that cannot be done, and hinting that failure will prove you are not up to your current grade. Other people start keeping their distance, worried about being associated with you.
- 1. Gather evidence and formally raise workplace bullying with the CEO and through a board channel — dignity +3, wealth -2; riesgo +0.17 (n=10)
- 2. Faced with impossible work, ask for a lower grade or a transfer, and leave with some dignity intact — dignity -1, network -1; riesgo -0.17 (n=5)

## The pay-review pot is tight and you are competing for a rise

Aparece 1341 veces (primer paso): L1 3%, L2 2%, L3 22%, L4 54%, L5 17%, L6 1%; meses 18–48 (mediana 27).

**Paso** `4c86f5e3ca5c` (1341 veces): This year’s pay-review pot is small, and too many good people are chasing it. In practice, you and a few equally strong colleagues are competing for the same rise. Your manager’s budget only stretches so far: what one person gets, another does not. If you want that rise, how do you play it?
- 1. Compete openly on results you can point to and a clear case for your value — skill +1, output +1, dignity +1, network +1; riesgo -0.81; expl3 -0.15; → `217298e3c07d` (n=816)
- 2. Quietly talk a rival down to your manager, so you look better by comparison — network -1, dignity -1; riesgo +0.64; expl3 -0.02; → `c42d909511ad` (n=26)
- 3. Work on your manager personally: a gift, a dinner, a private appeal — wealth -1, dignity -1; riesgo +0.18; expl3 +0.17; → `7352a0e1aef9` (n=41)

**Paso** `217298e3c07d` (1235 veces): You make your case with a solid summary of what you have delivered and a plan for what you will contribute next. Your manager accepts that you are capable, but says the others are strong too and there is a balance to strike. Then you hear a rival has been talking you down behind your back.
- 1. Do not hit back: keep letting your results speak, and set the record straight if needed without attacking them — skill +1, dignity +2, network +1, wealth +1; riesgo -0.65; expl3 -0.11 (n=759)
- 2. Get angry, and start talking them down in return — network -2, dignity -1; riesgo +0.65; expl3 +0.11 (n=28)

**Paso** `7352a0e1aef9` (39 veces): You try a gift and a dinner. Your manager either will not take it, or takes it and still has to justify the pay review to the team on results. You spend money, lower yourself, may still miss out on the rise, and look as if you did not trust your work to speak for itself.
- 1. Go back to doing it properly, and put your energy into results everyone will accept — skill +1, output +1, dignity +1; riesgo -0.37 (n=31)
- 2. Double down on winning your manager over personally — wealth -1, dignity -1; riesgo +0.37 (n=8)

**Paso** `c42d909511ad` (15 veces): You quietly make trouble for a rival. That kind of talk tends to travel. Managers dread someone who starts feuds and stabs colleagues in the back, and however capable that person is, they are hard to promote. You have staked your reputation as well as the rise.
- 1. Pull back before it goes further, stop the smearing, and compete on ability — skill +1, dignity +1; riesgo -0.18 (n=11)
- 2. Keep working against them behind their back — network -2, dignity -2; riesgo +0.18 (n=2)

## Training a model on customer conversations: where is the line?

Aparece 1303 veces (primer paso): L1 3%, L2 2%, L3 21%, L4 55%, L5 17%, L6 2%; meses 18–48 (mediana 28).

**Paso** `30b909c271df` (1303 veces): Product wants a 'smarter support' project: train a large model on old customer-service transcripts. It is technically feasible and could cut human support costs by about 30%. You find that the current privacy notice does not describe this use. Legal says you can sail close to the wind: ship first an
- 1. Pause all use of the transcripts until the privacy lead has assessed whether it is allowed, and ship only if so — skill +1, output -2, dignity +2; riesgo -0.56; expl3 -0.13; → `0f975ddc5526` (n=266)
- 2. Train an MVP on public datasets, and run the compliance work in parallel — skill +2, output +1; riesgo +0.56; expl3 +0.13; → `bc4993d1e2d6` (n=615)

**Paso** `bc4993d1e2d6` (820 veces): The MVP is only middling, but Product uses its numbers to argue for wider use of customer data. Then a user asks on social media how an AI seemed to know about their conversation, and a small PR row breaks out. Comms piles in and wants engineering to prove there was no misuse.
- 1. Pull together the technical records, show the training data was kept separate from the MVP, and recommend starting full compliance now — skill +1, dignity +1, output -1; riesgo -0.77; expl3 -0.20 (n=197)
- 2. Back the comms line, lean on the word 'anonymised', and play the risk down — network +1, dignity -2; riesgo +0.77; expl3 +0.20 (n=384)

**Paso** `0f975ddc5526` (432 veces): Holding the line delays the project by two months. Once live, it works well, but a competitor shipped something similar three months earlier and took the market. At the quarterly review the CEO says compliance matters but cannot be an excuse for falling behind, and there has to be a balance. Afterwa
- 1. Propose an 'agile compliance' process so the review is quicker next time — skill +2, network +1, output -1; riesgo +0.23; expl3 -0.05 (n=236)
- 2. Share the case within engineering, and push 'compliance first' harder as an engineering value — dignity +2, network -1; riesgo -0.23; expl3 +0.05 (n=21)

## A promotion without a pay rise

Aparece 1267 veces (primer paso): L1 3%, L2 3%, L3 21%, L4 55%, L5 17%, L6 1%; meses 18–48 (mediana 28).

**Paso** `81b3c6784393` (1267 veces): Your manager wants to talk about a 'promotion': a bigger title and a heavier workload, with the pay 'held for now — we'll look at it next year'. It is a better title with no rise: more prestige, more work, same money. The question is whether you take it, and on what terms.
- 1. Weigh what the title is actually worth, and whether it paves the way for a rise, before you negotiate — skill +1, dignity +1, output +1; riesgo -0.36; expl3 -0.12; → `f2c824141b8d` (n=798)
- 2. Get swept up by the title and take the lot without a second thought — output +1, health -1, dignity -1; riesgo +0.01; expl3 +0.06; → `998140e25476` (n=23)
- 3. Take the missing rise as an insult, refuse on the spot, and leave a sharp remark hanging — network -1; riesgo +0.34; expl3 +0.07; → `3a7e7317cad7` (n=27)

**Paso** `f2c824141b8d` (1172 veces): You look at it coolly. If the title gives you real experience of leading people or owning a piece of work, and sets up the next pay and promotion conversation, it is worth having. If it is just a vague promise with extra work attached, you should be wary. You take that view into the conversation wit
- 1. Take on the extra responsibility, but press for a clear pay-review date or the resources to match — skill +1, output +1, wealth +1, dignity +1, network +1; riesgo -0.17; expl3 -0.12 (n=749)
- 2. Take the title and say nothing at all about money — output +1, health -1; riesgo +0.17; expl3 +0.12 (n=22)

**Paso** `3a7e7317cad7` (26 veces): You refuse in a huff and leave a sharp remark behind. Your manager does not force the issue, but marks you down as emotional and unwilling to step up. The title might have been a stepping stone, and a flash of temper has left you little room to manoeuvre.
- 1. Cool down and go back, spelling out the terms on which you would accept — dignity +1, network +1, skill +1; riesgo -0.24 (n=21)
- 2. Make the refusal final, with no way back — network -2, output -1; riesgo +0.24 (n=1)

**Paso** `998140e25476` (22 veces): The title goes to your head and you take everything on. The work doubles and the pay does not move. 'We'll look at it next year' stays a vague promise. You become known as capable, compliant and cheap, which weakens your hand when you do try to talk about money.
- 1. Reopen the conversation, using what you have already delivered in the new role as leverage — skill +1, wealth +1, dignity +1, health -1; riesgo +0.23 (n=18)
- 2. Keep grafting for no extra money and never bring up pay — health -2, output -1; riesgo -0.23 (n=3)

## Stuck on repetitive work: do you look for something meatier?

Aparece 1461 veces (primer paso): L2 0%, L3 6%, L4 62%, L5 29%, L6 3%; meses 24–48 (mediana 35).

**Paso** `2cf4b074e7ca` (1461 veces): For a long time your work has been low-value and repetitive. It is steady, but it does not stretch you, and if you stay on it your skills will stall. Do you ask for work with more technical substance, something that would actually make you better?
- 1. Ask your manager for harder work, or find a way to make the repetitive work itself more efficient — skill +1, output +1, dignity +1; riesgo -0.71; expl3 -0.04 (n=877)
- 2. Keep the repetitive work because it is easy and does not take much thinking — skill -1; riesgo +0.37; expl3 +0.05 (n=36)
- 3. Treat the work as beneath you and phone in even the repetitive jobs — output -1, dignity -1; riesgo +0.34; expl3 -0.00 (n=17)

## An internal transfer into a new area opens up

Aparece 1454 veces (primer paso): L2 1%, L3 7%, L4 61%, L5 29%, L6 3%; meses 24–48 (mediana 34).

**Paso** `8b5416657168` (1454 veces): The company has opened internal transfers. You can apply to join a team in a more promising new area. The chance is rare, but you would have to learn a lot from scratch and give up the advantage of work you already know well. What do you do?
- 1. Weigh your interest and transferable skills, then apply, ready to learn from scratch — skill +1, dignity +1, network +1, health -1; riesgo -0.55; expl3 -0.05 (n=714)
- 2. Cling to your familiar role and skip the application — skill -1; riesgo +0.37; expl3 +0.10 (n=33)
- 3. Apply on a rush of enthusiasm, without thinking through whether you can close the gap — health -1; riesgo +0.17; expl3 -0.05 (n=212)

## Should you take a transitional role mixing engineering and management?

Aparece 1448 veces (primer paso): L2 0%, L3 7%, L4 63%, L5 27%, L6 3%; meses 24–48 (mediana 34).

**Paso** `aa16cff401b7` (1448 veces): Your manager suggests a transitional role: managing two or three people while keeping part of your engineering work. It would let you test the move from individual contributor towards management with less at stake. It could also mean doing neither job well. Do you take it?
- 1. Take it as a low-risk trial of management, and plan how you will split your time — skill +1, network +1, dignity +1; riesgo -0.63; expl3 -0.17 (n=874)
- 2. Play it safe, refuse any people responsibility, and stay a pure individual contributor — network -1; riesgo +0.30; expl3 +0.11 (n=24)
- 3. Take it but never split your time, try to do all of both jobs, and fail at both — health -1, output -1; riesgo +0.33; expl3 +0.06 (n=22)

## A fast-learning new hire stealing the limelight

Aparece 1447 veces (primer paso): L2 0%, L3 7%, L4 64%, L5 26%, L6 3%; meses 24–48 (mediana 34).

**Paso** `2ae18ed1c0f9` (1447 veces): The new joiner is full of energy, picks things up fast, and came in on a lower salary band. They have run a few meetings well. You can feel people comparing them with you in your more senior, more expensive role.
- 1. Set yourself apart: focus on architecture, quality and the hard problems the new joiner cannot yet handle — skill +2, dignity +1; riesgo -0.49; expl3 -0.15 (n=883)
- 2. Compete on hours and volume to prove you can keep up — output +1, health -2; riesgo +0.38; expl3 +0.18 (n=19)
- 3. Feel sour, quietly freeze them out, and be unhelpful — network -1, dignity -1; riesgo +0.11; expl3 -0.03 (n=27)

## Asked where you want to be in five years, you have no answer

Aparece 1447 veces (primer paso): L2 0%, L3 7%, L4 61%, L5 28%, L6 3%; meses 24–48 (mediana 34).

**Paso** `7234f844b95c` (1447 veces): During a one-to-one your manager asks you seriously: 'Have you thought about who you want to be in five years? Engineering, management, something else?' You realise you have no idea where you are heading in the long term. You are stuck for an answer.
- 1. Admit you are still working it out, and use the question to think through your long-term direction — skill +1, dignity +1; riesgo -0.18; expl3 -0.02 (n=671)
- 2. Invent an answer that sounds ambitious to get through the meeting, then never think about it again — dignity -1; riesgo +0.39; expl3 -0.06 (n=224)
- 3. Shrug it off as a pointless question: 'We'll see as we go' — dignity -1, network -1; riesgo -0.21; expl3 +0.08 (n=19)

## Build a second curve, or stay focused on the day job?

Aparece 1436 veces (primer paso): L2 1%, L3 6%, L4 67%, L5 25%, L6 2%; meses 24–48 (mediana 33).

**Paso** `29a10f21dbab` (1436 veces): You want a 'second curve' for the longer term: a new technical direction, some open source, or writing up what you know properly. It will take your evenings, and handled badly it could hurt the day job. How do you balance it?
- 1. Pick a second curve that sits alongside your career, and keep investing without letting the day job slip — skill +2, dignity +1, health -1; riesgo -0.72; expl3 -0.16 (n=883)
- 2. Dabble on and off, trying everything and finishing nothing — health -1; riesgo +0.07; expl3 -0.09 (n=20)
- 3. Dive into the side work and let the day job go to seed — output -1, network -1; riesgo +0.65; expl3 +0.25 (n=32)

## The company wants you full-stack — depth or breadth?

Aparece 1413 veces (primer paso): L2 1%, L3 5%, L4 63%, L5 28%, L6 3%; meses 24–48 (mediana 34).

**Paso** `f6855d7a804d` (1413 veces): The company wants people to go 'full-stack' and be able to pick up anything. Your strength is depth in one area, and now you are being asked to spread out. How you balance depth against breadth will shape what you end up good at.
- 1. Keep your depth as the base and widen out deliberately, building a T-shaped profile — skill +2, dignity +1, output +1; riesgo -0.72; expl3 -0.15 (n=859)
- 2. Learn a bit of everything, master none, and lose the depth you already had — skill -1; riesgo +0.28; expl3 +0.09 (n=24)
- 3. Refuse to widen out, stick to your small patch, and turn down anything new — skill -1, network -1; riesgo +0.45; expl3 +0.06 (n=25)

## Building a safety net while pay and energy still allow it

Aparece 1413 veces (primer paso): L2 0%, L3 8%, L4 62%, L5 27%, L6 3%; meses 24–48 (mediana 34).

**Paso** `28338d2cb560` (1413 veces): You realise your career will not always go this well. While your pay and energy are still decent, you start thinking about building a buffer: savings, a second skill or a network.
- 1. Plan it: build an emergency fund and steadily strengthen one transferable skill — wealth +1, skill +1, dignity +1; riesgo -0.66; expl3 -0.12 (n=864)
- 2. Let anxiety take over: save and study everything at once, and run yourself into the ground — skill +1, health -2; riesgo +0.09; expl3 -0.07 (n=15)
- 3. Decide you are overthinking it. Enjoy the present and prepare nothing — health +1, wealth -1; riesgo +0.57; expl3 +0.18 (n=26)

## A side project blurs the line with company business

Aparece 1405 veces (primer paso): L2 0%, L3 6%, L4 64%, L5 26%, L6 4%; meses 24–48 (mediana 34).

**Paso** `2323596a0539` (1473 veces): An open-source project you run in your own time unexpectedly takes off and starts to bring in consulting income. It is in the same field as the company but aimed at different customers. You have not used company time or kit. Then a client asks whether you also offer enterprise services, which would 
- 1. Tell your manager and compliance now, and ask them to assess the boundary — dignity +2, network +1, wealth -1; riesgo -1.01; expl3 -0.16; → `d9f24378d34d` (n=918)
- 2. Decline the enterprise work, keep the side project community-only, and do not tell the company yet — wealth +1, dignity +1; riesgo +1.01; expl3 +0.16; → `8034d7a663f4` (n=27)

**Paso** `d9f24378d34d` (1198 veces): Compliance confirms you are not currently in breach, but suggests you sign an extra restrictive-covenant clause limiting how far you can take enterprise services later.
- 1. Accept the terms, so the side project stays within a legal framework — dignity +2, wealth -1, network +1; riesgo +0.46; expl3 -0.11 (n=740)
- 2. Challenge the extra clause as too broad, and propose a tighter definition of the boundary — dignity +2, network -1; riesgo -0.46; expl3 +0.11 (n=25)

**Paso** `8034d7a663f4` (24 veces): The side project keeps growing. An investor approaches you about funding an 'enterprise' direction. That would raise its value sharply and put you squarely in the company's market.
- 1. Turn the investment down, disclose the side project in full, and ask compliance to review it — dignity +1, wealth -2; riesgo -0.18 (n=17)
- 2. Take the investment and prepare to leave, to put your energy into the side project — wealth +3, network -2, dignity -1; riesgo +0.18 (n=4)

## How long will the old stack last, and should you switch now?

Aparece 1404 veces (primer paso): L2 0%, L3 7%, L4 65%, L5 26%, L6 2%; meses 24–48 (mediana 34).

**Paso** `03bc33cddf88` (1404 veces): The older technology you have made your living from is still in demand, but the decline is getting harder to ignore. A voice in your head asks: is it too early to move into something new? Would waiting a bit longer be safer?
- 1. While the demand lasts and you can still think calmly, start learning a new direction now — skill +2, dignity +1, health -1; riesgo -0.51; expl3 -0.09 (n=819)
- 2. Tell yourself it will last for years yet, and stay put — skill -1; riesgo +0.02; expl3 -0.09 (n=75)
- 3. Panic and grab at every new direction, dabbling in all of them and finishing none — health -1; riesgo +0.49; expl3 +0.18 (n=22)

## Stay deep in the internals, or move to the application layer where results show faster?

Aparece 1394 veces (primer paso): L2 1%, L3 7%, L4 62%, L5 27%, L6 3%; meses 24–48 (mediana 34).

**Paso** `fe02373aed39` (1394 veces): You face a choice of technical direction: keep digging into hard, slow internals that few people can do, or move towards the application layer, where results show faster and get more attention. Each path has a cost, and the choice will shape your technical standing later.
- 1. Weigh your strengths, interest, and long-term value, then make a clear-eyed choice — skill +1, dignity +1, output +1; riesgo -0.32; expl3 -0.03 (n=770)
- 2. Chase quick wins and easier reviews, and follow the crowd into the application layer — skill -1; riesgo +0.70; expl3 +0.07 (n=21)
- 3. Stay on internals out of snobbery, look down on the application layer, and ignore the practical return — wealth -1, network -1; riesgo -0.38; expl3 -0.04 (n=122)

## Should you work seriously on management and communication skills?

Aparece 1351 veces (primer paso): L2 0%, L3 7%, L4 61%, L5 28%, L6 3%; meses 24–48 (mediana 34).

**Paso** `b987e684dad9` (1351 veces): Your technical work is strong, but communication, coordination, and dealing with senior people have always been the weak spots. Whether you stay on the engineering path or move into management, those skills matter more every year. Do you put real effort into closing the gap?
- 1. Treat soft skills as core skills too: study them and practise them deliberately — skill +1, network +1, dignity +1; riesgo -0.21; expl3 -0.05 (n=697)
- 2. Dismiss them: 'the tech is what counts — the rest is fluff' — network -1; riesgo +0.42; expl3 +0.15 (n=20)
- 3. Say you will work on them, then never practise and keep your head in the code — network -1; riesgo -0.21; expl3 -0.11 (n=146)

## Your manager hints that, after this long, you ought to be leading people

Aparece 1118 veces (primer paso): L2 0%, L3 2%, L4 56%, L5 39%, L6 3%; meses 30–48 (mediana 38).

**Paso** `51b982742b80` (1118 veces): Your manager needles you, half in jest: 'You're pretty senior on the engineering side — shouldn't you be thinking about leading people, moving up a bit? Staying on the tools forever isn't a plan.' Behind the joke, your manager clearly expects you to make the move soon. How do you answer the hint?
- 1. Take it as well meant, say whether you'd rather stay technical or try leading, and discuss a plan — skill +1, dignity +1, network +1; riesgo -0.68; expl3 -0.09 (n=641)
- 2. Let one remark push you into agreeing to lead people, against what you actually want — dignity -1; riesgo +0.27; expl3 -0.09 (n=40)
- 3. Take it as a sign they are writing you off, and snap back — network -1, dignity -1; riesgo +0.42; expl3 +0.18 (n=13)

## The promotion only comes if you move into leading people: take it?

Aparece 1073 veces (primer paso): L2 0%, L3 2%, L4 55%, L5 39%, L6 4%; meses 30–48 (mediana 38).

**Paso** `f2055b5b73d4` (1073 veces): A promotion is on the table, but the condition is a move into leading people. Pay and level go up, but you would largely leave hands-on engineering behind. It is the fork most engineers reach, where promotion means management. What do you decide?
- 1. Think through whether you are suited to leading people and actually want it, then decide — skill +1, dignity +1, network +1; riesgo -0.03; expl3 -0.13 (n=629)
- 2. Fix on the pay and the title and say yes, regardless of whether it fits — wealth +1, skill -1; riesgo +0.62; expl3 +0.18 (n=17)
- 3. Turn the promotion down without thinking, because change frightens you — dignity -1; riesgo -0.59; expl3 -0.05 (n=19)

## Write down what only you know, or keep it in your head?

Aparece 963 veces (primer paso): L2 1%, L3 7%, L4 65%, L5 25%, L6 2%; meses 24–48 (mediana 33).

**Paso** `0e1dcfcee727` (963 veces): You are the only person who really knows a core product area. For two years you have solved the hard problems, and you have never properly written down what you know. Your manager asks you to run a 'knowledge transfer' session and write a proper design document. You can see that if you hand everythi
- 1. Document it fully: the design thinking, the traps, and a troubleshooting handbook — skill +2, network +2, dignity +1; riesgo -0.48; expl3 -0.11; → `5dd8637a70d4` (n=601)
- 2. Write up the basic architecture, but keep the real troubleshooting and deeper principles to pass on in conversation — network -1, skill +1; riesgo +0.48; expl3 +0.11; → `b5a09286f316` (n=35)

**Paso** `5dd8637a70d4` (894 veces): The thorough write-up lifts the whole team. Two juniors can now handle problems that used to come only to you. At a promotion review, a panel member says you are technically strong, but it feels as if the team could now cover your current work. Shouldn't you be thinking at a higher level?
- 1. Take the feedback, and move towards architecture and technical research — skill +2, network +1; riesgo -0.43; expl3 -0.06 (n=561)
- 2. Push back: staying deep in the craft still has value, and you will not be 'managed' out of it — dignity +1, network -1; riesgo +0.43; expl3 +0.06 (n=21)

**Paso** `b5a09286f316` (34 veces): The basic document goes out, but the team still comes to you for anything complicated. You are seen as the busy expert, and you turn into the bottleneck. A critical incident hits while you are on holiday, and you cannot respond in time. A fix that should have taken an hour takes six, and a customer 
- 1. Own the mistake, start a full write-up at once, and train a deputy — dignity +2, network +1, skill +1; riesgo -0.41; expl3 -0.13 (n=24)
- 2. Blame the lack of a backup process, and say it wasn't entirely your fault — network -2, dignity -1; riesgo +0.41; expl3 +0.13 (n=5)

## Your partner's job offer in another city: live apart, stay, or rethink

Aparece 958 veces (primer paso): L2 1%, L3 6%, L4 62%, L5 28%, L6 3%; meses 24–48 (mediana 34).

**Paso** `c761ed5d2e85` (958 veces): Your partner has a strong job offer in another city that could define their career, and taking it would mean living there. You are growing fast at your current company, and your programmes and network are here. The options are living apart, one of you giving way, or making a new plan together. Which
- 1. Talk it through, back your partner and look into an internal move or remote working from their city — network +1, dignity +1, output -1; riesgo -0.30; expl3 -0.19; → `07f626b6d9cb` (n=574)
- 2. Keep things as they are: live apart, each build a career, and travel to see each other — output +1, health -2; riesgo +0.33; expl3 -0.06; → `774ee0aba7a6` (n=40)
- 3. Ask your partner to turn the offer down and stay for the household — output +1, dignity -1, network -1; riesgo -0.04; expl3 +0.25; → `50a50a700e1d` (n=20)

**Paso** `07f626b6d9cb` (851 veces): You find the nerve to talk to your manager about an internal move or remote working. The company does have a team in that city, but the role does not quite match your current direction. Going would mean proving yourself again and would slow promotion in the short term. What you and your partner both
- 1. Take the move as a fresh start that broadens your CV — skill +1, network +1, dignity +1, output -1; riesgo -0.39; expl3 -0.26 (n=540)
- 2. The terms of the move do not work, so stay and put up with the travel — output +1, health -1; riesgo +0.39; expl3 +0.26 (n=16)

**Paso** `774ee0aba7a6` (51 veces): You start living apart, kept together by weekends and video calls. The first months are fine. Then the travel wears you out, you miss important family moments, and the relationship and your energy both start to suffer. One night you race for a late train and turn up to a key review the next day in n
- 1. Agree a clear timetable for ending the distance, and plan your career around it — health +1, dignity +1, network +1; riesgo -1.11 (n=35)
- 2. Keep putting off the decision and let things drift — health -2, dignity -1; riesgo +1.11 (n=3)

**Paso** `50a50a700e1d` (21 veces): You talk your partner out of the offer. In the short term your career is untouched, but they often show regret, the atmosphere at home turns strained and you feel guilty. Six months later they are clearly low, and the sacrifice starts to damage the relationship. How do you make amends?
- 1. Make it up to them: make room for their next opportunity and take on more at home — dignity +1, network +1, health -1; riesgo +0.14 (n=15)
- 2. Take their sacrifice for granted and keep putting your own career first — output +1, dignity -2; riesgo -0.14 (n=2)

## The lunchtime badminton league and your body's limits

Aparece 954 veces (primer paso): L2 1%, L3 6%, L4 63%, L5 27%, L6 3%; meses 24–48 (mediana 34).

**Paso** `30cb2e5fe268` (954 veces): The sports club is running a badminton league. The captain wants you in: your game and fitness are both decent. An old neck and shoulder injury has flared up, though, and the project is in a sprint. You want to be part of it, but you know your body has limits.
- 1. Sign up, and say upfront that the old injury limits how hard you can play — network +1, dignity +1; riesgo -0.27; expl3 -0.11; → `57b0f72c07c2` (n=269)
- 2. Sit the matches out and help behind the scenes with the draw, the kit and the cheering — network +1, health +1, output +1; riesgo -0.23; expl3 -0.14; → `74a86f489578` (n=325)
- 3. Grit your teeth and go all in, to prove you can take it — network +1, health -2; riesgo +0.50; expl3 +0.25; → `aa3e6e549e1e` (n=11)

**Paso** `74a86f489578` (652 veces): You run the schedule, the snacks and the group chat so smoothly that the team does well. Someone says it is a shame you did not play.
- 1. Accept that your role off court still counts, and keep up the support work — dignity +1, network +1; riesgo -0.12; expl3 -0.04 (n=310)
- 2. Take the bait and jump on court for a game — health -1, network +1; riesgo +0.12; expl3 +0.04 (n=9)

**Paso** `57b0f72c07c2` (254 veces): On match day a teammate pulls out injured. The captain wants you to play an extra game. Your body could manage it, but the risk is clearly higher.
- 1. Stick to the limit you set, and suggest a substitute — dignity +1, health +1; riesgo -0.57; expl3 -0.02 (n=234)
- 2. Play the extra game and gamble that the injury won't flare up — network +1, health -2; riesgo +0.57; expl3 +0.02 (n=20)

**Paso** `aa3e6e549e1e` (15 veces): You play a run of hard games and win a key point. By evening your shoulder is really sore, and the next day even typing hurts.
- 1. Get it looked at, and ask the captain to change the rest of the plan — health +1, dignity +1, output -1; riesgo +0.75 (n=6)
- 2. Say nothing and keep carrying both the job and the matches — health -2, output -1; riesgo -0.75 (n=4)

## Whistleblowing on your manager's fake numbers

Aparece 948 veces (primer paso): L2 0%, L3 8%, L4 64%, L5 26%, L6 2%; meses 24–48 (mediana 34).

**Paso** `797a9bb03684` (948 veces): You stumble on it: your manager has been systematically inflating project numbers in reports to senior leaders, and those numbers are feeding important company decisions. You have solid evidence. Reporting would mean a break with your line manager and an uncertain future. Staying silent could make y
- 1. Secure the evidence and report carefully through compliance or internal audit — dignity +2, network -1; riesgo -1.06; expl3 -0.25; → `3d8172a6f9b2` (n=542)
- 2. Speak to your manager privately and give them a chance to put it right — network +1, dignity +1; riesgo +0.20; expl3 +0.19; → `3ffa30e45adc` (n=55)
- 3. Protect yourself: pretend you did not see it, and keep your distance — dignity -1; riesgo +0.86; expl3 +0.06; → `49cad4b1bdb2` (n=16)

**Paso** `3d8172a6f9b2` (836 veces): You put the evidence together carefully and report through compliance under your own name. The company investigates, the inflation is confirmed, and your manager is dealt with. You also become known as the person who reported their boss. Some people respect your honesty, while others are wary of you
- 1. Keep delivering solid work so your reputation rests on your ability alone — skill +2, output +1, dignity +1; riesgo -0.20; expl3 +0.03 (n=510)
- 2. Talk up the report afterwards and enjoy being the hero whistleblower — dignity -1, network -2; riesgo +0.20; expl3 -0.03 (n=17)

**Paso** `3ffa30e45adc` (67 veces): You warn your manager privately first. They deny it, then try to pull you in to 'keep it contained', even hinting it would be 'in your interest to be sensible'. You see they have no plan to stop and want you implicated too. It is messier than you thought.
- 1. Refuse to join in, keep the evidence, and report through proper channels — dignity +2, network -1; riesgo -0.79; expl3 -0.09 (n=10)
- 2. Give in to the pressure and inducements, and help cover it up — dignity -2; riesgo +0.79; expl3 +0.09 (n=43)

**Paso** `49cad4b1bdb2` (17 veces): You pretend nothing happened and keep working. Then the fake numbers come to light. Senior leaders are furious and a full investigation starts. It emerges that you had seen the data and said nothing, so you are blamed for knowing and not reporting it. You end up at the centre of it.
- 1. Explain at once, hand over the evidence you have, and cooperate — dignity +1, health -1; riesgo +0.00 (n=12)
- 2. Keep playing ignorant and try to distance yourself from it — dignity -2;  (n=2)

## Who owns your side-project algorithm?

Aparece 948 veces (primer paso): L2 1%, L3 5%, L4 63%, L5 28%, L6 4%; meses 24–48 (mediana 34).

**Paso** `232135469aa8` (948 veces): In your own time, and without directly using company resources, you have built an algorithm related to the company's work. It could be a product in its own right. Your contract says inventions connected to the business belong to the company. That clause alone does not settle it. Ownership depends on
- 1. Go along with the company filing, but ask to be named as inventor with a personal licence to use it — network +1, dignity +1, wealth +1; riesgo -0.07; expl3 -0.26; → `52a77b82154d` (n=580)
- 2. Argue it is a personal invention with no direct tie to the business, and refuse a company filing — dignity +2, network -2; riesgo +0.07; expl3 +0.26; → `dafe55b72a3a` (n=22)

**Paso** `52a77b82154d` (879 veces): The filing goes through, and you are named as inventor. Being named does not make you the owner of the patent. Once the technical detail is inside the company, your product team folds it into a core product, and the standalone product never gets off the ground. Legal then asks you to agree a separat
- 1. Accept it, and put your energy into a new technical direction — skill +1, dignity +1; riesgo +0.44; expl3 +0.05 (n=329)
- 2. Negotiate a waiver of the restrictive covenant, or compensation, for after you leave — wealth +2, network -1; riesgo -0.44; expl3 -0.05 (n=221)

**Paso** `dafe55b72a3a` (17 veces): Legal opens a file. They go through a year of your time records and commits, trying to show a technical link to a project you owned. Meanwhile your promotion review is paused because of the unresolved IP dispute.
- 1. Get independent advice from a solicitor who deals with employee inventions and post-employment restrictions — dignity +2, wealth -3, network -3; riesgo -0.45 (n=13)
- 2. Once it is clear which rights are yours, agree a one-off payment for assigning them: a private deal, not a statutory inventor award — wealth +3, dignity -2, network -1; riesgo +0.45 (n=3)

## The company goes all-in on a new bet and sidelines your work

Aparece 946 veces (primer paso): L2 0%, L3 7%, L4 65%, L5 26%, L6 2%; meses 24–48 (mediana 33).

**Paso** `e3310018ad80` (946 veces): The company loudly announces it is going all-in on a new technical direction. Headcount, budget and attention all move that way. The work you have spent years on is relabelled 'keep-the-lights-on' and starts to fade. People on the new project look like the future. People on the old product look like
- 1. Push for a place on the new work, start at the edges, and use what you know to catch up fast — skill +2, dignity +1, output +1, health -1; riesgo -0.65; expl3 -0.17; → `0c5fa01a0687` (n=594)
- 2. Stay put on the old product and wait to see whether the new bet crashes — skill -1; riesgo +0.48; expl3 +0.09; → `d7ae23484f41` (n=12)
- 3. Spread a story you know is untrue, blame named people, and slow the new team's delivery — network -2, dignity -1; riesgo +0.60; expl3 +0.01; → `096807f07880` (n=9)
- 4. Write up the cost, how mature the technology is and the risk of migrating customers, then carry out the decision — skill +1, dignity +1, output -1; riesgo -0.42; expl3 +0.07 (n=15)

**Paso** `0c5fa01a0687` (875 veces): You put your hand up for the new work, start with what you can already do, and contribute quickly on the engineering basics. The people running it notice that you learn fast and can be relied on, and they are willing to give you more. Competition is fierce, though. To stay, you still have to produce
- 1. Put your head down, make a real contribution and establish yourself on the new work — skill +2, output +2, network +1, dignity +1, health -1; riesgo -0.60; expl3 -0.12 (n=556)
- 2. Get in, then coast because you don't want to keep grafting — skill -1, output -1; riesgo +0.60; expl3 +0.12 (n=15)

**Paso** `d7ae23484f41` (12 veces): You sit on the old product and bet the new direction will fail. The company keeps investing, progress is decent, and people and budget keep being pulled off the old work. You are a little more sidelined every week. Waiting is starting to cost you.
- 1. Stop waiting and push for a move onto the new work — skill +1, dignity +1, output +1, health -1; riesgo +1.62 (n=9)
- 2. Keep watching until there is nowhere left to go — skill -2, output -1; riesgo -1.62 (n=1)

**Paso** `096807f07880` (11 veces): You spread a story you know is untrue, single people out, and get in the way of the new team's delivery. Word reaches leadership, and they mark you down as someone disrupting the work. A plainly stated technical objection would not have done that. Even if the new direction has real problems, you are
- 1. Drop the attitude, give the new work a fair look and get involved — skill +1, dignity +1, network +1; riesgo +1.31 (n=8)
- 2. Keep spreading the untrue story and blocking delivery — network -2, output -1; riesgo -1.31 (n=1)

## Colleagues invite you on a self-funded conference trip

Aparece 939 veces (primer paso): L2 0%, L3 8%, L4 62%, L5 26%, L6 3%; meses 24–48 (mediana 33).

**Paso** `d6d7a7d4fb8b` (939 veces): A few colleagues are planning to go to a tech conference in Singapore over the October half-term, with a couple of visits to friendly companies on the side. Most of it is self-funded. They are keen for you to come and say the trip will change how you see the work. You have a mortgage, and you are no
- 1. Sign up, but set a budget cap and learning goals first — skill +1, network +1, wealth -1; riesgo +0.09; expl3 -0.01; → `93980eac9a13` (n=19)
- 2. Stay at home: follow it online and write it up yourself — wealth +1, skill +1, dignity +1; riesgo -0.50; expl3 -0.19; → `d3df603756a4` (n=573)
- 3. Dither and leave the message unanswered — network -1; riesgo +0.42; expl3 +0.20; → `9e7e8aa0f326` (n=17)

**Paso** `d3df603756a4` (861 veces): You stay in the UK, follow the talks online and write notes. Someone teases that it does not count if you never left the house.
- 1. Turn the notes into a team session, and show that staying at home worked — skill +1, output +1, network +1; riesgo +0.03; expl3 -0.10 (n=528)
- 2. Take the teasing to heart, stop writing notes, and give up on the online talks halfway — skill -1, dignity -1; riesgo -0.03; expl3 +0.10 (n=24)

**Paso** `93980eac9a13` (24 veces): Before you leave, a colleague suggests upgrading the hotel and adding a business visit. That would take you well over your budget cap.
- 1. Stick to your budget and goals, and skip the upgrade — dignity +1, skill +1; riesgo -0.47 (n=13)
- 2. Say yes to keep in with the group, and worry about the money later — network +1, wealth -2; riesgo +0.47 (n=5)

**Paso** `9e7e8aa0f326` (19 veces): You still have not decided. Fares go up, and the organiser needs a final list. The group's keenness to have you along turns into mild exasperation.
- 1. Give a clear answer now, apologise, and accept the cost of dithering — dignity +1; riesgo +0.17 (n=10)
- 2. Keep delaying until someone else decides for you — network -1, dignity -1; riesgo -0.17 (n=7)

## Your manager asks: individual contributor or management?

Aparece 931 veces (primer paso): L2 0%, L3 7%, L4 67%, L5 23%, L6 3%; meses 24–48 (mediana 34).

**Paso** `0364764584dd` (931 veces): You have been in an engineering role for years, and you have reached a crossroads. Your manager sits you down: the company can keep you on the technical-expert track, or move you into leading a team. What do you actually want? This will shape a long stretch of your career, so it deserves a proper an
- 1. Weigh your interests, strengths and the long-term prospects of both paths before you choose — skill +1, dignity +1, network +1; riesgo -0.46; expl3 -0.11; → `6ef410af405f` (n=568)
- 2. Hear that management pays more and comes with people reporting to you, and pick it without thinking — skill -1; riesgo +0.28; expl3 +0.03; → `0755e0948935` (n=9)
- 3. Dodge the choice and say you are happy either way, whatever the company prefers — dignity -1; riesgo +0.18; expl3 +0.08; → `e6f094afadfa` (n=17)

**Paso** `6ef410af405f` (869 veces): You look at yourself honestly. Do you get more from digging into hard technical problems, or from organising people and resources and getting work done through others? Once that is clear, you know which way you lean, and what you would need to build if you took that path. You take the answer back to
- 1. Choose the path that fits, list the skills you still need, and ask your manager to help you grow into it — skill +2, dignity +1, network +1, output +1; riesgo -0.44; expl3 +0.00 (n=528)
- 2. See the answer clearly, then dither and refuse to commit — health -1, output -1; riesgo +0.44; expl3 -0.00 (n=23)

**Paso** `e6f094afadfa` (15 veces): You avoided the decision and handed it to the company. You are parked in a role that suits neither your strengths nor your wishes. With no plan of your own, someone else has decided where your career goes.
- 1. Take the decision back, work out your direction, and tell your manager what you want — skill +1, dignity +1, network +1; riesgo -0.61 (n=11)
- 2. Keep drifting and see what happens — skill -1, dignity -1; riesgo +0.61 (n=3)

**Paso** `0755e0948935` (11 veces): You chose management for the pay and the team under you. Leading people is a different job altogether: other people's moods, the team's numbers, endless coordination. It is nothing like the deep technical work you are good at, and for a while you are badly out of your depth.
- 1. Face the gap, learn to manage properly, and grow into a decent people manager — skill +2, network +1, output +1, health -1; riesgo -1.00 (n=6)
- 2. Fail to manage well and let your technical edge slip, losing both — skill -1, output -1; riesgo +1.00 (n=2)

## Empty your savings for a deposit, or keep cash in case work goes wrong

Aparece 918 veces (primer paso): L2 1%, L3 7%, L4 64%, L5 26%, L6 2%; meses 24–48 (mediana 33).

**Paso** `bb8eb260914a` (918 veces): After months of looking you have found a flat that fits, but the deposit would almost empty your savings and the family's, and the mortgage would take a large slice of your pay. The industry is uncertain and your product line's prospects are not especially bright. Buying means years of heavy borrowi
- 1. Do the sums: pick a mortgage you can live with and keep an emergency cash buffer — wealth +1, health +1; riesgo -0.64; expl3 -0.04; → `d4631c5f2e93` (n=430)
- 2. Go all in: empty your savings, borrow the maximum and bet your income will only rise — wealth +1, health -1; riesgo +1.20; expl3 +0.09; → `1ddb9e7a8fd1` (n=17)
- 3. Hold off: build a safety net first and watch how your job and the sector go — health +1, wealth -1, dignity -1; riesgo -0.56; expl3 -0.06; → `6eaaec0631ba` (n=141)

**Paso** `d4631c5f2e93` (687 veces): You buy a reasonably priced place, keep six months of emergency cash, and the mortgage is manageable. You feel steadier, and at work you can make longer-term choices. Then the company offers a high-risk, high-reward crunch programme. Success would speed up promotion, and failure could drag down six 
- 1. With a cash buffer behind you, take the high-reward programme and go for it — output +2, skill +1, health -1; riesgo -0.15; expl3 -0.01 (n=395)
- 2. Play it safe, take steady work, and pay the mortgage down slowly — health +1, output -1, dignity -1; riesgo +0.15; expl3 +0.01 (n=18)

**Paso** `6eaaec0631ba` (183 veces): You hold off and watch. Renting while you wait costs money, but you keep a buffer and decisions feel calmer. You feel a brief pang when family compare postcodes, but it is only a feeling and says nothing about you. Six months later both the options and your thinking have changed.
- 1. With stronger finances and a clearer head, buy without rushing when the time is right — wealth +1, health +1, dignity +1; riesgo -0.20 (n=131)
- 2. Let worry about rising prices push you into chasing a place that does not suit you — wealth -1, health -1; riesgo +0.20 (n=5)

**Paso** `1ddb9e7a8fd1` (15 veces): You borrow the maximum. On paper you are worth more, but your cash is almost gone and the mortgage is tight. Three months later there is talk of a restructure. You are more frightened of losing your job than anyone, because missing payments would be grim. The money worries start to wear down your ju
- 1. Cut spending hard, find extra income and keep your performance up at work — output +1, wealth +1, health -1; riesgo -1.50 (n=9)
- 2. Afraid of losing your job, agree with your manager on everything and keep your own views to yourself — dignity -2, health -1; riesgo +1.50 (n=5)

## Company-wide AI tools, and the fear of being replaced

Aparece 917 veces (primer paso): L2 1%, L3 7%, L4 65%, L5 25%, L6 3%; meses 24–48 (mediana 33).

**Paso** `68892377cb7e` (917 veces): The company is loudly rolling out AI coding and automation tools, wants everyone using them, and has said that 'the same work will be done with fewer people'. A lot of the day-to-day coding and boilerplate you own is exactly what AI does best. In the kitchen the talk is uneasy: 'Will the next round 
- 1. Lean in: learn the AI tools well and use them to get more done — skill +2, output +1, health -1; riesgo -0.54; expl3 -0.12; → `19f27bf33801` (n=514)
- 2. Play along in public but resist in private, sure it will never replace a real engineer — skill -1; riesgo +1.20; expl3 +0.21; → `6df399d431b1` (n=14)
- 3. Spiral: spend your energy on redundancy rumours and looking for a safe spot — network +1, health -2, output -1; riesgo -0.66; expl3 -0.10; → `7c9a905a3ed3` (n=68)

**Paso** `19f27bf33801` (782 veces): You quickly use AI to cut repetitive work by more than half. The time freed lets you take on harder system-design problems. Your manager notices both output and quality rising. Now you face a further choice: stay a highly efficient user, or learn to direct and judge what AI produces.
- 1. Move up: focus on judgement, design and quality gates that AI cannot replace — skill +2, dignity +2, network +1; riesgo -0.35; expl3 -0.10 (n=469)
- 2. Settle for being the fastest pair of hands and stop learning beyond that — output +1, skill -1; riesgo +0.35; expl3 +0.10 (n=18)

**Paso** `7c9a905a3ed3` (82 veces): You sink into anxiety, chasing rumours and refreshing Glassdoor. Your work visibly suffers. A more senior colleague says, 'Stop guessing when you'll be replaced and learn to use AI properly.' That pulls you back.
- 1. Put the anxiety to use: learn the tools and rebuild your edge — skill +2, health +1, output +1; riesgo +1.36 (n=64)
- 2. You know your colleague is right, but panic wins and you do nothing — health -2, output -1; riesgo -1.36 (n=1)

**Paso** `6df399d431b1` (11 veces): You nod along and barely use the new tools, working the old way. A few months later, colleagues who took up the tools are out-producing you, and even new starters using them quickly match your volume. People quietly start asking whether you are value for money. Staying as you are is now risky.
- 1. Drop the prejudice, learn the tools and rethink where your value lies — skill +2, output +1, dignity -1; riesgo -1.21 (n=7)
- 2. Stay stubborn and bet the company fad will pass — skill -1, output -1; riesgo +1.21 (n=2)

## Desk politics in the new office

Aparece 878 veces (primer paso): L2 1%, L3 8%, L4 64%, L5 25%, L6 2%; meses 24–48 (mediana 34).

**Paso** `64b3abc9c97d` (878 veces): The department is moving to a new office. Quiet window desks are scarce. Facilities has told teams to sort it out among themselves. Your work needs deep focus and noise easily distracts you, but you also don't want to be known as the person who grabs the good seats.
- 1. Propose open rules for allocation: the type of work, how often people collaborate, and a rotation — skill +1, dignity +1, network +1; riesgo -0.66; expl3 -0.11; → `e795a184adf7` (n=471)
- 2. Quietly get a good desk through people you know, and avoid a public row — network +1, dignity -1; riesgo +1.25; expl3 +0.19; → `168dba5be21a` (n=13)
- 3. Don't compete at all, and take whatever desk you are randomly given — health -1, output -1; riesgo -0.59; expl3 -0.08; → `c79b9c4ef557` (n=83)

**Paso** `e795a184adf7` (734 veces): The first draft of the rules gets a fair hearing. A senior colleague tells you not to be naive: going by length of service would be simpler. The mood in the room turns tense.
- 1. Compromise: give length of service some weight, but keep rotation and type of work as the priorities — network +1, dignity +1; riesgo -0.39; expl3 -0.04 (n=439)
- 2. Stick to the original rules and push back on the senior colleague in public — dignity +1, network -1; riesgo +0.39; expl3 +0.04 (n=18)

**Paso** `c79b9c4ef557` (104 veces): You end up by a noisy walkway. Two weeks in, you are clearly finding it harder to concentrate, and you start to regret not arguing.
- 1. Ask to move, backing your case with numbers on how the desk affects your delivery — output +1, dignity +1, skill +1; riesgo +0.78 (n=75)
- 2. Keep putting up with it, and rely on earplugs — health -1, output -1; riesgo -0.78 (n=5)

**Paso** `168dba5be21a` (11 veces): You secure a good desk early. On moving day someone notices the seating plan was quietly changed, and people start guessing who arranged it.
- 1. Explain how you got the desk, and suggest going back to a transparent allocation — dignity +1; riesgo +0.19 (n=8)
- 2. Say nothing and hope it blows over — network -1; riesgo -0.19 (n=3)

## Share options shrink in a buyback: living with the letdown

Aparece 691 veces (primer paso): L2 0%, L3 2%, L4 58%, L5 37%, L6 4%; meses 30–48 (mediana 38).

**Paso** `620f31dc7c8e` (691 veces): Years ago you took less cash pay in exchange for share options, and you stayed. A new funding round has cut the valuation hard. HR says the options will be bought back at a very low price. The number that once made your heart leap is now almost nothing. You feel disappointed, angry and misled. What 
- 1. Read the scheme and buyback terms, run the numbers and make your case from the paperwork — skill +1, dignity +1; riesgo -0.66; expl3 -0.17; → `cfd501ed7504` (n=400)
- 2. Take it as your cue to leave and start job-hunting in earnest — network +1, output -1; riesgo -0.25; expl3 -0.06; → `ee931e41291f` (n=22)
- 3. Let the grievance show at work: coast, and tell everyone the company over-promised — dignity -1, output -1; riesgo +0.91; expl3 +0.23; → `f696567d0062` (n=14)

**Paso** `cfd501ed7504` (616 veces): You go through the option agreement line by line and find that some clauses of the buyback leave room to negotiate. With a few longer-serving colleagues you put a reasoned case. The company softens and offers a compromise: cash, a pay rise, or faster vesting. Now you choose: take something certain, 
- 1. Push for cash or a pay rise and turn paper value into real money — wealth +2, dignity +1, network +1; riesgo -0.96; expl3 -0.05 (n=363)
- 2. Trust the company's story again and accept a new option arrangement — dignity +1, wealth -1; riesgo +0.96; expl3 +0.05 (n=12)

**Paso** `ee931e41291f` (27 veces): You take the loss as a warning, realise how long you have been tied to a future payday, and start testing your market value. A few conversations later it is clear you can get an offer with more guaranteed cash. Leaving in a rush also means giving up the relationships and the work you have built here
- 1. Once you have an offer with more guaranteed cash, hand over cleanly and go — wealth +2, network +1, skill +1; riesgo -0.28 (n=18)
- 2. Take the outside offer to your company and negotiate better terms to stay — wealth +1, dignity +1; riesgo +0.28 (n=4)

**Paso** `f696567d0062` (11 veces): Your grievance about the broken promises spills into your work. Output drops and you complain constantly. None of it brings the options back, and your manager starts to notice. Your performance slides too. Someone else made the mistake, and your prospects are paying for it. Time to stop the damage.
- 1. Set your feelings aside and decide: negotiate properly or leave, and stop sabotaging yourself — dignity +1, output +1; riesgo +0.25 (n=7)
- 2. Keep coasting in protest and bet the company will not touch you — output -2, dignity -2; riesgo -0.25 (n=3)

## Burnt out on the same work: reshape the job or not?

Aparece 680 veces (primer paso): L2 0%, L3 2%, L4 56%, L5 39%, L6 4%; meses 30–48 (mediana 38).

**Paso** `7fadd88f7d08` (680 veces): You have been doing the same kind of work for a long time. You could do it with your eyes closed, and you cannot find any energy for it. You have stopped growing, the spark has gone, and deep burnout has set in. You can see that if this goes on, you will go stale. Do you reshape the job, or keep num
- 1. Work out where the burnout comes from, and design a new direction or a reshaped role for yourself — skill +1, dignity +1, health +1; riesgo -0.66; expl3 -0.27; → `fcafef46f4d4` (n=410)
- 2. Keep telling yourself a new job would fix it, and spend your energy on job boards and daydreams — output -1; riesgo +0.88; → `f2b851ecccd1` (n=6)
- 3. Stay numb, coast, and stall your way through the days — output -1, health -1; riesgo -0.22; expl3 +0.27; → `29d7b9b01079` (n=8)

**Paso** `fcafef46f4d4` (630 veces): You think it through. Is it the lack of challenge, no sense of purpose, or the feeling that you are not learning anything new? Once that is clear, you sketch out changes: automating the repetitive work, taking on a harder brief, or stretching into a neighbouring skill. You take a proposal to your ma
- 1. Go after harder work that stretches you, and turn the burnout into a step up — skill +2, output +1, network +1, dignity +1; riesgo -0.30; expl3 +0.04 (n=375)
- 2. Lose your nerve with the plan in hand, and back off — dignity -1, health -1; riesgo +0.30; expl3 -0.04 (n=10)

**Paso** `29d7b9b01079` (7 veces): You stay numb, coast, and stall. The burnout does not ease. Your delivery and form keep sliding. Of all the ways to meet burnout, drifting like this does the most damage.
- 1. Hit rock bottom and push back: force a first step towards changing the job, and look for a small win — skill +1, output +1, health +1, dignity +1; riesgo -1.40 (n=5)
- 2. Keep sinking and fully check out — output -2, health -1; riesgo +1.40 (n=1)

**Paso** `f2b851ecccd1` (5 veces): You keep telling yourself a new place would fix it, and spend your energy on job boards and imagined exits. Then it dawns on you: you have not given yourself anything to grow into, and a new desk would bring the same repetition. The daydreaming has not eased the burnout, and the day job has suffered
- 1. Stop treating the next job as an escape, and reshape your work and growth from where you are — skill +1, dignity +1, output +1; riesgo +0.00 (n=5)
- 2. Stay hooked on the fantasy that the next job will be better, while the current one keeps sliding — sin datos

## A restrictive covenant on the way out: take the pay or keep your options

Aparece 679 veces (primer paso): L2 0%, L3 1%, L4 53%, L5 42%, L6 5%; meses 30–48 (mediana 38).

**Paso** `99f269c9e01e` (679 veces): You have decided to leave. When you get to the paperwork, HR produces a new restriction: for a year after you go, you must not join a competitor, in return for a monthly payment. Your better offer is from a company that may or may not count as a competitor. You can read the clause and negotiate, or 
- 1. Read the clauses, take advice if needed, and decide only once you know the scope and payment — skill +1, dignity +1; riesgo -0.89; expl3 -0.15; → `c180d2405ffb` (n=391)
- 2. Sign cheerfully so the exit goes smoothly, and worry about the next job later — network +1; riesgo +0.44; expl3 +0.15; → `b778b84f59a2` (n=13)
- 3. Decline the new restriction outright — dignity +1, network -1; riesgo +0.44; → `6d0915d4c6c3` (n=7)

**Paso** `c180d2405ffb` (632 veces): You work through the clauses: scope, payment, and what happens if you breach. You also weigh the risk that your new employer would count as a competitor. Knowing all that, you can negotiate on equal terms: narrow the scope, raise the payment, or simply go somewhere the restriction does not reach.
- 1. Negotiate a narrower scope or a better payment, and sign a version both sides can live with — wealth +1, dignity +1, network +1; riesgo +0.14; expl3 +0.01 (n=236)
- 2. Choose a direction the restriction does not cover and avoid the dispute altogether — skill +1, dignity +1; riesgo -0.14; expl3 -0.01 (n=143)

**Paso** `b778b84f59a2` (10 veces): You sign without a close read and leave smoothly. Three months later a solicitor's letter arrives. The old employer says your new company is caught by the clause and asks you to stop. Whether the clause applies, and whether it can be enforced, is now in dispute. Your signature did not settle either 
- 1. Stay calm, gather evidence, get professional help, and deal with the dispute by the rules — skill +1, dignity +1, wealth -1; riesgo +0.06 (n=8)
- 2. Panic, let them lead, and rush into a costly settlement — wealth -2, dignity -1; riesgo -0.06 (n=2)

**Paso** `6d0915d4c6c3` (5 veces): You decline the new clause. HR would rather you signed, but they still process the resignation. You can leave it there and sort out notice in the ordinary way, or you can refuse the handover, keep the company laptop, and argue it out with HR in the team channel.
- 1. Leave it there: agree how notice will work and go without signing the new restriction — dignity +1, network +1; riesgo +1.00 (n=3)
- 2. Refuse the handover, keep the company laptop, and argue it out with HR in the team channel — network -2, dignity -1; riesgo -1.00 (n=2)

## Stuck on the ladder: move into management or go deeper?

Aparece 655 veces (primer paso): L2 0%, L3 2%, L4 53%, L5 40%, L6 5%; meses 30–48 (mediana 39).

**Paso** `5d2ce1e8c306` (655 veces): You are a senior engineer, and you have been stuck at the same level for years. Technical roles above you are scarce, but management posts, oddly, are open. You can keep grinding on the specialist track and wait for one of the few expert roles, or move sideways into management and take a different r
- 1. Look hard at how far each path goes, how well you fit and how the company promotes, before you decide — skill +1, dignity +1, network +1; riesgo -0.25; expl3 -0.20; → `81fc813b94f7` (n=380)
- 2. Push into management, which you neither enjoy nor are good at, just for the title and the pay — skill -1; riesgo -0.47; expl3 -0.13; → `1f068500dd8d` (n=13)
- 3. Do neither: stay put and complain that the company won't give you a chance — output -1, dignity -1; riesgo +0.72; expl3 +0.33; → `eb654ba87e83` (n=12)

**Paso** `81fc813b94f7` (594 veces): You think both paths through. The specialist track is narrow, but the top of it is valuable. Management is wider, but it is a different job. Weighed against your temperament and how this company works, the choice becomes clearer. Now you have to act on it.
- 1. Commit: either go for a management role, or go deep enough to gain real technical influence — skill +2, output +1, network +1, dignity +1; riesgo -0.17; expl3 -0.04 (n=346)
- 2. Finish the analysis but stay on the fence, unwilling to commit — health -1, output -1; riesgo +0.17; expl3 +0.04 (n=12)

**Paso** `1f068500dd8d` (17 veces): You forced the move for the promotion. You neither enjoy nor are good at leading people, coordinating work or handling people problems. The team's results are flat, and the job never feels right. Having taken the role only for the grade, you find every day hard going.
- 1. Either put the work into becoming a capable manager, or admit it doesn't suit you and go back to the technical track — skill +1, dignity +1, network +1, health -1; riesgo +0.45 (n=11)
- 2. Grit your teeth in a role that doesn't suit you, and grow more bitter in it — health -2, output -1; riesgo -0.45 (n=2)

**Paso** `eb654ba87e83` (10 veces): You neither move across nor go deeper. Your energy goes into complaining. While you stand still, you slide backwards: your technical skills stop moving, the management route never starts, and even the day job begins to sag.
- 1. Stop complaining, make a choice, and act on it — skill +1, output +1, dignity +1; riesgo +0.00 (n=7)
- 2. Stay stuck and keep blaming everyone else — skill -1, output -1; riesgo +0.00 (n=2)
