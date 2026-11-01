# Due partite Luna: t13-read-v4 con il solo nuovo ciclo di chiamate

**Completate il 29 ottobre 2026: 32,26 e64,90; media48,58; una carriera su due completata.** Il ciclo di esecuzione viene seguito, ma queste due prove non dimostrano un miglioramento di gioco e non misurano l'efficienza token del runner ufficiale.

## Esperimento richiesto

Matteo ha chiesto espressamente due partite con Luna e aggiornamenti ogni tre mesi di gioco. Due giocatori nativi richiesti `gpt-6-luna`, ciascuno con contesto iniziale nuovo e una sola sessione MCP isolata, hanno giocato fino all'esito pubblico. Nessuna sostituzione dopo una sconfitta. Un solo intervento di coordinamento ha ricordato il momento dei checkpoint; nessun consiglio strategico o lookup empirico è stato fornito ai giocatori.

Padre: t13-read-v4, commit09d5735, bundle f78c8b8834082a8c. La sola modifica è la sezione Turn loop più un prefisso esecutivo nel manifest e il nome del pilot. Tutto il testo da `## Status line` alla fine, incluse storie, priorità trimestrali e memoria originale, è identico byte per byte al padre. Il ciclo accoppia esplicitamente take_action e observe; nel primo trimestre osserva entrambi i menu prima di riutilizzarli nelle successive chiamate trimestrali. Controlli ed errori ammettono osservazioni separate. Il trasporto non inserisce observe al posto del giocatore.

Bundle congelato: `e96e8843edf70c132e8d1a6ede54fc05ac4991a53a6ebb31e9004d6cee33e31d`. Protocollo/hash, lancio e copia del bundle sono in questa cartella. Il linter passa con6 REVIEW ereditati o equivalenti ai richiami del padre, zero errori; non è una certificazione di fair play.

## Risultati

| Partita | Esito | Mesi sopravvissuti | Livello finale | Q | Azioni rifiutate |
|---|---|---:|---|---:|---:|
|1 | Licenziata per seconda valutazione debole |24 |L2 |32,26 |0 |
|2 | Completata |48 |L5 |64,90 |0 |

**Partita1:** valutazioni C,C,D,C ai mesi6,12,18,24. Prima promozione L1→L2 al mese24, seguita nello stesso avanzamento dal licenziamento. Skill9, Network2, Output3, salute10, dignità7, Wealth8,2 al termine. Nessun messaggio pubblico di esplosione. Il blocco iniziale non è risolto dal nuovo ciclo.

**Partita2:** promozioni nei mesi12,18,30,42 (L2,L3,L4,L5), voti C,C,B,B,B,B,B,B. Un messaggio pubblico di esplosione al mese15. Chiude con Skill115, Network54, Output29, salute10, dignità10, Wealth26,1. La dimensione finale di controllo del rischio vale5/10, contro10/10 massimi: a parità degli altri termini mancano5 punti, ma non è un controfattuale causale sulla traiettoria senza esplosione. L5 arriva solo al mese42.

Il mese49 dell'osservazione finale è il normale stato dopo48 mesi liquidati; non è una carriera di49 mesi. I risultati usano `ending_score.survival_months`.

## Aggiornamenti trimestrali pubblici

Valori dopo il trimestre, normalmente nell'osservazione del mese successivo. I salari/eventi del nuovo mese possono già comparire. Il terminale del mese24 della prima partita precede il completamento del trimestre24; è riportato come esito finale sopra.

| Partita | Trimestre concluso | Livello | Salute | Skill | Network | Output |
|---|---:|---|---:|---:|---:|---:|
|1 |3 |L1 |6 |9 |3 |-1 |
|1 |6 |L1 |5 |9 |3 |3 |
|1 |9 |L1 |9 |9 |3 |1 |
|1 |12 |L1 |9 |9 |3 |3 |
|1 |15 |L1 |8 |9 |3 |3 |
|1 |18 |L1 |8 |9 |3 |3 |
|1 |21 |L1 |9 |9 |3 |3 |
|2 |3 |L1 |5 |8 |3 |2 |
|2 |6 |L1 |6 |9 |2 |0 |
|2 |9 |L1 |6 |9 |3 |3 |
|2 |12 |L2 |8 |11 |6 |6 |
|2 |15 |L2 |7 |19 |6 |5 |
|2 |18 |L3 |7 |27 |10 |10 |
|2 |21 |L3 |7 |39 |14 |12 |
|2 |24 |L3 |7 |42 |21 |16 |
|2 |27 |L3 |6 |42 |21 |16 |
|2 |30 |L4 |9 |46 |24 |18 |
|2 |33 |L4 |9 |56 |30 |21 |
|2 |36 |L4 |7 |69 |36 |26 |
|2 |39 |L4 |7 |80 |36 |26 |
|2 |42 |L5 |8 |95 |37 |28 |
|2 |45 |L5 |9 |106 |48 |27 |
|2 |48 |L5 |10 |115 |54 |29 |

Gli aggiornamenti richiesti sono stati inviati nella chat durante la partita. Alcuni checkpoint sono stati recuperati dal monitor anziché dal messaggio del giocatore; i mesi21 e24 della prima partita sono stati comunicati insieme. Una correzione nella chat chiarisce che la seconda partita ha mancato promozioni ai mesi6,24,36, non soltanto due volte.

## Verifica del trasporto e dell'aderenza

- Partita1: 95 take_action, 69/69 batch di storia con esattamente take_action→observe; note con tutti e5 i campi in 95/95 azioni; nota massima 101 caratteri;0 azioni rifiutate.
- Partita2: 197 take_action, 144/144 batch di storia con esattamente take_action→observe; note con tutti e5 i campi in 197/197 azioni; nota massima 211 caratteri;0 azioni rifiutate.

Verificati una sola new_game per sessione, esiti terminali pubblici, zero errori di trasporto registrati, note entro1000 caratteri, integrità delle traiettorie compresse e hash del bundle. Le chiamate sono state solo quelle dei cinque strumenti pubblici. I due server dedicati sono terminati e le porte risultano chiuse. Nessuna modifica al registro cloud, nessuna chiamata DeepSeek o chiave della competizione utilizzata. È stata consumata la quota dei modelli nativi dell'app, senza ricevuta separata di costo/token.

## Interpretazione e limiti

Il risultato positivo riguarda la capacità di Luna di eseguire le coppie di chiamate in questo trasporto. La sconfitta iniziale e il ritardo delle promozioni restano presenti. Non c'è controllo Luna-v4 senza loop né un confronto con cp-v12: non possiamo attribuire al ciclo la media48,58, né concludere che migliori o peggiori la strategia. Nessuna partita va esclusa.

Il trasporto nativo raggruppa richieste MCP da un task Luna, ma non è JiuwenSwarm0.2.4b3 con DeepSeek: non riproduce il suo contesto, routing o conteggio token. Non assegniamo quindi100 di efficienza né proiettiamo un voto di submission da queste due carriere. Per la decisione del cutoff serve ancora il confronto mirato sul modello designato. La configurazione richiesta `gpt-6-luna` è registrata dal lancio; non è disponibile una ricevuta indipendente del modello effettivamente risolto.

## Dati e riproduzione dell'analisi

- `game-1/`, `game-2/`: risultato pubblico, stato finale, checkpoint, summary e traiettoria pubblica compressa (solo chiamate/risposte e note, nessun ragionamento privato).
- `summary.json`: risultati combinati e metriche di aderenza.
- Dati operativi esterni: `/Users/matteozabban/careerlab-data/luna-v4-loop-20261029/`. Non copiare database o file interni del motore.
- Analisi senza nuove partite: `.venv/bin/python scripts/analyze_luna_v4_loop.py /Users/matteozabban/careerlab-data/luna-v4-loop-20261029 lab/reports/luna-v4-loop`.

## Relevo

Richiesta completata: esattamente due partite native Luna, nessun reset o rimpiazzo, aggiornamenti trimestrali, entrambi gli esiti conservati. Bundle e trasporto congelati prima della prima azione; gameplay di v4 immutato. Nessuna partita lasciata in corso e server terminati. Prossimo passo: integrare questo rapporto e i dati nella linea di valutazione esistente, senza presentare il pilot come prova di efficienza o superiorità DeepSeek. Non riavviare questi server né creare altre partite da questo protocollo concluso.
