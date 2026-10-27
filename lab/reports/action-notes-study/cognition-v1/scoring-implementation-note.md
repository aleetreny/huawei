# Scoring implementation note

Before inspecting model answers, the scorer treats identical public observe records as equivalent citations. A step-after observe is often repeated verbatim as the next step-before observe; either is an authoritative source under the frozen rubric. Payoff deltas still require both endpoints and at least two citation IDs. Curated checkpoint provenance IDs are kept distinct from raw records available to the model; primary strict citation scores and raw answer correctness are reported separately. No prompts, cases, thresholds or schedule changed.
