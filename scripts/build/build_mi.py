#!/usr/bin/env python3
"""Build Michigan FOIA exemptions, rules, and templates.

Michigan Freedom of Information Act, MCL 15.231-15.246.
Michigan's FOIA is disclosure-presumptive with enumerated exemptions.
One of the few states with mandatory punitive damages for arbitrary denials.

Run: python3 scripts/build/build_mi.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')


MI_EXEMPTIONS = [
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(a)',
        'exemption_number': '§ 15.243(1)(a)',
        'short_name': 'Invasion of Privacy',
        'category': 'privacy',
        'description': 'Protects information of a personal nature where the public disclosure of the information would constitute a clearly unwarranted invasion of an individual\'s privacy.',
        'scope': 'Personal information whose disclosure would be a clearly unwarranted invasion of privacy. Michigan courts apply a balancing test: the privacy interest must outweigh the public benefit of disclosure. Commonly applied to home addresses of private individuals, medical information, Social Security numbers, and personal financial details. Public employees retain minimal privacy interests in records of their official conduct.',
        'key_terms': json.dumps([
            'personal nature', 'unwarranted invasion', 'privacy', 'personal information',
            'home address', 'Social Security number', 'medical information', 'financial records',
        ]),
        'counter_arguments': json.dumps([
            'The invasion must be "clearly unwarranted" — the standard is higher than mere embarrassment or discomfort',
            'Public employees and officials have reduced privacy expectations in records of their official duties and compensation',
            'The public interest in accountability can override privacy interests — articulate a specific public benefit',
            'Salary, title, and disciplinary information for public employees is generally not protected',
            'Redaction of identifying information (name, address) while releasing substantive content is a less restrictive alternative',
            'Challenge whether the record truly contains "personal" information vs. records of official governmental action',
        ]),
        'notes': 'The Michigan Supreme Court in Bradley v. Saranac Community Schools Bd of Ed, 455 Mich 285 (1997) held that public employees have reduced privacy expectations. The "clearly unwarranted" standard is more stringent than a mere "unwarranted" standard — agencies must show the privacy invasion is obvious and substantial.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(b)',
        'exemption_number': '§ 15.243(1)(b)',
        'short_name': 'Investigating Records',
        'category': 'law_enforcement',
        'description': 'Protects investigating records compiled for law enforcement purposes to the extent that production would: interfere with law enforcement proceedings; deprive a person of a fair trial; constitute an unwarranted invasion of privacy; disclose confidential sources; disclose investigative techniques; or endanger law enforcement personnel.',
        'scope': 'Law enforcement investigation records where disclosure would: (i) interfere with enforcement proceedings; (ii) deprive a person of a right to a fair trial or impartial adjudication; (iii) constitute a clearly unwarranted invasion of personal privacy; (iv) disclose the identity of a confidential source; (v) disclose investigative techniques or procedures not generally known; or (vi) endanger law enforcement personnel. The exemption is qualified — agencies must show specific harm, not just invoke law enforcement status.',
        'key_terms': json.dumps([
            'investigating records', 'law enforcement', 'compiled for law enforcement',
            'confidential source', 'investigative techniques', 'fair trial',
            'endanger personnel', 'interference with proceedings',
        ]),
        'counter_arguments': json.dumps([
            'Records must be "compiled for law enforcement purposes" — not all police records qualify automatically',
            'Once proceedings conclude, the interference rationale evaporates for subsection (i)',
            'Factual portions of investigation files are generally segregable from protected deliberative content',
            'Routine investigative techniques that are publicly known do not qualify for protection',
            'Challenge whether harm from disclosure is specific and articulable, not speculative',
            'Completed investigations lose much of their protection — press for disclosure after case closure',
            'The agency must demonstrate each specific harm, not just assert the law enforcement label',
        ]),
        'notes': 'Michigan courts have interpreted this exemption consistently with the federal FOIA Exemption 7 framework. Key distinction: the exemption is permissive, and Michigan FOIA\'s default is disclosure. Agencies must show the specific subsection harm that applies.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(c)',
        'exemption_number': '§ 15.243(1)(c)',
        'short_name': 'Attorney-Client / Work Product',
        'category': 'deliberative',
        'description': 'Protects records or information specifically described as exempt from disclosure by statute or subject to a legally recognized privilege, including attorney-client communications and attorney work product.',
        'scope': 'Communications between an attorney and public body client that are subject to the attorney-client privilege, and attorney work product prepared in anticipation of litigation or for trial. Also covers records exempt by other specific statutes. The privilege in the government context is treated similarly to private-party privilege, but courts scrutinize overbroad claims.',
        'key_terms': json.dumps([
            'attorney-client', 'work product', 'legal advice', 'privileged communication',
            'litigation preparation', 'confidential communication', 'counsel',
        ]),
        'counter_arguments': json.dumps([
            'The privilege protects confidential communications seeking or giving legal advice — not all communications with attorneys qualify',
            'Factual information conveyed to an attorney does not automatically become privileged',
            'Work product protection applies only to documents prepared in anticipation of litigation, not routine legal work',
            'If the communication was disclosed to third parties, the privilege may be waived',
            'Final agency policy decisions reflected in legal advice may lose protection as "working law"',
            'Challenge whether the agency has actually established the specific elements of attorney-client privilege for each record',
        ]),
        'notes': 'Michigan FOIA § 15.243(1)(c) incorporates privileges recognized in law. Courts have held that the government attorney-client privilege is real but not unlimited — agencies cannot use it as a blanket shield for all attorney correspondence.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(d)',
        'exemption_number': '§ 15.243(1)(d)',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Protects records of a public body\'s personnel director relating to the examination, operating, or condition of employment of public employees, including performance evaluations.',
        'scope': 'Personnel records including performance evaluations, disciplinary files, employment history, and similar HR records. However, Michigan law also provides that basic public employee information — name, salary, title, dates of employment — is public. The exemption covers the more sensitive personnel file contents, not the basic employment facts.',
        'key_terms': json.dumps([
            'personnel', 'employment', 'performance evaluation', 'disciplinary record',
            'personnel director', 'HR records', 'employee records', 'employment condition',
        ]),
        'counter_arguments': json.dumps([
            'Basic employment information (name, salary, title, dates of employment) is public regardless of this exemption',
            'Final disciplinary actions resulting in termination or suspension are often public under Michigan case law',
            'Public officials\' conduct in their official capacity carries reduced protection',
            'Personnel records relating to misconduct that affects the public interest may tip toward disclosure',
            'Challenge the agency to distinguish between genuinely sensitive personal employment information and records of official misconduct',
        ]),
        'notes': 'Michigan has a separate Personnel Records Act (MCL 423.501 et seq.) governing employee access to their own records. Under FOIA, third-party requests for personnel records must navigate both statutes. Bradley v. Saranac and its progeny address the public employee privacy balance.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(e)',
        'exemption_number': '§ 15.243(1)(e)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Protects trade secrets or commercial or financial information voluntarily submitted to an agency, where disclosure would impair the government\'s ability to obtain necessary information or cause substantial harm to the competitive position of the submitting person.',
        'scope': 'Trade secrets and confidential commercial or financial information submitted to a public body by a private person or entity, where disclosure would: (1) impair the government\'s ability to obtain similar information in the future, or (2) cause substantial competitive harm to the submitter. Both prongs are independently sufficient. Information that is publicly available cannot be confidential.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information', 'competitive position',
            'voluntarily submitted', 'proprietary', 'competitive harm', 'confidential business',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate substantial competitive harm — not mere embarrassment or inconvenience',
            'Information already in the public domain cannot qualify as a trade secret',
            'Government-generated analysis of private submissions is not itself a trade secret',
            'The portions of a contract reflecting public expenditures are not protectable as trade secrets',
            'Challenge whether the information was truly "voluntarily" submitted or was required by law',
            'Boilerplate "proprietary" labels from contractors do not establish trade secret status',
            'The agency, not the submitter, makes the disclosure determination',
        ]),
        'notes': 'Michigan\'s trade secret exemption parallels the federal FOIA Exemption 4 structure. The Michigan Uniform Trade Secrets Act (MCL 445.1901) provides the underlying definition of "trade secret" — information that derives independent economic value from not being generally known.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(f)',
        'exemption_number': '§ 15.243(1)(f)',
        'short_name': 'Deliberative Process',
        'category': 'deliberative',
        'description': 'Protects intra-agency memoranda or letters that would not be routinely available by law to a private party in litigation with the public body, including advisory opinions, recommendations, and deliberations.',
        'scope': 'Predecisional, deliberative communications within a public body — draft documents, policy recommendations, advisory opinions, and internal deliberations that have not become final agency policy. Factual portions of deliberative documents must be segregated and released. Once a document is adopted as final policy, it loses its predecisional character.',
        'key_terms': json.dumps([
            'intra-agency', 'memoranda', 'advisory opinion', 'recommendation', 'deliberative',
            'predecisional', 'draft', 'internal deliberation', 'policy recommendation',
        ]),
        'counter_arguments': json.dumps([
            'Factual content embedded in a deliberative document must be segregated and released',
            'A document adopted as final agency policy is no longer predecisional and must be released',
            '"Working law" — internal rules that guide agency decisions — must be disclosed even if deliberative in form',
            'Challenge whether the document is truly predecisional or reflects a final determination',
            'External consultants\' reports submitted to an agency are not "intra-agency" materials',
            'Instructions to staff that affect the public must be released regardless of their deliberative character',
        ]),
        'notes': 'Michigan\'s deliberative process exemption is similar to federal FOIA Exemption 5\'s deliberative process component. Courts require the agency to show the document is both predecisional (prepared before a final decision) and deliberative (part of the decision-making process).',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(g)',
        'exemption_number': '§ 15.243(1)(g)',
        'short_name': 'Test Questions',
        'category': 'examination',
        'description': 'Protects test questions, scoring keys, and other examination data used to administer a licensing examination, employment examination, or academic examination before the examination is given or until the examination is no longer in use.',
        'scope': 'Test questions, answer keys, and examination materials for licensing, employment, and academic tests. The protection applies before the exam is administered and for as long as the exam remains in active use. Once the exam is retired, the rationale for withholding dissolves.',
        'key_terms': json.dumps([
            'test questions', 'scoring key', 'examination', 'licensing exam', 'employment test',
            'academic examination', 'before administration', 'exam security',
        ]),
        'counter_arguments': json.dumps([
            'Once the examination is no longer in active use, the exemption no longer applies',
            'Past exam editions that have been retired should be disclosed upon request',
            'Scoring rubrics, passing score thresholds, and general exam structure may not be "questions or keys"',
            'Challenge whether the specific materials requested are questions/keys vs. administrative records about the exam',
        ]),
        'notes': 'Narrow exemption protecting test integrity. Similar to NY § 87(2)(h). The exemption is explicitly time-limited by the phrase "until the examination is no longer in use."',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(h)',
        'exemption_number': '§ 15.243(1)(h)',
        'short_name': 'Real Estate Purchase Negotiations',
        'category': 'commercial',
        'description': 'Protects appraisals or negotiation strategies for real property purchases by a public body before the transaction is concluded or abandoned.',
        'scope': 'Real estate appraisals and negotiation strategies prepared for a public body in connection with a potential property acquisition. The exemption protects only pre-transaction materials — once the purchase is concluded or the deal falls through, the records are generally disclosable. Prevents strategic disclosure that could inflate prices or compromise negotiations.',
        'key_terms': json.dumps([
            'real property', 'appraisal', 'negotiation', 'purchase', 'acquisition',
            'real estate', 'property value', 'pending transaction',
        ]),
        'counter_arguments': json.dumps([
            'Once the transaction concludes or is abandoned, the exemption no longer applies',
            'Challenge whether the transaction is truly "pending" vs. already completed',
            'Post-transaction appraisals and final purchase prices are public records',
            'General property records not related to a specific pending acquisition are not covered',
        ]),
        'notes': 'Time-limited exemption protecting active real estate negotiations. Rationale is that disclosure of appraisals during negotiations could harm taxpayers by revealing the maximum price the government would pay.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(i)',
        'exemption_number': '§ 15.243(1)(i)',
        'short_name': 'Archaeology and Historic Sites',
        'category': 'safety',
        'description': 'Protects records the disclosure of which would jeopardize the security of a facility or system, including archaeological sites and historic properties.',
        'scope': 'Information about the location or description of archaeological sites, burial grounds, and sacred sites where disclosure could facilitate looting or vandalism. Also covers security-sensitive information about government facilities. Michigan has a strong tradition of protecting tribal archaeological sites under this exemption.',
        'key_terms': json.dumps([
            'archaeological site', 'burial ground', 'sacred site', 'security', 'facility security',
            'historic property', 'looting', 'vandalism', 'site location',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'General descriptions of archaeological methodology or findings without site location details may not qualify',
            'Academic or scientific records that do not reveal precise locations may be disclosable',
            'Challenge whether the specific information in the record, rather than the record generally, creates the security risk',
        ]),
        'notes': 'Michigan has significant archaeological resources including Native American burial grounds. This exemption is frequently invoked by DNR and tribal governments. Similar protections exist under the Native American Graves Protection and Repatriation Act (federal).',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(l)',
        'exemption_number': '§ 15.243(1)(l)',
        'short_name': 'Library Records',
        'category': 'privacy',
        'description': 'Protects library records identifying a library patron\'s borrowing habits or use of library information services.',
        'scope': 'Records of library circulation, computer usage, research queries, and similar records that would identify what an individual patron has borrowed, accessed, or inquired about. Covers public library records. The exemption reflects the First Amendment concern that disclosure of reading habits chills intellectual freedom.',
        'key_terms': json.dumps([
            'library record', 'patron', 'borrowing', 'circulation', 'reading habits',
            'library use', 'intellectual freedom', 'library privacy',
        ]),
        'counter_arguments': json.dumps([
            'Statistical or aggregate data that does not identify individual patrons is not protected',
            'Administrative and operational records about library functions (not patron use) are not covered',
            'Challenge whether the specific record identifies an individual\'s library use or is just a general library operational record',
        ]),
        'notes': 'Michigan Library Privacy Act (MCL 397.601) provides additional protection for library records beyond FOIA. Courts have held that protecting reading habits is essential to First Amendment values. Law enforcement access to library records requires a court order.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(m)',
        'exemption_number': '§ 15.243(1)(m)',
        'short_name': 'Medical/Mental Health Records',
        'category': 'privacy',
        'description': 'Protects information about a person\'s medical, psychiatric, or psychological history, diagnosis, condition, treatment, or evaluation.',
        'scope': 'Medical and mental health records, including diagnoses, treatment records, psychiatric evaluations, counseling records, and similar health information. Also covers information about substance abuse treatment. Protecting medical privacy is among the strongest privacy interests under Michigan FOIA.',
        'key_terms': json.dumps([
            'medical record', 'psychiatric', 'psychological', 'diagnosis', 'treatment',
            'mental health', 'counseling', 'health information', 'substance abuse',
        ]),
        'counter_arguments': json.dumps([
            'Statistical or aggregate health data without individual identifiers may be disclosable',
            'General descriptions of health programs or services without patient-specific information are not protected',
            'Records about a deceased person\'s health may receive reduced protection over time',
            'Information voluntarily disclosed to the public by the subject is not protected',
        ]),
        'notes': 'Michigan\'s medical privacy exemption overlaps with HIPAA protections for covered entities. HIPAA does not preempt state FOIA for government records not held by covered entities, but HIPAA-covered entities\' records also qualify for this exemption.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(n)',
        'exemption_number': '§ 15.243(1)(n)',
        'short_name': 'Security Plans',
        'category': 'security',
        'description': 'Protects records that would reveal the security plans or emergency preparedness plans of a public body, if the disclosure would endanger the security of the public body or the people.',
        'scope': 'Security plans, emergency response plans, vulnerability assessments, and similar records whose disclosure would endanger the security of a facility, system, or people. Must show a specific, articulable security risk from disclosure — not just general concerns about security.',
        'key_terms': json.dumps([
            'security plan', 'emergency preparedness', 'vulnerability assessment',
            'security measures', 'facility security', 'critical infrastructure',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and real, not speculative or generic',
            'General descriptions of security objectives without tactical details may not qualify',
            'After-action reports about past security incidents may be less sensitive than current plans',
            'Redaction of specific tactical details while releasing general program information is a less restrictive alternative',
            'Challenge whether the specific record reveals current vulnerabilities or just historical information',
        ]),
        'notes': 'Expanded after 9/11 and the post-2001 focus on critical infrastructure protection. Michigan courts require a specific nexus between the disclosed information and the claimed security risk.',
    },
    {
        'jurisdiction': 'MI',
        'statute_citation': 'MCL 15.243(1)(s)',
        'exemption_number': '§ 15.243(1)(s)',
        'short_name': 'Competitive Bid Documents',
        'category': 'commercial',
        'description': 'Protects sealed bids or proposals received in competitive bidding, prior to the opening of the bids.',
        'scope': 'Sealed bids and competitive proposals received by a public body before the bid opening. Once bids are opened, the exemption dissolves and all bid submissions are public. The exemption prevents bidders from adjusting their bids based on competitors\' pricing.',
        'key_terms': json.dumps([
            'sealed bid', 'competitive bid', 'proposal', 'procurement', 'bid opening',
            'competitive pricing', 'vendor', 'contract award',
        ]),
        'counter_arguments': json.dumps([
            'Once the bid opening occurs, all submitted bids become public records',
            'After bid opening, all bid submissions, evaluation criteria, and scoring must be disclosed',
            'Post-award contract documents are fully public',
            'Challenge any attempt to maintain bid confidentiality after the public bid opening',
        ]),
        'notes': 'Strictly time-limited to the period before bid opening. This exemption protects the integrity of competitive bidding, not contractor privacy after award. All sealed bids become public upon opening — Michigan courts have been clear on this.',
    },
]


MI_RULES = [
    {
        'jurisdiction': 'MI',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'MCL 15.235(2)',
        'notes': 'A public body must respond to a FOIA request within 5 business days after the public body receives the request. The response must either grant the request, deny the request in writing, or grant the request in part and deny it in part. This is one of the shorter state FOIA response windows.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'initial_response',
        'param_key': 'extension_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'MCL 15.235(2)(d)',
        'notes': 'If a public body cannot respond within 5 business days, it may extend the response period by up to 10 additional business days by notifying the requester in writing with a specific reason for the extension. Only one extension is permitted per request. Reasons that justify extension: the request requires search for records not located at the principal office; the request requires search for voluminous records; the public body needs to give notice to third parties.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'MCL 15.234(1)',
        'notes': 'Michigan caps copying fees at $0.10 per page for standard 8.5x11 copies — among the lowest statutory caps in the country. For other sizes or formats, the fee is the actual cost. Agencies may not charge more than $0.10 per page for standard copies. Fees must be estimated in advance and the requester may choose to narrow the request.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'fee_cap',
        'param_key': 'labor_cost_cap',
        'param_value': 'lowest_paid_capable_employee',
        'day_type': None,
        'statute_citation': 'MCL 15.234(1)(b)',
        'notes': 'Labor costs for search, examination, and review must be calculated at the hourly wage of the lowest-paid employee capable of performing the task, not the actual salary of the person who does the work. This is a significant consumer protection — agencies cannot use senior attorneys or administrators to run up labor fees. The rate must not include overtime or fringe benefits.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'fee_cap',
        'param_key': 'fee_waiver_indigence',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'MCL 15.234(4)',
        'notes': 'A public body must waive the first $20 of a fee for an individual who submits an affidavit stating they are indigent and receiving public assistance, or that they are not able to pay because of indigence. Indigence waiver applies per request, not per calendar year.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'fee_cap',
        'param_key': 'nonprofit_media_discount',
        'param_value': '50_percent_reduction',
        'day_type': None,
        'statute_citation': 'MCL 15.234(5)',
        'notes': 'A nonprofit organization or news media is entitled to a 50% reduction in fees if the request is made primarily for noncommercial purposes. Requester must identify themselves as media or nonprofit at the time of the request. This is a statutory discount, not a waiver — the nonprofit/media requester still pays half the assessed fee.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'appeal_deadline',
        'param_key': 'circuit_court_appeal',
        'param_value': 'no_administrative_appeal_required',
        'day_type': None,
        'statute_citation': 'MCL 15.240(1)',
        'notes': 'Michigan FOIA does NOT require an administrative appeal before seeking judicial review. A requester may go directly to circuit court after a denial or failure to respond. This is a significant advantage — no need to exhaust administrative remedies. The lawsuit must be filed in the circuit court for the county where the public body is located.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'statute_of_limitations',
        'param_value': '180',
        'day_type': 'calendar',
        'statute_citation': 'MCL 15.240(1)',
        'notes': 'A requester must file suit in circuit court within 180 days after the public body\'s final determination (denial or failure to respond). The 180-day period begins when the denial is received or, for constructive denials, when the response period expires without a response.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'mandatory_if_substantially_prevails',
        'day_type': None,
        'statute_citation': 'MCL 15.240(6)',
        'notes': 'If a requester substantially prevails in court, the court SHALL award reasonable attorney fees, costs, and disbursements against the public body. Unlike many states, Michigan\'s fee award is mandatory (shall), not discretionary (may), when the requester substantially prevails. This is a strong incentive for compliance.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'punitive_damages',
        'param_value': '500',
        'day_type': None,
        'statute_citation': 'MCL 15.240(7)',
        'notes': 'If the court finds the public body\'s denial was arbitrary and capricious, the court shall award punitive damages of $500 against the public body. This statutory punitive damages provision is unusual among state FOIA laws and provides a strong deterrent against bad-faith denials. The $500 is in addition to attorney fees and actual damages.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'initial_response',
        'param_key': 'denial_must_be_written',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'MCL 15.235(4)',
        'notes': 'Any denial of a FOIA request must be in writing and must specify the exemption(s) claimed, provide a brief statement of the reasons for denial, and describe the records or information withheld. The denial must also include a notice of the right to seek judicial review under MCL 15.240.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'MCL 15.244',
        'notes': 'When a public body determines that a public record contains exempt information, it must separate the exempt from the nonexempt information and release the nonexempt portions. The deletion must be noted in the copy provided. A blanket withholding of entire documents containing only partially exempt information is improper.',
    },
    {
        'jurisdiction': 'MI',
        'rule_type': 'fee_cap',
        'param_key': 'fee_deposit',
        'param_value': 'up_to_50_percent_advance',
        'day_type': None,
        'statute_citation': 'MCL 15.234(2)',
        'notes': 'Before processing a request, a public body may require a good-faith deposit of up to 50% of the estimated fee if the estimated fee exceeds $50. The public body must provide a written fee itemization before requiring the deposit. Requesters who have failed to pay for prior requests may be required to pay past unpaid fees before a new request is processed.',
    },
]


MI_TEMPLATES = [
    {
        'jurisdiction': 'MI',
        'record_type': 'general',
        'template_name': 'General Michigan FOIA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Coordinator
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — MCL 15.231 et seq.

Dear FOIA Coordinator:

Pursuant to the Michigan Freedom of Information Act, MCL 15.231-15.246, I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records covering the period {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (PDF or native file format) where available, to minimize costs. Under MCL 15.234(1), copying fees for standard pages are capped at $0.10 per page. Labor costs must be calculated at the rate of the lowest-paid employee capable of performing the search, per MCL 15.234(1)(b).

I am willing to pay fees up to ${{fee_limit}}. If you estimate that fees will exceed this amount, please provide a written itemization before processing so I may narrow my request.

If any portion of this request is denied, please: (1) specify each exemption under MCL 15.243 that is being claimed; (2) provide a brief written explanation of the reason for denial as required by MCL 15.235(4); (3) release all reasonably segregable nonexempt portions of any partially exempt records, as required by MCL 15.244; and (4) advise me of my right to seek judicial review under MCL 15.240.

I look forward to your response within 5 business days as required by MCL 15.235(2).

If you have any questions about this request, please contact me at {{requester_email}} or {{requester_phone}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived or reduced for the following reasons:

[If indigent]: Pursuant to MCL 15.234(4), I am an individual who is indigent and [receiving public assistance / unable to pay due to indigence]. I have attached an affidavit as required by the statute. Please waive the first $20 of any assessed fee.

[If nonprofit or media]: I am a [nonprofit organization / member of the news media] and request a 50% reduction in fees pursuant to MCL 15.234(5). This request is made primarily for noncommercial purposes. I am requesting these records in order to {{public_interest_explanation}}.

Disclosure of these records will contribute to public understanding of {{public_benefit_description}} and serves the public interest by informing the community about the activities of their government.''',
        'expedited_language': '''I request that this FOIA request be processed on an expedited basis. Although Michigan FOIA does not contain a statutory expedited processing provision, I ask that the agency respond as promptly as possible because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

Thank you for your prompt attention to this request.''',
        'notes': 'General Michigan FOIA template. Note that the designated recipient is the "FOIA Coordinator," not "Records Access Officer" (NY) or "FOIA Officer" (federal). Michigan FOIA does not require an administrative appeal before filing in circuit court — this is a key strategic advantage.',
    },
    {
        'jurisdiction': 'MI',
        'record_type': 'appeal',
        'template_name': 'Michigan FOIA Circuit Court Complaint',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

[Note: Michigan FOIA does not require an administrative appeal. You may file directly in circuit court after a denial or failure to respond. This template provides language for a circuit court complaint, not an administrative appeal.]

STATE OF MICHIGAN
CIRCUIT COURT FOR THE COUNTY OF {{county}}

{{requester_name}},
    Plaintiff,

vs.

{{agency_name}},
    Defendant.

Case No. ___________

COMPLAINT FOR INJUNCTIVE RELIEF AND FEES UNDER THE
MICHIGAN FREEDOM OF INFORMATION ACT, MCL 15.231-15.246

Plaintiff {{requester_name}} states as follows:

1. Plaintiff submitted a FOIA request to Defendant {{agency_name}} on {{original_request_date}}, requesting {{brief_description_of_records}}.

2. On {{response_date}}, Defendant {{description_of_denial}}. [OR: Defendant failed to respond within the 5-business-day period required by MCL 15.235(2).]

3. Defendant\'s denial is improper because {{grounds_for_challenge}}.

4. Specifically, the exemption(s) claimed under MCL 15.243 {{exemption_cited}} do not apply because:

{{exemption_challenge_arguments}}

5. Even if any portion of the requested records is exempt, Defendant is required to segregate and release nonexempt portions under MCL 15.244.

WHEREFORE, Plaintiff requests that this Court:
(a) Order Defendant to provide access to the requested records;
(b) Award Plaintiff reasonable attorney fees, costs, and disbursements as required by MCL 15.240(6);
(c) If Defendant\'s denial was arbitrary and capricious, award punitive damages of $500 under MCL 15.240(7);
(d) Grant such other relief as is just and equitable.

Respectfully submitted,
{{requester_name}}

Date: {{date}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Michigan FOIA is unique — there is NO mandatory administrative appeal process. Requesters may go directly to circuit court after denial or failure to respond. The complaint must be filed within 180 days under MCL 15.240(1). Attorney fees are mandatory (shall be awarded) if the requester substantially prevails. Punitive damages of $500 are available for arbitrary and capricious denials.',
    },
]


def build_exemptions(conn):
    added = 0
    skipped = 0
    for ex in MI_EXEMPTIONS:
        existing = conn.execute(
            'SELECT id FROM exemptions WHERE jurisdiction = ? AND statute_citation = ?',
            (ex['jurisdiction'], ex['statute_citation'])
        ).fetchone()
        if existing:
            conn.execute(
                '''UPDATE exemptions SET
                    exemption_number = ?, short_name = ?, category = ?,
                    description = ?, scope = ?, key_terms = ?,
                    counter_arguments = ?, notes = ?,
                    last_verified = datetime('now'), updated_at = datetime('now')
                WHERE id = ?''',
                (ex['exemption_number'], ex['short_name'], ex['category'],
                 ex['description'], ex['scope'], ex['key_terms'],
                 ex['counter_arguments'], ex['notes'], existing[0])
            )
            skipped += 1
        else:
            conn.execute(
                '''INSERT INTO exemptions (
                    jurisdiction, statute_citation, exemption_number,
                    short_name, category, description, scope,
                    key_terms, counter_arguments, notes, last_verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
                (ex['jurisdiction'], ex['statute_citation'], ex['exemption_number'],
                 ex['short_name'], ex['category'], ex['description'], ex['scope'],
                 ex['key_terms'], ex['counter_arguments'], ex['notes'])
            )
            added += 1
    return added, skipped


def build_rules(conn):
    added = 0
    skipped = 0
    for rule in MI_RULES:
        existing = conn.execute(
            'SELECT id FROM response_rules WHERE jurisdiction = ? AND rule_type = ? AND param_key = ?',
            (rule['jurisdiction'], rule['rule_type'], rule['param_key'])
        ).fetchone()
        if existing:
            conn.execute(
                '''UPDATE response_rules SET
                    param_value = ?, day_type = ?, statute_citation = ?,
                    notes = ?, last_verified = datetime('now'), updated_at = datetime('now')
                WHERE id = ?''',
                (rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                 rule.get('notes'), existing[0])
            )
            skipped += 1
        else:
            conn.execute(
                '''INSERT INTO response_rules (
                    jurisdiction, rule_type, param_key, param_value,
                    day_type, statute_citation, notes, last_verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
                (rule['jurisdiction'], rule['rule_type'], rule['param_key'],
                 rule['param_value'], rule.get('day_type'), rule['statute_citation'],
                 rule.get('notes'))
            )
            added += 1
    return added, skipped


def build_templates(conn):
    added = 0
    skipped = 0
    for tmpl in MI_TEMPLATES:
        existing = conn.execute(
            'SELECT id FROM request_templates WHERE jurisdiction = ? AND template_name = ?',
            (tmpl['jurisdiction'], tmpl['template_name'])
        ).fetchone()
        if existing:
            conn.execute(
                '''UPDATE request_templates SET
                    record_type = ?, template_text = ?,
                    fee_waiver_language = ?, expedited_language = ?,
                    notes = ?, updated_at = datetime('now')
                WHERE id = ?''',
                (tmpl['record_type'], tmpl['template_text'],
                 tmpl.get('fee_waiver_language'), tmpl.get('expedited_language'),
                 tmpl.get('notes'), existing[0])
            )
            skipped += 1
        else:
            conn.execute(
                '''INSERT INTO request_templates (
                    jurisdiction, record_type, template_name,
                    template_text, fee_waiver_language, expedited_language,
                    notes, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'prdb-built')''',
                (tmpl['jurisdiction'], tmpl['record_type'], tmpl['template_name'],
                 tmpl['template_text'], tmpl.get('fee_waiver_language'),
                 tmpl.get('expedited_language'), tmpl.get('notes'))
            )
            added += 1
    return added, skipped


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    totals = {'added': 0, 'skipped': 0, 'errors': 0}

    try:
        ea, es = build_exemptions(conn)
        ra, rs = build_rules(conn)
        ta, ts = build_templates(conn)
        conn.commit()
        totals['added'] = ea + ra + ta
        totals['skipped'] = es + rs + ts
        print(f'MI FOIA exemptions:  {ea} added, {es} updated')
        print(f'MI FOIA rules:       {ra} added, {rs} updated')
        print(f'MI FOIA templates:   {ta} added, {ts} updated')
    except Exception as e:
        totals['errors'] += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    write_receipt(
        script='build_mi',
        added=totals['added'],
        skipped=totals['skipped'],
        errors=totals['errors'],
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
