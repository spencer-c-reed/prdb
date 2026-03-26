#!/usr/bin/env python3
"""Build New Hampshire Right-to-Know Law data: exemptions, rules, and templates.

Covers New Hampshire's Right-to-Know Law, RSA 91-A.
New Hampshire has a 5-business-day response deadline, no administrative appeal,
and enforcement in superior court. $0.25/page copy fee. Attorney's fees for
prevailing requesters. RSA 91-A is notable for its strong open meetings provisions
(covered alongside records access in the same statute) and a broad definition of
"public body" that covers advisory committees and other entities often excluded
elsewhere. New Hampshire courts have been active in developing and enforcing
the Right-to-Know Law.

Run: python3 scripts/build/build_nh.py
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
# RSA 91-A:5 lists the categories of records exempt from the Right-to-Know Law.
# The New Hampshire Supreme Court has consistently construed exemptions narrowly
# against agencies. RSA 91-A:4 establishes the general right of access; RSA 91-A:5
# provides the specific exemptions. The burden of demonstrating an exemption is
# on the public body. Courts apply de novo review of withholding decisions.
# =============================================================================

NH_EXEMPTIONS = [
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, I',
        'exemption_number': 'RSA 91-A:5, I',
        'short_name': 'Personnel Records — Private Information',
        'category': 'privacy',
        'description': 'Personnel records, medical records, and similar files, the disclosure of which would constitute an invasion of privacy, are exempt from the New Hampshire Right-to-Know Law.',
        'scope': 'Personnel files containing private employee information: medical records, Social Security numbers, home addresses, personal financial data, and similar information whose disclosure would constitute a privacy invasion. However, basic employment and compensation data is public. The New Hampshire Supreme Court applies a balancing test: the privacy interest must be weighed against the public interest in accountability. Public employees have a reduced privacy expectation regarding their official conduct. Disciplinary records resulting in termination or significant formal action are generally public. Separation agreements and payments with public funds are public.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'privacy', 'medical records',
            'public employee', 'salary', 'disciplinary records', 'performance evaluation',
            'invasion of privacy', 'HR records',
        ]),
        'counter_arguments': json.dumps([
            'New Hampshire courts apply a balancing test — privacy interest must outweigh the public accountability interest',
            'Public employee salaries, job titles, and work-related conduct are public',
            'Formal disciplinary records resulting in suspension, demotion, or termination are generally public',
            'Separation agreements and severance payments are public as expenditures of public funds',
            'Law enforcement officer misconduct records warrant heightened disclosure under accountability principles',
            'Challenge overbroad privacy claims that redact basic employment information',
            'Settlement agreements resolving employee complaints are public',
        ]),
        'notes': 'The New Hampshire Supreme Court has applied a balancing approach to Right-to-Know Law privacy claims. See Union Leader Corp. v. City of Nashua, 141 N.H. 473 (1996). Public employee information relating to official conduct has a reduced privacy expectation. The Court has held that the Right-to-Know Law\'s purpose of promoting accountability requires narrow construction of privacy exemptions for public officials.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, II',
        'exemption_number': 'RSA 91-A:5, II',
        'short_name': 'Library Patron Records',
        'category': 'privacy',
        'description': 'Library patron records identifying what specific library users have requested, borrowed, or accessed are exempt from the Right-to-Know Law to protect intellectual privacy.',
        'scope': 'Library circulation records, database access logs, borrower records, and similar records that identify what specific library users have borrowed, accessed, or requested — whether in physical or digital form. The exemption protects the identity-to-reading-material link. Aggregate library statistics, collection data, and library administrative records are public. The exemption reflects the constitutional principle that individuals must be free to access information without government surveillance.',
        'key_terms': json.dumps([
            'library patron records', 'circulation records', 'library user',
            'borrower records', 'reading privacy', 'intellectual privacy',
            'library records', 'database access', 'library access',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library circulation statistics are public',
            'Library administrative records, budgets, and contracts are public',
            'Records subpoenaed for a criminal investigation may be disclosed pursuant to court order',
            'The exemption covers what patrons read — not library operations, programs, or staffing',
        ]),
        'notes': 'New Hampshire\'s library patron record exemption reflects the intellectual privacy principle. RSA 201-D:11 provides an additional specific protection for library circulation records under New Hampshire library law. The exemption is absolute for patron-specific data with no balancing test.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, III',
        'exemption_number': 'RSA 91-A:5, III',
        'short_name': 'Records Made Confidential by Other Statutes',
        'category': 'statutory',
        'description': 'Records that are specifically designated as confidential by other New Hampshire statutes or by federal law are exempt from disclosure under the Right-to-Know Law.',
        'scope': 'Records specifically covered by other confidentiality statutes — for example, tax return information (RSA 21-J:14), juvenile court records, FERPA-protected student records, HIPAA-protected medical records, and similar statutory confidentiality provisions. The exemption requires a specific applicable statute — not a general sensitivity claim. The cited statute must specifically cover the records at issue. Agencies must produce records that fall outside the scope of the referenced statute.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'FERPA', 'HIPAA', 'tax information',
            'confidential by statute', 'RSA 21-J:14', 'cross-reference exemption',
            'juvenile records', 'statutory protection',
        ]),
        'counter_arguments': json.dumps([
            'The cited statute must specifically cover the records at issue — general subject-matter overlap is insufficient',
            'Challenge whether the agency has correctly identified the applicable statute',
            'Some statutes create confidentiality only in specific contexts — verify the statute applies here',
            'Aggregate and anonymized data may fall outside the scope of the underlying confidentiality statute',
            'The agency must produce all records not specifically covered by the cited provision',
        ]),
        'notes': 'New Hampshire courts require agencies to identify a specific statute creating confidentiality. General assertions of sensitivity are insufficient. The Right-to-Know Law\'s narrow construction requirement applies to this exemption as to all others.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, IV',
        'exemption_number': 'RSA 91-A:5, IV',
        'short_name': 'Internal Confidential Business Information — Agency Proprietary',
        'category': 'commercial',
        'description': 'Confidential, commercial, or financial information submitted to an agency by private parties under an express or implied expectation of confidentiality is exempt from disclosure.',
        'scope': 'Commercially sensitive information submitted to government agencies by private entities: trade secrets, proprietary financial data, and confidential business information where disclosure would cause genuine competitive harm. The government\'s own financial records are not commercial information. Amounts paid under government contracts are public. The agency must independently evaluate commercial information claims — submitter designations do not control. New Hampshire courts apply the narrow construction principle to commercial information claims.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'confidential business',
            'contract pricing', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Government expenditure amounts are public regardless of vendor confidentiality claims',
            'Publicly available information cannot be withheld as confidential',
            'Information required by law to be submitted has reduced confidentiality expectations',
            'The submitter must demonstrate actual competitive harm',
            'Challenge overbroad designations where entire contracts are marked confidential',
            'Government-generated analysis of submitted data is not itself exempt',
        ]),
        'notes': 'New Hampshire courts apply a narrow construction to commercial information exemption claims. The New Hampshire Supreme Court has emphasized that the Right-to-Know Law\'s purpose of governmental accountability requires that exemptions not become shields for contractors avoiding scrutiny of public expenditures.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, V',
        'exemption_number': 'RSA 91-A:5, V',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or attorney work-product doctrine are exempt from disclosure under the New Hampshire Right-to-Know Law.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. Standard privilege elements apply: lawyer-client relationship, confidential communication, for legal advice. Policy and business advice from lawyers is not covered. Waiver through public disclosure eliminates the protection. New Hampshire courts apply the privilege narrowly given the Right-to-Know Law\'s strong disclosure mandate.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or business guidance',
            'Attorney billing records are generally public',
            'Waiver occurs when the agency publicly relies on or discloses legal advice',
            'Settlement agreements and consent orders are public once executed',
            'Facts communicated to an attorney are not privileged',
            'Challenge broad claims that all attorney correspondence is privileged',
        ]),
        'notes': 'New Hampshire courts apply the attorney-client privilege to government entities under standard evidentiary rules. The Right-to-Know Law\'s strong disclosure mandate narrows the privilege\'s practical reach. See Seacoast Newspapers v. City of Portsmouth, 148 N.H. 214 (2002) for the New Hampshire Supreme Court\'s approach to Right-to-Know Law exemptions.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, VI',
        'exemption_number': 'RSA 91-A:5, VI',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, and memoranda not in their final form, including preliminary drafts of proposed legislation, reports, or agency positions, are exempt under the Right-to-Know Law.',
        'scope': 'Predecisional working documents — drafts, notes, working papers, and internal memoranda — that contain opinions on policy or legal questions and have not been adopted as the agency\'s final position. The exemption does NOT cover: (1) purely factual material; (2) adopted final positions; (3) "working law"; (4) documents shared outside the agency. Factual portions of deliberative documents must be segregated and released. The New Hampshire Supreme Court has applied this exemption narrowly.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional',
            'working paper', 'intra-agency memo', 'draft document',
            'not final', 'internal document', 'policy deliberation',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative documents must be segregated and released',
            'Documents adopted as final positions are no longer covered',
            '"Working law" — standards the agency applies in practice — must be disclosed',
            'Challenge claims that entire documents are exempt when only recommendation portions qualify',
            'External communications are not "preliminary drafts"',
            'The agency must demonstrate that specific documents are genuinely predecisional and opinionated',
        ]),
        'notes': 'The New Hampshire Supreme Court applies the deliberative process exemption narrowly. The Court has emphasized that factual data does not become deliberative simply because it appears in a policy document. See Hawkins v. New Hampshire Department of Health, 147 N.H. 376 (2001) for the New Hampshire approach to deliberative process claims.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, VII',
        'exemption_number': 'RSA 91-A:5, VII',
        'short_name': 'Medical Records — Individual Privacy',
        'category': 'privacy',
        'description': 'Medical records of identifiable individuals held by government agencies are exempt from the Right-to-Know Law to protect individual medical privacy.',
        'scope': 'Medical, health, and psychiatric records of identifiable individuals held by government agencies. The exemption is individual-protective — it does not cover agency operational records, contracts with healthcare providers, or aggregate health statistics. HIPAA-protected categories align with this exemption. The New Hampshire Supreme Court has held that the individual privacy interest in medical records is among the strongest recognized under the Right-to-Know Law.',
        'key_terms': json.dumps([
            'medical records', 'health records', 'psychiatric records',
            'medical privacy', 'HIPAA', 'patient records', 'health information',
            'protected health information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Agency contracts with healthcare providers and expenditure data are public',
            'Policies about public health programs are public',
            'Challenge overbroad redactions that remove non-medical contextual information',
        ]),
        'notes': 'Individual medical record privacy is one of the most clearly established exemptions under New Hampshire\'s Right-to-Know Law. The exemption applies to identifiable individual records, not to aggregate data or agency healthcare operations.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, VIII',
        'exemption_number': 'RSA 91-A:5, VIII',
        'short_name': 'Security Plans — Public Facilities',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and similar documents for public facilities and critical infrastructure are exempt where disclosure would create a specific security risk.',
        'scope': 'Specific operational security documents for government buildings, water systems, power infrastructure, transportation networks, and emergency response systems. The exemption requires a specific, demonstrable security harm from disclosure — not merely that records relate to security. Budget records for security programs, general policy descriptions, and vendor contracts (excluding specific vulnerability data) are public. New Hampshire courts apply the narrow construction rule.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'facility security', 'emergency response',
            'infrastructure protection', 'public safety', 'security assessment',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable',
            'Budget and expenditure records for security programs are public',
            'General security policy descriptions are public',
            'Challenge claims that entire security contracts are exempt',
            'Historical security plans for completed projects may not create current risks',
        ]),
        'notes': 'New Hampshire courts apply the narrow construction rule to security exemption claims. Agencies must demonstrate a specific, articulable harm from disclosure — not merely that records involve security topics. The Right-to-Know Law\'s presumption of openness applies.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, IX',
        'exemption_number': 'RSA 91-A:5, IX',
        'short_name': 'Law Enforcement Records — Ongoing Investigations',
        'category': 'law_enforcement',
        'description': 'Law enforcement investigation records where disclosure would interfere with an ongoing investigation, endanger persons, or identify confidential informants are exempt from the Right-to-Know Law.',
        'scope': 'Active law enforcement investigation records where disclosure would specifically: (1) interfere with pending investigation or prosecution; (2) endanger the safety of any person; (3) identify a confidential informant; or (4) deprive a person of a fair trial. Completed investigation files are public once prosecution concludes. Arrest records, booking information, and incident reports documenting the basic facts of events are generally public. The New Hampshire Supreme Court requires record-specific justification for withholding.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'ongoing investigation',
            'confidential informant', 'endanger', 'pending prosecution',
            'active investigation', 'investigation records',
        ]),
        'counter_arguments': json.dumps([
            'Completed investigations do not retain this protection',
            'Arrest records and booking information are public regardless of investigation status',
            'The agency must identify a specific harm per withheld record',
            'Factual information not revealing informants or investigative techniques must be released',
            'Challenge withholding that extends beyond any plausible active investigation period',
            'New Hampshire courts apply a narrow construction to law enforcement exemptions',
        ]),
        'notes': 'The New Hampshire Supreme Court has consistently required specific harm justifications for law enforcement exemption claims. Completed investigation files are public. The narrow construction principle under RSA 91-A applies with full force. See Goode v. New Hampshire Office of Legislative Budget Assistant, 148 N.H. 551 (2002) for the general framework.',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:3, II',
        'exemption_number': 'RSA 91-A:3, II (Nonpublic Session)',
        'short_name': 'Open Meetings — Nonpublic Session Grounds',
        'category': 'deliberative',
        'description': 'New Hampshire\'s Right-to-Know Law governs both records and open meetings. RSA 91-A:3, II lists the specific grounds on which a public body may meet in nonpublic session. Records of those sessions may be sealed under specified conditions.',
        'scope': 'Public bodies may enter nonpublic session for: (a) personnel matters with privacy implications; (b) acquisition of real property if disclosure would affect price; (c) legal matters where consultation with counsel is necessary; (d) discussions of matters that if disclosed would adversely affect ongoing negotiations; (e) consideration of allegations of misconduct against an official. Records of nonpublic sessions may be sealed if the public interest requires it, but must be unsealed when the reason for sealing no longer applies. The unsealing obligation is an important enforcement tool — sealed records are not permanently secret.',
        'key_terms': json.dumps([
            'nonpublic session', 'executive session', 'closed meeting',
            'open meetings', 'RSA 91-A:3', 'sealed minutes', 'nonpublic records',
            'personnel matters', 'legal consultation', 'real property acquisition',
        ]),
        'counter_arguments': json.dumps([
            'Nonpublic session grounds are limited — meetings may not be closed for reasons not listed in RSA 91-A:3, II',
            'Records of nonpublic sessions must be unsealed when the reason for sealing no longer applies',
            'A vote to enter nonpublic session must be recorded in the public minutes',
            'The final action of the public body, even on matters discussed in nonpublic session, must be taken in public session',
            'Improper nonpublic sessions can be challenged as Right-to-Know Law violations',
            'Sealed minutes of nonpublic sessions may be requested and disclosed once the sealing reason expires',
        ]),
        'notes': 'New Hampshire\'s Right-to-Know Law uniquely integrates open meetings and records access in the same statute. RSA 91-A:3 governs when meetings may be closed. The requirement that sealed session records be unsealed when the reason expires is a significant accountability mechanism. The New Hampshire Supreme Court has actively enforced the open meetings provisions. See Akins v. Town of Enfield, 136 N.H. 158 (1992).',
    },
    {
        'jurisdiction': 'NH',
        'statute_citation': 'RSA 91-A:5, X',
        'exemption_number': 'RSA 91-A:5, X',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals and related records for proposed property acquisitions by public bodies are exempt prior to completion of the transaction.',
        'scope': 'Formal real property appraisals, feasibility studies, and related valuation documents prepared for a government body\'s proposed acquisition or sale of real estate. The exemption is temporary — it expires upon completion, cancellation, or abandonment of the transaction. Post-transaction, all appraisal records are public. The exemption protects the government\'s negotiating position, not a permanent secrecy interest.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property sale',
            'pre-acquisition', 'property valuation', 'real property',
            'condemnation', 'eminent domain', 'land purchase',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction completes, is cancelled, or is abandoned',
            'Challenge claims that transactions remain "pending" with no recent activity',
            'Post-transaction appraisals are uniformly public',
            'After condemnation judgment, all valuation records are public',
        ]),
        'notes': 'New Hampshire\'s pre-acquisition appraisal exemption is time-limited. It protects the government\'s negotiating position, not a permanent secrecy interest. Courts have not allowed agencies to claim indefinitely pending transactions to shield completed appraisal records.',
    },
]

# =============================================================================
# RULES
# New Hampshire Right-to-Know Law, RSA 91-A.
# 5 business days to respond. No administrative appeal. Superior court
# enforcement. $0.25/page. Attorney's fees for prevailing requesters. Strong
# open meetings provisions in the same statute (RSA 91-A:2, 91-A:3). Broad
# definition of "public body" covering advisory committees.
# =============================================================================

NH_RULES = [
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'RSA 91-A:4, IV',
        'notes': 'New Hampshire public bodies must respond to Right-to-Know Law requests within 5 business days of receipt. Within those 5 business days, the public body must either: (1) provide the requested records; (2) inform the requester that additional time is needed and provide a specific date for production; or (3) deny the request with a written explanation of the legal basis. The 5-day clock begins on the date the written request is received. A substantive response is required — a bare acknowledgment without a production timeline or denial with legal basis does not satisfy the requirement.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'extension_available',
        'param_value': 'yes_with_specific_date',
        'day_type': 'business',
        'statute_citation': 'RSA 91-A:4, IV',
        'notes': 'If a public body cannot produce records within 5 business days, it must notify the requester that additional time is needed and provide a specific date by which records will be produced. The extension must specify a definite response date — open-ended notices are insufficient. New Hampshire courts have found that indefinite extensions constitute constructive denials. Extensions should reflect genuine need, not agency delay strategy.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'RSA 91-A:4, IV',
        'notes': 'New Hampshire agencies may charge a reasonable fee for copies under the Right-to-Know Law. The standard rate for paper copies is $0.25 per page. For electronic records, the charge should reflect the actual cost of production — often zero for email delivery. Agencies may not charge for staff time spent searching, reviewing, or redacting records. Fees must be reasonable and must not function as a barrier to access. Some agencies have adopted specific fee schedules.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'fee_cap',
        'param_key': 'search_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'RSA 91-A:4, IV',
        'notes': 'New Hampshire\'s Right-to-Know Law does not authorize agencies to charge for staff time spent searching for, reviewing, or redacting records. Only actual reproduction costs are permissible. Agencies that add "research fees," "processing fees," or "staff time" charges are imposing costs beyond what the statute permits. Requesters should challenge such charges.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'RSA 91-A:4, IV',
        'notes': 'New Hampshire\'s Right-to-Know Law does not mandate fee waivers for specific requester categories. Agencies may waive fees at their discretion. Requesters seeking waivers should articulate the public interest served by the disclosure. For electronic records delivered by email, the actual cost is zero, making fee waivers less critical for electronic requests.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'RSA 91-A:7',
        'notes': 'New Hampshire\'s Right-to-Know Law has NO formal administrative appeal mechanism. There is no agency head review, state ombudsman, or administrative tribunal. A requester denied access — or whose request receives no response — must go directly to superior court under RSA 91-A:7. The Right-to-Know Law Ombudsman created by RSA 91-A:11 (effective 2020) provides an optional, non-binding mediation alternative to litigation, but use of the Ombudsman process is voluntary and does not toll any litigation deadlines.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'ombudsman_available',
        'param_value': 'voluntary_non_binding',
        'day_type': None,
        'statute_citation': 'RSA 91-A:11',
        'notes': 'New Hampshire created a Right-to-Know Law Ombudsman (RSA 91-A:11, effective 2020) to provide an alternative to litigation for resolving disputes. The Ombudsman may investigate complaints and issue findings, but the Ombudsman\'s decisions are advisory, not binding. Use of the Ombudsman process is voluntary — agencies may ignore findings, in which case judicial enforcement remains necessary. The Ombudsman process does not toll any litigation deadlines. It may be useful for straightforward disputes where the agency has made a clear error.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'RSA 91-A:7',
        'notes': 'A requester denied access (including by constructive denial through non-response) may file a petition in superior court under RSA 91-A:7. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may issue injunctive relief requiring production. New Hampshire superior courts have been active in enforcing the Right-to-Know Law. There is no explicit statute of limitations, but prompt filing is advisable. Cases may be filed in the superior court of the county where the public body is located.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'RSA 91-A:8',
        'notes': 'Courts may award attorney fees, costs, and civil forfeiture to a requester who substantially prevails under RSA 91-A:8. The award includes attorney fees and may include a civil forfeiture of up to $500 per violation. New Hampshire courts have been willing to award fees when agencies improperly withheld records. The fee-shifting and forfeiture provisions make judicial enforcement economically viable. The $500 civil forfeiture is per violation — multiple withholdings can aggregate to significant amounts.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'penalty',
        'param_key': 'civil_forfeiture_per_violation',
        'param_value': '$500_per_violation',
        'day_type': None,
        'statute_citation': 'RSA 91-A:8',
        'notes': 'RSA 91-A:8 authorizes a civil forfeiture of up to $500 per Right-to-Know Law violation, in addition to attorney fees and costs. The forfeiture is discretionary — courts award it for willful or egregious violations. Multiple improper withholdings can result in multiple forfeitures. This is a meaningful deterrent and enforcement tool. The forfeiture provision is distinct from attorney fees and supplements the fee-shifting remedy.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'open_meetings_same_statute',
        'param_value': 'RSA_91-A:2_through_91-A:3',
        'day_type': None,
        'statute_citation': 'RSA 91-A:2; RSA 91-A:3',
        'notes': 'New Hampshire\'s Right-to-Know Law uniquely covers both records access (RSA 91-A:4 et seq.) and open meetings (RSA 91-A:2 et seq.) in the same statute. Public bodies must meet in public under RSA 91-A:2 except as specifically permitted by RSA 91-A:3. The integration of meetings and records law means that violations of open meetings requirements may also implicate records access obligations — minutes, votes, and actions taken in improperly closed sessions may be challengeable.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'RSA 91-A:4',
        'notes': 'New Hampshire\'s Right-to-Know Law does not require requesters to identify themselves or explain their purpose. The right of access is available to any person without conditions of identity or purpose. Agencies may not condition access on requester identity or stated use. Contact information for delivery purposes may be requested but must be voluntary.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'RSA 91-A:5',
        'notes': 'When a record contains both exempt and non-exempt information, New Hampshire public bodies must redact the exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is improper. The public body must identify what has been withheld and the statutory basis for each withholding. New Hampshire courts have enforced the segregability requirement and have found violations when agencies withheld entire documents where only portions qualified for exemption.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'RSA 91-A:4; RSA 91-A:7',
        'notes': 'New Hampshire courts place the burden of demonstrating any Right-to-Know Law exemption on the public body. The presumption favors disclosure. In judicial proceedings, the public body must affirmatively establish that each claimed exemption applies to each specific withheld record. The New Hampshire Supreme Court reviews withholding decisions de novo and has consistently required agencies to meet their burden with specificity. General assertions of exemption categories without record-specific justification have been rejected.',
    },
    {
        'jurisdiction': 'NH',
        'rule_type': 'initial_response',
        'param_key': 'broad_public_body_definition',
        'param_value': 'includes_advisory_committees',
        'day_type': None,
        'statute_citation': 'RSA 91-A:1-a',
        'notes': 'New Hampshire\'s Right-to-Know Law applies to a broad range of "public bodies" including advisory committees, task forces, and similar bodies created by government authority, not just formal governmental agencies. RSA 91-A:1-a defines "public body" broadly to include any legislative, executive, or quasi-judicial body of the state or political subdivision, as well as multi-member bodies created by law or executive order. This broad definition means that many entities not formally considered government agencies are still subject to Right-to-Know Law obligations.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NH_TEMPLATES = [
    {
        'jurisdiction': 'NH',
        'record_type': 'general',
        'template_name': 'General New Hampshire Right-to-Know Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Right-to-Know Law Officer / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — RSA 91-A

Dear Records Custodian:

Pursuant to New Hampshire's Right-to-Know Law, RSA 91-A, I hereby request access to and copies of the following governmental records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format where available.

Regarding fees: I am willing to pay reasonable reproduction costs up to ${{fee_limit}}. Under RSA 91-A:4, IV, fees should reflect only the actual cost of reproduction — staff time spent searching, reviewing, or redacting records is not a chargeable cost. If costs will exceed ${{fee_limit}}, please notify me before proceeding.

Under RSA 91-A:4, I, all governmental records are presumptively open for public inspection. The burden of demonstrating any exemption rests on the public body. Under RSA 91-A:5, all nonexempt, reasonably segregable portions of any record must be released.

If any records or portions are withheld, please: (1) identify each withheld record; (2) cite the specific exemption under RSA 91-A:5 or other applicable provision; (3) explain how the exemption applies to each specific withheld record; (4) confirm that all nonexempt, segregable portions have been released.

Under RSA 91-A:4, IV, please respond within 5 business days of receipt of this request. If additional time is needed, please provide written notice within 5 business days specifying a definite date for production. An open-ended extension notice does not comply with RSA 91-A:4, IV.

If this request is denied, I will seek judicial enforcement under RSA 91-A:7 and request attorney fees and civil forfeiture under RSA 91-A:8.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While the Right-to-Know Law does not mandate a fee waiver, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records concern {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. For records provided electronically, the reproduction cost is zero.

A fee waiver is consistent with the Right-to-Know Law\'s purpose of promoting open access to governmental records.''',
        'expedited_language': '''I request expedited processing of this Right-to-Know Law request. The 5-business-day deadline under RSA 91-A:4, IV applies. Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if any clarification would allow faster processing.''',
        'notes': 'General-purpose New Hampshire Right-to-Know Law template. Key NH features: (1) 5 business days to respond per RSA 91-A:4, IV; (2) no administrative appeal — superior court under RSA 91-A:7 is the sole formal remedy (Ombudsman under RSA 91-A:11 is voluntary/non-binding); (3) attorney fees AND $500/violation civil forfeiture available under RSA 91-A:8; (4) $0.25/page — no staff time charges; (5) strong open meetings provisions integrated in same statute (RSA 91-A:2, 91-A:3); (6) broad "public body" definition covers advisory committees; (7) burden of proof on agency. Reference "Right-to-Know Law" and RSA 91-A, not "FOIA" or "IPRA."',
    },
    {
        'jurisdiction': 'NH',
        'record_type': 'law_enforcement',
        'template_name': 'New Hampshire Right-to-Know Law Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Right-to-Know Law Officer / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — Law Enforcement Records, RSA 91-A

Dear Records Custodian:

Pursuant to New Hampshire's Right-to-Know Law, RSA 91-A, I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary and complaint records
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Written communications relating to the above

Regarding any claimed exemption under RSA 91-A:5, IX: New Hampshire law requires a specific showing that disclosure of each identified record would: (1) interfere with a pending investigation or prosecution; (2) endanger a specific person; (3) identify a confidential informant; or (4) deprive a person of a fair trial. A generic assertion that records are "investigative" does not satisfy this standard. The agency must apply a record-by-record analysis.

[If matter appears concluded:] If no prosecution is pending and the investigation is closed, the RSA 91-A:5, IX exemption does not apply. Completed investigation records are public and must be produced.

Under RSA 91-A:4, I, all governmental records are presumptively open. Under RSA 91-A:5, nonexempt, segregable portions must be released. The burden of establishing exemptions is on the public body.

Reproduction costs up to ${{fee_limit}} at the standard rate are acceptable. Electronic delivery preferred.

Please respond within 5 business days per RSA 91-A:4, IV.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for law enforcement conduct. Electronic delivery incurs no reproduction cost. A fee waiver is appropriate given the public interest.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. The 5-business-day deadline under RSA 91-A:4, IV applies.''',
        'notes': 'New Hampshire law enforcement Right-to-Know Law template. Key NH features: (1) RSA 91-A:5, IX requires specific harm per record for active investigations only; (2) completed investigations are public; (3) 5 business days to respond; (4) no administrative appeal — superior court under RSA 91-A:7; (5) attorney fees AND $500/violation civil forfeiture under RSA 91-A:8; (6) New Hampshire Supreme Court has consistently enforced the Right-to-Know Law vigorously; (7) open meetings provisions in RSA 91-A:2-3 may also be relevant if seeking meeting records about law enforcement policy.',
    },
    {
        'jurisdiction': 'NH',
        'record_type': 'open_meetings',
        'template_name': 'New Hampshire Right-to-Know Law Request — Meeting Records and Minutes',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Right-to-Know Law Officer / Records Custodian
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — Meeting Records and Minutes, RSA 91-A

Dear Records Custodian:

Pursuant to New Hampshire's Right-to-Know Law, RSA 91-A, I request copies of the following records relating to public body meetings:

{{description_of_records}}

Specifically, for meetings of {{body_name}} occurring between {{date_range_start}} and {{date_range_end}}, I request:
- Agendas for all public meetings
- Minutes of all public sessions, whether approved or unapproved
- Any attachments, exhibits, or documents distributed at or incorporated into the meeting record
- Records of votes taken at each meeting
- Notice documents for each meeting
- Any nonpublic session minutes that have been unsealed or for which the reason for sealing has expired

Regarding nonpublic session records: under RSA 91-A:3, IV, minutes of nonpublic sessions must be unsealed when the reason for sealing no longer applies. I request production of any nonpublic session minutes from the requested period for which the sealing purpose has expired. If any nonpublic session minutes remain sealed, please identify the session date, the ground for continued sealing under RSA 91-A:3, II, and whether that ground remains applicable.

Under RSA 91-A:4, I, all governmental records are presumptively open. The burden of establishing any exemption is on the public body. Under RSA 91-A:5, nonexempt, segregable portions must be released.

Reproduction costs up to ${{fee_limit}} are acceptable. Electronic delivery preferred.

Please respond within 5 business days per RSA 91-A:4, IV.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. Public body meeting records — minutes, agendas, and votes — are core democratic accountability documents. Electronic delivery incurs no cost. A fee waiver is appropriate and consistent with the Right-to-Know Law\'s purpose.''',
        'expedited_language': '''I request prompt processing. These meeting records are needed by {{needed_by_date}} because {{urgency_explanation}}. The 5-business-day deadline under RSA 91-A:4, IV applies.''',
        'notes': 'New Hampshire meeting records Right-to-Know Law template. This template is unique because RSA 91-A integrates open meetings and records access in the same statute. Key features: (1) RSA 91-A:2 requires public bodies to meet in public; (2) RSA 91-A:3 limits nonpublic sessions to specific enumerated grounds; (3) nonpublic session minutes must be unsealed when the sealing purpose expires (RSA 91-A:3, IV) — this is an important enforcement tool; (4) vote records from nonpublic sessions (though not the deliberations) must be made public within 72 hours under RSA 91-A:3, III; (5) RSA 91-A:8 civil forfeiture applies to open meetings violations as well as records violations; (6) 5-business-day response deadline; (7) no administrative appeal.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in NH_EXEMPTIONS:
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

    print(f'NH exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in NH_RULES:
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

    print(f'NH rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in NH_TEMPLATES:
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

    print(f'NH templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'NH total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nh', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
