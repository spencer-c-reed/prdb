#!/usr/bin/env python3
"""Build Massachusetts Public Records Law data: exemptions, rules, and templates.

Covers the Massachusetts Public Records Law, M.G.L. c. 66 § 10, and the
exemptions under M.G.L. c. 4 § 7(26). Massachusetts underwent significant
reform in 2016 (chapter 121 of the Acts of 2016), adding firm deadlines,
fee caps, and enhanced enforcement.

Run: python3 scripts/build/build_ma.py
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
# Massachusetts exemptions are codified at M.G.L. c. 4 § 7(26)(a)-(r) (and beyond).
# The 2016 reform did not change the exemptions but significantly changed procedure.
# =============================================================================

MA_EXEMPTIONS = [
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(a)',
        'exemption_number': '(26)(a)',
        'short_name': 'National Security / Specifically Exempted',
        'category': 'statutory',
        'description': 'Records specifically or by necessary implication exempted from disclosure by statute, including records relating to national security and those whose disclosure would endanger national security.',
        'scope': 'Records that are specifically exempted by state or federal statute, or by necessary implication from a statute. Also covers records whose disclosure would endanger the security of the Commonwealth or the United States. This catch-all for statutory exemptions requires the agency to identify the specific statute or security basis — general confidentiality policies do not qualify.',
        'key_terms': json.dumps([
            'national security', 'specifically exempted', 'statute', 'by necessary implication',
            'security of the Commonwealth', 'federal statute', 'confidential by law',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that creates the exemption — "necessary implication" is a high standard',
            'Speculative or generalized security concerns do not meet the national security threshold',
            'Challenge whether the cited statute actually prohibits disclosure or merely regulates the information',
            'The Massachusetts Supervisor of Records has narrowly construed statutory exemptions and required agencies to show the cited statute directly applies',
        ]),
        'notes': 'Unlike the federal FOIA Exemption 1 (classified information), the MA exemption is not limited to formally classified materials. The security prong is rarely invoked at the state and local level. The statutory prong parallels NY § 87(2)(a). See Supervisor of Records ADV-2019-01.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(b)',
        'exemption_number': '(26)(b)',
        'short_name': 'Personnel and Medical Files',
        'category': 'privacy',
        'description': 'Personnel and medical files or information, and any other materials or data relating to a specifically named individual, the disclosure of which may constitute an unwarranted invasion of personal privacy.',
        'scope': 'Personnel files, medical files, and any individually identified data where disclosure would constitute an unwarranted invasion of personal privacy. Massachusetts courts apply a balancing test weighing the individual\'s privacy interest against the public interest in disclosure. Public employees have reduced privacy expectations for records of their official conduct. Salary and job title are generally public; disciplinary records of public employees are frequently disclosable after the balancing test.',
        'key_terms': json.dumps([
            'personnel file', 'medical file', 'personal privacy', 'unwarranted invasion',
            'individual data', 'privacy interest', 'public employee', 'balancing test',
            'home address', 'medical information',
        ]),
        'counter_arguments': json.dumps([
            'Massachusetts courts apply a balancing test: articulate a specific public interest in disclosure to tip the balance',
            'Public employees have minimal privacy interests in their official duties, compensation, and professional conduct',
            'Salary, title, and disciplinary records of public employees are generally not protected under this exemption',
            'Home addresses of private individuals receive stronger protection than professional contact information',
            'The word "unwarranted" imports a balancing test — not every privacy invasion justifies withholding',
            'Records that document an employee\'s official conduct are distinct from truly personal medical or financial information',
            'Challenge broad withholding of entire personnel files when only specific personal information qualifies',
        ]),
        'notes': 'The most frequently invoked Massachusetts exemption. The Supreme Judicial Court has held that public officials have reduced privacy expectations for records of their official conduct. See Hastings & Sons Publishing Co. v. City Treasurer of Lynn, 374 Mass. 812 (1978). The 2016 reform did not change the exemption but added enhanced enforcement.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(c)',
        'exemption_number': '(26)(c)',
        'short_name': 'Investigatory Materials — Law Enforcement',
        'category': 'law_enforcement',
        'description': 'Investigatory materials necessarily compiled out of the public view by law enforcement or other investigatory officials where the prospect of enforcement proceedings is more likely than not.',
        'scope': 'Materials compiled for law enforcement purposes, where the prospect of enforcement proceedings is more likely than not (i.e., a concrete, likely enforcement action, not mere possibility). Covers active criminal investigations, regulatory enforcement investigations, and similar proceedings. The "more likely than not" standard is higher than the mere possibility of enforcement. Factual portions may be segregable.',
        'key_terms': json.dumps([
            'investigatory materials', 'law enforcement', 'enforcement proceedings',
            'out of public view', 'more likely than not', 'criminal investigation',
            'regulatory investigation', 'compiled for investigation',
        ]),
        'counter_arguments': json.dumps([
            'The "more likely than not" standard requires a concrete, likely enforcement action — not speculative future enforcement',
            'Once proceedings conclude (prosecution dropped, settlement, acquittal), the rationale evaporates',
            'Factual portions of investigative records that do not reveal sources or methods are segregable',
            'Records created before an investigation began do not qualify as "compiled out of the public view" for the investigation',
            'Challenge whether enforcement proceedings are genuinely more likely than not, particularly for old or stagnant investigations',
            'The Supervisor of Records has held that mere regulatory oversight, without a specific enforcement target, does not qualify',
        ]),
        'notes': 'The "more likely than not" standard is stricter than the federal FOIA Exemption 7 standard (records compiled for law enforcement purposes). Massachusetts courts have required a concrete, articulable likelihood of enforcement proceedings. See District Attorney for the Norfolk District v. Flatley, 419 Mass. 507 (1995).',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(d)',
        'exemption_number': '(26)(d)',
        'short_name': 'Deliberative Process / Inter-Agency Materials',
        'category': 'deliberative',
        'description': 'Inter-agency or intra-agency memoranda or letters relating to policy positions being developed by the agency; but not factual staff reports or facts underlying policy positions, or records of final agency decisions.',
        'scope': 'Predecisional deliberative communications, including internal memoranda, drafts, recommendations, and communications between agency officials in the process of formulating policy. Does NOT protect: factual reports or underlying facts; records of final agency decisions; instructions to staff that affect the public; or external audits. Factual material must be segregated and released. The exemption is strictly for the deliberative (opinion and recommendation) components.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'inter-agency', 'intra-agency', 'draft',
            'policy development', 'recommendation', 'memorandum', 'internal communication',
            'opinion', 'advisory', 'working paper',
        ]),
        'counter_arguments': json.dumps([
            'Factual material embedded in deliberative documents must be segregated and released — Massachusetts law expressly excludes factual staff reports from this exemption',
            'Records of final agency decisions are not protected, even if they were once part of a deliberative process',
            'A document adopted as the agency\'s final position or working law must be disclosed',
            'Challenge attempts to shield entire documents when only recommendations or opinions qualify',
            'The Supervisor of Records has required agencies to produce factual summaries from otherwise exempt deliberative documents',
        ]),
        'notes': 'Massachusetts courts have applied this exemption narrowly to the truly deliberative (opinion/recommendation) elements of internal communications. The express exclusion of factual staff reports is a significant limitation. See Attorney General v. School Committee of Northampton, 375 Mass. 127 (1978).',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(e)',
        'exemption_number': '(26)(e)',
        'short_name': 'Real Estate Appraisals',
        'category': 'commercial',
        'description': 'Real estate appraisals or preliminary plans, and decisions to acquire real property, are exempt until the property has been acquired or the project has been abandoned.',
        'scope': 'Real estate appraisals, preliminary plans for real estate acquisitions, and agency decisions to acquire real property, during the period prior to acquisition or abandonment of the project. The exemption is strictly time-limited: it expires when the agency completes the acquisition or formally abandons it. Protects against strategic use of publicly known appraisal values in negotiations.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'preliminary plan', 'appraisal report',
            'real property', 'eminent domain', 'land acquisition',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is time-limited: once acquisition is complete or the project is abandoned, all appraisals and plans become public',
            'Post-acquisition disclosure requests cannot be denied under this exemption',
            'Challenge claims that a project has not been "abandoned" when it has been inactive for a significant period',
            'Related environmental and planning documents that do not reveal acquisition strategy are not covered',
        ]),
        'notes': 'Narrow, time-limited exemption. One of the clearer exemptions in the Massachusetts statute because its temporal scope is explicit. See Supervisor of Records, Decision No. 99-001.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(f)',
        'exemption_number': '(26)(f)',
        'short_name': 'Attorney-Client Privilege / Work Product',
        'category': 'deliberative',
        'description': 'Communications between a government agency and its legal counsel, and attorney work product, protected by the attorney-client privilege.',
        'scope': 'Attorney-client communications made in confidence for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege belongs to the agency (the client) and may be waived. Does not protect facts known to the attorney that were not disclosed in confidence for legal advice purposes.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'counsel', 'legal opinion', 'confidential',
        ]),
        'counter_arguments': json.dumps([
            'Challenge whether the communication was made for the purpose of obtaining legal advice — business or policy advice does not qualify',
            'Waiver: if the agency disclosed the legal advice publicly or acted on it in a public proceeding, privilege may be waived',
            'Billing records and retainer agreements are generally not privileged',
            'Facts known to the attorney that were obtained outside the privileged relationship are not protected',
            'The government attorney-client privilege is narrower than its private counterpart in Massachusetts',
        ]),
        'notes': 'Massachusetts courts have applied the attorney-client privilege to government entities but with some skepticism about overbroad claims. See Suffolk Construction Co. v. Division of Capital Asset Management, 449 Mass. 444 (2007).',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(g)',
        'exemption_number': '(26)(g)',
        'short_name': 'Trade Secrets / Commercial or Financial Information',
        'category': 'commercial',
        'description': 'Trade secrets and confidential commercial or financial information submitted to an agency where disclosure would harm the competitive position of the submitting entity.',
        'scope': 'Confidential commercial or financial information submitted by a private entity to a public agency, where disclosure would cause substantial competitive harm. The information must be: (1) commercial or financial in nature; (2) submitted in confidence; and (3) likely to cause substantial competitive injury if disclosed. Government-generated financial records are generally not covered.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information', 'competitive harm',
            'proprietary', 'confidential business', 'submitted in confidence', 'competitive injury',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate substantial competitive harm, not mere inconvenience or embarrassment',
            'Information in the public domain or known to competitors cannot be a trade secret',
            'Government-generated records reflecting the agency\'s analysis of private data are not "submitted by" a private entity',
            'The agency must make its own independent determination — it cannot simply defer to a submitter\'s "confidential" designation',
            'Contract prices and performance data may be public regardless of the submitter\'s commercial sensitivity claims',
        ]),
        'notes': 'Massachusetts courts apply a substantial competitive harm standard. See Babets v. Secretary of the Executive Office of Human Services, 403 Mass. 230 (1988).',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(h)',
        'exemption_number': '(26)(h)',
        'short_name': 'Appraisals / Examination of Financial Institutions',
        'category': 'commercial',
        'description': 'Examination and supervisory records of the Office of the Commissioner of Banks and related financial institution regulators, including bank examination reports.',
        'scope': 'Reports and records from the examination of financial institutions by state banking regulators, including the Division of Banks. Covers examination reports, supervisory correspondence, and records of regulatory enforcement proceedings against financial institutions.',
        'key_terms': json.dumps([
            'bank examination', 'financial institution', 'Division of Banks', 'supervisory record',
            'regulatory examination', 'bank regulator', 'supervisory correspondence',
        ]),
        'counter_arguments': json.dumps([
            'Publicly filed regulatory orders, consent agreements, and enforcement actions are not covered',
            'Aggregate or anonymized data from bank examinations is generally disclosable',
            'Challenge claims that routine correspondence with a financial institution is "examination" material',
        ]),
        'notes': 'Narrow exemption for bank regulatory records. Similar exemptions exist in many states to protect the integrity of bank examination processes and prevent market panic. Final enforcement orders are public.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(i)',
        'exemption_number': '(26)(i)',
        'short_name': 'Proposals and Bids',
        'category': 'commercial',
        'description': 'Proposals and bids to provide goods or services to a public agency are exempt until the procurement process is complete.',
        'scope': 'Proposals and bids submitted in response to competitive solicitations, until the contract is awarded or the procurement is otherwise concluded. Similar to Florida\'s sealed bid exemption but applies during the entire procurement period. Once the procurement is complete, all bids and proposals are fully public.',
        'key_terms': json.dumps([
            'bid', 'proposal', 'procurement', 'competitive solicitation', 'contract award',
            'RFP', 'RFQ', 'ITB', 'sealed bid', 'vendor proposal',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the procurement is complete — request records after contract award',
            'After award, all bids and proposals are public, including losing bids',
            'Challenge attempts to extend the exemption indefinitely to avoid disclosure of procurement records',
        ]),
        'notes': 'Time-limited procurement exemption. Massachusetts has robust procurement transparency requirements that take effect post-award. See M.G.L. c. 30B (Uniform Procurement Act).',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(j)',
        'exemption_number': '(26)(j)',
        'short_name': 'Abode / Place of Employment of Victims',
        'category': 'privacy',
        'description': 'The residential address or place of employment of a person who has been the victim of a criminal offense, where disclosure would endanger the safety of the victim.',
        'scope': 'Home addresses and workplace locations of crime victims, where disclosure would endanger their safety. Also covers similar information for witnesses who have requested protection. Applied broadly to victims of domestic violence, sexual assault, stalking, and other violent crimes. The safety endangerment requirement must be credible and specific.',
        'key_terms': json.dumps([
            'victim address', 'residential address', 'place of employment', 'victim safety',
            'crime victim', 'domestic violence', 'witness protection', 'endangered',
        ]),
        'counter_arguments': json.dumps([
            'The safety endangerment requirement must be credible — the agency cannot withhold addresses based on speculative risk',
            'Other information in the record about the crime or prosecution remains public',
            'Challenge attempts to withhold entire records on the ground that they contain a victim\'s address',
        ]),
        'notes': 'Similar to Florida\'s victim privacy exemption but requires a nexus to specific safety endangerment. Massachusetts courts have broadly construed "endangered" in the domestic violence context.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(n)',
        'exemption_number': '(26)(n)',
        'short_name': 'Library Circulation Records',
        'category': 'privacy',
        'description': 'Library circulation records and other records identifiable to a patron that reveal what materials a library patron has borrowed or used.',
        'scope': 'Records maintained by public libraries that identify which library materials an individual patron has borrowed, accessed, or requested. Protects intellectual privacy and freedom of inquiry. Does not protect aggregate library use statistics or records about library operations.',
        'key_terms': json.dumps([
            'library circulation', 'library patron', 'borrowed materials', 'library record',
            'reading privacy', 'intellectual privacy', 'patron record',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate or anonymized statistics about library use are not covered',
            'Records about library operations, staff conduct, or administrative functions are not patron records',
        ]),
        'notes': 'Strong intellectual privacy protection. Massachusetts courts and the Supervisor of Records have consistently applied this exemption broadly to protect patron privacy. The exemption reflects First Amendment concerns about chilling the freedom to read.',
    },
    {
        'jurisdiction': 'MA',
        'statute_citation': 'M.G.L. c. 4 § 7(26)(o)',
        'exemption_number': '(26)(o)',
        'short_name': 'Homeland Security Vulnerability Assessments',
        'category': 'safety',
        'description': 'Records or portions thereof relating to homeland security including security plans, security procedures, and vulnerability assessments for critical infrastructure.',
        'scope': 'Security plans, procedures, and vulnerability assessments for critical infrastructure, including water systems, power grids, transportation infrastructure, and government facilities. Also covers cybersecurity vulnerability information. The agency must demonstrate that disclosure would create a specific, articulable security risk.',
        'key_terms': json.dumps([
            'homeland security', 'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security procedure', 'cybersecurity', 'infrastructure protection',
        ]),
        'counter_arguments': json.dumps([
            'Challenge claims that routine operational records constitute a "vulnerability assessment"',
            'General facility information that is publicly known is not covered',
            'Expenditure records for security contracts are public — only technical security details qualify',
            'Challenge overly broad invocations that sweep in entire program files',
        ]),
        'notes': 'Added to the Massachusetts exemptions after 9/11. Construed broadly by the Supervisor of Records in security-sensitive contexts but limited to actual security planning documents.',
    },
]

# =============================================================================
# RULES
# Massachusetts Public Records Law, M.G.L. c. 66 § 10
# Major reform: Acts of 2016, c. 121 (effective January 1, 2017)
# =============================================================================

MA_RULES = [
    {
        'jurisdiction': 'MA',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'M.G.L. c. 66 § 10(b)',
        'notes': 'Following the 2016 reform (Acts of 2016, c. 121), agencies must respond to public records requests within 10 business days. The response must either produce the records, deny the request with written reasons citing specific exemptions, or provide an explanation of why more time is needed (with a specific extension period). This was a significant improvement from the pre-2016 standard of "within a reasonable time."',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'initial_response',
        'param_key': 'max_extension_days',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'M.G.L. c. 66 § 10(b)(viii)',
        'notes': 'If an agency cannot respond within 10 business days, it may extend the deadline by up to 15 additional business days by providing written notice that explains the reason for the extension. The notice must include a specific date by which the response will be provided. Further extensions may be available for very large or complex requests with Supervisor of Records approval.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'initial_response',
        'param_key': 'large_request_extension',
        'param_value': 'supervisor_approval_required',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(b)(ix)',
        'notes': 'For unusually voluminous or complex requests that cannot be fulfilled within the 15-business-day extension, agencies must seek approval from the Supervisor of Records for additional time. The Supervisor may grant a reasonable extension, subject to ongoing production requirements. The agency cannot simply sit on large requests indefinitely.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'appeal_deadline',
        'param_key': 'supervisor_of_records_appeal',
        'param_value': 'mandatory_before_court',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10A',
        'notes': 'Before filing a court action, a requester MUST appeal to the Supervisor of Records (within the Secretary of State\'s office). The Supervisor of Records appeal is mandatory — courts have dismissed direct petitions that bypass the Supervisor. The Supervisor reviews the denial, may order production, and issues written decisions. The Supervisor\'s decisions are publicly available and serve as persuasive authority.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'appeal_deadline',
        'param_key': 'supervisor_response_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'M.G.L. c. 66 § 10A(b)',
        'notes': 'After receiving a Supervisor of Records appeal, the Supervisor must issue a written determination within 10 business days (for state agencies) or 30 calendar days (for municipalities and other governmental bodies). In complex cases, the Supervisor may issue a preliminary ruling ordering interim production.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_review',
        'param_value': 'after_supervisor_denial',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10A(d)',
        'notes': 'After the Supervisor of Records issues a decision, either party may seek review in Superior Court. The standard of review is de novo. The 2016 reform also authorized the Supervisor of Records to assess civil penalties against agencies that fail to comply with Supervisor decisions, and to refer matters to the Attorney General for enforcement.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_if_prevails',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10A(d)',
        'notes': 'A requester who prevails in court may be awarded reasonable attorney fees and costs. Fee awards are discretionary but frequently granted where the agency had no reasonable basis for withholding. The 2016 reform made fee awards more common by clarifying the standard. Agencies that simply capitulate after a court action is filed may still face fee liability.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_standard',
        'param_value': '0.05',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(d)',
        'notes': 'Massachusetts has the lowest statutory copy fee in the nation: $0.05 per page for standard paper copies. This cap was set in 1973 and has never been adjusted for inflation. Agencies may not charge more than $0.05 per page for paper copies. Many agencies waive this fee for small requests as a matter of practice.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_records_fee',
        'param_value': 'actual_cost_of_electronic_production',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(d)',
        'notes': 'For electronic records, agencies may charge the actual cost of electronic production, including costs of conversion if necessary. However, agencies may not charge for the cost of reviewing records to determine if they are exempt — that is part of the agency\'s duty. The 2016 reform clarified that if records are already in electronic form, the cost of transmitting them via email is essentially zero.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fee',
        'param_value': 'for_public_entities_only',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(d)',
        'notes': 'The 2016 reform allows agencies to charge a "reasonable fee" for employee time spent searching and retrieving records for large or complex requests, at a rate not exceeding $25/hour (or $10/hour for municipalities). Agencies must notify requesters of anticipated fees over $10 before proceeding. The first 4 hours of search/retrieval time must be provided free of charge.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'yes_supervisory_discretion',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(d)(iii)',
        'notes': 'The 2016 reform allows agencies to waive fees for requesters who demonstrate financial hardship. The Supervisor of Records has authority to order fee waivers. In practice, many state agencies waive fees for journalists, nonprofits, and academic researchers as a matter of policy. There is no automatic fee waiver category equivalent to federal FOIA\'s news media category.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'expedited_processing',
        'param_key': 'expedited_statutory',
        'param_value': 'none_explicit',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10',
        'notes': 'Massachusetts does not have a statutory expedited processing provision. However, the 10-business-day deadline is already relatively short, and requesters may ask agencies to prioritize time-sensitive requests. The Supervisor of Records has authority to issue preliminary orders in urgent cases.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10(b)(iii)',
        'notes': 'Agencies must release all reasonably segregable, nonexempt portions of records. When withholding parts of a document, the agency must redact only the exempt portions and produce the rest. Blanket withholding of documents containing some exempt material is improper. The agency must provide a written explanation of what was withheld and why.',
    },
    {
        'jurisdiction': 'MA',
        'rule_type': 'appeal_deadline',
        'param_key': 'supervisor_civil_penalties',
        'param_value': 'up_to_1000_per_day',
        'day_type': None,
        'statute_citation': 'M.G.L. c. 66 § 10A(e)',
        'notes': 'The 2016 reform added civil penalty authority to the Supervisor of Records. The Supervisor may assess civil penalties of up to $1,000 per day against agencies that fail to comply with Supervisor orders. Penalties are paid to the Commonwealth (not the requester), but the threat of penalties is a significant enforcement lever added by the reform.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

MA_TEMPLATES = [
    {
        'jurisdiction': 'MA',
        'record_type': 'general',
        'template_name': 'General Massachusetts Public Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — M.G.L. c. 66 § 10

Dear Public Records Access Officer:

Pursuant to the Massachusetts Public Records Law, M.G.L. c. 66 § 10, I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I prefer to receive records in electronic format (PDF or native format) where available, which is lower cost for both of us.

I am willing to pay reasonable fees up to ${{fee_limit}}. Under M.G.L. c. 66 § 10(d), the fee for paper copies may not exceed $0.05 per page. If you anticipate fees exceeding $10.00, please notify me before proceeding so I may refine my request.

If any records are withheld, please: (1) identify each record withheld; (2) cite the specific exemption under M.G.L. c. 4 § 7(26) or other applicable provision for each withheld record; (3) release all nonexempt portions of any partially exempt records; and (4) state whether a more narrowly tailored request would yield additional records.

Under M.G.L. c. 66 § 10(b), I request a response within 10 business days. If you cannot respond within 10 business days, please provide written notice of the extension and a specific date by which you will respond, as required by § 10(b)(viii).

Thank you for your attention to this request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that any fees be waived for this request. I am {{requester_category_description}} and am requesting these records in the public interest to {{public_interest_explanation}}.

Under M.G.L. c. 66 § 10(d)(iii), the Supervisor of Records has authority to order fee waivers for requesters who demonstrate financial hardship or a compelling public interest. I request that the agency exercise its discretion to waive fees here because disclosure of these records will contribute to public understanding of {{subject_matter_explanation}}.

Even without a waiver, Massachusetts law limits paper copy fees to $0.05 per page — among the lowest in the nation. I ask that if a waiver is not granted, fees be calculated at the statutory minimum.''',
        'expedited_language': '''I request that this public records request be processed with priority. Although Massachusetts law does not have a formal expedited processing provision, I ask that the agency act promptly on this request because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

The 10-business-day statutory deadline under M.G.L. c. 66 § 10(b) already reflects a legislative judgment in favor of prompt production, and I ask that the agency honor that intent here.''',
        'notes': 'General-purpose Massachusetts public records template. Key Massachusetts-specific features: (1) mandatory administrative appeal to Supervisor of Records before court action; (2) $0.05/page copy fee cap — cite it; (3) 10-business-day deadline post-2016 reform; (4) correct title is "Public Records Access Officer" (some agencies use "Records Officer"). Reference M.G.L. c. 66 § 10, not "FOIA."',
    },
    {
        'jurisdiction': 'MA',
        'record_type': 'appeal',
        'template_name': 'Massachusetts Appeal to Supervisor of Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Supervisor of Records
Office of the Secretary of the Commonwealth
One Ashburton Place, Room 1719
Boston, MA 02108
publicrecords@sec.state.ma.us

Re: Appeal of Public Records Denial — {{agency_name}} — Request dated {{original_request_date}}

Dear Supervisor of Records:

Pursuant to M.G.L. c. 66 § 10A, I am appealing the denial/failure to respond to my public records request submitted to {{agency_name}} on {{original_request_date}}.

FACTUAL BACKGROUND

On {{original_request_date}}, I submitted a public records request to {{agency_name}} requesting:

{{description_of_records}}

On {{response_date}}, {{agency_name}} {{description_of_denial_or_nonresponse}}.

[If no response: As of {{date}}, {{agency_name}} has not responded to my request, which was submitted more than 10 business days ago in violation of M.G.L. c. 66 § 10(b).]

BASIS FOR APPEAL

{{appeal_arguments}}

The agency's reliance on {{exemption_cited}} is misplaced for the following reasons:

{{exemption_challenge_arguments}}

RELIEF REQUESTED

I respectfully request that the Supervisor of Records:

1. Order {{agency_name}} to produce the requested records in full within a specific, prompt time period;
2. Find that {{agency_name}}'s denial was improper and that no applicable exemption under M.G.L. c. 4 § 7(26) applies to the withheld records;
3. [If appropriate:] Assess civil penalties against {{agency_name}} pursuant to M.G.L. c. 66 § 10A(e) for failure to respond within the statutory deadline.

I also request that the Supervisor order {{agency_name}} to release all reasonably segregable nonexempt portions of any partially exempt records, and to provide a written log identifying each withheld record and the specific exemption claimed for each.

Enclosed: Copy of original request, copy of agency response (if any), and any related correspondence.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Massachusetts requires a mandatory appeal to the Supervisor of Records BEFORE filing a court action. This template is for that mandatory administrative appeal. The Supervisor is within the Secretary of the Commonwealth\'s office. The appeal triggers the Supervisor\'s 10-business-day response period for state agencies (30 calendar days for municipalities). Civil penalties of up to $1,000/day are available post-2016 reform. Include copies of all prior correspondence. Supervisor decisions are publicly available at sec.state.ma.us/pre.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in MA_EXEMPTIONS:
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

    print(f'MA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in MA_RULES:
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

    print(f'MA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in MA_TEMPLATES:
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

    print(f'MA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'MA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ma', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
