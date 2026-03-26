#!/usr/bin/env python3
"""Build Virginia Freedom of Information Act data: exemptions, rules, and templates.

Covers the Virginia Freedom of Information Act (VFOIA), Va. Code § 2.2-3700 et seq.
VFOIA provides a right of access to public records and meetings. Key features:
5-business-day response deadline with optional 7-day extension, no administrative
appeal (go directly to general district or circuit court), civil penalties of
$500-$2,000, mandatory attorney fees for prevailing requesters, and $0.50/page
maximum copy rate. Virginia courts construe exemptions narrowly.

Run: python3 scripts/build/build_va.py
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
# VFOIA exemptions are spread across Va. Code § 2.2-3705.1 through 2.2-3705.7
# (general exemptions) and numerous specific exemptions throughout the Code.
# The Act provides a presumption of openness — exemptions are permissive, not
# mandatory, meaning agencies may (but need not) withhold exempt records.
# Courts apply a strict construction against withholding.
# =============================================================================

VA_EXEMPTIONS = [
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.1(1)',
        'exemption_number': 'VFOIA § 2.2-3705.1(1)',
        'short_name': 'Proprietary Information — Trade Secrets',
        'category': 'commercial',
        'description': 'Proprietary information, trade secrets, and other confidential commercial or financial information submitted by a private entity to a public body are exempt from mandatory VFOIA disclosure when the private entity has identified the material as proprietary at the time of submission.',
        'scope': 'Commercially valuable information submitted by private parties to government bodies where: (1) the information constitutes a trade secret or confidential commercial/financial data; (2) the private entity has designated the information as proprietary at the time of submission; and (3) disclosure would cause competitive harm. Virginia applies the Uniform Trade Secrets Act definition. Government-generated records and public contract amounts are generally not trade secrets. Agencies may not simply accept vendor designations without independent evaluation. Amounts paid with public funds are public regardless of vendor designation.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'confidential commercial information',
            'competitive harm', 'UTSA', 'financial information', 'private entity submission',
            'competitive disadvantage', 'commercial data',
        ]),
        'counter_arguments': json.dumps([
            'VFOIA exemptions are permissive — the agency may disclose even if the exemption technically applies',
            'Contract prices, amounts paid with public funds, and performance data are public regardless of vendor designation',
            'The private entity must have designated the information as proprietary at the time of submission — post-hoc claims are not valid',
            'Publicly available information cannot qualify as a trade secret',
            'The agency must independently evaluate the trade secret claim — it may not simply defer to the submitter',
            'Challenge the adequacy of the submitter\'s secrecy measures — careless disclosure elsewhere defeats the claim',
        ]),
        'notes': 'VFOIA\'s trade secret exemption is permissive — agencies have discretion to disclose even if the exemption applies. Virginia courts have consistently held that amounts paid with public funds are public. The designation-at-time-of-submission requirement prevents retroactive trade secret claims. See Va. Dep\'t of Corrections v. Surovell, 290 Va. 255 (2015).',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.1(2)',
        'exemption_number': 'VFOIA § 2.2-3705.1(2)',
        'short_name': 'Working Papers — Governor, Lieutenant Governor, Attorney General',
        'category': 'deliberative',
        'description': 'Working papers and correspondence of the Governor, Lieutenant Governor, and Attorney General, including written advice and recommendations, are exempt from VFOIA disclosure. This executive privilege is narrow and does not extend to all executive branch agencies.',
        'scope': 'Personal working papers, private correspondence, and written advice received by the Governor, Lieutenant Governor, or Attorney General in their official capacity. This is a constitutional separation-of-powers exemption for the core executive offices. It does NOT extend to state agencies generally, to cabinet secretaries, or to agency heads below the constitutional office level. Final decisions, official communications sent on behalf of these offices, and records of official actions are public. Working papers that have been circulated broadly, acted upon, or otherwise made the basis of public decisions may lose their protected character.',
        'key_terms': json.dumps([
            'working papers', 'Governor\'s correspondence', 'executive privilege',
            'Attorney General working papers', 'written advice', 'executive branch deliberation',
            'constitutional officer', 'personal working papers',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is limited to the three named constitutional offices — it does not apply to state agencies or cabinet secretaries',
            'Final decisions and official communications are public regardless of this exemption',
            'Working papers that have been broadly circulated or acted upon as the basis of public decisions may not qualify',
            'VFOIA exemptions are permissive — agencies may choose to disclose even if the exemption technically applies',
            'Challenge claims that agency-level staff documents are "working papers" of the Governor',
        ]),
        'notes': 'Virginia\'s working papers exemption for constitutional officers is narrower than the federal executive privilege doctrine. Virginia courts have held it does not extend broadly to the executive branch. The permissive nature of VFOIA exemptions means agencies have discretion to disclose working papers even when technically exempt.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.1(3)',
        'exemption_number': 'VFOIA § 2.2-3705.1(3)',
        'short_name': 'Drafts and Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Drafts of legislation, executive orders, and agency rules or regulations — as well as confidential communications between government attorneys and their clients protected by the attorney-client privilege — are exempt from VFOIA.',
        'scope': 'Pre-decisional drafts of proposed legislation, executive orders, and proposed rules or regulations before their official promulgation. Also covers confidential communications between government entities and their attorneys made for the purpose of obtaining legal advice (attorney-client privilege) and work product prepared in anticipation of litigation. The draft exemption applies only while the draft is truly preliminary — once a draft is presented to a governing body or acted upon, it becomes public. Purely factual material in drafts is not protected. The attorney-client privilege requires that communications be for legal advice (not policy or business advice) and maintained in confidence.',
        'key_terms': json.dumps([
            'draft legislation', 'draft regulation', 'predecisional draft',
            'attorney-client privilege', 'work product', 'legal advice',
            'privileged communication', 'in anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'Once a draft is presented to a governing body or acted upon, it is no longer a draft and becomes public',
            'Purely factual information in drafts must be segregated and released',
            'Attorney-client privilege requires legal advice, not policy or business guidance',
            'Billing records and retainer agreements are not privileged',
            'Waiver occurs when the agency discloses advice in public proceedings or to non-essential third parties',
            'VFOIA exemptions are permissive — the agency may choose to disclose drafts',
        ]),
        'notes': 'Virginia\'s draft exemption is permissive — agencies have discretion to release drafts. The attorney-client privilege for government entities in Virginia is well-established but narrowly construed. Working law — standards and criteria agencies actually apply — must be disclosed even if contained in internal documents.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.2(1)',
        'exemption_number': 'VFOIA § 2.2-3705.2(1)',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Personnel records — including performance evaluations, disciplinary records, payroll deduction information, and similar records about individual employees — are exempt from VFOIA. However, the name, position, job classification, official salary, and dates of employment of public employees are expressly public.',
        'scope': 'Personnel records of individual public employees, including performance evaluations, disciplinary proceedings, medical information, payroll deduction details, and similar records relating to an individual employee\'s employment status. Virginia law expressly carves out as public: name, position, job classification, official salary or pay range, and dates of service. Aggregate compensation data, organizational charts, and position descriptions are public. The exemption does not protect official actions taken against employees that have public consequences — terminations for cause and disciplinary actions affecting public safety may be public through the common-law right of access.',
        'key_terms': json.dumps([
            'personnel record', 'employee file', 'performance evaluation', 'disciplinary record',
            'payroll deduction', 'public employee', 'salary', 'personnel file',
            'human resources record', 'employment record',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, job classification, official salary, and dates of service are expressly public under Va. Code § 2.2-3705.2(1)',
            'Final disciplinary actions affecting public safety or involving misconduct may be public',
            'Official actions taken against employees in their official capacity are distinguishable from purely personal personnel matters',
            'VFOIA exemptions are permissive — agencies may disclose personnel records even if technically exempt',
            'Aggregate data and statistical information from personnel records are not covered by this exemption',
        ]),
        'notes': 'Virginia\'s personnel exemption, like other VFOIA exemptions, is permissive — not mandatory. Va. Code § 2.2-3705.2(1) expressly states what is public. The permissive exemption means advocacy for voluntary disclosure is always available alongside VFOIA demands.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.2(2)',
        'exemption_number': 'VFOIA § 2.2-3705.2(2)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Medical and mental health records of identifiable individuals, including health information maintained by public health agencies, are exempt from VFOIA to protect patient privacy.',
        'scope': 'Individually identifiable medical and mental health records maintained by public bodies, including health departments, state psychiatric facilities, correctional facilities, and other government health providers. HIPAA applies independently to covered entities. The exemption covers individual medical records — not aggregate public health statistics, epidemiological data, or general health policy records. Anonymized or de-identified data is not covered by this exemption. Records about agency health programs, budgets, and operations are public.',
        'key_terms': json.dumps([
            'medical record', 'mental health record', 'patient information', 'health record',
            'HIPAA', 'individually identifiable', 'public health record',
            'patient privacy', 'health information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and de-identified public health data are not covered by this exemption',
            'Agency health policy records, budgets, and program operations are public',
            'Records about how the agency administers health programs — not individual patient information — are public',
            'VFOIA exemptions are permissive — agencies may disclose with patient consent or for public health purposes',
        ]),
        'notes': 'HIPAA applies independently to government entities that are HIPAA covered entities. Virginia\'s VFOIA medical records exemption and HIPAA work in conjunction. Virginia courts have held that the combination creates a strong presumption against disclosure of individual medical records, but this does not protect agency policies or aggregate data.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.2(7)',
        'exemption_number': 'VFOIA § 2.2-3705.2(7)',
        'short_name': 'Social Services and Public Assistance Records',
        'category': 'privacy',
        'description': 'Records of social services agencies identifying recipients of public assistance, beneficiaries of social services programs, and related case records are exempt from VFOIA to protect client privacy.',
        'scope': 'Case records, eligibility determinations, and related documents identifying individual recipients of social services, public assistance (SNAP, Medicaid, TANF), and similar programs administered by Virginia social services agencies. The exemption covers individual client information — not program budgets, aggregate statistics, or agency policies. Records about the agency\'s administration of programs, compliance with federal requirements, and fiscal management are public. The federal Privacy Act applies independently to some federally funded program records.',
        'key_terms': json.dumps([
            'social services records', 'public assistance', 'SNAP', 'Medicaid',
            'TANF', 'case records', 'benefit recipient', 'social services client',
            'welfare records', 'program recipient',
        ]),
        'counter_arguments': json.dumps([
            'Program budgets, aggregate statistics, and administrative records are public',
            'Agency policies, regulations, and eligibility criteria are public',
            'Federal oversight records and audit findings are generally public',
            'VFOIA exemptions are permissive — challenge whether the agency is making an independent disclosure decision',
        ]),
        'notes': 'Virginia social services records are protected by both VFOIA and federal statutes governing specific programs (e.g., 42 U.S.C. § 1306 for Social Security). The combination creates strong protection for individual client information but does not shield program administration from scrutiny.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3706',
        'exemption_number': 'VFOIA § 2.2-3706',
        'short_name': 'Law Enforcement and Criminal Records',
        'category': 'law_enforcement',
        'description': 'Criminal investigation records whose disclosure would jeopardize an ongoing investigation, reveal an informant, endanger life, or interfere with prosecution are exempt. Virginia law enforcement agencies have a separate, more detailed exemption scheme at Va. Code § 2.2-3706.',
        'scope': 'Law enforcement records where disclosure would: jeopardize a pending criminal investigation; reveal confidential informants; endanger any person\'s safety; enable a person to evade apprehension; identify undercover officers; or interfere with pending prosecution. Virginia also exempts certain categories of adult criminal history records (managed separately by VCIN), juvenile criminal records, and specific types of intelligence records. Once prosecution concludes or investigation is closed, most records become public. Incident reports and arrest records are generally public regardless of investigation status.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement records', 'confidential informant',
            'pending prosecution', 'undercover officer', 'criminal intelligence',
            'VCIN', 'arrest records', 'incident reports', 'investigation records',
        ]),
        'counter_arguments': json.dumps([
            'Incident reports, arrest records, and booking information are public regardless of investigation status',
            'Completed investigation records are generally public once prosecution concludes',
            'The exemption requires showing that specific harm would result from disclosure — generic "investigation" labels are insufficient',
            'Factual portions of investigation files that don\'t reveal informants or techniques must be released',
            'VFOIA exemptions are permissive — agencies may disclose even if technically exempt',
            'Virginia courts apply strict construction of exemptions against withholding',
        ]),
        'notes': 'Virginia\'s law enforcement exemption at § 2.2-3706 is detailed and creates mandatory disclosure requirements for specific records including: names of individuals arrested, charges, booking information, and police blotter information. The permissive nature of VFOIA exemptions means law enforcement agencies have discretion to release more than the mandatory disclosures.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.4(3)',
        'exemption_number': 'VFOIA § 2.2-3705.4(3)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related documents prepared by or for public bodies in connection with the acquisition, condemnation, or sale of real property are exempt until the transaction is complete or negotiations cease.',
        'scope': 'Formal property appraisals, feasibility studies, and related valuation documents prepared in connection with a government agency\'s purchase, sale, or condemnation of real property. The exemption is time-limited — it expires when the transaction closes or negotiations are terminated. Post-transaction, all appraisal records are public. The exemption exists to protect negotiating position and prevent agencies from being disadvantaged by disclosure of their maximum willingness to pay. Internal communications about general property value range (not formal appraisals) may not qualify.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'condemnation appraisal', 'pre-acquisition', 'property valuation',
            'real property', 'land purchase', 'negotiating position',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction closes or negotiations terminate — post-transaction appraisals are public',
            'Challenge claims that negotiations remain "pending" after extended inactivity',
            'General budget estimates and internal discussion documents may not qualify as formal appraisals',
            'After condemnation judgment, all valuation records are public',
            'VFOIA exemptions are permissive — agencies may disclose pre-acquisition appraisals',
        ]),
        'notes': 'Virginia\'s pre-acquisition appraisal exemption is time-limited and narrow. It applies only to formal appraisals in connection with actual acquisitions — not to general property assessments or studies. Once transactions complete, full disclosure is required.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.6(1)',
        'exemption_number': 'VFOIA § 2.2-3705.6(1)',
        'short_name': 'Attorney Work Product — Litigation',
        'category': 'deliberative',
        'description': 'Work product of government attorneys prepared in anticipation of litigation, including legal memoranda, case strategies, and research compiled for a specific litigation matter, is exempt from VFOIA.',
        'scope': 'Documents prepared by or at the direction of government attorneys for the purpose of pending or reasonably anticipated litigation. Includes case strategy memoranda, witness assessments, legal research prepared for a specific matter, and attorney notes. Does NOT include general legal advice unconnected to specific litigation, legal opinions about general regulatory matters, or billing records. The work product doctrine requires a specific nexus to anticipated litigation — speculative future litigation is insufficient. Factual information compiled during discovery or investigation that is not specifically attorney analysis is not work product.',
        'key_terms': json.dumps([
            'attorney work product', 'litigation preparation', 'work product doctrine',
            'anticipated litigation', 'case strategy', 'legal research',
            'attorney notes', 'litigation memorandum', 'trial preparation',
        ]),
        'counter_arguments': json.dumps([
            'General legal opinions on regulatory matters unconnected to specific litigation are not work product',
            'Factual information compiled by staff (not attorneys) for litigation is not attorney work product',
            'Billing records and retainer agreements are not work product',
            'Information about the outcome of litigation, settlements, and consent decrees is public',
            'Work product protection is waived when disclosed to adverse parties or the public',
            'VFOIA exemptions are permissive — agencies may disclose work product',
        ]),
        'notes': 'Virginia applies the common-law work product doctrine to government attorneys under VFOIA. The exemption is distinct from the attorney-client privilege — it requires specific anticipation of litigation, not just general legal advice. Virginia courts have generally applied the doctrine consistently with federal common law standards.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.7(10)',
        'exemption_number': 'VFOIA § 2.2-3705.7(10)',
        'short_name': 'Security Infrastructure and Emergency Response',
        'category': 'safety',
        'description': 'Records containing specific details of security systems, security plans, vulnerability assessments, or emergency response procedures for public buildings and infrastructure are exempt to the extent disclosure would compromise the security measures.',
        'scope': 'Specific technical details of physical security systems, access control mechanisms, vulnerability assessments identifying specific exploitable weaknesses, and detailed emergency response protocols for government facilities. The exemption is narrowly targeted at information that would actually help a bad actor defeat security measures — not at general emergency policy, budget, or administrative records. Aggregate statistics about security spending, general emergency management frameworks, and after-action reports that focus on policy improvements rather than vulnerability details are public.',
        'key_terms': json.dumps([
            'security system', 'vulnerability assessment', 'security plan',
            'emergency response procedure', 'physical security', 'access control',
            'critical infrastructure', 'security protocol', 'building security',
        ]),
        'counter_arguments': json.dumps([
            'General emergency management policies and frameworks are public',
            'Budget and staffing information for security programs is public',
            'After-action reports focused on policy improvements rather than specific vulnerabilities are public',
            'The exemption requires showing that specific security would be compromised — not a generalized security classification',
            'VFOIA exemptions are permissive — agencies have discretion to disclose security records',
        ]),
        'notes': 'Virginia\'s security exemption is more specific and narrower than many states\' equivalent provisions. Courts focus on whether the specific information would actually enable a security breach, not whether it relates generally to security. The permissive nature of the exemption gives agencies flexibility to share information with appropriate parties.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3705.3(7)',
        'exemption_number': 'VFOIA § 2.2-3705.3(7)',
        'short_name': 'Educational Records — Student Privacy',
        'category': 'privacy',
        'description': 'Educational records of individual students at public schools and universities, protected by FERPA (federal) and incorporated into VFOIA\'s exemption framework, are exempt from disclosure to protect student privacy.',
        'scope': 'Individually identifiable education records of students at Virginia public schools and universities, consistent with the Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g. Covers transcripts, disciplinary records, financial aid records, health records maintained by the school, and other records directly related to individual students. Does NOT cover: (1) directory information (name, address, enrollment status) where the student has not opted out under FERPA; (2) aggregate statistical data about student populations; (3) school administrative records, budget, and policy documents; (4) records about faculty and staff.',
        'key_terms': json.dumps([
            'student record', 'educational record', 'FERPA', 'student privacy',
            'student transcript', 'student disciplinary record', 'directory information',
            'personally identifiable information', 'school record',
        ]),
        'counter_arguments': json.dumps([
            'FERPA permits disclosure of directory information unless the student has opted out',
            'Aggregate data about student populations, graduation rates, and outcomes is public',
            'School policy documents, curriculum materials, and administrative records are public',
            'Faculty and staff records are not student records and are not covered by FERPA',
            'Records about school safety incidents and systemic policy failures may be public even if they involve students, if properly de-identified',
        ]),
        'notes': 'FERPA applies to all educational institutions receiving federal funding and creates a federal overlay on Virginia\'s VFOIA exemption. Virginia schools must comply with both. FERPA provides for exceptions including health and safety emergencies and the ability to disclose to appropriate parties. The combination of VFOIA\'s permissive exemption framework and FERPA\'s mandatory prohibition makes the analysis more complex.',
    },
    {
        'jurisdiction': 'VA',
        'statute_citation': 'Va. Code § 2.2-3700(B)',
        'exemption_number': 'VFOIA — Permissive Exemption Rule',
        'short_name': 'Permissive Nature of All VFOIA Exemptions',
        'category': 'deliberative',
        'description': 'All VFOIA exemptions are permissive, not mandatory. Virginia agencies may choose to disclose records that technically fall within an exemption. This is a structural feature of VFOIA that distinguishes it from many state public records laws.',
        'scope': 'Va. Code § 2.2-3700(B) explicitly states that VFOIA exemptions permit, but do not require, agencies to withhold records. This means: (1) agencies have discretion to disclose exempt records; (2) requesters can argue for voluntary disclosure even when an exemption technically applies; (3) an agency\'s decision to exercise discretion and disclose is not a VFOIA violation; and (4) advocacy and negotiation for voluntary disclosure is always available as a strategy alongside formal VFOIA demands. This is one of VFOIA\'s most distinctive and requester-friendly features.',
        'key_terms': json.dumps([
            'permissive exemption', 'agency discretion', 'voluntary disclosure',
            'may withhold', 'not required to withhold', 'discretionary withholding',
            'VFOIA exemption structure', 'disclosure policy',
        ]),
        'counter_arguments': json.dumps([
            'Always note that VFOIA exemptions are permissive — agencies may disclose even if an exemption technically applies',
            'Argue for voluntary disclosure on public interest grounds when an exemption technically applies',
            'An agency\'s decision to exercise discretion and disclose is not a violation of any other party\'s rights',
            'Use the permissive structure to engage in negotiation and advocacy before resorting to formal legal challenges',
            'Document agency decisions to withhold vs. disclose as part of accountability tracking',
        ]),
        'notes': 'The permissive nature of VFOIA exemptions is a fundamental feature of Virginia\'s public records framework. Va. Code § 2.2-3700(B) is explicit. Practitioners consistently find that framing requests to highlight the public interest can lead agencies to voluntarily disclose records they technically could withhold. This is an important strategic tool in Virginia VFOIA practice.',
    },
]

# =============================================================================
# RULES
# Virginia FOIA, Va. Code § 2.2-3700 et seq.
# Key features: 5-business-day response deadline, optional 7-day extension,
# no formal administrative appeal (go directly to general district or circuit
# court), mandatory civil penalties $500-$2,000, mandatory attorney fees for
# prevailing requesters, $0.50/page maximum copy rate.
# =============================================================================

VA_RULES = [
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'Va. Code § 2.2-3704(B)',
        'notes': 'VFOIA requires public bodies to respond to requests within 5 business days of receiving the request. Within 5 business days, the agency must either: (1) provide the records; (2) advise the requester when records will be available; or (3) invoke an extension not to exceed 7 additional business days. Failure to respond within 5 business days is itself a VFOIA violation — Virginia courts have held that non-response is equivalent to a denial. The 5-business-day clock begins on the business day the request is received. Requests received after business hours begin the clock the next business day.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'extension_days',
        'param_value': '7',
        'day_type': 'business',
        'statute_citation': 'Va. Code § 2.2-3704(B)(3)',
        'notes': 'Virginia agencies may extend the response deadline by up to 7 additional business days if they cannot respond within the initial 5-business-day period. To invoke an extension, the agency must: (1) notify the requester in writing within the initial 5-business-day period; (2) provide a reason for the extension; and (3) specify a date by which the response will be provided. The maximum extension is 7 business days — the total response period cannot exceed 12 business days (5 initial + 7 extension). Extensions must be genuine, not boilerplate. The Virginia Freedom of Information Advisory Council can provide guidance on appropriate extension use.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_max_per_page',
        'param_value': '0.50',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(F)',
        'notes': 'Virginia agencies may charge reasonable fees for VFOIA requests, but copying fees may not exceed $0.50 per page for standard documents. Agencies may also charge for staff time spent searching, reviewing, and redacting records at the hourly rate of the lowest-paid employee capable of performing the work — this is an important distinction from states like New Jersey that prohibit staff time charges. Agencies must notify the requester in advance if estimated fees will exceed $200, providing an itemized list of anticipated costs. Requesters can revise requests to reduce fees. Electronic records should generally be provided at a lower cost than paper.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_charges_allowed',
        'param_value': 'yes_at_lowest_paid_employee_rate',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(F)',
        'notes': 'Unlike some states, Virginia allows agencies to charge for staff time spent searching for, reviewing, and redacting records. The rate charged must reflect the hourly rate of the lowest-paid employee capable of performing the task — not the actual employee who performs it. If a $100/hour attorney spends time redacting, the agency can only charge the rate of the lowest-paid employee who could perform that redaction. Agencies must provide an itemized cost estimate before incurring charges exceeding $200. Requesters may then refine their request to reduce costs.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(F)',
        'notes': 'Virginia does not mandate fee waivers for any category of requester. Fee waivers are entirely at the agency\'s discretion. However, agencies have discretion to waive or reduce fees, and many do so for journalists, nonprofits, academic researchers, and other requesters demonstrating a public interest. When seeking a fee waiver, requesters should document: their identity and purpose, the public benefit of disclosure, their inability to pay, and the absence of commercial benefit to the request. Virginia\'s Freedom of Information Advisory Council can provide guidance on fee waiver practices.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'fee_cap',
        'param_key': 'advance_cost_estimate_threshold',
        'param_value': '200',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(F)',
        'notes': 'When estimated fees will exceed $200, Virginia agencies must notify the requester and provide an itemized list of anticipated costs before incurring those charges. The requester then has the option to pay, revise the request to reduce costs, or withdraw the request. This advance-notice requirement provides requesters with budget visibility and prevents surprise charges. Agencies cannot incur fees above $200 without this advance notice and the requester\'s agreement to proceed.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'appeal_deadline',
        'param_key': 'no_administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3713',
        'notes': 'Virginia has NO formal administrative appeal process for VFOIA denials. There is no agency head appeal, no state-level ombudsman, and no administrative tribunal for VFOIA disputes. A requester who is denied access must go directly to the general district court or circuit court under Va. Code § 2.2-3713. The Freedom of Information Advisory Council (FOIA Council) can provide guidance and informal mediation but has no adjudicatory authority. This means Virginia VFOIA enforcement is entirely judicial — there is no cheaper, faster administrative alternative.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'court_action_available',
        'param_value': 'general_district_or_circuit_court',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3713',
        'notes': 'A requester denied access to records may file a petition in the general district court or circuit court of the jurisdiction where the public body is located. The court reviews the denial and may order disclosure. General district court is faster and less expensive but has limited jurisdiction. Circuit court has full equity jurisdiction and can order complex relief. Va. Code § 2.2-3713(D) allows circuit courts to conduct in camera review of withheld records. There is no specific statute of limitations for VFOIA court actions, but courts may consider unreasonable delay in filing.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_range',
        'param_value': '$500-$2,000',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3714',
        'notes': 'Courts may assess civil penalties of $500 to $2,000 against a public body or officer who "willfully and knowingly" violates VFOIA. Penalties are assessed per violation, not per day, distinguishing Virginia from states like Washington with per diem penalty schemes. A "willful and knowing" violation requires more than negligence — the agency or officer must have known the records were public and deliberately withheld them. Penalties are payable to the Literary Fund (a state education fund). Virginia courts have found willful violations where agencies denied requests based on exemptions known to be inapplicable.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_mandatory',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3713(D)',
        'notes': 'Virginia courts SHALL award attorney fees and costs to a requester who substantially prevails in a VFOIA court action, unless special circumstances make an award unjust. The mandatory fee-shifting provision makes VFOIA enforcement economically viable. Courts have awarded substantial attorney fees in VFOIA cases, including cases where the violation was technical or the records modest. The fee award covers reasonable attorney fees and litigation costs, including copying costs and court fees.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'foia_council_advisory',
        'param_value': 'available_no_adjudicatory_power',
        'day_type': None,
        'statute_citation': 'Va. Code § 30-179',
        'notes': 'The Virginia Freedom of Information Advisory Council (FOIA Council), created under Va. Code § 30-179, provides informal guidance, training, and mediation for VFOIA disputes. The FOIA Council can issue advisory opinions on whether specific records should be disclosed, but these opinions are not binding on agencies or courts. The FOIA Council\'s advisory opinions are valuable persuasive authority — agencies that ignore them face greater risk in litigation. The Council can be a useful low-cost first step before litigation, particularly for disputes about novel exemption questions.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(B)',
        'notes': 'Virginia agencies must release all non-exempt, reasonably segregable portions of records when only part of a record qualifies for an exemption. Agencies cannot withhold entire documents because one section contains exempt material — they must redact the exempt portions and release the remainder. Virginia courts have consistently required agencies to demonstrate that they reviewed documents for partial disclosure. Blanket withholding of complex documents without segregation analysis supports a finding of willful violation.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3713(C)',
        'notes': 'The burden of proving that a VFOIA denial was lawful rests on the public body — not the requester. Va. Code § 2.2-3713(C) places the burden squarely on the agency to demonstrate that each exemption applies to each withheld record. This is consistent with VFOIA\'s presumption of openness in Va. Code § 2.2-3700(B). Generic claims of exemption categories without record-specific justification are insufficient. Virginia courts review VFOIA withholding decisions de novo.',
    },
    {
        'jurisdiction': 'VA',
        'rule_type': 'initial_response',
        'param_key': 'written_response_required',
        'param_value': 'yes_with_specific_citation',
        'day_type': None,
        'statute_citation': 'Va. Code § 2.2-3704(B)(2)',
        'notes': 'When denying a VFOIA request in whole or in part, Virginia agencies must provide a written response citing the specific statutory exemption that authorizes withholding. A denial that does not cite a specific Va. Code provision is legally deficient. The agency must identify the specific provision — citing § 2.2-3705 generally is insufficient; the specific subsection must be identified. This requirement enables requesters and courts to evaluate the validity of each claimed exemption.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

VA_TEMPLATES = [
    {
        'jurisdiction': 'VA',
        'record_type': 'general',
        'template_name': 'General Virginia FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Va. Code § 2.2-3700 et seq.

Dear FOIA Officer:

Pursuant to the Virginia Freedom of Information Act (VFOIA), Va. Code § 2.2-3700 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I prefer to receive records in electronic format (email or download link) where available, which reduces cost for both parties.

Regarding fees: Under Va. Code § 2.2-3704(F), I am willing to pay reasonable fees reflecting the actual costs of search and reproduction, calculated using the hourly rate of the lowest-paid employee capable of performing each task, plus $0.50 per page maximum for copies. If estimated fees will exceed $200, please provide an itemized cost estimate in advance so I may refine my request.

Under Va. Code § 2.2-3713(C), the burden of proving that any denial is authorized rests on the public body. If any records are withheld in whole or in part, I request that you: (1) identify each record or category of records withheld; (2) state the specific Virginia Code provision authorizing withholding (specific subsection of § 2.2-3705 or other exemption, not just the general section); (3) explain how the specific provision applies to each withheld record; and (4) confirm that all reasonably segregable non-exempt portions have been released.

Note: VFOIA exemptions are permissive under Va. Code § 2.2-3700(B) — I encourage {{agency_name}} to exercise its discretion to disclose records even where a technical exemption exists, in light of the public interest in transparency described above.

Under Va. Code § 2.2-3704(B), please respond within 5 business days. If an extension is needed, please notify me within 5 business days with a specific date for production.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that fees be waived or reduced for this request. While Virginia law does not mandate a fee waiver, I ask {{agency_name}} to exercise its discretion under Va. Code § 2.2-3704(F) to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. I have no commercial purpose in this request.

4. If records are provided electronically, search and reproduction costs are minimal or zero.

If a full waiver is not possible, I request that the fee be reduced to the actual cost of electronic reproduction, with any staff time charges limited to the minimum necessary.''',
        'expedited_language': '''I request expedited processing of this VFOIA request under the "most timely possible action" principle. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if clarification would allow faster production.''',
        'notes': 'General VFOIA template. Key VA features: (1) 5-business-day deadline with optional 7-day extension — cite Va. Code § 2.2-3704(B); (2) all VFOIA exemptions are PERMISSIVE — always note this and encourage voluntary disclosure; (3) no administrative appeal — go directly to general district or circuit court if denied; (4) civil penalties $500-$2,000 for willful violations; (5) mandatory attorney fees for prevailing requesters; (6) $0.50/page max copying fee; (7) staff time charges allowed at lowest-paid-employee rate; (8) advance notice required when estimated fees exceed $200; (9) burden of proof on agency; (10) specific Va. Code section required in any denial.',
    },
    {
        'jurisdiction': 'VA',
        'record_type': 'law_enforcement',
        'template_name': 'Virginia FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records, Va. Code § 2.2-3700 et seq.

Dear FOIA Officer:

Pursuant to the Virginia Freedom of Information Act (VFOIA), Va. Code § 2.2-3700 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and police offense reports
- Arrest reports, booking records, and charging documents
- Use-of-force reports and related documentation
- Body-worn camera and dash camera footage and metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Officer disciplinary records (final dispositions)
- Internal investigation records related to the above

Regarding exemptions under Va. Code § 2.2-3706: The law enforcement exemption is permissive under Va. Code § 2.2-3700(B) — {{agency_name}} has discretion to disclose records even where the exemption technically applies. Under Va. Code § 2.2-3706(A)(1), the following are mandatory disclosures regardless of investigation status: the name and address of any individual arrested, the charges, and the arresting officer\'s name and badge number. Please ensure all mandatory disclosures are made in addition to responding to this broader request.

Any claimed exemption under § 2.2-3706 must: (1) cite the specific subsection; (2) explain how the specific harm enumerated in that subsection applies to each withheld record; and (3) confirm that segregable non-exempt portions have been released.

Pursuant to Va. Code § 2.2-3713(C), the burden of proof for any denial rests on the public body.

I am willing to pay fees per Va. Code § 2.2-3704(F) up to ${{fee_limit}}. Please provide an itemized cost estimate if fees will exceed $200.

Please respond within 5 business days per Va. Code § 2.2-3704(B).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery minimizes reproduction costs. I encourage {{agency_name}} to exercise its permissive discretion under VFOIA to provide these records without charge.''',
        'expedited_language': '''I request expedited processing of this VFOIA request. These records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'Virginia law enforcement VFOIA template. Key features: (1) all exemptions are permissive — always emphasize agency discretion; (2) Va. Code § 2.2-3706(A)(1) mandates disclosure of arrest name, charges, and officer identity regardless of investigation status; (3) body camera footage is subject to VFOIA; (4) 5-business-day deadline; (5) no administrative appeal — circuit court is the forum for enforcement; (6) mandatory attorney fees for prevailing requesters.',
    },
    {
        'jurisdiction': 'VA',
        'record_type': 'contracts_procurement',
        'template_name': 'Virginia FOIA Request — Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Government Contracts and Procurement Records, Va. Code § 2.2-3700 et seq.

Dear FOIA Officer:

Pursuant to the Virginia Freedom of Information Act (VFOIA), Va. Code § 2.2-3700 et seq., I request copies of the following records relating to government contracts and procurement:

{{description_of_records}}

Specifically, I request:
- All contracts, purchase orders, and amendments between {{agency_name}} and {{contractor_or_vendor_name}} for {{date_range_start}} through {{date_range_end}}
- Requests for Proposals (RFPs), Invitations for Bids (IFBs), and related solicitation documents
- All bid and proposal submissions from competing vendors
- Evaluation criteria, scoring sheets, and selection committee records
- Invoices, payment records, and change orders
- Any communications between {{agency_name}} and {{contractor_or_vendor_name}} related to the above

Under VFOIA, contract prices, amounts paid with public funds, and performance metrics are public records. Any trade secret exemption claims under Va. Code § 2.2-3705.1(1) require that the vendor designated the information as proprietary AT THE TIME OF SUBMISSION — retroactive designations are not valid. Contract pricing is not a trade secret. I request that any redactions be limited to specific technical data meeting the UTSA definition, with all other contract information provided.

All VFOIA exemptions are permissive under Va. Code § 2.2-3700(B). I encourage {{agency_name}} to exercise its discretion to provide full contract information in the interest of public accountability.

Under Va. Code § 2.2-3704(F), please provide an itemized cost estimate if fees will exceed $200 before proceeding.

Please respond within 5 business days per Va. Code § 2.2-3704(B).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These procurement records concern the expenditure of public funds by {{agency_name}} and are a matter of significant public interest. Providing records electronically minimizes cost. I encourage the agency to exercise its permissive discretion under Va. Code § 2.2-3700(B) to waive fees in the interest of government transparency.''',
        'expedited_language': '''I request expedited processing because these procurement records are relevant to {{time_sensitive_reason}}. Delay would harm the public interest by {{harm_from_delay}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Virginia procurement VFOIA template. Key features: (1) all exemptions permissive — emphasize agency discretion; (2) trade secret claims require designation at time of submission — retroactive claims invalid; (3) contract prices and amounts paid with public funds are definitively public; (4) scoring sheets and evaluation records become public once the procurement decision is made; (5) 5-business-day deadline; (6) no administrative appeal — go to court if denied; (7) mandatory fees for prevailing requester in court action.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in VA_EXEMPTIONS:
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

    print(f'VA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in VA_RULES:
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

    print(f'VA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in VA_TEMPLATES:
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

    print(f'VA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'VA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_va', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
