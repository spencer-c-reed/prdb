#!/usr/bin/env python3
"""Build Missouri Sunshine Law catalog — exemptions, response rules, and request templates.

Missouri Sunshine Law, RSMo Chapter 610 (§§ 610.010–610.200).
Default rule is openness; exemptions are permissive except where another statute
mandates closure. Records are "public records" unless specifically closed.

Run: python3 scripts/build/build_mo.py
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
# =============================================================================

MO_EXEMPTIONS = [
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.100',
        'exemption_number': '§ 610.100',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement agencies that relate to open criminal investigations, undercover officers, or informants may be closed to protect the integrity of investigations.',
        'scope': 'Records of any law enforcement agency pertaining to: (1) open criminal investigations; (2) identities of undercover officers or informants; (3) techniques and procedures used in investigations if disclosure would harm future investigations; (4) records whose disclosure would endanger the life of any law enforcement officer or informant. Once a prosecution concludes, many underlying investigative records become open under § 610.100(3).',
        'key_terms': json.dumps([
            'law enforcement', 'criminal investigation', 'open investigation', 'undercover officer',
            'informant', 'investigative techniques', 'endanger life', 'prosecution concluded',
        ]),
        'counter_arguments': json.dumps([
            'Records of completed prosecutions — including arrest reports and incident reports — are generally open under § 610.100(3) once prosecution concludes or the statute of limitations expires',
            'The agency must demonstrate the investigation is genuinely "open" — closed or inactive cases do not qualify',
            'Incident reports and initial arrest reports are separately subject to disclosure requirements; challenge withholding of those specific record types',
            'The endangerment rationale requires a specific, articulable risk — generic concerns are insufficient',
            'Segregate and demand non-investigative portions: administrative records, budgets, and policy documents attached to investigative files must still be released',
        ]),
        'notes': 'Missouri\'s law enforcement exemption is one of its most frequently litigated provisions. Courts have held that arrest records — name, address, offense charged — are open even for pending cases. The AG has issued guidance that routine incident reports are generally open. See State ex rel. Schrier v. Mace, 896 S.W.2d 234 (Mo. App. 1995).',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(1)',
        'exemption_number': '§ 610.021(1)',
        'short_name': 'Legal Work / Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Legal actions, causes of action, litigation, or proposed litigation involving a public governmental body, including attorney-client communications and attorney work product.',
        'scope': 'Records relating to: legal actions, causes of action, or litigation involving the governmental body; attorney-client privileged communications; attorney work product; proposed settlement negotiations; and records whose disclosure would waive attorney-client or work product privilege. The exemption is permissive — the body may choose to disclose. Once litigation concludes, the justification for continued closure weakens significantly.',
        'key_terms': json.dumps([
            'attorney-client', 'work product', 'litigation', 'legal action', 'cause of action',
            'proposed litigation', 'settlement', 'legal counsel', 'privileged communication',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers litigation and legal advice — not all communications with an attorney qualify; administrative and policy communications are not automatically privileged',
            'Once litigation concludes, the rationale for closure disappears; challenge continued withholding of post-litigation records',
            'Final settlements and consent decrees are generally open public records; demand those even when litigation files are withheld',
            'The body must assert the privilege — it is not self-executing; if the body has not formally closed the records, they should be open',
            'Facts underlying a legal matter may be segregable from protected legal advice',
        ]),
        'notes': 'Missouri courts have held that the legal work exemption is permissive, not mandatory — the body can choose to open these records. See City of St. Louis v. City of Bridgeton, 884 S.W.2d 251 (Mo. App. 1994). The exemption does not cover records that were not actually prepared in connection with pending or anticipated litigation.',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(2)',
        'exemption_number': '§ 610.021(2)',
        'short_name': 'Leasing/Purchase Negotiations',
        'category': 'commercial',
        'description': 'Leaseholds and purchase of real estate by a public governmental body where public knowledge could adversely affect the acquisition.',
        'scope': 'Records pertaining to the leasing or acquisition of real property by a governmental body, where disclosure of the intended acquisition price or negotiating strategy could impair the government\'s ability to obtain fair market value. The exemption is time-limited — it applies only while negotiations are pending or imminent. Once the acquisition is complete, the records become open.',
        'key_terms': json.dumps([
            'real estate', 'property acquisition', 'leasehold', 'purchase price', 'negotiation',
            'adverse effect', 'fair market value', 'imminent acquisition',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is strictly time-limited to active negotiations; completed transactions are fully open',
            'The government must show that disclosure would actually and concretely impair the acquisition — speculative harm is insufficient',
            'Final purchase agreements and recorded deeds are public records regardless of prior negotiation confidentiality',
            'The exemption protects negotiating strategy, not the identity of properties the government is considering — challenge overbroad withholding',
        ]),
        'notes': 'Missouri courts interpret this exemption narrowly. The body bears the burden of showing that disclosure would adversely affect the acquisition. Post-closing records — deeds, appraisals once paid for, final contracts — are generally open.',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(3)',
        'exemption_number': '§ 610.021(3)',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Individually identifiable personnel records, performance ratings, or records pertaining to employees or applicants for employment, except for the names, positions, salaries, and lengths of service of officers and employees of public agencies.',
        'scope': 'Personnel files, performance evaluations, disciplinary records, and similar records identifying individual employees. However, Missouri law explicitly requires disclosure of employee names, positions, salaries, and lengths of service regardless of other personnel record protections. Medical records within personnel files receive stronger protection. Records of disciplinary action that resulted in termination are often open.',
        'key_terms': json.dumps([
            'personnel records', 'performance rating', 'employee record', 'applicant', 'salary',
            'individually identifiable', 'name', 'position', 'length of service', 'termination',
        ]),
        'counter_arguments': json.dumps([
            'Names, positions, salaries, and lengths of service of public employees are EXPLICITLY open under § 610.021(3) — no exemption applies to those fields',
            'Final disciplinary determinations resulting in significant employment action (termination, suspension) are generally open',
            'Records of an employee\'s official duties and public conduct are not "personnel records" and should be disclosed',
            'Challenge blanket withholding of entire personnel files when only specific sensitive items warrant protection; demand segregation',
            'Elected officials and high-level appointed officials have reduced privacy expectations regarding their official conduct',
        ]),
        'notes': 'Missouri\'s personnel exemption contains an important carve-out: names, positions, salaries, and lengths of service are public regardless of the general exemption. This is a common target for journalists seeking government compensation data. See State ex rel. ACLU v. City of Sugar Creek, 796 S.W.2d 843 (Mo. App. 1990).',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(14)',
        'exemption_number': '§ 610.021(14)',
        'short_name': 'Individual Privacy — SSN/Financial',
        'category': 'privacy',
        'description': 'Records that are protected from disclosure by state or federal law, including Social Security numbers and individually identifiable financial information.',
        'scope': 'Records containing Social Security numbers, individual financial account numbers, and similar identifying financial information. This exemption also serves as a catch-all for records protected by other state or federal privacy statutes (e.g., federal Privacy Act records, HIPAA-protected medical information). Applies to individual financial information only, not to the financial records of government bodies themselves.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'financial information', 'account number',
            'individually identifiable', 'federal privacy law', 'state privacy law', 'HIPAA',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute that requires confidentiality — general privacy concerns do not qualify under the "protected by law" prong',
            'Government financial records (budgets, expenditures, contracts) are not "individually identifiable financial information" — they remain open',
            'Redaction of SSNs and account numbers while releasing the substantive record is the correct approach; demand that approach rather than full withholding',
            'The HIPAA argument applies only to covered entities and covered health information — many government records with health references do not qualify',
        ]),
        'notes': 'Missouri courts have held that this exemption is not a general privacy exemption. The referenced "law" must specifically protect the records from disclosure. Mere sensitivity or embarrassment does not qualify. See Pulitzer Pub. Co. v. Missouri State Highway Commission, 596 S.W.2d 828 (Mo. App. 1980).',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(10)',
        'exemption_number': '§ 610.021(10)',
        'short_name': 'Sealed Bids / Specifications',
        'category': 'commercial',
        'description': 'Sealed bids and related documents, until the bids are opened; specifications and documents prepared for procurement until awarded.',
        'scope': 'Sealed bids and procurement specifications that are not yet public, while bids are being solicited and before the bid opening. Once bids are publicly opened, all responsive bids and related specifications become open public records. The exemption is strictly time-limited to the pre-award period.',
        'key_terms': json.dumps([
            'sealed bid', 'bid opening', 'procurement', 'specification', 'proposal', 'RFP',
            'solicitation', 'pre-award', 'competitive bidding',
        ]),
        'counter_arguments': json.dumps([
            'All bids and specifications are open immediately after the bid opening — the exemption ends at that precise moment',
            'Evaluation criteria, scoring rubrics, and award decisions are open once the contract is awarded',
            'Contracts awarded pursuant to a procurement process are fully open — the exemption does not extend to the resulting contract',
            'If the agency has publicly disclosed bid results in any form, the exemption may have been waived',
        ]),
        'notes': 'Missouri\'s sealed bid exemption mirrors most states\' approach. The time limit is firm: bid opening triggers disclosure. Requester should ask for the date of the bid opening and request all materials as of that date if they were denied during the sealed period.',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(4)',
        'exemption_number': '§ 610.021(4)',
        'short_name': 'Security Plans / Vulnerability Assessments',
        'category': 'safety',
        'description': 'Records that, if disclosed, could reasonably be expected to threaten the security of the public or the public\'s safety, including security plans and vulnerability assessments for public buildings or infrastructure.',
        'scope': 'Security plans, vulnerability assessments, evacuation procedures, and similar records for public buildings and infrastructure where disclosure could enable attacks or endanger the public. The exemption is subject to a "could reasonably be expected to threaten security" standard, not a speculative threat standard. General floor plans or information widely available elsewhere do not qualify.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'public safety', 'infrastructure security',
            'evacuation procedure', 'threat', 'reasonably expected', 'public building',
        ]),
        'counter_arguments': json.dumps([
            'The threat must be real and specific, not speculative; agencies cannot withhold records based on hypothetical misuse',
            'Information that is publicly available (e.g., building locations, general layouts) cannot be withheld on security grounds',
            'Challenge whether the specific record requested could "reasonably be expected" to enable a security threat — the standard requires more than possibility',
            'Administrative records about security spending, vendor contracts, and personnel do not automatically qualify for this exemption',
        ]),
        'notes': 'Missouri added enhanced security exemptions after 9/11. Courts have interpreted the "reasonably be expected to threaten security" standard to require a genuine, demonstrable risk. Generic invocation of security concerns is insufficient.',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(15)',
        'exemption_number': '§ 610.021(15)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Records of a public body that relate to the procurement of goods or services and that contain trade secrets or other proprietary, commercial, or financial information of private entities, where disclosure would place the private entity at a competitive disadvantage.',
        'scope': 'Trade secrets and proprietary commercial or financial information submitted by private entities to the government in connection with procurement, licensing, or regulatory proceedings. The private entity must demonstrate that disclosure would cause actual competitive harm, not merely embarrassment. Government-generated information does not qualify.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information', 'financial information',
            'competitive disadvantage', 'private entity', 'procurement', 'submitted',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate actual competitive harm, not merely assert "proprietary" status; boilerplate confidentiality claims are insufficient',
            'Government-generated records (audit findings, compliance reviews) are not "submitted by" a private entity',
            'Information that is publicly available elsewhere cannot be a trade secret',
            'The portion of a contract reflecting the price paid with public funds is generally not a trade secret',
            'Challenge whether the private entity has made a specific, documented showing of competitive harm',
        ]),
        'notes': 'Missouri courts apply a competitive harm standard similar to federal FOIA Exemption 4. The governmental body, not the submitter, makes the final determination. See Pulitzer Pub. Co. v. Missouri State Highway Commission, 596 S.W.2d 828 (Mo. App. 1980).',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(7)',
        'exemption_number': '§ 610.021(7)',
        'short_name': 'Medical Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, psychological, or alcoholism or drug dependency treatment records that are individually identifiable.',
        'scope': 'Individually identifiable medical records, psychiatric records, psychological records, and substance abuse treatment records. Applies to records held by public health agencies, public hospitals, public schools, and other governmental bodies. Non-identifiable aggregate health data and public health statistics remain open. HIPAA provides a parallel federal protection.',
        'key_terms': json.dumps([
            'medical record', 'psychiatric record', 'psychological record', 'drug treatment',
            'alcohol treatment', 'individually identifiable', 'health information', 'patient',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate, non-identifiable health data (e.g., disease rates, public health statistics) is not protected — demand those records',
            'Policy records about how health programs are administered are not "medical records"',
            'Challenge whether the records at issue are truly "individually identifiable" — records stripped of identifying information may be open',
            'HIPAA\'s preemption of more permissive state laws does not preempt the request — it only means both federal and state standards must be met',
        ]),
        'notes': 'Missouri\'s medical records exemption is consistent with HIPAA and broadly applied by public health agencies. However, courts have required that the records be genuinely identifiable and genuinely medical in nature, not merely health-related administrative records.',
    },
    {
        'jurisdiction': 'MO',
        'statute_citation': 'RSMo § 610.021(17)',
        'exemption_number': '§ 610.021(17)',
        'short_name': 'Audit Working Papers',
        'category': 'deliberative',
        'description': 'Auditor\'s working papers and audit reports before they are finalized and published.',
        'scope': 'Draft audit reports, working papers, and internal audit documentation before the final audit report is issued. The exemption is strictly time-limited to the pre-publication period. Once the audit is finalized and released, all underlying working papers generally become open. This exemption prevents premature disclosure that could lead to misunderstanding of preliminary findings.',
        'key_terms': json.dumps([
            'audit', 'working papers', 'draft audit', 'preliminary findings', 'auditor',
            'pre-publication', 'internal audit', 'audit report',
        ]),
        'counter_arguments': json.dumps([
            'Once the final audit report is published, the working papers and underlying documents generally become open',
            'The exemption covers pre-decisional working papers, not final reports or their appendices',
            'If the audit has been presented to any public body or quoted publicly, the exemption may have been waived',
            'Request the final published audit and its appendices — those are open regardless of the working paper exemption',
            'Factual data and financial records underlying the audit may be segregable from protected deliberative analysis',
        ]),
        'notes': 'Missouri courts have interpreted this exemption to apply only during the active audit period. Post-publication withholding of working papers has been successfully challenged. The AG has issued guidance that completed audits and their underlying documentation are subject to the Sunshine Law.',
    },
]

# =============================================================================
# RESPONSE RULES
# =============================================================================

MO_RULES = [
    {
        'jurisdiction': 'MO',
        'rule_type': 'initial_response',
        'param_key': 'days_to_respond',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'RSMo § 610.023(3)',
        'notes': 'Custodian must respond within 3 business days of receiving the request. Response may be access, denial, or a statement that additional time is needed. Missouri defines "business days" as Monday through Friday, excluding state holidays. The response deadline begins on the business day after the request is received.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'initial_response',
        'param_key': 'response_by_end_of_third_business_day',
        'param_value': 'true',
        'day_type': 'business',
        'statute_citation': 'RSMo § 610.023(3)',
        'notes': 'The statute specifies response "by the end of the third business day" — not within three calendar days. This is a specific formulation; the response must arrive by close of business on day three, not merely be mailed by that date. Agencies that fail to respond by that deadline have constructively denied the request and the requester may seek judicial relief.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial',
        'param_value': 'end_of_third_business_day',
        'day_type': 'business',
        'statute_citation': 'RSMo § 610.023(3)',
        'notes': 'Failure to respond by the end of the third business day constitutes a constructive denial, allowing the requester to immediately seek a court order under RSMo § 610.027. No additional administrative appeal step is required before seeking judicial relief — Missouri has no mandatory administrative appeal process.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'fee_cap',
        'param_key': 'copying_fee_standard',
        'param_value': 'actual_cost',
        'day_type': None,
        'statute_citation': 'RSMo § 610.026',
        'notes': 'Missouri does not set a statutory per-page cap. Fees are based on actual cost of document search, duplication, and transmission. The agency may charge for staff time to search and prepare records at the actual cost of providing the services, not to exceed the actual costs incurred. In practice, many agencies charge $0.10–$0.25/page for copies.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'fee_cap',
        'param_key': 'research_and_duplication',
        'param_value': 'actual_cost_not_profit',
        'day_type': None,
        'statute_citation': 'RSMo § 610.026',
        'notes': 'Fees may not exceed the actual costs of document search, duplication, and transmission. Agencies may not profit from Sunshine Law requests. Challenge any fee schedule that includes administrative overhead, profit margin, or costs not directly tied to fulfilling the specific request.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'fee_waiver',
        'param_key': 'waiver_for_news_media',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'RSMo § 610.026',
        'notes': 'Missouri law does not provide a mandatory fee waiver for media or public interest requesters. However, the agency has discretion to waive or reduce fees. Requesters may ask for a waiver based on public interest. Some agencies have informal policies favoring media requesters.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_suit',
        'param_value': 'immediate_after_denial',
        'day_type': None,
        'statute_citation': 'RSMo § 610.027',
        'notes': 'Missouri has NO mandatory administrative appeal. After a denial (or constructive denial from failure to respond by end of day 3), the requester may immediately file suit in circuit court. There is no requirement to exhaust administrative remedies first. The circuit court may issue an order compelling disclosure.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'burden_of_proof',
        'param_value': 'agency_bears_burden',
        'day_type': None,
        'statute_citation': 'RSMo § 610.027',
        'notes': 'In a Sunshine Law enforcement action, the public governmental body bears the burden of justifying any closure of records. The body must demonstrate that the records fall within a specific statutory exemption. The requester does not bear the burden of proving wrongful withholding.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'mandatory_if_knowing_violation',
        'day_type': None,
        'statute_citation': 'RSMo § 610.027(3)',
        'notes': 'If the court finds a knowing and purposeful violation of the Sunshine Law, attorney fees and costs SHALL be awarded to the requester. For non-knowing violations, fee awards are discretionary. This mandatory fee-shifting provision is stronger than most state FOI laws and provides a significant incentive for agencies to comply promptly.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'civil_penalty_knowing',
        'param_value': '1000_to_5000',
        'day_type': None,
        'statute_citation': 'RSMo § 610.027(3)',
        'notes': 'For knowing and purposeful violations, the court may impose a civil penalty between $1,000 and $5,000 per violation. This is assessed against the public body, not the individual employee. A pattern of violations can result in cumulative penalties.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'criminal_misdemeanor',
        'param_value': 'class_a_misdemeanor',
        'day_type': None,
        'statute_citation': 'RSMo § 610.027(4)',
        'notes': 'Purposeful violations of the Sunshine Law by a public official are a class A misdemeanor, punishable by up to one year in jail and/or a fine. Criminal prosecutions are rare but possible for egregious, willful violations. This is an unusually strong criminal enforcement provision for a state sunshine law.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'RSMo § 610.022(1)',
        'notes': 'When a record contains both open and closed portions, the custodian must separate the exempt portions and make the non-exempt portions available. The custodian must notify the requester of what has been withheld and cite the specific statutory basis for each closure. Blanket withholding of records with segregable open portions violates the Sunshine Law.',
    },
    {
        'jurisdiction': 'MO',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_citation',
        'day_type': None,
        'statute_citation': 'RSMo § 610.023(4)',
        'notes': 'Any denial must be in writing and must specify the provision of law under which access is denied. Oral denials and denials without legal citation are improper and may support a finding of a knowing violation. The written denial triggers the requester\'s right to seek judicial review.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

MO_TEMPLATES = [
    {
        'jurisdiction': 'MO',
        'record_type': 'general',
        'template_name': 'General Missouri Sunshine Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Sunshine Law Request for Public Records

Dear Custodian of Records:

Pursuant to the Missouri Sunshine Law, RSMo §§ 610.010–610.200, I hereby request access to and copies of the following public records:

{{description_of_records}}

I am requesting records for the time period {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records, I provide the following additional information:
{{additional_context}}

I request that records be produced in electronic format where available, to minimize costs to both parties.

I am willing to pay copying fees based on actual cost pursuant to RSMo § 610.026. If you estimate that fees will exceed ${{fee_limit}}, please notify me before processing so I may narrow or prioritize my request.

Pursuant to RSMo § 610.023, I request a response by the end of the third business day following receipt of this request. If access to any records will be denied, please provide a written statement citing the specific provision of law under which access is denied, as required by RSMo § 610.023(4).

If any record is partially closed, please separate the closed and open portions and provide the open portions, as required by RSMo § 610.022(1).

Thank you for your assistance.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that your agency waive or reduce the fees associated with this request. Although the Sunshine Law does not mandate a fee waiver, I ask that you exercise your discretion to waive fees because the records requested are of significant public interest.

These records relate to {{public_interest_explanation}}, a matter of direct concern to Missouri citizens. I am {{requester_category_description}} and intend to share this information with the public through {{dissemination_method}}.

A fee waiver would further the Sunshine Law\'s policy of maximum public access. Pursuant to RSMo § 610.026, fees may only recover actual costs and should not be used as a barrier to access.''',
        'expedited_language': '''I request that this Sunshine Law request be processed as quickly as possible. While the statute provides three business days for a response, the urgency of this request justifies prompt action.

Specifically, I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date would {{harm_from_delay}}.

I appreciate your prompt attention to this time-sensitive request.''',
        'notes': 'General-purpose Missouri Sunshine Law template. Uses correct Missouri statutory citations. The three business day response deadline runs from receipt of the request. Missouri has no mandatory administrative appeal — if denied, the requester may immediately seek circuit court review under RSMo § 610.027.',
    },
    {
        'jurisdiction': 'MO',
        'record_type': 'law_enforcement',
        'template_name': 'Missouri Sunshine Law — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Sunshine Law Request — Law Enforcement Records

Dear Custodian of Records:

Pursuant to the Missouri Sunshine Law, RSMo §§ 610.010–610.200, I hereby request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports, booking information, and jail records
- Call-for-service logs and dispatch records
- Use-of-force reports and related documentation
- Disciplinary records
- Body-worn camera footage and related metadata
- Any other records relating to the above

NOTICE REGARDING EXEMPTIONS: Pursuant to RSMo § 610.100(3), records relating to completed or declined prosecutions — including arrest reports and incident reports — are open public records. If any records are withheld under the investigation exemption in § 610.021(2) or § 610.100, please confirm in writing whether the referenced investigation or prosecution is currently open. If it is not open, the exemption does not apply.

Please separate any closed portions from open portions pursuant to RSMo § 610.022(1) and provide the open portions without delay.

If any records are denied, please provide a written statement citing the specific statutory provision for each denial, as required by RSMo § 610.023(4).

I am willing to pay actual copying costs pursuant to RSMo § 610.026 up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that the agency waive copying fees. These records relate to matters of significant public concern — {{public_interest_explanation}} — and disclosure serves the public interest in transparent law enforcement. The Sunshine Law\'s policy of maximum disclosure supports a fee waiver here.''',
        'expedited_language': None,
        'notes': 'Missouri law enforcement records template. Key Missouri distinction: arrest reports and completed prosecution records are generally open under § 610.100(3). Template includes language preempting the "open investigation" exemption by requesting written confirmation of investigation status. Missouri has no administrative appeal — denial leads directly to circuit court.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = {'exemptions': 0, 'rules': 0, 'templates': 0}
    skipped = {'exemptions': 0, 'rules': 0, 'templates': 0}
    errors = 0

    try:
        # --- Exemptions ---
        for exemption in MO_EXEMPTIONS:
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
                skipped['exemptions'] += 1
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
                added['exemptions'] += 1

        # --- Rules ---
        for rule in MO_RULES:
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
                skipped['rules'] += 1
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
                added['rules'] += 1

        # --- Templates ---
        for template in MO_TEMPLATES:
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
                skipped['templates'] += 1
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
                added['templates'] += 1

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    total_added = sum(added.values())
    total_skipped = sum(skipped.values())
    print(
        f'MO Sunshine Law: '
        f'{added["exemptions"]} exemptions, {added["rules"]} rules, {added["templates"]} templates added; '
        f'{total_skipped} updated; {errors} errors'
    )
    write_receipt(
        script='build_mo',
        added=total_added,
        skipped=total_skipped,
        errors=errors,
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
