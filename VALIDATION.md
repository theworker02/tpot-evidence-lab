# Validation for v3.2.0

The additions contain 12,066 scenarios and 24,401 sanitized retained events. Original combined observations (133,137), original chat examples (675) and evaluation tasks (601) are preserved. These overlapping snapshots are not an independent combined benchmark.

Checks for this release:
- Full Python suite: original endpoint contracts, expanded counts, schemas, source licenses, policy labels, timestamp removal, group isolation, input checksum rejection and path escape rejection.
- Equivalent canonical JSONL and Parquet rows for the two new configurations; original observation checks remain.
- All eleven card configurations load locally with Hugging Face datasets 5.1.0 and Hub networking disabled.
- Node harnesses test original filters/pagination/reset/empty/failure states and new scenario selection/responses/source-license status/invalid/empty/failure states.
- Public-text scanning, pinned upstream hashes, source licenses and SHA-256 release inventory; whitespace review and exclusion of Git metadata/caches/environments.

Initial Windows sandbox checks could not create temporary fixtures or use loopback HTTP; the suite was run in the existing Linux environment with these operations available. The public-text gate caught example addresses in MITRE documentation, not local telemetry. Documentation example addresses are now defanged.

Checks establish structural consistency and loadability, not correctness of weak labels, complete anonymity or model performance. Human adjudication remains pending. No model was trained; no compromise, identity or botnet membership is established by these data. Cross-version source/campaign overlap cannot be resolved from discarded mappings. Publication receipts are kept outside the public tree; live CI and release pages expose deployment status.
