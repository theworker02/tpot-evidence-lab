# Ollama deployment after training

This dataset is training data, not an Ollama model. After fine-tuning and exporting a compatible local model, copy `Modelfile.template` to `Modelfile`, replace the `FROM` path, then run:

```bash
ollama create tpot-evidence-lab -f Modelfile
ollama run tpot-evidence-lab
python tools/evaluate.py --run --backend ollama --model tpot-evidence-lab --split test --output predictions.jsonl
python tools/evaluate.py --predictions predictions.jsonl --split test
```

The evaluator accepts loopback-only endpoints, so it does not send this data to a remote API.

