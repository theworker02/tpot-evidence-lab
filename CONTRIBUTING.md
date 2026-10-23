# Contributing

Keep the distinction between raw observations, deterministic weak labels and human-reviewed findings. State source rights, provenance and transformation steps for any proposed collection. Never add malware binaries, credentials, raw command streams, source identifiers, correspondence or private deployment configuration.

Run all Python tests, both site tests and the release verifier as described in `docs/publishing.md`. Changes to rows, schemas, splits or task definitions require a versioned release and changelog entry. Preserve existing loader configurations. Include a regression test for parser, privacy, split or format changes.

For label review, cite the sanitized row ID, proposed disposition, supporting evidence and remaining uncertainty. Do not silently rewrite weak labels as verified ground truth. Model results must identify the exact dataset revision and address overlap, task leakage and source bias.
