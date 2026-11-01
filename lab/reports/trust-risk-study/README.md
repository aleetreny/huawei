# Fiducia, memoria degli incidenti e sopravvivenza nel primo anno

27 ottobre 2026. Studio richiesto da Matteo dopo l'esplorazione dei mesi 7–12. Solo bot Python e strumenti pubblici: nessuna chiamata a modelli IA e nessuna valutazione delle Skills con agenti.

**Seguito del 27 ottobre:** lo [studio della riserva economica](../financial-reserve-study/README.md) ha ora isolato due interventi economici dalla nuova partita e incontrato un'altra fase narrativa. Il catalogo conosciuto dei mesi 7–12 è esteso a 646/646 risposte narrative e 663/663 totali. I risultati di rischio e la fotografia da 661 risposte qui sotto restano quelli di questa raccolta.

## Risultato principale

Il segnale più chiaro è **cambiare prudenza dopo un incidente**, anziché affidarsi soltanto a ripulire il rischio corrente. Nel confronto randomizzato del bot congelato, la guardia che conserva la storia degli incidenti e usa associazioni empiriche di rischio porta le crisi di fiducia da **20/256 a 4/256**. La seconda promozione con sopravvivenza passa da **174/256 a 194/256**.

Il confronto riguarda un pacchetto preciso: memoria persistente **più** un catalogo empirico di risposte con esiti avversi. Non isola il solo effetto di ricordare, non scopre il vero contatore nascosto del gioco e non dimostra che un agente otterrà gli stessi risultati leggendo una regola generale.

La sola modifica del momento di una pulizia aggiuntiva non dà un vantaggio chiaro in questo campione. Questo non dimostra che la pulizia sia inutile: il confronto include il costo opportunità della crescita sostituita e non è abbastanza preciso da escludere effetti moderati.

## Prima osservazione: cosa era successo nei 46 crolli precedenti

L'audit parte dai 46 percorsi del precedente studio morti per crisi di fiducia **dopo** la seconda promozione. Tutti avevano già eseguito almeno una riduzione del rischio; 14 l'avevano eseguita nei mesi 3, 6 e 9. In 39 casi c'è una pulizia successiva al primo messaggio pubblico di esplosione, ma il percorso termina comunque in crisi.

La scelta finale proviene dal normale criterio del bot in 41 casi e da una deviazione esplorativa in cinque. La memoria del bot riporta nessun avviso corrente in 13 casi, avviso lieve in sette e forte in 26. Questa memoria può essere obsoleta e non coincide con il rischio reale.

Sono **fallimenti selezionati**, quindi non misurano l'efficacia della pulizia. Mostrano però che una pulizia o un segnale momentaneamente calmo non sono una prova pubblica sufficiente per cancellare la storia di un incidente. Tutti i percorsi e i riferimenti sono in [retrospective.json](retrospective.json).

## Esplorazione controllata congelata prima delle nuove partite

Il protocollo è [factorial-v1/protocol.json](factorial-v1/protocol.json), accompagnato da hash, copie del codice e dei due modelli empirici. Nessun aggiornamento online degli effetti o delle frequenze durante la raccolta. Gli input sono dieci archivi pubblici già esistenti: sette della prima esplorazione e tre della seconda.

Abbiamo avviato **713 nuove partite** per ottenere **512 assegnazioni eleggibili**. Ogni percorso parte da zero, segue lo stesso bot prima dell'assegnazione e diventa eleggibile al primo menu energetico completo del mese 6, vivo e già L2. La scelta casuale avviene prima dell'intervento, in blocchi permutati delle otto combinazioni, per **64 percorsi per combinazione**.

Gli altri 201 tentativi restano documentati: 190 percorsi vivi ma non eleggibili, fermati al termine del prefisso; dieci morti prima dell'eleggibilità; uno fermato senza assegnazione perché la sequenza era già completa. Non sono zeri nel denominatore assegnato, né carriere completate. Tutte le 512 assegnazioni hanno un esito pubblico risolto, senza interruzioni tecniche. Il limite iniziale di 1.024 tentativi non è stato raggiunto.

I tre fattori sono:

| Fattore | Disattivato | Attivato |
|---|---|---|
| Prevenzione anticipata | Due preparazioni di report + un recupero salute al menu del mese 6 | Una riduzione rischio + un recupero salute al menu del mese 6 |
| Prevenzione tardiva | Stesso piano di crescita al menu del mese 9 | Stesso piano di riduzione rischio al menu del mese 9 |
| Guardia dopo incidente | Normale scelta narrativa del bot congelato | Dopo un precedente messaggio pubblico di esplosione, penalità alle alternative associate storicamente a risposte avverse |

Entrambi i piani energetici costano tre punti e includono un recupero salute. Cambiano anche Output e Dignity guadagnabili dai report: stimiamo **il pacchetto e il suo costo opportunità**, non un effetto puro della riduzione rischio. Il prefisso e gli altri momenti conservano la politica comune; “disattivato” non significa che il bot non abbia mai fatto pulizia altrove.

La guardia usa una frequenza smussata, congelata, di risposte contenenti i messaggi pubblici di esplosione o crisi. Una risposta avversa può dipendere anche dalla storia e dal regolamento automatico: quella frequenza è un indicatore empirico, non un'etichetta causale della singola alternativa. La guardia resta fuori dalle Skills e non è un oracolo del rischio.

## Esiti e incertezza

L'outcome principale è la morte per crisi di fiducia entro la prima osservazione del mese 13. Il denominatore è assegnato al mese 6: non selezioniamo retrospettivamente chi sopravvive o chi ottiene la seconda promozione.

La tabella aggrega ciascun fattore sulle quattro combinazioni degli altri due; ogni lato contiene **256 percorsi**:

| Fattore | Crisi: disattivato → attivato | Seconda promozione e vivi: disattivato → attivato |
|---|---:|---:|
| Prevenzione anticipata | 12 → 12 | 180 → 188 |
| Prevenzione tardiva | 14 → 10 | 185 → 183 |
| Guardia dopo incidente | **20 → 4** | **174 → 194** |

Per la guardia, la differenza di crisi è **−6,25 punti percentuali**, con intervallo esplorativo al 95% di circa **−10,31 a −2,65**. Per la seconda promozione con sopravvivenza è **+7,81 punti**, intervallo circa **+0,02 a +15,48**: questo secondo segnale è molto meno preciso. Gli intervalli non sono corretti per confronti multipli e non costituiscono una dichiarazione confermativa di superiorità.

Per la prevenzione anticipata, l'intervallo della differenza di crisi va da circa −3,87 a +3,87 punti; per quella tardiva da −5,49 a +2,26. Non abbiamo una base per proclamare un calendario ottimale di pulizia.

Nel complesso delle 512 assegnazioni: **382 seconde promozioni, 368 con sopravvivenza, 438 sopravvissuti**, 24 morti per crisi di fiducia e 50 per insolvenza. Le combinazioni individuali e gli intervalli delle proporzioni sono in [results.json](factorial-v1/results.json); non selezioniamo la combinazione con il miglior piccolo campione come nuova regola vincente.

I gruppi distinti per un incidente **precedente all'assegnazione** sono anch'essi salvati. Fra chi ne aveva già uno, le crisi sono 12/41 senza guardia e 4/48 con guardia. Senza incidenti precedenti, sono 8/215 e 0/208; la guardia può comunque attivarsi dopo un primo incidente successivo. Sono sottogruppi piccoli e non dimostrano una protezione universale.

Il controllo indipendente ricostruisce il momento di assegnazione, verifica che la memoria non usi informazioni future, confronta la sequenza con il protocollo, controlla le azioni offerte e ricava gli esiti dagli stati pubblici. Tutti i 512 piani iniziali sono consegnati integralmente; tutti i 485 percorsi che raggiungono il piano successivo lo completano. Nessuna difformità. Vedi [independent-audit.json](factorial-v1/independent-audit.json).

## Il problema economico nasce spesso prima della seconda finestra

I 50 morti per insolvenza costituiscono ora la maggior parte delle morti del campione assegnato. **46/50 avevano già Wealth pari o inferiore a zero al momento dell'assegnazione nel mese 6**: 24 a zero, 15 a −1 e sette a −2. La prima perdita visibile di ciascuno avviene entro il mese 6.

In 43 di questi percorsi compare una perdita visibile associata alla scelta di finanziare favori relazionali tramite acquisti ripetuti; in 35 compare già nel prefisso. Questo è un audit di casi selezionati, non un confronto randomizzato della spesa. I cambiamenti netti possono inoltre includere altre conseguenze.

La diagnosi concreta è che il bot valorizza capacità e relazioni ma **non assegna un peso economico esplicito alle perdite di Wealth**. L'euristica prudente sugli incidenti non risolve questa lacuna. La protezione delle risorse va quindi studiata dall'inizio della carriera, anziché attivarla solo una volta raggiunto L2. La sua efficacia incrementale non è stata ancora isolata. Tutte le perdite e gli stati iniziali sono in [financial-failure-audit.json](financial-failure-audit.json).

## Catalogo ampliato e richiuso

La nuova ricerca ha incontrato una fase ulteriore di un titolo già noto. Nel campione randomizzato era stata eseguita una sola delle due risposte. Una ricerca mirata separata di **10 nuove partite**, senza IA, ha esercitato anche l'altra risposta. Queste dieci partite non entrano nei risultati randomizzati.

L'audit combinato dei vecchi e nuovi archivi, per la finestra dei mesi 7–12, copre ora **126 titoli, 265 fasi narrative e 644/644 risposte narrative**. Con i menu, **267 nodi e 661/661 risposte**, senza alternative incontrate rimaste aperte. Sono controllati 1.906 record dei cinque archivi, inclusi i prefissi parziali dichiarati. I 713 tentativi più le dieci partite mirate costituiscono le **723 nuove partite avviate** da questo studio; non sono 723 carriere complete fino al mese 12.

Il precedente catalogo da 659 risposte resta una fotografia valida dei dati allora raccolti. Il nuovo seguito è un esempio concreto del motivo per cui “tutte le risposte incontrate” non significa “tutti gli scenari possibili”. La nuova fase e i testimoni di ogni risposta sono in [extended-questions.json](extended-questions.json); integrità, provenienza e assenza di alternative mancanti sono in [extended-coverage-audit.json](extended-coverage-audit.json).

## Regole generali candidate

La sintesi operativa è in [first-year-strategy-draft.md](first-year-strategy-draft.md). Contiene principi trasferibili, senza titoli, risposte fisse, soglie nascoste o mesi prescritti:

1. Tenere separata la memoria degli incidenti dagli avvisi correnti e dalle azioni di pulizia.
2. Dopo un incidente, aumentare la prudenza su scorciatoie, divulgazioni e promesse; richiedere salvaguardie e seguito verificabili.
3. Proteggere la riserva economica fin dall'inizio, insieme a salute e dignità.
4. Continuare a diagnosticare crescita, relazioni e risultati; rivalutare il fabbisogno dopo ogni promozione.
5. Prepararsi prima della review e consolidare le relazioni dopo l'avanzamento.

Le prime due regole sono motivate dal confronto del pacchetto memoria/lookup, ma quel confronto **non valida direttamente questo testo**. La regola economica nasce dall'audit e richiede ancora un intervento isolato. Non abbiamo istruzioni garantite per ogni agente o ogni storia.

## Relevo

**Completato:** ricostruzione dei 46 crolli precedenti, protocollo congelato prima della raccolta, 512 assegnazioni risolte in otto combinazioni, audit indipendente degli esiti e dei piani, analisi economica, chiusura della nuova fase con dieci bot, catalogo esteso e bozza generale del primo anno. Nessun modello di gioco, quota IA, automazione o registro cloud utilizzato. Origine isolata `matteotrust`; dati esterni in `/Users/matteozabban/careerlab-data/matteo-trust-study`. Tutti i worker sono terminati. I bundle di Skills esistenti e il confronto Haiku congelato non sono stati modificati.

**Limiti:** risultati relativi al bot empirico e alla popolazione già promossa al menu del mese 6. Il denominatore non misura l'efficacia di una strategia per tutte le nuove carriere. Il catalogo e le frequenze storiche non sono un manuale trasferibile. Le conseguenze oltre il mese 12 non sono osservate. L'assenza di un beneficio chiaro della sola pulizia non equivale a inutilità.

**Seguito eseguito dopo questa raccolta:** la protezione economica nel prefisso è stata isolata con assegnazione casuale dalla nuova partita, mantenendo fissa la prudenza sugli incidenti e misurando le promozioni sull'intero denominatore iniziale. Le due raccolte e i loro limiti sono nello [studio economico](../financial-reserve-study/README.md). Nessuna ulteriore attività è pianificata automaticamente.

Validazione del software: **267 test passati**, con il warning Authlib già esistente. I controlli aggiunti verificano eleggibilità, fattori, costo uguale e recupero, memoria persistente, frequenze congelate, incertezza con zero eventi e ricostruzione della storia. Gli audit pubblici dei 512 esiti e delle 661 risposte sono completati. Questi controlli del codice non sono una valutazione delle Skills.

Riprodurre analisi e audit dai record pubblici raccolti:

```sh
.venv/bin/python scripts/analyze_trust_risk.py retrospective lab/reports/second-review-search lab/reports/trust-risk-study
.venv/bin/python scripts/analyze_trust_risk.py /Users/matteozabban/careerlab-data/matteo-trust-study/factorial-v1 lab/reports/trust-risk-study/factorial-v1
.venv/bin/python scripts/audit_trust_risk.py lab/reports/trust-risk-study/factorial-v1
.venv/bin/python scripts/extend_second_catalogue.py lab/reports/second-review-search lab/reports/trust-risk-study /Users/matteozabban/careerlab-data/matteo-trust-study/catalogue-closure
.venv/bin/python -m pytest -q
```

Il runner rifiuta un riavvio della cartella già utilizzata. Codice, modelli, protocollo, assegnazioni, fonti e hash sono conservati in `factorial-v1`; i record integrali sono nell'archivio compresso. La ricerca mirata è archiviata separatamente in `catalogue-closure`. Non cambiare il protocollo per incorporare retrospettivamente le conclusioni.
