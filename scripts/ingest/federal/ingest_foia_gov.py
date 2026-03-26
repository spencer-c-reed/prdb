#!/usr/bin/env python3
"""Ingest the federal agency FOIA directory from FOIA.gov.

FOIA.gov provides a public API with agency FOIA contact information,
submission methods, and links to agency FOIA pages.

API docs: https://www.foia.gov/developer/

Run: python3 scripts/ingest/federal/ingest_foia_gov.py
"""

import os
import json
import sys
import time
import logging

import requests

# Load .env if present (no dotenv dependency)
_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), '.env')
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'db', 'prdb.db')

# FOIA.gov API endpoint
FOIA_GOV_API = 'https://api.foia.gov/api'
FOIA_GOV_KEY = os.environ.get('FOIA_GOV_API_KEY', 'DEMO_KEY')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'PRDB-Research-Bot/1.0',
    'Accept': 'application/json',
    'X-API-Key': FOIA_GOV_KEY,
}


def fetch_agencies():
    """Fetch all agencies from FOIA.gov API."""
    # The FOIA.gov agency list is available at /agency_components
    # Try the Drupal JSON API endpoint
    url = f'{FOIA_GOV_API}/agency_components'
    all_components = []
    page = 0

    while True:
        params = {
            'page[offset]': page * 50,
            'page[limit]': 50,
        }
        logger.info(f'Fetching agencies page {page}...')

        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.error(f'API error: {e}')
            break
        except json.JSONDecodeError:
            logger.error(f'Invalid JSON response')
            break

        items = data.get('data', [])
        if not items:
            break

        # Filter out null/non-dict items from JSON:API response
        all_components.extend(item for item in items if isinstance(item, dict) and item.get('attributes'))
        page += 1

        # Check for next page
        next_link = data.get('links', {}).get('next')
        if not next_link:
            break

        time.sleep(1.0)

    return all_components


def parse_component(component):
    """Parse a FOIA.gov agency component into our agency format."""
    if not component or not isinstance(component, dict):
        return None
    attrs = component.get('attributes') or {}

    # Extract contact info
    email = None
    emails = attrs.get('email', [])
    if emails:
        email = emails[0] if isinstance(emails, list) else emails

    address_parts = []
    address = attrs.get('address', {})
    if isinstance(address, dict):
        for field in ['address_line1', 'address_line2', 'locality', 'administrative_area', 'postal_code']:
            val = address.get(field)
            if val:
                address_parts.append(val)
    mailing_address = ', '.join(address_parts) if address_parts else None

    phone = attrs.get('telephone')
    fax = attrs.get('fax')

    # Determine submission method
    portal_url = attrs.get('submission_url') or attrs.get('website', {}).get('uri')
    submission_methods = []
    if portal_url:
        submission_methods.append('portal')
    if email:
        submission_methods.append('email')
    if mailing_address:
        submission_methods.append('mail')
    if fax:
        submission_methods.append('fax')
    submission_method = ','.join(submission_methods) if submission_methods else 'unknown'

    # Fee waiver
    fee_waiver_info = attrs.get('fee_waiver_instructions')

    return {
        'name': attrs.get('title', 'Unknown Agency'),
        'jurisdiction': 'federal',
        'level': 'federal',
        'abbreviation': attrs.get('abbreviation'),
        'foia_officer_title': 'FOIA Officer',
        'foia_officer_name': attrs.get('foia_officer_name'),
        'email': email,
        'mailing_address': mailing_address,
        'phone': phone,
        'fax': fax,
        'portal_url': portal_url,
        'submission_method': submission_method,
        'fee_waiver_available': 1,
        'fee_waiver_criteria': fee_waiver_info,
        'source_url': attrs.get('reading_room_url', {}).get('uri') if isinstance(attrs.get('reading_room_url'), dict) else None,
        'notes': f'Component ID: {component.get("id", "unknown")}',
    }


def main():
    start = time.time()

    logger.info('Fetching agencies from FOIA.gov...')
    components = fetch_agencies()
    logger.info(f'Retrieved {len(components)} agency components')

    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for component in components:
            try:
                agency = parse_component(component)
                if agency is None:
                    skipped += 1
                    continue

                # Check if already exists (by name + jurisdiction)
                existing = conn.execute(
                    'SELECT id FROM agencies WHERE name = ? AND jurisdiction = ?',
                    (agency['name'], agency['jurisdiction'])
                ).fetchone()

                if existing:
                    # Update
                    conn.execute(
                        '''
                        UPDATE agencies SET
                            abbreviation = COALESCE(?, abbreviation),
                            foia_officer_name = COALESCE(?, foia_officer_name),
                            email = COALESCE(?, email),
                            mailing_address = COALESCE(?, mailing_address),
                            phone = COALESCE(?, phone),
                            fax = COALESCE(?, fax),
                            portal_url = COALESCE(?, portal_url),
                            submission_method = ?,
                            fee_waiver_criteria = COALESCE(?, fee_waiver_criteria),
                            source_url = COALESCE(?, source_url),
                            notes = ?,
                            last_verified = datetime('now'),
                            last_scraped = datetime('now'),
                            updated_at = datetime('now')
                        WHERE id = ?
                        ''',
                        (agency['abbreviation'], agency['foia_officer_name'],
                         agency['email'], agency['mailing_address'],
                         agency['phone'], agency['fax'],
                         agency['portal_url'], agency['submission_method'],
                         agency['fee_waiver_criteria'], agency['source_url'],
                         agency['notes'], existing[0])
                    )
                    skipped += 1
                else:
                    conn.execute(
                        '''
                        INSERT INTO agencies (
                            name, jurisdiction, level, abbreviation,
                            foia_officer_title, foia_officer_name,
                            email, mailing_address, phone, fax,
                            portal_url, submission_method,
                            fee_waiver_available, fee_waiver_criteria,
                            source_url, notes,
                            last_verified, last_scraped
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                datetime('now'), datetime('now'))
                        ''',
                        (agency['name'], agency['jurisdiction'], agency['level'],
                         agency['abbreviation'], agency['foia_officer_title'],
                         agency['foia_officer_name'], agency['email'],
                         agency['mailing_address'], agency['phone'], agency['fax'],
                         agency['portal_url'], agency['submission_method'],
                         agency['fee_waiver_available'], agency['fee_waiver_criteria'],
                         agency['source_url'], agency['notes'])
                    )
                    added += 1

            except Exception as e:
                logger.error(f'Error processing component: {e}')
                errors += 1

        conn.commit()
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'FOIA.gov agencies: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='ingest_foia_gov', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
