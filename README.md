---
language:
- en
license: other
license_name: tpot-evidence-lab-mixed-source
license_link: LICENSES.md
task_categories:
- text-classification
- text-generation
tags:
- cybersecurity
- honeypot
- weak-supervision
size_categories:
- 100K<n<1M
configs:
- config_name: observations
  default: true
  data_files:
  - split: train
    path: data/observations/train.parquet
  - split: validation
    path: data/observations/validation.parquet
  - split: test
    path: data/observations/test.parquet
- config_name: observations_parquet
  data_files:
  - split: train
    path: data/observations/train.parquet
  - split: validation
    path: data/observations/validation.parquet
  - split: test
    path: data/observations/test.parquet
- config_name: evaluation
  data_files:
  - split: train
    path: data/viewer/evaluation/train.parquet
  - split: validation
    path: data/viewer/evaluation/validation.parquet
  - split: test
    path: data/viewer/evaluation/test.parquet
- config_name: chat
  data_files:
  - split: train
    path: data/viewer/chat/train.parquet
  - split: validation
    path: data/viewer/chat/validation.parquet
  - split: test
    path: data/viewer/chat/test.parquet
- config_name: alpaca
  data_files:
  - split: train
    path: data/viewer/alpaca/train.parquet
  - split: validation
    path: data/viewer/alpaca/validation.parquet
  - split: test
    path: data/viewer/alpaca/test.parquet
- config_name: sharegpt
  data_files:
  - split: train
    path: data/viewer/sharegpt/train.parquet
  - split: validation
    path: data/viewer/sharegpt/validation.parquet
  - split: test
    path: data/viewer/sharegpt/test.parquet
- config_name: prompt_completion
  data_files:
  - split: train
    path: data/viewer/prompt_completion/train.parquet
  - split: validation
    path: data/viewer/prompt_completion/validation.parquet
  - split: test
    path: data/viewer/prompt_completion/test.parquet
- config_name: events
  data_files:
  - split: train
    path: data/parquet/train.parquet
  - split: validation
    path: data/parquet/validation.parquet
  - split: test
    path: data/parquet/test.parquet
- config_name: events_parquet
  data_files:
  - split: train
    path: data/parquet/train.parquet
  - split: validation
    path: data/parquet/validation.parquet
  - split: test
    path: data/parquet/test.parquet
- config_name: defensive_chat
  data_files:
  - split: train
    path: data/defensive-chat/train.parquet
  - split: validation
    path: data/defensive-chat/validation.parquet
  - split: test
    path: data/defensive-chat/test.parquet
- config_name: retained_events
  data_files:
  - split: train
    path: data/retained-events/train.parquet
  - split: validation
    path: data/retained-events/validation.parquet
  - split: test
    path: data/retained-events/test.parquet
---

# T-Pot Evidence Lab

<p align="center">
  <img src="assets/tpot-evidence-lab-avatar.png" width="164" alt="T-Pot Evidence Lab project avatar: connected evidence nodes and signal arcs">
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/Magnexis/tpot-evidence-lab"><img src="https://img.shields.io/badge/Hugging%20Face-Dataset-f9d154?logo=huggingface&logoColor=black" alt="Hugging Face Dataset"></a>
  <a href="https://github.com/theworker02/tpot-evidence-lab"><img src="https://img.shields.io/badge/GitHub-Repository-24292f?logo=github&logoColor=white" alt="GitHub Repository"></a>
  <a href="https://theworker02.github.io/tpot-evidence-lab/"><img src="https://img.shields.io/badge/GitHub%20Pages-Live-4285f4?logo=gitlab&logoColor=white" alt="GitHub Pages"></a>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-6b4e9b" alt="CC BY 4.0 License"></a>
  <img src="https://img.shields.io/badge/Release-v3.2.0-173f5f" alt="Release v3.2.0">
</p>

**A sanitized, weakly labelled honeypot-evidence dataset for defensive-security research, local model evaluation, and training-pipeline prototyping.**

The original supervised subset is a static release derived from a locally operated T-Pot honeypot deployment. It supports one narrow, auditable task: given a compact summary of observed honeypot behavior, determine whether the evidence meets a fixed incident-reporting threshold and name that threshold. It is not a general internet-threat corpus, a botnet-attribution dataset, a malware corpus, or evidence of production compromise.

## New in v3.2.0: defensive scenarios

**12,066 additional conversational scenarios** and **24,401 sanitized retained local events** are available as `defensive_chat` and `retained_events`. These are separate from the preserved v3.1 observation table and original supervised task; local snapshots overlap and counts must not be added as independent records. Expanded labels are rule-derived/template-authored and human adjudication is pending.

The new scenarios include 1,090 local T-Pot summaries, ten uncertain IDS-signature reviews, 7,016 CISA KEV task variants and 3,950 MITRE ATT&CK mitigation/detection examples. Exact local timing is replaced with relative offsets. Public documentation is not evidence that any local host was compromised.

```python
from datasets import load_dataset
chat = load_dataset("Magnexis/tpot-evidence-lab", "defensive_chat", revision="v3.2.0")
events = load_dataset("Magnexis/tpot-evidence-lab", "retained_events", revision="v3.2.0")
```

See [schemas, labels, split limits and methodology](docs/defensive-dataset.md), [source-specific licenses](LICENSES.md), [release history](CHANGELOG.md), and [validation](VALIDATION.md). This is a research data release; no model has been trained and the expanded scenarios are not an independently validated benchmark. The default `observations` configuration remains unchanged.

## Explore more than messages

**Version 3.1 adds 132,396 sanitized public T-Pot observations.** The combined observation table has **133,137 rows across 14 sensor types**, with timestamps, protocols, destination ports, corpus provenance, source groups, and per-row licensing. The original 675 instruction examples and 601 evaluation tasks remain available.

| Choose a viewer configuration | Contents | Rows |
| --- | --- | ---: |
| **observations** (structured table) | Combined structured observations | 133,137 |
| observations_parquet | Alias for the same observation table | 133,137 |
| events / events_parquet | Original detailed local events and behavioral flags | 741 |
| chat / alpaca / sharegpt / prompt_completion | Alternate formats of the original instruction examples | 675 each |
| evaluation | Original prompts with IDs and source groups; answers remain separate | 601 |

All viewer configurations use Parquet for loader compatibility; canonical JSONL downloads remain in their original folders. **These formats overlap; do not add their counts together.** Evaluation prompts retain the original source-disjoint splits. Do not train on evaluation prompts or answers when reporting held-out results.

```python
from datasets import load_dataset
observations = load_dataset("Magnexis/tpot-evidence-lab", "observations")
events = load_dataset("Magnexis/tpot-evidence-lab", "events")
chat = load_dataset("Magnexis/tpot-evidence-lab", "chat")
print(observations["train"][0])
```

### Collections and attribution

| Collection | Observations | Capture | License | Evidence |
| --- | ---: | --- | --- | --- |
| Magnexis local | 741 | October 20, 2026 | CC BY 4.0 | Original collector-rule fields |
| Multi-Regional Cloud Honeynet | 132,396 | June 9–11, 2025 | MIT | Unlabelled protocol/port observations |

The external source is the [Multi-Regional Cloud Honeynet Dataset](https://zenodo.org/records/15716735), by Enrique Feito-Casares, Ismael Gómez-Talal, and José Luis Rojo-Álvarez, Universidad Rey Juan Carlos. Its published CSV contains 132,425 rows; 29 became identical after sensitive columns were removed and were collapsed. Imported rows retain MIT licensing. See [third-party notices](THIRD_PARTY_NOTICES.md), [field definitions and reproducibility](docs/observations.md), and [exact observation counts](observation-statistics.json).

Imported observations **have no reporting labels**: missing authentication or command evidence is not a negative label. Source/destination addresses, locations, hostnames, commands, credentials, and raw payloads are excluded. Opaque groups are disjoint within each corpus; overlap between the two corpora cannot be checked. Event timing can still permit linkage to upstream data, so this is not a guarantee of anonymity.

For analysis, start with observations. For the original rule-classification task, use the original chat and evaluation files. No model has been trained and no larger supervised benchmark is claimed.

---

## Access the release

- **Download and use the dataset:** [Hugging Face — Magnexis/tpot-evidence-lab](https://huggingface.co/datasets/Magnexis/tpot-evidence-lab)
- **Browse the repository, documentation, and release history:** [GitHub — theworker02/tpot-evidence-lab](https://github.com/theworker02/tpot-evidence-lab)
- **Project landing page:** [T-Pot Evidence Lab on GitHub Pages](https://theworker02.github.io/tpot-evidence-lab/)

## Original collection and supervised task

The sections below describe the original local subset. They do not apply its weak labels to the imported collection.

## Contents

- [Why this exists](#why-this-exists)
- [Collection and acquisition](#collection-and-acquisition)
- [Sanitization](#sanitization-and-privacy)
- [Labels and task](#labels-and-task-definition)
- [Formats](#data-formats-and-schemas)
- [Usage](#using-the-dataset)
- [Evaluation](#evaluation)
- [Quality and responsible use](#quality-limits-and-responsible-use)
- [Release and licensing](#release-and-licensing)

## Why this exists

Honeypot data is often too sensitive to share or too unstructured for a local training workflow. This release supplies common, documented formats while preserving the line between observable behavior and claims about an operator.

Use it to prototype a defensive classifier, compare a model against explicit rules, test data ingestion, or evaluate an already local model. Do not use it to identify people, contact providers, attribute botnets or malware, block traffic, or make autonomous enforcement decisions.

| Item | Count |
| --- | ---: |
| Structured honeypot events | 741 |
| Opaque source groups | 126 |
| Instruction examples | 675 |
| Evaluation tasks | 601 |
| Capture interval | 2026-10-20T12:13:15Z – 2026-10-20T23:01:18Z |

Train, validation, and test splits are disjoint by opaque source group and stratified by whether a group has a qualifying window. Exact figures are in [statistics.json](statistics.json).

## Collection and acquisition

### Source environment

The observations came from a locally operated [T-Pot](https://github.com/telekom-security/tpotce) multi-honeypot deployment. Internet-facing decoy services accepted unsolicited connections and emitted their normal structured event records. No production-system telemetry, customer data, endpoint-agent telemetry, credential store, or packet capture was added.

The private source snapshot had three broad record categories: honeypot interactions, platform-management records, and passive ambient observations. Management and passive records were excluded from public examples and reporting decisions. The T-Pot deployment and reporting service were stopped before this data release was built.

### Processing method

1. Export structured honeypot records from the local snapshot.
2. Exclude management, passive, private, unverifiable, authorized-test, and ordinary-connection records from reporting candidates.
3. Group eligible behavior into evidence windows and apply the fixed deterministic rules below.
4. Replace source identifiers with sequential opaque source-group IDs. The original mapping is not released.
5. Remove direct identifiers and unsafe captured content.
6. Create source-disjoint train, validation, and test splits, then render each split into multiple interoperable formats.
7. Run release checks for record counts, split isolation, schema alignment, evaluator behavior, and obvious identifier leakage.

The dataset is a single collector at a single point in time. It is not representative of internet traffic as a whole.

## Sanitization and privacy

The public package excludes literal IP addresses, hostnames, provider contacts, source-group mappings, local target addresses, usernames, passwords, API keys, raw payloads, captured commands, uploaded objects, binaries, reporting ledgers, and correspondence.

It retains timestamps and behavioral summaries because those are needed for the stated task. This is not a guarantee of complete anonymization. Users must not attempt re-identification, correlate opaque groups with external records, or use this data to harass, accuse, or contact a presumed operator.

## Labels and task definition

Each instruction example asks for JSON with a Boolean `qualifies` field and an array of threshold names in `reasons`. `qualifies: true` means at least one fixed threshold was met:

- **Failed authentication:** five failed authentications from one source within 180 seconds.
- **Web/Redis probing:** five recognized web or Redis exploit probes.
- **Decoy-shell activity:** five explicit Cowrie or Adbhoney decoy-shell commands or uploads.
- **Multi-port activity:** five distinct honeypot TCP ports reached by one source.

These are deterministic weak labels, not human-reviewed findings. A negative row only means the compact window did not reach the threshold; it does not prove benign intent. A positive row only means a threshold was met. Neither result establishes identity, ownership, compromise, or motive.

## Data formats and schemas

| Format | Location | Use |
| --- | --- | --- |
| Chat JSONL | `data/chat/` | Hugging Face Datasets, TRL, Unsloth, Axolotl |
| Alpaca JSONL | `data/alpaca/` | Instruction-tuning loaders |
| ShareGPT JSONL | `data/sharegpt/` | LLaMA Factory and compatible tools |
| Prompt/completion JSONL | `data/prompt-completion/` | Custom fine-tuning loops |
| Event JSONL | `data/events/` | Streaming and language-agnostic processing |
| Parquet | `data/parquet/` | pandas, Polars, DuckDB, Spark |
| Evaluation tasks | `evaluation/` | Offline and local-model grading |

The canonical chat row is:

```json
{"id":"example-000001","messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"{\"qualifies\": false, \"reasons\": []}"}],"split":"train"}
```

`source_group` is an opaque split key, not an identity. Actual structured field names are visible in the event JSONL and Parquet files.

## Using the dataset

### Hugging Face Datasets

```python
from datasets import load_dataset
dataset = load_dataset("Magnexis/tpot-evidence-lab", "chat")
print(dataset["train"][0]["messages"])
```

For a local clone, JSONL needs only the standard library:

```python
import json
with open("data/chat/train.jsonl", encoding="utf-8") as handle:
    row = json.loads(next(handle))
print(row["messages"])
```

### Unsloth, TRL, and compatible chat trainers

Use `data/chat/train.jsonl`, preserve the role structure, and apply the chat template appropriate to the selected base model. Use validation for development and keep `evaluation/answers.jsonl` out of training. Report that the labels are deterministic and weak.

### Axolotl and LLaMA Factory

Merge [adapters/axolotl-dataset.yaml](adapters/axolotl-dataset.yaml) into an Axolotl model configuration. For LLaMA Factory, register the ShareGPT paths declared in [adapters/dataset_info.json](adapters/dataset_info.json). The release does not prescribe a base model, GPU, batch size, LoRA rank, or budget.

### Analytics

```python
import pandas as pd
events = pd.read_parquet("data/parquet/train.parquet")
print(events.columns.tolist())
```

### Ollama after training

Ollama serves models; it does not train directly on this dataset. Fine-tune/export a compatible model first, then follow [ollama/README.md](ollama/README.md). The evaluator uses loopback-only endpoints, so it does not send data to a remote API.

### Harness² and custom benchmark runners

[adapters/harness2_dataset.py](adapters/harness2_dataset.py) supplies local task iteration and exact-match scoring. It is intentionally framework-neutral; adapt its small interface to the current Harness² project contract rather than treating it as a native plugin.

## Evaluation

Prepare JSONL rows with an `id` and JSON `response`, then grade them:

```bash
python tools/evaluate.py --predictions predictions.jsonl --split test
```

For an already running local Ollama model:

```bash
python tools/evaluate.py --run --backend ollama --model your-local-model --split test --output predictions.jsonl
python tools/evaluate.py --predictions predictions.jsonl --split test
```

The grader validates the response schema and reports exact-match accuracy only. It does not establish real-world security effectiveness.

## Quality, limits, and responsible use

- This is a small, short-lived, single-environment collection with substantial coverage bias.
- Labels encode fixed thresholds, not verified maliciousness.
- Temporal features can produce shortcut learning; compare any model with the deterministic baseline.
- Public evaluation answers enable reproducible grading but can contaminate training if used improperly.
- Never execute content derived from this release or let a model make autonomous enforcement decisions.

## Release and licensing

Run these checks before publishing a derivative:

```bash
python -m unittest discover -s tests -p 'test_release.py'
python tools/verify_release.py
```

The verifier writes `release-manifest.json` with SHA-256 digests. [docs/publishing.md](docs/publishing.md) covers Hugging Face and GitLab publication. Private source snapshots, reporting artifacts, logs, and credentials are deliberately excluded and must stay excluded.

The original local dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Give appropriate credit, link the license, and indicate changes. Cite it with [CITATION.cff](CITATION.cff). See [CHANGELOG.md](CHANGELOG.md) for release history.

