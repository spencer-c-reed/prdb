#!/usr/bin/env python3
"""Build North Dakota Open Records Law data: exemptions, rules, and templates.

Covers North Dakota's Open Records Law, NDCC § 44-04-18 et seq.
North Dakota provides a broadly inclusive right of public access but with a
large number of specific statutory exemptions scattered throughout the code.
The Attorney General issues advisory opinions (not binding) and courts apply
a presumption of openness. No administrative appeal mechanism — district court
is the first and only formal enforcement venue. Attorney's fees available.

Run: python3 scripts/build/build_nd.py
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
# North Dakota's Open Records Law, NDCC § 44-04-18, creates a broad public
# right of access to all records of public entities. Exemptions must be
# specifically established by statute — the burden is on the agency to
# identify the specific statutory provision authorizing withholding. The AG
# issues advisory opinions interpreting the law (persuasive, not binding).
# Courts apply a presumption of openness. NDCC § 44-04-18.1 lists most of
# the categorical exemptions, but dozens more appear throughout the code.
# =============================================================================

ND_EXEMPTIONS = [
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(1)',
        'exemption_number': 'NDCC § 44-04-18.1(1)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, psychological, and other records created by or for a health care provider that pertain to the diagnosis, treatment, or health history of a patient are exempt from public disclosure to protect patient privacy.',
        'scope': 'Records created or maintained by health care providers — including hospitals, clinics, and public health agencies — that pertain to individual patient diagnosis, treatment, or health history. Covers both physical and mental health records. The exemption applies to records held by public entities in their capacity as health care providers (e.g., state hospital, public health department). General public health statistics, aggregate disease surveillance data, and operational records of health agencies that do not identify individual patients are not covered. Budget, staffing, and facility records of public health agencies are public.',
        'key_terms': json.dumps([
            'medical record', 'health record', 'patient record', 'psychiatric record',
            'mental health record', 'diagnosis', 'treatment', 'health history',
            'health care provider', 'HIPAA', 'patient privacy',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies to patient-specific records — aggregate health statistics and public health data without individual identifiers are public',
            'Operational and administrative records of public health agencies (budgets, contracts, staffing) are public regardless of this exemption',
            'Records that have been de-identified so that no individual is identifiable are not covered',
            'The agency must demonstrate the record pertains to a specific patient\'s diagnosis or treatment, not merely that the record was created by a health care provider',
            'The exemption does not shield public health agencies from accountability for their programs and spending — only patient-specific clinical records are protected',
        ]),
        'notes': 'NDCC § 44-04-18.1(1) is one of the most clearly established categorical exemptions in North Dakota\'s Open Records Law. Federal HIPAA requirements also apply to covered entities and may independently require protection of protected health information. The AG has consistently issued opinions affirming that patient records are exempt but operational health agency records are not.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(2)',
        'exemption_number': 'NDCC § 44-04-18.1(2)',
        'short_name': 'Personnel Records — Personal Information',
        'category': 'privacy',
        'description': 'Certain personal information in employee personnel files — including Social Security numbers, home addresses, home telephone numbers, and medical information — is exempt from public disclosure. However, job title, salary, dates of employment, and work performance information relating to public employees are public.',
        'scope': 'Personnel records of public employees, but the exemption is narrowly limited to specific personal data fields: SSNs, home addresses, home telephone numbers, medical information, and similar sensitive personal data. The exemption does NOT cover: job title, position, salary, dates of employment, job duties, disciplinary actions and their outcomes, performance evaluations that resulted in employment action, or records of misconduct. The name of the employee is public. North Dakota courts and AG opinions consistently hold that public employee compensation and disciplinary history are public under the principle that citizens have a right to know how public servants perform their duties.',
        'key_terms': json.dumps([
            'personnel record', 'employee record', 'Social Security number', 'home address',
            'home telephone', 'salary', 'public employee', 'disciplinary action',
            'performance evaluation', 'job title', 'compensation',
        ]),
        'counter_arguments': json.dumps([
            'Name, job title, salary, and dates of employment for public employees are explicitly public — this exemption is field-specific',
            'Disciplinary records and their outcomes are public records in North Dakota — the exemption does not shield misconduct from disclosure',
            'Performance evaluations that resulted in employment actions (termination, demotion, suspension) are public',
            'The agency must release the entire record with only the specifically protected fields (SSN, home address, home phone, medical info) redacted',
            'Challenge overbroad claims that entire personnel files are exempt — only enumerated sensitive data fields are protected',
            'AG Advisory Opinions consistently hold that compensation and disciplinary history of public employees are public',
        ]),
        'notes': 'NDCC § 44-04-18.1(2) reflects North Dakota\'s balance between employee privacy and public accountability. The AG has been firm in advisory opinions that public employee compensation is a public record and that agencies may not use this exemption to shield disciplinary history or performance records from the public.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(12)',
        'exemption_number': 'NDCC § 44-04-18.1(12)',
        'short_name': 'Law Enforcement Investigative Records',
        'category': 'law_enforcement',
        'description': 'Records of active law enforcement investigations that would interfere with the investigation, identify a confidential informant, or endanger a person\'s safety are exempt. Records of concluded investigations are generally public.',
        'scope': 'Investigative records of active criminal investigations where disclosure would: (1) interfere with the investigation or prosecution; (2) reveal the identity of a confidential informant; (3) endanger the life or physical safety of any person; or (4) reveal investigative techniques not generally known to the public. The exemption is time-limited — once an investigation is concluded (prosecution complete, charges declined, or investigation closed), the exemption no longer applies and records become public. Factual portions of investigative files (incident descriptions, witness names for completed matters, basic incident information) that do not implicate an enumerated harm must be segregated and released.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'active investigation',
            'confidential informant', 'investigative technique', 'pending investigation',
            'interference with prosecution', 'endangerment', 'closed investigation',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only to active investigations — once prosecution is complete or investigation is closed, records become public',
            'Incident reports documenting the existence of an event, arrest records, and booking information are generally public regardless of investigation status',
            'The agency must identify the specific harm — "investigation ongoing" is not sufficient justification for withholding every record in the file',
            'Factual portions of investigative records that do not reveal informants, techniques, or endanger safety must be segregated and released',
            'Challenge claims that an investigation remains "active" when there has been no investigative activity for an extended period',
            'Records about completed prosecutions and their outcomes are public — courts\' records in criminal cases are always public',
        ]),
        'notes': 'NDCC § 44-04-18.1(12) tracks the standard law enforcement investigative records exemption found in most state open records laws. North Dakota AG opinions emphasize that the exemption is not a permanent shield — concluded investigation files are public. The AG has also noted that arrest records and basic incident information are public even during active investigations.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(6)',
        'exemption_number': 'NDCC § 44-04-18.1(6)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted to a public entity in confidence, whose disclosure would cause competitive harm to the submitter, are exempt from public disclosure.',
        'scope': 'Information submitted by private parties to state agencies that: (1) constitutes a trade secret under North Dakota law; or (2) is commercial or financial information submitted in confidence when the agency gives an assurance of confidentiality and disclosure would cause competitive harm. The agency must independently evaluate whether the information qualifies — a "confidential" designation by the submitter is not controlling. Publicly available information cannot be withheld. Amounts paid with public funds and contract prices are generally public regardless of trade secret claims. Government-generated analysis and reports using submitted data are public even when the underlying submitted data might be exempt.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm', 'commercial information',
            'financial information', 'confidential business information', 'competitive advantage',
            'economic value', 'trade secret designation', 'secrecy',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must establish that the information meets the trade secret definition — a stamp or self-designation is not sufficient',
            'Publicly available information cannot be withheld as a trade secret regardless of the submitter\'s characterization',
            'Contract prices and amounts paid with public funds are public regardless of trade secret claims',
            'The agency must conduct an independent analysis — it may not automatically defer to the submitter\'s designation',
            'Challenge whether the submitter actually maintained reasonable secrecy measures',
            'Government analysis and reports based on submitted data are public even if the raw submitted data is exempt',
        ]),
        'notes': 'NDCC § 44-04-18.1(6) requires agencies to independently evaluate trade secret claims. The AG has issued opinions emphasizing that agencies may not rubber-stamp vendor confidentiality claims and that amounts paid with public funds are always public.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(5)',
        'exemption_number': 'NDCC § 44-04-18.1(5)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Communications between a public entity and its attorneys that are subject to the attorney-client privilege, and attorney work product prepared in anticipation of litigation, are exempt from public disclosure.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining or providing legal advice, and work product prepared by attorneys in anticipation of or in connection with litigation. The attorney-client privilege for government entities in North Dakota requires: (1) a communication between the government and its attorney; (2) made in confidence; (3) for the purpose of legal advice (not policy or business advice); and (4) not subsequently waived. Billing records, retainer agreements, and general financial arrangements with outside counsel are not privileged. The privilege is held by the agency (the client) and may be waived.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'confidential communication', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy guidance, administrative decisions, or general business counsel',
            'Waiver occurs through disclosure to third parties not involved in the legal matter or in public proceedings',
            'Billing records and invoices describing services rendered are generally public',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis and opinion',
            'Work product protection requires the document be prepared in anticipation of actual or reasonably expected litigation, not merely possible future disputes',
            'Challenge whether the agency has constructively waived by relying on the legal advice publicly',
        ]),
        'notes': 'North Dakota recognizes the attorney-client privilege and work product doctrine as exemptions to its Open Records Law. The AG has noted that these privileges belong to the agency-client and must be affirmatively asserted — agencies cannot retroactively claim privilege after producing records. The ND Supreme Court applies privilege narrowly in the public context.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(7)',
        'exemption_number': 'NDCC § 44-04-18.1(7)',
        'short_name': 'Preliminary and Deliberative Process Records',
        'category': 'deliberative',
        'description': 'Preliminary drafts and notes, recommendations, and intra-agency memorandums that are not adopted as final agency policy and contain opinions on legal or policy matters are exempt from public disclosure to protect the deliberative process.',
        'scope': 'Preliminary drafts, working notes, recommendations, and intra-agency or inter-agency memorandums that: (1) are predecisional (not yet adopted as agency position); and (2) contain opinions, policy recommendations, or legal analysis rather than purely factual material. The exemption does NOT protect: (a) purely factual information, even if embedded in deliberative documents; (b) records that have been adopted as agency policy; (c) "working law" — standards and criteria agencies actually apply even if labeled internal. Factual data underlying recommendations must be segregated and released. The North Dakota courts apply this exemption narrowly, consistent with the presumption of openness.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'predecisional', 'working paper', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'opinion', 'working law',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — the exemption covers only opinion and recommendation portions',
            'Once a draft or recommendation is adopted as agency policy, the exemption no longer applies',
            '"Working law" — standards and criteria actually applied in agency decisions — must be disclosed even if labeled internal',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'Documents shared with parties outside the agency may lose their predecisional character',
            'The burden is on the agency to demonstrate each specific document, or specific portion, is predecisional and opinion-based',
        ]),
        'notes': 'NDCC § 44-04-18.1(7) is the North Dakota analog to the federal deliberative process privilege. The AG has issued advisory opinions requiring agencies to release factual information within deliberative documents. The ND Supreme Court has held that the exemption must be applied narrowly consistent with the presumption of openness.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(13)',
        'exemption_number': 'NDCC § 44-04-18.1(13)',
        'short_name': 'Security and Infrastructure Protection Plans',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and related records for public buildings and critical infrastructure are exempt where disclosure would create a specific and articulable security risk to public safety.',
        'scope': 'Security plans, vulnerability assessments, access control systems, intrusion detection systems, and similar operational security documents for public facilities and critical infrastructure. The exemption requires that disclosure create a specific and identifiable security risk — generalized assertions that records are "security-related" are insufficient. Budget records, contract pricing, and expenditure data for security programs are generally public. The agency must articulate the specific harm that would result from disclosure of each withheld record.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'access control', 'intrusion detection', 'emergency response',
            'facility security', 'infrastructure protection', 'cybersecurity',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative or general',
            'Budget and expenditure records for security programs are public regardless of this exemption',
            'General descriptions of security policies that do not reveal specific vulnerabilities are not covered',
            'Challenge claims that entire security vendor contracts are exempt when only specific technical specifications might warrant protection',
            'Security plans for non-critical facilities with widely known access patterns do not qualify',
        ]),
        'notes': 'NDCC § 44-04-18.1(13) mirrors the security exemption found in most state open records laws. North Dakota courts require specificity — the agency must articulate the actual security risk posed by each withheld record, not merely assert that the subject matter is security-related.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(3)',
        'exemption_number': 'NDCC § 44-04-18.1(3)',
        'short_name': 'Student Educational Records',
        'category': 'privacy',
        'description': 'Educational records of individual students at public educational institutions are exempt from public disclosure under North Dakota law and the federal Family Educational Rights and Privacy Act (FERPA).',
        'scope': 'Educational records directly related to an individual student maintained by a public educational agency or institution — including grades, disciplinary records, enrollment records, and financial aid information. Covers records at K-12 public schools, community colleges, and state universities. The exemption applies to records identifying individual students. Aggregate institutional data (enrollment statistics, graduation rates, demographic summaries without individual identifiers) and institutional administrative records are public. FERPA compliance provides an independent federal basis for withholding even when state law alone might not require it.',
        'key_terms': json.dumps([
            'student record', 'educational record', 'FERPA', 'student privacy',
            'grades', 'disciplinary record', 'enrollment record', 'financial aid',
            'NDCC § 15.1', 'student information', 'academic record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate institutional data (enrollment totals, graduation rates, demographic breakdowns) without individual identifiers are public',
            'Administrative and operational records of educational institutions (budgets, contracts, personnel) are fully public',
            'Challenge whether requested records are actually "student records" or administrative records that happen to reference students',
            'Directory information (name, enrollment status, degree, dates of attendance) may be disclosed unless the student has opted out',
            'Records about employees of educational institutions who are not students are not covered',
        ]),
        'notes': 'North Dakota\'s student records exemption operates in conjunction with federal FERPA requirements. The AG has noted that educational institutions have both state and federal obligations to protect student record privacy. The exemption is student-specific — institutional administrative and financial records are not shielded.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.1(4)',
        'exemption_number': 'NDCC § 44-04-18.1(4)',
        'short_name': 'Tax Return and Revenue Information',
        'category': 'statutory',
        'description': 'State and local tax return information submitted by taxpayers to the Tax Commissioner or local taxing authorities is confidential and exempt from public disclosure.',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individual or business taxpayers to the North Dakota Tax Commissioner or local taxing authorities. Covers income tax, sales tax, and other state tax filings. Aggregate tax revenue statistics, enforcement orders, and final judgments in tax disputes are generally public once filed with courts. The exemption does not protect the Tax Commissioner\'s operational and enforcement records or aggregate revenue data.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Tax Commissioner', 'income tax',
            'sales tax return', 'taxpayer information', 'tax filing', 'tax confidentiality',
            'tax records', 'revenue information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Final court judgments in tax collection cases are public court records',
            'Tax enforcement orders and public sanctions are not covered by this exemption',
            'Challenge whether the specific records requested are actually "tax return information" versus general regulatory or administrative correspondence',
            'Information about the Tax Commissioner\'s own operations and enforcement programs is public',
        ]),
        'notes': 'NDCC § 44-04-18.1(4) reflects the universal confidentiality rule for tax return information. The AG has confirmed that taxpayer-specific return data is categorically exempt, but that the Tax Commissioner\'s operational records and aggregate revenue data are public.',
    },
    {
        'jurisdiction': 'ND',
        'statute_citation': 'NDCC § 44-04-18.10',
        'exemption_number': 'NDCC § 44-04-18.10',
        'short_name': 'Home Address and Telephone — Private Individuals',
        'category': 'privacy',
        'description': 'Home addresses and home telephone numbers of private individuals contained in government records are exempt from public disclosure to protect personal safety and privacy.',
        'scope': 'Home addresses and home telephone numbers of private individuals who have provided that information to a government agency in the course of regulated or permitted activities. The exemption is limited to home contact information — business addresses, business phone numbers, and work addresses are public. For public employees, home addresses and home telephone numbers are also exempt under this provision, while workplace contact information is public. Does not cover the identity, business activities, or regulated activities of the individual — only the home contact details.',
        'key_terms': json.dumps([
            'home address', 'home telephone', 'residential address', 'personal address',
            'private individual', 'home contact information', 'address privacy',
            'telephone number', 'NDCC § 44-04-18.10',
        ]),
        'counter_arguments': json.dumps([
            'Business addresses and business telephone numbers of individuals are public',
            'The exemption covers only the home contact fields — all other information about the individual and their regulated activities is public',
            'For public employees, workplace address and work telephone are public — only the home versions are exempt',
            'Where a private individual uses their home address as a business address, the exemption may not apply',
            'The agency must redact only the home contact fields and release the remainder of the record',
        ]),
        'notes': 'NDCC § 44-04-18.10 is a standalone provision protecting home contact information. It applies broadly — to private individuals in any type of government record. The AG has confirmed that this exemption requires only the home address and phone fields to be redacted, not entire records containing those fields.',
    },
]

# =============================================================================
# RULES
# North Dakota Open Records Law, NDCC § 44-04-18 et seq.
# The statute requires "timely" access but does not specify a number of days.
# AG advisory opinions define "timely" as context-specific but generally within
# a few days to two weeks for most requests. No administrative appeal — district
# court enforcement only. Copy fees set at $0.25/page or actual cost for
# electronic media. Attorney's fees available for prevailing requesters.
# =============================================================================

ND_RULES = [
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'response_timeline',
        'param_value': 'timely',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota\'s Open Records Law requires "timely" access to public records but does not specify a fixed number of days. The term is context-dependent: simple requests for readily available records should be fulfilled immediately or within a few days. Complex requests may take longer, but the AG has issued opinions suggesting that "timely" means within a reasonable period of days, generally not exceeding two weeks for most requests. Agencies may not use the absence of a fixed deadline as license to delay indefinitely. The AG\'s advisory opinions set the practical standard in the absence of statutory specificity.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'statutory_mandate',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'NDCC § 44-04-18 creates a strong presumption that all records of public entities are open for inspection and copying. The burden of demonstrating that a record is exempt falls entirely on the agency — not on the requester to justify why they need the record. Courts apply this presumption actively and review withholding decisions with skepticism. Agencies must identify the specific statutory provision authorizing withholding for each withheld record — general claims that records are "confidential" without citation are insufficient.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota does not require public records requests to be submitted in writing. Oral requests are valid. However, written requests are strongly advisable to document the scope of the request, establish the date of submission, and create a record for potential AG complaint or court enforcement. Many agencies have adopted forms or online portals, but use of these systems is not required.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota agencies may not require requesters to identify themselves or state the purpose of their public records request as a condition of access. The right of access is universal. Agencies may ask for contact information for delivery purposes but cannot condition access on the provision of identity. AG advisory opinions have consistently held that purpose and identity restrictions are impermissible unless specifically authorized by statute.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'When a record contains both exempt and non-exempt information, the agency must release the non-exempt portions after redacting the exempt content. Blanket withholding of entire documents on the basis that they contain some exempt material is not permissible under North Dakota law. The AG has consistently held in advisory opinions that agencies must segregate and release all portions of records that are not independently covered by a specific exemption.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota agencies may charge up to $0.25 per page for paper copies of public records. The fee is intended to cover actual reproduction costs. Agencies may charge actual costs for electronic media (CDs, USB drives) and electronic transmission where those costs are incurred. Agencies may not charge for staff time spent locating, reviewing, or redacting records — those costs are part of the agency\'s public service obligation. Waiving fees is within agency discretion but is not mandated by statute.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota\'s Open Records Law does not mandate fee waivers for any requester category. Agencies may waive fees at their discretion, and many do for journalists, nonprofits, and educational researchers. For electronic records delivered by email, actual reproduction costs are minimal to zero, making fee waivers effectively moot in many cases. Requesters should argue for fee waivers on public interest grounds where applicable.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'North Dakota has NO formal administrative appeal mechanism for public records denials. There is no agency head appeal, no ombudsman, and no administrative review body. A requester who is denied access may seek an advisory opinion from the Attorney General (which is persuasive but not binding) or file directly in district court. The AG opinion process is the practical pre-litigation step in North Dakota — it is informal, free, and relatively fast, but it cannot compel disclosure.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'appeal_deadline',
        'param_key': 'attorney_general_advisory_opinion',
        'param_value': 'available_not_binding',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-21.1',
        'notes': 'A requester who is denied access may request an advisory opinion from the North Dakota Attorney General under NDCC § 44-04-21.1. The opinion is advisory — it does not legally compel the agency to produce records, but it carries significant persuasive weight and agencies routinely comply. The AG opinion process is faster and cheaper than court enforcement and is the standard pre-litigation step in North Dakota. AG opinions interpreting the Open Records Law are published and serve as the primary interpretive authority in the absence of extensive case law.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-21.2',
        'notes': 'A requester denied access to public records may seek enforcement in North Dakota district court under NDCC § 44-04-21.2. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may order the agency to produce records, assess costs, and award attorney fees to a prevailing requester. North Dakota district courts have jurisdiction over open records enforcement actions regardless of the amount in controversy. Cases are typically filed in the county where the agency is located.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_prevailing_requester',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-21.2',
        'notes': 'A court may award reasonable attorney fees and litigation costs to a requester who substantially prevails in a district court enforcement action. Unlike Washington\'s mandatory fee-shifting, attorney fees in North Dakota are discretionary — the court considers the circumstances including whether the agency acted in good faith, the clarity of the law, and the public importance of the records. In practice, courts award fees when agencies withhold records without a reasonable legal basis.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-18',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure under North Dakota\'s Open Records Law is on the agency. The statute creates a strong presumption of openness. An agency claiming an exemption must identify the specific statutory provision authorizing withholding and explain how that provision applies to the specific record. General assertions of confidentiality without statutory citation are insufficient. The AG and courts apply de novo review of withholding claims.',
    },
    {
        'jurisdiction': 'ND',
        'rule_type': 'initial_response',
        'param_key': 'scope_of_coverage',
        'param_value': 'public_entities',
        'day_type': None,
        'statute_citation': 'NDCC § 44-04-17.1',
        'notes': 'North Dakota\'s Open Records Law applies to all "public entities" as defined in NDCC § 44-04-17.1, including state agencies, counties, cities, townships, school districts, and other political subdivisions. The definition is broad — it includes entities created by state law that exercise governmental functions even if they receive private funding. Private entities that are not created by law or do not exercise governmental functions are not covered. Contractors performing governmental functions may be covered to the extent they hold records relating to that function.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

ND_TEMPLATES = [
    {
        'jurisdiction': 'ND',
        'record_type': 'general',
        'template_name': 'General North Dakota Open Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — North Dakota Open Records Law, NDCC § 44-04-18 et seq.

Dear Public Records Custodian:

Pursuant to the North Dakota Open Records Law, NDCC § 44-04-18 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

Please provide records in electronic format (email or download link) where available, which minimizes cost and production time.

I am willing to pay reasonable reproduction fees consistent with NDCC § 44-04-18 (up to $0.25/page for paper copies). I am not willing to pay for staff time spent locating, reviewing, or redacting records — that is a cost the public entity bears as part of its public records obligation. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or make payment arrangements.

Under NDCC § 44-04-18, all records of public entities are presumptively open and the burden of demonstrating that any record is exempt rests on the agency. If any records are withheld in whole or in part, I request that you: (1) identify each withheld record; (2) cite the specific statutory provision (NDCC citation) authorizing withholding; (3) describe the withheld record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all non-exempt, segregable portions of partially withheld records have been released.

Please respond as promptly as possible, consistent with NDCC § 44-04-18's "timely" access requirement.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that reproduction fees be waived for this request. North Dakota\'s Open Records Law does not mandate fee waivers, but I ask that {{agency_name}} exercise its discretion to waive fees because:

1. The requested records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual reproduction cost is zero, making a fee waiver consistent with NDCC § 44-04-18's purpose of providing broad public access to government records.''',
        'expedited_language': '''I request that this records request be processed as promptly as possible. Expedited response is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if there are any clarifying questions that would allow faster production.''',
        'notes': 'General-purpose North Dakota Open Records template. Key ND features: (1) no fixed response deadline — "timely" is the standard, argue for a few days to two weeks for most requests; (2) no administrative appeal — if denied, options are AG advisory opinion (NDCC § 44-04-21.1, persuasive but not binding) or district court (NDCC § 44-04-21.2); (3) $0.25/page for paper copies; (4) attorney fees discretionary for prevailing requester; (5) burden of proof on agency for all exemption claims. Reference "NDCC § 44-04-18," not "FOIA."',
    },
    {
        'jurisdiction': 'ND',
        'record_type': 'government_accountability',
        'template_name': 'North Dakota Open Records Request — Public Employee Misconduct and Disciplinary Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Public Employee Records, NDCC § 44-04-18

Dear Public Records Custodian:

Pursuant to the North Dakota Open Records Law, NDCC § 44-04-18 et seq., I request copies of the following records relating to public employees of {{agency_name}}:

{{description_of_records}}

Specifically, I request:
- Disciplinary records and their outcomes for the employee(s) identified below or in the time period specified
- Records of formal complaints or misconduct allegations and their disposition
- Performance evaluations that resulted in any employment action (termination, demotion, suspension, written warning)
- Records of any settlement agreements relating to employment disputes
- Salary and compensation records for the identified employee(s) or position(s)

Employee/position (if applicable): {{employee_or_position}}
Time period: {{date_range_start}} through {{date_range_end}}

North Dakota law is clear that public employee disciplinary records and compensation are public records. The exemption in NDCC § 44-04-18.1(2) protects only specific personal data fields (Social Security numbers, home addresses, home telephone numbers, and medical information) — it does not shield disciplinary history, performance records, or compensation from disclosure. The North Dakota Attorney General has consistently held in advisory opinions that citizens have a right to know how public servants perform their public duties.

If any records are withheld, please: (1) identify each withheld record; (2) cite the specific NDCC provision authorizing withholding; and (3) confirm that non-exempt portions (including disciplinary outcomes, job titles, salary, and dates of employment) have been released with only the specifically exempt fields (SSN, home address, home telephone, medical info) redacted.

Please respond as promptly as possible per NDCC § 44-04-18.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern public employee conduct — a matter of core government accountability. Electronic delivery involves zero reproduction cost. A fee waiver is consistent with North Dakota\'s presumption of openness under NDCC § 44-04-18.''',
        'expedited_language': '''I request prompt processing of this request. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. Please contact me with any clarifying questions.''',
        'notes': 'North Dakota public employee records template. Key ND features: (1) personnel exemption (NDCC § 44-04-18.1(2)) covers only SSN, home address, home telephone, and medical info — NOT disciplinary records, salary, or job title; (2) AG advisory opinions are the primary interpretive authority and consistently hold that public employee disciplinary history and compensation are public; (3) if denied, seek AG advisory opinion first (NDCC § 44-04-21.1) before district court action; (4) attorney fees available in district court for prevailing requester.',
    },
    {
        'jurisdiction': 'ND',
        'record_type': 'law_enforcement',
        'template_name': 'North Dakota Open Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, NDCC § 44-04-18

Dear Public Records Custodian:

Pursuant to the North Dakota Open Records Law, NDCC § 44-04-18 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Officer disciplinary and complaint records for involved personnel
- Internal investigation records relating to the above

Regarding NDCC § 44-04-18.1(12): the investigative records exemption applies only to active investigations. If any prosecution relating to this incident has concluded or the investigation has been closed, the investigative records exemption does not apply and all records should be produced. Even for active investigations, the agency must: (1) identify the specific enumerated harm (interference with prosecution; revealing informant identity; endangering a person; or revealing non-public investigative technique) that applies to each withheld record; and (2) segregate and release all factual portions of records that do not implicate that specific harm.

Incident reports documenting the existence and nature of the incident, arrest records, and booking information are public under North Dakota law regardless of investigation status.

Please respond as promptly as possible per NDCC § 44-04-18.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern law enforcement actions and public accountability. Electronic delivery costs nothing to reproduce. A fee waiver is consistent with the presumption of openness under NDCC § 44-04-18.''',
        'expedited_language': '''I request prompt processing under NDCC § 44-04-18\'s timely access requirement. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'North Dakota law enforcement records template. Key ND features: (1) NDCC § 44-04-18.1(12) investigative records exemption is time-limited — expires when investigation or prosecution concludes; (2) incident reports and arrest records are public regardless of investigation status; (3) agency must identify specific enumerated harm for each withheld record, not assert blanket investigative privilege; (4) AG advisory opinions are available as a pre-litigation step (NDCC § 44-04-21.1); (5) district court enforcement with discretionary attorney fees under NDCC § 44-04-21.2.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in ND_EXEMPTIONS:
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

    print(f'ND exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in ND_RULES:
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

    print(f'ND rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in ND_TEMPLATES:
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

    print(f'ND templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'ND total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nd', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
