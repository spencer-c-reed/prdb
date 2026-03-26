#!/usr/bin/env python3
"""Build Tennessee Public Records Act data: exemptions, rules, and templates.

Covers Tennessee's Public Records Act, T.C.A. § 10-7-503 et seq.
Tennessee has a broad definition of "public record" and a strong disclosure
presumption. The statute requires agencies to respond "promptly" and allows
enforcement directly in chancery or circuit court, with mandatory attorney's
fees for prevailing requesters. There is no administrative appeal mechanism.

Run: python3 scripts/build/build_tn.py
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
# Tennessee's Public Records Act defines "public record" broadly to include
# essentially all documents made or received in connection with official
# government business, regardless of form. T.C.A. § 10-7-503(a)(1)(A).
# Exemptions are scattered across the Tennessee Code and must be specifically
# invoked — a generic confidentiality claim is insufficient. Courts apply
# strict construction of exemptions in favor of disclosure.
# =============================================================================

TN_EXEMPTIONS = [
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(1)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(1)',
        'short_name': 'Medical Records',
        'category': 'privacy',
        'description': 'Medical records, health information, and related treatment records of individual patients held by state or local health agencies and public hospitals are confidential and exempt from public disclosure.',
        'scope': 'Individual patient medical records, treatment records, health histories, and diagnostic information held by state or local public health agencies, public hospitals, and similar governmental health entities. The exemption protects individually identifiable health information. Aggregate health statistics, disease surveillance data, and public health reports that do not identify individuals are generally public. Administrative records, contracts, and financial documents of public health agencies are also public. Health department inspection reports for restaurants, facilities, and regulated entities are generally public.',
        'key_terms': json.dumps([
            'medical record', 'patient record', 'health information', 'treatment record',
            'public hospital', 'health department', 'individually identifiable',
            'HIPAA', 'protected health information', 'PHI', 'mental health record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are not covered by this exemption',
            'Administrative and financial records of public health agencies are fully public',
            'Restaurant and facility inspection reports are public records regardless of this exemption',
            'The exemption covers individually identifiable patient records — not the policies, procedures, and contracts of the healthcare entity',
            'Challenge whether a record is actually a "medical record" vs. an administrative correspondence that happens to mention health',
            'Records about public employee workers compensation injuries may have reduced protection as employment records',
        ]),
        'notes': 'T.C.A. § 10-7-504(a)(1) is one of Tennessee\'s most established confidentiality provisions for health records. Tennessee also incorporates federal HIPAA protections, but the state exemption applies independently to public agencies. Health department inspection reports for food service, childcare, and other regulated facilities are public records under a separate provision and are not protected by this exemption.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(2)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(2)',
        'short_name': 'Law Enforcement Investigative Records',
        'category': 'law_enforcement',
        'description': 'Records of investigation conducted by a law enforcement agency are confidential to the extent that disclosure would reveal the identity of a confidential informant, reveal evidence that would compromise an ongoing investigation, endanger life, or interfere with pending prosecution.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) reveal the identity of a confidential informant; (2) jeopardize the safety of any person; (3) impede or compromise an ongoing criminal investigation; or (4) interfere with a pending prosecution. The exemption is harm-based — it does not protect all investigation records automatically. Once prosecution concludes or investigation is closed with no prosecution, the interference rationale evaporates. Arrest records, booking records, incident reports, and records documenting the fact and nature of an incident are generally public. Factual portions of investigative files not implicating an enumerated harm must be segregated and released.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'ongoing investigation', 'pending prosecution', 'investigative technique',
            'endanger life', 'criminal intelligence', 'undercover operation',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records, booking records, and incident reports are public regardless of investigation status',
            'Completed investigation files are generally public once prosecution concludes or the matter is closed',
            'The agency must articulate a specific harm for each withheld record — a generic "investigation ongoing" is insufficient',
            'Factual material that does not reveal informants or techniques must be segregated and released',
            'Internal affairs investigation files for officer misconduct have been held public once concluded in Tennessee courts',
            'Challenge claims that civilian complaints against officers are covered — Tennessee courts have been skeptical of blanket IA exemptions',
        ]),
        'notes': 'Tennessee\'s law enforcement investigation exemption is frequently litigated. Tennessee courts have consistently held that the exemption is harm-based and does not protect all law enforcement records. The Tennessee Supreme Court has held that completed investigation files are generally public. Internal affairs records for concluded officer misconduct investigations have been subject to disclosure orders in several cases.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(7)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(7)',
        'short_name': 'Attorney-Client and Work Product',
        'category': 'deliberative',
        'description': 'Communications between an attorney and a governmental entity client made in confidence for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation, are exempt from public disclosure under the attorney-client privilege.',
        'scope': 'Confidential communications between government attorneys and their agency clients made for the purpose of obtaining legal advice. Covers attorney-client communications and attorney work product. The privilege requires that the communication be for legal (not business or policy) advice, made in confidence, and not waived. Billing records, general retainer agreements, and communications that are not seeking or providing legal advice are generally not privileged. The exemption does not protect facts independently known to the agency merely because they were communicated to an attorney. Tennessee courts apply the privilege to government entities but narrowly, consistent with the public records presumption.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'in anticipation of litigation',
            'privileged communication', 'legal opinion', 'confidential communication',
            'government attorney', 'attorney general opinion',
        ]),
        'counter_arguments': json.dumps([
            'The communication must seek legal advice, not business or policy guidance — the latter is not privileged',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when the agency discloses the content in public proceedings, to non-attorney staff, or to third parties outside the privilege',
            'Facts independently known to the agency are not privileged merely because they were shared with counsel',
            'Challenge whether the agency has waived privilege by acting on the advice in public decision-making',
            'Tennessee courts apply the privilege narrowly given the strong public records presumption in T.C.A. § 10-7-503',
        ]),
        'notes': 'Tennessee recognizes attorney-client privilege and work product protection for government entities through incorporation into the Public Records Act framework. T.C.A. § 10-7-504(a)(7) specifically references privileged communications. Tennessee courts have held that the privilege must be narrowly applied consistent with the strong disclosure policy underlying the Act. Attorney General opinions, once released publicly, are not covered by the privilege.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(4)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(4)',
        'short_name': 'Trade Secrets and Proprietary Business Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted by private entities to government agencies in the course of regulatory compliance or licensing may be withheld where disclosure would cause competitive harm to the submitter.',
        'scope': 'Trade secrets and proprietary commercial, financial, or business information submitted by private entities to state or local agencies in connection with licensing, regulation, procurement, or compliance. The information must: (1) be actually confidential; (2) have independent economic value from secrecy; and (3) be subject to reasonable measures to protect secrecy. Government-generated information does not constitute a trade secret. Contract prices and amounts paid with public funds are generally not protected. The agency must independently evaluate trade secret designations and may not defer entirely to vendor claims.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm', 'commercial information',
            'financial information', 'business confidential', 'economic value',
            'secrecy', 'regulatory submission', 'proprietary data',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts paid with public funds are generally public regardless of trade secret claims',
            'The submitter must demonstrate the information meets the legal trade secret definition — a confidentiality label is insufficient',
            'Publicly available information cannot be withheld as a trade secret',
            'Information required by law to be submitted to regulators has reduced secrecy expectations',
            'Challenge whether the submitter actually maintained secrecy — careless disclosure elsewhere defeats the claim',
            'Government-generated records and analyses cannot constitute trade secrets',
        ]),
        'notes': 'Tennessee\'s trade secret exemption applies Tennessee\'s Uniform Trade Secrets Act definition. The Tennessee Court of Appeals has held that agencies must independently analyze trade secret claims rather than simply accepting vendor designations. Contract amounts paid with public funds are uniformly public. The exemption is narrowly construed consistent with Tennessee\'s broad public records definition.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(17)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(17)',
        'short_name': 'Critical Infrastructure Security Information',
        'category': 'safety',
        'description': 'Records containing specific information about the vulnerability of critical public or privately owned infrastructure to attack or disruption, security plans for public facilities, and related information whose disclosure would create a specific security risk are exempt.',
        'scope': 'Specific vulnerability assessments, security plans, and related records for critical infrastructure (utilities, water systems, transportation) and public facilities where disclosure would create an articulable, specific security risk. The exemption requires that disclosure would present a specific risk — not a general possibility of misuse. Budget records, contracts, and expenditure data for security programs are generally public. The agency must articulate the specific harm for each withheld record, not invoke a blanket security exception.',
        'key_terms': json.dumps([
            'critical infrastructure', 'security plan', 'vulnerability assessment',
            'security risk', 'public facility', 'infrastructure protection',
            'terrorism', 'sabotage', 'cyber security', 'emergency response',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable for each withheld record — general security concerns are insufficient',
            'Budget and expenditure records for security programs are public',
            'Physical descriptions of public buildings and their general layout are not covered',
            'Challenge claims that entire contracts with security vendors are exempt when only specific technical details warrant protection',
            'General policies and procedures that do not reveal specific vulnerabilities are not covered',
        ]),
        'notes': 'T.C.A. § 10-7-504(a)(17) was added post-9/11 to address security concerns. Tennessee courts have applied it narrowly consistent with the overall disclosure mandate. Agencies invoking this exemption must articulate a specific, non-speculative security risk for each record withheld.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(27)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(27)',
        'short_name': 'Personal Information in Personnel Files',
        'category': 'privacy',
        'description': 'Certain personal information in the personnel files of public employees — including home addresses, personal telephone numbers, Social Security numbers, and medical information — is confidential and not subject to public disclosure, while employment-related information remains public.',
        'scope': 'Specific personal data fields within public employee personnel files: home addresses, personal telephone numbers, Social Security numbers, bank account information, and medical information. The exemption is field-specific — it protects personal details, not the entire personnel file. Public employment information including name, job title, department, salary, position, date of hire, and employment status remains public. Disciplinary actions and performance evaluations are generally public in Tennessee, though some details may be protected. The exemption reflects the distinction between public employees\' roles as government actors (fully public) and their personal private lives (protected).',
        'key_terms': json.dumps([
            'personnel file', 'public employee', 'home address', 'personal telephone',
            'Social Security number', 'employee privacy', 'employment record',
            'salary', 'disciplinary record', 'performance evaluation',
        ]),
        'counter_arguments': json.dumps([
            'Public employee name, job title, salary, department, and date of hire are public regardless of this exemption',
            'Disciplinary actions and formal reprimands are generally public in Tennessee',
            'The exemption is field-specific — only the enumerated personal data categories are protected, not the entire file',
            'Use-of-force and misconduct records for law enforcement officers have heightened public interest that may override privacy claims',
            'Records of final personnel actions (terminations, demotions, suspensions) are public',
            'Challenge whether requested information is actually within the protected fields or is employment-related information that must be disclosed',
        ]),
        'notes': 'Tennessee\'s personnel file exemption is among the more nuanced in the statute. T.C.A. § 10-7-504(a)(27) was amended over time to clarify which portions of personnel files are public. The general rule is that employment-related information is public while personal private information is protected. Tennessee courts have consistently held that salary, job title, and disciplinary records are public.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(26)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(26)',
        'short_name': 'Personal Identifying Information of Private Citizens',
        'category': 'privacy',
        'description': 'Social Security numbers, bank account numbers, and similar personal identifying information of private citizens (non-public employees) contained in government records is exempt from public disclosure to protect against identity theft.',
        'scope': 'Social Security numbers, bank account numbers, credit card numbers, driver\'s license numbers, and similar financial and personal identifying data of private (non-government-employee) individuals appearing in government records. The exemption is field-specific — it protects specific data elements, not entire records. Government records containing these fields must be produced with those fields redacted. Does not extend to names, addresses, professional licenses, regulatory compliance status, or other information about private parties\' interactions with government.',
        'key_terms': json.dumps([
            'Social Security number', 'bank account', 'private citizen', 'identity theft',
            'personal identifying information', 'PII', 'financial account', 'credit card number',
            'driver license number', 'identity fraud',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — agencies must redact the specific protected fields and release the remainder',
            'Names, addresses, professional license status, and regulatory records of private parties are public',
            'Challenge overbroad redactions where the agency removed non-exempt contextual information',
            'Information already publicly available cannot be withheld under this exemption',
        ]),
        'notes': 'T.C.A. § 10-7-504(a)(26) provides targeted protection for sensitive personal identifying data of private individuals in government records. It reflects a practical compromise: the government must be able to collect this information for legitimate purposes, but should not become a vector for identity theft. The exemption is limited to the specific data fields and does not justify wholesale withholding of records.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(6)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(6)',
        'short_name': 'Tax Returns and Confidential Tax Information',
        'category': 'statutory',
        'description': 'State and local tax returns and tax return information submitted by individuals or businesses to the Tennessee Department of Revenue or county revenue officials are confidential and exempt from public disclosure.',
        'scope': 'Individual and business tax returns, tax return information, and related tax filings submitted to the Department of Revenue or local county revenue offices. Covers income tax, franchise and excise tax, sales and use tax returns, and related filings. Aggregate revenue statistics, delinquency statistics, and enforcement program information are public. Final court judgments in tax collection cases and public liens filed in the court record are public. Does not protect information about the Department\'s operations, rulemaking, or enforcement policies.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'franchise tax',
            'excise tax', 'sales tax', 'taxpayer information', 'tax filing',
            'tax confidentiality', 'county assessor', 'property tax',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Final court judgments in tax collection cases are public',
            'Tax liens recorded in court records are public',
            'Information about the Department\'s own enforcement policies and operations is public',
            'Challenge whether the specific records are actual "tax return information" vs. regulatory correspondence',
            'Property tax assessment records (distinct from returns) are generally public in Tennessee',
        ]),
        'notes': 'Tennessee\'s tax confidentiality provision is well-established. Property tax assessment records are generally public as they are used in public valuation and appeals processes. The exemption is narrower than it might appear — it covers returns and return-derived information, not all revenue department records.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(10)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(10)',
        'short_name': 'Education Records — Student Privacy',
        'category': 'privacy',
        'description': 'Student education records held by public educational institutions are confidential pursuant to FERPA (20 U.S.C. § 1232g) and the corresponding Tennessee statutory framework, protecting individually identifiable student information.',
        'scope': 'Education records directly related to individual students at public schools, colleges, and universities, including transcripts, grades, disciplinary records, enrollment information, and other personally identifiable student data. Incorporates federal FERPA protections as a matter of state law. Aggregate educational statistics (graduation rates, test score distributions, enrollment figures) that do not identify individual students are public. Administrative and financial records of educational institutions unrelated to individual students are public. Records about faculty and staff are not student records and are subject to regular public records analysis.',
        'key_terms': json.dumps([
            'student record', 'education record', 'FERPA', 'student privacy',
            'transcript', 'grades', 'student disciplinary record', 'enrollment record',
            'personally identifiable student information', 'public school', 'university records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics that do not identify individual students are fully public',
            'Administrative and financial records of public educational institutions are public',
            'Faculty and staff employment records are not student records — apply standard public records analysis',
            'Records about institutional policies, disciplinary procedures, and systemic patterns may be public even if individual disciplinary records are protected',
            'Challenge claims that budget, facilities, and contractual records are covered by FERPA',
            'Once a student turns 18 or enrolls in post-secondary education, the student (not parents) controls the record, and may waive protection',
        ]),
        'notes': 'Tennessee incorporates FERPA protections for student education records. The federal FERPA framework applies to any educational institution receiving federal funding, which includes essentially all public schools and universities. The exemption is student-specific — it protects individually identifiable student data, not all records of educational institutions.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(f)',
        'exemption_number': 'T.C.A. § 10-7-504(f)',
        'short_name': 'Adoption Records',
        'category': 'privacy',
        'description': 'Records of adoption proceedings and related documents filed in court or held by state agencies that identify birth parents, adoptees, or adoptive families are confidential except as provided in Tennessee\'s controlled-access adoption records statutes.',
        'scope': 'Records of adoption proceedings, court filings identifying birth parents or adoptees, adoption agency records, and related documents. Tennessee has a specific statutory scheme for accessing adoption records that permits access under specified conditions through the courts and the Department of Children\'s Services. The general public records exemption does not override this specific statutory access scheme. Adult adoptees and birth parents have specific rights under the adoption records statutes that differ from the general public records right of access.',
        'key_terms': json.dumps([
            'adoption record', 'birth parent', 'adoptee', 'adoption agency',
            'Department of Children\'s Services', 'sealed record', 'birth certificate',
            'adoption decree', 'confidential intermediary',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics about adoption processes and outcomes are public',
            'Administrative records about adoption agency licensing and oversight are public',
            'Tennessee law provides specific rights of access for adult adoptees and birth parents through designated channels',
            'Records about systemic failures in the adoption system may be public even if individual adoption records are sealed',
        ]),
        'notes': 'Tennessee has a detailed statutory scheme for adoption records access separate from the general Public Records Act. This exemption operates as a reference to that scheme rather than a blanket prohibition. Tennessee law has been amended over time to expand access rights for adult adoptees seeking identifying information about their origins.',
    },
    {
        'jurisdiction': 'TN',
        'statute_citation': 'T.C.A. § 10-7-504(a)(36)',
        'exemption_number': 'T.C.A. § 10-7-504(a)(36)',
        'short_name': 'Cyber Security Vulnerability Information',
        'category': 'safety',
        'description': 'Information related to identified security vulnerabilities in government computer systems, networks, and critical technology infrastructure is confidential where disclosure would enable exploitation of those vulnerabilities.',
        'scope': 'Technical vulnerability assessments, penetration test results, security audit findings, and related documentation identifying specific exploitable weaknesses in government information systems, networks, and technology infrastructure. The exemption requires that the information identify a specific, exploitable vulnerability — general IT security policies, security budgets, and vendor contracts are not covered. Requires the agency to articulate why disclosure of the specific information would enable exploitation.',
        'key_terms': json.dumps([
            'cyber security', 'vulnerability', 'penetration test', 'security audit',
            'information system', 'network security', 'exploit', 'government network',
            'IT security', 'security assessment',
        ]),
        'counter_arguments': json.dumps([
            'General IT security policies and procedures that do not reveal specific vulnerabilities are public',
            'Budget and expenditure records for IT security programs are public',
            'Contracts with security vendors are generally public except for specific technical vulnerability details',
            'The agency must articulate why disclosure of the specific information would enable exploitation',
            'After vulnerabilities are patched, the exemption no longer applies to the historical finding',
        ]),
        'notes': 'T.C.A. § 10-7-504(a)(36) reflects the modern legislative trend of protecting cyber security information. Tennessee courts have not yet extensively interpreted this exemption, but the statutory text requires a specific nexus between disclosure and exploitation risk. Remediated vulnerabilities lose the protection rationale.',
    },
]

# =============================================================================
# RULES
# Tennessee Public Records Act, T.C.A. § 10-7-503 et seq.
# Tennessee's statute requires agencies to respond "promptly." The standard
# copy fee is $0.15/page. There is no administrative appeal — enforcement is
# directly in chancery or circuit court. Attorney's fees are available for
# prevailing requesters. The Office of Open Records Counsel provides advisory
# guidance but has no binding enforcement authority.
# =============================================================================

TN_RULES = [
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'response_standard',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(2)(A)',
        'notes': 'Tennessee agencies must respond to public records requests "promptly." The statute does not define a specific number of days. Tennessee courts and the Office of Open Records Counsel have interpreted "promptly" to generally mean within 7 business days for routine requests, though this is not a hard statutory deadline. Larger or more complex requests may require more time, but the agency must communicate with the requester about timing. Unreasonable delay is enforceable through chancery court. The "promptly" standard creates a practical window for follow-up if no response is received within 5-7 business days.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'written_acknowledgment_not_required',
        'param_value': 'no_specific_acknowledgment_deadline',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(2)(A)',
        'notes': 'Unlike some states, Tennessee does not specify a mandatory written acknowledgment deadline separate from the production requirement. The "promptly" standard applies to the overall response. Requesters should follow up if they do not hear back within 7 business days. For oral requests, Tennessee law is clear that in-person inspection of records must be accommodated promptly during normal business hours. Written requests create a clearer paper trail for enforcement purposes.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'in_person_inspection_right',
        'param_value': 'yes_during_business_hours',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(2)(A)',
        'notes': 'Tennessee law expressly provides that any citizen of Tennessee has the right to inspect public records during business hours free of charge. The right of inspection is distinct from the right to obtain copies. Agencies must allow in-person inspection without charge — they may only charge for making copies. Agencies may not require advance notice for routine inspection of records that are not actively in use. Tennessee courts have enforced the inspection right broadly.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate_per_page',
        'param_value': '0.15',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-506(a)',
        'notes': 'Tennessee agencies may charge a fee for copies of public records. The standard rate is $0.15 per page for standard 8.5" x 11" paper copies. T.C.A. § 10-7-506 governs fees and specifies that charges must reflect the actual cost of reproduction. Agencies may not charge for staff time spent locating or reviewing records. For electronic records, actual cost is minimal. The Office of Open Records Counsel has issued guidance on permissible fee structures. Unreasonably high fees may constitute an effective denial of access.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-506(a)',
        'notes': 'Tennessee agencies may not charge requesters for staff time spent locating, reviewing, or redacting records. Only the actual cost of reproduction is chargeable. This is a significant protection — agencies may not impose search fees or review fees as a deterrent to public records requests. Requesters should expressly object to any invoice that includes staff time charges and cite T.C.A. § 10-7-506.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_agency_discretion',
        'param_value': 'agency_discretion_no_statutory_right',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-506(a)',
        'notes': 'Tennessee does not provide a statutory right to fee waiver. Agencies may waive fees at their discretion. Requesters may argue for fee waivers on the basis of public interest, news media status, or nonprofit purpose, but these arguments rely on agency discretion rather than a legal entitlement. For electronic records delivered by email, the actual cost is often zero, effectively rendering fee waiver moot for many requests.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-505',
        'notes': 'Tennessee has NO formal administrative appeal mechanism for Public Records Act denials. There is no agency head appeal and no state administrative tribunal. The Office of Open Records Counsel provides advisory opinions but cannot compel disclosure. A requester denied access or facing unreasonable delay must bring an action directly in chancery or circuit court under T.C.A. § 10-7-505. This direct-to-court enforcement model means requesters should document the denial carefully for potential litigation.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'office_of_open_records_counsel',
        'param_value': 'advisory_only',
        'day_type': None,
        'statute_citation': 'T.C.A. § 8-4-601 et seq.',
        'notes': 'The Office of Open Records Counsel (OORC) provides free advisory opinions on public records disputes and guidance to agencies on compliance. However, OORC opinions are advisory only — they are not legally binding on the agency or a court. Nonetheless, OORC opinions carry persuasive weight and agencies that ignore them risk adverse outcomes in subsequent court proceedings. Requesters may consult OORC before or instead of litigation, and a favorable OORC opinion strengthens the requester\'s legal position.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'chancery_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-505',
        'notes': 'A requester denied access or facing unreasonable delay may bring a civil action in chancery or circuit court under T.C.A. § 10-7-505. The court reviews the denial de novo and may conduct in camera inspection of withheld records. If the court finds the agency violated the Act, it must award attorney\'s fees and costs to the requester. Courts in Tennessee have historically been willing to enforce the Public Records Act, including in cases of delay. There is no formal statute of limitations, but promptness in filing is advisable.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_mandatory',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-505(g)',
        'notes': 'If a requester substantially prevails in a public records enforcement action, the court SHALL award reasonable attorney\'s fees and costs. The fee-shifting provision is mandatory for prevailing requesters, making Tennessee a strong enforcement state despite the absence of administrative remedies. Attorneys\' fees are available when the requester obtains records through court order or when the agency releases records in response to a filed lawsuit (catalyst theory). This provision makes litigation economically viable even for modest-value requests.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(1)(A)',
        'notes': 'Tennessee law places the burden of demonstrating that a record is confidential or exempt on the agency. T.C.A. § 10-7-503(a)(1)(A) establishes a broad presumption that all public records are open to inspection. Agencies must affirmatively establish that a specific exemption applies to each withheld record. Tennessee courts review withholding decisions de novo without deference to the agency\'s initial determination. Vague or conclusory invocations of exemptions are insufficient.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(1)(A)',
        'notes': 'Tennessee agencies must release all non-confidential portions of records when only part of a record qualifies for an exemption. Blanket withholding of documents containing some confidential content is a violation of the Act. Agencies must redact the specifically protected portions and release the remainder. Tennessee courts have enforced segregability requirements and have imposed attorney\'s fees where agencies withheld entire documents when only portions were exempt.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'broad_definition_of_public_record',
        'param_value': 'all_documents_in_official_capacity',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-301(6)',
        'notes': 'Tennessee\'s definition of "public record" is among the broadest in the United States. T.C.A. § 10-7-301(6) defines public records as "all documents, papers, letters, maps, books, photographs, microfilms, electronic data processing files and output, films, sound recordings, or other material, regardless of physical form or characteristics" made or received in connection with official business. The definition is medium-neutral and includes electronic communications (email, text messages) made by public officials in their official capacity. Courts have held that the format of a record does not affect its status as a public record.',
    },
    {
        'jurisdiction': 'TN',
        'rule_type': 'initial_response',
        'param_key': 'citizen_of_tennessee_requirement',
        'param_value': 'yes_for_in_person_inspection',
        'day_type': None,
        'statute_citation': 'T.C.A. § 10-7-503(a)(2)(A)',
        'notes': 'Tennessee\'s Public Records Act technically limits the right of inspection to "any citizen of Tennessee." However, this limitation applies primarily to in-person inspection. In practice, Tennessee agencies routinely respond to requests from non-residents, and the restriction has been broadly interpreted. Additionally, federal and constitutional considerations may limit the enforceability of a strict citizenship requirement. Requesters who are not Tennessee residents should note this provision but should not assume their requests will be categorically refused.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

TN_TEMPLATES = [
    {
        'jurisdiction': 'TN',
        'record_type': 'general',
        'template_name': 'General Tennessee Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Tennessee Public Records Act, T.C.A. § 10-7-503 et seq.

Dear Records Custodian:

Pursuant to the Tennessee Public Records Act, T.C.A. § 10-7-503 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or downloadable file) where available, to minimize reproduction costs and production time.

I am willing to pay fees reflecting the actual cost of reproduction per T.C.A. § 10-7-506. I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Tennessee law. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under T.C.A. § 10-7-503(a)(1)(A), all public records are presumptively open to inspection and the burden of demonstrating that any record is confidential rests entirely on the agency. Any exemption must be specifically cited by T.C.A. section number — a general claim of confidentiality is insufficient.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) state the specific statutory basis for withholding (T.C.A. citation); (3) describe the record sufficiently for me to evaluate the claimed exemption; and (4) confirm that all non-confidential, segregable portions of partially withheld records have been released.

Please respond promptly as required by T.C.A. § 10-7-503(a)(2)(A). If you have questions that would assist in fulfilling this request, please contact me at the information above.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Tennessee law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is zero or minimal, making a fee waiver consistent with T.C.A. § 10-7-506.

The Tennessee Public Records Act reflects a strong public policy in favor of open government and government accountability.''',
        'expedited_language': '''I request that this public records request be processed as expeditiously as possible under the "promptly" requirement of T.C.A. § 10-7-503(a)(2)(A). Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond that date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would permit faster production.''',
        'notes': 'General-purpose Tennessee Public Records Act template. Key Tennessee features: (1) "promptly" is the response standard — no specific day count, but 7 business days is common practice; (2) no administrative appeal — go directly to chancery or circuit court if denied (T.C.A. § 10-7-505); (3) mandatory attorney\'s fees for prevailing requesters (T.C.A. § 10-7-505(g)); (4) $0.15/page standard copy fee, no staff time charges; (5) broad definition of public record includes electronic communications; (6) Office of Open Records Counsel provides advisory opinions but cannot compel disclosure. Reference T.C.A. § 10-7-503, not "FOIA."',
    },
    {
        'jurisdiction': 'TN',
        'record_type': 'law_enforcement',
        'template_name': 'Tennessee PRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, T.C.A. § 10-7-503 et seq.

Dear Records Custodian:

Pursuant to the Tennessee Public Records Act, T.C.A. § 10-7-503 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and related documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Written communications relating to the above
- Internal investigation records relating to the above (if concluded)

Regarding claimed exemptions under T.C.A. § 10-7-504(a)(2): Tennessee law does not permit blanket withholding of law enforcement records. Any withholding under this provision requires: (1) identification of the specific harm subcategory (reveals informant identity; endangers life; would impede ongoing investigation; would interfere with pending prosecution); and (2) articulation of how disclosure of each specific record would cause that specific harm.

[If matter appears concluded:] If no criminal prosecution is pending or prosecution has concluded, the "ongoing investigation" and "pending prosecution" rationales under T.C.A. § 10-7-504(a)(2) do not apply, and investigation records should be released.

Under T.C.A. § 10-7-503(a)(1)(A), the burden of demonstrating that any record is confidential rests entirely on the agency. All non-confidential, segregable portions of partially withheld records must be released.

I am willing to pay the actual cost of reproduction per T.C.A. § 10-7-506, up to ${{fee_limit}}, but not staff review time charges.

Please respond promptly as required by T.C.A. § 10-7-503(a)(2)(A).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs zero reproduction cost. The Tennessee Public Records Act reflects a strong policy of open government accountability.''',
        'expedited_language': '''I request expedited processing under T.C.A. § 10-7-503(a)(2)(A)\'s "promptly" requirement. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Tennessee law enforcement records template. Key Tennessee features: (1) T.C.A. § 10-7-504(a)(2) is harm-based — agencies must articulate specific harm for each record withheld; (2) arrest records and booking records are public; (3) completed investigation files are generally public once prosecution concludes; (4) internal affairs records for concluded investigations are subject to public disclosure; (5) no administrative appeal — T.C.A. § 10-7-505 provides for direct chancery/circuit court enforcement with mandatory attorney\'s fees; (6) Office of Open Records Counsel advisory opinions available as a pre-litigation step.',
    },
    {
        'jurisdiction': 'TN',
        'record_type': 'government_contracts',
        'template_name': 'Tennessee PRA Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Purchasing Director
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Government Contracts and Expenditures, T.C.A. § 10-7-503 et seq.

Dear Records Custodian:

Pursuant to the Tennessee Public Records Act, T.C.A. § 10-7-503 et seq., I request access to and copies of the following public records related to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, amendments, and change orders between {{agency_name}} and {{vendor_or_contractor_name}} from {{date_range_start}} through {{date_range_end}}
- Solicitation documents (RFPs, IFBs, RFQs) and all responsive bids or proposals
- Bid tabulation sheets and scoring documents
- Correspondence and communications related to the contract award process
- Invoices, payment records, and expenditure documentation
- Performance reports and compliance documentation

Regarding trade secret claims: Contract prices, quantities, and amounts paid with public funds are not trade secrets and must be disclosed. If trade secret claims are made for specific technical materials, the agency must independently evaluate those claims and may not simply defer to vendor designations. In any case, the agency must disclose the contract price and all amounts paid with public funds.

Under T.C.A. § 10-7-503(a)(1)(A), all public records are presumptively open and the burden of demonstrating any exemption rests on the agency.

I am willing to pay the actual cost of reproduction per T.C.A. § 10-7-506, up to ${{fee_limit}}.

Please respond promptly per T.C.A. § 10-7-503(a)(2)(A).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records relate to the expenditure of public funds, which is a matter of core public accountability. Electronic delivery incurs zero reproduction cost. A fee waiver serves the strong public interest in government transparency.''',
        'expedited_language': '''I request expedited processing under T.C.A. § 10-7-503(a)(2)(A). Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Tennessee government contracts template. Tennessee-specific notes: (1) contract amounts paid with public funds are always public regardless of trade secret claims; (2) bid documents and scoring records are generally public after contract award; (3) solicitation records (RFPs, proposals) may be withheld during the competitive procurement process but become public after award; (4) the broad Tennessee definition of "public record" includes all contract-related documents regardless of format; (5) "promptly" response standard applies; (6) mandatory attorney\'s fees for prevailing requesters creates strong enforcement leverage.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in TN_EXEMPTIONS:
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

    print(f'TN exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in TN_RULES:
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

    print(f'TN rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in TN_TEMPLATES:
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

    print(f'TN templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'TN total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_tn', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
