# Awesome CVPR 2026 Papers

**A searchable, citation-ready index of CVPR 2026 papers, arXiv links, project pages, and public code resources.**

This repository is designed as a practical discovery hub for researchers, engineers, founders, and students who want to track the CVPR 2026 literature without manually jumping between the official proceedings, virtual poster pages, arXiv, GitHub, and project websites. The name **`awesome-cvpr-2026-papers`** was chosen because it is concise, search-friendly, immediately recognizable in the open-source research community, and aligned with the established “awesome list” convention.

> The official CVF Open Access repository states that these papers are the open-access versions provided by the Computer Vision Foundation, and that, except for the watermark, they are identical to the accepted versions; the final proceedings version is available through IEEE Xplore.[1]

## Repository Snapshot

The current index was generated from the official CVF Open Access list for CVPR 2026 and enriched with public code, project, data, demo, and website links from CVPR virtual pages and community-maintained code indexes.[1] [2] [3] [4] [5]

| Metric | Count | Interpretation |
|---|---:|---|
| CVF Open Access papers indexed | 4,069 | Main-conference papers parsed from the official CVF Open Access all-papers page. |
| Papers with direct arXiv links | 2,671 | Papers where the official CVF page or enrichment sources exposed an arXiv URL. |
| Papers with public code/resource links | 952 | Papers where at least one public code, project, data, demo, model, or resource link was discovered. |
| Papers with direct GitHub repository links | 685 | Papers where a direct `github.com` implementation link was found. |
| Papers mapped to CVPR virtual poster pages | 3,929 | Papers matched to the CVPR 2026 virtual poster program by title. |
| Papers enriched with abstracts and taxonomy labels | 4,069 | Papers categorized by primary area, novelty angle, and inferred improvement mechanism. |

## Why This Repository Exists

CVPR is large enough that a flat proceedings page is difficult to navigate. This repository turns the official proceedings into an engineering-friendly dataset with explicit link columns, so that a reader can quickly answer practical questions such as whether a paper has code, whether the implementation is on GitHub, whether a project website exists, and whether there is an arXiv version to cite or read.

| File | Purpose |
|---|---|
| [`papers.md`](papers.md) | Full Markdown index of all parsed CVPR 2026 papers, including authors, arXiv, CVF PDF, poster, code flag, GitHub links, and project links. |
| [`papers-with-code.md`](papers-with-code.md) | Focused Markdown index of papers with public code, data, demo, model, project, or implementation resources. |
| [`research-map.md`](research-map.md) | Strategic research map that summarizes CVPR 2026 by broad area, novelty angle, improvement axis, and code availability. |
| [`papers-by-category.md`](papers-by-category.md) | Full grouped Markdown index of all papers by automated research category, including novelty and improvement rationale. |
| [`RESEARCH_TAXONOMY.md`](RESEARCH_TAXONOMY.md) | Taxonomy reference explaining the area labels, novelty-angle labels, improvement axes, methodology, and limitations. |
| [`data/cvpr2026_papers.csv`](data/cvpr2026_papers.csv) | Machine-readable CSV version suitable for spreadsheet filtering, scripts, and downstream analysis. |
| [`data/cvpr2026_papers_categorized.csv`](data/cvpr2026_papers_categorized.csv) | Abstract-enriched CSV with `primary_area`, `secondary_area`, `novelty_angle`, `improvement_axis`, and `improvement_rationale`. |
| [`data/cvpr2026_papers.json`](data/cvpr2026_papers.json) | Structured JSON export for applications, search tools, and API-style use. |
| [`data/cvpr2026_papers_categorized.json`](data/cvpr2026_papers_categorized.json) | Structured JSON export of the categorized paper dataset. |
| [`data/category_stats.json`](data/category_stats.json) | Summary counts for research areas, novelty angles, improvement axes, and code availability by area. |
| [`data/taxonomy.json`](data/taxonomy.json) | Machine-readable definition of the research taxonomy and generated label fields. |
| [`data/stats.json`](data/stats.json) | Summary statistics produced by the enrichment script. |
| [`scripts/build_cvpr2026_dataset.py`](scripts/build_cvpr2026_dataset.py) | Reproducible parser used to build the base dataset from public sources. |
| [`scripts/enrich_abstracts.py`](scripts/enrich_abstracts.py) | Fetches and caches CVF abstracts so the categorization layer can reason over title and abstract evidence. |
| [`scripts/categorize_papers.py`](scripts/categorize_papers.py) | Adds automated research-area, novelty-angle, improvement-axis, and rationale labels. |
| [`scripts/generate_category_docs.py`](scripts/generate_category_docs.py) | Generates the research-map, grouped paper index, taxonomy JSON, and supporting charts. |

## What the Columns Mean

The repository separates **direct implementation repositories** from broader public resources because many papers publish their work through project pages, demos, Hugging Face spaces, Colab notebooks, or data portals before releasing a GitHub repository.

| Column | Meaning |
|---|---|
| `title` | Paper title parsed from the official CVF Open Access page. |
| `authors` | Author list parsed from the official CVF Open Access page. |
| `arxiv` | Direct arXiv link when available from CVF or enrichment sources. |
| `cvf_html` and `cvf_pdf` | Official CVF paper landing page and PDF URL. |
| `poster_url` | CVPR 2026 virtual poster page when a title match was found. |
| `code_resource_found` | `Yes` if any public code, data, demo, model, project, or related implementation resource was found. |
| `github` | Direct GitHub repository links only. |
| `website` | Project pages, lab pages, and non-GitHub public resource pages. |
| `model_demo` | Hugging Face, Colab, or model/demo resources when discovered. |
| `link_sources` | Source index that supplied the enrichment link. |
| `abstract` | CVF abstract text used by the categorization layer. |
| `primary_area` and `secondary_area` | Automated broad research-area labels inferred from title and abstract evidence. |
| `novelty_angle` | The main kind of methodological novelty, such as multimodal grounding, geometry priors, new representations, efficiency, safety, or evaluation. |
| `improvement_axis` | The practical improvement the paper appears to target, such as accuracy, speed, scalability, robustness, controllability, or physical consistency. |
| `approach_summary` | A short abstract-derived sentence summarizing the proposed method or contribution. |
| `improvement_rationale` | A compact explanation of why the inferred approach may improve the selected axis. |
| `taxonomy_confidence` | Heuristic confidence score for the automated label assignment. |

## Suggested Use Cases

Researchers can use the Markdown files for quick browsing and the CSV/JSON files for systematic literature review workflows. Engineers can filter the CSV for papers with GitHub links to identify reproducible baselines. Startup teams can monitor project pages and demos to understand which CVPR 2026 ideas are closest to production readiness. The new taxonomy layer adds a higher-level map of **where the field is moving**, organizing the proceedings by broad research area, novelty angle, and the likely reason each method improves over prior work.

| Task | Recommended File | Example Filter |
|---|---|---|
| Find all papers with GitHub code | `data/cvpr2026_papers.csv` | `github` is not empty. |
| Browse all official CVF papers | `papers.md` | Search by title, author, or keyword. |
| Track project pages and demos | `papers-with-code.md` | Review `Project / Website` links. |
| Understand big research directions | `research-map.md` | Compare `primary_area`, `novelty_angle`, and `improvement_axis` distributions. |
| Browse papers by category | `papers-by-category.md` | Jump to an area such as generative models, 3D vision, VLMs, video, robotics, or safety. |
| Build a custom paper search app | `data/cvpr2026_papers_categorized.json` | Load JSON into a search index with category filters. |
| Verify official publication metadata | `papers.md` or CSV | Open the `CVF` and `arXiv` columns. |

## Data Sources and Methodology

The primary source of truth is the official CVF Open Access page for CVPR 2026, which provides paper titles, author names, CVF paper pages, PDFs, supplements, BibTeX entries, page ranges, and many arXiv links.[1] The CVPR 2026 virtual program was used to map papers to poster pages where a normalized title match was possible.[2]

Public code and project links were enriched from multiple public indexes. Paper Digest’s CVPR 2026 code/data page describes itself as an automated index of accepted papers with associated public code or data repositories, while noting that some repositories may become public only around the conference dates.[3] Additional GitHub and project links were merged from community-maintained repositories focused on CVPR 2026 papers with code.[4] [5]

| Source | Data Used | Role |
|---|---|---|
| CVF Open Access | Titles, authors, PDFs, supplements, BibTeX, page ranges, arXiv links | Authoritative paper metadata. |
| CVPR Virtual Program | Poster page URLs and poster identifiers | Poster/session navigation. |
| Paper Digest Code/Data Index | Code, data, demo, and project-resource links | Broad public resource enrichment. |
| amusi CVPR2026 Papers with Code | GitHub, project, and arXiv links | Community code enrichment. |
| SkalskiP Top CVPR 2026 Papers | Curated high-signal code, demo, and project links | Additional curated enrichment. |

## Limitations

The `code_resource_found` field should be interpreted as **discovered public resource availability**, not a guarantee that a paper has a complete, official, maintained implementation. Some links point to project pages, demos, model cards, data resources, or repositories that may be private, incomplete, or released later. Conversely, some papers may have code that was missed because it was released after the scrape, published under a different title, or hosted on a non-indexed page.

The taxonomy labels are **automated navigation labels**, not peer-reviewed subject classifications. They are generated from paper titles and abstracts using a deterministic keyword-scoring pipeline. This makes the repository easier to browse at CVPR scale, but readers should still use the official paper, arXiv link, and project page to verify a paper’s exact contribution.

The official CVF Open Access page contained 4,069 parsed main-conference entries at build time, while some community pages mention a larger accepted-paper count for CVPR 2026. This repository intentionally reports the number parsed from the official open-access source used to construct the dataset rather than asserting a separate acceptance statistic.[1] [5]

## Updating the Dataset

To rebuild the dataset, refresh the source HTML files and run the parser. The script is intentionally kept in the repository so future updates can add newly released repositories, project pages, or arXiv links.

```bash
python3 scripts/build_cvpr2026_dataset.py
python3 scripts/enrich_abstracts.py
python3 scripts/categorize_papers.py
python3 scripts/generate_category_docs.py
```

A future improvement would be to add scheduled refreshes, GitHub Actions, or a lightweight web UI that supports full-text search, category facets, topic tags, and sorting by code availability.

## Contributing

Contributions are welcome, especially corrections for missing code repositories, official project pages, arXiv links, and broken URLs. Please include a source link when opening a pull request so the entry can be verified quickly.

## References

[1]: https://openaccess.thecvf.com/CVPR2026?day=all "CVPR 2026 Open Access Repository — Computer Vision Foundation"
[2]: https://cvpr.thecvf.com/virtual/2026/papers.html "CVPR 2026 Virtual Papers — The Computer Vision Foundation"
[3]: https://www.paperdigest.org/2026/06/cvpr-2026-papers-with-code-data/ "CVPR 2026 Papers with Code & Data — Paper Digest"
[4]: https://github.com/amusi/CVPR2026-Papers-with-Code "amusi/CVPR2026-Papers-with-Code"
[5]: https://github.com/SkalskiP/top-cvpr-2026-papers "SkalskiP/top-cvpr-2026-papers"
