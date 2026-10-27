# Crescita con vincoli di sostenibilità

27 ottobre 2026. Richiesta di Matteo: ricostruire le 101 scelte in cui la crescita congiunta scavalcava la prudenza, definire un filtro e confrontarlo con bot senza quota IA.

## Decisione

**Il filtro recupera parte del danno del bonus congiunto, ma non sostituisce il controllo attuale.** In 192 partite per braccio, il filtrato porta i sopravvissuti da 165 a 181 rispetto al congiunto; il controllo resta a 190. Le seconde promozioni con sopravvivenza sono 120, 122 e 122 rispettivamente. Il vantaggio rispetto alla crescita senza filtro riguarda soprattutto la sopravvivenza; non emerge un guadagno dimostrato sull'outcome principale.

Tutte le **576 nuove partite** sono risolte, senza interruzioni tecniche. Il confronto usa bot Python con strumenti pubblici ufficiali, nessun modello di gioco IA o quota IA. Non è una valutazione delle Skills e non produce una strategia garantita al 100%.

## Che cosa cercavano le 101 scelte storiche

Fonte: archivio congelato del precedente `growth-gap-study/balanced-v1`, con hash verificato. La [diagnosi completa](override-diagnosis.json) conserva riferimenti a partita e passo, testo pubblico, stato, scelta eseguita, alternativa comune non eseguita, effetti nominali, frequenze empiriche e risposta ricevuta.

- **101 scelte in 68 carriere**, su 27 titoli, distribuite fra i mesi 3 e 12.
- Rispetto alla scelta comune, 60 hanno un delta nominale migliore di Network, 60 di Output, 11 di Skill; le categorie si sovrappongono.
- In **79** il delta nominale di Dignity è peggiore e in **15** quello di Health. Nessuna peggiora il delta nominale di Wealth rispetto alla scelta comune.
- La differenza mediana del bonus di preparazione è **+8**. Il bonus spesso premia evitare una perdita di preparazione che la scelta prudente comporterebbe, non un aumento assoluto del punteggio.
- Solo **sei** risposte sono immediatamente avverse secondo il rilevatore pubblico di incidenti. Quindici delle 68 carriere finiscono con una crisi di fiducia, ma questo non attribuisce la crisi a una scelta specifica.

Esempio concreto: nel caso `run13/step38` del mese 10, mantenere riservato un rapporto e sperare che il problema non si manifesti conserva Output e Network; segnalare e preparare una soluzione d'emergenza perde preparazione nel proxy. Il bonus congiunto favorisce la prima opzione, pur essendo associata nel lookup a maggiore esposizione. Non è una raccomandazione per quello scenario: mostra un conflitto fra preparazione visibile e gestione delle conseguenze. Per ogni caso il passo esatto e le due risposte sono nel JSON; l'alternativa comune non è stata eseguita nello stesso stato.

Sono casi selezionati e associazioni storiche. Il lookup non identifica il rischio vero, e l'assenza di una risposta avversa immediata non dimostra né assenza né presenza di conseguenze differite. Le nuove partite studiano l'intero pacchetto, senza pretendere un controfattuale esatto per ciascuno dei 101 casi.

## Protocollo congelato prima delle nuove partite

[Protocollo](study-v1/protocol.json): **192 nuove partite per ciascuno di tre bracci**, assegnate prima di `new_game` in blocchi permutati di tre. Stesso lookup congelato della calibrazione economica leggera, nessun apprendimento online e nessuna esplorazione adattiva nella raccolta.

1. **Controllo:** riserva leggera e guardia persistente degli incidenti, invariati.
2. **Congiunto:** stesso bonus congiunto del precedente studio, invariato.
3. **Filtrato:** stesso punteggio congiunto, con filtro delle alternative prima della graduatoria.

Il filtro conserva sempre la scelta del controllo nello stesso stato. Dopo un precedente incidente pubblico esclude alternative narrative con frequenza empirica avversa superiore a quella scelta. Esclude inoltre alternative che peggiorano rispetto al controllo il deficit nominale di Wealth rispetto a 1, Health rispetto a 4, Dignity rispetto a 2. Esclude alternative dal cambiamento nominale sconosciuto. Le protezioni della pulizia esplicitamente richiesta e delle scelte documentali restano intatte.

Questi numeri sono **impostazioni private di ricerca**, non soglie identificate del gioco o istruzioni da inserire in una Skill. Per esempio un costo di salute è ancora ammesso se la proiezione non apre il deficit, e un deficit già inevitabile nella scelta comune non viene vietato in assoluto. La scelta comune può essere già rischiosa; le proiezioni nominali possono differire dal regolamento effettivo. Si studia un pacchetto di vincoli, non l'effetto separato di ciascuno.

Outcome principale: seconda promozione entro il mese 12 e vivi alla prima osservazione del mese 13, su tutte le assegnazioni iniziali. Contrasti previsti: congiunto meno controllo; filtrato meno controllo; filtrato meno congiunto. Sopravvivenza e cause di morte sono outcome secondari essenziali; il protocollo esclude di adottare un semplice aumento numerico della promozione accompagnato da peggiore sopravvivenza. Intervalli Wilson/Newcombe al 95%, esplorativi senza correzione multipla. Nessun arresto basato sui risultati o sostituzione delle interruzioni.

L'input storico usato per progettare il filtro è conservato esattamente in `study-v1/design-input-diagnosis.json`, con hash nel protocollo. Nessun dato della nuova raccolta modifica il controller o il protocollo.

## Risultati sul totale assegnato

| Braccio, 192 partite ciascuno | Prima promozione entro M6 | Seconda entro M12 | Seconda e vivi | Vivi alla fine | Insolvenza | Crisi fiducia |
|---|---:|---:|---:|---:|---:|---:|
| Controllo | 140 | 122 | **122** | **190** | 2 | 0 |
| Congiunto | 148 | 124 | **120** | 165 | 8 | 19 |
| Filtrato | 141 | 123 | **122** | 181 | 5 | 6 |

Nessuna morte per Blackout. Tutti gli esiti sono noti, quindi il denominatore risolto coincide con quello assegnato.

| Contrasto previsto | Differenza seconda e vivi, punti % [95%] | Differenza sopravvivenza, punti % [95%] |
|---|---:|---:|
| Congiunto − controllo | −1,04 [−10,60; +8,55] | **−13,02 [−18,70; −8,03]** |
| Filtrato − controllo | 0,00 [−9,55; +9,55] | **−4,69 [−8,99; −1,03]** |
| Filtrato − congiunto | +1,04 [−8,55; +10,60] | **+8,33 [+2,36; +14,49]** |

Le crisi di fiducia scendono da 19 a sei fra congiunto e filtrato: differenza −6,77 punti, intervallo −12,09 a −1,83. Rispetto al controllo sono sei contro zero: +3,13 punti, intervallo +0,54 a +6,65. Sono intervalli nominali esplorativi e i numeri piccoli richiedono cautela. L'uguaglianza 122 contro 122 sull'outcome principale non dimostra equivalenza; l'intervallo lascia differenze rilevanti in entrambe le direzioni.

Non si aggrega questo controllo con i precedenti: le carriere sono indipendenti e non inizializzate allo stesso seed di gioco. Non si confronta il dato 181 direttamente con controlli di altre raccolte per scegliere una variante.

## Il filtro è stato applicato, ma il suo perimetro è limitato

L'audit riproduce **28.523 decisioni** e verifica separatamente i vincoli nominali in tutte le **9.590 decisioni** del braccio filtrato.

Il filtro cambia **145 scelte**, tutte narrative: 116 coinvolgono la frequenza empirica dopo incidente, 27 la salute fragile, due la riserva fragile e una la dignità fragile. Le categorie si sovrappongono. Il veto sulle alternative dagli effetti sconosciuti non modifica direttamente la scelta vincente in questa raccolta.

Le scelte narrative diverse dal controllo nello stesso stato sono 364 nel congiunto e 216 nel filtrato. Dopo un incidente, quelle con frequenza empirica maggiore del controllo sono **106 nel congiunto e zero nel filtrato**. Questo verifica una proprietà del controller; non identifica un numero di incidenti evitati.

La [traccia delle crisi residue](study-v1/residual-failure-traces.json) mostra un limite concreto:

- Prima del primo incidente pubblico, il filtrato compie 206 scelte narrative diverse dal controllo; **129** hanno una frequenza empirica avversa maggiore. Questo era ammesso dal protocollo.
- Dopo un incidente compie dieci scelte narrative diverse, nessuna con frequenza superiore al controllo.
- Tutte le **sei crisi residue** avvengono dopo almeno un precedente incidente pubblico. La scelta fatale coincide in tutti e sei i casi con la scelta del controllo **in quello stato raggiunto**. Quattro carriere hanno precedenti scelte di crescita diverse dal controllo.

Lo stesso nome di azione nello stato finale non rende uguali due storie. Questi dati non dimostrano che le 129 scelte abbiano causato le crisi, né che estendere il veto dall'inizio le impedirebbe. Mostrano perché una garanzia relativa alla singola scelta successiva all'incidente non è una garanzia sulla sostenibilità dell'intero percorso.

Fra i sopravvissuti del filtrato, 43 hanno mancato la prima promozione in tempo e 16 sono fermi a L2 dopo una prima in tempo; nel controllo sono 51 e 17. Sono gruppi successivi al trattamento, non confronti causali condizionati alla sopravvivenza.

## Conseguenze per il manuale

La [bozza generale](../trust-risk-study/first-year-strategy-draft.md) resta una proposta non validata con agenti. Il risultato sostiene di considerare esposizione e impegni anche prima del primo incidente, e di distinguere “non peggiore di una scelta abituale su una stima” da “sicura”. Non trasferiamo il filtro numerico alle Skills e non promuoviamo il bot filtrato a sostituto del controllo.

Il problema aperto ha due parti: conservare preparazione senza comprare esposizione, e migliorare il tasso di promozione del controllo senza erodere la sua sopravvivenza. Questo studio recupera parte della seconda perdita prodotta dal bonus precedente; non dimostra di aver risolto la prima parte.

## Dati e riproducibilità

- [Diagnosi storica](override-diagnosis.json): 101 casi con alternative e conseguenze pubbliche.
- [Risultati](study-v1/results.json): denominatori, outcome, tutti i contrasti, consegna del filtro e gruppi intermedi.
- [Audit indipendente](study-v1/independent-audit.json): assegnazioni, prefissi completi, ogni decisione, memoria solo del passato, ricostruzione degli outcome e vincoli.
- [Tracce delle crisi residue](study-v1/residual-failure-traces.json): scelte effettive, alternative comuni non eseguite e incidenti precedenti.
- [Continuità del catalogo](catalogue-continuity-audit.json): nessun nuovo nodo nei mesi 1–6 o 7–12 nei 576 nuovi record. Il catalogo conosciuto 7–12 resta **646/646 risposte narrative, 663/663 totali**; non è enumerazione di tutti gli stati nascosti.
- `study-v1`: archivio pubblico compresso completo, protocolli, modelli, schedule casuale, hash e snapshot dei sorgenti.

## Relevo

**Completato:** ricostruzione dei 101 casi storici, protocollo a tre bracci congelato, 576 nuove partite risolte senza interruzioni, audit delle 28.523 decisioni e dei 9.590 vincoli decisionali, tracce delle sei crisi residue, continuità del catalogo e aggiornamento generale della bozza. Nessuna variante adottata.

Origine `matteofilter`, dati esterni `/Users/matteozabban/careerlab-data/matteo-constrained-growth/study-v1`. Solo strumenti pubblici del gioco, nessun modello IA di gioco, quota IA, lettura degli interni del simulatore, registro cloud o automazione. Tutti i sei worker sono terminati. Skills di consegna e confronto Haiku congelato restano invariati e non giocati.

**Pubblicazione remota completata:** il push fino ad `a180e29` è riuscito il 27 ottobre, includendo lo studio, il pannello e il confronto con Ale nella PR #12. I precedenti errori TLS/HTTP408 sono risolti; nessuna partita da rilanciare.

**Possibile seguito, non avviato:** isolare un filtro applicato prima del primo incidente, con controllo fresco e stesso bonus. Trattarlo come nuova ipotesi, non correzione già dimostrata; prima ricostruire le 129 scelte pre-incidente per capire quanto il veto sposterebbe preparazione e costi. In alternativa approfondire la conservazione della preparazione nei casi del controllo che mancano la review, senza aggiungere un premio indiscriminato. Non lanciare una nuova raccolta modificando il protocollo esistente.

Validazione software: 287 test passati con il warning Authlib preesistente. I sette controlli nuovi verificano il vincolo prima/dopo incidente, il confronto relativo dei deficit, il fallback comune, la protezione dagli effetti sconosciuti, l'identità dei due riferimenti, la pulizia richiesta e l'impossibilità per il bonus di scavalcare il veto. Questi controlli non sono una valutazione delle Skills.

Riprodurre dai record già raccolti:

```sh
.venv/bin/python scripts/diagnose_growth_overrides.py lab/reports/growth-gap-study/balanced-v1 lab/reports/constrained-growth-study/override-diagnosis.json
.venv/bin/python scripts/analyze_constrained_growth.py /Users/matteozabban/careerlab-data/matteo-constrained-growth/study-v1 lab/reports/constrained-growth-study/study-v1
.venv/bin/python scripts/audit_constrained_growth.py lab/reports/constrained-growth-study/study-v1
.venv/bin/python scripts/trace_constrained_failures.py lab/reports/constrained-growth-study/study-v1
.venv/bin/python scripts/analyze_growth_gap.py catalogue lab/reports/constrained-growth-study
.venv/bin/python -m pytest -q
```

Il runner rifiuta il riavvio di cartelle già giocate. Un nuovo intervento richiede un nuovo protocollo.
