# Awesome CVPR 2026 Papers

**A research-map-driven index of CVPR 2026 papers with code availability, GitHub repositories, arXiv links, project pages, and practical taxonomy labels.**

This repository turns the CVPR 2026 proceedings into a browsable and machine-readable discovery layer for researchers, engineers, students, founders, and applied AI teams. Instead of being only a flat list of papers, **`awesome-cvpr-2026-papers`** combines official CVF metadata, arXiv links, public code/resource discovery, project websites, abstracts, and automatically inferred research categories so that readers can quickly find papers that are both scientifically relevant and practically actionable.[1] [2] [3]

> The official CVF Open Access repository states that the available papers are open-access versions provided by the Computer Vision Foundation and that, except for the watermark, they are identical to the accepted versions; the final proceedings version is available through IEEE Xplore.[1]

## Start Here

The fastest way to use the repository is to choose the entry point that matches your goal. The Markdown files are optimized for human browsing, while the CSV and JSON exports are designed for systematic literature review, internal research tooling, dashboards, and search applications.

| Goal | Start With | Best For |
|---|---|---|
| Browse every indexed CVPR 2026 paper | [`papers.md`](papers.md) | Full proceedings-style navigation with CVF, arXiv, code, GitHub, and website links. |
| Find papers with implementations or public resources | [`papers-with-code.md`](papers-with-code.md) | Engineers, practitioners, and reproducibility-focused readers. |
| Understand the big research directions | [`research-map.md`](research-map.md) | Strategic overviews, literature planning, and field-level trend discovery. |
| Browse by research area and novelty angle | [`papers-by-category.md`](papers-by-category.md) | Topic-first exploration across generative vision, 3D, VLMs, video, robotics, safety, and more. |
| Reuse the dataset programmatically | [`data/cvpr2026_papers_categorized.csv`](data/cvpr2026_papers_categorized.csv) | Scripts, notebooks, dashboards, search indexes, and internal knowledge bases. |
| Understand the taxonomy | [`RESEARCH_TAXONOMY.md`](RESEARCH_TAXONOMY.md) | Transparent interpretation of labels, improvement axes, confidence, and limitations. |

## Highlights at a Glance

The current build indexes **4,069 CVF Open Access papers**, including **2,671 arXiv links**, **952 discovered public code/resource matches**, **685 direct GitHub repository links**, and **3,929 mapped CVPR virtual poster pages**.[6] The categorization layer covers **4,069 papers with abstracts**, assigning each paper a primary research area, secondary area, novelty angle, improvement axis, application context, approach summary, and improvement rationale.[7]

| Metric | Count | Why It Matters |
|---|---:|---|
| CVF Open Access papers indexed | 4,069 | Provides broad coverage of the official open-access CVPR 2026 paper list used by this repository. |
| Papers with direct arXiv links | 2,671 | Makes preprints and citation-friendly versions easier to access. |
| Papers with public code/resource links | 952 | Surfaces papers with code, datasets, demos, project pages, model resources, or related implementation assets. |
| Papers with direct GitHub repository links | 685 | Helps users identify reproducible baselines and implementation-ready projects. |
| Papers mapped to CVPR virtual poster pages | 3,929 | Adds conference-program navigation and poster-page context. |
| Papers with taxonomy labels and abstracts | 4,069 | Enables trend analysis, category browsing, and higher-level literature discovery. |

![CVPR 2026 research-area distribution](assets/cvpr2026_area_distribution.png)

## Why This Repository Exists

CVPR is large enough that even highly motivated readers can miss important papers when the only navigation layer is a proceedings page, search bar, or social-media thread. This repository is designed to reduce that friction. It provides a **single, structured, version-controlled resource** for identifying what was published, which papers have public implementations, how papers cluster into major research directions, and what kind of improvement each method appears to target.

| Audience | What This Repository Helps Them Do |
|---|---|
| Researchers | Build reading lists, compare neighboring papers, find arXiv versions, and discover papers by area or novelty angle. |
| Engineers | Filter for GitHub-backed papers, project pages, demos, datasets, and implementation resources. |
| Students | Explore CVPR 2026 by major topic instead of reading the proceedings sequentially. |
| Founders and product teams | Track practical advances in generative media, 3D reconstruction, video understanding, robotics, medical vision, document AI, and trustworthy AI. |
| Dataset and tooling builders | Load CSV/JSON exports into search indexes, dashboards, recommendation systems, and internal knowledge bases. |

## Research Trend Snapshot

The automated taxonomy suggests that the largest inferred CVPR 2026 research areas in this dataset are **Generative Models, Editing & Creative Vision** with **750 papers** and **3D Vision, Geometry & Neural Rendering** with **748 papers**.[7] Together, these two areas account for **1,498 indexed papers**, showing how strongly the conference is oriented toward controllable generation, reconstruction, spatial intelligence, and visual world modeling.[7]

| Rank | Primary Area | Papers | Public Code / Resource Links | Direct GitHub Links |
|---:|---|---:|---:|---:|
| 1 | Generative Models, Editing & Creative Vision | 750 | 161 | 110 |
| 2 | 3D Vision, Geometry & Neural Rendering | 748 | 156 | 83 |
| 3 | Learning, Optimization & Efficient Foundation Models | 457 | 111 | 103 |
| 4 | Video, Motion & Temporal Understanding | 417 | 88 | 60 |
| 5 | Vision-Language & Multimodal Intelligence | 352 | 77 | 55 |
| 6 | Recognition, Detection & Segmentation | 341 | 99 | 86 |
| 7 | Datasets, Benchmarks & Evaluation | 250 | 79 | 48 |
| 8 | Embodied AI, Robotics & Autonomous Driving | 220 | 41 | 23 |

The novelty-angle distribution also highlights the shape of the field. **Multimodal fusion and grounding** appears as the largest inferred novelty angle, followed by **geometry or physical priors**, **application or system integration**, and **efficiency, acceleration, or compression**.[7]

![CVPR 2026 novelty-angle distribution](assets/cvpr2026_novelty_angles.png)

| Novelty Angle | Papers | Interpretation |
|---|---:|---|
| Multimodal Fusion / Grounding | 823 | Methods that connect vision with language, audio, 3D, actions, prompts, or other modalities. |
| Geometry or Physical Prior | 753 | Papers that use structure, shape, camera geometry, physical constraints, or spatial consistency. |
| Application or System Integration | 496 | Work that packages methods into complete systems, pipelines, deployment scenarios, or domain applications. |
| Efficiency / Acceleration / Compression | 361 | Approaches focused on reducing inference cost, memory, compute, data needs, or training overhead. |
| Model Architecture | 314 | Papers where the main contribution is a new network, module, transformer variant, or architectural design. |
| New Representation | 267 | Work proposing new latent spaces, scene formats, features, tokens, fields, or visual abstractions. |
| Data, Dataset or Synthetic-Data Engine | 266 | Contributions centered on new datasets, generated training data, annotation methods, or benchmark construction. |

## Browse the Collection

The repository is intentionally organized around both **human-readable Markdown** and **machine-readable data files**. This makes it useful as a public awesome list, a research map, and a reusable dataset.

| File | Purpose |
|---|---|
| [`papers.md`](papers.md) | Full Markdown index of all parsed CVPR 2026 papers, including authors, arXiv, CVF PDF, poster, code flag, GitHub links, and project links. |
| [`papers-with-code.md`](papers-with-code.md) | Focused Markdown index of papers with public code, data, demo, model, project, or implementation resources. |
| [`research-map.md`](research-map.md) | Strategic research map summarizing CVPR 2026 by broad area, novelty angle, improvement axis, and code availability. |
| [`papers-by-category.md`](papers-by-category.md) | Grouped Markdown index of all papers by automated research category, including novelty and improvement rationale. |
| [`RESEARCH_TAXONOMY.md`](RESEARCH_TAXONOMY.md) | Taxonomy reference explaining the area labels, novelty-angle labels, improvement axes, methodology, and limitations. |
| [`data/cvpr2026_papers.csv`](data/cvpr2026_papers.csv) | Base CSV dataset suitable for spreadsheet filtering, scripts, and downstream analysis. |
| [`data/cvpr2026_papers_categorized.csv`](data/cvpr2026_papers_categorized.csv) | Abstract-enriched CSV with category labels, novelty labels, improvement axes, and rationales. |
| [`data/cvpr2026_papers.json`](data/cvpr2026_papers.json) | Structured JSON export for applications, search tools, and API-style use. |
| [`data/cvpr2026_papers_categorized.json`](data/cvpr2026_papers_categorized.json) | Structured JSON export of the categorized paper dataset. |
| [`data/category_stats.json`](data/category_stats.json) | Summary counts for research areas, novelty angles, improvement axes, and code availability by area. |
| [`data/taxonomy.json`](data/taxonomy.json) | Machine-readable definition of the taxonomy labels and generated fields. |
| [`data/stats.json`](data/stats.json) | Summary statistics produced by the enrichment pipeline. |

## Papers With Code and Public Resources

The `code_resource_found` field should be read as a practical discovery flag. It indicates that the pipeline found at least one public code, data, demo, model, project, or related implementation resource, while the `github` field is stricter and only stores direct `github.com` repository links.[3] [4] [5]

| Resource Type | Where to Look | Practical Use |
|---|---|---|
| Direct GitHub implementations | `github` column and [`papers-with-code.md`](papers-with-code.md) | Clone code, inspect reproducibility, compare baselines, and evaluate implementation quality. |
| Project websites | `website` column | Find demos, method pages, videos, data portals, checkpoints, and official release notes. |
| Model and demo resources | `model_demo` column | Locate Hugging Face spaces, model cards, hosted demos, or notebooks when available. |
| CVF and arXiv links | `cvf_html`, `cvf_pdf`, and `arxiv` columns | Read the official paper, cite the work, and compare camera-ready and preprint versions. |

## Most Actionable Research Angles

For applied users, the repository can be read as a map from research contribution to practical opportunity. A paper may be scientifically important without having code, but papers with public code, demos, or project pages are often easier to evaluate quickly.

| Practical Angle | Useful Categories | Suggested Workflow |
|---|---|---|
| Image and video generation | Generative Models, Editing & Creative Vision; Video, Motion & Temporal Understanding | Filter for `code_resource_found`, then inspect project pages for demos, checkpoints, and controllability examples. |
| 3D reconstruction and spatial AI | 3D Vision, Geometry & Neural Rendering; Embodied AI, Robotics & Autonomous Driving | Use `primary_area` plus `novelty_angle = Geometry or Physical Prior` to find spatially grounded methods. |
| Multimodal and VLM systems | Vision-Language & Multimodal Intelligence; Learning, Optimization & Efficient Foundation Models | Search for grounding, reasoning, instruction tuning, retrieval, and multimodal fusion labels. |
| Efficient deployment | Learning, Optimization & Efficient Foundation Models; Recognition, Detection & Segmentation | Filter by `improvement_axis = Efficiency / Speed` or `novelty_angle = Efficiency / Acceleration / Compression`. |
| Safety and robustness | Safety, Robustness, Privacy & Trustworthy CV | Prioritize papers whose improvement axis is robustness, trustworthiness, privacy, or evaluation clarity. |
| Domain applications | Medical, Scientific, Remote-Sensing & Domain Vision; Document, OCR & Visual Information Extraction | Use category labels to identify applied pipelines and datasets that may transfer into products. |

## Research Taxonomy

The taxonomy is designed to make the collection searchable by **big angle**, **novel approach**, and **reason for improvement**. Each paper receives a primary area, secondary area, novelty angle, improvement axis, application context, approach summary, improvement rationale, evidence sentence, confidence score, and research tags.[7]

| Taxonomy Field | Meaning |
|---|---|
| `primary_area` | The broadest inferred research family, such as generative vision, 3D vision, VLMs, video, robotics, medical vision, safety, or low-level vision. |
| `secondary_area` | A secondary category when the paper appears to bridge multiple areas. |
| `novelty_angle` | The main type of contribution, such as multimodal grounding, new representation, model architecture, efficiency, evaluation, or safety. |
| `improvement_axis` | The practical dimension the method appears to improve, such as quality, speed, scalability, robustness, controllability, or physical consistency. |
| `application_context` | The likely applied context inferred from the title and abstract. |
| `approach_summary` | A compact title-and-abstract-derived summary of the proposed approach. |
| `improvement_rationale` | A short explanation of why the method may improve the selected axis. |
| `taxonomy_confidence` | A heuristic confidence score for the automated label assignment. |
| `research_tags` | Additional keywords that make filtering and search easier. |

## How Categorization Works

The categorization layer is deterministic and reproducible. It uses CVF titles and abstracts, applies taxonomy-specific keyword and phrase scoring, assigns broad areas and novelty labels, and generates short rationale fields from the available evidence. This makes the repository easier to browse at CVPR scale, but the labels should be interpreted as **navigation aids**, not peer-reviewed subject classifications.[7]

| Step | Output | Notes |
|---|---|---|
| Parse official metadata | Base paper records | Titles, authors, CVF URLs, PDFs, supplements, BibTeX keys, page ranges, and arXiv links are parsed from CVF Open Access where available.[1] |
| Match conference pages | Poster URLs | Normalized title matching links papers to CVPR virtual poster pages when possible.[2] |
| Merge public resource indexes | Code, GitHub, website, demo, and model links | Public resource discovery is merged from Paper Digest and community-maintained GitHub indexes.[3] [4] [5] |
| Fetch abstracts | Abstract-enriched records | Abstracts support more accurate taxonomy assignment than title-only categorization. |
| Assign taxonomy labels | Categorized CSV, JSON, and Markdown | Research areas, novelty angles, improvement axes, and rationales are generated into reusable artifacts. |

## Dataset Schema

The dataset separates official publication metadata from discovered implementation resources and inferred research labels. This makes the data useful both for citation-aware literature review and for practical code-first exploration.

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
| `novelty_angle` | The main kind of methodological novelty inferred for the paper. |
| `improvement_axis` | The practical improvement the paper appears to target. |
| `application_context` | The applied or scientific setting inferred for the paper. |
| `approach_summary` | A short evidence-derived sentence summarizing the contribution. |
| `improvement_rationale` | A compact explanation of why the approach may improve the selected axis. |
| `taxonomy_confidence` | Heuristic confidence score for the automated label assignment. |

## Programmatic Usage

The categorized CSV can be loaded directly with pandas. The example below finds GitHub-backed papers in a specific research area and exports a focused reading list.

```python
import pandas as pd

papers = pd.read_csv("data/cvpr2026_papers_categorized.csv")

subset = papers[
    (papers["primary_area"] == "Generative Models, Editing & Creative Vision")
    & papers["github"].fillna("").ne("")
]

subset[["title", "authors", "arxiv", "github", "website", "novelty_angle", "improvement_axis"]].to_csv(
    "generative_cvpr2026_with_github.csv",
    index=False,
)
```

The JSON export can also be loaded into a static search page, a vector database, a local knowledge base, or an internal research assistant. For search applications, the most useful fields are usually `title`, `authors`, `abstract`, `primary_area`, `novelty_angle`, `improvement_axis`, `github`, `website`, and `arxiv`.

## Rebuilding and Updating the Dataset

To rebuild the dataset, install the dependencies and run the scripts in order. The scripts are included so future updates can add newly released repositories, project pages, arXiv links, corrected links, and improved taxonomy rules.

```bash
pip install -r requirements.txt
python3 scripts/build_cvpr2026_dataset.py
python3 scripts/enrich_abstracts.py
python3 scripts/categorize_papers.py
python3 scripts/validate_categories.py
python3 scripts/generate_category_docs.py
```

| Script | Purpose |
|---|---|
| [`scripts/build_cvpr2026_dataset.py`](scripts/build_cvpr2026_dataset.py) | Rebuilds the base dataset from public CVF, virtual-program, and community resource pages. |
| [`scripts/enrich_abstracts.py`](scripts/enrich_abstracts.py) | Fetches and caches CVF abstracts for categorization. |
| [`scripts/categorize_papers.py`](scripts/categorize_papers.py) | Adds research-area, novelty-angle, improvement-axis, and rationale labels. |
| [`scripts/validate_categories.py`](scripts/validate_categories.py) | Produces validation statistics and spot-check summaries for generated labels. |
| [`scripts/generate_category_docs.py`](scripts/generate_category_docs.py) | Generates the research map, grouped category index, taxonomy JSON, and charts. |

## Contribution Guide

Contributions are welcome, especially corrections for missing code repositories, official project pages, arXiv links, broken URLs, duplicate entries, and taxonomy improvements. Please include a source link with each correction so the update can be verified quickly.

| Contribution Type | What to Include |
|---|---|
| Add missing code | Paper title, official paper link, repository URL, and whether the repository is official or community-maintained. |
| Add a project page | Paper title, project website URL, and source evidence from the paper, author page, or official repository. |
| Fix metadata | The incorrect field, corrected value, and a source URL. |
| Improve taxonomy | Paper title, current label, suggested label, and a short explanation. |
| Report broken links | Broken URL, paper title, and replacement URL if available. |

## Quality, Caveats, and Limitations

The `code_resource_found` field means that a public resource was discovered; it does not guarantee that the code is official, complete, maintained, reproducible, or released under a permissive license. Some links point to project pages, model cards, demos, datasets, or repositories that may become public later. Conversely, some papers may have code that was missed because it was released after the scrape, hosted under a different title, or published outside the indexed sources.[3] [4] [5]

The taxonomy labels are automated discovery labels rather than authoritative paper classifications. They are intended to help readers explore CVPR at scale, identify neighboring papers, and reason about likely improvement mechanisms. Readers should always consult the official paper, arXiv version, project page, and repository before making technical or citation decisions.

## Suggested Citation and Acknowledgement

If this repository helps your research, reading group, product exploration, or internal tooling, please consider starring the repository and linking to it from your own work. A lightweight citation format is provided below.

```bibtex
@misc{awesome_cvpr_2026_papers,
  title        = {Awesome CVPR 2026 Papers},
  author       = {Manus AI and contributors},
  year         = {2026},
  howpublished = {\url{https://github.com/firetix/awesome-cvpr-2026-papers}},
  note         = {CVPR 2026 paper index with code links, arXiv links, project pages, and research taxonomy}
}
```

## Roadmap

Future improvements could make the repository more useful as both an awesome list and a research-intelligence dataset. High-impact additions include periodic refreshes, GitHub Actions for link checking, GitHub star counts for implementation repositories, official-code verification, topic-specific leaderboards, a lightweight searchable web UI, and richer human-reviewed taxonomy corrections.

| Future Feature | Expected Benefit |
|---|---|
| Scheduled refreshes | Captures newly released code, project pages, demos, and arXiv updates. |
| Link-health checks | Detects broken project pages and moved repositories. |
| GitHub metadata enrichment | Adds stars, forks, license, last commit date, and implementation activity. |
| Official-code verification | Distinguishes author-maintained implementations from community implementations. |
| Searchable web interface | Provides filters for area, novelty angle, code availability, and application context. |
| Human-reviewed taxonomy improvements | Increases trust and precision for high-traffic categories. |

## References

[1]: https://openaccess.thecvf.com/CVPR2026?day=all "CVPR 2026 Open Access Repository — Computer Vision Foundation"
[2]: https://cvpr.thecvf.com/virtual/2026/papers.html "CVPR 2026 Virtual Papers — The Computer Vision Foundation"
[3]: https://www.paperdigest.org/2026/06/cvpr-2026-papers-with-code-data/ "CVPR 2026 Papers with Code & Data — Paper Digest"
[4]: https://github.com/amusi/CVPR2026-Papers-with-Code "amusi/CVPR2026-Papers-with-Code"
[5]: https://github.com/SkalskiP/top-cvpr-2026-papers "SkalskiP/top-cvpr-2026-papers"
[6]: data/stats.json "Repository-generated base dataset statistics"
[7]: data/category_stats.json "Repository-generated taxonomy and category statistics"
