#!/usr/bin/env python3
"""Build Vermont Public Records Act catalog — exemptions, response rules, and request templates.

Vermont Public Records Act (PRA), 1 VSA §§ 315–320.
Vermont has one of the fastest response deadlines in the country (3 business days)
and a two-step appeal process: head of agency first, then Superior Court.
The Secretary of State\'s office provides guidance and mediation assistance.

Run: python3 scripts/build/build_vt.py
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

VT_EXEMPTIONS = [
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(1)',
        'exemption_number': '§ 317(b)(1)',
        'short_name': 'Records Exempt by Other Statute',
        'category': 'statutory',
        'description': 'Records that are specifically exempted from disclosure by another Vermont statute or by federal law.',
        'scope': 'Records that a specific Vermont or federal statute affirmatively prohibits from disclosure. The exemption requires an express statutory bar, not merely a discretionary confidentiality provision. Vermont courts construe this exemption narrowly in keeping with the PRA\'s presumption of openness.',
        'key_terms': json.dumps([
            'exempt by statute', 'specifically exempted', 'state statute', 'federal law',
            'affirmative prohibition', 'mandated confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that requires confidentiality — a general privacy policy or regulation does not qualify',
            'The cited statute must affirmatively prohibit disclosure, not merely permit discretionary withholding',
            'Challenge whether the specific record falls within the exact scope of the cited statute',
            'Vermont\'s PRA expressly states that exemptions are construed narrowly — use this principle to challenge ambiguous claims',
            'Vermont courts have rejected claims that federal laws preempt the PRA unless the federal statute expressly prohibits state disclosure',
        ]),
        'notes': 'Vermont\'s PRA requires that the exempting statute specifically prohibit disclosure. The Vermont Supreme Court has held that Vermont law is to be liberally construed in favor of public access. See Caledonian-Record Publishing Co. v. Vermont State Colleges, 175 Vt. 438 (2003).',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(2)',
        'exemption_number': '§ 317(b)(2)',
        'short_name': 'Personal Documents Not Governmental in Nature',
        'category': 'privacy',
        'description': 'Records that are personal in nature and whose disclosure would be a clearly unwarranted invasion of personal privacy, when the subject has no relationship to public duties or government services.',
        'scope': 'Purely personal documents held by a government agency that have no relationship to the person\'s public duties or governmental services — e.g., personal notes, private correspondence, and personal financial information voluntarily stored on government systems. Vermont applies a balancing test weighing the privacy interest against the public\'s interest in disclosure.',
        'key_terms': json.dumps([
            'personal documents', 'personal nature', 'unwarranted invasion', 'personal privacy',
            'no governmental relationship', 'private correspondence', 'personal notes',
        ]),
        'counter_arguments': json.dumps([
            'Vermont requires a "clearly unwarranted" invasion — the threshold is high; mere personal embarrassment is insufficient',
            'Documents relating to a public employee\'s performance of official duties are not "personal" even if they contain personal information',
            'Public officials have a reduced privacy expectation in records touching on their exercise of public authority',
            'The balancing test strongly favors disclosure for records related to public administration',
            'Challenge whether the documents truly have "no relationship" to government functions — most documents held by agencies relate to governmental activities',
        ]),
        'notes': 'Vermont courts apply a balancing test with a strong presumption in favor of disclosure. The phrase "clearly unwarranted" sets a high threshold. See Agency of Human Services v. Soundness, 2006 VT 115.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(5)',
        'exemption_number': '§ 317(b)(5)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled by a law enforcement agency in connection with a criminal investigation, where disclosure would interfere with law enforcement proceedings or deprive a person of a fair trial.',
        'scope': 'Records compiled for law enforcement purposes that, if disclosed, would: (1) interfere with enforcement proceedings; (2) deprive a person of a right to a fair trial or impartial adjudication; (3) identify a confidential source; (4) disclose investigative techniques and procedures; or (5) endanger the life or physical safety of any person. Vermont follows a harm-based standard for each category.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'compiled for law enforcement',
            'interfere with proceedings', 'fair trial', 'confidential source',
            'investigative techniques', 'endanger life',
        ]),
        'counter_arguments': json.dumps([
            'Each withheld record must fall within one of the specific harm categories — blanket withholding of all investigation records is improper',
            'Records of completed investigations and concluded prosecutions no longer implicate most harm-based grounds',
            'Incident reports, arrest records, and booking information are generally open even for pending cases',
            'Routine investigative techniques that are publicly known do not qualify for protection',
            'Segregable factual portions (names, dates, locations) that do not reveal investigative strategy must be released',
        ]),
        'notes': 'Vermont courts apply a harm-based standard requiring specific, articulable harm from disclosure. The Vermont Supreme Court has held that completed prosecutions significantly reduce (though do not eliminate) the grounds for withholding. See Vermont v. Tallman, 148 Vt. 465 (1987).',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(9)',
        'exemption_number': '§ 317(b)(9)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted by a private entity to a government agency, where disclosure would cause substantial harm to the competitive position of the submitting entity.',
        'scope': 'Trade secrets and proprietary commercial or financial information submitted by private entities in connection with regulatory proceedings, permits, or procurement. The submitter must demonstrate actual competitive harm from disclosure. Government-generated information does not qualify. Vermont courts apply a competitive harm standard.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'financial information',
            'competitive harm', 'substantial competitive injury', 'submitted by private entity',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate specific, substantial competitive harm — boilerplate "confidential" labels are insufficient',
            'Government-generated analysis and regulatory findings, even if based on private data, are not "submitted by" the private entity',
            'The price of a contract paid with public funds is generally not a trade secret',
            'Information publicly available elsewhere cannot qualify as a trade secret',
            'The agency, not the submitter, makes the final determination; submitter objection alone is insufficient',
        ]),
        'notes': 'Vermont courts apply a competitive harm standard. The Secretary of State\'s guidance notes that agencies must conduct their own independent assessment, not defer to the submitter\'s labeling. See In re Vermont Gas Systems, 2012 VT 87.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(4)',
        'exemption_number': '§ 317(b)(4)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between a public agency and its legal counsel that are protected by attorney-client privilege.',
        'scope': 'Confidential communications between a government agency and its attorneys for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege applies in the FOAA context using the same standards as in private litigation. Vermont courts have held that the privilege is not a blanket shield for all government legal files.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'legal counsel', 'legal advice', 'work product',
            'confidential communication', 'anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'Not all communications with an attorney are privileged — only confidential communications made for the purpose of obtaining legal advice',
            'Factual reports to attorneys and administrative direction are not privileged',
            'Once litigation concludes, work product protection weakens; challenge continued withholding of post-litigation records',
            'Final settlement agreements are public records',
            'Documents adopted as final agency policy lose their privileged character',
        ]),
        'notes': 'Vermont courts apply traditional attorney-client privilege analysis in the PRA context. The Vermont Supreme Court has held that the privilege is not unlimited and must be asserted specifically for each document. See Caledonian-Record Publishing Co. v. Vermont State Colleges, 175 Vt. 438 (2003).',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(7)',
        'exemption_number': '§ 317(b)(7)',
        'short_name': 'Tax Returns',
        'category': 'privacy',
        'description': 'State income tax returns and related financial disclosure forms filed with the Vermont Department of Taxes.',
        'scope': 'Vermont state income tax returns, supporting schedules, and related documents filed with or held by the Department of Taxes. This is a specific, narrow exemption limited to tax return information. Does not protect general government financial records or non-tax financial information.',
        'key_terms': json.dumps([
            'tax return', 'income tax', 'tax filing', 'Vermont Department of Taxes',
            'financial disclosure', 'state tax',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to tax returns, not to all tax-related records — audit correspondence, policy documents, and aggregate statistics remain open',
            'This exemption does not protect financial information submitted outside the tax context',
            'Government financial records (budgets, appropriations, expenditures) are not tax returns',
            'The exemption is narrow and specific — challenge attempts to use it as a general financial privacy shield',
        ]),
        'notes': 'Narrow, specific exemption for tax return information. Vermont courts have not significantly expanded this exemption beyond its text.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(8)',
        'exemption_number': '§ 317(b)(8)',
        'short_name': 'Personnel Evaluations',
        'category': 'privacy',
        'description': 'Personnel evaluations, performance appraisals, and records of employee discipline, except for the final disposition of disciplinary proceedings that result in the imposition of a serious sanction.',
        'scope': 'Performance evaluations, disciplinary proceedings in progress, and similar employment records. However, Vermont law requires disclosure of the final disposition of serious disciplinary proceedings. Names, titles, salaries, and dates of employment are generally open. Records of official conduct are not personnel evaluations.',
        'key_terms': json.dumps([
            'personnel evaluation', 'performance appraisal', 'employee discipline', 'serious sanction',
            'final disposition', 'employment record', 'performance review',
        ]),
        'counter_arguments': json.dumps([
            'Final dispositions of serious disciplinary proceedings are EXPLICITLY open — no exemption applies to those outcomes',
            'Names, titles, salaries, and dates of employment of public employees are open regardless of this exemption',
            'Records of an employee\'s official conduct and public duties are not "personnel evaluations"',
            'Challenge blanket withholding of entire files; only the specific evaluation or active disciplinary process is protected',
            'Elected officials and high-level public officials have reduced privacy expectations',
        ]),
        'notes': 'Vermont\'s personnel evaluation exemption has an important exception for final dispositions of serious disciplinary proceedings. Vermont courts have held that the public\'s interest in knowing how agencies discipline employees outweighs privacy when the outcome is a significant sanction.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(11)',
        'exemption_number': '§ 317(b)(11)',
        'short_name': 'Real Estate Appraisals',
        'category': 'commercial',
        'description': 'Real estate appraisals and engineering or feasibility estimates for the acquisition or disposal of government property, prior to the completion of the transaction.',
        'scope': 'Appraisals and feasibility estimates prepared for or in connection with the government\'s acquisition or disposal of real property, while the transaction is pending. The exemption is time-limited — once the property transaction is complete, the appraisals and related documents become open public records.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'feasibility estimate', 'property acquisition',
            'property disposal', 'pending transaction', 'engineering estimate',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is strictly time-limited to pending transactions — once complete, all appraisals are open',
            'Final purchase prices and recorded deeds are public records regardless of this exemption',
            'Challenge whether the transaction is genuinely "pending" — expired or abandoned transactions do not qualify',
            'The exemption protects the appraisal values themselves, not administrative records about the appraisal process',
        ]),
        'notes': 'Vermont courts have consistently held this exemption ends when the property transaction concludes. This is consistent with the PRA\'s general policy that time-limited exemptions should be construed narrowly.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(12)',
        'exemption_number': '§ 317(b)(12)',
        'short_name': 'Student Records',
        'category': 'privacy',
        'description': 'Education records that are protected by the federal Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g.',
        'scope': 'Student education records protected by FERPA at public schools, colleges, and universities. Vermont incorporates FERPA\'s protections into the PRA through this cross-reference. Non-identifiable aggregate student data, school policies, and administrative records that are not student education records remain open.',
        'key_terms': json.dumps([
            'student records', 'education records', 'FERPA', 'Family Educational Rights and Privacy Act',
            'student privacy', 'school records', 'academic records',
        ]),
        'counter_arguments': json.dumps([
            'FERPA protects individual student education records, not aggregate data or school-wide statistics',
            'School policies, curriculum materials, and administrative records are not "education records" under FERPA',
            'FERPA allows disclosure of directory information unless the student has opted out — challenge blanket withholding of directory-type data',
            'Records about a school\'s general operations, spending, and programs are not student records',
            'Challenge whether the specific records requested are "maintained by" the educational institution for the purpose that triggers FERPA',
        ]),
        'notes': 'Vermont incorporates FERPA by reference. Vermont courts and the Secretary of State\'s office have held that this exemption covers only genuine education records as defined by FERPA, not all records held by educational institutions.',
    },
    {
        'jurisdiction': 'VT',
        'statute_citation': '1 VSA § 317(b)(14)',
        'exemption_number': '§ 317(b)(14)',
        'short_name': 'Security Plans and Procedures',
        'category': 'safety',
        'description': 'Security plans and security procedures for public buildings and facilities, where disclosure could reasonably be expected to endanger public safety.',
        'scope': 'Specific security plans, intrusion detection procedures, and vulnerability assessments for public buildings and infrastructure. Does not protect general publicly available information about the location or existence of public facilities. The threat of harm must be specific and articulable, not speculative.',
        'key_terms': json.dumps([
            'security plan', 'security procedures', 'public building', 'facility security',
            'endanger safety', 'vulnerability', 'intrusion detection',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers specific security procedures, not general information about public buildings',
            'Publicly available information cannot be withheld on security grounds',
            'Administrative records about security spending and contracts do not automatically qualify',
            'Challenge whether the specific information requested could realistically enable a security threat',
        ]),
        'notes': 'Vermont added this exemption in the post-9/11 period. The Secretary of State\'s office has issued guidance that it should be applied narrowly to specific operational security details.',
    },
]

# =============================================================================
# RESPONSE RULES
# =============================================================================

VT_RULES = [
    {
        'jurisdiction': 'VT',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': '1 VSA § 318(a)(1)',
        'notes': 'Vermont requires a response within 3 business days of receiving the request — one of the fastest mandatory response timelines in the country. The response must be a grant, denial, or acknowledgment with an estimated completion date. Business days means Monday through Friday, excluding Vermont legal holidays.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'initial_response',
        'param_key': 'extension_for_unusual_circumstances',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': '1 VSA § 318(a)(1)',
        'notes': 'For unusual circumstances, the agency may extend the deadline by up to 10 additional business days. "Unusual circumstances" means: (1) the need to search for and collect records from multiple locations; (2) the need to examine a voluminous amount of records; or (3) the need to consult with another agency or unit. The agency must notify the requester in writing of the extension and the reason.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'failure_to_respond_within_3_business_days',
        'day_type': 'business',
        'statute_citation': '1 VSA § 318(a)(1)',
        'notes': 'Failure to respond within 3 business days (or the extended period for unusual circumstances) may be treated as a denial, allowing the requester to appeal to the head of the agency or seek court relief. The agency\'s failure to acknowledge the request within the statutory period is itself a violation of the PRA.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'fee_cap',
        'param_key': 'copying_per_page_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': '1 VSA § 316(b)',
        'notes': 'Vermont allows agencies to charge up to $0.25 per page for paper copies. This is a ceiling, not a floor — agencies may charge less. The fee must reflect the actual cost of reproduction, not administrative overhead.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'fee_cap',
        'param_key': 'copying_fee_actual_cost',
        'param_value': 'actual_cost_of_reproduction',
        'day_type': None,
        'statute_citation': '1 VSA § 316(b)',
        'notes': 'Fees must not exceed the actual cost of providing the records. Agencies may not include administrative overhead, profit, or indirect costs in their fee calculations. Challenge fee schedules that exceed actual reproduction costs.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'appeal_deadline',
        'param_key': 'appeal_to_agency_head_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '1 VSA § 318(b)',
        'notes': 'Vermont requires the requester to first appeal to the head of the agency within 5 business days of the denial. This internal administrative appeal is a mandatory prerequisite to seeking judicial review. The appeal must be in writing and state the grounds for the appeal.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'appeal_deadline',
        'param_key': 'agency_head_response_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '1 VSA § 318(b)',
        'notes': 'The head of the agency must respond to the administrative appeal within 5 business days. If the agency head denies the appeal, the requester may then seek review in Superior Court. If the agency head fails to respond within 5 business days, the failure constitutes a denial and the requester may proceed to court.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_review',
        'param_value': 'after_agency_head_denial',
        'day_type': None,
        'statute_citation': '1 VSA § 319',
        'notes': 'After the agency head denies the appeal (or fails to respond within 5 business days), the requester may seek review in Vermont Superior Court. The court applies de novo review of the withholding decision. The agency bears the burden of demonstrating that the withheld records fall within a specific exemption.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_if_agency_acted_without_reasonable_basis',
        'day_type': None,
        'statute_citation': '1 VSA § 319(c)',
        'notes': 'Courts may award reasonable attorney fees and litigation costs to a prevailing requester if the agency acted without a reasonable basis in law. Fee awards are discretionary — the court evaluates whether the agency\'s withholding had a legally sound foundation. Vermont courts have awarded fees in cases of clear PRA violations.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'secretary_of_state_guidance',
        'param_value': 'available_informally',
        'day_type': None,
        'statute_citation': '1 VSA § 315',
        'notes': 'Vermont\'s Secretary of State provides informal guidance on PRA questions through an open government coordinator. This is non-binding but useful for resolving straightforward disputes before litigation. The Secretary of State also publishes training materials and plain-language guides to the PRA.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '1 VSA § 317(b)',
        'notes': 'Vermont\'s PRA requires agencies to segregate exempt portions of records and release the non-exempt portions. When only part of a record is exempt, the rest must be released with the exempt portions redacted. The agency must identify the specific exemption for each redaction.',
    },
    {
        'jurisdiction': 'VT',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_exemption_citation',
        'day_type': None,
        'statute_citation': '1 VSA § 318(a)(2)',
        'notes': 'Any denial must be in writing and must specify the exemption under which access is denied, including the specific subsection. A denial without a specific legal citation is improper and may support a finding of a PRA violation. The written denial is required both for the initial denial and for the agency head\'s denial on appeal.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

VT_TEMPLATES = [
    {
        'jurisdiction': 'VT',
        'record_type': 'general',
        'template_name': 'General Vermont PRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request

Dear Custodian of Public Records:

Pursuant to the Vermont Public Records Act (PRA), 1 VSA §§ 315–320, I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be produced in electronic format where available, to minimize cost to both parties.

I am willing to pay copying fees based on actual cost as permitted by 1 VSA § 316(b), up to ${{fee_limit}}. Vermont law permits agencies to charge up to $0.25 per page for paper copies. If you estimate that fees will exceed my stated limit, please notify me before processing so I may narrow or prioritize this request.

Pursuant to 1 VSA § 318(a)(1), I request a response within 3 business days of your receipt of this request. If access to any records will be denied, please provide a written statement citing the specific PRA exemption relied upon for each denial, as required by 1 VSA § 318(a)(2).

If any record is partially exempt, please redact only the exempt portions and produce the remainder, in accordance with the PRA\'s segregability requirement.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that your agency waive or reduce copying fees for this request. While the PRA does not mandate a fee waiver, I ask that you exercise your discretion to waive fees because these records are of significant public interest.

These records relate to {{public_interest_explanation}}, a matter of direct public concern in Vermont. I am {{requester_category_description}} and intend to share the information with the public through {{dissemination_method}}.

Vermont\'s $0.25/page cap under 1 VSA § 316(b) provides some protection, but a full waiver would best serve the PRA\'s policy of maximum public access.''',
        'expedited_language': '''I request that this PRA request be processed as promptly as possible. Vermont\'s 3-business-day response deadline already reflects the legislature\'s intent for swift responses, but the particular urgency of this request justifies the earliest possible production.

Specifically, I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond that date would {{harm_from_delay}}.

I appreciate your prompt attention to this request.''',
        'notes': 'General-purpose Vermont PRA template. Vermont has one of the fastest mandatory response deadlines (3 business days). Key Vermont features: mandatory internal administrative appeal to the agency head (within 5 business days of denial) before court review, and Secretary of State guidance available as an informal resource.',
    },
    {
        'jurisdiction': 'VT',
        'record_type': 'appeal',
        'template_name': 'Vermont PRA — Administrative Appeal to Agency Head',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Head of Agency / Agency Head\'s Designee
{{agency_name}}
{{agency_address}}

Re: Public Records Act Appeal — Request dated {{original_request_date}}

Dear {{agency_head_title}}:

Pursuant to 1 VSA § 318(b), I hereby appeal the denial of my Public Records Act request dated {{original_request_date}}.

BACKGROUND

On {{original_request_date}}, I submitted a PRA request to {{agency_name}} for {{brief_description_of_records}}. On {{response_date}}, the custodian {{description_of_denial}}.

GROUNDS FOR APPEAL

{{appeal_arguments}}

Specifically, I dispute the agency\'s reliance on {{exemption_cited}} for the following reasons:

{{exemption_challenge_arguments}}

Vermont\'s PRA requires that exemptions be construed narrowly in light of the strong public policy favoring disclosure. See 1 VSA § 315(a). The agency has not satisfied its burden of demonstrating that the withheld records fall squarely within the claimed exemption.

RELIEF REQUESTED

I respectfully request that you reverse the initial denial and:
1. Grant access to all withheld records;
2. In the alternative, release all segregable non-exempt portions of any partially exempt records; and
3. Provide a written explanation with specific statutory citations for any records that remain withheld.

Pursuant to 1 VSA § 318(b), I request a response within 5 business days.

If this appeal is denied, I intend to seek review in Vermont Superior Court under 1 VSA § 319.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Vermont requires an administrative appeal to the agency head before seeking judicial review — this step is mandatory. Must be filed within 5 business days of the initial denial. The agency head must respond within 5 business days. If the agency head denies or fails to respond, the requester may then file in Superior Court under 1 VSA § 319.',
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
        for exemption in VT_EXEMPTIONS:
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
        for rule in VT_RULES:
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
        for template in VT_TEMPLATES:
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
        f'VT PRA: '
        f'{added["exemptions"]} exemptions, {added["rules"]} rules, {added["templates"]} templates added; '
        f'{total_skipped} updated; {errors} errors'
    )
    write_receipt(
        script='build_vt',
        added=total_added,
        skipped=total_skipped,
        errors=errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
