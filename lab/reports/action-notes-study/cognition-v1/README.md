# Benchmark cognitivo Luna — in esecuzione

Matteo ha autorizzato la prosecuzione dopo la proposta di576 decisioni.48 casi da48 carriere pubbliche diverse, otto categorie, quattro condizioni, tre repliche. Protocollo, manuale, schedule e rubric congelati prima delle risposte; preflight gpt-6-luna via Codex CLI con accesso ChatGPT riuscito. Nessuna API pagata e nessuna partita nuova.

Le condizioni sono current_only, full_history, curated_checkpoint e stale_recovery. I checkpoint corretti sono riassunti curati, non note scritte autonomamente dal modello. Il recupero è simulato tramite consegna dei log pubblici dopo richiesta strutturata; non è una chiamata MCP nativa. I casi semantici interrogano ciò che era esplicito nella descrizione storica, non dichiarano che il problema sia ancora aperto al punto finale del prefisso.

## Relevo

In corso, nessuna classifica parziale interpretata. Stato live e risposte fuori repo in `/Users/matteozabban/careerlab-data/matteo-notes-cognitive/benchmark-v1d`; processo avviato con scripts/run_note_cognitive_benchmark.py, sessione exec34279. Non rilanciare la schedule e non modificare il runner o i casi congelati. Limiti:720 richieste incluse eventuali144 riprese,24M input e250k output dichiarati;4 richieste indipendenti in parallelo. Arresto su errori di route/quota o tetto, senza sostituire risposte.

Checkpoint operativo: {"completed": 341, "assigned": 344, "target": 576, "usage": {"input_tokens": 8176343, "output_tokens": 50272, "cached_input_tokens": 4654848, "reasoning_output_tokens": 329, "requests": 400}, "stop_reasons": []}

Dopo il termine eseguire analyze_note_cognitive_benchmark.py e audit_note_cognitive_results.py, archiviare dati e risultati, aggiornare solo Matteo T4, commit/push e PR12.297 test software passati.
