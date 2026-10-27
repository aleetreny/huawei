# Confronto dei pattern con i risultati di Ale

27 ottobre 2026. Richiesta: verificare che i sei pattern brevi condivisi in chat siano consistenti con la ricerca di Ale. Fonte recuperata con fetch mirato, senza cambiare branch: `origin/cloud-lab-run`, commit `26e976f`, chiusura del 26 ottobre alle 23:25 UTC. La nostra copia di lavoro del vecchio report cloud si fermava alle 16:19; non basta per questo confronto. Snapshot e hash in `provenance.json`.

## Esito

**Coerenti nella direzione generale, ma non sei regole tutte confermate indipendentemente.** Occorre distinguere associazioni storiche, esiti di pacchetti e trasferimento fra bot, Haiku e DeepSeek. Nessuna garanzia universale.

| Pattern della chat | Riscontro di Ale | Precisazione necessaria |
|---|---|---|
| Grow in balance | G4 e ricerca sugli stati: uscire da L1, risultati visibili, collaborazione; inseguire Network perché è il numero minore compare nelle carriere fallite | Diagnosticare un vero limite da feedback e cambiamenti; non pareggiare i numeri o massimizzare una sola statistica |
| Check the payoff | G4 riporta Skill che smette di crescere al livello; G2 segnala recupero eccessivo nelle sconfitte v1 | Compatibile, ma Ale non dimostra che cambiare sempre azione dopo un guadagno nullo sia universalmente migliore |
| Protect your progress | Il campione temporale ha 1.177/4.701 transizioni di storia coincidenti con calo Output/Network; il campione non isola causalità. Il campione di gara favorisce il guardrail limitato a Output/Network prima della prima promozione | Evitare il veto assoluto: la variante che protegge Skill/Network/Output per tutta la carriera completa 2/4 ed è scartata. Alcune perdite possono essere necessarie |
| Remember past problems | G1 e distillazione R5: dopo un incidente un messaggio rassicurante può precedere un'altra crisi | La memoria non sostituisce azioni di risanamento e risposta ai segnali. Ale favorisce cleanup sui segnali lungo tutta la carriera; noi abbiamo stimato un diverso pacchetto memoria+lookup |
| Keep a financial buffer | Ale segnala uscite Broke e raccomanda Wealth positivo; il deficit finale di ricchezza è soprattutto legato al livello/salario | La specifica riserva leggera è sostenuta dal nostro studio con bot, non confermata indipendentemente dai confronti di Ale |
| Think beyond immediate reward | G1/G2/G5, fallimenti delle varianti aggressive e rischio degli impegni non chiusi | Coerente; non dimostra l'efficacia di un qualsiasi filtro numerico. Il nostro filtro non supera il riferimento |

Due elementi di Ale meritano presenza esplicita nella sintesi: **risposta concreta alle review deboli** (G3) e **cura preventiva della salute senza recupero inutile** (G2). Un manuale che elimina il piano di recupero della performance può fallire anche se contiene regole apparentemente ragionevoli su rischio e crescita.

## Risultati recenti da non confondere con quelli preliminari

Il report finale della gara, alle 23:24, riporta `targeted-1026-201334` campione con media Q51,6 e 10/13 completate. Il 10/12 e Q53,9 riportato nelle lezioni è il dato precedente al momento della promozione a campione (21:29), non una contraddizione. Il guardrail è limitato a preservare Output e Network nelle storie fino alla prima promozione, mantenendo le protezioni del padre. Il dato non identifica una formula causale né una garanzia.

Il principio più ampio di preservare tutte e tre le statistiche in ogni storia è stato provato e scartato (2/4, Q42,8). Perciò la frase “protect your progress” da sola è troppo facile da interpretare rigidamente. Anche “equilibrio” richiede feedback e contesto, non minimi numerici confrontati fra scale diverse.

La ricerca di Ale sullo stato mostra 2/14 completamenti per carriere ancora a L1 al secondo taglio contro 26/38 già promosse, condizionati a essere osservate e attive. Essere in ritardo è un allarme, non una condanna. Il nostro gruppo di 53 mancati primi avanzamenti contiene 45 recuperi entro dodici mesi; i due numeri non sono comparabili direttamente e non sono in conflitto.

## English version to share

- Work on the real bottleneck, not simply the lowest number.
- Protect delivery and relationships, especially before the first promotion; accept necessary costs.
- After a weak review, address the named weakness and keep delivering.
- Recover early, act on risk warnings, and remember past incidents.
- Check actual benefits before repeating an investment.
- Keep cash positive without sacrificing useful growth or safety.

These are working principles, not a guaranteed promotion recipe. Our specific light-reserve policy has supporting bot evidence; Ale has not independently confirmed it.

## Sources

- `sources/ale-lessons.md`: G1–G5, promising ideas, failed variants, frontier and caveats. The word “proven” is the source's wording; this comparison does not promote observational evidence to causal proof.
- `sources/ale-race-status.md`: final ladder counts and champion at 23:24.
- `sources/ale-decision-research.md`: predictive state analysis, missing observations, temporal alignment and limits on attributing effects to actions.
- Our existing financial, incident, growth-gap and safety-filter reports remain unchanged. This comparison changes no frozen policy, protocol, bundle or visualization.

## Relevo

Completed: targeted fetch, read-only review of Ale's newer reports, comparison of all six claims, narrower English wording and documented version differences. Updated only Matteo's T4 row. No new game, gameplay model call, automation, registry write or message to another person/thread. No merge of Ale's branch; frozen copies permit review without changing checkout.

Validation: checked source hashes and consistency between final champion counts and the earlier snapshot; 287 software tests passed with the pre-existing Authlib warning. Commit and push on our own branch, using existing PR #12 to request integration. Earlier pushes were pending due GitHub connection failures; if publishing fails again, retain local commits and retry `git push origin HEAD:matteo-t4-growth`. No gameplay to restart. This is a documentation review, not a new experiment or a test of the revised English instructions.
