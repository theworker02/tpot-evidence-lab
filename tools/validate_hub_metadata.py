"""Validate the public dataset card with the Hub's metadata endpoint (network required)."""
from pathlib import Path
from huggingface_hub import DatasetCard

if __name__=='__main__':
    path=Path(__file__).resolve().parents[1]/'README.md'
    DatasetCard.load(str(path)).validate()
    print('Hugging Face server-side dataset card validation passed.')
