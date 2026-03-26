#!/usr/bin/env python3
"""Build Ohio Public Records Act data: exemptions, rules, and templates.

Covers Ohio's Public Records Act, ORC § 149.43.
Ohio has one of the stronger public records laws in the country — the statute
broadly defines "public record," places the burden of proving an exemption on
the agency, and provides for statutory damages of $100/day (up to $1,000) plus
mandatory attorney fees. Enforcement is via mandamus in the Court of Claims
or common pleas court. No administrative appeal process exists.

Run: python3 scripts/build/build_oh.py
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
# Ohio Public Records Act, ORC § 149.43
# Ohio law defines "public record" broadly and lists specific statutory
# exceptions. Exemptions are strictly construed against the agency — courts
# apply a presumption of openness and require agencies to meet their burden
# on each claimed exception. ORC § 149.43(A)(1) lists the general categories
# of exempted records, but each category has narrow scope under case law.
# =============================================================================

OH_EXEMPTIONS = [
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(h)',
        'exemption_number': 'ORC § 149.43(A)(1)(h)',
        'short_name': 'Confidential Law Enforcement Investigatory Records',
        'category': 'law_enforcement',
        'description': 'Confidential law enforcement investigatory records (CLEIRs) are exempt where disclosure would create a high probability of disclosing the identity of a confidential source, specific confidential investigatory techniques, information that would endanger the life or safety of law enforcement personnel, or information that would prejudice or impair ongoing criminal prosecution.',
        'scope': 'CLEIRs are narrowly defined under Ohio law. The exemption requires a specific, articulable harm — a generic claim that records are "investigatory" is not sufficient. Closed investigation files generally lose CLEIR status once prosecution concludes. Arrest records, incident reports, booking information, and dispatch logs are typically public even when an investigation is ongoing. Ohio courts apply a case-by-case analysis of whether each specific record meets the CLEIR definition. Under State ex rel. Steckman v. Jackson, 70 Ohio St.3d 420 (1994), the exemption is strictly construed.',
        'key_terms': json.dumps([
            'CLEIR', 'confidential law enforcement investigatory record',
            'ongoing investigation', 'confidential informant', 'investigative technique',
            'ORC 149.43(A)(1)(h)', 'law enforcement exemption', 'prejudice prosecution',
            'endanger safety', 'criminal investigation',
        ]),
        'counter_arguments': json.dumps([
            'The CLEIR exemption is strictly construed — each record must independently satisfy the specific harm test, not just be labeled "investigatory"',
            'Closed investigation files lose CLEIR status once prosecution is complete or the case is abandoned',
            'Arrest records, incident/offense reports, booking data, and CAD logs are public regardless of CLEIR claims',
            'Under Steckman, the agency must demonstrate that specific disclosure would cause a specific enumerated harm, not assert a general category',
            'If the alleged "confidential technique" is common knowledge or standard police practice, the exemption does not apply',
            'Challenge overbroad redactions where non-exempt contextual information is removed along with legitimately exempt content',
            'Body-worn camera footage is generally public in Ohio unless a specific CLEIR harm applies to each segment',
        ]),
        'notes': 'State ex rel. Steckman v. Jackson, 70 Ohio St.3d 420 (1994) is the foundational Ohio CLEIR case. Ohio courts consistently hold that completed-case files are not CLEIRs. The Ohio Supreme Court has emphasized that the burden of proving the exemption rests entirely on the agency. Ohio AG opinions provide additional guidance on specific record types within law enforcement agencies.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(v); ORC § 149.43(A)(7)(a)',
        'exemption_number': 'ORC § 149.43(A)(1)(v)',
        'short_name': 'Medical Records and Protected Health Information',
        'category': 'privacy',
        'description': 'Medical records, mental health records, and related protected health information maintained by a public agency are exempt from disclosure to protect individual privacy and comply with state and federal health information laws.',
        'scope': 'Medical records as defined in ORC § 149.43(A)(3): any document or combination of documents, including writings, drawings, graphs, charts, photographs, recordings, and other data compilations in any form, that are maintained by a medical provider or public agency and that describe a patient\'s or person\'s health history, diagnosis, condition, treatment, or evaluation. The exemption applies to identifiable individual health information — aggregate or anonymized health data and public health statistics are not covered. HIPAA preempts inconsistent state disclosure requirements. Records describing an agency\'s medical program policy, expenditures, or contracting are generally public.',
        'key_terms': json.dumps([
            'medical record', 'protected health information', 'PHI', 'HIPAA',
            'health information', 'mental health record', 'patient record',
            'diagnosis', 'treatment record', 'ORC 149.43(A)(1)(v)',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health data and anonymized public health statistics are public — only individually identifiable records are exempt',
            'Records describing agency health program policy, budgets, and contracts are not patient records and must be disclosed',
            'Challenge whether the record actually qualifies as a "medical record" under ORC § 149.43(A)(3) — the definition is not unlimited',
            'Redaction of identifying information may allow disclosure of the underlying health data',
            'Deceased persons\' medical records may have reduced privacy protection depending on context',
        ]),
        'notes': 'Ohio\'s medical records exemption tracks the definition in ORC § 149.43(A)(3). Federal HIPAA requirements generally parallel Ohio\'s protection for individually identifiable health information. The Ohio Supreme Court has held that agencies must segregate and release non-exempt portions of records containing medical information rather than withholding entire documents.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(p)',
        'exemption_number': 'ORC § 149.43(A)(1)(p)',
        'short_name': 'Attorney-Client Privileged Communications',
        'category': 'deliberative',
        'description': 'Records that are attorney-client privileged communications are exempt from public disclosure. The privilege protects confidential communications between government attorneys and their client agencies made for the purpose of obtaining or providing legal advice.',
        'scope': 'Confidential communications between a government agency and its legal counsel made for the purpose of rendering or receiving legal advice, and attorney work product prepared in anticipation of litigation. The privilege is narrow — it covers legal advice, not business or policy recommendations. Billing records, engagement letters, and general financial arrangements with outside counsel are generally not privileged. Facts independently known by the agency are not protected simply because they were communicated to an attorney. Waiver occurs through voluntary disclosure in non-privileged contexts.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'privileged communication', 'litigation', 'ORC 149.43(A)(1)(p)',
            'attorney work product', 'in anticipation of litigation',
            'legal opinion', 'confidential legal communication',
        ]),
        'counter_arguments': json.dumps([
            'Communications providing policy or business advice rather than legal advice are not privileged',
            'The privilege is waived if the agency discloses the advice in public proceedings or to outside parties',
            'Attorney billing records are generally public — they describe services rendered, not legal advice',
            'Facts underlying legal advice are not privileged — the agency cannot shield factual information by routing it through counsel',
            'Ohio courts apply the privilege narrowly given the PRA\'s strong disclosure mandate',
            'Challenge whether the communication was truly confidential or whether waiver occurred through agency action based on the advice',
        ]),
        'notes': 'Ohio recognizes attorney-client privilege and work product protection for government entities under ORC § 149.43(A)(1)(p). The Ohio Supreme Court has applied the privilege narrowly and consistently requires record-specific justification. See State ex rel. Leslie v. Ohio Housing Finance Agency, 105 Ohio St.3d 261 (2005).',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(a)',
        'exemption_number': 'ORC § 149.43(A)(1)(a)',
        'short_name': 'Trial Preparation Records',
        'category': 'law_enforcement',
        'description': 'Trial preparation records — records prepared by or for a public office or its legal counsel in connection with pending or contemplated litigation — are exempt from disclosure under Ohio law.',
        'scope': 'Records prepared by or for a public office in connection with pending or reasonably anticipated litigation. The exemption covers true work product: attorney mental impressions, litigation strategy, legal theories, and materials assembled for trial. It does not cover underlying factual records that existed independently of the litigation, even if those records are now being used in litigation. The agency must be a party to or reasonably anticipating specific litigation — speculative future litigation does not qualify. Records that would be discoverable in the litigation may be subject to reduced exemption protection.',
        'key_terms': json.dumps([
            'trial preparation', 'litigation records', 'work product',
            'pending litigation', 'contemplated litigation', 'ORC 149.43(A)(1)(a)',
            'attorney work product', 'litigation strategy', 'legal theory',
        ]),
        'counter_arguments': json.dumps([
            'Pre-existing factual records that the agency is now using in litigation are not trial preparation records — they were public before litigation began',
            'Speculative future litigation does not trigger the exemption — there must be a specific, reasonably anticipated case',
            'Challenge whether the record was "prepared for" litigation or was a routine agency record that happens to be relevant to litigation',
            'Records that would be subject to civil discovery may have reduced exemption claims',
            'Once litigation concludes, the trial preparation exemption argument weakens significantly',
        ]),
        'notes': 'Ohio\'s trial preparation exemption under ORC § 149.43(A)(1)(a) is distinct from the CLEIR exemption and focuses on litigation context. Ohio courts have held that this exemption does not protect pre-existing public records from disclosure merely because they are relevant to pending litigation. See State ex rel. Thomas v. Ohio State University, 71 Ohio St.3d 245 (1994).',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(q); ORC § 3701.17',
        'exemption_number': 'ORC § 149.43(A)(1)(q)',
        'short_name': 'Adoption and Juvenile Court Records',
        'category': 'privacy',
        'description': 'Adoption records, juvenile court records, and records of the Bureau of Criminal Identification and Investigation (BCI) relating to juvenile adjudications are exempt from disclosure to protect the privacy of minors and the integrity of juvenile proceedings.',
        'scope': 'Records sealed by a court, adoption records under ORC Chapter 3107, and juvenile delinquency records under ORC Chapter 2152. The exemption is grounded in Ohio\'s strong public policy of rehabilitating juvenile offenders and sealing their records from public view. Adult criminal records are generally public. The exemption does not cover general juvenile justice program statistics, aggregate data, or policy documents about the juvenile justice system.',
        'key_terms': json.dumps([
            'adoption record', 'juvenile court record', 'juvenile delinquency',
            'sealed record', 'minor', 'BCI', 'Bureau of Criminal Identification',
            'ORC Chapter 3107', 'ORC Chapter 2152', 'juvenile adjudication',
        ]),
        'counter_arguments': json.dumps([
            'Adult criminal records and adult court proceedings are fully public',
            'Aggregate statistics about juvenile justice outcomes and program performance are public',
            'Policy documents and budget records for juvenile agencies are public',
            'Challenge claims that records about adults involved in juvenile matters are themselves protected as juvenile records',
        ]),
        'notes': 'Ohio\'s juvenile records protections are codified primarily in ORC Chapter 2152 and ORC § 149.43(A)(1)(q). Courts have held that the protection is for the specific records of the juvenile proceedings, not for all agency records that reference a minor.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.433',
        'exemption_number': 'ORC § 149.433',
        'short_name': 'Infrastructure and Security Records',
        'category': 'safety',
        'description': 'Infrastructure records and security records relating to critical public infrastructure — including water systems, power grids, transportation networks, and government buildings — are exempt from disclosure where release would create a specific security risk.',
        'scope': 'Under ORC § 149.433, "infrastructure record" means any record that discloses the specific operational details of a critical infrastructure facility, the location of any critical infrastructure, or the security vulnerabilities of any critical infrastructure. "Security record" means any record that contains information directly used for protecting or securing a critical infrastructure facility. The exemption requires specificity — budget records, contracts, and general program descriptions for infrastructure security are not automatically protected. The agency must identify the specific security harm from disclosure.',
        'key_terms': json.dumps([
            'infrastructure record', 'security record', 'critical infrastructure',
            'ORC 149.433', 'water system', 'power grid', 'transportation',
            'security vulnerability', 'infrastructure security', 'facility security',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a specific security vulnerability — general "security-related" labeling is insufficient',
            'Budget and expenditure records for infrastructure security programs are public',
            'Contracts with security vendors are generally public except for the specific technical specifications that would reveal vulnerabilities',
            'Inspection records and compliance documents that do not reveal specific vulnerabilities are public',
            'Challenge whether the record actually discloses "operational details" or "security vulnerabilities" rather than general program information',
        ]),
        'notes': 'ORC § 149.433 is Ohio\'s dedicated critical infrastructure exemption, enacted after 9/11. Ohio courts apply it narrowly and require specific justification for each withheld record. General contract amounts and performance metrics are public even for infrastructure security contractors.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(b)',
        'exemption_number': 'ORC § 149.43(A)(1)(b)',
        'short_name': 'Personnel Records — Private Employee Information',
        'category': 'privacy',
        'description': 'Personal information in employee records — including home addresses, home telephone numbers, personal email addresses, Social Security numbers, and medical information — is exempt. However, the name, position, salary, and work contact information of public employees are public.',
        'scope': 'Ohio\'s personnel records exemption is carefully bounded. Under ORC § 149.43(A)(1)(b) and related provisions, the following are exempt: Social Security numbers, home addresses, home phone numbers, personal email, bank account numbers, and medical information in personnel files. The following are affirmatively public: employee name, current and prior positions held, current and prior duties, current and prior salary, current and prior employer, business address, and business phone. Disciplinary records and performance evaluations may be partially exempt but contain public components.',
        'key_terms': json.dumps([
            'personnel record', 'employee record', 'home address', 'Social Security number',
            'personal email', 'ORC 149.43(A)(1)(b)', 'employee privacy',
            'salary record', 'disciplinary record', 'public employee',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, salary, work address, and work phone of public employees are affirmatively public under Ohio law',
            'Disciplinary records must be partially disclosed — the nature of the violation and discipline imposed is public even if some personal details are exempt',
            'An employee\'s work activities, work communications, and work-related conduct are public, not personal',
            'Challenge overbroad redactions where the agency has removed public information (name, position, salary) along with genuinely exempt personal details',
            'Retirement and pension records of public employees are generally public under Ohio law',
        ]),
        'notes': 'Ohio\'s personnel records framework is a model of careful exemption scoping. The Ohio Supreme Court and Ohio Attorney General opinions have consistently reinforced that name, position, and salary are public. See State ex rel. Dispatch Printing Co. v. Wells, 18 Ohio St.3d 382 (1985) for the foundational analysis.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(aa)',
        'exemption_number': 'ORC § 149.43(A)(1)(aa)',
        'short_name': 'Residential and Familial Information of Specified Officials',
        'category': 'privacy',
        'description': 'Home addresses, home telephone numbers, and personal information of specified public officials — including judges, prosecutors, law enforcement officers, and their immediate family members — are exempt from disclosure to protect against targeted harassment or violence.',
        'scope': 'Residential and personal contact information of judges, magistrates, prosecutors, assistant prosecutors, law enforcement officers, and their spouses and minor children. The exemption was expanded in recent years to include additional categories of public safety personnel. It applies only to home/personal contact information — the official\'s work address, work phone, and official contact information remain public. The exemption is specific to enumerated categories of officials and does not extend to all public employees.',
        'key_terms': json.dumps([
            'judge home address', 'prosecutor personal information', 'law enforcement residential',
            'ORC 149.43(A)(1)(aa)', 'judicial privacy', 'official safety',
            'residential information', 'family member protection', 'personal contact information',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers only enumerated categories of officials — it does not extend to all government employees',
            'Work address, work phone, and official contact information for these officials remain public',
            'Challenge whether the claimed official falls within the specific statutory enumeration',
            'General information about the official\'s conduct and duties remains public',
        ]),
        'notes': 'Ohio has progressively expanded this exemption over recent legislative sessions. As of the most recent amendments, the list includes judges, magistrates, bailiffs, prosecutors, law enforcement officers, firefighters, and emergency medical personnel. Each expansion reflects concerns about targeted violence against public officials.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 1347.08; ORC § 149.43(A)(1)(m)',
        'exemption_number': 'ORC § 149.43(A)(1)(m)',
        'short_name': 'Social Security Numbers and Personal Identifiers',
        'category': 'privacy',
        'description': 'Social Security numbers and comparable personal identifiers in government records are exempt from disclosure to prevent identity theft and financial fraud. This exemption applies regardless of whether the record as a whole is public.',
        'scope': 'Social Security numbers, driver\'s license numbers, and similar government-issued identification numbers in any public record. The exemption is field-specific — the agency must redact the specific identifier and release the remainder of the record. It does not protect the entire document containing the identifier. Ohio\'s identity fraud statute (ORC § 2913.49) reinforces the policy against disclosure. Financial account numbers, PINs, and similar information are also typically protected under this provision.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'driver\'s license number',
            'personal identifier', 'ORC 149.43(A)(1)(m)', 'identity theft',
            'identity fraud', 'financial account number', 'PII',
            'personally identifiable information',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — the agency must redact only the identifier and release the rest of the document',
            'Names, positions, salaries, and other information in the same document are not protected by this exemption',
            'Challenge blanket withholding of entire documents when only specific identifier fields are exempt',
            'Information that has been made publicly available elsewhere cannot be withheld under this exemption',
        ]),
        'notes': 'Ohio\'s protection for personal identifiers is reinforced by ORC § 1347.08 (personal information systems) and aligns with federal identity fraud policy. The exemption is broadly applied to any government record containing SSNs or equivalent identifiers, but requires redaction-and-release rather than wholesale withholding.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(r)',
        'exemption_number': 'ORC § 149.43(A)(1)(r)',
        'short_name': 'Intellectual Property and Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial information submitted to Ohio public agencies by private entities are exempt from disclosure where they meet the Uniform Trade Secrets Act definition — independently valuable, not generally known, and subject to reasonable secrecy measures.',
        'scope': 'Trade secrets as defined in ORC § 1333.61 (Ohio\'s Uniform Trade Secrets Act): information, including a formula, pattern, compilation, program, device, method, technique, or process that derives independent economic value from not being generally known and is subject to reasonable efforts to maintain secrecy. Government-generated records cannot be trade secrets. The agency must independently evaluate trade secret claims — it cannot simply defer to vendor designations. Government contract prices and amounts paid with public funds are generally public even when claimed as trade secrets.',
        'key_terms': json.dumps([
            'trade secret', 'ORC 1333.61', 'proprietary information', 'UTSA',
            'competitive harm', 'commercial information', 'economic value',
            'confidential business information', 'ORC 149.43(A)(1)(r)',
            'vendor information', 'contractor records',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts and prices paid with public funds are generally public regardless of trade secret claims',
            'The submitter must affirmatively demonstrate that the information meets the UTSA definition — a "confidential" designation is not self-executing',
            'Information required by law to be submitted to the government has reduced expectations of secrecy',
            'Challenge whether the submitter actually maintained reasonable secrecy measures — disclosure elsewhere defeats the claim',
            'Government-generated records and analysis cannot be trade secrets',
            'The agency, not the submitter, controls the final determination and must apply an independent analysis',
        ]),
        'notes': 'Ohio\'s trade secret exemption applies the UTSA framework under ORC § 1333.61. The Ohio Supreme Court has held that agencies must conduct an independent analysis and may not simply accept vendor designations. See State ex rel. Plain Dealer Publishing Co. v. Cleveland, 75 Ohio St.3d 31 (1996).',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(o)',
        'exemption_number': 'ORC § 149.43(A)(1)(o)',
        'short_name': 'Audit Working Papers',
        'category': 'deliberative',
        'description': 'Audit working papers of the Auditor of State and other public auditors are exempt from disclosure during an active audit to protect the integrity of the audit process and prevent premature disclosure of tentative findings that may change before the final report.',
        'scope': 'Working papers, draft findings, internal audit memoranda, and preliminary materials prepared during an ongoing audit by the Auditor of State or an authorized audit function. The exemption applies only during the audit — once the final audit report is issued, the underlying working papers become public. The final audit report itself is always public. The exemption does not protect communications with the audited agency after findings are communicated, because those communications relate to final, not preliminary, conclusions.',
        'key_terms': json.dumps([
            'audit working papers', 'Auditor of State', 'draft audit findings',
            'preliminary audit', 'ORC 149.43(A)(1)(o)', 'audit memorandum',
            'ongoing audit', 'internal audit', 'audit process',
        ]),
        'counter_arguments': json.dumps([
            'The final audit report is always public and may be requested even while an audit is ongoing',
            'Once the audit concludes, working papers become public — challenge any post-audit withholding',
            'Communications with the audited agency about final findings are not working papers',
            'Budget and contracting records for the audit function itself are public',
        ]),
        'notes': 'Ohio\'s audit working papers exemption is a recognized but time-limited protection. The Ohio Auditor of State regularly issues final reports that are broadly public. Challenge any claim that working papers remain exempt after the final report is issued.',
    },
    {
        'jurisdiction': 'OH',
        'statute_citation': 'ORC § 149.43(A)(1)(s)',
        'exemption_number': 'ORC § 149.43(A)(1)(s)',
        'short_name': 'Confidential Personal Financial Information',
        'category': 'privacy',
        'description': 'Personal financial information submitted to public agencies by private individuals — including tax returns, financial statements, and bank account information — is exempt from public disclosure to protect individual financial privacy.',
        'scope': 'Personal financial information submitted by private individuals in connection with applications for licenses, permits, assistance programs, or regulatory compliance. Includes personal tax returns, personal financial statements, personal bank account records, and similar documents. Does not protect corporate financial information submitted by business entities, information about public funds and expenditures, or aggregate financial data. Information about how agencies spend public money is never exempt under this provision.',
        'key_terms': json.dumps([
            'personal financial information', 'tax return', 'financial statement',
            'bank account information', 'ORC 149.43(A)(1)(s)', 'financial privacy',
            'income information', 'asset information', 'personal finance',
        ]),
        'counter_arguments': json.dumps([
            'Corporate and business financial information submitted by entities (not individuals) has different protection under trade secret analysis',
            'Information about how the agency itself spends public money is never protected',
            'Aggregate program statistics and eligibility data are public',
            'Challenge whether the information is truly "personal" or relates to a business activity',
            'Information that has been publicly filed (e.g., in court proceedings) cannot be withheld under this exemption',
        ]),
        'notes': 'Ohio\'s personal financial information exemption protects individual privacy in the regulatory and benefits context. It is distinct from the trade secret exemption applicable to business information. Ohio courts have consistently held that public expenditure and government financial data are not covered by any financial privacy exemption.',
    },
]

# =============================================================================
# RULES
# Ohio Public Records Act, ORC § 149.43
# Ohio's distinctive features: 4-business-day response standard (not
# deadline for production, but for response); mandamus enforcement in Court
# of Claims or common pleas; statutory damages of $100/day up to $1,000;
# mandatory attorney fees for prevailing requesters; no administrative appeal.
# ORC § 149.43(B) sets out the core access and response obligations.
# =============================================================================

OH_RULES = [
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'response_standard_days',
        'param_value': '4',
        'day_type': 'business',
        'statute_citation': 'ORC § 149.43(B)(1)',
        'notes': 'Under ORC § 149.43(B)(1), a public office must respond to a records request within a reasonable period of time not to exceed 4 business days for certain request types, or notify the requester within 4 business days if more time is needed. This is frequently cited as a 4-business-day standard, though technically ORC § 149.43(B)(1) states records must be provided within a "reasonable" timeframe. The Ohio Supreme Court has used 4 business days as a benchmark. Longer delays trigger the statutory damages provision. Note: Ohio does not have a strict production deadline — it has a standard of reasonableness anchored to the 4-business-day acknowledgment benchmark.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'acknowledge_or_extend_deadline_days',
        'param_value': '4',
        'day_type': 'business',
        'statute_citation': 'ORC § 149.43(B)(1)',
        'notes': 'An Ohio public office that cannot provide all requested records within 4 business days must notify the requester within that 4-business-day period and provide an estimated production date. The office must also identify any records being withheld and cite the specific statutory exemption for each withheld record. Failure to provide notice within 4 business days is itself a violation of the PRA that can support the statutory damages remedy. The notice must include specific exemption citations, not mere category descriptions.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(B)',
        'notes': 'Ohio does not require public records requests to be in writing. Oral requests are valid under the PRA. However, written requests are strongly recommended to establish the record of the request, trigger the 4-business-day clock, and document any denials. Many Ohio agencies have online portals for submitting requests, which is convenient but not mandatory. The requester need not provide their name, address, or purpose for the request.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'purpose_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(B)',
        'notes': 'Ohio agencies may NOT require requesters to state the purpose of their request or provide their identity. The right of access is universal — motive is irrelevant. An agency that conditions access on a stated purpose or identity is violating the PRA. The Ohio Supreme Court has repeatedly held that intent and purpose are not proper considerations in evaluating a public records request. Agencies are also prohibited from asking whether the requester will use records for commercial purposes as a condition of access.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(B)(1)',
        'notes': 'Ohio agencies must release all nonexempt, reasonably segregable portions of records when only part qualifies for an exemption. Blanket withholding of documents containing some exempt content is a PRA violation. The agency must make specific redactions and release the remainder. Ohio courts apply this requirement strictly — failure to segregate can result in statutory damages and mandatory attorney fees. The agency must provide a log identifying each withheld record and the specific exemption claimed.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_per_page',
        'param_value': '0.05',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(B)(1)',
        'notes': 'Ohio agencies may charge the actual cost of copying records — not staff time for searching, reviewing, or redacting. The standard paper copy rate is typically $0.05 per page for black-and-white letter-size copies, though this varies by agency. Agencies may not charge for labor associated with searching or compiling records. For electronic records, the charge is the actual cost of the digital medium — often zero for email delivery. Excessive fee estimates that effectively prevent access may be challenged as violations of the PRA.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'fee_cap',
        'param_key': 'no_search_or_review_fees',
        'param_value': 'prohibited',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(B)(1)',
        'notes': 'Ohio explicitly prohibits charging for staff time spent searching for, compiling, or reviewing records. Only actual reproduction costs are permissible. An agency that charges hourly rates for "research" or "review" time is violating the PRA. This is a significant distinction from some other states that permit research fees. Ohio requesters can challenge any fee estimate that includes labor components.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(C)',
        'notes': 'Ohio has NO formal administrative appeal process for public records denials. There is no agency head appeal, no ombudsman, and no state-level administrative tribunal. A requester who believes records were wrongfully withheld or that response was unreasonably delayed must seek relief through mandamus in the Ohio Court of Claims or the court of common pleas. The Ohio Attorney General\'s office offers informal mediation assistance in some cases, but this is not a formal appeal mechanism and does not toll any deadlines.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'mandamus_in_court_of_claims',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(C)(1)',
        'notes': 'A requester may file a mandamus action in the Ohio Court of Claims under ORC § 149.43(C)(1) to compel production of records. The Court of Claims has exclusive original jurisdiction for mandamus actions against state agencies. Mandamus actions against local agencies (counties, cities, townships, school boards) are filed in the court of common pleas. The court reviews the denial de novo and may conduct in camera review. There is no statute of limitations for mandamus actions, but unreasonable delay may affect the court\'s discretion on damages.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'penalty',
        'param_key': 'statutory_damages_per_day',
        'param_value': '100',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(C)(2)',
        'notes': 'Ohio provides for statutory damages of $100 per day (maximum $1,000 per request) for each day the requester was prevented from inspecting or copying public records after the 4-business-day benchmark period. Under ORC § 149.43(C)(2), the court SHALL award these damages if the public office violated the PRA, unless the office had a good-faith basis for withholding. The $100/day statutory damages are unique among state public records laws and provide strong deterrence against unjustified withholding. The maximum $1,000 per request cap limits the total exposure.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_mandatory',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(C)(2)(b)',
        'notes': 'Under ORC § 149.43(C)(2)(b), if a requester substantially prevails in a mandamus action, the court SHALL award reasonable attorney fees and litigation costs. This is a mandatory provision — the court has no discretion to deny fees to a prevailing requester. The mandatory fee-shifting provision makes it economically viable for requesters and their attorneys to bring PRA enforcement actions. Fees are awarded for all reasonable attorney time expended in the litigation, not just the portion related to specific records.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'penalty',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(A)(1)',
        'notes': 'Under Ohio law, the burden of demonstrating that any record is exempt from the definition of "public record" rests on the public office claiming the exemption. The definition of "public record" in ORC § 149.43(A)(1) explicitly excludes enumerated categories — the agency must show that the specific record falls within an enumerated exclusion. Mere generalized assertions are insufficient. Ohio courts review the agency\'s exemption claims de novo in mandamus proceedings.',
    },
    {
        'jurisdiction': 'OH',
        'rule_type': 'initial_response',
        'param_key': 'mediation_available',
        'param_value': 'ohio_ag_informal',
        'day_type': None,
        'statute_citation': 'ORC § 149.43(D)',
        'notes': 'The Ohio Attorney General\'s office offers a free informal mediation service for public records disputes. Under ORC § 149.43(D), a requester or public office may ask the Ohio AG to informally mediate a dispute. The mediation is non-binding and does not toll any deadlines or create formal legal rights. It is often faster than court action and can resolve disputes without litigation. The AG\'s office also issues public records advisory opinions, which are persuasive but not binding on courts.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

OH_TEMPLATES = [
    {
        'jurisdiction': 'OH',
        'record_type': 'general',
        'template_name': 'General Ohio Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Ohio Public Records Act Request — ORC § 149.43

Dear Public Records Officer:

Pursuant to the Ohio Public Records Act, ORC § 149.43 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. Electronic delivery incurs zero reproduction cost.

I am willing to pay the actual cost of reproducing records per ORC § 149.43(B)(1). Ohio law does not permit agencies to charge for staff time spent searching for, compiling, or reviewing records. If copying fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under ORC § 149.43(A)(1), the burden of demonstrating that any record falls within a statutory exception rests on the public office. Under ORC § 149.43(B)(1), the agency must release all nonexempt, reasonably segregable portions of any record where only part qualifies for an exception.

If any records or portions of records are withheld, I request that you: (1) identify each withheld record with sufficient detail to evaluate the claimed exception; (2) cite the specific statutory exception under ORC § 149.43(A)(1) (specific subsection, not just "ORC § 149.43"); (3) explain how the specific exception applies to each specific record; and (4) confirm that all nonexempt, segregable portions of partially withheld records have been released.

Ohio law requires a response within a reasonable time — the Ohio Supreme Court has established 4 business days as the benchmark. Please respond within that period.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Ohio's Public Records Act does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically via email or download link, the actual cost of reproduction is zero under ORC § 149.43(B)(1).

Ohio's PRA reflects a strong public policy of governmental transparency. A fee waiver for this request would advance that policy.''',
        'expedited_language': '''I request that this public records request be processed as expeditiously as possible. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately at {{requester_phone}} or {{requester_email}} if there are any questions that would allow faster production.''',
        'notes': 'General Ohio PRA template. Key Ohio features: (1) 4-business-day response benchmark — cite ORC § 149.43(B)(1); (2) no administrative appeal — mandamus in Court of Claims (state agencies) or common pleas (local agencies) under ORC § 149.43(C); (3) statutory damages of $100/day (max $1,000) under ORC § 149.43(C)(2); (4) mandatory attorney fees for prevailing requesters under ORC § 149.43(C)(2)(b); (5) no charge for search or review time — only reproduction costs; (6) no reason or identity required. Reference ORC § 149.43, not "FOIA."',
    },
    {
        'jurisdiction': 'OH',
        'record_type': 'law_enforcement',
        'template_name': 'Ohio Public Records Act Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Ohio Public Records Act Request — Law Enforcement Records, ORC § 149.43

Dear Public Records Officer:

Pursuant to the Ohio Public Records Act, ORC § 149.43 et seq., I request copies of the following law enforcement records:

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

Regarding the Confidential Law Enforcement Investigatory Records (CLEIR) exception under ORC § 149.43(A)(1)(h): Ohio law does not permit blanket withholding of law enforcement records. Under State ex rel. Steckman v. Jackson, 70 Ohio St.3d 420 (1994), each CLEIR claim requires specific identification of which harm applies — confidential informant identity, specific investigative technique, safety endangerment, or interference with pending prosecution. A generic statement that records are "investigatory" is insufficient.

[If matter appears concluded:] If no criminal prosecution is currently pending or if any related prosecution has concluded, the interference rationale under ORC § 149.43(A)(1)(h) does not apply to completed matters.

Ohio agencies bear the burden of demonstrating that each specific record qualifies as a CLEIR. Under ORC § 149.43(B)(1), all nonexempt, reasonably segregable portions of partially withheld records must be released.

I am willing to pay reasonable reproduction costs (not search or review time fees). If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Please respond within 4 business days per the Ohio Supreme Court's benchmark under ORC § 149.43(B)(1).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs zero reproduction cost. A fee waiver is consistent with Ohio's strong public records policy under ORC § 149.43.''',
        'expedited_language': '''I request expedited processing of this records request. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Ohio law enforcement records template. Ohio-specific features: (1) CLEIR exception under ORC § 149.43(A)(1)(h) is strictly construed — cite Steckman to signal awareness; (2) completed investigation files are generally not CLEIRs; (3) body camera footage is generally public absent a specific CLEIR harm; (4) no administrative appeal — mandamus in Court of Claims or common pleas; (5) statutory damages $100/day up to $1,000 under ORC § 149.43(C)(2); (6) mandatory attorney fees for prevailing requesters.',
    },
    {
        'jurisdiction': 'OH',
        'record_type': 'government_contracts',
        'template_name': 'Ohio Public Records Act Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Ohio Public Records Act Request — Contracts and Expenditure Records, ORC § 149.43

Dear Public Records Officer:

Pursuant to the Ohio Public Records Act, ORC § 149.43 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Contractor/vendor (if applicable): {{contractor_name}}
Contract period: {{date_range_start}} through {{date_range_end}}
Contract number (if known): {{contract_number}}

This request includes, but is not limited to:
- Executed contracts and all amendments/modifications
- Bid and proposal documents, including all submitted bids
- Invoices, payment records, and vouchers
- Performance evaluations and compliance records
- Correspondence between the agency and the contractor relating to the contract

Regarding trade secret claims under ORC § 149.43(A)(1)(r): Under Ohio law, contract prices, amounts paid with public funds, and total compensation are always public regardless of vendor trade secret designations. See State ex rel. Plain Dealer Publishing Co. v. Cleveland, 75 Ohio St.3d 31 (1996). Vendor designations of "proprietary" or "confidential" are not self-executing — the agency must independently determine whether records meet the UTSA definition under ORC § 1333.61 and cannot simply defer to contractor claims.

Under ORC § 149.43(A)(1), the burden of demonstrating that any record falls within a statutory exception rests on the public office. The agency may not withhold entire contracts because some portions may qualify for protection — it must release all nonexempt, segregable portions.

I am willing to pay the actual cost of reproduction (not search or review time). If fees will exceed ${{fee_limit}}, please notify me.

Please respond within 4 business days per ORC § 149.43(B)(1).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records relate to {{public_interest_explanation}} and concern the expenditure of public funds — a matter at the core of governmental transparency. Electronic delivery incurs zero reproduction cost. A fee waiver is consistent with Ohio's strong public records policy under ORC § 149.43.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. These contract records are needed by {{needed_by_date}} due to {{urgency_explanation}}.''',
        'notes': 'Ohio government contracts template. Key points: (1) contract prices and amounts paid with public funds are always public — cite Plain Dealer v. Cleveland; (2) trade secret claims require independent agency analysis, not deference to vendor designations; (3) the agency must redact only legitimately exempt portions and release the remainder; (4) this template is well-suited for investigative journalism, government accountability research, and contractor compliance monitoring.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in OH_EXEMPTIONS:
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

    print(f'OH exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in OH_RULES:
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

    print(f'OH rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in OH_TEMPLATES:
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

    print(f'OH templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'OH total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_oh', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
