#!/usr/bin/env python3
"""Build Utah GRAMA data: exemptions, rules, and templates.

Covers Utah's Government Records Access and Management Act (GRAMA),
Utah Code § 63G-2-101 et seq. Utah has a unique, highly structured
classification system: records are classified as public, private, protected,
or controlled. 10-business-day response deadline. Free administrative appeal
to the State Records Committee (45 days). $0.25/page. District court
review after Records Committee. Attorney's fees for prevailing requesters.

Run: python3 scripts/build/build_ut.py
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
# Utah GRAMA, Utah Code § 63G-2-301 through § 63G-2-309, classifies records
# into four categories: public (§ 63G-2-301), private (§ 63G-2-302),
# protected (§ 63G-2-305), and controlled (§ 63G-2-304).
# Public records are accessible by anyone. Private and protected records
# are accessible only to persons with a substantial need that outweighs
# the interests protected by the exemption. The classification system is
# more structured than most states — agencies must actively classify records
# and maintain indexes of classified records.
# =============================================================================

UT_EXEMPTIONS = [
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-302',
        'exemption_number': 'Utah Code § 63G-2-302',
        'short_name': 'Private Records — Personal Information',
        'category': 'privacy',
        'description': 'Records containing personal information about individuals — including home addresses, personal phone numbers, Social Security numbers, financial information, and medical information — are classified as "private" under GRAMA. Private records are not accessible to the general public but may be accessed by the subject of the record or persons with a substantial need.',
        'scope': 'Private records include: (1) records containing personal information about an individual that would cause a clearly unwarranted invasion of personal privacy if disclosed; (2) records containing Social Security numbers, financial account numbers, and similar identifying data; (3) home addresses and phone numbers where the individual has not consented to public disclosure; (4) medical, psychological, and psychiatric information about individuals; (5) personnel records of government employees to the extent they contain genuinely personal information. Private classification does not protect names, job titles, official salaries, or performance of official duties of government employees — those are public. Private records may be released if the requester demonstrates a substantial interest that outweighs the protected privacy interest.',
        'key_terms': json.dumps([
            'private records', 'personal information', 'home address', 'Social Security number',
            'financial information', 'medical information', 'personnel records', 'personal privacy',
            'clearly unwarranted invasion', 'private classification', 'GRAMA private',
        ]),
        'counter_arguments': json.dumps([
            'Private classification does not shield names, job titles, official salaries, or the performance of official duties of government employees',
            'A requester may access private records by demonstrating a substantial interest that outweighs the privacy interest (Utah Code § 63G-2-202(1))',
            'The subject of a private record always has the right to access their own records',
            'Challenge overbroad private classification where the agency has classified records that do not contain genuinely personal information',
            'Records that have been publicly disclosed by the agency or are publicly available cannot be reclassified as private',
            'The Records Committee can review the adequacy of a private classification and order release where the requester\'s interest outweighs privacy',
        ]),
        'notes': 'Utah Code § 63G-2-302 defines private records. Utah\'s classification system is more structured than most states — agencies must actively classify records as private, not simply claim privacy on an ad hoc basis. The Records Committee (Utah Code § 63G-2-501) provides a free, fast appeals mechanism to challenge improper private classification. A person denied access to private records may appeal to the Records Committee within 30 days of denial.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305',
        'exemption_number': 'Utah Code § 63G-2-305',
        'short_name': 'Protected Records — Government Interests',
        'category': 'law_enforcement',
        'description': 'Protected records include a broad range of government records that are not in the public interest to disclose — including law enforcement investigative records, attorney-client communications, commercial information, security plans, and other specified categories. Protected records may be accessed only by the subject, with agency consent, or upon a showing of compelling need.',
        'scope': 'Protected records under Utah Code § 63G-2-305 include more than 50 specific categories: (1) law enforcement investigative records where disclosure would impair investigations, reveal informants, or endanger persons; (2) records prepared in anticipation of litigation or as part of attorney work product; (3) records containing commercial information whose disclosure would harm competitive interests; (4) security plans for critical infrastructure; (5) preliminary drafts and predecisional documents; (6) records that if disclosed would jeopardize the life or safety of an individual; and others. Protected classification does not mean permanent withholding — a requester with a compelling need may still obtain protected records after balancing. The Records Committee adjudicates disputes about protected classification.',
        'key_terms': json.dumps([
            'protected records', 'GRAMA protected', 'law enforcement investigation', 'attorney work product',
            'commercial information', 'security plan', 'preliminary draft', 'predecisional',
            'compelling need', 'protected classification', 'Utah Code § 63G-2-305',
        ]),
        'counter_arguments': json.dumps([
            'Protected classification requires articulation of the specific subsection of § 63G-2-305 that applies to each withheld record',
            'A requester with a compelling need that outweighs the protected interest may obtain protected records (Utah Code § 63G-2-202(2))',
            'Challenge overbroad protected classification where the agency has classified entire documents when only specific portions qualify',
            'The Records Committee can review protected classifications — appeals are free and decided within 45 days',
            'Completed law enforcement investigations are generally no longer protected under the investigation subsection',
            'Segregation is required: even protected documents must have non-protected portions released',
        ]),
        'notes': 'Utah Code § 63G-2-305 is GRAMA\'s primary protected records provision. It lists specific categories of protected records. Unlike private records (personal privacy focus), protected records primarily protect government operational and investigative interests. The Records Committee provides a free, structured appeal mechanism. A person denied access to protected records may appeal to the Records Committee within 30 days.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(7)',
        'exemption_number': 'Utah Code § 63G-2-305(7)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records prepared by or for a governmental entity in anticipation of litigation, or records that constitute attorney work product or attorney-client communications, are classified as protected under GRAMA and are not subject to mandatory public disclosure.',
        'scope': 'Attorney work product prepared in anticipation of litigation, attorney-client communications made for the purpose of seeking or providing legal advice, and related privileged communications between government entities and their legal counsel. The privilege tracks common-law standards: (1) the communication must be with an attorney; (2) made in confidence; (3) for the purpose of legal advice (not business or policy guidance). Billing records and general retainer agreements are generally not privileged. Facts independently known are not privileged merely because they were communicated to an attorney. Waiver occurs when privileged content is disclosed in public proceedings or to persons outside the attorney-client relationship.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'attorney work product', 'legal opinion',
            'government attorney', 'outside counsel', 'protected legal communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not general business or policy guidance',
            'Attorney billing records are generally public — privilege covers content, not the existence of the relationship',
            'Waiver occurs through public disclosure or disclosure to persons outside the legal matter',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis',
            'Challenge whether communications labeled "legal" were actually business or policy decisions',
            'Appeal to the Records Committee to review the adequacy of the protected classification',
        ]),
        'notes': 'Utah Code § 63G-2-305(7) classifies attorney work product and attorney-client communications as protected records. The analysis follows standard common-law privilege doctrine. The Records Committee can review whether specific records genuinely qualify for protected classification under this subsection. The privilege must be established with specificity for each withheld record.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(9)',
        'exemption_number': 'Utah Code § 63G-2-305(9)',
        'short_name': 'Trade Secrets and Commercial Information',
        'category': 'commercial',
        'description': 'Records containing trade secrets or commercial or financial information submitted by a private entity to a governmental entity that, if disclosed, would result in unfair competitive injury to the submitter or would impair the government\'s ability to obtain similar information in the future are classified as protected.',
        'scope': 'Commercially sensitive information submitted by private businesses to government agencies that constitutes a trade secret or whose disclosure would cause competitive harm. The protected classification covers information that: (1) is a trade secret under Utah law; (2) is commercial or financial information that, if disclosed, would result in unfair competitive injury; or (3) whose disclosure would impair the government\'s ability to obtain similar information in the future. Contract amounts paid with public funds are generally public regardless of commercial sensitivity claims. Agencies must independently evaluate trade secret claims. The Records Committee can review whether the protected classification was properly applied.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'competitive harm', 'proprietary information',
            'financial information', 'unfair competitive injury', 'protected commercial records',
            'GRAMA trade secret', 'business confidential', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts paid with public funds are generally public regardless of commercial sensitivity claims',
            'Government-generated records cannot constitute trade secrets — only privately submitted information qualifies',
            'Publicly available information cannot qualify for protected classification',
            'Agencies must independently evaluate claims and may not defer to vendor designations',
            'Appeal to the Records Committee to review the adequacy of the protected classification',
            'The "unfair competitive injury" standard requires genuine competitive harm, not mere preference for secrecy',
        ]),
        'notes': 'Utah Code § 63G-2-305(9) protects trade secrets and commercial information. The Records Committee can review whether the protected classification was properly applied. Contract amounts and public expenditures are consistently public. The protected classification requires affirmative justification — agencies cannot simply defer to vendor designations.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(10)',
        'exemption_number': 'Utah Code § 63G-2-305(10)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and memoranda that are not intended to give notice of a final agency action or decision and that are prepared as part of the agency\'s deliberative process are classified as protected under GRAMA.',
        'scope': 'Predecisional, deliberative documents — preliminary drafts, working papers, notes, and recommendations reflecting the agency\'s internal deliberative process that have not been adopted as the agency\'s final position. The protected classification requires that the document: (1) be predecisional — prepared before final agency action; and (2) be deliberative — contain opinion, analysis, or recommendation rather than purely factual material. Factual material embedded within deliberative documents must be segregated and released. Final agency decisions and adopted policies are not protected. Working law — standards the agency actually applies — must be disclosed. The Records Committee can review whether the protected classification was properly applied.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'working paper',
            'intra-agency memorandum', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'protected deliberative',
        ]),
        'counter_arguments': json.dumps([
            'Factual material within deliberative documents must be segregated and released',
            'Once adopted as final agency policy, the document is no longer predecisional and must be disclosed',
            '"Working law" — standards actually applied — must be disclosed even in internal documents',
            'Documents shared outside the agency may lose their predecisional character',
            'Challenge claims that entire documents are deliberative when only specific sections contain opinions',
            'Appeal to the Records Committee to review the adequacy of the protected classification',
        ]),
        'notes': 'Utah Code § 63G-2-305(10) classifies deliberative process documents as protected. GRAMA\'s structured classification system requires agencies to specifically identify which subsection of § 63G-2-305 applies to each withheld record. The Records Committee provides a free, efficient appeal mechanism to challenge improper protected classification.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(1)',
        'exemption_number': 'Utah Code § 63G-2-305(1)',
        'short_name': 'Law Enforcement Investigative Records',
        'category': 'law_enforcement',
        'description': 'Law enforcement investigative records are classified as protected under GRAMA where disclosure would: impair an investigation, reveal the identity of a confidential informant, endanger the safety of persons, or reveal investigative techniques whose effectiveness depends on secrecy.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) interfere with an ongoing investigation or prosecution; (2) reveal the identity of a confidential informant; (3) endanger the life or physical safety of a law enforcement officer, witness, or other person; or (4) reveal investigative techniques that would be compromised by disclosure. The protected classification applies primarily to active matters — completed investigations generally do not retain the same protection. Factual portions of investigation files that do not implicate the enumerated harms must be segregated and released. Basic factual information (that an incident occurred, the nature of the incident) and arrest records are generally public regardless of investigation status.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'ongoing investigation', 'pending prosecution',
            'endanger', 'protected law enforcement', 'GRAMA investigation records',
            'police investigation records',
        ]),
        'counter_arguments': json.dumps([
            'The protected classification applies primarily to active investigations — completed matters are generally public',
            'Each withheld record must implicate a specific enumerated harm, not merely be related to an investigation',
            'Arrest records, booking information, and basic incident reports are generally public',
            'Factual information in investigation files that does not reveal informants or techniques must be released',
            'Appeal to the Records Committee to challenge the scope of the protected classification',
            'The Records Committee can order production of records where the requester\'s need outweighs the protected interest',
        ]),
        'notes': 'Utah Code § 63G-2-305(1) classifies law enforcement investigative records as protected. The Records Committee provides a free, structured appeals mechanism. Protected classification requires specific articulation of which subsection applies to each withheld record. Completed investigation files are generally no longer protected once prosecution concludes.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(8)',
        'exemption_number': 'Utah Code § 63G-2-305(8)',
        'short_name': 'Security Plans for Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and operational security records for critical infrastructure and government facilities are classified as protected under GRAMA where disclosure would create a specific security risk.',
        'scope': 'Operational security plans, vulnerability assessments, access control procedures, and similar security documents for public buildings, water systems, energy infrastructure, and other critical facilities. The protected classification requires a specific, articulable security risk from disclosure. Budget and expenditure records for security programs are generally public. Physical security plans for non-critical facilities with widely known access patterns do not qualify for protected classification. The Records Committee can review the adequacy of the protected classification.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure', 'security risk',
            'access control', 'infrastructure protection', 'emergency response',
            'protected security records', 'GRAMA security', 'operational security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal exploitable vulnerabilities are not covered',
            'Appeal to the Records Committee to challenge the adequacy of the protected classification',
            'Physical security plans for non-critical facilities may not qualify for protected classification',
        ]),
        'notes': 'Utah Code § 63G-2-305(8) classifies security plans and vulnerability assessments as protected. The Records Committee provides a free appeal mechanism to challenge the adequacy of the protected classification. Administrative and budget records for security programs remain public.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-302(1)(b)',
        'exemption_number': 'Utah Code § 63G-2-302(1)(b)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical, psychological, psychiatric, and mental health records about an individual are classified as private under GRAMA. Private records are not accessible to the general public but may be accessed by the subject or persons with a substantial need that outweighs the privacy interest.',
        'scope': 'Medical records, mental health and psychiatric records, psychological evaluations, and related health information about identified individuals held by state and local government agencies. Covers records held by state hospitals, the Department of Health, the Division of Services for People with Disabilities, and other government health providers. Private classification applies to individually identifiable health information. Aggregate health data, anonymized records, and statistical reports are public. Administrative and financial records of government health agencies are public and not private classified. The subject of a private record always has the right to access their own records.',
        'key_terms': json.dumps([
            'medical records', 'mental health records', 'psychiatric records', 'psychological evaluation',
            'health information', 'patient records', 'private medical', 'GRAMA private medical',
            'individual health information', 'patient privacy',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized health data are public — private classification applies to individually identifiable records',
            'Administrative and financial records of government health agencies are public',
            'The subject of a private record has the right to access their own records',
            'A requester with a substantial need that outweighs the privacy interest may obtain private records',
            'Appeal to the Records Committee to demonstrate a substantial need for access',
        ]),
        'notes': 'Utah Code § 63G-2-302(1)(b) classifies individual medical and mental health records as private. The Records Committee provides a free appeal mechanism. A requester can demonstrate substantial need for private medical records when, for example, seeking information about a public official\'s fitness for duty and the public interest in accountability outweighs the privacy interest.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-305(25)',
        'exemption_number': 'Utah Code § 63G-2-305(25)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared for a government entity in connection with prospective acquisition or sale of property are classified as protected until the acquisition is complete or the entity withdraws from the transaction.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with prospective government acquisition or sale of real property. Protected classification expires when the transaction closes or is formally abandoned. Post-transaction, all appraisal documents become public records. Appraisals for property the government already owns are not covered. The Records Committee can review the adequacy of the protected classification and whether a transaction is genuinely still pending.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation', 'pre-acquisition',
            'condemnation appraisal', 'feasibility study', 'land purchase', 'real property',
            'GRAMA pre-acquisition', 'protected appraisal',
        ]),
        'counter_arguments': json.dumps([
            'The protected classification expires when the transaction is complete or abandoned',
            'Challenge whether a transaction is genuinely still "pending" after extended inactivity',
            'Appraisals for property already owned by the government are not covered',
            'After condemnation proceedings conclude, all valuation records are public',
            'Appeal to the Records Committee to challenge the adequacy of the classification',
        ]),
        'notes': 'Utah Code § 63G-2-305(25) classifies pre-acquisition appraisals as protected. The protected classification is time-limited. The Records Committee can review whether the protected classification was properly applied and whether the transaction remains genuinely active.',
    },
    {
        'jurisdiction': 'UT',
        'statute_citation': 'Utah Code § 63G-2-304',
        'exemption_number': 'Utah Code § 63G-2-304',
        'short_name': 'Controlled Records — Heightened Restriction',
        'category': 'statutory',
        'description': 'Controlled records are a special, restricted classification under GRAMA — more restrictive than private or protected. Controlled classification applies to records that contain highly sensitive information whose disclosure could endanger persons, compromise national security, or violate specific federal requirements.',
        'scope': 'Controlled records under Utah Code § 63G-2-304 include: records that contain information whose disclosure is prohibited by federal statute; records containing information whose disclosure would constitute an unreasonable risk of harm to persons; and records involving highly sensitive intelligence or security matters. Controlled classification is more restrictive than private or protected — access is limited to specific categories of authorized persons defined by statute or agency rule. The classification is uncommon in state government contexts but applies to specific law enforcement intelligence, certain child welfare records, and records subject to federal access restrictions.',
        'key_terms': json.dumps([
            'controlled records', 'GRAMA controlled', 'highly restricted', 'federal prohibition',
            'risk of harm', 'intelligence records', 'security records', 'controlled classification',
            'most restricted GRAMA category', 'access restricted',
        ]),
        'counter_arguments': json.dumps([
            'Controlled classification is narrowly limited to the specific circumstances listed in § 63G-2-304 — it cannot be applied broadly',
            'Challenge claims that routine government records qualify for controlled classification',
            'Controlled classification must be supported by a specific federal statutory prohibition or documented risk of harm',
            'Appeal to the Records Committee to review the adequacy of the controlled classification',
            'Even controlled records may be accessible to specific authorized persons with appropriate need',
        ]),
        'notes': 'Utah Code § 63G-2-304 defines the most restrictive GRAMA record classification — controlled. Controlled classification is uncommon in most state agency contexts. The Records Committee can review controlled classification decisions. Agencies cannot simply designate records as controlled to achieve more protection than private or protected classification would provide.',
    },
]

# =============================================================================
# RULES
# Utah GRAMA, Utah Code § 63G-2-101 et seq.
# 10-business-day response deadline. Free administrative appeal to the
# State Records Committee (decided within 45 days). $0.25/page. District
# court review after Records Committee. Attorney's fees. Strong classification
# system (public/private/protected/controlled). Agencies must maintain
# indexes of classified records.
# =============================================================================

UT_RULES = [
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'Utah Code § 63G-2-204(3)',
        'notes': 'Utah agencies must respond to a GRAMA request within 10 business days of receiving it. This is longer than most states\' response deadlines. The agency must either: (1) provide the requested records; (2) deny the request with a specific legal basis; or (3) notify the requester that additional time is needed and state the reason and a new production date. For very large or complex requests, the agency may extend the deadline an additional 10 business days with written notice. Failure to respond within the deadline is treated as a denial and triggers the requester\'s right to appeal to the Records Committee. The 10-business-day clock begins on receipt of a written request.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'record_classification_system',
        'param_value': 'public_private_protected_controlled',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-301 through § 63G-2-304',
        'notes': 'Utah GRAMA uses a four-tier classification system: (1) Public (§ 63G-2-301) — accessible to any person; (2) Private (§ 63G-2-302) — contains personal information, accessible to the subject or persons with substantial need; (3) Protected (§ 63G-2-305) — contains government operational or investigative information, accessible to the subject or with compelling need; (4) Controlled (§ 63G-2-304) — most restricted, only specified authorized persons. Agencies must actively classify records and maintain indexes of classified records. A requester denied access may challenge the adequacy of any classification before the State Records Committee.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_classification_citation',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-205',
        'notes': 'When a Utah agency denies a GRAMA request in whole or in part, the denial must be in writing and must: (1) identify the records withheld; (2) state the classification category (private, protected, or controlled) for each withheld record; (3) cite the specific statutory subsection justifying the classification; and (4) notify the requester of the right to appeal to the State Records Committee. A denial without the specific GRAMA classification subsection is procedurally deficient. The written denial is critical for establishing the record for Records Committee appeal.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-308',
        'notes': 'Utah agencies must release all non-classified portions of records when only part of a record qualifies for private, protected, or controlled classification. Utah Code § 63G-2-308 requires agencies to provide access to the portions of records that are not classified. Blanket withholding of documents where only specific fields or sections qualify for classification is improper. The agency must redact only the specifically classified portions and release the remainder.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'record_index_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-503',
        'notes': 'Utah agencies are required to maintain and make available a subject matter index of the records they hold, including identification of records that are classified as private, protected, or controlled. Utah Code § 63G-2-503 requires agencies to maintain record retention schedules and indexes. The index itself is a public record accessible to anyone. Requesters can use the index to identify the types of records held by an agency and to frame more targeted GRAMA requests.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-203',
        'notes': 'Utah agencies may charge fees for GRAMA requests based on the actual cost of providing records. The standard rate for paper copies is $0.25 per page under Utah Code § 63G-2-203. For electronic records, fees should reflect the actual cost of producing the electronic copy, which may be minimal or zero for email delivery. Agencies may also charge for the time of the lowest-paid employee capable of performing record retrieval and review tasks, subject to the fee schedule adopted by the State Records Committee. Fee schedules must be published by the agency.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion_with_news_media_preference',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-203(4)',
        'notes': 'Utah Code § 63G-2-203(4) provides that agencies shall reduce or waive fees for news media and nonprofit organizations if the fee reduction would be in the public interest. Unlike most states where fee waivers are entirely discretionary, Utah\'s GRAMA provides a standard for fee reduction that is more than mere discretion — agencies should reduce fees when the public interest standard is met. Requesters who are news media or nonprofit organizations should specifically invoke § 63G-2-203(4) and explain the public interest basis for their request.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'appeal_deadline',
        'param_key': 'records_committee_appeal',
        'param_value': 'free_appeal_within_30_days',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-401; § 63G-2-501',
        'notes': 'Utah has a unique free administrative appeal mechanism — the State Records Committee. Under Utah Code § 63G-2-401, a requester denied access to records (or whose request is unreasonably delayed) may appeal to the State Records Committee within 30 days of the denial. The Records Committee is an independent five-member body that: (1) schedules a hearing within 45 days; (2) hears from both the requester and the agency; (3) may conduct in camera review of withheld records; and (4) issues a written decision. The Records Committee appeal is free — no filing fee. This is one of the best administrative appeal mechanisms in the country for public records requesters.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'appeal_deadline',
        'param_key': 'records_committee_decision_deadline',
        'param_value': '45',
        'day_type': 'calendar',
        'statute_citation': 'Utah Code § 63G-2-502',
        'notes': 'The State Records Committee must schedule a hearing and issue a decision within 45 days of receiving an appeal. This is a firm statutory deadline that makes Utah\'s administrative appeal one of the fastest in the country. The Records Committee\'s decision is binding on the agency unless appealed to district court. A requester who prevails before the Records Committee is entitled to have their request fulfilled promptly. The 45-day deadline begins when the Records Committee receives the appeal.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_review',
        'param_value': 'available_after_records_committee',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-404',
        'notes': 'After the State Records Committee issues its decision, either party (the requester or the agency) may seek review in the district court. Utah Code § 63G-2-404 provides for district court review of Records Committee decisions. The court reviews the Records Committee decision de novo for questions of law and may conduct in camera review. Either party may bypass the Records Committee and go directly to district court, but the Records Committee appeals is free and faster. The district court may order production of records, award attorney\'s fees, and impose other relief.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-405',
        'notes': 'A requester who prevails in a GRAMA enforcement action may recover attorney\'s fees from the agency under Utah Code § 63G-2-405. Attorney\'s fees are available when the court finds that the agency\'s denial was without reasonable basis or the agency acted in bad faith. The availability of attorney\'s fees, combined with the free Records Committee appeal mechanism, makes GRAMA enforcement accessible to individual requesters.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'substantial_need_access_to_private_records',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-202(1)',
        'notes': 'Under Utah Code § 63G-2-202(1), a person may access private or protected records if they can demonstrate a substantial interest in the records that outweighs the interests protected by the classification. This is a key GRAMA mechanism for obtaining otherwise restricted records: the requester presents a substantial need argument to the agency, and if denied, may appeal to the Records Committee. Journalists investigating matters of public concern, researchers with clear academic need, and others with strong public interest arguments can often obtain private or protected records through this mechanism.',
    },
    {
        'jurisdiction': 'UT',
        'rule_type': 'initial_response',
        'param_key': 'government_presumptive_openness',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Utah Code § 63G-2-201',
        'notes': 'Utah Code § 63G-2-201 establishes that all records not classified as private, protected, or controlled are public records accessible to any person. The default classification for government records in Utah is "public" — records without a specific classification are public. Agencies bear the burden of establishing that a specific classification applies. GRAMA is premised on the presumption of public access: records are public unless specifically classified otherwise. This presumption is the foundation for the entire GRAMA framework.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

UT_TEMPLATES = [
    {
        'jurisdiction': 'UT',
        'record_type': 'general',
        'template_name': 'General Utah GRAMA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Records Officer
{{agency_name}}
{{agency_address}}

Re: Government Records Access and Management Act (GRAMA) Request — Utah Code § 63G-2-101 et seq.

Dear Records Officer:

Pursuant to Utah's Government Records Access and Management Act (GRAMA), Utah Code § 63G-2-101 et seq., I hereby request access to and copies of the following records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available to minimize cost and production time.

I am willing to pay reasonable fees under Utah Code § 63G-2-203. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under Utah Code § 63G-2-201, all records that are not classified as private, protected, or controlled are public records accessible to any person. The default classification is public. The agency bears the burden of establishing that any record qualifies for a non-public classification.

If any records are withheld in whole or in part, I request a written denial under Utah Code § 63G-2-205 that: (1) identifies each record withheld; (2) states the specific GRAMA classification (private, protected, or controlled) and the specific statutory subsection; and (3) notifies me of my right to appeal to the State Records Committee under Utah Code § 63G-2-401.

Under Utah Code § 63G-2-204(3), please respond within 10 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived or reduced for this request under Utah Code § 63G-2-203(4). These records relate to {{public_interest_explanation}}, a matter of significant public interest that supports a fee reduction.

I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

Under Utah Code § 63G-2-203(4), agencies shall reduce or waive fees for news media and nonprofit organizations when a fee reduction is in the public interest. I ask that {{agency_name}} apply this standard to my request.

If records are delivered electronically, reproduction costs are minimal or zero, making a fee waiver practical as well as appropriate.''',
        'expedited_language': '''I request that this GRAMA request be processed as expeditiously as possible. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose Utah GRAMA template. Key Utah features: (1) 10-business-day response deadline (Utah Code § 63G-2-204(3)); (2) four-tier classification system: public/private/protected/controlled; (3) free State Records Committee appeal within 30 days of denial, decided within 45 days (Utah Code § 63G-2-401, § 63G-2-502); (4) district court review after Records Committee (Utah Code § 63G-2-404); (5) attorney\'s fees for prevailing requesters (Utah Code § 63G-2-405); (6) $0.25/page copy fee; (7) fee waiver standard for news media and nonprofits (Utah Code § 63G-2-203(4)); (8) substantial need standard for private/protected records (Utah Code § 63G-2-202(1)). Reference "GRAMA" or "Utah Code § 63G-2-101 et seq.", not "FOIA."',
    },
    {
        'jurisdiction': 'UT',
        'record_type': 'law_enforcement',
        'template_name': 'Utah GRAMA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Officer
{{agency_name}}
{{agency_address}}

Re: GRAMA Request — Law Enforcement Records, Utah Code § 63G-2-101 et seq.

Dear Records Officer:

Pursuant to Utah's Government Records Access and Management Act (GRAMA), Utah Code § 63G-2-101 et seq., I request copies of the following law enforcement records:

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

Regarding protected classification under Utah Code § 63G-2-305(1): GRAMA does not permit blanket protection of all law enforcement records. Any protected classification under § 63G-2-305(1) requires: (1) identification of the specific subsection that applies; and (2) articulation of how disclosure of each specifically withheld record would cause the stated harm. A generic "investigation ongoing" claim is insufficient.

[If applicable:] If no prosecution is pending or any related prosecution has concluded, the § 63G-2-305(1) protection does not apply to closed investigation matters.

Under Utah Code § 63G-2-201, records that do not qualify for private, protected, or controlled classification are public by default.

Under Utah Code § 63G-2-204(3), please respond within 10 business days.

If denied, I intend to appeal to the State Records Committee under Utah Code § 63G-2-401.

I am willing to pay fees under Utah Code § 63G-2-203, up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived or reduced under Utah Code § 63G-2-203(4). These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs minimal reproduction cost. A fee reduction is in the public interest.''',
        'expedited_language': '''I request expedited processing of this GRAMA request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Utah GRAMA law enforcement records template. Key features: (1) 10-business-day response deadline (Utah Code § 63G-2-204(3)); (2) § 63G-2-305(1) protected classification requires specific harm articulation for each withheld record; (3) completed investigation files are generally public; (4) free Records Committee appeal within 30 days, decided in 45 days (Utah Code § 63G-2-401, § 63G-2-502) — mention this as a signaling tool; (5) attorney\'s fees for prevailing requesters (Utah Code § 63G-2-405); (6) substantial need access to protected records available (Utah Code § 63G-2-202(2)).',
    },
    {
        'jurisdiction': 'UT',
        'record_type': 'personnel',
        'template_name': 'Utah GRAMA Request — Public Employee Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Officer
{{agency_name}}
{{agency_address}}

Re: GRAMA Request — Public Employee Records, Utah Code § 63G-2-101 et seq.

Dear Records Officer:

Pursuant to Utah's Government Records Access and Management Act (GRAMA), Utah Code § 63G-2-101 et seq., I request copies of the following records relating to public employee(s):

{{description_of_records}}

Relating to employee(s): {{employee_name_or_position}}
Date range: {{date_range_start}} through {{date_range_end}}

This request includes, but is not limited to:
- Employment applications and credentials
- Salary, compensation, and benefits records
- Performance evaluations
- Disciplinary records, complaints, and related investigations
- Separation records, if applicable
- Any records relating to the employee's performance of official duties

Regarding private classification under Utah Code § 63G-2-302: GRAMA's private classification does not shield records relating to an employee's performance of their official government duties. Under Utah Code § 63G-2-301, names, job titles, official salaries, and records relating to the exercise of official duties are specifically classified as public. Only genuinely personal information unrelated to official duties (home address, personal medical conditions, personal financial data) may qualify for private classification.

If any records are classified as private, I note that I have a substantial interest in records relating to {{requester_interest_explanation}} that I believe outweighs the privacy interest. I am prepared to present this argument before the State Records Committee under Utah Code § 63G-2-401 if necessary.

Under Utah Code § 63G-2-204(3), please respond within 10 business days.

I am willing to pay fees under Utah Code § 63G-2-203, up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived or reduced under Utah Code § 63G-2-203(4). These records concern {{public_interest_explanation}}, a matter of government accountability for public employee conduct. Electronic delivery incurs minimal reproduction cost.''',
        'expedited_language': '''I request expedited processing of this GRAMA request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Utah GRAMA public employee records template. Key features: (1) names, job titles, official salaries, and records relating to official duties are specifically classified PUBLIC under Utah Code § 63G-2-301 — agencies cannot classify these as private; (2) private classification under § 63G-2-302 is limited to genuinely personal information; (3) substantial need argument available for private records (Utah Code § 63G-2-202(1)); (4) free Records Committee appeal within 30 days; (5) 10-business-day response deadline; (6) attorney\'s fees for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in UT_EXEMPTIONS:
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

    print(f'UT exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in UT_RULES:
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

    print(f'UT rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in UT_TEMPLATES:
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

    print(f'UT templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'UT total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ut', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
