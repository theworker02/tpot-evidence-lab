---
language:
- en
license: cc-by-4.0
task_categories:
- text-classification
- text-generation
tags:
- cybersecurity
- honeypot
- weak-supervision
- defensive-security
pretty_name: T-Pot Evidence Lab
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/chat/train.jsonl
  - split: validation
    path: data/chat/validation.jsonl
  - split: test
    path: data/chat/test.jsonl
---

# T-Pot Evidence Lab

**A sanitized, weakly labelled honeypot-evidence dataset for defensive-security research, local model evaluation, and training-pipeline prototyping.**

This is a small, static release derived from a locally operated T-Pot honeypot deployment. It supports one narrow, auditable task: given a compact summary of observed honeypot behavior, determine whether the evidence meets a fixed incident-reporting threshold and name that threshold. It is not a general internet-threat corpus, a botnet-attribution dataset, a malware corpus, or evidence of production compromise.

## Access the release

- **Download and use the dataset:** [Hugging Face — Magnexis/tpot-evidence-lab](https://huggingface.co/datasets/Magnexis/tpot-evidence-lab)
- **Browse the repository, documentation, and release history:** [GitLab — theworker02/tpot-evidence-lab](https://gitlab.com/theworker02/tpot-evidence-lab)
- **Project landing page:** [T-Pot Evidence Lab on GitLab Pages](https://tpot-evidence-lab-ec5dff.gitlab.io)

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
dataset = load_dataset("YOUR_NAMESPACE/tpot-evidence-lab", "default")
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

This dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Give appropriate credit, link the license, and indicate changes. Cite it with [CITATION.cff](CITATION.cff). See [CHANGELOG.md](CHANGELOG.md) for release history.

