#!/usr/bin/env python3
"""Build Texas Public Information Act response rules.

Response deadlines, AG ruling requirements, fee rules, and enforcement
mechanisms from Tex. Gov't Code Chapter 552.

Run: python3 scripts/build/build_tx_rules.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TX_RULES = [
    # Initial response
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'prompt_production',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.221',
        'notes': 'A governmental body that has access to requested public information must promptly produce it for inspection, duplication, or both. "Promptly" is the operative standard — there is no fixed day count for production of information the government body does not intend to withhold.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'days_to_request_ag_ruling',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.301(a)',
        'notes': 'If a governmental body believes requested information is excepted from required disclosure, it must request an Attorney General ruling within 10 business days of receiving the request. Failure to timely request a ruling results in a waiver of the right to withhold, and the information must be disclosed.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'days_to_notify_requester_of_ag_referral',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.301(b)',
        'notes': 'The governmental body must notify the requestor in writing within 10 business days of receiving the request that it is requesting an AG ruling. This notice must inform the requester of the right to submit written arguments to the AG about whether the information should be disclosed.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'constructive_waiver',
        'param_value': 'failure_to_timely_request_ruling',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.302',
        'notes': 'If a governmental body fails to timely request an AG ruling (within 10 business days), it is presumed to have waived the right to withhold the information and must release it. This is one of the strictest consequences in TPIA — there is no cure for a missed deadline.',
    },
    # AG ruling process
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'ag_ruling_deadline_days',
        'param_value': '45',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.306',
        'notes': 'The AG must issue an open records ruling within 45 business days of receiving the request for ruling. The AG may request additional time from the governmental body if needed. Failure by the AG to issue a ruling within the 45-day period is treated as a determination that the information is public.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'submission_of_written_comments',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.304',
        'notes': 'A requestor may submit written comments to the AG stating why the information should be disclosed, within 15 business days of receiving notice that the governmental body has requested an AG ruling. The AG must consider these comments in making its determination.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'third_party_submission',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.305',
        'notes': 'A third party whose records are the subject of the request (e.g., a private company whose submitted documents are sought) may submit written comments to the AG within 15 business days of notice. The AG considers both the requester\'s and third party\'s arguments.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'governmental_body_submission_deadline',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'Tex. Gov\'t Code § 552.301(e)',
        'notes': 'When requesting an AG ruling, the governmental body must submit to the AG: (1) a signed statement of why the information is excepted, (2) a copy of the requested information or a representative sample, and (3) a copy of the written request. Submission is due within 15 business days of the original records request.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'binding_effect',
        'param_value': 'binding_on_governmental_body',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.011',
        'notes': 'AG open records rulings are binding on governmental bodies. A governmental body that disagrees with a ruling must either comply or seek judicial relief. Previous AG determinations are persuasive precedent in subsequent requests for similar records by the same or different agencies.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'ag_ruling',
        'param_key': 'appeal_of_adverse_ag_ruling',
        'param_value': 'file_declaratory_judgment_within_30_calendar_days',
        'day_type': 'calendar',
        'statute_citation': 'Tex. Gov\'t Code § 552.324',
        'notes': 'A governmental body that disagrees with an AG ruling requiring disclosure must file suit in Travis County district court within 30 calendar days of the ruling, or within 30 days of the requester filing suit if the requester acts first. The AG is not a party to the suit; the dispute is between the governmental body and the requestor.',
    },
    # No administrative appeal — direct routes
    {
        'jurisdiction': 'TX',
        'rule_type': 'appeal_deadline',
        'param_key': 'no_administrative_appeal',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.321',
        'notes': 'Unlike FOIA, the TPIA does not have an internal administrative appeal process. A requestor who is denied access (or who disagrees with a decision not to seek an AG ruling) goes directly to the AG for a ruling or to court. There is no agency-level appeal to exhaust before pursuing remedies.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'appeal_deadline',
        'param_key': 'requestor_suit_for_writ_of_mandamus',
        'param_value': 'after_ag_ruling_favorable_to_requester',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.321',
        'notes': 'A requestor may sue for a writ of mandamus to compel disclosure if: (1) the governmental body refuses to release information after a favorable AG ruling, or (2) the governmental body fails to request an AG ruling and refuses to disclose. Venue is in Travis County or the county where the governmental body is located.',
    },
    # Judicial review
    {
        'jurisdiction': 'TX',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'venue_for_suit',
        'param_value': 'Travis_County_or_county_where_governmental_body_is_located',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.321(b)',
        'notes': 'Suits for mandamus to compel disclosure are filed in district court in Travis County, or in the county in which the main offices of the governmental body are located. This differs from federal FOIA, which requires suit in specific district courts.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorney_fees_if_requestor_prevails',
        'param_value': 'mandatory',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.323',
        'notes': 'If a requestor substantially prevails in litigation to compel disclosure, the court shall award the requestor reasonable attorney\'s fees and court costs. This fee-shifting provision is mandatory ("shall"), not discretionary ("may"), which creates a significant incentive for governmental bodies to comply voluntarily.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'standard_of_review',
        'param_value': 'de_novo',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.324',
        'notes': 'Courts review TPIA disclosure disputes de novo, without deference to the AG\'s ruling. The AG ruling is persuasive but not binding on the court. The governmental body bears the burden of demonstrating that the exception applies.',
    },
    # Criminal penalties
    {
        'jurisdiction': 'TX',
        'rule_type': 'penalty',
        'param_key': 'criminal_penalty_knowing_violation',
        'param_value': 'class_b_misdemeanor',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.352',
        'notes': 'An officer or employee of a governmental body who distributes information that is confidential under the TPIA, or who knowingly refuses to release information that is public, commits a Class B misdemeanor (punishable by up to 180 days in county jail and/or a fine up to $2,000). This is one of the few public records laws in the country with criminal enforcement against officers who withhold.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_destruction_of_records',
        'param_value': 'up_to_10000_per_violation',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.353',
        'notes': 'A person who destroys, mutilates, removes, or conceals public information that is subject to disclosure is liable for a civil penalty of up to $10,000 per violation. The AG may bring suit to collect the civil penalty.',
    },
    # Fee rules
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_cap',
        'param_key': 'labor_per_hour',
        'param_value': '15.00',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.261; 1 Tex. Admin. Code § 70.3',
        'notes': 'Personnel costs for locating records: $15 per hour for the first 50 pages; $10 per hour thereafter. These rates are set by the Office of the Attorney General in open records rules. Standard personnel rates apply to both clerical and professional time.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_standard',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': '1 Tex. Admin. Code § 70.3',
        'notes': 'Standard paper copy rate is $0.10 per page for letter or legal size copies. Other sizes and media (microfiche, photographs, CD, etc.) have separate rates prescribed in the OAG\'s open records rules. Agencies cannot charge above the OAG-established rates.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_cap',
        'param_key': 'no_fee_threshold',
        'param_value': '40.00',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.267',
        'notes': 'A governmental body may waive fees when the charge does not exceed $40 total. The agency has discretion to waive fees under this threshold. This is not a mandatory waiver threshold — it is an administrative convenience provision.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_waiver',
        'param_key': 'indigency_waiver',
        'param_value': 'available_for_financial_hardship',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.267',
        'notes': 'A requestor who is indigent and cannot pay fees may be entitled to a fee waiver. The governmental body may require affidavit of indigency. This is a discretionary waiver; there is no absolute right to a fee waiver based on financial hardship under the TPIA.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_waiver',
        'param_key': 'news_media_fee_waiver',
        'param_value': 'not_available_as_statutory_right',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.267',
        'notes': 'Unlike FOIA, the TPIA does not have a statutory fee waiver for news media or requestors seeking records for public benefit. Fee waivers under TPIA are discretionary, based on financial hardship. However, some agencies may adopt policies providing preferred fee treatment for journalists.',
    },
    {
        'jurisdiction': 'TX',
        'rule_type': 'fee_cap',
        'param_key': 'cost_estimate_required_if_over_threshold',
        'param_value': '40.00',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.2615',
        'notes': 'If the estimated cost of complying with a request exceeds $40, the governmental body must provide a written itemized cost estimate to the requestor before proceeding. The requestor may then narrow the request or prepay. If the requester does not respond within 10 business days, the request is considered withdrawn.',
    },
    # Expedited processing
    {
        'jurisdiction': 'TX',
        'rule_type': 'expedited_processing',
        'param_key': 'no_formal_expedited_process',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.221',
        'notes': 'Unlike FOIA, the TPIA does not have a formal expedited processing mechanism. However, the "promptly" standard applies to all requests, and the AG has stated that governmental bodies should prioritize requests where delay would result in harm. In urgent circumstances, a requestor may seek emergency injunctive relief in district court.',
    },
    # Electronic records
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_format',
        'param_value': 'must_provide_in_requested_format_if_readily_available',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.228',
        'notes': 'A governmental body shall provide a copy of public information in an electronic format if the information is maintained in an electronic format and can readily be converted. If the governmental body uses software to produce the information in the requested format, it may charge for the cost of the software.',
    },
    # Confidentiality protection
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'third_party_notice_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.305',
        'notes': 'Before releasing information that relates to a third party (e.g., a private company that submitted records to the government), the governmental body must notify the third party of the request and give them an opportunity to submit arguments to the AG about whether the information qualifies for an exception. This is similar in purpose to the federal submitter notice rule under E.O. 12600.',
    },
    # Open records request — no written request required
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'written_request_required',
        'param_value': 'false_oral_requests_accepted',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.221',
        'notes': 'The TPIA does not require a written request — a governmental body that possesses public information and is asked for it must provide it promptly. However, a written request is strongly recommended to create a record of the date of the request (triggering the 10-business-day AG-ruling deadline) and to document the information sought.',
    },
    # Duty to identify responsive records
    {
        'jurisdiction': 'TX',
        'rule_type': 'initial_response',
        'param_key': 'duty_to_identify_responsive_records',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Tex. Gov\'t Code § 552.222',
        'notes': 'A governmental body that receives a request for information must make a good-faith effort to determine whether it has responsive records. It may ask a requestor to clarify an unclear request, but may not use the need for clarification as a basis to delay or deny disclosure. If the body identifies non-responsive records, it should inform the requestor.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for rule in TX_RULES:
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
    print(f'Texas TPIA response rules: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_tx_rules', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
