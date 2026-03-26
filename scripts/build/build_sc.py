#!/usr/bin/env python3
"""Build South Carolina Freedom of Information Act data: exemptions, rules, and templates.

Covers South Carolina's Freedom of Information Act, S.C. Code § 30-4-10 et seq.
South Carolina has a moderately strong public records law with a 15-business-day
response deadline (recently extended from 10), a 10-business-day extension option,
attorney's fees, civil penalties, and circuit court enforcement. No administrative
appeal process. Courts apply a balancing test for some exemptions.

Run: python3 scripts/build/build_sc.py
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
# S.C. Code § 30-4-40 provides the list of exemptions from the FOIA.
# South Carolina courts apply a strict construction against the agency claiming
# an exemption consistent with § 30-4-15's mandate that the FOIA be "liberally
# construed." The agency bears the burden of proving each exemption. Some
# exemptions require a balancing of public interest against privacy interest.
# =============================================================================

SC_EXEMPTIONS = [
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(1)',
        'exemption_number': '§ 30-4-40(a)(1)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information received from a person or business are exempt where disclosure would provide competitive advantage or harm the submitting entity\'s competitive position.',
        'scope': 'Applies to commercial or financial information submitted to a government body by a private entity that qualifies as a trade secret under South Carolina law or whose disclosure would cause competitive harm. Does not protect government-generated records or amounts paid with public funds. The submitter must demonstrate that the information actually qualifies as a trade secret or confidential commercial information — a "confidential" stamp alone is not sufficient. Contract prices paid with public funds are generally public.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm', 'commercial information',
            'financial information', 'confidential business', 'competitive position',
            'economic value', 'trade secret misappropriation',
        ]),
        'counter_arguments': json.dumps([
            'Amounts paid with public funds are public regardless of vendor trade secret claims',
            'The submitter must demonstrate actual competitive harm from disclosure — a general claim is insufficient',
            'Publicly available information cannot qualify as a trade secret',
            'The agency, not the submitter, decides whether to withhold — agencies may not defer entirely to vendor confidentiality demands',
            'Challenge whether the submitter maintained the information in confidence — prior public disclosure defeats the trade secret claim',
            'Contract terms, deliverables, and performance metrics are public even if underlying pricing formulas are protected',
        ]),
        'notes': 'South Carolina courts construe the trade secret exemption narrowly in keeping with § 30-4-15\'s liberal construction mandate. Contract amounts and expenditure data paid with public funds are uniformly held to be public. Courts require the claiming party to demonstrate specific competitive harm, not just assert confidentiality.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(2)',
        'exemption_number': '§ 30-4-40(a)(2)',
        'short_name': 'Personal Privacy — Unwarranted Invasion',
        'category': 'privacy',
        'description': 'Information of a personal nature where disclosure would constitute an unreasonable invasion of privacy is exempt. The exemption requires a balancing test weighing the public interest in disclosure against the privacy interest in withholding.',
        'scope': 'Personal information where disclosure would be an unreasonable invasion of personal privacy, balanced against the public interest in disclosure. The exemption does not automatically protect all personal information in government records. South Carolina courts apply a multi-factor balancing test. Public employees\' information related to their official duties has reduced privacy protection. Home addresses, medical information, and personal financial data unrelated to public employment generally receive stronger protection. The exemption cannot be used to shield public employees from accountability for their exercise of governmental authority.',
        'key_terms': json.dumps([
            'personal privacy', 'unreasonable invasion', 'personal information',
            'public employee privacy', 'home address', 'medical information',
            'balancing test', 'privacy interest', 'public interest',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires an "unreasonable" invasion of privacy — public employees\' official conduct does not meet this standard',
            'The balancing test favors disclosure when the public interest in accountability outweighs the privacy interest',
            'Salary, job title, and official duties of public employees are not protected by this exemption',
            'Challenge overbroad redactions where personal identifying information has been removed along with clearly public information',
            'The agency bears the burden of demonstrating that the specific privacy interest outweighs the public interest in disclosure',
            'Information that is already publicly available cannot be withheld on privacy grounds',
        ]),
        'notes': 'The South Carolina privacy exemption requires a genuine balancing test under § 30-4-40(a)(2). Courts have held that public employees\' official conduct is subject to full disclosure and that privacy interests must specifically and substantially outweigh the public interest. See Burton v. York County Sheriff\'s Dep\'t, 358 S.C. 339 (Ct. App. 2004).',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(3)',
        'exemption_number': '§ 30-4-40(a)(3)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement agencies compiled for law enforcement purposes are exempt where production would interfere with enforcement proceedings, deprive a person of a fair trial, identify a confidential source, reveal investigative techniques, or endanger law enforcement personnel.',
        'scope': 'Law enforcement investigation records compiled for law enforcement purposes where disclosure would cause one of the enumerated harms: interference with proceedings, fair trial deprivation, confidential source identification, investigative technique disclosure, or endangerment. The exemption applies only to records compiled for law enforcement purposes — not all records held by law enforcement agencies. Routine administrative records of law enforcement agencies are public. Completed investigation files are generally public once the case is closed. Incident reports and arrest records documenting the existence of criminal events are public.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'active investigation', 'pending prosecution',
            'enforcement proceedings', 'law enforcement records', 'undercover operation',
        ]),
        'counter_arguments': json.dumps([
            'The exemption does not cover all records held by law enforcement — only records compiled for law enforcement purposes',
            'Incident reports, arrest records, and booking information are public regardless of the investigation status',
            'Once prosecution is complete or investigation closed, the interference rationale evaporates',
            'The agency must identify the specific enumerated harm for each withheld record — a generic "active investigation" response is insufficient',
            'Administrative records, payroll, and budget documents of law enforcement agencies are public',
            'Challenge claims that body camera footage is exempt — it must be produced with only specific sensitive portions redacted',
        ]),
        'notes': 'South Carolina courts strictly construe the law enforcement exemption against the agency. The exemption requires a showing of specific, articulable harm from disclosure of particular records, not a categorical assertion that all investigation records are protected. See Howard v. South Carolina Dep\'t of Corrections, 399 S.C. 618 (2012).',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(4)',
        'exemption_number': '§ 30-4-40(a)(4)',
        'short_name': 'Medical and Clinical Records',
        'category': 'privacy',
        'description': 'Medical records and similarly sensitive personal health information held by government agencies are exempt from disclosure to protect patient privacy. The exemption applies to individually identifiable health information.',
        'scope': 'Individually identifiable medical, clinical, psychological, and health records held by government agencies including public hospitals, health departments, correctional facilities, and other government entities. Aggregate health statistics, de-identified data, and public health program information are not covered. The policies and procedures of public health agencies are public. Budget and administrative records of health agencies are public. The exemption aligns with federal HIPAA requirements for covered entities.',
        'key_terms': json.dumps([
            'medical record', 'clinical record', 'patient privacy', 'HIPAA',
            'individually identifiable', 'health information', 'medical treatment',
            'health record', 'mental health record', 'prescription record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health data and de-identified statistics are not covered',
            'Policies and procedures of public health agencies are public',
            'Budget and administrative records of health agencies are fully public',
            'Challenge whether specific records actually contain individually identifiable health information',
            'Information about health programs and services (distinct from individual patient records) is public',
        ]),
        'notes': 'South Carolina\'s medical records exemption protects individually identifiable health information. The exemption is consistent with HIPAA requirements. It does not shield the operations of public health agencies from scrutiny.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(5)',
        'exemption_number': '§ 30-4-40(a)(5)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between a public body and its attorney when the public body is a party to actual or prospective litigation, or where the communication is a confidential legal communication between the public body and its attorney, are exempt.',
        'scope': 'Confidential attorney-client communications made for the purpose of obtaining legal advice, and work product prepared in anticipation of actual or prospective litigation. South Carolina\'s FOIA attorney-client exemption is narrower than some states: it applies specifically to litigation-related communications and confidential legal communications. Routine legal advice on general agency operations may have reduced protection. Attorney billing records and retainer agreements are generally public. Facts independently known are not protected merely because communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'legal communication', 'litigation',
            'attorney work product', 'legal advice', 'prospective litigation',
            'confidential communication', 'government attorney', 'public body counsel',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is specifically limited to litigation-related and confidential legal communications — routine policy advice may not be protected',
            'Attorney billing records and retainer agreements are generally public',
            'Waiver occurs when the agency uses the legal advice in public decision-making or discloses it to third parties',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis',
            'Challenge claims that all communications with outside counsel are privileged',
        ]),
        'notes': 'South Carolina\'s attorney-client FOIA exemption under § 30-4-40(a)(5) is specifically tied to litigation and confidential legal communications. Courts have held that the exemption does not protect all communications with attorneys — only those that are both confidential and legal (not business) advice.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(6)',
        'exemption_number': '§ 30-4-40(a)(6)',
        'short_name': 'Personnel Files — Employee Privacy',
        'category': 'privacy',
        'description': 'Personnel files of public employees are exempt from public disclosure to the extent they contain information whose disclosure would constitute an unreasonable invasion of personal privacy. The exemption protects private personal information but does not shield accountability records.',
        'scope': 'Personnel files containing personal information such as medical history, home address, personal financial data, and similar private data. Does not protect information directly related to the employee\'s official public duties: salary, job title, disciplinary records for official misconduct, termination decisions, and similar accountability information are public. South Carolina courts apply the same unreasonable-invasion balancing test as the general privacy exemption. Public employees acting in their official capacities have reduced privacy expectations.',
        'key_terms': json.dumps([
            'personnel file', 'employee privacy', 'personal information', 'disciplinary record',
            'salary', 'job title', 'public employee', 'unreasonable invasion',
            'home address', 'employment record',
        ]),
        'counter_arguments': json.dumps([
            'Salary, title, dates of employment, and job description are public regardless of the personnel file exemption',
            'Disciplinary records for official misconduct are public accountability records, not protected private information',
            'The exemption requires an "unreasonable invasion of personal privacy" — a balancing test that favors disclosure for public employment actions',
            'Challenge overbroad redactions where the agency has removed clearly public accountability information along with private data',
            'Request a specific list of what was withheld and under what exemption subsection',
        ]),
        'notes': 'South Carolina applies the unreasonable invasion of privacy test to personnel files. Courts have consistently held that disciplinary records of public employees performing public duties are public. The exemption protects truly private personal information, not records of official conduct.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(7)',
        'exemption_number': '§ 30-4-40(a)(7)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary and draft documents, preliminary advisory opinions, recommendations, and minutes of preliminary deliberations are exempt before the body takes final action, to protect candid internal deliberations. Final agency decisions and adopted policies are public.',
        'scope': 'Internal draft documents, preliminary advisory opinions, recommendations, and records of preliminary deliberations before a public body takes final action. The exemption is predecisional — it expires when the agency adopts a final position. Factual material within deliberative documents must be segregated and released. Final decisions, adopted policies, and records of what the agency decided are fully public. South Carolina courts construe this exemption narrowly and require the agency to demonstrate that the specific document is both predecisional and deliberative.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'advisory opinion',
            'internal deliberation', 'draft document', 'recommendation', 'working paper',
            'preliminary minutes', 'intra-agency communication',
        ]),
        'counter_arguments': json.dumps([
            'Once a draft or recommendation is adopted as the agency\'s final position, the exemption expires',
            'Factual material within deliberative documents must be released — only opinion and recommendation portions are protected',
            '"Working law" applied to the public must be disclosed even if in internal documents',
            'Challenge claims that entire documents are deliberative — only the opinion/recommendation portions qualify',
            'Communications circulated to persons outside the agency may lose predecisional character',
            'Final minutes of public body meetings are public regardless of this exemption',
        ]),
        'notes': 'South Carolina\'s deliberative process exemption is strictly construed under the FOIA\'s liberal construction mandate. Courts have held that the exemption is predecisional only — it expires when the agency acts. Factual material must be segregated and released.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(8)',
        'exemption_number': '§ 30-4-40(a)(8)',
        'short_name': 'Security Plans and Infrastructure Vulnerability',
        'category': 'safety',
        'description': 'Records revealing specific details of security plans for critical infrastructure, public buildings, and emergency response systems are exempt where disclosure would create a specific security risk.',
        'scope': 'Security plans, vulnerability assessments, access protocols, and similar operational security records for critical public infrastructure (water, power, transportation) and public buildings where disclosure of specific details would enable exploitation of identified vulnerabilities. The exemption requires specific, articulable risk — not speculative or general security concerns. Budget records, contracts, and general descriptions of security programs are public.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'access protocol', 'infrastructure protection',
            'emergency response plan', 'public building security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable — general security concerns are insufficient',
            'Budget records for security programs are public',
            'General descriptions of security policies that do not identify specific vulnerabilities are not covered',
            'Challenge claims that all records from a security department are exempt',
        ]),
        'notes': 'South Carolina\'s security exemption requires the agency to demonstrate specific, articulable risk from disclosure of particular records. General assertions that records are "security-related" are not sufficient.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(9)',
        'exemption_number': '§ 30-4-40(a)(9)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and valuation records prepared for government acquisition or sale of real property are exempt until the transaction is completed or the agency\'s interest in the property terminates.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuations prepared for the purpose of negotiating acquisition or disposal of real property. The exemption is time-limited: it expires automatically when the transaction closes or is abandoned. Post-transaction, all appraisal and valuation records are public. Does not cover general budget discussions about property programs.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'pre-acquisition', 'real property', 'land purchase', 'feasibility study',
            'property sale', 'condemnation',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction closes or is abandoned',
            'Challenge the claim that a transaction is "pending" if no action has been taken for an extended period',
            'Post-transaction appraisals are fully public',
            'General budget discussions about property are not formal appraisals',
        ]),
        'notes': 'South Carolina\'s pre-acquisition appraisal exemption is time-limited. It exists to prevent the agency from being disadvantaged in negotiations — not to permanently shield valuation records.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(10)',
        'exemption_number': '§ 30-4-40(a)(10)',
        'short_name': 'Computer Software Programs',
        'category': 'commercial',
        'description': 'Computer programs used or developed by a public body are exempt where the programs constitute proprietary information. Records produced using those programs remain public.',
        'scope': 'Source code, compiled programs, and software developed by or for a government agency that constitutes proprietary software. The exemption is narrow: it applies to the programs themselves, not to records created by or maintained in those programs. A database program may be exempt, but the records stored in that database (personnel records, financial records, etc.) are not exempt merely because they are stored in proprietary software. The exemption is frequently overextended by agencies to shield records stored in proprietary systems.',
        'key_terms': json.dumps([
            'computer program', 'proprietary software', 'source code', 'software',
            'computer system', 'database software', 'program code',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers the program itself, not the records stored in the program',
            'Challenge claims that entire databases are exempt — only the software code qualifies, not the data stored in it',
            'Records produced by government operations and stored in proprietary systems are public regardless of the software exemption',
            'Government-developed software is particularly unlikely to qualify as "proprietary" — it was developed with public funds',
        ]),
        'notes': 'South Carolina courts have held that the computer program exemption applies only to the software code itself, not to government records stored in or produced by those programs. Agencies may not use this exemption to withhold databases containing public records.',
    },
    {
        'jurisdiction': 'SC',
        'statute_citation': 'S.C. Code § 30-4-40(a)(12)',
        'exemption_number': '§ 30-4-40(a)(12)',
        'short_name': 'Library Patron Circulation Records',
        'category': 'privacy',
        'description': 'Library circulation records identifying what individual patrons have borrowed or accessed at publicly funded libraries are exempt to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying which specific patrons borrowed, accessed, or inquired about specific library materials. Covers circulation records, database access logs, interlibrary loan requests, and similar patron-specific records. Library administrative records, budget documents, collection statistics, and programming records are public.',
        'key_terms': json.dumps([
            'library circulation', 'library patron', 'borrower records', 'reading privacy',
            'intellectual privacy', 'library records', 'database access',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library statistics and collection data are not covered',
            'Library administrative and budget records are fully public',
            'Records required by court order may be disclosed',
        ]),
        'notes': 'South Carolina\'s library patron privacy exemption reflects the standard American library confidentiality norm. It is narrow — it protects patron-specific reading records, not library operations.',
    },
]

# =============================================================================
# RULES
# South Carolina Freedom of Information Act, S.C. Code § 30-4-10 et seq.
# Key features: 15-business-day response deadline (extended from 10);
# 10-business-day extension; $0.25/page; no administrative appeal;
# circuit court enforcement; attorney's fees + civil penalties up to $1,500
# per violation plus $500/day for continuing violations.
# =============================================================================

SC_RULES = [
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'S.C. Code § 30-4-30(C)',
        'notes': 'South Carolina requires a public body to respond to a FOIA request within 15 business days of receipt of a written request. This deadline was extended from 10 business days by legislative amendment. The response must either: (1) make the records available for inspection or provide copies; or (2) deny the request in writing with the specific statutory basis for denial. Failure to respond within 15 business days is itself a FOIA violation. The 15-day deadline begins when the public body receives the written request.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'extension_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'S.C. Code § 30-4-30(C)',
        'notes': 'A public body may extend the 15-business-day response deadline by an additional 10 business days (total of up to 25 business days) if the request is voluminous or requires extensive research. The extension requires written notice to the requester specifying: (1) the reason the extension is needed; and (2) the estimated date records will be available. The extension notice must be provided before the original 15-day deadline expires. Extensions are not automatic — a failure to provide timely notice of extension means the original 15-day deadline controls.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(B)',
        'notes': 'South Carolina allows public bodies to charge up to $0.25 per page for paper copies of records. For records in electronic format that can be delivered by email or electronic medium, the agency may charge only the actual cost of the electronic medium, which is typically zero for email delivery. Agencies may not charge for staff time spent locating, reviewing, or redacting records under the standard fee provision. Extraordinary costs for large-scale requests may be negotiated, but standard requests are subject to the $0.25/page cap.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(B)',
        'notes': 'South Carolina FOIA does not mandate fee waivers but public bodies have discretion to reduce or waive fees. Requesters may argue fee waivers are appropriate when records are of significant public interest, when electronic delivery eliminates reproduction costs, or when the requester is a journalist, nonprofit, or academic. The FOIA\'s liberal construction mandate supports fee waivers that advance public access.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-100',
        'notes': 'South Carolina FOIA has NO administrative appeal mechanism. There is no agency head review, no state ombudsman, and no administrative tribunal for FOIA appeals. A requester denied access must go directly to the circuit court under § 30-4-100. This requires filing a civil action, which is more expensive and time-consuming than states with AG-level administrative review. However, the availability of attorney fees and civil penalties makes court enforcement viable for significant denials.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-100',
        'notes': 'Any person denied access to a public record may bring a civil action in the circuit court of the county where the record is kept. The court reviews the denial de novo and may order production of the records. The court may award attorney fees, litigation costs, and civil penalties. Cases should be brought promptly — unreasonable delay in seeking enforcement may affect the court\'s assessment of the denial\'s ongoing harm. The court may conduct in camera review of withheld records.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_per_violation',
        'param_value': 'up to $1,500',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-110',
        'notes': 'South Carolina allows courts to impose civil penalties up to $1,500 per violation against a public body that wrongfully withholds records. Additionally, for continuing violations (ongoing refusal to produce records), penalties may accrue at $500 per day. The civil penalty is distinct from attorney fees — a requester may recover both. The $1,500 per-violation amount is relatively modest compared to states with per diem penalties that accumulate over time, but the $500/day continuing violation penalty can become significant for prolonged withholding.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-100',
        'notes': 'Courts may award attorney fees and other litigation costs to a requester who prevails in a FOIA enforcement action. The fee award is discretionary — courts consider whether the agency had a reasonable basis for its denial, whether the denial was willful, and the public benefit served by disclosure. Attorney fees in combination with civil penalties provide meaningful incentive for agencies to comply with FOIA requirements.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(D)',
        'notes': 'When a public body denies a FOIA request, the denial must be in writing and must cite the specific provision of § 30-4-40 (or other applicable statute) relied upon as the exemption. A denial without a specific statutory citation is procedurally deficient. Requesters should insist on written denials with specific statutory citations — this is essential to evaluating and challenging the denial in court.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(A)',
        'notes': 'When a record contains both exempt and non-exempt portions, the public body must allow access to the non-exempt portions. The agency must segregate and release all non-exempt material. Blanket withholding of documents containing some exempt content is a FOIA violation. The agency bears the burden of identifying what is specifically exempt and must release the remainder.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-15',
        'notes': 'Under § 30-4-15\'s liberal construction mandate, the burden of demonstrating that any exemption applies rests entirely on the public body. Courts apply a strict construction of exemptions against the agency claiming them. A public body may not simply assert a general exemption category — it must demonstrate that the specific record falls within the specific exemption.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'written_request_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(A)',
        'notes': 'South Carolina FOIA requires requests to be in writing. Oral requests do not trigger the formal response deadlines. Written requests should identify the records with reasonable particularity. The writing requirement makes South Carolina slightly more formalistic than states that accept oral requests, but in practice email requests satisfy the written requirement. Agencies may not require requesters to use a specific form — any written communication identifying the records sought is sufficient.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(A)',
        'notes': 'South Carolina does not require requesters to identify themselves or state the purpose of their FOIA request. Any citizen of South Carolina may request public records — however, the statute does reference "citizens" which could theoretically limit access for non-residents. In practice, South Carolina agencies routinely respond to requests from non-residents and this limitation is rarely enforced. Contact information for delivery purposes is appropriate but may not be required as a condition of access.',
    },
    {
        'jurisdiction': 'SC',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_available',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'S.C. Code § 30-4-30(B)',
        'notes': 'Public bodies must provide records in the format requested where practicable, including electronic formats. If a record exists in electronic form, the requester may request electronic delivery, which typically eliminates per-page copying fees. Agencies are not required to create new records or produce records in formats they do not use, but existing electronic records must be provided electronically upon request.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

SC_TEMPLATES = [
    {
        'jurisdiction': 'SC',
        'record_type': 'general',
        'template_name': 'General South Carolina FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Freedom of Information Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — S.C. Code § 30-4-30

Dear Freedom of Information Officer:

Pursuant to the South Carolina Freedom of Information Act, S.C. Code § 30-4-10 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which eliminates per-page copying fees and expedites production.

For paper copies, I am willing to pay up to $0.25 per page per S.C. Code § 30-4-30(B). If the estimated total fee will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment. I am not willing to pay for staff time spent locating or reviewing records.

Under S.C. Code § 30-4-15, the FOIA must be liberally construed to ensure access to public records. The burden of proving any exemption applies rests on {{agency_name}}. Under S.C. Code § 30-4-30(A), any record containing both exempt and non-exempt portions must be produced with only the specifically exempt portions withheld — the non-exempt portions must be made available.

If any records or portions of records are withheld, I request a written denial per S.C. Code § 30-4-30(D) that: (1) identifies each withheld record; (2) cites the specific subsection of § 30-4-40 or other statute relied upon; (3) describes the record with sufficient detail to evaluate the claimed exemption; and (4) confirms that all non-exempt, segregable portions have been provided.

Per S.C. Code § 30-4-30(C), please respond within 15 business days. If an extension is necessary, please provide written notice within the 15-day period stating the reason and the estimated date of availability.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the South Carolina FOIA does not mandate fee waivers, {{agency_name}} has discretion to reduce or waive fees. A fee waiver is appropriate here because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. To the extent records are available in electronic form and can be delivered by email, the actual cost is zero, making a fee waiver consistent with the spirit of § 30-4-30(B).

South Carolina FOIA's liberal construction mandate under § 30-4-15 supports a fee waiver that removes barriers to public access.''',
        'expedited_language': '''I request that this FOIA request be processed as promptly as possible within the 15-business-day deadline under § 30-4-30(C). Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if questions would allow faster processing.''',
        'notes': 'General-purpose South Carolina FOIA template. Key features: (1) 15-business-day response deadline with 10-day extension option (§ 30-4-30(C)); (2) written request required; (3) written denial with specific statutory citation required (§ 30-4-30(D)); (4) no administrative appeal — go directly to circuit court (§ 30-4-100); (5) civil penalties up to $1,500/violation plus $500/day continuing (§ 30-4-110); (6) attorney fees available for prevailing requester; (7) $0.25/page maximum. Cite "South Carolina FOIA" and § 30-4, not "FOIL" or federal FOIA.',
    },
    {
        'jurisdiction': 'SC',
        'record_type': 'law_enforcement',
        'template_name': 'South Carolina FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Freedom of Information Officer
{{agency_name}}
{{agency_address}}

Re: South Carolina FOIA Request — Law Enforcement Records, S.C. Code § 30-4-30

Dear Freedom of Information Officer:

Pursuant to the South Carolina Freedom of Information Act, S.C. Code § 30-4-10 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Internal investigation records for this matter

Regarding claimed exemptions under § 30-4-40(a)(3): The law enforcement exemption requires a specific, articulable harm from disclosure of each withheld record. A generic statement that records are part of an "active investigation" is insufficient. Please identify: (1) the specific enumerated harm from § 30-4-40(a)(3) that applies to each withheld record; and (2) how disclosure of that specific record would cause that specific harm.

[If matter appears concluded:] If the related criminal proceeding has concluded or no prosecution is pending, please confirm that the active investigation rationale under § 30-4-40(a)(3) no longer applies and produce all relevant records.

Under § 30-4-15, the FOIA must be liberally construed. Exemptions are strictly construed against the agency. The burden of proving any exemption rests on {{agency_name}}.

I am willing to pay up to $0.25 per page for paper copies, up to ${{fee_limit}} total. Please provide records in electronic format where available.

Please respond within 15 business days per § 30-4-30(C).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs no reproduction cost. The FOIA\'s liberal construction mandate supports a fee waiver here.''',
        'expedited_language': '''I request prompt processing within FOIA\'s 15-business-day deadline. These records are needed urgently because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'South Carolina law enforcement records template. Key points: (1) the § 30-4-40(a)(3) exemption requires specific, articulable harm per record — not categorical denial; (2) completed investigation files are generally public; (3) incident reports and arrest records are public regardless of investigation status; (4) civil penalties under § 30-4-110 ($1,500/violation + $500/day) provide enforcement leverage; (5) no administrative appeal — circuit court enforcement under § 30-4-100.',
    },
    {
        'jurisdiction': 'SC',
        'record_type': 'government_meetings',
        'template_name': 'South Carolina FOIA Request — Public Meeting Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Freedom of Information Officer
{{agency_name}}
{{agency_address}}

Re: South Carolina FOIA Request — Public Body Meeting Records, S.C. Code § 30-4-30; § 30-4-70 et seq.

Dear Freedom of Information Officer:

Pursuant to the South Carolina Freedom of Information Act, S.C. Code § 30-4-10 et seq., and the FOIA's Open Meetings provisions, S.C. Code § 30-4-70 et seq., I request the following records:

{{description_of_records}}

Specifically, I request for the period {{date_range_start}} through {{date_range_end}}:
- Agendas for all regular and special meetings of {{public_body_name}}
- Minutes of all regular and special meetings (including any portions initially closed under executive session)
- Supporting documents distributed to members prior to or at the referenced meetings
- All executive session minutes, logs, or memoranda from the referenced period
- Any written communications from the general public submitted during public comment periods
- Votes, resolutions, and official actions taken during the referenced period

Regarding executive session records: S.C. Code § 30-4-70(b) requires that a log or other record be maintained of actions taken in executive session. Those action records are public. While deliberations in properly convened executive sessions may be exempt, the fact of any action taken and the general subject matter of the session are public.

I request that minutes and meeting documents be provided in electronic format where available.

I am willing to pay up to $0.25 per page for paper copies, up to ${{fee_limit}} total.

Please respond within 15 business days per § 30-4-30(C).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for these meeting records. Public body meeting records are at the core of governmental transparency. These records concern {{public_interest_explanation}}. Electronic delivery is available at no reproduction cost.''',
        'expedited_language': '''I request prompt processing within the 15-business-day deadline. These meeting records are needed promptly because: {{expedited_justification}}. Please contact me if there are any questions.''',
        'notes': 'South Carolina public meeting records template. Key points: (1) S.C. Code § 30-4-70 et seq. governs open meetings and creates its own records obligations; (2) executive session minutes are generally public after any pending litigation or personnel matter is resolved; (3) meeting agendas and supporting documents distributed to members are public; (4) votes and official actions taken in executive session are always public regardless of the session\'s closed status.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in SC_EXEMPTIONS:
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

    print(f'SC exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in SC_RULES:
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

    print(f'SC rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in SC_TEMPLATES:
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

    print(f'SC templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'SC total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_sc', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
