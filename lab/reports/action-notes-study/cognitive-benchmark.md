# Benchmark cognitivo delle note — proposta iniziale

**Aggiornamento:** dopo “bene vai avanti” è stato congelato ed eseguito il benchmark v1:576 decisioni Luna,107 recuperi,683 richieste. [Risultati, protocollo operativo e limiti](cognition-v1/README.md). Il testo seguente conserva la proposta precedente; non descrive più lo stato di esecuzione.

Obiettivo: misurare se il modello recupera fatti corretti e li usa, separando conservazione, ricordo, aggiornamento e decisione. Il benchmark non è stato eseguito; non è una nuova versione del manuale o una prova di promozione. Zero nuove chiamate modello in questa indagine meccanica.

## Campione e risposte verificabili

48 prefissi pubblici,6 per categoria: conseguenza ritardata; impegno aperto; impegno risolto esplicitamente; avviso attuale assente dopo incidente storico; investimento con risultato diverso dall'atteso; aggiornamento di review; nuovo fatto che smentisce una nota precedente; assenza di informazione sufficiente. Usare più carriere e famiglie di eventi; l'ultima categoria deve premiare la risposta unknown. Ogni fatto viene etichettato con il tool-result pubblico che lo supporta e la prima decisione alla quale era disponibile. Nessun finale futuro, soglia nascosta o conoscenza del simulatore nell'etichetta o nel prompt.

Il set richiede due passaggi separati: annotazione e controllo delle fonti. Non considerare una statistica piatta come prova di inutilità causale; non considerare risolto un problema per la sola scomparsa di un warning. Raggruppare per carriera e famiglia: prefissi dello stesso episodio non sono repliche indipendenti. Separare24 casi di sviluppo e24 di conferma per gruppi, prima dei risultati modello. La sufficienza del numero48 è da valutare rispetto all'incertezza; non garantisce potenza statistica.

## Quattro condizioni, stesso prefisso e modello

1. Stato pubblico corrente senza storia: riferimento per quanta informazione è già in observe.
2. Storia pubblica completa del prefisso: riferimento di accessibilità, non oracolo di buona decisione.
3. Stato + ultimo checkpoint corretto e compatto: condizione primaria di memoria esplicita.
4. Stato + checkpoint precedente non aggiornato + log recuperabili: misura rilevazione di obsolescenza e recupero.

Tre ripetizioni per prefisso/condizione, ordine casuale congelato:576 decisioni per modello. Ogni prova parte con contesto indipendente; stesso manuale, tool, modello esatto e impostazioni. Ogni risposta contiene solo fatti strutturati, fonti pubbliche, stato aperto/chiuso/unknown, scelta offerta e nota aggiornata: non si richiede catena di pensiero privata. Non chiamare take_action per dare un esito inventato al prefisso: una scelta offline non è un replay controfattuale del gioco.

Prima misurare estrazione e uso delle informazioni. La qualità strategica di una scelta richiede una rubric motivata da manuale/pubblico, non l'azione del giocatore storico come verità assoluta. Registrare separatamente fatti corretti e accordo con quella rubric.

## Stress test da fissare dopo il campione di sviluppo

- Distanza del fatto1/5/20/50 azioni, riportando cosa il prefisso rende possibile senza inventare una griglia completa.
- Budget della nota100/300/800 caratteri; stessa informazione essenziale dove entra, annotare esplicitamente quando il budget impedisce di includerla. Conservazione e posizione del fatto sono interventi distinti.
- Nessuna compressione, compressione naturale nel client ufficiale, ripresa con solo session_id. Per una prova controllata della soglia, occupazione misurata sotto/sopra il trigger con contenuto sintetico neutrale; non cambiare la configurazione della valutazione ufficiale. Il test forzato va etichettato come harness di ricerca.
- Compressione ripetuta: misurare il fatto prima/dopo ogni riassunto e conservare hash dei messaggi effettivamente rimandati al modello. Non confondere cancellazione dal prompt con irreperibilità dal log.
- Inattività sotto/sopra300 secondi con occupazione bassa/alta, se il runtime è quello fissato. Osservare gli eventi reali; non dedurre un offload dalla sola latenza.
- Note obsolete che possono essere corrette soltanto dal nuovo tool-result; nessuna istruzione ostile o tentativo di manipolare il valutatore.

La griglia completa sarebbe molto più grande del benchmark primario. Scegliere sul set di sviluppo poche condizioni di stress, fissare quelle di conferma, budget e arresto prima delle chiamate. Non chiamare100% una ricerca finita.

## Misure e telemetria

Recall/precisione dei fatti con denominatori espliciti; false risoluzioni, fatti inventati, aspettative presentate come risultati, adesione a note smentite, capacità di dire unknown. Errori ripetuti e scelta coerente con il fatto rilevante. Numero di log richiesti, record restituiti, lunghezza di note e prompt, token effettivi input/output/cache se esposti, costo fatturato se esposto, ritardi, rifiuti e fallimenti tecnici. Non convertire caratteri in contatori fatturati.

Per ogni compressione: tempo monotono, sessione, modello e configurazione effettivi, budget risolto, occupancy prima/dopo, conteggio messaggi, hash/identificatori dei fatti presenti prima/dopo, evento di compressione/offload e record di usage. Il fatto perso dal riassunto ma recuperabile nel log ha un'etichetta distinta dal fatto inventato o mai salvato. Una cache miss senza cambiamento del testo disponibile non viene etichettata come dimenticanza.

Confronti appaiati per prefisso ma incertezza raggruppata per carriera/famiglia; non aggregare modelli o harness diversi. Nessuna promozione di una variante dal solo Q di una carriera o da576 richieste correlate. Solo dopo un vantaggio replicato di correttezza/decisione passare a carriere complete randomizzate con promozione e sopravvivenza, e relativo budget fissato prima del gioco.

## Relevo

Protocollo proposto, non eseguito o implicitamente autorizzato come spesa API. Prima dell'esecuzione servono dataset etichettato, ambiente/modello scelto, configurazione effettiva verificata e tetto di consumo. L'indagine corrente ha eseguito soltanto prove senza modelli ed esame del client/framework fissato. Non ha acceso Jiuwen, caricato credenziali o riavviato il confronto Haiku sospeso.
