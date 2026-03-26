#!/usr/bin/env python3
"""Build California Public Records Act (CPRA) request templates.

Model request language for common record types under Cal. Gov. Code
§§ 7920-7931 (as renumbered effective January 1, 2023). Includes the
new post-2023 section citations alongside legacy § 6250-6270 cross-refs
to help requesters dealing with agencies or staff who use the old numbering.

Run: python3 scripts/build/build_ca_templates.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

CA_TEMPLATES = [
    {
        'jurisdiction': 'CA',
        'record_type': 'general',
        'template_name': 'General California CPRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Act Coordinator / City Clerk / Records Officer
{{agency_name}}
{{agency_address}}

Re: California Public Records Act Request

Dear Records Officer:

Pursuant to the California Public Records Act (Gov. Code § 7920.000 et seq., formerly § 6250 et seq.), I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in locating the records, I provide the following additional context:
{{additional_context}}

Under Gov. Code § 7922.530, I understand fees may be charged only for the direct cost of duplication — not for search, review, or redaction time. I am willing to pay duplication fees up to a maximum of ${{fee_limit}}. Please notify me before incurring costs above this amount.

If any records are withheld in whole or in part, please cite the specific exemption(s) under Gov. Code § 7920.000 et seq. that you believe apply, and provide a description of the withheld records sufficient to evaluate the exemption claim. Please also disclose all reasonably segregable, non-exempt portions of any partially exempt records (Gov. Code § 7922.525).

I would prefer to receive responsive records in electronic format (PDF or native format) by email to {{requester_email}}.

Under Gov. Code § 7922.535, you must notify me within 10 calendar days whether you will comply with this request. If you require additional time under the unusual circumstances extension (Gov. Code § 7922.535(b)), please notify me in writing within that 10-day period.

If you need clarification to locate the records, please contact me promptly so we can narrow or refine the request.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'General-purpose California CPRA template using post-2023 Gov. Code citations (§ 7920 series). Note: California law does not provide for a formal "fee waiver" mechanism like federal FOIA — fees are simply limited to direct duplication costs under § 7922.530. There is no public interest fee waiver provision in the CPRA.',
    },
    {
        'jurisdiction': 'CA',
        'record_type': 'police_records',
        'template_name': 'California CPRA - Law Enforcement Records (SB 1421 / AB 748)',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Act Coordinator / Records Bureau
{{agency_name}} (Police Department / Sheriff's Department)
{{agency_address}}

Re: California Public Records Act Request — Peace Officer Records and Use-of-Force Materials

Dear Records Officer:

Pursuant to the California Public Records Act (Gov. Code § 7920.000 et seq.) and California Penal Code § 832.7 (as amended by SB 1421 (2019) and AB 748 (2019)), I request the following records:

{{description_of_records}}

Specifically, I request all records relating to: {{subject_or_incident}}

Date range: {{date_range_start}} through {{date_range_end}}

STATUTORY BASIS

Under Penal Code § 832.7(b)(1), the following categories of records are expressly public and may NOT be withheld under the law enforcement investigatory exemption (Gov. Code § 7923.600) or any other CPRA exemption:

(A) Records relating to an incident in which a peace officer or custodial officer discharged a firearm at a person.

(B) Records relating to an incident in which the use of force by a peace officer or custodial officer resulted in death or great bodily injury.

(C) Records relating to a sustained finding that a peace officer or custodial officer engaged in sexual assault involving a member of the public.

(D) Records relating to a sustained finding of dishonesty by a peace officer or custodial officer directly relating to the reporting, investigation, or prosecution of a crime, or directly relating to the reporting of, or investigation of misconduct by, another peace officer or custodial officer.

If any of the records I am requesting fall within categories (A) through (D) above, they are categorically public under Penal Code § 832.7 and must be produced regardless of any claimed exemption.

For records not within those categories, I request that you:
1. Review each record individually rather than applying a blanket exemption;
2. Identify the specific exemption by Gov. Code section number for any withheld record;
3. Disclose all reasonably segregable non-exempt portions (Gov. Code § 7922.525);
4. Provide a description of any withheld records sufficient for me to evaluate the exemption.

BODY-WORN CAMERA / VIDEO FOOTAGE

Under Penal Code § 832.7(b)(2), any video or audio recording of an incident covered by § 832.7(b)(1) must be disclosed within 45 calendar days of the incident, unless an ongoing criminal investigation is directly compromised. If disclosure is delayed under this provision, please state so in writing and specify the earliest date by which the recording will be released.

FEES

Under Gov. Code § 7922.530, fees may only cover the direct cost of duplication. I am willing to pay up to ${{fee_limit}} for this request.

Please respond within 10 calendar days as required by Gov. Code § 7922.535.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': '''I request prompt processing of this request. The records relate to a matter of immediate public concern involving {{urgency_description}}. The 10-day response deadline under Gov. Code § 7922.535 is binding, and I ask that you prioritize locating and producing these records within that window.''',
        'notes': 'Template for peace officer records under SB 1421 (Penal Code § 832.7). Agencies frequently attempt to invoke the law enforcement investigatory exemption (Gov. Code § 7923.600) to shield records that are expressly public under § 832.7 — this template preemptively addresses those arguments. Also covers AB 748 body camera footage requirements.',
    },
    {
        'jurisdiction': 'CA',
        'record_type': 'general',
        'template_name': 'California CPRA - Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Act Coordinator
{{agency_name}}
{{agency_address}}

Re: California Public Records Act Request — Contracts, Expenditures, and Vendor Records

Dear Records Officer:

Pursuant to the California Public Records Act (Gov. Code § 7920.000 et seq.), I request copies of the following records relating to government contracts and public expenditures:

1. All contracts, agreements, and amendments between {{agency_name}} and {{contractor_or_vendor_name}} for the period {{date_range_start}} through {{date_range_end}};

2. All invoices, payment records, and purchase orders related to the above contracts;

3. All requests for proposals (RFPs), requests for qualifications (RFQs), and bid solicitations issued by {{agency_name}} related to {{subject_matter}} during the same period;

4. All bid responses and proposals received in response to the above solicitations;

5. All contract monitoring, audit, or performance review records for the above contracts;

6. All correspondence between {{agency_name}} and {{contractor_or_vendor_name}} regarding contract performance, disputes, or modifications.

APPLICABLE LAW

Government contracts represent expenditure of public funds and are matters of public interest. The CPRA broadly defines "public records" to include all records "relating to the conduct of the public's business" (Gov. Code § 7920.530). Contract documents, invoices, and financial records clearly fall within this definition.

Note that trade secret claims by contractors (Gov. Code § 7924.510) must be evaluated by the agency independently — a contractor's assertion that contract terms are proprietary does not bind the agency and does not relieve it of its disclosure obligations without a genuine showing of competitive harm.

FEES

Under Gov. Code § 7922.530, fees are limited to the direct cost of duplication only. I am willing to pay up to ${{fee_limit}}.

Please respond within 10 calendar days (Gov. Code § 7922.535). If you need clarification to locate the records, please contact me promptly.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for government contracts and spending records. Directly addresses common trade secret overclaiming by contractors. Invoices and payment amounts are consistently held public under the CPRA regardless of contract confidentiality clauses between the agency and vendor.',
    },
    {
        'jurisdiction': 'CA',
        'record_type': 'emails',
        'template_name': 'California CPRA - Email and Electronic Communications',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Act Coordinator
{{agency_name}}
{{agency_address}}

Re: California Public Records Act Request — Email and Electronic Communications

Dear Records Officer:

Pursuant to the California Public Records Act (Gov. Code § 7920.000 et seq.), I request copies of all email and electronic communications meeting the following criteria:

1. To or from: {{officials_or_offices}} (titles and/or names)
2. Date range: {{date_range_start}} through {{date_range_end}}
3. Relating to or containing any of the following terms or subjects: {{search_terms}}

This request includes communications on all government-managed systems and accounts. Under the California Supreme Court's holding in City of San Jose v. Superior Court (2017) 2 Cal.5th 608, communications by public officials on personal devices or accounts that relate to the conduct of public business are public records subject to the CPRA, even if sent on personal email accounts. This request therefore includes:

- Communications on agency email systems ({{agency_domain}});
- Any communications on personal email accounts (Gmail, Yahoo, etc.) or personal devices by the above officials that relate to the conduct of public business, to the extent the agency is able to locate and retrieve them.

ELECTRONIC FORMAT

Under Gov. Code § 7922.545 (formerly § 6253.9), I request that records be provided in electronic format (native email format or PDF). If native email format is available, please provide it in that format. For emails, the metadata (sender, recipient, date, subject line) must be preserved.

REDACTION AND SEGREGABILITY

If any communications are withheld or partially redacted, please: (1) cite the specific statutory exemption by Gov. Code section number; (2) provide a description of the withheld communication sufficient to evaluate the exemption; and (3) disclose all non-exempt portions (Gov. Code § 7922.525).

FEES

Fees are limited to direct duplication costs only under Gov. Code § 7922.530. I am willing to pay up to ${{fee_limit}}. Please do not charge for search, review, or attorney time.

Please respond within 10 calendar days as required by Gov. Code § 7922.535.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for email communications. Cites City of San Jose v. Superior Court (2017) which extended CPRA to personal device/account communications about public business. Agencies frequently attempt to resist producing personal device communications — this template establishes the legal basis upfront.',
    },
    {
        'jurisdiction': 'CA',
        'record_type': 'appeal',
        'template_name': 'California CPRA - Petition for Writ of Mandate (Complaint Template)',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Superior Court of California
County of {{county}}
{{court_address}}

Re: Petition for Writ of Mandate — California Public Records Act
    {{agency_name}} — Request dated {{original_request_date}}

[CAPTION]

{{requester_name}}, Petitioner,
v.
{{agency_name}}, Respondent.

Case No.: [To be assigned]

VERIFIED PETITION FOR WRIT OF MANDATE
(Cal. Gov. Code § 7923.000; Code of Civil Procedure § 1085)

Petitioner {{requester_name}} alleges as follows:

INTRODUCTION

This is an action under the California Public Records Act (Gov. Code § 7920.000 et seq.) to compel {{agency_name}} to disclose public records it has unlawfully withheld.

PARTIES

1. Petitioner {{requester_name}} is a [person/journalist/organization] located at {{requester_address}}.

2. Respondent {{agency_name}} is a public agency within the meaning of Gov. Code § 7920.530, located at {{agency_address}}.

FACTS

3. On {{original_request_date}}, Petitioner submitted a CPRA request to Respondent seeking: {{brief_description_of_records}}.

4. [CHOOSE ONE:]
   (a) Respondent failed to respond within 10 calendar days as required by Gov. Code § 7922.535, constituting a constructive denial; OR
   (b) On {{response_date}}, Respondent denied the request, citing {{exemption_cited}}.

5. The requested records are public records within the meaning of Gov. Code § 7920.530 because {{public_records_argument}}.

LEGAL ARGUMENT

6. {{agency_name}} bears the burden of demonstrating that the requested records fall within a specific exemption (Gov. Code § 7923.000). It has not and cannot meet this burden because:

{{exemption_challenge_arguments}}

7. The requested records are not subject to any applicable exemption because: {{additional_arguments}}

8. Under Gov. Code § 7922.525, even if some portions of the records were exempt, Respondent is required to segregate and produce the non-exempt portions.

PRAYER FOR RELIEF

Petitioner requests that this Court:

1. Issue a peremptory writ of mandate directing {{agency_name}} to immediately disclose and produce the requested records;

2. Award Petitioner attorney's fees and costs pursuant to Gov. Code § 7923.115;

3. Grant such other and further relief as the Court deems proper.

Dated: {{date}}

Respectfully submitted,
{{requester_name}} [or Counsel for Petitioner]
{{requester_address}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template/guide for CPRA writ of mandate petition. IMPORTANT: California CPRA does NOT require administrative appeal — requesters may go directly to superior court after any denial or constructive denial (Gov. Code § 7923.000). This template is a starting point only; actual litigation requires an attorney or careful pro se preparation. The attorney\'s fees provision (§ 7923.115) is a significant leverage tool.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for template in CA_TEMPLATES:
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
    print(f'CA CPRA templates: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_ca_templates', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
