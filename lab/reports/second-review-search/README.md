# Esplorazione dei mesi 7–12 e della seconda promozione

26 ottobre 2026. Ricerca richiesta da Matteo: proseguire l'esplorazione del gioco con bot, senza usare quota IA e senza valutare manuali con un modello.

**Aggiornamento del 27 ottobre:** questo rapporto conserva la fotografia iniziale da 659 risposte. Lo [studio successivo del rischio](../trust-risk-study/README.md) ha incontrato e chiuso una fase ulteriore: il catalogo esteso è ora 644/644 risposte narrative e 661/661 totali. I numeri della raccolta originaria qui sotto restano invariati.

## Risultato e ambito

**1.183 partite nuove risolte, nessuna interruzione tecnica.** Ogni bot parte da una nuova partita e conserva il percorso completo dei mesi 1–12. Nessuno stato L2 è costruito artificialmente. Si fermano alla prima osservazione del mese 13 o alla morte; non viene eseguita alcuna azione nel mese 13.

Il catalogo dei **soli mesi 7–12** contiene **126 titoli narrativi, 264 fasi/domande e 642 risposte narrative**. Tutte le **642/642 risposte** sono state eseguite almeno una volta con successo. Includendo i due menu trimestrali, abbiamo **266 nodi e 659/659 risposte**, senza alternative incontrate ancora da provare. Rispetto al catalogo dei primi sei mesi, compaiono **37 titoli nuovi e 52 nuove fasi narrative**; le due finestre condividono anche molti scenari.

Questa è la copertura completa del **catalogo incontrato**, non di ogni possibile storia, stato nascosto o conseguenza oltre il mese 12. Il controllo indipendente ricostruisce tutte le alternative direttamente dagli archivi pubblici, verifica i tre hash ed esige una risposta `success: true`, applicata e non ambigua entro la finestra. Vedi [independent-coverage-audit.json](independent-coverage-audit.json).

## Come abbiamo usato il manuale senza un modello

Il riferimento congelato in ogni batch è [promotion-readiness-v2](../../policies-src/matteo-first-review/promotion-readiness-v2/bundle/skills/promotion-readiness/SKILL.md). Un programma Python non interpreta un manuale come farebbe un LLM: ne abbiamo implementato un'approssimazione esplicita, separata dal bundle di consegna.

- La scelta predefinita bilancia crescita, salute, dignità e avvisi di rischio. I confronti di effetti usano menu pubblici ed effetti nominali già raccolti attraverso i log ufficiali.
- Il bot ricorda investimenti trimestrali con beneficio visibile nullo, a parità di livello e mese, e riconsidera la ripetizione. Reagisce ad avvisi pubblici sul rischio e usa euristiche testuali generali per evitare alcuni comportamenti pericolosi.
- L'esplorazione sovrascrive esplicitamente questa scelta per eseguire alternative non provate o seguire un ramo dello stesso titolo. Alcune decisioni sono quindi deliberatamente dannose.
- Le varianti usano obiettivi numerici **ipotetici di ricerca**, non soglie del gioco identificate. Le varianti `balanced`, `risk` e `broad` cambiano la priorità; `low-dignity`, usata nella chiusura, cerca intenzionalmente stati sfavorevoli per raggiungere rami rari.
- `safe` significa soltanto assenza di deviazioni esplorative, non sicurezza certificata. I bot non implementano una comprensione completa delle promesse o della riservatezza: conserviamo l'intera storia per studiarle, ma non attribuiamo al bot una capacità semantica che non ha.

Gli effetti nominali vengono aggiornati dai log pubblici delle partite concluse. Le scelte successive dipendono quindi dall'esplorazione precedente e dall'ordine di completamento dei worker. Gli esiti non sono una stima dell'efficacia del manuale né un confronto causale tra varianti.

Nessuna chiamata a Claude, DeepSeek o altre API di modelli; nessun uso del budget di gioco IA. Il confronto 4+4 con Haiku resta fermo. Origine `matteotwelve`, dati e server isolati in `/Users/matteozabban/careerlab-data/matteo-second-review`; nessuna scrittura nel registro cloud e nessuna lettura degli interni del simulatore. Sono state usate soltanto le cinque interfacce pubbliche.

## Le tre esplorazioni

| Batch | Partite | Vive alla prima osservazione del mese 13 | Seconde promozioni | Seconde promozioni e vive |
|---|---:|---:|---:|---:|
| `discovery` | 48 | 16 | 9 | 7 |
| `exploration` | 768 | 418 | 308 | 266 |
| `closure` | 367 | 193 | 126 | 121 |
| Totale | **1.183** | **627** | **443** | **394** |

Il batch iniziale campiona le varianti e registra le prime risposte. Il secondo amplia la copertura con zero, una, tre o molte deviazioni esplorative. Il terzo si concentra sui rami mancanti e si arresta quando tutte le alternative conosciute risultano eseguite, completando le partite già iniziate. Il limite di 1.536 nuove partite di chiusura non è stato raggiunto.

Le versioni del runner sono conservate separatamente. Dopo `discovery`, il calcolo degli effetti medi include esplicitamente anche gli zeri per gli indicatori non menzionati nei log. In `closure` sono state rafforzate alcune penalità generali per risposte rischiose e introdotta l'esposizione a bassa dignità. Queste revisioni fanno parte della ricerca adattiva; non confrontare i batch come trattamenti randomizzati.

## Denominatori e promozioni

| Passaggio | Percorsi |
|---|---:|
| Nuove partite | 1.183 |
| Raggiungono vivi il mese 7 | 1.123 |
| Prima promozione entro il mese 6 | 812 |
| Prima promozione e vivi al mese 7 | 783 |
| Seconda promozione L2 → L3 entro il mese 12 | 443 |
| Seconda promozione e vivi alla prima osservazione del mese 13 | 394 |

Tra i **783** percorsi che entrano nel mese 7 già promossi e vivi, **443** ottengono la seconda promozione e **394** superano anche la finestra vivi. Gli stessi esiti restano riportati sul totale di 1.183 nuove partite: le morti precedenti non spariscono dal denominatore. I 204 percorsi ancora L1 alla seconda review possono ottenere lì la loro **prima** promozione; non li contiamo come seconde promozioni.

Le 49 morti dopo la seconda promozione sono etichettate dal gioco come 46 crisi di fiducia, due insolvenze e un collasso fisico. Due insolvenze sono rilevate alla transizione verso il mese 13, senza azioni eseguite in quel mese; l'outcome richiede di arrivare vivi a quella prima osservazione. Questi numeri includono scelte esplorative e non descrivono una probabilità di morte per un agente che segue il manuale.

## Pattern utili per la seconda promozione

### Preparazione prima del confine

Le **767** seconde review osservate avvengono tutte nel passaggio **11 → 12**. Le allocazioni osservate nei mesi **6 e 9** precedono quella decisione; il menu del mese 12 arriva dopo. Di conseguenza il percorso 7–12 eredita anche come sono state usate le risorse nel mese 6. Guardare soltanto le azioni dal mese 7 cancellerebbe una parte della preparazione.

Questi sono confini osservati in questa raccolta. Il manuale trasferibile deve parlare di preparazione prima della review effettiva, senza incorporare il calendario ricavato dalla ricerca.

### Il voto non identifica la promozione

Tra le **563** review di chi arriva già L2:

| Voto | Promossi L3 | Rimasti L2 |
|---|---:|---:|
| B | 378 | 14 |
| C | 65 | 106 |

Anche qui una C può accompagnare l'avanzamento e una B non lo garantisce. Servono controlli separati di voto, livello, avvisi e sopravvivenza.

### Dopo L2 va rivalutato il fabbisogno di crescita

I promossi L3 hanno Skill osservata dopo la risposta di review tra **18 e 21**. Il livello di preparazione dei primi mesi non può quindi essere usato automaticamente come obiettivo permanente. Gli effetti trimestrali mostrano inoltre investimenti positivi nominali senza guadagno netto a valori diversi dopo L2: **368** osservazioni di Network a 7, **120** di Output a 6 e **29** di Skill a 21.

Sono profili descrittivi e azioni correlate, non soglie di promozione o tetti universali. Il punto operativo è rivalutare il beneficio reale dopo il cambio di livello: un investimento fermo a L1 può diventare utile a L2, e uno utile può poi saturare nuovamente.

Non abbiamo identificato una formula esatta della seconda promozione. Le risposte della review possono includere l'effetto dell'ultima scelta, cambi di livello, avvisi, salario e altre conseguenze. Nei 419 promossi senza i due messaggi espliciti di esplosione simultanea, per esempio, Output dopo la risposta varia da 5 a 6; nel totale dei promossi può scendere fino a 1. Copiare valori post-review come requisiti pre-review sarebbe lo stesso errore già incontrato nello studio iniziale.

### La promozione ha conseguenze sulle relazioni

**443/443** seconde promozioni osservate includono il messaggio pubblico che collega l'avanzamento rapido a maggiore attrito con i vecchi contatti. In tutte queste risposte Network cala rispetto allo stato prima dell'ultima azione: il cambiamento netto va da −1 a −4, con −3 in 333 casi.

Il messaggio rende esplicito un meccanismo narrativo del gioco; la differenza numerica complessiva non isola però una penalità pura della promozione. La regola operativa candidata è prevedere un consolidamento delle relazioni dopo l'avanzamento, invece di dare per scontato che il sostegno precedente resti intatto.

### Le risorse economiche diventano una parte visibile della sopravvivenza

Oltre a fiducia e salute, compare spesso l'insolvenza nei percorsi esplorati. Negoziazioni, benefit, bonus, offerte esterne e carichi aggiuntivi ampliano gli scambi tra soldi, reputazione e sostenibilità. Va preservata una riserva economica quando si decide se accettare costi o sacrifici. Il conteggio di queste morti dipende anche dai limiti del bot: non prova che la finestra temporale causi di per sé un rischio finanziario maggiore.

### Le conseguenze attraversano i semestri

Sono registrati **84 collegamenti distinti e 294 ricorrenze** dello stesso titolo da una scelta entro il mese 6 a una fase nei mesi 7–12. Conserviamo scelta, stato e tempi dei due estremi in [same-title-chains.csv](same-title-chains.csv). Si tratta di continuità temporale osservata: non ogni ricorrenza dimostra da sola un nesso causale.

I nuovi scenari mantengono i grandi meccanismi già individuati: consegna tecnica, collaborazione e confini, integrità, riconoscimento e carriera, capacità sostenibile, apprendimento. Nei nuovi titoli diventano più visibili sicurezza e cambiamenti tecnici rischiosi, cambio di manager e fiducia, compensi e promesse economiche, salute e carichi ereditati. La classificazione è interpretativa; qui non pretendiamo una nuova partizione causale automatica.

## Dati consultabili

- [catalogue.md](catalogue.md): tutte le domande e risposte incontrate, mesi, livelli, conteggi e testimoni.
- [questions.json](questions.json): alternative, distribuzioni dei cambiamenti immediati, successori ed esiti associati. Gli esiti aggregati non sono effetti causali della singola risposta.
- [reviews.json](reviews.json): stato prima/dopo, ultima scelta, voto, avvisi ed esito di ogni review.
- [outcomes.json](outcomes.json) e [summary.json](summary.json): denominatori completi e condizionati, batch e morti.
- [patterns.json](patterns.json): pattern riproducibili, gruppi osservazionali all'inizio del mese 11 e limiti.
- [observed-edges.csv](observed-edges.csv) e [same-title-chains.csv](same-title-chains.csv): transizioni immediate e possibili continuazioni narrative, anche attraverso il semestre.
- [independent-coverage-audit.json](independent-coverage-audit.json): testimone pubblico verificato per tutte le 659 risposte.
- Cartelle `discovery`, `exploration`, `closure`: archivi completi `public-trajectories.jsonl.gz`, hash, manuale di riferimento, runner, ambiente, effetti iniziali e stato finale della copertura. Gli archivi includono anche tutto il prefisso 1–6.

L'ultima risposta mancante è stata eseguita in `closure/run363/step46`, mese 12, nel seguito della storia del collega remoto. È documentata nell'audit; le risposte esplorate non sono automaticamente raccomandazioni per gli agenti.

## Relevo

**Completato:** esplorazione 7–12 richiesta da Matteo, 1.183 partite risolte, copertura 642/642 risposte narrative e 659/659 totali, tre archivi pubblici verificati, analisi della seconda review e delle conseguenze successive. Tutti i worker sono terminati. Nessun modello di gioco, automatismo futuro o test di efficacia delle Skills avviato. Il manuale v2 e il confronto IA congelato sono rimasti invariati.

**Limiti e seguito:** nessuna garanzia di aver enumerato scenari non incontrati, stati nascosti o esiti oltre il mese 12. Gli effetti osservati ai confini temporali restano mescolati. L'implementazione dei bot è una traduzione incompleta del manuale, con ricerca empirica aggiunta: non rappresenta il comportamento di un agente. Per proseguire l'esplorazione si possono variare gli stati di ingresso e le priorità dei bot; se compaiono nuove domande, il catalogo va riaperto. Per i mesi successivi conservare le stesse storie e distinguere sempre avanzamento e sopravvivenza.

Validazione del software: sette controlli mirati su copertura temporale, distinzione prima/seconda promozione, sopravvivenza, effetti nominali, memoria di saturazione e audit indipendente. Suite completa: **260 test passati**, con il warning Authlib preesistente. Questo controllo del codice non è una valutazione dei manuali.

Riprodurre gli artefatti dai record pubblici esterni già raccolti:

```sh
.venv/bin/python scripts/analyze_second_review.py /Users/matteozabban/careerlab-data/matteo-second-review lab/reports/second-review-search
.venv/bin/python scripts/audit_second_review.py lab/reports/second-review-search
.venv/bin/python scripts/second_review_patterns.py lab/reports/second-review-search
.venv/bin/python -m pytest -q
```

Per una nuova esplorazione senza IA, usare una cartella di output nuova e i batch esistenti come esperienza pubblica, ad esempio:

```sh
.venv/bin/python scripts/second_review_search.py \
  --output /Users/matteozabban/careerlab-data/matteo-second-review/further-exploration \
  --prior /Users/matteozabban/careerlab-data/matteo-second-review/discovery \
          /Users/matteozabban/careerlab-data/matteo-second-review/exploration \
          /Users/matteozabban/careerlab-data/matteo-second-review/closure \
  --runs 192 --workers 4 --seed 450026
```

Questo comando non è stato eseguito e non è pianificato. Una raccolta futura può rivelare nuove alternative anche se oggi tutte quelle incontrate sono coperte.
