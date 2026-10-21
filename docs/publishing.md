# Publishing the reviewed candidate

This working copy is a local 3.1.0 candidate. Publication requires the repository owner's explicit approval. Existing GitLab CI is unchanged.

```bash
python -m unittest discover -s tests -p 'test_*.py'
node tests/test_preview.cjs
python tools/verify_release.py
```

README front matter and `card-metadata.yaml` must agree. `observations` must remain the default configuration so visitors land on the structured table. The original chat material is available as `chat`. Preserve every original data format and retain third-party notices.

After approval, upload the reviewed directory to `Magnexis/tpot-evidence-lab` with `hf upload`, excluding `.git`, `__pycache__`, and `.cache`. Review the GitLab diff before committing and pushing. Its existing Pages job publishes `site/`. Do not upload source archives, private snapshots, source mappings, or reporting artifacts.

To preview the site locally, run `python -m http.server 8000 --bind localhost --directory site` and open the loopback URL. The preview contains a bounded, explicitly labelled selection of real records; full tables are linked on Hugging Face. It never loads raw traffic or executes captured text.
