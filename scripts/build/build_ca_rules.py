#!/usr/bin/env python3
"""Build California Public Records Act (CPRA) response rules.

Response deadlines, extension rules, judicial review procedures, and fee
rules from Cal. Gov. Code §§ 7922.000-7931.000 (as renumbered effective
January 1, 2023 by Stats. 2021, Ch. 614 (SB 92)).

Run: python3 scripts/build/build_ca_rules.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

CA_RULES = [
    # Initial response
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '10',
        'day_type': 'calendar',
        'statute_citation': 'Cal. Gov. Code § 7922.535',
        'notes': 'Agency must determine within 10 calendar days whether the request, in whole or in part, seeks disclosable public records. Formerly Gov. Code § 6253(c). Note: this is a determination deadline, not a production deadline — records can be provided later while production is being prepared.',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'determination_content',
        'param_value': 'grant_deny_or_partial',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.535(a)',
        'notes': 'The 10-day determination must state: (1) whether responsive records exist and will be provided; (2) the specific exemptions relied on for any denial; or (3) a partial grant with explanation of what is and is not being produced. A non-committal acknowledgment does not satisfy the determination requirement.',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'after_10_day_deadline',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.535',
        'notes': 'Failure to respond within 10 days is a constructive denial, which the requester may immediately treat as a denial and seek judicial review without waiting further. Courts have held that agencies cannot cure a constructive denial by later producing records to moot a lawsuit.',
    },
    # Extension
    {
        'jurisdiction': 'CA',
        'rule_type': 'extension',
        'param_key': 'max_extension_days',
        'param_value': '14',
        'day_type': 'calendar',
        'statute_citation': 'Cal. Gov. Code § 7922.535(b)',
        'notes': 'Agency may extend the 10-day determination deadline by up to 14 calendar days (for a total of 24 calendar days) upon written notice to the requester stating the reason for the extension. Formerly Gov. Code § 6253(c).',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'extension',
        'param_key': 'unusual_circumstances_criteria',
        'param_value': 'need_to_search_facilities,voluminous_records,consult_other_agency,legal_review',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.535(b)',
        'notes': 'Unusual circumstances justifying extension include: (1) need to search and collect records from field facilities or multiple components; (2) voluminous records requiring extensive search; (3) need to consult with another agency; (4) need for legal review of complex exemption questions. The notice must state the specific reason.',
    },
    # Production timeline (distinct from determination)
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'production_timeline',
        'param_value': 'promptly_as_practicable',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.530',
        'notes': 'Even after a timely 10-day determination, production of the records must occur "promptly" — as soon as reasonably practicable. The CPRA does not set a fixed production deadline separate from the determination deadline, but courts have found that unreasonable delays in production violate the act. Agencies may not use the determination/production distinction to indefinitely delay disclosure.',
    },
    # No administrative appeal required
    {
        'jurisdiction': 'CA',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal_required',
        'param_value': 'false',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7923.000',
        'notes': 'California CPRA does NOT require exhaustion of administrative remedies. A requester may proceed directly to superior court after a denial (or constructive denial). This is a significant difference from federal FOIA, which requires administrative appeal before suit. Formerly Gov. Code § 6258.',
    },
    # Judicial review
    {
        'jurisdiction': 'CA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'court',
        'param_value': 'superior_court',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7923.000',
        'notes': 'Judicial review of CPRA denials is in the superior court of the county where the agency is located or where the requester resides. Requesters may seek a writ of mandate (Code of Civil Procedure § 1085) to compel disclosure.',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'burden_of_proof',
        'param_value': 'agency',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7923.000',
        'notes': 'The burden of proving an exemption applies rests on the agency. The agency must affirmatively demonstrate both that the exemption exists and that the specific records fall within it. Formerly Gov. Code § 6259. This differs from federal FOIA where the agency also bears the burden.',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'statute_of_limitations',
        'param_value': 'unclear_apply_general_3yr',
        'day_type': 'years',
        'statute_citation': 'Cal. Code Civ. Proc. § 338',
        'notes': 'The CPRA does not set an explicit statute of limitations for seeking judicial review. Courts typically apply the general 3-year statute of limitations for non-contract civil claims (CCP § 338). Act promptly after denial regardless.',
    },
    # Fees
    {
        'jurisdiction': 'CA',
        'rule_type': 'fee_cap',
        'param_key': 'fee_basis',
        'param_value': 'direct_cost_of_duplication',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.530(b)',
        'notes': 'California limits fees to the "direct cost of duplication" — the actual, incremental cost of making the copies. Agencies may NOT charge for staff time to search, review, or redact records. This is more restrictive than federal FOIA and many other states. Formerly Gov. Code § 6253(b).',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_records_fee',
        'param_value': 'direct_cost_only',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.530(b)',
        'notes': 'For records provided in electronic format, the fee is limited to the direct cost of producing an electronic copy (e.g., cost of a USB drive, or essentially nothing for email delivery). Agencies cannot charge for staff time to extract or convert electronic records.',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'fee_cap',
        'param_key': 'search_or_review_fees',
        'param_value': 'not_permitted',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.530',
        'notes': 'Expressly prohibited: agencies cannot charge for time spent searching for, locating, or reviewing records, or for time spent by attorneys reviewing records for exemptions. Only the actual cost of making copies is recoverable. This is one of the strongest fee protections for requesters in any U.S. public records law.',
    },
    # Attorney's fees
    {
        'jurisdiction': 'CA',
        'rule_type': 'fee_waiver',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7923.115',
        'notes': 'A court may award attorney\'s fees and costs to a requester who "prevails" in a CPRA lawsuit. California courts have interpreted "prevails" broadly: if the lawsuit was the catalyst that caused the agency to produce records, the requester may recover fees even if the case is dismissed as moot after production. This is a powerful enforcement mechanism. Formerly Gov. Code § 6259(d).',
    },
    {
        'jurisdiction': 'CA',
        'rule_type': 'fee_waiver',
        'param_key': 'catalyst_doctrine',
        'param_value': 'applies',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7923.115',
        'notes': 'Under the catalyst doctrine (confirmed in Press Enterprise Co. v. Superior Court), a requester who files suit and receives records after filing — even if the agency claims it would have produced them anyway — may be the "prevailing party" for attorney\'s fees. This discourages strategic delays by agencies.',
    },
    # Inspection vs. copies
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'inspection_right',
        'param_value': 'free',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.530(a)',
        'notes': 'Any person has the right to inspect public records free of charge. Fees may only be charged for copies (duplication). A requester who wants only to inspect records and take notes cannot be charged any fee. Formerly Gov. Code § 6253(a).',
    },
    # Format
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'electronic_format_requirement',
        'param_value': 'required_if_requested_and_feasible',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.545',
        'notes': 'If a public record is available in electronic format and the requester requests it in electronic format, the agency must provide it in that format, provided it does not jeopardize the integrity of the record or the agency\'s computer system. Formerly Gov. Code § 6253.9. Agency cannot charge extra for electronic delivery if it reduces duplication costs.',
    },
    # Redaction and segregability
    {
        'jurisdiction': 'CA',
        'rule_type': 'initial_response',
        'param_key': 'segregability',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'Cal. Gov. Code § 7922.525',
        'notes': 'The agency must segregate exempt from non-exempt portions and disclose the non-exempt portions. If a record contains both exempt and non-exempt information, only the exempt portion may be withheld. Failure to segregate is an independent CPRA violation. Formerly Gov. Code § 6257.',
    },
    # Judicial review — injunctive relief
    {
        'jurisdiction': 'CA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'preliminary_injunction',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Cal. Code Civ. Proc. § 527',
        'notes': 'Courts may grant preliminary injunctions or temporary restraining orders to compel production of public records pending final judgment. In urgent cases — especially those involving time-sensitive public interest matters — a TRO can be obtained in 1-3 days. Courts have granted emergency relief in election and breaking-news contexts.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for rule in CA_RULES:
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
    print(f'CA CPRA response rules: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ca_rules', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
