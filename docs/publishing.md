# Publishing

## Hugging Face Dataset repository

After reviewing the release locally, create a public dataset repository and upload this directory:

```bash
hf repos create YOUR_NAMESPACE/tpot-evidence-lab --type dataset --public
hf upload YOUR_NAMESPACE/tpot-evidence-lab . --type dataset --commit-message "Release T-Pot Evidence Lab v3.0.0"
```

The YAML front matter in `README.md` declares the default chat configuration. The `data/parquet/` files remain available for analytics.

## GitLab repository and Pages

Create a new public GitLab project, commit this directory, and push it. `.gitlab-ci.yml` validates the release and publishes `site/` as GitLab Pages. The page links to the final Hugging Face dataset URL once that URL is set in `site/config.js`.

## Before publishing

Run `python -m unittest discover -s tests -p 'test_release.py'` and `python tools/verify_release.py`. Do not add the private snapshot, prior reporting ledgers, API keys, logs, or archives to either repository.

