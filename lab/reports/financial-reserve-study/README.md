# Riserva economica dalla nuova partita

27 ottobre 2026. Studio autorizzato da Matteo: esplorare con bot, senza quota IA, se proteggere le risorse economiche fin dall'inizio evita le morti successive senza sacrificare le promozioni.

## Risultato

La protezione economica riduce le insolvenze in entrambi i confronti. La prima versione, più severa, migliora la sopravvivenza ma **non migliora il conteggio dell'obiettivo principale**, seconda promozione con sopravvivenza. Una calibrazione più leggera, congelata prima di altre partite e confrontata con un nuovo controllo, dà un segnale promettente anche su quell'obiettivo.

Ogni riga contiene **256 nuove partite**, assegnate prima di `new_game`. Tutti gli esiti sono risolti e tutte le morti precoci restano nel denominatore:

| Raccolta e strategia | Insolvenze | Prima promozione entro M6 | Seconda promozione entro M12 | Seconda promozione e vivi | Vivi alla fine della finestra |
|---|---:|---:|---:|---:|---:|
| Prima raccolta: controllo | 26 | 198 | 163 | 160 | 228 |
| Prima raccolta: riserva più severa | **2** | 194 | 154 | 152 | **248** |
| Calibrazione: nuovo controllo | 35 | 186 | 129 | 125 | 217 |
| Calibrazione: riserva più leggera | **5** | 199 | **171** | **166** | **246** |

Per “vivi” intendiamo vivi alla prima osservazione del mese 13; non vengono eseguite azioni nel mese 13. La prima promozione e la seconda sono ricavate dai cambi di livello, non dal voto della review.

La conclusione candidata è **mantenere una riserva sostenibile lasciando spazio alla crescita e alle spese giustificate**. Non abbiamo dimostrato quale intensità sia ottimale o una regola che garantisca le promozioni per ogni agente.

## Che cosa cambia tra i bot

Entrambi usano lo stesso bot empirico congelato: bilanciamento di capacità, relazioni, risultati, salute e dignità; memoria persistente degli incidenti; stessa penalità empirica sulle risposte storicamente associate a esplosioni quando un incidente è già avvenuto. La memoria degli incidenti è attiva fin dall'inizio in entrambi i bracci. Le allocazioni trimestrali restano dipendenti dallo stato; non c'è un calendario forzato di pulizia.

La sola differenza del braccio `reserve` è un termine economico aggiunto al punteggio delle **scelte narrative**. Il termine usa il Wealth corrente e gli effetti nominali di un lookup congelato, costruito in precedenza dai log pubblici. Aumenta il peso di una perdita quando erode la riserva e valorizza il suo ripristino. Le spese per benefici sufficientemente importanti, come evitare una condizione fisica critica, restano possibili.

Il termine di ricerca è:

```text
weight × [min(target, Wealth + nominal_delta) − min(target, Wealth)]
− max(0, −nominal_delta)
```

La prima versione usa `target=2`, `weight=6`; la seconda `target=1`, `weight=2`. Sono **parametri ipotetici del bot**, non soglie economiche identificate nel simulatore e non istruzioni da copiare nelle Skills. Il trattamento cambia sia il costo attribuito alle uscite sia il valore attribuito al ripristino di una piccola riserva: non isola un veto puro alla spesa.

I modelli di effetti e di frequenze avverse sono esattamente gli stessi in entrambe le raccolte, senza aggiornamenti online. Un bot Python con lookup non equivale a un agente che legge il manuale; nessuna efficacia delle Skills è attribuita a questi risultati.

## Disegno e sequenza dello studio

1. Congelato il primo protocollo, i modelli, le dipendenze del codice e 512 assegnazioni in blocchi permutati di due. Eseguite tutte le partite indipendenti e non seminate dal controller.
2. Dopo aver osservato il primo risultato, preparato **un protocollo nuovo** per la calibrazione. Il protocollo originale è rimasto immutato. Il nuovo contiene l'hash dei risultati precedenti e dichiara il motivo della revisione: il vantaggio sulla sopravvivenza non si accompagnava a un miglioramento del conteggio principale.
3. Congelati i nuovi parametri e una nuova sequenza casuale; eseguite altre 512 partite con controllo fresco.

Gli outcome non determinano arresti anticipati e nessuna partita viene sostituita. Le due raccolte totalizzano **1.024 nuove partite assegnate**, senza interruzioni tecniche. Non selezioniamo solo i bot promossi al mese 6 e non condizioniamo l'outcome principale alla sopravvivenza intermedia.

Il controllo della prima raccolta ottiene 160 seconde promozioni con sopravvivenza, quello della seconda 125. Questa variazione è importante: **non possiamo confrontare direttamente 152 e 166 per attribuire al cambio di intensità un effetto incrementale**. Ciascun trattamento va confrontato con il proprio controllo. La seconda regola è stata scelta dopo la prima raccolta: non è una replica della prima e i campioni non vanno mescolati per proclamare una strategia vincente.

Rispetto al precedente studio sui rischi cambia anche la popolazione: qui il denominatore parte dalla nuova partita, mentre lì iniziava da L2 al menu del mese 6. I tassi fra i due studi non sono confrontabili come trattamenti.

## Differenze e incertezza

Gli intervalli sotto sono al 95%, esplorativi e non corretti per la molteplicità degli outcome. La differenza è riserva meno controllo, in punti percentuali:

| Outcome | Riserva più severa | Riserva più leggera |
|---|---:|---:|
| Insolvenza | −9,38 [−13,72; −5,65] | −11,72 [−16,60; −7,25] |
| Prima promozione entro M6 | −1,56 [−8,88; +5,77] | +5,08 [−2,41; +12,49] |
| Seconda promozione e vivi | −3,13 [−11,49; +5,30] | **+16,02 [+7,44; +24,26]** |
| Sopravvivenza | +7,81 [+3,44; +12,49] | +11,33 [+6,34; +16,55] |

Il primo risultato non dimostra un danno alla crescita: l'intervallo è ampio. Giustifica però esplorare una regola meno restrittiva anziché dichiarare risolto il problema grazie alle sole insolvenze evitate. La seconda versione dà un segnale utile sull'outcome principale, ma merita una replica congelata prima di essere scelta come versione definitiva.

Le crisi di fiducia sono 2 contro 6 nella prima raccolta e 4 contro 5 nella seconda; in entrambi i casi la differenza è incerta. Non ci sono morti per collasso fisico in questi campioni. Il miglioramento economico non autorizza a disattivare le altre salvaguardie.

## Cosa cambia nelle scelte e negli stati intermedi

La riserva più severa modifica la scelta predefinita in **273 azioni, distribuite su 176 partite**. Quella più leggera in **142 azioni su 112 partite**. La differenza è registrata rispetto alla scelta che il medesimo criterio di base avrebbe selezionato nello stato corrente; l'alternativa non viene eseguita come clone controfattuale.

Fra chi arriva vivo alla prima osservazione del mese 7:

- Prima raccolta: Wealth pari o inferiore a zero in 28/255 controlli e 5/256 trattati; mediana 2 contro 3.
- Calibrazione: Wealth pari o inferiore a zero in 41/252 controlli e 11/256 trattati; mediana 2 contro 3.

Sono descrizioni **condizionate all'arrivo al mese 7**, non gli effetti primari sul totale assegnato. Mostrano un meccanismo coerente con l'audit precedente: la riserva va protetta già nel prefisso, prima che i problemi emergano nei mesi successivi.

Le decisioni successive, compresi i menu trimestrali, possono divergere perché cambia lo stato. Il codice comune resta uguale: queste differenze sono conseguenze possibili del trattamento, non modifiche nascoste al confronto.

## Audit pubblico e integrità

Per ogni raccolta sono conservati protocollo, hash, modelli, assegnazioni, fonti del codice, osservazione iniziale e intere traiettorie pubbliche. Gli audit:

- ricostruiscono la sequenza casuale dal seme del controller e includono tutti gli slot iniziali;
- verificano prefisso completo, continuità fra osservazioni, azioni offerte e risposte applicate senza ambiguità;
- ricostruiscono la memoria degli incidenti esclusivamente dalle risposte precedenti;
- **riproducono ogni decisione** con il codice e i modelli congelati, verificando anche il punteggio economico registrato;
- ricavano promozioni, sopravvivenza e motivi di morte dagli stati pubblici e li riconciliano con le tabelle.

Sono riprodotte 25.223 azioni della prima raccolta e 25.133 della seconda, senza difformità. I rapporti sono [study-v1/independent-audit.json](study-v1/independent-audit.json) e [calibration-v1/independent-audit.json](calibration-v1/independent-audit.json). Le copie del codice rendono distinguibili le versioni; il runner rifiuta un riavvio nella stessa cartella.

## Nuovo ramo e catalogo esteso

È emerso un seguito ulteriore di uno scenario sulle dipendenze tra team. Le raccolte randomizzate avevano eseguito una sola delle due risposte. Una ricerca adattiva separata di **73 nuove partite**, senza IA, ha eseguito anche l'alternativa mancante; queste partite non sono incluse nei confronti.

L'audit combinato dei mesi **7–12** verifica ora **126 titoli, 266 fasi narrative e 646/646 risposte narrative**, oppure **268 nodi e 663/663 risposte** con i menu. Sono controllati 3.003 record di otto archivi, compresi i prefissi parziali dichiarati dello studio precedente. Copertura delle risposte incontrate, non di tutte le storie o gli stati nascosti possibili.

I nuovi testimoni sono in [extended-questions.json](extended-questions.json), l'integrità e l'assenza di alternative mancanti in [extended-coverage-audit.json](extended-coverage-audit.json). I cataloghi precedenti restano fotografie storiche corrette, non vengono riscritti per attribuire loro scoperte successive.

## Conseguenza per la strategia generale

La regola candidata è **proteggere una riserva sostenibile e valutare gli investimenti nel contesto di crescita, salute e fiducia**. Il saldo non deve diventare un obiettivo isolato. Le spese sostenibili con benefici credibili possono essere sensate, mentre spendere per approvazione immediata quando la riserva è fragile può compromettere la carriera successiva.

La [bozza del primo anno](../trust-risk-study/first-year-strategy-draft.md) è aggiornata con questo equilibrio, senza parametri numerici, titoli o risposte fisse. Il testo generale non è stato valutato con un agente. I bundle di Skills e il confronto Haiku congelato restano invariati e non giocati.

## Relevo

**Completato:** due protocolli distinti, 512+512 partite assegnate dalla nuova partita, modelli congelati e prudenza sugli incidenti comune; audit e riproduzione di 50.356 decisioni; analisi completa delle promozioni, insolvenze e sopravvivenza; 73 partite mirate per chiudere il nuovo ramo; catalogo da 663 risposte verificato. In totale **1.097 nuove partite** in questa indagine. Tutti i worker sono terminati. Nessuna chiamata a modelli IA, consumo di quota di gioco IA, registro cloud, automazione futura o lettura degli interni del simulatore. Origine `matteocash`; dati esterni in `/Users/matteozabban/careerlab-data/matteo-financial-reserve`.

**Limiti e seguito:** la calibrazione è adattiva fra raccolte, non durante una raccolta. Il diverso esito dei controlli richiede prudenza sui confronti fra intensità. Non abbiamo una strategia garantita né una prova sul comportamento di un agente. La riserva più leggera è una candidata per una replica indipendente congelata, mantenendo tutti i nuovi giochi nel denominatore; in alternativa, uno studio successivo può esplorare quali gap di crescita rimangono nei sopravvissuti senza seconda promozione. Nessuna di queste attività è stata avviata automaticamente.

Validazione software: **273 test passati**, con il warning Authlib preesistente. I nuovi controlli verificano costo della riserva, ripristino, scelta di spesa, eccezione per salute critica, guardia incidenti comune e creazione della calibrazione senza alterare il protocollo padre. Questi controlli del codice non sono una valutazione delle Skills.

Riprodurre gli artefatti dai record già raccolti:

```sh
.venv/bin/python scripts/analyze_financial_reserve.py /Users/matteozabban/careerlab-data/matteo-financial-reserve/study-v1 lab/reports/financial-reserve-study/study-v1
.venv/bin/python scripts/audit_financial_reserve.py lab/reports/financial-reserve-study/study-v1
.venv/bin/python scripts/analyze_financial_reserve.py /Users/matteozabban/careerlab-data/matteo-financial-reserve/calibration-v1 lab/reports/financial-reserve-study/calibration-v1
.venv/bin/python scripts/audit_financial_reserve.py lab/reports/financial-reserve-study/calibration-v1
.venv/bin/python scripts/extend_second_catalogue.py lab/reports/second-review-search lab/reports/financial-reserve-study /Users/matteozabban/careerlab-data/matteo-financial-reserve/catalogue-closure lab/reports/trust-risk-study
.venv/bin/python -m pytest -q
```

Non riusare le cartelle già giocate per una nuova raccolta. Un ulteriore intervento richiede un nuovo protocollo con le sue fonti e i suoi parametri fissati prima dei risultati.
