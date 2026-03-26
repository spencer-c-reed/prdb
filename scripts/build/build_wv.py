#!/usr/bin/env python3
"""Build West Virginia Freedom of Information Act data: exemptions, rules, and templates.

Covers West Virginia's Freedom of Information Act (FOIA), W. Va. Code § 29B-1-1 et seq.
West Virginia has a 5-business-day response deadline, no administrative appeal, and
enforcement directly in circuit court. $0.25/page copy fee. Reasonable search/retrieval
fees are authorized (distinguishing WV from some states). Attorney's fees for prevailing
requesters.

Run: python3 scripts/build/build_wv.py
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
# W. Va. Code § 29B-1-4 lists the specific categories of records exempt from
# disclosure. The exemptions are construed narrowly — the West Virginia Supreme
# Court has held that FOIA's policy of full disclosure must be given effect and
# exemptions interpreted to avoid unnecessary secrecy. The burden of proving
# an exemption applies is on the public body.
# =============================================================================

WV_EXEMPTIONS = [
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(1)',
        'exemption_number': '§ 29B-1-4(a)(1)',
        'short_name': 'Trade Secrets and Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information obtained from a person that are privileged or confidential are exempt from disclosure under the West Virginia FOIA.',
        'scope': 'Information submitted by private entities to government agencies that: (1) constitutes a genuine trade secret — information deriving economic value from secrecy and subject to reasonable protective measures; or (2) is confidential commercial or financial information whose disclosure would cause competitive harm. Government-generated financial records are not trade secrets. Amounts paid with public funds are public. Agencies must independently evaluate trade secret designations and may not simply defer to submitter labels.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'confidential business',
            'competitive advantage', 'business records', 'contract pricing',
        ]),
        'counter_arguments': json.dumps([
            'Amounts paid under government contracts are public regardless of trade secret claims',
            'Publicly available information cannot be withheld as a trade secret',
            'Information required by law to be submitted has reduced confidentiality expectations',
            'The submitter must demonstrate actual competitive harm — a confidentiality label is not sufficient',
            'Government-generated analysis and reports using submitted data are not themselves trade secrets',
            'Challenge overbroad designations that mark entire contracts as confidential when only specific technical specs qualify',
        ]),
        'notes': 'West Virginia courts apply a narrow construction to FOIA exemptions. The West Virginia Supreme Court has held that trade secret claims require a showing of genuine competitive harm. See Associated Press v. Canterbury, 224 W. Va. 708 (2009) for the foundational analysis of FOIA exemptions.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(2)',
        'exemption_number': '§ 29B-1-4(a)(2)',
        'short_name': 'Personnel Files — Unwarranted Privacy Invasion',
        'category': 'privacy',
        'description': 'Information in personnel files, the disclosure of which would constitute an unreasonable invasion of privacy, is exempt from the West Virginia FOIA.',
        'scope': 'Private personal information in the personnel files of public employees: medical records, home addresses, Social Security numbers, personal financial information, and similar data whose disclosure would cause an unreasonable privacy intrusion. However, names, job titles, salaries, and general employment status of public employees are public. Disciplinary records involving public-facing misconduct are subject to a balancing test that often favors disclosure in the public accountability interest. The "unreasonable invasion" standard requires a balancing of privacy interests against the public interest in disclosure.',
        'key_terms': json.dumps([
            'personnel file', 'employee records', 'privacy invasion', 'personal information',
            'public employee', 'salary', 'disciplinary records', 'performance evaluation',
            'employment records', 'HR records',
        ]),
        'counter_arguments': json.dumps([
            'Public employee names, job titles, and salaries are public — the privacy exemption does not cover core employment data',
            'Disciplinary records resulting in suspension, demotion, or termination involve the public interest and are often public',
            'The "unreasonable invasion" standard requires a balancing test — the privacy interest must outweigh the public accountability interest',
            'Separation agreements and severance payments made with public funds are public',
            'Settlement agreements resolving employee misconduct claims are generally public',
            'Law enforcement officer misconduct records have heightened disclosure requirements',
            'Challenge overbroad claims that entire personnel files are exempt based on one protected data element',
        ]),
        'notes': 'The West Virginia Supreme Court applies a balancing test for personnel file privacy claims. See AFSCME v. Landmark Communications, 182 W. Va. 188 (1989). Public employee conduct in the performance of official duties has a reduced privacy expectation. The "unreasonable" qualifier is key — agencies cannot withhold simply by asserting privacy without showing the disclosure would be genuinely unreasonable.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(3)',
        'exemption_number': '§ 29B-1-4(a)(3)',
        'short_name': 'Test Questions and Scoring Keys',
        'category': 'deliberative',
        'description': 'Test questions, scoring keys, and other examination data used to administer a licensure, employment, or academic examination are exempt to preserve the integrity of future testing.',
        'scope': 'Unpublished test questions, answer keys, and examination forms for professional licensing examinations, civil service employment tests, and academic examinations administered by public agencies or institutions. This exemption protects test integrity — releasing answers would undermine future examinations. Once a specific exam form is retired and no longer in use, the protection may no longer apply. Examination results (i.e., individual scores) may be subject to privacy protections but the exemption here is directed at the test instrument itself, not individual results.',
        'key_terms': json.dumps([
            'test questions', 'scoring key', 'examination data', 'licensure exam',
            'civil service test', 'academic exam', 'exam integrity', 'test bank',
            'employment test', 'examination form',
        ]),
        'counter_arguments': json.dumps([
            'Retired exam forms no longer in active use may not qualify — the secrecy is no longer necessary for test integrity',
            'General examination policies, scoring rubrics, and passing standards are public',
            'Aggregate pass rates, statistical analysis of exam performance, and overall exam results are public',
            'Examining board policies and procedures are public; only the specific test instrument is protected',
        ]),
        'notes': 'This exemption is narrowly targeted at protecting the integrity of active testing instruments. It does not cover examination policies, aggregate results, or the general operation of licensing or employment programs.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(4)',
        'exemption_number': '§ 29B-1-4(a)(4)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or attorney work-product doctrine are exempt from FOIA disclosure in West Virginia.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. Requires: (1) a lawyer-client relationship; (2) a confidential communication; (3) for legal advice purposes. Business and policy advice from attorneys is not covered. Billing records and retainer amounts are generally not privileged. Waiver occurs through disclosure in public proceedings or to non-privileged persons.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'government attorney', 'in-house counsel',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or business guidance',
            'Attorney billing records and invoice descriptions are generally public',
            'Facts communicated to an attorney are not privileged — only the attorney\'s analysis',
            'Waiver: if the agency cited or relied on the legal advice in public decision-making, the privilege is waived',
            'Settlement agreements and consent orders, once executed, are public regardless of the legal advice leading to them',
            'Challenge claims that entire meeting minutes are privileged because an attorney attended',
        ]),
        'notes': 'West Virginia courts apply the attorney-client privilege to government entities with the same standards as private parties. The West Virginia Supreme Court has emphasized that the privilege must not become a tool for agencies to hide decision-making from public scrutiny. FOIA\'s strong disclosure mandate narrows the privilege\'s practical reach.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(5)',
        'exemption_number': '§ 29B-1-4(a)(5)',
        'short_name': 'Law Enforcement — Ongoing Investigation',
        'category': 'law_enforcement',
        'description': 'Information compiled in connection with the investigation of crimes or internal government investigations, if the public interest in law enforcement and orderly administration of justice requires nondisclosure, is exempt from disclosure.',
        'scope': 'Records of ongoing criminal investigations where disclosure would: (1) interfere with pending prosecutorial proceedings; (2) endanger the life or physical safety of an informant or witness; (3) deprive a person of a fair trial; (4) identify a confidential informant; or (5) constitute an unwarranted invasion of personal privacy. Completed investigations do not retain the exemption — once prosecution concludes or the matter is closed, records are generally public. Factual portions of investigation files that do not implicate these harms must be released.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'ongoing investigation',
            'confidential informant', 'endanger', 'pending prosecution', 'internal investigation',
            'crime investigation', 'law enforcement records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a public interest in nondisclosure — agencies must articulate that interest specifically',
            'Completed investigation files are generally public once prosecution concludes',
            'Arrest records, booking information, and incident reports documenting the basic facts of an event are public',
            'Challenge broad withholding where the agency cannot identify a specific enumerated harm',
            'Factual information in investigative files that does not reveal informants or techniques must be segregated and released',
            'Internal government investigations (as opposed to criminal investigations) require a particularly strong showing',
        ]),
        'notes': 'The West Virginia Supreme Court has applied this exemption narrowly, requiring agencies to demonstrate a specific public interest in nondisclosure, not merely assert that records are "investigative." See Ogden Newspapers v. City of Williamstown, 192 W. Va. 648 (1994). Blanket claims of investigative privilege for completed matters have been rejected.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(6)',
        'exemption_number': '§ 29B-1-4(a)(6)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related documents relating to the acquisition, sale, or lease of real property by a public body are exempt prior to completion of the transaction.',
        'scope': 'Formal real property appraisals, feasibility studies, and related valuation documents prepared for a government agency\'s proposed acquisition, sale, or lease of real estate. The exemption is temporary — it expires upon completion, cancellation, or abandonment of the transaction. Post-transaction, all appraisal records are public. The exemption is designed to protect the agency\'s negotiating position, not to create a permanent shield. Budget discussions about property values and informal estimates are generally not covered.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property sale', 'property lease',
            'pre-acquisition', 'property valuation', 'real property', 'condemnation',
            'eminent domain', 'land purchase',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge claims that transactions remain "pending" with no recent activity',
            'Post-transaction appraisals are uniformly public',
            'Budget discussions about general property value ranges are not formal appraisals',
            'After condemnation judgment, all valuation records are public',
        ]),
        'notes': 'West Virginia\'s pre-acquisition appraisal exemption is time-limited by nature. Courts have not allowed agencies to claim indefinitely ongoing transactions to shield completed appraisal records.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(7)',
        'exemption_number': '§ 29B-1-4(a)(7)',
        'short_name': 'Academic and Research Data — In Progress',
        'category': 'deliberative',
        'description': 'Research data, including formulas, patterns, compilations, programs, devices, methods, techniques, or processes that are the subject of research at a public higher education institution, where the release would damage the institution\'s competitive position or ongoing research, may be temporarily exempt.',
        'scope': 'Active research data, unpublished experimental results, formulas, and related materials at public higher education institutions where premature disclosure would damage the institution\'s competitive standing or compromise ongoing research. The exemption is temporary — once research is published, publicly presented, or the project concludes, the exemption no longer applies. Aggregate research statistics, final published research, and grant award information are public. The exemption does not cover institutional operations, administrative records, or research on human subjects (which is subject to separate IRB disclosure obligations).',
        'key_terms': json.dumps([
            'research data', 'academic research', 'unpublished research', 'research formula',
            'competitive research position', 'university research', 'higher education',
            'ongoing research', 'research project', 'laboratory data',
        ]),
        'counter_arguments': json.dumps([
            'Published or publicly presented research is not covered — the exemption is temporary',
            'Grant award amounts and funding sources are public',
            'Institutional research budgets and contracts are public',
            'IRB-approved human subjects research protocols are generally public',
            'Research produced pursuant to a government contract is often publicly funded and should be public',
            'Challenge claims that administrative records about a research program are "research data"',
        ]),
        'notes': 'This exemption protects genuine competitive research interests at public universities. It is narrow and temporary — it does not shield institutional operations or publicly funded completed research from FOIA scrutiny.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(8)',
        'exemption_number': '§ 29B-1-4(a)(8)',
        'short_name': 'Medical and Psychiatric Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, psychological, and similar records of individuals held by government agencies are exempt from FOIA disclosure to protect medical privacy.',
        'scope': 'Personal medical, psychiatric, and psychological records of identifiable individuals held by government agencies including corrections, human services, public schools, and public health departments. The exemption is individual-protective — it does not cover agency operations, contracts with healthcare providers, or aggregate health statistics. Policies about agency healthcare programs are public. The exemption tracks HIPAA-protected categories.',
        'key_terms': json.dumps([
            'medical records', 'psychiatric records', 'psychological records',
            'health information', 'medical privacy', 'HIPAA', 'patient records',
            'mental health records', 'protected health information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Agency contracts with healthcare providers and expenditure data are public',
            'Policies governing public health programs are public',
            'Challenge overbroad redactions that remove non-medical contextual information',
            'A public official\'s fitness for duty may be a matter of public concern in some circumstances',
        ]),
        'notes': 'West Virginia\'s medical records exemption aligns with HIPAA and state privacy law. It protects individual patients, not agency operations. The narrow construction rule applies — agencies must demonstrate that specific records contain protected personal health information.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(9)',
        'exemption_number': '§ 29B-1-4(a)(9)',
        'short_name': 'Security Plans for Government Facilities',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and related records for government facilities and critical infrastructure are exempt where disclosure would create a specific security risk.',
        'scope': 'Specific operational security documents for government buildings, critical infrastructure (water, power, transportation), and emergency response systems. The exemption requires a specific, articulable security risk from disclosure — not merely that records relate to security topics. Budget records for security programs, general descriptions of security policies, and contracts with security vendors (excluding specific technical vulnerability data) are generally public.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'facility security', 'security risk', 'emergency response',
            'public building security', 'infrastructure protection',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies and procedures are public',
            'Challenge claims that entire security contracts are exempt when only specific technical details warrant protection',
            'Physical security plans for non-critical facilities with widely known access patterns do not qualify',
        ]),
        'notes': 'West Virginia courts apply the narrow construction rule to security exemptions. Agencies must demonstrate a specific, articulable harm from disclosure — not merely that the records involve security topics. See State ex rel. Farber v. Mazzone, 213 W. Va. 661 (2003) for the general framework of FOIA exemption analysis.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(10)',
        'exemption_number': '§ 29B-1-4(a)(10)',
        'short_name': 'Welfare and Social Services — Individual Records',
        'category': 'privacy',
        'description': 'Individual records held by the Department of Health and Human Resources relating to public assistance recipients, welfare services, and social services programs are exempt to protect vulnerable individuals.',
        'scope': 'Personal case records of individuals receiving public assistance (welfare, food stamps, Medicaid, child welfare services, foster care) from state social services agencies. The exemption protects vulnerable individuals, not agency operations. Aggregate program statistics, budget records, and agency operational policies are public. Case records may be disclosable in limited circumstances — for example, to the subject of the record or pursuant to court order.',
        'key_terms': json.dumps([
            'welfare records', 'social services records', 'public assistance', 'DHHR',
            'Medicaid records', 'child welfare', 'foster care', 'benefits records',
            'case records', 'recipient records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate program statistics and anonymized data are public',
            'Agency operational policies and procedures are public',
            'Budget records and contracts with service providers are public',
            'Challenge overbroad withholding that conceals systemic program failures under individual privacy claims',
        ]),
        'notes': 'West Virginia\'s social services record exemption reflects the heightened privacy interests of vulnerable populations receiving government assistance. The exemption is individual-protective and does not shield agency operations from accountability.',
    },
    {
        'jurisdiction': 'WV',
        'statute_citation': 'W. Va. Code § 29B-1-4(a)(11)',
        'exemption_number': '§ 29B-1-4(a)(11)',
        'short_name': 'Deliberative Process — Internal Agency Recommendations',
        'category': 'deliberative',
        'description': 'Internal memoranda or letters received or prepared by a public body, to the extent they consist of advice, opinions, and recommendations as part of the deliberative, decision-making process of the public body, are exempt from disclosure.',
        'scope': 'Predecisional internal agency documents containing opinions, recommendations, and policy advice made as part of the agency\'s deliberative process before a final decision is reached. The exemption does NOT cover: (1) purely factual material, even if embedded in a deliberative document; (2) documents adopted as final agency position; (3) "working law" — the actual criteria the agency applies in practice; (4) documents shared outside the agency. Factual portions of deliberative documents must be segregated and released. West Virginia courts strictly limit this exemption.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'internal memorandum', 'agency recommendations',
            'policy deliberation', 'draft document', 'advice and opinions',
            'decision-making process', 'working paper',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative documents is not exempt — must be segregated and released',
            'Documents adopted as final agency position are no longer predecisional',
            '"Working law" — standards and criteria the agency applies in practice — must be disclosed',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'External communications shared outside the agency lose predecisional character',
            'The agency must demonstrate that each specific document is opinionated and predecisional, not merely label it "internal"',
        ]),
        'notes': 'The West Virginia Supreme Court applies the deliberative process exemption narrowly. The factual/opinion distinction is critical. See Cobb v. Department of Finance, 183 W. Va. 570 (1990). Agencies may not use this exemption to shield accountability for administrative decisions.',
    },
]

# =============================================================================
# RULES
# West Virginia FOIA, W. Va. Code § 29B-1-1 et seq.
# 5 business days to respond. Reasonable fees for search and retrieval plus
# $0.25/page for copies — notably different from states that prohibit
# search/retrieval fees. No administrative appeal. Circuit court enforcement.
# Attorney's fees for prevailing requesters.
# =============================================================================

WV_RULES = [
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'W. Va. Code § 29B-1-3(4)',
        'notes': 'West Virginia public bodies must respond to FOIA requests within 5 business days of receipt. Within those 5 days, the public body must either: (1) provide access to the requested records; (2) deny the request with a written explanation; or (3) acknowledge receipt and provide a good-faith estimate of when records will be available. Silence beyond 5 business days is a constructive denial. The 5-day clock begins on the day the request is received by the public body.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'extension_available',
        'param_value': 'yes_with_notice',
        'day_type': 'business',
        'statute_citation': 'W. Va. Code § 29B-1-3(4)',
        'notes': 'A public body may request an extension beyond 5 business days if it provides written notice to the requester explaining the reason for delay and providing a specific date by which records will be produced. Extensions should be reasonable — courts have rejected indefinite or unreasonably long extensions as constructive denials. The extension notice must give a specific production date, not an open-ended acknowledgment.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-3(5)',
        'notes': 'West Virginia agencies may charge up to $0.25 per page for paper copies of public records. For electronic records, the charge should reflect the actual cost of production (often nominal for email delivery). The $0.25 per page rate applies to standard paper copies. Charges for CD/DVD or other physical media may be charged at actual cost of the medium.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'fee_cap',
        'param_key': 'search_retrieval_fee_authorized',
        'param_value': 'reasonable_fee',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-3(5)',
        'notes': 'West Virginia FOIA is notable because it expressly authorizes a "reasonable fee for the search and retrieval" of documents. This distinguishes WV from states like Washington that prohibit search-time fees. However, "reasonable" is a standard courts can police — agencies may not charge fees that are disproportionate to actual costs or that function as a barrier to access. Requesters should challenge fees that appear calculated to deter requests rather than cover genuine costs. Consider requesting a detailed fee breakdown before paying.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-3(5)',
        'notes': 'West Virginia FOIA does not mandate fee waivers for specific requester categories, but agencies may waive fees in their discretion. Requesters seeking waivers should articulate the public interest served by the disclosure, their nonprofit or journalistic status, and the fact that electronic delivery would eliminate reproduction costs. For electronic records delivered by email, the reproduction cost is typically zero, making the fee issue moot for most modern requests.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-5',
        'notes': 'West Virginia FOIA has NO formal administrative appeal mechanism. There is no agency head review, no state ombudsman, and no administrative tribunal. A requester denied access — or whose request receives no response — must go directly to circuit court under § 29B-1-5. This makes West Virginia enforcement simultaneously direct (courts can award fees) and demanding (litigation required). The West Virginia Attorney General\'s office can provide informal guidance but has no binding enforcement authority for FOIA denials.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-5',
        'notes': 'A requester denied access (including a constructive denial through silence or unreasonable delay) may file an enforcement action in circuit court under § 29B-1-5. The court may conduct in camera review of withheld records. The court reviews the denial de novo — no deference to the agency. West Virginia circuit courts have been willing to award fees in contested FOIA cases. Cases may be brought in the circuit court of the county where the public body is located.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-7',
        'notes': 'Courts may award attorney fees and costs to a requester who substantially prevails in a FOIA enforcement action. The award is discretionary (courts "may" award fees), but West Virginia courts have consistently awarded fees when agencies improperly withheld records. The fee-shifting provision makes it economically viable for requesters and their attorneys to enforce FOIA rights even for modest requests. Fees are not available if the public body had a reasonable basis for withholding.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-3',
        'notes': 'West Virginia FOIA does not require requesters to identify themselves or state a purpose for their request. The right of access is open to all persons regardless of identity, citizenship, or stated reason. An agency that conditions access on requester identification or purpose statement is violating FOIA. Contact information for delivery purposes may be requested but must be voluntary.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-4(b)',
        'notes': 'When a document contains both exempt and non-exempt information, West Virginia agencies must redact the exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is improper. § 29B-1-4(b) expressly requires agencies to release all nonexempt portions of records when only part qualifies for an exemption. The agency must identify what has been redacted and why.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-1; § 29B-1-5',
        'notes': 'West Virginia FOIA establishes a strong presumption in favor of disclosure. The burden of demonstrating that any record is exempt is on the public body, not the requester. In any enforcement action, the public body must affirmatively establish that each claimed exemption applies to each specific withheld record. The West Virginia Supreme Court has consistently held that exemptions must be construed narrowly to effectuate FOIA\'s purpose of open government.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'W. Va. Code § 29B-1-3(4)',
        'notes': 'When a public body denies a FOIA request, it must provide a written denial stating the legal basis for the denial with specificity. A vague denial citing broad exemption categories is insufficient. The requester is entitled to know the specific statutory basis for each withholding so they can evaluate whether to pursue judicial enforcement. Failure to provide a written denial with statutory citation may support an inference that the denial lacks legal basis.',
    },
    {
        'jurisdiction': 'WV',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial_rule',
        'param_value': 'silence_after_5_days',
        'day_type': 'business',
        'statute_citation': 'W. Va. Code § 29B-1-3(4)',
        'notes': 'A public body that fails to respond within 5 business days without providing an extension notice is deemed to have constructively denied the request. A constructive denial triggers the requester\'s right to seek judicial enforcement in circuit court under § 29B-1-5 without waiting for a formal written denial. Requesters should calendar the 5-day deadline and file suit promptly if it passes without response.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

WV_TEMPLATES = [
    {
        'jurisdiction': 'WV',
        'record_type': 'general',
        'template_name': 'General West Virginia FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — W. Va. Code § 29B-1-1 et seq.

Dear FOIA Officer:

Pursuant to the West Virginia Freedom of Information Act, W. Va. Code § 29B-1-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes both reproduction costs and production time.

Regarding fees: I am willing to pay the reasonable reproduction fee of up to $0.25 per page for paper copies per W. Va. Code § 29B-1-3(5). I acknowledge that West Virginia FOIA also authorizes a reasonable search and retrieval fee. However, any such fee must be genuinely reasonable and proportionate to actual costs — fees calculated to deter access rather than recover costs would be improper. If total fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under W. Va. Code § 29B-1-1, all public records are presumptively open to inspection. The burden of demonstrating that any record is exempt rests on the public body. Under § 29B-1-4(b), all nonexempt, reasonably segregable portions of any record must be released regardless of any claimed exemption.

If any records or portions are withheld, please: (1) identify each withheld record; (2) cite the specific statutory exemption under W. Va. Code § 29B-1-4(a) that applies; (3) explain how the exemption applies to the specific record; and (4) confirm that nonexempt, segregable portions have been released.

Under W. Va. Code § 29B-1-3(4), please respond within 5 business days of receipt of this request. Silence beyond that period constitutes a constructive denial that I will treat as authorizing immediate circuit court action under § 29B-1-5.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that fees be waived for this request. While West Virginia FOIA does not mandate a fee waiver, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records concern {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. For records delivered electronically, both reproduction and search costs are minimal or zero.

A fee waiver is consistent with FOIA\'s purpose of ensuring open access to government information.''',
        'expedited_language': '''I request expedited processing of this FOIA request. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if any clarification would allow faster processing.

Note: The 5-business-day deadline under § 29B-1-3(4) already applies to this request.''',
        'notes': 'General-purpose West Virginia FOIA template. Key WV features: (1) 5 business days to respond — per § 29B-1-3(4); (2) no administrative appeal — go directly to circuit court under § 29B-1-5 if denied; (3) constructive denial rule — silence after 5 business days = denial; (4) search and retrieval fees authorized (unique among states) but must be reasonable; (5) $0.25/page for paper copies; (6) attorney fees available for prevailing requesters; (7) segregability required under § 29B-1-4(b); (8) burden of proof on agency. Reference "FOIA" and W. Va. Code § 29B-1, not "IPRA" or federal FOIA.',
    },
    {
        'jurisdiction': 'WV',
        'record_type': 'law_enforcement',
        'template_name': 'West Virginia FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: FOIA Request — Law Enforcement Records, W. Va. Code § 29B-1-1 et seq.

Dear FOIA Officer:

Pursuant to the West Virginia Freedom of Information Act, W. Va. Code § 29B-1-1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary and complaint records
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Written communications relating to the above

Regarding any claimed exemption under § 29B-1-4(a)(5): West Virginia FOIA requires that the public body demonstrate a specific public interest in nondisclosure — a general assertion that records are "investigative" is insufficient. Each withheld record must implicate a specific enumerated harm: endangering a person, identifying an informant, interfering with a pending prosecution, or creating an invasion of personal privacy. General claims do not suffice.

[If matter appears concluded:] If no prosecution is currently pending and the investigation is closed, the investigation exemption under § 29B-1-4(a)(5) does not apply. Completed investigation files are public records and must be produced.

Under § 29B-1-1, the presumption favors disclosure. Under § 29B-1-4(b), nonexempt, segregable portions of withheld records must be released. The burden of establishing any exemption rests on the public body.

Reasonable fees under § 29B-1-3(5) are acceptable up to ${{fee_limit}}.

Please respond within 5 business days per § 29B-1-3(4).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery minimizes reproduction and search costs. A fee waiver is appropriate given the public interest served.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. The 5-business-day deadline under § 29B-1-3(4) applies, and I will calendar it accordingly.''',
        'notes': 'West Virginia law enforcement FOIA template. WV-specific features: (1) § 29B-1-4(a)(5) requires a specific public interest in nondisclosure — not a blanket protection for all police records; (2) completed investigation files are public; (3) search and retrieval fees are authorized (unusual among states) — challenge unreasonable amounts; (4) $0.25/page copy fee; (5) 5 business days to respond; (6) no administrative appeal — circuit court under § 29B-1-5; (7) attorney fees available. The West Virginia Supreme Court has consistently rejected broad law enforcement exemption claims in favor of disclosure.',
    },
    {
        'jurisdiction': 'WV',
        'record_type': 'government_contracts',
        'template_name': 'West Virginia FOIA Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: FOIA Request — Government Contracts and Expenditures, W. Va. Code § 29B-1-1 et seq.

Dear FOIA Officer:

Pursuant to the West Virginia Freedom of Information Act, W. Va. Code § 29B-1-1 et seq., I request copies of the following records relating to government expenditures and contracts:

{{description_of_records}}

Relating to: {{vendor_or_contract_subject}}
Date range: {{date_range_start}} through {{date_range_end}}

This request includes, but is not limited to:
- Executed contracts, amendments, and task orders
- Request for proposals (RFPs), solicitation documents, and bid tabulations
- Records of payments made under the identified contracts
- Vendor evaluation and selection records
- Correspondence relating to contract performance, disputes, or modifications

I anticipate that the responding agency may claim trade secret or commercial information protection under § 29B-1-4(a)(1) for portions of these records. Please be advised:

Amounts paid with public funds are public regardless of any trade secret claim — government expenditure data is not commercially sensitive information protected by FOIA. Only specific, legitimately proprietary technical information (e.g., formulas, specific process details) may qualify. Blanket confidentiality designations by vendors do not constitute a legal basis for withholding.

Under § 29B-1-4(b), all nonexempt, segregable portions of withheld records must be released. Under § 29B-1-1, the presumption favors disclosure. The burden of establishing any exemption is on the public body.

Reasonable fees under § 29B-1-3(5) are acceptable up to ${{fee_limit}}, including a reasonable search and retrieval fee. Please notify me of fee estimates before incurring significant costs.

Please respond within 5 business days per § 29B-1-3(4).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. Government contract and expenditure records are matters of core public accountability — taxpayers are entitled to know how public funds are spent. I am {{requester_category_description}}. Electronic delivery minimizes reproduction costs. A fee waiver is appropriate.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if any clarification would expedite production.''',
        'notes': 'West Virginia government contracts FOIA template. Key issues: (1) trade secret exemption (§ 29B-1-4(a)(1)) is frequently over-invoked by agencies and vendors — this template anticipates and pushes back on it; (2) government expenditure amounts are always public regardless of vendor confidentiality claims; (3) search and retrieval fees are authorized under WV law — factor this into fee cap and consider challenging unreasonable charges; (4) 5 business days to respond; (5) circuit court enforcement under § 29B-1-5.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in WV_EXEMPTIONS:
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

    print(f'WV exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in WV_RULES:
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

    print(f'WV rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in WV_TEMPLATES:
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

    print(f'WV templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'WV total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_wv', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
