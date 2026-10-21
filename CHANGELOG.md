# Changelog

All notable changes to T-Pot Evidence Lab are documented here.

## 3.1.0 — 2026-10-21

- Added 132,396 sanitized, attributed MIT-licensed cloud honeynet observations; 133,137 combined observations, 14 sensor types.
- Added combined JSONL and Parquet viewer configurations, exposed all original formats and evaluation prompts, and fixed the namespace in loading examples.
- Preserved original supervised data and labels; imported rows remain unlabelled.
- Added pinned-source import tooling, provenance, license notices, schema documentation, exact counts, and a filterable real-data preview.
- Fixed release-manifest self-inclusion and excluded Python/cache artifacts from manifest generation.

## 3.0.0 — 2026-10-20

### Added

- First public static release: 741 sanitized structured honeypot events and 675 weakly labelled instruction examples.
- Source-group-disjoint train, validation, and test splits with qualifying-window stratification.
- Chat, Alpaca, ShareGPT, prompt/completion, JSONL, and Parquet representations.
- Offline exact-match evaluator plus local Ollama/OpenAI-compatible loopback runner.
- Axolotl, LLaMA Factory, Ollama, and framework-neutral Harness² bridge documentation.
- Hugging Face metadata, GitLab CI verification, GitLab Pages landing site, release manifest generation, and CC BY 4.0 license metadata.

### Privacy and safety

- Removed literal source identifiers, provider contacts, local targets, credentials, raw payloads, captured commands, uploads, source mappings, reporting ledgers, and correspondence.
- Added checks for basic identifier leakage, split isolation, canonical-format alignment, and evaluator contracts.

### Notes

- Labels are deterministic weak labels for a limited defensive-evidence task. No model is trained or included.
- This is the first public version; unreleased private capture formats have no compatibility commitment.

