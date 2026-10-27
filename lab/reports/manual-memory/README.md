# Memoria nei manuali: inventario, canale e costo

27 ottobre 2026. Richiesta di Matteo: capire se i manuali hanno memoria, se possiamo aggiungerla e a quale costo. **La memoria esiste già; è disomogenea e non equivale a un archivio persistente gestito dal modello.** Non si modifica alcun manuale congelato o giocato.

## Che cosa c'è già

| Manuale | Memoria prevista |
|---|---|
| observed-growth-v1, run personale Q70,94 | Ricordare ultima debolezza di review, avvisi aperti, impegni e benefici degli investimenti; nota breve priorità/evidenza/scelta. Nessuna serializzazione completa obbligatoria |
| promotion-readiness-v2 | Memoria compatta di beneficio atteso/effettivo e impegni con proprietario, prossima azione e condizione di seguito. Nessun canale persistente esplicito |
| Bozza generale primo anno | Distingue avvisi correnti, storia degli incidenti e impegni aperti. Non validata con agenti |
| F6 commitment-ledger | Registro esplicito in ogni nota: open, promised, risks, weak, plan; recupero dai log dopo reset |
| Campione di Ale targeted-1026-201334 | Stato Clear/Raised/Escalating, discesa dopo un trimestre senza segnali, piano dopo review debole e recupero dei log quando servono; nessun registro esplicito distinto degli incidenti passati |

I primi quattro sono letti dalla nostra branch. Il campione è congelato dal commit cloud `26e976f`; testo in `ale-champion-snapshot.md`. Percorsi e hash sono in `audit.json`. Sono istruzioni previste: non provano che l'agente le esegua o ricordi ogni fatto.

## Come renderla recuperabile senza nuovi strumenti

Il worker (`careerlab/actors/claude_cli.py`) espone solo i cinque strumenti del gioco. `take_action` accetta `notes`, e `check_latest_logs` restituisce log pubblici. Il prompt di identità già prevede observe + log in caso di contesto mancante (`careerlab/prompts/identity.md`). Le continuazioni Claude possono avviare un nuovo processo; conservare soltanto il ragionamento interno non basta a garantire il recupero.

Non abbiamo un tool di scrittura di file o di memoria dedicata fra i cinque strumenti. Una frase in una Skill non aggiunge tale capacità. Il checkout del runner ufficiale non è presente qui: non pretendiamo di aver verificato adesso la sua gestione attuale di MEMORY.md, cancellazione dei messaggi o compressione. Nessuna lettura degli interni del simulatore. Le note devono contenere solo fatti della partita corrente, non informazioni apprese da altre partite.

Verifica offline su un prefisso pubblico già raccolto, `constrained-growth-study/study-v1/run0`: 51 azioni, 50 note ritrovate esattamente nei log ufficiali archiviati. La nota dell'azione `Continue` non compare; le altre 50 sono brevi, massimo60 caratteri. Questo conferma un canale utilizzabile nelle azioni osservate, **non** l'assenza di troncamento per note lunghe, la restituzione su ogni tipo di azione, il recupero dopo reset o una garanzia di ordine/completezza per un numero piccolo di log. Non è stata lanciata una nuova partita per verificarlo. In caso di recupero cercare l'ultimo record effettivamente presente, senza inventare fatti mancanti.

## Proposta minima

Non riscrivere da zero un sistema già presente. Aggiungere a una nuova variante solo il pezzo mancante: memoria esplicita degli incidenti passati separata dall'avviso corrente, insieme all'ultimo beneficio verificato. Un record candidato può mantenere quattro campi brevi:

`Past incident | Open + next | Review gap | Last payoff`

Le note sostituiscono il riassunto corrente sul piano semantico, non cancellano le vecchie note dalla cronologia del runner. Si eliminano gli impegni risolti solo con evidenza; un incidente passato non sparisce quando il pannello si calma. Non fare un diario completo o copiare tutte le statistiche già visibili.

Il [testo inglese proposto](memory-addon-draft.md) è una proposta reviewable, non una Skill registrata, non una modifica al campione e non un intervento eseguito. Un futuro confronto dovrebbe cambiare solo questo componente, mantenendo invariati priorità, risposte alle review e gestione delle risorse.

## Costo: scrittura e rilettura sono cose diverse

Preparare istruzioni e audit offline non consuma quota di gioco. In partita le note possono usare la chiamata take_action che l'agente deve già fare: **nessuna chiamata aggiuntiva richiesta per ogni salvataggio**. Un recupero dei log aggiunge invece il suo output e le successive letture; usarlo solo quando manca il contesto o un fatto necessario.

Esempio di pianificazione, **non misura del tokenizer DeepSeek o previsione empirica**: 200 azioni e40–60 token **aggiuntivi rispetto alle note attuali**, a48 mesi. Assumiamo che ogni nota entri alla fine di un'azione e sia riletta in due richieste del modello per ciascuna azione successiva, senza compressione o scarto della cronologia.

| Token extra per azione | Output extra | Input extra da riletture | Totale extra |
|---|---:|---:|---:|
| 40 | 8.000 | 1.592.000 | 1.600.000 |
| 60 | 12.000 | 2.388.000 | 2.400.000 |

Formula dello scenario: output = L×A; input = L×r×A×(A−1)/2. Le richieste reali possono essere più o meno di due per azione; la compressione cambia il conto, e le chiamate di recupero possono aumentarlo. Sono esclusi istruzioni statiche, serializzazione e possibili variazioni del ragionamento. Le nuove istruzioni statiche aggiungono il loro numero di token a ogni richiesta che le include. Il valore40–60 è un'ipotesi di budget, non una lunghezza misurata del testo proposto.

**Prezzo in denaro:** non assegnare un costo per token inventato. Costo marginale = (input non in cache×tariffa input + letture cache×tariffa cache + output×tariffa output)/1.000.000, con eventuali scritture cache fatturate separatamente. Servono modello, route, prezzi applicabili e contatori reali di cache. Non è effettuata una stima corrente in USD o euro.

**Punteggio token:** secondo la formula implementata nel nostro lab (`careerlab/stats.py`), nello scenario sopra e solo nel tratto lineare,1,6–2,4M token aggiuntivi su48 mesi costerebbero circa0,13–0,20 punti della componente pesata totale (E pesa10%). Se il consumo resta sotto la soglia di massimo, o intervengono clipping/cap di uscita anticipata, la differenza cambia anche fino a zero. Non è un punteggio misurato, una nuova verifica del regolamento o una garanzia di costo trascurabile.

## Vale la pena?

L'effetto della memoria non è ancora isolato. Ale riporta F6 a3/6 completate eQ40,8; il pacchetto con registro non ha superato i riferimenti, ma non si può attribuire il risultato al registro perché cambiano anche le regole. Anche le semplici righe di stato non hanno confermato il beneficio iniziale. Il nostro studio incidenti stima memoria **insieme** a un lookup empirico: non prova l'effetto della sola memoria in un agente che legge prosa.

Proposta: breve memoria fattuale recuperabile, senza un nuovo agente riassuntore o un registro verboso. Prima misurare che la nuova versione scriva e recuperi i fatti corretti; solo successivamente valutarne gli esiti con agenti, se autorizzato. Restano non eseguiti controlli live di note lunghe, reset e tokenizer/costi nel runner target. Il confronto Haiku sospeso resta invariato e non giocato.

## Relevo

Completato: inventario di cinque manuali/bozze con hash; snapshot del campione di Ale; verifica di50 note pubbliche già archiviate e limite dell'azione Continue; proposta inglese separata; scenario riproducibile di token e punteggio con assunzioni esplicite. Solo file del nostro laboratorio e risposte pubbliche già raccolte. Nessun modello di gioco, nuova partita, quota di gioco, automazione, modifica al runtime, pacchetto o database interno, bundle congelato o registro centrale.

Riprodurre: `.venv/bin/python scripts/audit_manual_memory.py`. Validazione: 287 test software passati con il warning Authlib preesistente; non è una valutazione della strategia. Aggiornare solo la rigaT4 di Matteo, commit/push sulla nostra branch e PR#12. Nessuna nuova versione in coda. Per implementare una variante scegliere prima il padre e sostituire istruzioni ridondanti, non aggiungere75 parole a ogni manuale indiscriminatamente: il campione letto ha479 parole eF6 ne ha642 contando il file intero, già oltre l'obiettivo indicativo di circa400 del laboratorio.
