#!/usr/bin/env python3
"""Build Kansas Open Records Act data: exemptions, rules, and templates.

Covers the Kansas Open Records Act (KORA), K.S.A. 45-215 et seq.
Kansas presumes all records are open; agencies bear the burden of proving
an exemption applies. Response deadline is 3 business days. No administrative
appeal — enforcement is via district court mandamus. Civil penalties of $500
per violation and mandatory attorney's fees for prevailing requesters.

Run: python3 scripts/build/build_ks.py
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
# KORA, K.S.A. 45-221, enumerates more than 50 specific categories of records
# that "shall not be required to be open." The exemptions are permissive —
# agencies MAY withhold qualifying records but are not required to do so.
# Kansas courts construe exemptions narrowly given the strong presumption of
# openness in K.S.A. 45-216. The burden is always on the agency to justify
# withholding. Segregability is required — partial exemptions do not justify
# full-document withholding.
# =============================================================================

KS_EXEMPTIONS = [
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(1)',
        'exemption_number': 'K.S.A. 45-221(a)(1)',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Personnel records of individual employees, officers, or applicants are exempt to the extent that disclosure would constitute a clearly unwarranted invasion of personal privacy. The exemption is not categorical — it requires a balancing test between privacy interests and the public\'s interest in disclosure.',
        'scope': 'Personnel files, performance evaluations, disciplinary records, and related documents for individual government employees where disclosure would constitute a clearly unwarranted invasion of personal privacy. The exemption is not a blanket shield for all personnel records. Kansas courts apply a balancing test: the privacy interest of the employee against the public\'s interest in accountability. Names, positions, salaries, job titles, and official conduct of public employees are generally not protected. Medical information, home addresses, and highly personal financial details carry stronger privacy interests. Disciplinary findings involving public officials acting in their official capacity are generally public.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation', 'disciplinary record',
            'personal privacy', 'clearly unwarranted invasion', 'personnel file',
            'job application', 'employment history', 'government employee',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, salaries, and official duties of public employees are public regardless of this exemption',
            'The exemption requires a "clearly unwarranted invasion of personal privacy" — a high bar that requires balancing public interest against privacy',
            'Disciplinary records of public officials relating to their official conduct are subject to the public interest in accountability',
            'Records that have already been disclosed or made public by the agency cannot be withheld retroactively',
            'Challenge overbroad claims that treat entire personnel files as exempt when only specific personal data (e.g., home address, medical condition) warrants protection',
            'K.S.A. 45-221 exemptions are permissive, not mandatory — the agency may choose to release even if an exemption applies',
        ]),
        'notes': 'K.S.A. 45-221(a)(1) is one of KORA\'s most frequently invoked exemptions. Kansas courts apply a balancing test rather than a categorical rule. The Kansas Court of Appeals has held that salaries and job classifications of government employees are not exempt. See Kansas City Star Co. v. Fossey, 230 Kan. 240 (1981). The "clearly unwarranted" standard requires more than mere privacy preference — the privacy intrusion must be plainly unjustified given the public\'s legitimate interest.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(10)',
        'exemption_number': 'K.S.A. 45-221(a)(10)',
        'short_name': 'Law Enforcement — Ongoing Investigation',
        'category': 'law_enforcement',
        'description': 'Criminal investigation records are exempt to the extent that disclosure would harm the investigation, endanger a person\'s safety, reveal a confidential informant\'s identity, or impair the ability to locate a suspect. The exemption applies only during the pendency of the investigation or prosecution — completed matters generally become public.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) harm the investigation or prosecution; (2) reveal the identity of a confidential informant; (3) endanger the life or physical safety of law enforcement personnel or witnesses; or (4) impair the ability to apprehend a suspect. The exemption is limited to active matters — once prosecution is complete or the investigation is closed without charges, the justification for withholding evaporates. Factual portions of investigation files that do not implicate any of the enumerated harms must be released. Arrest records, incident reports, and booking information documenting the existence and basic facts of an incident are generally public regardless of investigation status.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement records', 'confidential informant',
            'ongoing investigation', 'investigative technique', 'pending prosecution',
            'endanger life', 'witness protection', 'investigation file', 'police records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only to active investigations — completed cases are generally public',
            'Each withheld document must implicate one of the specific enumerated harms, not merely be "related to" an investigation',
            'Arrest records, booking information, and incident reports are generally public even during an active investigation',
            'Factual information in investigation files that does not reveal informants or techniques must be segregated and released',
            'Challenge blanket claims that all records are exempt because an investigation is "ongoing" without specific harm articulation',
            'KORA exemptions are permissive — the agency may release even if the exemption technically applies',
        ]),
        'notes': 'K.S.A. 45-221(a)(10) is Kansas\'s primary law enforcement investigation exemption. Kansas courts require agencies to tie each withholding decision to a specific, articulable harm — a generic "investigation pending" response is insufficient. The exemption is permissive: the agency is not required to withhold even if the exemption applies. After prosecution concludes, the exemption largely disappears.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(8)',
        'exemption_number': 'K.S.A. 45-221(a)(8)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records that are privileged under the attorney-client relationship or protected as attorney work product are exempt from required disclosure under KORA. The exemption tracks the common-law privilege as applied to government entities.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of seeking or providing legal advice, and attorney work product prepared in anticipation of litigation or for trial. The privilege requires: (1) an attorney-client relationship; (2) confidential communications; (3) made for the purpose of legal (not business or policy) advice. Billing records and retainer agreements are generally not privileged. Facts independently known to the agency are not protected merely because they were communicated to an attorney. The privilege can be waived by disclosure to third parties not involved in the legal matter.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'attorney work product', 'legal opinion',
            'confidential communication', 'government attorney', 'outside counsel',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not general business or policy guidance',
            'Attorney billing records and invoices are generally public — privilege covers content, not existence of the relationship',
            'Waiver occurs when the agency discloses the privileged content in public proceedings or to non-attorney personnel not involved in the matter',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and mental impressions',
            'Challenge whether communications characterized as "legal advice" were actually business or policy decisions',
            'K.S.A. 45-221 exemptions are permissive — even if privilege applies, the agency may choose to release',
        ]),
        'notes': 'K.S.A. 45-221(a)(8) incorporates attorney-client privilege and work product doctrine into KORA. Kansas courts apply the standard common-law privilege analysis. The fact that an attorney reviewed a document does not automatically make it privileged — the communication must have been for legal advice purposes. Government waiver of the privilege is analyzed under the same standards as private clients.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(30)',
        'exemption_number': 'K.S.A. 45-221(a)(30)',
        'short_name': 'Preliminary Drafts and Deliberative Materials',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and memoranda prepared as part of the deliberative or decision-making process that are not adopted as the agency\'s final position are exempt from required disclosure.',
        'scope': 'Predecisional, deliberative documents: preliminary drafts, working papers, notes, recommendations, and memoranda reflecting the agency\'s deliberative process. The exemption requires that the document: (1) be predecisional — prepared before the final agency decision; and (2) be deliberative — contain opinion, analysis, or recommendation rather than pure fact. Purely factual material, even within deliberative documents, must be segregated and released. Once a draft or recommendation is adopted as the agency\'s final position, it becomes public. Working law — standards and criteria the agency actually applies — must be disclosed. The exemption is designed to protect the candor of internal agency discussions, not to shield government decisions from accountability.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'working paper',
            'intra-agency memorandum', 'recommendation', 'draft document',
            'policy deliberation', 'advisory opinion', 'working notes',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released',
            'Once the draft or recommendation is adopted as final agency policy, the exemption no longer applies',
            '"Working law" — standards the agency actually applies in practice — must be disclosed even if in internal documents',
            'Documents circulated outside the agency lose their predecisional character',
            'Challenge claims that entire documents are exempt when only recommendation or opinion sections qualify',
            'The exemption covers the deliberative process, not the underlying facts on which the decision was based',
        ]),
        'notes': 'K.S.A. 45-221(a)(30) is Kansas\'s deliberative process exemption. Kansas courts apply the standard factual/opinion distinction — factual data does not become deliberative merely because it is embedded in a recommendation memorandum. The exemption is permissive and requires the agency to articulate the specific deliberative harm from disclosure.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(4)',
        'exemption_number': 'K.S.A. 45-221(a)(4)',
        'short_name': 'Medical, Psychiatric, and Social Work Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, psychological, and social work records that would constitute a clearly unwarranted invasion of personal privacy are exempt from required disclosure. This includes health records of individual patients or clients of government health and social services agencies.',
        'scope': 'Medical and mental health records, psychiatric and psychological evaluations, and social work case files held by state and local government agencies that relate to identified individuals. Covers records held by state hospitals, Medicaid agencies, Department for Children and Families, and other government health and social services providers. The exemption is linked to the "clearly unwarranted invasion of personal privacy" standard, requiring a balancing of the individual\'s health privacy interest against the public interest in disclosure. Aggregate health data and anonymized records are generally not covered. Administrative and financial records of government health agencies are public.',
        'key_terms': json.dumps([
            'medical records', 'psychiatric records', 'psychological evaluation', 'social work records',
            'health information', 'patient records', 'mental health records', 'HIPAA',
            'clearly unwarranted invasion', 'personal health information', 'patient privacy',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized health data are not covered by this exemption',
            'Administrative and financial records of government health agencies are fully public',
            'Records relating to a public official\'s fitness for duty in a government position may be subject to disclosure where the public interest in accountability outweighs privacy',
            'Challenge overbroad withholding where the agency has not identified the specific privacy harm from disclosure of specific records',
            'KORA exemptions are permissive — the agency may release even if technically exempt',
        ]),
        'notes': 'K.S.A. 45-221(a)(4) protects medical, psychiatric, and social work records. The "clearly unwarranted invasion of personal privacy" standard requires a genuine balancing — not a categorical rule that all health records are always exempt. Kansas courts apply the balancing test case by case. Administrative records of health agencies (budgets, contracts, staffing) are entirely separate from patient records and are not covered.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(23)',
        'exemption_number': 'K.S.A. 45-221(a)(23)',
        'short_name': 'Trade Secrets and Proprietary Business Information',
        'category': 'commercial',
        'description': 'Trade secrets, proprietary business information, and commercial or financial information submitted by private entities to government agencies are exempt where disclosure would give competitors an unfair advantage or would constitute a clearly unwarranted invasion of the submitter\'s business privacy.',
        'scope': 'Commercially sensitive information submitted by private businesses to government agencies that: (1) qualifies as a trade secret under Kansas law; or (2) constitutes commercial or financial information whose disclosure would cause competitive harm. Kansas applies the Uniform Trade Secrets Act. The exemption does not cover government-generated records, expenditures of public funds, contract amounts, or publicly available information. Agencies may not simply defer to vendor trade secret designations — they must independently evaluate the claim. General business information that is not genuinely commercially sensitive does not qualify.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'competitive harm',
            'business confidential', 'UTSA', 'Uniform Trade Secrets Act',
            'financial information', 'competitive advantage', 'proprietary data',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate that the information meets the UTSA definition — a confidential designation is not sufficient',
            'Contract amounts paid with public funds are public regardless of trade secret claims',
            'Publicly available information cannot qualify as a trade secret',
            'Government-generated records cannot constitute trade secrets — only privately submitted information qualifies',
            'Challenge whether the submitter actually maintained reasonable secrecy measures',
            'Agencies must conduct an independent evaluation and may not simply accept vendor designations',
        ]),
        'notes': 'K.S.A. 45-221(a)(23) protects trade secrets and proprietary business information. Kansas courts apply the UTSA framework and require genuine independent evaluation by the agency. Contract prices, bid amounts, and public expenditures are uniformly public. The exemption is permissive — the agency may release even if the exemption technically applies.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(2)',
        'exemption_number': 'K.S.A. 45-221(a)(2)',
        'short_name': 'Records Exempt by Other Statutes',
        'category': 'statutory',
        'description': 'Records that are specifically required or authorized to be kept confidential by federal or state statute are exempt from required disclosure under KORA. This exemption incorporates external statutory confidentiality provisions by reference.',
        'scope': 'Records that are specifically designated as confidential by an external Kansas statute or federal law. The exemption requires that the external statute specifically mandate or authorize confidentiality — general statutory language is not sufficient. Examples include tax return information (K.S.A. 79-3234), child welfare records (K.S.A. 38-2209), and adoption records (K.S.A. 59-2122). The exemption is a passthrough to the specific external statute; requesters should identify and analyze the cited external statute independently. Agencies may not bootstrap a general policy preference into a statutory exemption by citing this provision without identifying a specific external statute.',
        'key_terms': json.dumps([
            'statutory exemption', 'confidential by statute', 'federal law', 'state statute',
            'required to be kept confidential', 'statutory confidentiality', 'authorized by statute',
            'tax records', 'child welfare', 'adoption records', 'external statute',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific external statute that mandates or authorizes confidentiality — general "this is sensitive" claims are insufficient',
            'The cited external statute must actually mandate or authorize confidentiality for the specific type of record requested',
            'Many records claimed under this exemption can be challenged by analyzing the actual scope of the cited external statute',
            'Aggregate data and anonymized records are generally not covered even if individual records are statutorily confidential',
            'Challenge whether the external statute applies to the specific records requested or only to a subset',
        ]),
        'notes': 'K.S.A. 45-221(a)(2) is a passthrough exemption that incorporates external statutes. The analysis depends on the specific external statute cited. Agencies must identify the external statute with specificity. This exemption is frequently overclaimed — requesters should obtain the specific statutory citation and independently verify its applicability.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(11)',
        'exemption_number': 'K.S.A. 45-221(a)(11)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property and personal property appraisals and related evaluation documents prepared by or for an agency in connection with prospective acquisition of property are exempt until the acquisition is complete or the agency abandons the transaction.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared by or for a government agency in connection with prospective purchase, condemnation, or lease of real property. The exemption is time-limited — it expires automatically when the transaction closes, is formally abandoned, or the agency publicly discloses the appraisal value. The purpose is to prevent negotiating disadvantage by shielding the agency\'s maximum willingness to pay during active negotiations. Post-transaction, all appraisal documents become public records. Appraisals for property the agency already owns (not in acquisition mode) are not covered.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation', 'pre-acquisition',
            'condemnation appraisal', 'feasibility study', 'land purchase', 'real property',
            'property negotiation', 'acquisition pending',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction is complete, cancelled, or abandoned',
            'Challenge the claim that a transaction is still "pending" if there has been no activity for an extended period',
            'Appraisals for property the agency already owns are not covered by this exemption',
            'After a final condemnation judgment, all valuation records are public',
            'Budget estimates and general discussions about property values are not formal appraisals and may not qualify',
        ]),
        'notes': 'K.S.A. 45-221(a)(11) protects pre-acquisition appraisals. The exemption is strictly time-limited to the acquisition period. Kansas courts have held that the exemption terminates upon completion of the transaction regardless of whether the agency formally "closes" the file.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(6)',
        'exemption_number': 'K.S.A. 45-221(a)(6)',
        'short_name': 'Security Plans for Public Buildings and Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and operational security documents for public buildings and critical infrastructure are exempt where disclosure would create a specific, articulable security risk to persons or facilities.',
        'scope': 'Security plans, vulnerability assessments, access control procedures, intrusion detection systems, and similar operational security documents for public buildings, water systems, transportation networks, and other critical infrastructure. The exemption requires a specific, articulable security risk from disclosure — not a general claim that the records are security-related. Budget and expenditure records for security programs are generally public. Physical security plans for non-critical facilities with widely known access patterns do not qualify. The agency must demonstrate that disclosure of the specific records would create a concrete risk, not merely a theoretical one.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure', 'security risk',
            'access control', 'public building security', 'infrastructure protection',
            'emergency response plan', 'intrusion detection', 'security procedures',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative or general',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal exploitable vulnerabilities are not covered',
            'Challenge claims that entire security contracts are exempt when only specific technical specifications warrant protection',
            'Physical security plans for facilities with widely known access patterns do not qualify',
        ]),
        'notes': 'K.S.A. 45-221(a)(6) protects security plans and vulnerability assessments. Kansas courts require agencies to articulate a specific risk — a generic assertion that records are "security-related" is insufficient. Expenditure and administrative records for security programs remain public.',
    },
    {
        'jurisdiction': 'KS',
        'statute_citation': 'K.S.A. 45-221(a)(26)',
        'exemption_number': 'K.S.A. 45-221(a)(26)',
        'short_name': 'Financial Institution Examination Records',
        'category': 'commercial',
        'description': 'Examination reports, confidential supervisory information, and related records produced in connection with the examination and regulation of financial institutions by the Office of the State Bank Commissioner and other financial regulators are exempt from required disclosure.',
        'scope': 'Confidential supervisory information produced in connection with the examination and regulation of state-chartered banks, credit unions, mortgage lenders, insurance companies, and other financial institutions regulated under Kansas law. Includes examination reports, safety-and-soundness findings, matters requiring attention (MRA) letters, and related regulatory correspondence. Final enforcement orders, consent agreements, public sanctions, license status, and aggregate financial statistics are public. The exemption is designed to protect the candid supervisory exchange between regulators and regulated entities essential to effective financial regulation.',
        'key_terms': json.dumps([
            'financial institution examination', 'bank examination', 'supervisory information',
            'State Bank Commissioner', 'safety and soundness', 'confidential examination report',
            'regulatory correspondence', 'bank regulation', 'credit union examination',
            'financial regulator',
        ]),
        'counter_arguments': json.dumps([
            'Final enforcement orders, consent agreements, and public sanctions are not covered — they are public from issuance',
            'License status, licensing history, and financial data aggregated for public reporting are public',
            'Challenge claims that all correspondence between a regulator and a financial institution is "examination records"',
            'Information about final regulatory decisions that affected the public (e.g., bank closures, enforcement actions) is public',
        ]),
        'notes': 'K.S.A. 45-221(a)(26) protects financial institution examination records. The exemption mirrors the federal model of confidential banking supervision. It does not cover public enforcement actions, license status, or aggregate financial data. Final orders and consent agreements are public records from the moment of issuance.',
    },
]

# =============================================================================
# RULES
# Kansas Open Records Act, K.S.A. 45-215 et seq.
# Kansas imposes a 3-business-day response deadline — one of the shorter
# deadlines in the country. No administrative appeal mechanism exists —
# enforcement is directly in district court via mandamus or injunction.
# Civil penalties of $500 per violation and mandatory attorney's fees for
# prevailing requesters. Exemptions are permissive, not mandatory.
# =============================================================================

KS_RULES = [
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'K.S.A. 45-218(d)',
        'notes': 'Kansas agencies must respond to a KORA request within 3 business days of receiving it. This is one of the shortest statutory response deadlines in the country. The agency must either (1) provide the requested records; (2) provide written notice that additional time is needed and state the reason; or (3) deny the request in writing with the specific statutory basis for the denial. If the agency needs additional time, it must specify when records will be available. The 3-business-day clock begins on receipt of the request, not on the next business day. A delay beyond 3 business days without written notice is itself a KORA violation.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-218(e)',
        'notes': 'When a Kansas agency denies a KORA request in whole or in part, the denial must be in writing and must state the specific statutory basis for the denial — a citation to K.S.A. 45-221 and the specific subsection. A blanket denial without statutory citation is a KORA violation. The written denial must identify the specific records withheld and the legal basis for withholding each. Partial denials must be accompanied by production of all non-exempt, reasonably segregable portions of withheld records. The written denial is important for establishing the record for any subsequent court challenge.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-221(b)',
        'notes': 'When a record contains both exempt and non-exempt information, the agency must release all non-exempt, reasonably segregable portions. Kansas agencies may not withhold entire documents merely because some portion qualifies for an exemption. K.S.A. 45-221(b) explicitly requires that agencies identify exempt portions and release the remainder. Blanket withholding of documents with mixed content is a KORA violation. The agency must describe what was redacted and the legal basis for each redaction.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-216',
        'notes': 'K.S.A. 45-216 establishes that the policy of the State of Kansas is that public records be open for inspection by any person. The burden of justifying any withholding rests entirely on the agency — requesters need not demonstrate a need for or interest in records. KORA exemptions are permissive ("shall not be required to be open") rather than mandatory — agencies may choose to release records even if technically exempt. The presumption of openness is a core substantive rule, not merely an interpretive guide.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'identity_and_purpose_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-217',
        'notes': 'Kansas agencies may NOT require requesters to identify themselves or state the reason for their request as a condition of access to public records. K.S.A. 45-217 provides that any person may inspect and copy public records regardless of identity. Requiring identification or purpose as a condition of access is a KORA violation. Some agencies may ask for contact information for delivery purposes — but providing it must be voluntary and not a condition of compliance.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-219',
        'notes': 'Kansas agencies may charge fees for copying public records at a rate not to exceed $0.25 per page. Agencies may also charge for the actual cost of reproduction for other formats. Staff time for locating, reviewing, or redacting records is generally a permissible fee element in Kansas — unlike some states where staff time charges are prohibited. Agencies must publish their fee schedules. Fees must be reasonable and may not be set so high as to constitute a practical barrier to access. For electronic records, fees should reflect only actual reproduction costs.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_fee_allowed',
        'param_value': 'yes_with_limits',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-219',
        'notes': 'Kansas agencies may charge for staff time spent locating, reviewing, and redacting records under K.S.A. 45-219, subject to reasonableness limits. This distinguishes Kansas from states that prohibit staff time charges. However, staff time fees must be reasonable, must be based on the actual hourly rate of the lowest-paid employee capable of performing the task, and must be disclosed in advance if they will be significant. Requester may challenge fees that appear designed to discourage access rather than to recover genuine costs.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-219',
        'notes': 'KORA does not provide a mandatory fee waiver for any category of requesters. Agencies may waive fees at their discretion. Requesters — particularly journalists, nonprofits, and academic researchers — can request a fee waiver by demonstrating that the records serve a significant public interest. While there is no legal right to a fee waiver, agencies frequently grant them for requests that clearly serve the public interest. Electronic delivery often eliminates or minimizes reproduction fees.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-222',
        'notes': 'Kansas has NO formal administrative appeal mechanism for KORA denials. There is no agency head review, no ombudsman, and no administrative tribunal. A requester denied access must seek enforcement directly in district court. K.S.A. 45-222 provides the district court enforcement mechanism. This makes Kansas a direct-to-court state, which concentrates enforcement power but also requires litigation for formal relief.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_mandamus',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-222',
        'notes': 'A requester denied access to public records may seek a writ of mandamus or injunctive relief in the district court of the county where the public agency is located or where the requester resides. K.S.A. 45-222 provides the enforcement mechanism. The court may order the agency to permit inspection and copying of records. There is no specific statute of limitations, but requesters should act promptly. District court enforcement is the only formal remedy available under KORA.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_per_violation',
        'param_value': '500',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-223',
        'notes': 'A public agency or individual officer who violates KORA is subject to a civil penalty of $500 per violation under K.S.A. 45-223. The penalty applies to each violation — willful withholding of multiple records may result in multiple $500 penalties. The civil penalty is in addition to any other relief ordered by the court, including attorney\'s fees and costs. The penalty can be imposed on the agency itself or on the individual officer responsible for the violation. This is a meaningful enforcement mechanism that courts take seriously.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-222(c)',
        'notes': 'A requester who prevails in a KORA enforcement action may recover attorney\'s fees and other litigation costs from the agency. K.S.A. 45-222(c) provides for attorney\'s fees for the prevailing party. While phrased permissively ("may"), Kansas courts routinely award fees to prevailing requesters as a matter of KORA enforcement policy. The availability of attorney\'s fees makes it economically viable to bring enforcement actions for denied records even when the immediate monetary stakes are modest.',
    },
    {
        'jurisdiction': 'KS',
        'rule_type': 'initial_response',
        'param_key': 'exemptions_permissive_not_mandatory',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'K.S.A. 45-221',
        'notes': 'A distinctive feature of KORA is that all exemptions in K.S.A. 45-221 are permissive — they provide that listed records "shall not be required to be open" but do not mandate withholding. An agency may choose to release records even if an exemption technically applies. This is an important distinction: requesters can argue that the agency should exercise its discretion to release even technically exempt records where the public interest in disclosure is strong. Agencies that withhold solely because an exemption exists may be acting more restrictively than KORA requires.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

KS_TEMPLATES = [
    {
        'jurisdiction': 'KS',
        'record_type': 'general',
        'template_name': 'General Kansas Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Kansas Open Records Act Request — K.S.A. 45-215 et seq.

Dear Public Records Officer:

Pursuant to the Kansas Open Records Act (KORA), K.S.A. 45-215 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available to minimize cost and production time.

I am willing to pay reasonable fees under K.S.A. 45-219. If fees will exceed ${{fee_limit}}, please notify me before incurring those costs so I may refine my request or arrange payment. Please provide an itemized fee estimate in advance.

Under K.S.A. 45-216, all public records are presumed open and accessible to any person. Under K.S.A. 45-221(b), if any records or portions of records are withheld, you must release all non-exempt, reasonably segregable portions.

If any records are withheld in whole or in part, I request a written denial under K.S.A. 45-218(e) that: (1) identifies each record withheld; (2) states the specific statutory basis (K.S.A. 45-221 subsection) for each withholding; and (3) confirms that all non-exempt portions of partially withheld records have been released.

I also note that KORA exemptions under K.S.A. 45-221 are permissive ("shall not be required to be open"), not mandatory. Even if an exemption applies, I respectfully ask that the agency exercise its discretion to release records where the public interest in disclosure is strong.

Under K.S.A. 45-218(d), please respond within 3 business days of receiving this request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While KORA does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, reproduction costs are minimal or zero.

KORA's strong presumption of openness (K.S.A. 45-216) supports a fee waiver for requests that serve the public interest.''',
        'expedited_language': '''I request that this KORA request be processed as expeditiously as possible. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose KORA template. Key Kansas features: (1) 3-business-day response deadline — one of the shortest in the country (K.S.A. 45-218(d)); (2) no administrative appeal — enforcement is via district court mandamus (K.S.A. 45-222); (3) civil penalties of $500 per violation (K.S.A. 45-223); (4) attorney\'s fees for prevailing requesters (K.S.A. 45-222(c)); (5) exemptions are permissive, not mandatory (K.S.A. 45-221); (6) $0.25/page copy fee cap (K.S.A. 45-219); (7) staff time fees are allowed but must be reasonable. Reference "KORA" or "K.S.A. 45-215 et seq.", not "FOIA."',
    },
    {
        'jurisdiction': 'KS',
        'record_type': 'law_enforcement',
        'template_name': 'Kansas KORA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Kansas Open Records Act Request — Law Enforcement Records, K.S.A. 45-215 et seq.

Dear Public Records Officer:

Pursuant to the Kansas Open Records Act (KORA), K.S.A. 45-215 et seq., I request copies of the following law enforcement records:

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

Regarding claimed exemptions under K.S.A. 45-221(a)(10): Kansas law does not permit blanket withholding of law enforcement records. Any withholding under K.S.A. 45-221(a)(10) requires: (1) identification of the specific harm that would result from disclosure (e.g., would identify a confidential informant; would endanger a specific person; would impair an ongoing prosecution); and (2) articulation of how disclosure of each specific withheld record would cause that specific harm. A generic "investigation ongoing" response is insufficient.

[If applicable:] If no prosecution is pending or any related prosecution has concluded, please apply the standard for completed investigations — the interference rationale under K.S.A. 45-221(a)(10) does not apply to closed matters.

Note also that K.S.A. 45-221 exemptions are permissive — the agency may choose to release records even if an exemption technically applies.

Under K.S.A. 45-218(d), please respond within 3 business days of receiving this request.

I am willing to pay fees under K.S.A. 45-219, up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs minimal reproduction cost. A fee waiver is consistent with KORA's strong presumption of openness under K.S.A. 45-216.''',
        'expedited_language': '''I request expedited processing of this KORA request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'KORA law enforcement records template. Kansas-specific features: (1) 3-business-day response deadline (K.S.A. 45-218(d)); (2) K.S.A. 45-221(a)(10) exemption requires specific harm articulation for each withheld record — not blanket "investigation pending"; (3) completed investigation files are generally public once prosecution concludes; (4) K.S.A. 45-221 exemptions are permissive — agencies can release even if technically exempt; (5) $500 civil penalty per violation (K.S.A. 45-223) if agency wrongfully withholds; (6) attorney\'s fees for prevailing requesters (K.S.A. 45-222(c)); (7) direct district court enforcement — no administrative appeal.',
    },
    {
        'jurisdiction': 'KS',
        'record_type': 'government_contracts',
        'template_name': 'Kansas KORA Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Kansas Open Records Act Request — Government Contracts and Expenditures, K.S.A. 45-215 et seq.

Dear Public Records Officer:

Pursuant to the Kansas Open Records Act (KORA), K.S.A. 45-215 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Invoices, payment records, and expenditure documentation under those contracts
- Requests for proposals (RFPs), bid submissions, and bid evaluation records
- Any correspondence regarding contract negotiation, performance, or compliance
- Any audit or review records relating to the above contracts

Regarding trade secret claims: Under K.S.A. 45-221(a)(23), only information that genuinely qualifies as a trade secret under the Uniform Trade Secrets Act may be withheld. Contract amounts paid with public funds, unit prices for services procured with public money, and general contract terms are public regardless of vendor confidentiality designations. The agency must independently evaluate any trade secret claim and may not simply defer to vendor designations.

Under K.S.A. 45-216, all public records are presumed open. Under K.S.A. 45-221(b), all non-exempt, reasonably segregable portions of any partially withheld record must be released.

Under K.S.A. 45-218(d), please respond within 3 business days.

I am willing to pay fees under K.S.A. 45-219, up to ${{fee_limit}}. Please provide an itemized estimate before incurring significant costs.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern the expenditure of public funds on {{public_interest_explanation}}, which is a core accountability matter. The public interest in knowing how tax dollars are spent substantially outweighs any agency interest in fee recovery. A fee waiver is consistent with KORA's presumption of openness under K.S.A. 45-216.''',
        'expedited_language': '''I request expedited processing of this KORA request. These records involve ongoing expenditures of public funds where prompt disclosure is in the public interest. I need these records by {{needed_by_date}}.''',
        'notes': 'KORA government contracts template. Key Kansas features: (1) contract amounts and expenditures with public funds are public regardless of trade secret claims — challenge overbroad vendor confidentiality designations; (2) K.S.A. 45-221(a)(23) trade secret exemption requires genuine independent evaluation by the agency, not deference to vendor designations; (3) K.S.A. 45-221(b) requires segregation — even if some contract provisions qualify for exemption, non-exempt pricing and terms must be released; (4) 3-business-day response deadline; (5) $500 civil penalty per violation; (6) attorney\'s fees for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in KS_EXEMPTIONS:
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

    print(f'KS exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in KS_RULES:
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

    print(f'KS rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in KS_TEMPLATES:
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

    print(f'KS templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'KS total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ks', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
