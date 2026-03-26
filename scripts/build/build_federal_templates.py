#!/usr/bin/env python3
"""Build federal FOIA request templates.

Model request language for common record types, fee waiver language,
and expedited processing language.

Run: python3 scripts/build/build_federal_templates.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

FEDERAL_TEMPLATES = [
    {
        'jurisdiction': 'federal',
        'record_type': 'general',
        'template_name': 'General Federal FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request

Dear FOIA Officer:

Pursuant to the Freedom of Information Act (FOIA), 5 U.S.C. § 552, I hereby request access to and copies of the following records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To help identify the records I am seeking, I offer the following additional information:
{{additional_context}}

I am willing to pay fees for this request up to a maximum of ${{fee_limit}}. If you estimate that the fees will exceed this limit, please inform me first.

{{fee_waiver_paragraph}}

If my request is denied in whole or in part, I ask that you justify all deletions by reference to specific exemptions of the FOIA. I also request that you release all segregable portions of otherwise exempt material.

I would prefer to receive records in electronic format (PDF) if available.

I look forward to your response within 20 business days, as required by law. If you have any questions about this request, please contact me at {{requester_email}} or {{requester_phone}}.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver of all fees for this request. Disclosure of the requested information is in the public interest because it is likely to contribute significantly to public understanding of the operations or activities of the government and is not primarily in my commercial interest.

Specifically, the requested records will shed light on {{public_interest_explanation}}. I plan to disseminate the information to the public through {{dissemination_method}}.

I am {{requester_category_description}}, and I have no commercial interest in the requested information.''',
        'expedited_language': '''I request expedited processing of this FOIA request pursuant to 5 U.S.C. § 552(a)(6)(E).

{{expedited_justification}}

I certify that the above statements are true and correct to the best of my knowledge and belief.''',
        'notes': 'General-purpose federal FOIA template. Suitable for most agencies.',
    },
    {
        'jurisdiction': 'federal',
        'record_type': 'emails',
        'template_name': 'Federal FOIA - Email Communications',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Email Communications

Dear FOIA Officer:

Pursuant to the Freedom of Information Act (FOIA), 5 U.S.C. § 552, I request copies of all email communications meeting the following criteria:

1. Sent to or from: {{officials_or_offices}}
2. Date range: {{date_range_start}} through {{date_range_end}}
3. Containing any of the following terms or relating to the following subjects: {{search_terms}}

This request includes emails on all government email systems and accounts, including any official communications conducted on personal devices or accounts in accordance with the Federal Records Act.

I am willing to pay fees up to ${{fee_limit}}. Please inform me if costs will exceed this amount.

{{fee_waiver_paragraph}}

I request records in electronic format (native email format or PDF). If any records are withheld, please provide a Vaughn index identifying each withheld record and the exemption claimed.

Thank you for your prompt attention to this request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver pursuant to 5 U.S.C. § 552(a)(4)(A)(iii). The requested communications will illuminate government decision-making regarding {{topic}}, which is a matter of significant public interest.''',
        'expedited_language': None,
        'notes': 'Template for requesting email communications from federal officials.',
    },
    {
        'jurisdiction': 'federal',
        'record_type': 'contracts',
        'template_name': 'Federal FOIA - Government Contracts',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Government Contracts

Dear FOIA Officer:

Pursuant to the Freedom of Information Act (FOIA), 5 U.S.C. § 552, I request copies of the following records related to government contracts:

1. The complete contract, including all modifications and amendments, for: {{contract_description}}
2. Contract number (if known): {{contract_number}}
3. Contractor name (if known): {{contractor_name}}
4. All task orders issued under this contract
5. All performance evaluations or contractor performance assessment reports
6. All invoices and payment records

Date range: {{date_range_start}} through {{date_range_end}}.

Note: Government contracts and contractor proposals that have been incorporated into contracts are generally not protected by Exemption 4 (trade secrets). See, e.g., Public Citizen v. Dep't of Defense (D.C. Cir. 2014).

I am willing to pay reasonable fees for this request up to ${{fee_limit}}.

{{fee_waiver_paragraph}}

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. Government contracts represent expenditure of public funds and are matters of inherent public interest. Disclosure will contribute to public understanding of how taxpayer dollars are being spent.''',
        'expedited_language': None,
        'notes': 'Template for requesting government contract records.',
    },
    {
        'jurisdiction': 'federal',
        'record_type': 'police_records',
        'template_name': 'Federal FOIA - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records

Dear FOIA Officer:

Pursuant to the Freedom of Information Act (FOIA), 5 U.S.C. § 552, I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}

I understand that certain law enforcement records may be subject to Exemption 7 of FOIA. However, I request that you: (1) review each responsive record individually rather than applying a blanket exemption; (2) release all non-exempt portions of partially exempt records (segregability); and (3) provide a detailed justification citing the specific sub-exemption (7A through 7F) for each withholding.

I am willing to pay fees up to ${{fee_limit}}.

{{fee_waiver_paragraph}}

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. The requested records relate to law enforcement activity that is a matter of significant public concern. Disclosure will contribute to public understanding of {{public_interest_explanation}}.''',
        'expedited_language': None,
        'notes': 'Template for law enforcement records. Includes preemptive language about Exemption 7 segregability.',
    },
    {
        'jurisdiction': 'federal',
        'record_type': 'appeal',
        'template_name': 'Federal FOIA Administrative Appeal',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Chief FOIA Officer / Appeals Authority
{{agency_name}}
{{agency_address}}

Re: FOIA Appeal — Request No. {{request_number}}, dated {{original_request_date}}

Dear Chief FOIA Officer:

I am writing to appeal the {{denial_type}} of my FOIA request, reference number {{request_number}}, dated {{original_request_date}}. The agency's response was dated {{response_date}}.

BACKGROUND

On {{original_request_date}}, I submitted a FOIA request for {{brief_description_of_records}}. On {{response_date}}, the agency {{description_of_denial}}.

GROUNDS FOR APPEAL

{{appeal_arguments}}

The agency's reliance on {{exemption_cited}} is misplaced for the following reasons:

{{exemption_challenge_arguments}}

CONCLUSION

For the foregoing reasons, I respectfully request that you reverse the initial determination and release the requested records in full. In the alternative, I request that you release all reasonably segregable non-exempt portions.

I also wish to note that I have the right to seek mediation services from the Office of Government Information Services (OGIS) at the National Archives and Records Administration as a non-exclusive alternative to litigation, pursuant to 5 U.S.C. § 552(h)(3).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'appeal_template': None,
        'notes': 'Template for administrative FOIA appeal. The appeal_arguments and exemption_challenge_arguments sections should be populated by the LLM using research from the exemptions catalog and case law corpus.',
    },
    {
        'jurisdiction': 'federal',
        'record_type': 'first_party',
        'template_name': 'Federal FOIA/Privacy Act - First Party Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA/Privacy Act Officer
{{agency_name}}
{{agency_address}}

Re: FOIA/Privacy Act Request for Records About Myself

Dear FOIA/Privacy Act Officer:

Pursuant to the Freedom of Information Act (5 U.S.C. § 552) and the Privacy Act of 1974 (5 U.S.C. § 552a), I request access to all records maintained by {{agency_name}} that pertain to me:

Name: {{requester_full_name}}
Date of Birth: {{requester_dob}}
Social Security Number (last 4): XXX-XX-{{requester_ssn_last4}}
Other identifying information: {{additional_identifiers}}

I am specifically requesting: {{description_of_records}}

For verification purposes, I have enclosed {{verification_documents}}.

As I am requesting records about myself, I understand that this request falls under both FOIA and the Privacy Act, and I request that you process it under whichever statute provides greater access to my records.

I request a fee waiver as this request is for records about myself and not for commercial purposes.

Sincerely,
{{requester_name}}

Enclosures: {{verification_documents}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Combined FOIA/Privacy Act request for records about the requester. Includes identity verification guidance.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for template in FEDERAL_TEMPLATES:
            existing = conn.execute(
                'SELECT id FROM request_templates WHERE jurisdiction = ? AND template_name = ?',
                (template['jurisdiction'], template['template_name'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE request_templates SET
                        record_type = ?, template_text = ?,
                        fee_waiver_language = ?, expedited_language = ?,
                        notes = ?, updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (template['record_type'], template['template_text'],
                     template.get('fee_waiver_language'), template.get('expedited_language'),
                     template.get('notes'), existing[0])
                )
                skipped += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO request_templates (
                        jurisdiction, record_type, template_name,
                        template_text, fee_waiver_language, expedited_language,
                        notes, source
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'prdb-built')
                    ''',
                    (template['jurisdiction'], template['record_type'],
                     template['template_name'], template['template_text'],
                     template.get('fee_waiver_language'), template.get('expedited_language'),
                     template.get('notes'))
                )
                added += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'Federal templates: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_federal_templates', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
