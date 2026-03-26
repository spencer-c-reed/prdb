#!/usr/bin/env python3
"""Build Maine Freedom of Access Act catalog — exemptions, response rules, and request templates.

Maine Freedom of Access Act (FOAA), 1 MRSA §§ 400–414.
Default rule is public access; exceptions must be expressly authorized by statute.
Maine's Public Access Ombudsman (within Department of the Attorney General) provides
informal mediation as a pre-litigation alternative.

Run: python3 scripts/build/build_me.py
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

ME_EXEMPTIONS = [
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(A)',
        'exemption_number': '§ 402(3)(A)',
        'short_name': 'Confidential by Statute',
        'category': 'statutory',
        'description': 'Records that are specifically made confidential or excepted from disclosure by a state or federal statute.',
        'scope': 'Records that a specific Maine statute or federal law expressly makes confidential or prohibits from disclosure. The exemption requires an affirmative statutory prohibition — a general policy of confidentiality or a discretionary confidentiality provision does not qualify. Examples include certain tax return information, grand jury records, and sealed court records.',
        'key_terms': json.dumps([
            'confidential by statute', 'specifically made confidential', 'state statute',
            'federal statute', 'expressly prohibited', 'mandated confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that mandates confidentiality — general confidentiality policies do not qualify',
            'A statute permitting (but not requiring) confidentiality does not establish this exemption; the statute must affirmatively prohibit disclosure',
            'Challenge whether the specific record falls within the scope of the cited statute — statutes are often narrower than agencies claim',
            'Federal statutes that restrict disclosure must actually apply to the specific record at issue; agencies sometimes cite inapplicable federal laws',
            'Maine\'s FOAA policy of liberal construction favors disclosure when exemption scope is ambiguous',
        ]),
        'notes': 'Maine courts construe exemptions narrowly in light of FOAA\'s strong disclosure policy. The AG\'s office and Public Access Ombudsman have issued guidance that the exemption requires a specific, affirmative statutory prohibition. See Guy Gannett Pub. Co. v. University of Maine, 555 A.2d 470 (Me. 1989).',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(B)',
        'exemption_number': '§ 402(3)(B)',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Individually identifiable personnel records, except for the name, title, compensation, and dates of employment of each employee — which are always open.',
        'scope': 'Personnel files, performance evaluations, disciplinary records, and similar records identifying individual employees. However, Maine law explicitly requires disclosure of employee names, titles, dates of employment, and compensation regardless of the personnel record exemption. Medical records within personnel files receive additional protection. Final disciplinary actions resulting in significant employment consequences are often open.',
        'key_terms': json.dumps([
            'personnel records', 'performance evaluation', 'individually identifiable', 'employee',
            'name', 'title', 'compensation', 'dates of employment', 'disciplinary record',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, compensation, and dates of employment are EXPLICITLY open under § 402(3)(B) — no exemption covers those fields',
            'Final disciplinary determinations, especially those resulting in termination or significant sanction, are generally open',
            'Records of an employee\'s official conduct and public duties are not "personnel records"',
            'Challenge blanket withholding of entire files when only specific sensitive items warrant protection; request segregation of open and closed portions',
            'Public officials and high-ranking employees have reduced privacy expectations in their official conduct',
        ]),
        'notes': 'Maine courts have held that the personnel exemption is narrowly construed. The carve-out for names, titles, compensation, and dates of employment is mandatory — agencies must disclose those fields even when the broader personnel file is protected. See Bangor Publishing Co. v. University of Maine System, 1997 ME 64.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(C)',
        'exemption_number': '§ 402(3)(C)',
        'short_name': 'Labor Negotiations',
        'category': 'commercial',
        'description': 'Records pertaining to collective bargaining strategy and labor negotiations, while negotiations are pending.',
        'scope': 'Records reflecting the government\'s negotiating strategy, bottom-line positions, and internal deliberations about collective bargaining, while those negotiations are ongoing. The exemption is strictly time-limited — once a contract is reached or negotiations conclude, the underlying records generally become open. Final collective bargaining agreements are public records.',
        'key_terms': json.dumps([
            'collective bargaining', 'labor negotiations', 'negotiating strategy', 'union contract',
            'pending negotiations', 'labor relations', 'bargaining position',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only while negotiations are active and pending — completed negotiations lose their protection',
            'Final collective bargaining agreements are public records — demand the executed contract',
            'Historical wage data and benefits schedules, once agreed upon, are open',
            'Records about labor relations that are not part of active negotiations (e.g., grievance procedures, established work rules) are open',
            'Challenge whether negotiations are genuinely "pending" — inactive or expired contract negotiations do not qualify',
        ]),
        'notes': 'Maine courts have consistently held that this exemption is time-limited to active negotiations. Once a contract is executed, the negotiating history becomes open. See Maine Teachers Association v. Board of Education, 1993 ME 97.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(D)',
        'exemption_number': '§ 402(3)(D)',
        'short_name': 'Attorney-Client / Legal Work Product',
        'category': 'deliberative',
        'description': 'Communications between an agency and its legal counsel that are protected by attorney-client privilege or attorney work product doctrine.',
        'scope': 'Attorney-client privileged communications and attorney work product prepared in anticipation of litigation or for giving legal advice. The privilege belongs to the governmental body, not the individual attorney. Maine courts apply the same attorney-client privilege analysis as in private litigation, modified for the public context. Final settlement agreements are generally open.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal counsel', 'legal advice',
            'anticipation of litigation', 'privileged communication', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'The privilege applies to confidential legal advice, not to all communications with an attorney; administrative direction to counsel and factual reports are not privileged',
            'Once litigation concludes, the work product rationale weakens significantly; challenge continued withholding of post-litigation records',
            'Final settlements and consent decrees are public records and cannot be withheld under this exemption',
            'The governmental attorney-client privilege is narrower than the private privilege in some jurisdictions; challenge overbroad claims',
            'Documents adopted as final agency policy lose their privileged character even if they began as legal advice',
        ]),
        'notes': 'Maine courts apply attorney-client privilege in the FOAA context using traditional privilege analysis. The privilege can be waived by voluntary disclosure to third parties. See Bangor Daily News v. Erwin, 2014 ME 120.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(E)',
        'exemption_number': '§ 402(3)(E)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled as part of a law enforcement investigation, including intelligence information on criminal organizations.',
        'scope': 'Records compiled by a law enforcement agency during the course of an active or recently concluded criminal investigation. Covers informant identities, undercover techniques, and information whose disclosure would jeopardize an ongoing investigation. Once a prosecution concludes (conviction, acquittal, or declination), many underlying investigative records become open. Incident reports, arrest records, and other non-investigative law enforcement records remain open.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'informant', 'intelligence',
            'undercover', 'ongoing investigation', 'compiled for law enforcement',
            'jeopardize investigation',
        ]),
        'counter_arguments': json.dumps([
            'Incident reports and initial complaint reports are generally open even for pending cases',
            'Once a prosecution concludes, challenge continued withholding of investigative materials',
            'The agency must show the investigation is actively open and that disclosure would actually jeopardize it',
            'Routine law enforcement records — patrol logs, call-for-service records, booking information — are not "investigation records" and must be released',
            'Segregable portions not relating to investigative strategy or informant identity must be released',
        ]),
        'notes': 'Maine courts distinguish between routine law enforcement records (generally open) and investigation records (may be protected). See Bangor Publishing Co. v. City of Bangor, 2002 ME 49. The AG\'s office has issued guidance that arrest records are open unless they would identify an undercover officer or informant.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(F)',
        'exemption_number': '§ 402(3)(F)',
        'short_name': 'Individual Financial Records',
        'category': 'privacy',
        'description': 'Records that contain information about an individual\'s personal finances, including tax returns, financial statements, and similar documents.',
        'scope': 'Individual (personal) financial records — tax returns, personal financial statements, bank account information, and similar documents held by a government agency. Does not protect the financial records of the government itself or financial information about businesses, though separately submitted proprietary business financial information may qualify under the trade secrets exemption.',
        'key_terms': json.dumps([
            'personal financial information', 'tax return', 'financial statement', 'bank account',
            'individual finances', 'income', 'assets', 'liabilities',
        ]),
        'counter_arguments': json.dumps([
            'Government financial records — budgets, expenditures, contracts, grants — are not "individual financial records" and remain open',
            'Business financial information is not protected as "individual" financial information unless separately covered by trade secrets exemption',
            'Aggregate financial data that does not identify individuals is not protected',
            'The agency must show the records are genuinely about individual personal finances, not merely that they contain financial figures',
        ]),
        'notes': 'Maine courts apply this exemption narrowly to true personal financial information. Government fiscal records are not protected. See Portland Evening News v. Superintendent of Schools, 1984 ME 50.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(G)',
        'exemption_number': '§ 402(3)(G)',
        'short_name': 'Medical Records',
        'category': 'privacy',
        'description': 'Medical and psychiatric records of individual patients, clients, or recipients of government services.',
        'scope': 'Individually identifiable medical, psychiatric, and mental health records held by state and local agencies, public hospitals, public health programs, and similar entities. Non-identifiable aggregate health data and public health statistics remain open. HIPAA provides parallel federal protection for covered entities.',
        'key_terms': json.dumps([
            'medical record', 'psychiatric record', 'mental health record', 'patient',
            'individually identifiable', 'health information', 'treatment record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate, de-identified health data is open — demand non-identifiable versions of health statistics',
            'Policy documents about health program administration are not "medical records"',
            'Challenge whether records are genuinely individually identifiable — records stripped of patient identifiers may be open',
            'Records about systemic health department practices and procedures, not individual patients, are open',
        ]),
        'notes': 'Maine\'s medical record exemption is consistent with HIPAA. The Public Access Ombudsman has issued guidance that aggregate public health data — disease rates, public health surveillance — remains open regardless of this exemption.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(H)',
        'exemption_number': '§ 402(3)(H)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets and other confidential commercial or financial information submitted to a government agency by a private entity, where disclosure would cause substantial harm to the competitive position of the submitting entity.',
        'scope': 'Trade secrets and proprietary commercial or financial information submitted by private entities in connection with licensing, regulatory compliance, or procurement. The submitter must demonstrate that disclosure would cause substantial competitive harm. Government-generated information does not qualify. Maine courts apply a competitive harm standard.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'confidential',
            'competitive harm', 'substantial harm', 'competitive position', 'submitted by private entity',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate specific, substantial competitive harm — not merely assert proprietary status',
            'Information publicly available elsewhere cannot be a trade secret',
            'The government body, not the submitter, makes the final withholding determination; submitter objection alone is insufficient',
            'The price paid with public funds in a contract is generally not a trade secret',
            'Government-generated analysis or audit findings based on private data are not themselves "submitted by" the private entity',
        ]),
        'notes': 'Maine courts apply a competitive harm standard. The Public Access Ombudsman has issued guidance that agencies must make their own independent assessment of competitive harm, not simply defer to the submitter\'s claim of confidentiality.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(I)',
        'exemption_number': '§ 402(3)(I)',
        'short_name': 'Security Assessments',
        'category': 'safety',
        'description': 'Records that contain specific security assessments, security plans, or vulnerability analyses for public infrastructure or buildings.',
        'scope': 'Specific security plans, vulnerability assessments, and security-related architectural information for public buildings and critical infrastructure where disclosure could enable attacks or compromise security. Does not protect general information about public facilities that is otherwise publicly available.',
        'key_terms': json.dumps([
            'security assessment', 'security plan', 'vulnerability analysis', 'critical infrastructure',
            'public building', 'security measures', 'threat assessment',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers specific security details, not general information about public facilities',
            'Publicly available information about facility locations and general layouts is not protected',
            'Administrative records about security contracts and spending do not automatically qualify',
            'Challenge whether the specific record could realistically enable a security threat — speculative harm is insufficient',
        ]),
        'notes': 'Maine added this exemption after 9/11. The Public Access Ombudsman has noted that the exemption should be applied only to specific security-sensitive details, not as a general shield for government building information.',
    },
    {
        'jurisdiction': 'ME',
        'statute_citation': '1 MRSA § 402(3)(J)',
        'exemption_number': '§ 402(3)(J)',
        'short_name': 'Intelligence / Counterterrorism Records',
        'category': 'safety',
        'description': 'Records compiled for counterterrorism purposes, including intelligence information about potential terrorism threats.',
        'scope': 'Records compiled in connection with counterterrorism investigations, including intelligence information about suspected terrorist organizations, threat assessments, and information shared with federal agencies under counterterrorism information sharing arrangements. The exemption is intended for genuine security intelligence, not general public safety records.',
        'key_terms': json.dumps([
            'counterterrorism', 'intelligence', 'terrorism', 'threat assessment',
            'homeland security', 'information sharing', 'security intelligence',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to counterterrorism intelligence, not to general law enforcement or public safety information',
            'Records must genuinely relate to terrorism threats — agencies cannot use this exemption as a catch-all for sensitive law enforcement records',
            'Factual portions of counterterrorism records (e.g., policy procedures, agency structure) may be segregable from protected intelligence',
            'Challenge overly broad claims that routine public safety records constitute "counterterrorism intelligence"',
        ]),
        'notes': 'Added post-9/11. Maine courts have not extensively construed this exemption. The AG and Public Access Ombudsman have cautioned that it should be applied narrowly to genuine counterterrorism intelligence, not as a general national security shield.',
    },
]

# =============================================================================
# RESPONSE RULES
# =============================================================================

ME_RULES = [
    {
        'jurisdiction': 'ME',
        'rule_type': 'initial_response',
        'param_key': 'days_to_acknowledge',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '1 MRSA § 408-A(1)',
        'notes': 'An agency must acknowledge a public records request within 5 business days of receipt. The acknowledgment must include an estimate of the time needed to produce the records and an estimate of any fees. If the agency can provide the records within 5 business days, a separate acknowledgment is not required — it can simply produce the records.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'initial_response',
        'param_key': 'days_to_produce',
        'param_value': 'reasonable_time',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(1)',
        'notes': 'Maine\'s FOAA requires production within a "reasonable time." Unlike many states, there is no specific statutory deadline for actually producing records (beyond the 5-day acknowledgment). What is "reasonable" depends on the volume and complexity of the request. Courts have found delays of more than a few weeks unreasonable for simple requests.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'after_unreasonable_delay',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(1)',
        'notes': 'Unreasonable delay in producing records may be treated as a constructive denial, allowing the requester to seek court review or refer the matter to the Public Access Ombudsman. There is no specific trigger date — courts evaluate reasonableness based on the circumstances. The absence of any response beyond 5 business days is a strong indicator of unreasonable delay.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'fee_cap',
        'param_key': 'copying_per_page_paper',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(8)',
        'notes': 'Copying fees for paper documents are limited to $0.10 per page (letter and legal size) or the actual cost of the medium for other formats. This is one of the lowest per-page caps of any state. Agencies may not charge more than this statutory maximum for standard paper copies.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'fee_cap',
        'param_key': 'copying_fee_actual_cost_electronic',
        'param_value': 'actual_cost_of_medium',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(8)',
        'notes': 'For electronic records, agencies may charge the actual cost of the medium (e.g., a USB drive or CD). Agencies may not charge programming or staff time for producing electronic records that already exist in retrievable form. The $0.10/page cap does not apply to electronic records, but the "actual cost" standard still prohibits profit.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval',
        'param_value': 'actual_cost_not_to_exceed_statutory',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(8)',
        'notes': 'Agencies may charge for the actual cost of search and retrieval, but not a profit margin. The fee must reflect actual staff time at the actual cost of that staff (not overhead). Challenge fee estimates that include administrative overhead, profit, or costs not directly attributable to the specific request.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'public_access_ombudsman',
        'param_value': 'available_before_court',
        'day_type': None,
        'statute_citation': '1 MRSA § 414-A',
        'notes': 'Maine has a Public Access Ombudsman within the Attorney General\'s office who provides informal mediation and advisory opinions on FOAA disputes. Requesters may refer disputes to the Ombudsman before filing suit. The Ombudsman\'s opinions are non-binding but persuasive. Referral to the Ombudsman does not toll any court deadlines.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_review',
        'param_value': 'after_denial_or_unreasonable_delay',
        'day_type': None,
        'statute_citation': '1 MRSA § 409',
        'notes': 'Maine has no mandatory administrative appeal. After a denial or unreasonable delay, the requester may seek review in Superior Court. The court may conduct an in camera review of withheld records. The agency bears the burden of justifying each withholding.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_for_prevailing_requester',
        'day_type': None,
        'statute_citation': '1 MRSA § 409(3)',
        'notes': 'Courts may award reasonable attorney fees and costs to a prevailing requester. Fee awards are discretionary — the court considers whether the agency\'s withholding was reasonable and whether the suit was necessary to obtain disclosure. Maine courts have awarded fees in cases of clear FOAA violations.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '1 MRSA § 407',
        'notes': 'When a record contains both public and exempt portions, the agency must separate the exempt portions and make the non-exempt portions available. The agency must inform the requester of the reason for any deletion. Blanket withholding of entire documents when only portions are exempt violates FOAA.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'fee_waiver',
        'param_key': 'waiver_for_public_benefit',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(8)',
        'notes': 'Maine law does not provide a mandatory fee waiver, but agencies have discretion to waive or reduce fees when disclosure would primarily benefit the general public. Requesters may request a fee waiver based on public interest. The Public Access Ombudsman may address fee disputes informally.',
    },
    {
        'jurisdiction': 'ME',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_legal_basis',
        'day_type': None,
        'statute_citation': '1 MRSA § 408-A(3)',
        'notes': 'Any denial must be in writing and must state the legal basis for the denial. An oral denial is not sufficient. The written denial allows the requester to evaluate whether to challenge the withholding before the Ombudsman or in court.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

ME_TEMPLATES = [
    {
        'jurisdiction': 'ME',
        'record_type': 'general',
        'template_name': 'General Maine FOAA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records / Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Access Act Request for Public Records

Dear Custodian of Records:

Pursuant to the Maine Freedom of Access Act (FOAA), 1 MRSA §§ 400–414, I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be produced in electronic format where available, to minimize cost.

Pursuant to 1 MRSA § 408-A(8), I am willing to pay copying fees based on actual cost, up to ${{fee_limit}}. If you estimate that fees will exceed this amount, please notify me before processing so I may prioritize my request.

Pursuant to 1 MRSA § 408-A(1), I ask that you acknowledge this request within 5 business days and produce the records within a reasonable time thereafter.

If any portion of this request is denied, I ask that you: (1) provide a written statement of the specific legal basis for each denial, as required by 1 MRSA § 408-A(3); and (2) separate and provide the non-exempt portions of any partially exempt records, pursuant to 1 MRSA § 407.

If you have questions about this request, please contact me at {{requester_email}} or {{requester_phone}}.

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that the agency waive or reduce the fees associated with this request. Although FOAA does not mandate a fee waiver, I ask that you exercise your discretion to waive fees because disclosure of these records serves the public interest.

These records relate to {{public_interest_explanation}}, a matter of significant public concern. I am {{requester_category_description}} and intend to share this information with the public through {{dissemination_method}}.

Maine\'s $0.10/page copy fee cap under 1 MRSA § 408-A(8) already provides some protection against excessive fees, but a full waiver would better serve the FOAA\'s policy of maximum access.''',
        'expedited_language': '''I request that this FOAA request be processed promptly. While I understand that the statute requires only an acknowledgment within 5 business days, I ask that the agency prioritize this request because:

{{urgency_explanation}}

Specifically, I need these records by {{needed_by_date}}. Delay beyond that date would {{harm_from_delay}}.

I appreciate your prompt attention to this time-sensitive matter.''',
        'notes': 'General-purpose Maine FOAA template. Uses correct Maine statutory citations. Key Maine features: 5-business-day acknowledgment requirement, $0.10/page copy fee cap, and availability of the Public Access Ombudsman as an informal dispute resolution resource before court. No mandatory administrative appeal.',
    },
    {
        'jurisdiction': 'ME',
        'record_type': 'appeal',
        'template_name': 'Maine FOAA — Public Access Ombudsman Referral',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Access Ombudsman
Office of the Attorney General
6 State House Station
Augusta, ME 04333

Re: Referral of FOAA Dispute — {{agency_name}} / Request dated {{original_request_date}}

Dear Public Access Ombudsman:

I am requesting the Ombudsman\'s assistance with a dispute arising under the Maine Freedom of Access Act, 1 MRSA §§ 400–414.

BACKGROUND

On {{original_request_date}}, I submitted a public records request to {{agency_name}} for {{brief_description_of_records}}. A copy of my request is attached.

On {{response_date}}, the agency {{description_of_agency_response}}.

NATURE OF DISPUTE

{{nature_of_dispute}}

Specifically, I dispute the agency\'s reliance on {{exemption_or_basis_cited}} for the following reasons:

{{grounds_for_dispute}}

RELIEF REQUESTED

I respectfully request that the Ombudsman:

1. Contact {{agency_name}} and inquire about the basis for its response;
2. Provide guidance on whether the agency\'s action is consistent with FOAA; and
3. Facilitate disclosure of the withheld records.

I have enclosed / attached:
- Copy of my original FOAA request ({{original_request_date}})
- Copy of the agency\'s response ({{response_date}})
- Any additional correspondence

I am available to provide additional information at {{requester_email}} or {{requester_phone}}.

Respectfully,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Template for referral to Maine\'s Public Access Ombudsman (within the AG\'s office) as an informal pre-litigation step. The Ombudsman\'s process is free, informal, and non-binding, but effective for resolving straightforward FOAA disputes without litigation. A referral does not toll court deadlines. If the Ombudsman process is unsuccessful, the requester may still file in Superior Court under 1 MRSA § 409.',
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
        for exemption in ME_EXEMPTIONS:
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
        for rule in ME_RULES:
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
        for template in ME_TEMPLATES:
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
        f'ME FOAA: '
        f'{added["exemptions"]} exemptions, {added["rules"]} rules, {added["templates"]} templates added; '
        f'{total_skipped} updated; {errors} errors'
    )
    write_receipt(
        script='build_me',
        added=total_added,
        skipped=total_skipped,
        errors=errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
