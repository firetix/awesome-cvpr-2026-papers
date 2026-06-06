from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / ".cache" / "cvf_pages"
CACHE.mkdir(parents=True, exist_ok=True)

INPUT_CSV = DATA / "cvpr2026_papers.csv"
OUTPUT_CSV = DATA / "cvpr2026_papers_with_abstracts.csv"
OUTPUT_JSON = DATA / "cvpr2026_papers_with_abstracts.json"

HEADERS = {"User-Agent": "awesome-cvpr-2026-papers/1.0 (+research index)"}


def cache_path(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return CACHE / f"{digest}.html"


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip()


def extract_abstract(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find(id="abstract") or soup.find("div", class_=re.compile("abstract", re.I))
    if div:
        return clean_text(div.get_text(" ", strip=True))
    # CVF pages usually place the abstract after an H2/H3 heading.
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        if clean_text(heading.get_text()).lower() == "abstract":
            texts = []
            node = heading.find_next_sibling()
            while node is not None and getattr(node, "name", None) not in {"h1", "h2", "h3", "h4"}:
                if getattr(node, "get_text", None):
                    texts.append(node.get_text(" ", strip=True))
                node = node.find_next_sibling()
            candidate = clean_text(" ".join(texts))
            if candidate:
                return candidate
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        return clean_text(meta["content"])
    return ""


def fetch_one(row: dict) -> dict:
    url = row.get("cvf_html", "")
    row = dict(row)
    row.setdefault("abstract", "")
    if not url or not urlparse(url).scheme:
        return row
    path = cache_path(url)
    html = ""
    if path.exists():
        html = path.read_text(encoding="utf-8", errors="ignore")
    else:
        last_error = ""
        for attempt in range(3):
            try:
                response = requests.get(url, headers=HEADERS, timeout=25)
                response.raise_for_status()
                html = response.text
                path.write_text(html, encoding="utf-8")
                break
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                time.sleep(0.5 * (attempt + 1))
        if not html:
            row["abstract_fetch_error"] = last_error
            return row
    row["abstract"] = extract_abstract(html)
    return row


def main() -> None:
    with INPUT_CSV.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    enriched = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(fetch_one, row): row for row in rows}
        for i, fut in enumerate(as_completed(futures), start=1):
            enriched.append(fut.result())
            if i % 250 == 0:
                print(f"processed {i}/{len(rows)}", flush=True)
    enriched.sort(key=lambda r: int(r.get("index", 0) or 0))
    fieldnames = list(rows[0].keys()) + ["abstract", "abstract_fetch_error"]
    seen = []
    for name in fieldnames:
        if name not in seen:
            seen.append(name)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=seen, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)
    OUTPUT_JSON.write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding="utf-8")
    abstract_count = sum(1 for r in enriched if r.get("abstract"))
    print(json.dumps({"papers": len(enriched), "abstracts": abstract_count}, indent=2))


if __name__ == "__main__":
    main()
