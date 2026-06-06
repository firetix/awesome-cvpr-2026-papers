# Contributing

Thank you for helping improve **Awesome CVPR 2026 Papers**. This repository is intended to be a reliable discovery index for CVPR 2026 papers, arXiv links, official pages, project websites, and public code resources.

## What to Contribute

High-value contributions include missing official GitHub repositories, project websites, arXiv links, corrected paper metadata, broken-link fixes, and improved parsing logic. Please prefer official author links when available, and include a source URL in every pull request so the update can be verified quickly.

| Contribution Type | Required Evidence |
|---|---|
| GitHub repository | A direct repository URL, preferably linked from the paper, project page, or author profile. |
| Project website | A public project page associated with the paper title or authors. |
| arXiv link | A matching arXiv abstract URL for the paper. |
| Metadata correction | A citation to the CVF paper page, arXiv page, or official project page. |
| Parser improvement | A short explanation of the source format and expected output change. |

## Data Quality Policy

A `code_resource_found` value of `Yes` means a public code, data, demo, model, project, or implementation-related resource was discovered. It does not guarantee that the resource is complete, official, maintained, or reproducible. When possible, direct GitHub repositories should be placed in the `github` field and project/demo pages should be placed in `website` or `model_demo`.

## Rebuilding the Dataset

Install the Python dependency and run the builder from the repository root.

```bash
pip install -r requirements.txt
python3 scripts/build_cvpr2026_dataset.py
```

The generated outputs are `papers.md`, `papers-with-code.md`, `data/cvpr2026_papers.csv`, `data/cvpr2026_papers.json`, and `data/stats.json`.
