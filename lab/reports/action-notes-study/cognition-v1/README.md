# Luna: disponibilità, recupero e uso dei fatti

27 ottobre 2026. **Completate 576 decisioni offline su 48 prefissi di 48 carriere diverse**, quattro condizioni e tre ripetizioni. 107 richieste di recupero portano il totale a **683 chiamate Luna**, senza errori tecnici, uso di tool o arresti per quota. Nessuna partita nuova, azione del gioco o API pagata. Modello richiesto `gpt-6-luna`, reasoning low, accesso ChatGPT tramite Codex CLI 0.163.0-alpha.11.1. Non è il runner Jiuwen della gara né il precedente attore nativo della partita Luna.

## Risultato principale e correttezza delle risposte

I 42 casi con fatto noto producono 126 risposte per condizione. I sei casi di informazione nascosta non identificabile producono altre 18 risposte, riportate separatamente.

| Informazione fornita | Risposta esatta al fatto noto | Risposta esatta + supporto valido, criterio fissato |
|---|---:|---:|
| Solo observe corrente | 18/126 (14,3%) | 18/126 (14,3%) |
| Storia pubblica completa | 71/126 (56,3%) | 59/126 (46,8%) |
| Checkpoint corretto curato | 119/126 (94,4%) | 42/126 (33,3%) |
| Checkpoint vecchio + recupero richiesto | 92/126 (73,0%) | 88/126 (69,8%) |

**Il checkpoint curato non supera il confronto principale fissato**, che esige anche una citazione valida. Molte risposte citano gli ID originali elencati nella provenienza del checkpoint, invece del record CHECKPOINT realmente fornito al modello. Il conteggio stretto registra 87 risposte con citazioni non ammesse in questa condizione, anche quando il contenuto è corretto. Non li presentiamo come 87 fatti dimenticati. La differenza primaria checkpoint−storia è −13,49 punti percentuali, intervallo esplorativo bootstrap per famiglia [−34,15; +3,70]. Nessun nuovo campione adottato.

Esiste però un segnale netto di accessibilità dell'informazione: molte più risposte hanno il contenuto giusto con un fatto compatto e pertinente. Per separarlo dagli errori di formato/provenienza, abbiamo aggiunto una diagnostica **post-hoc**, mantenendo invariati i risultati principali. Riconosce una risposta che comincia con Yes/No e segue con una spiegazione, normalizza gli interi e risolve soltanto ID di provenienza esplicitamente presenti nel checkpoint. Non corregge risposte sbagliate usando il gold o il testo della nota.

| Condizione | Contenuto corretto dopo sola normalizzazione del formato | Con supporto dopo normalizzazione e risoluzione della provenienza |
|---|---:|---:|
| Solo corrente | 18/126 | 18/126 |
| Storia completa | 95/126 | 81/126 |
| Checkpoint curato | 120/126 | 120/126 |
| Recupero | 97/126 | 93/126 |

Questa analisi spiega una parte degli errori di interfaccia, **non è una conferma indipendente** del checkpoint. Il prossimo confronto deve chiarire il contratto delle citazioni prima del gioco e usare casi nuovi. I checkpoint di questa prova sono curati da noi per contenere il fatto pertinente: non dimostrano che un agente sappia selezionarlo e scriverlo autonomamente.

## Quali dinamiche si vedono

- **Informazione assente:** nella condizione solo corrente, tutte le 144 risposte rispettano il criterio di calibrazione del test. Il modello usa correttamente la salute corrente e si astiene sulle informazioni storiche non fornite. Tutte le condizioni rispondono unknown in 18/18 prove sui parametri nascosti. Questo non è una prova di assenza di allucinazioni in generale.
- **Informazione fresca contro nota vecchia:** Health corretto in 18/18 prove per ciascuna condizione, anche con un valore vecchio realmente osservato in passato. In questi casi non si osserva obbedienza cieca al vecchio numero.
- **Review:** 18/18 risposte esatte con storia, checkpoint o recupero. Il test contiene solo gradi C e B; non copre ogni tipo di feedback o piano di recupero.
- **Beneficio osservato contro bonus nominale:** 17/18 risposte esatte con checkpoint, 3/18 con storia completa e 4/18 dopo recupero, prima della diagnostica del formato. In alcune risposte il modello riporta il bonus annunciato pur avendo calcolato correttamente nella nota un delta osservato nullo. Tutti i sei casi selezionati hanno delta zero: non è una stima di accuratezza per ogni possibile rendimento.
- **Rischio storico contro avviso corrente:** alcuni errori scambiano avvisi HR su rischi futuri per un evento ufficiale Old landmines già avvenuto. Sono due tipi di informazione diversi. Un messaggio attuale calmo non annulla un incidente passato; un avviso severo non prova che l'incidente sia già successo.
- **Aperto contro completato:** promessa di credito, disponibilità a fare qualcosa e completamento verificato vanno distinti. Alcuni unknown riflettono anche la diversa interpretazione di “non è stato riportato” rispetto a “non è successo”. Le domande semantiche del set riguardano ciò che era esplicito nella descrizione storica, non lo stato attuale di ogni impegno.
- **Risposta contro nota:** cinque testimoni selezionati mostrano il fatto pertinente corretto nella nota ma una risposta incompatibile nel campo answer. Non è un tasso globale di contraddizione. È evidenza che almeno quegli errori non si possono spiegare semplicemente con la scomparsa di quel fatto dal contesto.

Esempi verificabili in `posthoc-error-diagnostics.json`: posizione25, risposta yes mentre la nota dice nessun secondo incidente; posizione31, risposta unknown mentre la nota registra Network 3→3, delta0; posizione47, risposta +1 mentre la nota registra delta0; posizioni311 e 422, unknown nonostante conteggio zero/delta zero nella nota. Le posizioni si riferiscono alla schedule congelata.

Il recupero viene richiesto in 107/144 prove della condizione vecchio checkpoint. Prima del recupero il modello è calibrato in 143/144 risposte, con una risposta non sostenuta dalle informazioni disponibili. Dopo il recupero il criterio stretto supera la storia completa di +23,02 punti, intervallo esplorativo [11,31; 37,93]. Questa è una procedura con una chiamata aggiuntiva e il precedente tentativo nel prompt, non un confronto a pari lavoro o una vittoria della memoria sulla storia.

Tutte le 576 scelte sono legalmente offerte e tutte le 576 note finali sono non vuote e nei 800 caratteri richiesti. Rispetto a solo corrente, la scelta cambia in 27/144 prove con storia, 13/144 con checkpoint e 29/144 con recupero. Non abbiamo una scelta ottima certificata: variazione e legalità non provano maggiore qualità, sopravvivenza o promozione.

## Follow-up: note scritte dall’agente

La [prova writer→reader separata](../agent-written-v1/README.md) usa otto casi già visti, due budget e32 richieste, senza mostrare al writer la futura domanda. Con128 caratteri il writer rispetta il budget in0/8 casi; con800 in3/8. Il reader recupera2/8 risposte in entrambi i bracci: salute corrente e unknown, nessuno dei sei fatti storici. Alcuni fatti sono omessi o aggregati male; altri sono presenti ma privi di tipo/fonte/tempo sufficiente per la domanda. Non è una misura pura del budget o una conferma su casi indipendenti. Il checkpoint curato non rappresenta quindi la capacità di scrittura autonoma dimostrata da questo pilot.

## Token reali, cache e limiti del runtime

Input osservato: **14.308.667 token**, dei quali **8.373.120 cached input (58,5%)**. Output riportato: 85.467; reasoning output riportato separatamente: 329. Non sommiamo automaticamente contatori dalla semantica potenzialmente sovrapposta per ricavare una fattura. Nessuna ricevuta di spesa in valuta disponibile; zero stime in dollari.

| Condizione | Richieste | Input totale | Input medio per decisione principale |
|---|---:|---:|---:|
| Solo corrente | 144 | 2.127.363 | 14.773 |
| Storia completa | 144 | 4.326.405 | 30.044 |
| Checkpoint curato | 144 | 2.134.758 | 14.825 |
| Recupero | 251 | 5.720.141 | 39.723 |

Il checkpoint usa il 50,7% di input in meno della storia completa in questo harness. Non è un risparmio monetario misurato né il costo marginale della memoria nel runner target. Il prologo del client Codex pesa già circa 13–15k token nelle richieste brevi: i dati non sono trasferibili al costo di Jiuwen/DeepSeek. Il recupero aumenta il lavoro per decisione e va usato quando il checkpoint non basta.

La [documentazione ufficiale OpenAI sul prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) descrive il riuso del prefisso di input, distinto dalla generazione di una risposta nuova. Una cache hit non certifica che una storia assente sia entrata nel prompt e non è una misura di ricordo corretto.

Una [sonda separata di tre richieste](../cache-prefix-v1/audit.json) confronta un controllo corto e lo stesso prefisso sintetico unico prima/dopo almeno 300 secondi. Prima: 22.617 input,13.056 cached. Dopo300,004 secondi: 22.065 input,11.008 cached. L'hash del prompt fornito è identico, ma l'input totale riportato cambia: non controlliamo l'intero contesto renderizzato lato servizio. Si osserva ancora cache parziale; **non si identifica la scadenza del prefisso unico né si separano scadenza, routing e cambiamenti del prefisso implicito**. Nessuna prova che la cache si azzeri completamente ogni cinque minuti, nessuna garanzia che il prefisso unico sia stato riusato integralmente.

Il preflight è una richiesta separata. Prima del follow-up: 687 richieste (683 benchmark, 3 cache, 1 preflight). Con le 32 richieste writer→reader, il totale finale è **719 richieste**, input complessivo **15.037.662**, sotto i tetti annunciati di 24M input e 720 richieste. Il benchmark non forza compressioni naturali o ripetute: non misura il punto di cancellazione dei fatti dentro Jiuwen né il TTL della route organizzatore.

## Metodo, artefatti e limiti

`protocol.json`, `scoring-frozen.json`, Skill e schedule sono congelati prima delle risposte del benchmark. Il dataset ha48 carriere diverse; sviluppo/conferma24+24 sono separati per famiglia del fatto interrogato. La composizione delle categorie cambia fra le due metà: review/rischio storico sono solo in sviluppo, salute contro nota vecchia solo in conferma. Non si dichiara una replica confermativa di ogni categoria. Nessuna regola è stata adattata ai risultati di sviluppo durante la schedule.

Un secondo passaggio ricostruisce i fatti e i confini temporali da archivi pubblici. Non è una revisione di un secondo annotatore umano cieco. Le risposte non ricevono gold, categorie, esiti futuri, pacchetti del simulatore o lookup empirici. Ogni richiesta usa un processo CLI effimero e un thread distinto; gli hash di tutti i prompt sono verificati e la storia viene fornita soltanto nelle condizioni previste. Il recupero è una consegna simulata del prefisso dopo richiesta strutturata, non una chiamata MCP nativa del modello.

`public-benchmark.jsonl.gz` contiene protocollo, Skill,48 prefissi pubblici, risposte e usage; `archive-sha256.txt` ne verifica l'integrità. I native events archiviati non contengono ragionamenti privati del modello. `independent-audit.json` verifica683 thread distinti,683 hash dei prompt,683 usage e 576 assegnazioni uniche. `summary.json` e `scored-responses.json` conservano risultati e denominatori; `posthoc-error-diagnostics.json` conserva la diagnostica separata. Il modello è quello richiesto al CLI; non abbiamo una ricevuta indipendente di risoluzione del backend.

Le tre repliche dello stesso prefisso sono correlate: 126 risposte note per condizione non sono126 carriere indipendenti. Gli intervalli esplorativi ricampionano24 famiglie dei42 casi noti, senza correzione per confronti multipli; il set è selezionato intenzionalmente, non un campione casuale di ogni scenario. Non si inferiscono cambiamenti dei pesi, apprendimento fra partite o una regola universale di promozione.

## Relevo

Esecuzione terminata, nessun worker o server di questa prova da riprendere. Origine dati `/Users/matteozabban/careerlab-data/matteo-notes-cognitive/benchmark-v1d`; sonda cache nella directory sorella cache-prefix-v1. Il confronto Haiku sospeso, gara cloud e bundle congelati restano invariati. Le tre preparazioni precedenti del builder non hanno avviato prove modello; solo il set v1d ha ricevuto la schedule. Protocollo del benchmark e runner non modificati dopo il lancio.

Riprodurre l'audit del risultato senza modelli: `.venv/bin/python scripts/audit_note_cognitive_results.py lab/reports/action-notes-study/cognition-v1`. La diagnostica post-hoc si riproduce con `scripts/diagnose_note_cognitive_errors.py` sulla stessa cartella. Ricalcolare l'analisi completa dalla directory dati esterna con `scripts/analyze_note_cognitive_benchmark.py`. Non rilanciare il runner sui dati esistenti e non trattare un recupero come una seconda partita.

Prossimo passo concreto: correggere e verificare il contratto dei checkpoint scritti dall’agente — tipo/fonte/tempo, payoff della singola azione, limite macchina della lunghezza e coerenza fra nota e risposta — su casi nuovi. Poi stress di compressione/ripresa reale nello stesso runtime di destinazione; soltanto dopo valutare promozioni in carriere complete. Nessuna adozione automatica della variante curata o garanzia di promozione. Commit/push nella branch Matteo e richiesta di merge su PR12.

Validazione finale: **300 test software passati**, con il warning Authlib preesistente. Hash dei prompt, archive e protocolli verificati; nessuna chiamata modello usata per i test software.
