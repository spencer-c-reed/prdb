#!/usr/bin/env python3
"""Build law enforcement request templates for states missing them.

Adds law enforcement records request templates for MA, ME, MI, MN, NE, VT.
Each template cites the state-specific public records statute and requests
common law enforcement record categories (incident reports, body camera footage,
use of force reports, internal affairs, 911/dispatch, arrest records).

Run: python3 scripts/build/build_law_enforcement_templates.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TEMPLATES = [
    {
        'jurisdiction': 'MA',
        'record_type': 'law_enforcement',
        'template_name': 'Massachusetts Public Records Law - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records
    M.G.L. c. 66, § 10

Dear Records Access Officer:

Pursuant to the Massachusetts Public Records Law, M.G.L. c. 66, § 10, and 950 C.M.R. 32.00, I request access to and copies of the following law enforcement records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following records:

1. All incident reports, offense reports, and supplemental reports related to the above incident
2. All body camera and dashcam footage from officers responding to or involved in the incident
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation records related to the incident or the named officer(s)
5. All 911 call recordings, dispatch logs, and CAD records related to the incident
6. All arrest records, booking records, and custody documentation for {{subject_name}} related to this incident

I understand that certain investigatory materials may be exempt under the public records exemption for investigatory materials at M.G.L. c. 4, § 7(26)(f). However, I ask that you:
(a) Apply exemptions narrowly and release all reasonably segregable non-exempt portions;
(b) Provide a specific written explanation for any withheld records identifying the exemption claimed;
(c) Note that completed investigation reports and routine booking information are generally not exempt.

Under 950 C.M.R. 32.06(2), you must respond within 10 business days. If you determine that additional time is needed, you must petition the Supervisor of Records for an extension.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide a detailed estimate before proceeding. I request a fee waiver if applicable under 950 C.M.R. 32.07.

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver of fees pursuant to 950 C.M.R. 32.07. Disclosure of the requested law enforcement records is in the public interest because the records shed light on the operations and activities of government — specifically, law enforcement conduct in {{incident_location}} — and the information is not primarily in my commercial interest. The public has a strong interest in transparency and accountability in policing.''',
        'expedited_language': None,
        'notes': 'Massachusetts law enforcement records template under M.G.L. c. 66, § 10. The key exemption for law enforcement records is M.G.L. c. 4, § 7(26)(f), covering "investigatory materials necessarily compiled out of the public view by law enforcement." This exemption is narrower than it appears — courts have held it does not cover routine reports, booking information, or records from completed investigations where no prosecution is pending. The 2016 public records reform (c. 121 of the Acts of 2016) strengthened response timelines and created the Supervisor of Records enforcement mechanism.',
    },
    {
        'jurisdiction': 'ME',
        'record_type': 'law_enforcement',
        'template_name': 'Maine Freedom of Access Act - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Freedom of Access Request — Law Enforcement Records
    1 M.R.S.A. § 408

Dear Records Custodian:

Pursuant to the Maine Freedom of Access Act (FOAA), 1 M.R.S.A. § 408, I request access to and copies of the following law enforcement records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following records:

1. All incident reports, offense reports, and supplemental reports related to the above incident
2. All body camera and dashcam footage from officers responding to or involved in the incident
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation records related to the incident or the named officer(s)
5. All 911 call recordings, dispatch logs, and CAD records related to the incident
6. All arrest records, booking records, and custody documentation for {{subject_name}} related to this incident

I understand that 16 M.R.S.A. § 804 makes certain law enforcement records confidential during an active investigation, including "intelligence and investigative record information." However, I note that:
(a) Records of completed investigations are generally public;
(b) Basic booking and arrest information (name, charge, bail) is public under 16 M.R.S.A. § 803;
(c) Any withholding must be based on a specific statutory provision, not a blanket claim.

Under 1 M.R.S.A. § 408-A, you must acknowledge receipt of this request within 5 business days and provide a good-faith estimate of the time needed to respond.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide a written estimate before proceeding. I request that fees be limited to the actual cost of copying, as required by 1 M.R.S.A. § 408(5).

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver or reduction. The requested records relate to law enforcement activities that are a matter of significant public interest, and disclosure will contribute to public understanding of government operations. The information will not be used for commercial purposes.''',
        'expedited_language': None,
        'notes': 'Maine FOAA law enforcement template. Maine has a separate statute governing law enforcement records confidentiality: 16 M.R.S.A. §§ 803-809. Section 803 makes basic booking/arrest info public. Section 804 protects "intelligence and investigative record information" but only during active investigations — once an investigation is complete or a case is closed, records generally become public. The distinction between active and closed investigations is critical. Appeals go to the Superior Court under 1 M.R.S.A. § 409.',
    },
    {
        'jurisdiction': 'MI',
        'record_type': 'law_enforcement',
        'template_name': 'Michigan FOIA - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Coordinator
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records
    MCL 15.231 et seq.

Dear FOIA Coordinator:

Pursuant to the Michigan Freedom of Information Act (FOIA), MCL 15.231 et seq., I request access to and copies of the following law enforcement records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following records:

1. All incident reports, offense reports, and supplemental reports related to the above incident
2. All body camera and dashcam footage from officers responding to or involved in the incident
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation records related to the incident or the named officer(s)
5. All 911 call recordings, dispatch logs, and CAD records related to the incident
6. All arrest records, booking records, and custody documentation for {{subject_name}} related to this incident

I understand that MCL 15.243(1)(b) exempts records of "law enforcement communication codes or plans for deployment of law enforcement" and that MCL 15.243(1)(b)(i)-(vi) provides specific exemptions for law enforcement investigatory records. However, I note that:
(a) These exemptions are discretionary, not mandatory — the statute says the agency "may" exempt, not "shall";
(b) Exemptions must be applied narrowly and non-exempt portions must be segregated and released per MCL 15.244(1);
(c) The agency must provide a written explanation for each denial citing the specific statutory basis per MCL 15.235(5).

Under MCL 15.235(2), you must respond within 5 business days of receipt. You may extend this period by up to 10 additional business days with written notice.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide a detailed, itemized fee estimate before proceeding, as required by MCL 15.234. I note that labor costs for search and review must be based on the hourly wage of the lowest-paid employee capable of performing the task.

Please provide records in electronic format if available, at no additional charge per MCL 15.233(1)(d).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver or reduction of fees pursuant to MCL 15.234(3). Disclosure of the requested law enforcement records is in the public interest because the records will contribute significantly to public understanding of government operations — specifically, law enforcement conduct and accountability. I am not requesting these records for commercial purposes. The fee charged should not exceed the actual incremental cost of duplicating the records.''',
        'expedited_language': None,
        'notes': 'Michigan FOIA law enforcement template. Key distinction: Michigan FOIA exemptions are discretionary ("may exempt"), not mandatory. This means agencies can choose to release records even if an exemption applies. MCL 15.243(1)(b)(i)-(vi) lists specific law enforcement exemptions covering investigatory records, informant identities, and law enforcement techniques. The 2014 FOIA amendments added fee limitations and required itemized cost breakdowns. Michigan has no administrative appeal — denials go directly to Circuit Court under MCL 15.240, though requesters can also file complaints with the legislative oversight body.',
    },
    {
        'jurisdiction': 'MN',
        'record_type': 'law_enforcement',
        'template_name': 'Minnesota Government Data Practices Act - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Responsible Authority / Data Practices Compliance Official
{{agency_name}}
{{agency_address}}

Re: Data Practices Request — Law Enforcement Data
    Minn. Stat. § 13.82

Dear Responsible Authority:

Pursuant to the Minnesota Government Data Practices Act (MGDPA), Minn. Stat. Chapter 13, and specifically § 13.82 governing law enforcement data, I request access to and copies of the following records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following data:

1. All incident reports, offense reports, and supplemental reports — these constitute "public" data under Minn. Stat. § 13.82, subd. 2 (response and incident data)
2. All body camera and dashcam footage from officers responding to or involved in the incident — classified under Minn. Stat. § 13.825
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation data related to the incident or the named officer(s) — noting that certain complaint data is classified as public under § 13.82, subd. 13
5. All 911 call recordings, dispatch logs, and CAD records — classified as public data under Minn. Stat. § 13.82, subd. 2 (response data)
6. All arrest records, booking data, and custody documentation for {{subject_name}} related to this incident — arrest data is public under Minn. Stat. § 13.82, subd. 2

I am aware that Minnesota's Data Practices Act classifies government data into three categories: public, private, and confidential. For law enforcement data specifically, § 13.82 establishes detailed classification rules:
- Subdivision 2 makes response/incident data PUBLIC (including date, time, location, nature of call, names of officers, use of force, and, for adults, the identity of arrested persons)
- Subdivision 7 makes certain criminal investigative data CONFIDENTIAL or PROTECTED NONPUBLIC during active investigations, but this data becomes public upon completion of the investigation
- Subdivision 13 addresses internal affairs data

I ask that you classify and release each responsive record according to its specific statutory classification, rather than applying a blanket "investigative" classification to all records.

Under Minn. Stat. § 13.03, subd. 3, you must respond to this request "immediately, if possible" or within a reasonable time. If any data is classified as private or confidential, please provide a written statement citing the specific statutory provision.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide an estimate before proceeding. Fees must not exceed the actual cost of searching for and copying the data per Minn. Stat. § 13.03, subd. 3(c).

Please provide data in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a reduction or waiver of fees. The requested law enforcement data relates to matters of significant public concern — specifically, {{public_interest_explanation}}. Disclosure will contribute to public understanding of law enforcement operations. Minnesota law requires that fees not exceed actual costs, and I ask that the agency exercise its discretion to waive or reduce fees given the public interest served by disclosure.''',
        'expedited_language': None,
        'notes': 'Minnesota uses the Government Data Practices Act (MGDPA) rather than a traditional FOIA-style law. The MGDPA classifies ALL government data as public, private, or confidential — a fundamentally different framework from exemption-based systems. For law enforcement, § 13.82 is the critical statute with over 30 subdivisions creating specific classification rules for different types of law enforcement data. Key subdivisions: subd. 2 (response/incident data = public), subd. 7 (investigative data = confidential while active, public when inactive), subd. 13 (internal affairs). Body camera footage is governed by § 13.825, which creates its own classification scheme. Appeals go to the Commissioner of Administration or directly to district court under § 13.085.',
    },
    {
        'jurisdiction': 'NE',
        'record_type': 'law_enforcement',
        'template_name': 'Nebraska Public Records Law - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records
    Neb. Rev. Stat. § 84-712

Dear Records Custodian:

Pursuant to the Nebraska Public Records Statutes, Neb. Rev. Stat. §§ 84-712 through 84-712.09, I request access to and copies of the following law enforcement records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following records:

1. All incident reports, offense reports, and supplemental reports related to the above incident
2. All body camera and dashcam footage from officers responding to or involved in the incident
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation records related to the incident or the named officer(s)
5. All 911 call recordings, dispatch logs, and CAD records related to the incident
6. All arrest records, booking records, and custody documentation for {{subject_name}} related to this incident

I understand that Neb. Rev. Stat. § 84-712.05(5) allows withholding of records that constitute "records developed or received by law enforcement agencies and other public bodies charged with duties of investigation or examination of persons, institutions, or businesses" when disclosure would interfere with an ongoing investigation. However, I note that:
(a) This exemption applies only during active investigations — records from closed cases are generally public;
(b) The Nebraska Supreme Court has held that exemptions must be narrowly construed in favor of disclosure;
(c) Basic incident reports and arrest records are routinely available as public records.

Under Neb. Rev. Stat. § 84-712(4), you must respond within 4 business days. If access is denied, you must provide a written statement of the reasons for denial citing the specific statutory basis.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide an estimate before proceeding. Fees should reflect only the actual cost of reproducing the records per § 84-712(3)(b).

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver or reduction of fees. The requested law enforcement records concern matters of significant public interest, and their disclosure will contribute to public understanding of law enforcement operations and accountability. I will not use the records for commercial purposes.''',
        'expedited_language': None,
        'notes': 'Nebraska public records law enforcement template. Nebraska has a relatively straightforward public records statute. The key law enforcement exemption is § 84-712.05(5), which protects investigatory records only when disclosure would interfere with ongoing investigations or examinations. The Nebraska Supreme Court has interpreted exemptions narrowly, and the burden is on the agency to justify withholding. Nebraska has a 4-business-day response deadline — one of the shorter timelines among states. Appeals are to the Attorney General under § 84-712.03 or directly to district court.',
    },
    {
        'jurisdiction': 'VT',
        'record_type': 'law_enforcement',
        'template_name': 'Vermont Public Records Act - Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records
    1 V.S.A. § 315

Dear Records Custodian:

Pursuant to the Vermont Public Records Act, 1 V.S.A. §§ 315-320, I request access to and copies of the following law enforcement records:

Subject/Incident: {{subject_name}}
Incident date: {{incident_date}}
Incident location: {{incident_location}}
Case/incident number (if known): {{case_number}}
Officer(s) involved (if known): {{officer_name}}

Specifically, I request the following records:

1. All incident reports, offense reports, and supplemental reports related to the above incident
2. All body camera and dashcam footage from officers responding to or involved in the incident — noting that 20 V.S.A. § 4622 governs law enforcement body camera recordings
3. All use of force reports filed in connection with the incident
4. All internal affairs complaints and investigation records related to the incident or the named officer(s)
5. All 911 call recordings, dispatch logs, and CAD records related to the incident
6. All arrest records, booking records, and custody documentation for {{subject_name}} related to this incident

I understand that 1 V.S.A. § 317(c) provides exemptions from disclosure, including § 317(c)(5) for records that, if disclosed, could interfere with law enforcement investigations. However, I note that:
(a) Vermont law establishes a strong presumption in favor of public access — the burden is on the agency to justify each withholding;
(b) Exemptions must be applied narrowly to specific records, not broadly to entire categories;
(c) Completed investigation records and routine incident reports are generally public;
(d) Even exempt records must be released in redacted form if non-exempt portions can be segregated.

Under 1 V.S.A. § 318(a)(2), you must respond within 3 business days of receipt. If additional time is needed, you must provide a specific date by which the records will be available, not to exceed 10 business days from receipt.

I am willing to pay reasonable fees. If the cost will exceed ${{fee_limit}}, please provide an estimate before proceeding. Under 1 V.S.A. § 316(e), fees must be limited to the actual cost of providing the copies.

Please provide records in electronic format if available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a waiver or reduction of fees pursuant to 1 V.S.A. § 316(e). The requested law enforcement records relate to matters of clear public interest — specifically, {{public_interest_explanation}}. Disclosure will meaningfully contribute to public understanding of law enforcement conduct and government accountability. I will not use the records for commercial purposes.''',
        'expedited_language': None,
        'notes': 'Vermont Public Records Act law enforcement template. Vermont has a strong public records law with a 3-business-day initial response deadline (one of the shortest in the country). The key law enforcement exemption is 1 V.S.A. § 317(c)(5), which protects records whose disclosure would interfere with ongoing investigations. Body camera footage is specifically governed by 20 V.S.A. § 4622, enacted in 2016, which creates retention and access rules for law enforcement body camera recordings. Vermont also has specific provisions regarding internal affairs records — complaints against officers are generally public once an investigation is complete. Appeals go to the Superior Court under 1 V.S.A. § 319.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for template in TEMPLATES:
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
                print(f"  {template['jurisdiction']}: law_enforcement template already exists, updated")
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
                print(f"  {template['jurisdiction']}: inserted")

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'Law enforcement templates: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_law_enforcement_templates', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
