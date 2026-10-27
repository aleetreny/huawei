# v10 contro BHR: replica alternata

27 ott 2026, sera. Matteo ha chiesto 8 partite in più della v10 e 8 di BHR, da fermare se una delle due fosse risultata chiaramente migliore. Le partite sono alternate (v10, BHR, v10…) nello stesso lotto, 8 alla volta, con l'attore `017798b931bc18f8` (Haiku, CLI 2.1.310), lo stesso dei pilota.

**Regola fissata prima dei risultati:** fermare le partite in coda se P(uno migliore) ≥ 0,95 dopo la prima ondata. Alla prima ondata P(v10 migliore) era 0,68, quindi tutte le partite sono state giocate.

**Incidente:** il primo avvio si è fermato subito perché BHR era registrato da una copia temporanea già cancellata. La copia è stata ricreata dallo stesso commit (d73697a), quindi il manuale è identico, e il lotto è stato rimesso in coda. Le partite interrotte (job 00008–00014) non hanno voto. Il job BHR 00015, rilasciato dal recupero, è stato giocato, quindi BHR ha 9 partite nuove e la v10 8.

## Risultato

| | v10 | BHR |
|---|---:|---:|
| Partite nuove | 8 | 9 |
| Q media delle nuove | **51,14** | **37,90** |
| Tutte (pilota + nuove) | 16 | 17 |
| Q media di tutte | **55,35** (dev. st. 20,1) | **48,06** (dev. st. 19,7) |
| Completate | 11/16 | 11/17 |
| Chiuse in L5 o oltre | 9/16 (una in L6) | 6/17 |
| Licenziate in L1 al mese 24 | 1 | 5 |

**Differenza v10 − BHR = +7,3 ± 6,9; P(v10 migliore) = 0,85.**

Partite nuove della v10: 77,78 (L6), 73,25, 70,05, 60,46, 45,52, 42,72, 19,94, 19,40.
Partite nuove di BHR: 60,67, 59,41, 56,52, 48,05, 35,92, 23,23, 22,98, 19,07, 15,23.

## Lettura

- **La v10 è probabilmente migliore di BHR**, ma non "chiaramente": l'85 % non arriva al 95 % fissato.
- Nel lotto alternato, che è il confronto più pulito, la differenza è grande: 51,1 contro 37,9. BHR ha avuto 4 licenziamenti al mese 24 in L1 su 9 partite. La memoria e le modalità di BHR non proteggono la prima promozione meglio della v10, e il checkpoint lungo costa token.
- **Entrambi sono scesi rispetto ai pilota** (v10 da 59,6 a 51,1; BHR da 59,5 a 37,9): è l'effetto del primo lotto fortunato. Le stime giuste sono quelle con tutte le partite: **v10 circa 55, BHR circa 48.**
- La v10 ha fatto la prima partita in **L6** della famiglia (77,78).

## Conclusione

**La v10 resta il manuale migliore di Matteo** ed è anche il più economico in token. BHR non va proposto.

## Relevo

1. **Fatto:** 17 partite nuove (8 v10, 9 BHR), dati esportati in `lab/registry-origins/matteo/`. Freno della quota tolto e ripristinato.
2. **Prossimo passo:** consegnare la v10 (compilare `instruction`, controllare la rubrica) e, se possibile, 3 partite DeepSeek tramite Ale.
