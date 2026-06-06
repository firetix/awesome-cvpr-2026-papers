#!/usr/bin/env python3
"""Build compact static data for the GitHub Pages explorer.

The public repository keeps richer CSV/JSON datasets under data/. GitHub Pages should load a
smaller browser-oriented JSON file with only the fields required for interactive filtering.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "cvpr2026_papers_categorized.csv"
OUTPUT_DIR = ROOT / "docs" / "data"
OUTPUT = OUTPUT_DIR / "papers.min.json"

FIELDS = [
    "title",
    "authors",
    "primary_area",
    "secondary_area",
    "novelty_angle",
    "improvement_axis",
    "improvement_rationale",
]


def clean(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\n", " ").split())


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"true", "1", "yes", "y"}


def first_present(row: dict[str, str], names: list[str]) -> str:
    for name in names:
        value = clean(row.get(name, ""))
        if value:
            return value
    return ""


def yes_no(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"yes", "true", "1", "y"}


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f"Missing categorized dataset: {INPUT}")

    rows: list[dict[str, object]] = []
    with INPUT.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            item = {field: clean(row.get(field, "")) for field in FIELDS}
            item["id"] = idx
            item["has_code"] = yes_no(row.get("code_resource_found", "")) or bool(clean(row.get("github", "")))
            item["source_url"] = first_present(row, ["cvf_html", "cvf_pdf", "poster_url"])
            item["paper_url"] = first_present(row, ["cvf_pdf", "cvf_html"])
            item["cvf_url"] = first_present(row, ["cvf_html", "cvf_pdf"])
            item["poster_url"] = clean(row.get("poster_url", ""))
            item["github_url"] = clean(row.get("github", ""))
            item["project_url"] = clean(row.get("website", ""))
            item["demo_url"] = clean(row.get("model_demo", ""))
            item["code_url"] = first_present(row, ["github", "website", "model_demo"])
            item["arxiv_url"] = clean(row.get("arxiv", ""))
            rows.append(item)

    area_counts = Counter(str(r.get("primary_area", "Uncategorized")) or "Uncategorized" for r in rows)
    novelty_counts = Counter(str(r.get("novelty_angle", "Uncategorized")) or "Uncategorized" for r in rows)
    code_count = sum(1 for r in rows if r.get("has_code"))

    payload = {
        "generated_from": "data/cvpr2026_papers_categorized.csv",
        "paper_count": len(rows),
        "code_count": code_count,
        "github_count": sum(1 for r in rows if r.get("github_url")),
        "arxiv_count": sum(1 for r in rows if r.get("arxiv_url")),
        "areas": dict(area_counts.most_common()),
        "novelty_angles": dict(novelty_counts.most_common()),
        "papers": rows,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(rows):,} papers ({OUTPUT.stat().st_size / 1024 / 1024:.2f} MiB).")


if __name__ == "__main__":
    main()
