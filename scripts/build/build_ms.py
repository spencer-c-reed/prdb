#!/usr/bin/env python3
"""Build Mississippi Public Records Act data: exemptions, rules, and templates.

Covers the Mississippi Public Records Act, Miss. Code § 25-61-1 et seq.
Mississippi requires acknowledgment within 1 business day and production
within 7 business days. $0.50/page copy fee. No administrative appeal —
enforcement is in Chancery court. The Mississippi Ethics Commission handles
complaints. Attorney's fees for prevailing requesters.

Run: python3 scripts/build/build_ms.py
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
# Mississippi Public Records Act, Miss. Code § 25-61-1 et seq.
# Mississippi's exemptions are found both within Chapter 61 and scattered
# across specific subject-matter statutes. The Act provides that all public
# records are subject to inspection unless specifically exempted by law.
# Unlike some states, Mississippi does not have a strong constitutional or
# statutory presumption of openness with teeth — enforcement relies largely
# on chancery court action. Exemptions must be specifically authorized by law.
# =============================================================================

MS_EXEMPTIONS = [
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11',
        'exemption_number': 'Miss. Code § 25-61-11',
        'short_name': 'Records Exempt by Statute or Declared Confidential',
        'category': 'statutory',
        'description': 'Records that are declared confidential, privileged, or exempt from disclosure by a specific provision of Mississippi or federal law are not subject to mandatory public disclosure under the Public Records Act. This exemption operates as a passthrough to other statutory confidentiality provisions.',
        'scope': 'Records specifically designated as confidential or exempt by another Mississippi statute or federal law. The exemption requires a specific statutory provision — general policy preferences or administrative designations are not sufficient. Examples include: tax records (Miss. Code § 27-3-77), adoption records (Miss. Code § 93-17-25), certain child welfare records (Miss. Code § 43-21-261), and records protected by federal confidentiality requirements. The requesting party should obtain the specific statutory citation and verify its actual applicability to the records requested. Mississippi courts require a specific legal basis for withholding — vague assertions that records are "confidential" without citation are insufficient.',
        'key_terms': json.dumps([
            'statutory exemption', 'confidential by statute', 'required by law', 'federal law',
            'specifically exempt', 'tax records', 'adoption records', 'child welfare',
            'statutory confidentiality', 'protected by law',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that mandates or authorizes confidentiality — a vague "confidential" claim is insufficient',
            'The cited statute must actually cover the specific type of record requested, not just the general subject area',
            'Aggregate data and anonymized records are generally public even if individual records are statutorily confidential',
            'Challenge whether the external statute actually applies to the specific records requested or only to a subset',
            'Many statutory confidentiality provisions have sunset clauses or exceptions for public interest access that should be analyzed',
        ]),
        'notes': 'Miss. Code § 25-61-11 is a passthrough exemption. Analysis depends on the specific external statute cited. Mississippi courts require agencies to identify the specific statutory basis for withholding. This exemption is frequently overclaimed — requesters should obtain the specific statutory citation and independently verify its applicability and scope.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(c)',
        'exemption_number': 'Miss. Code § 25-61-11(c)',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Personnel records of individual employees and applicants are exempt to the extent that disclosure would constitute a clearly unwarranted invasion of personal privacy. Public employee salary, title, and official conduct are generally not protected.',
        'scope': 'Personnel files, performance evaluations, medical and benefit records, home addresses, and similar highly personal information for individual government employees where disclosure would constitute a clearly unwarranted invasion of personal privacy. The exemption is not categorical — it requires a case-by-case balancing of the employee\'s privacy interest against the public\'s interest in government accountability. Names, job titles, salaries, official duties, and disciplinary findings relating to the employee\'s official conduct are generally public. Home addresses, medical information, and personal financial details carry stronger privacy interests. Disciplinary records of government officials acting in their official capacities are subject to higher disclosure standards because of the public accountability interest.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation', 'personal privacy',
            'clearly unwarranted invasion', 'disciplinary record', 'employment file',
            'government employee', 'public employee', 'personnel file',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, salaries, and official duties of public employees are public and cannot be withheld under this exemption',
            'The "clearly unwarranted invasion" standard requires genuine balancing, not a blanket privacy claim',
            'Disciplinary records of officials relating to their official conduct are subject to public accountability interests',
            'Challenge overbroad claims that treat entire personnel files as exempt when only specific sensitive data warrants protection',
            'Records already disclosed publicly cannot be withheld retroactively under a privacy claim',
        ]),
        'notes': 'Mississippi applies a balancing test for personnel record privacy. The "clearly unwarranted invasion" standard means that not all privacy interests justify withholding — the privacy harm must be significant and the public interest in disclosure minimal. Salaries and official conduct of government employees are consistently treated as public in Mississippi.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(a)',
        'exemption_number': 'Miss. Code § 25-61-11(a)',
        'short_name': 'Law Enforcement — Investigative Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement agencies or their investigations are exempt where disclosure would impair investigations, endanger persons, or reveal confidential investigative techniques or information. Completed investigation records generally become accessible.',
        'scope': 'Law enforcement investigation and intelligence records where disclosure would: (1) harm an ongoing investigation; (2) reveal the identity of a confidential informant; (3) endanger the life or safety of a law enforcement officer or witness; or (4) reveal confidential investigative techniques. The exemption applies primarily to active matters — Mississippi courts have generally held that completed investigation files, closed cases, and concluded prosecutions do not retain the same exemption protection. Basic arrest records, incident reports, and booking information are generally public regardless of investigation status. Factual portions of investigation files that do not implicate the enumerated harms must be released.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'ongoing investigation', 'endanger', 'police records',
            'investigation file', 'pending prosecution', 'intelligence records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to active investigations — completed cases are generally public',
            'Each withheld document must implicate a specific enumerated harm, not merely be "related to" an investigation',
            'Arrest records, booking information, and basic incident reports are generally public regardless of investigation status',
            'Factual information in investigation files that does not reveal informants or techniques must be released',
            'Challenge blanket claims that all records are exempt because an investigation is "ongoing" without specific harm articulation',
            'Mississippi courts require agencies to identify the specific harm from disclosure of each withheld record',
        ]),
        'notes': 'Miss. Code § 25-61-11(a) covers law enforcement investigative records. Mississippi courts apply a specific-harm standard — agencies must articulate how disclosure of each withheld record would cause one of the enumerated harms. The exemption does not cover all law enforcement records, only those where specific harm would result from disclosure.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(d)',
        'exemption_number': 'Miss. Code § 25-61-11(d)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Communications and records that are subject to the attorney-client privilege or attorney work product doctrine are exempt from required public disclosure under the Public Records Act.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and work product prepared by attorneys in anticipation of litigation. The privilege requires: (1) a bona fide attorney-client relationship; (2) communications made in confidence; (3) for the purpose of legal advice (not general business or policy guidance). Billing records, retainer agreements, and general contract terms are not privileged. Facts independently known to the agency are not protected merely because they were shared with an attorney. Waiver occurs when the privileged communication is disclosed to third parties not involved in the legal matter, or used in public proceedings.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'attorney work product', 'legal opinion',
            'government attorney', 'outside counsel', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not business or policy guidance — the latter is not privileged',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when the agency discloses the privileged content publicly or to non-attorney staff not involved in the legal matter',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis',
            'Challenge whether communications labeled "legal advice" were actually business decisions',
            'The privilege belongs to the agency, which may waive it through inconsistent conduct',
        ]),
        'notes': 'Mississippi recognizes attorney-client privilege and work product protection for government entities under Miss. Code § 25-61-11(d). The analysis follows standard common-law privilege doctrine. The privilege must be claimed with specificity — a generic assertion that records are "legal" documents is insufficient.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(b)',
        'exemption_number': 'Miss. Code § 25-61-11(b)',
        'short_name': 'Trade Secrets and Confidential Business Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted by private entities to government agencies are exempt where disclosure would give competitors an unfair advantage or cause competitive harm.',
        'scope': 'Commercially sensitive information submitted by private businesses to state agencies that constitutes a trade secret under Mississippi law or whose disclosure would cause genuine competitive harm. Covers information submitted in connection with licensing, permitting, contracting, or regulatory compliance. The exemption does not cover government-generated records, expenditures of public funds, contract amounts, or information that is publicly available. Agencies must independently evaluate trade secret claims rather than simply deferring to vendor designations. General business information that is not genuinely commercially sensitive does not qualify. Information submitted pursuant to mandatory government requirements carries a reduced expectation of secrecy.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'competitive harm',
            'business confidential', 'financial information', 'competitive advantage',
            'proprietary data', 'business trade secret', 'commercially sensitive',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts paid with public funds are public regardless of trade secret claims',
            'Government-generated records cannot constitute trade secrets',
            'Publicly available information cannot qualify as a trade secret regardless of vendor designations',
            'Information submitted under government mandate carries a reduced expectation of secrecy',
            'Agencies must independently evaluate trade secret claims and may not simply defer to vendor designations',
            'Challenge whether the submitter actually maintained reasonable secrecy measures for the claimed trade secret',
        ]),
        'notes': 'Miss. Code § 25-61-11(b) protects trade secrets and confidential business information. Mississippi courts apply standard trade secret analysis. Contract amounts, unit prices, and expenditures of public funds are consistently public. Vendor confidentiality designations are not dispositive — the agency must independently evaluate the claim.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-9',
        'exemption_number': 'Miss. Code § 25-61-9',
        'short_name': 'Security Plans for Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and operational security records for critical infrastructure and public facilities are exempt where disclosure would create a specific security risk to persons or facilities.',
        'scope': 'Operational security plans, vulnerability assessments, and access control procedures for public buildings, water systems, energy infrastructure, and other critical facilities where disclosure would create a concrete security risk. The exemption requires a specific, articulable security risk — not a general claim that the records are security-related. Budget and expenditure records for security programs are generally public. The agency must demonstrate that disclosure of the specific records requested would create a genuine risk, not merely that the records are labeled "security." Physical security plans for non-critical facilities with widely known access patterns do not qualify.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure', 'security risk',
            'access control', 'public facility security', 'infrastructure protection',
            'emergency response plan', 'security procedures', 'operational security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal exploitable vulnerabilities are not covered',
            'Challenge claims that entire security contracts are exempt when only specific technical specifications warrant protection',
            'Physical security plans for non-critical facilities do not qualify',
        ]),
        'notes': 'Miss. Code § 25-61-9 protects security plans for critical infrastructure. Mississippi courts require agencies to identify a specific risk — not merely assert that records are "security-related." Administrative and budget records for security programs remain public.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(e)',
        'exemption_number': 'Miss. Code § 25-61-11(e)',
        'short_name': 'Preliminary Drafts and Deliberative Materials',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memoranda prepared as part of the agency\'s deliberative and decision-making process are exempt from required disclosure, to the extent they contain opinions and have not been adopted as the agency\'s final position.',
        'scope': 'Predecisional, deliberative documents — preliminary drafts, working papers, notes, and recommendations that reflect the agency\'s internal deliberative process. The exemption requires that the document be: (1) predecisional — prepared before the final agency action; and (2) deliberative — containing opinion, analysis, or recommendation rather than purely factual material. Purely factual material embedded within deliberative documents must be segregated and released. Final agency decisions, adopted policies, and working law that the agency actually applies must be disclosed. Documents circulated outside the agency or to persons not involved in the deliberative process may lose their predecisional character.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'working paper',
            'intra-agency memorandum', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'internal communication',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — only the opinion and recommendation portions qualify',
            'Once adopted as the agency\'s final position, the document is no longer predecisional and must be disclosed',
            '"Working law" — standards and criteria the agency actually applies — must be disclosed even if in internal documents',
            'Documents shared outside the agency may lose their predecisional character',
            'Challenge claims that entire documents are deliberative when only specific sections contain opinions',
        ]),
        'notes': 'Miss. Code § 25-61-11(e) is Mississippi\'s deliberative process exemption. Mississippi courts apply the factual/opinion distinction — factual data does not become deliberative merely because it is embedded in a recommendation memo. The exemption covers the deliberative process, not the underlying facts on which decisions are based.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 45-29-1 et seq.',
        'exemption_number': 'Miss. Code § 45-29-1',
        'short_name': 'Criminal History Records — Dissemination Restrictions',
        'category': 'law_enforcement',
        'description': 'Criminal history record information maintained by the Mississippi Department of Public Safety is subject to dissemination restrictions that limit access to certain categories of requesters for specific purposes. Not all criminal history information is freely accessible to the public.',
        'scope': 'Criminal history record information (CHRI) maintained in the Mississippi Criminal Information Center (MCIC) statewide database, including arrest records, conviction records, and disposition information. Mississippi restricts access to CHRI for many purposes — access is generally limited to law enforcement, criminal justice agencies, employers in regulated industries, and individuals seeking their own records. Broader public access is limited. However, court records and publicly filed criminal documents are generally accessible through court record systems rather than through the MCIC system. The exemption does not shield information that was publicly disclosed in open court proceedings.',
        'key_terms': json.dumps([
            'criminal history', 'criminal record', 'CHRI', 'MCIC', 'arrest record',
            'conviction record', 'criminal background', 'rap sheet', 'criminal information',
            'Department of Public Safety',
        ]),
        'counter_arguments': json.dumps([
            'Court records and publicly filed criminal documents are accessible through court record systems regardless of CHRI restrictions',
            'Information disclosed in open court proceedings is public regardless of CHRI exemption status',
            'Challenge claims that information already in the public record (court filings, published judgments) is exempt under CHRI restrictions',
            'Aggregate criminal statistics and anonymized data are public',
            'The exemption covers the centralized database, not all records that might contain criminal history information',
        ]),
        'notes': 'Mississippi\'s criminal history record dissemination restrictions under Miss. Code § 45-29-1 et seq. govern access to the MCIC database. These restrictions are separate from the Public Records Act\'s general framework. Court records remain accessible through clerk offices regardless of CHRI restrictions. Requesters seeking criminal history information should consider both the MCIC access rules and the separate court records access framework.',
    },
    {
        'jurisdiction': 'MS',
        'statute_citation': 'Miss. Code § 25-61-11(f)',
        'exemption_number': 'Miss. Code § 25-61-11(f)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared for or by a government agency in connection with prospective acquisition or sale of property are exempt until the transaction is complete or the agency withdraws from the transaction.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with a prospective government acquisition or sale. The exemption is time-limited — it expires automatically when the transaction closes, is formally abandoned, or the agency discloses the appraisal value publicly. The rationale is to prevent negotiating disadvantage during active acquisition proceedings. Post-transaction, all appraisal documents become public. Appraisals for property the agency already owns are not covered. Budget discussions about general property value ranges are not formal appraisals and may not qualify.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation', 'pre-acquisition',
            'condemnation appraisal', 'feasibility study', 'land purchase', 'real property',
            'property negotiation', 'acquisition pending',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge whether a transaction is still "pending" if there has been no activity for a significant period',
            'Appraisals for property already owned by the agency are not covered',
            'After condemnation proceedings conclude, all valuation records are public',
            'Budget estimates and internal discussions about property value are not formal appraisals',
        ]),
        'notes': 'Miss. Code § 25-61-11(f) protects pre-acquisition appraisals. The exemption is strictly time-limited. Mississippi courts have held that the exemption terminates upon transaction completion regardless of how the agency characterizes the matter.',
    },
]

# =============================================================================
# RULES
# Mississippi Public Records Act, Miss. Code § 25-61-1 et seq.
# Mississippi requires 1-business-day acknowledgment and 7-business-day
# production. No administrative appeal — enforcement via Chancery Court.
# The Ethics Commission handles complaints. Attorney's fees for prevailing
# requesters. $0.50/page copy fee.
# =============================================================================

MS_RULES = [
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'acknowledge_deadline_days',
        'param_value': '1',
        'day_type': 'business',
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'Mississippi public bodies must acknowledge receipt of a public records request within 1 business day of receiving it. This is one of the fastest acknowledgment deadlines in the country. The acknowledgment does not need to include the records themselves — it simply confirms that the request was received. Failure to acknowledge within 1 business day is a statutory violation and may be reported to the Ethics Commission. Many agencies send a brief acknowledgment email the same day. The 1-business-day clock begins on receipt of the written request.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'production_deadline_days',
        'param_value': '7',
        'day_type': 'business',
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'After acknowledging a request, Mississippi agencies must provide the requested records within 7 business days of receiving the request. If the records cannot be produced within 7 business days, the agency must provide written notice explaining the reason for the delay and specifying when the records will be available. Repeated or unreasonable delays may be reported to the Ethics Commission. The 7-business-day production deadline is firm — agencies may not simply assert volume as an excuse for indefinite delay without providing a specific production date.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'written_request_permitted',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'Mississippi public records requests may be submitted in writing (letter, email, or online portal) or orally. Written requests are strongly recommended to establish the acknowledgment and production deadlines, document the scope of the request, and create a record for any subsequent court challenge or Ethics Commission complaint. Mississippi does not require requesters to use a specific form, but agencies may provide a form as a convenience. The 1-business-day acknowledgment and 7-business-day production deadlines are triggered by receipt of the request.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'Mississippi does not require requesters to identify themselves or state the purpose of their request as a condition of accessing public records. The Public Records Act provides access to "any person." Requiring identification or purpose as a condition of access is improper. Some agencies ask for contact information for delivery purposes, but providing it must be voluntary.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'When a record contains both exempt and non-exempt information, the Mississippi agency must release all non-exempt, reasonably segregable portions and provide a written explanation of what was redacted and the legal basis for each redaction. Blanket withholding of documents containing some exempt content is improper. The agency must release the non-exempt portions rather than withholding the entire document.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate',
        'param_value': '0.50',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-7',
        'notes': 'Mississippi agencies may charge up to $0.50 per page for paper copies of public records. This is among the higher per-page rates in the country — requesters should ask about electronic delivery as an alternative to reduce costs. For electronic records delivered digitally, the fee should reflect only the actual cost of the digital medium or transmission. Agencies must publish their fee schedules and provide advance notice of fees that will exceed a specified threshold. Staff time for record retrieval and review is generally a permissible fee element in Mississippi, which can substantially increase the total cost for large requests.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_fee_allowed',
        'param_value': 'yes_with_advance_notice',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-7',
        'notes': 'Mississippi agencies may charge for staff time spent locating, reviewing, and redacting records, in addition to per-page copy fees. Staff time charges must be based on the actual cost of the employee time expended, using the hourly rate of the lowest-paid employee capable of performing the task. Agencies must provide advance notice before incurring significant fees and must provide an itemized estimate if requested. Fees set at levels that constitute a practical barrier to access may be challenged as inconsistent with the Act.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-7',
        'notes': 'Mississippi\'s Public Records Act does not mandate fee waivers for any category of requesters. Agencies may waive fees at their discretion. Requesters can argue that the public interest in disclosure supports a fee waiver. Journalists, nonprofits, and academic researchers frequently request fee waivers by demonstrating public interest. Agencies that routinely waive fees for favored requesters while charging others may be acting in a discriminatory manner inconsistent with the Act\'s universal access provision.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-13',
        'notes': 'Mississippi has NO formal administrative appeal mechanism for Public Records Act denials. A requester denied access may not appeal to an agency head or administrative body — the only formal remedy is chancery court. However, the Mississippi Ethics Commission accepts complaints about public records denials and may investigate or mediate disputes. Ethics Commission complaints are not a formal appeal and do not stay agency action, but they can be an effective pressure mechanism. Miss. Code § 25-61-13 provides the chancery court enforcement mechanism.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'appeal_deadline',
        'param_key': 'ethics_commission_complaint',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-4-1 et seq.',
        'notes': 'The Mississippi Ethics Commission accepts complaints about violations of the Public Records Act under Miss. Code § 25-4-1 et seq. The Ethics Commission can investigate complaints, issue advisory opinions, and refer matters for enforcement. Filing an Ethics Commission complaint is not a formal legal appeal and does not toll any deadlines. However, it is a meaningful informal remedy — agencies often respond to Ethics Commission inquiries more quickly than to court filings. Complaints should include: the specific records requested, the date of the request, the agency\'s response, and the specific provision of the Public Records Act allegedly violated.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'chancery_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-13',
        'notes': 'A requester denied access to public records may seek enforcement in the Chancery Court of the county where the agency is located. Miss. Code § 25-61-13 provides that a person aggrieved by a denial may bring a civil action in chancery court. The court may order production of the records, assess damages, and award attorney\'s fees to a prevailing requester. There is no specific statute of limitations, but requesters should act promptly. Chancery courts in Mississippi are the court of general equity jurisdiction and have broad powers to fashion appropriate relief.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-15',
        'notes': 'A requester who prevails in a Public Records Act enforcement action may recover attorney\'s fees and other litigation costs from the agency under Miss. Code § 25-61-15. Attorney\'s fees are available when the agency wrongfully denied access. The availability of attorney\'s fees makes it economically viable to bring enforcement actions even for modest-size requests. Mississippi courts have discretion to award fees and typically do so when the agency\'s withholding was without reasonable legal basis.',
    },
    {
        'jurisdiction': 'MS',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'Miss. Code § 25-61-5',
        'notes': 'When a Mississippi agency denies a public records request in whole or in part, the denial must be in writing and must state the specific statutory basis for the denial. A blanket denial without a statutory citation is a violation of the Public Records Act. The written denial is important for establishing the record for any subsequent chancery court challenge or Ethics Commission complaint. Partial denials must be accompanied by production of all non-exempt, reasonably segregable portions of withheld records.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

MS_TEMPLATES = [
    {
        'jurisdiction': 'MS',
        'record_type': 'general',
        'template_name': 'General Mississippi Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Mississippi Public Records Act, Miss. Code § 25-61-1 et seq.

Dear Public Records Officer:

Pursuant to the Mississippi Public Records Act, Miss. Code § 25-61-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available to minimize cost and production time.

I am willing to pay reasonable fees under Miss. Code § 25-61-7. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment. Please provide an itemized fee estimate in advance.

If any records are withheld in whole or in part, I request a written denial under Miss. Code § 25-61-5 that: (1) identifies each record withheld; (2) states the specific statutory basis (statute citation and subsection) for each withholding; and (3) confirms that all non-exempt, reasonably segregable portions of partially withheld records have been released.

Under Miss. Code § 25-61-5, please acknowledge receipt of this request within 1 business day and produce responsive records within 7 business days of receiving this request. If the 7-business-day deadline cannot be met, please provide written notice stating the reason and a specific date when records will be available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the Mississippi Public Records Act does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, reproduction costs are minimal or zero, making a fee waiver practical as well as appropriate.''',
        'expedited_language': '''I request that this Public Records Act request be processed as expeditiously as possible. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose Mississippi Public Records Act template. Key Mississippi features: (1) 1-business-day acknowledgment deadline (Miss. Code § 25-61-5); (2) 7-business-day production deadline (Miss. Code § 25-61-5); (3) no administrative appeal — enforcement in Chancery Court (Miss. Code § 25-61-13); (4) Ethics Commission complaints as informal remedy (Miss. Code § 25-4-1 et seq.); (5) attorney\'s fees for prevailing requesters (Miss. Code § 25-61-15); (6) $0.50/page copy fee (Miss. Code § 25-61-7); (7) staff time fees allowed with advance notice. Reference "Mississippi Public Records Act" or "Miss. Code § 25-61-1 et seq.", not "FOIA."',
    },
    {
        'jurisdiction': 'MS',
        'record_type': 'law_enforcement',
        'template_name': 'Mississippi Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, Miss. Code § 25-61-1 et seq.

Dear Public Records Officer:

Pursuant to the Mississippi Public Records Act, Miss. Code § 25-61-1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Body-worn camera footage and metadata
- Dispatch logs and Computer-Aided Dispatch (CAD) records
- Officer complaint and disciplinary records for involved personnel
- Internal investigation records relating to the above incident

Regarding claimed exemptions under Miss. Code § 25-61-11(a): Mississippi law does not permit blanket withholding of law enforcement records. Any withholding under Miss. Code § 25-61-11(a) requires articulation of the specific harm that would result from disclosure of each withheld record. A generic "investigation ongoing" response is insufficient.

[If applicable:] If no prosecution is pending or any related prosecution has concluded, please apply the standard for completed investigations — the withholding rationale under Miss. Code § 25-61-11(a) does not apply to closed matters.

Please acknowledge receipt within 1 business day and respond within 7 business days per Miss. Code § 25-61-5.

I am willing to pay fees under Miss. Code § 25-61-7, up to ${{fee_limit}}. Please provide an itemized estimate before incurring significant costs.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs minimal reproduction cost. A fee waiver is consistent with the Act's access mandate.''',
        'expedited_language': '''I request expedited processing of this Public Records Act request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Mississippi law enforcement records template. Key features: (1) 1-business-day acknowledgment, 7-business-day production (Miss. Code § 25-61-5); (2) Miss. Code § 25-61-11(a) exemption requires specific harm articulation for each withheld record; (3) completed investigation files are generally public once prosecution concludes; (4) no administrative appeal — Ethics Commission complaint (Miss. Code § 25-4-1) or Chancery Court (Miss. Code § 25-61-13); (5) attorney\'s fees for prevailing requesters (Miss. Code § 25-61-15); (6) $0.50/page copy fee — request electronic delivery to reduce costs.',
    },
    {
        'jurisdiction': 'MS',
        'record_type': 'government_contracts',
        'template_name': 'Mississippi Public Records Request — Government Contracts',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Government Contracts and Expenditures, Miss. Code § 25-61-1 et seq.

Dear Public Records Officer:

Pursuant to the Mississippi Public Records Act, Miss. Code § 25-61-1 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Invoices, payment records, and expenditure documentation under those contracts
- Requests for proposals (RFPs), bid submissions, and bid evaluation records
- Any correspondence regarding contract performance or compliance
- Any audit or review records relating to the above contracts

Regarding trade secret claims: Under Miss. Code § 25-61-11(b), only information that genuinely qualifies as a trade secret may be withheld. Contract amounts paid with public funds, unit prices for services procured with public money, and general contract terms are public regardless of vendor confidentiality designations. The agency must independently evaluate any trade secret claim.

Under Miss. Code § 25-61-5, please acknowledge receipt within 1 business day and produce records within 7 business days.

I am willing to pay fees under Miss. Code § 25-61-7, up to ${{fee_limit}}. Please provide an itemized estimate in advance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern expenditures of public funds on {{public_interest_explanation}}, a core accountability matter. The public interest in knowing how tax dollars are spent substantially outweighs any agency interest in fee recovery.''',
        'expedited_language': '''I request expedited processing of this request. These records involve ongoing expenditures of public funds where prompt disclosure is in the public interest. I need these records by {{needed_by_date}}.''',
        'notes': 'Mississippi government contracts template. Key features: (1) 1-business-day acknowledgment, 7-business-day production (Miss. Code § 25-61-5); (2) contract amounts and expenditures with public funds are public regardless of trade secret claims — challenge overbroad vendor confidentiality designations under Miss. Code § 25-61-11(b); (3) $0.50/page copy fee — request electronic delivery; (4) Ethics Commission complaint as informal remedy; (5) attorney\'s fees for prevailing requesters (Miss. Code § 25-61-15).',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in MS_EXEMPTIONS:
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

    print(f'MS exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in MS_RULES:
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

    print(f'MS rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in MS_TEMPLATES:
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

    print(f'MS templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'MS total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ms', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
