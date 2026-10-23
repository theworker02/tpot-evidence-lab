# Versioning and release procedure

`VERSION` is the release version. The card loading revision, citation and site configuration must match the package version. Defensive statistics and row dataset_version identify the data revision, which can remain unchanged in a packaging-only patch. Use semantic versions: patch for compatible corrections/documentation, minor for additive configurations/collections, major for changed schemas or label contracts in existing configurations. Never silently replace a tagged release; record corrections and affected versions in CHANGELOG.md.

Version 3.2.0 is additive. GitHub is the current source/release destination, GitHub Pages serves the inert site directory, and Hugging Face hosts dataset files and viewer configurations. The historical GitLab repository remains a provenance source; this release does not push there.

## Verification

Python 3.12+ and Node.js 20+ are sufficient. Loading/checks require no GPU.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-validation.txt
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
node tests/test_preview.cjs
node tests/test_scenarios.cjs
.venv/bin/python tools/verify_hf_configs.py
python tools/verify_release.py
git diff --check
```

On Windows use .venv/Scripts/python and .venv/Scripts/pip. The Hub verifier loads local Parquet offline. README front matter and card-metadata.yaml must agree; observations remains default. The SHA-256 manifest excludes itself, Git metadata and caches. Text uses LF for stable cross-platform hashes. Import tooling refuses changed source hashes and overwriting existing outputs. See defensive-dataset.md for the private-local reproducibility boundary.

## Publish an approved release

Review the diff, rights and manifest. Never include original captures, private snapshots, mappings, credentials, reporting ledgers or correspondence. Commit only the dedicated public repository. Push main to https://github.com/theworker02/tpot-evidence-lab, create the version tag and a GitHub release containing the reviewed archive, release manifest and archive checksums.

Split site/ into gh-pages and push that branch to GitHub; configure Pages to publish its root. No server, analytics or paid hosting is required. The browser renders example text without executing it; filtering does not transmit telemetry.

Use hf upload --type dataset to upload only reviewed manifest-listed public files to Magnexis/tpot-evidence-lab. Preserve existing remote files; do not use deletion patterns. Exclude Git metadata, environments, caches and private artifacts. Tag the Hub commit with the release version and verify viewer configurations, remote hashes and metadata. GitHub and Hub have different commit IDs; matching version tags identify corresponding releases.

Save publication receipts privately outside the repository. Confirm CI passes, Pages succeeds and both new configurations have expected counts. Viewer generation may lag uploads; report its actual state. Nothing publishes automatically on import; CI verifies but never uploads to the Hub.

Local site preview: python -m http.server 8000 --bind localhost --directory site. The preview is a bounded selection of actual rows. The legacy evaluator grades only the original fixed-rule task, not expanded task-dependent responses.
