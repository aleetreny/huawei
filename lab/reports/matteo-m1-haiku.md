# M1: una partita Haiku

27 ott 2026. Manuale `m1` (`lab/policies-src/matteo-memory/m1` sulla branch `matteo-t4-growth`, commit 18b8685). È la v10 con in più un "checkpoint" fattuale scritto nelle note di ogni azione. Giocato con l'attore `017798b931bc18f8` (Haiku, CLI 2.1.310), lo stesso dei pilota v3–v12. Job `matteo-pilo-a2c31483-017798-00000-a1`.

## Risultato

**Completata, 48 mesi, Q 64,06, chiusura in L5.**

| Review | S/N/O | Dignity | Voto | Promosso |
|---|---|---:|---|---|
| m6 | 8/3/1 | 10 | C | no: nel mese 5 ha perso 2 punti di Output e 1 di Skill |
| m12 | 9/3/3 | 10 | C | sì, L2 |
| m18 | 21/4/5 | 9 | B | sì, L3 |
| m24 | 38/20/13 | 10 | B | no: 1 punto di Output sotto la soglia |
| m30 | 42/19/16 | 10 | B | sì, L4 |
| m36 | 62/36/25 | 10 | B | no: Skill bassa |
| m42 | 85/36/25 | 10 | A | no: mancavano circa 5 punti di Skill |
| m48 | 103/34/25 | 10 | A | sì, L5 |

Dimensioni finali:
- livello 50 (L5);
- soldi 39,25 (31,4);
- salute e dignità 95;
- Skill 87,5 (105);
- controllo del rischio 80;
- Network 58,33 (35).

Mai una crisi di fiducia, Dignity sempre tra 9 e 10.

## Lettura

- È la prima partita della famiglia observed-growth che chiude in L5 con la promozione dell'ultima review. Due volte su otto la promozione è stata persa per un solo punto (Output al mese 5 e al mese 23), lo stesso schema della v7–v10.
- In L4 Skill è cresciuta di circa 10–17 punti a trimestre, più che nella v7 (vedi il report v10–v12). Il checkpoint non ha impedito le perdite di un punto prima della review.
- **Una partita sola è un aneddoto:** il rumore è di circa 19 punti per partita. Non dimostra che M1 sia migliore della v10 (59,56 su 8 partite).
- Costo Haiku: 210 azioni, 190 observe, 3 azioni rifiutate. Circa 45 milioni di token in cache in 48 mesi, con note lunghe. Non è confrontabile con i token di DeepSeek, ma suggerisce che le note-checkpoint sono costose.

## Relevo

1. **Fatto:** 1 partita Haiku di M1, registrata nell'origine `matteo` ed esportata in `lab/registry-origins/matteo/`. Il manuale è stato letto da una copia temporanea di `matteo-t4-growth`, senza cambiare quella branch.
2. **Freno della quota:** tolto per questa partita (`quota_cap.json`), ripristinato alla fine.
3. **Prossimo passo, se interessa:** altre partite di M1 nello stesso lotto della v10, per vedere se il checkpoint aiuta davvero in L4. Misurare con DeepSeek quanto costano le note lunghe.
