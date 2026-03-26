#!/usr/bin/env python3
"""Ingest OGIS (Office of Government Information Services) advisory opinions
and compliance assessments from archives.gov.

Sources:
- Advisory opinions: https://www.archives.gov/ogis/advisory-opinions
- Compliance assessments: https://www.archives.gov/ogis/resources/ogis-compliance-assessments

Run: python3 scripts/ingest/federal/ingest_ogis.py
"""

import os
import re
import sys
import time
import logging

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from ingest.utils import insert_document, log_ingestion, normalize_text
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'db', 'prdb.db')
OGIS_BASE = 'https://www.archives.gov'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0 (public records research database; +https://github.com)',
    'Accept': 'text/html',
}

RATE_LIMIT_DELAY = 2.0  # seconds between requests

SOURCES = [
    {
        'index_url': '/ogis/advisory-opinions',
        'document_type': 'Agency Guidance',
        'type_slug': 'advisory-opinion',
        'label': 'advisory opinion',
    },
    {
        'index_url': '/ogis/resources/ogis-compliance-assessments',
        'document_type': 'Compliance Assessment',
        'type_slug': 'compliance-assessment',
        'label': 'compliance assessment',
    },
]


def slug_from_url(url: str) -> str:
    """Derive a stable slug from a URL path."""
    path = url.split('?')[0].rstrip('/')
    # Take the last path segment
    slug = path.split('/')[-1]
    # Normalize to lowercase, replace non-alphanumeric runs with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower()).strip('-')
    return slug or 'unknown'


def is_pdf(url: str) -> bool:
    """Return True if the URL looks like a PDF link."""
    return url.lower().split('?')[0].endswith('.pdf')


def fetch_index_links(index_path: str) -> list[str]:
    """Fetch the index page and return all in-site links that look like
    individual opinion/assessment pages (not PDFs, not the index itself)."""
    url = OGIS_BASE + index_path
    logger.info(f'Fetching index: {url}')

    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    links = []
    seen = set()
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()

        # Resolve relative URLs
        if href.startswith('/'):
            full = OGIS_BASE + href
        elif href.startswith('http'):
            full = href
        else:
            continue

        # Only keep pages under archives.gov/ogis
        if 'archives.gov/ogis' not in full:
            continue

        # Skip PDFs
        if is_pdf(full):
            logger.debug(f'Skipping PDF: {full}')
            continue

        # Skip the index page itself and generic resource/landing pages
        if full.rstrip('/') in (OGIS_BASE + index_path).rstrip('/'):
            continue

        # Skip anchor-only links and fragment variants
        clean = full.split('#')[0].rstrip('/')
        if clean in seen:
            continue
        seen.add(clean)
        links.append(clean)

    logger.info(f'Found {len(links)} candidate links on {index_path}')
    return links


def fetch_page_text(url: str) -> str | None:
    """Fetch a page and extract its main text content."""
    logger.info(f'Fetching page: {url}')

    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Try common content containers on archives.gov
    content = (
        soup.find('div', id='main-col')
        or soup.find('div', class_='main-content')
        or soup.find('main')
        or soup.find('article')
        or soup.find('div', id='content')
        or soup.find('div', class_='field-name-body')
    )

    if not content:
        logger.warning(f'Could not find content container for {url}')
        return None

    # Strip nav, scripts, styles, and sidebar noise
    for tag in content.find_all(['nav', 'script', 'style', 'header', 'footer']):
        tag.decompose()

    text = content.get_text(separator='\n')
    text = normalize_text(text)

    if len(text) < 100:
        logger.warning(f'Suspiciously short text ({len(text)} chars) for {url}')
        return None

    return text


def extract_title(url: str, soup: BeautifulSoup) -> str:
    """Pull a title from the page, falling back to the URL slug."""
    # Try h1 inside main content first, then page <title>
    for selector in (['h1'], ['title']):
        tag = soup.find(*selector)
        if tag:
            return tag.get_text(separator=' ').strip()
    return slug_from_url(url).replace('-', ' ').title()


def ingest_source(source: dict) -> tuple[int, int, int]:
    """Ingest all documents from one source. Returns (added, skipped, errors)."""
    added = skipped = errors = 0

    try:
        links = fetch_index_links(source['index_url'])
    except requests.RequestException as e:
        logger.error(f'Failed to fetch index {source["index_url"]}: {e}')
        return 0, 0, 1

    time.sleep(RATE_LIMIT_DELAY)

    for url in links:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            content = (
                soup.find('div', id='main-col')
                or soup.find('div', class_='main-content')
                or soup.find('main')
                or soup.find('article')
                or soup.find('div', id='content')
                or soup.find('div', class_='field-name-body')
            )

            if not content:
                logger.warning(f'No content container found: {url}')
                errors += 1
                time.sleep(RATE_LIMIT_DELAY)
                continue

            for tag in content.find_all(['nav', 'script', 'style', 'header', 'footer']):
                tag.decompose()

            raw_text = content.get_text(separator='\n')
            text = normalize_text(raw_text)

            if len(text) < 100:
                logger.warning(f'Too short ({len(text)} chars), skipping: {url}')
                skipped += 1
                time.sleep(RATE_LIMIT_DELAY)
                continue

            title = extract_title(url, soup)
            slug = slug_from_url(url)
            doc_id = f'ogis-{source["type_slug"]}-{slug}'

            doc = {
                'id': doc_id,
                'title': title,
                'document_type': source['document_type'],
                'jurisdiction': 'federal',
                'source': 'ogis',
                'source_url': url,
                'text': text,
            }

            if insert_document(DB_PATH, doc):
                added += 1
                logger.info(f'Inserted {doc_id}')
            else:
                skipped += 1
                logger.info(f'Skipped {doc_id} (already exists)')

        except requests.RequestException as e:
            logger.error(f'HTTP error for {url}: {e}')
            errors += 1
        except Exception as e:
            logger.error(f'Error processing {url}: {e}')
            errors += 1

        time.sleep(RATE_LIMIT_DELAY)

    return added, skipped, errors


def main():
    start = time.time()
    total_added = total_skipped = total_errors = 0

    for source in SOURCES:
        logger.info(f'--- Ingesting OGIS {source["label"]}s ---')
        added, skipped, errors = ingest_source(source)
        total_added += added
        total_skipped += skipped
        total_errors += errors
        logger.info(f'{source["label"]}: {added} added, {skipped} skipped, {errors} errors')

    elapsed = time.time() - start
    log_ingestion(
        DB_PATH,
        source='ogis',
        added=total_added,
        skipped=total_skipped,
        errors=total_errors,
        notes='OGIS advisory opinions and compliance assessments from archives.gov',
    )

    print(f'OGIS: {total_added} added, {total_skipped} skipped, {total_errors} errors')
    write_receipt(
        script='ingest_ogis',
        added=total_added,
        skipped=total_skipped,
        errors=total_errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
