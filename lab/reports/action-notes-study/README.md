# Studiare le note delle scelte — proposta

27 ottobre 2026. Matteo propone che la funzione per annotare sotto ogni scelta sia la chiave e chiede come esplorarla. **Piano soltanto: nessuna nuova partita o chiamata a un modello autorizzata da questa proposta.**

## Domande da separare

1. **Canale:** la nota viene salvata integralmente e può essere recuperata quando serve? Sono già verificate note brevi nei log pubblici. Restano da verificare lunghezze, caratteri, tipi di azione, count ridotto e recupero dopo reset. Continue non restituiva la nota nel testimone precedente: non assumere che ogni chiamata la conservi.
2. **Eventuale effetto diretto sul gioco:** sappiamo che le note compaiono nei log, non abbiamo dimostrato se il loro contenuto cambia transizioni o valutazione. Non assumere né che lo faccia né che sia sicuramente inerte.
3. **Effetto sull'agente:** l'annotazione corretta viene letta, aggiornata e usata per modificare opportunamente una decisione successiva? Questa è una domanda distinta dalla presenza di un registro.

## Prima fase: riusare i dati, senza quota di gioco

Il pilot Luna ha93 note con prefisso Memory; sette Prepare report materials, quattro con delta visibile di Output nullo. L'audit trova già un esempio: dopo il primo investimento il modello continua a scrivere “no investments” e ne ripete un altro senza registrare il payoff. Conserva invece debolezza della review e una correzione di sicurezza rimasta aperta.

Annotare le93 note usando esclusivamente informazioni disponibili prima della rispettiva azione: fatto ricordato corretto, fatto mancante, fatto superato, impegno aperto/chiuso con evidenza, risultato precedente osservato, aspettativa distinta da risultato, reazione alla mancata utilità. Separare gli errori di registrazione dalla scelta che il manuale prescrive. Un peggioramento o un mancato guadagno non è automaticamente un errore: possono esserci benefici indiretti o costi necessari.

Prima fissare questa scheda di lettura e poi estendere alle note del campione, senza usare il punteggio finale per etichettare una scelta. L'audit Luna già esistente è post-hoc: non ribattezzarlo cieco.

## Una nota verificabile, scritta prima della scelta

Formato candidato di informazioni pubbliche, non di ragionamento esteso:

`Previous observed result | Open issue + next step | Expected benefit now | Condition for reassessment`

La nota corrente può riportare il risultato della scelta **precedente**. Il risultato della scelta corrente non è ancora noto: si verifica nella successiva observe e si aggiorna nella nota successiva. Tenere separato lo storico degli incidenti seri dagli avvisi correnti; non scambiare messaggio calmo per risoluzione.

Esempio generale: “Previous: no visible delivery gain. Open: delivery gap. Expected: verifiable work evidence. Recheck: reconsider if no relevant benefit.” Non contiene risposte a eventi, soglie nascoste o un ordine di interrompere qualsiasi azione che non muove una statistica.

## Seconda fase: verifiche del canale e del testo con bot

Da autorizzare e congelare prima di nuove sessioni. Usare solo le cinque API pubbliche. Per il canale: note sintetiche non istruttive e di lunghezza crescente; verificare accettazione e restituzione senza leggere file interni. Non usare prompt injection, pretese sull'esito, comandi o tentativi di manipolare il valutatore.

Per l'effetto diretto del testo: assegnazione casuale prima della partita fra note neutrali e note fattuali; medesimo controller che ignora le note nel decidere, modelli e parametri congelati. Le partite sono indipendenti e non clonabili: “stesso controller” non significa che raggiungeranno le stesse domande o eseguiranno la stessa sequenza. Misurare transizioni pubbliche ed esiti, mantenendo morti iniziali e interruzioni nei denominatori previsti. Un risultato nullo su una raccolta finita non prova che il testo sia universalmente inerte; un'apparente differenza richiede replica e verifica degli errori.

## Terza fase: isolare l'effetto sul giocatore

Preparare un A/B con lo **stesso modello Luna e lo stesso padre**: note originali contro una sola variante del formato verificabile. Congelare istruzioni, budget delle note, strumenti, memoria disponibile e gestione del contesto. Nessuna simultanea modifica alle priorità di rischio, salute, review o crescita. Assegnazione intercalata prima di new_game; limite di spesa e numero di episodi fissati prima dei risultati. Una singola partita non misura l'effetto della memoria.

Prima delle carriere complete sono possibili prove di decisione su prefissi pubblici identici: ricordo di fatti, aspettative, prossima scelta. Usano comunque quota del modello e non sono replay di un esito né prova di sopravvivenza; non si eseguono senza una nuova autorizzazione.

Misurare: correttezza/aggiornamento delle note, errori ripetuti, conservazione degli impegni e degli incidenti, reazione agli investimenti senza utilità visibile, promozione e sopravvivenza, token reali e richieste di log. Non scegliere la nota vincente dalla lunghezza, dal prefisso Memory o da un singolo Q alto. Gli esiti delle prove usate per costruire il formato non sono conferma finale.

## Relevo

Preparata proposta a tre livelli dal nuovo incarico, collegata ai testimoni Luna. Non implementato o avviato un nuovo controller, A/B, reset, sessione, modello o automazione. Il precedente singolo pilot è finito: Q25,76, morte24, L1, dati in `../memory-pilot/luna-v1`. Prossimo passo concreto suggerito: scheda di lettura offline e classificazione delle93 note, poi scegliere una sola modifica verificabile. Questa proposta non dichiara che le note siano il driver nascosto delle promozioni.
