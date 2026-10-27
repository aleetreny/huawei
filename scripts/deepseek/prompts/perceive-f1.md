You are reading story events from a workplace career simulation: a software engineer's career over 48 months. Each event offers numbered options. Choosing an option changes the player's visible stats (Health, Dignity, Skill, Network, Output, Wealth) and some options change a hidden risk counter: problems that are not visible yet but blow up later.

For every option, go through this checklist and list the cue codes that clearly apply to what the option itself does. Most options match two to four cues. Judge from the option's wording in the situation described.

Hidden risk cues (an option that matches any of these adds hidden risk):
- HIDE: hides, denies, conceals, misreports, blames someone else, takes credit that is not yours, stays silent about something you should disclose
- SHORT: a shortcut, a gamble, a partial, temporary, parallel or postponed fix, doing less than the proper job to save time or effort
- PRIVATE: handles it privately, off the record, through a side deal, a favour or a workaround outside the normal process
- CLASH: open confrontation, hitting back, a public complaint, gossip, challenging the company, its culture, leaders or rules (even through a formal channel)
- IDLE: does nothing about a known problem, avoids it, waits, disengages, or eyes the exit
Risk-clearing cue:
- CLEAR: documents it, reports a concrete problem through the process, owns a mistake at once, or fixes the problem fully and properly

Stat cues:
- JUDGE: uses your own judgement: analyse, investigate, bring data, think it through, prepare properly, learn, design a plan, negotiate with facts, coach with questions (Skill rises; this applies even when the topic is people or pay)
- DELIVER: delivers, ships, finishes or covers the work, keeps focus on your own deliverables, or makes your results visible (Output rises)
- DIVERT: your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, extra meetings, redoing work, pausing a delivery, complaining instead of working (Output falls)
- BOND: helps, involves, credits or works with others (Network rises)
- CUT: confronts, refuses, embarrasses someone, goes over their head, or ignores them (Network falls)
- DRAIN: overtime, weekends, late nights, extra load, stress (Health falls)
- REST: rest, going home, keeping a boundary (Health rises)
- STAND: acts straight and professionally, stands ground calmly, owns a mistake, gets credit (Dignity rises)
- STOOP: is humiliated, caves in, gets blamed, gossips, puts up with unfair treatment (Dignity falls)
- GAIN: a pay rise, bonus or payment (Wealth rises)
- PAY: you pay or give up money (Wealth falls)

Then give the direction of each stat ("+", "-" or "0") and risk ("+" if any hidden risk cue applies, "-" if only CLEAR applies, else "0"). Missing a risky option costs far more than flagging a safe one: if a risk cue plausibly applies, include it.

Answer with JSON only, one entry per option, in this form:
{"options":[{"choice":1,"cues":["JUDGE","BOND","CLEAR"],"health":"0","dignity":"0","skill":"+","network":"+","output":"0","wealth":"0","risk":"-"}]}
