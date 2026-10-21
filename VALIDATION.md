# Local validation — October 21, 2026

This is a reviewed local candidate for version 3.1.0. Hugging Face, GitLab, and the deployed Pages site have not been updated. No commit, push, release, deployment, or upload was performed.

## Implemented

- 133,137 combined observations: 741 original local events plus 132,396 sanitized imported observations.
- Imported the pinned MIT-licensed Multi-Regional Cloud Honeynet CSV: 132,425 input rows, 29 identical projected rows collapsed, 2,460 imported opaque source groups.
- Nine named Hub configurations, including combined observations, original detailed events, alternate training formats, and split evaluation prompts.
- Preserved original chat `default` loader behavior and every original event, instruction, and evaluation source file.
- Added attribution, per-row licensing, source records, schema and split documentation, checksum-pinned import tooling, and viewer preparation tooling.
- Added a bounded real-record site preview with search, collection/sensor filters, pagination, reset, empty-state handling, and fetch-failure handling.
- Excluded manifest self-inclusion and Python/cache files from release digests.

## Verified locally

- `python -m unittest discover -s tests -p 'test_*.py'`: 10 tests passed. Includes original local HTTP endpoint contracts, group isolation, counts, input rejection, checksum rejection, privacy field allowlist, and real preview membership.
- `node tests/test_preview.cjs`: search, filters, pagination, reset, empty results, and failed-fetch behavior passed using a DOM test harness without opening a browser.
- All nine configurations loaded through the installed Hugging Face `datasets` library with networking disabled. Split counts match their files; the original `default` configuration still yields 493/109/73 chat rows.
- Combined JSONL rows equal Parquet rows exactly in every split.
- `python tools/verify_release.py`: public-text safety checks passed and SHA-256 manifest generated.
- `git diff --check`: no whitespace errors.

The initial HTTP contract test was blocked by sandbox socket permissions; rerunning with loopback networking permitted passed. No pre-existing code failure was found.

## Limits

- Imported observations have no weak reporting labels, raw messages, commands, credentials, geolocation, or addresses. The supervised benchmark remains 675 examples and 601 evaluation tasks.
- Cross-corpus identity overlap cannot be checked; split independence is within each corpus only.
- Retained timing can permit linkage with the public upstream collection; complete anonymization is not claimed.
- Browser rendering, accessibility-tree behavior, and live Hub viewer generation have not been checked. Browser automation and remote publication require the owner's approval under the supplied custom instructions.
- Existing CI configuration is unchanged; its current Python command runs only the original `test_release.py`. Run the full commands above when reviewing this candidate.
