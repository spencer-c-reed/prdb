#!/usr/bin/env python3
"""Build Oklahoma Open Records Act data: exemptions, rules, and templates.

Covers Oklahoma's Open Records Act, 51 O.S. § 24A.1 et seq.
Oklahoma requires "prompt, reasonable access." Copy fees are $0.25/page.
There is no administrative appeal mechanism — enforcement is directly in
district court. Attorney's fees are available. Willful violations constitute
a criminal misdemeanor under 51 O.S. § 24A.17. The Act covers records of
any public body regardless of physical form.

Run: python3 scripts/build/build_ok.py
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
# Oklahoma's Open Records Act defines "public body" broadly and creates a
# presumption of access. The Act lists specific exemptions, but they are
# narrowly construed by Oklahoma courts. The criminal misdemeanor provision
# for willful violations (§ 24A.17) is a distinctive enforcement tool.
# Exemptions are set out primarily in § 24A.7 through § 24A.14.
# =============================================================================

OK_EXEMPTIONS = [
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.7(A)(1)',
        'exemption_number': '51 O.S. § 24A.7(A)(1)',
        'short_name': 'Law Enforcement Investigative Records — Ongoing',
        'category': 'law_enforcement',
        'description': 'Records compiled in the course of an ongoing criminal investigation by a law enforcement agency are confidential and not subject to disclosure while the investigation is active, to prevent compromising the investigation.',
        'scope': 'Records compiled in the course of a specific criminal investigation that is still ongoing at the time of the request. The exemption requires that the investigation be genuinely ongoing — a closed or concluded investigation does not receive protection. Arrest records, booking records, incident reports documenting the fact and nature of an incident, and records about completed investigations are generally public. Oklahoma courts have held that the exemption must be invoked for specific records tied to a specific ongoing investigation, not as a blanket protection for all law enforcement files. Once the investigation concludes (by prosecution, declination, or closure), records become public.',
        'key_terms': json.dumps([
            'ongoing investigation', 'criminal investigation', 'law enforcement records',
            'investigative records', 'pending investigation', 'active investigation',
            'confidential investigation', 'criminal intelligence',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records, booking records, and incident reports are public regardless of this exemption',
            'Once an investigation is concluded (by prosecution, declination, or closure), records become public',
            'The agency must demonstrate the investigation is genuinely ongoing — not merely characterize it as such',
            'Oklahoma courts have held that completed investigation files are public and this exemption does not apply retroactively',
            'Factual portions of investigation records not implicating specific harm must be segregated and released',
            'Challenge categorical claims that all law enforcement records are covered — the exemption is investigation-specific',
        ]),
        'notes': 'Oklahoma\'s investigation records exemption is tied specifically to "ongoing" investigations. The Oklahoma Supreme Court has held that once prosecution concludes or the investigation is closed, the exemption no longer applies and records should be disclosed. Arrest records are separately governed and are generally public. The criminal misdemeanor provision in § 24A.17 applies to willful violations — invoking this exemption in bad faith for closed investigations could expose agency officials to criminal liability.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.7(A)(2)',
        'exemption_number': '51 O.S. § 24A.7(A)(2)',
        'short_name': 'Internal Investigative Reports — Pending Disposition',
        'category': 'law_enforcement',
        'description': 'Internal investigation and disciplinary reports regarding law enforcement officers or public employees are exempt from disclosure while the matter is pending final disposition, but become public once the process concludes.',
        'scope': 'Internal affairs investigation files and disciplinary proceedings against law enforcement officers or public employees, but only while the matter is pending final administrative or judicial disposition. Once the disciplinary process concludes — whether by exoneration, discipline, settlement, or court judgment — the records become public. This is a time-limited exemption. Oklahoma courts have held that finalized disciplinary records for public employees are public records subject to disclosure. The exemption protects the process, not the outcome.',
        'key_terms': json.dumps([
            'internal investigation', 'disciplinary record', 'pending disposition',
            'internal affairs', 'officer misconduct', 'employee discipline',
            'administrative proceeding', 'personnel investigation',
        ]),
        'counter_arguments': json.dumps([
            'Once the disciplinary process concludes, records are fully public — challenge claims that matters are "still pending" after final disposition',
            'Oklahoma courts have held that finalized officer disciplinary records are public',
            'The public accountability interest in officer misconduct is particularly strong in Oklahoma courts\' balancing analysis',
            'Challenge blanket invocations of this exemption for records of concluded internal affairs matters',
            'The criminal misdemeanor provision in § 24A.17 applies to willful improper withholding',
        ]),
        'notes': 'Oklahoma\'s internal investigation exemption is explicitly time-limited. The Oklahoma Court of Appeals has confirmed that finalized disciplinary records, including records of officer misconduct findings, are public records once the administrative process concludes. The exemption only protects the integrity of pending proceedings, not finalized outcomes.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.7(B)',
        'exemption_number': '51 O.S. § 24A.7(B)',
        'short_name': 'Victim and Witness Personal Information',
        'category': 'privacy',
        'description': 'The home addresses, telephone numbers, and other personal contact information of crime victims and witnesses contained in law enforcement records are confidential to protect victims from retaliation and witnesses from intimidation.',
        'scope': 'Home addresses, personal telephone numbers, and other personal contact details of crime victims and witnesses in law enforcement records. The exemption is field-specific and narrow — it protects identifying contact information that could enable retaliation or harassment, not all information about victims or witnesses. The name and general identifying information of adult victims in public court proceedings may be public. Aggregate crime statistics and information about crime patterns are public. Oklahoma courts apply this exemption narrowly to the specific data categories. Domestic violence and sexual assault victims have additional protections.',
        'key_terms': json.dumps([
            'crime victim', 'witness', 'victim privacy', 'home address',
            'personal contact information', 'witness intimidation', 'harassment',
            'domestic violence', 'sexual assault victim', 'victim protection',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — names and general incident information are generally public',
            'Aggregate crime statistics and information about incident patterns are public',
            'The exemption covers contact information enabling harassment, not all victim-related information',
            'Challenge claims that entire police reports are exempt because they reference victim contact information',
            'Information already publicly available in court filings cannot be withheld under this exemption',
        ]),
        'notes': 'Oklahoma\'s victim/witness contact information exemption reflects the specific harm of enabling retaliation and intimidation. It is narrowly targeted at contact data rather than all victim-related information. Oklahoma courts have enforced the exemption consistently but have declined to extend it beyond the specific enumerated data categories.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.8',
        'exemption_number': '51 O.S. § 24A.8',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical and mental health treatment records of individual patients held by public health agencies, public hospitals, and government mental health facilities are confidential and exempt from public disclosure.',
        'scope': 'Individually identifiable medical and mental health treatment records held by state or local public health agencies, public hospitals, and mental health facilities. Protects individual patient health data from disclosure. Incorporates applicable HIPAA protections as a matter of state law. Aggregate health statistics, epidemiological data, and facility-level quality reports that do not identify individual patients are public. Administrative, financial, and regulatory records of public health institutions are public. Health inspection reports for regulated facilities are public.',
        'key_terms': json.dumps([
            'medical record', 'mental health record', 'patient record',
            'public hospital', 'health department', 'individually identifiable',
            'HIPAA', 'protected health information', 'treatment record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Administrative and financial records of public health agencies are public',
            'Health inspection and licensing records for regulated facilities are public',
            'The exemption covers individual patient records, not all health agency operations',
            'Challenge claims that personnel medical records for workers compensation are covered — employment context may reduce protection',
        ]),
        'notes': 'Oklahoma\'s medical records exemption under § 24A.8 is well-established. HIPAA protections are also incorporated. The exemption is limited to individually identifiable patient data and does not protect the operations, finances, or regulatory records of public health entities.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.9',
        'exemption_number': '51 O.S. § 24A.9',
        'short_name': 'Personnel Records — Personal Information',
        'category': 'privacy',
        'description': 'Home addresses, telephone numbers, and similar personal contact information in the personnel files of public employees are confidential, while employment-related information including name, job title, and compensation remains public.',
        'scope': 'Specific personal data fields in public employee personnel files — home addresses, personal telephone numbers, Social Security numbers, and medical information — are protected. The exemption is field-specific: public employment information including name, job title, salary, position, department, dates of employment, and professional credentials remains fully public. Disciplinary records and performance evaluations are generally public in Oklahoma once the process concludes. The exemption reflects the distinction between public employees\' professional roles (fully public) and their personal private information (protected).',
        'key_terms': json.dumps([
            'personnel record', 'public employee', 'home address', 'personal telephone',
            'Social Security number', 'employee privacy', 'employment record',
            'salary', 'job title', 'disciplinary record',
        ]),
        'counter_arguments': json.dumps([
            'Public employee names, job titles, salaries, positions, and dates of employment are fully public',
            'The exemption is field-specific — only the enumerated personal data categories are protected',
            'Disciplinary records for concluded proceedings are public under § 24A.7(A)(2)',
            'Challenge blanket withholding of entire personnel files where only specific personal data fields are protected',
            'Use-of-force records and misconduct findings for law enforcement officers have strong public interest',
        ]),
        'notes': 'Oklahoma\'s personnel records exemption in § 24A.9 is field-specific, not a blanket personnel file exemption. The public employment information carve-out is broad — essentially all employment-related information is public. The exemption protects only personal private data that is incidental to the employment relationship.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.10',
        'exemption_number': '51 O.S. § 24A.10',
        'short_name': 'Trade Secrets and Proprietary Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted by private entities to public bodies in connection with contracts, bids, or regulatory proceedings are exempt from disclosure where disclosure would cause competitive harm.',
        'scope': 'Trade secrets and proprietary commercial, financial, or technical information submitted by private entities to government agencies in connection with procurement, regulatory compliance, or licensing. The information must actually qualify as a trade secret — it must derive economic value from secrecy and be subject to reasonable confidentiality measures. Contract prices and amounts paid with public funds are generally public regardless of vendor trade secret claims. Government-generated records cannot constitute trade secrets. The agency must independently evaluate trade secret claims rather than simply accepting vendor designations.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm',
            'commercial information', 'financial information', 'business confidential',
            'economic value', 'secrecy', 'procurement', 'bid information',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds must be disclosed',
            'The submitter must demonstrate competitive harm from disclosure — a label is insufficient',
            'Publicly available information cannot be withheld as a trade secret',
            'Information required by law to be submitted has reduced secrecy expectations',
            'Challenge whether the submitter maintained reasonable secrecy measures',
            'Government-generated analyses and records cannot constitute trade secrets',
            'The agency must independently evaluate trade secret claims',
        ]),
        'notes': 'Oklahoma\'s trade secret exemption under § 24A.10 applies the common trade secret definition. The Oklahoma Supreme Court has held that contract pricing information paid with public funds is public regardless of vendor trade secret claims. Agencies must conduct independent analysis of trade secret designations.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.12',
        'exemption_number': '51 O.S. § 24A.12',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between public bodies and their attorneys made in confidence for the purpose of obtaining legal advice are exempt from public disclosure under the attorney-client privilege as incorporated into the Open Records Act.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice. Covers attorney-client communications and work product prepared in anticipation of litigation. The privilege requires the communication to be for legal (not business or policy) advice, made in confidence, and not waived through disclosure. Attorney billing records, general retainer terms, and non-privileged correspondence are public. Facts independently known to the agency are not privileged merely because they were communicated to counsel.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'in anticipation of litigation', 'privileged communication', 'legal opinion',
            'government attorney', 'confidential communication', 'corporation counsel',
        ]),
        'counter_arguments': json.dumps([
            'The communication must seek legal advice, not business or policy guidance',
            'Attorney billing records and general financial terms are public',
            'Waiver occurs when the agency discloses content in public proceedings or to third parties',
            'Facts independently known to the agency are not privileged',
            'Challenge whether the agency has constructively waived by acting on advice in public proceedings',
            'Final settlements, consent decrees, and court judgments are public',
        ]),
        'notes': 'Oklahoma\'s Open Records Act incorporates attorney-client privilege through § 24A.12. Oklahoma courts apply the privilege to government entities consistently with the general privilege doctrine. The strong public records presumption limits expansive privilege claims. Final legal resolutions including settlement agreements are generally public in Oklahoma.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.7(A)(4)',
        'exemption_number': '51 O.S. § 24A.7(A)(4)',
        'short_name': 'Confidential Informant Identity',
        'category': 'law_enforcement',
        'description': 'The identity of a confidential informant who provided information to a law enforcement agency is exempt from disclosure to protect the informant\'s safety and to preserve the investigative capability of law enforcement.',
        'scope': 'The identity of individuals who have provided confidential information to law enforcement under an expectation of anonymity. This is a narrow, person-specific exemption — it protects only the identity of the informant, not all information in the file. Records that describe an informant\'s information without identifying the person are not covered. The exemption persists even after an investigation concludes because the safety rationale extends beyond the specific investigation. However, if the informant is identified in court proceedings or their identity becomes publicly known through other means, the exemption may no longer apply.',
        'key_terms': json.dumps([
            'confidential informant', 'informant identity', 'snitch', 'cooperating witness',
            'informant protection', 'informant safety', 'CI identity',
            'law enforcement informant',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects only the informant\'s identity — not all information derived from the informant',
            'Records describing what an informant said (without identifying who said it) are not covered',
            'An informant who has been publicly identified in court proceedings cannot claim continued anonymity under this exemption',
            'Challenge claims that an entire file is exempt because it references a confidential informant — segregation is required',
        ]),
        'notes': 'Oklahoma\'s confidential informant exemption is narrowly targeted at the informant\'s identity rather than all informant-related records. The Oklahoma Supreme Court has required segregation — agencies must release non-identifying portions of records that reference informant information. The exemption is persistent (not time-limited) because the safety rationale extends beyond the specific investigation.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.5(6)',
        'exemption_number': '51 O.S. § 24A.5(6)',
        'short_name': 'Critical Infrastructure and Security Plans',
        'category': 'safety',
        'description': 'Records that identify specific vulnerabilities in critical infrastructure and security plans for public facilities are exempt from disclosure where disclosure would create a specific, articulable security risk.',
        'scope': 'Specific vulnerability assessments, security plans, and related records for critical infrastructure (utility systems, water supply, transportation) and public facilities where disclosure would enable exploitation of a specific vulnerability. The exemption is narrow — it requires a specific, articulable nexus between the record and an exploitable security risk. Budget records, general security policies, and vendor contracts are generally public unless specific technical vulnerabilities are implicated. The agency must identify the specific harm that disclosure would cause for each withheld record.',
        'key_terms': json.dumps([
            'critical infrastructure', 'security plan', 'vulnerability assessment',
            'security risk', 'infrastructure protection', 'public facility',
            'cyber security', 'access control', 'emergency response', 'terrorism',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable — general security concerns are insufficient',
            'Budget and expenditure records for security programs are public',
            'General policies and procedures not revealing specific vulnerabilities are public',
            'Challenge claims that entire vendor contracts are exempt when only specific technical details warrant protection',
            'After vulnerabilities are remediated, the exemption no longer applies',
        ]),
        'notes': 'Oklahoma\'s critical infrastructure exemption requires a specific, non-speculative security risk. Agencies must identify how disclosure of the specific record would enable exploitation of a vulnerability. General security concerns do not meet this standard.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.11',
        'exemption_number': '51 O.S. § 24A.11',
        'short_name': 'Student Records',
        'category': 'privacy',
        'description': 'Student education records at public educational institutions are exempt from public disclosure, consistent with FERPA protections. Individually identifiable student information is protected.',
        'scope': 'Education records directly related to individual students at public schools and universities, including transcripts, grades, enrollment data, and disciplinary records. Incorporates FERPA (20 U.S.C. § 1232g) requirements as Oklahoma law. Aggregate educational statistics that do not identify individual students are public. Administrative, financial, and institutional records unrelated to individual students are public. Faculty and staff records are not student records and are subject to the standard Open Records Act analysis.',
        'key_terms': json.dumps([
            'student record', 'education record', 'FERPA', 'student privacy',
            'transcript', 'student disciplinary record', 'enrollment record',
            'personally identifiable student information', 'public school', 'university',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics not identifying individual students are public',
            'Administrative and financial records of educational institutions are public',
            'Faculty and staff records are not student records',
            'Systemic patterns in institutional practices may be public even if individual records are protected',
            'Challenge claims that budget, facilities, and contractual records are FERPA-covered',
        ]),
        'notes': 'Oklahoma\'s student records exemption incorporates FERPA. The exemption is limited to individually identifiable student data, not all records of educational institutions. Oklahoma courts have applied the exemption to protect individual student privacy while requiring disclosure of institutional records.',
    },
    {
        'jurisdiction': 'OK',
        'statute_citation': '51 O.S. § 24A.13',
        'exemption_number': '51 O.S. § 24A.13',
        'short_name': 'Real Estate Appraisal — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related valuation documents prepared by or for a public body in connection with prospective acquisition or sale of real property are exempt until the transaction is completed or abandoned.',
        'scope': 'Formal real estate appraisals, feasibility studies, and valuation documents for specific properties that a public body is actively seeking to acquire or sell. The exemption is time-limited: it applies only while the acquisition or sale is pending. Once the transaction closes, fails, or is abandoned, all appraisal records become public. The exemption exists to prevent agencies from being disadvantaged in negotiations if their valuation is disclosed before purchase. Post-transaction, all records are public. Appraisals for property already owned and not in transaction are not covered.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'feasibility study', 'pre-acquisition', 'real property', 'land purchase',
            'property sale', 'condemnation appraisal', 'eminent domain',
        ]),
        'counter_arguments': json.dumps([
            'The exemption automatically expires when the transaction concludes, fails, or is abandoned',
            'Post-transaction appraisal records are fully public',
            'Challenge claims that transactions are "still pending" when no activity has occurred',
            'Appraisals for property already owned by the agency are not covered',
            'Budget documents discussing general property value range may not qualify as formal appraisals',
        ]),
        'notes': 'Oklahoma\'s pre-acquisition appraisal exemption is time-limited. It expires automatically on conclusion of the transaction. Oklahoma courts have held that agencies may not claim the exemption for appraisals of property already in their inventory.',
    },
]

# =============================================================================
# RULES
# Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq.
# Oklahoma requires "prompt, reasonable access." $0.25/page copy fee.
# No administrative appeal. District court enforcement. Attorney's fees.
# Criminal misdemeanor for willful violations (§ 24A.17).
# =============================================================================

OK_RULES = [
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'response_standard',
        'param_value': 'prompt_reasonable_access',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5',
        'notes': 'Oklahoma\'s Open Records Act requires public bodies to provide "prompt, reasonable access" to records. The statute does not specify a fixed number of days, but Oklahoma courts and the Oklahoma Open Records Act coordinator have interpreted "prompt" to mean within a reasonable time, generally no more than 3-5 business days for routine requests. Complex requests may require more time, but the agency must communicate proactively about timing. The absence of a fixed deadline means requesters should follow up promptly if they do not hear back within a week.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'reasonable_time_for_review',
        'param_value': 'agency_may_take_reasonable_time',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5(2)',
        'notes': 'Oklahoma law allows agencies a "reasonable" amount of time to locate records and determine if any exemptions apply before disclosing. § 24A.5(2) specifically provides that if a request requires a response not immediately available, the agency "shall promptly notify" the requester and establish a specific date and time for production. This notification requirement is important — agencies that fail to notify while also failing to produce are doubly non-compliant. Requesters should press for a specific production date if the agency claims it needs more time.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5(3)',
        'notes': 'Oklahoma public bodies may charge up to $0.25 per page for standard paper copies. The fee must reflect the actual cost of reproduction. Agencies may not charge for staff time spent locating, reviewing, or redacting records — only the actual reproduction cost is permissible. For electronic records, the actual cost is typically minimal. Some Oklahoma agencies charge less than $0.25; the $0.25 is a ceiling, not a floor. Requesters should ask for electronic delivery to minimize or eliminate copy fees.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5(3)',
        'notes': 'Oklahoma agencies may not charge requesters for staff time spent locating, reviewing, or preparing records. Only the actual cost of reproduction is chargeable under § 24A.5(3). Requesters should challenge any invoice that includes search fees, review fees, or labor charges beyond the per-page reproduction cost.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_agency_discretion',
        'param_value': 'agency_discretion_no_statutory_right',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5(3)',
        'notes': 'Oklahoma does not provide a statutory right to fee waiver. Agencies may waive fees at their discretion. Requesters may argue for waivers based on public interest, media status, or nonprofit purpose. For electronic records, the actual reproduction cost is often zero, making fee waiver arguments less important for digital document requests.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.17',
        'notes': 'Oklahoma has NO formal administrative appeal mechanism for Open Records Act denials. There is no agency head appeal and no administrative tribunal with authority to compel disclosure. A requester denied access must bring an action directly in district court. The Oklahoma district attorney may also prosecute willful violations as criminal misdemeanors under § 24A.17. Requesters should document all communications with the agency carefully before bringing a court action.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.17(A)',
        'notes': 'A requester denied access may bring a civil action in district court under § 24A.17(A). The court may order the agency to produce records and may award attorney\'s fees and costs to a prevailing requester. Oklahoma courts review withholding decisions and apply the presumption of access. There is no specific statute of limitations in the Act, but the general limitations period for civil actions applies. Requesters should file promptly after a denial to preserve their claims.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'penalty',
        'param_key': 'criminal_misdemeanor_willful_violation',
        'param_value': 'class_b_misdemeanor',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.17(B)',
        'notes': 'Oklahoma\'s Open Records Act contains a criminal enforcement provision unique among US public records laws: any person who willfully violates the Act is guilty of a misdemeanor and upon conviction can be fined up to $500 or imprisoned up to one year, or both. This criminal provision applies to public officials who willfully deny access to records to which the public is entitled. While prosecutions are rare, the criminal provision provides a powerful deterrent. Requesters whose requests have been willfully denied can report potential violations to the district attorney. The criminal provision also applies to willful destruction of records.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.17(C)',
        'notes': 'A requester who substantially prevails in an Open Records Act civil action may recover reasonable attorney\'s fees and court costs. The fee award is available under § 24A.17(C) and makes litigation economically viable even for modest requests. Oklahoma courts have awarded attorney\'s fees in cases where agencies withheld records without adequate legal justification. The catalyst theory applies — fees may be available where the agency produces records after suit is filed without a formal court judgment.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5',
        'notes': 'Oklahoma law creates a presumption that all records of public bodies are public and available for inspection. Agencies bear the burden of demonstrating that a specific exemption applies to each withheld record. A conclusory invocation of an exemption category without record-specific justification is insufficient. Oklahoma courts apply the presumption of access strictly and have declined to uphold withholding where agencies failed to provide specific exemption justifications.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.5',
        'notes': 'Oklahoma agencies must release all non-exempt portions of records when only part of a record qualifies for an exemption. Agencies must redact the specifically protected information and release the remainder. Blanket withholding of documents containing some exempt content is a violation of the Act. Oklahoma courts have enforced the segregability requirement and have held that agencies must make a good-faith effort to identify and release non-exempt portions.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'broad_definition_public_body',
        'param_value': 'all_entities_exercising_public_function',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.3(2)',
        'notes': 'Oklahoma\'s Act applies to all "public bodies" — a broad definition covering state agencies, local governments, school districts, public trusts, authorities, and any entity exercising governmental functions with public funding. Oklahoma courts have extended the Act\'s coverage to entities that might otherwise appear private when they are performing public functions with public funds. The broad coverage is consistent with Oklahoma\'s stated commitment to government accountability.',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'public_trust_coverage',
        'param_value': 'oklahoma_public_trusts_covered',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.3(2); 60 O.S. § 176 et seq.',
        'notes': 'Oklahoma uses public trusts extensively for economic development, utility, and facilities management purposes. Oklahoma courts have consistently held that public trusts created under 60 O.S. § 176 et seq., particularly those with governmental beneficiaries (municipalities, counties), are "public bodies" subject to the Open Records Act. This is an important jurisdictional point: entities that claim to be private but function as public trusts with governmental beneficiaries are covered. Requesters should investigate the organizational structure of entities denying records as "private."',
    },
    {
        'jurisdiction': 'OK',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_included',
        'param_value': 'yes_format_neutral',
        'day_type': None,
        'statute_citation': '51 O.S. § 24A.3(1)',
        'notes': 'Oklahoma\'s Open Records Act defines "record" broadly to include all documents, papers, books, photographs, maps, films, tapes, recordings, or other documentary materials regardless of physical form. Electronic records including emails, text messages on government devices, databases, and other digital materials are covered. The format-neutral definition prevents agencies from avoiding disclosure by using electronic communications instead of paper. Oklahoma courts have confirmed that emails by public officials in their official capacity are public records.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

OK_TEMPLATES = [
    {
        'jurisdiction': 'OK',
        'record_type': 'general',
        'template_name': 'General Oklahoma Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq.

Dear Records Custodian:

Pursuant to the Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or downloadable file) where available to minimize both cost and production time.

I am willing to pay fees reflecting the actual cost of reproduction per 51 O.S. § 24A.5(3), not to exceed $0.25 per page for paper copies. I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Oklahoma law. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under 51 O.S. § 24A.5, all records of public bodies are presumptively available to the public. The burden of demonstrating that any record is exempt rests on {{agency_name}}. Any exemption must be identified by specific statutory citation. Under § 24A.5(2), if records are not immediately available, please promptly notify me and establish a specific date and time for production.

If any records or portions of records are withheld: (1) identify each record withheld; (2) cite the specific statutory basis (51 O.S. § 24A. section); and (3) confirm that all non-exempt, segregable portions have been released.

Please note that willful denial of access to public records constitutes a criminal misdemeanor under 51 O.S. § 24A.17(B).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Oklahoma law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is zero.

The Oklahoma Open Records Act reflects a strong policy of public accountability.''',
        'expedited_language': '''I request the most expedited processing possible under the "prompt, reasonable access" standard of 51 O.S. § 24A.5. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production.''',
        'notes': 'General-purpose Oklahoma Open Records Act template. Key Oklahoma features: (1) "prompt, reasonable access" standard (§ 24A.5) — generally 3-5 business days in practice; (2) § 24A.5(2) requires notification and specific production date if records not immediately available; (3) no administrative appeal — district court enforcement (§ 24A.17); (4) criminal misdemeanor for WILLFUL violations (§ 24A.17(B)) — include citation to signal seriousness; (5) attorney\'s fees for prevailing requesters (§ 24A.17(C)); (6) $0.25/page maximum copy fee; (7) Oklahoma public trusts (60 O.S. § 176) are covered public bodies. Reference "Oklahoma Open Records Act" or "51 O.S. § 24A," not "FOIA."',
    },
    {
        'jurisdiction': 'OK',
        'record_type': 'law_enforcement',
        'template_name': 'Oklahoma Open Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Law Enforcement Records, 51 O.S. § 24A.1 et seq.

Dear Records Custodian:

Pursuant to the Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking records
- Use-of-force reports and documentation
- Officer disciplinary records for involved personnel (concluded proceedings)
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Written communications related to the above
- Internal investigation records for concluded proceedings

Regarding claimed exemptions:
- § 24A.7(A)(1) (ongoing investigations) applies only to genuinely active investigations — not closed cases. If prosecution has concluded or the investigation is closed, please confirm this and produce records accordingly.
- § 24A.7(A)(2) (internal investigations) is time-limited — it applies only while proceedings are pending, not to finalized disciplinary records.
- Arrest records are separately public regardless of investigation status.

For each record withheld: cite the specific § 24A subsection; confirm the investigation is genuinely ongoing; confirm that all segregable non-exempt portions have been released.

Under 51 O.S. § 24A.17(B), willful denial of access is a criminal misdemeanor. I am willing to pay reproduction costs up to ${{fee_limit}} at $0.25/page.

Please provide prompt, reasonable access per 51 O.S. § 24A.5.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived. These records concern {{public_interest_explanation}}, a core public accountability matter. Electronic delivery incurs zero cost. The Oklahoma Open Records Act's public accountability policy supports a waiver.''',
        'expedited_language': '''I request expedited production under the "prompt, reasonable access" standard of § 24A.5. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Oklahoma law enforcement records template. Key Oklahoma features: (1) § 24A.7(A)(1) ongoing investigation exemption applies only to genuinely active cases — concluded investigations are public; (2) § 24A.7(A)(2) internal investigation exemption is time-limited and expires upon final disposition; (3) arrest records are always public; (4) criminal misdemeanor for willful denial (§ 24A.17(B)) — include citation; (5) no administrative appeal — district court action (§ 24A.17); (6) attorney\'s fees available (§ 24A.17(C)); (7) Oklahoma public trusts coverage extends to entities like public facility authorities with law enforcement functions.',
    },
    {
        'jurisdiction': 'OK',
        'record_type': 'government_contracts',
        'template_name': 'Oklahoma Open Records Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Custodian
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Government Contracts and Expenditures, 51 O.S. § 24A.1 et seq.

Dear Records Custodian:

Pursuant to the Oklahoma Open Records Act, 51 O.S. § 24A.1 et seq., I request access to the following government contracts and expenditure records:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, amendments, and change orders between {{agency_name}} and {{vendor_or_contractor_name}} from {{date_range_start}} through {{date_range_end}}
- Solicitation documents (RFPs, IFBs, RFQs) and responsive bids or proposals
- Bid tabulation sheets and scoring documents
- Invoices, payment records, and expenditure documentation

Regarding trade secret claims under § 24A.10: Contract prices and amounts paid with public funds must be disclosed regardless of trade secret claims. If specific technical materials are claimed as trade secrets, the agency must independently evaluate those claims with specific justification — vendor confidentiality designations alone are insufficient. In all cases, the contract amount and all payments with public funds must be disclosed.

Under 51 O.S. § 24A.5, all records of public bodies are presumptively public. Under § 24A.17(B), willful denial is a criminal misdemeanor. I am willing to pay reproduction costs at $0.25/page up to ${{fee_limit}}.

Please respond promptly per § 24A.5.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived. These records concern public expenditures, a core accountability matter. Electronic delivery incurs zero cost. Oklahoma's Open Records Act reflects a strong public interest in financial transparency.''',
        'expedited_language': '''I request prompt production under § 24A.5's "prompt, reasonable access" standard. Production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Oklahoma government contracts template. Key Oklahoma features: (1) contract prices and public expenditures always public regardless of trade secret claims; (2) criminal misdemeanor for willful denial (§ 24A.17(B)) — cite to signal seriousness; (3) § 24A.10 trade secret exemption requires independent agency analysis of claims; (4) Oklahoma public trusts (60 O.S. § 176) are covered — many economic development entities are public bodies; (5) no administrative appeal — direct district court action; (6) attorney\'s fees available.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in OK_EXEMPTIONS:
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

    print(f'OK exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in OK_RULES:
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

    print(f'OK rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in OK_TEMPLATES:
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

    print(f'OK templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'OK total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ok', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
