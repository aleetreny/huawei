# Singolo pilot Luna con memoria — completato

27 ottobre 2026. Matteo ha autorizzato espressamente **GPT-6 Luna + manuale campione di Ale**, con la sola aggiunta di memoria. Una partita completata fino all'eliminazione, nessuna sostituzione o partita aggiuntiva.

## Risultato

- **Q25,76/100**, eliminazione al mese24 per valutazioni deboli ripetute; nessuna promozione, livello finaleL1.
- 93 azioni, nessuna rifiutata. Review osservate: C, C, C, D.
- Stato finale: Health8, Dignity5, Skill9, Network2, Output0, Wealth10 visualizzato; il report finale riporta ricchezza10,2.
- Tutte le93 note iniziano con `Memory:`;32.515 caratteri totali, mediana370, massimo496,4.709 parole. Questi conteggi **non sono token del modello né un costo fatturato**.
- Nessun contatore per-token/per-valuta è esposto dall'interfaccia di collaborazione usata. Non attribuire un prezzo, un risparmio o un consumo di cache stimato a questo pilot.

La memoria testuale è stata prodotta, ma la corretta esecuzione del ciclo rimane parziale. Il modello ricorda la debolezza indicata dalle review e mantiene il problema di sicurezza aperto fino al suo ritorno. All'inizio, dopo investimenti eseguiti, continua invece a scrivere “no investments” e non registra sistematicamente il beneficio visibile. Sette preparazioni dei materiali, quattro senza incremento visibile di Output; nei primi esempi il modello ripete l'investimento senza aggiornare il registro del beneficio.

Le sette scelte principali trimestrali sono: un progetto, due report al manager e quattro Lay low. Ciò descrive una carriera difensiva e stagnante; non dimostra che una diversa scelta avrebbe promosso o che la memoria abbia causato la sconfitta. La politica del padre dà priorità al rischio rispetto alla review, e gli eventi raggiunti cambiano i costi.

## Esecuzione e isolamento

Candidato `lab/policies-src/matteo-memory/champion-memory-v1`, copia del campione `targeted-1026-201334` da cloud `26e976f` con una sezione aggiunta. Tutto il testo del padre è preservato byte per byte. Hash del bundle congelato prima del gioco: `d5d71bb2af09a8db48970eae830dfd8f6dde8e16e6795cc97fc7b983fa33a6b4`.

Attore nativo richiesto `gpt-6-luna`, task `/root/luna_memory_player`, contesto iniziale nuovo. Al modello sono forniti solo Skill congelata, istruzioni del trasporto e strumenti pubblici della sua partita. Nessun lookup empirico, risultato storico o consiglio dell'analista durante il gioco. Il ruolo del padre è preparare il trasporto, leggere lo stato per aggiornare Matteo e analizzare dopo la fine. Il task nativo ha strumenti generali: il vincolo MCP-only è istruttivo, non una sandbox tecnica certificata; non pretendiamo una ricevuta separata del routing backend.

Il bridge locale espone i cinque strumenti pubblici, impedisce un secondo tentativo new_game, registra richieste e risposte e restituisce una nuova observe dopo ogni take_action. È un harness diverso da Claude CLI e JiuwenSwarm/DeepSeek. Non si confrontano causalmente Q25,76 con il picco personale70,94 o la media del campione di Ale.

Una sola new_game; una chiamata handbook;93 take_action;94 observe automatiche; un recupero finale dei log per l'archivio. Luna non ha richiesto log aggiuntivi. Nessun reset del contesto forzato: il recupero della memoria dopo una ripartenza non è stato verificato. Nessun messaggio ufficiale Old landmines nella partita; l'incidente di sicurezza della storia è un fatto diverso. Il server dedicato e il task del giocatore sono terminati.

## Dati e audit

`luna-v1/` contiene protocollo e hash, copia congelata del bundle, configurazione di lancio, richieste/risposte pubbliche, archivio compresso con hash, risultato, summary, tutte le note e audit con testimoni. Non contiene pacchetto o database del simulatore, né ragionamenti privati del modello. Gli outcome sono ricostruiti da ending_score e stato pubblico; le azioni offerte e l'unicità della nuova partita sono verificate.

Audit semantico **post-hoc, non cieco**, con esempi di memoria mantenuta e di beneficio non registrato. La presenza del prefisso Memory non è una misura di correttezza globale; un guadagno visibile nullo non prova l'assenza di benefici indiretti.

## Relevo

Completato un solo pilot autorizzato; risultato negativo conservato. Origine `matteoluna`, dati esterni `/Users/matteozabban/careerlab-data/matteo-luna-memory/pilot-v1`. Nessuna modifica durante la partita a protocollo, bundle o trasporto. Nessuna partita nuova da avviare o sessione da riprendere. Nessun uso di Haiku, riavvio della gara cloud o modifica al confronto Haiku4+4 sospeso. Nessuna evidenza causale dell'effetto della memoria e nessuna promozione a nuovo campione.

Prossimo problema proposto da Matteo: studiare separatamente la funzione notes, distinguendo memoria dell'agente ed eventuale effetto diretto del testo sul gioco. Piano preparato in `../action-notes-study/README.md`; nessun nuovo esperimento avviato.

Validazione: lint del candidato senza rilievi su129 titoli;287 test software passati prima del termine; analisi e audit eseguiti sui dati reali. Verifica software finale completata: 287 test passati, un warning Authlib già presente. Tutti i dati, script e Relevo vanno nella nostra branch e PR#12.

Riprodurre senza chiamare il gioco:

```sh
.venv/bin/python scripts/analyze_native_memory_pilot.py /Users/matteozabban/careerlab-data/matteo-luna-memory/pilot-v1 lab/reports/memory-pilot/luna-v1
.venv/bin/python scripts/audit_native_memory_notes.py lab/reports/memory-pilot/luna-v1
```

Non rilanciare prepare o new_game sul pilot esistente e non modificare il bundle congelato.
