# bhr-cooperate: 8 partite Haiku

27 ott 2026. Manuale `lab/policies-src/matteo-memory/bhr-cooperate` (sostituisce `bhr-countdown`, rimosso). È BHR più:
- il contatore `Review in N` all'inizio di ogni nota;
- solo quando N = 1, la regola "scegli l'opzione che coinvolge la persona, mai quella che prende le distanze; non rimandare il tuo lavoro; sempre onesto";
- una protezione per la salute.

La regola nasce dai dati: tutte le perdite di Network nel mese 5 delle partite BHR e bhr-countdown venivano da opzioni "di distanza". Attore `017798b931bc18f8`, lo stesso di BHR. Job `matteo-pilo-1ebd52f3-017798-0000{0..7}-a1`.

## Risultato

**Q media 48,92 (deviazione standard 15,7, errore standard 5,5); 5 su 8 completate; 2 su 8 chiuse in L5.** BHR aveva fatto 59,49, con 7 completate e 5 in L5.

| Partita | Q | Mesi | Livello finale | Esito |
|---|---:|---:|---|---|
| 00 | 62,70 | 48 | L5 | |
| 03 | 61,35 | 48 | L5 | |
| 04 | 59,40 | 48 | L4 | |
| 02 | 54,35 | 48 | L4 | |
| 01 | 52,33 | 48 | L4 | |
| 07 | 48,23 | 41 | L4 | crisi di fiducia (esplosioni ai mesi 18 e 41) |
| 05 | 36,94 | 37 | L4 | crisi di fiducia (esplosioni ai mesi 15 e 37) |
| 06 | 16,07 | 12 | L2 | esaurimento al mese 12 |

## Lettura

- **La prima review migliora: 6 promosse su 8** (BHR 4/8, bhr-countdown 2/8). **Network è al tetto in tutte e 8.** La regola "non prendere le distanze" fa quello che doveva fare nel mese 5. Le due bocciate hanno perso Output.
- **Peggiora tutto il resto:**
  - 2 crisi di fiducia (BHR: 0) e 1 esaurimento;
  - meno L5 (2 contro 5): Output resta basso in L3 e la 05 è rimasta ferma tre review con O 13.
- Le crisi di fiducia: su 4 esplosioni, solo 1 viene subito dopo una scelta del mese N = 1 (07, mese 18). Le altre arrivano in mesi in cui la regola non si applicava, ma con avvertimenti di HR non risolti da mesi. Sono possibili due spiegazioni: o la regola "assecondare" si estende anche agli altri mesi (la contaminazione misurata da Ale), oppure è rumore. Con 8 partite non si può distinguere.
- Con 8 partite per lato la differenza di Q media (−10,6, errore standard circa 7,6) è al limite del rumore. Però la direzione è negativa e i meccanismi di sconfitta sono nuovi.

## Conclusione

**Non sostituisce la v10 né BHR.** Resta una scoperta utile: nel mese prima della review la perdita di Network si elimina con "engage, don't distance" (8/8 al tetto). Ma serve un modo di applicarla senza far crescere il rischio nascosto. Per esempio: limitarla al mese 5 della prima review, oppure aggiungere "un avvertimento di HR non risolto ha la precedenza: Defuse e Lay low".

## Relevo

1. **Fatto:** 8 partite complete, dati esportati in `lab/registry-origins/matteo/`. Freno della quota tolto per il lotto e ripristinato.
2. **Prossimo passo, se interessa:** v10 o BHR + "engage, don't distance" **solo prima della prima review** + priorità assoluta al rischio quando HR non è sereno. Valutarla sulla prima review, con 8 partite fermate al mese 12 per spendere poco.
