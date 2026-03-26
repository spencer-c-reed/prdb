#!/usr/bin/env python3
"""Build Iowa Open Records Law data: exemptions, rules, and templates.

Covers Iowa's Open Records Law, Iowa Code Ch. 22 (formerly Iowa Code § 22.1
et seq.). Iowa requires agencies to respond "promptly" — in practice 10-20
days. Copy fees are $0.25/page. Iowa's Iowa Public Information Board (IPIB)
provides free, binding decisions, making Iowa one of the few states with an
effective administrative enforcement mechanism. Attorney's fees and civil
penalties are available.

Run: python3 scripts/build/build_ia.py
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
# Iowa Code Ch. 22 creates a broad presumption of public access.
# Iowa Code § 22.7 contains the most important list of confidential records
# — over 70 specific provisions — making Iowa's exemption structure one of
# the most detailed in the country. However, the IPIB has consistently
# interpreted the exemptions narrowly consistent with the public records
# presumption. Iowa Code § 22.2(1) establishes the default: all records
# are public unless a specific provision applies.
# =============================================================================

IA_EXEMPTIONS = [
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(1)',
        'exemption_number': 'Iowa Code § 22.7(1)',
        'short_name': 'Personal Information — Unwarranted Privacy Invasion',
        'category': 'privacy',
        'description': 'Records whose disclosure would constitute an unwarranted invasion of personal privacy are confidential under Iowa Code § 22.7(1), subject to a balancing test that weighs the privacy interest against the public interest in disclosure.',
        'scope': 'Records containing personal information where disclosure would be a "clearly unwarranted invasion of personal privacy." Iowa applies a balancing test: the privacy interest of the individual must be weighed against the public interest in disclosure. Public employees acting in their official capacity have significantly reduced privacy expectations under Iowa law. Personal data about private citizens (home addresses, personal phone numbers, medical information) generally qualifies, but this is not absolute — the public interest can override even private citizen privacy interests in appropriate cases. The IPIB has consistently held that public employees\' official activities are not "personal" for purposes of this exemption.',
        'key_terms': json.dumps([
            'personal privacy', 'unwarranted invasion', 'home address', 'personal information',
            'privacy interest', 'balancing test', 'public vs private', 'private citizen',
            'individual privacy', 'personal data',
        ]),
        'counter_arguments': json.dumps([
            'Iowa requires a balancing test — the public interest in disclosure must be weighed against the privacy interest',
            'Public employees acting in their official capacity have significantly reduced privacy interests',
            'The IPIB has consistently held that the exemption is narrow and does not protect most government operations information',
            'Public employee compensation, job duties, and official conduct are public regardless of this exemption',
            'Challenge the agency\'s characterization of the balance — the IPIB can review and correct misapplied balancing',
            'Information publicly available through other channels cannot be withheld under this exemption',
        ]),
        'notes': 'Iowa Code § 22.7(1) is Iowa\'s primary personal privacy exemption. Unlike some states that have categorical privacy exemptions, Iowa requires a genuine balancing test. The Iowa Public Information Board has developed a substantial body of advisory opinions and decisions defining when the privacy interest prevails. The exemption applies to private citizens more readily than to public employees in their official roles.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(2)',
        'exemption_number': 'Iowa Code § 22.7(2)',
        'short_name': 'Trade Secrets and Proprietary Information',
        'category': 'commercial',
        'description': 'Trade secrets submitted by private entities to government agencies are confidential under Iowa Code § 22.7(2), protecting genuinely proprietary commercial information from disclosure to competitors.',
        'scope': 'Trade secrets and proprietary commercial or financial information submitted by private parties to government agencies. Must qualify as a trade secret under Iowa law: information that (1) derives independent economic value from not being generally known; (2) is subject to reasonable measures to maintain secrecy. Contract prices and amounts paid with public funds are generally not trade secrets and must be disclosed — the IPIB has consistently held that government contract amounts are public. Government-generated records cannot constitute trade secrets. Agencies must independently evaluate trade secret designations.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm',
            'commercial information', 'financial information', 'business confidential',
            'economic value', 'secrecy', 'Iowa trade secret',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds must be disclosed regardless of trade secret claims',
            'The submitter must demonstrate the information meets the legal trade secret definition',
            'Government-generated information cannot constitute a trade secret',
            'Publicly available information cannot be withheld as a trade secret',
            'The IPIB has consistently held that contract pricing is public',
            'Agencies must independently analyze trade secret claims, not defer to vendor designations',
        ]),
        'notes': 'Iowa Code § 22.7(2) trade secret exemption is consistently applied narrowly by the IPIB. The Board has issued numerous opinions confirming that government contract amounts and publicly funded expenditures are not trade secrets. Iowa courts have applied the exemption consistently with the IPIB\'s approach.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(5)',
        'exemption_number': 'Iowa Code § 22.7(5)',
        'short_name': 'Law Enforcement Investigatory Records',
        'category': 'law_enforcement',
        'description': 'Law enforcement investigative records and intelligence information are confidential under § 22.7(5) to protect ongoing investigations, confidential informants, investigative techniques, and the integrity of the criminal justice process.',
        'scope': 'Law enforcement investigatory records where disclosure would: (1) endanger the life of any person; (2) reveal the identity of a confidential informant; (3) reveal investigative techniques; (4) interfere with a pending prosecution; or (5) deprive the defendant of a fair trial. Arrest records, booking records, and records documenting the fact of police contact are generally public. Completed investigations are subject to the standard Ch. 22 analysis — the investigatory exemption does not apply indefinitely. The IPIB has held that agencies must identify specific harm for each withheld record, not claim categorical exemption for all law enforcement files.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'ongoing investigation', 'pending prosecution', 'investigative technique',
            'endanger life', 'criminal intelligence', 'arrest record',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records and booking records are public regardless of this exemption',
            'Once prosecution concludes or the investigation is closed, the exemption does not apply',
            'The IPIB requires agencies to articulate specific harm for each withheld record',
            'Factual portions of investigative records not implicating specific harm must be segregated and released',
            'The IPIB has authority to review and override agency withholding decisions',
            'Iowa\'s IPIB process provides a fast, free mechanism to challenge improper withholding',
        ]),
        'notes': 'Iowa Code § 22.7(5) law enforcement exemption is harm-based. The IPIB has consistently held that it does not apply to completed investigations, closed files, or records documenting general law enforcement activities. Iowa\'s IPIB binding decision authority makes it a particularly powerful enforcement tool for challenging improper law enforcement records withholding.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(6)',
        'exemption_number': 'Iowa Code § 22.7(6)',
        'short_name': 'Personnel Records — Personal Information',
        'category': 'privacy',
        'description': 'Personal and financial information in the personnel files of public employees is confidential, while employment-related information including compensation and job duties remains public under Iowa\'s Open Records Law.',
        'scope': 'Personal data in public employee personnel files — home addresses, personal telephone numbers, Social Security numbers, financial account information, and medical information — is protected. The exemption is field-specific: public employment information including name, position, compensation, department, date of hire, and employment status is public. Disciplinary records for public employees acting in their official capacity are generally public in Iowa under the balancing test of § 22.7(1). The IPIB has consistently held that employment information is public even when employees claim personal privacy under § 22.7(1).',
        'key_terms': json.dumps([
            'personnel record', 'public employee', 'home address', 'personal telephone',
            'Social Security number', 'employee privacy', 'salary', 'job title',
            'disciplinary record', 'employment history',
        ]),
        'counter_arguments': json.dumps([
            'Public employee names, job titles, salaries, and dates of hire are always public',
            'The IPIB has consistently held that employment performance information is public',
            'Disciplinary records for public employees in their official capacity are generally public under the § 22.7(1) balancing test',
            'The exemption is field-specific — challenge blanket withholding of entire personnel files',
            'Challenge the agency\'s balancing analysis through the IPIB process',
        ]),
        'notes': 'Iowa\'s personnel records exemption under § 22.7(6) is field-specific. The IPIB has developed detailed guidance distinguishing personal information (protected) from employment-related information (public). Iowa law is clear that public employee compensation is public. The IPIB provides a fast, free mechanism to challenge overly broad personnel file withholding.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(3)',
        'exemption_number': 'Iowa Code § 22.7(3)',
        'short_name': 'Tax Return Information',
        'category': 'statutory',
        'description': 'State tax returns and related tax return information submitted to the Iowa Department of Revenue are confidential under Iowa Code § 22.7(3) and Iowa Code § 422.20.',
        'scope': 'Individual and business tax returns and tax return information submitted to the Iowa Department of Revenue. Covers income tax, sales tax, and other state tax filings. Iowa Code § 422.20 establishes the specific tax confidentiality rule within the tax code, and § 22.7(3) incorporates it into the Open Records Law framework. Aggregate tax revenue statistics, anonymized data, and information about the Department\'s operations are public. Final court judgments in tax collection cases and public tax liens are public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'income tax',
            'sales tax', 'taxpayer information', 'Iowa Code 422.20', 'tax confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax statistics and anonymized data are public',
            'Tax liens recorded in court records are public',
            'Final court judgments in tax collection cases are public',
            'Information about the Department\'s own operations is public',
            'Property tax assessment records are generally public in Iowa',
        ]),
        'notes': 'Iowa\'s tax return confidentiality under § 22.7(3) and § 422.20 is one of the clearest exemptions in the Iowa Open Records Law. Property tax assessment records, which are publicly filed, are treated differently from income tax returns and are generally public.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(15)',
        'exemption_number': 'Iowa Code § 22.7(15)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between government bodies and their attorneys made in confidence for the purpose of obtaining legal advice are exempt from disclosure under the attorney-client privilege as incorporated in Iowa Code § 22.7(15).',
        'scope': 'Confidential communications between government agencies and their attorneys for the purpose of obtaining legal advice. Covers attorney-client communications and work product prepared in anticipation of litigation. The privilege requires that the communication be for legal (not policy or business) advice, made in confidence, and not waived. Attorney billing records and general retainer terms are generally not privileged. Facts independently known to the agency are not privileged merely because they were communicated to counsel. Iowa courts apply the privilege to government entities narrowly, consistent with the public records presumption.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'in anticipation of litigation', 'privileged communication', 'legal opinion',
            'government attorney', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'Communications must seek legal advice, not business or policy guidance',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when the agency discloses content in public proceedings or to non-attorney staff',
            'Facts independently known to the agency are not privileged',
            'Challenge through the IPIB — the Board reviews privilege claims independently',
            'Final settlements and consent decrees are public',
        ]),
        'notes': 'Iowa Code § 22.7(15) incorporates attorney-client privilege. Iowa courts and the IPIB apply the privilege consistently with general privilege doctrine but narrow it where the public interest in disclosure is strong. The IPIB has authority to review attorney-client privilege claims and can order disclosure if the privilege is misapplied.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(18)',
        'exemption_number': 'Iowa Code § 22.7(18)',
        'short_name': 'Deliberative Process — Pre-Decisional',
        'category': 'deliberative',
        'description': 'Pre-decisional, predecisional deliberative records including preliminary drafts, recommendations, and opinions on policy matters are confidential under Iowa Code § 22.7(18) to protect the integrity of the agency\'s decision-making process.',
        'scope': 'Preliminary drafts, notes, recommendations, and predecisional memoranda that contain opinions on legal or policy matters and have not been adopted as the agency\'s final position. Iowa courts and the IPIB apply this exemption narrowly: factual material embedded in deliberative documents must be segregated and released. "Working law" and standards actually applied by agencies must be disclosed. Once a draft or recommendation is adopted as the agency\'s final position, the exemption no longer applies. The IPIB has consistently required agencies to release factual portions of deliberative documents.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'intra-agency memorandum',
            'recommendation', 'advisory opinion', 'policy deliberation', 'working paper',
            'draft document', 'pre-decisional',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative documents must be segregated and released',
            'Once adopted as the agency\'s final position, the exemption does not apply',
            '"Working law" — standards actually applied by the agency — must be disclosed',
            'The IPIB can review deliberative process claims and order partial release of factual portions',
            'Challenge claims that entire documents are exempt when only recommendation sections qualify',
            'Iowa applies this exemption narrowly consistent with the strong disclosure presumption in § 22.2(1)',
        ]),
        'notes': 'Iowa Code § 22.7(18) deliberative process exemption is narrowly applied by both Iowa courts and the IPIB. The Board consistently requires agencies to segregate factual material and release it. Iowa\'s IPIB process makes it practical to challenge deliberative process withholding without incurring litigation costs.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(11)',
        'exemption_number': 'Iowa Code § 22.7(11)',
        'short_name': 'Security Plans for Critical Infrastructure',
        'category': 'safety',
        'description': 'Specific vulnerability assessments and security plans for critical public infrastructure are confidential under Iowa Code § 22.7(11) where disclosure would create a specific, articulable security risk.',
        'scope': 'Detailed vulnerability assessments, security plans, and related records for critical infrastructure (utility systems, water supply, transportation) and public facilities where disclosure would enable exploitation of a specific security vulnerability. The exemption is narrow — general security policies, budget records, and vendor contracts are public unless specific technical vulnerabilities are implicated. The agency must demonstrate that the specific record reveals an exploitable vulnerability. After vulnerabilities are remediated, the exemption rationale may no longer support withholding.',
        'key_terms': json.dumps([
            'critical infrastructure', 'security plan', 'vulnerability assessment',
            'security risk', 'infrastructure protection', 'public facility',
            'cyber security', 'access control', 'terrorism', 'emergency response',
        ]),
        'counter_arguments': json.dumps([
            'The IPIB can review security plan withholding claims independently',
            'Budget and expenditure records for security programs are public',
            'General policies not revealing specific vulnerabilities are public',
            'Challenge claims that entire security contracts are exempt',
            'After vulnerabilities are patched, the exemption no longer applies to historical findings',
        ]),
        'notes': 'Iowa Code § 22.7(11) security exemption requires a specific, articulable security risk. The IPIB has authority to review security-related withholding claims through its binding decision process, providing a practical check on overbroad security claims.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(4); Iowa Code § 135.42',
        'exemption_number': 'Iowa Code § 22.7(4)',
        'short_name': 'Medical and Health Records',
        'category': 'privacy',
        'description': 'Individually identifiable medical and health records held by state or local public health agencies are confidential under Iowa Code § 22.7(4), consistent with HIPAA and Iowa\'s specific health information confidentiality statutes.',
        'scope': 'Individually identifiable patient health records, treatment records, and related health data held by public health agencies, public hospitals, and governmental mental health facilities. Incorporates HIPAA protections and Iowa-specific health confidentiality statutes (Iowa Code § 135.42 et seq.). Aggregate health statistics, epidemiological data, and facility-level quality reports not identifying individuals are public. Administrative, financial, and regulatory records of public health institutions are public. Health inspection reports for regulated facilities are public.',
        'key_terms': json.dumps([
            'medical record', 'health record', 'patient record', 'HIPAA',
            'protected health information', 'public hospital', 'health department',
            'individually identifiable', 'mental health record', 'treatment record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Administrative and financial records of public health agencies are public',
            'Health inspection reports for regulated facilities are public',
            'The exemption covers individually identifiable patient data, not all health agency operations',
            'Challenge through the IPIB — the Board reviews confidentiality claims independently',
        ]),
        'notes': 'Iowa Code § 22.7(4) medical records exemption is well-established. HIPAA protections and Iowa Code § 135.42 are incorporated. The exemption is limited to individually identifiable patient data. The IPIB provides a free, binding mechanism to challenge overbroad health records withholding.',
    },
    {
        'jurisdiction': 'IA',
        'statute_citation': 'Iowa Code § 22.7(13)',
        'exemption_number': 'Iowa Code § 22.7(13)',
        'short_name': 'Real Estate Appraisal — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related valuation documents prepared by or for a government body in connection with prospective acquisition or sale of property are confidential until the transaction is completed or abandoned.',
        'scope': 'Formal real estate appraisals, feasibility studies, and valuation documents for specific properties that a government body is actively seeking to acquire or sell. The exemption is time-limited: applies only while the acquisition or sale is pending. Once the transaction closes, fails, or is abandoned, records become public. The exemption prevents disclosure of government valuation before purchase negotiations conclude. Post-transaction, all records are fully public. The IPIB has confirmed this time-limited interpretation.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'pre-acquisition', 'real property', 'land purchase', 'property sale',
            'condemnation appraisal', 'eminent domain', 'pending transaction',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction concludes, fails, or is abandoned',
            'Post-transaction appraisal records are fully public',
            'Challenge claims that transactions are "still pending" when no activity has occurred',
            'Appraisals for property already owned by the agency are not covered',
            'The IPIB can review and override improper extension of this exemption to concluded transactions',
        ]),
        'notes': 'Iowa Code § 22.7(13) pre-acquisition appraisal exemption is time-limited and automatically expires on transaction conclusion. The IPIB has confirmed this interpretation. Iowa courts have declined to extend the exemption to post-transaction situations.',
    },
]

# =============================================================================
# RULES
# Iowa Open Records Law, Iowa Code Ch. 22
# Iowa's "promptly" standard means 10-20 days in practice.
# Iowa Public Information Board (IPIB) — free, binding decisions.
# $0.25/page copy fee. Attorney's fees and civil penalties available.
# =============================================================================

IA_RULES = [
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'response_standard',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.8',
        'notes': 'Iowa agencies must respond to public records requests "promptly" under Iowa Code § 22.8. Iowa does not specify a fixed number of days, but in practice "promptly" means 10-20 business days for routine requests. The Iowa Public Information Board (IPIB) has interpreted "promptly" to require timely action commensurate with the complexity and scope of the request. Agencies may not use the "promptly" standard as license to delay — the IPIB has found violations for unreasonable delays even within 20 days for simple requests. Requesters should follow up if they do not hear back within 10 business days.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'iowa_public_information_board',
        'param_value': 'binding_administrative_decisions',
        'day_type': None,
        'statute_citation': 'Iowa Code § 23.1 et seq.',
        'notes': 'Iowa\'s Iowa Public Information Board (IPIB) is one of the most powerful open records enforcement bodies in the United States. The IPIB accepts complaints free of charge, conducts independent review of withholding decisions, and issues BINDING decisions that agencies must follow. IPIB orders are enforceable in district court. The IPIB also issues non-binding advisory opinions on records questions. The IPIB process typically takes 30-60 days — faster than litigation. Filing an IPIB complaint is often the best first step for requesters facing improper denials. The IPIB can award attorney\'s fees and civil penalties in binding proceedings.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'ipib_advisory_opinions',
        'param_value': 'available_persuasive',
        'day_type': None,
        'statute_citation': 'Iowa Code § 23.1 et seq.',
        'notes': 'In addition to binding complaint proceedings, Iowa\'s IPIB issues advisory opinions on open records questions. Advisory opinions are persuasive (not binding on courts) but carry significant weight because the IPIB is the designated state authority on open records law. Requesters and agencies alike may request advisory opinions. A favorable advisory opinion substantially strengthens a requester\'s legal position even before formal proceedings. The IPIB publishes all opinions on its website, creating a body of Iowa-specific open records guidance.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.3(2)',
        'notes': 'Iowa agencies may charge a fee for copies of public records. The standard rate for paper copies is $0.25 per page. Agencies may charge only the actual cost of reproduction — not staff time for locating or reviewing records. For electronic records, the actual cost is typically minimal or zero. Iowa Code § 22.3(2) governs fee standards. The IPIB has found that unreasonably high fees constitute an improper barrier to access and may be challenged through the IPIB complaint process.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.3(2)',
        'notes': 'Iowa agencies may not charge requesters for staff time spent locating, reviewing, or preparing records. Only the actual cost of reproduction is permissible under § 22.3(2). Requesters should challenge invoices that include labor charges, search fees, or legal review costs beyond the per-page reproduction cost. Fee disputes can be raised with the IPIB through the complaint process.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_for_news_media',
        'param_value': 'available_for_news_media',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.3(2)',
        'notes': 'Iowa provides that the news media are entitled to receive copies of records at actual cost, without any additional fee for staff time. Requesters who are members of the news media — journalists, news organizations — may invoke this provision to minimize fees. Other requesters may request fee waivers at agency discretion. The actual cost for electronic records is typically zero, making fee waiver arguments less important for digital document requests.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'appeal_deadline',
        'param_key': 'ipib_complaint_binding_review',
        'param_value': 'ipib_binding_30_60_days',
        'day_type': None,
        'statute_citation': 'Iowa Code § 23.6',
        'notes': 'Iowa\'s IPIB provides a binding administrative appeal mechanism for Open Records Law denials. A requester denied access may file a complaint with the IPIB at no cost. The IPIB investigates the complaint, allows the agency to respond, and issues a binding order if a violation is found. IPIB proceedings typically conclude within 30-60 days. IPIB orders are enforceable in district court. The IPIB process is significantly faster, cheaper, and more accessible than litigation. Requesters should strongly consider filing with the IPIB before or instead of a court action.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.8(1)',
        'notes': 'A requester denied access may bring an action in district court to compel production of records under Iowa Code § 22.8(1). Courts apply de novo review. Courts may award attorney\'s fees and costs to a prevailing requester. There is no requirement to first exhaust the IPIB process before filing in court, but IPIB opinions are influential evidence. Iowa courts have consistently enforced the Open Records Law and have required disclosure in numerous cases where agencies improperly withheld records.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty',
        'param_value': 'up_to_500_per_violation',
        'day_type': None,
        'statute_citation': 'Iowa Code § 23.7',
        'notes': 'The IPIB may impose civil penalties of up to $500 per violation in binding proceedings where an agency is found to have violated the Open Records Law. Civil penalties are in addition to any order compelling disclosure and attorney\'s fee award. The IPIB also has authority to issue formal reprimands. The civil penalty authority provides a meaningful deterrent and makes the IPIB an effective enforcement mechanism without requiring court litigation.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_in_court_and_ipib',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.10(3)(c)',
        'notes': 'Attorney\'s fees and litigation costs are available for a requester who prevails in a district court action under Iowa Code § 22.10(3)(c). The IPIB may also award attorney\'s fees in binding proceedings. Iowa courts have regularly awarded attorney\'s fees in cases where agencies improperly withheld records. The availability of fees in both the IPIB process and court proceedings makes the Iowa enforcement system particularly accessible.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.2(1)',
        'notes': 'Iowa Code § 22.2(1) establishes the baseline presumption: "Every person shall have the right to examine and copy a public record." The burden of demonstrating that a record falls within a confidentiality provision rests on the agency. The IPIB reviews agency withholding decisions de novo — there is no deference to the agency\'s initial determination. Agencies must identify the specific § 22.7 provision that applies to each withheld record. Conclusory or categorical assertions of confidentiality are insufficient.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.2(1)',
        'notes': 'Iowa agencies must release all non-confidential portions of records when only part of a record qualifies for confidentiality under § 22.7. Blanket withholding of records containing some confidential information violates the presumption of access in § 22.2(1). The IPIB has consistently required agencies to segregate confidential portions and release the remainder. The IPIB can order partial release of records after reviewing redacted vs. non-redacted versions in camera.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_format',
        'param_value': 'format_of_requester_choice',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.1(3)(a)',
        'notes': 'Iowa\'s Open Records Law defines "public record" in format-neutral terms, covering records in any format including electronic records. Iowa Code § 22.1(3)(a) defines "government body" broadly to include all agencies and public bodies. Requesters may ask for electronic records in their native format. Agencies may not refuse to provide electronic records merely because the requester could alternatively receive paper copies. The IPIB has held that agencies must provide records in the format in which they are reasonably maintained when the requester requests that format.',
    },
    {
        'jurisdiction': 'IA',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Iowa Code § 22.2(1)',
        'notes': 'Iowa\'s Open Records Law provides that "every person" has the right to examine public records. Agencies may not require requesters to state their purpose for requesting records or to identify themselves as a condition of access. The IPIB has confirmed that anonymous requests are valid. Contact information may be provided voluntarily for delivery purposes but may not be required as a condition of access.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

IA_TEMPLATES = [
    {
        'jurisdiction': 'IA',
        'record_type': 'general',
        'template_name': 'General Iowa Open Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Records Custodian / Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Iowa Open Records Law, Iowa Code Ch. 22

Dear Records Custodian:

Pursuant to Iowa's Open Records Law, Iowa Code § 22.1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or downloadable file) where available, which minimizes both cost and production time.

I am willing to pay fees reflecting the actual cost of reproduction per Iowa Code § 22.3(2), not to exceed $0.25 per page for paper copies. I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Iowa law. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under Iowa Code § 22.2(1), every person has the right to examine and copy public records. The burden of demonstrating that any record is confidential rests on {{agency_name}}. Any claimed confidentiality must be specifically justified under Iowa Code § 22.7 (citing the specific subdivision) — a general "confidential" label is insufficient.

If any records or portions of records are withheld: (1) identify each record withheld; (2) cite the specific § 22.7 subdivision; (3) confirm that all non-confidential, segregable portions have been released.

Please respond promptly as required by Iowa Code § 22.8. If I do not receive a response within 10 business days, I will consider filing a complaint with the Iowa Public Information Board (IPIB).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. If I am requesting records as a member of the news media, Iowa law provides that I receive records at actual cost without additional charges. Regardless, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is zero.

Iowa's Open Records Law reflects a strong public policy of government accountability.''',
        'expedited_language': '''I request expedited processing of this open records request under Iowa Code § 22.8's "promptly" standard. Expedited production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay will {{harm_from_delay}}.

If I do not receive these records promptly, I will consider filing a complaint with the Iowa Public Information Board (IPIB), which has binding authority to order production.''',
        'notes': 'General-purpose Iowa Open Records Law template. Key Iowa features: (1) "promptly" response standard (§ 22.8) — 10-20 business days in practice; (2) IPIB (Iowa Code § 23.1 et seq.) provides FREE, BINDING administrative review — cite as leverage; (3) § 22.7 contains 70+ specific confidentiality provisions — require specific citation; (4) attorney\'s fees available in court and IPIB proceedings; (5) civil penalties up to $500/violation in IPIB proceedings; (6) $0.25/page standard copy fee; (7) news media entitled to records at actual cost; (8) IPIB complaint recommended as first step before litigation. Reference "Iowa Open Records Law" or "Iowa Code § 22," not "FOIA."',
    },
    {
        'jurisdiction': 'IA',
        'record_type': 'law_enforcement',
        'template_name': 'Iowa Open Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Law Enforcement Records, Iowa Code § 22.1 et seq.

Dear Records Custodian:

Pursuant to Iowa's Open Records Law, Iowa Code § 22.1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking records
- Use-of-force reports and documentation
- Officer disciplinary records for concluded proceedings
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Written communications relating to the above
- Internal investigation records for concluded matters

Regarding claimed exemptions under Iowa Code § 22.7(5): Iowa law does not permit categorical withholding of law enforcement records. Any withholding requires: (1) identification of the specific harm enumerated in § 22.7(5) that applies; (2) specific justification for how disclosure of each particular record would cause that harm; and (3) confirmation that all non-exempt, segregable portions have been released.

[If matter appears concluded:] If prosecution has concluded or the investigation is closed, § 22.7(5) does not apply and records should be released.

Under Iowa Code § 22.2(1), the burden of demonstrating confidentiality rests on {{agency_name}}. If this request is not handled promptly, I will consider filing a complaint with the Iowa Public Information Board (IPIB), which has binding authority to order production and impose civil penalties.

I will pay reproduction costs up to ${{fee_limit}} at the statutory $0.25/page rate.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived. These records concern {{public_interest_explanation}}, a core public accountability matter. Electronic delivery incurs zero cost. Iowa's Open Records Law reflects a strong policy of accountability for government law enforcement actions.''',
        'expedited_language': '''I request expedited processing under Iowa Code § 22.8's "promptly" standard. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}. Failure to respond promptly may result in an IPIB complaint.''',
        'notes': 'Iowa law enforcement records template. Key Iowa features: (1) § 22.7(5) investigatory exemption is harm-based — requires specific harm identification for each record; (2) completed investigations are not covered; (3) IPIB binding review available free of charge — cite as leverage in every request; (4) civil penalties up to $500/violation in IPIB proceedings; (5) attorney\'s fees available in court and IPIB; (6) arrest records are public; (7) IPIB has issued numerous opinions that law enforcement agencies must release completed investigation files.',
    },
    {
        'jurisdiction': 'IA',
        'record_type': 'government_contracts',
        'template_name': 'Iowa Open Records Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Government Contracts and Expenditures, Iowa Code § 22.1 et seq.

Dear Records Custodian:

Pursuant to Iowa's Open Records Law, Iowa Code § 22.1 et seq., I request access to the following government contracts and expenditure records:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, amendments, and change orders between {{agency_name}} and {{vendor_or_contractor_name}} from {{date_range_start}} through {{date_range_end}}
- Solicitation documents (RFPs, IFBs, RFQs) and responsive bids or proposals
- Bid tabulation sheets and scoring documents
- Invoices, payment records, and expenditure documentation
- Performance and compliance documentation

Regarding trade secret claims under Iowa Code § 22.7(2): Contract prices and amounts paid with public funds must be disclosed regardless of vendor trade secret claims. The IPIB has consistently held that government contract amounts are not trade secrets. If specific technical materials are claimed as trade secrets, {{agency_name}} must independently evaluate those claims with specific justification — vendor confidentiality designations alone are insufficient.

Under Iowa Code § 22.2(1), the burden of demonstrating confidentiality rests on {{agency_name}}. If this request is not handled promptly, I will consider filing a complaint with the Iowa Public Information Board (IPIB), which has binding authority to order production and impose civil penalties of up to $500 per violation.

I will pay reproduction costs at $0.25/page up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived. These records concern public expenditures, a core accountability matter. Electronic delivery incurs zero cost. Iowa's Open Records Law reflects a strong policy of financial transparency.''',
        'expedited_language': '''I request expedited production under Iowa Code § 22.8's "promptly" standard. Production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}. If not produced promptly, I will consider an IPIB complaint.''',
        'notes': 'Iowa government contracts template. Key Iowa features: (1) contract prices and public expenditures always public per IPIB decisions; (2) IPIB binding review available free of charge — strongest pre-litigation enforcement tool in the US; (3) civil penalties up to $500/violation in IPIB proceedings; (4) attorney\'s fees available in court and IPIB; (5) § 22.7(2) trade secret exemption requires independent agency analysis; (6) "promptly" response standard — 10-20 business days in practice; (7) IPIB advisory opinions on Iowa.gov provide useful precedent for common withholding disputes.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in IA_EXEMPTIONS:
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

    print(f'IA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in IA_RULES:
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

    print(f'IA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in IA_TEMPLATES:
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

    print(f'IA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'IA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ia', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
