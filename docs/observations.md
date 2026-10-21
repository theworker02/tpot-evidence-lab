# Observation fields and source boundaries

`observations` is the combined structured default configuration; `observations_parquet` is an alias for the same rows and splits. All viewer configurations use Parquet to avoid mixing loader formats within one repository. Canonical JSONL downloads remain in `data/observations/` and the original format folders. Both contain 133,137 rows. Original messages remain under the explicit `chat` configuration.

| Field | Meaning |
| --- | --- |
| id | Unique record ID; gaps in cloud IDs reflect removed projection duplicates |
| corpus | `magnexis-local-2026` or `cloud-honeynet-2025` |
| source_group | Opaque corpus-scoped source group; never an identity |
| timestamp_utc | Recorded UTC event time, retained without rounding |
| sensor | Upstream honeypot name; `attackType` in the cloud source denotes a sensor, not a verified attack class |
| transport | Upstream protocol/service description; not necessarily a layer-four transport |
| destination_port | Explicit integer destination port; null where absent in the local data |
| rule_label | Original local collector label; null for imported observations |
| label_basis | `collector_rule` or `unlabelled_observation` |
| license | Original row license: `CC-BY-4.0` or `MIT` |
| source_url | Source publication URL |
| split | Train, validation, or test |

The imported projection includes only timestamps, sensor names, protocol descriptions, destination ports, and opaque source groups. Source/destination IPs, source ports, organizations, locations, hostnames, commands, credentials, URLs captured from traffic, raw messages, and payloads are excluded. This is a limited projection, not a guarantee of anonymity: timing and behavior can still permit linkage with the public source. Do not attempt re-identification.

Splits are deterministic and source-group-disjoint within each corpus. Imported groups use a seeded SHA-256 partition of source addresses, then receive sequential opaque names; neither addresses nor hashes are published. Local groups retain their original split assignments. Cross-corpus source overlap cannot be checked because the original local mapping is unavailable. Do not describe the combined splits as globally independent identities. Group-level partitioning does not guarantee balanced event counts.

The upstream CSV has 132,425 rows. Removing fields produces 29 identical projected rows; these are collapsed, leaving 132,396 imported observations. These are projection duplicates, not a claim that upstream events were duplicates. No original local row is removed.

Cloud observations do not include event IDs, authentication outcomes, command counts, or enough evidence to reconstruct the original reporting task. No labels or instruction answers are generated from them. Unknown evidence stays unknown. The collection expands exploratory analytics, not the supervised benchmark.

## Reproduce the import

Use Python with `pyarrow` and `PyYAML` installed. Download `CloudHoneyNetDataset.zip` from the pinned [Zenodo record](https://zenodo.org/records/15716735), then run:

```bash
python tools/build_observations.py /path/to/CloudHoneyNetDataset.zip
python tools/prepare_viewer.py
python -m unittest discover -s tests -p 'test_*.py'
python tools/verify_release.py
```

The builder verifies the archive checksum before reading the one named CSV member. It never extracts or executes upstream notebooks, scripts, or raw logs. Invalid input fails the build. Archive MD5 and SHA-256 digests and exact counts appear in `observation-statistics.json`. Raw archives must stay outside this repository.

The original 675 instruction rows are alternate renderings of the original task; they are not 675 independent new observations. The 601 evaluation tasks remain unchanged. Compare models with the deterministic rules before drawing conclusions about model quality.
