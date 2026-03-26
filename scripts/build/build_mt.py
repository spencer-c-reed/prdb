#!/usr/bin/env python3
"""Build Montana Right to Know data: exemptions, rules, and templates.

Covers Montana's Right to Know constitutional provision (Mont. Const. Art. II, § 9)
and the statutory framework at Mont. Code Ann. § 2-6-101 et seq. Montana's Right to
Know is grounded in the state constitution, which provides a stronger foundation for
access than a purely statutory scheme. There is no specific response deadline — agencies
must respond "in a reasonable time." No administrative appeal exists; enforcement is by
petition to District Court. Copy fees are capped at $0.10/page. Attorney's fees are
available for prevailing requesters.

Run: python3 scripts/build/build_mt.py
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
# Montana's public records law is rooted in the state constitution (Art. II, § 9),
# which declares a right to know about government affairs. Statutory exemptions at
# Mont. Code Ann. § 2-6-101 et seq. and scattered throughout the code limit this
# right. Because the right is constitutional, courts apply strict scrutiny to
# exemptions and narrowly construe them against the agency. The constitutional
# foundation makes Montana's access rights particularly strong.
# =============================================================================

MT_EXEMPTIONS = [
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(1)',
        'exemption_number': '§ 2-6-1003(1)',
        'short_name': 'Privacy — Clearly Unwarranted Invasion',
        'category': 'privacy',
        'description': 'Information that would constitute a clearly unwarranted invasion of personal privacy is exempt from disclosure under Montana\'s Right to Know. The privacy interest must substantially outweigh the public interest in disclosure. Courts apply a balancing test that begins with the constitutional presumption of public access.',
        'scope': 'Personally identifiable information whose disclosure would constitute a clearly unwarranted invasion of personal privacy. Montana applies a balancing test: the individual\'s privacy interest is weighed against the public\'s interest in disclosure. Because the Right to Know has constitutional status, the privacy interest must clearly and substantially outweigh the public interest — a high threshold. Information about public officials conducting government business, compensation of public employees, and government operations generally does not qualify for the privacy exemption. The most clearly protected information includes Social Security numbers, medical records, home addresses of private individuals, and similar highly personal data.',
        'key_terms': json.dumps([
            'personal privacy', 'clearly unwarranted', 'privacy invasion',
            'personally identifiable information', 'privacy interest', 'public interest',
            'balancing test', 'individual privacy', 'private information',
        ]),
        'counter_arguments': json.dumps([
            'The privacy exemption requires that the invasion be "clearly unwarranted" — a high threshold given Montana\'s constitutional right to know',
            'Public employees\' compensation, official conduct, and performance of government duties are not protected by this exemption',
            'The agency must demonstrate both that a privacy interest exists and that it clearly and substantially outweighs the public interest in disclosure',
            'Information about how government money is spent, contracts awarded, and official decisions made is presumptively public notwithstanding privacy claims',
            'Challenge overbroad privacy claims where the agency has redacted non-private contextual information along with genuinely personal data',
            'Montana courts interpret privacy exemptions narrowly given the constitutional foundation of the right to know',
        ]),
        'notes': 'Montana\'s privacy exemption in § 2-6-1003(1) must be read against the backdrop of the constitutional right to know in Art. II, § 9. The Montana Supreme Court has consistently held that exemptions to the constitutional right are narrowly construed. The "clearly unwarranted" standard is more demanding than a simple privacy-interest test. See Great Falls Tribune Co. v. Day, 2006 MT 353 for the balancing framework.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(2)',
        'exemption_number': '§ 2-6-1003(2)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records compiled for law enforcement purposes are exempt from disclosure where disclosure could reasonably be expected to interfere with enforcement proceedings, deprive a person of a fair trial, reveal confidential informant identity, endanger safety, or disclose investigative techniques.',
        'scope': 'Records compiled by law enforcement agencies in the course of criminal investigations. The exemption applies only where a specific harm can be articulated — it does not provide blanket protection for all law enforcement records. Montana courts, consistent with the constitutional right to know, require that each withheld record be connected to a specific enumerated harm. Arrest records, basic incident information, booking data, and records documenting the existence and nature of an incident are generally public. Once prosecution is concluded, investigative files of closed matters are generally public. The exemption does not apply to civil rights investigations by law enforcement agencies unless a criminal proceeding is pending.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'pending prosecution', 'enforcement proceeding',
            'fair trial', 'endangerment', 'investigative file', 'right to know',
        ]),
        'counter_arguments': json.dumps([
            'Montana\'s constitutional right to know requires specific harm justification — each withheld record must be connected to a specific enumerated harm',
            'Arrest records, booking information, and basic incident reports are public regardless of investigative status',
            'Completed investigation files are generally public once prosecution concludes or investigation closes without charges',
            'Factual information in investigative files that does not reveal informants, techniques, or create safety risks must be segregated and released',
            'Challenge categorical withholding where the agency asserts exemption for entire files rather than specific records',
            'Montana courts narrowly construe law enforcement exemptions given the constitutional access right',
        ]),
        'notes': 'Montana\'s law enforcement investigative records exemption in § 2-6-1003(2) is narrowly construed given the constitutional right to know. The Montana Supreme Court has held that agencies must articulate specific harm from disclosure — generalized assertions that records relate to "an investigation" are insufficient. Arrest records are among the most commonly requested public records in Montana, and they are public.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(3)',
        'exemption_number': '§ 2-6-1003(3)',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information submitted to a government agency by a private entity that would cause substantial competitive harm if disclosed are exempt from Montana\'s Right to Know.',
        'scope': 'Information submitted to Montana government agencies by private entities that constitutes a genuine trade secret or confidential commercial or financial information whose disclosure would cause substantial competitive harm. The exemption requires: (1) the information was submitted by a private entity; (2) it constitutes a trade secret or is confidential commercial/financial information; and (3) disclosure would cause substantial competitive harm. Government-generated records cannot qualify. Contract amounts, amounts paid with public funds, and bid results after award are generally public. The agency must make an independent determination — it cannot simply accept a vendor\'s confidentiality designation.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'substantial harm',
            'competitive position', 'business confidential', 'economic advantage',
        ]),
        'counter_arguments': json.dumps([
            'Contract amounts and amounts paid with public funds are public regardless of trade secret claims',
            'The submitter must demonstrate substantial competitive harm from disclosure, not merely assert that information is proprietary',
            'Information that has been publicly disclosed elsewhere cannot be withheld as a trade secret',
            'Government-generated records cannot constitute trade secrets',
            'The agency bears independent responsibility to evaluate trade secret claims — it may not simply defer to vendor designations',
            'Challenge overbroad claims where entire contracts are withheld when only narrow technical specifications might qualify for protection',
        ]),
        'notes': 'Montana\'s trade secret exemption requires a showing of substantial competitive harm — a higher threshold than merely asserting information is "confidential." The agency must conduct an independent evaluation of each claim. Montana courts apply this exemption narrowly given the constitutional right to know. Government expenditure records and contract pricing are uniformly public in Montana.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(4)',
        'exemption_number': '§ 2-6-1003(4)',
        'short_name': 'Deliberative Process — Preliminary Agency Documents',
        'category': 'deliberative',
        'description': 'Preliminary agency documents including drafts, notes, recommendations, and intra-agency memoranda that are predecisional and deliberative in nature are exempt from disclosure under Montana\'s Right to Know, subject to the constitutional presumption of public access.',
        'scope': 'Predecisional, deliberative documents including drafts, internal memoranda, and recommendations that reflect the give-and-take of agency deliberation. The exemption is limited to documents that are both predecisional (produced before a final decision) and genuinely deliberative (reflecting the agency\'s reasoning process, not mere factual data). Montana courts apply this exemption very narrowly given the constitutional right to know. Purely factual material within deliberative documents must be released. Final agency decisions, adopted policies, and "working law" are always public. The Montana Supreme Court has emphasized that the public\'s interest in government transparency requires a strong presumption against the deliberative process exemption.',
        'key_terms': json.dumps([
            'deliberative process', 'preliminary draft', 'predecisional document',
            'intra-agency memorandum', 'working paper', 'recommendation',
            'advisory opinion', 'policy deliberation', 'draft document',
        ]),
        'counter_arguments': json.dumps([
            'Montana\'s constitutional right to know creates a strong presumption against deliberative process withholding — courts apply the exemption very narrowly',
            'Purely factual material within deliberative documents must be released — the exemption applies only to opinion and deliberative portions',
            'Once a draft or recommendation is adopted as final agency policy, the exemption no longer applies',
            '"Working law" — policies, standards, and criteria agencies actually apply — must be disclosed even in internal documents',
            'Documents circulated to persons outside the agency may lose their predecisional character',
            'The agency must demonstrate that the specific document, or specific portion, is both predecisional and deliberative — general labels are insufficient',
        ]),
        'notes': 'Montana\'s deliberative process exemption is among the most narrowly construed in the United States given the constitutional right to know in Art. II, § 9. The Montana Supreme Court has consistently held that the constitutional access right requires that exemptions be narrowly interpreted. The factual/opinion distinction is critical, and agencies must demonstrate both prongs (predecisional and deliberative) for each withheld document.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(5)',
        'exemption_number': '§ 2-6-1003(5)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between government agencies and their legal counsel that are subject to the attorney-client privilege are exempt from disclosure under Montana\'s Right to Know. The privilege is applied narrowly given the constitutional access right.',
        'scope': 'Confidential communications between Montana government agencies and their attorneys (state or local government lawyers) made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege requires that the communication be for legal (not policy or business) advice, made in confidence, and not waived. Given Montana\'s constitutional right to know, courts apply the attorney-client privilege for government entities more narrowly than in the private sector. Billing records, engagement terms, and general financial arrangements with outside counsel are generally public. Facts independently known to the agency are not privileged merely because they were communicated to counsel.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'government attorney',
            'privileged communication', 'litigation privilege', 'legal opinion',
            'confidential communication', 'in anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'Given Montana\'s constitutional right to know, the attorney-client privilege for government entities is applied more narrowly than in the private sector',
            'Communications for policy or business guidance — even from in-house counsel — are not privileged',
            'Billing records and engagement terms with outside counsel are generally public in Montana',
            'Waiver occurs when the agency discloses substance in public proceedings or to non-attorney personnel',
            'Challenge whether communications labeled "legal advice" are in fact policy guidance from attorneys who perform dual legal/policy functions',
            'The privilege belongs to the agency, which may waive it — challenge whether the agency has constructively waived by relying on the advice in public decisions',
        ]),
        'notes': 'Montana recognizes the attorney-client privilege and work product doctrine for government entities, but the constitutional right to know limits these protections. The Montana Supreme Court has emphasized that the privilege must be applied narrowly for government entities to preserve the public\'s constitutional right of access. Government attorneys who perform both legal and policy functions may not shield policy communications under the legal advice label.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'exemption_number': '§ 2-6-1006',
        'short_name': 'Personnel Records — Public Employee Privacy',
        'category': 'privacy',
        'description': 'Personnel files and employment records of public employees are generally exempt from disclosure to the extent they contain information whose disclosure would constitute a clearly unwarranted invasion of personal privacy, but compensation, official conduct, and disciplinary records are generally public.',
        'scope': 'Personnel files, employment applications, performance evaluations, and related records of government employees. The exemption applies to genuinely personal information — home addresses, medical records, and similar data unrelated to job performance. Compensation, salary, benefits, and job classification are uniformly public. Disciplinary records resulting in significant employment action (termination, demotion, suspension) are generally public. Records of official conduct in the employee\'s public capacity are public. Montana\'s constitutional right to know means that government employees have reduced privacy expectations regarding their official conduct compared to private individuals.',
        'key_terms': json.dumps([
            'personnel file', 'employment record', 'public employee', 'personal privacy',
            'performance evaluation', 'disciplinary record', 'salary information',
            'government employee', 'HR record', 'employment history',
        ]),
        'counter_arguments': json.dumps([
            'Compensation, salary, and benefits for public employees are always public — the constitutional right to know protects this',
            'Disciplinary actions resulting in termination, demotion, or suspension are matters of public record',
            'Records of official conduct in the employee\'s government capacity are public regardless of their location in personnel systems',
            'Montana\'s constitutional right to know requires that privacy claims be balanced against substantial public interest in government accountability',
            'Challenge blanket withholding of personnel files — the agency must identify the specific, narrow portions that qualify for privacy protection',
        ]),
        'notes': 'Montana\'s personnel records exemption must be balanced against the constitutional right to know. Montana courts have consistently held that public employee compensation is public, that records of official conduct are public, and that the personnel file exemption is limited to genuinely private information unrelated to the employee\'s government role. The constitutional foundation of Montana\'s access rights gives this exemption a narrower scope than in purely statutory states.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(6)',
        'exemption_number': '§ 2-6-1003(6)',
        'short_name': 'Medical and Health Records',
        'category': 'privacy',
        'description': 'Medical records, psychiatric records, and other health information pertaining to identifiable individuals held by government agencies are exempt from public disclosure to protect individual health privacy.',
        'scope': 'Medical records, psychiatric and psychological treatment records, health information, and similar records identifying health conditions of specific individuals. This exemption applies to records held by health agencies, correctional facilities, public hospitals, and any other state or local government entity. Aggregate health statistics, anonymized epidemiological data, and public health program information are public. The exemption applies to medical information about any individual, not just public employees. Records of a public official\'s medical condition may be subject to disclosure if directly relevant to their capacity to perform public duties.',
        'key_terms': json.dumps([
            'medical records', 'health records', 'psychiatric records', 'treatment records',
            'health information', 'patient records', 'medical privacy', 'HIPAA',
            'mental health records', 'identifiable health information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and anonymized data are public and not covered by this exemption',
            'Public health agency operational records, contracts, and program documents are public regardless of this exemption',
            'Where a public official\'s medical condition is directly relevant to their fitness to perform public duties, the balance may favor disclosure',
            'Challenge claims that operational health and safety records (inspection reports, facility compliance) are protected as "medical records"',
        ]),
        'notes': 'Montana\'s medical records exemption reflects strong individual health privacy protections that coexist with the constitutional right to know. The exemption is self-evidently justified because of the sensitive nature of health information. Consistent with the constitutional framework, it applies narrowly to individually identifiable health data, not to health program operations or public health statistics.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(7)',
        'exemption_number': '§ 2-6-1003(7)',
        'short_name': 'Security Plans for Public Infrastructure',
        'category': 'safety',
        'description': 'Records detailing specific security vulnerabilities, security plans, or vulnerability assessments for critical public infrastructure or government facilities are exempt from Montana\'s Right to Know where disclosure would create a specific, articulable security threat.',
        'scope': 'Security plans, vulnerability assessments, and related documents for critical infrastructure and public buildings where disclosure would directly enable a security breach or create a specific, identifiable threat. Montana courts apply this exemption narrowly — all security-related records are not exempt, only those whose disclosure would directly enable harm. Budget records and expenditure data for security programs are public. General descriptions of security policies that do not reveal specific vulnerabilities are public.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security threat', 'infrastructure security', 'facility protection',
            'cyber security', 'access control', 'security breach',
        ]),
        'counter_arguments': json.dumps([
            'Montana\'s constitutional right to know requires that the security threat be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'General security policy descriptions that do not reveal specific vulnerabilities are not exempt',
            'Challenge claims that entire contracts with security vendors are exempt when only narrow technical specifications qualify',
        ]),
        'notes': 'Montana\'s security infrastructure exemption is applied narrowly consistent with the constitutional right to know. Agencies must demonstrate a specific, articulable security threat from disclosure — not merely assert that records relate to "security." The constitutional foundation of the access right means that speculative security concerns are insufficient to justify withholding.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 15-30-2618',
        'exemption_number': '§ 15-30-2618',
        'short_name': 'Tax Return Information',
        'category': 'privacy',
        'description': 'Individual and business tax returns and related tax information submitted to or held by the Montana Department of Revenue are confidential and exempt from public disclosure under Montana tax confidentiality statutes.',
        'scope': 'Individual income tax returns, corporate tax returns, and related return information filed with or generated by the Montana Department of Revenue in connection with tax collection, audit, and enforcement. The confidentiality provision is absolute for return data — it does not apply to aggregate revenue statistics, enforcement policy documents, or the Department\'s operational records. Recorded tax liens and final court judgments in tax collection proceedings are public through court records systems. The Department\'s administrative records, budget documents, and policy statements are public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'income tax',
            'tax confidentiality', 'taxpayer information', 'business tax return',
            'tax audit', 'tax filing', 'return information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized taxpayer data are public',
            'Recorded tax liens and final court judgments in tax collection proceedings are public',
            'The Department of Revenue\'s operational records, audit policies, and program documents are public',
            'Challenge whether specific records constitute "tax return information" versus general regulatory correspondence',
        ]),
        'notes': 'Montana\'s tax return confidentiality is governed by § 15-30-2618 and related provisions in the Montana Code. The confidentiality protection applies to return data, not to all Department of Revenue records. Montana\'s constitutional right to know does not override this specific, clearly established statutory confidentiality protection. The Department\'s own operational records remain public.',
    },
    {
        'jurisdiction': 'MT',
        'statute_citation': 'Mont. Code Ann. § 2-6-1003(8)',
        'exemption_number': '§ 2-6-1003(8)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared by or for a government agency in connection with the prospective acquisition or sale of real property are exempt from disclosure until the transaction is complete or abandoned.',
        'scope': 'Formal real estate appraisals, property valuations, and related documents prepared in connection with a pending government acquisition or sale of real property. The exemption is temporary — it expires when the transaction closes, is abandoned, or the property is no longer being actively considered. The purpose is to prevent agencies from being disadvantaged in arm\'s-length real property negotiations if their maximum willingness to pay is disclosed before the transaction. After transaction completion, all appraisal and valuation records are fully public under Montana\'s Right to Know.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'pre-acquisition appraisal', 'real property purchase',
            'condemnation appraisal', 'eminent domain', 'land purchase',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction is complete, abandoned, or the property is no longer being actively pursued',
            'Challenge the agency\'s claim that the transaction remains "pending" if there has been no active negotiation for an extended period',
            'Appraisals for property already owned by the agency and not in active acquisition or sale mode are not covered',
            'After condemnation judgment, all valuation records are public',
            'Budget documents and legislative appropriations for property acquisition are public even when specific appraisal figures are protected',
        ]),
        'notes': 'Montana\'s real property appraisal exemption is time-limited and expires upon transaction completion. The Montana Supreme Court has held that this exemption is narrow — it protects formal appraisals, not general discussions of property value. Consistent with the constitutional right to know, all appraisal records become public once the transaction concludes.',
    },
]

# =============================================================================
# RULES
# Montana Right to Know, Mont. Const. Art. II, § 9; Mont. Code Ann. § 2-6-101 et seq.
# Key features: no specific deadline ("reasonable time"); constitutional right to know
# applies strict scrutiny to exemptions; no administrative appeal; District Court
# enforcement by petition; $0.10/page copy fee; attorney's fees for prevailing requesters.
# =============================================================================

MT_RULES = [
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline',
        'param_value': 'reasonable_time_no_specific_deadline',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006; Mont. Const. Art. II, § 9',
        'notes': 'Montana\'s Right to Know law does not establish a specific response deadline in days. Agencies must respond "in a reasonable time," which courts have interpreted based on the circumstances: the complexity of the request, the volume of records, and the agency\'s resources. There is no 5-day, 10-day, or 30-day statutory clock. This is Montana\'s most significant procedural weakness compared to other states. However, because the right to know is constitutional, unreasonable delay is itself a constitutional violation. Requesters experiencing significant delay should send a written follow-up citing the constitutional right and noting that they may petition District Court if a response is not forthcoming.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'constitutional_right_to_know',
        'param_value': 'mont_const_art_ii_sec_9',
        'day_type': None,
        'statute_citation': 'Mont. Const. Art. II, § 9',
        'notes': 'Montana\'s Right to Know is grounded in the state constitution: "No person shall be deprived of the right to examine documents or to observe the deliberations of all public bodies or agencies of state government and its subdivisions, except in cases in which the demand of individual privacy clearly exceeds the public interest." This constitutional foundation is more powerful than a purely statutory right — it creates a constitutional presumption of public access, requires strict construction of exemptions, and makes unreasonable withholding a constitutional violation. Montana courts have used this provision to strike down overbroad exemptions and to require narrow construction of all access limitations.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency_strict_scrutiny',
        'day_type': None,
        'statute_citation': 'Mont. Const. Art. II, § 9; Mont. Code Ann. § 2-6-1006',
        'notes': 'The burden of demonstrating that an exemption applies rests entirely on the agency asserting it. Because the right to know is constitutional, Montana courts apply strict scrutiny to exemption claims — the agency must demonstrate that the specific exemption is narrowly tailored and serves a compelling governmental interest. This is a higher standard than the "clearly applies" standard used in purely statutory states. Every withheld record must be individually justified. General categorical assertions of exemption are constitutionally insufficient.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_cap_per_page',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006(4)',
        'notes': 'Montana\'s copy fee cap is $0.10 per page for paper copies — among the lowest default copy rates in the United States. Agencies may not charge for staff time spent locating or reviewing records. For electronic records, actual cost of the medium or transmission applies, which is often zero for email delivery. The $0.10/page cap reflects Montana\'s strong commitment to access. Fee schedules must reflect actual reproduction costs; fees disproportionate to actual costs may constitute an unlawful barrier to the constitutional right.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fees',
        'param_value': 'not_permitted',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006(4)',
        'notes': 'Montana agencies may not charge for the staff time spent searching for, locating, or reviewing records. The $0.10/page fee covers only the actual cost of reproduction. Labor costs associated with record retrieval, review, and redaction are not chargeable to requesters. This is consistent with Montana\'s constitutional access right — allowing agencies to charge for review time would effectively price the constitutional right out of reach for many requesters.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'notes': 'Montana\'s Right to Know law does not mandate fee waivers for any specific requester category. However, agencies may waive or reduce fees at their discretion. For electronic records delivered by email, actual cost is typically zero, making fees a non-issue. Requesters should note the constitutional foundation of the right to know when requesting fee waivers — the $0.10/page cap already reflects a policy of minimizing financial barriers to the constitutional right.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'notes': 'Montana has NO formal administrative appeal mechanism for Right to Know denials. There is no agency head review, no state ombudsman, and no administrative tribunal. A requester denied access must petition the District Court for enforcement. The Attorney General\'s office does not provide a formal Right to Know appeal process. Montana\'s constitutional right to know, however, provides direct constitutional grounds for judicial relief without exhausting administrative remedies.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available_by_petition',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'notes': 'A requester denied access to records may petition the District Court for enforcement of Montana\'s Right to Know. The court conducts a de novo review and may conduct in camera inspection of withheld records. Because the right is constitutional, requesters may also assert constitutional claims directly. The court may order the agency to produce records and award attorney\'s fees and costs. Montana courts have been receptive to Right to Know enforcement petitions given the constitutional basis of the right. There is no specific statute of limitations in the Right to Know statute, but claims should be brought promptly.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'discretionary_award_available',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006(5)',
        'notes': 'A court may award reasonable attorney\'s fees and costs to a requester who substantially prevails in a Right to Know enforcement action in District Court. The award is discretionary — courts consider whether the agency\'s denial was justified and whether the requester\'s suit served the constitutional right to know. Montana courts have been willing to award fees where agencies engaged in unjustified withholding or where the denial was clearly inconsistent with the constitutional right. The constitutional basis of the access right makes fee awards more common in Montana than in purely statutory states.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Mont. Const. Art. II, § 9',
        'notes': 'Montana\'s constitutional Right to Know belongs to "any person" and agencies may not require requesters to identify themselves or state the purpose of their request. The constitutional right is not conditioned on identity, citizenship, or purpose. Anonymous requests are valid. Some agencies may ask for contact information for delivery purposes, but providing that information cannot be required as a condition of exercising the constitutional right.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Mont. Const. Art. II, § 9; Mont. Code Ann. § 2-6-1006',
        'notes': 'Montana agencies must release all nonexempt portions of records when only part of a record qualifies for a specific exemption. Blanket withholding of documents containing some exempt content violates the constitutional right to know. The agency must segregate and release all nonexempt, reasonably segregable material. Given the constitutional basis, failure to segregate is not merely a statutory violation — it is a constitutional one. Montana courts apply this requirement strictly.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_exemption_citation',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'notes': 'Montana agencies must provide a written denial specifically identifying the statutory or constitutional basis for withholding each record. A denial must cite the specific exemption provision and explain how it applies to each withheld record. Generic denials without specific justification are constitutionally insufficient given the Right to Know\'s constitutional foundation. The agency must also provide notice that the requester may petition District Court for enforcement.',
    },
    {
        'jurisdiction': 'MT',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Mont. Code Ann. § 2-6-1006',
        'notes': 'Montana\'s Right to Know encompasses electronic records. Agencies must provide records in electronic format when requested and when records exist in electronic form. The $0.10/page copy fee cap does not mean agencies can convert electronic records to paper to generate per-page charges. When records are delivered electronically (by email or download), the actual cost is typically zero. Montana\'s constitutional right to know supports broad access to records in their native format.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

MT_TEMPLATES = [
    {
        'jurisdiction': 'MT',
        'record_type': 'general',
        'template_name': 'General Montana Right to Know Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Right to Know Request — Mont. Const. Art. II, § 9; Mont. Code Ann. § 2-6-101 et seq.

Dear Custodian of Records:

Pursuant to Montana's constitutional Right to Know (Mont. Const. Art. II, § 9) and the Montana public records statutes, Mont. Code Ann. § 2-6-101 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional context:
{{additional_context}}

I request that records be provided in electronic format (via email or download link) where records exist in electronic form, at no cost or at the actual cost of the electronic medium.

I am willing to pay copying fees at the rate established by Mont. Code Ann. § 2-6-1006(4) ($0.10 per page for paper copies). I am not willing to pay for staff time spent searching for, locating, or reviewing records, which is not a permissible fee under Montana law. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Montana's constitution establishes that "no person shall be deprived of the right to examine documents" held by government agencies (Mont. Const. Art. II, § 9). This right is presumptively broad, and exceptions must be narrowly construed. The burden of demonstrating that any record is exempt from public access rests entirely on your agency, not on me.

If any records or portions of records are withheld, I request that you:
(1) identify each record withheld by description;
(2) state the specific statutory or constitutional provision under which records are being withheld (citing the precise subsection of Mont. Code Ann. § 2-6-1003 or other authority);
(3) explain specifically how the claimed exemption applies to each withheld record; and
(4) confirm that all nonexempt, reasonably segregable portions of partially withheld records have been released.

Please respond promptly. Because Montana's right to know is grounded in the state constitution, unreasonable delay is itself a constitutional violation. If I do not receive a substantive response within a reasonable time, I reserve my right to petition the District Court for enforcement under Mont. Code Ann. § 2-6-1006.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. Montana's constitutional Right to Know reflects a strong public policy in favor of government transparency. I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability consistent with the constitutional right to know.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is effectively zero, making a fee waiver consistent with both the letter and spirit of Mont. Code Ann. § 2-6-1006(4).''',
        'expedited_language': '''I request that this Right to Know request be processed as promptly as possible. Montana\'s constitutional Right to Know reflects an urgent public policy favoring government transparency. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me if there are any questions that might allow faster production.''',
        'notes': 'General-purpose Montana Right to Know template. Key MT features: (1) constitutional basis in Art. II, § 9 — cite this prominently, it creates a stronger access right than statute alone; (2) NO specific response deadline — "reasonable time" only; (3) $0.10/page copy fee cap — among the lowest in the US; (4) no administrative appeal — petition District Court directly; (5) attorney\'s fees available for prevailing requesters; (6) no search/retrieval fees permitted; (7) strict construction of exemptions because of constitutional basis. Always reference the constitutional provision, not just the statutes. Unreasonable delay is a constitutional violation.',
    },
    {
        'jurisdiction': 'MT',
        'record_type': 'law_enforcement',
        'template_name': 'Montana Right to Know Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Right to Know Request — Law Enforcement Records, Mont. Const. Art. II, § 9; Mont. Code Ann. § 2-6-101 et seq.

Dear Custodian of Records:

Pursuant to Montana's constitutional Right to Know (Mont. Const. Art. II, § 9) and Mont. Code Ann. § 2-6-101 et seq., I request copies of the following law enforcement records:

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

Regarding any claimed exemption under Mont. Code Ann. § 2-6-1003(2): Montana\'s constitutional Right to Know requires that any exemption claim be narrowly construed and specifically justified. A claim that records are exempt because they relate to "a law enforcement investigation" is constitutionally insufficient. The agency must: (1) identify the specific enumerated harm that disclosure would cause (interference with pending proceedings, revelation of informant identity, endangerment of safety, or disclosure of unique investigative techniques); and (2) demonstrate that each specific withheld record — not records of this general type — would cause that harm.

If any related prosecution has concluded or the investigation is closed, the interference rationale no longer applies, and the constitutional right to know requires disclosure of those records.

Under Mont. Code Ann. § 2-6-1006, all nonexempt, segregable portions of partially withheld records must be released.

I am willing to pay copying fees per Mont. Code Ann. § 2-6-1006(4) ($0.10/page) up to ${{fee_limit}}.

Please respond promptly. Unreasonable delay on a constitutionally protected request may be challenged by petition to the District Court.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this law enforcement records request. These records concern {{public_interest_explanation}}, a matter of constitutional accountability for government conduct. Electronic delivery incurs no reproduction cost. A fee waiver is consistent with Montana\'s constitutional commitment to public access.''',
        'expedited_language': '''I request prompt processing of this Right to Know request consistent with Montana\'s constitutional mandate. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}. Unreasonable delay in responding to a constitutionally protected request may be challenged in District Court.''',
        'notes': 'Montana law enforcement records template under the constitutional Right to Know. Key features: (1) constitutional basis in Art. II, § 9 provides stronger access right than statute alone — cite it; (2) § 2-6-1003(2) exemption requires specific harm justification, not categorical withholding; (3) arrest records and incident information are public; (4) completed investigation files are generally public; (5) no administrative appeal — District Court petition for enforcement; (6) $0.10/page fee cap; (7) strict scrutiny applied to all exemption claims given constitutional foundation.',
    },
    {
        'jurisdiction': 'MT',
        'record_type': 'government_spending',
        'template_name': 'Montana Right to Know Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Right to Know Request — Government Contracts and Expenditure Records, Mont. Const. Art. II, § 9

Dear Custodian of Records:

Pursuant to Montana\'s constitutional Right to Know (Mont. Const. Art. II, § 9) and Mont. Code Ann. § 2-6-101 et seq., I request the following records concerning public expenditures and government contracts:

{{description_of_records}}

This request includes, but is not limited to:
- All contracts, amendments, and purchase orders with {{vendor_or_contractor}} from {{date_range_start}} through {{date_range_end}}
- Payment records and invoices for the above contracts
- Procurement records including bids received, bid evaluations, and award justifications
- Correspondence between the agency and {{vendor_or_contractor}} relating to contract performance
- Any audit, review, or evaluation of contractor performance

Note on trade secret claims: Amounts paid with public funds, bid results after contract award, and government expenditure records are not protectable trade secrets under Montana law. Any claim that contract pricing or public expenditure data constitutes a trade secret must specifically demonstrate that disclosure would cause substantial competitive harm (Mont. Code Ann. § 2-6-1003(3)), not merely that the contractor designated information as "confidential." The agency must conduct an independent evaluation of any trade secret claim consistent with its constitutional obligation.

Under Mont. Const. Art. II, § 9, the presumption of public access to government records is constitutional and strong. The burden of demonstrating any exemption rests on the agency. All nonexempt, segregable portions of partially withheld records must be released.

I am willing to pay copying fees per Mont. Code Ann. § 2-6-1006(4) ($0.10/page) up to ${{fee_limit}}. Electronic delivery is preferred.

Please respond promptly consistent with the constitutional right to know.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this government spending records request. These records concern {{public_interest_explanation}}, a matter of core constitutional accountability: how government spends public money. The constitutional right to know in Art. II, § 9 is especially strong for records of public expenditures. Electronic delivery incurs no cost. A fee waiver is appropriate and consistent with the constitutional mandate.''',
        'expedited_language': '''I request prompt processing of this Right to Know request for government spending records. Montana\'s constitutional right to know requires timely access to records of how public money is spent. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Montana government spending/contracts template. Key points: (1) government expenditure records are at the core of the constitutional right to know — this is the strongest basis for access; (2) trade secret claims do not protect contract amounts or public expenditure data; (3) bid results after award are public; (4) constitutional basis means strict scrutiny applies to any exemption claim; (5) $0.10/page fee cap; (6) no administrative appeal; (7) District Court enforcement available. Government spending records are among the most clearly public records under Montana\'s constitutional framework.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in MT_EXEMPTIONS:
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

    print(f'MT exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in MT_RULES:
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

    print(f'MT rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in MT_TEMPLATES:
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

    print(f'MT templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'MT total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_mt', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
