# Indice del lavoro di Matteo

27 ott 2026. Tutto il lavoro di Matteo è raccolto nella branch **`matteo/main`**, al posto di 15 branch separate. Questa pagina mette le scoperte in ordine di importanza e rimanda ai report che le dimostrano.

Livelli di affidabilità usati sotto:
- **solida:** confermata con molte partite o in modo indipendente da Ale;
- **pilota:** 8–9 partite Haiku, al limite del rumore (circa 19 punti per partita);
- **ipotesi:** da verificare.

## A. Scoperte che decidono la partita

| # | Scoperta | Affidabilità | Dove |
|---|---|---|---|
| A1 | **La prima promozione decide la carriera.** Chi sale alla prima review fa in media circa 57; chi è ancora in L1 alla seconda, circa 22. Quasi tutte le sconfitte sono il licenziamento al mese 24 dopo quattro review C/D. | solida (anche Ale e la nube) | [promotion-study](../../lab/reports/matteo-promotion-study.md), [scenario-patterns](../../lab/reports/scenario-patterns/README.md) |
| A2 | **La review si applica all'inizio del mese**, prima degli eventi e della distribuzione di quel mese. Conta lo stato dopo l'ultima decisione del mese precedente. Tutte le 1.940 prime review osservate cadono nel passaggio dal mese 5 al 6, sempre con voto C. | solida | [promotion-study](../../lab/reports/matteo-promotion-study.md), [scenario-patterns](../../lab/reports/scenario-patterns/README.md) |
| A3 | **La promozione è deterministica:** S, N e O devono essere almeno alla soglia del livello, con Dignity non bassa. In L1 Network e Output devono stare al tetto, quindi **un punto perso al mese 5 costa la promozione**. Correzione: la "moneta al 55 %" era un errore di misura. | solida (confermata da Ale: 221 su 221 promossi tra quelli in soglia) | [v9, correzione](../../lab/reports/matteo-observed-growth-v9.md) |
| A4 | **Il punto si perde per rigidità "di principio".** Nei due mesi prima della review, 98 scelte su 377 tolgono N o O. Rifiutare o bloccare: 17 perdite e 1 guadagno. Collaborare o parlarne in privato: 7 perdite e 23 guadagni. | pilota (9 partite v7) | [v7](../../lab/reports/matteo-observed-growth-v7.md), [v8](../../lab/reports/matteo-observed-growth-v8.md) |
| A5 | **Le regole del manuale cambiano poco le scelte di Haiku nelle storie**, mentre la distribuzione trimestrale la governano. Ale ha mostrato poi che dove il manuale comanda c'è poco punteggio. | solida (con T20 di Ale) | [v10–v12](../../lab/reports/matteo-observed-growth-v10-v12.md) |
| A6 | **In L4 Skill è il collo di bottiglia.** Circa il 70 % delle azioni va su N/O già al tetto. Haiku usa raramente rotation e Skill learning, anche quando glielo si dice. | pilota | [v10–v12](../../lab/reports/matteo-observed-growth-v10-v12.md) |
| A7 | **Token:** circa 670.000 al mese con DeepSeek (dato F1). Arrivare al mese 48 vale molto più che accorciare il manuale: una partita interrotta ha la voce token limitata a 50. | stima | nota in questa pagina |

## B. Manuali (famiglia observed-growth), dal migliore

Tutti sono in `lab/policies-src/matteo-feedback-growth/` e giocati con Haiku, attore `017798b931bc18f8` (CLI 2.1.310), salvo dove indicato.

| Manuale | Partite | Q media | Terminate | Cosa cambia | Esito |
|---|---:|---:|---:|---|---|
| **v10** | 8 | **59,56** | 7/8 | v9 + regola "Capped" + meccanica di Ale (Dignity, rischio, soldi, mai High-intensity) | **candidata migliore**; ma la regola Capped non viene eseguita, quindi rispetto alla v7 la differenza è probabilmente rumore |
| bhr (M1 + BUILD/HOLD/REPAIR) | 8 | 59,49 | 7/8 | memoria nelle note + modalità esplicite | identica alla v10 (5/8 in L5, prima review 4/8); [report](../../lab/reports/matteo-bhr-haiku.md) |
| bhr-cooperate (BHR + contatore + "engage, don't distance" nel mese prima della review) | 8 | 48,92 | 5/8 | regola visibile al posto della checklist dei costi | prima review **6/8** con Network al tetto 8/8; ma 2 crisi di fiducia, 1 esaurimento, 2/8 in L5: peggiore di BHR; [report](../../lab/reports/matteo-bhr-cooperate.md) |
| bhr-countdown (BHR + contatore e checklist del mese 5) | 8 (fermate al mese 6–11) | — | — | contatore `Review in N` + marcature N/O | **scartata**: prima review 2/8 (BHR 4/8), 1 esaurimento; marca le opzioni ma non vede quale costa Network; [report](../../lab/reports/matteo-bhr-countdown.md) |
| m1 (v10 + checkpoint nelle note) | 1 | 64,06 | 1/1 | memoria fattuale nelle note | chiusa in L5; una partita sola; [report](../../lab/reports/matteo-m1-haiku.md) |
| v7 | 9 | 57,56 | 7/9 | regole v6 con riga di stato fissa | PR #13. Nel test di Ale, 40 % promossi alla prima review contro 47 % di f3-lean: nessuna differenza |
| v3 | 8 | 51,04 | 5/8 | ripristinata la pulizia del rischio | il primo 71,4 era fortuna; nella gara: 61, 19, 52, 64 |
| v6 | 8 | 50,08 | 6/8 | regole del promotion-study | in gara 5 di 8 |
| v12 | 1 | 50,2 | 0/1 | meccanica esatta (scala HR, Lay low) | 1 partita, crisi di fiducia al mese 43; non informativa |
| v9 | 8 (fino al mese 12) | — | — | "honest without rigidity" | 4/8 in soglia alla prima review (valore corretto) |
| v8 | 8 (fino al mese 12) | — | — | "honest and collaborative" | 5/8 fuori da L1; tiene N, perde O |
| v11 | parziale | — | — | blocco di Skill basato sulle review | fermata da Matteo |
| v2 | 4 | 43,18 | 2/4 | — | 2 crisi di fiducia, quasi niente Defuse |
| v1 | 1 + 4 | 64,78 / 40,85 | 1 + 1/4 | prima sintesi | il pilota locale non si replica |
| v4 / v5 | 4 / 4 | 32,76 / 30,32 | 1/4 / 1/4 | crescita / soldi | scartate |
| value-conversion-v1 | 4 in gara | — | — | conversione di valore | sotto il leader |

Altri manuali: `matteo-first-review/promotion-readiness-v1/v2` (Codex, mai testato con un modello) e `matteo-memory/champion-memory-v1` (preparato, non registrato).

## C. Errori e correzioni da ricordare

1. **Il 71,4 della v3 era fortuna:** su 8 partite fa 51,04. La stessa cosa è successa a f1 con la riga di stato e ad altri campioni. Mai scegliere un manuale con 4 partite.
2. **Errore di misura sulla promozione:** si leggeva lo stato prima dell'ultima decisione del mese 5. La v9 era 4/8, non 6/8. La correzione è nel report v9 e nella PR #15.
3. **La regola "Capped" della v10 non viene eseguita da Haiku:** una regola che chiede al modello di accorgersi di un effetto nascosto non funziona.
4. **Versione della CLI:** un aggiornamento automatico (2.1.311) cambia l'attore. Per confrontare va bloccata la 2.1.310.

## D. Studi con bot (senza quota IA)

| Studio | Cosa ha trovato | Dove |
|---|---|---|
| Promotion study | review all'inizio del mese; tetto visibile al momento della review | [report](../../lab/reports/matteo-promotion-study.md) |
| First-review search | catalogo completo dei primi 6 mesi; politica di ricerca al 65,6 % di promozioni | [report](../../lab/reports/first-review-search/README.md) |
| Known-catalogue closure | 510/510 risposte narrative coperte almeno una volta | [report](../../lab/reports/known-catalogue-closure/README.md) |
| Scenario patterns | sei meccanismi ricorrenti; 25 titoli su 89 compaiono solo dopo la prima review | [report](../../lab/reports/scenario-patterns/README.md) |
| Second-review search | mesi 7–12 e seconda promozione | [report](../../lab/reports/second-review-search/README.md) |
| Trust-risk study | memoria degli incidenti e sopravvivenza nel primo anno | [report](../../lab/reports/trust-risk-study/README.md) |
| Financial reserve | riserva leggera e sostenibile; nessuna intensità ottimale dimostrata | [report](../../lab/reports/financial-reserve-study/README.md) |
| Growth gap | 1.152 partite: nessuna priorità di crescita batte il controllo | [report](../../lab/reports/growth-gap-study/README.md) |
| Constrained growth | 576 partite: crescita con vincoli di sostenibilità | [report](../../lab/reports/constrained-growth-study/README.md) |
| Consistency with Ale | i nostri pattern confrontati con i suoi | [report](../../lab/reports/consistency-with-ale/README.md) |
| Manual memory / memory pilot | inventario e costo della memoria nei manuali | [report](../../lab/reports/manual-memory/README.md), [pilota](../../lab/reports/memory-pilot/README.md) |
| Strategia e pannello | manuale promotion-readiness e pannello visuale | [strategia](../../lab/reports/promotion-strategy/README.md), [pannello](../../lab/reports/research-dashboard/README.md) |
| Prime simulazioni random | 73.858 partite random; nessuna arriva alla fine | [legacy](legacy/docs/exploratory-findings.md) |

**Attenzione:** `lab/reports/first-review-search/` contiene un catalogo di eventi del gioco di sviluppo. È solo materiale di studio: non va mai copiato in un manuale né passato ai progettisti.

## E. Strumenti

- `scripts/promotion-study/run.py` e `analyse.py`: bot e analisi della promozione.
- `research/matteo/legacy/tools/local-game/`: la prima interfaccia browser per giocare a mano.
- `research/matteo/legacy/solution/`: le prime tre Skills (M3) e i primi documenti di design.
- Dati delle partite: `lab/registry-origins/matteo/*.jsonl`. Il registro unito ha 54 valutazioni, senza duplicati.

## F. Le branch vecchie (da dove viene ogni cosa)

Ogni commit di queste branch è antenato di `matteo/main`: non si è perso niente. Per ricreare una branch: `git branch <nome> <sha>`.

| Branch | SHA di punta | Ultima modifica | Contenuto |
|---|---|---|---|
| `Matteo` | b6e1d638c4 | 26 ott | prima interfaccia, Skills M3 e random (ora in `research/matteo/legacy/`) |
| `matteo-t4-growth` | 3113433ac5 | 27 ott | studi con bot di Codex (sezione D). **Resta aperta**: Codex ci lavora ancora dal Mac |
| `matteo/promotion-study` | 7da7bd5951 | 26 ott | studio della promozione |
| `matteo/observed-growth-v2` … `-v5` | 6f097c2605, 9cff533553, dcade953ba, 3d1bea6c22 | 26 ott | manuali v2–v5 |
| `matteo/observed-growth-v6` | 63bd04c2d1 | 26 ott | v6 e le 2 partite riprese |
| `matteo/observed-growth-v7` … `-v9` | 16a78bd60a, 8debfde644, 94ab5d300a | 26–27 ott | v7–v9 (PR #13 e #15) |
| `matteo/observed-growth-v10` … `-v12` | 04e136797f, d1458408bc, 8b7f990f87 | 27 ott | v10–v12 |
| `matteo/confronto-v10` | aefd1f3c99 | 27 ott | richiesta di confronto con Ale (PR #18 chiusa) |

## Relevo

1. **Fatto:** 15 branch unite in `matteo/main` con merge veri, senza squash, così tutta la storia resta. Conflitti risolti così:
   - `ESTADO.md`: la versione più recente, con la riga T4 sintetizzata;
   - registro `evaluations.jsonl`: unione delle righe, senza duplicati;
   - `README.md` e `.gitignore`: quelli di `main`, con la riga in più del vecchio `.gitignore`;
   - la vecchia branch `Matteo`: spostata in `research/matteo/legacy/`, con il suo README salvato lì.

   Test: 352 passati.
2. **Non riuscito:** creare tag di backup su GitHub (il proxy della sessione non lo permette). Al loro posto c'è la tabella F.
3. **Prossimo passo:** unire `matteo/main` in `main` (PR unica). Se vengono partite DeepSeek della v10, i risultati vanno in questa pagina, sezione B. Il campo `instruction` del manifest della v10 va compilato in inglese prima di consegnarla.
