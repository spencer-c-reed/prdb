#!/usr/bin/env python3
"""Build Idaho Public Records Act data: exemptions, rules, and templates.

Covers Idaho's Public Records Act, Idaho Code § 74-101 et seq.
Idaho has a 3-business-day response deadline with a 10-day extension available.
No administrative appeal; enforcement is in district court. $0.10/page copy fee.
Attorney's fees for prevailing requesters. Civil penalties available. Idaho's law
is generally strong on disclosure with a clear presumption in favor of openness.

Run: python3 scripts/build/build_id.py
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
# Idaho Code § 74-104 establishes that all public records are subject to
# disclosure unless specifically exempt. The exemptions are in § 74-105 through
# § 74-126 and in various other statutes. The burden of establishing an
# exemption is on the agency. Courts construe exemptions narrowly.
# =============================================================================

ID_EXEMPTIONS = [
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(1)',
        'exemption_number': '§ 74-105(1)',
        'short_name': 'Personal Information — Privacy Protection',
        'category': 'privacy',
        'description': 'Personal records or information about a person — including information that would disclose personal details about a private individual where disclosure would constitute an unreasonable invasion of personal privacy — may be exempt.',
        'scope': 'Personal identifying information about private individuals: Social Security numbers, financial account information, home addresses, medical information, and similar personal data whose disclosure would constitute an unreasonable invasion of personal privacy. The standard is whether a reasonable person would find the disclosure objectionable in light of the public interest in the information. Public employees have a reduced privacy expectation in records relating to their official conduct. Names, titles, salaries, and work-related conduct of public employees are generally public. The "unreasonable invasion" test requires balancing — not all personal information is automatically exempt.',
        'key_terms': json.dumps([
            'personal information', 'privacy', 'personal records', 'unreasonable invasion',
            'Social Security number', 'financial information', 'home address',
            'medical information', 'personally identifiable information',
        ]),
        'counter_arguments': json.dumps([
            'Public employee names, salaries, job titles, and work-related conduct are public — the privacy exemption does not protect core employment data',
            'The "unreasonable invasion" standard requires balancing — agencies must show the privacy interest outweighs the public interest',
            'Information already in the public domain cannot be withheld as a privacy matter',
            'Disciplinary records involving misconduct in the performance of official duties are generally public',
            'Challenge overbroad privacy claims that redact non-personal contextual information',
        ]),
        'notes': 'Idaho courts apply the unreasonable invasion standard under a balancing approach. The Idaho Supreme Court has held that public employee conduct in the performance of official duties has a diminished privacy expectation. See Cowles Publishing v. Magistrate Court, 118 Idaho 753 (1990).',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(4)',
        'exemption_number': '§ 74-105(4)',
        'short_name': 'Personnel Records — Investigations and Performance',
        'category': 'privacy',
        'description': 'Personnel records of public employees, including performance evaluations, disciplinary investigations that did not result in formal discipline, and related personal employment data are exempt, subject to significant exceptions for matters of public accountability.',
        'scope': 'Private personal information in public employee personnel files: medical records, informal investigations that did not result in discipline, personal financial data, home addresses. However, Idaho law makes public: (1) names, job titles, and salaries of all public employees; (2) records of formal disciplinary actions resulting in suspension, demotion, or termination; (3) separation agreements and payments; (4) job application materials for finalists for senior public positions. The exemption does not shield evidence of serious misconduct. Law enforcement officer disciplinary records have reduced exemption protection.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation',
            'disciplinary records', 'public employee', 'salary', 'employment records',
            'HR records', 'formal discipline', 'misconduct investigation',
        ]),
        'counter_arguments': json.dumps([
            'Idaho Code § 74-108 makes public the name, position, pay, and pay changes for all public employees',
            'Formal disciplinary actions resulting in suspension, demotion, or termination are public',
            'Separation agreements and severance payments with public funds are public',
            'Senior job applicant records are public for finalist candidates',
            'Law enforcement officer misconduct records are subject to heightened disclosure',
            'Challenge claims that investigations closed without discipline were "disciplinary investigations" — informal inquiries may not qualify',
        ]),
        'notes': 'Idaho Code § 74-108 expressly requires disclosure of basic public employee compensation data. This is a separate, affirmative disclosure obligation that overrides the general personnel record exemption for compensation information. Idaho courts have held that formal disciplinary records are public under the accountability principle.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(5)',
        'exemption_number': '§ 74-105(5)',
        'short_name': 'Law Enforcement Records — Ongoing Investigations',
        'category': 'law_enforcement',
        'description': 'Criminal investigation records that, if disclosed, would interfere with an active investigation, endanger a person\'s life or safety, or identify a confidential informant, are exempt from public disclosure.',
        'scope': 'Active criminal investigation records where disclosure would specifically: (1) interfere with a pending investigation or prosecution; (2) endanger the life or physical safety of any person; (3) identify a confidential informant; or (4) deprive a person of a fair trial. Completed investigations do not retain this protection — Idaho courts have held that once prosecution concludes, investigation records become public. Arrest records, booking information, and incident reports are generally public. The exemption requires a record-specific showing of harm, not a categorical claim.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'ongoing investigation',
            'confidential informant', 'endanger', 'pending prosecution', 'active investigation',
            'investigation records', 'law enforcement records',
        ]),
        'counter_arguments': json.dumps([
            'Completed investigations are public — the interference rationale does not apply to closed matters',
            'Arrest records and booking information are public regardless of investigation status',
            'The agency must identify a specific harm per withheld record, not make a broad categorical claim',
            'Factual information that does not reveal informants or investigative techniques must be released',
            'Challenge withholding that extends well beyond any plausible active investigation period',
            'Idaho courts apply a narrow construction to law enforcement exemptions in favor of disclosure',
        ]),
        'notes': 'Idaho courts consistently hold that completed investigation records are public. The law enforcement exemption is strictly limited to active investigations with articulable specific harms. See Boundary County v. Sherwood, 109 Idaho 205 (1985) for the basic framework.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(6)',
        'exemption_number': '§ 74-105(6)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memoranda that are not retained as final agency records and have not been adopted as the agency\'s official position are conditionally exempt.',
        'scope': 'Predecisional working documents — drafts, notes, recommendations, and internal memoranda — that contain opinions on legal or policy questions and have not been adopted as the agency\'s final position. The exemption does NOT cover: (1) purely factual material; (2) documents adopted as final agency positions; (3) "working law" — criteria the agency actually applies; (4) documents shared outside the agency. Factual portions of deliberative documents must be segregated and released. Idaho courts apply the same narrowing principles as other states with deliberative process exemptions.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memo',
            'predecisional', 'working paper', 'recommendations', 'draft document',
            'policy deliberation', 'internal memorandum',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative documents is not exempt — must be segregated and released',
            'Documents adopted as final agency positions are no longer predecisional',
            '"Working law" must be disclosed regardless of its internal format',
            'Challenge claims that entire documents are deliberative when only recommendation portions qualify',
            'External communications lose predecisional character',
            'The agency must show each document is genuinely opinionated and predecisional, not merely label it "draft"',
        ]),
        'notes': 'Idaho\'s deliberative process exemption under § 74-105(6) is interpreted consistently with the federal common law deliberative process privilege. The factual/opinion distinction is the primary limiting principle. Idaho courts have rejected overbroad invocations of this exemption.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(7)',
        'exemption_number': '§ 74-105(7)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or attorney work-product doctrine are exempt from disclosure under the Idaho Public Records Act.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. Standard privilege elements required: lawyer-client relationship, confidential communication, for legal advice. Business and policy advice from attorneys is not covered. Billing records are generally not privileged. Waiver through public disclosure eliminates the protection.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or business guidance',
            'Attorney billing records and invoice descriptions are public',
            'Waiver occurs when the agency cites legal advice in public proceedings',
            'Settlement agreements and consent orders are public once executed',
            'Facts communicated to an attorney are not privileged — only the attorney\'s analysis',
            'Challenge broad claims that all attorney correspondence is exempt',
        ]),
        'notes': 'Idaho courts apply the attorney-client privilege to government entities under standard evidentiary privilege rules. The Idaho Public Records Act\'s strong disclosure mandate narrows the privilege\'s practical reach. Agencies must demonstrate that specific communications meet all privilege elements.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(13)',
        'exemption_number': '§ 74-105(13)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted to state agencies by private parties are exempt from disclosure to protect legitimate competitive interests.',
        'scope': 'Privately submitted information meeting the trade secret or confidential commercial information standard: (1) genuine economic value from secrecy; (2) subject to reasonable protective measures; (3) disclosure would cause competitive harm. Government-generated financial records are not trade secrets. Contract prices and amounts paid with public funds are public. The agency must independently evaluate claims — submitter designations are not controlling.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm',
            'commercial information', 'financial information', 'business information',
            'contract pricing', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Government expenditure amounts are public regardless of vendor confidentiality claims',
            'The submitter must demonstrate actual competitive harm — a "confidential" label is not sufficient',
            'Publicly available information cannot be a trade secret',
            'Information required by law to be submitted has reduced confidentiality expectations',
            'Challenge overbroad designations where entire contracts are marked confidential',
            'Government-generated reports analyzing submitted data are not trade secrets',
        ]),
        'notes': 'Idaho courts apply a narrow construction to trade secret claims consistent with the Public Records Act\'s disclosure mandate. The public expenditure principle — government expenditure data is always public — applies with full force. Agencies must independently analyze trade secret claims rather than deferring to vendor designations.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(2)',
        'exemption_number': '§ 74-105(2)',
        'short_name': 'Medical Records — Individuals',
        'category': 'privacy',
        'description': 'Medical records of identifiable individuals held by government agencies are exempt from public disclosure to protect individual medical privacy.',
        'scope': 'Medical, health, and related personal records of identifiable individuals held by government agencies including corrections, public health, public schools, and social services. The exemption is individual-protective. Agency operational records, contracts with healthcare providers, and aggregate health statistics are public. The exemption tracks HIPAA-protected categories. Aggregate and anonymized health data is not covered by the exemption.',
        'key_terms': json.dumps([
            'medical records', 'health records', 'medical privacy', 'HIPAA',
            'patient records', 'health information', 'protected health information',
            'individual health data',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Agency contracts with healthcare providers and expenditure data are public',
            'Policies about public health programs are public',
            'Challenge overbroad redactions that remove non-medical contextual information',
            'Fitness-for-duty determinations for public officials may be public in appropriate contexts',
        ]),
        'notes': 'Idaho\'s medical records exemption aligns with HIPAA and protects individual patients, not agency operations. Aggregate and de-identified data is not exempt under this provision.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(14)',
        'exemption_number': '§ 74-105(14)',
        'short_name': 'Security Plans — Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and related documents for critical infrastructure and public facilities are exempt where disclosure would create a specific security risk.',
        'scope': 'Specific operational security documents for government buildings, water systems, power infrastructure, transportation networks, and emergency response systems where disclosure would create an articulable security risk. The exemption requires a specific, demonstrable security harm — not merely that records involve security topics. Budget records for security programs, general security policy descriptions, and vendor contracts (excluding specific vulnerability data) are public.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'facility security', 'emergency response',
            'infrastructure protection', 'public safety',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General security policy descriptions are public',
            'Challenge claims that entire vendor contracts are exempt when only specific technical details qualify',
            'Historical security plans from completed projects may not create current security risks',
        ]),
        'notes': 'Idaho\'s security exemption under § 74-105(14) requires agencies to demonstrate specific harm from disclosure. The narrow construction rule applies — agencies may not broadly designate all security-related records as exempt.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-106',
        'exemption_number': '§ 74-106',
        'short_name': 'Public Employee Compensation — Affirmative Disclosure Obligation',
        'category': 'privacy',
        'description': 'Notwithstanding any privacy exemption, Idaho Code § 74-108 requires affirmative disclosure of the name, position title, pay grade, and actual salary of every public employee. This affirmative obligation overrides the personnel record exemption for compensation data.',
        'scope': 'Idaho Code § 74-108 requires agencies to affirmatively maintain and make available records of the name, position title, pay grade, and current salary of every state and local government employee. This is a mandatory disclosure obligation, not a mere exception to an exemption. It means that any privacy or personnel records exemption claim cannot shield basic compensation data. The provision reflects the fundamental principle that how public money is spent on public employees is a matter of public record.',
        'key_terms': json.dumps([
            'public employee compensation', 'salary disclosure', 'pay grade',
            'position title', 'mandatory disclosure', 'Idaho Code § 74-108',
            'public employee salary', 'government pay',
        ]),
        'counter_arguments': json.dumps([
            '§ 74-108 is a mandatory disclosure obligation — it cannot be defeated by a privacy exemption claim',
            'All state and local government employees are covered — there is no "senior official" limitation',
            'Pay grades and salary ranges are public in addition to actual salaries',
            'Historical salary data (past years) is also public under the same principle',
            'Any agency that claims privacy exemption for employee salary data is violating § 74-108',
        ]),
        'notes': 'Idaho Code § 74-108 is a strong affirmative disclosure provision for public employee compensation. It is unusual because it is a mandatory disclosure rule, not merely an exception to an exemption. This provision is one of Idaho\'s most important public accountability tools.',
    },
    {
        'jurisdiction': 'ID',
        'statute_citation': 'Idaho Code § 74-105(3)',
        'exemption_number': '§ 74-105(3)',
        'short_name': 'Student Records — FERPA',
        'category': 'privacy',
        'description': 'Student education records protected under FERPA and Idaho law are exempt from public disclosure to protect student privacy.',
        'scope': 'Education records of identified students at public schools and universities containing personally identifiable information: grades, transcripts, disciplinary records (with limited exceptions), enrollment status. Aggregate statistics, de-identified data, and institutional operational records are public. FERPA compliance is mandatory for institutions receiving federal funds. Directory information policies of individual institutions determine what basic student data is releasable.',
        'key_terms': json.dumps([
            'student records', 'FERPA', 'education records', 'student privacy',
            'transcript', 'disciplinary records', 'personally identifiable',
            'student data', 'enrollment records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics and de-identified student data are public',
            'Institutional operational records are public',
            'Directory information may be releasable depending on institutional policy and student opt-out',
            'Records about school officials are not student records',
        ]),
        'notes': 'Idaho\'s student records exemption incorporates FERPA. Institutions must follow FERPA requirements and may have additional state law protections. The exemption protects identified students, not institutional operations.',
    },
]

# =============================================================================
# RULES
# Idaho Public Records Act, Idaho Code § 74-101 et seq.
# 3 business days to respond (very short). 10-day extension available.
# No administrative appeal. District court enforcement. $0.10/page.
# Attorney's fees for prevailing requesters. Civil penalties available.
# =============================================================================

ID_RULES = [
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'Idaho Code § 74-103(1)',
        'notes': 'Idaho has one of the shortest public records response deadlines in the country: 3 business days from receipt of a written request. Within 3 business days, the agency must either (1) provide access to the records; (2) deny the request with written justification; or (3) provide written notice that a 10-day extension is needed (§ 74-103(2)). The 3-day clock begins when the agency receives the written request. Silence beyond 3 business days without an extension notice constitutes a constructive denial.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'extension_available',
        'param_value': '10_additional_business_days',
        'day_type': 'business',
        'statute_citation': 'Idaho Code § 74-103(2)',
        'notes': 'An agency may extend the response period by up to 10 additional business days if it provides written notice within the initial 3-business-day period. The extension notice must explain the reason for the extension and give a specific date for response. The total maximum response period with extension is 13 business days. Agencies may not stack extensions — one 10-day extension is the maximum. A failure to provide timely extension notice means the 3-day deadline applies without extension.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_per_page',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-102(10)',
        'notes': 'Idaho agencies may charge up to $0.10 per page for paper copies, one of the lower per-page rates among state public records laws. For electronic records, the charge should reflect the actual cost of production — often zero for email delivery. Fees for physical media (CD, USB) may be charged at actual cost. Agencies may not charge for staff time spent searching or redacting — only actual reproduction costs are authorized. If no fee schedule is adopted, the $0.10 default rate applies.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'fee_cap',
        'param_key': 'search_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-102(10)',
        'notes': 'Idaho\'s Public Records Act does not authorize agencies to charge for staff time spent searching for, reviewing, or redacting records. Only actual reproduction costs are permissible. Agencies that add "research fees," "processing fees," or "staff time" charges are imposing costs not authorized by the statute. Requesters should challenge such charges and cite § 74-102(10), which defines permissible fees as the cost of copying.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-102(10)',
        'notes': 'Idaho law does not mandate fee waivers for specific requester categories, but agencies may waive fees at their discretion. Requesters seeking waivers should articulate the public interest served by the disclosure. For electronic records delivered by email, the actual cost is typically zero, making fee waivers less critical for electronic requests.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-115',
        'notes': 'Idaho\'s Public Records Act has NO formal administrative appeal mechanism. There is no agency head review, state ombudsman, or administrative tribunal for denied requests. A requester denied access — or whose request is not answered within the statutory deadline — must go directly to district court under § 74-115. This direct enforcement model means there is no opportunity to resolve disputes without litigation, though informal agency negotiations are always possible before filing suit.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-115',
        'notes': 'A requester denied access may file an enforcement action in the district court of the county where the agency maintains its office. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may order production and award civil penalties and attorney fees. There is no exhaustion requirement before filing suit. Idaho district courts have been willing to enforce disclosure obligations vigorously.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-116',
        'notes': 'Courts may award attorney fees and costs to a requester who substantially prevails in a Public Records Act enforcement action. The award is discretionary. Idaho courts have awarded fees when agencies improperly withheld records without reasonable legal basis. The fee-shifting provision makes judicial enforcement economically viable for requesters with meritorious claims. Fees are not available where the agency had a reasonable basis for withholding.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'penalty',
        'param_key': 'civil_penalties_available',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-116',
        'notes': 'In addition to attorney fees, Idaho courts may award civil penalties against agencies that willfully and wrongfully deny access to public records. Civil penalties are separate from and cumulative with attorney fee awards. The availability of civil penalties is a meaningful deterrent for agencies that routinely deny access without adequate legal justification.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-102(4)',
        'notes': 'Idaho\'s Public Records Act does not require requesters to identify themselves, explain their purpose, or demonstrate any particular interest in the records. The right of access is open to all persons. An agency that conditions access on requester identity or purpose is violating the Act. Contact information for delivery purposes may be requested but must be voluntary.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-104(2)',
        'notes': 'When a record contains both exempt and non-exempt information, Idaho agencies must redact the exempt portions and release the remainder. § 74-104(2) requires that all nonexempt, reasonably segregable portions of records be produced. Blanket withholding of documents containing some exempt content is improper. The agency must describe what has been withheld and the specific exemption claimed.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-104(1)',
        'notes': 'Idaho Code § 74-104(1) establishes a strong presumption that all public records are subject to disclosure. The agency bears the burden of demonstrating that an exemption applies to any withheld record. In enforcement proceedings, the agency must affirmatively establish each claimed exemption applies to each specific withheld record. Idaho courts consistently hold that exemptions must be narrowly construed in favor of disclosure.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial_rule',
        'param_value': 'silence_after_3_business_days_without_extension',
        'day_type': 'business',
        'statute_citation': 'Idaho Code § 74-103(1)',
        'notes': 'Failure to respond within 3 business days without providing a valid extension notice constitutes a constructive denial triggering judicial enforcement rights under § 74-115. Requesters should calendar the 3-business-day deadline carefully — it is one of the shortest deadlines in any state public records law. The constructive denial rule means agencies must respond promptly or risk immediate litigation.',
    },
    {
        'jurisdiction': 'ID',
        'rule_type': 'initial_response',
        'param_key': 'mandatory_salary_disclosure',
        'param_value': 'required_under_section_74-108',
        'day_type': None,
        'statute_citation': 'Idaho Code § 74-108',
        'notes': 'Idaho Code § 74-108 imposes a mandatory affirmative disclosure obligation for public employee compensation data. Agencies must maintain and provide records of the name, position, pay grade, and salary of every public employee. This provision overrides the general personnel record exemption for compensation data. Any claim that employee salary is exempt under a privacy exemption must be rejected as inconsistent with § 74-108\'s mandatory disclosure requirement.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

ID_TEMPLATES = [
    {
        'jurisdiction': 'ID',
        'record_type': 'general',
        'template_name': 'General Idaho Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Idaho Code § 74-101 et seq.

Dear Public Records Custodian:

Pursuant to the Idaho Public Records Act, Idaho Code § 74-101 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format where available.

Regarding fees: under Idaho Code § 74-102(10), the copying fee is up to $0.10 per page for paper copies. I am willing to pay reproduction costs up to ${{fee_limit}}. I am not willing to pay for staff time, research time, or any fee not authorized by the Public Records Act. If costs will exceed ${{fee_limit}}, please notify me before proceeding.

Under Idaho Code § 74-104(1), all public records are presumptively subject to disclosure. The burden of demonstrating any exemption rests on the agency. Under § 74-104(2), all nonexempt, reasonably segregable portions of any record must be released.

If any records or portions are withheld, please: (1) identify each withheld record; (2) cite the specific statutory exemption under Idaho Code § 74-105 et seq. that applies; (3) explain how the exemption applies to the specific record; (4) confirm that nonexempt, segregable portions have been released.

Under Idaho Code § 74-103(1), please respond within 3 business days of receipt of this request. If an extension is needed, please provide written notice within 3 business days specifying a definite response date no more than 10 additional business days away, as required by § 74-103(2). Failure to respond within the statutory period constitutes a constructive denial authorizing judicial enforcement under § 74-115.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the Idaho Public Records Act does not mandate a fee waiver, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records concern {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. For records provided electronically, the actual reproduction cost is zero.

A fee waiver is consistent with the Public Records Act\'s mandate of open access to government information.''',
        'expedited_language': '''I request expedited processing of this Public Records Act request. The 3-business-day deadline under § 74-103(1) already applies. Any production before that deadline is welcome given:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'General-purpose Idaho Public Records Act template. Key ID features: (1) 3 business days to respond — one of the shortest deadlines in the country; (2) 10-day extension available with timely written notice per § 74-103(2); (3) no administrative appeal — district court under § 74-115 is the sole formal remedy; (4) constructive denial after 3 business days without extension notice; (5) $0.10/page copy fee — no staff time charges authorized; (6) attorney fees and civil penalties available for prevailing requesters; (7) mandatory salary disclosure under § 74-108; (8) burden of proof on agency. Reference "Public Records Act" and Idaho Code § 74, not "FOIA."',
    },
    {
        'jurisdiction': 'ID',
        'record_type': 'personnel',
        'template_name': 'Idaho Public Records Act Request — Public Employee Compensation',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Public Employee Compensation Records, Idaho Code § 74-108

Dear Public Records Custodian:

Pursuant to the Idaho Public Records Act, Idaho Code § 74-101 et seq., and specifically the mandatory disclosure requirement of Idaho Code § 74-108, I request the following records relating to public employee compensation:

{{description_of_records}}

This request includes, but is not limited to, for each identified employee or position category:
- Name of each employee
- Position title and job classification
- Pay grade or salary range
- Current annual salary or hourly rate
- Any pay changes (increases, decreases) during the requested period

Idaho Code § 74-108 requires every state and local government agency to maintain and make available this information for all public employees. This is a mandatory disclosure obligation — it is not subject to the general personnel records privacy exemption under § 74-105(4). Any claim that employee compensation data is exempt from disclosure conflicts directly with § 74-108 and should be rejected.

Under Idaho Code § 74-104(1), all public records are presumptively disclosable. The burden of establishing any exemption is on the agency.

Reproduction fees under § 74-102(10) are acceptable up to ${{fee_limit}} at $0.10 per page for paper copies. Electronic delivery at no cost is preferred.

Please respond within 3 business days per § 74-103(1).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. Public employee compensation data is subject to mandatory disclosure under § 74-108 — this is a core public accountability record. Electronic delivery incurs no reproduction cost. A fee waiver is appropriate.''',
        'expedited_language': '''I request prompt processing. These records are subject to mandatory disclosure under § 74-108. I need them by {{needed_by_date}} because {{urgency_explanation}}. The 3-business-day statutory deadline applies.''',
        'notes': 'Idaho public employee compensation template. Idaho Code § 74-108 is a mandatory affirmative disclosure provision — it overrides the general personnel privacy exemption for compensation data. Key points: (1) § 74-108 covers ALL public employees at state and local agencies; (2) name, position title, pay grade, and salary are all mandatory disclosures; (3) privacy exemption claims for compensation data are legally incorrect and should be rejected; (4) 3-business-day response deadline; (5) no administrative appeal; (6) attorney fees available for prevailing requesters.',
    },
    {
        'jurisdiction': 'ID',
        'record_type': 'law_enforcement',
        'template_name': 'Idaho Public Records Act Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Law Enforcement Records, Idaho Code § 74-101 et seq.

Dear Public Records Custodian:

Pursuant to the Idaho Public Records Act, Idaho Code § 74-101 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary records
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Written communications relating to the above

Regarding any claimed exemption under § 74-105(5): Idaho\'s law enforcement exemption requires a specific showing that disclosure of each individual record would: (1) interfere with a pending investigation or prosecution; (2) endanger a specific person\'s life or safety; (3) identify a confidential informant; or (4) deprive a person of a fair trial. Generic assertions that records are "investigative" do not suffice.

[If matter appears concluded:] If no prosecution is currently pending and the investigation is closed, the § 74-105(5) exemption does not apply. Completed investigation files are public records. Please apply this standard.

Under § 74-104(1), all records are presumptively disclosable. Under § 74-104(2), nonexempt, segregable portions must be released. The burden of establishing exemptions is on the agency.

Reproduction fees under § 74-102(10) at $0.10/page are acceptable up to ${{fee_limit}}. Electronic delivery preferred.

Please respond within 3 business days per § 74-103(1). If an extension is needed, please provide written notice within 3 business days per § 74-103(2).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs no reproduction cost. A fee waiver is appropriate given the public interest in this disclosure.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. The 3-business-day deadline under § 74-103(1) applies, and I will calendar it accordingly.''',
        'notes': 'Idaho law enforcement Public Records Act template. Key ID features: (1) § 74-105(5) requires specific harm per record for active investigations only; (2) completed investigations are public; (3) 3-business-day response deadline with 10-day extension option; (4) no administrative appeal — district court under § 74-115; (5) $0.10/page copy fee; (6) attorney fees and civil penalties available; (7) mandatory salary disclosure under § 74-108 applies to law enforcement officer compensation data. Idaho courts apply a narrow construction to law enforcement exemptions in favor of disclosure.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in ID_EXEMPTIONS:
        try:
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
                skipped += 1
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
                added += 1
        except Exception as e:
            errors += 1
            print(f'Error inserting exemption {exemption["short_name"]}: {e}', file=sys.stderr)

    print(f'ID exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in ID_RULES:
        try:
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
        except Exception as e:
            errors += 1
            print(f'Error inserting rule {rule["param_key"]}: {e}', file=sys.stderr)

    print(f'ID rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in ID_TEMPLATES:
        try:
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
        except Exception as e:
            errors += 1
            print(f'Error inserting template {template["template_name"]}: {e}', file=sys.stderr)

    print(f'ID templates: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    total_added = 0
    total_skipped = 0
    total_errors = 0

    try:
        ea, es, ee = build_exemptions(conn)
        ra, rs, re_ = build_rules(conn)
        ta, ts, te = build_templates(conn)

        total_added = ea + ra + ta
        total_skipped = es + rs + ts
        total_errors = ee + re_ + te

        conn.commit()
    except Exception as e:
        total_errors += 1
        print(f'Fatal error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'ID total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_id', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
