#!/usr/bin/env python3
"""Build New Mexico Inspection of Public Records Act data: exemptions, rules, and templates.

Covers New Mexico's Inspection of Public Records Act (IPRA), NMSA 1978 § 14-2-1 et seq.
New Mexico has a 15-calendar-day response deadline — the longest statutory deadline of any
state IPRA law. No administrative appeal exists; enforcement is directly in district court.
Civil penalties of $100/day for willful violations plus attorney's fees make it a meaningful
enforcement regime despite the long response window.

Run: python3 scripts/build/build_nm.py
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
# NMSA 1978 § 14-2-1 establishes a general right of inspection. § 14-2-1(A) states
# that "every person has a right to inspect public records." Exemptions are listed
# in § 14-2-1(D)-(E) and in other statutes incorporated by reference. The burden
# of demonstrating any exemption is on the custodian. Courts construe exemptions
# narrowly against the agency.
# =============================================================================

NM_EXEMPTIONS = [
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(1)',
        'exemption_number': '§ 14-2-1(D)(1)',
        'short_name': 'Law Enforcement Records — Pending Investigation',
        'category': 'law_enforcement',
        'description': 'Letters of reference, attorney-client privileged records, and law enforcement records subject to disclosure limitations — including records of active criminal investigations where release would prejudice the investigation or endanger any person.',
        'scope': 'Active criminal investigation records where disclosure would (1) endanger the life or safety of any person, (2) prevent the apprehension of a suspect, (3) compromise an ongoing investigation, or (4) reveal confidential informant identities. Completed investigations do not retain this protection. Incident reports, arrest records, and offense reports documenting the existence of events are generally public regardless of investigative status. Booking records and jail logs are public. The exemption does not cover routine police records about past, completed events.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'active investigation', 'criminal investigation',
            'confidential informant', 'endanger', 'pending prosecution', 'arrest record',
            'offense report', 'police record', 'investigation records',
        ]),
        'counter_arguments': json.dumps([
            'Completed investigations lose exemption protection — once prosecution is concluded or matter is closed, records become public',
            'Arrest records, booking information, and incident reports documenting the basic facts of an event are public regardless of investigation status',
            'The agency must identify a specific harm from disclosure, not merely label records as "investigative"',
            'Factual information in investigative files that does not reveal informant identities or investigative techniques must be segregated and released',
            'Challenge withholding that extends years beyond any plausible active investigation',
            'Body camera footage is a law enforcement record — its withholding requires specific justification under the same analysis',
        ]),
        'notes': 'New Mexico courts strictly construe IPRA exemptions against the agency. The law enforcement exemption does not provide blanket protection for all police files. See Cox v. New Mexico Dep\'t of Pub. Safety, 148 N.M. 139 (Ct. App. 2010). Agencies must apply a record-specific rather than category-wide analysis.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(2)',
        'exemption_number': '§ 14-2-1(D)(2)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Letters of reference and attorney-client privileged communications are exempt from inspection under IPRA. The exemption tracks the common law and statutory attorney-client privilege as applied to government counsel.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege requires: (1) a lawyer-client relationship; (2) a confidential communication; (3) made for the purpose of legal advice. Facts communicated to an attorney remain discoverable even if the communication itself is privileged. Billing records are generally not privileged. Business and policy advice from attorneys is not legal advice and therefore not covered. Waiver occurs when contents are disclosed in public proceedings.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not general business or policy direction',
            'Facts independently known by the agency are not privileged merely because they were relayed to an attorney',
            'Attorney billing records and invoice descriptions are generally public under New Mexico law',
            'Waiver: if the agency disclosed the substance of legal advice in public meetings or documents, the privilege is waived',
            'The privilege belongs to the agency and may be waived by the government entity itself — challenge whether waiver has occurred',
            'Settlement agreements and consent decrees, once executed, are public regardless of the legal advice leading to them',
        ]),
        'notes': 'New Mexico courts apply the attorney-client privilege to government entities under the general evidentiary privilege rules. The privilege is not automatically expanded by the government context — it requires the same elements as the private attorney-client privilege. IPRA\'s narrow construction of exemptions applies with equal force to the attorney-client privilege claim.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(3)',
        'exemption_number': '§ 14-2-1(D)(3)',
        'short_name': 'Tactical Response Plans — Law Enforcement',
        'category': 'safety',
        'description': 'Tactical response plans and similar law enforcement operational security documents are exempt where disclosure would create a specific security risk or compromise the effectiveness of emergency response.',
        'scope': 'Specific operational details of tactical law enforcement response plans, emergency response protocols, and related security documents whose disclosure would enable a person to evade or neutralize law enforcement action. The exemption is narrow — it covers specific tactical details, not general descriptions of police operations, staffing levels, or budget. Policies describing the circumstances under which force may be used are generally public; specific tactical formation plans may not be. Agencies must identify the specific harm that would result from disclosure.',
        'key_terms': json.dumps([
            'tactical response plan', 'law enforcement operations', 'emergency response',
            'security risk', 'SWAT', 'tactical unit', 'operational security',
            'response protocol', 'police operations', 'public safety',
        ]),
        'counter_arguments': json.dumps([
            'General descriptions of department policies, use-of-force standards, and training programs are public',
            'Budget records, staffing levels, and equipment inventories are not operational security documents',
            'Policies governing when and how force may be used are matters of public accountability and are not exempt',
            'Challenge claims that after-action reports and incident reviews are tactical plans',
            'Historical tactical plans from completed incidents with no ongoing application are not genuinely security-sensitive',
        ]),
        'notes': 'This exemption is interpreted narrowly under IPRA\'s strong disclosure mandate. New Mexico courts have rejected broad agency claims that general police records are "tactical" in nature.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(4)',
        'exemption_number': '§ 14-2-1(D)(4)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and privileged or confidential commercial or financial information submitted to a government agency by private parties are exempt from public disclosure to protect legitimate competitive interests.',
        'scope': 'Information submitted by private entities to state or local agencies that: (1) qualifies as a trade secret under applicable law; or (2) constitutes confidential commercial or financial information whose disclosure would cause competitive harm. The submitter must demonstrate that the information actually meets these criteria — a "confidential" label is not sufficient. Government-generated financial records are not trade secrets. Contract prices and amounts paid with public funds are generally public. Agencies must independently evaluate claims and may not simply accept submitter designations.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm',
            'confidential commercial information', 'financial information',
            'competitive advantage', 'business information', 'contract pricing',
        ]),
        'counter_arguments': json.dumps([
            'Amounts paid with public funds under government contracts are public regardless of trade secret claims',
            'The submitter must demonstrate actual competitive harm from disclosure, not merely assert confidentiality',
            'Information required by law to be submitted to the government has reduced expectations of confidentiality',
            'Publicly available information cannot be withheld as a trade secret',
            'Challenge overbroad designations where entire contracts are marked confidential when only specific technical specs qualify',
            'Government-generated analysis of submitted data is not itself a trade secret',
        ]),
        'notes': 'New Mexico courts apply the narrow construction rule to trade secret exemption claims under IPRA. The agency, not the submitter, bears the burden of demonstrating that the specific records qualify. Government expenditure data is uniformly public under the transparency mandate of NMSA 1978 § 14-2-1(A).',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(5)',
        'exemption_number': '§ 14-2-1(D)(5)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical records and mental health records of individuals that are held by government agencies are exempt from public disclosure to protect medical privacy.',
        'scope': 'Medical records, mental health records, psychiatric evaluations, and related health information of identifiable individuals held by government agencies including corrections departments, health and human services agencies, public schools, and public employers. The exemption protects the individual, not the agency — it does not cover agency budget records, contracts with medical providers, or aggregate health statistics. Policy records about public health programs are not personal medical records.',
        'key_terms': json.dumps([
            'medical records', 'mental health records', 'psychiatric records',
            'health information', 'medical privacy', 'protected health information',
            'HIPAA', 'patient records', 'health records', 'medical privacy',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Agency contracts with medical providers and expenditure data are public',
            'Policy documents governing public health programs are not personal medical records',
            'Records about an identified public official\'s fitness for duty may be public in appropriate contexts',
            'Challenge overbroad redactions that remove non-medical contextual information from agency records',
        ]),
        'notes': 'IPRA\'s medical records exemption aligns with HIPAA-protected categories. New Mexico courts have held that this exemption is individual-protective — it does not shield agency operations from scrutiny. See NMSA 1978 § 14-6-1 et seq. (Medical Records Act) for the broader framework.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(6)',
        'exemption_number': '§ 14-2-1(D)(6)',
        'short_name': 'Student Education Records',
        'category': 'privacy',
        'description': 'Student education records protected under the Family Educational Rights and Privacy Act (FERPA) and New Mexico law are exempt from public disclosure.',
        'scope': 'Education records of identified students at public schools and public universities — records that contain personally identifiable information directly linked to a student, including grades, transcripts, disciplinary records, and enrollment status. Aggregate statistics, de-identified data, and records about the institution (rather than individual students) are public. FERPA compliance is mandatory for institutions receiving federal funds. Directory information may be releasable depending on institution policies and student opt-out status.',
        'key_terms': json.dumps([
            'student records', 'FERPA', 'education records', 'student privacy',
            'transcript', 'disciplinary records', 'personally identifiable information',
            'student data', 'enrollment records', 'school records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics about student performance, graduation rates, and demographic data are public',
            'Records about the institution\'s operations — staffing, budgets, discipline policies — are public',
            'De-identified data that cannot be linked to individual students is not a FERPA-protected education record',
            'Directory information (name, enrollment status, major) may be releasable under institutional directory information policies',
            'Records of school officials who are not students are not protected as education records',
        ]),
        'notes': 'FERPA creates a federal framework for student record privacy at institutions receiving federal education funds. New Mexico public school and university records are subject to FERPA. The exemption protects individual students, not institutional operations. NMSA 1978 § 22-2-14 provides additional New Mexico student privacy protections.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(7)',
        'exemption_number': '§ 14-2-1(D)(7)',
        'short_name': 'Deliberative Process — Predecisional Internal Documents',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, intra-agency memoranda, and other predecisional documents reflecting the deliberative process of an agency are conditionally exempt where disclosure would impair the agency\'s deliberative function.',
        'scope': 'Predecisional internal agency documents containing recommendations, opinions on legal or policy questions, and draft materials that reflect the deliberative process. The exemption does NOT cover: (1) purely factual material, even if embedded in a deliberative document; (2) documents that have been adopted as final agency policy; (3) "working law" — the actual standards the agency applies in practice. Factual portions of deliberative documents must be segregated and released. New Mexico courts apply a narrow construction to this exemption consistent with IPRA\'s strong disclosure mandate.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'preliminary draft', 'intra-agency memo',
            'working paper', 'recommendations', 'policy deliberation', 'draft document',
            'internal deliberation', 'agency decision-making',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative documents is not exempt — must be segregated and released',
            'Documents adopted as final agency position are no longer predecisional',
            '"Working law" — standards and criteria the agency actually applies — must be disclosed',
            'Challenge claims that entire documents are deliberative when only conclusion sections qualify',
            'External communications circulated outside the agency typically lose predecisional character',
            'The agency must demonstrate that each withheld document is genuinely predecisional and opinionated, not factual',
        ]),
        'notes': 'New Mexico courts apply the deliberative process exemption narrowly under IPRA. The factual/opinion distinction is critical — factual data does not become deliberative because it appears in a policy memo. The agency bears the burden of establishing the exemption applies to each specific document.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(8)',
        'exemption_number': '§ 14-2-1(D)(8)',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Personnel records of public employees that contain private information — including performance evaluations, medical information, Social Security numbers, and similar personal data — are exempt from public disclosure, though basic employment and compensation data remains public.',
        'scope': 'Private portions of personnel records: medical records, Social Security numbers, home addresses, performance evaluations, disciplinary records (with important exceptions for public accountability), and similar personal data. However, New Mexico law makes public the names, titles, salaries, and general employment status of public employees. Disciplinary records resulting in termination or significant public-facing discipline may be public under the accountability interest. Personnel records of law enforcement officers involved in misconduct are subject to heightened disclosure obligations. The exemption protects the private individual, not the agency.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'performance evaluation',
            'disciplinary records', 'salary', 'public employee', 'employment records',
            'HR records', 'termination records', 'employee privacy',
        ]),
        'counter_arguments': json.dumps([
            'Names, job titles, salaries, and general job classifications of public employees are public under IPRA',
            'Disciplinary records that resulted in suspension, demotion, or termination are public as matters of governmental accountability',
            'Law enforcement officer misconduct records have heightened disclosure obligations following national reforms',
            'Separation agreements, settlement agreements, and payments to departing employees are public',
            'Agency policies, not employee personal data, are what govern the agency — policies are always public',
            'Challenge broad withholding that conceals evidence of systemic misconduct under a personnel privacy claim',
        ]),
        'notes': 'New Mexico courts have balanced employee privacy against the public accountability interest in government employee conduct. The New Mexico Supreme Court has held that disciplinary records of public officials exercising public duties have a reduced privacy expectation. See Board of County Commissioners v. Ogden, 117 N.M. 181 (1994).',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(9)',
        'exemption_number': '§ 14-2-1(D)(9)',
        'short_name': 'Computer Security — Infrastructure Vulnerability Data',
        'category': 'safety',
        'description': 'Records identifying specific computer security vulnerabilities, system architecture details that would enable unauthorized access, and related cybersecurity assessments are exempt to protect critical government infrastructure.',
        'scope': 'Technical details of computer and network security systems for government agencies: specific vulnerability assessments, penetration test results identifying exploitable weaknesses, network architecture diagrams that would facilitate unauthorized access, and similar operational security data. Budget records for IT security programs, general descriptions of security policies, and records about security certifications are public. The exemption requires a specific, articulable security harm — not merely that the records involve IT systems.',
        'key_terms': json.dumps([
            'computer security', 'cybersecurity', 'vulnerability assessment',
            'network security', 'system architecture', 'penetration test',
            'information security', 'critical infrastructure', 'cyber vulnerability',
            'IT security',
        ]),
        'counter_arguments': json.dumps([
            'Budget and expenditure records for IT security programs are public',
            'General descriptions of security certifications and compliance status are public',
            'Policies governing acceptable use of government systems are public',
            'Contracts with security vendors are public (with possible redaction of specific technical specs)',
            'Challenge claims that all IT procurement documents are security-sensitive',
        ]),
        'notes': 'New Mexico\'s cybersecurity exemption follows the narrow construction rule — it covers specific vulnerability data whose disclosure would create an exploitable risk, not all records relating to IT systems. The harm from disclosure must be specific and articulable.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(10)',
        'exemption_number': '§ 14-2-1(D)(10)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related valuation documents prepared by or for a government agency in connection with proposed acquisition or disposal of real property are exempt until the transaction is completed or abandoned.',
        'scope': 'Formal real property appraisals, feasibility studies, and related valuation documents prepared for proposed government acquisition or sale of real estate. The exemption is time-limited — it expires when the transaction is completed, abandoned, or a final condemnation judgment is entered. The purpose is to protect the agency\'s negotiating position, not to create a permanent shield. Post-transaction, all appraisal records are public. The exemption does not cover budget discussions about general property values or informal internal estimates.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'pre-acquisition', 'real property', 'condemnation',
            'land purchase', 'property sale', 'eminent domain',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction completes or is abandoned',
            'Challenge the agency\'s claim that a transaction remains "pending" with no recent activity',
            'Post-transaction appraisals are uniformly public',
            'Budget discussions about general property value ranges are not formal appraisals and are not covered',
            'After a final condemnation judgment, all valuation records are public',
        ]),
        'notes': 'New Mexico\'s pre-acquisition appraisal exemption is temporary by nature. Agencies may not extend it indefinitely by claiming a transaction remains "under consideration." The exemption requires a live, active contemplated transaction.',
    },
    {
        'jurisdiction': 'NM',
        'statute_citation': 'NMSA 1978 § 14-2-1(D)(11)',
        'exemption_number': '§ 14-2-1(D)(11)',
        'short_name': 'Grand Jury Records and Sealed Court Documents',
        'category': 'law_enforcement',
        'description': 'Records of grand jury proceedings and records sealed by court order are exempt from IPRA disclosure, as these are subject to judicial control and confidentiality.',
        'scope': 'Grand jury proceedings, testimony, and documents specifically presented to a grand jury; court records sealed by judicial order. This exemption tracks the judiciary\'s authority over its own proceedings, not agency discretion. Administrative records held by an executive agency that were also provided to a grand jury are not necessarily exempt — the exemption covers the grand jury record, not all agency records that happen to relate to the same subject matter. Court orders sealing records must be specifically reviewed for scope.',
        'key_terms': json.dumps([
            'grand jury', 'sealed records', 'court order', 'grand jury secrecy',
            'judicial seal', 'confidential proceedings', 'grand jury testimony',
            'sealed indictment', 'court-ordered confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Agency records that were not specifically presented to a grand jury are not exempt merely because the same subject matter was investigated',
            'The seal order must be reviewed — it may be narrower than the agency claims',
            'After indictment and during public trial proceedings, grand jury-related materials often become public',
            'Challenge claims that administrative investigation records are "grand jury records" just because they were later turned over to prosecutors',
        ]),
        'notes': 'Grand jury secrecy is a procedural rule governed by New Mexico Rule of Criminal Procedure 5-203. IPRA incorporates the exemption by reference to judicial confidentiality. Agencies cannot independently designate records as "grand jury materials" — there must be actual grand jury proceedings involving the specific records.',
    },
]

# =============================================================================
# RULES
# New Mexico IPRA, NMSA 1978 § 14-2-1 et seq.
# The 15-calendar-day response deadline (§ 14-2-8) is the longest of any state
# IPRA statute. No administrative appeal exists — district court enforcement is
# the sole formal remedy. $0.25/page copy fee. $100/day civil penalty for willful
# violations. Attorney's fees for prevailing requesters.
# =============================================================================

NM_RULES = [
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '15',
        'day_type': 'calendar',
        'statute_citation': 'NMSA 1978 § 14-2-8(D)',
        'notes': 'New Mexico has the longest statutory response deadline of any state IPRA law: 15 calendar days. The custodian must permit inspection of public records during regular business hours or mail copies within 15 calendar days after receiving a written request. The 15-day period begins on the date the written request is received by the custodian. If inspection is not permitted within 15 days, the request is deemed denied. A "response" that acknowledges receipt but does not produce records or explain a valid exemption does not satisfy the deadline.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'acknowledgment_required',
        'param_value': 'yes_with_estimate',
        'day_type': 'calendar',
        'statute_citation': 'NMSA 1978 § 14-2-8(D)',
        'notes': 'While the IPRA statute requires response within 15 calendar days, best practice and many agency rules require an acknowledgment within a shorter period confirming receipt. Some agencies acknowledge within 3-5 business days per internal policy. The 15-day calendar day window for actual production is the binding statutory deadline. If the agency cannot produce all records within 15 days, it must explain why and provide a schedule for production.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'written_request_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-8(A)',
        'notes': 'New Mexico IPRA requires a written request to trigger the formal 15-day response clock. Oral requests are permissible at common law but do not trigger the statutory response timeline. Written requests should be directed to the "custodian" of records — which IPRA defines (§ 14-2-6(B)) as the person responsible for maintaining a public body\'s records. Requesters should identify the public body and the custodian clearly, as misdirected requests may restart the clock.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-9(A)',
        'notes': 'New Mexico agencies may charge a reasonable fee not to exceed $0.25 per page for paper copies. For electronic records, the fee is the actual cost of reproduction, which is often nominal. Agencies may not charge for the staff time spent locating, reviewing, or redacting records — only the actual reproduction cost. A fee that substantially exceeds the actual cost of reproduction may be challenged as an unlawful barrier to access. Agencies should not require prepayment for requests under $25.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'fee_cap',
        'param_key': 'search_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-9',
        'notes': 'New Mexico IPRA does not authorize agencies to charge for staff time spent searching for, reviewing, or redacting records. Only actual reproduction costs (up to $0.25/page for paper) are permissible. Agencies that add "research fees," "processing fees," or "staff time" charges are imposing fees not authorized by the statute. Requesters should challenge such charges by citing § 14-2-9 and noting that the statute authorizes only reproduction costs.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-9',
        'notes': 'IPRA does not expressly mandate fee waivers for any requester category, but agencies have discretion to waive fees. The New Mexico Attorney General\'s office has indicated that fee waivers are appropriate when disclosure primarily benefits the public rather than the requester\'s private interest. Requesters seeking fee waivers should articulate the public interest served by the disclosure. For electronic records, the actual reproduction cost is typically zero, making the fee issue moot.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-12',
        'notes': 'New Mexico IPRA has NO formal administrative appeal mechanism. There is no agency head review, no state ombudsman, and no administrative tribunal for IPRA denials. A requester denied access — or whose request is not answered within 15 calendar days — must go directly to district court under NMSA 1978 § 14-2-12. The deemed-denial rule (no response within 15 days = denial) triggers the right to seek judicial enforcement. The New Mexico Attorney General\'s office can informally assist with IPRA disputes but has no binding enforcement authority outside of its own records.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-12',
        'notes': 'A requester denied access (including a deemed denial after 15 calendar days without response) may file an action in the district court of the county in which the records are maintained or in Santa Fe County. The court shall conduct a hearing and issue an order within a reasonable time. The court may review withheld records in camera. Judicial review is de novo — the court does not defer to the agency\'s withholding determination. There is no explicit statute of limitations, but prompt filing is advisable.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_willful_violation',
        'param_value': '$100 per day',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-12(D)',
        'notes': 'Courts may impose a civil penalty of $100 per day for each day a custodian willfully refused or failed to provide access to public records without justification. The penalty accrues from the date the district court finds the refusal was unjustified. "Willful" requires that the custodian knew or should have known the records were subject to disclosure. The penalty is a significant deterrent for agencies that routinely deny access without adequate justification. The civil penalty is in addition to attorney fees.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-12(C)',
        'notes': 'Courts SHALL award reasonable attorney fees and costs to a requester who substantially prevails in an IPRA enforcement action. The fee-shifting provision is mandatory, not discretionary — a court that finds the agency wrongfully withheld records must award fees unless special circumstances exist. This makes IPRA enforcement economically viable for requesters and their attorneys. Attorney fees are cumulative with the $100/day civil penalty.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-8',
        'notes': 'IPRA does not require requesters to identify themselves, state a purpose, or demonstrate standing. The right to inspect public records belongs to "every person" under § 14-2-1(A). Anonymous requests are valid. Some agencies request contact information for delivery purposes, but providing it must be voluntary. An agency that conditions access on requester identity or stated purpose is violating IPRA.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-1(C)',
        'notes': 'When a record contains both exempt and non-exempt information, the custodian must redact the exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is improper. The custodian bears the burden of demonstrating that specific portions of records are exempt — and must produce everything that is not specifically covered by an applicable exemption. New Mexico courts have consistently required segregation and partial production.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'NMSA 1978 § 14-2-1(A); § 14-2-12(A)',
        'notes': 'The presumption under IPRA is that all government records are public. The burden of demonstrating that any record is exempt falls entirely on the custodian, not the requester. § 14-2-12(A) states that in an enforcement action, the burden of proof is on the custodian to establish an applicable exemption. Record-specific, not category-wide, justification is required. General assertions that records "fall within" an exemption category are insufficient.',
    },
    {
        'jurisdiction': 'NM',
        'rule_type': 'initial_response',
        'param_key': 'deemed_denial_rule',
        'param_value': 'no_response_within_15_days',
        'day_type': 'calendar',
        'statute_citation': 'NMSA 1978 § 14-2-8(D)',
        'notes': 'If a custodian does not permit inspection or mail copies within 15 calendar days of receiving a written request, the request is deemed denied. A deemed denial triggers the requester\'s right to seek enforcement in district court without waiting for a formal written denial. This is a critical procedural right — requesters should calendar the 15-day deadline and file suit promptly if the deadline passes without response or production.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NM_TEMPLATES = [
    {
        'jurisdiction': 'NM',
        'record_type': 'general',
        'template_name': 'General New Mexico IPRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Inspection of Public Records Act Request — NMSA 1978 § 14-2-1 et seq.

Dear Custodian of Public Records:

Pursuant to the New Mexico Inspection of Public Records Act (IPRA), NMSA 1978 § 14-2-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format where available, to minimize reproduction costs.

I am willing to pay reasonable reproduction fees consistent with NMSA 1978 § 14-2-9, which limits charges to the actual cost of reproduction not to exceed $0.25 per page for paper copies. I am not willing to pay for staff time, research time, or any fee not authorized by statute. If reproduction costs will exceed ${{fee_limit}}, please notify me before proceeding.

Under NMSA 1978 § 14-2-1(A), all public records are presumptively open to inspection by every person. Under § 14-2-12(A), the burden of establishing any exemption rests on the custodian. Under § 14-2-1(C), all nonexempt, reasonably segregable portions of any record must be released.

If any records or portions are withheld, please: (1) identify each withheld record with sufficient description; (2) cite the specific statutory exemption under NMSA 1978 § 14-2-1(D) or other applicable law; (3) explain how the exemption applies to the specific record; and (4) confirm that nonexempt, segregable portions have been released.

Under NMSA 1978 § 14-2-8(D), inspection must be permitted or copies mailed within 15 calendar days of receipt of this written request. Failure to respond within 15 calendar days constitutes a deemed denial, which I will treat as authorizing immediate court action under § 14-2-12.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that reproduction fees be waived for this request. While IPRA does not mandate a fee waiver, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records concern {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. For records provided electronically, the actual reproduction cost is zero under § 14-2-9.

The New Mexico Attorney General has recognized that fee waivers are appropriate when disclosure primarily serves the public interest.''',
        'expedited_language': '''I request expedited processing of this IPRA request. Timely production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if any clarification would allow faster processing.

Note: The 15-calendar-day statutory deadline under NMSA 1978 § 14-2-8(D) already applies, and I will calendar that deadline carefully.''',
        'notes': 'General-purpose New Mexico IPRA template. Key NM features: (1) 15 calendar days — the longest statutory deadline of any state, running from receipt of written request; (2) no administrative appeal — go directly to district court under § 14-2-12 if denied or no response within 15 days; (3) deemed denial rule — silence = denial triggering court jurisdiction; (4) $100/day civil penalty for willful violations; (5) mandatory attorney fees for prevailing requesters; (6) $0.25/page copy fee maximum, no staff time charges authorized; (7) burden of proof on agency for all claimed exemptions. Reference "IPRA" and cite NMSA 1978 § 14-2-1, not "FOIA."',
    },
    {
        'jurisdiction': 'NM',
        'record_type': 'law_enforcement',
        'template_name': 'New Mexico IPRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: IPRA Request — Law Enforcement Records, NMSA 1978 § 14-2-1 et seq.

Dear Custodian of Public Records:

Pursuant to the New Mexico Inspection of Public Records Act, NMSA 1978 § 14-2-1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch logs and Computer-Aided Dispatch (CAD) records
- Written communications relating to the above incident or subject

Regarding any claimed exemption under § 14-2-1(D)(1): New Mexico IPRA does not permit blanket withholding of law enforcement records. The exemption for active investigations requires a specific showing that disclosure would: (1) endanger a specific person; (2) prevent apprehension of a named suspect; (3) compromise an ongoing investigation with respect to identified records; or (4) reveal a confidential informant. General claims that records are "investigative" are insufficient.

[If matter appears concluded:] If no prosecution is pending or investigation is active, the § 14-2-1(D)(1) investigation exemption does not apply. Completed investigation files are public records. Please apply this standard.

Under § 14-2-1(A), all public records are presumptively open. Under § 14-2-12(A), the burden is on the custodian to establish each exemption. Under § 14-2-1(C), nonexempt, segregable portions of withheld records must be released.

Reproduction fees under § 14-2-9 are acceptable up to ${{fee_limit}}. Staff time is not a chargeable cost under IPRA.

Under § 14-2-8(D), please respond within 15 calendar days of receipt of this written request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that reproduction fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement conduct. Electronic delivery incurs no reproduction cost under § 14-2-9. A fee waiver is appropriate given the significant public interest in this matter.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. The 15-calendar-day deadline under § 14-2-8(D) already applies, and I will calendar that deadline. Any earlier production is welcome.''',
        'notes': 'New Mexico law enforcement IPRA template. NM-specific features: (1) § 14-2-1(D)(1) exemption is narrow — requires specific harm per record for active investigations only; (2) completed investigations are public; (3) $0.25/page cap, no staff time charges; (4) 15 calendar days to respond — the longest of any state; (5) no administrative appeal — district court under § 14-2-12 is the sole formal remedy; (6) $100/day civil penalty for willful violations plus mandatory attorney fees. The deemed denial rule (§ 14-2-8(D)) means silence after 15 days triggers immediate court jurisdiction.',
    },
    {
        'jurisdiction': 'NM',
        'record_type': 'personnel',
        'template_name': 'New Mexico IPRA Request — Public Employee Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: IPRA Request — Public Employee Records, NMSA 1978 § 14-2-1 et seq.

Dear Custodian of Public Records:

Pursuant to the New Mexico Inspection of Public Records Act, NMSA 1978 § 14-2-1 et seq., I request copies of the following records relating to public employees:

{{description_of_records}}

Employee(s) / position(s) at issue: {{employee_or_position}}
Date range: {{date_range_start}} through {{date_range_end}}

This request includes, but is not limited to:
- Name, job title, job classification, and salary of each identified employee
- Records of disciplinary actions, including any resulting in suspension, demotion, or termination
- Separation agreements and severance payments to departing employees
- Settlement agreements resolving complaints against agency employees
- Contracts and agreements with individual contractors performing public functions

Under New Mexico law, the names, titles, salaries, and general employment status of public employees are public records regardless of any general personnel privacy exemption. The personnel exemption under § 14-2-1(D)(8) does not protect basic employment and compensation data, nor does it shield evidence of serious misconduct from public scrutiny.

I specifically do not request medical records, Social Security numbers, home addresses, or other personal data protected by statute. I do request all records relating to the exercise of public duties by these employees.

Under § 14-2-8(D), please respond within 15 calendar days of receipt of this written request. I am willing to pay reproduction fees up to ${{fee_limit}} at the § 14-2-9 rate of up to $0.25 per page for paper copies.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. These records concern the conduct of public employees in the exercise of official duties — a core matter of government accountability. Electronic delivery is preferred and incurs no reproduction cost. A waiver is appropriate given the public interest served by this disclosure.''',
        'expedited_language': '''I request prompt processing. These records are time-sensitive because {{urgency_explanation}}. I need them by {{needed_by_date}}. The statutory 15-calendar-day deadline applies, and I will calendar it accordingly.''',
        'notes': 'New Mexico public employee records template. The personnel privacy exemption (§ 14-2-1(D)(8)) does not protect core employment data (names, salaries, titles) or records of serious misconduct. New Mexico courts have recognized a reduced privacy expectation for public officials regarding their official conduct. Disciplinary records resulting in significant adverse action are generally public. Settlement agreements paid with public funds are public. This template is designed to anticipate and preempt overbroad privacy claims.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in NM_EXEMPTIONS:
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

    print(f'NM exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in NM_RULES:
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

    print(f'NM rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in NM_TEMPLATES:
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

    print(f'NM templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'NM total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nm', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
