# Easter eggs: esistono scorciatoie per saltare livelli?

**Conclusione:** no, non con le risposte alle storie. Su 8.691 partite (6.291 vecchie + 2.400 nuove che forzano apposta le risposte mai o quasi mai esplorate) ogni promozione è +1, avviene solo alla review semestrale e solo con Skill e Output alla soglia. Nessuna storia, riga di sistema o catena nuova.

Linea di Matteo, rama `matteo/easter-eggs`, 28 ott 2026. Domanda nata da voci sul canale Discord secondo cui esistono combinazioni nascoste (interazioni con persone rilevanti) che fanno saltare livelli. Costo: zero API, zero quota Claude (solo bot scriptati sul motore ufficiale in locale).

## 1. Rilettura dei log esistenti (gratis)

`lab/data/ingenieria-inversa/*`: 6.291 partite, 662.701 decisioni, 406 nodi evento.

| Controllo | Risultato |
|---|---|
| Cambi di livello | 13.633, tutti +1 e tutti al mese di review |
| Salti di due livelli, promozioni fuori review, retrocessioni | 0 |
| Promozioni con Skill o Output sotto soglia | 7 su 13.633, tutte L1 al mese 6 con Output 2 su 3. Artefatto: lo stato registrato è prima dell'ultima risposta del mese 5, che dà il +1 mancante |
| Storie "di carriera" (karaoke con il panel, VP nuovo, director alla festa, *A promotion without a pay rise*, *IC or management?*, *Stuck on the ladder*) | Solo i soliti delta (±1/±3 su Network, Skill, Dignity, Output). Nessun effetto sul livello |

Il punto cieco: 192 risposte viste meno di 30 volte (139 storie) e 20 risposte di follow-up mai viste, perché l'oracolo le evita. Un easter egg, se esiste, starebbe lì.

## 2. Bot che forza le risposte rare

`scripts/ingenieria-inversa/prober.py`: l'oracolo `m02r` (gioca bene per arrivare in fondo) che, davanti a una storia bersaglio, sceglie la risposta meno esplorata (conteggio del catalogo v2 + quante volte l'ha già forzata), e fa lo stesso con qualsiasi storia fuori catalogo. Tre modalità, 800 partite ciascuna, motore ufficiale 1.0.6 / dataset 1.0.8, valori del runner ufficiale.

| Lotto | Bersagli | Risposte forzate | Coppie storia-risposta diverse | Livello finale (L5 / L6 / L7) | Anomalie di livello | Storie o righe nuove |
|---|---|---:|---:|---|---:|---:|
| `ee-never` | solo risposte mai viste | 156 | 9 | 171 / 535 / 1 | 0 | 0 |
| `ee-career` | mai viste + tutte le rare delle storie di carriera | 6.013 | 54 | 290 / 370 / 0 | 0 | 0 |
| `ee-rare` | ogni risposta vista < 30 volte | 13.398 | 182 | 144 / 13 / 0 | 0 | 0 |

- 2.400 partite, 8.985 promozioni: tutte +1, tutte alla review.
- 3 promozioni "sotto soglia" (Output 2 su 3 a L1, 13 su 14 a L3): ancora l'artefatto di misura, verificato partita per partita (l'ultima risposta del mese precedente dà Output +1).
- Zero titoli di storie e zero righe di sistema normalizzate che non fossero già nelle 6.291 partite vecchie, anche dopo le risposte mai prese prima. I follow-up delle risposte forzate sono storie già note.
- Forzare le risposte rare peggiora la carriera (in `ee-rare` quasi tutti si fermano a L4–L5): sono rare perché sono peggiori, non perché nascondono qualcosa.

## 3. Limiti

- Delle 20 risposte mai viste se ne sono raggiunte 9: le altre sono follow-up di catene che compaiono raramente. Coprirle richiederebbe un bot che insegue la catena dalla storia madre.
- Si esplorano solo le scelte del giocatore (storie, energia, azione trimestrale). Non si è guardato dentro il motore (NORMAS §4) né provato input fuori dalle opzioni offerte.
- Il dataset di sviluppo può differire da quello della valutazione ufficiale; se l'easter egg di cui parla Discord è nel set di test, qui non si vede.

## Relevo

1. **Fatto:** rilettura dei log esistenti; bot `prober` con tre modalità; 2.400 partite; analisi contro la baseline.
2. **Dati:** `~/careerlab-data/easter-eggs/ee-{never,career,rare}/` e `summary.json` (fuori Git: contengono testo del gioco). Per rigenerarli:
   ```bash
   uv sync && uv run career-emulator-engine update --source distribution --split dev
   export BB_DATA=~/careerlab-data/easter-eggs
   M=$PWD/lab/data/ingenieria-inversa/models/m02r.json
   PYTHONPATH=. .venv/bin/python scripts/ingenieria-inversa/run.py --batch ee-rare --policy prober --games 800 \
     --procs 2 --slots 3 --kw "{\"model\":\"$M\",\"mode\":\"rare\",\"review_boost\":5.0,\"skill_focus_from\":3,\"w_skill_hi\":2.0,\"detonators\":true}"
   python3 scripts/easter-eggs/analyze.py
   ```
   Circa 20 minuti per 800 partite con 2 core.
3. **A metà:** le 11 risposte mai viste non raggiunte.
4. **Prossimo passo, solo se Discord dà un indizio concreto** (livello, mese, tipo di interazione): bot che insegue quella catena specifica. Altrimenti la linea si può chiudere e il risultato va in HALLAZGOS come livello A: "nessuna scorciatoia di livello nelle scelte del giocatore".
