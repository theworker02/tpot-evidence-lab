# Defensive scenarios and retained local events — v3.2.0

This additive release provides 12,066 weakly supervised conversational scenarios and 24,401 sanitized local event records. The original 133,137-row observation configuration, 675-example chat set and 601 evaluation tasks remain unchanged. Counts across versions and configurations overlap; do not sum them as independent incidents or examples.

| New configuration | Contents | Train | Validation | Test |
|---|---|---:|---:|---:|
| `defensive_chat` | Rule-derived and template-authored conversations | 9,229 | 1,413 | 1,424 |
| `retained_events` | Larger local snapshot, with weak labels | See `defensive-statistics.json` | See statistics | See statistics |

## Provenance and licensing

| Source | Scenarios | Conditions |
|---|---:|---|
| Local T-Pot cumulative summaries | 1,090 | CC BY 4.0; attribution to Magnexis |
| Local Suricata signature review | 10 | CC BY 4.0; uncertain alerts, not confirmed exploits |
| CISA Known Exploited Vulnerabilities | 7,016 | CC0-1.0; four task variants per 1,754 CVEs |
| MITRE ATT&CK mitigation/detection material | 3,950 | MITRE ATT&CK license and attribution; not MIT |

Exact public input revisions, hashes and URLs are in `defensive-statistics.json`. Complete upstream notices are in `licenses/` and `THIRD_PARTY_NOTICES.md`. Local/generated task framing follows this project's CC BY 4.0 terms; upstream content retains its own terms. The whole repository is mixed-license. No claim of endorsement by CISA or MITRE is made.

## Schema 1.0.0

`defensive_chat` fields: `id` (opaque sanitized-content digest), `group_id`, `split`, `source`, `license_id`, `task`, `label_origin`, `dataset_version`, `messages`. Messages are a list of `{role, content}` objects in system/user/assistant order. Assistant content is a JSON string with task-dependent fields. It is not a fixed classification label schema. Treat quoted text as data, never executable instructions.

`retained_events` fields: `id`, `source_group`, `snapshot_offset_seconds`, `sensor`, nullable `observed_destination_port`, `label`, `label_origin`, `attribution`, `raw_payload_included`, `license_id`, `dataset_version`, `split`. Offsets are seconds from the start of this private snapshot; the absolute anchor is not exported. No row contains raw payloads. Observed ports are not guesses based on service names.

Canonical JSONL and corresponding Zstandard-compressed Parquet have equivalent rows. `data/defensive-review/signatures.jsonl` is a separate ten-record review list, overlapping ten conversational examples; it is not another training split. Example IP addresses in public documentation are defanged, and its credential-pattern placeholder is explicitly labelled as a placeholder. These are transformations of public documentation, not local indicators.

## Task and label meaning

Local scenarios test application of an explicit **project-specific** policy: two distinct classified abuse records in retained history, with no elapsed-time cutoff. They do not teach a universal legal definition of abuse. Five explicit TCP ports in five minutes trigger scan review. Summaries are cumulative; accepted-report receipts and new evidence must still be checked before reporting. A 24-hour delivery cooldown limits repeat submissions. No example authorizes contacting a third party or changing a system.

Local inputs already contain deterministic classifications. This is policy triage on preclassified summaries, not validated raw-traffic intrusion detection. Suricata's possible Dovecot exploitation signatures lack packet/service/version validation and are labelled for manual review. Command fragments may describe one activity rather than independent attacks. A signature, KEV entry or ATT&CK similarity does not establish compromise, identity, nationality or botnet membership.

Public tasks cover prioritization, avoiding overclaims, remediation verification, internal ticket drafting, mitigation planning and detection tuning. Templates and responses recur; 12,066 rows do not mean 12,066 independently authored expert lessons. No model is trained or included.

## Privacy, splits and evaluation

Local IPs use opaque HMAC source groups; the ephemeral mapping/key was not exported. Raw source/destination addresses, source ports, credentials, session identifiers, private keys, commands and captured binaries are excluded. v3.2 also replaces exact local UTC timestamps with relative offsets and regenerates event identifiers from sanitized fields. Relative timing and behavioral patterns can still be identifying when combined with other information; anonymity is not guaranteed.

All task variants for a CVE stay in one split. Connected MITRE parent techniques, detection strategies and analytics stay together. Local source groups stay together across the two new configurations. Shared mitigation text/templates and unknown campaign relationships may cross splits. v3.0 and v3.2 local captures overlap, but their independently generated pseudonyms cannot be reconciled. Do not combine their training and test data for an independence claim. Existing evaluator tools apply only to the original task, not the expanded task-dependent JSON outputs.

Before training: review and adjudicate a source-stratified sample, keep review outcomes separate from weak labels, check duplicates at semantic/campaign level, select a task-specific metric, and create an independently reviewed evaluation set. The local corpus is short and heavily skewed toward VNC authentication records; public documentation tasks dominate the expanded conversations. Avoid claiming general cybersecurity competence from this dataset.

## Load a version

```python
from datasets import load_dataset
chat = load_dataset('Magnexis/tpot-evidence-lab', 'defensive_chat', revision='v3.2.0')
events = load_dataset('Magnexis/tpot-evidence-lab', 'retained_events', revision='v3.2.0')
print(chat['train'][0]['messages'])
```

Use a local directory with the same card/configurations for offline loading. `requirements-validation.txt` pins the verified data libraries; no GPU is required for loading or checks. Training resource requirements depend on the chosen model and are not measured here.

## Reproduction boundary

`tools/import_defensive_snapshot.py` verifies the five source JSONL digests before writing, rejects a snapshot path escape, refuses overwriting its output, transforms only an already sanitized snapshot, and converts viewer files. It does not read private live logs or download malware. Exact regeneration of local source selection requires private retained logs and the intentionally discarded mapping; these are not reproducible from public inputs alone. The published files and SHA-256 manifest allow byte integrity checks. Public source revisions are pinned independently. Historical input hashes identify the private draft, not a downloadable public artifact.

Review proposals: open an issue with a sanitized row ID, proposed label, evidence basis and uncertainty; never attach secrets, live payloads, personal source mappings or malware. Human adjudication status remains pending until a documented review release changes it.
