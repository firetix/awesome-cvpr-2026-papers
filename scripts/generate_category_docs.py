from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from textwrap import dedent

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
CSV_PATH = DATA / "cvpr2026_papers_categorized.csv"
STATS_PATH = DATA / "category_stats.json"
RESEARCH_MAP = ROOT / "research-map.md"
PAPERS_BY_CATEGORY = ROOT / "papers-by-category.md"
TAXONOMY_DOC = ROOT / "RESEARCH_TAXONOMY.md"
TAXONOMY_JSON = DATA / "taxonomy.json"

AREA_DESCRIPTIONS = {
    "Generative Models, Editing & Creative Vision": "Papers that create, edit, synthesize, or control visual media, including diffusion, flow matching, image/video generation, style transfer, and creative reconstruction pipelines.",
    "3D Vision, Geometry & Neural Rendering": "Papers focused on 3D understanding, multiview geometry, depth, pose, reconstruction, neural rendering, Gaussian splatting, SLAM, point clouds, meshes, and radiance-field style representations.",
    "Learning, Optimization & Efficient Foundation Models": "Papers where the central contribution is training strategy, representation learning, distillation, compression, quantization, test-time adaptation, or efficient foundation-model use.",
    "Video, Motion & Temporal Understanding": "Papers whose main signal is temporal: video understanding, motion modeling, tracking, frame-level dynamics, long-context video, scene flow, and temporal consistency.",
    "Vision-Language & Multimodal Intelligence": "Papers connecting vision with language or other modalities, including VLMs, MLLMs, grounding, VQA, captioning, open-vocabulary recognition, and multimodal reasoning.",
    "Recognition, Detection & Segmentation": "Papers centered on object/category recognition, detection, segmentation, localization, open-set/open-vocabulary recognition, and related dense prediction tasks.",
    "Datasets, Benchmarks & Evaluation": "Papers whose contribution is primarily a dataset, benchmark, evaluation protocol, metric, diagnostic suite, or empirical measurement framework.",
    "Embodied AI, Robotics & Autonomous Driving": "Papers tied to physical or simulated agents, including robotics, manipulation, navigation, autonomous driving, world models, and vision-language-action systems.",
    "Safety, Robustness, Privacy & Trustworthy CV": "Papers that examine robustness, jailbreaks, adversarial behavior, privacy, watermarking, bias, uncertainty, out-of-distribution behavior, or safety evaluation.",
    "Human-Centric Vision, Biometrics & Behavior": "Papers about people, bodies, hands, faces, gait, re-identification, gaze, emotion, talking heads, avatars, and human-object interaction.",
    "Medical, Scientific, Remote-Sensing & Domain Vision": "Papers applying CV to specialized domains such as medical imaging, biology, pathology, remote sensing, aerial/satellite imagery, industrial inspection, and scientific measurement.",
    "Low-Level Vision & Computational Photography": "Papers on restoration, super-resolution, denoising, deblurring, dehazing, HDR, low-light imaging, image quality, compression, ISP, and camera pipelines.",
    "Document, OCR & Visual Information Extraction": "Papers about scene text, OCR, document parsing, chart/table understanding, layout analysis, reading order, and visual information extraction.",
    "General Computer Vision": "Papers that did not receive a high-confidence match to a more specific automated category.",
}

NOVELTY_DESCRIPTIONS = {
    "New Representation": "The contribution changes how visual information is encoded, tokenized, factorized, or represented.",
    "Model Architecture": "The contribution is mainly a network, module, backbone, attention mechanism, adapter, encoder-decoder, or architectural design.",
    "Training / Pretraining Objective": "The contribution is mainly a loss, training schedule, pretraining strategy, distillation setup, or adaptation objective.",
    "Data, Dataset or Synthetic-Data Engine": "The contribution is mainly a dataset, benchmark, annotation source, simulator, synthetic-data generator, or data pipeline.",
    "Efficiency / Acceleration / Compression": "The contribution improves speed, memory, compute, model size, sampling cost, latency, or deployment practicality.",
    "Multimodal Fusion / Grounding": "The contribution aligns, fuses, or grounds information across vision, language, audio, actions, or other modalities.",
    "Reasoning, Planning or Agentic Control": "The contribution emphasizes reasoning, planning, control, agent behavior, policies, or decision-making.",
    "Editing, Control or Compositionality": "The contribution improves controllability, editing, composition, style, layout, or attribute-level manipulation.",
    "Geometry or Physical Prior": "The contribution injects 3D, geometric, multiview, camera, physics, ray, or rendering priors.",
    "Robustness, Safety or Privacy Method": "The contribution proposes a method for safety, robustness, privacy, watermarking, bias mitigation, attacks, or defenses.",
    "Evaluation, Benchmark or Metric": "The contribution creates or improves measurement, protocols, diagnostics, metrics, or leaderboards.",
    "Application or System Integration": "The contribution packages multiple components into a practical system, framework, pipeline, or domain-specific solution.",
    "Theoretical or Analytical Insight": "The contribution is primarily an analysis, theory, diagnostic study, or principled interpretation.",
}


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def pct(n: int, total: int) -> str:
    return f"{(100*n/total):.1f}%" if total else "0.0%"


def first_link(value: str) -> str:
    if not value:
        return ""
    return value.split("; ")[0].strip()


def link(label: str, url: str) -> str:
    if not url:
        return ""
    return f"[{label}]({url})"


def code_flag(row: dict) -> str:
    if str(row.get("code_resource_found", "")).lower() in {"true", "yes", "1"}:
        return "Yes"
    return "No"


def plot_bar(data: dict[str, int], title: str, xlabel: str, output: Path, top_n: int = 14) -> None:
    items = list(data.items())[:top_n]
    labels = [k for k, _ in items][::-1]
    values = [v for _, v in items][::-1]
    plt.figure(figsize=(12, max(5, 0.38 * len(labels))))
    bars = plt.barh(labels, values, color="#3B82F6")
    plt.title(title, fontsize=15, weight="bold")
    plt.xlabel(xlabel)
    plt.grid(axis="x", linestyle="--", alpha=0.25)
    for bar, value in zip(bars, values):
        plt.text(value + max(values) * 0.01, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(output, dpi=180, bbox_inches="tight")
    plt.close()


def build_taxonomy_json(stats: dict) -> None:
    taxonomy = {
        "schema_version": "2026.1",
        "note": "Automated navigation taxonomy generated from CVF titles and abstracts. Labels are intended for discovery, not as authoritative paper classifications.",
        "primary_areas": AREA_DESCRIPTIONS,
        "novelty_angles": NOVELTY_DESCRIPTIONS,
        "improvement_axes": list(stats["improvement_axes"].keys()),
        "fields": {
            "primary_area": "Dominant research area inferred from title and abstract.",
            "secondary_area": "Second strongest area signal, useful for interdisciplinary papers.",
            "novelty_angle": "The main type of methodological novelty inferred from evidence terms.",
            "improvement_axis": "The primary kind of improvement the abstract appears to target.",
            "application_context": "A coarse practical setting when a clear one is present.",
            "approach_summary": "A short evidence sentence, usually from the abstract, describing the proposed method.",
            "improvement_rationale": "A compact explanation of why the paper is likely to improve the target axis, anchored to abstract evidence.",
            "taxonomy_confidence": "Heuristic confidence score from 0 to 1 based on label evidence and score margin.",
        },
    }
    TAXONOMY_JSON.write_text(json.dumps(taxonomy, indent=2, ensure_ascii=False), encoding="utf-8")


def write_taxonomy_doc(stats: dict) -> None:
    area_rows = "\n".join(
        f"| {md_escape(area)} | {count:,} | {pct(count, stats['paper_count'])} | {md_escape(AREA_DESCRIPTIONS.get(area, ''))} |"
        for area, count in stats["areas"].items()
    )
    novelty_rows = "\n".join(
        f"| {md_escape(angle)} | {count:,} | {pct(count, stats['paper_count'])} | {md_escape(NOVELTY_DESCRIPTIONS.get(angle, ''))} |"
        for angle, count in stats["novelty_angles"].items()
    )
    axis_rows = "\n".join(
        f"| {md_escape(axis)} | {count:,} | {pct(count, stats['paper_count'])} |"
        for axis, count in stats["improvement_axes"].items()
    )
    text = f"""# CVPR 2026 Research Taxonomy

**Author:** Manus AI  
**Repository:** `awesome-cvpr-2026-papers`

This document defines the navigation taxonomy used to organize CVPR 2026 papers by **research area**, **novelty angle**, and **improvement rationale**. It is designed for discovery rather than formal bibliometric analysis. The labels are generated from paper titles and CVF abstracts, then exposed in `data/cvpr2026_papers_categorized.csv`, `data/cvpr2026_papers_categorized.json`, and [`papers-by-category.md`](papers-by-category.md).

The taxonomy is motivated by public CVPR 2026 trend pages and official program pages. The reviewed sources emphasize that the conference is no longer only a collection of classical recognition, detection, and segmentation papers; it now strongly reflects **generative modeling**, **3D and neural rendering**, **vision-language systems**, **video/world modeling**, **embodied AI**, and **trustworthy multimodal intelligence**.[1] [2] [3] [4]

> **Interpretation note.** A paper may legitimately belong to multiple areas. The `primary_area` field is the strongest automated signal, while `secondary_area` preserves the most likely cross-cutting angle.

## Primary Research Areas

| Primary area | Papers | Share | Interpretation |
|---|---:|---:|---|
{area_rows}

## Novelty Angles

The **novelty angle** captures the main mechanism by which the paper appears to move the field forward. This is intentionally different from the application area; for example, a 3D reconstruction paper may contribute through a new representation, a diffusion-based training objective, an evaluation benchmark, or a speed-oriented system design.

| Novelty angle | Papers | Share | Interpretation |
|---|---:|---:|---|
{novelty_rows}

## Improvement Axes

The **improvement axis** describes the type of gain implied by the paper’s title and abstract. It is a compact answer to the question: “What kind of improvement is this work trying to deliver?”

| Improvement axis | Papers | Share |
|---|---:|---:|
{axis_rows}

## Categorization Method

The categorization pipeline is implemented in [`scripts/categorize_papers.py`](scripts/categorize_papers.py). It reads the abstract-enriched CSV, scores each paper against weighted keyword dictionaries, and writes structured labels and evidence fields. The `improvement_rationale` is intentionally anchored to a sentence from the abstract when available, so that readers can audit why a label was assigned.

| Field | Meaning |
|---|---|
| `primary_area` | Dominant research area inferred from the paper title and abstract. |
| `secondary_area` | Second strongest area signal, useful for interdisciplinary work. |
| `novelty_angle` | Main methodological or conceptual angle, such as representation, architecture, data, geometry, safety, or efficiency. |
| `improvement_axis` | The kind of improvement the work appears to target, such as quality, speed, scalability, robustness, editability, or physical consistency. |
| `approach_summary` | A short abstract-derived sentence describing the method or proposed contribution. |
| `improvement_rationale` | A compact, evidence-linked explanation of why the approach is likely to improve the target axis. |
| `taxonomy_confidence` | A heuristic confidence score based on keyword evidence and score margin. |

## Limitations

This taxonomy is **not a substitute for reading the paper**. It is a pragmatic browsing layer for a very large conference. Some papers will be interdisciplinary, and some labels will be imperfect when abstracts use broad language or when a paper’s true contribution is only clear after reading the full PDF. The repository therefore keeps the official CVF, arXiv, poster, and project links next to every categorized entry.

## References

[1]: https://www.bohrium.com/en/blog/research-notes/cvpr-2026-accepted-papers-highlights/ "Bohrium — CVPR 2026 Accepted Papers: Trends, Big Tech Bets & Top Highlights"
[2]: https://www.paperdigest.org/2026/04/cvpr-2026-papers-highlights/ "Paper Digest — CVPR 2026 Papers & Highlights"
[3]: https://cvpr.thecvf.com/virtual/2026/events/Highlights2026 "CVPR 2026 Virtual Program — Highlighted Papers"
[4]: https://cvpr.thecvf.com/virtual/2026/events/AwardCandidates2026 "CVPR 2026 Virtual Program — Award Candidates"
"""
    TAXONOMY_DOC.write_text(text, encoding="utf-8")


def write_research_map(rows: list[dict], stats: dict) -> None:
    total = stats["paper_count"]
    top_two = stats["areas"].get("Generative Models, Editing & Creative Vision", 0) + stats["areas"].get("3D Vision, Geometry & Neural Rendering", 0)
    area_table = "\n".join(
        f"| {md_escape(area)} | {count:,} | {pct(count, total)} | {stats['code_by_area'][area]['with_code_or_resource']:,} | {stats['code_by_area'][area]['with_github']:,} |"
        for area, count in stats["areas"].items()
    )
    novelty_table = "\n".join(
        f"| {md_escape(angle)} | {count:,} | {pct(count, total)} |"
        for angle, count in stats["novelty_angles"].items()
    )
    axis_table = "\n".join(
        f"| {md_escape(axis)} | {count:,} | {pct(count, total)} |"
        for axis, count in stats["improvement_axes"].items()
    )

    by_area = defaultdict(list)
    for r in rows:
        by_area[r["primary_area"]].append(r)

    sections = []
    for area, count in stats["areas"].items():
        selected = sorted(
            by_area[area],
            key=lambda r: (
                0 if r.get("github") else 1,
                0 if str(r.get("code_resource_found", "")).lower() in {"true", "yes", "1"} else 1,
                r.get("title", ""),
            ),
        )[:10]
        rows_md = []
        for r in selected:
            title = link(md_escape(r["title"]), r.get("cvf_html", "")) or md_escape(r["title"])
            arxiv = link("arXiv", first_link(r.get("arxiv", "")))
            github = link("GitHub", first_link(r.get("github", "")))
            website = link("Website", first_link(r.get("website", "")))
            rationale = md_escape(r.get("improvement_rationale", ""))[:360]
            rows_md.append(f"| {title} | {code_flag(r)} | {github} | {arxiv} | {md_escape(r.get('novelty_angle',''))} | {md_escape(r.get('improvement_axis',''))} | {rationale} |")
        table = "\n".join(rows_md) if rows_md else "| _No entries_ |  |  |  |  |  |  |"
        sections.append(
            f"""### {area}

{AREA_DESCRIPTIONS.get(area, '')} In this automated map, the area contains **{count:,} papers** and **{stats['code_by_area'][area]['with_code_or_resource']:,} discovered code/resource entries**.

| Example paper | Code/resource | GitHub | arXiv | Novelty angle | Improvement axis | Improvement rationale |
|---|---|---|---|---|---|---|
{table}
"""
        )

    text = f"""# CVPR 2026 Research Map

**A high-level map of CVPR 2026 by research area, novelty angle, and improvement mechanism.**

This page adds a strategic browsing layer on top of the full paper index. It is meant to help readers quickly answer questions such as: **Which areas dominate the conference? Which methodological patterns recur? Which papers are likely improving quality, speed, robustness, controllability, or 3D consistency?** The labels are generated from CVF titles and abstracts and should be treated as a discovery aid rather than a definitive classification.

The current categorized dataset contains **{total:,} CVF Open Access papers** with abstracts. The two largest automated areas, **Generative Models, Editing & Creative Vision** and **3D Vision, Geometry & Neural Rendering**, account for **{top_two:,} papers** or **{pct(top_two, total)}** of the parsed index. This aligns with public CVPR 2026 trend commentary that highlights the rise of multimodal, generative, video, and embodied directions alongside continued depth in 3D and geometry.[1] [2]

![CVPR 2026 papers by primary research area](assets/cvpr2026_area_distribution.png)

## Area Distribution and Code Availability

| Primary area | Papers | Share | With code/resource | Direct GitHub |
|---|---:|---:|---:|---:|
{area_table}

![CVPR 2026 novelty angles](assets/cvpr2026_novelty_angles.png)

## Novelty Angles

| Novelty angle | Papers | Share |
|---|---:|---:|
{novelty_table}

## Improvement Axes

| Improvement axis | Papers | Share |
|---|---:|---:|
{axis_table}

## How to Use This Map

Readers doing a literature review should start with the **primary area** and then filter by **novelty angle**. Engineers looking for reproducible work should filter `code_resource_found == Yes` and then inspect `github`, `website`, and `model_demo`. Founders or applied teams should pay special attention to `improvement_axis`, because it separates papers targeting quality from those targeting speed, controllability, scalability, safety, or deployability.

| Goal | Recommended filter |
|---|---|
| Find fast or deployable methods | `novelty_angle = Efficiency / Acceleration / Compression` or `improvement_axis = Efficiency / Speed`. |
| Find new foundation-model training ideas | `primary_area = Learning, Optimization & Efficient Foundation Models` plus `novelty_angle = Training / Pretraining Objective`. |
| Find project-ready methods | `code_resource_found = Yes`, then sort by `primary_area` and inspect `github` or `website`. |
| Find papers with a clear evaluation contribution | `primary_area = Datasets, Benchmarks & Evaluation` or `novelty_angle = Evaluation, Benchmark or Metric`. |
| Find likely high-growth research themes | Review generative, 3D, multimodal, video, embodied, and safety categories together. |

## Representative Papers by Area

The tables below intentionally show a small, code-prioritized slice of each area. The complete grouped index is available in [`papers-by-category.md`](papers-by-category.md), and the machine-readable version is available in [`data/cvpr2026_papers_categorized.csv`](data/cvpr2026_papers_categorized.csv).

{''.join(sections)}

## References

[1]: https://www.bohrium.com/en/blog/research-notes/cvpr-2026-accepted-papers-highlights/ "Bohrium — CVPR 2026 Accepted Papers: Trends, Big Tech Bets & Top Highlights"
[2]: https://www.paperdigest.org/2026/04/cvpr-2026-papers-highlights/ "Paper Digest — CVPR 2026 Papers & Highlights"
"""
    RESEARCH_MAP.write_text(text, encoding="utf-8")


def write_papers_by_category(rows: list[dict], stats: dict) -> None:
    by_area = defaultdict(list)
    for r in rows:
        by_area[r["primary_area"]].append(r)
    parts = [
        "# CVPR 2026 Papers by Category\n\n",
        "This file groups every parsed CVPR 2026 paper by the repository’s automated research taxonomy. Each row keeps the original paper links together with the inferred **novelty angle**, **improvement axis**, and a short evidence-linked rationale. The labels are generated from title and abstract text and should be used for navigation rather than formal classification.\n\n",
        "| Field | Meaning |\n|---|---|\n| Code | Whether a public code, project, data, demo, model, or resource link was discovered. |\n| Novelty | Main methodological or conceptual angle. |\n| Improvement | Main improvement axis inferred from the abstract. |\n| Rationale | Compact explanation anchored to abstract evidence. |\n\n",
    ]
    for area, count in stats["areas"].items():
        parts.append(f"## {area}\n\n")
        parts.append(f"{AREA_DESCRIPTIONS.get(area, '')} This section contains **{count:,} papers**.\n\n")
        parts.append("| Paper | Code | GitHub | Website | arXiv | Novelty | Improvement | Rationale |\n")
        parts.append("|---|---|---|---|---|---|---|---|\n")
        for r in sorted(by_area[area], key=lambda x: x.get("title", "")):
            title = link(md_escape(r["title"]), r.get("cvf_html", "")) or md_escape(r["title"])
            github = link("GitHub", first_link(r.get("github", "")))
            website = link("Website", first_link(r.get("website", "")))
            arxiv = link("arXiv", first_link(r.get("arxiv", "")))
            rationale = md_escape(r.get("improvement_rationale", ""))[:420]
            parts.append(
                f"| {title} | {code_flag(r)} | {github} | {website} | {arxiv} | {md_escape(r.get('novelty_angle',''))} | {md_escape(r.get('improvement_axis',''))} | {rationale} |\n"
            )
        parts.append("\n")
    PAPERS_BY_CATEGORY.write_text("".join(parts), encoding="utf-8")


def main() -> None:
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    plot_bar(stats["areas"], "CVPR 2026 Papers by Primary Research Area", "Number of papers", ASSETS / "cvpr2026_area_distribution.png")
    plot_bar(stats["novelty_angles"], "CVPR 2026 Papers by Novelty Angle", "Number of papers", ASSETS / "cvpr2026_novelty_angles.png")
    build_taxonomy_json(stats)
    write_taxonomy_doc(stats)
    write_research_map(rows, stats)
    write_papers_by_category(rows, stats)
    print(json.dumps({
        "research_map": str(RESEARCH_MAP),
        "papers_by_category": str(PAPERS_BY_CATEGORY),
        "taxonomy_doc": str(TAXONOMY_DOC),
        "taxonomy_json": str(TAXONOMY_JSON),
    }, indent=2))


if __name__ == "__main__":
    main()
