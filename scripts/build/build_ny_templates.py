#!/usr/bin/env python3
"""Build New York FOIL request templates.

Model request language for common record types under New York's
Freedom of Information Law, Public Officers Law §§ 84-90.

Run: python3 scripts/build/build_ny_templates.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

NY_TEMPLATES = [
    {
        'jurisdiction': 'NY',
        'record_type': 'general',
        'template_name': 'General New York FOIL Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Law Request

Dear Records Access Officer:

Pursuant to the New York Freedom of Information Law (FOIL), Public Officers Law §§ 84-90, I hereby request access to and copies of the following records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I offer the following additional information:
{{additional_context}}

I request that records be produced in electronic format (PDF or native format) where available, to minimize duplication costs.

I am willing to pay copying fees up to ${{fee_limit}}. If you estimate that fees will exceed this amount, please notify me before processing so I may narrow or prioritize my request.

If any portion of this request is denied, I ask that you: (1) identify each record withheld and the specific FOIL exemption(s) claimed for each; (2) release all reasonably segregable, non-exempt portions of any partially exempt records, pursuant to Public Officers Law § 89(2)(a); and (3) provide a written explanation sufficient for me to file an informed appeal.

I look forward to your acknowledgment within 5 business days and a determination within 20 business days, as required by Public Officers Law § 89(3)(a).

If you have questions about this request, please contact me at {{requester_email}} or {{requester_phone}}.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that the agency waive or reduce any fees associated with this request. Although FOIL does not provide a statutory fee waiver, I ask that the agency exercise its discretion to waive fees because disclosure of these records serves the public interest.

Specifically, the requested records will contribute to public understanding of {{public_interest_explanation}}. I am {{requester_category_description}}, and I intend to share the information with the public through {{dissemination_method}}.

The copying fee cap of $0.25 per page under Public Officers Law § 87(1)(b)(iii) provides some protection, but a full waiver would best serve the public interest here.''',
        'expedited_language': '''I request that this FOIL request be processed on an expedited basis. Although FOIL does not contain a statutory expedited processing provision, I ask that the agency act promptly because:

{{expedited_justification}}

Specifically, I need these records by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

I appreciate your prompt attention to this urgent request.''',
        'notes': 'General-purpose NY FOIL template. Suitable for most state and local agencies. Uses correct NY statutory citations and terminology (Records Access Officer, not FOIA Officer).',
    },
    {
        'jurisdiction': 'NY',
        'record_type': 'police_records',
        'template_name': 'New York FOIL - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Law Request — Law Enforcement Records

Dear Records Access Officer:

Pursuant to the New York Freedom of Information Law (FOIL), Public Officers Law §§ 84-90, I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and complaint reports
- Arrest records and booking information
- Use-of-force reports
- Disciplinary records
- Body-worn camera footage (if applicable)
- Any other records relating to the above

I understand that certain law enforcement records may be subject to exemptions under Public Officers Law § 87(2)(e). However, I request that the agency: (1) review each responsive record individually rather than applying a blanket exemption; (2) release all reasonably segregable non-exempt portions of any partially exempt records under § 89(2)(a); (3) provide a specific written explanation for each withholding, identifying the subsection of § 87(2)(e) relied upon; and (4) explain why the public interest in disclosure does not outweigh the claimed harm.

Note: Completed criminal proceedings reduce or eliminate the basis for withholding under § 87(2)(e)(i) (interference with pending proceedings). If any proceedings referenced in these records have concluded, please apply the reduced standard accordingly.

I am willing to pay copying fees up to ${{fee_limit}}.

Please provide records in electronic format where available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that the agency waive copying fees. These records relate to {{public_interest_explanation}}, a matter of significant public concern. Disclosure will contribute to public accountability and understanding of law enforcement activity affecting the community.''',
        'expedited_language': None,
        'notes': 'Template for law enforcement records from NYPD, county sheriffs, state police, and similar agencies. Includes preemptive language about segregability and the effect of concluded proceedings on § 87(2)(e)(i) claims.',
    },
    {
        'jurisdiction': 'NY',
        'record_type': 'personnel_records',
        'template_name': 'New York FOIL - Public Employee Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Law Request — Public Employee Records

Dear Records Access Officer:

Pursuant to the New York Freedom of Information Law (FOIL), Public Officers Law §§ 84-90, I request copies of records relating to the following public employee(s) or position(s):

Employee name / position: {{employee_name_or_position}}
Agency / department: {{department}}
Date range: {{date_range_start}} through {{date_range_end}}

Specifically, I request:
{{description_of_records}}

This request includes, but is not limited to: salary, title, and compensation records; job duties and responsibilities; disciplinary records and findings; performance evaluations (final determinations); and records of official conduct.

Note on Privacy: The Committee on Open Government and New York courts have consistently held that public employees have reduced privacy interests in records relating to their official duties, compensation, and professional conduct. See, e.g., Matter of Gould v. New York City Police Dept., 89 N.Y.2d 267 (1996). Salary and title information is not exempt from disclosure. Final disciplinary determinations are generally disclosable. I ask that the agency apply these standards and not apply the privacy exemption to records of official public conduct.

If any records are withheld, please identify the specific FOIL exemption relied upon for each withheld record and release all reasonably segregable non-exempt portions.

I am willing to pay copying fees up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for requests targeting public employee records — salaries, conduct, discipline. Includes COOG and Gould citation to preempt overbroad privacy objections.',
    },
    {
        'jurisdiction': 'NY',
        'record_type': 'contracts',
        'template_name': 'New York FOIL - Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Law Request — Government Contracts and Procurement

Dear Records Access Officer:

Pursuant to the New York Freedom of Information Law (FOIL), Public Officers Law §§ 84-90, I request copies of the following records related to government contracts and procurement:

1. The complete contract (including all amendments, modifications, and task orders) for: {{contract_description}}
2. Contract number (if known): {{contract_number}}
3. Contractor name (if known): {{contractor_name}}
4. All bid or proposal submissions received
5. Bid evaluation records and scoring sheets
6. All invoices, payment records, and vouchers
7. Any performance evaluations or audits
8. Communications between agency staff and the contractor relating to contract performance

Date range: {{date_range_start}} through {{date_range_end}}.

Note on Trade Secrets: If the agency intends to claim that any contractor-submitted information is protected by the trade secret exemption under Public Officers Law § 87(2)(d), I ask that the agency: (1) make its own independent determination of exempt status rather than deferring to the contractor's claims; (2) demonstrate that disclosure would cause substantial competitive injury, not merely inconvenience; and (3) release all portions of the contract that reflect the expenditure of public funds, which are not protectable as trade secrets. See Encore College Bookstores, Inc. v. Auxiliary Service Corp., 87 N.Y.2d 410 (1995).

I am willing to pay copying fees up to ${{fee_limit}}.

Please provide records in electronic format where available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. Government contracts represent the expenditure of public funds, and these records are of direct public interest. Disclosure will contribute to public understanding of how taxpayer money is being spent.''',
        'expedited_language': None,
        'notes': 'Template for government contract records. Includes preemptive language challenging trade secret claims and citing Encore College Bookstores.',
    },
    {
        'jurisdiction': 'NY',
        'record_type': 'appeal',
        'template_name': 'New York FOIL Administrative Appeal',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Head of Agency / Appeals Officer
{{agency_name}}
{{agency_address}}

Re: FOIL Appeal — Request dated {{original_request_date}} / Reference No. {{request_number}}

Dear {{appeals_officer_title}}:

Pursuant to Public Officers Law § 89(4)(a), I am appealing the {{denial_type}} of my Freedom of Information Law request dated {{original_request_date}}, reference number {{request_number}}. The agency's response was dated {{response_date}}.

BACKGROUND

On {{original_request_date}}, I submitted a FOIL request to {{agency_name}} for {{brief_description_of_records}}. On {{response_date}}, the agency {{description_of_denial}}.

GROUNDS FOR APPEAL

{{appeal_arguments}}

Specifically, the agency's reliance on {{exemption_cited}} is misplaced for the following reasons:

{{exemption_challenge_arguments}}

ADDITIONAL GROUNDS

{{additional_grounds}}

CONCLUSION

For the foregoing reasons, I respectfully request that you reverse the initial determination and grant access to the requested records in full. In the alternative, I ask that you release all reasonably segregable non-exempt portions pursuant to Public Officers Law § 89(2)(a), and provide a specific written explanation for any continued withholding identifying the precise FOIL exemption relied upon for each withheld record.

If you deny this appeal, please provide a written explanation with sufficient specificity to permit judicial review.

I look forward to your response within 10 business days as required by Public Officers Law § 89(4)(a).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for FOIL administrative appeal. Must be filed within 30 calendar days of the denial. The appeal arguments and exemption challenge sections should be populated using the exemptions catalog and COOG advisory opinions. Agency must respond within 10 business days.',
    },
    {
        'jurisdiction': 'NY',
        'record_type': 'electronic_records',
        'template_name': 'New York FOIL - Electronic Records and Data',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Law Request — Electronic Records

Dear Records Access Officer:

Pursuant to the New York Freedom of Information Law (FOIL), Public Officers Law §§ 84-90, I request copies of the following electronic records:

{{description_of_records}}

Date range: {{date_range_start}} through {{date_range_end}}.

FORMAT REQUEST: I request that records be provided in their native electronic format, or as machine-readable data (e.g., CSV, JSON, or Excel) where the underlying data exists in a structured format. Under Public Officers Law § 87(1)(b)(iii), the agency may only charge the actual cost of the electronic medium, not programming or staff time for records that already exist in the agency's systems.

If the records exist in a database or data system, I request the data in a structured, machine-readable format rather than printed paper copies or static PDFs, as the data is more useful and the cost of production is lower.

This request includes:
- All electronic records matching the criteria above, including emails, spreadsheets, databases, and documents in any file format
- Metadata sufficient to authenticate the records (creation date, modification date, author)
- Any records maintained on portable devices or personal accounts used for official business

I am willing to pay the actual cost of the electronic medium (e.g., a USB drive) but not programming fees for records that already exist in retrievable form.

If any records are withheld, please identify the specific FOIL exemption for each withheld record and release all reasonably segregable non-exempt portions.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that the agency provide records electronically at no charge, or at the cost of the electronic medium only, pursuant to Public Officers Law § 87(1)(b)(iii). Providing records in electronic format costs the agency nothing beyond the medium, and charging full duplication fees for electronic records would be inconsistent with FOIL's policy of maximum disclosure.''',
        'expedited_language': None,
        'notes': 'Template for requesting electronic records, databases, and structured data. Emphasizes the electronic records fee limitation and machine-readable format preference. Useful for data journalism and systematic research requests.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for template in NY_TEMPLATES:
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
    print(f'NY FOIL templates: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ny_templates', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
