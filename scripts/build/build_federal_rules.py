#!/usr/bin/env python3
"""Build federal FOIA response rules.

Response deadlines, extension rules, appeal deadlines, and fee waiver criteria
from 5 U.S.C. § 552 and 28 CFR Part 16.

Run: python3 scripts/build/build_federal_rules.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

FEDERAL_RULES = [
    # Initial response
    {
        'jurisdiction': 'federal',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '20',
        'day_type': 'business',
        'statute_citation': '5 U.S.C. § 552(a)(6)(A)(i)',
        'notes': 'Agency must make a determination within 20 business days of receipt. Clock starts when request reaches proper FOIA office.',
    },
    # Extension
    {
        'jurisdiction': 'federal',
        'rule_type': 'extension',
        'param_key': 'max_extension_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': '5 U.S.C. § 552(a)(6)(B)(i)',
        'notes': 'Agency may extend by up to 10 business days in "unusual circumstances" (need to search field offices, voluminous records, or consult with other agencies).',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'extension',
        'param_key': 'unusual_circumstances_criteria',
        'param_value': 'search_field_offices,voluminous_records,consult_other_agency',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(6)(B)(iii)',
        'notes': 'Unusual circumstances: (I) records in field offices, (II) voluminous records, (III) need to consult with another agency or agency component.',
    },
    # Appeal deadline
    {
        'jurisdiction': 'federal',
        'rule_type': 'appeal_deadline',
        'param_key': 'days_to_appeal',
        'param_value': '90',
        'day_type': 'calendar',
        'statute_citation': '28 CFR § 16.9(a)',
        'notes': 'DOJ allows 90 calendar days to file administrative appeal. Other agencies may have different deadlines — check agency-specific regulations.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'appeal_deadline',
        'param_key': 'appeal_response_days',
        'param_value': '20',
        'day_type': 'business',
        'statute_citation': '5 U.S.C. § 552(a)(6)(A)(ii)',
        'notes': 'Agency must make a determination on appeal within 20 business days.',
    },
    # Judicial review
    {
        'jurisdiction': 'federal',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'statute_of_limitations',
        'param_value': '6',
        'day_type': 'years',
        'statute_citation': '28 U.S.C. § 2401(a)',
        'notes': 'General 6-year statute of limitations for civil actions against the US. Must exhaust administrative remedies first.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'court_standard',
        'param_value': 'de_novo',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(4)(B)',
        'notes': 'Court reviews agency withholding de novo. Burden is on the agency to justify withholding.',
    },
    # Fee waiver
    {
        'jurisdiction': 'federal',
        'rule_type': 'fee_waiver',
        'param_key': 'standard',
        'param_value': 'public_interest',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(4)(A)(iii)',
        'notes': 'Fee waiver or reduction if disclosure is in the public interest because it is likely to contribute significantly to public understanding of the operations or activities of the government and is not primarily in the commercial interest of the requester.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'fee_waiver',
        'param_key': 'requester_categories',
        'param_value': 'commercial,educational_institution,noncommercial_scientific,news_media,other',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(4)(A)(ii)',
        'notes': 'Fee schedule varies by requester category. News media and educational/scientific requesters get reduced fees.',
    },
    # Expedited processing
    {
        'jurisdiction': 'federal',
        'rule_type': 'expedited_processing',
        'param_key': 'response_to_request',
        'param_value': '10',
        'day_type': 'calendar',
        'statute_citation': '5 U.S.C. § 552(a)(6)(E)(ii)',
        'notes': 'Agency must respond to request for expedited processing within 10 calendar days.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'expedited_processing',
        'param_key': 'criteria',
        'param_value': 'imminent_threat_to_life,urgency_to_inform_public,loss_of_due_process,agency_specific',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(6)(E)(i)',
        'notes': 'Expedited processing standards: (I) imminent threat to life/safety, (II) urgency to inform public about government activity (for requesters primarily engaged in disseminating information). Agencies may establish additional criteria.',
    },
    # Fee caps
    {
        'jurisdiction': 'federal',
        'rule_type': 'fee_cap',
        'param_key': 'search_per_hour',
        'param_value': 'varies_by_agency',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(4)(A)(ii)',
        'notes': 'Fees vary by agency. OMB Fee Guidelines establish categories: search fees, duplication fees, review fees. Agencies set specific hourly rates.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page',
        'param_value': '0.10-0.25',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(4)(A)(ii)',
        'notes': 'Standard duplication cost is $0.10-$0.25 per page. Electronic records may have different cost structures.',
    },
    {
        'jurisdiction': 'federal',
        'rule_type': 'fee_cap',
        'param_key': 'minimum_charge_threshold',
        'param_value': '25.00',
        'day_type': None,
        'statute_citation': 'OMB Fee Guidelines',
        'notes': 'Many agencies waive fees below $25 (or similar threshold). Check agency-specific FOIA regulations.',
    },
    # Constructive denial
    {
        'jurisdiction': 'federal',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'after_deadline',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(a)(6)(C)',
        'notes': 'If agency fails to respond within statutory time limits, requester may treat as constructive denial and file suit. However, courts may allow agency additional time under "exceptional circumstances."',
    },
    # OGIS mediation
    {
        'jurisdiction': 'federal',
        'rule_type': 'appeal_deadline',
        'param_key': 'ogis_mediation',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': '5 U.S.C. § 552(h)',
        'notes': 'OGIS (Office of Government Information Services) offers free mediation services as a non-exclusive alternative to litigation. Available at any point in the process.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for rule in FEDERAL_RULES:
            existing = conn.execute(
                'SELECT id FROM response_rules WHERE jurisdiction = ? AND rule_type = ? AND param_key = ?',
                (rule['jurisdiction'], rule['rule_type'], rule['param_key'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE response_rules SET
                        param_value = ?, day_type = ?, statute_citation = ?,
                        notes = ?, last_verified = datetime('now'), updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                     rule.get('notes'), existing[0])
                )
                skipped += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO response_rules (
                        jurisdiction, rule_type, param_key, param_value,
                        day_type, statute_citation, notes, last_verified
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    ''',
                    (rule['jurisdiction'], rule['rule_type'], rule['param_key'],
                     rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                     rule.get('notes'))
                )
                added += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'Federal response rules: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_federal_rules', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
