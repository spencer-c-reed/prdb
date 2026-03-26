#!/usr/bin/env python3
"""Build Nebraska Public Records Statutes catalog — exemptions, response rules, and request templates.

Nebraska Public Records Statutes, Neb. Rev. Stat. §§ 84-712 to 84-712.09.
Nebraska\'s public records law has a strong presumption of openness. All public
records are open unless a specific statute or the Public Records Statutes expressly
permits closure. No mandatory administrative appeal — requesters may go directly to
district court after a denial.

Run: python3 scripts/build/build_ne.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

# =============================================================================
# EXEMPTIONS
# =============================================================================

NE_EXEMPTIONS = [
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(1)',
        'exemption_number': '§ 84-712.05(1)',
        'short_name': 'Records Confidential by Statute',
        'category': 'statutory',
        'description': 'Records that are specifically made confidential or excepted from disclosure by state statute or by federal law.',
        'scope': 'Records that a specific Nebraska statute or federal law affirmatively prohibits from disclosure. Nebraska courts require a specific, affirmative statutory bar — a general policy of confidentiality or a permissive confidentiality provision does not qualify. Nebraska\'s public records law itself acknowledges that other statutes may create exceptions, but those statutes must expressly restrict disclosure.',
        'key_terms': json.dumps([
            'confidential by statute', 'specifically made confidential', 'state statute',
            'federal law', 'affirmative prohibition', 'expressly restricted',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that mandates confidentiality — general administrative policies do not qualify',
            'The cited statute must affirmatively prohibit disclosure, not merely authorize discretionary confidentiality',
            'Challenge whether the specific record falls within the exact scope of the cited statute',
            'Nebraska courts construe the public records law in favor of disclosure; ambiguity in exemption scope favors the requester',
            'Federal statutes cited as grounds must actually preempt state disclosure — confirm the federal statute expressly prohibits disclosure rather than merely authorizing federal confidentiality',
        ]),
        'notes': 'Nebraska courts apply a liberal construction to the Public Records Statutes in favor of disclosure. The Nebraska Supreme Court has held that exemptions are to be strictly construed. See State ex rel. Grein v. O\'Connell, 235 Neb. 229 (1990).',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(3)',
        'exemption_number': '§ 84-712.05(3)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets and other proprietary, confidential commercial or financial information submitted by a private entity, where disclosure would cause substantial competitive harm.',
        'scope': 'Trade secrets and proprietary commercial or financial information submitted by private entities to the government in connection with licensing, regulatory proceedings, or procurement. The submitter must demonstrate that disclosure would cause substantial competitive harm. Government-generated information does not qualify. The agency makes the final determination, not the submitter.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'financial information',
            'competitive harm', 'substantial competitive injury', 'submitted by private entity',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate actual substantial competitive harm — boilerplate "confidential" markings are insufficient',
            'Government-generated analysis of private information is not itself "submitted by" the private entity',
            'The price paid with public funds in a contract is generally not a trade secret',
            'Information that is publicly available elsewhere cannot be a trade secret',
            'The agency, not the submitter, makes the final determination; submitter objection alone is insufficient to establish the exemption',
        ]),
        'notes': 'Nebraska courts apply a competitive harm standard. The Nebraska Attorney General has issued opinions that agencies must conduct independent analysis of trade secret claims rather than deferring to the submitter\'s assertion. See Op. Att\'y Gen. No. 92-030.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(4)',
        'exemption_number': '§ 84-712.05(4)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled by a law enforcement agency in connection with a criminal investigation, where disclosure would interfere with law enforcement proceedings, identify a confidential source, or endanger the life of any person.',
        'scope': 'Records compiled by law enforcement agencies during the course of criminal investigations, where disclosure would: (1) interfere with enforcement proceedings; (2) identify a confidential source or informant; (3) disclose investigative techniques and procedures not generally known; or (4) endanger the life or physical safety of any person. Nebraska courts require a specific, articulable harm for each category.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'compiled for law enforcement',
            'interfere with proceedings', 'confidential source', 'informant',
            'investigative techniques', 'endanger life',
        ]),
        'counter_arguments': json.dumps([
            'Incident reports, arrest records, and booking information are generally open even for pending cases',
            'Each withheld record must fall within one of the specific harm categories — blanket withholding of all investigative files is improper',
            'Records of completed investigations and concluded prosecutions no longer qualify under most harm-based grounds',
            'Routine investigative procedures that are generally known to the public do not qualify for protection',
            'Segregable factual portions of investigative records must be released even when the strategic or source-identifying portions are withheld',
        ]),
        'notes': 'Nebraska courts distinguish between routine law enforcement records (generally open) and investigation records (potentially protected). The Nebraska Supreme Court has held that the exemption requires a specific, articulable harm from disclosure. See State ex rel. Grein v. O\'Connell, 235 Neb. 229 (1990).',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(5)',
        'exemption_number': '§ 84-712.05(5)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between a public body and its legal counsel that are protected by attorney-client privilege.',
        'scope': 'Confidential attorney-client communications and attorney work product for purposes of legal advice or anticipated litigation. Nebraska courts apply standard attorney-client privilege analysis in the public records context. The privilege belongs to the governmental body and may be waived by voluntary disclosure.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'legal counsel', 'legal advice', 'work product',
            'confidential communication', 'anticipated litigation', 'privileged',
        ]),
        'counter_arguments': json.dumps([
            'Not all communications with an attorney are privileged — only confidential communications made for the purpose of obtaining legal advice',
            'Administrative communications with counsel and factual reports are not privileged',
            'Final settlement agreements are public records and cannot be withheld under this exemption',
            'Documents adopted as final agency policy lose their privileged character',
            'Once litigation concludes, work product protection weakens — challenge continued withholding of post-litigation materials',
        ]),
        'notes': 'Nebraska courts apply traditional attorney-client privilege analysis. The privilege is narrower in the government context and must be asserted specifically for each document withheld. General attorney-oversight of an agency\'s programs does not make all communications privileged.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(6)',
        'exemption_number': '§ 84-712.05(6)',
        'short_name': 'Personnel Evaluations',
        'category': 'privacy',
        'description': 'Personnel evaluation records, unless the employee consents to disclosure or the record relates to a final disciplinary action that resulted in dismissal, demotion, or suspension.',
        'scope': 'Performance evaluations, personnel assessment records, and related employment documents. However, Nebraska law requires disclosure of records relating to final disciplinary actions resulting in dismissal, demotion, or suspension of a public employee. Names, titles, salaries, and dates of employment of public employees are generally open under the general public records policy.',
        'key_terms': json.dumps([
            'personnel evaluation', 'performance evaluation', 'employee assessment', 'disciplinary action',
            'final disposition', 'dismissal', 'demotion', 'suspension', 'public employee',
        ]),
        'counter_arguments': json.dumps([
            'Final disciplinary actions resulting in dismissal, demotion, or suspension are EXPLICITLY open — no exemption applies to those outcomes',
            'Names, titles, salaries, and employment dates of public employees are generally open',
            'Records of an employee\'s official conduct in a public-facing role are not "personnel evaluations"',
            'Challenge blanket withholding of entire personnel files; only specific evaluation documents are protected',
            'Elected officials and senior appointed officials have reduced privacy expectations regarding their performance in public roles',
        ]),
        'notes': 'Nebraska\'s personnel evaluation exemption has an important exception for final disciplinary actions resulting in significant employment consequences. The Nebraska AG has issued opinions that the public\'s interest in government accountability outweighs employee privacy when serious discipline has occurred.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(7)',
        'exemption_number': '§ 84-712.05(7)',
        'short_name': 'Student Records',
        'category': 'privacy',
        'description': 'Student education records protected by the federal Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g.',
        'scope': 'Individual student education records at public schools, colleges, and universities. Nebraska incorporates FERPA\'s protections. Non-identifiable aggregate data, school policy documents, and administrative records that are not student education records remain open. FERPA\'s directory information exception allows disclosure of certain student information unless the student has opted out.',
        'key_terms': json.dumps([
            'student records', 'education records', 'FERPA', 'Family Educational Rights and Privacy Act',
            'student privacy', 'school records', 'academic records',
        ]),
        'counter_arguments': json.dumps([
            'FERPA protects individual student education records, not aggregate statistics or school-wide data',
            'School policies, curriculum materials, and administrative records are not "education records" under FERPA',
            'FERPA\'s directory information exception allows disclosure of designated categories unless students opt out',
            'Records about a school\'s general operations, spending, and programs are not student records',
            'Challenge whether the specific records requested are "maintained by" the educational institution and "directly related to" the student, as required by FERPA',
        ]),
        'notes': 'Nebraska incorporates FERPA by reference. The Nebraska AG has issued opinions that this exemption covers only genuine education records as defined by FERPA, not all records held by educational institutions.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(8)',
        'exemption_number': '§ 84-712.05(8)',
        'short_name': 'Tax Returns',
        'category': 'privacy',
        'description': 'Individual and corporate tax returns and related documents filed with the Nebraska Department of Revenue.',
        'scope': 'State income tax returns, supporting schedules, and related tax documents filed with the Nebraska Department of Revenue. This is a specific, narrow exemption limited to tax return filings. Does not protect general government financial records, tax policy documents, or aggregate tax data.',
        'key_terms': json.dumps([
            'tax return', 'income tax', 'tax filing', 'Department of Revenue',
            'tax document', 'state tax', 'corporate tax',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to actual tax returns, not all tax-related records — audit correspondence, policy documents, and aggregate statistics remain open',
            'Government financial records and appropriations documents are not "tax returns"',
            'Challenge overbroad use of this exemption to withhold financial information unrelated to specific tax filings',
        ]),
        'notes': 'Narrow, specific exemption for tax return information. Nebraska courts have not significantly expanded this exemption beyond its text.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(9)',
        'exemption_number': '§ 84-712.05(9)',
        'short_name': 'Adoption Records',
        'category': 'privacy',
        'description': 'Adoption records and related court records that are sealed under Nebraska\'s adoption statutes.',
        'scope': 'Records related to adoption proceedings that are sealed under Nebraska adoption statutes (Neb. Rev. Stat. §§ 43-101 et seq.). The exemption reflects the historically confidential nature of adoption records under Nebraska law. Access to sealed adoption records is governed by the adoption statutes, not the general public records law.',
        'key_terms': json.dumps([
            'adoption records', 'sealed records', 'adoption proceedings', 'birth records',
            'adoption statutes', 'confidential adoption',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to sealed adoption records; administrative records about adoption policy and programs are open',
            'Aggregate adoption statistics and program data that do not identify individuals remain open',
            'Challenge whether the specific records requested are adoption records subject to statutory sealing, as opposed to general agency records',
        ]),
        'notes': 'Narrow exemption tied specifically to Nebraska\'s adoption sealing statutes. Does not extend to general child welfare records or agency administrative records.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(2)',
        'exemption_number': '§ 84-712.05(2)',
        'short_name': 'Medical Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, psychological, and related health records of individually identifiable persons held by public agencies.',
        'scope': 'Individually identifiable medical and mental health records held by state and local agencies, public hospitals, public health agencies, and similar entities. Non-identifiable aggregate public health data and health program statistics remain open. HIPAA provides parallel federal protection for covered entities.',
        'key_terms': json.dumps([
            'medical records', 'psychiatric records', 'psychological records', 'health records',
            'individually identifiable', 'patient records', 'treatment records', 'HIPAA',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate, de-identified public health data is open — demand non-identifiable versions of health statistics',
            'Policy documents about health program administration are not medical records',
            'Challenge whether records are truly "individually identifiable" — records stripped of patient identifiers may be open',
            'Records about the operations, spending, and performance of health programs are open',
        ]),
        'notes': 'Nebraska\'s medical records exemption is consistent with HIPAA. The AG has issued opinions that aggregate public health data does not qualify as individually identifiable medical information and remains open.',
    },
    {
        'jurisdiction': 'NE',
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05(10)',
        'exemption_number': '§ 84-712.05(10)',
        'short_name': 'Security Measures',
        'category': 'safety',
        'description': 'Records containing specific security plans, security assessments, and vulnerability information for public infrastructure and facilities.',
        'scope': 'Specific security plans, vulnerability assessments, and security-sensitive architectural information for public buildings and critical infrastructure where disclosure could enable attacks or endanger the public. Does not protect general information about public facilities that is publicly available. The security threat must be specific and articulable.',
        'key_terms': json.dumps([
            'security plan', 'security assessment', 'vulnerability', 'critical infrastructure',
            'public safety', 'security measures', 'threat assessment',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers specific security details, not general information about public facilities',
            'Publicly available information cannot be withheld on security grounds',
            'Administrative records about security contracts and spending do not automatically qualify',
            'Challenge whether the specific information requested could realistically enable a security threat — speculative harm is insufficient',
        ]),
        'notes': 'Nebraska added enhanced security exemptions in the post-9/11 period. Nebraska courts and the AG\'s office have noted that this exemption should be applied narrowly to specific operational security information.',
    },
]

# =============================================================================
# RESPONSE RULES
# =============================================================================

NE_RULES = [
    {
        'jurisdiction': 'NE',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '4',
        'day_type': 'business',
        'statute_citation': 'Neb. Rev. Stat. § 84-712(2)',
        'notes': 'The custodian must provide requested records within 4 business days of receiving the request. If the records cannot be provided within 4 business days, the custodian must provide a written explanation stating when the records will be available. Business days in Nebraska means Monday through Friday, excluding state holidays.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'initial_response',
        'param_key': 'extension_extraordinary_circumstances',
        'param_value': '8',
        'day_type': 'business',
        'statute_citation': 'Neb. Rev. Stat. § 84-712(2)',
        'notes': 'For extraordinary circumstances, the custodian may extend the response period by up to 8 additional business days. "Extraordinary circumstances" include: (1) need to search and collect records from multiple locations; (2) voluminous amount of records; or (3) need to consult with another agency. The custodian must notify the requester in writing of the extension, its duration, and the reason.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'failure_to_respond_within_4_business_days',
        'day_type': 'business',
        'statute_citation': 'Neb. Rev. Stat. § 84-712(2)',
        'notes': 'Failure to respond within 4 business days (or the extended period) may be treated as a constructive denial, entitling the requester to seek judicial relief in district court. Nebraska has no mandatory administrative appeal — district court is available immediately after a denial or constructive denial.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'fee_cap',
        'param_key': 'copying_per_page_letter_size',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712(3)',
        'notes': 'The fee for paper copies of letter-size (8.5" x 11") documents may not exceed $0.25 per page. Agencies may charge less. This is a statutory maximum — challenge any higher per-page fee for standard letter-size documents.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'fee_cap',
        'param_key': 'copying_fee_actual_cost',
        'param_value': 'actual_cost_not_to_exceed_statutory_maximum',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712(3)',
        'notes': 'Overall fees must not exceed the actual cost to the agency of providing the records. Agencies may charge for actual staff time to search and retrieve records, but not at a profit. Electronic records may be provided at the actual cost of the medium. Challenge fee schedules that include administrative overhead or indirect costs not tied to the specific request.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fees',
        'param_value': 'actual_cost_of_staff_time',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712(3)',
        'notes': 'Agencies may charge for actual staff time spent searching, retrieving, and preparing records, at the actual cost of that staff (not overhead rates). The total fees — including search, retrieval, and copying — may not exceed actual costs. Request an itemized fee estimate for large requests.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_suit',
        'param_value': 'immediately_after_denial',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712.03',
        'notes': 'Nebraska has NO mandatory administrative appeal process. After a denial (or constructive denial), the requester may immediately file suit in district court to compel disclosure. There is no requirement to exhaust administrative remedies before going to court. This is one of Nebraska\'s key open-government provisions.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'burden_of_proof',
        'param_value': 'agency_bears_burden',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712.03',
        'notes': 'In a district court enforcement action, the custodian bears the burden of demonstrating that the withheld records fall within a specific exemption under § 84-712.05 or another statute. The requester does not bear the burden of proving wrongful withholding. Nebraska courts apply this burden-shifting consistent with the strong public access policy.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712.03(2)',
        'notes': 'Courts may award reasonable attorney fees and costs to a prevailing requester. Fee awards are discretionary — the court considers whether the agency acted without reasonable basis and whether the litigation was necessary to obtain disclosure. Nebraska courts have awarded fees in cases of clear public records violations.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712.05',
        'notes': 'Nebraska\'s Public Records Statutes require agencies to segregate exempt portions of records and release the non-exempt portions. When only part of a record is exempt, the remainder must be released with the exempt portions redacted. Blanket withholding of entire documents when only portions are exempt is improper.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_statutory_basis',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712(2)',
        'notes': 'Any denial must be in writing and must state the specific statutory basis for the denial. A denial without a legal citation is improper. The written denial triggers the requester\'s right to seek district court review under § 84-712.03. Oral denials do not constitute a proper denial and should be treated as a constructive denial.',
    },
    {
        'jurisdiction': 'NE',
        'rule_type': 'fee_waiver',
        'param_key': 'waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Neb. Rev. Stat. § 84-712(3)',
        'notes': 'Nebraska law does not provide a mandatory fee waiver. Agencies have discretion to waive or reduce fees for media, public interest, or research requesters. Requesters may ask for a waiver based on public interest. The Nebraska AG has noted that fee waivers can promote the public records law\'s policy of maximum transparency.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NE_TEMPLATES = [
    {
        'jurisdiction': 'NE',
        'record_type': 'general',
        'template_name': 'General Nebraska Public Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Nebraska Public Records Statutes

Dear Custodian of Public Records:

Pursuant to the Nebraska Public Records Statutes, Neb. Rev. Stat. §§ 84-712 to 84-712.09, I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be produced in electronic format where available, to minimize cost to both parties.

I am willing to pay copying fees based on actual cost as permitted by Neb. Rev. Stat. § 84-712(3), up to ${{fee_limit}}. Per § 84-712(3), fees for letter-size paper copies may not exceed $0.25 per page. If you estimate that fees will exceed my stated limit, please notify me before processing so I may narrow or prioritize this request.

Pursuant to Neb. Rev. Stat. § 84-712(2), I request a response within 4 business days of your receipt of this request. If records cannot be provided within 4 business days, please notify me in writing with the estimated date of production.

If any portion of this request is denied, I ask that you: (1) provide a written statement citing the specific statutory provision under which access is denied, as required by § 84-712(2); (2) segregate any exempt portions and provide the non-exempt portions of any partially exempt records; and (3) provide sufficient detail to allow me to evaluate whether to seek district court review under § 84-712.03.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that your agency waive or reduce the fees associated with this request. While Nebraska law does not mandate a fee waiver, I ask that you exercise your discretion because the records requested serve the public interest.

These records relate to {{public_interest_explanation}}, a matter of direct public concern to Nebraska citizens. I am {{requester_category_description}} and intend to share this information with the public through {{dissemination_method}}.

Nebraska\'s strong policy of public access under § 84-712 supports a fee waiver here. Providing records at no cost (or minimal cost) would advance the purpose of the Public Records Statutes without imposing any significant burden on the agency.''',
        'expedited_language': '''I request that this public records request be processed as quickly as possible. While Nebraska law provides 4 business days for a response, the particular urgency of this request warrants the earliest possible action.

Specifically, I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond that date would {{harm_from_delay}}.

I appreciate your prompt attention to this time-sensitive request.''',
        'notes': 'General-purpose Nebraska Public Records request template. Key Nebraska features: 4-business-day response deadline (with up to 8 additional days for extraordinary circumstances); $0.25/page cap for letter-size copies; NO mandatory administrative appeal — requester may go directly to district court after denial. Nebraska AG opinions are persuasive authority on exemption scope.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = {'exemptions': 0, 'rules': 0, 'templates': 0}
    skipped = {'exemptions': 0, 'rules': 0, 'templates': 0}
    errors = 0

    try:
        # --- Exemptions ---
        for exemption in NE_EXEMPTIONS:
            existing = conn.execute(
                'SELECT id FROM exemptions WHERE jurisdiction = ? AND statute_citation = ?',
                (exemption['jurisdiction'], exemption['statute_citation'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE exemptions SET
                        exemption_number = ?,
                        short_name = ?,
                        category = ?,
                        description = ?,
                        scope = ?,
                        key_terms = ?,
                        counter_arguments = ?,
                        notes = ?,
                        last_verified = datetime('now'),
                        updated_at = datetime('now')
                    WHERE id = ?
                    ''',
                    (
                        exemption['exemption_number'],
                        exemption['short_name'],
                        exemption['category'],
                        exemption['description'],
                        exemption['scope'],
                        exemption['key_terms'],
                        exemption['counter_arguments'],
                        exemption['notes'],
                        existing[0],
                    )
                )
                skipped['exemptions'] += 1
            else:
                conn.execute(
                    '''
                    INSERT INTO exemptions (
                        jurisdiction, statute_citation, exemption_number,
                        short_name, category, description, scope,
                        key_terms, counter_arguments, notes, last_verified
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    ''',
                    (
                        exemption['jurisdiction'],
                        exemption['statute_citation'],
                        exemption['exemption_number'],
                        exemption['short_name'],
                        exemption['category'],
                        exemption['description'],
                        exemption['scope'],
                        exemption['key_terms'],
                        exemption['counter_arguments'],
                        exemption['notes'],
                    )
                )
                added['exemptions'] += 1

        # --- Rules ---
        for rule in NE_RULES:
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
                skipped['rules'] += 1
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
                added['rules'] += 1

        # --- Templates ---
        for template in NE_TEMPLATES:
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
                skipped['templates'] += 1
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
                added['templates'] += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    total_added = sum(added.values())
    total_skipped = sum(skipped.values())
    print(
        f'NE Public Records: '
        f'{added["exemptions"]} exemptions, {added["rules"]} rules, {added["templates"]} templates added; '
        f'{total_skipped} updated; {errors} errors'
    )
    write_receipt(
        script='build_ne',
        added=total_added,
        skipped=total_skipped,
        errors=errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
