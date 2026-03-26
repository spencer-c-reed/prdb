#!/usr/bin/env python3
"""Build New York FOIL response rules.

Response deadlines, appeal rules, fee schedules, and judicial review
under New York Public Officers Law §§ 84-90 (Freedom of Information Law).

Run: python3 scripts/build/build_ny_rules.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

NY_RULES = [
    # Initial response — acknowledgment
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'days_to_acknowledge',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'N.Y. Pub. Off. Law § 89(3)(a)',
        'notes': 'Agency must acknowledge receipt of a FOIL request within 5 business days. The acknowledgment must include a reference number and an estimate of when records will be available. If the agency can provide the records within 5 business days, a separate acknowledgment is not required.',
    },
    # Initial response — grant/deny
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '20',
        'day_type': 'business',
        'statute_citation': 'N.Y. Pub. Off. Law § 89(3)(a)',
        'notes': 'Agency must grant or deny access to records within 20 business days of receipt. If the agency cannot do so within 20 business days, it must provide an approximate date (within a reasonable time) when the request will be granted or denied. "Reasonable time" has been interpreted by courts and COOG as typically no more than a few months absent exceptional circumstances.',
    },
    # Reasonable time / constructive denial
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'after_reasonable_time',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 89(3)(a)',
        'notes': 'If an agency fails to respond within 20 business days AND fails to provide a reasonable estimated response date, the failure constitutes a constructive denial that may be appealed. Courts have held that open-ended delays without a specific date are appealable as constructive denials. See Matter of Thomas v. Records Access Officer, 247 A.D.2d 875 (4th Dep\'t 1998).',
    },
    # Appeal deadline — requester must file
    {
        'jurisdiction': 'NY',
        'rule_type': 'appeal_deadline',
        'param_key': 'days_to_appeal',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': 'N.Y. Pub. Off. Law § 89(4)(a)',
        'notes': 'Requester must file an administrative appeal within 30 calendar days of a denial. The appeal goes to the head of the agency or the agency\'s designated appeals officer. Some agencies have shorter internal appeal periods — check the specific agency\'s FOIL regulations.',
    },
    # Appeal — agency must respond
    {
        'jurisdiction': 'NY',
        'rule_type': 'appeal_deadline',
        'param_key': 'appeal_response_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'N.Y. Pub. Off. Law § 89(4)(a)',
        'notes': 'Agency must fully explain in writing each reason for denial within 10 business days of receiving the appeal. The written explanation must identify the specific statutory exemption(s) relied upon. A failure to respond within 10 business days may be treated as a denial and reviewed by Article 78 proceeding.',
    },
    # Judicial review — Article 78
    {
        'jurisdiction': 'NY',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'statute_of_limitations',
        'param_value': '4',
        'day_type': 'months',
        'statute_citation': 'N.Y. C.P.L.R. § 217(1)',
        'notes': 'Article 78 proceedings to challenge FOIL denials must be commenced within 4 months of the final agency determination (i.e., the denial of the administrative appeal, or the expiration of the 10-business-day appeal response period). This is the general Article 78 statute of limitations.',
    },
    {
        'jurisdiction': 'NY',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'court_standard',
        'param_value': 'arbitrary_and_capricious',
        'day_type': None,
        'statute_citation': 'N.Y. C.P.L.R. § 7803(3); N.Y. Pub. Off. Law § 89(4)(b)',
        'notes': 'Courts review FOIL denials under the arbitrary and capricious standard. The agency bears the burden of demonstrating that the withheld records fall within a specific exemption. Courts may conduct in camera review of withheld records.',
    },
    {
        'jurisdiction': 'NY',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_if_substantially_prevails',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 89(4)(c)',
        'notes': 'Courts may award reasonable attorney fees and litigation costs to a requester who substantially prevails AND where the agency had no reasonable basis for denying access OR failed to respond to the request or appeal within statutory time limits. Fee awards are discretionary, not mandatory.',
    },
    # Fees — standard copy
    {
        'jurisdiction': 'NY',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_standard',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(1)(b)(iii)',
        'notes': 'Maximum fee of $0.25 per page for copies of records up to 9 inches by 14 inches. This is a statutory cap — agencies may not charge more per page for standard copies. Agencies may charge less.',
    },
    # Fees — large format
    {
        'jurisdiction': 'NY',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_large',
        'param_value': '0.50',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(1)(b)(iii)',
        'notes': 'Maximum fee of $0.50 per page for copies of records larger than 9 inches by 14 inches (e.g., architectural drawings, maps). Some agencies charge the actual cost of reproduction for oversized records.',
    },
    # Fees — electronic records
    {
        'jurisdiction': 'NY',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_records_fee',
        'param_value': 'actual_cost_of_medium_only',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(1)(b)(iii)',
        'notes': 'For electronic records, agencies may only charge the actual cost of the medium (e.g., a USB drive or CD). Agencies may NOT charge programming costs or staff time for extracting data from existing databases unless the agency can show no existing data retrieval capability. COOG has held that if a record exists in electronic form, the agency must provide it electronically at minimal cost.',
    },
    # Fee waiver — no statutory provision
    {
        'jurisdiction': 'NY',
        'rule_type': 'fee_waiver',
        'param_key': 'statutory_waiver',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(1)(b)',
        'notes': 'FOIL does not contain a statutory fee waiver provision analogous to federal FOIA. However, individual agencies may adopt fee waiver policies by regulation or policy. Requesters may ask for a fee waiver and cite public interest, but no statutory right to a waiver exists. The $0.25/page cap is the main cost protection. Some agencies waive fees for small requests or for nonprofit/media requesters by internal policy.',
    },
    # Expedited processing — no statutory provision
    {
        'jurisdiction': 'NY',
        'rule_type': 'expedited_processing',
        'param_key': 'statutory_expedited',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law §§ 84-90',
        'notes': 'FOIL does not contain a statutory expedited processing provision. However, requesters may ask for expedited treatment citing urgency, and courts have recognized that agencies should respond promptly to time-sensitive requests. In practice, arguing that records are needed for imminent litigation or a court deadline may prompt faster agency action.',
    },
    # COOG advisory opinions
    {
        'jurisdiction': 'NY',
        'rule_type': 'appeal_deadline',
        'param_key': 'coog_advisory_opinions',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 89(1)(b)',
        'notes': 'The Committee on Open Government (COOG) within the Department of State issues non-binding advisory opinions on FOIL and Open Meetings Law questions. Advisory opinions are persuasive authority: courts give them significant weight. Requesters and agencies may submit written questions to COOG. COOG opinions are available at https://www.dos.ny.gov/coog/.',
    },
    # Records availability — agency requirement to maintain
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'subject_matter_list',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(3)',
        'notes': 'Each agency must maintain a reasonably detailed current list by subject matter of all records in the agency\'s possession. The list must be available for public inspection and copying. Requesters may use this list to identify responsive records and to challenge agency claims of non-existence.',
    },
    # Records availability — posted online
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'online_posting_requirement',
        'param_value': 'required_for_frequently_requested',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 87(3)(b)',
        'notes': 'Agencies must post frequently requested records online. A record that has been requested three or more times must be posted on the agency\'s website. This provision, added in 2017, is intended to reduce redundant FOIL requests and improve transparency.',
    },
    # Segregability
    {
        'jurisdiction': 'NY',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'N.Y. Pub. Off. Law § 89(2)(a)',
        'notes': 'When an agency denies access to a record that contains both exempt and non-exempt portions, it must release the non-exempt portions after deleting the exempt material. The agency must inform the requester that portions are being withheld and cite the specific exemption for each deletion. Blanket withholding of entire documents when only portions are exempt is improper.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for rule in NY_RULES:
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
    print(f'NY FOIL response rules: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ny_rules', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
