# Sopravvivere senza seconda promozione: diagnosi e priorità di crescita

27 ottobre 2026. Richiesta di Matteo: studiare gli 80 percorsi vivi senza seconda promozione, mantenendo riserva leggera e prudenza sugli incidenti, poi esplorare correzioni con bot senza quota IA.

## Conclusione operativa

**Nessuna delle nuove varianti giustifica sostituire il controllo attuale.** Una priorità tecnica aggiuntiva corregge il gap tecnico osservato ma non migliora l'outcome complessivo; spingere relazioni o risultati peggiora il conteggio di seconde promozioni con sopravvivenza. Un successivo bonus di preparazione congiunta dà un piccolo aumento numerico delle promozioni con sopravvivenza, incerto, e un calo della sopravvivenza.

La distinzione utile è tra **guadagnare preparazione e conservarla**. I fallimenti non sono tutti uno stesso blocco a L2, e un indicatore migliorato non compensa necessariamente una lacuna nuova o un incidente. Il bot con riserva leggera e guardia degli incidenti resta il riferimento per questo studio; nessuna formula numerica è promossa a Skill o a garanzia del gioco.

Sono state eseguite **1.152 nuove partite**: 768 nel confronto delle priorità separate e 384 nel seguito con priorità congiunta. Tutte assegnate dalla nuova partita, tutte risolte, nessuna interruzione tecnica. Nessun modello IA, quota di gioco IA o registro cloud utilizzato.

## Gli 80 percorsi originari non sono tutti stagnazioni a L2

La fonte è il braccio `reserve` della calibrazione economica precedente: 246 sopravvissuti alla prima osservazione del mese 13, dei quali 166 con seconda promozione.

| Gruppo dei restanti 80 | Percorsi | Stato alla fine |
|---|---:|---|
| Mancata prima promozione entro il mese 6 | **53** | 45 ottengono la prima promozione più tardi e finiscono L2; otto finiscono L1 |
| Prima promozione in tempo, mancata seconda | **27** | Tutti finiscono L2 |

Fra i 53 che mancano la prima finestra, **33** non hanno gap nel proxy di crescita all'inizio del mese 5. Nei 27 fermi a L2, all'inizio del mese 11 ci sono 14 casi con gap tecnico, sei con gap di risultati (quattro sovrapposti al gap tecnico) e 11 senza gap nel proxy. Nessuno di questi 27 ha un gap di relazioni in quel momento.

Il proxy usa ipotesi numeriche ricavate dalla ricerca: per L1 Skill/Network/Output 8/3/3, per L2 18/6/6. **Non sono soglie pubblicate o una formula identificata.** Le osservazioni al mese 5 o 11 precedono la review, ma la scelta e le conseguenze successive possono cambiare lo stato. I gruppi sono sopravvissuti selezionati, non una stima causale sull'intera popolazione.

L'audit al confine trova, nei fallimenti studiati:

- Prima review: 27/53 sono pronti nel proxy prima dell'ultima scelta; per 23/53 esiste almeno un'alternativa nota che conserverebbe o raggiungerebbe il proxy nella proiezione nominale. La scelta effettiva non risulta pronta in nessuno dei 53 casi secondo tale proiezione.
- Seconda review dei 27: sette sono pronti prima dell'ultima scelta; in tre casi esiste un'alternativa con proiezione pronta. La scelta effettiva non risulta pronta nel proxy in nessuno dei 27 casi.
- In **cinque casi di ciascun gruppo**, lo stato è pronto prima della scelta ma tutte le alternative note aprono un gap nella proiezione nominale. Un esempio è lo scambio fra contestazione pubblica con perdita di relazioni e discussione privata con perdita di risultati.

Queste sono **proiezioni del lookup**, non controfattuali eseguiti. Non includono tutti i regolamenti automatici e non provano che un esito sia inevitabile. Sono però una ragione concreta per non confondere una fotografia pronta con una promozione assicurata, o attribuire ogni fallimento a scarsa preparazione iniziale. Casi, alternative, risposte pubbliche e limiti sono in [diagnosis.json](diagnosis.json).

## Primo confronto: una priorità alla volta

Protocollo congelato prima delle nuove partite: [study-v1/protocol.json](study-v1/protocol.json). Quattro bracci, **192 nuove partite ciascuno**, blocchi permutati di quattro assegnati prima di `new_game`.

Tutti condividono riserva leggera, guardia empirica degli incidenti, gestione dello stato e modelli congelati. Nei tre bracci attivi si aggiunge una priorità marginale verso il proxy di **un solo indicatore**. Il bonus penalizza anche la perdita sotto il target e non premia guadagni trimestrali positivi già osservati come saturi. La pulizia esplicitamente richiesta dall'avviso di rischio resta protetta.

Il trattamento cambia il criterio di scelta: non significa semplicemente eseguire sempre una particolare azione. I numeri del proxy e il peso del bonus sono impostazioni private del bot di ricerca, non istruzioni di consegna.

| Braccio | Prima promozione entro M6 | Seconda entro M12 | Seconda e vivi | Vivi alla fine | Insolvenza / crisi fiducia |
|---|---:|---:|---:|---:|---:|
| Controllo comune | 149 | 135 | **131** | 184 | 3 / 5 |
| Più priorità tecnica | 143 | 132 | **131** | 189 | 0 / 3 |
| Più priorità alle relazioni | 118 | 92 | **92** | 182 | 4 / 6 |
| Più priorità ai risultati | 146 | 108 | **108** | 180 | 4 / 8 |

L'outcome principale è seconda promozione con sopravvivenza alla prima osservazione del mese 13, sul totale iniziale assegnato. Differenze rispetto al controllo, in punti percentuali, con intervalli esplorativi al 95%:

- Priorità tecnica: **0,00**, intervallo −9,25 a +9,25.
- Relazioni: **−20,31**, intervallo −29,61 a −10,46.
- Risultati: **−11,98**, intervallo −21,37 a −2,28.

Gli intervalli non sono corretti per confronti multipli. Non sono una conclusione che Skill, Network o Output siano inutili: sono gli esiti di queste modifiche del controller empirico.

### L'indicatore può migliorare mentre il percorso peggiora

Fra chi raggiunge l'inizio del mese 11 a L2:

| Braccio | L2 osservati | Sotto proxy Skill | Sotto proxy Network | Sotto proxy Output |
|---|---:|---:|---:|---:|
| Controllo | 148 | 14 | 10 | 18 |
| Priorità tecnica | 142 | **0** | 8 | 16 |
| Relazioni | 118 | 17 | **2** | 23 |
| Risultati | 144 | 23 | 13 | **14** |

Sono gruppi **successivi al trattamento**, con denominatori diversi: la tabella è diagnostica, non una stima causale condizionata all'arrivo a L2. È coerente con lo spostamento dei gap: la metrica favorita migliora, ma altre mancanze restano o crescono. La versione tecnica non migliora il risultato globale nonostante l'assenza del gap tecnico osservato; quella relazionale perde già molte prime promozioni.

Fra i sopravvissuti del controllo rimangono 41 casi che hanno mancato la prima promozione e 12 fermi a L2 dopo una prima promozione in tempo. Questo conferma quanto sia importante distinguere il momento in cui il percorso si è fermato.

## Seguito separato: un bonus di preparazione congiunta

Dopo il primo confronto è stato congelato **un protocollo nuovo**, con controllo fresco e 192 partite per braccio. Il protocollo originale non è stato modificato. [balanced-v1/protocol.json](balanced-v1/protocol.json) registra l'hash esatto dei risultati disponibili quando è stato progettato il seguito; il relativo input è conservato in `design-input-results.json` e verificato dall'audit.

Il bonus congiunto considera il prodotto delle proporzioni Skill/target, Network/target e Output/target, ciascuna limitata a uno. Un indicatore già sufficiente non riceve premio aggiuntivo oltre quel punto; perdere un altro requisito può annullare il progresso. Il bonus resta **sommato** al punteggio comune, con la medesima riserva, guardia incidenti e protezione della pulizia esplicita.

Questa è una scelta sperimentale di progettazione, non una formula del gioco o una prova di complementarità universale.

| Braccio del seguito | Prima promozione entro M6 | Seconda entro M12 | Seconda e vivi | Vivi alla fine | Insolvenza / crisi fiducia |
|---|---:|---:|---:|---:|---:|
| Nuovo controllo | 140 | 107 | **107** | **182** | 3 / 7 |
| Bonus congiunto | 147 | 121 | **116** | **169** | 6 / 17 |

L'outcome principale migliora numericamente di **4,69 punti**, ma l'intervallo va da −5,14 a +14,39. La sopravvivenza cala di **6,77 punti**, intervallo −12,62 a −1,13. Le crisi aumentano da sette a 17. Non adottiamo quindi questa variante come miglioramento dimostrato.

Il controllo del primo confronto ottiene 131 seconde promozioni con sopravvivenza, quello del seguito 107. Si confronta ogni intervento con il proprio controllo; non si usa il dato del primo per giudicare direttamente il secondo. Il seguito è adattivo fra raccolte, ma nessun risultato ha cambiato la politica all'interno di una raccolta.

## Perché mantenere un peso di prudenza non basta a preservare le decisioni prudenti

La riproduzione delle decisioni individua **101 scelte narrative** del braccio congiunto in cui, dopo un incidente, il bonus di crescita sostituisce la scelta comune con un'alternativa dalla frequenza empirica di risposte avverse più alta. Nei tre bracci separati i conteggi analoghi sono 14 per Skill, 33 per Network e 47 per Output.

Si confrontano opzioni disponibili nello **stesso stato osservato**, non si eseguono esiti controfattuali. Le frequenze sono associazioni storiche, non rischi veri delle singole azioni. La traccia mostra comunque una proprietà del controller: un bonus può scavalcare una penalità rimasta formalmente invariata. Conservare il peso della prudenza non equivale a conservare le sue scelte quando si aggiunge un premio grande altrove.

La futura ipotesi da isolare è una crescita vincolata alla sostenibilità della decisione, senza consentire al premio di comprare esposizione ulteriore indiscriminatamente. Non abbiamo eseguito quel nuovo intervento e non ne attribuiamo risultati a questo studio.

## Quale parte della strategia resta utile

La [bozza generale del primo anno](../trust-risk-study/first-year-strategy-draft.md) mantiene riserva sostenibile, memoria degli incidenti, capacità fisica e preparazione bilanciata. Aggiunge il controllo che un guadagno non apra una lacuna in un'altra dimensione già necessaria, e la distinzione fra recuperare una prima promozione mancata e crescere dopo L2.

Non sostituiamo il manuale con i bonus numerici studiati. Una soglia empirica o una proiezione nominale non sono il meccanismo completo della review. Un'alternativa che preserva il proxy può avere altri costi; talvolta nessuna proiezione disponibile conserva tutto. Questi casi richiedono studio della storia e della preparazione precedente, non una promessa di successo garantito.

## Dati, audit e catalogo

- [diagnosis.json](diagnosis.json): gli 80 casi originari, fotografie prima delle review, alternative e risposte pubbliche.
- Cartelle `study-v1` e `balanced-v1`: protocolli, assegnazioni, modelli congelati, fonti del codice, risultati e archivi pubblici completi 1–12.
- `results.json` di ogni raccolta: denominatori iniziali, outcome, intervalli, gruppi intermedi e partizione dei sopravvissuti.
- `independent-audit.json`: ricostruzione indipendente dei cambi di livello e delle morti; riproduzione di ogni decisione, inclusi bonus, memoria e scelte comuni.
- [catalogue-continuity-audit.json](catalogue-continuity-audit.json): nessun nuovo nodo pubblico incontrato nei mesi 1–6 o 7–12 rispetto ai riferimenti congelati, nei 1.152 record nuovi.

Sono riprodotte **38.388 + 18.901 = 57.289 decisioni**, senza difformità. La completezza dei prefissi, l'assegnazione prima della nuova partita, le azioni offerte e il mancato uso di informazioni future sono verificati. Nessuna azione viene eseguita nel mese 13.

Il catalogo conosciuto dei mesi 7–12 resta quindi **646/646 risposte narrative e 663/663 totali**. Non è enumerazione di tutti gli stati o di tutti gli esiti possibili: la nuova esplorazione non ha aggiunto testi di domanda, ma aggiunge molti contesti ed esiti di domande già note.

## Relevo

**Completato:** diagnosi dei due gruppi originari, confronto congelato di tre priorità con controllo (768 partite), seguito congiunto separato (384), audit delle 57.289 decisioni, controllo di continuità del catalogo e aggiornamento della bozza generale. Tutte le 1.152 partite hanno un esito risolto, nessuna interruzione tecnica. Origine `matteogaps`, dati esterni `/Users/matteozabban/careerlab-data/matteo-growth-gaps`, nessuna chiamata a modelli IA, quota di gioco IA, registro cloud, automazione o lettura degli interni del simulatore. Tutti i worker sono terminati. I bundle di Skills e il confronto Haiku congelato sono invariati e non giocati.

**Decisione:** non sostituire il controllo con nessuna delle varianti nuove. Le priorità separate non migliorano l'outcome principale; il seguito congiunto ha un vantaggio incerto e costa sopravvivenza. La regola generale deve preservare l'insieme dei requisiti e la sostenibilità, senza convertire un deficit osservato in un ordine permanente di massimizzare quell'indicatore.

**Possibile seguito, non avviato:** isolare un vincolo di rischio e sostenibilità che limiti le alternative prima di premiare la crescita; oppure approfondire i casi pronti in cui tutte le opzioni aprono un gap nel proxy, ricostruendo gli antecedenti. Per estendere ai mesi 13–18, conservare anche i percorsi con prima promozione tardiva e i loro impegni. Non dedurre da un mancato avanzamento iniziale una morte certa: 45 dei 53 casi originari recuperano la prima promozione entro la finestra osservata.

Validazione software: **280 test passati**, con il warning Authlib preesistente. Verificati controllo identico alla riserva leggera, bonus sopra il vecchio obiettivo tecnico L2, penalità di perdita, memoria dei guadagni saturi, protezione della pulizia esplicita e proprietà del bonus congiunto. Questi controlli non sono una valutazione delle Skills.

Riprodurre gli artefatti dai record pubblici già raccolti:

```sh
.venv/bin/python scripts/diagnose_growth_gaps.py lab/reports/financial-reserve-study/calibration-v1 lab/reports/growth-gap-study
.venv/bin/python scripts/analyze_growth_gap.py /Users/matteozabban/careerlab-data/matteo-growth-gaps/study-v1 lab/reports/growth-gap-study/study-v1
.venv/bin/python scripts/audit_growth_gap.py lab/reports/growth-gap-study/study-v1
.venv/bin/python scripts/analyze_growth_gap.py /Users/matteozabban/careerlab-data/matteo-growth-gaps/balanced-v1 lab/reports/growth-gap-study/balanced-v1
.venv/bin/python scripts/audit_growth_gap.py lab/reports/growth-gap-study/balanced-v1
.venv/bin/python scripts/analyze_growth_gap.py catalogue lab/reports/growth-gap-study
.venv/bin/python -m pytest -q
```

I runner rifiutano il riavvio delle cartelle già giocate. Un nuovo intervento richiede un nuovo protocollo; i risultati di questi due confronti restano separati.
