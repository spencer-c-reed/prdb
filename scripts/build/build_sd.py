#!/usr/bin/env python3
"""Build South Dakota Open Records Law data: exemptions, rules, and templates.

Covers South Dakota's Open Records Law, SDCL § 1-27-1 et seq.
South Dakota has one of the weakest public records laws in the United States.
There is no specific response deadline — agencies must allow access only "at
reasonable hours." There is no administrative appeal, no attorney's fees provision,
no civil penalties, and no per diem penalty mechanism. The only enforcement mechanism
is a mandamus action in Circuit Court, which is expensive and time-consuming. The
statute provides a right to inspect and copy but imposes minimal obligations on agencies.

Run: python3 scripts/build/build_sd.py
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
# South Dakota's Open Records Law at SDCL § 1-27-1 creates a public right to
# inspect and copy "public records." Exemptions are scattered throughout the
# South Dakota Codified Laws and are numerous. SDCL § 1-27-1.5 provides the
# general framework, and dozens of additional statutes create specific exemptions.
# South Dakota courts have been relatively permissive in upholding agency
# withholding decisions, and the weak enforcement mechanism means agencies
# face little practical risk for non-compliance.
# =============================================================================

SD_EXEMPTIONS = [
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(1)',
        'exemption_number': '§ 1-27-1.5(1)',
        'short_name': 'Privacy — Clearly Unwarranted Invasion of Personal Privacy',
        'category': 'privacy',
        'description': 'Records containing information that would constitute a clearly unwarranted invasion of personal privacy if disclosed are exempt from South Dakota\'s Open Records Law. The exemption requires balancing the individual\'s privacy interest against the public\'s interest in disclosure.',
        'scope': 'Personally identifiable information whose disclosure would constitute a clearly unwarranted invasion of personal privacy. South Dakota applies a balancing test, though courts have generally been more deferential to agency withholding decisions than in states with stronger access laws. Information about public officials conducting government business, compensation of public employees, and government operations generally does not qualify for the privacy exemption. Social Security numbers, home addresses of private individuals, medical records, and similar highly personal data are the core of this exemption. The weak enforcement mechanism in South Dakota means agencies sometimes invoke this exemption more broadly than would be justified under the statute.',
        'key_terms': json.dumps([
            'personal privacy', 'clearly unwarranted', 'privacy invasion',
            'personally identifiable information', 'privacy interest', 'public interest',
            'balancing test', 'individual privacy', 'private information',
        ]),
        'counter_arguments': json.dumps([
            'The invasion must be "clearly unwarranted" — a high threshold that requires specific justification',
            'Public employees\' compensation, official conduct, and performance of government duties are not protected',
            'Information about how government money is spent, contracts awarded, and official decisions made is presumptively public',
            'South Dakota courts have held that the privacy exemption applies to genuinely private personal information, not to official conduct',
            'Challenge overbroad privacy claims where the agency has redacted non-private contextual information along with genuinely personal data',
            'The agency must demonstrate both that a privacy interest exists and that disclosure would be "clearly unwarranted" — not merely inconvenient or embarrassing',
        ]),
        'notes': 'SDCL § 1-27-1.5(1) is South Dakota\'s general privacy exemption. South Dakota courts have been relatively deferential to agency withholding decisions given the weak enforcement mechanism — a requester\'s only recourse is a mandamus action in Circuit Court with no attorney\'s fees available if they prevail. This creates a practical imbalance that favors agencies in borderline cases. Despite this, the statutory standard remains "clearly unwarranted" — agencies should be challenged when they invoke this exemption for clearly public information.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(2)',
        'exemption_number': '§ 1-27-1.5(2)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled by law enforcement agencies in the course of criminal investigations and prosecutions are exempt from disclosure while investigations and prosecutions are ongoing, to the extent that disclosure would interfere with law enforcement proceedings.',
        'scope': 'Records compiled by law enforcement agencies in active criminal investigations and prosecutions. The exemption applies while the investigation or prosecution is ongoing. Once proceedings conclude, records generally become public. South Dakota courts have been somewhat more permissive about law enforcement withholding than states with stronger access laws, but the statutory standard still requires an ongoing proceeding and a specific interference risk. Arrest records, booking information, and basic incident reports documenting the existence and nature of an incident are generally public even during ongoing investigations.',
        'key_terms': json.dumps([
            'criminal investigation', 'law enforcement records', 'ongoing investigation',
            'pending prosecution', 'investigative file', 'enforcement proceeding',
            'interference with investigation', 'police records', 'criminal records',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records, booking information, and basic incident reports are public regardless of investigative status',
            'Once prosecution concludes or investigation closes without charges, records are generally public',
            'The exemption requires an ongoing proceeding and specific interference risk, not merely that records relate to a "law enforcement matter"',
            'Factual information that does not reveal investigative techniques or endanger safety must be released',
            'South Dakota courts have held that the exemption does not provide blanket protection for all law enforcement agency records',
            'Challenge categorical withholding where the agency asserts exemption for entire files rather than specific records',
        ]),
        'notes': 'SDCL § 1-27-1.5(2) is South Dakota\'s law enforcement investigative records exemption. Like all South Dakota open records exemptions, the practical enforcement challenge is that a requester\'s only remedy is a mandamus action with no fee-shifting — this creates a significant practical barrier to challenging unjustified law enforcement withholding. Despite this, the statutory standard requires an ongoing proceeding, and arrest records and incident reports remain public.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(3)',
        'exemption_number': '§ 1-27-1.5(3)',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information of a privileged or confidential nature obtained from a person are exempt from South Dakota\'s Open Records Law, provided that disclosure would cause substantial harm to the competitive position of the source.',
        'scope': 'Trade secrets and confidential commercial or financial information submitted to South Dakota government agencies by private entities. The exemption requires that information be (1) from a private entity, (2) a trade secret or privileged/confidential commercial/financial information, and (3) whose disclosure would cause substantial competitive harm. Government-generated records cannot constitute trade secrets. Contract amounts, expenditure records, and bid results after award are generally public. The agency must make an independent determination of trade secret claims. In South Dakota\'s practical environment — with no attorney\'s fees and no penalties — agencies may be more willing to accept broad trade secret designations from vendors.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'substantial harm',
            'competitive position', 'business confidential',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts and amounts paid with public funds are always public — trade secret claims do not protect government expenditure records',
            'The submitter must demonstrate substantial competitive harm, not merely assert confidentiality',
            'Information publicly available elsewhere cannot be withheld as a trade secret',
            'Government-generated records cannot be trade secrets — only privately submitted information qualifies',
            'The agency must independently evaluate claims rather than simply accepting vendor designations',
            'South Dakota\'s weak enforcement does not change the statutory standard — challenge overbroad trade secret claims on the merits',
        ]),
        'notes': 'SDCL § 1-27-1.5(3) provides the trade secret exemption in South Dakota\'s open records framework. The practical reality is that South Dakota\'s lack of attorney\'s fees and penalties creates an environment where agencies may be more willing to accept broad vendor trade secret designations without independent scrutiny. Despite this, the statutory standard requires substantial competitive harm, and government expenditure records and contract amounts are always public.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(4)',
        'exemption_number': '§ 1-27-1.5(4)',
        'short_name': 'Deliberative Process — Preliminary Agency Materials',
        'category': 'deliberative',
        'description': 'Preliminary, draft, or predecisional documents, notes, recommendations, and intra-agency memoranda in which opinions are expressed or policies formulated prior to final agency action are exempt from South Dakota\'s Open Records Law.',
        'scope': 'Predecisional documents including drafts, internal memoranda, and recommendations that reflect agency deliberation and that have not been adopted as final policy. The exemption covers only opinion-based and deliberative content — purely factual material must be released. Once a draft or recommendation becomes final agency policy, the exemption no longer applies. South Dakota courts have been somewhat deferential in applying this exemption, consistent with the general pattern of agency-favorable interpretation. Factual data underlying recommendations, working law, and adopted standards must be disclosed.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional document',
            'intra-agency memorandum', 'working paper', 'recommendation',
            'policy deliberation', 'draft document', 'opinion on policy',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — the exemption covers only opinion portions',
            'Once a draft or recommendation is adopted as agency policy, the exemption no longer applies',
            '"Working law" — standards and criteria agencies actually apply — must be disclosed',
            'Challenge claims that entire documents are deliberative where only isolated recommendation sections qualify',
            'Documents circulated outside the agency may lose their predecisional character',
            'South Dakota\'s deference to agencies on this exemption does not change the requirement that the specific document must be predecisional and deliberative',
        ]),
        'notes': 'SDCL § 1-27-1.5(4) is South Dakota\'s deliberative process exemption. South Dakota courts have been generally deferential in applying exemptions under the state\'s weak open records law. The practical effect is that requesters rarely challenge deliberative process withholding given the cost of mandamus litigation with no fee-shifting. Despite this, the statutory standard requires that the document be both predecisional and deliberative, and purely factual material must be released.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(5)',
        'exemption_number': '§ 1-27-1.5(5)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or work product doctrine are exempt from South Dakota\'s Open Records Law. The privilege applies to confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice.',
        'scope': 'Confidential communications between South Dakota government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The standard elements of the privilege apply: communication between attorney and client, for the purpose of legal advice, made in confidence, not waived. South Dakota courts have applied the privilege in the government context similarly to its application in private litigation. Policy communications from government attorneys who also perform non-legal functions are generally not privileged. Billing records and engagement terms with outside counsel are generally public.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'government attorney',
            'privileged communication', 'litigation privilege', 'legal opinion',
            'confidential communication', 'in anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'Communications for policy guidance — even from government attorneys — are not privileged',
            'Waiver occurs when substance is disclosed in public proceedings or to non-attorney personnel',
            'Attorney billing records are generally public in South Dakota',
            'Facts independently known to the agency are not protected',
            'Challenge whether communications labeled "legal advice" are in fact policy guidance from in-house counsel',
            'The privilege belongs to the agency, which may waive it',
        ]),
        'notes': 'South Dakota recognizes the attorney-client privilege for government entities under § 1-27-1.5(5). South Dakota courts apply the privilege in the government context with reference to standard privilege principles. The weak enforcement mechanism of the open records law means that privilege claims are less frequently challenged than in states with stronger access laws, but the privilege\'s substantive requirements — legal advice, confidentiality, no waiver — remain.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(7)',
        'exemption_number': '§ 1-27-1.5(7)',
        'short_name': 'Medical and Health Records',
        'category': 'privacy',
        'description': 'Medical records, psychiatric records, and other health information pertaining to identifiable individuals held by government agencies are exempt from South Dakota\'s Open Records Law to protect individual health privacy.',
        'scope': 'Individually identifiable medical, psychiatric, and health records held by South Dakota government agencies, including health departments, correctional facilities, and public hospitals. The exemption reflects strong individual health privacy interests and is supported by both South Dakota law and federal HIPAA. Aggregate health statistics and anonymized public health data are public. The operational records of health agencies — budgets, contracts, and program documents — are public.',
        'key_terms': json.dumps([
            'medical records', 'health records', 'psychiatric records', 'patient records',
            'treatment records', 'health information', 'HIPAA', 'medical privacy',
            'mental health records', 'health confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public',
            'Health agency operational records, contracts, and budget documents are public',
            'Challenge claims that operational health and safety records (inspection reports, facility compliance) are protected as "medical records"',
            'A public official\'s medical condition may be relevant to their fitness for public duties in narrow circumstances',
        ]),
        'notes': 'SDCL § 1-27-1.5(7) is South Dakota\'s medical records exemption under the open records law. This exemption is among the clearest and most consistently applied in South Dakota open records practice — the privacy interest in health information is self-evident and well-established. The exemption applies to patient records, not to the operational records of health agencies.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(8)',
        'exemption_number': '§ 1-27-1.5(8)',
        'short_name': 'Security Plans and Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and records detailing specific security vulnerabilities or security measures for government buildings, critical infrastructure, and emergency response systems are exempt from South Dakota\'s Open Records Law where disclosure would create a security risk.',
        'scope': 'Security plans, vulnerability assessments, and specific operational security records for government facilities and critical infrastructure where disclosure would create an articulable security risk. The exemption is targeted at records whose disclosure would directly enable harm — not at all security-related records. Budget and expenditure records for security programs are public. General descriptions of security policies that do not reveal specific vulnerabilities are public.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'facility security', 'infrastructure security',
            'cyber security', 'emergency response', 'access control',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not merely asserted',
            'Budget and expenditure records for security programs are public',
            'General security policy descriptions that do not reveal specific vulnerabilities are not covered',
            'Challenge claims that entire security vendor contracts are exempt when only narrow technical specifications qualify',
        ]),
        'notes': 'SDCL § 1-27-1.5(8) is South Dakota\'s security infrastructure exemption. Even in South Dakota\'s weak open records environment, the security exemption requires a specific articulable risk — not just that records relate to "security." However, the practical reality is that South Dakota\'s lack of enforcement mechanisms means agencies face little pressure to justify security withholding claims precisely.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(6)',
        'exemption_number': '§ 1-27-1.5(6)',
        'short_name': 'Personnel Files — Employee Privacy',
        'category': 'privacy',
        'description': 'Personnel files and employment records of public employees are exempt from South Dakota\'s Open Records Law to the extent they contain information whose disclosure would constitute a clearly unwarranted invasion of personal privacy, though compensation and significant disciplinary records are generally public.',
        'scope': 'Personnel files, employment applications, performance evaluations, and similar records of government employees. South Dakota\'s personnel file exemption is broadly interpreted by some agencies, consistent with the general pattern of weak enforcement. However, the statutory standard still requires that disclosure constitute a "clearly unwarranted" privacy invasion. Compensation, salary, and job title information for public employees is generally public. Disciplinary actions resulting in termination, demotion, or suspension are matters of public record. The exemption most clearly protects home addresses, medical information, and minor disciplinary details.',
        'key_terms': json.dumps([
            'personnel file', 'employment record', 'public employee', 'personal privacy',
            'performance evaluation', 'disciplinary record', 'salary information',
            'government employee', 'HR record',
        ]),
        'counter_arguments': json.dumps([
            'Compensation, salary, and job title information for public employees is generally public even under South Dakota\'s weak open records law',
            'Disciplinary actions resulting in termination, demotion, or suspension are matters of public record',
            'Records of official conduct in the employee\'s government capacity are public',
            'The "clearly unwarranted" standard requires specific justification — South Dakota\'s weak enforcement does not change this substantive threshold',
            'Challenge blanket withholding of personnel files by identifying the specific public accountability interest in the requested records',
        ]),
        'notes': 'SDCL § 1-27-1.5(6) is South Dakota\'s personnel file exemption. The practical context of South Dakota\'s weak enforcement means that agencies sometimes apply this exemption more broadly than the statutory standard warrants. Despite the limited enforcement mechanism, the substantive standard — "clearly unwarranted" privacy invasion — remains the legal test, and compensation and significant disciplinary records are public.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 10-59-36',
        'exemption_number': '§ 10-59-36',
        'short_name': 'Tax Return Information',
        'category': 'privacy',
        'description': 'Individual and business tax returns and related tax information submitted to or held by the South Dakota Department of Revenue are confidential and exempt from public disclosure under South Dakota tax confidentiality statutes.',
        'scope': 'Tax returns and return information submitted to or held by the South Dakota Department of Revenue in connection with sales tax, use tax, and other state tax administration. The confidentiality provision is absolute for return data — it does not apply to aggregate revenue statistics, enforcement policy documents, or the Department\'s operational records. Final court judgments in tax collection proceedings and recorded tax liens are public. The Department\'s administrative records and program documents are public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'sales tax',
            'tax confidentiality', 'taxpayer information', 'business tax return',
            'tax filing', 'return information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Recorded tax liens and final court judgments in tax collection proceedings are public',
            'The Department\'s operational records, audit policies, and program documents are public',
            'Challenge whether records constitute "tax return information" versus general regulatory correspondence',
        ]),
        'notes': 'South Dakota\'s tax return confidentiality under § 10-59-36 is among the most clearly established exemptions in South Dakota open records practice. The confidentiality applies to return data, not to the Department\'s operational records. Like all South Dakota open records matters, the weak enforcement mechanism means agencies face limited practical pressure to justify withholding decisions, but the substantive scope of the exemption is clear.',
    },
    {
        'jurisdiction': 'SD',
        'statute_citation': 'SDCL § 1-27-1.5(9)',
        'exemption_number': '§ 1-27-1.5(9)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real estate appraisals, feasibility studies, and related valuation documents prepared by or for a government agency in connection with the prospective acquisition or sale of real property are exempt until the transaction is complete or abandoned.',
        'scope': 'Formal real estate appraisals and property valuations prepared for South Dakota government agencies in connection with pending real property acquisitions or sales. The exemption is temporary — it expires when the transaction closes or is abandoned. The purpose is to prevent agencies from being disadvantaged in negotiation if their maximum willingness to pay is disclosed pre-purchase. Post-transaction, all appraisal and valuation records are public. Given South Dakota\'s general open records environment, some agencies may attempt to extend this exemption beyond completed transactions, which should be challenged.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'pre-acquisition appraisal', 'real property purchase',
            'land purchase', 'condemnation appraisal', 'eminent domain',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete or abandoned — post-transaction appraisals are public',
            'Challenge the agency\'s claim that the transaction remains "pending" if negotiations have stalled for an extended period',
            'After condemnation judgment, all valuation records are public',
            'Budget documents and legislative appropriations for property acquisition are public',
            'Appraisals for property already owned by the agency are not covered',
        ]),
        'notes': 'SDCL § 1-27-1.5(9) is South Dakota\'s real property appraisal exemption. Like all SD open records matters, the weak enforcement mechanism means agencies face limited practical pressure to release post-transaction appraisals promptly. Despite this, the exemption automatically expires upon transaction completion, and requesters should specifically request post-transaction appraisals with a note that the transaction is concluded.',
    },
]

# =============================================================================
# RULES
# South Dakota Open Records Law, SDCL § 1-27-1 et seq.
# Key features: NO specific response deadline ("reasonable hours" only); NO
# administrative appeal; NO attorney's fees; NO penalties for non-compliance;
# only remedy is mandamus in Circuit Court; no fee cap in statute (fees must
# be "reasonable"). South Dakota is widely considered one of the weakest
# open records laws in the US.
# =============================================================================

SD_RULES = [
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline',
        'param_value': 'no_specific_deadline_reasonable_hours_only',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not specify any response deadline. Agencies are required to allow inspection and copying of public records "at reasonable hours," but there is no 5-day, 10-day, or 30-day response clock. This is one of South Dakota\'s most significant procedural deficiencies. In practice, agencies may take weeks or months to respond with no legal consequence, since there are no penalties for delay and no administrative appeal process. A requester experiencing unreasonable delay may petition the Circuit Court for a mandamus order, but the cost of doing so (with no fee-shifting) makes this impractical for most requests.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'access_at_reasonable_hours',
        'param_value': 'yes_during_normal_business_hours',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law guarantees access to public records "at reasonable hours." This generally means during normal government business hours. Agencies may not restrict access to a narrow window of hours or require appointments far in advance. While there is no specific response deadline, the "reasonable hours" standard does provide some basis for challenging agencies that impose unreasonable access restrictions. Requesters should specifically request that records be provided in electronic format to avoid in-person inspection requirements.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency_but_weak_enforcement',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s statute does not explicitly place the burden of proof on the agency, and South Dakota courts have not established as clear a presumption of disclosure as states like Washington or Montana. The practical effect is that agencies in South Dakota have more latitude to withhold records without detailed justification, since the only enforcement mechanism is an expensive mandamus action with no fee-shifting. Requesters should nonetheless demand specific statutory justification for any denial, citing the general principle that open records laws are to be construed in favor of disclosure.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_standard',
        'param_value': 'reasonable_cost_no_statutory_cap',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not establish a specific per-page fee cap. Agencies may charge "reasonable" fees for copying. In practice, many South Dakota agencies charge $0.25 per page or less, consistent with actual reproduction costs. Unlike states with explicit statutory caps (Rhode Island at $0.15/page, Montana at $0.10/page), South Dakota\'s lack of a cap means agencies have more latitude on fee amounts. Requesters should challenge fees that appear disproportionate to actual reproduction costs and request electronic delivery to minimize fees.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fees',
        'param_value': 'potentially_chargeable_no_statutory_prohibition',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not explicitly prohibit agencies from charging for staff time spent locating or reviewing records, unlike states with explicit prohibitions (Washington, Montana, Rhode Island). Some South Dakota agencies charge search and retrieval fees, particularly for large or complex requests. This is one of South Dakota\'s weaker aspects compared to most state open records laws. Requesters should contest search and retrieval fees and argue that only actual reproduction costs are permissible, but the statutory support for this position is weaker in South Dakota than in most states.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver',
        'param_value': 'agency_discretion_only_no_statutory_provision',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not include any fee waiver provision. There is no statutory right to a fee waiver for any requester category, including news media, nonprofits, or academic researchers. Agencies may waive fees at their discretion, and some do so in practice. Requesters should ask for fee waivers based on public interest grounds, but should not expect them as a matter of right under South Dakota law. For electronic records delivered by email, actual cost is typically zero, effectively mooting the fee issue for many requests.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota has NO administrative appeal mechanism for open records denials. There is no agency head review, no state attorney general review process, no ombudsman, and no administrative tribunal. A requester who receives an improper denial must go directly to Circuit Court by filing a mandamus action. This is the single most significant structural weakness of South Dakota\'s open records law. Unlike Delaware (which has the AG advisory opinion process) or many other states (which have formal administrative appeals), South Dakota provides no cost-effective intermediate remedy.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_mandamus',
        'param_value': 'available_mandamus_only',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1; SDCL § 21-29-1 et seq.',
        'notes': 'The only enforcement mechanism under South Dakota\'s Open Records Law is a mandamus action in Circuit Court under SDCL § 21-29-1 et seq. Mandamus requires showing a clear legal right to the records, a corresponding duty on the agency to produce them, and no other adequate remedy. South Dakota Circuit Courts will issue mandamus orders where an agency has clearly violated the open records law, but the cost of litigation — without fee-shifting — makes this remedy impractical for most individual requests. South Dakota\'s lack of any other enforcement mechanism is widely cited by open government advocates as its most significant deficiency.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees',
        'param_value': 'not_available',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does NOT provide for attorney\'s fees for prevailing requesters. This is one of its most significant weaknesses compared to most other state open records laws. Without fee-shifting, the cost of Circuit Court mandamus litigation effectively prices out most individual requesters. This creates a strong practical deterrent against challenging agency withholding decisions. South Dakota is in a small minority of states that do not provide some form of fee-shifting for prevailing open records requesters.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'penalty',
        'param_key': 'civil_penalties',
        'param_value': 'not_available',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not provide for civil penalties or fines against agencies or officials who violate the statute. There are no per diem penalties (like Washington\'s $5-$100/day), no civil fines (like Rhode Island\'s $2,000 per violation), and no contempt sanctions for non-compliance with mandamus orders outside of standard contempt proceedings. The complete absence of penalties means agencies face no financial risk for non-compliance, which significantly undermines the law\'s effectiveness.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes_by_general_principle',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not contain an explicit segregability requirement comparable to Washington (RCW 42.56.210) or Rhode Island (R.I.G.L. § 38-2-3(b)). However, the general principle that agencies must release nonexempt portions of records is implied by the access right and supported by South Dakota case law. Requesters should specifically invoke the segregability principle and request that redacted, non-exempt portions of partially withheld records be released. Without an explicit statutory provision, this argument relies on the general construction of open records laws in favor of disclosure.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes_by_general_interpretation',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law references "public records" generally and has been interpreted to encompass electronic records. Requesters may request records in electronic format, and agencies generally comply when records exist electronically. There is no specific statutory provision requiring electronic access, unlike states with explicit electronic records provisions. For electronic records delivered by email, actual cost is typically zero — requesting electronic delivery is the most effective way to minimize costs and avoid search/retrieval fee issues in South Dakota\'s weak fee structure.',
    },
    {
        'jurisdiction': 'SD',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_best_practice',
        'param_value': 'required_by_general_principle',
        'day_type': None,
        'statute_citation': 'SDCL § 1-27-1',
        'notes': 'South Dakota\'s Open Records Law does not contain an explicit requirement that denials be in writing with specific statutory citations, unlike Delaware (29 Del. Code § 10003(h)(3)) or Rhode Island. In practice, requesters should always demand written denials with specific statutory citations for withheld records, even though the statute does not explicitly require them. Without a written denial and statutory citation, it is difficult to evaluate whether withholding is justified or to challenge it in Circuit Court. South Dakota\'s weak statutory framework makes it especially important for requesters to document all communications.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

SD_TEMPLATES = [
    {
        'jurisdiction': 'SD',
        'record_type': 'general',
        'template_name': 'General South Dakota Open Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — SDCL § 1-27-1 et seq.

Dear Custodian of Records:

Pursuant to South Dakota's Open Records Law, SDCL § 1-27-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional context:
{{additional_context}}

I request that records be provided in electronic format (via email or download link) where records exist in electronic form, which minimizes both cost and the need for in-person inspection.

I am willing to pay reasonable copying fees reflecting the actual cost of reproduction. I am not willing to pay for staff time spent locating or reviewing records beyond what is necessary for reasonable access. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

South Dakota's open records law establishes a right to inspect and copy public records. This right should be construed in favor of access. If any records or portions of records are withheld, I request that you:
(1) identify each record withheld;
(2) state the specific statutory provision under which records are being withheld (citing the precise section of SDCL);
(3) explain how the claimed exemption applies to each withheld record; and
(4) release all nonexempt, reasonably segregable portions of any partially withheld records.

While I understand that South Dakota law does not specify a response deadline, I request a response at the earliest practicable time consistent with the "reasonable hours" standard of SDCL § 1-27-1. Please confirm receipt of this request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived or minimized for this request. South Dakota\'s open records law does not mandate fee waivers, but I ask that {{agency_name}} exercise its discretion to accommodate this request because:

1. These records relate to {{public_interest_explanation}}, a matter of public accountability and government transparency.

2. If records are delivered electronically (via email), the actual cost of reproduction is effectively zero, and a fee waiver or reduction would be consistent with the spirit of South Dakota\'s open records law.

3. I am {{requester_category_description}} and the public will benefit from disclosure because {{public_benefit_explanation}}.''',
        'expedited_language': '''I request that this open records request be processed as promptly as possible. While South Dakota\'s open records law does not specify a response deadline, unreasonable delay may constitute a denial that I may challenge in Circuit Court.

I need these records as soon as practicable because: {{expedited_justification}}. These records are needed by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me if there are any questions that might allow faster production.''',
        'notes': 'General-purpose South Dakota Open Records Law template. Key SD limitations that requesters must understand: (1) NO response deadline — "reasonable hours" only; (2) NO administrative appeal — only Circuit Court mandamus; (3) NO attorney\'s fees for prevailing requesters — making litigation impractical for most; (4) NO civil penalties for violations; (5) NO statutory fee cap — "reasonable" fees only; (6) search/retrieval fees may be chargeable; (7) NO explicit segregability requirement (though implied). South Dakota is widely considered one of the weakest open records laws in the US. Requesters should be persistent but realistic about enforcement options. Document all communications carefully. For significant requests, consider whether the cost of mandamus litigation is justified. Emphasize in the request letter that the law is construed in favor of disclosure.',
    },
    {
        'jurisdiction': 'SD',
        'record_type': 'law_enforcement',
        'template_name': 'South Dakota Open Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Law Enforcement Records, SDCL § 1-27-1 et seq.

Dear Custodian of Records:

Pursuant to South Dakota's Open Records Law, SDCL § 1-27-1 et seq., I request copies of the following law enforcement records:

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
- Written communications relating to the above
- Officer disciplinary records for involved personnel

Regarding any claimed exemption under SDCL § 1-27-1.5(2): South Dakota\'s law enforcement investigative records exemption applies only to records of ongoing criminal investigations and prosecutions where disclosure would specifically interfere with those proceedings. The exemption does not apply to: (1) arrest records, booking information, and basic incident reports; (2) records of concluded investigations and prosecutions; or (3) records not compiled for law enforcement investigative purposes.

Please provide a written response identifying any withheld records by description and citing the specific statutory provision and the specific harm that disclosure would cause for each withheld record.

I am willing to pay reasonable copying fees for reproduction. Please contact me regarding fee estimates before incurring significant copying costs.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be minimized or waived for this law enforcement records request. These records concern {{public_interest_explanation}}, a matter of public accountability for government conduct. Electronic delivery incurs no reproduction cost and I request that format as the preferred method of delivery.''',
        'expedited_language': '''I request prompt processing of this open records request. While South Dakota\'s open records law does not specify a response deadline, I need these records as soon as practicable because: {{expedited_justification}}. Needed by {{needed_by_date}}.''',
        'notes': 'South Dakota law enforcement records template under the Open Records Law. Key points specific to SD law enforcement records: (1) § 1-27-1.5(2) applies only to ongoing investigations — arrest records and incident reports are public; (2) SD\'s weak enforcement means agencies may be more willing to broadly invoke the law enforcement exemption — push back with specific challenges; (3) document all communications in writing since there is no administrative appeal process and Circuit Court mandamus requires a clear factual record; (4) no attorney\'s fees means challenging denial is expensive — focus requests on clearly public records to maximize practical access; (5) no response deadline — follow up in writing if no response within 10-15 business days.',
    },
    {
        'jurisdiction': 'SD',
        'record_type': 'government_contracts',
        'template_name': 'South Dakota Open Records Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Government Contracts and Expenditure Records, SDCL § 1-27-1 et seq.

Dear Custodian of Records:

Pursuant to South Dakota's Open Records Law, SDCL § 1-27-1 et seq., I request the following records concerning public expenditures and government contracts:

{{description_of_records}}

This request includes, but is not limited to:
- All contracts, amendments, and purchase orders with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Payment records and invoices for the above contracts
- Procurement records including solicitations, bids received, bid evaluations, and award justifications
- Correspondence between the agency and {{vendor_or_contractor}} relating to contract performance

Note on trade secret claims: Amounts paid with public funds, bid results after contract award, and government expenditure records are not protectable trade secrets under South Dakota law — SDCL § 1-27-1.5(3) requires demonstration of substantial competitive harm from disclosure, and government expenditure data does not meet this standard. Please provide specific justification for any withholding, citing the specific provision of SDCL that applies to each withheld record and explaining the specific harm that disclosure would cause.

While I understand South Dakota\'s open records law does not provide a specific response deadline, I request a response as soon as reasonably practicable. Please confirm receipt of this request.

I am willing to pay reasonable copying fees. Electronic delivery is preferred.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be minimized or waived for this government spending records request. These records concern {{public_interest_explanation}}, a matter of core accountability — how South Dakota government spends public funds. South Dakota\'s open records law reflects a public policy in favor of transparency about government expenditures. Electronic delivery incurs no cost. I appreciate your consideration.''',
        'expedited_language': '''I request prompt processing of this request for government spending records. While South Dakota\'s open records law does not specify a response deadline, I need these records as soon as practicable because: {{expedited_justification}}. Needed by {{needed_by_date}}.''',
        'notes': 'South Dakota government contracts/spending template under the Open Records Law. Key points: (1) government expenditure records are core public records even under SD\'s weak law — trade secret claims do not protect contract amounts; (2) bid results after award are public; (3) document all requests and communications carefully since Circuit Court mandamus requires a clear record; (4) SD\'s lack of attorney\'s fees means requesters should focus on clearly public records (contracts, invoices, expenditures) where the case for mandamus would be most clear-cut; (5) no response deadline — follow up in writing if no response within 10-15 business days; (6) electronic delivery preferred to minimize costs and avoid search/retrieval fee issues.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in SD_EXEMPTIONS:
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

    print(f'SD exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in SD_RULES:
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

    print(f'SD rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in SD_TEMPLATES:
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

    print(f'SD templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'SD total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_sd', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
