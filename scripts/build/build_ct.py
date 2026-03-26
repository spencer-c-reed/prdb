#!/usr/bin/env python3
"""Build Connecticut Freedom of Information Act data: exemptions, rules, and templates.

Covers Connecticut's Freedom of Information Act (CTFOIA), C.G.S. § 1-200 et seq.
Key features: 4-business-day response deadline, Freedom of Information Commission
(FOIC) quasi-judicial appeal with binding authority, $0.50/page copy rate, civil
penalties, and mandatory attorney fees for prevailing requesters. The FOIC is one
of the most active and effective FOI enforcement bodies in the country — its
decisions constitute persuasive and often binding authority in Connecticut courts.

Run: python3 scripts/build/build_ct.py
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
# Connecticut FOI exemptions are codified at C.G.S. § 1-210(b) (22 categories)
# and numerous specific exemptions throughout the General Statutes. The FOIC
# has quasi-judicial authority to interpret and apply these exemptions, and its
# decisions carry significant weight. Connecticut courts give substantial
# deference to FOIC interpretations of the FOIA.
# =============================================================================

CT_EXEMPTIONS = [
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(1)',
        'exemption_number': 'CTFOIA § 1-210(b)(1)',
        'short_name': 'Personnel, Medical, and Similar Files — Privacy',
        'category': 'privacy',
        'description': 'Personnel files, medical files, and similar files whose disclosure would constitute an unreasonable invasion of personal privacy are exempt from Connecticut FOI disclosure.',
        'scope': 'Personnel files, medical records, and similar records about identifiable individuals where disclosure would constitute an unreasonable invasion of personal privacy. Connecticut applies a balancing test: the privacy interest must substantially outweigh the public interest in disclosure. For public employees acting in their official capacity, the privacy interest is significantly reduced. Salary information, job title, dates of employment, and official actions are public for government employees. Connecticut courts and the FOIC have consistently held that disciplinary records for public employees involved in misconduct affecting the public are not protected by this exemption.',
        'key_terms': json.dumps([
            'personnel file', 'medical file', 'personal privacy', 'unreasonable invasion',
            'privacy balancing', 'public employee privacy', 'similar files',
            'personnel record', 'medical record',
        ]),
        'counter_arguments': json.dumps([
            'Salary, job title, employment dates, and official actions are public for government employees',
            'The FOIC has consistently held that disciplinary records for public employees involved in misconduct are not protected',
            'The "unreasonable invasion" standard requires the privacy harm to substantially outweigh the public interest — a high bar for official conduct',
            'Information about how an employee performed official duties is not a purely personal matter',
            'The FOIC applies a strong presumption of disclosure for records relating to the official conduct of public employees',
            'Challenge overbroad claims that entire personnel files are exempt — only portions with genuine privacy interests qualify',
        ]),
        'notes': 'C.G.S. § 1-210(b)(1) is one of the most frequently litigated CTFOIA exemptions. The FOIC has an extensive body of decisions applying the "unreasonable invasion" standard. Connecticut courts give significant deference to FOIC interpretations. The FOIC has consistently held that public employees have a reduced privacy expectation for records relating to their official duties.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(2)',
        'exemption_number': 'CTFOIA § 1-210(b)(2)',
        'short_name': 'Records Confidential by Statute',
        'category': 'statutory',
        'description': 'Records specifically exempted from disclosure by federal law, state statute, or regulations adopted under state statute are exempt from Connecticut FOI disclosure to the extent required by the applicable law.',
        'scope': 'Records specifically designated confidential by federal or Connecticut law. Examples include: tax records under C.G.S. § 12-15; motor vehicle records under DPPA; juvenile court records under C.G.S. § 46b-124; and certain mental health records. The exemption applies only to the extent required by the other law — if the other law has exceptions permitting disclosure, those exceptions apply. Agencies must identify the specific applicable statute, not simply assert "confidential by law." Aggregate and anonymized data from confidential records are generally public.',
        'key_terms': json.dumps([
            'confidential by statute', 'statutory confidentiality', 'federal law exemption',
            'state statute exemption', 'tax records', 'juvenile records', 'DPPA',
            'mandated confidentiality', 'regulatory confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute — a generic "confidential by law" claim is insufficient',
            'The other statute\'s exceptions and disclosure permissions apply',
            'Aggregate and anonymized data are generally public',
            'Administrative records of agencies holding confidential records are public',
            'Challenge whether the specific record actually falls within the other statute\'s scope',
        ]),
        'notes': 'The FOIC strictly requires specific citation to the applicable statute or regulation. Blanket claims of statutory confidentiality without specific citation are rejected. The FOIC also requires that the cited statute actually mandate (not merely permit) confidentiality.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(3)',
        'exemption_number': 'CTFOIA § 1-210(b)(3)',
        'short_name': 'Trade Secrets — Preliminary Drafts and Commercial Information',
        'category': 'commercial',
        'description': 'Records of a commercial entity\'s financial and commercial information, trade secrets, and preliminary drafts — including preliminary or final memoranda, correspondence, and financial or commercial information — that were submitted in confidence and whose disclosure would cause substantial harm are exempt.',
        'scope': 'Commercially valuable information submitted by private entities to government bodies where: (1) the information was submitted in confidence; (2) the information constitutes a trade secret or confidential commercial/financial data; and (3) disclosure would cause substantial harm to the competitive position of the submitter. Connecticut applies the Uniform Trade Secrets Act. Contract prices, amounts paid with public funds, and government-generated records do not qualify. The FOIC requires specific, documented competitive harm — not merely that the submitter prefers confidentiality.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information',
            'submitted in confidence', 'substantial competitive harm',
            'proprietary data', 'preliminary memorandum', 'UTSA',
            'commercial entity', 'confidential business information',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds are public regardless of vendor claims',
            'The submission must have been made in confidence — agency-generated records cannot be trade secrets',
            'The FOIC requires specific, documented competitive harm — not general claims of sensitivity',
            'The agency must independently evaluate trade secret claims, not defer to vendor designations',
            'Publicly available information cannot qualify as a trade secret',
            'Challenge whether information claimed as confidential was actually treated as such by the submitter',
        ]),
        'notes': 'Connecticut\'s trade secret exemption requires a specific showing of substantial competitive harm. The FOIC has rejected numerous trade secret claims for lack of specific harm documentation. Contract amounts and government expenditure records are uniformly treated as public. The FOIC applies heightened scrutiny to trade secret claims for government contracts.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(4)',
        'exemption_number': 'CTFOIA § 1-210(b)(4)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related documents prepared for the purpose of property acquisition or sale are exempt from disclosure until the acquisition or sale is complete or negotiations are terminated.',
        'scope': 'Formal property appraisals, feasibility studies, and related valuation documents prepared by or for a Connecticut public agency in connection with a pending acquisition or sale of real property. The exemption is time-limited — it expires automatically when the transaction closes or negotiations terminate. It protects the government\'s negotiating position. Post-transaction, all appraisal records are public. Internal budget estimates and general property value discussions do not qualify as formal appraisals.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'pre-acquisition appraisal', 'negotiating position', 'real property',
            'condemnation appraisal', 'pending acquisition',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction closes or negotiations terminate',
            'Challenge claims that negotiations remain "pending" after extended inactivity',
            'Informal budget estimates and internal discussions are not formal appraisals',
            'Post-transaction appraisals are fully public',
            'After condemnation judgment, all valuation records are public',
        ]),
        'notes': 'Connecticut\'s pre-acquisition appraisal exemption is narrow and time-limited. The FOIC has consistently held that the exemption does not apply to informal property value estimates or general budgetary discussions. Once transactions complete, all records are public.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(5)',
        'exemption_number': 'CTFOIA § 1-210(b)(5)',
        'short_name': 'Test Questions and Scoring Keys',
        'category': 'deliberative',
        'description': 'Questions, scoring keys, and related materials used in pre-employment tests, civil service examinations, and similar competitive evaluations are exempt prior to and during administration.',
        'scope': 'Unpublished test questions, answer keys, and scoring instructions for government-administered examinations including civil service tests, licensing examinations, and competitive hiring evaluations. The exemption is prospective — it expires after test administration and when results are finalized. General examination policies, scoring criteria in the abstract, and aggregate performance data are public.',
        'key_terms': json.dumps([
            'test questions', 'scoring key', 'examination questions', 'civil service exam',
            'pre-employment test', 'answer key', 'competitive evaluation',
            'test security', 'examination materials',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires after test administration — post-test materials may be public',
            'General examination policies and scoring methodology (not specific questions) are public',
            'Prior-year examination questions that are no longer in use may not remain protected',
            'Aggregate performance data and passing rates are public',
        ]),
        'notes': 'Connecticut\'s examination exemption is time-limited by nature. The FOIC has consistently held that examination security requires protection only until the test is administered. Post-administration, the public interest in accountability weighs heavily in favor of disclosure.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(10)',
        'exemption_number': 'CTFOIA § 1-210(b)(10)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege — including confidential legal communications between government entities and their attorneys — and attorney work product prepared in anticipation of litigation are exempt.',
        'scope': 'Confidential communications between government agencies and their attorneys for the purpose of obtaining or providing legal advice (attorney-client privilege), and documents prepared by attorneys specifically in anticipation of litigation (work product). The privilege requires that communications be for legal advice (not policy or business guidance), maintained in confidence, and not waived. The FOIC applies the common-law attorney-client privilege framework to government entities. Billing records and retainer agreements are generally not privileged. Work product requires anticipation of specific litigation.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'privileged communication', 'in anticipation of litigation',
            'government attorney', 'legal opinion', 'attorney work product',
        ]),
        'counter_arguments': json.dumps([
            'Communications for policy or business advice (not legal advice) are not privileged',
            'Billing records are generally public',
            'Waiver occurs when advice is disclosed in public proceedings or to non-essential parties',
            'Work product requires specific anticipated litigation — generalized future litigation claims are insufficient',
            'Facts underlying legal advice are not privileged',
            'The FOIC requires a privilege log identifying each withheld document with specific basis',
        ]),
        'notes': 'The FOIC requires agencies to provide privilege logs for attorney-client claims. The FOIC applies the privilege narrowly and has found it inapplicable where communications were for policy rather than legal advice. Connecticut courts give significant deference to FOIC privilege determinations.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(17)',
        'exemption_number': 'CTFOIA § 1-210(b)(17)',
        'short_name': 'Security and Emergency Procedures',
        'category': 'safety',
        'description': 'Records containing specific details of security measures, emergency response plans, or vulnerability assessments for critical infrastructure and public facilities — where disclosure would significantly impair the security of those facilities — are exempt.',
        'scope': 'Specific technical details of physical security systems, vulnerability assessments identifying exploitable weaknesses, and detailed emergency protocols for government facilities and critical infrastructure. The exemption requires a specific, articulated security risk from disclosure — not a generalized security classification. General emergency management policies, security budget information, and after-action reports focusing on policy improvements are public. The FOIC applies strict scrutiny to security exemption claims and frequently requires in camera review of claimed security documents.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'emergency response procedure',
            'critical infrastructure', 'physical security', 'facility security',
            'security protocol', 'cybersecurity', 'access control',
        ]),
        'counter_arguments': json.dumps([
            'General emergency management frameworks and policies are public',
            'Security budget and staffing information is public',
            'After-action reports focusing on policy improvements are public',
            'The FOIC requires specific articulation of how disclosure would impair security',
            'The FOIC frequently orders in camera review rather than accepting blanket security claims',
        ]),
        'notes': 'Connecticut\'s security exemption is one of the most carefully applied by the FOIC. The Commission consistently requires agencies to demonstrate specific security impairment, not merely classify records as security-related. The FOIC\'s in camera review procedure is a significant check on overbroad security claims.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(19)',
        'exemption_number': 'CTFOIA § 1-210(b)(19)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts of memoranda, communications, letters, correspondence, and records in which opinions are expressed or policies formulated or recommended are exempt when: (1) they are preliminary in character; and (2) disclosure would not serve the public interest.',
        'scope': 'Predecisional drafts containing opinions, policy recommendations, and deliberative content. The Connecticut FOIA\'s deliberative process exemption has a distinctive two-part test: the record must be (1) a preliminary draft, AND (2) disclosure must not serve the public interest. This is more requester-friendly than many states because even preliminary drafts must be released if disclosure serves the public interest. Purely factual material is not protected. Once a draft is adopted as final policy, the exemption does not apply. Working law must be disclosed.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'opinion', 'policy recommendation', 'predecisional', 'working paper',
            'draft document', 'advisory communication',
        ]),
        'counter_arguments': json.dumps([
            'Connecticut\'s deliberative process exemption has a two-part test — the agency must show BOTH that the record is preliminary AND that disclosure would not serve the public interest',
            'Even preliminary drafts must be disclosed if disclosure would serve the public interest',
            'Purely factual material in deliberative documents must be segregated and released',
            'Once a draft is adopted as final policy, the exemption evaporates',
            '"Working law" must be disclosed regardless of the deliberative process exemption',
            'The FOIC frequently finds that the public interest in disclosure outweighs the deliberative process interest',
        ]),
        'notes': 'Connecticut\'s deliberative process exemption is more nuanced than most state equivalents because of the public interest override. The FOIC has interpreted the public interest exception broadly, frequently finding that disclosure of deliberative documents would serve the public interest in government accountability. This makes the Connecticut exemption narrower in practice than similar provisions in other states.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(22)',
        'exemption_number': 'CTFOIA § 1-210(b)(22)',
        'short_name': 'Law Enforcement Investigative Files',
        'category': 'law_enforcement',
        'description': 'Records compiled in connection with the detection or investigation of crime, juvenile matters, or quasi-criminal proceedings — where disclosure would identify confidential informants, endanger life, reveal investigative techniques, or interfere with pending prosecutions — are exempt.',
        'scope': 'Records compiled by law enforcement agencies for the purpose of detecting or investigating crime, where disclosure would: (1) identify confidential informants; (2) endanger the life or physical safety of any person; (3) reveal investigative techniques not generally known; or (4) interfere with pending prosecution or criminal investigation. The exemption does not apply to completed investigations where prosecution has concluded. Incident reports, arrest records, and booking information are generally public. Connecticut law creates specific mandatory disclosure requirements for certain law enforcement records including arrest information.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement investigation', 'confidential informant',
            'investigative technique', 'pending prosecution', 'criminal intelligence',
            'investigation records', 'law enforcement file', 'detective records',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records, booking information, and incident reports are public regardless of investigation status',
            'Records of completed investigations where prosecution has concluded are generally public',
            'Each withheld record requires a specific harm showing — generic "investigation ongoing" labels are insufficient',
            'Factual information not implicating an enumerated harm must be segregated and released',
            'The FOIC applies strict scrutiny to law enforcement exemption claims and requires record-specific justification',
        ]),
        'notes': 'The FOIC has an extensive body of decisions on the law enforcement exemption. It consistently holds that the exemption is narrow and applies only to records whose disclosure would cause specific, enumerated harms. The FOIC frequently requires in camera review of claimed law enforcement records. Connecticut\'s mandatory disclosure requirements for arrest information further limit this exemption.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(11)',
        'exemption_number': 'CTFOIA § 1-210(b)(11)',
        'short_name': 'Records of Child Welfare and Protective Services',
        'category': 'privacy',
        'description': 'Records of the Department of Children and Families relating to child abuse, neglect, and child welfare investigations — including records identifying children, parents, and other parties in child protective proceedings — are exempt from disclosure.',
        'scope': 'Records maintained by DCF and related agencies involving child protective services, child abuse and neglect investigations, foster care, and related proceedings. The exemption is designed to protect children\'s safety and the integrity of child welfare investigations. Non-identifying aggregate statistics about child welfare programs, outcomes, and agency operations are public. Systematic failures in the child welfare system — patterns of agency conduct, budget decisions, and policy failures — may be public even if individual case records are not.',
        'key_terms': json.dumps([
            'child welfare', 'DCF records', 'child abuse investigation', 'child neglect',
            'foster care', 'child protective services', 'juvenile records',
            'child safety', 'child welfare investigation',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics about child welfare programs and outcomes are public',
            'Agency policy, budget, and administrative records are public even if individual case records are not',
            'Systemic failures in the child welfare system may be exposed through aggregate data and policy records',
            'Challenge whether specific records identify children or parents, as opposed to describing agency policy',
        ]),
        'notes': 'Connecticut\'s child welfare records exemption is among the most carefully protected in the statute. The DCF maintains extensive confidentiality obligations under both CTFOIA and the federal Child Abuse Prevention and Treatment Act (CAPTA). However, the FOIC has held that systematic agency failures and policy decisions are not shielded by individual record confidentiality.',
    },
    {
        'jurisdiction': 'CT',
        'statute_citation': 'C.G.S. § 1-210(b)(25)',
        'exemption_number': 'CTFOIA § 1-210(b)(25)',
        'short_name': 'Library and Borrower Records',
        'category': 'privacy',
        'description': 'Library records identifying the materials borrowed, requested, or accessed by an individual library patron are exempt to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying which specific library patrons accessed, borrowed, requested, or inquired about specific library materials or databases at Connecticut public libraries. The exemption covers physical circulation records, electronic database access, interlibrary loan requests, and reference inquiries revealing specific reading interests of identifiable individuals. Aggregate library usage statistics, collection data, and administrative records are public. The exemption applies to public libraries and public university libraries.',
        'key_terms': json.dumps([
            'library records', 'circulation records', 'library patron', 'borrower records',
            'database access', 'reading privacy', 'intellectual privacy',
            'library privacy', 'interlibrary loan',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library usage statistics and collection data are not covered',
            'Library administrative records, contracts, and budgets are public',
            'Records subpoenaed pursuant to a criminal investigation may be disclosed by court order',
            'The exemption covers what patrons read — not library operations or programming',
        ]),
        'notes': 'Connecticut\'s library patron privacy exemption reflects the strong public policy that individuals should be able to access information without fear of government surveillance. The FOIC has consistently upheld this exemption as one of the most absolute in the statute.',
    },
]

# =============================================================================
# RULES
# Connecticut FOIA, C.G.S. § 1-200 et seq.
# Key features: 4-business-day response deadline (one of the shortest in the
# country), Freedom of Information Commission (FOIC) quasi-judicial binding
# appeal, $0.50/page copy rate, civil penalties, mandatory attorney fees for
# prevailing requesters.
# =============================================================================

CT_RULES = [
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '4',
        'day_type': 'business',
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'Connecticut has one of the shortest public records response deadlines in the country — 4 business days from receipt of a request. Within 4 business days, the agency must: (1) provide inspection or copies; (2) notify the requester when records will be available; or (3) deny the request in writing with specific reasons and statutory citation. The 4-business-day clock is strict. The FOIC has consistently held that failure to respond within 4 business days is a CTFOIA violation. Many agencies use the 4-day period to provide an initial response with an estimated production date for larger requests.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'prompt_production_required',
        'param_value': 'promptly_or_schedule_within_4_days',
        'day_type': 'business',
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'If the agency cannot provide all records within 4 business days, it must acknowledge the request and provide a specific schedule for when records will be made available. The production schedule must be reasonable — the FOIC has found unreasonably long production timelines to be CTFOIA violations even when the initial 4-day acknowledgment was timely. For large requests, Connecticut practice involves agencies providing rolling production with updated timelines, but the FOIC monitors these timelines for reasonableness.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate_per_page',
        'param_value': '0.50',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-212(a)',
        'notes': 'Connecticut agencies may charge a fee not exceeding $0.50 per page for copies of public records. This rate applies to paper copies. For electronic records, agencies may charge the cost of creating and transmitting digital copies, which is typically minimal or zero for email delivery. Connecticut does not have a specific provision for charging staff time for searching or reviewing records — the standard practice is to charge only for actual reproduction costs. Agencies may not charge for time spent redacting records. If fees exceed $10, agencies should provide an advance estimate.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion_and_foic_oversight',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-212(d)',
        'notes': 'Connecticut agencies may waive fees at their discretion under C.G.S. § 1-212(d). The FOIC has encouraged fee waivers for news media, nonprofit organizations, and academic researchers requesting records for public interest purposes. If an agency unreasonably refuses to waive fees for a clearly public interest request, the FOIC may consider this as evidence of bad faith in a complaint proceeding. There is no automatic mandatory fee waiver for any specific requester category, but the FOIC\'s oversight creates practical pressure for reasonable fee practices.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'appeal_deadline',
        'param_key': 'foic_complaint_deadline_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': 'C.G.S. § 1-206(b)(1)',
        'notes': 'A requester denied access to public records — or whose request is not responded to within 4 business days — may file a complaint with the Freedom of Information Commission (FOIC) within 30 calendar days of the denial or the expiration of the 4-day response period. The FOIC is a quasi-judicial body with binding authority to order disclosure and impose civil penalties. FOIC proceedings are less expensive than court but require a formal complaint. The FOIC schedules hearings, takes evidence, and issues written decisions. FOIC decisions are entitled to substantial judicial deference and carry precedential weight.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'appeal_deadline',
        'param_key': 'foic_decision_binding',
        'param_value': 'binding_subject_to_judicial_review',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-206',
        'notes': 'FOIC decisions are binding on the parties and are subject to judicial review by appeal to the Superior Court. The standard of judicial review for FOIC factual findings is substantial evidence. Legal interpretations by the FOIC receive substantial deference. FOIC decisions are the primary source of CTFOIA jurisprudence — they constitute an extensive, well-organized body of precedent. Requesters should research relevant FOIC decisions before filing a complaint, as the FOIC will apply its prior holdings. FOIC decisions are searchable on the FOIC website.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_range',
        'param_value': 'up to $1,000 per violation',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-206(b)(2)',
        'notes': 'The FOIC may impose civil penalties of up to $1,000 per violation for willful or knowing violations of the CTFOIA. Penalties are not automatic — the FOIC considers the nature and severity of the violation, the agency\'s history of compliance, and the circumstances. The FOIC has imposed penalties for systematic non-compliance, bad-faith withholding, and deliberate obstruction. Penalties are paid to the state treasury. The FOIC may also recommend referral to the State Ethics Commission or other oversight bodies for egregious violations.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-206(b)(2)',
        'notes': 'Connecticut courts may award attorney fees and costs to requesters who prevail in appeals from FOIC decisions or in independent court actions challenging CTFOIA violations. While not as explicitly mandatory as New Jersey\'s provision, Connecticut courts consistently award fees to prevailing requesters. The FOIC may also recommend fee awards. The availability of attorney fees makes CTFOIA enforcement economically viable for complex cases involving significant violations.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'Connecticut agencies may NOT require requesters to identify themselves or state the purpose of their request. The CTFOIA provides a universal right of access regardless of identity or stated purpose. The FOIC has consistently held that requiring identification as a condition of processing a request is a CTFOIA violation. Anonymous requests are valid. Agencies may request contact information for delivery purposes but providing it must be voluntary.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure rests on the agency, not the requester. The FOIC and Connecticut courts apply a strict construction against exemptions — any ambiguity is resolved in favor of disclosure. The agency must affirmatively demonstrate that each specific exemption applies to each specific withheld record. Generic assertions of exemption categories without record-specific justification are rejected by the FOIC.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_with_specific_citation',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'When denying a CTFOIA request, agencies must provide a written response stating the specific statutory basis for withholding — citing the specific subsection of § 1-210(b) or other applicable provision. A denial without a specific statutory citation is legally deficient and the FOIC treats it as a denial without justification. The denial must be in writing. The FOIC has consistently held that oral denials do not satisfy the CTFOIA\'s requirements.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-210(a)',
        'notes': 'Connecticut agencies must release all reasonably segregable non-exempt portions of records when only part of a record qualifies for an exemption. Blanket withholding of documents containing some exempt content is a CTFOIA violation. The FOIC frequently orders partial disclosure, redacting only the exempt portions and requiring release of the remainder. In camera review allows the FOIC to verify that agencies are properly segregating exempt from non-exempt content.',
    },
    {
        'jurisdiction': 'CT',
        'rule_type': 'initial_response',
        'param_key': 'foic_in_camera_review',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'C.G.S. § 1-206(b)',
        'notes': 'The FOIC has authority to conduct in camera review of withheld records to assess whether claimed exemptions actually apply. In camera review is a powerful tool that allows the FOIC to independently evaluate exemption claims without disclosing potentially exempt content to the requester. The FOIC uses in camera review routinely for law enforcement, security, and deliberative process claims. This prevents agencies from successfully claiming exemptions for records that don\'t actually qualify.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

CT_TEMPLATES = [
    {
        'jurisdiction': 'CT',
        'record_type': 'general',
        'template_name': 'General Connecticut Freedom of Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Freedom of Information Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — C.G.S. § 1-200 et seq.

Dear Freedom of Information Officer:

Pursuant to the Connecticut Freedom of Information Act (CTFOIA), C.G.S. § 1-200 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes costs for both parties.

I am willing to pay copying fees not exceeding $0.50 per page as permitted by C.G.S. § 1-212(a). I am not willing to pay for staff time spent reviewing or redacting records, which is not a permissible CTFOIA fee. If fees will exceed ${{fee_limit}}, please provide an advance estimate so I may refine my request.

The burden of demonstrating that any record is exempt from disclosure rests on the agency. If any records are withheld, I request that you: (1) identify each record or category of records withheld; (2) state the specific subsection of C.G.S. § 1-210(b) (or other applicable statutory provision) that authorizes withholding; (3) explain how that provision applies to each specific withheld record; and (4) confirm that all reasonably segregable non-exempt portions have been released.

Under C.G.S. § 1-210(a), please respond within 4 business days. If records cannot be fully provided within 4 business days, please notify me within that period with a specific production schedule.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request under C.G.S. § 1-212(d). These records concern {{public_interest_explanation}}, a matter of significant public interest and government accountability. I am {{requester_category_description}} with no commercial purpose. Disclosure will benefit the public by {{public_benefit_explanation}}. If records are provided electronically, copying costs are minimal or zero.

I note that the Freedom of Information Commission (FOIC) has encouraged agencies to waive fees for news media, nonprofit, and academic public interest requests, and that unreasonable fee demands for public interest requests may be considered in the context of any FOIC complaint.''',
        'expedited_language': '''I request that this CTFOIA request be processed as expeditiously as possible. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if clarification would allow faster production.''',
        'notes': 'General CTFOIA template. Key CT features: (1) 4-business-day response deadline — one of the shortest in the country; (2) FOIC is a quasi-judicial body with binding authority — file complaint within 30 days of denial; (3) $0.50/page copy rate — no staff time charges; (4) civil penalties up to $1,000 per violation; (5) attorney fees available for prevailing requesters; (6) burden of proof on agency; (7) specific C.G.S. § 1-210(b) subsection required in denial; (8) FOIC conducts in camera review; (9) use "CTFOIA" and "C.G.S. § 1-200" — not federal "FOIA"; (10) deliberative process exemption has public interest override.',
    },
    {
        'jurisdiction': 'CT',
        'record_type': 'law_enforcement',
        'template_name': 'Connecticut FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Freedom of Information Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Connecticut Freedom of Information Act Request — Law Enforcement Records, C.G.S. § 1-200 et seq.

Dear Freedom of Information Officer:

Pursuant to the Connecticut Freedom of Information Act (CTFOIA), C.G.S. § 1-200 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and police offense reports
- Arrest records, booking information, and charging documents
- Use-of-force reports and related documentation
- Body-worn camera and dash camera footage and metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Officer disciplinary records
- Internal affairs records (for concluded matters)
- Complaints against officers (with outcomes)

Regarding the investigative records exemption at C.G.S. § 1-210(b)(22): Arrest records, booking information, and incident reports are public records regardless of investigation status. Any claimed exemption under § 1-210(b)(22) must: (1) cite the specific harm enumerated in that subsection; (2) identify how each specific withheld record implicates that harm; and (3) confirm that all segregable non-exempt portions have been released.

The Connecticut Freedom of Information Commission has jurisdiction to review claimed exemptions through in camera review and may independently assess whether records qualify for the claimed exemption. Generic "ongoing investigation" labels are insufficient under CTFOIA.

Fees: I am willing to pay up to ${{fee_limit}} at the $0.50/page rate. Please provide advance notice if fees will exceed this amount.

Please respond within 4 business days per C.G.S. § 1-210(a).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These law enforcement records concern {{public_interest_explanation}}, a matter of public accountability. I am {{requester_category_description}} with no commercial purpose. If provided electronically, copying costs are minimal. The FOIC has encouraged fee waivers for public interest requests of this type.''',
        'expedited_language': '''I request expedited processing of this CTFOIA request. These records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'Connecticut law enforcement CTFOIA template. Key features: (1) 4-business-day response deadline; (2) arrest records, incident reports, and booking information are public regardless of investigation status; (3) investigative records exemption (§ 1-210(b)(22)) requires specific harm showing per record; (4) FOIC conducts in camera review of claimed exemptions; (5) FOIC complaint available within 30 days; (6) civil penalties up to $1,000 per violation; (7) attorney fees for prevailing requesters.',
    },
    {
        'jurisdiction': 'CT',
        'record_type': 'education',
        'template_name': 'Connecticut FOIA Request — Education Records (Non-Student)',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Freedom of Information Officer / Superintendent / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Connecticut Freedom of Information Act Request — Education Records, C.G.S. § 1-200 et seq.

Dear Custodian of Records:

Pursuant to the Connecticut Freedom of Information Act (CTFOIA), C.G.S. § 1-200 et seq., I request copies of the following records relating to {{school_district_or_institution}}:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

Note: This request does not seek individually identifiable student education records protected under FERPA (20 U.S.C. § 1232g) or C.G.S. § 1-210(b)(17). I am seeking records relating to [school administration / personnel / budget / policies / curriculum / facility / other non-student records].

Specifically, I request:
- Administrative and policy records (not individual student records)
- Budget documents, expenditure records, and financial information
- Personnel records limited to: name, position, job classification, and salary
- Curriculum materials, instructional policies, and academic program information
- Facility inspection, safety, and maintenance records
- Correspondence relating to the above

Regarding personnel records: Under CTFOIA, the names, positions, salaries, and official duties of public employees — including school district employees — are public records. Please provide all personnel information to the extent required by C.G.S. § 1-210.

Under C.G.S. § 1-210(a), please respond within 4 business days.

I am willing to pay up to ${{fee_limit}} at the standard $0.50/page rate per C.G.S. § 1-212(a). Please provide an advance estimate if fees will exceed this amount.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request under C.G.S. § 1-212(d). These records concern the administration of public education and public expenditure of school funds — a matter of significant public interest. I am {{requester_category_description}} with no commercial purpose. Disclosure will benefit the public by {{public_benefit_explanation}}.''',
        'expedited_language': '''I request expedited processing. These education records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'Connecticut education CTFOIA template (non-student records). Key features: (1) explicitly distinguishes from FERPA-protected student records; (2) targets administrative, financial, and policy records that are unquestionably public; (3) salary and personnel information for school employees is public; (4) FOIC has jurisdiction over school district CTFOIA disputes; (5) 4-business-day deadline; (6) FOIC has extensive precedent on school district compliance.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in CT_EXEMPTIONS:
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

    print(f'CT exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in CT_RULES:
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

    print(f'CT rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in CT_TEMPLATES:
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

    print(f'CT templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'CT total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ct', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
