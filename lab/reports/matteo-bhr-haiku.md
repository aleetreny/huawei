# BHR: 8 partite Haiku

27 ott 2026. Manuale `bhr` (`lab/policies-src/matteo-memory/bhr` sulla branch `matteo-t4-growth`, commit d73697a). È M1 con tre modalità esplicite: BUILD (costruire), HOLD (mantenere) e REPAIR (riparare). Giocato con l'attore `017798b931bc18f8` (Haiku, CLI 2.1.310), lo stesso dei pilota v3–v12 e di M1. Job `matteo-pilo-55adabfe-017798-0000{0..7}-a1`, 8 in parallelo.

## Risultato

**Q media 59,49 (deviazione standard 14,7, errore standard 5,2); 7 su 8 completate; 5 su 8 chiuse in L5.**

| Partita | Q | Mesi | Livello finale | Note |
|---|---:|---:|---|---|
| 01 | 74,00 | 48 | L5 | L5 già al mese 42 |
| 04 | 68,08 | 48 | L5 | bocciata alla prima review, poi promossa a ogni review |
| 07 | 67,14 | 48 | L5 | voti A ai mesi 30 e 36 |
| 05 | 63,43 | 48 | L5 | L4 al mese 24 |
| 02 | 62,85 | 48 | L5 | |
| 03 | 58,58 | 48 | L4 | bocciata ai mesi 6 e 18 |
| 06 | 55,88 | 48 | L4 | bocciata ai mesi 6 e 18 |
| 00 | 25,93 | 24 | L1 | quattro review C/D con Network sotto il tetto, licenziata |

**Prima review: 4 promosse su 8.** Tutte le bocciate erano a S 9 con N o O sotto il tetto, cioè il punto perso nel mese 5. Al mese 12, 7 su 8 erano fuori da L1. Nessuna crisi di fiducia e Dignity quasi sempre 10.

## Confronto con lo stesso attore

| Manuale | Partite | Q media | Completate | Chiuse in L5 |
|---|---:|---:|---:|---:|
| observed-growth-v7 | 9 | 57,56 | 7 | 6 |
| observed-growth-v10 | 8 | 59,56 | 7 | 5 |
| **bhr** | 8 | **59,49** | 7 | 5 |
| m1 | 1 | 64,06 | 1 | 1 |

BHR è **identico alla v10** in media, completamento e distribuzione dei livelli finali (10, 40, 40 e cinque volte 50). La memoria nelle note e le modalità BUILD/HOLD/REPAIR non cambiano il risultato in modo visibile con 8 partite. Soprattutto non evitano il punto perso prima della prima review: 4 su 8, come la v9 corretta.

## Relevo

1. **Fatto:** 8 partite Haiku di BHR, registrate nell'origine `matteo` ed esportate in `lab/registry-origins/matteo/`. Il manuale è stato letto da una copia temporanea di `matteo-t4-growth`, senza cambiare quella branch.
2. **Freno della quota:** tolto per il lotto (`quota_cap.json`), ripristinato alla fine.
3. **Conclusione:** BHR, M1 e v10 sono indistinguibili con Haiku. Visto che le note-checkpoint di M1 e BHR costano più token, per la consegna conviene la v10, che è più corta, a meno che DeepSeek mostri il contrario.
4. **Prossimo passo possibile:** il collo di bottiglia resta il mese 5. Nessuna regola testata finora (v8, v9, v10, M1, BHR) lo ha spostato con Haiku.
