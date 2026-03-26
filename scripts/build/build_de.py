#!/usr/bin/env python3
"""Build Delaware Freedom of Information Act data: exemptions, rules, and templates.

Covers Delaware's Freedom of Information Act (FOIA), 29 Del. Code § 10001 et seq.
Delaware FOIA requires a response within 15 business days, with extensions available.
The Attorney General's office provides an optional mediation/review mechanism (not
a formal administrative appeal). Court enforcement is in Superior Court. Copy fees
are capped at $0.25/page. Attorney's fees are available for prevailing requesters.
The AG's office issues advisory opinions on FOIA compliance.

Run: python3 scripts/build/build_de.py
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
# Delaware FOIA, 29 Del. Code § 10002(l), defines "public records" broadly and
# then provides a list of categories that are exempt. Exemptions are at
# § 10002(l)(1)-(17) and scattered elsewhere in the code. Delaware courts
# interpret FOIA exemptions narrowly. The Attorney General's office issues
# advisory opinions that provide practical guidance on exemption boundaries.
# =============================================================================

DE_EXEMPTIONS = [
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(1)',
        'exemption_number': '§ 10002(l)(1)',
        'short_name': 'Personnel Files and Employment Records',
        'category': 'privacy',
        'description': 'Personnel files and records kept by a public body relating to an employee\'s employment, including applications, promotions, disciplinary records, and performance evaluations, are exempt from FOIA to the extent they would constitute a clearly unwarranted invasion of personal privacy.',
        'scope': 'Personnel files, employment applications, performance evaluations, disciplinary records, and similar records maintained by public bodies regarding their employees. The exemption is qualified — it protects genuinely personal information but does not shield records of official conduct, compensation, or significant disciplinary actions. Delaware courts and the AG\'s office have consistently held that salary, compensation, and job title information is public. Disciplinary actions resulting in demotion, suspension, or termination are matters of public record. The exemption most clearly applies to home addresses, medical information, personal references, and the details of minor disciplinary matters that did not result in significant employment consequences.',
        'key_terms': json.dumps([
            'personnel file', 'employment record', 'performance evaluation', 'disciplinary record',
            'public employee', 'personal privacy', 'HR records', 'employee file',
            'employment application', 'termination record', 'suspension record',
        ]),
        'counter_arguments': json.dumps([
            'Salary, compensation, and job title information for public employees is always public under Delaware FOIA',
            'Disciplinary actions resulting in suspension, demotion, or termination are matters of public record',
            'Records documenting official conduct in the employee\'s government capacity are not shielded by the personnel file exemption',
            'The Delaware AG\'s office has issued advisory opinions holding that salary and compensation schedules are public',
            'Challenge blanket withholding of personnel files — the agency must identify specifically which portions qualify for the privacy exemption',
            'Policies and directives that employees are required to follow are public regardless of their location in personnel systems',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(1) is among the most frequently litigated exemptions. The Delaware AG\'s office has issued numerous advisory opinions holding that public employee compensation is public, that disciplinary records resulting in significant employment action are public, and that the exemption applies narrowly to genuinely private information. Delaware courts have consistently held that public accountability requires transparency about how agencies manage their employees.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(2)',
        'exemption_number': '§ 10002(l)(2)',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information obtained from a person that is of a privileged or confidential nature, or where disclosure would cause substantial harm to the competitive position of the submitter, are exempt from Delaware FOIA.',
        'scope': 'Trade secrets and confidential commercial or financial information submitted by private entities to Delaware public bodies. The exemption requires that the information be: (1) submitted by a private entity; (2) constitute a trade secret, privileged information, or confidential commercial/financial information; and (3) whose disclosure would cause substantial competitive harm. Amounts paid with public funds, contract prices after award, and expenditure records are uniformly public — they cannot be withheld as trade secrets. The public body must make an independent determination of trade secret claims; it may not simply defer to the submitter\'s designation.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'substantial harm',
            'competitive position', 'business confidential', 'privileged information',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts, bid results after award, and amounts paid with public funds are always public — trade secret claims do not apply',
            'The submitter must demonstrate substantial competitive harm from disclosure, not merely assert confidentiality',
            'Information that has been publicly disclosed elsewhere cannot be withheld as a trade secret',
            'Government-generated records cannot constitute trade secrets — only privately submitted information qualifies',
            'The agency must independently evaluate trade secret claims and may not simply accept vendor designations',
            'Challenge overbroad redactions where entire contracts are withheld when only narrow technical specifications might qualify',
        ]),
        'notes': 'Delaware\'s trade secret exemption in § 10002(l)(2) has been interpreted by the AG\'s office to require a showing of actual competitive harm, not merely a vendor\'s assertion of confidentiality. The AG has consistently held that contract amounts paid with public funds are public. Delaware courts and the AG\'s advisory opinion process provide useful guidance on specific trade secret claims in the government contracting context.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(3)',
        'exemption_number': '§ 10002(l)(3)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memoranda in which opinions are expressed or policies formulated that have not been adopted by the public body are exempt from Delaware FOIA\'s disclosure requirements.',
        'scope': 'Predecisional documents including drafts, internal memoranda, and recommendations that reflect the give-and-take of agency deliberation and that have not been adopted as agency policy. The exemption is limited to opinion-based and deliberative content — purely factual material must be released even if contained within a deliberative document. Delaware courts and the AG\'s office have held that once a draft or recommendation is adopted as a final decision, the exemption no longer applies. Working law — standards and criteria agencies actually apply in practice — must be disclosed even if found in internal documents.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'predecisional', 'working paper', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'opinion on policy',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — the exemption covers only opinion and deliberative portions',
            'Once a draft or recommendation is adopted as final agency policy, the exemption no longer applies',
            '"Working law" — standards and criteria agencies actually apply — must be disclosed even if found in internal documents',
            'The Delaware AG has held that factual summaries prepared to support deliberation are not covered by this exemption',
            'Challenge claims that entire documents are deliberative where only recommendation sections qualify — segregation is required',
            'Documents circulated outside the agency may lose their predecisional character',
        ]),
        'notes': 'Delaware\'s deliberative process exemption in § 10002(l)(3) tracks the federal deliberative process privilege but is applied in light of FOIA\'s disclosure mandate. The Delaware AG\'s office has issued advisory opinions emphasizing that the exemption is narrow and that factual material, even within deliberative documents, must be released. The factual/opinion distinction is a recurring issue in Delaware FOIA practice.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(6)',
        'exemption_number': '§ 10002(l)(6)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled in the regular course of an ongoing criminal investigation or prosecution are exempt from Delaware FOIA while the investigation or prosecution is pending, to the extent that disclosure would interfere with the proceeding.',
        'scope': 'Records of ongoing criminal investigations and prosecutions compiled by law enforcement agencies. The exemption applies only while the investigation or prosecution is active — once a prosecution concludes or an investigation is closed without charges, the interference rationale disappears and records generally become public under FOIA. Delaware courts have held that arrest records, basic incident information, and booking data are public regardless of investigative status. The exemption requires that disclosure would actually interfere with proceedings, not merely that records relate to an investigation.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement records', 'ongoing investigation',
            'pending prosecution', 'investigative file', 'enforcement proceeding',
            'interference with investigation', 'criminal records', 'police records',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records, booking information, and basic incident reports are public regardless of investigative status',
            'Once prosecution concludes or investigation closes, the interference rationale disappears and records are generally public',
            'The exemption requires that disclosure would actually interfere with proceedings — speculative interference is insufficient',
            'Factual information that does not reveal investigative techniques or endanger safety must be released',
            'The Delaware AG has held that police agency records that were not compiled "in the regular course of an investigation" are not covered by this exemption',
            'Challenge whether records were truly compiled for law enforcement purposes or for administrative/operational purposes',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(6) limits the law enforcement exemption to records compiled in the "regular course" of ongoing criminal investigations. The Delaware AG\'s advisory opinions and courts have consistently held that this exemption is narrow and does not protect law enforcement agency records generally — only investigative records of active criminal matters. Closed investigation records become public.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(9)',
        'exemption_number': '§ 10002(l)(9)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records subject to the attorney-client privilege or work product doctrine are exempt from Delaware FOIA. The privilege applies to confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice, and to attorney work product prepared in anticipation of litigation.',
        'scope': 'Confidential communications between public bodies and their legal counsel made for the purpose of obtaining or providing legal advice, and attorney work product prepared in anticipation of litigation or in connection with ongoing legal proceedings. The privilege requires: (1) a communication between attorney and client; (2) made in confidence; (3) for the purpose of legal advice (not general policy or business guidance). Billing records, engagement letters, and general financial arrangements with outside counsel are generally not privileged. Facts independently known to the agency are not protected merely because they were communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation privilege',
            'privileged communication', 'attorney work product', 'legal opinion',
            'government attorney', 'confidential communication', 'in anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'Communications for policy or business guidance — even from government attorneys — are not privileged',
            'Waiver occurs when the agency discloses substance in public proceedings, to non-attorney personnel not in the relationship, or to third parties',
            'Attorney billing records and invoices are generally public in Delaware under FOIA',
            'Facts independently known to the agency are not privileged',
            'The Delaware AG has held that privilege claims must be specific — blanket invocations of attorney-client privilege are insufficient',
            'Challenge whether communications labeled "legal advice" are in fact policy guidance from in-house counsel who perform dual functions',
        ]),
        'notes': 'Delaware recognizes the attorney-client privilege and work product doctrine for public bodies under § 10002(l)(9). The Delaware AG\'s office has addressed privilege claims in numerous advisory opinions, consistently holding that the privilege must be specifically invoked for each withheld document and that policy communications from government attorneys do not qualify. The purpose of the communication — legal advice versus policy guidance — is the key distinction.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(4)',
        'exemption_number': '§ 10002(l)(4)',
        'short_name': 'Medical, Psychiatric, and Health Records',
        'category': 'privacy',
        'description': 'Medical records, psychiatric and psychological records, and similar health information pertaining to identifiable individuals that are required to be kept confidential under state or federal law are exempt from Delaware FOIA.',
        'scope': 'Individually identifiable medical, psychiatric, psychological, and health records held by Delaware public bodies, including health agencies, correctional facilities, public hospitals, and any state or local agency that receives such information in the course of providing services. The exemption is supported by both FOIA and the separate confidentiality provisions of Delaware\'s health information statutes and federal HIPAA. Aggregate health statistics, anonymized public health data, and public health program documents are public. The operational records of health agencies — budgets, contracts, staffing — are public.',
        'key_terms': json.dumps([
            'medical records', 'health records', 'psychiatric records', 'treatment records',
            'health information', 'patient records', 'HIPAA', 'medical privacy',
            'mental health records', 'identifiable health information', 'health confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public and not covered by this exemption',
            'Health agency operational records, contracts, and budget documents are public regardless of this exemption',
            'Where a public official\'s medical condition is directly relevant to their fitness to perform public duties, the balance may favor disclosure',
            'Challenge claims that health agency compliance and enforcement records are protected as "medical records"',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(4) incorporates both FOIA and state/federal health information confidentiality requirements. The exemption is clearly established for individually identifiable health records. Health agency operational records are separate from patient records and are fully public under FOIA. The Delaware AG\'s office has held that the operational records of a health agency — how it spends money, how it makes decisions, how it enforces regulations — are public.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(11)',
        'exemption_number': '§ 10002(l)(11)',
        'short_name': 'Security Plans and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, or other records the disclosure of which would jeopardize the security of any public building, structure, facility, utility system, or other critical infrastructure are exempt from Delaware FOIA.',
        'scope': 'Security plans, vulnerability assessments, access control system details, intrusion detection configurations, and similar records for public buildings and critical infrastructure where disclosure would directly enable a security breach. The exemption applies narrowly to records whose disclosure would jeopardize security — not to all security-related records. Budget records and expenditure data for security programs are public. General descriptions of security policies that do not reveal specific vulnerabilities are public. The agency must demonstrate that the specific information would enable a specific harm.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security threat', 'public building security', 'facility security',
            'cyber security', 'infrastructure protection', 'access control',
        ]),
        'counter_arguments': json.dumps([
            'The threat must be specific and articulable — a general assertion that records relate to "security" is insufficient',
            'Budget and expenditure records for security programs are public',
            'General security policy descriptions that do not reveal specific vulnerabilities are not covered',
            'Challenge claims that entire contracts with security vendors are exempt when only narrow technical specifications qualify',
            'Security audit reports that identify systemic problems may be subject to partial disclosure with specific vulnerability details redacted',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(11) is applied narrowly by Delaware courts and the AG\'s office consistent with the overall disclosure mandate of FOIA. Agencies must demonstrate a specific connection between disclosure and a concrete security threat. The AG\'s office has held that security-related records are not categorically exempt — only specific records whose disclosure would directly jeopardize security qualify.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(7)',
        'exemption_number': '§ 10002(l)(7)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals, feasibility studies, and related valuation documents prepared by or for a public body in connection with the prospective acquisition, sale, or lease of real property are exempt until the transaction is complete or abandoned.',
        'scope': 'Formal real estate appraisals, property valuations, and related documents prepared for a Delaware public body in connection with a pending acquisition or sale of real property. The exemption is temporary — it expires when the transaction is complete, abandoned, or the property is no longer being actively pursued. The purpose is to prevent agencies from being disadvantaged in negotiation if their maximum willingness to pay is disclosed. After transaction completion or abandonment, all appraisal and valuation records are public under FOIA.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'feasibility study', 'pre-acquisition appraisal',
            'real property purchase', 'land purchase', 'condemnation appraisal',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, abandoned, or no longer being actively pursued',
            'Challenge the agency\'s claim that the transaction remains "pending" if there has been no active negotiation or legislative action for an extended period',
            'Post-condemnation judgment, all valuation records are public',
            'Budget documents and legislative appropriations for property acquisition are public',
            'Appraisals for property already owned by the agency and not in active acquisition or sale mode are not covered',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(7) is a well-established, time-limited exemption. The AG\'s office has confirmed that the exemption automatically expires upon transaction completion and that post-transaction appraisals are fully public. The exemption protects formal valuation documents, not general budget discussions or legislative testimony about property values.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(5)',
        'exemption_number': '§ 10002(l)(5)',
        'short_name': 'Test Questions and Examination Data',
        'category': 'commercial',
        'description': 'Test questions, scoring keys, and other examination data used to administer licensing examinations, civil service examinations, or academic examinations by public bodies are exempt from Delaware FOIA to preserve the integrity and validity of the examinations.',
        'scope': 'Questions, scoring keys, model answers, and related examination materials used in active examinations administered by or on behalf of Delaware public bodies. The exemption applies prospectively to questions that remain in active use. Past examination questions that will not be reused generally become public after the examination cycle closes. Aggregate examination results, pass/fail statistics, and score distributions are public. The exemption does not cover examination policies, content outlines, or general descriptions of examination subjects.',
        'key_terms': json.dumps([
            'test questions', 'examination data', 'scoring key', 'licensing examination',
            'civil service examination', 'academic examination', 'employment test',
            'examination integrity', 'answer key', 'standardized test',
        ]),
        'counter_arguments': json.dumps([
            'Examination questions from past administrations that will not be reused are generally public',
            'Aggregate pass/fail rates, score distributions, and examination statistics are public',
            'General information about examination structure, content areas, and format is public',
            'Examination scoring policies and grading criteria in general terms are public',
            'The Delaware AG has held that the exemption applies only to examination questions that remain in active use',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(5) protects the integrity of government-administered examinations. The AG\'s office has confirmed that the exemption is prospective — it protects questions in current active use, not questions from past administrations. The exemption does not extend to examination program administration, scoring methodology in general terms, or aggregate performance statistics.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(12)',
        'exemption_number': '§ 10002(l)(12)',
        'short_name': 'Library Patron Records',
        'category': 'privacy',
        'description': 'Library circulation records and other records identifying what materials a library patron has accessed, borrowed, or requested from a public library are exempt from Delaware FOIA to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying specific library patrons\' borrowing, access, or inquiry activity at public libraries. Covers circulation records, electronic database access logs, interlibrary loan records, and reference inquiries that reveal the reading interests of identifiable individuals. Aggregate usage statistics, collection data, and general program information are public. Library administrative records, budget documents, and personnel files are public. The exemption extends to digital resource access logs consistent with its purpose of protecting intellectual privacy.',
        'key_terms': json.dumps([
            'library records', 'circulation records', 'library patron', 'borrower records',
            'database access', 'intellectual privacy', 'reading privacy', 'interlibrary loan',
            'library privacy', 'patron confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library usage statistics and collection data are public and not covered',
            'Library administrative records, budget documents, and contracts are fully public',
            'The exemption covers patron-specific reading records, not library operations or system administration',
            'Records pursuant to a court order in a criminal investigation may be disclosed consistent with that order',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(12) reflects the strong public policy protecting library patron privacy. The exemption is absolute for patron-specific reading records — there is no balancing test. Delaware\'s library privacy protection is consistent with similar provisions in most states and reflects the principle that individuals should be able to access information without fear of government surveillance.',
    },
    {
        'jurisdiction': 'DE',
        'statute_citation': '29 Del. Code § 10002(l)(16)',
        'exemption_number': '§ 10002(l)(16)',
        'short_name': 'Collective Bargaining Negotiation Records',
        'category': 'deliberative',
        'description': 'Records of labor relations negotiations and collective bargaining strategy documents prepared by or for a public body in connection with pending collective bargaining negotiations are exempt from Delaware FOIA while negotiations are ongoing.',
        'scope': 'Strategy documents, negotiating positions, and related records prepared for use in collective bargaining negotiations between public employers and employee unions. The exemption is temporary — it applies while negotiations are actively ongoing. Once a collective bargaining agreement is ratified or negotiations conclude without agreement, the exemption expires and negotiation records generally become public. Final collective bargaining agreements, pay scales, and terms of employment under negotiated contracts are fully public. The exemption does not cover general employment policies or already-adopted compensation schedules.',
        'key_terms': json.dumps([
            'collective bargaining', 'labor negotiations', 'union negotiations',
            'bargaining strategy', 'negotiating position', 'labor relations',
            'collective bargaining agreement', 'pending negotiations', 'public employer',
        ]),
        'counter_arguments': json.dumps([
            'Final collective bargaining agreements, adopted pay scales, and ratified contract terms are public',
            'Once negotiations conclude — whether by agreement or impasse — the exemption expires',
            'General employment policies and previously adopted compensation schedules are public regardless of this exemption',
            'Challenge claims that the exemption continues to apply after negotiations have concluded or been suspended for an extended period',
            'Budget documents and appropriations for collective bargaining settlements are public',
        ]),
        'notes': 'Delaware FOIA § 10002(l)(16) is a negotiations-in-progress exemption that expires when collective bargaining is complete. The AG\'s office has confirmed that final contracts are public and that the exemption is limited to the active negotiation period. This exemption is frequently relevant in the context of public school district and municipal labor relations in Delaware.',
    },
]

# =============================================================================
# RULES
# Delaware Freedom of Information Act, 29 Del. Code § 10001 et seq.
# Key features: 15-business-day initial response deadline; extensions available with
# notice; Attorney General mediation/advisory opinions (voluntary); no formal admin
# appeal; Superior Court enforcement; $0.25/page copy fee cap; attorney's fees for
# prevailing requesters.
# =============================================================================

DE_RULES = [
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': '29 Del. Code § 10003(h)(1)',
        'notes': 'Delaware public bodies must respond to FOIA requests within 15 business days of receipt. The response must either produce the records, deny the request with specific statutory justification, or notify the requester that an extension is being taken. A failure to respond within 15 business days constitutes a constructive denial that the requester may appeal to the Attorney General or challenge in Superior Court. The 15-business-day clock begins on the date the request is received.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'extension_available',
        'param_value': 'yes_upon_written_notice',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(h)(2)',
        'notes': 'Delaware public bodies may extend the response deadline when necessary to respond to a complex or voluminous request. The extension must be communicated to the requester in writing before the initial 15-business-day deadline expires, and must state the reason for the extension and provide an estimated date of production. There is no specified maximum extension period in the statute, but extensions must be reasonable. Unreasonable extensions may be challenged before the Attorney General or in Superior Court as constructive denials.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_statutory_citation',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(h)(3)',
        'notes': 'Delaware public bodies must provide a written denial that cites the specific statutory exemption under which records are being withheld, citing the specific subsection of 29 Del. Code § 10002(l). A denial must explain how the claimed exemption applies to the withheld records and advise the requester of the right to appeal to the Attorney General or seek judicial review in Superior Court. A generic denial without specific citation is legally insufficient and may constitute an independent violation.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10005(c)',
        'notes': 'The burden of demonstrating that any record is exempt from public access under Delaware FOIA rests on the public body, not on the requester. The agency must affirmatively demonstrate that a specific exemption in 29 Del. Code § 10002(l) applies to each specific withheld record. General assertions that records fall within broad exemption categories are insufficient. The AG\'s advisory opinion process reinforces this burden — the AG consistently holds that agencies must specifically justify each denial.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(g)',
        'notes': 'Delaware public bodies must release all nonexempt portions of records when only part of a record qualifies for an exemption under FOIA. The agency must redact exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is a FOIA violation. The agency must identify which portions are being withheld and under what specific statutory authority. The Delaware AG\'s office regularly enforces the segregability requirement in advisory opinions.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(a)',
        'notes': 'Delaware\'s FOIA grants access rights to "any citizen." In practice, the AG\'s office and Delaware courts have not construed this requirement to exclude non-Delaware residents from making FOIA requests, though the statutory language technically limits the right to citizens. Agencies may not require requesters to state the purpose of their request. Providing contact information for delivery purposes is practical but cannot be required as a condition of access.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_cap_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(m)',
        'notes': 'Delaware FOIA caps copy fees at $0.25 per page for paper copies. This is among the higher per-page caps in the region, though still modest. Agencies may not charge for staff time spent locating, reviewing, or redacting records. For electronic records, agencies may charge for the cost of the medium (disc, thumb drive) but not for the time spent creating the electronic copy. Many agencies provide electronic records by email at no charge. Fee schedules must be published and may not include labor costs.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fees',
        'param_value': 'not_permitted',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(m)',
        'notes': 'Delaware agencies may not charge for staff time spent searching for, locating, reviewing, or redacting records in response to a FOIA request. The $0.25/page cap covers only the actual cost of reproduction. Fee assessments that include labor costs for document review or redaction may be challenged as unlawful barriers to FOIA access. The AG\'s office has addressed fee-related complaints and consistently held that only actual reproduction costs are chargeable.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_news_media',
        'param_value': 'available_by_agency_discretion',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(m)',
        'notes': 'Delaware\'s FOIA does not mandate fee waivers for news media or any other requester category. However, agencies may waive or reduce fees at their discretion. News media organizations, nonprofits, and academic researchers commonly receive fee waivers in practice. For electronic records delivered by email, actual cost is typically zero. Requesters should affirmatively request a fee waiver, explain the public interest basis, and note that electronic delivery incurs no reproduction cost.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'appeal_deadline',
        'param_key': 'attorney_general_review',
        'param_value': 'voluntary_advisory_opinion_available',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10005(e)',
        'notes': 'Delaware\'s Attorney General\'s office provides an optional mediation and advisory opinion process for FOIA complaints. A requester who is denied access may petition the AG\'s office for review. The AG\'s office will review the denial and issue an advisory opinion on whether the public body complied with FOIA. This is NOT a formal administrative appeal — the AG\'s opinion is advisory and not binding on the public body. However, AG opinions carry significant persuasive weight and public bodies generally comply. The AG process is faster and cheaper than Superior Court litigation and should normally be attempted first.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'appeal_deadline',
        'param_key': 'ag_review_filing_deadline',
        'param_value': '60_calendar_days_from_denial',
        'day_type': 'calendar',
        'statute_citation': '29 Del. Code § 10005(e)',
        'notes': 'A requester seeking an AG advisory opinion must file within 60 calendar days of the denial or constructive denial. The AG\'s office has an established process for reviewing FOIA complaints, which includes providing the public body an opportunity to respond. The AG typically issues opinions within 60-90 days of receipt. The AG\'s opinion database is publicly accessible and provides a body of precedent on common exemption questions.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10005(a)',
        'notes': 'A requester may seek judicial enforcement of Delaware FOIA in Superior Court. The court conducts a de novo review and may conduct in camera inspection of withheld records. The requester need not exhaust the AG advisory opinion process before filing in Superior Court, though the AG process is generally faster and less expensive. If the court finds that the agency improperly denied access, it may order production and award attorney\'s fees and costs to the prevailing requester.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'discretionary_award_available',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10005(b)',
        'notes': 'A court may award reasonable attorney\'s fees and costs to a requester who substantially prevails in a Delaware FOIA enforcement action in Superior Court. The award is discretionary — courts consider whether the agency\'s denial was justified, the public interest served by the requester\'s suit, and whether the requester acted reasonably in seeking access. Delaware courts have been willing to award fees where agencies engaged in unjustified withholding or categorical denial of clearly public records.',
    },
    {
        'jurisdiction': 'DE',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '29 Del. Code § 10003(a)',
        'notes': 'Delaware FOIA encompasses electronic records. Public bodies must provide access to records in electronic format when requested and when records exist in electronic form. Agencies may not require requesters to accept paper copies when electronic records are available and electronic delivery is feasible. For most electronic records, delivery by email incurs no reproduction cost. The AG\'s office has consistently held that electronic records are fully subject to FOIA.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

DE_TEMPLATES = [
    {
        'jurisdiction': 'DE',
        'record_type': 'general',
        'template_name': 'General Delaware FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Coordinator (or Custodian of Records)
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — 29 Del. Code § 10001 et seq.

Dear FOIA Coordinator:

Pursuant to the Delaware Freedom of Information Act (FOIA), 29 Del. Code § 10001 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional context:
{{additional_context}}

I request that records be provided in electronic format (via email or download link) where available and where records exist in electronic form. Electronic delivery minimizes both cost and production time.

I am willing to pay copying fees at the rate established by 29 Del. Code § 10003(m) ($0.25 per page for paper). I am not willing to pay for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Delaware FOIA. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under 29 Del. Code § 10005(c), the burden of demonstrating that any record is exempt from public access rests on your agency. If any records or portions of records are withheld, I request that you:
(1) identify each record withheld by description;
(2) state the specific statutory exemption under which records are being withheld, citing the precise subsection of 29 Del. Code § 10002(l);
(3) confirm that all nonexempt, reasonably segregable portions of partially withheld records have been released; and
(4) advise me of my right to seek review through the Attorney General\'s office under 29 Del. Code § 10005(e) or judicial review in Superior Court under 29 Del. Code § 10005(a).

Under 29 Del. Code § 10003(h)(1), you must respond to this request within 15 business days of receipt. If additional time is needed, please provide timely written notice of the extension consistent with § 10003(h)(2). Failure to respond within 15 business days constitutes a constructive denial.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Delaware\'s FOIA does not mandate fee waivers, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is effectively zero, making a fee waiver consistent with the letter and spirit of 29 Del. Code § 10003(m).

I appreciate your consideration of this fee waiver request.''',
        'expedited_language': '''I request that this FOIA request be processed as expeditiously as possible within the 15-business-day statutory deadline. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are questions that might allow faster production.''',
        'notes': 'General-purpose Delaware FOIA template. Key DE features: (1) 15-business-day response deadline — cite 29 Del. Code § 10003(h)(1); (2) extensions must be communicated in writing before the deadline; (3) no formal administrative appeal — AG advisory opinion process is optional but recommended as faster/cheaper than litigation; (4) $0.25/page copy fee cap — cite § 10003(m); (5) no search/retrieval fees; (6) attorney\'s fees for prevailing requesters in Superior Court; (7) AG opinions are advisory but carry strong persuasive weight. The AG opinion database is a valuable resource for understanding DE FOIA exemption boundaries. Reference "FOIA" and cite 29 Del. Code, not federal FOIA.',
    },
    {
        'jurisdiction': 'DE',
        'record_type': 'law_enforcement',
        'template_name': 'Delaware FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Coordinator
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records, 29 Del. Code § 10001 et seq.

Dear FOIA Coordinator:

Pursuant to the Delaware Freedom of Information Act (FOIA), 29 Del. Code § 10001 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Body-worn camera footage and associated metadata
- Written communications (email, radio logs) relating to the above
- Officer disciplinary records for involved personnel
- Internal affairs investigation records relating to the above incident

Regarding the law enforcement exemption at 29 Del. Code § 10002(l)(6): Delaware FOIA does not permit blanket withholding of law enforcement records. The exemption applies only to records compiled in the "regular course" of ongoing criminal investigations where disclosure would actually interfere with proceedings. It does not protect: (1) records of concluded investigations or prosecutions; (2) arrest records, booking information, and basic incident reports; (3) records not compiled for law enforcement purposes.

Any withholding under § 10002(l)(6) requires specific identification of the harm that disclosure would cause and the specific record to which the exemption applies — not a categorical assertion that records relate to "a law enforcement matter."

Under 29 Del. Code § 10003(g), all nonexempt, segregable portions of partially withheld records must be released. Under 29 Del. Code § 10005(c), the burden of demonstrating any exemption rests on your agency.

Please respond within 15 business days per 29 Del. Code § 10003(h)(1). I am willing to pay fees per § 10003(m) up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this law enforcement records request. These records concern {{public_interest_explanation}}, a matter of public accountability for government conduct. Electronic delivery incurs no reproduction cost. I appreciate your consideration of this fee waiver request.''',
        'expedited_language': '''I request expedited processing within the 15-business-day statutory deadline. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}. Please contact me if questions might allow faster production.''',
        'notes': 'Delaware law enforcement records template under FOIA. Key DE law enforcement records features: (1) § 10002(l)(6) applies only to records compiled in the "regular course" of ongoing criminal investigations — not all police records; (2) arrest records, booking data, and incident reports are public; (3) completed investigation files are generally public once prosecution concludes; (4) specific harm justification required for each withheld record; (5) AG advisory opinion process available as alternative to litigation — faster and less expensive; (6) 15-business-day deadline; (7) $0.25/page fee cap.',
    },
    {
        'jurisdiction': 'DE',
        'record_type': 'government_contracts',
        'template_name': 'Delaware FOIA Request — Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Coordinator
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Government Contracts and Procurement Records, 29 Del. Code § 10001 et seq.

Dear FOIA Coordinator:

Pursuant to the Delaware Freedom of Information Act (FOIA), 29 Del. Code § 10001 et seq., I request the following records relating to government contracts and procurement:

{{description_of_records}}

This request includes, but is not limited to:
- All contracts, amendments, and purchase orders with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Payment records, invoices, and expenditure reports for the above contracts
- Procurement records including solicitations, bids received, bid evaluations, and award justifications
- Correspondence between the agency and {{vendor_or_contractor}} relating to contract performance
- Any audits, performance reviews, or contract evaluations

Note on trade secret claims: Pursuant to the Delaware AG\'s advisory opinions, amounts paid with public funds, bid results after contract award, and government expenditure records are not protectable trade secrets under 29 Del. Code § 10002(l)(2). Any trade secret claim requires demonstration of substantial competitive harm from disclosure, not merely a vendor\'s confidentiality designation. The agency must independently evaluate such claims.

Under 29 Del. Code § 10005(c), the burden of demonstrating any exemption rests on your agency. Under § 10003(g), all nonexempt, segregable portions of withheld records must be released.

Please respond within 15 business days per 29 Del. Code § 10003(h)(1). I am willing to pay fees per § 10003(m) up to ${{fee_limit}}, with electronic delivery preferred.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this government contracting records request. These records concern {{public_interest_explanation}}, a matter of accountability for how Delaware government spends public money. Electronic delivery incurs no reproduction cost. The AG\'s FOIA advisory opinions consistently recognize that government expenditure records are at the core of FOIA\'s purpose. I appreciate your consideration.''',
        'expedited_language': '''I request prompt processing within the 15-business-day statutory deadline. Prompt production is important because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Delaware government contracts/procurement template under FOIA. Key points: (1) contract amounts and public expenditure data are always public — cite the AG\'s advisory opinion body to reinforce this; (2) trade secret claims require specific harm demonstration; (3) bid results after award are public; (4) AG advisory opinion process is available and often faster than litigation for contract-related disputes; (5) 15-business-day deadline; (6) $0.25/page fee cap; (7) attorney\'s fees available in Superior Court for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in DE_EXEMPTIONS:
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

    print(f'DE exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in DE_RULES:
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

    print(f'DE rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in DE_TEMPLATES:
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

    print(f'DE templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'DE total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_de', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
