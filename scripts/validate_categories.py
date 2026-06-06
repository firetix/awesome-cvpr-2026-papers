from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CSV_PATH = DATA / "cvpr2026_papers_categorized.csv"
REPORT_PATH = DATA / "category_validation_report.json"


def main() -> None:
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    report = {
        "paper_count": len(rows),
        "abstracts_present": sum(1 for r in rows if r.get("abstract")),
        "primary_area_count": len(set(r.get("primary_area", "") for r in rows)),
        "empty_primary_area": sum(1 for r in rows if not r.get("primary_area")),
        "empty_novelty_angle": sum(1 for r in rows if not r.get("novelty_angle")),
        "empty_improvement_rationale": sum(1 for r in rows if not r.get("improvement_rationale")),
        "top_primary_areas": Counter(r.get("primary_area", "") for r in rows).most_common(15),
        "top_novelty_angles": Counter(r.get("novelty_angle", "") for r in rows).most_common(15),
        "sample_records": [
            {
                "title": r.get("title"),
                "primary_area": r.get("primary_area"),
                "secondary_area": r.get("secondary_area"),
                "novelty_angle": r.get("novelty_angle"),
                "improvement_axis": r.get("improvement_axis"),
                "improvement_rationale": r.get("improvement_rationale"),
                "github": r.get("github"),
            }
            for r in rows[:12]
        ],
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
