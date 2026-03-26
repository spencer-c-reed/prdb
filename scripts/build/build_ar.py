#!/usr/bin/env python3
"""Build Arkansas Freedom of Information Act data: exemptions, rules, and templates.

Covers the Arkansas Freedom of Information Act (AFOIA), Ark. Code § 25-19-101 et seq.
Arkansas has one of the broadest FOIA statutes in the country — the Act requires
agencies to respond "immediately" or within 3 business days. $0.10/page copy fee.
No administrative appeal. Circuit court enforcement. Criminal penalties for willful
noncompliance by public officials. Attorney's fees for prevailing requesters.

Run: python3 scripts/build/build_ar.py
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
# Arkansas FOIA, Ark. Code § 25-19-105, lists specific exempt categories.
# Arkansas courts strictly construe exemptions in favor of disclosure —
# the Act's declaration of policy in § 25-19-102 emphasizes that government
# is "the servant of the people" and that public business must be conducted
# openly. Criminal penalties for willful noncompliance are unique and make
# Arkansas's FOIA enforcement particularly powerful.
# =============================================================================

AR_EXEMPTIONS = [
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(12)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(12)',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Personnel records of individual employees are exempt to the extent that their disclosure would constitute a clearly unwarranted invasion of personal privacy. The exemption requires a genuine balancing of privacy interests against the public\'s right to know — it is not categorical.',
        'scope': 'Personnel files, performance evaluations, medical records, and similar personal information where disclosure would constitute a clearly unwarranted invasion of personal privacy. Arkansas courts apply a balancing test: the employee\'s privacy interest against the public\'s interest in accountability. Names, positions, salaries, job classifications, and official conduct of public employees are consistently treated as public. Home addresses, medical information, and personal financial details carry stronger privacy interests. Disciplinary records of public officials relating to their official duties are subject to public accountability interests — Arkansas courts have held that such records are generally public even if technically in a personnel file. The critical distinction is between records about an employee\'s personal life versus records about their performance of public duties.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation', 'personal privacy',
            'clearly unwarranted invasion', 'disciplinary record', 'employment file',
            'government employee', 'public employee', 'personnel file',
        ]),
        'counter_arguments': json.dumps([
            'Names, titles, salaries, and official duties of public employees are public and cannot be shielded by this exemption',
            'Disciplinary records relating to an employee\'s official conduct are generally public — Arkansas courts apply robust public accountability standards',
            'The "clearly unwarranted invasion" standard requires genuine balancing, not a blanket privacy claim',
            'Challenge overbroad claims that treat entire personnel files as exempt when only specific sensitive data (home address, medical condition) warrants protection',
            'Arkansas courts strictly construe exemptions in favor of disclosure — ambiguities go against withholding',
            'Records about performance of public duties cannot be shielded by a personal privacy claim',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(12) is Arkansas\'s primary personnel record exemption. Arkansas courts apply a robust balancing test and are hostile to broad claims of personnel record privacy. The Arkansas Supreme Court has repeatedly held that the public\'s right to know about how public duties are performed outweighs the privacy interest in personnel records documenting official conduct. See Stilley v. McBride, 332 Ark. 306 (1998).',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(6)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(6)',
        'short_name': 'Law Enforcement — Investigative Records',
        'category': 'law_enforcement',
        'description': 'Investigative records of law enforcement agencies are exempt where disclosure would impair an ongoing investigation, endanger the safety of persons, or reveal confidential informant identities. The exemption does not apply to completed investigations.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) harm an ongoing investigation or prosecution; (2) reveal the identity of a confidential informant; (3) endanger a person\'s life or physical safety; or (4) reveal investigative techniques that would compromise their effectiveness. The exemption applies only during active matters — Arkansas courts have been clear that completed investigations, closed cases, and concluded prosecutions do not retain the investigative records exemption. Basic factual information (that an incident occurred, the nature of the incident, arrests made) is generally public even during an active investigation. Incident reports, arrest records, and booking information are almost always public. Agencies must identify with specificity which harm applies to which record.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement investigation', 'confidential informant',
            'investigative technique', 'ongoing investigation', 'pending prosecution',
            'endanger', 'police records', 'investigation file', 'intelligence records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only to active investigations — completed cases and closed matters are public',
            'Each withheld document must implicate a specific harm from disclosure, not merely be "related to" an investigation',
            'Incident reports, arrest records, and booking information are generally public even during active investigations',
            'Factual information in investigation files that does not reveal informants or techniques must be released',
            'Challenge blanket claims that all records are exempt because an investigation is "ongoing" without specific harm articulation',
            'Arkansas courts strictly construe exemptions against withholding — ambiguities favor disclosure',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(6) covers law enforcement investigative records. Arkansas courts apply strict construction. The exemption is limited to active investigations with specific articulable harms. Once prosecution concludes or investigation closes, records become public. The Arkansas Supreme Court has consistently held that the FOIA must be "liberally construed" with exemptions construed "narrowly." See McCambridge v. City of Little Rock, 298 Ark. 219 (1989).',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(2)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(2)',
        'short_name': 'Records Declared Confidential by Statute',
        'category': 'statutory',
        'description': 'Records specifically required or authorized to be kept confidential by a specific Arkansas statute or federal law are exempt from required disclosure under the AFOIA. The exemption is a passthrough to external statutory provisions.',
        'scope': 'Records specifically designated as confidential by an external Arkansas statute or federal law. The exemption requires a specific statutory provision — general policy preferences or administrative designations are not sufficient. Examples include: tax return information (Ark. Code § 26-18-303), adoption records (Ark. Code § 9-9-217), and child welfare records (Ark. Code § 12-18-109). Arkansas courts require agencies to identify the specific external statute and demonstrate that the specific records requested fall within its scope. The exemption cannot be bootstrapped from a general "sensitive" designation without a specific statutory basis.',
        'key_terms': json.dumps([
            'statutory exemption', 'confidential by statute', 'required by law', 'federal law',
            'specifically exempt', 'tax records', 'adoption records', 'child welfare',
            'statutory confidentiality', 'authorized by statute',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that mandates or authorizes confidentiality',
            'The cited statute must actually apply to the specific records requested, not just the general subject area',
            'Aggregate data and anonymized records are generally public even if individual records are statutorily confidential',
            'Challenge whether the external statute\'s scope actually covers the specific documents requested',
            'Arkansas courts strictly construe exemptions — agencies cannot bootstrap a broad exemption from a narrow statutory confidentiality provision',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(2) is a passthrough exemption that incorporates external Arkansas and federal statutes. Analysis depends on the specific external statute cited. Arkansas courts apply strict construction — agencies must demonstrate that the specific records requested are within the specific statutory exemption claimed.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(7)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(7)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that are subject to the attorney-client privilege or attorney work product doctrine are exempt from required disclosure under the Arkansas FOIA.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege requires: (1) a bona fide attorney-client relationship; (2) confidential communications; (3) made for the purpose of legal advice (not general business or policy guidance). Billing records and retainer agreements are generally not privileged. Facts independently known to the agency are not protected merely because they were communicated to an attorney. Waiver occurs when privileged content is disclosed in public proceedings or to persons not involved in the legal matter. Arkansas courts apply strict construction of exemptions — the privilege must be clearly established for each withheld record.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'attorney work product', 'legal opinion',
            'government attorney', 'outside counsel', 'confidential legal communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not business or policy guidance',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when the agency discloses privileged content in public proceedings',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and mental impressions',
            'Challenge whether communications labeled "legal" were actually policy or business decisions',
            'Arkansas courts strictly construe exemptions — the privilege must be affirmatively established',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(7) incorporates attorney-client privilege and work product doctrine into the AFOIA. Arkansas courts apply strict construction consistent with the FOIA\'s strong disclosure mandate. The privilege must be established with specificity for each withheld record — a general assertion that records involve legal matters is insufficient.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(9)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(9)',
        'short_name': 'Medical, Psychological, and Social Work Records',
        'category': 'privacy',
        'description': 'Medical, psychological, psychiatric, and social work records that would constitute a clearly unwarranted invasion of personal privacy are exempt from required disclosure.',
        'scope': 'Medical and mental health records, psychological and psychiatric evaluations, and social work case files held by state and local government agencies that relate to identified individuals. Covers records held by the Arkansas Department of Health, Department of Human Services, state hospitals, and other government health and social services providers. The exemption applies when disclosure would constitute a "clearly unwarranted invasion of personal privacy" — a balancing test, not a categorical rule. Aggregate health data, anonymized records, and statistical reports are generally public. Administrative and financial records of government health agencies are public. Records about a public official\'s fitness for public duties may be subject to heightened disclosure standards.',
        'key_terms': json.dumps([
            'medical records', 'psychiatric records', 'psychological evaluation', 'social work records',
            'health information', 'patient records', 'mental health records',
            'clearly unwarranted invasion', 'personal health information', 'patient privacy',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized health data are not covered by this exemption',
            'Administrative and financial records of government health agencies are fully public',
            'Records relating to a public official\'s fitness for duty may be disclosable where public accountability interest is high',
            'Challenge overbroad claims where the agency has not identified the specific privacy harm from disclosure',
            'The "clearly unwarranted" standard requires genuine balancing, not automatic withholding of all health records',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(9) protects medical, psychological, and social work records. The "clearly unwarranted invasion" standard requires case-by-case balancing — not a categorical rule. Administrative records of health agencies (budgets, contracts, staffing) are entirely separate from patient records and are fully public.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(10)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(10)',
        'short_name': 'Trade Secrets and Proprietary Business Information',
        'category': 'commercial',
        'description': 'Trade secrets, proprietary business information, and commercially sensitive financial information submitted by private entities to government agencies are exempt where disclosure would cause competitive harm.',
        'scope': 'Commercially sensitive information submitted by private businesses that qualifies as a trade secret under Arkansas law or whose disclosure would cause genuine competitive harm. The exemption does not cover government-generated records, contract amounts paid with public funds, or publicly available information. Agencies must independently evaluate trade secret claims — they may not simply defer to vendor designations. Information submitted under mandatory government requirements carries a reduced expectation of secrecy. Arkansas courts apply strict construction: only information that genuinely meets the trade secret definition qualifies, and any ambiguity is resolved in favor of disclosure.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'competitive harm',
            'business confidential', 'financial information', 'competitive advantage',
            'proprietary data', 'commercial trade secret', 'commercially sensitive',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts paid with public funds are public regardless of trade secret claims',
            'Government-generated records cannot constitute trade secrets',
            'Publicly available information cannot qualify as a trade secret',
            'Information submitted under government mandate carries a reduced expectation of secrecy',
            'Agencies must independently evaluate claims and cannot defer to vendor designations',
            'Arkansas courts strictly construe exemptions — the trade secret claim must be affirmatively established',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(10) protects trade secrets and proprietary business information. Arkansas courts apply strict construction consistent with the FOIA\'s disclosure mandate. Contract amounts, unit prices, and public expenditures are consistently public. Vendor confidentiality designations are not dispositive.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(8)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(8)',
        'short_name': 'Security Plans for Public Buildings and Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and operational security records for public buildings and critical infrastructure are exempt where disclosure would create a specific, articulable security risk.',
        'scope': 'Operational security plans, vulnerability assessments, access control procedures, and similar security documents for public buildings, water systems, energy infrastructure, and other critical facilities. The exemption requires a specific, articulable security risk from disclosure — not a general assertion that the records are security-related. Budget and expenditure records for security programs are generally public. Physical security plans for non-critical facilities with widely known access patterns do not qualify. Arkansas courts require the agency to demonstrate a concrete risk, consistent with the FOIA\'s strict construction of exemptions.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure', 'security risk',
            'access control', 'public building security', 'infrastructure protection',
            'emergency response', 'security procedures', 'operational security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal exploitable vulnerabilities are not covered',
            'Challenge claims that entire contracts are exempt when only specific technical details warrant protection',
            'Arkansas courts strictly construe exemptions — a generic "security" label is not enough',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(8) protects security plans and vulnerability assessments. Arkansas\'s strict construction standard means agencies must specifically articulate the risk from disclosure of each withheld record. Administrative and budget records for security programs remain public.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(13)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(13)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related valuation documents prepared for a government agency in connection with prospective acquisition or sale of property are exempt until the transaction is complete or the agency withdraws.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with prospective government acquisition or sale of real property. The exemption is time-limited — it expires when the transaction closes, is formally abandoned, or the agency discloses the value publicly. The purpose is to prevent negotiating disadvantage. Post-transaction, all appraisal documents become public. Appraisals for property the agency already owns are not covered. Arkansas courts apply strict construction — the exemption is limited to formal appraisal documents prepared specifically for an active acquisition or sale.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation', 'pre-acquisition',
            'condemnation appraisal', 'feasibility study', 'land purchase', 'real property',
            'property negotiation', 'acquisition pending',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge whether a transaction is still "pending" after extended inactivity',
            'Appraisals for property the agency already owns are not covered',
            'After condemnation proceedings conclude, all valuation records are public',
            'Budget estimates and general internal discussions about property values are not formal appraisals',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(13) protects pre-acquisition appraisals. The exemption is strictly time-limited. Arkansas courts apply strict construction — the exemption is limited to formal valuation documents for active acquisitions.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(5)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(5)',
        'short_name': 'Unpublished Telephone Numbers',
        'category': 'privacy',
        'description': 'Unpublished telephone numbers of individuals contained in government records are exempt from required disclosure to protect individual privacy and prevent harassment.',
        'scope': 'Unlisted or unpublished telephone numbers of private individuals that happen to appear in government records — for example, in personnel files, benefit records, or agency contact databases. The exemption is narrow and specific: it covers only telephone numbers that are unpublished (not in public directories or voluntarily disclosed). Published telephone numbers and business telephone numbers are not covered. The exemption protects the specific data point (the unlisted number) but does not extend to entire records containing that information — the rest of the record must be released with the number redacted.',
        'key_terms': json.dumps([
            'unpublished telephone number', 'unlisted telephone number', 'phone number privacy',
            'personal telephone number', 'unlisted number', 'private telephone',
            'contact information', 'telephone privacy',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is specific to unpublished numbers — published and business telephone numbers are not covered',
            'The exemption protects only the specific telephone number data point, not the entire record containing it',
            'Challenge claims that entire documents are withheld because they contain an unpublished telephone number',
            'Business telephone numbers and numbers voluntarily disclosed to the public are not covered',
            'The rest of the record must be released with only the unpublished number redacted',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(5) is a narrow, specific exemption for unpublished telephone numbers. It is data-point specific — it does not justify withholding entire records. Arkansas courts apply strict construction: only actually unpublished numbers qualify. Published or voluntarily disclosed numbers are public.',
    },
    {
        'jurisdiction': 'AR',
        'statute_citation': 'Ark. Code § 25-19-105(b)(14)',
        'exemption_number': 'Ark. Code § 25-19-105(b)(14)',
        'short_name': 'Scholastic Records — Student Privacy',
        'category': 'privacy',
        'description': 'Scholastic records of individual students at public schools, colleges, and universities that would constitute a clearly unwarranted invasion of personal privacy are exempt under the Arkansas FOIA and are also protected by the federal Family Educational Rights and Privacy Act (FERPA).',
        'scope': 'Individual student educational records at Arkansas public schools and state universities — grades, disciplinary records, financial aid records, and similar personally identifiable student information. The exemption applies to individually identifiable student records. Aggregate and anonymized academic data (school performance metrics, graduation rates, anonymized test scores) are public. Records about school or university administration, budgets, and faculty conduct are public. Arkansas FOIA exemption incorporates FERPA requirements, which restrict disclosure of personally identifiable student records without student or parent consent.',
        'key_terms': json.dumps([
            'scholastic records', 'student records', 'student privacy', 'FERPA',
            'educational records', 'grade records', 'disciplinary records', 'academic records',
            'Family Educational Rights and Privacy Act', 'personally identifiable student information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized academic data are not covered by this exemption',
            'School and university administrative records, budgets, and faculty records are fully public',
            'Records about institutional administration (school board actions, policy decisions) are public',
            'Challenge claims that entire school records are exempt when only specific individually identifiable student data warrants protection',
            'Information that students or parents have voluntarily made public loses its FERPA protection',
        ]),
        'notes': 'Ark. Code § 25-19-105(b)(14) protects student scholastic records and incorporates FERPA. Analysis must address both the state FOIA exemption and federal FERPA requirements. Administrative records of educational institutions (budgets, contracts, policies) are entirely separate from student records and are fully public.',
    },
]

# =============================================================================
# RULES
# Arkansas FOIA, Ark. Code § 25-19-101 et seq.
# "Immediately" or within 3 business days — one of the fastest deadlines
# in the country. Criminal penalties for willful violations by public
# officials. Attorney's fees for prevailing requesters. No administrative
# appeal — enforcement via circuit court. $0.10/page copy fee.
# Strict construction of exemptions in favor of disclosure.
# =============================================================================

AR_RULES = [
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'Ark. Code § 25-19-105(a)(3)',
        'notes': 'Arkansas agencies must respond to AFOIA requests "immediately" or within 3 business days. Ark. Code § 25-19-105(a)(3) provides that records must be available for inspection and copying during the agency\'s regular business hours, and for large or complex requests, the agency must make the records available within 3 business days or provide written notice explaining why additional time is needed. The "immediately" language means that for records that are readily available, the agency must produce them on the spot — not schedule a future appointment. The 3-business-day deadline is a maximum, not a standard response time. Delay without written explanation is itself a violation of the AFOIA.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'immediate_inspection_right',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(a)(1)',
        'notes': 'Arkansas FOIA provides a right to immediate inspection of public records during normal business hours. Ark. Code § 25-19-105(a)(1) states that all public records shall be open to inspection and copying by any citizen of the State of Arkansas during regular business hours. The right to inspect in person is immediate — agencies cannot require advance appointments for records that are readily available. The 3-business-day deadline for providing copies or accommodating inspection of records that require retrieval or review does not eliminate the right to immediate inspection of readily available records.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'citizens_only_requirement',
        'param_value': 'arkansas_citizens_or_via_agent',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(a)(1)',
        'notes': 'Arkansas FOIA technically limits the right to inspect records to "citizens of the State of Arkansas." However, this restriction has been interpreted broadly — non-residents may access records through an Arkansas citizen agent, and many agencies do not strictly enforce the citizenship requirement. Non-citizens (including non-resident journalists and researchers) should either identify an Arkansas-based contact person to make the request, or note that they are acting on behalf of or with the assistance of an Arkansas citizen. Federal courts have questioned the constitutionality of state citizenship requirements for public records access.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(c)',
        'notes': 'When an Arkansas agency denies an AFOIA request in whole or in part, the denial must be in writing and must state the specific statutory basis for the denial — citing the specific Ark. Code § 25-19-105(b) subsection that applies. A blanket denial without statutory citation is a AFOIA violation. The written denial is critical for establishing the record for any subsequent circuit court challenge. Partial denials must be accompanied by production of all non-exempt, reasonably segregable portions of withheld records.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(c)',
        'notes': 'When a record contains both exempt and non-exempt information, the Arkansas agency must release all non-exempt, reasonably segregable portions and identify what was redacted and why. Blanket withholding of documents containing some exempt content is an AFOIA violation. Arkansas courts apply strict construction of exemptions — blanket withholding without genuine segregation analysis is improper. The agency must release all portions that do not themselves qualify for an exemption.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'strict_construction_of_exemptions',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-102',
        'notes': 'Arkansas courts strictly construe AFOIA exemptions in favor of disclosure. Ark. Code § 25-19-102 declares the Act\'s policy: that government is the "servant of the people" and that public records must be available so citizens can evaluate government performance. The Arkansas Supreme Court has repeatedly held that the AFOIA must be "liberally construed" and exemptions "narrowly construed." Any ambiguity in whether an exemption applies must be resolved in favor of disclosure. The burden of establishing that an exemption applies rests entirely on the agency. See McCambridge v. City of Little Rock, 298 Ark. 219 (1989).',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(d)',
        'notes': 'Arkansas agencies may charge for copying public records at a fee that does not exceed the actual cost of reproduction. The standard rate under Ark. Code § 25-19-105(d) is $0.10 per page for paper copies — one of the lowest standard rates in the country. For electronic records delivered digitally, the fee should reflect only the actual cost of the digital medium or transmission, which is often effectively zero for email delivery. Agencies may not charge for staff time spent reviewing or redacting records under the standard AFOIA fee framework. Fee schedules must be published.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(d)',
        'notes': 'Arkansas FOIA does not provide a statutory fee waiver right. Agencies may waive fees at their discretion. Given the $0.10/page rate (among the lowest in the country) and electronic delivery options, fees are rarely a significant barrier in Arkansas. Requesters seeking fee waivers can argue that the records serve a significant public interest consistent with the Act\'s declaration of policy in § 25-19-102.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-107',
        'notes': 'Arkansas has NO formal administrative appeal mechanism for AFOIA denials. A requester denied access must seek enforcement directly in circuit court under Ark. Code § 25-19-107. There is no agency head appeal, no ombudsman, and no administrative tribunal. Arkansas is a direct-to-court state for FOIA enforcement.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-107',
        'notes': 'A requester denied access to public records may bring a civil action in the circuit court of the county in which the public records are located or the county in which the agency is located. Ark. Code § 25-19-107 provides the enforcement mechanism. The court may order production of records, award attorney\'s fees, and assess other relief. There is no specific statute of limitations, but requesters should act promptly.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'penalty',
        'param_key': 'criminal_penalty_for_willful_noncompliance',
        'param_value': 'misdemeanor',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-104',
        'notes': 'Arkansas FOIA has a unique criminal enforcement mechanism: Ark. Code § 25-19-104 makes it a misdemeanor for any public official or employee to willfully refuse to provide access to public records that are required to be open. A conviction carries a fine of $25 to $200 and/or up to 30 days in jail. While prosecutions are rare, the criminal penalty is a meaningful deterrent and can be referenced in correspondence with agencies that appear to be willfully withholding records without legal basis. The criminal provision applies only to willful violations — negligent or mistaken denials do not trigger criminal liability.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-107(a)',
        'notes': 'A requester who prevails in an AFOIA enforcement action may recover attorney\'s fees and other litigation costs from the agency under Ark. Code § 25-19-107(a). Attorney\'s fees are available when the court finds that the agency wrongfully denied access. Arkansas courts routinely award fees to prevailing requesters as a matter of FOIA enforcement policy. The availability of attorney\'s fees makes it economically viable to bring enforcement actions even for modest-size records requests.',
    },
    {
        'jurisdiction': 'AR',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Ark. Code § 25-19-105(d)',
        'notes': 'Electronic records are public records subject to the AFOIA. Arkansas agencies must provide electronic records in electronic format upon request. Agencies may not require requesters to accept paper copies of records that exist in electronic form. When records are maintained in electronic format, the copy fee should reflect only the actual cost of digital reproduction or transmission, which is often effectively zero for email delivery. Requesters should specifically request electronic format to minimize both cost and production time.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

AR_TEMPLATES = [
    {
        'jurisdiction': 'AR',
        'record_type': 'general',
        'template_name': 'General Arkansas Freedom of Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Ark. Code § 25-19-101 et seq.

Dear Custodian of Records:

Pursuant to the Arkansas Freedom of Information Act (AFOIA), Ark. Code § 25-19-101 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available to minimize cost and production time.

I am willing to pay fees not to exceed the actual cost of reproduction per Ark. Code § 25-19-105(d). If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under Ark. Code § 25-19-102, Arkansas's FOIA declares that government is the "servant of the people" and that public records shall be available so that citizens may evaluate government performance. Exemptions under Ark. Code § 25-19-105(b) must be narrowly construed in favor of disclosure, and the burden of establishing any exemption rests entirely on the agency.

If any records are withheld in whole or in part, I request a written denial under Ark. Code § 25-19-105(c) that: (1) identifies each record withheld; (2) states the specific statutory subsection (Ark. Code § 25-19-105(b)(___)) for each withholding; and (3) confirms that all non-exempt, reasonably segregable portions of partially withheld records have been released.

Under Ark. Code § 25-19-105(a)(3), please respond immediately or within 3 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the AFOIA does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest consistent with the Act's declaration of policy in Ark. Code § 25-19-102.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, reproduction costs are effectively zero.''',
        'expedited_language': '''I request that this AFOIA request be processed immediately as provided by Ark. Code § 25-19-105(a)(3). Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose AFOIA template. Key Arkansas features: (1) "immediately" or 3-business-day response deadline (Ark. Code § 25-19-105(a)(3)); (2) strict construction of exemptions in favor of disclosure (Ark. Code § 25-19-102); (3) criminal penalty for willful noncompliance — misdemeanor fine and/or jail (Ark. Code § 25-19-104); (4) no administrative appeal — enforcement via circuit court (Ark. Code § 25-19-107); (5) attorney\'s fees for prevailing requesters (Ark. Code § 25-19-107(a)); (6) $0.10/page copy fee — lowest in the country (Ark. Code § 25-19-105(d)); (7) technically limited to Arkansas citizens but broadly interpreted. Reference "AFOIA" or "Ark. Code § 25-19-101 et seq.", not "federal FOIA."',
    },
    {
        'jurisdiction': 'AR',
        'record_type': 'law_enforcement',
        'template_name': 'Arkansas FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records, Ark. Code § 25-19-101 et seq.

Dear Custodian of Records:

Pursuant to the Arkansas Freedom of Information Act (AFOIA), Ark. Code § 25-19-101 et seq., I request copies of the following law enforcement records:

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

Regarding claimed exemptions under Ark. Code § 25-19-105(b)(6): Arkansas courts require strict construction of exemptions. Any withholding under § 25-19-105(b)(6) requires: (1) identification of the specific harm that would result from disclosure of each withheld record; and (2) demonstration that the record is within the specific scope of the exemption. A generic "investigation ongoing" claim is insufficient.

[If applicable:] If no prosecution is pending or any prosecution has concluded, the § 25-19-105(b)(6) exemption does not apply to closed investigation matters.

Note: A public official who willfully refuses to provide access to public records that are required to be open commits a misdemeanor under Ark. Code § 25-19-104.

Under Ark. Code § 25-19-105(a)(3), please respond immediately or within 3 business days.

I am willing to pay fees under Ark. Code § 25-19-105(d), up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs effectively zero reproduction cost. A fee waiver is consistent with the Act's declaration of policy in Ark. Code § 25-19-102.''',
        'expedited_language': '''I request immediate processing of this AFOIA request under Ark. Code § 25-19-105(a)(3). Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Arkansas law enforcement records template. Key features: (1) "immediately" or 3-business-day deadline (Ark. Code § 25-19-105(a)(3)); (2) § 25-19-105(b)(6) exemption requires specific harm articulation for each withheld record — strict construction applies; (3) completed investigation files are generally public; (4) criminal penalty for willful noncompliance — misdemeanor (Ark. Code § 25-19-104) — cite to signal seriousness; (5) no administrative appeal — circuit court enforcement (Ark. Code § 25-19-107); (6) attorney\'s fees for prevailing requesters; (7) $0.10/page copy fee — lowest in the country.',
    },
    {
        'jurisdiction': 'AR',
        'record_type': 'personnel',
        'template_name': 'Arkansas FOIA Request — Public Employee Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Public Employee Records, Ark. Code § 25-19-101 et seq.

Dear Custodian of Records:

Pursuant to the Arkansas Freedom of Information Act (AFOIA), Ark. Code § 25-19-101 et seq., I request copies of the following records relating to public employee(s):

{{description_of_records}}

Relating to employee(s): {{employee_name_or_position}}
Date range: {{date_range_start}} through {{date_range_end}}

This request includes, but is not limited to:
- Employment applications, resumes, and credentials submitted for the position
- Salary, compensation, and benefits records
- Performance evaluations
- Disciplinary records, complaints, and related investigation records
- Termination records, if applicable
- Any correspondence relating to the employee's performance of official duties

Regarding claimed exemptions under Ark. Code § 25-19-105(b)(12): The personnel record exemption requires a "clearly unwarranted invasion of personal privacy" — a high bar that requires genuine balancing. Under Arkansas law, records relating to a government employee's performance of their official duties are generally public. The Arkansas Supreme Court has held that the public's interest in accountability for government performance outweighs personal privacy interests in records documenting official conduct.

Specifically: names, titles, salaries, official duties, and disciplinary findings relating to official conduct are public and cannot be withheld under § 25-19-105(b)(12). Only genuinely personal information unrelated to official duties (home address, personal medical conditions, unrelated personal financial data) may qualify for exemption.

Under Ark. Code § 25-19-105(a)(3), please respond immediately or within 3 business days.

I am willing to pay fees under Ark. Code § 25-19-105(d), up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of government accountability for public employee conduct. Electronic delivery incurs effectively zero reproduction cost. A fee waiver is consistent with the Act's strong disclosure policy under Ark. Code § 25-19-102.''',
        'expedited_language': '''I request immediate processing of this AFOIA request under Ark. Code § 25-19-105(a)(3). Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Arkansas public employee records template. Key features: (1) personnel record exemption under Ark. Code § 25-19-105(b)(12) requires genuine balancing — "clearly unwarranted invasion" standard; (2) Arkansas courts robustly protect the public\'s right to know about official conduct — disciplinary records for public duties are generally public; (3) "immediately" or 3-business-day deadline; (4) criminal penalty for willful noncompliance; (5) strict construction of exemptions — ambiguities favor disclosure; (6) $0.10/page copy fee.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in AR_EXEMPTIONS:
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

    print(f'AR exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in AR_RULES:
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

    print(f'AR rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in AR_TEMPLATES:
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

    print(f'AR templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'AR total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ar', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
