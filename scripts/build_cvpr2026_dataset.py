from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '.cache' / 'sources'
OUT = ROOT
DATA = OUT / 'data'
DATA.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

BASE_CVF = 'https://openaccess.thecvf.com'
BASE_CVPR = 'https://cvpr.thecvf.com'

SOURCE_URLS = {
    'cvf_openaccess_all.html': 'https://openaccess.thecvf.com/CVPR2026?day=all',
    'virtual_papers.html': 'https://cvpr.thecvf.com/virtual/2026/papers.html',
    'paperdigest_code.html': 'https://www.paperdigest.org/2026/06/cvpr-2026-papers-with-code-data/',
    'amusi_readme.md': 'https://raw.githubusercontent.com/amusi/CVPR2026-Papers-with-Code/main/README.md',
    'skalski_readme.md': 'https://raw.githubusercontent.com/SkalskiP/top-cvpr-2026-papers/master/README.md',
}

def download_sources(force: bool = False):
    for filename, url in SOURCE_URLS.items():
        target = SRC / filename
        if target.exists() and not force:
            continue
        request = Request(url, headers={'User-Agent': 'awesome-cvpr-2026-papers/1.0'})
        with urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())



def norm_title(title: str) -> str:
    title = unicodedata.normalize('NFKD', title or '')
    title = title.encode('ascii', 'ignore').decode('ascii')
    title = title.lower().replace('&', 'and')
    title = re.sub(r'[^a-z0-9]+', ' ', title)
    return re.sub(r'\s+', ' ', title).strip()


def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').replace('\xa0', ' ')).strip()


def md_escape(text: str) -> str:
    text = clean_text(text)
    return text.replace('|', '\\|').replace('\n', ' ')


def md_link(label: str, url: str) -> str:
    if not url:
        return '—'
    return f'[{label}]({url})'


def split_urls(urls):
    return '; '.join(dict.fromkeys([u for u in urls if u]))


def classify_links(urls):
    github, websites, models, videos, other = [], [], [], [], []
    for url in urls:
        if not url:
            continue
        low = url.lower()
        if 'github.com' in low:
            github.append(url)
        elif any(x in low for x in ['huggingface.co', 'colab.research.google.com']):
            models.append(url)
        elif any(x in low for x in ['youtube.com', 'youtu.be']):
            videos.append(url)
        elif low.startswith('http'):
            websites.append(url)
        else:
            other.append(url)
    return {
        'github_links': split_urls(github),
        'website_links': split_urls(websites),
        'model_demo_links': split_urls(models),
        'video_links': split_urls(videos),
        'other_links': split_urls(other),
    }


def parse_cvf_openaccess():
    html = (SRC / 'cvf_openaccess_all.html').read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    papers = []
    for idx, dt in enumerate(soup.select('dt.ptitle'), start=1):
        title_a = dt.find('a')
        if not title_a:
            continue
        title = clean_text(title_a.get_text(' ', strip=True))
        html_url = urljoin(BASE_CVF, title_a.get('href', ''))
        dds = []
        sib = dt.find_next_sibling()
        while sib is not None and getattr(sib, 'name', None) != 'dt':
            if getattr(sib, 'name', None) == 'dd':
                dds.append(sib)
            sib = sib.find_next_sibling()
        author_dd = dds[0] if dds else None
        link_dd = dds[1] if len(dds) > 1 else (dds[0] if dds else None)
        authors = []
        if author_dd:
            for inp in author_dd.select('input[name="query_author"]'):
                value = clean_text(inp.get('value', ''))
                if value:
                    authors.append(value)
            if not authors:
                authors = [clean_text(a.get_text(' ', strip=True)) for a in author_dd.find_all('a') if clean_text(a.get_text(' ', strip=True))]
        pdf_url = supp_url = arxiv_url = ''
        if link_dd:
            for a in link_dd.find_all('a'):
                label = clean_text(a.get_text(' ', strip=True)).lower()
                href = a.get('href', '')
                if not href:
                    continue
                url = urljoin(BASE_CVF, href)
                if 'arxiv.org' in href.lower() or label == 'arxiv':
                    arxiv_url = url
                elif label == 'pdf' or href.endswith('_paper.pdf'):
                    pdf_url = url
                elif label == 'supp' or 'supplemental' in href:
                    supp_url = url
        bibtex = ''
        pages = ''
        if link_dd:
            bib = link_dd.select_one('.bibref')
            if bib:
                bibtex = bib.get_text('\n', strip=True)
                m = re.search(r'pages\s*=\s*\{([^}]+)\}', bibtex)
                if m:
                    pages = m.group(1).strip()
        papers.append({
            'index': idx,
            'title': title,
            'authors': '; '.join(authors),
            'cvf_html': html_url,
            'cvf_pdf': pdf_url,
            'supplement': supp_url,
            'arxiv': arxiv_url,
            'pages': pages,
            'bibtex_key': re.search(r'@InProceedings\{([^,]+),', bibtex).group(1) if re.search(r'@InProceedings\{([^,]+),', bibtex) else '',
            'source': 'CVF Open Access',
        })
    return papers


def parse_virtual_posters():
    html = (SRC / 'virtual_papers.html').read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    mapping = {}
    for a in soup.select('a[href*="/virtual/2026/poster/"]'):
        href = a.get('href', '')
        title = clean_text(a.get_text(' ', strip=True))
        m = re.search(r'/poster/(\d+)', href)
        if m and title:
            mapping[norm_title(title)] = {
                'poster_id': m.group(1),
                'poster_url': urljoin(BASE_CVPR, href),
            }
    return mapping


def parse_paperdigest_code():
    html = (SRC / 'paperdigest_code.html').read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    by_title = defaultdict(list)
    by_poster = defaultdict(list)
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 4:
            continue
        paper_td, code_td = tds[1], tds[3]
        title_a = paper_td.find('a', href=re.compile(r'paper/\?paper_id='))
        title = clean_text(title_a.get_text(' ', strip=True)) if title_a else ''
        if not title:
            strong = paper_td.find('strong')
            title = clean_text(strong.get_text(' ', strip=True)) if strong else ''
        poster_id = ''
        view = paper_td.find('a', href=re.compile(r'cvpr\.thecvf\.com/virtual/2026/poster/'))
        if view:
            m = re.search(r'/poster/(\d+)', view.get('href', ''))
            if m:
                poster_id = m.group(1)
        urls = []
        for a in code_td.find_all('a'):
            href = a.get('href', '')
            if href and href.startswith('http'):
                urls.append(href)
        if urls:
            item = {'title': title, 'poster_id': poster_id, 'urls': urls, 'source': 'Paper Digest code/data index'}
            if title:
                by_title[norm_title(title)].append(item)
            if poster_id:
                by_poster[poster_id].append(item)
    return by_title, by_poster


def parse_amusi_readme():
    text = (SRC / 'amusi_readme.md').read_text(encoding='utf-8', errors='ignore')
    entries = {}
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m_title = re.match(r'^\*\*(.+?)\*\*$', line)
        if m_title:
            current = clean_text(m_title.group(1).strip('* '))
            entries.setdefault(norm_title(current), {'title': current, 'paper': [], 'code': [], 'project': [], 'model': [], 'other': []})
            continue
        if current is None and not line.startswith('* '):
            if len(line) > 8 and not line.startswith('#') and not line.startswith('>') and not line.startswith('!'):
                current = clean_text(line.strip('* '))
                entries.setdefault(norm_title(current), {'title': current, 'paper': [], 'code': [], 'project': [], 'model': [], 'other': []})
                continue
        if current and line.startswith('* '):
            mm = re.match(r'^\*\s*([^:]+):\s*(.*)$', line)
            if not mm:
                continue
            key = mm.group(1).strip().lower()
            value = mm.group(2).strip()
            urls = re.findall(r'https?://[^\s)<>]+', value)
            urls = [u.rstrip('.,') for u in urls]
            if not urls and value.lower() in {'none', 'null'}:
                urls = []
            if 'paper' in key:
                entries[norm_title(current)]['paper'].extend(urls)
            elif 'code' in key:
                entries[norm_title(current)]['code'].extend(urls)
            elif 'project' in key:
                entries[norm_title(current)]['project'].extend(urls)
            elif 'model' in key or 'demo' in key:
                entries[norm_title(current)]['model'].extend(urls)
            else:
                entries[norm_title(current)]['other'].extend(urls)
    return entries


def parse_skalski_readme():
    text = (SRC / 'skalski_readme.md').read_text(encoding='utf-8', errors='ignore')
    entries = {}
    blocks = re.split(r'\n\s*\n', text)
    for block in blocks:
        if '[[paper]' not in block.replace(' ', '') and '[ [paper]' not in block:
            continue
        title = ''
        links = defaultdict(list)
        first_line = block.strip().splitlines()[0] if block.strip().splitlines() else ''
        bolds = re.findall(r'\*\*(.*?)\*\*', first_line)
        if bolds:
            title = clean_text(re.sub(r'^[🏆🔥📢\s]+', '', bolds[-1]))
        else:
            m = re.search(r'\[([^\]]+)\]\(https?://arxiv\.org/abs/[^)]+\)', first_line)
            if m:
                title = clean_text(m.group(1))
        for label, url in re.findall(r'\[\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*\]', block):
            links[label.lower()].append(url)
        if title:
            entries[norm_title(title)] = {'title': title, **links}
    return entries


def main():
    download_sources()
    papers = parse_cvf_openaccess()
    virtual = parse_virtual_posters()
    pd_by_title, pd_by_poster = parse_paperdigest_code()
    amusi = parse_amusi_readme()
    skalski = parse_skalski_readme()

    enriched = []
    for p in papers:
        key = norm_title(p['title'])
        poster = virtual.get(key, {})
        poster_id = poster.get('poster_id', '')
        poster_url = poster.get('poster_url', '')
        urls = []
        link_sources = []

        for item in pd_by_title.get(key, []) + pd_by_poster.get(poster_id, []):
            urls.extend(item['urls'])
            link_sources.append(item['source'])
        if key in amusi:
            ent = amusi[key]
            if not p.get('arxiv') and ent.get('paper'):
                p['arxiv'] = ent['paper'][0].replace('/pdf/', '/abs/').rstrip('.pdf')
            urls.extend(ent.get('code', []))
            urls.extend(ent.get('project', []))
            urls.extend(ent.get('model', []))
            urls.extend(ent.get('other', []))
            link_sources.append('amusi/CVPR2026-Papers-with-Code')
        if key in skalski:
            ent = skalski[key]
            if not p.get('arxiv') and ent.get('paper'):
                p['arxiv'] = ent['paper'][0]
            for lk in ['code', 'demo', 'video', 'colab']:
                urls.extend(ent.get(lk, []))
            link_sources.append('SkalskiP/top-cvpr-2026-papers')

        unique_urls = list(dict.fromkeys(urls))
        classified = classify_links(unique_urls)
        github_links = classified['github_links']
        website_links = classified['website_links']
        model_demo_links = classified['model_demo_links']
        video_links = classified['video_links']
        has_code_resource = bool(github_links or website_links or model_demo_links or classified['other_links'])
        row = {
            **p,
            'poster_id': poster_id,
            'poster_url': poster_url,
            'code_resource_found': 'Yes' if has_code_resource else 'No',
            'github': github_links,
            'website': website_links,
            'model_demo': model_demo_links,
            'video': video_links,
            'other_resource': classified['other_links'],
            'link_sources': '; '.join(dict.fromkeys(link_sources)),
        }
        enriched.append(row)

    csv_fields = ['index', 'title', 'authors', 'arxiv', 'cvf_html', 'cvf_pdf', 'poster_url', 'code_resource_found', 'github', 'website', 'model_demo', 'video', 'supplement', 'pages', 'bibtex_key', 'link_sources']
    with (DATA / 'cvpr2026_papers.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows([{k: r.get(k, '') for k in csv_fields} for r in enriched])

    with (DATA / 'cvpr2026_papers.json').open('w', encoding='utf-8') as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    code_yes = sum(1 for r in enriched if r['code_resource_found'] == 'Yes')
    github_yes = sum(1 for r in enriched if r['github'])
    arxiv_yes = sum(1 for r in enriched if r['arxiv'])
    poster_yes = sum(1 for r in enriched if r['poster_url'])
    stats = {
        'paper_count': len(enriched),
        'arxiv_count': arxiv_yes,
        'poster_count': poster_yes,
        'code_or_resource_count': code_yes,
        'github_repo_count': github_yes,
        'paperdigest_code_entries_matched_or_available': sum(len(v) for v in pd_by_title.values()),
        'generated_from': {
            'cvf_openaccess': 'https://openaccess.thecvf.com/CVPR2026?day=all',
            'cvpr_virtual': 'https://cvpr.thecvf.com/virtual/2026/papers.html',
            'paperdigest_code': 'https://www.paperdigest.org/2026/06/cvpr-2026-papers-with-code-data/',
            'amusi': 'https://github.com/amusi/CVPR2026-Papers-with-Code',
            'skalski': 'https://github.com/SkalskiP/top-cvpr-2026-papers',
        }
    }
    (DATA / 'stats.json').write_text(json.dumps(stats, indent=2), encoding='utf-8')

    # Full Markdown index.
    lines = []
    lines.append('# CVPR 2026 Paper Index')
    lines.append('')
    lines.append('This index is generated from the official CVF Open Access paper list and enriched with public code, project, demo, and website links from community code indexes. A `Yes` value in the `Code / Resource` column means that at least one public implementation, data resource, demo, or project resource was found by the enrichment script; the `GitHub` column is populated only when a direct GitHub repository link was found.')
    lines.append('')
    lines.append(f'Generated dataset size: **{len(enriched)} papers**. Direct arXiv links were found for **{arxiv_yes} papers**. Public code/resource links were found for **{code_yes} papers**, including **{github_yes} papers with direct GitHub links**.')
    lines.append('')
    lines.append('| # | Paper | Authors | arXiv | CVF | Poster | Code / Resource | GitHub | Project / Website |')
    lines.append('|---:|---|---|---|---|---|---|---|---|')
    for r in enriched:
        title = md_escape(r['title'])
        paper_cell = f'[{title}]({r["cvf_html"]})' if r.get('cvf_html') else title
        authors = md_escape(r['authors'])
        if len(authors) > 300:
            authors = authors[:297] + '...'
        github = '<br>'.join(md_link(f'GitHub {i+1}', u) for i, u in enumerate(r['github'].split('; ')) if u) if r['github'] else '—'
        websites = []
        if r['website']:
            websites.extend(r['website'].split('; '))
        if r['model_demo']:
            websites.extend(r['model_demo'].split('; '))
        website = '<br>'.join(md_link(f'Link {i+1}', u) for i, u in enumerate(websites) if u) if websites else '—'
        lines.append('| {idx} | {paper} | {authors} | {arxiv} | {cvf} | {poster} | {code} | {github} | {website} |'.format(
            idx=r['index'],
            paper=paper_cell,
            authors=authors,
            arxiv=md_link('arXiv', r['arxiv']),
            cvf=md_link('PDF', r['cvf_pdf']),
            poster=md_link('Poster', r['poster_url']),
            code=r['code_resource_found'],
            github=github,
            website=website,
        ))
    (OUT / 'papers.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    # Markdown subset with code/resources for README inclusion.
    code_rows = [r for r in enriched if r['code_resource_found'] == 'Yes']
    code_lines = []
    code_lines.append('# CVPR 2026 Papers with Public Code or Resources')
    code_lines.append('')
    code_lines.append('This file lists CVPR 2026 papers for which a public code, data, demo, model, or project resource was found during enrichment.')
    code_lines.append('')
    code_lines.append('| # | Paper | arXiv | GitHub | Project / Website | Source |')
    code_lines.append('|---:|---|---|---|---|---|')
    for r in code_rows:
        title = md_escape(r['title'])
        paper_cell = f'[{title}]({r["cvf_html"]})' if r.get('cvf_html') else title
        github = '<br>'.join(md_link(f'GitHub {i+1}', u) for i, u in enumerate(r['github'].split('; ')) if u) if r['github'] else '—'
        websites = []
        if r['website']:
            websites.extend(r['website'].split('; '))
        if r['model_demo']:
            websites.extend(r['model_demo'].split('; '))
        website = '<br>'.join(md_link(f'Link {i+1}', u) for i, u in enumerate(websites) if u) if websites else '—'
        code_lines.append(f'| {r["index"]} | {paper_cell} | {md_link("arXiv", r["arxiv"])} | {github} | {website} | {md_escape(r["link_sources"])} |')
    (OUT / 'papers-with-code.md').write_text('\n'.join(code_lines) + '\n', encoding='utf-8')

    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
