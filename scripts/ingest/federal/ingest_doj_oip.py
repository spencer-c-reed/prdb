#!/usr/bin/env python3
"""Ingest DOJ Office of Information Policy (OIP) FOIA guidance documents.

Scrapes the OIP guidance listing at https://www.justice.gov/oip/oip-guidance
and ingests linked HTML guidance pages.

Run: python3 scripts/ingest/federal/ingest_doj_oip.py
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

DOJ_BASE = 'https://www.justice.gov'
OIP_GUIDANCE_URL = 'https://www.justice.gov/oip/oip-guidance'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0 (public records research database; +https://github.com)',
    'Accept': 'text/html',
}

RATE_LIMIT_DELAY = 2.0  # seconds between requests


def url_to_slug(url: str) -> str:
    """Derive a stable slug from a URL path."""
    path = url.split('justice.gov', 1)[-1] if 'justice.gov' in url else url
    # Strip query strings and fragments
    path = path.split('?')[0].split('#')[0]
    # Normalize slashes and replace non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-')
    return slug or 'unknown'


def is_html_link(url: str) -> bool:
    """Return True if the URL looks like an HTML page we can scrape."""
    lower = url.lower()
    # Skip PDFs, Word docs, and other binary formats
    if re.search(r'\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|mp3|mp4)(\?|$)', lower):
        return False
    return True


def fetch_guidance_links(listing_url: str) -> list[dict]:
    """Fetch the OIP guidance listing page and return links to individual guidance docs."""
    logger.info(f'Fetching guidance listing: {listing_url}')
    resp = requests.get(listing_url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # The main content area on justice.gov pages
    content = (
        soup.find('div', class_='field-name-body')
        or soup.find('div', class_='views-element-container')
        or soup.find('main')
        or soup.find('div', id='content')
    )
    if not content:
        content = soup

    links = []
    seen = set()

    for a in content.find_all('a', href=True):
        href = a['href'].strip()

        # Resolve relative URLs
        if href.startswith('/'):
            href = DOJ_BASE + href
        elif not href.startswith('http'):
            continue

        # Only follow justice.gov links
        if 'justice.gov' not in href:
            continue

        # Skip the listing page itself and anchor-only links
        if href.rstrip('/') == listing_url.rstrip('/') or href.startswith('#'):
            continue

        # Skip non-HTML resources
        if not is_html_link(href):
            logger.debug(f'Skipping non-HTML link: {href}')
            continue

        if href in seen:
            continue
        seen.add(href)

        title = a.get_text(separator=' ').strip()
        if not title:
            continue

        links.append({'url': href, 'title': title})

    logger.info(f'Found {len(links)} candidate guidance links')
    return links


def fetch_page_text(url: str) -> tuple[str | None, str | None]:
    """Fetch a guidance page and return (title, text). Returns (None, None) on failure."""
    logger.info(f'Fetching guidance page: {url}')
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f'HTTP error fetching {url}: {e}')
        return None, None

    # If we got redirected to a PDF, skip it
    final_url = resp.url
    if not is_html_link(final_url):
        logger.info(f'Skipping after redirect to non-HTML: {final_url}')
        return None, None

    content_type = resp.headers.get('Content-Type', '')
    if 'html' not in content_type:
        logger.info(f'Skipping non-HTML content-type ({content_type}) at {url}')
        return None, None

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Extract page title
    h1 = soup.find('h1')
    page_title = h1.get_text(separator=' ').strip() if h1 else None
    if not page_title:
        title_tag = soup.find('title')
        page_title = title_tag.get_text().strip() if title_tag else None

    # Find the main content area
    content = (
        soup.find('div', class_='field-name-body')
        or soup.find('article')
        or soup.find('main')
        or soup.find('div', id='content')
    )
    if not content:
        logger.warning(f'Could not find content container for {url}')
        return page_title, None

    # Remove navigation and non-content elements
    for tag in content.find_all(['nav', 'script', 'style', 'footer', 'header']):
        tag.decompose()

    text = content.get_text(separator='\n')
    text = normalize_text(text)

    if len(text) < 100:
        logger.warning(f'Suspiciously short text ({len(text)} chars) for {url}')
        return page_title, None

    return page_title, text


def main():
    start = time.time()
    added = 0
    skipped = 0
    errors = 0

    # Step 1: get the listing page links
    try:
        links = fetch_guidance_links(OIP_GUIDANCE_URL)
    except requests.RequestException as e:
        logger.error(f'Failed to fetch guidance listing: {e}')
        write_receipt(script='ingest_doj_oip', status='error', added=0, skipped=0, errors=1,
                      elapsed_s=time.time() - start)
        sys.exit(1)

    time.sleep(RATE_LIMIT_DELAY)

    # Step 2: ingest each linked page
    for link in links:
        url = link['url']
        link_title = link['title']

        try:
            page_title, text = fetch_page_text(url)

            if text is None:
                logger.info(f'No usable text for {url}, skipping')
                skipped += 1
                time.sleep(RATE_LIMIT_DELAY)
                continue

            title = page_title or link_title
            slug = url_to_slug(url)
            doc_id = f'doj-oip-{slug}'

            doc = {
                'id': doc_id,
                'title': title,
                'document_type': 'Agency Guidance',
                'jurisdiction': 'federal',
                'source': 'doj-oip',
                'source_url': url,
                'text': text,
            }

            if insert_document(DB_PATH, doc):
                added += 1
                logger.info(f'Inserted: {title[:80]}')
            else:
                skipped += 1
                logger.info(f'Skipped (already exists): {title[:80]}')

        except Exception as e:
            logger.error(f'Error processing {url}: {e}')
            errors += 1

        time.sleep(RATE_LIMIT_DELAY)

    elapsed = time.time() - start
    log_ingestion(DB_PATH, source='doj-oip', added=added, skipped=skipped, errors=errors,
                  notes='DOJ OIP FOIA guidance documents from justice.gov/oip/oip-guidance')

    print(f'DOJ OIP guidance: {added} added, {skipped} skipped, {errors} errors')
    write_receipt(script='ingest_doj_oip', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
