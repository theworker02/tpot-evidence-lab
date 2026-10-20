# Training and evaluation adapters

## Unsloth, TRL, and Hugging Face

Use `data/chat/*.jsonl`: every row has a `messages` array with `system`, `user`, and `assistant` entries. Apply the chat template for the base model you choose. Do not train on `evaluation/answers.jsonl` when measuring held-out results.

## Axolotl

`adapters/axolotl-dataset.yaml` declares the chat path and `type: chat_template`. Merge its dataset block into your model-specific Axolotl configuration.

## LLaMA Factory

`data/sharegpt/*.jsonl` uses `from`/`value` messages. Add the paths from `adapters/dataset_info.json` to your LLaMA Factory dataset registry.

## Ollama

Ollama runs models; it does not train directly on a JSONL dataset. Fine-tune a compatible base model first using one of the formats above, export merged weights or GGUF, then use [ollama/README.md](ollama/README.md) to import it. `tools/evaluate.py --run` can evaluate an already running local Ollama model without sending data to a remote service.

## Harness²

`adapters/harness2_dataset.py` is a small local task-and-grading bridge. It is intentionally framework-neutral because Harness² integration contracts vary by project. Adapt its `iter_tasks` and `score` methods to the project’s current benchmark adapter interface; it does not claim native plug-and-play support.

