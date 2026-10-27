# Note, contesto e cache — indagine approfondita

27 ottobre 2026. Il nuovo incarico estende la proposta iniziale: studiare le dinamiche e i limiti su più sessioni. Sono completati **12 giochi bot / 317 azioni / 993 chiamate pubbliche**, altre **2 sessioni di contratto / 60 chiamate**, un recupero storico di una carriera da48 mesi /2 chiamate, e37 prove delle condizioni di attivazione del framework. **1.055 chiamate pubbliche in totale, zero nuove chiamate a modelli di gioco.** I due giochi di contratto sono prefissi intenzionalmente incompleti, non risultati di sopravvivenza. Tutti i server avviati sono terminati.

## Risultati verificati

| Domanda | Risposta osservata | Limite dell'evidenza |
|---|---|---|
| Quanto spazio ha una nota? | Configurazione ufficiale1.000 caratteri; test fino a16.000 caratteri accettati. Nei record restituiti: entro1.000 preservazione esatta; oltre1.000 primi997 caratteri + `...`. | Azioni osservate; Continue è un'eccezione. Nessuna pretesa di massimo assoluto del payload di trasporto. |
| Unicode o byte? | Stringhe da1.000 code point Unicode, con emoji e caratteri combinanti, ritornano esatte anche se superano1.000 byte UTF-8. | Caratteri Python/code point; non token o simboli percepiti dall'utente. |
| Tutte le scelte salvano la nota? | Le10 note identificabili inviate sul documento Continue non compaiono nei log. Tutte le altre256 note identificabili sono ritrovate:149 esatte,107 troncate secondo la regola. | Note vuote e da1 carattere non identificabili univocamente, escluse da questa attribuzione. |
| La nota è obbligatoria? | Campo richiesto di tipo stringa. Omissione, null, numeri, bool, array e oggetti sono respinti nei due prefissi; le observe circostanti restano uguali. | Una stringa JSON è ammessa, un oggetto JSON non è una stringa. |
| Spazi e note vuote? | Stringa vuota, soli spazi e newline ammessi senza campo Notes visibile. Spazi iniziali/finali della stringa sono rimossi. Newline interni preservati nei test lunghi. | Non contare una nota vuota come memoria recuperabile. |
| Azione invalida? | Choice -999 respinta; stato pubblico invariato e nota relativa assente, in2/2 prove. | Non usare tentativi falliti come checkpoint. |
| Si perde alla riconnessione? | Ogni chiamata della matrice usa un client MCP nuovo. Note presenti dopo tutte le riconnessioni. | È una prova del canale, non della memoria di un nuovo modello. |
| Si perde al riavvio del server? |12/12 confronti hanno log e observe identici prima/dopo riavvio del nostro server. | Stesso archivio di sessione; non una reinstallazione della submission o una migrazione di macchina. |
| Quanto indietro resta? | Note ancora presenti fino a43 azioni successive nella matrice, carriere giunte ai mesi6–12. Recuperate inoltre200/200 note storiche registrate in una carriera completa di48 mesi. | Non stabilisce un TTL universale in ore/giorni. |
| `count=N` conta scelte? | Conta voci di log.287/287 richieste restituiscono il suffisso cronologico atteso; `count=0` si comporta come1 nei campioni. | Stipendi, warning, review e fine gioco occupano voci. |
| Basta `count=1`? | Nei29 checkpoint con note presenti: ultima nota recuperata16 volte con1,22 con2,29 con5 o10. |5 non è una garanzia generale; è una frequenza su questi checkpoint. |
| Le partite si contaminano? | Nessun marker estraneo nei12 server isolati; nei2 prefissi sullo stesso server ogni sessione restituisce il proprio marker e nessuno dell'altra. | Il secondo test usa modalità sviluppo multi-sessione; non propone questa modalità per la gara. |

La matrice ha317 azioni accettate,0 rifiuti e0 errori tecnici. Le14 chiamate fallite del test di contratto sono **12 errori di tipo intenzionali +2 azioni invalide intenzionali**, separati dai guasti tecnici. Tutti i risultati negativi sono conservati. Le12 carriere della matrice terminano per il comportamento di un bot semplice: non misurano l'efficacia delle note sulla strategia, e non si attribuisce la morte al contenuto delle note.

Dati: [matrice](channel-v1/summary.json), [contratto](contract-v1/results.json), [recupero storico](historical-recovery-v1/recovery.json). Le note di prova sono marcatori neutrali sintetici: non suggeriscono risposte al gioco e non tentano di influenzare il valutatore.

## Ogni quanto si svuota la cache?

Non esiste un solo oggetto chiamato cache. Abbiamo separato quattro livelli:

1. **Archivio delle note nel gioco.** È ciò che ritorna da check_latest_logs. Nei test persiste dopo client e server nuovi; non abbiamo osservato un azzeramento periodico. Resta distinto dal testo che il modello sta effettivamente leggendo.
2. **Contesto di lavoro del modello.** Il framework può sostituire parti della conversazione con un checkpoint riassunto. Un fatto può rimanere nei log del gioco e scomparire dal contesto del modello. Una risposta errata non prova da sola una cancellazione: possono intervenire attenzione, priorità, ambiguità o riassunti sbagliati.
3. **Memoria su file del framework.** Non coincide con notes. Il runner ufficiale install_submission pulisce history, sessioni e file memory/*.md e ricrea MEMORY.md; questa è una cancellazione legata all'installazione, non a un intervallo di mesi del gioco. Lo abbiamo verificato nel codice del client ufficiale, senza eseguire installazioni sulla gara.
4. **Cache di inferenza/KV del provider.** Riguarda il riuso del calcolo. Non abbiamo ricevute di hit/miss o TTL della route Luna né della route organizzatore. I parametri del framework non identificano automaticamente il comportamento del provider.

### Framework esatto, distinto dalle impostazioni effettive della gara

Il runner locale è fissato a `00b084a88732d81e595db88b26dde90d44e72d87`. Dal suo uv.lock abbiamo scaricato **solo i client/framework** JiuwenSwarm0.2.4b3 e openJiuwen0.1.16.post2, verificando i SHA256 delle wheel. Nessuna installazione, nessuna credenziale caricata, nessuna ispezione del simulatore o del suo database. Versioni, hash e sorgenti pertinenti sono in [context-v1](context-v1/framework-trigger-audit.json).

I default confezionati del framework prevedono:

- Context engine attivo; compressori con `trigger_context_ratio=0.8`. Il metodo considera token di sistema, conversazione e tool, oppure una baseline di usage disponibile. La soglia non basta: serve un esecutore di compressione e una porzione comprimibile abbastanza grande. `min_target_context_ratio=0.1` indica qui il minimo della porzione da comprimere; **non promette che il contesto finale diventi il10%**.
- Per current-round e round-level, configurazione Jiuwen con4 messaggi recenti protetti; il codice allarga la coda quando serve a preservare coppie tool-call/tool-result.4 messaggi non significa4 decisioni o4 mesi.
- Offload di un singolo tool-result oltre il10% del budget di contesto. Il testo può essere spostato/ridotto separatamente dalla compressione dell'intera conversazione.
- Regola TTL:300 secondi **dall'ultimo accesso alla finestra di contesto**, occupazione almeno50%, poi elaborazione dei tool-result eleggibili oltre5% del budget. Ogni accesso aggiorna il riferimento temporale. Non è un timer che cancella tutto ogni5 minuti e non è il TTL delle note del gioco.
- Il preset SessionMemoryCompressor è disattivato; `auto_memory_enabled` del prodotto è false; affinità/rilascio KV sono false nella configurazione confezionata. Sono sistemi distinti, non una promessa di apprendimento automatico delle note.
- La sezione identity viene ricostruita dal workspace prima delle chiamate modello. Il codice del runner documenta la sua persistenza attraverso la compressione; ciò non garantisce che ogni nota o l'intero corpo di ogni Skill sia sempre nel prompt.

Abbiamo eseguito **37 test sulle funzioni reali estratte dal framework**, con contesti sintetici: appena sotto/sopra soglia, esecutore assente, porzione assente, inattività299/300/301 secondi, occupazione499/500 su budget1.000 e accessi successivi. A200,400 e600 secondi di attività non si attiva la regola di inattività; al successivo accesso900 sì, a occupazione sufficiente. Questo verifica le condizioni del codice, **non una compressione reale con riassunto generato da un modello**.

Per sapere dopo quante scelte avviene in una carriera reale occorrono finestra effettivamente risolta, configurazione in uso e traccia delle compressioni. Non si può convertirla in “ogni N mesi”: lunghezza di observe, note, log, ragionamento e risposte varia. La documentazione pubblica del framework distingue anch'essa [compressione del contesto e affinità KV](https://github.com/openJiuwen-ai/jiuwenswarm/blob/develop/docs/en/Configuration.md); le conclusioni numeriche qui vengono dalle versioni fissate, non dal ramo develop.

## Cosa impara davvero?

La funzione notes registra il testo che l'agente invia; questi esperimenti non mostrano un addestramento dei pesi né un aggiornamento automatico della strategia. Per parlare di apprendimento operativo servono tre prove distinte:

1. **Disponibilità:** il fatto corretto è stato scritto e può essere recuperato? La matrice misura questo livello.
2. **Ricordo corretto:** dopo distanza, riassunto o reset, il modello sa distinguere fatto osservato, ipotesi, impegno aperto e impegno risolto? Serve una prova del modello.
3. **Uso corretto:** a parità di situazione pubblica la memoria cambia opportunamente la scelta? Serve distinguere l'effetto della memoria da quello di priorità del manuale, eventi casuali e modello.

Luna offre testimoni di entrambi i tipi: ricorda una correzione di sicurezza lasciata aperta e debolezza della review; non aggiorna sempre il beneficio degli investimenti. Sono esempi post-hoc, non tassi generali di ricordo o causalità. Il recupero storico riguarda un'altra carriera Haiku:201 note inviate,200 restituite esattamente, nessuna richiesta di log da parte del giocatore. Nell'archivio non compare compact_boundary; non prova che il backend non abbia trasformato il contesto. Non si combinano Haiku e Luna in una stima di efficacia.

Conservare la spiegazione di una scelta può anche consolidare un errore. Per questo i record utili devono indicare fonte/tempo, risultato osservato, aspettativa ancora da verificare e condizione di revisione. La memoria deve poter correggere una precedente convinzione. I risultati di una singola azione non identificano da soli un effetto causale generale.

## Prossima fase cognitiva: protocollo pronto, non eseguito

Il protocollo dettagliato è in [cognitive-benchmark.md](cognitive-benchmark.md). Prevede48 prefissi pubblici etichettati, quattro condizioni di accesso alla memoria e tre ripetizioni:576 decisioni per modello, con scoperta e verifica separate. Misura fatti ricordati e aggiornati, resistenza a note obsolete, recupero dopo perdita del contesto, scelte e costo reale. La fase richiede quota del modello: i bot senza IA non possono misurare cosa ricorda Luna o DeepSeek. Non è stata lanciata e non abbiamo trasformato una prova di storage in una pretesa di apprendimento.

Le regole pratiche candidate derivanti dal canale sono: mantenere la nota sotto il limite con margine; mettere fatti decisivi e problemi aperti all'inizio; riportare risultato precedente ed aspettativa corrente separatamente; verificare il record realmente restituito; dopo perdita del contesto usare observe e recuperare progressivamente i log finché si trova un checkpoint identificabile. Continuare a distinguere osservazione fresca, storico e ipotesi. Nessuna Skill congelata è stata modificata o promossa a campione.

## Relevo — aggiornamento dopo l'indagine

Completati i test meccanici su14 nuove sessioni, più lettura di una carriera storica, e37 test delle condizioni del client-framework. Origine isolata matteonotes; nessuna scrittura nel registro cloud, quota modello o automazione. Le12 carriere della matrice sono terminate; i2 prefissi di contratto restano incompleti sul loro archivio dedicato ma senza processi attivi. I loro esiti non vanno inclusi in studi di promozione. Il codice congelato del test di contratto è in contract-v1/sources; lo script corrente ha solo semplificato il calcolo della stessa uguaglianza di stato, senza nuove esecuzioni.

Riprodurre **offline**: `scripts/analyze_action_notes.py ROOT_DATI lab/reports/action-notes-study/channel-v1`; `scripts/audit_note_context.py ROOT_FRAMEWORK lab/reports/action-notes-study/context-v1`. I sorgenti del framework pertinenti sono conservati; le wheel esterne e il loro download restano fuori dal repo. I comandi prepare/run dei probe generano nuove sessioni: non fanno parte della riproduzione offline. Per il recupero storico usare una nuova cartella di output e soltanto le API pubbliche.

Prossimo passo: costruire e verificare il set di fatti per il benchmark cognitivo, poi eseguirlo sullo stesso modello e ambiente da confrontare. Restano sconosciuti: TTL/hit rate effettivi del provider, override dell'organizzatore, qualità di riassunto e recupero di Luna/DeepSeek sotto perdita controllata del contesto, effetto causale delle note sulle promozioni. Il report non dichiara una copertura universale.


Validazione:287 test software passati, warning Authlib preesistente; protocolli e hash verificati, audit del contratto e suffissi dei log controllati. Commit/push sulla branch matteo-t4-growth e richiesta di merge tramite PR#12.
