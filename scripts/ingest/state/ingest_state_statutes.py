#!/usr/bin/env python3
"""Ingest state public records law statutes for NY, CA, and TX.

Sources:
  NY  - NY Senate website (Public Officers Law §§ 84-90 — FOIL)
  CA  - California Legislative Information (Gov. Code §§ 7920.000-7931 — CPRA)
  TX  - Texas Statutes (Gov. Code Ch. 552 — TPIA)

Run: python3 scripts/ingest/state/ingest_state_statutes.py
"""

import os
import re
import sys
import time
import logging

import requests
from bs4 import BeautifulSoup

# Resolve project root (four levels up from this file)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from ingest.utils import insert_document, log_ingestion, normalize_text
from ingest.utils.receipt import write_receipt

# Ensure the state/ directory exists (idempotent)
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    'db', 'prdb.db'
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0 (public records research database; +https://github.com)',
    'Accept': 'text/html',
}

RATE_LIMIT_DELAY = 3.0  # seconds between requests

# ---------------------------------------------------------------------------
# Statute definitions
# Each entry carries source-routing metadata so the fetcher knows which
# extraction strategy to use.
# ---------------------------------------------------------------------------

STATUTES = [
    # -----------------------------------------------------------------------
    # New York — Freedom of Information Law (FOIL)
    # NY Public Officers Law §§ 84-90
    # Source: NY Senate website
    # -----------------------------------------------------------------------
    {
        'id': 'ny-statute-foil-84',
        'citation': 'N.Y. Pub. Off. Law § 84',
        'title': 'New York Freedom of Information Law (FOIL) — Legislative Declaration',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/84',
        'summary': 'Legislative declaration establishing the policy that government is the public\'s business and that the public\'s right to know must be protected.',
    },
    {
        'id': 'ny-statute-foil-85',
        'citation': 'N.Y. Pub. Off. Law § 85',
        'title': 'New York FOIL — Short Title',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/85',
        'summary': 'Establishes the short title "Freedom of Information Law" for Article 6 of the Public Officers Law.',
    },
    {
        'id': 'ny-statute-foil-86',
        'citation': 'N.Y. Pub. Off. Law § 86',
        'title': 'New York FOIL — Definitions',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/86',
        'summary': 'Defines key terms including "agency," "record," and "person" as used in the Freedom of Information Law.',
    },
    {
        'id': 'ny-statute-foil-87',
        'citation': 'N.Y. Pub. Off. Law § 87',
        'title': 'New York FOIL — Access to Agency Records',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/87',
        'summary': 'Core access provision requiring agencies to make records available for public inspection and copying, with enumerated exemptions.',
    },
    {
        'id': 'ny-statute-foil-88',
        'citation': 'N.Y. Pub. Off. Law § 88',
        'title': 'New York FOIL — Agency Publication Requirements',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/88',
        'summary': 'Requires agencies to publish rules, final opinions, instructions affecting the public, and policy statements.',
    },
    {
        'id': 'ny-statute-foil-89',
        'citation': 'N.Y. Pub. Off. Law § 89',
        'title': 'New York FOIL — Procedures, Fees, and Appeals',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/89',
        'summary': 'Establishes request procedures, agency response timelines, fee schedules, and the administrative appeal process.',
    },
    {
        'id': 'ny-statute-foil-90',
        'citation': 'N.Y. Pub. Off. Law § 90',
        'title': 'New York FOIL — Severability',
        'document_type': 'State FOIL Statute',
        'jurisdiction': 'NY',
        'source': 'nysenate',
        'url': 'https://www.nysenate.gov/legislation/laws/PBO/90',
        'summary': 'Severability clause for the Freedom of Information Law.',
    },

    # -----------------------------------------------------------------------
    # California — California Public Records Act (CPRA)
    # Gov. Code §§ 7920.000 – 7931 (renumbered 2023)
    # Source: California Legislative Information
    # -----------------------------------------------------------------------
    {
        'id': 'ca-statute-cpra-7920',
        'citation': 'Cal. Gov. Code § 7920.000',
        'title': 'California Public Records Act (CPRA) — Definitions',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7920.000.&lawCode=GOV',
        'summary': 'Core definitions for the California Public Records Act, including "public agency," "public records," and related terms.',
    },
    {
        'id': 'ca-statute-cpra-7921',
        'citation': 'Cal. Gov. Code § 7921.000',
        'title': 'California Public Records Act — Legislative Intent',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7921.000.&lawCode=GOV',
        'summary': 'Legislative intent: public records are a fundamental right; disclosure is the rule and withholding the exception.',
    },
    {
        'id': 'ca-statute-cpra-7922',
        'citation': 'Cal. Gov. Code § 7922.000',
        'title': 'California Public Records Act — Right of Access',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7922.000.&lawCode=GOV',
        'summary': 'Establishes the right of every person to inspect or receive copies of public records, subject to the enumerated exemptions.',
    },
    {
        'id': 'ca-statute-cpra-7923',
        'citation': 'Cal. Gov. Code § 7923.000',
        'title': 'California Public Records Act — Exemptions',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7923.000.&lawCode=GOV',
        'summary': 'General exemptions from disclosure, including the catchall balancing test for records where the public interest in nondisclosure outweighs the interest in disclosure.',
    },
    {
        'id': 'ca-statute-cpra-7927',
        'citation': 'Cal. Gov. Code § 7927.000',
        'title': 'California Public Records Act — Law Enforcement Records',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7927.000.&lawCode=GOV',
        'summary': 'Exemptions and disclosure obligations specific to law enforcement records, including investigative files and personnel records.',
    },
    {
        'id': 'ca-statute-cpra-7930',
        'citation': 'Cal. Gov. Code § 7930.000',
        'title': 'California Public Records Act — Response Requirements',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7930.000.&lawCode=GOV',
        'summary': 'Agency obligation to respond within 10 days, notify of determinations, and provide access or state reasons for withholding.',
    },
    {
        'id': 'ca-statute-cpra-7931',
        'citation': 'Cal. Gov. Code § 7931.000',
        'title': 'California Public Records Act — Judicial Remedies',
        'document_type': 'State CPRA Statute',
        'jurisdiction': 'CA',
        'source': 'ca-leginfo',
        'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7931.000.&lawCode=GOV',
        'summary': 'Enforcement mechanism: any person denied access may petition the superior court for an order requiring disclosure; prevailing parties may recover attorney fees.',
    },

    # -----------------------------------------------------------------------
    # Texas — Texas Public Information Act (TPIA)
    # Gov. Code Ch. 552
    # Source: Texas Statutes (capitol.texas.gov)
    # Fetched as a single chapter page — split by subchapter in the extractor.
    # -----------------------------------------------------------------------
    {
        'id': 'tx-statute-tpia-552',
        'citation': 'Tex. Gov. Code Ch. 552',
        'title': 'Texas Public Information Act (TPIA)',
        'document_type': 'State TPIA Statute',
        'jurisdiction': 'TX',
        'source': 'tx-statutes',
        'url': 'https://statutes.capitol.texas.gov/Docs/GV/htm/GV.552.htm',
        'summary': 'Texas Public Information Act: establishes that government information is presumed to be available to the public, sets out procedures for requesting records, enumerates exceptions, and provides remedies for wrongful withholding.',
    },
]


# ---------------------------------------------------------------------------
# Source-specific fetchers
# ---------------------------------------------------------------------------

def fetch_nysenate(url: str) -> str | None:
    """Fetch a single section from the NY Senate website."""
    logger.info(f'Fetching NY Senate: {url}')
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # The statute text lives in .c-bill-text or .bill-text on nysenate.gov
    content = (
        soup.find('div', class_='c-bill-text')
        or soup.find('div', class_='bill-text')
        or soup.find('section', class_='c-bill-text')
        or soup.find('div', {'data-ng-bind-html': True})
    )

    if not content:
        # Fallback: look for the main article body
        content = soup.find('main') or soup.find('article') or soup.find('div', id='content')

    if not content:
        logger.warning(f'No content container found for {url}')
        return None

    for tag in content.find_all(['nav', 'script', 'style', 'header', 'footer']):
        tag.decompose()

    text = content.get_text(separator='\n')
    return normalize_text(text)


def fetch_ca_leginfo(url: str) -> str | None:
    """Fetch a section from California Legislative Information."""
    logger.info(f'Fetching CA LegInfo: {url}')
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Cal LegInfo wraps statute text in div#codeLawSectionNoHead or similar
    content = (
        soup.find('div', id='codeLawSectionNoHead')
        or soup.find('div', id='codeLawSection')
        or soup.find('div', class_='legislativeContentDiv')
    )

    if not content:
        # Broader fallback
        content = soup.find('div', id='content') or soup.find('main')

    if not content:
        logger.warning(f'No content container found for {url}')
        return None

    for tag in content.find_all(['nav', 'script', 'style', 'header', 'footer']):
        tag.decompose()

    text = content.get_text(separator='\n')
    return normalize_text(text)


def fetch_tx_statutes(url: str) -> str | None:
    """Fetch a chapter from the Texas Statutes website."""
    logger.info(f'Fetching TX Statutes: {url}')
    resp = requests.get(url, headers=HEADERS, timeout=120)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # The TX statutes page is a plain HTML file; most content is in <body>
    # Strip navigation boilerplate at the top/bottom.
    for tag in soup.find_all(['nav', 'script', 'style']):
        tag.decompose()

    body = soup.find('body')
    if not body:
        logger.warning(f'No body tag found for {url}')
        return None

    text = body.get_text(separator='\n')
    return normalize_text(text)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

SOURCE_FETCHERS = {
    'nysenate': fetch_nysenate,
    'ca-leginfo': fetch_ca_leginfo,
    'tx-statutes': fetch_tx_statutes,
}


def fetch_statute(statute: dict) -> str | None:
    """Dispatch to the appropriate fetcher based on statute['source']."""
    fetcher = SOURCE_FETCHERS.get(statute['source'])
    if not fetcher:
        logger.error(f'No fetcher for source "{statute["source"]}"')
        return None

    text = fetcher(statute['url'])

    if text and len(text) < 100:
        logger.warning(f'Suspiciously short text ({len(text)} chars) for {statute["citation"]}')
        return None

    return text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    start = time.time()
    added = 0
    skipped = 0
    errors = 0

    for statute in STATUTES:
        try:
            text = fetch_statute(statute)
            if not text:
                logger.error(f'Failed to extract text for {statute["citation"]}')
                errors += 1
                continue

            doc = {
                'id': statute['id'],
                'citation': statute['citation'],
                'title': statute['title'],
                'document_type': statute['document_type'],
                'jurisdiction': statute['jurisdiction'],
                'source': statute['source'],
                'source_url': statute['url'],
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
    log_ingestion(
        DB_PATH,
        source='state-statutes',
        added=added,
        skipped=skipped,
        errors=errors,
        notes='NY FOIL (PBO §§ 84-90), CA CPRA (Gov. Code §§ 7920-7931), TX TPIA (Gov. Code Ch. 552)',
    )

    print(f'State statutes: {added} added, {skipped} skipped, {errors} errors')
    write_receipt(
        script='ingest_state_statutes',
        added=added,
        skipped=skipped,
        errors=errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
