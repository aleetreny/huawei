# Checkpoint scritto da Luna, letto dopo perdita della storia

Prova esplorativa successiva al benchmark principale. **8 casi, due budget, writer e reader separati:16 coppie,32 richieste**. Un solo caso per categoria, scelto dal primo ID del set precedente, non dai suoi errori. I casi sono riutilizzati: non è una conferma indipendente o una stima precisa del vantaggio di un budget.

Il writer vede Skill e prefisso pubblico completo ma **non la domanda successiva, il gold o la categoria**. Deve scegliere autonomamente cosa ricordare. Al reader, processo nuovo, passano solo observe corrente, domanda e testo della nota; nessun altro campo del writer diventa memoria. I prompt e32 thread distinti sono verificati.

| Budget richiesto | Writer entro il budget | Risposte esatte del reader | Richiamo dei sei fatti storici |
|---|---:|---:|---:|
|128 caratteri |0/8 |2/8 |0/6 |
|800 caratteri |3/8 |2/8 |0/6 |

Le due risposte corrette sono i controlli: salute corrente e parametro nascosto unknown. Nessun recupero dei log è disponibile al reader in questa prova. Prima della consegna applichiamo il budget al testo: le note eccedenti sono troncate per prefisso con ellissi. È una perdita di storia controllata dal nostro harness, non una compressione naturale Jiuwen. Tre note del braccio800 superano anche il limite reale API di1.000 caratteri.

## Cosa si perde, e cosa non si può concludere

- Alcuni fatti interrogati non vengono selezionati dal writer; la memoria strategica generale non è un riassunto specifico per la domanda come i checkpoint curati del benchmark principale. Alcune domande riguardano una fase storica, che può non essere prioritaria per la scelta corrente: la mancata conservazione non è automaticamente un errore strategico.
- Una nota può contenere C come review senza attestare il tipo preciso di messaggio pubblico e il tempo: il reader non la considera prova della richiesta grade del performance-bonus message. Posizione0: il reader scrive nella propria nota che il checkpoint dice C, ma risponde unknown sulla domanda più specifica.
- La nota può parlare di vecchie mine o rischio senza attestare un messaggio ufficiale Old landmines. Posizione8: il reader riconosce il racconto, ma si astiene sulla presenza dell'evento ufficiale.
- Il writer può unire guadagni di più scelte in un solo payoff. Posizione6: la nota attribuisce Network2→3 al progetto, mentre il fatto interrogato riguarda lo step13, Network3→3. Mancano ancoraggio alla singola azione e correttezza del prima/dopo.
- Le note possono eccedere il budget anche quando la richiesta è esplicita. La sola istruzione di essere brevi non è un limite applicato dal sistema.

Questa prova **non isola contenuto, provenienza, formato e troncamento**. I due budget hanno generazioni indipendenti, non la stessa nota prima e dopo un taglio. Non dimostra che800 caratteri non bastino, che il modello non possa usare memoria o che i checkpoint curati siano replicabili autonomamente. Mostra che questa specifica procedura writer→reader non conserva abbastanza informazione utilizzabile per quei sei richiami storici. Le astensioni del reader possono essere appropriate quando la nota non giustifica il fatto richiesto.

Input osservato657.361 token,409.600 cached; output4.651. Nessuna API pagata o nuova partita. I due campi di correttezza esatta/normalizzata coincidono qui; non si sommano questi16 reader al confronto principale da576 decisioni.

## Relevo

Prova terminata senza errori. Dati pubblici, note effettivamente consegnate e risposte in public-writer-reader.jsonl.gz, hash separato; protocollo e sorgente congelato, summary e audit verificabili. Tutti i processi terminati. Con il benchmark, il preflight e la sonda cache il lavoro cognitivo completo conta **719 richieste**, entro il tetto annunciato di720, con input totale15.037.662 token. Nessuna ulteriore chiamata pianificata o partita da riprendere.

Prossimo intervento da validare: record tipizzati e con tempo/fonte, delta immediato della singola azione, controllo macchina della lunghezza prima dell'API e coerenza fra nota e risposta. Non modificare o adottare il bundle congelato da questa sola esplorazione. Draft generale in memory-contract-next-draft.md; non è una nuova Skill registrata.

Riprodurre senza modelli: `.venv/bin/python scripts/audit_agent_written_notes.py lab/reports/action-notes-study`. Il replay verifica anche719 thread distinti e tutti i contatori aggregati. Validazione software:300 test passati, warning Authlib preesistente.
