#!/usr/bin/env python3
"""Build Maryland Public Information Act data: exemptions, rules, and templates.

Covers Maryland's Public Information Act (MPIA), Md. Code Gen. Prov. § 4-101
et seq. (formerly Art. 76A and Md. Code Ann., State Gov't § 10-611 et seq.).
Key features: 10-business-day initial response deadline (30 days when third-party
notice required), State Public Information Act Compliance Board review option,
$0.25/page standard copy rate, no attorney's fees provision (a notable weakness),
and a fee waiver available for indigent requesters. Maryland courts construe
exemptions strictly against agencies.

Run: python3 scripts/build/build_md.py
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
# Maryland PIA exemptions are codified at Md. Code Gen. Prov. § 4-301 through
# § 4-344. The Act creates a presumption of openness — the custodian bears the
# burden of showing that withholding is authorized. Maryland courts apply a
# strict construction against withholding. The 2015 reforms created the
# Compliance Board as a free adjudicatory alternative to court.
# =============================================================================

MD_EXEMPTIONS = [
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-301',
        'exemption_number': 'MPIA § 4-301',
        'short_name': 'Confidential by Law — Other Statute or Regulation',
        'category': 'statutory',
        'description': 'Records that are specifically declared confidential by another Maryland statute or regulation, or by federal law, are required to be withheld to the extent mandated by the applicable law.',
        'scope': 'Records specifically designated confidential by another Maryland statute, state regulation, or federal law. Examples include: income tax returns under Md. Code Tax-Gen. § 13-202; child protective services records under Md. Code Fam. Law § 5-707; Medicaid beneficiary records under federal law; and motor vehicle records under the Driver\'s Privacy Protection Act (DPPA). The exemption only applies to the extent required by the other law — if the other law has exceptions that permit disclosure, those exceptions apply. The custodian must identify the specific statute or regulation and explain how it mandates withholding.',
        'key_terms': json.dumps([
            'confidential by law', 'statutory confidentiality', 'federal confidentiality',
            'tax return', 'child protective services', 'DPPA', 'mandated confidentiality',
            'protected by another statute', 'regulatory confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'The custodian must identify the specific statute or regulation — a general "confidential by law" claim is insufficient',
            'The other statute\'s exceptions apply — if there is an exception for public interest disclosure, it should be invoked',
            'Aggregate and anonymized data from confidential records are generally public',
            'Administrative records of agencies that maintain confidential records are public',
            'Challenge whether the specific record actually falls within the other statute\'s scope',
        ]),
        'notes': 'Md. Code Gen. Prov. § 4-301 is the mandatory confidentiality provision — it applies when another law requires withholding. This is distinct from § 4-343 (permissive withholding). The custodian must demonstrate that the other law mandates (not merely permits) withholding of the specific record requested.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-305',
        'exemption_number': 'MPIA § 4-305',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Personnel records of individual state employees, including performance evaluations, disciplinary files, and similar employment records, are exempt from disclosure. However, salary information, job titles, and official employment information are public.',
        'scope': 'Personnel records of individual government employees including performance evaluations, disciplinary proceedings, medical records, and similar documents relating to an individual\'s employment. Maryland law expressly makes public: the name, position, salary, and employment dates of State employees. The exemption does not protect official actions taken against employees that have public safety implications. Maryland courts have held that disciplinary records for public employees involved in misconduct affecting the public may be accessible, balancing privacy against the public interest.',
        'key_terms': json.dumps([
            'personnel record', 'performance evaluation', 'disciplinary record',
            'employment file', 'state employee', 'salary', 'public employee privacy',
            'human resources record', 'personnel file',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, salary, and employment dates of state employees are expressly public',
            'Final disciplinary actions involving public safety or misconduct may be public',
            'Official actions taken against employees in their official capacity are distinguishable from purely personal personnel matters',
            'The Compliance Board has held that the exemption does not protect all records mentioning employee performance',
            'Challenge whether specific records are "personnel records" vs. operational records that happen to involve employees',
        ]),
        'notes': 'Maryland\'s personnel record exemption requires balancing individual privacy against public interest. The Compliance Board has developed significant guidance on what constitutes a personnel record versus an operational record. In 2020, Maryland enacted legislation expanding access to police disciplinary records.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-307',
        'exemption_number': 'MPIA § 4-307',
        'short_name': 'Medical and Psychological Records',
        'category': 'privacy',
        'description': 'Medical records, psychological records, and related health information that would constitute a clearly unwarranted invasion of personal privacy are exempt from MPIA disclosure.',
        'scope': 'Individually identifiable medical, psychological, and health records maintained by government agencies including health departments, correctional facilities, public hospitals, and other government health providers. Applies the "clearly unwarranted invasion of personal privacy" standard. Aggregate public health statistics, epidemiological data, and de-identified health data are not covered. Agency health policy, budget, and program administration records are public. HIPAA applies independently to covered entities.',
        'key_terms': json.dumps([
            'medical record', 'psychological record', 'health information', 'patient privacy',
            'HIPAA', 'individually identifiable', 'personal privacy', 'health record',
            'mental health record', 'public health record',
        ]),
        'counter_arguments': json.dumps([
            'The privacy standard requires a "clearly unwarranted invasion" — a high bar for public employees\' job-related health information',
            'Aggregate and de-identified public health data are not covered',
            'Agency health program administration records are public',
            'Fitness-for-duty information for employees in safety-sensitive positions may be subject to reduced privacy protection',
        ]),
        'notes': 'Maryland courts apply the "clearly unwarranted invasion of personal privacy" standard consistently with the federal Privacy Act framework. The Compliance Board has held that fitness-for-duty evaluations for law enforcement officers may have reduced privacy protection given the public safety implications.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-311',
        'exemption_number': 'MPIA § 4-311',
        'short_name': 'Investigative Files — Law Enforcement and Prosecution',
        'category': 'law_enforcement',
        'description': 'Law enforcement investigative files — including information that would identify confidential informants, reveal investigative techniques, interfere with pending prosecutions, or endanger safety — are exempt from mandatory disclosure.',
        'scope': 'Records compiled by law enforcement or prosecutorial agencies for the purpose of investigating and prosecuting crimes, where disclosure would: (1) identify confidential informants; (2) reveal investigative techniques not otherwise generally known; (3) endanger the life or safety of a person; (4) cause a criminal defendant to escape prosecution; or (5) deprive a person of the right to a fair trial. Once prosecution concludes, the exemption weakens significantly. Incident reports, arrest records, and booking information are public regardless of investigation status. Maryland courts require specific, record-by-record justification for withholding.',
        'key_terms': json.dumps([
            'investigative file', 'law enforcement investigation', 'confidential informant',
            'investigative technique', 'pending prosecution', 'criminal investigation',
            'police investigation record', 'prosecution file', 'investigation records',
        ]),
        'counter_arguments': json.dumps([
            'Incident reports, arrest records, and charging documents are public regardless of investigation status',
            'Records of completed investigations and concluded prosecutions are generally public',
            'The custodian must make a specific, record-by-record showing of harm — generic "investigation ongoing" claims are insufficient',
            'Factual information not implicating any enumerated harm must be segregated and released',
            'Maryland courts require specific evidence of harm, not speculative risks',
            'The Compliance Board scrutinizes broad law enforcement exemption claims carefully',
        ]),
        'notes': 'Maryland\'s law enforcement exemption is among the most litigated MPIA provisions. The Compliance Board has consistently required specific harm documentation for each withheld record. In 2021, the Maryland General Assembly enacted the Anton\'s Law (effective October 1, 2021) expanding access to police disciplinary records, including Internal Affairs investigation records for sustained misconduct.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-312',
        'exemption_number': 'MPIA § 4-312',
        'short_name': 'Inter-Agency and Intra-Agency Documents — Deliberative Process',
        'category': 'deliberative',
        'description': 'Memoranda, letters, and other documents — including recommendations, opinions, and advice — exchanged within or between governmental units as part of the deliberative process in developing policies or making decisions are exempt to the extent they contain advisory opinions and recommendations.',
        'scope': 'Predecisional communications within or between government agencies that reflect the deliberative process of policy development. The exemption protects advisory opinions, recommendations, and intra-agency deliberations before final decisions. It does NOT protect: (1) purely factual material; (2) final decisions and adopted policies; (3) working law — standards agencies actually apply; or (4) documents that have been circulated outside the agency. Maryland courts and the Compliance Board apply the standard deliberative process framework: the document must be predecisional AND deliberative. The factual/opinion distinction is critical.',
        'key_terms': json.dumps([
            'deliberative process', 'inter-agency memorandum', 'intra-agency memorandum',
            'predecisional', 'advisory opinion', 'recommendation', 'policy deliberation',
            'draft', 'working paper', 'staff recommendation',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released',
            'Once a recommendation or draft is adopted as final agency policy, the exemption does not apply',
            '"Working law" — criteria and standards agencies actually use — must be disclosed even if in internal documents',
            'Documents widely circulated outside the agency may lose their predecisional character',
            'Maryland courts require that each claimed document be both predecisional AND deliberative — meeting only one criterion is insufficient',
            'Challenge blanket withholding of entire documents when only specific recommendation sections qualify',
        ]),
        'notes': 'Maryland\'s deliberative process exemption is codified at § 4-312 and closely tracks the federal deliberative process privilege. The Compliance Board has issued significant guidance distinguishing factual from deliberative content. The "working law" exception is particularly important in Maryland administrative law practice.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-313',
        'exemption_number': 'MPIA § 4-313',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and confidential commercial or financial information submitted by a private entity to a government custodian are exempt from mandatory MPIA disclosure when disclosure would result in substantial competitive harm.',
        'scope': 'Commercially valuable information submitted by private parties to government agencies where: (1) the information constitutes a trade secret under Maryland\'s Uniform Trade Secrets Act; (2) disclosure would cause substantial competitive harm to the submitter; and (3) the submitter made reasonable efforts to maintain secrecy. Government-generated records do not qualify. Contract prices and amounts paid with public funds are generally public. The competitive harm must be substantial — speculative or minor harm is insufficient. Agencies must independently evaluate trade secret claims.',
        'key_terms': json.dumps([
            'trade secret', 'competitive harm', 'confidential commercial information',
            'financial information', 'proprietary data', 'UTSA', 'substantial competitive harm',
            'private entity submission', 'commercial secrecy',
        ]),
        'counter_arguments': json.dumps([
            'Maryland requires "substantial" competitive harm — speculative or minor competitive impacts are insufficient',
            'Contract prices and amounts paid with public funds are public regardless of trade secret designations',
            'The agency must independently evaluate the claim — it cannot simply defer to vendor designations',
            'Publicly available information cannot qualify as a trade secret',
            'Challenge the adequacy of the submitter\'s secrecy measures',
            'Information required by law to be submitted has reduced secrecy expectations',
        ]),
        'notes': 'Maryland\'s trade secret exemption requires a showing of "substantial" competitive harm — a higher standard than mere competitive disadvantage. The Compliance Board and Maryland courts have consistently held that public contract amounts are public regardless of vendor claims. The independent agency evaluation requirement prevents agencies from rubber-stamping vendor designations.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-320',
        'exemption_number': 'MPIA § 4-320',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared by or for a custodian in connection with the acquisition or sale of real property are exempt until the transaction is completed or withdrawn.',
        'scope': 'Formal property appraisals, feasibility studies, and related valuation documents prepared in connection with a government body\'s acquisition or sale of real estate. The exemption is time-limited — it expires automatically when the transaction closes or is abandoned. It protects the government\'s negotiating position. Internal estimates and budget discussions about property values may not qualify as formal appraisals. Post-transaction, all appraisal records are public.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property valuation', 'property acquisition',
            'pre-acquisition appraisal', 'negotiating position', 'real property',
            'condemnation appraisal', 'feasibility study',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction closes or is abandoned — post-transaction records are public',
            'Challenge claims that an acquisition remains "pending" after extended inactivity',
            'Informal budget estimates and internal discussion documents may not qualify as formal appraisals',
            'After final condemnation judgment, all valuation records are public',
        ]),
        'notes': 'Maryland\'s pre-acquisition appraisal exemption is narrow and time-limited. Maryland courts have consistently held that it applies only to formal appraisal documents, not to general internal discussions about property value. Post-transaction access is absolute.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-328',
        'exemption_number': 'MPIA § 4-328',
        'short_name': 'Student Records — Educational Privacy',
        'category': 'privacy',
        'description': 'Student education records at Maryland public schools and universities, protected by FERPA and incorporated into Maryland\'s MPIA framework, are exempt from mandatory disclosure.',
        'scope': 'Individually identifiable education records of students at Maryland public schools and universities, consistent with FERPA (20 U.S.C. § 1232g). Covers transcripts, disciplinary records, financial aid records, and other records directly related to individual students. Does not cover directory information unless the student opted out, aggregate statistical data, or school administrative and policy records. Faculty and staff records are not student records.',
        'key_terms': json.dumps([
            'student record', 'FERPA', 'education record', 'student privacy',
            'directory information', 'student transcript', 'student disciplinary record',
            'school record', 'personally identifiable student information',
        ]),
        'counter_arguments': json.dumps([
            'Directory information is public unless the student opted out under FERPA',
            'Aggregate data about student populations, outcomes, and graduation rates is public',
            'School administrative, policy, and budget records are public',
            'Properly de-identified aggregate data about incidents involving students is public',
            'Faculty and staff records are not student records',
        ]),
        'notes': 'FERPA applies federally to all Maryland public schools and universities receiving federal funding. Maryland\'s MPIA exemption works in conjunction with FERPA\'s requirements. Both create a strong presumption against disclosure of individual student records, subject to FERPA\'s enumerated exceptions.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-339',
        'exemption_number': 'MPIA § 4-339',
        'short_name': 'Security Information — Critical Infrastructure',
        'category': 'safety',
        'description': 'Records containing specific technical security vulnerabilities, emergency response procedures with security-sensitive details, and related information whose disclosure would endanger critical infrastructure or public safety are exempt.',
        'scope': 'Specific technical details of security systems, vulnerability assessments identifying exploitable weaknesses, and detailed emergency protocols for critical infrastructure. The exemption targets information that would actually help a bad actor — not general security policy, budget documents, or administrative records. Agencies must show that disclosure would specifically endanger security, not merely that the records relate to security. After-action reports focused on policy improvements rather than specific vulnerabilities are generally public.',
        'key_terms': json.dumps([
            'security vulnerability', 'critical infrastructure', 'security plan',
            'vulnerability assessment', 'emergency response procedure', 'physical security',
            'facility security', 'cybersecurity', 'security protocol',
        ]),
        'counter_arguments': json.dumps([
            'General emergency management policy and procedures are public',
            'Security program budgets and staffing levels are public',
            'After-action reports focusing on policy improvements are public',
            'Challenge broad security classifications that cover administrative records',
            'The agency must show specific harm from disclosure, not a generalized security concern',
        ]),
        'notes': 'Maryland\'s security exemption was strengthened after the September 11 attacks and further refined by the Compliance Board. The Board has consistently required specific harm justification rather than accepting broad security designations.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-344',
        'exemption_number': 'MPIA § 4-344',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege — including confidential legal advice from government attorneys — and attorney work product prepared in anticipation of litigation are exempt from MPIA disclosure.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining or providing legal advice (attorney-client privilege), and documents prepared by attorneys in anticipation of specific litigation (work product). The attorney-client privilege requires that communications be for legal advice (not policy or business guidance), maintained in confidence, and not waived. Billing records and retainer agreements are generally not privileged. The work product doctrine requires a specific nexus to anticipated litigation.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'privileged communication',
            'in anticipation of litigation', 'government attorney', 'legal opinion',
            'attorney work product', 'confidential legal communication',
        ]),
        'counter_arguments': json.dumps([
            'Communications for policy or business advice (not legal advice) are not privileged',
            'Billing records and retainer agreements are generally not privileged',
            'Waiver occurs when advice is disclosed in public proceedings or to non-essential parties',
            'Work product requires anticipation of specific litigation — speculative future litigation is insufficient',
            'Facts underlying legal advice are not privileged — only attorney analysis',
            'The Compliance Board has required privilege logs identifying each withheld document',
        ]),
        'notes': 'Maryland recognizes attorney-client privilege and work product protection for government entities under the MPIA. The Compliance Board requires custodians to provide privilege logs for claimed attorney-client and work product records. Maryland courts apply the common-law privilege framework to government attorneys consistently with federal common law.',
    },
    {
        'jurisdiction': 'MD',
        'statute_citation': 'Md. Code Gen. Prov. § 4-343',
        'exemption_number': 'MPIA § 4-343',
        'short_name': 'Permissive Withholding — Unwarranted Privacy Invasion',
        'category': 'privacy',
        'description': 'Even where no specific exemption applies, a custodian may deny access to a public record when disclosure would constitute a "clearly unwarranted invasion of personal privacy," balancing the public\'s right to know against the individual\'s privacy interest.',
        'scope': 'A catch-all permissive exemption allowing custodians to withhold records not covered by specific exemptions when disclosure would constitute a clearly unwarranted invasion of personal privacy. The "clearly unwarranted" standard requires that the privacy harm substantially outweigh the public interest in disclosure. For public employees acting in their official capacity, this standard is rarely met. For private individuals\' personal information, the standard is more easily satisfied. The balancing test weighs: nature of the information, public vs. private status of the subject, public benefit of disclosure, and potential for harm.',
        'key_terms': json.dumps([
            'personal privacy', 'clearly unwarranted invasion', 'privacy balancing',
            'privacy interest', 'public benefit', 'catch-all privacy exemption',
            'permissive withholding', 'personal information', 'privacy vs. transparency',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" — a high bar that frequently fails for public employees\' official conduct',
            'Public employees acting in their official capacity have a reduced privacy expectation',
            'The public benefit of disclosure must be weighed against the privacy harm — accountability concerns routinely outweigh privacy for official records',
            'Information already in the public domain cannot support a privacy exemption claim',
            'Aggregate and de-identified information does not implicate personal privacy',
        ]),
        'notes': 'Section 4-343 is Maryland\'s general privacy balancing provision. The Compliance Board has developed an extensive body of guidance on the balancing test. The "clearly unwarranted" standard is consistently applied to mean that privacy must substantially outweigh the public interest — a high bar for public employee official conduct.',
    },
]

# =============================================================================
# RULES
# Maryland PIA, Md. Code Gen. Prov. § 4-101 et seq.
# Key features: 10-business-day initial response deadline (30 days when
# third-party notice required), Compliance Board review as free alternative
# to court, $0.25/page standard copy rate, no attorney's fees provision
# (significant weakness), fee waiver for indigent requesters.
# =============================================================================

MD_RULES = [
    {
        'jurisdiction': 'MD',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'Md. Code Gen. Prov. § 4-203(a)',
        'notes': 'Maryland custodians must respond to MPIA requests within 10 business days of receiving the request. This is longer than many states. Within 10 business days, the custodian must either: (1) produce the records; (2) grant inspection; (3) deny the request with specific reasons; or (4) invoke the extended deadline for third-party notification. The 10-business-day clock begins when the request is actually received by the appropriate custodian. Requests directed to the wrong agency are not deemed received until forwarded to the correct custodian.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'initial_response',
        'param_key': 'third_party_notice_extended_deadline_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': 'Md. Code Gen. Prov. § 4-203(b)',
        'notes': 'When a third party submitted the records to the custodian and may have a privacy or confidentiality interest in them, Maryland allows the custodian to extend the response deadline to 30 calendar days from receipt of the request. This extended deadline applies when the custodian must notify the third party and allow them an opportunity to object to disclosure. The third-party notice requirement is common for commercial trade secret claims and personnel records submitted by contractors. Custodians must notify the requester promptly when invoking the extended deadline and explain the reason.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-206(b)',
        'notes': 'Maryland custodians may charge a fee not exceeding $0.25 per page for standard paper copies. For electronic records, custodians may charge the actual cost of creating and transferring the records, which is often minimal. Maryland also permits custodians to charge for staff time spent searching for and preparing records — this is a significant cost element that distinguishes Maryland from states with stricter fee limits. The fee must be "reasonable" and reflect actual costs. Custodians must provide an advance cost estimate before charging fees.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_charges_allowed',
        'param_value': 'yes_reasonable_fee',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-206(b)',
        'notes': 'Maryland custodians may charge a "reasonable fee" for staff time spent searching, reviewing, and preparing records. Unlike states that prohibit staff time charges (e.g., New Jersey), Maryland permits them as long as they reflect actual costs. Custodians should use the hourly rate of staff actually performing the work. Requesters can challenge fees as unreasonable before the Compliance Board. The Compliance Board has found some fee calculations excessive and ordered reductions.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_indigent',
        'param_value': 'available_for_indigent_requesters',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-206(e)',
        'notes': 'Maryland provides a fee waiver for indigent requesters — individuals who cannot afford the fees. The waiver is mandatory (not discretionary) once the requester establishes indigency. Documentation of financial need may be required. Maryland also permits custodians to waive fees at their discretion for other requesters, particularly for requests serving a public interest, but this is not mandatory. Journalists, nonprofits, and academic researchers should request fee waivers based on public interest even if they do not qualify as indigent.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary_public_interest',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-206(e)',
        'notes': 'Beyond the mandatory waiver for indigent requesters, Maryland custodians have discretion to waive fees for requests serving the public interest, even for non-indigent requesters. Factors supporting discretionary waivers: journalistic or academic purpose, public benefit of disclosure, absence of commercial purpose, and the requester\'s demonstrated inability to pay even if not technically indigent. The Compliance Board has encouraged agencies to exercise discretion liberally for public interest requests.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'appeal_deadline',
        'param_key': 'compliance_board_complaint_deadline_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': 'Md. Code Gen. Prov. § 4-1B-04',
        'notes': 'A requester who is denied access may file a complaint with the Maryland State Public Information Act Compliance Board within 30 calendar days of the denial. The Compliance Board, created by the 2015 MPIA reforms, provides free adjudication of MPIA disputes. The Board can order disclosure, but cannot award attorney fees — a significant limitation. Board proceedings are less formal than court, faster, and free. The Board can also mediate disputes. For large or complex cases where attorney fees may be warranted, court remains the preferred forum. The Board\'s decisions are subject to judicial review.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'appeal_deadline',
        'param_key': 'circuit_court_action_available',
        'param_value': 'yes_alternative_to_compliance_board',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-362',
        'notes': 'In addition to Compliance Board complaints, requesters may file an action in Maryland circuit court to compel disclosure under Md. Code Gen. Prov. § 4-362. Circuit court proceedings are more formal than Compliance Board proceedings but allow broader relief. Critically, Maryland courts have discretion to award attorney fees — but the statute does not mandate them, unlike New Jersey and Washington. This is one of Maryland\'s most significant weaknesses: requesters may win but cannot recover the cost of litigation. Courts apply de novo review of withholding decisions.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_not_mandatory',
        'param_value': 'discretionary_not_mandatory',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-362(d)',
        'notes': 'IMPORTANT WEAKNESS: Maryland does not provide for mandatory attorney fees for prevailing requesters. Courts have discretion to award fees but are not required to do so. This is one of Maryland\'s most significant structural weaknesses — the absence of mandatory fee-shifting makes MPIA litigation economically unattractive for small or modest cases. By contrast, New Jersey, Washington, and Connecticut have mandatory fee-shifting provisions. Maryland requesters should document all litigation costs carefully and make a strong case for discretionary fee awards when they prevail.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_bad_faith',
        'param_value': 'available_for_bad_faith_violations',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-362(e)',
        'notes': 'Maryland courts may award civil penalties in cases of bad-faith withholding — where the custodian knowingly and willfully violated the MPIA without reasonable justification. The penalty provision is rarely invoked but available for egregious violations. The Compliance Board may also refer matters to the Attorney General for enforcement action in cases of systematic or bad-faith violations. Maryland does not have the per-day penalty structure found in Washington.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_custodian',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-203(d)',
        'notes': 'The burden of demonstrating that denial of access is authorized rests on the custodian, not the requester. Md. Code Gen. Prov. § 4-203(d) explicitly places the burden on the agency to justify withholding. The Compliance Board and circuit courts review withholding decisions de novo — there is no deference to the custodian\'s initial determination. Generic assertions of exemption categories without record-specific justification are insufficient. Custodians must provide specific statutory authority for each withheld record.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required_with_citation',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-203(c)',
        'notes': 'When denying a request in whole or in part, the custodian must provide a written denial stating the specific statutory provision(s) that authorize withholding. A denial without a specific statutory citation is legally deficient. The denial must also inform the requester of the right to seek review before the Compliance Board or in circuit court. Failure to provide adequate written denial reasons strengthens a requester\'s case before the Compliance Board.',
    },
    {
        'jurisdiction': 'MD',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Md. Code Gen. Prov. § 4-203(b)',
        'notes': 'Maryland custodians must release all reasonably segregable non-exempt portions of records when only part of a record qualifies for an exemption. Blanket withholding of complex documents because one section contains exempt material is not permitted. The Compliance Board has consistently required custodians to demonstrate that they reviewed documents for partial disclosure and separated exempt from non-exempt content.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

MD_TEMPLATES = [
    {
        'jurisdiction': 'MD',
        'record_type': 'general',
        'template_name': 'General Maryland Public Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Maryland Public Information Act Request — Md. Code Gen. Prov. § 4-101 et seq.

Dear Custodian of Records:

Pursuant to the Maryland Public Information Act (MPIA), Md. Code Ann., General Provisions § 4-101 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which reduces costs for both parties.

Regarding fees: I am willing to pay reasonable fees as permitted by Md. Code Gen. Prov. § 4-206(b), including standard copying fees not to exceed $0.25 per page and reasonable staff time charges reflecting actual costs. If total estimated fees will exceed ${{fee_limit}}, please provide an itemized estimate before proceeding so I may refine my request or arrange payment.

Under Md. Code Gen. Prov. § 4-203(d), the burden of demonstrating that any denial is authorized rests on the custodian. If any records are withheld in whole or in part, I request that you: (1) identify each record or category withheld; (2) state the specific provision of the Maryland Code that authorizes withholding; (3) explain how that provision applies to each specific record; and (4) confirm that all reasonably segregable non-exempt portions have been released.

Under Md. Code Gen. Prov. § 4-203(a), please respond within 10 business days. If a third-party notification period is required under § 4-203(b), please notify me promptly.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. Under Md. Code Gen. Prov. § 4-206(e):

[If claiming indigency:]
I am unable to pay the fees associated with this request due to financial hardship. I certify that I meet the standard for an indigent requester under Maryland law.

[If claiming public interest:]
I respectfully request a discretionary fee waiver because: (1) these records concern {{public_interest_explanation}}, a matter of significant public interest; (2) I am {{requester_category_description}} with no commercial purpose; (3) disclosure will benefit the public by {{public_benefit_explanation}}; and (4) electronic delivery minimizes reproduction costs.''',
        'expedited_language': '''I request that this MPIA request be processed as expeditiously as possible. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if clarification would allow faster processing.''',
        'notes': 'General MPIA template. Key MD features: (1) 10-business-day response deadline (30 days for third-party notice); (2) Compliance Board is a FREE alternative to court — file within 30 days of denial; (3) $0.25/page copy rate; (4) staff time charges allowed but must be reasonable; (5) mandatory fee waiver for indigent requesters; (6) NO mandatory attorney fees — significant weakness; (7) burden of proof on custodian; (8) specific statutory citation required in any denial; (9) cite "MPIA" and "Md. Code Gen. Prov. § 4" — not "FOIA."',
    },
    {
        'jurisdiction': 'MD',
        'record_type': 'law_enforcement',
        'template_name': 'Maryland MPIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Maryland Public Information Act Request — Law Enforcement Records, Md. Code Gen. Prov. § 4-101 et seq.

Dear Custodian of Records:

Pursuant to the Maryland Public Information Act (MPIA), Md. Code Ann., General Provisions § 4-101 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports, booking records, and charging documents
- Use-of-force reports and documentation
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Internal Affairs investigation records for sustained findings (Anton\'s Law, effective Oct. 1, 2021)
- Officer disciplinary records subject to Anton\'s Law

Regarding Anton\'s Law (effective October 1, 2021): Pursuant to Md. Code Pub. Safety § 3-104, Internal Affairs investigation records for sustained findings of misconduct are now subject to mandatory public disclosure. Please identify any responsive records covered by Anton\'s Law and provide them separately from any other responsive records.

Regarding claimed exemptions under § 4-311: Any claimed law enforcement investigative file exemption requires: (1) identification of the specific harm that disclosure would cause; (2) explanation of how each specific withheld record implicates that harm; and (3) confirmation that all non-exempt, segregable portions have been released.

Under Md. Code Gen. Prov. § 4-203(d), the burden of proving that any denial is authorized rests on the custodian.

I am willing to pay fees per § 4-206(b) up to ${{fee_limit}}. Please provide an advance itemized estimate if fees will exceed this amount.

Please respond within 10 business days per § 4-203(a).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for law enforcement actions. I am {{requester_category_description}}. Disclosure will benefit the public by enabling scrutiny of law enforcement conduct. Electronic delivery minimizes reproduction costs.''',
        'expedited_language': '''I request expedited processing of this MPIA request. These records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'Maryland law enforcement MPIA template. Key features: (1) Anton\'s Law (Md. Code Pub. Safety § 3-104, effective Oct. 1, 2021) mandates disclosure of Internal Affairs records for sustained misconduct findings — always invoke this separately; (2) investigative file exemption (§ 4-311) requires specific harm showing per record; (3) incident reports and arrest records are public regardless of investigation status; (4) Compliance Board is the preferred low-cost forum for enforcement disputes; (5) no mandatory attorney fees — document all costs for potential discretionary award; (6) 10-business-day response deadline.',
    },
    {
        'jurisdiction': 'MD',
        'record_type': 'contracts_procurement',
        'template_name': 'Maryland MPIA Request — Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Maryland Public Information Act Request — Government Contracts and Procurement, Md. Code Gen. Prov. § 4-101 et seq.

Dear Custodian of Records:

Pursuant to the Maryland Public Information Act (MPIA), Md. Code Ann., General Provisions § 4-101 et seq., I request copies of the following records relating to government contracts and procurement:

{{description_of_records}}

Specifically, I request:
- All contracts, task orders, and amendments between {{agency_name}} and {{contractor_or_vendor_name}} for {{date_range_start}} through {{date_range_end}}
- Requests for Proposals (RFPs), Invitations for Bids (IFBs), and solicitation documents
- All proposal and bid submissions from competing vendors
- Evaluation criteria, scoring sheets, and award decision memoranda
- Invoices, payment records, and change orders
- Correspondence relating to the above contracts

Regarding trade secret claims: Under Maryland law, contract prices and amounts paid with public funds are public records and do not qualify as trade secrets. Under § 4-313, trade secret protection requires a showing of "substantial" competitive harm — speculative or minor competitive disadvantage is insufficient. Any trade secret claim must be supported by specific evidence identifying the exact information claimed as proprietary and explaining the mechanism of substantial competitive harm.

Third-party vendors claiming trade secret protection must have designated information as proprietary when submitted. If {{agency_name}} receives a third-party objection under § 4-203(b), please notify me promptly and continue processing the non-contested portions of this request.

Under Md. Code Gen. Prov. § 4-203(d), the burden of proving that any denial is authorized rests on the custodian.

I am willing to pay fees per § 4-206(b) up to ${{fee_limit}}.

Please respond within 10 business days per § 4-203(a).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived or reduced for this request. These procurement records concern public expenditures by {{agency_name}}, a matter of significant public interest. I am {{requester_category_description}} with no commercial purpose. Disclosure will benefit the public by enabling scrutiny of how public funds are spent. Electronic records can be provided at minimal cost.''',
        'expedited_language': '''I request expedited processing because these procurement records relate to {{time_sensitive_reason}} and delay would harm the public interest by {{harm_from_delay}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Maryland procurement MPIA template. Key features: (1) trade secret exemption requires "substantial" competitive harm — a higher standard than many states; (2) third-party notification procedure under § 4-203(b) may extend response to 30 days — note this in the request; (3) contract prices and amounts paid with public funds are definitively public; (4) Compliance Board is available for free dispute resolution; (5) no mandatory attorney fees — document costs carefully; (6) 10-business-day initial deadline.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in MD_EXEMPTIONS:
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

    print(f'MD exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in MD_RULES:
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

    print(f'MD rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in MD_TEMPLATES:
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

    print(f'MD templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'MD total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_md', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
