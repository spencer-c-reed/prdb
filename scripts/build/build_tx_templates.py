#!/usr/bin/env python3
"""Build Texas Public Information Act request templates.

Model request language for common record types under Tex. Gov't Code Chapter 552.
Includes fee estimate language, appeal language, and AG ruling request language.

Run: python3 scripts/build/build_tx_templates.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TX_TEMPLATES = [
    {
        'jurisdiction': 'TX',
        'record_type': 'general',
        'template_name': 'General Texas Public Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer / Public Information Officer
{{governmental_body_name}}
{{governmental_body_address}}

Re: Public Information Act Request — Texas Government Code Chapter 552

Dear Open Records Officer:

Pursuant to the Texas Public Information Act (TPIA), Tex. Gov't Code Chapter 552, I hereby request access to and copies of the following public information:

{{description_of_records}}

Time period: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested information, I provide the following additional context:
{{additional_context}}

I understand that if you believe any portion of the requested information is excepted from disclosure, you must request a ruling from the Texas Attorney General within 10 business days of receiving this request and notify me of that referral. See Tex. Gov't Code § 552.301.

I am willing to pay fees for this request up to a maximum of ${{fee_limit}}. If the cost will exceed this amount, please provide an itemized written estimate before proceeding, as required by Tex. Gov't Code § 552.2615. I reserve the right to narrow or modify the request upon receipt of the estimate.

I would prefer to receive records in electronic format (PDF or native format) if available.

If any records are withheld, please provide a written statement identifying each document withheld, the specific statutory exception claimed for each, and a brief explanation of why the exception applies.

I look forward to your prompt response as required by Tex. Gov't Code § 552.221.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver of fees for this request pursuant to Tex. Gov't Code § 552.267. I am unable to pay the estimated fees due to financial hardship. I have enclosed an affidavit of indigency as required. If you require additional documentation of financial hardship, please inform me promptly.

I note that the requested information is a matter of significant public interest and will be used for {{public_purpose_description}}, not for commercial purposes.''',
        'expedited_language': '''I am requesting prompt handling of this request due to the following circumstances:

{{urgency_explanation}}

While the TPIA does not have a formal expedited processing mechanism, Tex. Gov't Code § 552.221 requires that governmental bodies provide information "promptly." I ask that you prioritize this request accordingly. If expedited handling is not possible, please advise me of the expected timeline as soon as possible.''',
        'notes': 'General-purpose TPIA template. The key TPIA-specific element is the reminder about the 10-business-day AG ruling deadline. Unlike FOIA, there is no 20-day response deadline — the operative standard is "promptly." Suitable for most Texas state and local governmental bodies.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'law_enforcement',
        'template_name': 'Texas TPIA - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer / Custodian of Records
{{law_enforcement_agency_name}}
{{agency_address}}

Re: Public Information Act Request — Law Enforcement Records
    Tex. Gov't Code Chapter 552

Dear Custodian of Records:

Pursuant to the Texas Public Information Act, Tex. Gov't Code Chapter 552, I request copies of the following law enforcement records:

{{description_of_records}}

Subject/Incident: {{subject_or_incident_description}}
Date range: {{date_range_start}} through {{date_range_end}}
Case/Incident number (if known): {{case_or_incident_number}}

Specifically, I am requesting the following categories of records (as applicable):

1. All incident reports, offense reports, and supplemental reports related to the above
2. All dispatch records, call-for-service records, and CAD logs
3. All arrest records, booking records, and jail records
4. All evidence logs and chain of custody documentation
5. All use-of-force reports related to the incident or subject
6. All body camera and dashcam footage (to the extent maintained separately from criminal investigation files)
7. All internal affairs or professional standards records related to the above
8. All policies and procedures governing the conduct at issue

I understand that some records may be subject to exception under Tex. Gov't Code § 552.108 (law enforcement records). However, I ask that you:
(a) Review each responsive record individually rather than applying a blanket exception;
(b) Release all non-excepted portions of partially excepted records;
(c) If you request an AG ruling, identify specifically which sub-provision of § 552.108 applies to each withheld record.

Please note that basic incident/offense reports are generally public information under Texas law and should be disclosed without an AG ruling. See, e.g., Houston Chronicle v. City of Houston, 531 S.W.2d 177 (Tex. Civ. App. 1975).

I am willing to pay fees up to ${{fee_limit}}. Please provide an itemized cost estimate if fees will exceed $40.

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver under Tex. Gov't Code § 552.267. The requested law enforcement records relate to matters of significant public concern — specifically, {{public_interest_explanation}} — and will not be used for commercial purposes. If a fee waiver based on public interest is not available under TPIA, I request that you waive fees under your agency's discretionary fee waiver authority given the importance of this request to the public interest.''',
        'expedited_language': None,
        'notes': 'Template for requesting law enforcement records from Texas police departments, sheriffs\' offices, and other law enforcement agencies. Includes preemptive language about § 552.108 and the established rule that offense reports are generally public. Note that body camera footage is subject to specific regulations under Tex. Occ. Code Chapter 1701, which may require separate requests.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'contracts',
        'template_name': 'Texas TPIA - Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{governmental_body_name}}
{{governmental_body_address}}

Re: Public Information Act Request — Government Contracts
    Tex. Gov't Code Chapter 552

Dear Open Records Officer:

Pursuant to the Texas Public Information Act, Tex. Gov't Code Chapter 552, I request copies of the following records relating to government contracts and procurement:

1. The complete executed contract, including all attachments, exhibits, and incorporated documents, for: {{contract_description}}
2. Contract number (if known): {{contract_number}}
3. Contractor/vendor name: {{contractor_name}}
4. All amendments, modifications, and change orders to the contract
5. All task orders or work orders issued under the contract
6. All invoices submitted by the contractor and all payment records
7. All performance evaluations, vendor performance reports, and compliance reviews
8. All correspondence between the governmental body and the contractor related to performance, disputes, or modifications
9. All bid and proposal documents submitted in the procurement process (for procurements that have concluded)
10. All evaluation scoring sheets, award recommendations, and selection committee reports

Date range: {{date_range_start}} through {{date_range_end}}.

I note that executed government contracts and the financial terms thereof are public information under Texas law. The competitive bidding exception in Tex. Gov't Code § 552.104 does not apply to completed procurements. To the extent a contractor claims trade secret or commercial confidentiality protection under § 552.110, that claim requires a specific factual showing of substantial competitive harm — a general assertion of proprietary information is insufficient. See Boeing Co. v. Paxton, 466 S.W.3d 831 (Tex. 2015).

I am willing to pay fees up to ${{fee_limit}}. Please provide an itemized estimate if fees will exceed $40.

Please provide records in electronic format.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. Government contracts represent the expenditure of public funds and are inherently matters of public interest. The requested records will illuminate how public dollars are being spent on {{contract_subject}}, which is a matter of significant concern to taxpayers.''',
        'expedited_language': None,
        'notes': 'Template for requesting government contract records from Texas state and local agencies. Includes the Boeing v. Paxton citation, which established that § 552.110 claims require specific factual evidence of competitive harm — useful preemptive language when contractors are likely to object to contract disclosure.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'emails',
        'template_name': 'Texas TPIA - Email and Electronic Communications',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{governmental_body_name}}
{{governmental_body_address}}

Re: Public Information Act Request — Email and Electronic Communications
    Tex. Gov't Code Chapter 552

Dear Open Records Officer:

Pursuant to the Texas Public Information Act, Tex. Gov't Code Chapter 552, I request copies of all email and electronic communications meeting the following criteria:

1. Sent to or from: {{officials_or_offices}}
2. Date range: {{date_range_start}} through {{date_range_end}}
3. Relating to or containing any of the following subjects or terms: {{search_terms_or_topics}}

This request includes:
- Emails on all governmental email systems (including agency email accounts)
- Emails on personal email accounts used for governmental business
- Text messages and instant messages conducted on government-issued devices
- Electronic documents attached to responsive communications

Please note that public business conducted on personal devices or accounts remains subject to the TPIA. See Tex. Gov't Code § 552.002(a) (public information defined as information "collected, assembled, or maintained" in connection with official business).

If any responsive communications were deleted or are otherwise unavailable, please inform me of that fact and explain when they were deleted and under what retention policy.

I am willing to pay fees up to ${{fee_limit}}. Please provide an itemized estimate if fees will exceed $40.

Please provide records in electronic format (native email format or PDF with metadata preserved if possible).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. The requested communications relate to public business conducted by governmental officials regarding {{topic}}, a matter of significant public concern. These records will not be used for commercial purposes.''',
        'expedited_language': None,
        'notes': 'Template for email and electronic communications. Includes language addressing personal device/account use — a contested area under Texas law. The TPIA definition of "public information" (§ 552.002) broadly covers records collected in connection with official business, regardless of the device or account used.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'appeal',
        'template_name': 'Texas TPIA - Complaint / Request for AG Ruling as Requestor',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Office of the Attorney General of Texas
Open Records Division
P.O. Box 12548
Austin, Texas 78711-2548

Re: Request for Open Records Ruling
    Governmental Body: {{governmental_body_name}}
    Date of Original Request: {{original_request_date}}
    Reference No. (if assigned): {{reference_number}}

Dear Open Records Division:

I am writing to submit my written arguments in connection with the above-referenced open records matter, pursuant to Tex. Gov't Code § 552.304. I am the requestor.

BACKGROUND

On {{original_request_date}}, I submitted a public information request to {{governmental_body_name}} for: {{brief_description_of_records}}.

On {{notice_date}}, I received notice that the governmental body has requested an AG ruling on whether the information must be disclosed. [OR: The governmental body has failed to respond to my request and has not requested an AG ruling within 10 business days, constituting a waiver under Tex. Gov't Code § 552.302.]

ARGUMENTS IN FAVOR OF DISCLOSURE

{{requestor_arguments}}

The governmental body's reliance on {{exception_cited}} is misplaced for the following reasons:

{{exception_challenge_arguments}}

CONCLUSION

For the reasons stated above, I respectfully request that the Attorney General determine that the requested information must be disclosed. The public interest in transparency and open government outweighs any claimed basis for withholding.

I ask that the AG consider the following case law and prior determinations in reaching its decision: {{relevant_authorities}}.

Respectfully submitted,
{{requester_name}}

cc: {{governmental_body_name}}, Open Records Officer''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'appeal_template': None,
        'notes': 'Template for a requestor\'s submission to the Texas AG under § 552.304, arguing in favor of disclosure. This is not an "appeal" in the traditional sense — the TPIA has no administrative appeal. Instead, the requestor may submit written arguments to the AG for consideration in the AG\'s ruling. Must be filed within 15 business days of receiving notice of the AG referral. The arguments and exception challenges should be populated using research from the exemptions catalog.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'body_camera',
        'template_name': 'Texas TPIA - Body Camera Footage',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer / Custodian of Records
{{law_enforcement_agency_name}}
{{agency_address}}

Re: Public Information Act Request — Body Camera Footage
    Tex. Gov't Code Chapter 552 and Tex. Occ. Code § 1701.661

Dear Custodian of Records:

Pursuant to the Texas Public Information Act, Tex. Gov't Code Chapter 552, and the law enforcement officer standards provisions at Tex. Occ. Code § 1701.661 et seq., I request copies of the following body camera footage and related records:

FOOTAGE REQUESTED:
Date(s) of incident: {{incident_date}}
Approximate time: {{incident_time}}
Location: {{incident_location}}
Officer(s) involved (if known): {{officer_names_or_badge_numbers}}
Incident/case number (if known): {{case_or_incident_number}}
Description of incident: {{incident_description}}

ADDITIONAL RECORDS REQUESTED:
1. All CAD logs and dispatch records for the above incident
2. All written reports prepared by the involved officer(s) relating to the incident
3. Any dashcam footage capturing the same incident
4. The agency's policy governing the retention and release of body camera footage

I understand that body camera footage involving certain sensitive subjects (e.g., medical calls, child victims, locations of confidential informants) may be subject to exception or redaction. However, footage depicting law enforcement officers in their official capacity performing law enforcement functions is generally subject to disclosure. I request that you release all footage not subject to a specific statutory exception and redact only the portions that are actually excepted.

Per Tex. Occ. Code § 1701.661(d), if you decline to release footage, please identify the specific statutory basis for each withheld segment.

I am willing to pay fees up to ${{fee_limit}}. Please provide an itemized estimate before proceeding if fees will exceed $40.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. The requested body camera footage documents a law enforcement encounter that is a matter of significant public interest. Disclosure serves the public interest in accountability for law enforcement conduct. If a fee waiver is not available, please provide a detailed cost estimate itemizing all charges.''',
        'expedited_language': None,
        'notes': 'Body camera footage is governed by Tex. Occ. Code § 1701.661, which creates a specific framework for release of law enforcement body camera recordings. That statute works in tandem with the TPIA — body camera footage is public information subject to the TPIA, but § 1701.661 provides additional procedures and exceptions specific to footage. As of 2016, law enforcement agencies must adopt written policies governing body camera footage and make those policies publicly available.',
    },
    {
        'jurisdiction': 'TX',
        'record_type': 'personnel',
        'template_name': 'Texas TPIA - Public Employee Personnel Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{governmental_body_name}}
{{governmental_body_address}}

Re: Public Information Act Request — Public Employee Records
    Tex. Gov't Code Chapter 552

Dear Open Records Officer:

Pursuant to the Texas Public Information Act, Tex. Gov't Code Chapter 552, I request copies of the following records regarding public employee(s) of your governmental body:

Employee(s) at issue: {{employee_name_title_or_description}}
Date range: {{date_range_start}} through {{date_range_end}}

RECORDS REQUESTED:

1. Name, sex, ethnicity, job title, and classification (publicly available under Tex. Gov't Code § 552.024(a))
2. Salary, compensation, and benefits information (publicly available under Tex. Gov't Code § 552.024(a))
3. Dates of employment and employment history with the governmental body
4. Disciplinary records, including letters of reprimand, suspensions, demotions, and terminations related to conduct in office
5. All complaints filed against the employee related to their official duties
6. All investigations conducted by the agency into the employee's official conduct, including findings and conclusions
7. All performance evaluations
8. Separation agreements, resignation letters, and exit records (including any non-disclosure agreements)

I acknowledge that home addresses, home telephone numbers, date of birth, and Social Security numbers of employees are excepted from disclosure under Tex. Gov't Code §§ 552.114 and 552.117, and I do not request those specific items.

I note that records of an employee's official conduct — including disciplinary actions related to job performance and investigations into on-the-job conduct — are public information and are not protected by the personnel records exception at § 552.102. See generally, Tex. AG Open Records Decision No. OR2011-07534.

I am willing to pay fees up to ${{fee_limit}}. Please provide an itemized estimate if fees will exceed $40.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for requesting public employee records. Strategically acknowledges the § 552.114/§ 552.117 exceptions (home address, DOB, SSN) to preempt over-broad withholding, while asserting the public nature of official conduct records. Key distinction: records about what an employee did in their official role are public; purely personal information is not.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for template in TX_TEMPLATES:
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
    print(f'Texas TPIA templates: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_tx_templates', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
