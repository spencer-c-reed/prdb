#!/usr/bin/env python3
"""Build Kentucky Open Records Act data: exemptions, rules, and templates.

Covers Kentucky's Open Records Act (ORA), KRS 61.870-61.884.
Kentucky has a strong public records law with a 5-business-day response
deadline, a binding Attorney General appeal process (unique and highly
effective), $0.10/page copy fee (one of the lowest in the country),
attorney's fees for prevailing requesters, and strong AG enforcement.
The AG opinion process is faster and cheaper than court enforcement and
creates binding precedent on agencies.

Run: python3 scripts/build/build_ky.py
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
# Kentucky ORA, KRS 61.878, provides the list of exemptions. Kentucky courts
# strictly construe exemptions against the agency — KRS 61.882(3) provides
# that any person denied inspection has the right to appeal to the AG, whose
# decision is binding on the agency unless challenged in circuit court.
# The AG has issued thousands of opinions interpreting the ORA and its
# exemptions, creating a rich body of interpretive guidance. The AG's Office
# of Open Records serves as an accessible enforcement mechanism.
# =============================================================================

KY_EXEMPTIONS = [
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(a)',
        'exemption_number': 'KRS 61.878(1)(a)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, correspondence with private individuals other than correspondence that is intended to give notice of final agency action, recommendations, and memoranda in which opinions are expressed or policies formulated or recommended are exempt from public inspection.',
        'scope': 'Predecisional deliberative documents including: preliminary drafts of agency documents, notes and working papers, correspondence with private individuals that is not notice of final action, internal recommendations, and memoranda expressing opinions or policy recommendations. The exemption does not protect: (1) factual material within deliberative documents; (2) documents that have been adopted as the agency\'s final position; (3) "working law" — the standards and criteria the agency actually applies to the public. Kentucky AG opinions have developed extensive guidance on the scope of this exemption, consistently narrowing it in favor of disclosure. The exemption is one of the most heavily litigated in Kentucky\'s ORA.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'recommendation',
            'advisory memorandum', 'working paper', 'draft document', 'intra-agency',
            'opinion', 'policy formulation', 'KRS 61.878(1)(a)',
        ]),
        'counter_arguments': json.dumps([
            'Factual material within deliberative documents must be segregated and released — the exemption covers only opinion and recommendation portions',
            'Once a draft or recommendation is adopted as the agency\'s final position, the exemption expires',
            '"Working law" — the criteria and standards the agency actually applies to public decisions — must be disclosed even if in internal documents',
            'Challenge claims that entire documents are deliberative — require specific identification of each opinion-based portion',
            'Kentucky AG opinions consistently hold that this exemption must be narrowly construed',
            'Communications with persons outside the agency lose their predecisional character',
            'File a KRS 61.880(2) AG appeal — the AG has extensive experience rejecting overbroad deliberative process claims',
        ]),
        'notes': 'KRS 61.878(1)(a) is the most frequently cited exemption in Kentucky ORA disputes and also the most heavily scrutinized by the AG\'s Office. Kentucky AG opinions consistently require agencies to segregate and release factual material and to demonstrate that specific documents (not just general categories) are predecisional and deliberative. See OAG 87-37, OAG 92-117, and numerous subsequent opinions. The AG appeal process is the most efficient way to challenge overbroad claims under this exemption.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(b)',
        'exemption_number': 'KRS 61.878(1)(b)',
        'short_name': 'Personnel Files — Employee Privacy',
        'category': 'privacy',
        'description': 'Personnel files and preliminary and other supporting documentation directly related to a specifically named individual, including preliminary notes, are exempt to the extent that their disclosure would constitute a clearly unwarranted invasion of personal privacy.',
        'scope': 'Personnel files and related supporting documentation where disclosure would constitute a "clearly unwarranted invasion of personal privacy." The exemption requires a balancing test: the public interest in disclosure must be weighed against the privacy interest in withholding. For public employees acting in their official capacity, the public interest typically outweighs privacy. Information about official misconduct, disciplinary actions, salary, job title, and performance related to official duties is generally public. Kentucky AG opinions have consistently held that personnel decisions affecting the public interest must be disclosed. Information about purely private personal matters (medical conditions, personal financial data, home address) may be withheld.',
        'key_terms': json.dumps([
            'personnel file', 'personal privacy', 'clearly unwarranted invasion',
            'public employee', 'salary', 'disciplinary record', 'employment record',
            'official duty', 'privacy interest', 'balancing test',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a "clearly unwarranted" invasion — a high standard that the agency must meet for each withheld item',
            'Salary, job title, and employment status of public employees are public under Kentucky AG opinions',
            'Official disciplinary actions are public — the "clearly unwarranted" standard is not met when disclosure serves the public interest in accountability',
            'Kentucky AG opinions have held that misconduct investigations involving public employees are generally public after completion',
            'Challenge overbroad redactions by filing a KRS 61.880(2) AG appeal — the AG has extensive experience narrowing this exemption',
            'The balancing test favors disclosure when the privacy intrusion is modest and the public interest is significant',
        ]),
        'notes': 'KRS 61.878(1)(b) has been interpreted extensively by the Kentucky AG. The "clearly unwarranted invasion of personal privacy" standard requires genuine balancing — not a blanket protection for all personnel records. Kentucky AG opinions have been particularly protective of public employee accountability: disciplinary records, misconduct investigations, and employment decisions are generally public. See OAG 91-210, OAG 94-ORD-113.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(h)',
        'exemption_number': 'KRS 61.878(1)(h)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement agencies or agencies involved in administrative adjudication that are compiled in the process of detecting and investigating statutory or regulatory violations are exempt if disclosure would harm the investigation or subject someone to undue hardship, or if the records contain information furnished by the subject.',
        'scope': 'Law enforcement investigation records compiled in the process of detecting or investigating statutory or regulatory violations, where disclosure would: (1) harm the investigation; (2) subject a person to undue hardship; or (3) involve information furnished to the agency by the subject of the investigation. The exemption terminates when enforcement action is completed (charges filed, citation issued, case closed). Kentucky AG opinions have narrowly construed this exemption — agencies must demonstrate harm specific to each withheld record. Completed investigation files are generally public. Incident reports and arrest records are public.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'regulatory investigation',
            'active investigation', 'statutory violation', 'enforcement action',
            'investigation records', 'confidential source', 'investigative technique',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only while investigation is ongoing — once enforcement action concludes, records are public',
            'The agency must show specific harm from disclosure of each withheld record — categorical denial is insufficient',
            'Incident reports and arrest records are public regardless of investigation status',
            'Kentucky AG opinions consistently hold that completed investigation files must be disclosed',
            'File a KRS 61.880(2) AG appeal — the AG has extensive experience narrowing overbroad law enforcement exemption claims',
            'Administrative records, budget, and policy documents of law enforcement agencies are public',
        ]),
        'notes': 'KRS 61.878(1)(h) is strictly construed by Kentucky AG opinions. The exemption terminates on completion of enforcement action. Kentucky AG opinions have developed a clear rule: once charges are filed, a case is closed, or prosecution concludes, investigation records are subject to full ORA disclosure. See OAG 86-32, OAG 97-ORD-20.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(k)',
        'exemption_number': 'KRS 61.878(1)(k)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'All public records or information the disclosure of which is prohibited by federal law or regulation, or by the privacy provisions of the federal Family Educational Rights and Privacy Act, and all public records or information the disclosure of which is prohibited or restricted or otherwise made confidential by enactment of the Kentucky General Assembly are exempt.',
        'scope': 'Records whose disclosure is prohibited by federal or Kentucky state law. Specifically includes attorney-client privileged communications and work product (recognized by Kentucky AG opinions as within the scope of this exemption and KRS 61.878(1)(l)). Also includes records protected by federal statutes such as FERPA, HIPAA, and other federal confidentiality laws. The exemption is limited to records specifically covered by an identifiable federal or state statute — it does not create a general implied exemption.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'federal law prohibition',
            'FERPA', 'HIPAA', 'state confidentiality statute', 'federal prohibition',
            'Kentucky General Assembly', 'statutory confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific federal or state statute that prohibits disclosure — a general claim is insufficient',
            'Attorney-client privilege is narrow — it covers legal advice only, not policy or business guidance',
            'Billing records and general correspondence with outside counsel are not privileged',
            'Waiver occurs when the agency uses the privileged advice in public decision-making',
            'Kentucky AG opinions strictly interpret this exemption — the statutory prohibition must specifically cover the records at issue',
        ]),
        'notes': 'KRS 61.878(1)(k) incorporates federal and state statutory confidentiality requirements into the ORA framework. Kentucky AG opinions have held that the exemption requires identification of the specific statute and demonstration that it specifically covers the records at issue. The attorney-client privilege is recognized as an implied protection under KRS 61.878(1)(l) as well.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(c)',
        'exemption_number': 'KRS 61.878(1)(c)',
        'short_name': 'Test Instruments and Evaluation Materials',
        'category': 'deliberative',
        'description': 'Records confidentially disclosed to an agency and compiled and maintained for scientific research or academic examination or evaluation purposes, including preliminary drafts, notes, recommendations, and memoranda in which opinions are expressed or policies formulated or recommended are exempt.',
        'scope': 'Scientific research data, academic examination materials, and evaluation records that are confidentially provided to agencies for the purpose of scientific or academic evaluation. Covers examination questions, test keys, scoring rubrics, and similar materials used in competitive examinations by government agencies. The exemption protects the integrity of testing and evaluation processes — once an examination is concluded and results are final, some materials may become subject to disclosure. Does not protect general administrative records of testing programs.',
        'key_terms': json.dumps([
            'test instrument', 'evaluation material', 'scientific research', 'examination',
            'test questions', 'scoring rubric', 'competitive examination',
            'academic evaluation', 'confidential research',
        ]),
        'counter_arguments': json.dumps([
            'Once an examination is concluded and final, some materials may be subject to disclosure',
            'Aggregate test results and statistical data are generally public',
            'Administrative records of testing programs (costs, contractors, schedules) are public',
            'Challenge the agency\'s claim that materials are "confidentially disclosed" if they are government-generated',
        ]),
        'notes': 'KRS 61.878(1)(c) protects examination integrity for government testing programs. The exemption has been applied to civil service examinations, professional licensing examinations, and similar competitive processes. Kentucky AG opinions have held that some examination materials may be disclosed after the relevant examination cycle concludes.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(i)',
        'exemption_number': 'KRS 61.878(1)(i)',
        'short_name': 'Preliminary Recommendations — Specific Agency Actions',
        'category': 'deliberative',
        'description': 'Preliminary recommendations and preliminary memoranda in which opinions are expressed or policies formulated or recommended regarding the acquisition of real property, the award of contracts, or the granting of licenses or permits are exempt until final action is taken.',
        'scope': 'Preliminary recommendations and memoranda specifically relating to: (1) acquisition of real property; (2) award of contracts; or (3) granting of licenses or permits. The exemption is time-limited — it applies only until final action is taken. Once the agency makes a final decision (awards the contract, grants the license, acquires the property), the underlying recommendations and supporting documents become public. This exemption protects the agency\'s negotiating position and deliberative process for specific transactional decisions.',
        'key_terms': json.dumps([
            'preliminary recommendation', 'contract award', 'real property acquisition',
            'license', 'permit', 'competitive bidding', 'procurement',
            'pre-award', 'predecisional', 'transactional deliberation',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when final action is taken — all documents become public after contract award, license grant, or property acquisition',
            'Challenge the agency\'s claim that a decision is still "preliminary" if final action has been taken',
            'Post-award records, including evaluation criteria and scoring sheets, are public after contract award',
            'Kentucky AG opinions consistently hold that competitive procurement records are public after contract award',
        ]),
        'notes': 'KRS 61.878(1)(i) specifically protects certain transactional deliberations until final action. Kentucky AG opinions have held that this exemption terminates absolutely upon final agency action — post-award procurement records are subject to full disclosure. This is important for government contracting accountability.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(e)',
        'exemption_number': 'KRS 61.878(1)(e)',
        'short_name': 'Medical and Personal Health Records',
        'category': 'privacy',
        'description': 'Public records containing medical, psychiatric, psychological, or other similar individually identifiable health information concerning an individual are exempt from public inspection to protect patient privacy.',
        'scope': 'Individually identifiable medical, psychiatric, psychological, and health records held by government agencies including public hospitals, correctional facilities, public health departments, and agencies providing health services. Aggregate health statistics and de-identified data are public. Policies, procedures, and budget records of public health agencies are public. The exemption is consistent with HIPAA requirements for covered government entities.',
        'key_terms': json.dumps([
            'medical record', 'health information', 'psychiatric record', 'psychological record',
            'patient privacy', 'HIPAA', 'individually identifiable', 'treatment record',
            'mental health record', 'health care',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and de-identified data are public',
            'Policies and procedures of public health agencies are public',
            'Budget and administrative records of health agencies are fully public',
            'Challenge whether specific records actually contain individually identifiable health information',
        ]),
        'notes': 'KRS 61.878(1)(e) protects individually identifiable health information consistent with HIPAA and general privacy principles. The exemption is well-established and uncontroversial. It does not protect aggregate data or agency operations records.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(j)',
        'exemption_number': 'KRS 61.878(1)(j)',
        'short_name': 'Genealogical Information and Personal Data',
        'category': 'privacy',
        'description': 'Records containing information of a personal nature where the public disclosure thereof would constitute a clearly unwarranted invasion of personal privacy, such as birth records, adoption records, social security numbers, and other similar personal data are exempt.',
        'scope': 'Personal identifying information including: birth records (to the extent identifying), adoption records, Social Security numbers, and similar personal data whose disclosure would constitute a clearly unwarranted invasion of privacy. Kentucky AG opinions apply the same "clearly unwarranted invasion" balancing test as for personnel records. Information about public employees and officials in their official capacity does not meet this standard. Information already publicly available cannot be withheld under this exemption.',
        'key_terms': json.dumps([
            'personal privacy', 'Social Security number', 'birth record', 'adoption record',
            'personal data', 'clearly unwarranted invasion', 'personal identifying information',
            'PII', 'genealogical information',
        ]),
        'counter_arguments': json.dumps([
            'The "clearly unwarranted" standard requires genuine harm from disclosure — not mere inconvenience or preference for privacy',
            'Information already in the public domain cannot be withheld under this exemption',
            'Challenge overbroad redactions where personal identifiers have been removed along with clearly public information',
            'Kentucky AG opinions require agencies to redact specific protected identifiers rather than withhold entire documents',
        ]),
        'notes': 'KRS 61.878(1)(j) is a general personal privacy exemption applied by the AG Office using the "clearly unwarranted invasion" balancing test consistent with KRS 61.878(1)(b). Kentucky AG opinions require agencies to redact specific personal identifiers rather than withhold entire records.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(n)',
        'exemption_number': 'KRS 61.878(1)(n)',
        'short_name': 'Software and Computer Security',
        'category': 'safety',
        'description': 'Software programs used by agencies, including source code for such programs, are exempt from disclosure, as are records containing information specifically compiled by an agency to detect or prevent unauthorized computer access.',
        'scope': 'Software source code, compiled programs, and records specifically compiled to detect or prevent unauthorized computer access to government systems. The exemption is narrow: it applies to the software programs themselves and to records specifically about computer security vulnerabilities. It does not protect records stored in or produced by government software systems. Government databases may contain the software program (exempt) and the data records (public) — the exemption covers only the former.',
        'key_terms': json.dumps([
            'software program', 'source code', 'computer security', 'cybersecurity',
            'unauthorized access', 'vulnerability information', 'security system',
            'computer program', 'system security',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers software programs themselves, not records stored in those programs',
            'Government databases contain public records — the database software may be exempt but the underlying data is public',
            'Challenge claims that entire computer systems or databases are exempt under this provision',
            'Budget and contract records for software purchases and IT services are public',
        ]),
        'notes': 'KRS 61.878(1)(n) protects software programs and specific security vulnerability records. Kentucky AG opinions have consistently held that this exemption does not extend to records maintained by government computer systems — only to the systems themselves. Government data stored in proprietary databases remains public.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(l)',
        'exemption_number': 'KRS 61.878(1)(l)',
        'short_name': 'Administrative Proceedings — Preliminary Information',
        'category': 'deliberative',
        'description': 'Correspondence and other documents relating to a specific proposed or pending administrative proceeding before an agency, board, commission, or authority, including information received during the administrative proceeding, are exempt until the proceeding is complete.',
        'scope': 'Correspondence and documents specifically related to a pending administrative proceeding — similar to the law enforcement investigation exemption but for administrative (non-criminal) proceedings. The exemption applies only while proceedings are pending — once the administrative matter is resolved (final order issued, case dismissed, settlement reached), the records become public. The exemption does not protect general agency correspondence or records unrelated to a specific pending proceeding.',
        'key_terms': json.dumps([
            'administrative proceeding', 'pending proceeding', 'agency proceeding',
            'board proceeding', 'commission hearing', 'administrative hearing',
            'regulatory proceeding', 'pending administrative action',
        ]),
        'counter_arguments': json.dumps([
            'The exemption applies only while the proceeding is pending — final orders and completed proceedings are public',
            'General agency correspondence unrelated to a specific pending proceeding is not covered',
            'Once a final order is issued or a case is settled, all related records become public',
            'Kentucky AG opinions require agencies to identify the specific pending proceeding for each withheld record',
        ]),
        'notes': 'KRS 61.878(1)(l) is the administrative proceedings analog to the law enforcement investigation exemption. Kentucky AG opinions hold that it terminates upon completion of the proceeding. Agencies may not characterize all regulatory files as "pending" to maintain permanent exemption.',
    },
    {
        'jurisdiction': 'KY',
        'statute_citation': 'KRS 61.878(1)(f)',
        'exemption_number': 'KRS 61.878(1)(f)',
        'short_name': 'Tax Return Information',
        'category': 'statutory',
        'description': 'State income tax returns and information contained in income tax returns, including supporting documents, are exempt from public disclosure under Kentucky\'s revenue confidentiality statutes cross-referenced in the ORA.',
        'scope': 'Individual and business state income tax returns and related financial information submitted to the Kentucky Department of Revenue. Aggregate tax revenue statistics and department operational records are public. Tax delinquency notices and final court judgments in tax enforcement cases are generally accessible through court records. The exemption covers taxpayer-specific returns, not the agency\'s administrative operations.',
        'key_terms': json.dumps([
            'tax return', 'income tax', 'Kentucky Department of Revenue', 'tax information',
            'taxpayer records', 'state tax', 'tax confidentiality', 'KRS 131',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics are public',
            'Tax delinquency judgments in court records are accessible',
            'Information about the Department\'s own administrative operations is public',
            'Challenge whether specific records are "tax return information" vs. general correspondence',
        ]),
        'notes': 'Kentucky\'s tax return confidentiality is incorporated into the ORA through KRS 61.878(1)(f) and the revenue statutes in KRS Chapter 131. The exemption is well-established for taxpayer-specific data.',
    },
]

# =============================================================================
# RULES
# Kentucky Open Records Act, KRS 61.870-61.884.
# Key features: 5-business-day response deadline; binding AG appeal process
# (unique in the country — AG opinions are binding on agencies unless
# challenged in court within 30 days); $0.10/page (lowest standard rate in US);
# attorney's fees for prevailing requester; no criminal penalties but strong
# AG enforcement; AG opinion issued within 20 days.
# =============================================================================

KY_RULES = [
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'KRS 61.880(1)',
        'notes': 'Kentucky agencies must respond to Open Records Act requests within 5 business days of receiving the written request. KRS 61.880(1) requires that the agency either: (1) make the records available; or (2) deny the request in writing with specific citation to the applicable statutory exemption. The 5-day deadline is strictly enforced by the Kentucky AG. Failure to respond within 5 business days constitutes a per se violation of the ORA that the AG will cite in any appeal. The 5-day period may be extended in extraordinary circumstances for large or complex requests, but only with written notice to the requester stating the reason and anticipated production date.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_mandatory_with_specific_citation',
        'day_type': None,
        'statute_citation': 'KRS 61.880(1)',
        'notes': 'KRS 61.880(1) requires that any denial of an Open Records request be in writing and cite the specific exception under KRS 61.878 justifying the denial. The written denial must: (1) state that the request is denied; (2) identify the specific exception under KRS 61.878 (by subsection); and (3) briefly explain why the exception applies to the records at issue. A denial citing only general categories without specific statutory subsections is procedurally insufficient. The AG\'s Office treats insufficient denials as independent ORA violations. This written denial requirement makes Kentucky\'s ORA one of the most procedurally protective statutes in the country.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'KRS 61.874(3)',
        'notes': 'Kentucky\'s standard copying fee is $0.10 per page — one of the lowest statutory copy rates in the United States and dramatically lower than the $0.25/page that most states allow. KRS 61.874(3) sets the $0.10 standard and limits agencies to actual reproduction costs. Agencies may not charge for staff time spent locating, reviewing, or redacting records. For electronic records delivered by email, the actual cost is zero. Kentucky\'s very low copy rate reflects the legislature\'s strong intent to minimize financial barriers to public access.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'KRS 61.874(3)',
        'notes': 'Kentucky does not mandate fee waivers but agencies have discretion to reduce or waive the $0.10/page fee. Given the already low copy rate, fee waiver arguments are less critical in Kentucky than in states with higher per-page rates. For electronic records provided by email, the actual cost is zero, making the fee question largely moot for digital records. Requesters who need paper copies may still request a waiver based on public interest grounds.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'appeal_deadline',
        'param_key': 'ag_appeal_deadline_days',
        'param_value': 'available_after_denial',
        'day_type': None,
        'statute_citation': 'KRS 61.880(2)',
        'notes': 'Kentucky\'s binding AG appeal process is the most distinctive feature of the state\'s ORA and one of the most effective administrative appeal mechanisms in the country. Under KRS 61.880(2), a requester who is denied access to records may appeal to the Kentucky Attorney General\'s Office of Open Records. The appeal must be filed within the time provided after the denial. The AG must issue a written opinion within 20 calendar days of receiving the appeal. The AG opinion is BINDING on the agency — the agency must comply with the AG\'s decision unless it files a legal action in circuit court within 30 days challenging the opinion. This makes the AG appeal faster, cheaper, and more accessible than court enforcement in most states. There is no filing fee for AG appeals.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'appeal_deadline',
        'param_key': 'ag_opinion_deadline_days',
        'param_value': '20',
        'day_type': 'calendar',
        'statute_citation': 'KRS 61.880(2)',
        'notes': 'The AG must issue a written opinion on an ORA appeal within 20 calendar days of receipt. This fast turnaround makes the AG appeal process highly practical — a requester denied records on Monday can have a binding AG opinion compelling production within three to four weeks without filing a lawsuit. The AG opinion is enforceable against the agency: compliance is mandatory unless the agency challenges the opinion in circuit court within 30 days. The 20-day AG opinion deadline is one of the fastest administrative appeal timelines in the country for public records disputes.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_review',
        'param_value': 'available_within_30_days_of_ag_opinion',
        'day_type': None,
        'statute_citation': 'KRS 61.882',
        'notes': 'A party aggrieved by an AG opinion on an ORA appeal may seek review in the circuit court of the county where the record is located. The circuit court action must be filed within 30 calendar days of the AG opinion. If the agency does not seek circuit court review within 30 days, the AG opinion becomes final and enforceable. The circuit court reviews the AG opinion under the arbitrary and capricious standard for the agency\'s factual determinations, but applies de novo review to legal questions of ORA interpretation. A requester who prevails in court (either enforcing an AG opinion or directly) is entitled to attorney fees.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'KRS 61.882(5)',
        'notes': 'Courts may award attorney fees and other litigation costs to a requester who substantially prevails in an ORA enforcement action in circuit court. The fee award is discretionary but frequently granted when agencies acted without reasonable basis. Attorney fees are not available for AG appeals (no court action), but the ability to recover fees in subsequent circuit court proceedings creates an incentive for agencies to comply with AG opinions rather than challenge them. The combination of the no-cost AG appeal process and potential attorney fee recovery makes Kentucky\'s enforcement framework highly accessible.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'penalty',
        'param_key': 'ag_enforcement_mechanism',
        'param_value': 'binding_opinions',
        'day_type': None,
        'statute_citation': 'KRS 61.880(2)',
        'notes': 'The AG\'s binding opinion mechanism is Kentucky\'s primary enforcement tool and uniquely effective compared to other states. When a requester appeals a denial, the AG investigates, obtains the agency\'s response, and issues a written opinion. If the AG finds the agency acted improperly, the opinion orders the agency to provide access. The agency must comply or file for circuit court review within 30 days. The AG maintains a searchable database of all ORA opinions — thousands of precedents that guide agency behavior. This creates a body of accessible guidance that both requesters and agencies can consult to assess the merits of access disputes without litigation.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'KRS 61.882(3)',
        'notes': 'The burden of proving that any exemption applies rests on the agency claiming it. KRS 61.882(3) provides that in any action to enforce the ORA, the burden is on the agency to justify withholding. The AG enforces this standard in appeal proceedings — agencies that cannot provide specific justification for each withheld record will have the denial overturned. Kentucky AG opinions consistently impose this burden and frequently find agencies have failed to meet it.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'KRS 61.878(4)',
        'notes': 'KRS 61.878(4) explicitly requires agencies to separate and produce non-exempt portions of records when only part of a record qualifies for an exemption. If any portion of a record is exempt, the agency must separate the exempt and non-exempt materials and release the non-exempt portions. Blanket withholding of documents containing some exempt content is an ORA violation. The AG\'s Office enforces this provision actively — agencies that withhold entire documents when only portions are exempt will have the denial overturned on appeal.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'KRS 61.872(1)',
        'notes': 'Any person may inspect public records under Kentucky\'s ORA — there is no citizenship, residency, or identity requirement. KRS 61.872(1) provides a universal right of access. Agencies may not require requesters to identify themselves or state the purpose of their request. Anonymous requests are valid. Contact information for delivery purposes is acceptable but may not be required as a condition of access.',
    },
    {
        'jurisdiction': 'KY',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_access',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'KRS 61.874(2)(a)',
        'notes': 'Kentucky\'s ORA provides that if records exist in electronic form, the requester may request electronic copies. Agencies must provide electronic records in standard electronic format unless the records are only available in a non-standard format. For records transmitted electronically, the agency may charge only the actual cost of the electronic medium or transmission — which is typically zero for email delivery. Kentucky AG opinions have held that agencies must provide records in the format that makes them most accessible to requesters.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

KY_TEMPLATES = [
    {
        'jurisdiction': 'KY',
        'record_type': 'general',
        'template_name': 'General Kentucky Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Official Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Act Request — KRS 61.870 et seq.

Dear Official Custodian of Records:

Pursuant to the Kentucky Open Records Act (ORA), KRS 61.870-61.884, I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. For electronic records, there is no reproduction cost per KRS 61.874(2)(a).

For paper copies, the standard fee under KRS 61.874(3) is $0.10 per page. I am willing to pay up to ${{fee_limit}} in copying fees. If fees will exceed that amount, please notify me before proceeding so I may refine my request.

Under KRS 61.882(3), the burden of demonstrating that any exception applies to requested records rests on {{agency_name}}, not on me. Under KRS 61.878(4), any record containing both exempt and non-exempt portions must be produced with the exempt portions separated and the non-exempt portions made available.

Under KRS 61.880(1), please respond within 5 business days. If the records cannot be produced within 5 business days, please provide written notification of the reason and the anticipated production date.

If any records or portions are denied, KRS 61.880(1) REQUIRES a written denial that: (1) states that the request is denied; (2) cites the specific exception under KRS 61.878 (by subsection letter) relied upon for each withheld record; and (3) briefly explains why the exception applies to those specific records. A denial citing only general categories without identifying the specific subsection of KRS 61.878 is legally insufficient.

Please be advised that any denial may be appealed to the Kentucky Attorney General under KRS 61.880(2), which will issue a binding opinion within 20 calendar days. An AG opinion adverse to the agency is binding unless {{agency_name}} challenges it in circuit court within 30 days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that all fees be waived for this Open Records request. While Kentucky\'s ORA does not mandate fee waivers, the standard $0.10/page fee may be waived at {{agency_name}}\'s discretion. A waiver is appropriate because:

1. These records concern {{public_interest_explanation}}, a matter of significant public accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. To the extent records are available in electronic format and can be delivered by email, the cost is zero per KRS 61.874(2)(a), making a fee waiver for electronic records consistent with the statute.''',
        'expedited_language': '''I request that this ORA request be processed within the mandatory 5-business-day period under KRS 61.880(1). Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if there are questions that would allow faster production. Failure to respond within 5 business days will be treated as a denial subject to AG appeal under KRS 61.880(2).''',
        'notes': 'General Kentucky ORA template. Key features: (1) 5-business-day response deadline (KRS 61.880(1)); (2) written denial with SPECIFIC KRS 61.878 subsection citation required (KRS 61.880(1)); (3) binding AG appeal available within 20 days — no filing fee (KRS 61.880(2)); (4) AG opinion is binding unless agency seeks circuit court review within 30 days; (5) $0.10/page — lowest standard rate in the US (KRS 61.874(3)); (6) attorney fees available for prevailing requester in court (KRS 61.882(5)); (7) burden on agency (KRS 61.882(3)); (8) segregation required (KRS 61.878(4)). The explicit mention of the AG appeal mechanism is important — it signals that the requester knows their rights and will use the highly accessible enforcement mechanism.',
    },
    {
        'jurisdiction': 'KY',
        'record_type': 'law_enforcement',
        'template_name': 'Kentucky Open Records Act Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Official Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Kentucky Open Records Act Request — Law Enforcement Records, KRS 61.870 et seq.

Dear Official Custodian of Records:

Pursuant to the Kentucky Open Records Act, KRS 61.870-61.884, I request the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Internal investigation records for this matter

Regarding claimed exemptions under KRS 61.878(1)(h): This exemption applies ONLY while the investigation is ongoing. Once enforcement action concludes (charges filed, case closed, prosecution complete), investigation records are subject to full ORA disclosure. Kentucky AG opinions have consistently held this. For each withheld record, KRS 61.880(1) requires a written denial citing the specific subsection and explaining how disclosure of that specific record — not records of this general type — would harm the investigation.

Under KRS 61.882(3), the burden of demonstrating that any exception applies rests on {{agency_name}}. Under KRS 61.878(4), non-exempt portions of partially withheld records must be separated and released.

I am willing to pay up to $0.10/page per KRS 61.874(3), up to ${{fee_limit}} total. Electronic delivery preferred and free of charge.

Please respond within 5 business days per KRS 61.880(1). Any denial may be appealed to the Kentucky Attorney General under KRS 61.880(2) for a binding opinion within 20 days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern {{public_interest_explanation}}, a core public accountability matter. Kentucky\'s $0.10/page rate is already very low. Electronic delivery is available at no cost per KRS 61.874(2)(a). A fee waiver is appropriate given the significant public interest in law enforcement accountability.''',
        'expedited_language': '''I request processing within the 5-business-day deadline under KRS 61.880(1). These law enforcement records are urgently needed because: {{expedited_justification}}. I need them by {{needed_by_date}}. Please contact me immediately with any questions. Failure to respond within 5 days will be treated as a denial subject to AG appeal under KRS 61.880(2).''',
        'notes': 'Kentucky law enforcement records template. Key points: (1) KRS 61.878(1)(h) investigation exemption terminates when enforcement action concludes — extensive Kentucky AG opinions confirm this; (2) mandatory written denial with specific KRS 61.878(1)(h) citation required; (3) binding AG appeal under KRS 61.880(2) — 20-day opinion, no filing fee, binding on agency; (4) $0.10/page — lowest standard rate in US; (5) burden on agency under KRS 61.882(3). The availability of the AG appeal without court costs makes Kentucky one of the most accessible states for challenging law enforcement records denials.',
    },
    {
        'jurisdiction': 'KY',
        'record_type': 'government_contracts',
        'template_name': 'Kentucky Open Records Act Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Official Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Kentucky Open Records Act Request — Government Contracts and Expenditure Records

Dear Official Custodian of Records:

Pursuant to the Kentucky Open Records Act, KRS 61.870-61.884, I request the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments between {{agency_name}} and {{contractor_vendor_name}} from {{date_range_start}} through {{date_range_end}}
- Invoices, purchase orders, and payment records for these contracts
- Correspondence relating to contract negotiation and performance
- Post-award bid evaluation records and scoring sheets (public after contract award per KRS 61.878(1)(i))
- Any performance evaluations or audits of the contractor's work

Regarding post-award records: KRS 61.878(1)(i) protects preliminary recommendations and memoranda relating to contract awards only until final action is taken. Once the contract is awarded, all evaluation records including bid scoring, recommendations, and related documentation become subject to full ORA disclosure. Kentucky AG opinions consistently enforce this rule.

Any vendor trade secret or confidentiality claims regarding amounts paid with public funds should be rejected — public expenditure data is not within the scope of any ORA exemption. The burden of establishing any exemption rests on {{agency_name}} under KRS 61.882(3).

I am willing to pay $0.10/page per KRS 61.874(3), up to ${{fee_limit}}. Electronic delivery preferred and free of charge.

Please respond within 5 business days per KRS 61.880(1). Any denial may be appealed to the Kentucky Attorney General under KRS 61.880(2) for a binding opinion within 20 days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for these government contracts records. At Kentucky\'s $0.10/page rate, fees are already minimal. Electronic delivery is available at no cost. These records concern the expenditure of public funds — a core accountability matter. A fee waiver is consistent with the ORA\'s purpose.''',
        'expedited_language': '''I request processing within the 5-business-day deadline under KRS 61.880(1). These government spending records are needed promptly for {{expedited_justification}}. Please contact me with any questions. Any denial will be appealed to the AG under KRS 61.880(2).''',
        'notes': 'Kentucky government contracts template. Key points: (1) KRS 61.878(1)(i) pre-award exemption terminates upon contract award — post-award evaluation records are fully public; (2) Kentucky AG opinions consistently enforce this rule for procurement records; (3) amounts paid with public funds are public regardless of vendor confidentiality claims; (4) $0.10/page copy fee is the lowest standard rate in the US; (5) binding AG appeal available within 20 days if denied — no filing fee. Kentucky\'s combination of low fees, binding AG review, and strong post-award disclosure requirements makes it an excellent jurisdiction for government contracting transparency.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in KY_EXEMPTIONS:
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

    print(f'KY exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in KY_RULES:
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

    print(f'KY rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in KY_TEMPLATES:
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

    print(f'KY templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'KY total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ky', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
