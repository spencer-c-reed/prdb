#!/usr/bin/env python3
"""Ingest the federal FOIA statute (5 U.S.C. § 552) and related statutes
from Cornell LII.

Also ingests:
- Privacy Act (5 U.S.C. § 552a)
- Government in the Sunshine Act (5 U.S.C. § 552b)
- OPEN Government Act provisions

Run: python3 scripts/ingest/federal/ingest_foia_statute.py
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
CORNELL_BASE = 'https://www.law.cornell.edu'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0 (public records research database; +https://github.com)',
    'Accept': 'text/html',
}

STATUTES = [
    {
        'url': '/uscode/text/5/552',
        'section': '552',
        'title_num': '5',
        'citation': '5 U.S.C. § 552',
        'title': 'Freedom of Information Act (FOIA)',
        'document_type': 'Federal FOIA Statute',
        'summary': 'The Freedom of Information Act requires federal agencies to disclose records to any person who makes a proper request, subject to nine exemptions and three exclusions.',
    },
    {
        'url': '/uscode/text/5/552a',
        'section': '552a',
        'title_num': '5',
        'citation': '5 U.S.C. § 552a',
        'title': 'Privacy Act of 1974',
        'document_type': 'Privacy Act Statute',
        'summary': 'The Privacy Act governs the collection, maintenance, use, and dissemination of personally identifiable information maintained by federal agencies in systems of records.',
    },
    {
        'url': '/uscode/text/5/552b',
        'section': '552b',
        'title_num': '5',
        'citation': '5 U.S.C. § 552b',
        'title': 'Government in the Sunshine Act',
        'document_type': 'Open Meetings Statute',
        'summary': 'The Government in the Sunshine Act requires that meetings of multi-member federal agencies be open to public observation, with ten exemptions.',
    },
]

RATE_LIMIT_DELAY = 3.0  # seconds between requests


def fetch_statute_text(url):
    """Fetch and extract statute text from Cornell LII."""
    full_url = CORNELL_BASE + url
    logger.info(f'Fetching {full_url}')

    resp = requests.get(full_url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Find the statute content
    content_div = soup.find('div', class_='field-name-body') or soup.find('div', id='content')
    if not content_div:
        # Try alternative selectors
        content_div = soup.find('div', class_='tab-pane')

    if not content_div:
        logger.warning(f'Could not find content div for {url}')
        return None

    # Remove navigation, footnotes, and other non-content elements
    for tag in content_div.find_all(['nav', 'script', 'style']):
        tag.decompose()

    text = content_div.get_text(separator='\n')
    text = normalize_text(text)

    if len(text) < 100:
        logger.warning(f'Suspiciously short text ({len(text)} chars) for {url}')
        return None

    return text


def main():
    start = time.time()
    added = 0
    skipped = 0
    errors = 0

    for statute in STATUTES:
        try:
            text = fetch_statute_text(statute['url'])
            if not text:
                logger.error(f'Failed to extract text for {statute["citation"]}')
                errors += 1
                continue

            doc = {
                'id': f'federal-statute-{statute["section"]}',
                'citation': statute['citation'],
                'title': statute['title'],
                'document_type': statute['document_type'],
                'jurisdiction': 'federal',
                'source': 'cornell-lii',
                'source_url': CORNELL_BASE + statute['url'],
                'text': text,
                'summary': statute['summary'],
            }

            if insert_document(DB_PATH, doc):
                added += 1
                logger.info(f'Inserted {statute["citation"]}')
            else:
                skipped += 1
                logger.info(f'Skipped {statute["citation"]} (already exists)')

            time.sleep(RATE_LIMIT_DELAY)

        except requests.RequestException as e:
            logger.error(f'HTTP error for {statute["citation"]}: {e}')
            errors += 1
        except Exception as e:
            logger.error(f'Error processing {statute["citation"]}: {e}')
            errors += 1

    elapsed = time.time() - start
    log_ingestion(DB_PATH, source='cornell-lii-foia', added=added, skipped=skipped, errors=errors,
                  notes=f'Federal FOIA/Privacy/Sunshine statutes from Cornell LII')

    print(f'Federal statutes: {added} added, {skipped} skipped, {errors} errors')
    write_receipt(script='ingest_foia_statute', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
