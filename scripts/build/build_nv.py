#!/usr/bin/env python3
"""Build Nevada Public Records Act data: exemptions, rules, and templates.

Covers the Nevada Public Records Act (NPRA), NRS Chapter 239.
Nevada requires a response within 5 business days. $0.25/page for paper,
$0.50/page electronic (unique). No administrative appeal — enforcement via
district court. Attorney's fees for prevailing requesters. The Act has a
broad definition of "public books and records" and presumes openness.

Run: python3 scripts/build/build_nv.py
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
# Nevada Public Records Act, NRS 239.010 et seq.
# Nevada's exemptions are found both within NRS Chapter 239 and scattered
# across other NRS provisions. The Act presumes that all public books and
# records are open to inspection. Exemptions must be specifically authorized
# by statute. Nevada courts construe exemptions narrowly and have emphasized
# the Act's strong policy favoring public access.
# =============================================================================

NV_EXEMPTIONS = [
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.010(5); NRS 239.0107',
        'exemption_number': 'NRS 239.0107',
        'short_name': 'Records Declared Confidential by Statute',
        'category': 'statutory',
        'description': 'Records that are declared confidential by a specific provision of Nevada or federal law are exempt from required public disclosure under the NPRA. This exemption is a passthrough to external statutory confidentiality provisions.',
        'scope': 'Records specifically designated as confidential by another Nevada statute or federal law. The exemption requires a specific statutory provision — general policy preferences or administrative designations are insufficient. Examples include: tax return information (NRS 360.247), certain welfare records, adoption records (NRS 127.140), and records subject to federal confidentiality requirements. The agency must identify the specific external statute with citation. Nevada courts require a specific legal basis for withholding — vague "confidential" assertions without citation are improper. Requesters should obtain the specific statutory citation and independently verify its actual scope and applicability.',
        'key_terms': json.dumps([
            'statutory exemption', 'confidential by statute', 'required by law', 'federal law',
            'specifically exempt', 'tax records', 'adoption records', 'welfare records',
            'statutory confidentiality', 'protected by law', 'NRS exemption',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that mandates or authorizes confidentiality',
            'The cited statute must actually apply to the specific records requested, not just the general subject area',
            'Aggregate data and anonymized records are generally public even if individual records are statutorily confidential',
            'Challenge whether the external statute\'s scope actually covers the specific documents requested',
            'Nevada courts construe exemptions narrowly — agencies cannot bootstrap a broad exemption from a narrow statutory provision',
        ]),
        'notes': 'NRS 239.0107 and NRS 239.010(5) together establish the passthrough exemption framework. Analysis depends on the specific external statute cited. Nevada courts construe exemptions narrowly consistent with the NPRA\'s strong presumption of openness in NRS 239.010. Agencies must provide the specific statutory citation — vague confidentiality claims are insufficient.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(2); NRS 281.641',
        'exemption_number': 'NRS 281.641',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Certain personnel information about individual public employees — including home addresses, personal telephone numbers, and medical information — is protected from disclosure. However, official salaries, job titles, and records relating to the performance of official duties are generally public.',
        'scope': 'Personnel files and related records containing genuinely personal information about individual government employees where disclosure would constitute an unwarranted invasion of personal privacy. Nevada courts apply a balancing test: the employee\'s privacy interest against the public\'s interest in government accountability. Names, job titles, official compensation, and records documenting the performance of official duties are consistently public. Home addresses, personal telephone numbers, medical information, and other genuinely personal data carry stronger privacy interests. Disciplinary records of public officials relating to their official conduct are generally subject to disclosure given the public accountability interest. NRS 281.641 provides additional protections for certain personnel information.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation', 'personal privacy',
            'unwarranted invasion', 'disciplinary record', 'employment file',
            'government employee', 'public employee', 'personnel information',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, official salaries, and the performance of official duties are public and cannot be withheld under privacy claims',
            'Disciplinary records of public officials relating to official conduct are generally disclosable given the accountability interest',
            'The unwarranted invasion standard requires genuine balancing — not a blanket privacy claim',
            'Challenge overbroad claims that treat entire personnel files as exempt when only specific personal data warrants protection',
            'Records already publicly disclosed cannot be retroactively shielded by a privacy claim',
        ]),
        'notes': 'Nevada personnel record privacy is governed by a balancing test. Nevada courts have consistently held that official conduct, compensation, and performance of public duties are public. The privacy protection is limited to genuinely personal information that bears no relationship to the employee\'s official functions. NRS 281.641 provides specific confidentiality for certain personnel information but does not override the general public accountability standard.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(b)',
        'exemption_number': 'NRS 239.0107(1)(b)',
        'short_name': 'Law Enforcement — Investigative and Intelligence Records',
        'category': 'law_enforcement',
        'description': 'Law enforcement investigative records and intelligence files are exempt from required public disclosure where disclosure would impair ongoing investigations, reveal confidential informant identities, endanger persons, or reveal investigative techniques whose effectiveness depends on secrecy.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) interfere with an ongoing investigation or prosecution; (2) reveal the identity of a confidential informant; (3) endanger the life or physical safety of a law enforcement officer, witness, or other person; or (4) reveal investigative techniques that would be compromised by disclosure. The exemption applies primarily to active matters — Nevada courts have held that completed investigation files are generally public once prosecution concludes or the investigation closes. Incident reports, arrest records, and booking information are generally public regardless of investigation status. Factual portions of investigation files that do not implicate the enumerated harms must be released. The agency must identify the specific harm from disclosure of each withheld record.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'ongoing investigation', 'pending prosecution',
            'intelligence records', 'police records', 'investigation file', 'endanger',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to active investigations — completed cases are generally public',
            'Each withheld document must implicate a specific harm, not merely be related to an investigation',
            'Arrest records, booking information, and basic incident reports are generally public',
            'Factual information in investigation files that does not reveal informants or techniques must be released',
            'Challenge blanket claims that all records are exempt because an investigation is "ongoing" without specific harm articulation',
            'Nevada courts construe exemptions narrowly — the harm must be specific and articulable',
        ]),
        'notes': 'NRS 239.0107(1)(b) covers law enforcement investigative and intelligence records. Nevada courts apply narrow construction of exemptions consistent with the NPRA\'s presumption of openness in NRS 239.010. Agencies must articulate the specific harm from disclosure of each withheld record. Completed investigation files are generally public once prosecution concludes.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(a)',
        'exemption_number': 'NRS 239.0107(1)(a)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that are subject to the attorney-client privilege or attorney work product doctrine are exempt from required public disclosure under the Nevada Public Records Act.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege requires: (1) a bona fide attorney-client relationship; (2) confidential communications; (3) for the purpose of legal advice (not business or policy guidance). Billing records and retainer agreements are generally not privileged. Facts independently known to the agency are not protected merely because they were shared with an attorney. Waiver occurs when privileged content is disclosed in public proceedings or to persons outside the legal matter.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'attorney work product', 'legal opinion',
            'government attorney', 'outside counsel', 'NRS attorney privilege',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not business or policy guidance',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when privileged content is publicly disclosed or disclosed to persons outside the legal matter',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis',
            'Challenge whether communications labeled "legal" were actually business or policy decisions',
            'Nevada courts construe exemptions narrowly — the privilege must be affirmatively established',
        ]),
        'notes': 'NRS 239.0107(1)(a) incorporates attorney-client privilege and work product doctrine into the NPRA. Nevada courts apply standard common-law privilege analysis, narrowly construed consistent with the NPRA\'s disclosure mandate. The privilege must be established with specificity for each withheld record.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(c)',
        'exemption_number': 'NRS 239.0107(1)(c)',
        'short_name': 'Trade Secrets and Proprietary Business Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercially sensitive information submitted by private entities to government agencies are exempt from required public disclosure where disclosure would cause genuine competitive harm.',
        'scope': 'Commercially sensitive information submitted by private businesses to state agencies that constitutes a trade secret under Nevada law or whose disclosure would cause genuine competitive harm. The exemption does not cover government-generated records, contract amounts paid with public funds, or publicly available information. Agencies must independently evaluate trade secret claims — they may not simply defer to vendor designations. Information submitted under mandatory government requirements carries a reduced expectation of secrecy. Nevada courts apply narrow construction of exemptions — only information that genuinely meets the trade secret definition qualifies.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'competitive harm',
            'business confidential', 'financial information', 'competitive advantage',
            'NRS trade secret', 'commercially sensitive', 'proprietary data',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts paid with public funds are public regardless of trade secret claims',
            'Government-generated records cannot constitute trade secrets',
            'Publicly available information cannot qualify for trade secret protection',
            'Information submitted under government mandate carries a reduced expectation of secrecy',
            'Agencies must independently evaluate claims and cannot defer to vendor designations',
            'Nevada courts construe exemptions narrowly — the trade secret must be affirmatively established',
        ]),
        'notes': 'NRS 239.0107(1)(c) protects trade secrets and proprietary business information. Nevada courts apply narrow construction consistent with the NPRA\'s disclosure mandate. Contract amounts, unit prices, and public expenditures are consistently public. Vendor designations are not dispositive — the agency must independently evaluate each claim.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(d)',
        'exemption_number': 'NRS 239.0107(1)(d)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, mental health, and related health records about identified individuals held by government agencies are exempt from required public disclosure to protect personal medical privacy.',
        'scope': 'Individual medical records, mental health and psychiatric evaluations, and related health information held by state and local government agencies. Covers records held by the Nevada Department of Health and Human Services, state hospitals, the Division of Mental Health and Developmental Services, and other government health providers. The exemption applies to individually identifiable health information. Aggregate health data, anonymized records, and statistical reports are generally public. Administrative and financial records of government health agencies are public. The agency must identify the specific privacy harm from disclosure of each withheld record.',
        'key_terms': json.dumps([
            'medical records', 'mental health records', 'psychiatric records', 'health information',
            'patient records', 'HIPAA', 'personal health information', 'patient privacy',
            'medical privacy', 'NRS medical records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized health data are public — the exemption applies to individually identifiable records',
            'Administrative and financial records of government health agencies are fully public',
            'Records relating to a public official\'s fitness for duty may be disclosable given the public accountability interest',
            'Challenge overbroad claims where the agency has not identified the specific privacy harm from disclosure',
            'Nevada courts construe exemptions narrowly — the privacy harm must be specifically articulated',
        ]),
        'notes': 'NRS 239.0107(1)(d) protects individual medical and mental health records. Nevada courts apply narrow construction of exemptions. Administrative records of health agencies (budgets, contracts, staffing) are entirely separate from patient records and are public. The exemption must be specifically established for each withheld record.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(e)',
        'exemption_number': 'NRS 239.0107(1)(e)',
        'short_name': 'Security Plans for Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and operational security records for critical infrastructure and government facilities are exempt where disclosure would create a specific, articulable security risk.',
        'scope': 'Operational security plans, vulnerability assessments, and access control procedures for public buildings, water systems, energy infrastructure, and other critical facilities. The exemption requires a specific, articulable security risk from disclosure — not a general assertion that records are security-related. Budget and expenditure records for security programs are generally public. Physical security plans for non-critical facilities with widely known access patterns do not qualify. Nevada courts apply narrow construction — agencies must specifically articulate the risk from disclosure of each withheld record.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure', 'security risk',
            'access control', 'infrastructure protection', 'emergency response',
            'NRS security records', 'operational security', 'facility security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal exploitable vulnerabilities are not covered',
            'Challenge claims that entire contracts are exempt when only specific technical details warrant protection',
            'Nevada courts construe exemptions narrowly — a generic "security" label is not enough',
        ]),
        'notes': 'NRS 239.0107(1)(e) protects security plans and vulnerability assessments. Nevada courts require agencies to specifically articulate the security risk from disclosure of each withheld record. Administrative and budget records for security programs remain public.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(f)',
        'exemption_number': 'NRS 239.0107(1)(f)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and internal agency memoranda prepared as part of the agency\'s deliberative process are exempt from required disclosure to the extent they contain opinions and have not been adopted as the agency\'s final position.',
        'scope': 'Predecisional, deliberative documents — preliminary drafts, working papers, notes, and recommendations that reflect the agency\'s internal deliberative process and have not been adopted as final policy. The exemption requires that the document be: (1) predecisional — prepared before final agency action; and (2) deliberative — containing opinion, analysis, or recommendation rather than purely factual material. Factual material embedded in deliberative documents must be segregated and released. Final agency decisions, adopted policies, and working law must be disclosed. Nevada courts apply narrow construction — agencies cannot use the deliberative process exemption as a general shield against accountability.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'working paper',
            'intra-agency memorandum', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'NRS deliberative process',
        ]),
        'counter_arguments': json.dumps([
            'Factual material within deliberative documents must be released — only opinion and recommendation portions qualify',
            'Once adopted as final agency policy, the document is no longer predecisional',
            '"Working law" — standards actually applied — must be disclosed even in internal documents',
            'Documents shared outside the agency may lose their predecisional character',
            'Challenge claims that entire documents are deliberative when only specific sections contain opinions',
        ]),
        'notes': 'NRS 239.0107(1)(f) protects deliberative process documents. Nevada courts apply narrow construction consistent with the NPRA\'s disclosure mandate. The factual/opinion distinction is critical — factual data does not become deliberative merely because it is embedded in a recommendation memo.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.010(4)',
        'exemption_number': 'NRS 239.010(4)',
        'short_name': 'Financial Institution Examination Records',
        'category': 'commercial',
        'description': 'Examination reports and confidential supervisory information produced in connection with the examination and regulation of financial institutions by the Nevada Department of Business and Industry are exempt from required public disclosure.',
        'scope': 'Confidential supervisory information produced in connection with the examination and regulation of state-chartered banks, credit unions, mortgage companies, insurance companies, and other financial institutions licensed in Nevada. Includes examination reports, safety-and-soundness findings, and related regulatory correspondence. Final enforcement orders, consent agreements, public sanctions, license status, and aggregate financial data are public. The exemption is designed to protect the candid supervisory exchange between regulators and regulated entities that is essential to effective financial regulation.',
        'key_terms': json.dumps([
            'financial institution examination', 'bank examination', 'supervisory information',
            'Nevada financial regulator', 'Department of Business and Industry',
            'examination report', 'safety and soundness', 'regulatory examination',
            'bank regulation', 'financial institution supervision',
        ]),
        'counter_arguments': json.dumps([
            'Final enforcement orders, consent agreements, and public sanctions are public from the moment of issuance',
            'License status, licensing history, and aggregate financial data are public',
            'Challenge claims that all correspondence between a regulator and a financial institution is "examination records"',
            'Information about final regulatory decisions that affected the public (bank closures, enforcement actions) is public',
        ]),
        'notes': 'NRS 239.010(4) protects financial institution examination records. The exemption mirrors the federal model of confidential banking supervision and does not cover public enforcement actions, license status, or aggregate financial data.',
    },
    {
        'jurisdiction': 'NV',
        'statute_citation': 'NRS 239.0107(1)(g)',
        'exemption_number': 'NRS 239.0107(1)(g)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared for a government agency in connection with prospective acquisition or sale of property are exempt until the transaction is complete or the agency withdraws.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with prospective government acquisition or sale of real property. The exemption is time-limited — it expires when the transaction closes, is formally abandoned, or the agency publicly discloses the value. The purpose is to prevent negotiating disadvantage during active acquisition proceedings. Post-transaction, all appraisal documents become public. Appraisals for property the government already owns are not covered. Nevada courts apply narrow construction — only formal appraisal documents for active acquisitions qualify.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation', 'pre-acquisition',
            'condemnation appraisal', 'feasibility study', 'land purchase', 'real property',
            'Nevada pre-acquisition', 'NRS appraisal exemption',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge whether a transaction is still "pending" after extended inactivity',
            'Appraisals for property the government already owns are not covered',
            'After condemnation proceedings conclude, all valuation records are public',
            'Budget estimates and internal discussions about property values are not formal appraisals',
        ]),
        'notes': 'NRS 239.0107(1)(g) protects pre-acquisition appraisals. The exemption is strictly time-limited. Nevada courts apply narrow construction — the exemption is limited to formal appraisal documents for active acquisitions.',
    },
]

# =============================================================================
# RULES
# Nevada Public Records Act, NRS Chapter 239.
# 5-business-day response deadline. No administrative appeal — enforcement
# via district court. $0.25/page paper, $0.50/page electronic (unusual).
# Attorney's fees for prevailing requesters. Strong presumption of openness.
# =============================================================================

NV_RULES = [
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'NRS 239.0107(1)',
        'notes': 'Nevada agencies must respond to a public records request within 5 business days of receiving it. The agency must either: (1) provide the requested records; (2) provide written notice that additional time is needed and state a specific date for production; or (3) deny the request in writing with a specific statutory basis. If the agency cannot respond within 5 business days, it must notify the requester in writing with a specific production date. Failure to respond within 5 business days without written notice is itself a violation of the NPRA. The 5-business-day clock begins on receipt of the written request.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'NRS 239.0107(2)',
        'notes': 'When a Nevada agency denies a public records request in whole or in part, the denial must be in writing and must state the specific statutory basis for the denial — citing the specific NRS provision that applies. A blanket denial without statutory citation violates the NPRA. The written denial must identify each record withheld and the specific legal basis for withholding each. Partial denials must be accompanied by production of all non-exempt, reasonably segregable portions. The written denial is critical for establishing the record for any subsequent district court challenge.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NRS 239.010(1)',
        'notes': 'NRS 239.010(1) establishes that all public books and records of governmental entities are open to inspection by any person during regular business hours. The Nevada Supreme Court has held that the NPRA must be liberally construed in favor of public access, and exemptions must be narrowly construed. The burden of establishing that any exemption applies rests on the agency. The presumption of openness is a core substantive rule that applies in all NPRA disputes.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NRS 239.0107',
        'notes': 'When a record contains both exempt and non-exempt information, the Nevada agency must release all non-exempt, reasonably segregable portions and provide a written explanation of what was redacted and the legal basis for each redaction. Blanket withholding of documents containing some exempt content is improper under Nevada law. Nevada courts have held that agencies must segregate and release all portions that do not qualify for a specific statutory exemption.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'NRS 239.010(1)',
        'notes': 'Nevada agencies may NOT require requesters to identify themselves or state the purpose of their request as a condition of accessing public records. NRS 239.010(1) provides that all public books and records are open to inspection by any person — not limited by identity or stated purpose. Requiring identification as a condition of access is improper. Anonymous and pseudonymous requests are valid under the NPRA.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'fee_cap',
        'param_key': 'standard_paper_copy_rate',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'NRS 239.052',
        'notes': 'Nevada agencies may charge up to $0.25 per page for paper copies of public records under NRS 239.052. This is the standard paper copy rate. Fees must reflect actual reproduction costs — agencies may not charge for staff time spent reviewing or redacting records under the standard paper copy fee framework. Fee schedules must be published. The $0.25/page rate applies to standard paper copies. For oversize documents, photographs, or other non-standard formats, the fee should reflect the actual cost of reproduction.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_copy_rate',
        'param_value': '0.50',
        'day_type': None,
        'statute_citation': 'NRS 239.052',
        'notes': 'Nevada uniquely allows agencies to charge up to $0.50 per page equivalent for electronic copies under NRS 239.052 — higher than the $0.25/page paper rate. This counterintuitive rate structure means that requesting electronic records in Nevada may cost more than paper copies. Requesters should ask agencies whether the electronic fee is calculated per page of content or per file. The electronic fee applies when the agency must convert paper records to electronic format. When records are already in electronic form and can be emailed directly, the actual cost is often minimal and agencies should not apply the full $0.50 rate.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'generally_no',
        'day_type': None,
        'statute_citation': 'NRS 239.052',
        'notes': 'Nevada agencies generally may not charge for staff time spent locating, reviewing, or redacting records under the basic NPRA fee framework. The standard fees in NRS 239.052 are for reproduction costs — not staff labor. This distinguishes Nevada from states like Kansas and Mississippi that allow staff time charges. For very large or burdensome requests, agencies may raise the staff time issue, but the baseline rule is that standard NPRA fees cover only reproduction costs.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'NRS 239.052',
        'notes': 'Nevada\'s NPRA does not provide a statutory fee waiver right. Agencies may waive fees at their discretion. Requesters — particularly journalists, nonprofits, and academic researchers — can request fee waivers by demonstrating that the records serve a significant public interest. Agencies that routinely waive fees for favored requesters while charging others may be acting inconsistently with the NPRA\'s universal access provision.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'NRS 239.011',
        'notes': 'Nevada has NO formal administrative appeal mechanism for NPRA denials. There is no agency head appeal, no ombudsman, and no administrative tribunal. A requester denied access must seek enforcement directly in district court under NRS 239.011. Nevada is a direct-to-court state for public records enforcement.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'NRS 239.011',
        'notes': 'A requester denied access to public records may bring a civil action in the district court of the county where the agency is located. NRS 239.011 provides the enforcement mechanism. The court may order the agency to permit inspection and copying of records and may award attorney\'s fees to a prevailing requester. There is no specific statute of limitations, but requesters should act promptly. Nevada district courts apply de novo review and may conduct in camera inspection of withheld records.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'NRS 239.011(2)',
        'notes': 'A requester who prevails in an NPRA enforcement action may recover attorney\'s fees and litigation costs from the agency under NRS 239.011(2). Attorney\'s fees are available when the court finds that the agency wrongfully denied access. The availability of attorney\'s fees makes it economically viable to bring enforcement actions even for modest-size records requests. Nevada courts have awarded fees when agencies withheld records without a reasonable legal basis.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'narrow_construction_of_exemptions',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NRS 239.001',
        'notes': 'Nevada courts and the legislature have consistently held that NPRA exemptions must be narrowly construed in favor of disclosure. NRS 239.001 establishes the NPRA\'s policy: that the purpose of government is to serve the people, and that public records access supports democratic accountability. The Nevada Supreme Court has held that where there is doubt about whether an exemption applies, the doubt must be resolved in favor of disclosure. The burden of establishing any exemption rests entirely on the agency.',
    },
    {
        'jurisdiction': 'NV',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NRS 239.0107(3)',
        'notes': 'Electronic records are public records subject to the NPRA. Nevada agencies must provide electronic records in the format in which they are maintained (or a reasonably usable format) upon request. Agencies may not require requesters to accept paper copies of records that exist in electronic form. Note that Nevada\'s unusual fee structure allows agencies to charge up to $0.50/page equivalent for electronic records — requesters should ask agencies to clarify how the electronic fee is calculated, particularly for records already in electronic form that can be emailed at minimal cost.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NV_TEMPLATES = [
    {
        'jurisdiction': 'NV',
        'record_type': 'general',
        'template_name': 'General Nevada Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Nevada Public Records Act Request — NRS Chapter 239

Dear Public Records Officer:

Pursuant to the Nevada Public Records Act, NRS 239.010 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. Please clarify whether the electronic copy fee under NRS 239.052 will apply, and if so, how it is calculated per file or per page equivalent.

I am willing to pay reasonable fees under NRS 239.052. If fees will exceed ${{fee_limit}}, please notify me before incurring those costs so I may refine my request or arrange payment. Please provide an itemized fee estimate in advance.

Under NRS 239.010(1), all public books and records of governmental entities are open to inspection by any person, and exemptions must be narrowly construed in favor of disclosure. The burden of establishing that any exemption applies rests on the agency.

If any records are withheld in whole or in part, I request a written denial under NRS 239.0107(2) that: (1) identifies each record withheld; (2) states the specific statutory basis for each withholding; and (3) confirms that all non-exempt, reasonably segregable portions of partially withheld records have been released.

Under NRS 239.0107(1), please respond within 5 business days of receiving this request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the Nevada Public Records Act does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability consistent with the NPRA's policy declaration in NRS 239.001.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically from files already in electronic format, the actual reproduction cost is minimal.''',
        'expedited_language': '''I request that this NPRA request be processed as expeditiously as possible. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose Nevada NPRA template. Key Nevada features: (1) 5-business-day response deadline (NRS 239.0107(1)); (2) no administrative appeal — enforcement via district court (NRS 239.011); (3) attorney\'s fees for prevailing requesters (NRS 239.011(2)); (4) $0.25/page paper, $0.50/page electronic — unusual structure, ask agencies to clarify electronic fee calculation (NRS 239.052); (5) staff time generally not chargeable; (6) narrow construction of exemptions (NRS 239.001); (7) presumption of openness (NRS 239.010(1)). Reference "Nevada Public Records Act" or "NRS Chapter 239", not "FOIA."',
    },
    {
        'jurisdiction': 'NV',
        'record_type': 'law_enforcement',
        'template_name': 'Nevada Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Nevada Public Records Act Request — Law Enforcement Records, NRS Chapter 239

Dear Public Records Officer:

Pursuant to the Nevada Public Records Act, NRS 239.010 et seq., I request copies of the following law enforcement records:

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

Regarding claimed exemptions under NRS 239.0107(1)(b): Nevada law does not permit blanket withholding of law enforcement records. Under NRS 239.010(1) and the Nevada Supreme Court's narrow construction rule, any exemption under NRS 239.0107(1)(b) requires: (1) identification of the specific harm that would result from disclosure of each withheld record; and (2) a showing that disclosure would actually cause that harm. A generic "investigation ongoing" claim is insufficient.

[If applicable:] If no prosecution is pending or any prosecution has concluded, the NRS 239.0107(1)(b) exemption does not apply to closed matters.

Under NRS 239.0107(1), please respond within 5 business days.

I am willing to pay fees under NRS 239.052, up to ${{fee_limit}}. Please provide an itemized fee estimate in advance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions consistent with the NPRA's policy declaration in NRS 239.001. A fee waiver is appropriate given the strong public interest.''',
        'expedited_language': '''I request expedited processing of this NPRA request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Nevada NPRA law enforcement records template. Key features: (1) 5-business-day deadline (NRS 239.0107(1)); (2) NRS 239.0107(1)(b) exemption requires specific harm articulation for each withheld record — narrow construction applies (NRS 239.001); (3) completed investigation files are generally public; (4) no administrative appeal — district court enforcement (NRS 239.011); (5) attorney\'s fees for prevailing requesters (NRS 239.011(2)); (6) $0.25/page paper copy fee; note unusual $0.50/page electronic fee — clarify how calculated.',
    },
    {
        'jurisdiction': 'NV',
        'record_type': 'government_contracts',
        'template_name': 'Nevada Public Records Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Nevada Public Records Act Request — Government Contracts and Expenditures, NRS Chapter 239

Dear Public Records Officer:

Pursuant to the Nevada Public Records Act, NRS 239.010 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Invoices, payment records, and expenditure documentation under those contracts
- Requests for proposals (RFPs), bid submissions, and bid evaluation records
- Any correspondence regarding contract performance or compliance
- Any audit or review records relating to the above contracts

Regarding trade secret claims: Under NRS 239.0107(1)(c), only information that genuinely constitutes a trade secret may be withheld. Contract amounts paid with public funds, unit prices, and general contract terms are public regardless of vendor confidentiality designations. The agency must independently evaluate any trade secret claim and may not defer to vendor designations. Under NRS 239.010(1) and the Nevada Supreme Court's narrow construction rule, any exemption must be specifically established for each withheld record.

Under NRS 239.0107(1), please respond within 5 business days.

I am willing to pay fees under NRS 239.052, up to ${{fee_limit}}. Please provide an itemized estimate in advance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern the expenditure of public funds on {{public_interest_explanation}}, a core accountability matter consistent with the NPRA's policy in NRS 239.001. The public interest in knowing how public money is spent substantially outweighs any agency interest in fee recovery.''',
        'expedited_language': '''I request expedited processing of this NPRA request. These records involve ongoing expenditures of public funds where prompt disclosure is in the public interest. I need these records by {{needed_by_date}}.''',
        'notes': 'Nevada NPRA government contracts template. Key features: (1) 5-business-day deadline (NRS 239.0107(1)); (2) trade secret exemption under NRS 239.0107(1)(c) requires narrow construction — contract amounts and public expenditures are public; (3) no administrative appeal — district court enforcement (NRS 239.011); (4) attorney\'s fees for prevailing requesters (NRS 239.011(2)); (5) unusual electronic fee structure — $0.50/page electronic vs $0.25/page paper (NRS 239.052) — request electronic delivery and clarify fee calculation.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in NV_EXEMPTIONS:
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

    print(f'NV exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in NV_RULES:
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

    print(f'NV rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in NV_TEMPLATES:
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

    print(f'NV templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'NV total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nv', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
