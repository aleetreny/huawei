# bhr-countdown: 8 partite Haiku, fermate dopo la prima review

27 ott 2026. Manuale `bhr-countdown` (rimosso dal repo su richiesta di Matteo e sostituito da `bhr-cooperate`; le partite restano nel registro, policy `f1519df2f6601d3f`): è BHR più un contatore `Review in N` all'inizio di ogni nota e una checklist per il mese prima della review (N = 1). La checklist marca le opzioni "N" (contro una persona) e "O" (tolgono tempo al proprio lavoro) e fa scegliere un'opzione onesta senza marchi. Idea presa dal `t10-countdown` di Alejandro (T20). Attore `017798b931bc18f8`, lo stesso di BHR. Job `matteo-pilo-f1519df2-017798-0000{0..7}-a1`.

## Risultato

**Prima review: 2 promosse su 8 (BHR: 4 su 8). Una partita è morta di esaurimento al mese 6 (Q 17,27).** Il test aveva come obiettivo proprio la prima review, quindi le altre 7 partite sono state fermate subito dopo, come Matteo aveva chiesto di fare con le partite che non servono più al test. Sono registrate come interrotte, senza voto.

| Partita | Stato alla review del mese 6 | Esito |
|---|---|---|
| 00 | 9/3/3 | promossa |
| 03 | 8/3/3 | promossa |
| 01, 05, 06, 07 | 9/1/3 | non promosse: Network a 1 |
| 02 | 9/3/2 | non promossa |
| 04 | 9/0/3, Salute 0 | esaurimento, fine partita |

## Cosa è successo

- **Il contatore viene eseguito:** tutte le note iniziano con `Review in N` (64–88 note per partita) e nel mese 5 compaiono le marcature, per esempio `Review in 1 | marks: 1=- 2=- 3=N → 1`.
- **Le marcature però sono sbagliate:** Haiku sceglie opzioni che ha marcato "senza costi" e perde comunque Network. In 4 partite su 7 arriva alla review con Network a 1. È la lezione 7 di Ale: *per vietare un effetto nascosto il modello deve saperlo vedere*, e Haiku non sa quale opzione costa Network.
- L'esaurimento della 04 (Salute 0 al mese 6) indica che le regole in più sottraggono attenzione alla salute.

## Conclusione

Con 8 partite, 2/8 contro 4/8 non è una prova definitiva (l'intervallo è largo), ma non c'è nessun segnale di miglioramento e c'è un danno visibile. **Scartato.** Il punto perso nel mese 5 resta il problema principale, e nessuna formulazione provata finora lo risolve con Haiku: v8, v9, v10, M1, BHR e bhr-countdown.

## Relevo

1. **Fatto:** manuale scritto e registrato; 8 partite avviate. Il lotto è stato fermato dopo la prima review: 1 partita conclusa, 7 interrotte. Freno della quota tolto e poi ripristinato. Dati esportati in `lab/registry-origins/matteo/`.
2. **Prossimo passo possibile:** invece di chiedere al modello di riconoscere il costo, cambiare cosa fa nel mese 5. Per esempio, nessuna scelta che coinvolga terzi quando c'è un'opzione che riguarda solo il proprio lavoro. Va provato prima nel banco di situazioni di Ale, non con partite intere.
