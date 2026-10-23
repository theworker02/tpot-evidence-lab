# Changelog

All notable changes to T-Pot Evidence Lab are documented here.

## 3.2.1 — 2026-10-23

- Fixed cross-platform manifest key ordering and normalized the model template line endings. Added a deterministic-manifest regression test.
- Release archives and the Hub publication use this corrected package; the initial v3.2.0 GitHub tag remains intact. Data rows retain dataset_version 3.2.0 because this patch changes packaging only.

## 3.2.0 — 2026-10-23

- Added 12,066 defensive scenarios in `defensive_chat` and 24,401 sanitized records in `retained_events`, with canonical JSONL and equivalent Parquet.
- Added four CISA KEV task variants per CVE and MITRE ATT&CK mitigation/detection tasks, pinned provenance and complete upstream licenses.
- Added local timestamp offsets, sanitized-content event IDs, explicit policy differences, uncertain-signature examples, cross-version overlap warnings and human-review guidance.
- Preserved every original dataset configuration and default observation table; no counts are combined across overlapping snapshots.
- Added semantic version source, release verification, expanded schema/privacy/split tests, GitHub release instructions and an interactive scenario preview.
- Published project source and a static site on GitHub/GitHub Pages; Hugging Face remains the dataset distribution endpoint.

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

