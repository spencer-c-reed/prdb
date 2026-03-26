#!/usr/bin/env python3
"""Ingest federal FOIA case law from CourtListener.

Searches CourtListener for opinions citing 5 U.S.C. § 552 (FOIA),
filtering for federal courts.

API docs: https://www.courtlistener.com/api/rest/v4/

Run: python3 scripts/ingest/federal/ingest_courtlistener_foia.py
"""

import os
import json
import sys
import time
import logging
from datetime import datetime, timedelta

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from ingest.utils import insert_document, log_ingestion, normalize_text
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'db', 'prdb.db')

CL_API = 'https://www.courtlistener.com/api/rest/v4'
CL_TOKEN = os.environ.get('COURTLISTENER_TOKEN', '')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0',
}
if CL_TOKEN:
    HEADERS['Authorization'] = f'Token {CL_TOKEN}'

# FOIA-related search queries
FOIA_QUERIES = [
    '"freedom of information act"',
    '"5 U.S.C. § 552"',
    '"5 U.S.C. 552"',
    'FOIA exemption',
]

# Federal court IDs in CourtListener
FEDERAL_COURTS = [
    'scotus',     # Supreme Court
    'ca1', 'ca2', 'ca3', 'ca4', 'ca5', 'ca6', 'ca7', 'ca8', 'ca9', 'ca10', 'ca11', 'cadc', 'cafc',  # Circuits
]

RATE_LIMIT_DELAY = 2.0  # seconds between API calls
MAX_RESULTS_PER_QUERY = 200  # per search query

# CourtListener v4 opinions endpoint requires auth token.
# Search endpoint is public and returns metadata + snippets.
# We use search data directly rather than fetching full opinion text.
SKIP_OPINION_FETCH = not CL_TOKEN


def _classify_court(court_str):
    """Classify court type from CourtListener court string."""
    if not court_str:
        return 'Federal Court Opinion'
    court_lower = court_str.lower()
    if 'supreme' in court_lower:
        return 'Supreme Court Opinion'
    if 'circuit' in court_lower or 'court of appeals' in court_lower:
        return 'Circuit Court Opinion'
    if 'district' in court_lower:
        return 'District Court Opinion'
    return 'Federal Court Opinion'


def search_opinions(query, max_results=MAX_RESULTS_PER_QUERY):
    """Search CourtListener for FOIA opinions."""
    results = []
    offset = 0
    page_size = 20

    while len(results) < max_results:
        params = {
            'q': query,
            'type': 'o',  # opinions
            'order_by': 'score desc',
            'stat_Published': 'on',
            'court': ','.join(FEDERAL_COURTS),
        }

        url = f'{CL_API}/search/'
        logger.info(f'Searching CourtListener: {query} (offset {offset})')

        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
            if resp.status_code == 429:
                logger.warning('Rate limited, waiting 30s...')
                time.sleep(30)
                continue
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.error(f'API error: {e}')
            break
        except json.JSONDecodeError:
            logger.error('Invalid JSON response')
            break

        hits = data.get('results', [])
        if not hits:
            break

        results.extend(hits)
        offset += page_size

        if not data.get('next'):
            break

        time.sleep(RATE_LIMIT_DELAY)

    return results[:max_results]


def fetch_opinion_text(cluster_id):
    """Fetch full opinion text from CourtListener."""
    url = f'{CL_API}/opinions/?cluster={cluster_id}'
    logger.info(f'Fetching opinion text for cluster {cluster_id}')

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        opinions = data.get('results', [])
        if not opinions:
            return None

        # Get the main opinion (usually the first one)
        for op in opinions:
            text = op.get('plain_text') or op.get('html_lawbox') or op.get('html_columbia') or op.get('html')
            if text:
                # Strip HTML if needed
                if '<' in text and '>' in text:
                    from bs4 import BeautifulSoup
                    text = BeautifulSoup(text, 'html.parser').get_text(separator='\n')
                return normalize_text(text)

        return None
    except Exception as e:
        logger.error(f'Error fetching opinion {cluster_id}: {e}')
        return None


def main():
    start = time.time()
    added = 0
    skipped = 0
    errors = 0
    seen_ids = set()

    for query in FOIA_QUERIES:
        logger.info(f'Processing query: {query}')
        results = search_opinions(query)
        logger.info(f'Got {len(results)} results for: {query}')

        for result in results:
            cluster_id = result.get('cluster_id')
            if not cluster_id or cluster_id in seen_ids:
                continue
            seen_ids.add(cluster_id)

            case_name = result.get('caseName', 'Unknown Case')
            court = result.get('court', '')
            date_filed = result.get('dateFiled', '')
            citation = result.get('citation', [])
            citation_str = citation[0] if citation else f'CL-{cluster_id}'
            absolute_url = result.get('absolute_url', '')
            snippet = result.get('snippet', '')

            doc_type = _classify_court(court)
            docket_number = result.get('docketNumber', '')
            judge = result.get('judge', '')

            # Try to get full text if we have auth
            text = None
            if not SKIP_OPINION_FETCH:
                try:
                    text = fetch_opinion_text(cluster_id)
                    time.sleep(RATE_LIMIT_DELAY)
                except Exception:
                    text = None

            if not text:
                # Build structured text from search metadata so each case is unique
                parts = [case_name]
                if court:
                    parts.append(f'Court: {court}')
                if date_filed:
                    parts.append(f'Date: {date_filed[:10]}')
                if docket_number:
                    parts.append(f'Docket: {docket_number}')
                if citation_str:
                    parts.append(f'Citation: {citation_str}')
                if judge:
                    parts.append(f'Judge: {judge}')
                if snippet:
                    # Strip HTML highlight tags from snippet
                    clean_snippet = snippet.replace('<mark>', '').replace('</mark>', '')
                    parts.append(f'\n{clean_snippet}')
                text = '\n'.join(parts)

            source_url = f'https://www.courtlistener.com{absolute_url}' if absolute_url else None

            doc = {
                'id': f'cl-foia-{cluster_id}',
                'citation': citation_str,
                'title': case_name,
                'date': date_filed[:10] if date_filed else None,
                'court': court,
                'document_type': doc_type,
                'jurisdiction': 'federal',
                'source': 'courtlistener-foia',
                'source_url': source_url,
                'text': text,
                'summary': snippet[:500].replace('<mark>', '').replace('</mark>', '') if snippet else None,
            }

            try:
                if insert_document(DB_PATH, doc):
                    added += 1
                    if added % 10 == 0:
                        logger.info(f'Progress: {added} added, {skipped} skipped')
                else:
                    skipped += 1
            except Exception as e:
                logger.error(f'Error inserting {case_name}: {e}')
                errors += 1

    elapsed = time.time() - start
    log_ingestion(DB_PATH, source='courtlistener-foia', added=added, skipped=skipped, errors=errors,
                  notes=f'Federal FOIA case law from CourtListener ({len(seen_ids)} unique clusters)')

    print(f'CourtListener FOIA: {added} added, {skipped} skipped, {errors} errors ({len(seen_ids)} unique)')
    write_receipt(script='ingest_courtlistener_foia', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
