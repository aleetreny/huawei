# Scelta del manuale per il primo cutoff — 27 ottobre 2026

**Raccomandazione: inviare `t13-read-v4`, identico al bundle provato, dalla linea di Ale che integra idee della v10 di Matteo.** È la migliore scelta disponibile per il modello ufficiale; non è dimostrato che abbia una media di 70. Non sostituirlo adesso con una combinazione nuova né con il record isolato di script-v1.

## Perimetro e metodo

Recuperati tutti i **27 branch remoti** presenti al momento dell'audit, senza fare merge nelle linee degli altri. Inventariate **130 combinazioni distinte di percorso + metadati policy** (non 130 modelli indipendenti). Unione dei registri: **1.295 valutazioni distinte per job_id**, incluse prove con bot, interruzioni e risultati senza voto. Si conserva l'ingestione più recente di ogni job. Nessuna nuova partita, chiamata di modello o API a pagamento.

- `refs.json`: SHA esatti delle fonti; i branch possono avanzare dopo questa fotografia.
- `inventory.json`: tutti i candidati trovati nei policy.json e branch di provenienza; varianti dello stesso percorso possono comparire più volte.
- `ranking.json` e `ranking.csv`: tutti i gruppi policy/attore con score non nullo e senza interruption. Includono sconfitte valutate; escludono interruzioni, che vanno lette separatamente. Sono una ricognizione, non una graduatoria comparabile tra attori, ambienti e scopi.
- Risultati ufficiali molto recenti non ancora esportati nei registri (script-v1/v2, v7) sono presi dai rapporti del rispettivo branch e indicati come tali. Le traiettorie esterne ai repo di Ale/Leah non sono state ricostruite.

## Candidati decisivi

| Linea / manuale | Attore e campione | Q media | Carriere completate | Decisione |
|---|---|---:|---|---|
| Ale + idee Matteo, t13-read-v4 | DeepSeek ufficiale: 2 con voto, più 1 interrotta | 70,95 sui due voti | 2; la terza era in L1 al mese 22 | Prima scelta per il cutoff |
| Ale, script-v1 | DeepSeek ufficiale, rapporto: 76,87 e 13,23 | 45,05 | 1/2 | Miglior record DeepSeek, varianza troppo alta |
| Ale, script-v2 | DeepSeek ufficiale, rapporto: 51,12 e 30,60 | 40,86 | il rapporto documenta stallo e crisi | Scartare per questo cutoff |
| Ale, t13-read-v5 / v7 | DeepSeek ufficiale, 1 ciascuno | 66,71 / 67,27 | 1/1 ciascuno | Nessuna prova di vantaggio su v4 |
| Matteo, observed-growth-v10 | Haiku CLI 2.1.310, 16 | 55,35 | 11/16 | Preferenza tra i manuali Matteo |
| Matteo, observed-growth-v7 | Stesso Haiku, 9 | 57,56 | 7/9 | Media numericamente superiore a v10, differenza inconclusiva |
| Matteo, BHR | Stesso Haiku, 17 | 48,06 | 11/17 | Replica negativa rispetto al primo lotto |
| Matteo, M1 | Stesso Haiku, 1 | 64,06 | 1/1 | Campione insufficiente |
| Ale, t13-final | Haiku, modalità ufficiale, 12 | 57,24 | 10/12 | Buon riferimento precedente, superato dalla prova target di v4 |
| Ale, f3-lean-v1 | Stesso attore di t13-final, 43 | 50,52 | 30/43 | Riferimento, non prima scelta |
| Leah, l1-review-clock-v1 | Haiku Pro CLI 2.1.295, 3 | 52,06 | 2/3 | Nessuna evidenza target; altro attore: 37,72 su 4 |
| Leah, l1-review-clock-v2 / v3 | Haiku Pro, 1 ciascuno | 20,48 / 21,76 | 0/1 ciascuno | Non proporre |
| Leah, l6-routine-v1 | Haiku Pro, 1 | 23,01 | 0/1 | Regola trimestrale seguita, riferimento non accessibile all'attore: test limitato |

**Q è quantitative_score della partita, non il punteggio finale della submission.** Il confronto 80% partite + 10% qualità SKILL + 10% token non è stato ricalcolato integralmente. I voti del banco di percezione, del simulatore e della rubrica non sono voti di carriere del modello ufficiale.

## Perché v4

È già stato eseguito da deepseek-v4-flash nel runner ufficiale: due finali L5, rischio finale 0, Health e Dignity piene. La protezione dei valori migliori del livello e la finestra prima della review provengono anche dal lavoro di Matteo: policy.json attribuisce esplicitamente la derivazione a observed-growth-v10. Separazione delle fasi, protezione dei punti prima della review e filtro di rischio risolvono fallimenti osservati nelle versioni precedenti.

Il bundle con script ha raggiunto L6 e 76,87, ma l'altra carriera è morta con 13,23. La media osservata 45,05 conta più del record. Inoltre il rapporto segnala circa 110M token di input per la carriera completa contro 66–70M di v4; l'effetto preciso sulla valutazione dipende dalla formula e dai token di tutte le partite. script-v3 era ancora in prova nel rapporto; il commit v3b corregge una morte per insolvibilità in v3. Nessuna conferma completa di v3b era disponibile nella fotografia: promettente per dopo, non un vincitore provato oggi.

## Il limite da non nascondere

I due risultati 71,67 e 70,22 non autorizzano a promettere una media di 70: una terza v4 è arrivata al mese 22 in L1 e si è interrotta per collisione di porte. La traiettoria riportata suggerisce un prossimo licenziamento; non sappiamo il suo voto terminale. Non la conto come una carriera riuscita né le attribuisco un voto inventato.

Sensibilità, **non stima**: se quella carriera avesse fatto 15–25, la media delle tre sarebbe stata 52,30–55,63. In una submission di tre carriere una sola sconfitta pesa molto. Il rapporto DeepSeek propone 63–65 come proiezione usando il tasso L1 dell'intera famiglia, ma quel tasso non è una stima affidabile specifica di v4: campione piccolo, versioni diverse e interruzioni. La scelta di v4 è un giudizio sulla prova target e sui meccanismi, non una superiorità statisticamente dimostrata.

## Matteo e Leah: cosa resta buono

**Matteo:** il primo lotto v10 (59,56 su 8) non è più il dato aggiornato. La replica aggiunge 8 partite da 51,14: totale 55,35 su 16, una partita record Haiku da 77,78 in L6. BHR passa da 59,49 su 8 a 48,06 su 17; nel lotto alternato, v10 51,14 contro BHR 37,90. La preferenza per v10 regge, pur senza raggiungere il 95% nella valutazione del rapporto (P=0,85 sul totale). v7 ha 57,56, ma con 9 carriere non ne dimostra la superiorità. v8/v9/v11 sono prevalentemente test interrotti dopo review, v12 ha una sola carriera da 50,20, le varianti cooperate peggiorano; M1 una sola carriera. Non userei queste versioni al cutoff senza evidenza DeepSeek.

**Leah:** l1-review-clock-v1 è il suo candidato con i migliori dati sulle carriere locali (52,06 su 3), ma l'altra valutazione nello stesso repo scende a 37,72 su 4 con un attore diverso. l1-review-clock-v3 ha anche un gruppo da 52,26 su 4 nell'attore della corsa: campione piccolo e nessuna prova DeepSeek. La linea t13-perc migliora alcune etichette ma non le scelte: nel banco prima della review perde punti nel 30% contro 18% di t13-final (60 situazioni, intervalli sovrapposti); la stessa Leah sconsiglia l'integrazione. Votazione 55,1 è un voto di bot nella replica, non un risultato target. Non sceglierei un suo manuale per questa prima consegna; il contributo alla diagnosi e agli strumenti è sostanziale.

Le famiglie storiche P0/F1–F8, M3, o1–o3, bb-mechanics, periodos/secciones, targeted/stretch/bold e le varianti di trasmissione sono tutte censite negli allegati. Non emerge una combinazione di prove target e stabilità migliore del candidato v4. Le prove con Opus e i bot con informazioni privilegiate sono tetti diagnostici, non candidati di consegna.

## Cosa congelare per inviare

- Sorgente: branch `alejandro/deepseek`, versione t13-read-v4 introdotta in `09d5735`, policy `f78c8b8834082a8c`.
- Cartella: `lab/policies-src/deepseek/t13-read-v4/bundle/`; Skill `career-rules` e manifest insieme, identici ai byte valutati.
- SHA256 completo del bundle verificato: `f78c8b8834082a8c816c65cd9bf3704407f37b51b9355d515d9836bc3efffea7`.
- Lint locale eseguito su estrazione esatta: exit 0, **6 segnalazioni REVIEW**, nessun errore bloccante. Non equivale ad approvazione di conformità né a validazione finale del pacchetto. Le segnalazioni riguardano calendario pubblico e numeri di formato/contatori; il controllo finale resta all'organizzatore.
- Aggiornare i documenti di consegna che nominano ancora v2 al candidato congelato, includere il video e passare il validatore ufficiale sul pacchetto finale. Questo audit non ha creato né inviato una submission.
- Se resta tempo e budget già autorizzato al responsabile: una conferma v4 isolata dai conflitti di porte è più utile di un'altra riscrittura. Non è stata lanciata da questo audit.

## Fonti verificabili

- [Partite DeepSeek v2–v7, inclusa v4 interrotta](https://github.com/aleetreny/huawei/blob/c9850d56a9e07ea908b74139c49fc85d76d7c90e/lab/reports/deepseek/mejora-nota.md)
- [Script: risultati, varianza e token](https://github.com/aleetreny/huawei/blob/d8c4019da7d43666dbb4d6d63a26d2eba9bff06c/lab/reports/formato/README.md)
- [Replica aggiornata v10/BHR](https://github.com/aleetreny/huawei/blob/678efbb1228130595f3594112376fc5a572df96a/lab/reports/matteo-v10-vs-bhr.md)
- [Primo lotto BHR e M1](https://github.com/aleetreny/huawei/blob/678efbb1228130595f3594112376fc5a572df96a/lab/reports/matteo-bhr-haiku.md)
- [Percezione e test negativo di Leah](https://github.com/aleetreny/huawei/blob/305a20486bef50a825f2c0fd25b6db588a68a385/lab/reports/stat-perception/README.md)
- [Indice dei manuali precedenti di Leah](https://github.com/aleetreny/huawei/blob/305a20486bef50a825f2c0fd25b6db588a68a385/docs/historico/research/leah/README.md)
- [Confronto Haiku t13-final e riferimenti](https://github.com/aleetreny/huawei/blob/53025e191d365e8ce3e52ef8ffdb819826421831/lab/reports/transmision/resumen.md)

## Relevo

Audit richiesto da Matteo per la prima submission: inventario completo dei branch, deduplicazione dei registri, lettura dei rapporti più recenti e controllo del bundle v4. Raccomandazione congelata sopra; nessun cambiamento ai manuali o alle linee degli altri. Nessun costo AI/API, nessuna nuova carriera. Il sito ufficiale non era accessibile via strumento web: calendario e requisiti sono riferiti ai documenti del repo, non verificati online in questa sessione.

Prossimo passo dell'organizzatore: riesaminare eventuali nuovi risultati script-v3/v3b successivi agli SHA in refs.json; se non cambiano il quadro con più carriere complete e senza aumentare le sconfitte, confezionare v4 e validare la submission. Unire solo questo rapporto e gli allegati; non serve unire l'intera storia della branch di Matteo.
