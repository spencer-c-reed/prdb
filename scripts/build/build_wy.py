#!/usr/bin/env python3
"""Build Wyoming Public Records Act data: exemptions, rules, and templates.

Covers Wyoming's Public Records Act, Wyo. Stat. § 16-4-201 et seq.
Wyoming provides a broad right of public access but with notably weak
enforcement mechanisms compared to most states. The statute requires
"prompt" response without a specific number of days. No administrative appeal.
District court enforcement with reasonable fees and discretionary attorney fees.
Wyoming is considered a mid-tier transparency state — good access rights on paper
but limited practical enforcement tools.

Run: python3 scripts/build/build_wy.py
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
# Wyoming's Public Records Act, Wyo. Stat. § 16-4-201 et seq., creates a
# right of public access to all public records unless specifically exempted.
# Exemptions appear in § 16-4-203 and throughout the Wyoming statutes.
# Wyoming courts apply a presumption of openness, but the statute's weak
# enforcement mechanisms limit practical access. The burden is on the agency
# to identify and justify each claimed exemption.
# =============================================================================

WY_EXEMPTIONS = [
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(i)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(i)',
        'short_name': 'Medical and Health Records — Personal Privacy',
        'category': 'privacy',
        'description': 'Medical, dental, psychiatric, psychological, and other health records whose disclosure would constitute a clearly unwarranted invasion of personal privacy are exempt from public disclosure.',
        'scope': 'Records containing personal health information whose disclosure would constitute a "clearly unwarranted invasion of personal privacy." The standard requires balancing: not every health record automatically qualifies — the privacy interest must be substantial enough to be "clearly unwarranted." Records held by public agencies in their capacity as health care providers covering individual patient diagnosis and treatment qualify. Aggregate health statistics, operational health agency records, and records about agency programs rather than individual patients are not covered. Wyoming courts assess whether the privacy interest outweighs the public\'s interest in disclosure on a case-by-case basis.',
        'key_terms': json.dumps([
            'medical record', 'health record', 'personal privacy', 'clearly unwarranted',
            'invasion of privacy', 'dental record', 'psychiatric record',
            'mental health record', 'personal health information', 'health agency',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" invasion — not merely any privacy interest; the agency must demonstrate the privacy interest is substantial',
            'Aggregate health data and statistics without individual identifiers are not covered',
            'Operational records of public health agencies are public regardless of this exemption',
            'For public officials, health records directly relevant to their ability to perform public duties may not be protected',
            'Challenge overbroad claims that extend to administrative health agency records rather than clinical patient data',
            'The burden is on the agency to demonstrate the specific privacy harm from disclosure',
        ]),
        'notes': 'Wyo. Stat. § 16-4-203(d)(i) applies a "clearly unwarranted invasion of personal privacy" standard rather than categorical protection. Wyoming courts have interpreted this to require genuine balancing, not automatic withholding of any health-related record. Federal HIPAA requirements also apply independently to covered entities.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(ii)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(ii)',
        'short_name': 'Personnel Records — Clearly Unwarranted Privacy',
        'category': 'privacy',
        'description': 'Information in personnel files of public employees whose disclosure would constitute a clearly unwarranted invasion of personal privacy is exempt. Salary, job title, dates of employment, and disciplinary records that resulted in final employment actions are generally public.',
        'scope': 'Information in public employee personnel files whose disclosure would constitute a "clearly unwarranted invasion of personal privacy." The exemption is not categorical — it requires case-by-case assessment. Generally public: salary, job title, dates of employment, performance evaluation outcomes, and disciplinary actions that resulted in formal employment actions (termination, suspension, demotion). Generally protected: home addresses, Social Security numbers, home telephone numbers, and medical information within personnel files. Wyoming courts have held that citizens have a right to know whether public employees are performing their duties competently, which limits the privacy protection for performance and disciplinary records.',
        'key_terms': json.dumps([
            'personnel record', 'employee record', 'Social Security number', 'home address',
            'salary', 'public employee', 'disciplinary action', 'performance evaluation',
            'job title', 'compensation', 'clearly unwarranted', 'privacy',
        ]),
        'counter_arguments': json.dumps([
            'Salary, job title, and dates of employment for public employees are generally public in Wyoming',
            'Disciplinary records and their outcomes are generally public once the action is final',
            'The exemption requires case-by-case balancing — it is not a categorical shield for all personnel records',
            'The agency must release the entire record with only the specifically protected fields (SSN, home address, medical info) redacted',
            'Challenge overbroad claims that entire personnel files are exempt when only specific sensitive data fields warrant protection',
            'Wyoming courts have held that accountability for public employee performance takes precedence over privacy in most cases',
        ]),
        'notes': 'Wyoming\'s personnel records exemption requires a "clearly unwarranted invasion of personal privacy" analysis rather than categorical protection. Wyoming courts have been consistent that public employee compensation and disciplinary history are public records, applying the balancing test in favor of transparency for accountability-related information.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(iii)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(iii)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement investigations are exempt if disclosure would interfere with law enforcement proceedings, deny a person a fair trial, reveal a confidential source, disclose investigative techniques, or endanger the life of any person.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) interfere with enforcement proceedings; (2) deprive a person of a fair trial; (3) reveal the identity of a confidential informant; (4) disclose investigative techniques not generally known; or (5) endanger the life or physical safety of any person. The exemption applies to active investigations — concluded investigation files are generally public once prosecution is complete or investigation is closed. Incident reports, arrest records, and basic factual information about the existence of events are generally public regardless of investigation status.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'active investigation',
            'confidential informant', 'investigative technique', 'enforcement proceedings',
            'fair trial', 'endangerment', 'closed investigation', 'incident report',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only to active investigations — once prosecution is complete or investigation is closed, records become public',
            'Incident reports and arrest records are generally public regardless of investigation status',
            'The agency must demonstrate a specific enumerated harm for each withheld record, not assert a blanket investigative privilege',
            'Factual portions of investigative records that do not reveal informants, techniques, or endanger safety must be released',
            'Challenge claims that an investigation remains "active" when no investigative activity has occurred for an extended period',
            'Records about concluded prosecutions and their outcomes are public',
        ]),
        'notes': 'Wyo. Stat. § 16-4-203(d)(iii) is Wyoming\'s law enforcement investigative records exemption. Wyoming courts require agencies to identify the specific harm that would result from disclosure — general assertions of investigative sensitivity are insufficient. The exemption is not permanent: concluded investigation files are public.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(iv)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(iv)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information submitted to a public agency in confidence by private parties, whose disclosure would cause competitive harm, are exempt from public disclosure.',
        'scope': 'Information submitted by private parties to state agencies that constitutes a trade secret or confidential commercial or financial information whose disclosure would cause substantial competitive harm. The agency must independently evaluate whether information qualifies — submitter self-designations are not controlling. Amounts paid with public funds, contract prices, and government expenditures are generally public. Government-generated analyses based on submitted data are public even if the underlying submitted data is exempt.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'competitive harm', 'financial information',
            'proprietary information', 'confidential business information', 'competitive advantage',
            'economic value', 'secrecy', 'private submission',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must establish that the information meets the trade secret definition — mere designation is insufficient',
            'Publicly available information cannot be withheld as a trade secret',
            'Contract prices and amounts paid with public funds are public regardless of trade secret claims',
            'The agency must conduct an independent analysis — it cannot simply defer to submitter designations',
            'Challenge whether the submitter maintained reasonable secrecy measures',
            'Government analysis and reports based on submitted data are public',
        ]),
        'notes': 'Wyoming requires agencies to independently evaluate trade secret claims. The state follows the general principle that amounts paid with public funds are always public, regardless of trade secret designations for underlying product information.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(v)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(v)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memorandums relating to the deliberative process of a governmental agency, not yet adopted as agency policy, are exempt from public disclosure.',
        'scope': 'Preliminary drafts, working notes, recommendations, and intra-agency or inter-agency memorandums that: (1) are predecisional; and (2) contain opinions or recommendations rather than purely factual material. Purely factual information must be segregated and released. Final agency decisions, adopted policies, and "working law" (standards agencies actually apply) must be disclosed. The exemption protects the deliberative process — not the final product of that process. Wyoming courts apply the exemption narrowly in line with the presumption of openness.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'predecisional', 'working paper', 'recommendation', 'policy deliberation',
            'draft document', 'working law', 'opinion',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — only opinion and recommendation portions are protected',
            'Once adopted as agency policy, documents are no longer predecisional and the exemption no longer applies',
            '"Working law" — the standards and criteria actually applied — must be disclosed regardless of label',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'Documents shared outside the agency may lose their predecisional character',
        ]),
        'notes': 'Wyo. Stat. § 16-4-203(d)(v) is Wyoming\'s deliberative process exemption. Wyoming courts require the factual/opinion distinction to be applied rigorously — factual data does not become deliberative merely because it appears in a memo.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(b)(i)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(b)(i)',
        'short_name': 'Records Closed by Other Statute',
        'category': 'statutory',
        'description': 'Records that are specifically closed or made confidential by another Wyoming statute are exempt from disclosure under the Public Records Act. This cross-reference provision incorporates the many statutory confidentiality requirements throughout Wyoming law.',
        'scope': 'Any record independently made confidential or closed by a specific provision of Wyoming law other than the Public Records Act itself. Common examples include: tax return information (Wyo. Stat. § 39-11-102), juvenile records (Wyo. Stat. § 14-6-203), adoption records (Wyo. Stat. § 1-22-203), and various professional licensing and regulatory records. The agency must identify the specific other statute — a general claim of confidentiality without citation is insufficient. Agency regulations that require confidentiality but lack statutory grounding do not qualify.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'closed by statute', 'another statute',
            'cross-referenced exemption', 'statutory protection', 'confidential by law',
            'tax records', 'juvenile records', 'adoption records',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific other statute — a general claim is insufficient',
            'Agency regulations without statutory grounding do not trigger this exemption',
            'The cited statute must actually apply to the specific records at issue',
            'Challenge whether the other statute\'s confidentiality provision was intended to cover the specific context at issue',
            'Even where another statute applies, it may only protect specific fields — the remainder must be released',
        ]),
        'notes': 'Wyo. Stat. § 16-4-203(b)(i) incorporates the many confidentiality statutes scattered throughout Wyoming law. It is one of the most commonly cited exemptions because Wyoming has numerous statutes that independently protect specific categories of information. Agencies must cite the specific statute with precision.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(vi)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(vi)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records subject to the attorney-client privilege or work-product doctrine are exempt from public disclosure under the Wyoming Public Records Act.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining or providing legal advice, and work product prepared in anticipation of or in connection with litigation. The privilege for government entities requires: (1) communication between government and its attorney; (2) made in confidence; (3) for the purpose of legal advice; and (4) not waived. Billing records, retainer agreements, and general financial arrangements are not privileged. Facts underlying legal advice are not privileged. The privilege belongs to the agency and may be waived.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or administrative guidance',
            'Waiver occurs through disclosure to third parties not involved in the legal matter',
            'Attorney billing records and invoices are generally public',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis',
            'Work product requires preparation in anticipation of actual or reasonably expected litigation',
            'Challenge whether the agency constructively waived by relying on the advice in public decisions',
        ]),
        'notes': 'Wyoming recognizes attorney-client privilege and work product protection for government entities as incorporated into the Public Records Act. Wyoming courts apply the privilege narrowly given the strong disclosure presumption in the Act.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(vii)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(vii)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related valuation documents prepared by or for a government agency in connection with prospective acquisition or disposition of property are exempt until the transaction is complete or abandoned.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with anticipated government property acquisition or sale. The exemption is strictly time-limited — upon completion, cancellation, or abandonment of the transaction, all appraisal records become public. The exemption does not cover appraisals of property already owned by the agency when no acquisition or sale is contemplated.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'pre-acquisition', 'real property',
            'condemnation', 'land purchase', 'property sale',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge claims that a transaction remains "pending" with no recent activity',
            'Appraisals for property already owned by the agency are not covered',
            'Post-transaction, all valuation records are public',
        ]),
        'notes': 'Wyoming\'s pre-acquisition appraisal exemption is time-limited. It terminates automatically upon completion or abandonment of the transaction. Post-transaction, all records including internal valuations and maximum willingness-to-pay analyses are public.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 39-11-102.1(c)',
        'exemption_number': 'Wyo. Stat. § 39-11-102.1(c)',
        'short_name': 'Tax Return Information',
        'category': 'statutory',
        'description': 'State tax return information submitted to the Wyoming Department of Revenue is confidential by statute and exempt from public disclosure under the Public Records Act\'s cross-reference provision.',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individuals or businesses to the Wyoming Department of Revenue. Covers sales tax, mineral severance tax, and other state tax filings. Aggregate tax revenue statistics, enforcement orders, and final court judgments in tax disputes are public. The Department of Revenue\'s operational and enforcement records are public. Only specific taxpayer-submitted return data is protected.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'sales tax',
            'severance tax', 'taxpayer information', 'tax filing', 'tax confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Final court judgments in tax collection cases are public court records',
            'Tax enforcement orders and public sanctions are not covered',
            'The Department\'s own operations and enforcement programs are public',
            'Challenge whether specific records are actual "tax return information" versus general regulatory correspondence',
        ]),
        'notes': 'Wyo. Stat. § 39-11-102.1(c) independently requires tax return confidentiality, which is incorporated into the Public Records Act via the cross-reference exemption in § 16-4-203(b)(i). Taxpayer-specific return data is categorically protected, but aggregate data and agency operational records are public.',
    },
    {
        'jurisdiction': 'WY',
        'statute_citation': 'Wyo. Stat. § 16-4-203(d)(viii)',
        'exemption_number': 'Wyo. Stat. § 16-4-203(d)(viii)',
        'short_name': 'Security Plans and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and similar records for government facilities and critical infrastructure are exempt from public disclosure where release would create a specific and articulable security risk.',
        'scope': 'Security plans, vulnerability assessments, access control systems, and operational security documents for government facilities and critical infrastructure. The exemption requires a specific, articulable security risk — not merely that records are "security-related." Budget records, contract pricing, and expenditure data for security programs are generally public. General security policies that do not reveal specific vulnerabilities are not covered.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'access control', 'public safety', 'emergency response',
            'infrastructure protection', 'cybersecurity',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General security policies that do not reveal vulnerabilities are not covered',
            'Challenge claims that entire security contracts are exempt when only specific technical details warrant protection',
        ]),
        'notes': 'Wyoming\'s security records exemption requires a specific, articulable security risk. Agencies must identify the actual harm that would result from disclosure, not merely assert that records are security-related.',
    },
]

# =============================================================================
# RULES
# Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq.
# Wyoming requires "prompt" response without specifying a number of days —
# one of the weakest response time requirements among US states. No
# administrative appeal. District court enforcement with reasonable fees.
# Attorney's fees available but discretionary. Limited enforcement mechanisms
# overall — requesters face practical challenges enforcing rights without
# the specific deadlines and penalty structures found in stronger state laws.
# =============================================================================

WY_RULES = [
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'response_timeline',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202',
        'notes': 'Wyoming\'s Public Records Act requires agencies to respond to requests "promptly" but does not specify a number of days. This is one of the weakest statutory response-time standards among US states. In practice, what constitutes "prompt" is context-dependent: simple requests for readily available records should be filled immediately or within a few days; complex requests may require longer. Courts have not uniformly defined "promptly," making enforcement difficult. Requesters should specify a reasonable deadline in their request letter and document any delay for potential court enforcement.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'statutory_mandate',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-201',
        'notes': 'Wyo. Stat. § 16-4-201 establishes that all public records are open for inspection by any person unless specifically exempted. The statute creates a strong presumption that government records are public. The burden of demonstrating that a record is exempt falls on the agency. Courts apply this presumption actively in cases that reach litigation, but weak enforcement tools limit its practical effect for requesters who cannot afford to litigate.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202',
        'notes': 'Wyoming does not require public records requests to be submitted in writing. Oral requests are valid. However, written requests are strongly advisable — they document the scope of the request, establish a record of submission, and create the evidentiary basis for potential court enforcement. Given Wyoming\'s weak enforcement tools, documentation is particularly important.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202',
        'notes': 'Wyoming agencies may not require requesters to identify themselves or state the purpose of their request as a condition of access. The right of access under Wyo. Stat. § 16-4-201 is universal. Agencies may ask for contact information for delivery purposes but cannot condition access on identity disclosure.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-203',
        'notes': 'When a record contains both exempt and non-exempt information, Wyoming agencies must release the non-exempt portions after redacting the exempt content. Blanket withholding of entire documents because they contain some exempt material is not permissible under Wyoming law. Agencies must segregate and release all reasonably segregable non-exempt portions of records.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'fee_cap',
        'param_key': 'reasonable_fees_allowed',
        'param_value': 'actual_cost_of_reproduction',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202(d)',
        'notes': 'Wyoming agencies may charge reasonable fees for copying public records. Fees must reflect the actual cost of reproduction — paper, toner, electronic media — and may not include staff time spent locating, reviewing, or redacting records. Wyoming does not have a legislatively specified per-page copy rate; agencies set their own reasonable rates. For electronic records delivered by email, actual reproduction costs are minimal to zero. Fee waivers are within agency discretion.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202(d)',
        'notes': 'Wyoming\'s Public Records Act does not mandate fee waivers for any requester category. Agencies may waive fees at their discretion, and many do for journalists, nonprofits, and educational researchers. For electronic records, actual reproduction costs are often zero, making the fee question effectively moot for many requests.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-201 et seq.',
        'notes': 'Wyoming has NO formal administrative appeal mechanism for Public Records Act denials. There is no agency head appeal, no ombudsman, and no administrative review body. A requester denied access must file directly in district court. The absence of an administrative appeal, combined with the vague "promptly" response standard and discretionary attorney fees, makes Wyoming one of the states with the weakest practical enforcement mechanisms for public records rights.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-205',
        'notes': 'A requester denied access to public records may seek enforcement in Wyoming district court under Wyo. Stat. § 16-4-205. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may order production of records and award costs and attorney fees to a prevailing requester. Wyoming courts have jurisdiction over Public Records Act enforcement regardless of the amount in controversy. Cases are typically filed in the county where the agency is located.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_prevailing_requester',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-205',
        'notes': 'A court may award reasonable attorney fees and costs to a requester who substantially prevails in a district court enforcement action. Attorney fees in Wyoming are discretionary — the court considers whether the agency acted in good faith, the clarity of the law, and the public importance of the records. In practice, courts award fees when agencies withheld records without a reasonable legal basis. The discretionary nature of fee awards, combined with the cost of district court litigation, makes Wyoming\'s enforcement mechanism less effective than states with mandatory fee-shifting.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-201',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure rests on the agency, not the requester. Wyo. Stat. § 16-4-201 creates a strong presumption of openness. An agency claiming an exemption must identify the specific statutory provision authorizing withholding and explain how it applies to each withheld record. General claims of confidentiality without statutory citation are insufficient.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'scope_of_coverage',
        'param_value': 'public_agencies',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-201',
        'notes': 'Wyoming\'s Public Records Act applies to all "public agencies" — state agencies, counties, municipalities, school districts, and other governmental entities. The definition covers entities created by law that exercise governmental functions. Private entities performing governmental functions under contract may be covered for records relating to that function. The Act applies uniformly to state and local governmental entities throughout Wyoming.',
    },
    {
        'jurisdiction': 'WY',
        'rule_type': 'initial_response',
        'param_key': 'public_inspection_allowed',
        'param_value': 'yes_without_copying',
        'day_type': None,
        'statute_citation': 'Wyo. Stat. § 16-4-202',
        'notes': 'Wyoming\'s Public Records Act provides for both inspection and copying of public records. A person may inspect records at the agency\'s offices without paying copying fees — the right of inspection is separate from and does not require payment of copying fees. Agencies must provide reasonable facilities for public inspection. Requiring payment as a condition of inspection (rather than copying) is not permissible under Wyoming law.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

WY_TEMPLATES = [
    {
        'jurisdiction': 'WY',
        'record_type': 'general',
        'template_name': 'General Wyoming Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq.

Dear Public Records Custodian:

Pursuant to the Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes cost and production time.

I am willing to pay reasonable reproduction fees consistent with Wyo. Stat. § 16-4-202(d) (actual cost of reproduction only). I am not willing to pay for staff time spent locating, reviewing, or redacting records. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or make payment arrangements.

Under Wyo. Stat. § 16-4-201, all public records are presumptively open for inspection and the burden of demonstrating that any record is exempt rests on the agency. If any records are withheld in whole or in part, I request that you: (1) identify each withheld record; (2) state the specific statutory provision (Wyo. Stat. citation) authorizing withholding; (3) describe the record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all non-exempt, segregable portions of partially withheld records have been released.

Wyoming law requires "prompt" response. I ask that you respond as quickly as practicable — my preference would be a response within 10 business days, or written acknowledgment with a projected completion date within that time.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that reproduction fees be waived for this request. Wyoming\'s Public Records Act does not mandate fee waivers, but I ask that {{agency_name}} exercise its discretion to waive fees because:

1. The requested records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual reproduction cost is zero, making a fee waiver consistent with the statute\'s access mandate under Wyo. Stat. § 16-4-201.''',
        'expedited_language': '''I request that this request be processed as promptly as possible under Wyo. Stat. § 16-4-202\'s prompt response requirement. Expedited response is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if there are any clarifying questions that would allow faster production.''',
        'notes': 'General-purpose Wyoming Public Records Act template. Key WY features: (1) "promptly" standard — no fixed deadline; specify a reasonable timeframe in the request; (2) no administrative appeal — if denied, go directly to district court (Wyo. Stat. § 16-4-205); (3) reasonable copying fees — actual cost only, no staff time charges; (4) attorney fees discretionary for prevailing requester; (5) burden of proof on agency; (6) weak enforcement overall — consider whether AG complaint or media attention might be more effective than litigation for small requests. Reference "Wyo. Stat. § 16-4-201," not "FOIA."',
    },
    {
        'jurisdiction': 'WY',
        'record_type': 'government_accountability',
        'template_name': 'Wyoming Public Records Request — Government Contracting and Expenditure Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Government Expenditure Records, Wyo. Stat. § 16-4-201

Dear Public Records Custodian:

Pursuant to the Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq., I request copies of the following records relating to government contracting and expenditures:

{{description_of_records}}

Specifically, I request:
- Contracts, amendments, and extensions with vendors or contractors
- Invoices, payment records, and expenditure documentation
- Bid documents, proposals, and award communications
- Any sole-source justifications or waivers of competitive bidding
- Correspondence with vendors or contractors regarding contract performance, disputes, or compliance
- Any audits or reviews of contract performance

Contract/vendor (if applicable): {{contract_or_vendor}}
Time period: {{date_range_start}} through {{date_range_end}}

Note on trade secret claims: Government expenditures, contract prices, and amounts paid with public funds are public records in Wyoming regardless of any trade secret designation by the contractor. The trade secret exemption under Wyo. Stat. § 16-4-203(d)(iv) does not extend to amounts paid from public funds. If any records are withheld on trade secret grounds, please specifically identify what commercially sensitive information (beyond the pricing and expenditure data itself) you claim is protected, and explain why disclosure of that specific information would cause competitive harm.

Please respond promptly under Wyo. Stat. § 16-4-202. I welcome this request to be processed within 10 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern government expenditures — a core matter of public accountability. Electronic delivery involves zero reproduction cost. A fee waiver is consistent with Wyoming\'s presumption of openness under Wyo. Stat. § 16-4-201.''',
        'expedited_language': '''I request prompt processing under Wyo. Stat. § 16-4-202. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'Wyoming government contracting records template. Key WY points: (1) contract prices and government expenditures are always public — trade secret claims cannot shield pricing paid with public funds; (2) Wyoming\'s weak enforcement means advance documentation of requests is especially important for potential future litigation; (3) sole-source justifications and bid waivers are particularly important public accountability records; (4) no administrative appeal — district court is the only formal enforcement venue; (5) attorney fees discretionary under Wyo. Stat. § 16-4-205.',
    },
    {
        'jurisdiction': 'WY',
        'record_type': 'law_enforcement',
        'template_name': 'Wyoming Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, Wyo. Stat. § 16-4-201

Dear Public Records Custodian:

Pursuant to the Wyoming Public Records Act, Wyo. Stat. § 16-4-201 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Officer complaint and disciplinary records
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs

Regarding Wyo. Stat. § 16-4-203(d)(iii): the law enforcement investigation exemption applies only where disclosure would cause a specific enumerated harm (interference with proceedings; fair trial; revealing informant; disclosing investigative techniques; or endangering life). The agency must demonstrate the specific harm for each withheld record. Incident reports, arrest records, and basic factual information about the existence of events are generally public regardless of investigation status.

[If matter appears concluded:] If prosecution of any related matter has concluded or the investigation has been closed, the investigation exemption does not apply and all records should be produced.

Please respond promptly under Wyo. Stat. § 16-4-202. I welcome a response within 10 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern law enforcement actions and public accountability. Electronic delivery involves zero reproduction cost.''',
        'expedited_language': '''I request prompt processing under Wyo. Stat. § 16-4-202. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'Wyoming law enforcement records template. Key WY points: (1) Wyo. Stat. § 16-4-203(d)(iii) investigative exemption requires specific harm for each withheld record; (2) concluded investigation records are public; (3) incident reports and arrest records are generally public regardless of investigation status; (4) Wyoming has weak enforcement — no administrative appeal, only district court; (5) attorney fees discretionary; (6) "promptly" response standard with no defined deadline is a practical challenge — document all communications for future litigation.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in WY_EXEMPTIONS:
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

    print(f'WY exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in WY_RULES:
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

    print(f'WY rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in WY_TEMPLATES:
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

    print(f'WY templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'WY total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_wy', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
