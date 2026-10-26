# Manuale di strategia e percorso di verifica

26 ottobre 2026. Richiesta di Matteo: salvare il manuale nella branch e decidere se studiare la seconda promozione oppure risolvere prima le incertezze sulla prima.

## Decisione

**Il manuale è pronto come candidato; la promozione alla prima review non è garantita.** Prima di aprire la ricerca sistematica sui mesi 7–12, verifichiamo applicazione e limiti della strategia nei primi sei mesi. L'obiettivo operativo è promozione **e** sopravvivenza, non il solo avviso di avanzamento.

Il manuale per l'agente è [promotion-readiness-v2](../../policies-src/matteo-first-review/promotion-readiness-v2/bundle/skills/promotion-readiness/SKILL.md). È in inglese e contiene un solo ciclo decisionale, senza titoli di eventi, risposte precostituite, soglie numeriche ricavate dal gioco o mesi prescritti. Non è ancora stato valutato con un agente. La versione v1 e il confronto 4+4 già congelato restano invariati.

## La strategia

1. **Osservare:** stato, feedback, avvisi, risultato dell'ultima azione e impegni ancora aperti.
2. **Diagnosticare:** identificare il limite attuale tra capacità tecnica, collaborazione, risultato riconosciuto, salute e problemi irrisolti.
3. **Agire:** scegliere un intervento sostenibile che affronti quel limite, specificandone il beneficio atteso e il costo accettabile.
4. **Verificare:** controllare il cambiamento effettivo; riorientare lo sforzo quando l'investimento non produce più il beneficio necessario.

In parallelo, tenere un registro minimo di promesse, difetti, rischi e conflitti: cosa resta aperto, chi deve agire e quale condizione richiede un seguito. Cercare risultati verificabili e attribuzione corretta del merito. Prepararsi prima della review, preservando salute e dignità anche dopo una promozione.

La priorità dipende dallo stato: un rischio urgente può venire prima della crescita. Non esiste ancora evidenza che un progetto, un mentore o una sequenza narrativa specifica siano obbligatori.

## Perché non dichiariamo il 100%

Il catalogo conosciuto copre 528/528 risposte pubbliche incontrate, non tutte le combinazioni di storie e stati. Nei sette archivi abbiamo 2.558 episodi risolti e 31 interruzioni tecniche; 1.940 transizioni di prima review osservate. La firma numerica post-review inizialmente perfetta ha già un controesempio nel campione ampliato. Inoltre il bot empirico consulta effetti appresi: il suo successo non misura l'efficacia del manuale per un agente.

Un numero finito di partite vinte non dimostra una garanzia universale. Per dimostrare il 100% servirebbe una caratterizzazione completa delle transizioni e di tutti gli stati raggiungibili, o una proprietà pubblicata che la implichi. L'interfaccia disponibile non offre clonazione dello stato, scelta del seme o enumerazione completa. Non leggiamo il simulatore per aggirare questo limite.

Possiamo invece cercare attivamente di falsificare la regola e misurarne l'affidabilità sotto condizioni dichiarate. Se emerge un ramo in cui nessuna azione disponibile salva l'obiettivo, occorre distinguere uno stato irrecuperabile causato da decisioni precedenti da una possibile sequenza inevitabile: nessuna delle due conclusioni segue da una singola sconfitta.

## Nuovo controllo: stati apparentemente uguali

Ho eseguito un audit offline di tutti i 1.940 passaggi di review, verificando gli hash dei sette archivi e confrontando **solo informazioni disponibili prima della risposta**. L'esito è il cambiamento di livello nella risposta immediatamente successiva, non un avanzamento successivo nella finestra.

| Descrizione usata per raggruppare | Gruppi distinti | Gruppi ripetuti | Gruppi con esiti diversi |
|---|---:|---:|---:|
| Solo Skill, Network, Output | 161 | 142 | 18 |
| Tutti gli indicatori dello stato | 1.291 | 162 | 61 |
| Tutti gli indicatori + scelta effettuata | 1.829 | 84 | 0 |
| Intera osservazione pubblica + scelta, escluso ID sessione | 1.829 | 84 | 0 |

Quindi gli indicatori, da soli, non determinano l'esito osservato. **Questo non dimostra una variabile nascosta:** nei gruppi discordanti possono differire l'evento, l'azione che precede la review e la storia. Quando fissiamo anche l'azione, le contraddizioni scompaiono nel campione, ma rimangono soltanto 84 gruppi ripetuti, per 195 osservazioni complessive. La maggioranza dei casi non ha un confronto ripetuto; non possiamo concludere che la storia sia irrilevante o che il modello sia deterministico.

Esempio verificabile: stesso stato pubblico completo prima della review in `factorial-v2/run12/step19` e `factorial-v2/run590/step19`, ma domande e azioni diverse; il primo promuove, il secondo no. Le risposte includono anche avvisi di rischio diversi. È una coppia utile per formulare ipotesi, non un confronto causale.

Tutti i gruppi discordanti, due testimoni per gruppo, gli hash e i limiti sono in [observability-audit.json](observability-audit.json). Non sono stati lanciati nuovi giochi o usati modelli.

## Metodo: falsificazione mirata e verifica dell'esecuzione

**Passo 1 — Separare regola e comportamento.** Il confronto v1 contro manuale precedente, quattro partite per braccio con lo stesso Haiku, è già congelato e non giocato. La ripresa resta manuale, come richiesto da Matteo. È un controllo preliminare, non una prova statistica di superiorità. Misurare promozione, sopravvivenza e applicazione delle istruzioni separatamente: diagnosi del limite, controllo del beneficio reale, gestione degli impegni e reazione agli avvisi. Ricostruire l'aderenza da azioni e osservazioni, senza pretendere di leggere il ragionamento interno. Per v2 serve un confronto distinto: non cambiare il testo nel test v1.

**Passo 2 — Cercare il caso che rompe la strategia.** Congelare una politica di ricerca e generare nuove storie indipendenti. Annotare ogni fallimento secondo tre classi: istruzione non applicata; istruzione applicata ma insufficiente; problema tecnico. Non eliminare le morti precedenti alla review. Cercare esposizioni diverse: scarsa salute, dignità in calo, rischio annunciato, crescita sbilanciata, contributi senza riconoscimento e impegni rimasti aperti. Sono condizioni da osservare nelle risposte pubbliche; il generatore non può imporle come stati iniziali.

**Passo 3 — Intervenire sul meccanismo, non sul titolo.** Per una causa candidata, usare un nuovo protocollo congelato prima dei risultati. Esempio concreto: al primo menu energetico eleggibile, assegnare casualmente tra due piani entrambi disponibili: un'azione di riduzione rischio contro un piano di uguale costo orientato alla crescita; mantenere identica la politica del resto dell'episodio. Registrare il piano completo, perché il confronto stima il pacchetto e il costo opportunità, non un effetto puro del rischio. Randomizzare prima della scelta, registrare lo stato e gli avvisi pre-intervento, non selezionare retrospettivamente i sopravvissuti. Confrontare tutti gli episodi assegnati e separare mancata eleggibilità, morte e interruzione tecnica. Gli strati devono dipendere solo da informazioni precedenti all'assegnazione. Non trattare le storie non identiche come cloni controfattuali.

Per la prima prova del meccanismo proponiamo 128 episodi eleggibili, assegnazione casuale indipendente 1:1, massimo 256 tentativi di nuova partita, senza arresto anticipato per un risultato favorevole. Politica, piani di pari costo, criteri di eleggibilità, semi dell'assegnazione, outcome e gestione delle interruzioni devono essere fissati in un protocollo nuovo prima del lancio. Il numero di campioni è un limite esplorativo, non una potenza garantita. Qui è definito il metodo; il nuovo runner di intervento non è implementato e questo esperimento non è stato avviato.

**Passo 4 — Verifica indipendente della versione finale.** Ogni correzione produce una nuova versione; i risultati usati per correggerla non sono il test finale. Su una versione congelata, 299 episodi indipendenti tutti riusciti darebbero un limite inferiore unilaterale al 95% di circa 99% per la probabilità di successo, assumendo episodi indipendenti e una distribuzione stabile. È una misura condizionata a modello, ambiente e distribuzione, non il 100%, né la garanzia per ogni agente. Il calcolo è `0.05 ** (1 / 299)`. Non si può cambiare manuale o scegliere quando fermarsi e conservare automaticamente questa interpretazione.

## Quando aprire i mesi 7–12

L'assenza di una garanzia matematica non deve bloccare per sempre la ricerca. La soglia di passaggio proposta è: un confronto di trasferimento completo, audit dell'aderenza, cause dei fallimenti documentate e una versione congelata per lo studio successivo. Questo è un criterio operativo, non una dichiarazione di certezza.

Per il blocco successivo proseguire gli stessi episodi tramite strumenti pubblici, conservando tutta la storia; non inventare un nuovo stato di partenza L2. Riportare sia l'esito complessivo dalla nuova partita sia l'esito condizionato a prima promozione e sopravvivenza. Distinguere seconda promozione entro il mese 12, promozione alla seconda review e sopravvivenza attraverso il mese 12. Verificare il confine effettivo della review osservandolo, senza assumere che tutte le regole del livello precedente restino valide. Le sconfitte nei primi sei mesi rimangono nel denominatore complessivo.

## Relevo

Creati il manuale v2, la documentazione di adozione e l'audit di osservabilità. Nessuna modifica alla v1 o al protocollo di trasferimento congelato; nessuna nuova simulazione, chiamata IA, automazione o scrittura nei registri cloud. La ricerca dei mesi 7–12 non è iniziata: resta da verificare il trasferimento della strategia e da congelare un eventuale esperimento mirato.

Validazione: lint del bundle v2 contro tutti gli 89 titoli conosciuti senza rilievi; **253 test passati**, incluso controllo dei gruppi discordanti, separazione delle azioni, esclusione di risposte ambigue/rifiutate e integrità degli archivi. Rimane il warning Authlib già presente.

Riprodurre l'audit:

```sh
.venv/bin/python scripts/audit_promotion_observability.py lab/reports/first-review-search lab/reports/promotion-strategy/observability-audit.json
.venv/bin/python -m pytest -q
```

Il prossimo passo eseguibile già predisposto è il confronto v1, con comandi e vincoli in [first-review-transfer](../first-review-transfer/README.md). Eseguire v2 richiede un nuovo confronto congelato. Il metodo di intervento sopra è la proposta per lo studio seguente; non attribuirgli risultati dell'audit osservazionale.
