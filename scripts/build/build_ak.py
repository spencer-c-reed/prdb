#!/usr/bin/env python3
"""Build Alaska Public Records Act data: exemptions, rules, and templates.

Covers Alaska's Public Records Act, AS 40.25.100 et seq.
Alaska amended the Act in 2020 to require agencies to respond within 10
business days (or provide a written explanation of delay). No administrative
appeal — requesters go directly to superior court. Reasonable copying charges
are allowed but staff review time may not be charged. Attorney's fees available
for prevailing requesters. The Act applies broadly to all public agencies
including municipalities.

Run: python3 scripts/build/build_ak.py
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
# Alaska's Public Records Act, AS 40.25.100 et seq., creates a broad right of
# public access. The 2020 amendment added the 10-business-day response deadline
# and strengthened enforcement. Exemptions appear both in the Act itself and
# in dozens of other statutes cross-referenced by AS 40.25.120. Courts apply
# a presumption of openness and require agencies to justify withholding with
# specificity. The Act does not have a general balancing test — exemptions
# are categorical, not discretionary.
# =============================================================================

AK_EXEMPTIONS = [
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(1)',
        'exemption_number': 'AS 40.25.120(a)(1)',
        'short_name': 'Records Privileged or Confidential by Another Statute',
        'category': 'statutory',
        'description': 'Records that are specifically made privileged or confidential by another Alaska statute are exempt from disclosure under the Public Records Act. This cross-reference provision incorporates dozens of statutory confidentiality requirements throughout Alaska law.',
        'scope': 'Any record that is independently made confidential or privileged by a specific provision of Alaska law other than the Public Records Act itself. Examples include: tax return information (AS 43.05.230), medical assistance records (AS 47.05.010), juvenile records (AS 47.12.310), and various professional licensing records. The exemption is not self-executing — the agency must identify the specific other statute that independently requires or authorizes confidentiality. A general claim that records are "confidential" without citing the applicable statute is insufficient. Records protected only by agency regulation (not statute) do not qualify.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'privileged by statute', 'another statute',
            'cross-referenced exemption', 'statutory protection', 'confidential by law',
            'AS 43.05.230', 'tax records', 'independent statutory basis',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific other statute — a general claim of confidentiality is insufficient',
            'Agency regulations that require confidentiality but are not grounded in statute do not trigger this exemption',
            'The cited statute must actually require or authorize withholding of the specific type of record requested',
            'Challenge whether the other statute\'s confidentiality provision applies to the specific records at issue or was intended to cover a different context',
            'Even where another statute applies, it may only protect specific fields or categories within a record — the remainder must be released',
        ]),
        'notes': 'AS 40.25.120(a)(1) is the gateway provision that incorporates the many confidentiality statutes scattered throughout Alaska law. It is one of the most commonly cited exemptions because Alaska has dozens of statutes that independently protect specific categories of information. The Alaska AG and courts require agencies to cite the specific "other statute" with precision.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(2)',
        'exemption_number': 'AS 40.25.120(a)(2)',
        'short_name': 'Medical and Related Records — Personal Privacy',
        'category': 'privacy',
        'description': 'Medical, dental, psychiatric, and other records whose disclosure would constitute a clearly unwarranted invasion of personal privacy are exempt from public disclosure.',
        'scope': 'Records containing personal medical, dental, psychiatric, and related health information whose disclosure would constitute a "clearly unwarranted invasion of personal privacy." The exemption requires a balancing: the privacy interest must be substantial enough to constitute a "clearly unwarranted" invasion — not merely any privacy interest. Records about private individuals\' medical treatment held by public agencies qualify. Records about agency operations, aggregate health statistics, and general public health data are not covered. The exemption does not categorically protect all health-related records — it requires case-by-case assessment of whether disclosure would be "clearly unwarranted."',
        'key_terms': json.dumps([
            'medical record', 'health record', 'personal privacy', 'clearly unwarranted',
            'invasion of privacy', 'dental record', 'psychiatric record',
            'mental health record', 'personal health information', 'privacy interest',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" invasion — not merely any privacy interest; the agency must show the privacy interest is substantial',
            'Aggregate health data and statistics without individual identifiers are not covered',
            'Operational records of public health agencies are public regardless of this exemption',
            'For public officials\' medical records where the health condition is directly relevant to their public duties, the privacy interest may be reduced',
            'Challenge overbroad claims that cover medical-related administrative records rather than actual patient clinical data',
            'The burden is on the agency to demonstrate the specific privacy harm from disclosure',
        ]),
        'notes': 'AS 40.25.120(a)(2) applies a "clearly unwarranted invasion of personal privacy" standard rather than categorical protection. Alaska courts have interpreted this to require genuine balancing, not automatic withholding of any record touching on personal matters. The standard is similar to but not identical to the federal FOIA privacy exemption.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(3)',
        'exemption_number': 'AS 40.25.120(a)(3)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement investigations are exempt if disclosure would (1) interfere with enforcement proceedings, (2) deprive a person of a fair trial, (3) reveal a confidential source, (4) reveal investigative techniques, (5) endanger law enforcement personnel, or (6) constitute an unwarranted invasion of personal privacy.',
        'scope': 'Records compiled for law enforcement purposes that would, if disclosed: (1) interfere with enforcement proceedings; (2) deprive a person of the right to a fair trial; (3) constitute an unwarranted invasion of privacy; (4) reveal the identity of a confidential informant; (5) disclose investigative techniques and procedures; or (6) endanger law enforcement personnel. Each claimed harm must be specifically demonstrated for each withheld record — blanket assertions are insufficient. The exemption is not permanent — concluded investigation files are generally public once prosecution is complete or investigation is closed. Incident reports documenting the existence and nature of events, arrest records, and basic factual information are generally public.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'active investigation',
            'confidential informant', 'investigative technique', 'enforcement proceedings',
            'fair trial', 'endanger law enforcement', 'closed investigation',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires demonstration of a specific enumerated harm — generalized claims that records are "investigative" are insufficient',
            'Concluded investigation records are public once prosecution is complete or investigation is closed',
            'Incident reports documenting existence of events and arrest records are generally public regardless of investigation status',
            'Factual portions of investigative records that do not reveal informants, techniques, or endanger safety must be released',
            'Challenge "fair trial" claims when no trial is pending or likely',
            'Alaska courts apply the exemption narrowly consistent with the presumption of openness',
        ]),
        'notes': 'AS 40.25.120(a)(3) tracks the standard law enforcement investigative records exemption. Alaska courts require agencies to demonstrate specific, articulable harm for each withheld record. The Alaska AG has issued opinions emphasizing that the exemption is not a permanent shield and that concluded investigation files are public.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(4)',
        'exemption_number': 'AS 40.25.120(a)(4)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memorandums that are predecisional and contain opinions on legal or policy matters not adopted as the agency\'s final position are exempt from public disclosure.',
        'scope': 'Preliminary drafts, working notes, recommendations, and intra-agency or inter-agency memorandums that: (1) are predecisional; and (2) contain opinions or recommendations rather than purely factual material. Purely factual information embedded in deliberative documents must be segregated and released. Final agency decisions, adopted policies, and "working law" — standards agencies actually apply — must be disclosed even if in internal documents. The exemption does not protect factual data, supporting studies, or analyses that inform agency decisions, only the opinion and recommendation portions. Alaska courts apply the exemption narrowly.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'predecisional', 'working paper', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'working law',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released',
            'Once a draft or recommendation is adopted as agency policy, the exemption no longer applies',
            '"Working law" — the criteria and standards agencies actually apply — must be disclosed regardless of label',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'Documents shared outside the agency may lose their predecisional character',
            'The agency bears the burden of demonstrating each specific document is predecisional and opinion-based',
        ]),
        'notes': 'AS 40.25.120(a)(4) is Alaska\'s deliberative process exemption. Alaska courts apply it narrowly, consistent with the strong presumption of openness in AS 40.25.100. The factual/opinion distinction is the critical analytical question: factual data does not become deliberative simply because it appears in a memo.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(5)',
        'exemption_number': 'AS 40.25.120(a)(5)',
        'short_name': 'Trade Secrets and Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and confidential commercial or financial information submitted by private parties to a government agency, whose disclosure would cause substantial competitive harm, are exempt from public disclosure.',
        'scope': 'Information submitted by private parties to state agencies that: (1) constitutes a trade secret; or (2) is confidential commercial or financial information whose disclosure would cause substantial competitive harm to the submitter. The agency must independently evaluate whether the information qualifies — vendor self-designations are not controlling. Government expenditures, contract prices, and amounts paid with public funds are generally public. Government-generated reports and analyses based on submitted data are public. The exemption requires that competitive harm be "substantial," not merely speculative.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'competitive harm', 'financial information',
            'proprietary information', 'confidential business information', 'competitive advantage',
            'economic value', 'secrecy', 'substantial harm',
        ]),
        'counter_arguments': json.dumps([
            'The competitive harm must be "substantial" — speculative or de minimis harm is insufficient',
            'The submitter must demonstrate the information meets the trade secret definition, not merely assert it',
            'Publicly available information cannot be withheld regardless of the submitter\'s characterization',
            'Contract prices and amounts paid with public funds are public regardless of trade secret claims',
            'The agency must conduct an independent analysis — it cannot defer to submitter designations',
            'Challenge whether the submitter maintained reasonable secrecy measures',
        ]),
        'notes': 'AS 40.25.120(a)(5) requires substantial competitive harm — a higher standard than some state laws. Alaska courts and the AG require agencies to conduct independent analysis of claimed trade secrets. Contract amounts paid with public funds are uniformly treated as public in Alaska.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(6)',
        'exemption_number': 'AS 40.25.120(a)(6)',
        'short_name': 'Personnel Evaluations and Complaints',
        'category': 'privacy',
        'description': 'Personnel evaluations and related records, including formal complaints against employees and the agency\'s response, are exempt until the investigation is complete or the evaluation process concludes, after which records documenting final personnel actions become public.',
        'scope': 'Personnel evaluation records, formal complaint records, and related investigative documents during the period of active investigation or evaluation. Once the personnel action is final — termination, discipline, written warning, or clearance — the record of the action and its outcome becomes public. The exemption is time-limited: it protects the process, not the final disposition. Compensation, job title, and employment status of public employees are public regardless. The names of complainants may be redacted to protect privacy, but the substance of complaints and their resolution is public once proceedings conclude.',
        'key_terms': json.dumps([
            'personnel evaluation', 'personnel complaint', 'disciplinary record',
            'employee complaint', 'internal investigation', 'public employee',
            'final personnel action', 'disciplinary proceeding', 'employment record',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is time-limited — once the personnel action is final, records of the outcome are public',
            'Salary, job title, and employment status of public employees are always public',
            'Final disciplinary actions and their outcomes are public records in Alaska',
            'Challenge claims that an evaluation or investigation remains "active" when no action has been taken for an extended period',
            'The agency must release the record of the final action even if details of the process remain protected',
        ]),
        'notes': 'AS 40.25.120(a)(6) protects the personnel evaluation and complaint process, not its outcome. The Alaska AG has confirmed that final disciplinary actions and their outcomes are public records. The time-limited nature of this exemption is important — once proceedings conclude, disclosure obligations attach to the final action.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(7)',
        'exemption_number': 'AS 40.25.120(a)(7)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related documents prepared by or for a government agency in connection with the prospective purchase, sale, or condemnation of property are exempt until the transaction is complete, abandoned, or the property is no longer under consideration.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with anticipated government acquisition or disposition of property. The exemption exists to prevent the government from being disadvantaged in property negotiations if its maximum willingness to pay is disclosed pre-transaction. It is strictly time-limited — upon completion, cancellation, or abandonment of the transaction, all appraisal records become public. The exemption does not cover appraisals of property already owned by the agency when no acquisition or sale is contemplated.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'feasibility study', 'pre-acquisition', 'real property',
            'condemnation appraisal', 'land purchase', 'property sale',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned — all appraisal records are then public',
            'Challenge the agency\'s claim that the transaction remains "pending" if there has been no activity for an extended period',
            'Appraisals for property already owned by the agency are not covered',
            'Post-transaction, all valuation records — including maximum willingness to pay — are public',
            'Budget discussions about general property value ranges may not constitute formal appraisals covered by this exemption',
        ]),
        'notes': 'AS 40.25.120(a)(7) is a standard time-limited pre-acquisition appraisal exemption. The Alaska AG has confirmed that the exemption terminates automatically upon completion or abandonment of the transaction. Post-transaction, all records including internal valuations and appraisals are public.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(8)',
        'exemption_number': 'AS 40.25.120(a)(8)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records subject to the attorney-client privilege or work-product doctrine are exempt from public disclosure under the Public Records Act. The privilege applies to confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining or providing legal advice, and work product prepared in anticipation of or in connection with litigation. Requires: (1) a communication between government and its attorney; (2) made in confidence; (3) for the purpose of legal advice (not general policy or business guidance); and (4) not subsequently waived. Attorney billing records, retainer agreements, and general financial arrangements with outside counsel are not privileged. Facts independently known are not protected merely because they were communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or administrative guidance',
            'Waiver occurs through disclosure to third parties outside the legal matter or in public proceedings',
            'Attorney billing records and invoices are generally public',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis and opinion',
            'Work product requires preparation in anticipation of actual or reasonably expected litigation',
            'Challenge whether the agency constructively waived by relying on the advice in public decision-making',
        ]),
        'notes': 'Alaska recognizes attorney-client privilege and work product protection for government entities as incorporated into the Public Records Act by AS 40.25.120(a)(8). Alaska courts apply the privilege narrowly given the strong disclosure mandate in AS 40.25.100. The privilege belongs to the agency and can be waived.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(9)',
        'exemption_number': 'AS 40.25.120(a)(9)',
        'short_name': 'Oil and Gas Geological and Geophysical Data',
        'category': 'commercial',
        'description': 'Geological and geophysical data submitted by oil and gas companies to the Alaska Department of Natural Resources or other regulatory agencies is exempt for a specified period to protect the competitive value of exploration data.',
        'scope': 'Geological, geophysical, and geochemical data submitted by private entities to state agencies in connection with oil, gas, and mineral exploration and leasing. The exemption is time-limited — data typically becomes public after a specified period (commonly 10 years for exploration data, shorter for other data types) established by the applicable regulation or statute. Aggregate resource assessments, summary findings by state agencies, and data about state-owned land produced by state employees are public. The exemption reflects Alaska\'s unique economic dependence on resource extraction and the competitive sensitivity of exploration data.',
        'key_terms': json.dumps([
            'geological data', 'geophysical data', 'oil exploration', 'gas exploration',
            'mineral exploration', 'DNR', 'exploration data', 'geochemical data',
            'resource extraction', 'competitive exploration data', 'seismic data',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is time-limited — data becomes public after the specified period, regardless of whether the company has used it',
            'State-generated resource assessments and agency analyses are public regardless of this exemption',
            'Aggregate resource data and statewide resource estimates are public',
            'Challenge claims that data remains confidential after the applicable time limit has expired',
            'Royalty and production data (amounts actually produced) are generally public once production begins',
        ]),
        'notes': 'AS 40.25.120(a)(9) reflects Alaska\'s unique context as a resource extraction economy where geological data has high commercial value. The time-limited nature is critical — the AG and DNR have confirmed that data becomes public automatically upon expiration of the applicable confidentiality period.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 43.05.230; AS 40.25.120(a)(1)',
        'exemption_number': 'AS 43.05.230',
        'short_name': 'Tax Return and Revenue Information',
        'category': 'statutory',
        'description': 'State tax return information submitted to the Department of Revenue is confidential by statute (AS 43.05.230) and therefore exempt from public disclosure under the Public Records Act\'s cross-reference provision (AS 40.25.120(a)(1)).',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individuals or businesses to the Alaska Department of Revenue. Covers income tax, oil and gas production tax, fisheries business tax, and other state tax filings. Aggregate tax revenue data, enforcement orders, and final court judgments in tax disputes are public. The Department of Revenue\'s operational and enforcement records are public. Only the specific taxpayer-submitted return information is protected.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'income tax',
            'production tax', 'taxpayer information', 'tax filing', 'AS 43.05.230',
            'tax confidentiality', 'revenue information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics are public',
            'Final court judgments in tax collection cases are public court records',
            'Tax enforcement orders and public sanctions are not protected',
            'Challenge whether requested records are "tax return information" versus general regulatory correspondence',
            'Information about the Department\'s own operations and enforcement programs is public',
        ]),
        'notes': 'AS 43.05.230 independently requires tax return confidentiality, which is incorporated into the Public Records Act exemption framework via AS 40.25.120(a)(1). This is one of the clearest and most consistently applied exemptions in Alaska public records law.',
    },
    {
        'jurisdiction': 'AK',
        'statute_citation': 'AS 40.25.120(a)(10)',
        'exemption_number': 'AS 40.25.120(a)(10)',
        'short_name': 'Security Plans and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and related records for public facilities and critical infrastructure are exempt from public disclosure where release would create a specific and articulable security risk.',
        'scope': 'Security plans, vulnerability assessments, access control systems, intrusion detection systems, and similar operational security documents for state facilities, critical infrastructure, and public safety systems. The exemption requires that disclosure create a specific, identifiable security risk — not merely that the records are "security-related." Budget records, contract pricing, and expenditure data for security programs are generally public. Physical security plans for facilities with widely known access patterns do not qualify.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'access control', 'public safety', 'emergency response',
            'infrastructure protection', 'cybersecurity', 'facility security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General security policies that do not reveal specific vulnerabilities are not covered',
            'Challenge claims that entire security vendor contracts are exempt when only specific technical specifications might warrant protection',
        ]),
        'notes': 'AS 40.25.120(a)(10) mirrors the security exemption common to most state public records laws. Alaska courts require agencies to identify the specific security risk posed by disclosure of each withheld record.',
    },
]

# =============================================================================
# RULES
# Alaska Public Records Act, AS 40.25.100 et seq.
# The 2020 amendment added a 10-business-day response deadline (previously
# no specific deadline). Agencies may provide written notice of delay with
# explanation. No administrative appeal — directly to superior court.
# Reasonable copying charges allowed but no charges for staff review time.
# Attorney's fees available for prevailing requesters.
# =============================================================================

AK_RULES = [
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'AS 40.25.110',
        'notes': 'Under the 2020 amendment to the Alaska Public Records Act, agencies must respond to public records requests within 10 business days. The response must either (1) provide the requested records; (2) acknowledge the request and provide a date by which records will be provided; or (3) deny the request in whole or in part with a written statement of the legal basis for the denial. This was a significant change from prior law, which had no specific deadline. The 10-business-day clock begins when the agency receives the request.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'written_delay_notice_allowed',
        'param_value': 'yes_with_reason',
        'day_type': None,
        'statute_citation': 'AS 40.25.110',
        'notes': 'When an agency cannot provide records within the 10-business-day response period, it must provide a written explanation of the reason for the delay and a date by which records will be available. The delay notice must be specific — agencies may not use vague language about needing "more time." Unexplained delays beyond 10 business days are not permitted under the 2020 amendment. Agencies that habitually use delay notices without producing records within the stated extension period are vulnerable to court enforcement.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'statutory_mandate',
        'day_type': None,
        'statute_citation': 'AS 40.25.100',
        'notes': 'AS 40.25.100 establishes a broad right of public access to all public records in Alaska. The statute creates a presumption that all records of public agencies are open to inspection and copying by any person. The burden of demonstrating that a record is exempt falls on the agency. Agencies must affirmatively demonstrate that a specific statutory exemption applies to each withheld record — generalized claims of confidentiality are insufficient.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'AS 40.25.110',
        'notes': 'Alaska does not require public records requests to be submitted in writing. Oral requests are valid. However, written requests are strongly advisable to document the request and establish the 10-business-day response clock. Many agencies have adopted online portals or designated public records officers for written requests, but use of these systems is not legally required.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'AS 40.25.100',
        'notes': 'Alaska agencies may not require requesters to identify themselves or state the purpose of their request as a condition of access. The right of access under AS 40.25.100 is universal. Agencies may ask for contact information for delivery purposes, but providing identity may not be a condition of access.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'AS 40.25.120',
        'notes': 'When a record contains both exempt and non-exempt information, Alaska agencies must release the non-exempt portions after redacting exempt content. Blanket withholding of entire documents because they contain some exempt material is not permissible. The agency must segregate and release all reasonably segregable non-exempt portions of records.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'fee_cap',
        'param_key': 'reasonable_copying_charges',
        'param_value': 'actual_cost_of_reproduction',
        'day_type': None,
        'statute_citation': 'AS 40.25.110(d)',
        'notes': 'Alaska agencies may charge "reasonable" fees for copying records — interpreted as the actual cost of reproduction, not staff time. Agencies may not charge for the time spent locating, reviewing, or redacting records. For electronic records delivered by email, reproduction costs are minimal to zero. Agencies must publish their fee schedules. Fees may not be used as a barrier to access — unreasonably high fees may be challenged as an improper restriction on public access rights under AS 40.25.100.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'AS 40.25.110(d)',
        'notes': 'Alaska\'s Public Records Act does not mandate fee waivers for any requester category. Agencies may waive fees at their discretion. Requesters can argue for fee waivers based on public interest grounds or when electronic delivery makes reproduction costs effectively zero. Many agencies waive fees for journalists, nonprofit organizations, and academic researchers.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'AS 40.25.100 et seq.',
        'notes': 'Alaska has NO formal administrative appeal mechanism for Public Records Act denials. There is no agency head appeal, no ombudsman, and no administrative review body. A requester denied access must go directly to superior court. This is a significant practical barrier to enforcement compared to states with administrative appeal mechanisms. The absence of an administrative appeal means that court enforcement is the only formal remedy.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'AS 40.25.151',
        'notes': 'A requester denied access to public records may seek enforcement in Alaska superior court under AS 40.25.151. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may order production of records and award attorney fees to a prevailing requester. Actions are typically filed in the judicial district where the agency is located. The court may also assess civil penalties against agencies found to have violated the Act.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_prevailing_requester',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'AS 40.25.151',
        'notes': 'A court may award reasonable attorney fees and litigation costs to a requester who prevails in a superior court enforcement action under AS 40.25.151. Attorney fees in Alaska are discretionary — the court considers whether the agency acted in good faith, the public importance of the records, and the reasonableness of the agency\'s position. In practice, courts award fees when agencies withheld records without a reasonable legal basis. The prospect of attorney fees creates an incentive for agencies to comply voluntarily with the Act.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'AS 40.25.100',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure under Alaska\'s Public Records Act rests entirely on the agency. The statute creates a strong presumption of public access. An agency claiming an exemption must identify the specific statutory provision authorizing withholding and explain how it applies to each withheld record. General assertions of confidentiality without statutory citation are insufficient under Alaska law.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'denial_must_cite_statute',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'AS 40.25.110',
        'notes': 'Under the 2020 amendment, when an Alaska agency denies a public records request in whole or in part, the written denial must state the specific legal basis for withholding. A denial that merely asserts records are "confidential" or "exempt" without citing the applicable statute is procedurally deficient. Requesters can challenge both the substantive denial and the procedural adequacy of the denial notice in superior court.',
    },
    {
        'jurisdiction': 'AK',
        'rule_type': 'initial_response',
        'param_key': 'scope_of_coverage',
        'param_value': 'public_agencies',
        'day_type': None,
        'statute_citation': 'AS 40.25.220',
        'notes': 'Alaska\'s Public Records Act applies to all "public agencies" as defined in AS 40.25.220 — state agencies, municipalities, school districts, and other governmental entities. The definition includes entities created by law that exercise governmental functions. Private entities performing governmental functions under contract may be covered for records relating to that function. The Act applies equally to municipal and state agencies, providing uniform coverage across Alaska\'s governmental structure.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

AK_TEMPLATES = [
    {
        'jurisdiction': 'AK',
        'record_type': 'general',
        'template_name': 'General Alaska Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — AS 40.25.100 et seq.

Dear Public Records Officer:

Pursuant to the Alaska Public Records Act, AS 40.25.100 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes cost and production time.

I am willing to pay reasonable fees reflecting the actual cost of reproduction consistent with AS 40.25.110(d). I am not willing to pay for staff time spent locating, reviewing, or redacting records. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under AS 40.25.100, all records of public agencies are presumptively open for public inspection. The burden of demonstrating that any record is exempt rests on the agency. If any records are withheld in whole or in part, I request that you: (1) identify each withheld record; (2) state the specific statutory basis for withholding (AS citation), not merely an exemption category; (3) describe the withheld record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all non-exempt, reasonably segregable portions of partially withheld records have been released.

Under the 2020 amendment to AS 40.25.110, please respond within 10 business days of receipt of this request. If you cannot provide records within that period, please provide written notification of the reason for delay and a date certain by which records will be available.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that reproduction fees be waived for this request. Alaska\'s Public Records Act does not mandate fee waivers, but I ask that {{agency_name}} exercise its discretion to waive fees because:

1. The requested records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual reproduction cost is zero, making a fee waiver consistent with AS 40.25.100\'s broad access mandate.''',
        'expedited_language': '''I request expedited processing of this request. The 10-business-day deadline under AS 40.25.110 is important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if there are any clarifying questions that would allow faster production.''',
        'notes': 'General-purpose Alaska Public Records Act template. Key AK features: (1) 10 business day response deadline (2020 amendment) — cite AS 40.25.110; (2) written denial must state specific statutory basis — cite the applicable AS provision; (3) no administrative appeal — must go directly to superior court under AS 40.25.151; (4) attorney fees discretionary for prevailing requester; (5) reasonable copying charges allowed but no staff time charges; (6) burden of proof on agency. Reference "AS 40.25" not "FOIA."',
    },
    {
        'jurisdiction': 'AK',
        'record_type': 'law_enforcement',
        'template_name': 'Alaska Public Records Act Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Law Enforcement Records, AS 40.25.100

Dear Public Records Officer:

Pursuant to the Alaska Public Records Act, AS 40.25.100 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs

Regarding claimed exemptions under AS 40.25.120(a)(3): the investigative records exemption requires the agency to demonstrate a specific enumerated harm for each withheld record — not merely that records are "investigative." The enumerated harms are: (1) interference with enforcement proceedings; (2) deprivation of fair trial rights; (3) clearly unwarranted invasion of personal privacy; (4) revealing identity of a confidential informant; (5) disclosing investigative techniques; or (6) endangering law enforcement personnel.

[If matter appears concluded:] If any prosecution relating to this incident has concluded or the investigation has been closed, the exemption under AS 40.25.120(a)(3) does not apply and all investigative records should be produced.

Incident reports, arrest records, and basic factual information are generally public under Alaska law regardless of investigation status.

Under AS 40.25.110 as amended in 2020, please respond within 10 business days. If records are withheld, please state the specific AS citation and demonstrate the specific harm that disclosure would cause.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern law enforcement actions and public accountability. Electronic delivery involves zero reproduction cost. A fee waiver is consistent with Alaska\'s broad public access mandate under AS 40.25.100.''',
        'expedited_language': '''I request expedited processing under the 10-business-day deadline of AS 40.25.110. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'Alaska law enforcement records template. Key AK features: (1) AS 40.25.120(a)(3) requires demonstration of specific enumerated harm for each withheld record; (2) concluded investigation records are public; (3) arrest records and incident reports are public regardless of investigation status; (4) 10-business-day response deadline; (5) denial must state specific AS citation; (6) no administrative appeal — superior court enforcement under AS 40.25.151 with discretionary attorney fees.',
    },
    {
        'jurisdiction': 'AK',
        'record_type': 'natural_resources',
        'template_name': 'Alaska Public Records Act Request — Natural Resources and Extraction Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Natural Resources Records, AS 40.25.100

Dear Public Records Officer:

Pursuant to the Alaska Public Records Act, AS 40.25.100 et seq., I request copies of the following natural resources and extraction records:

{{description_of_records}}

Relating to: {{subject_or_lease_area}}
Date range: {{date_range_start}} through {{date_range_end}}
Agency/Division (if applicable): {{agency_division}}

This request includes, but is not limited to:
- Lease agreements, royalty agreements, and related contracts
- Production reports and royalty payment records
- Environmental assessment and compliance records
- Enforcement actions and violation records
- Correspondence between the agency and lessees regarding production, compliance, or disputes

If geological, geophysical, or geochemical data is responsive to this request, I note that the exemption under AS 40.25.120(a)(9) is time-limited. Please identify any data claimed to be within an active confidentiality period and the specific period's expiration date. Any data for which the confidentiality period has expired must be produced.

Royalty and production data (amounts of resources actually produced and royalties paid to the state) are public records not subject to the geological data exemption.

Under AS 40.25.100, the burden of demonstrating any exemption rests on the agency. Under AS 40.25.110, please respond within 10 business days. If records are withheld, please state the specific AS citation and expiration date of any claimed time-limited exemption.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern natural resource extraction and public revenues — matters of core public interest in Alaska. Electronic delivery involves zero reproduction cost. A fee waiver is consistent with AS 40.25.100\'s broad access mandate.''',
        'expedited_language': '''I request prompt processing under the 10-business-day deadline of AS 40.25.110. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'Alaska natural resources records template. Alaska-specific considerations: (1) geological/geophysical data is time-limited under AS 40.25.120(a)(9) — always ask for expiration dates of claimed confidentiality periods; (2) royalty and production amounts paid to the state are always public; (3) lease terms, royalty rates, and contract provisions are public; (4) 10-business-day response deadline; (5) no administrative appeal — superior court under AS 40.25.151.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in AK_EXEMPTIONS:
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

    print(f'AK exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in AK_RULES:
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

    print(f'AK rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in AK_TEMPLATES:
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

    print(f'AK templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'AK total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ak', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
