#!/usr/bin/env python3
"""Build Rhode Island Access to Public Records Act data: exemptions, rules, and templates.

Covers Rhode Island's Access to Public Records Act (APRA), R.I.G.L. § 38-2-1 et seq.
APRA establishes a 10-business-day response deadline with a 20-business-day extension
available upon written notice. There is no administrative appeal — requesters must go
directly to Superior Court. The statute provides for attorney's fees and costs for
prevailing requesters. Copy fees are capped at $0.15/page for paper.

Run: python3 scripts/build/build_ri.py
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
# Rhode Island's APRA, R.I.G.L. § 38-2-2(4), enumerates categories of records
# that are exempt from public disclosure. The exemptions are listed in § 38-2-2(4)(A)
# through (Z) and beyond. Unlike some states, Rhode Island courts interpret APRA
# exemptions somewhat broadly, but the statute still creates a presumption of access.
# Agencies bear the burden of demonstrating that a specific exemption applies.
# =============================================================================

RI_EXEMPTIONS = [
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(A)',
        'exemption_number': '§ 38-2-2(4)(A)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, impressions, memoranda, working papers, and work products, including those used in the deliberative process, are exempt from APRA if they are developed for deliberative purposes and have not been adopted as official agency policy.',
        'scope': 'Covers predecisional documents including drafts, notes, working papers, and memoranda generated as part of an agency\'s internal deliberative process. The exemption applies only to documents that are truly predecisional and deliberative — meaning they reflect the give-and-take of the deliberative process, not purely factual information. Once a draft is adopted as agency policy or an official agency decision, the deliberative process protection disappears. Factual material within deliberative documents must be segregated and released. Rhode Island courts have held that the exemption does not protect purely factual summaries or data compilations, even if they were prepared to inform a decision.',
        'key_terms': json.dumps([
            'preliminary draft', 'working paper', 'deliberative process', 'predecisional',
            'intra-agency memorandum', 'draft document', 'work product', 'advisory opinion',
            'policy deliberation', 'deliberative privilege', 'recommendation',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released — the exemption covers only opinion and deliberative portions',
            'Once a draft, recommendation, or working paper is adopted as agency policy or final decision, the exemption no longer applies',
            'Challenge claims that entire documents are deliberative where only isolated recommendation sections qualify — segregation is required',
            'Documents shared outside the agency or with persons not involved in the deliberative process may lose their predecisional character',
            'The agency must demonstrate that the specific document is both predecisional and deliberative — a generic "working paper" label is insufficient',
            'Final agency decisions, regulations, and "working law" standards agencies actually apply must be disclosed regardless of internal deliberative character',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(A) is Rhode Island\'s codified deliberative process exemption. Rhode Island courts have interpreted this provision to require that the document be both predecisional (produced before a final agency decision) and deliberative (reflect the agency\'s reasoning process). The factual/deliberative distinction is critical. See Hydron Laboratories, Inc. v. Dep\'t of Attorney General, 492 A.2d 135 (R.I. 1985) for the foundational analysis.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(B)',
        'exemption_number': '§ 38-2-2(4)(B)',
        'short_name': 'Personnel and Employment Records',
        'category': 'privacy',
        'description': 'Personnel files and other records related to a government employee\'s employment, including applications, promotions, disciplinary records, and performance evaluations, are generally exempt from public disclosure to the extent they would constitute a clearly unwarranted invasion of personal privacy.',
        'scope': 'Personnel files, employment applications, performance evaluations, disciplinary records, and related employment documents for government employees. The exemption is not absolute — information about a public employee\'s conduct in their public capacity, compensation, disciplinary actions that resulted in termination or suspension, and records relevant to the exercise of public duties are generally public. The exemption protects highly personal information like medical records, home addresses, personal financial disclosures, and details of minor disciplinary matters. Rhode Island courts balance the employee\'s privacy interest against the public\'s interest in government accountability.',
        'key_terms': json.dumps([
            'personnel file', 'employment record', 'performance evaluation', 'disciplinary record',
            'government employee', 'personal privacy', 'public employee', 'HR records',
            'employment application', 'termination record', 'suspension record',
        ]),
        'counter_arguments': json.dumps([
            'Compensation, salary, and benefits information for public employees is public — this is core government accountability information',
            'Disciplinary actions resulting in suspension, demotion, or termination are matters of public record',
            'Records of employee conduct in their official capacity and in the exercise of public duties are not protected by the personnel file exemption',
            'Policies, procedures, and directives that employees are required to follow are public regardless of their location in personnel systems',
            'Challenge blanket withholding of personnel files — the agency must identify which specific portions qualify for the privacy exemption',
            'Information about disciplinary proceedings that have been finalized and resulted in public action is not exempt',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(B) reflects the balance between government employee privacy and public accountability. Rhode Island\'s Supreme Court has recognized that public employees have reduced privacy expectations regarding their conduct in office. Salary and compensation records are uniformly public under APRA. The exemption is most clearly applicable to genuinely personal information like home addresses, medical conditions, and personal financial matters unrelated to government employment.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(C)',
        'exemption_number': '§ 38-2-2(4)(C)',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information obtained from a person or entity which is of a privileged or confidential nature, and which if disclosed would give economic advantage to competitors or cause substantial harm to the competitive position of the source, are exempt from public disclosure.',
        'scope': 'Information submitted to government agencies by private entities that constitutes a trade secret or confidential commercial or financial information. The exemption requires that the information: (1) be commercial or financial in nature; (2) have been obtained from a private person or entity; (3) be privileged or confidential in character; and (4) if disclosed, would cause substantial competitive harm. Amounts paid under government contracts, bid prices after award, and information about government expenditures are generally public. The agency may not simply accept a vendor\'s confidentiality designation — it must make an independent determination that the information qualifies.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'commercial advantage',
            'business confidential', 'competitive position', 'economic advantage',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate actual competitive harm from disclosure, not merely assert that information is "confidential"',
            'Contract amounts, bid results after award, and public expenditure data are not protectable as trade secrets',
            'Information that has been disclosed elsewhere (in patent applications, published filings, or other public documents) cannot be withheld as a trade secret',
            'Government-generated records cannot constitute trade secrets — only privately submitted information can qualify',
            'The agency bears the burden of independently evaluating trade secret claims rather than simply deferring to vendor designations',
            'Challenge overbroad redactions where the agency has withheld entire documents when only narrow technical specifications might qualify',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(C) applies a competitive harm standard similar to Exemption 4 of the federal FOIA. Rhode Island agencies must make an independent evaluation of claimed trade secrets and may not simply accept a vendor\'s designation. Contract amounts paid with public funds are uniformly public. The burden of demonstrating competitive harm rests on the party seeking protection, but the agency must independently evaluate the claim.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(D)',
        'exemption_number': '§ 38-2-2(4)(D)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Law enforcement records, including records of criminal investigations, that are compiled for law enforcement purposes are exempt where disclosure could reasonably be expected to interfere with enforcement proceedings, deprive a person of a fair trial, reveal the identity of a confidential informant, endanger life or physical safety, or disclose investigative techniques.',
        'scope': 'Records compiled by law enforcement agencies in the course of criminal investigations, including incident reports, investigative files, interview records, surveillance records, and evidence logs. The exemption requires a specific articulable harm from disclosure — not merely that records are part of an investigation. Rhode Island courts have held that the exemption does not protect completed investigation files once prosecution has concluded. Factual information in investigative files that does not reveal informants, investigative techniques, or create safety risks must be released. Arrest records, booking data, and records of the existence and nature of an incident are generally public.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'pending investigation', 'ongoing investigation',
            'enforcement proceeding', 'fair trial', 'endangerment', 'investigative file',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a specific articulable harm from disclosure, not merely an assertion that records are part of an investigation',
            'Arrest records, booking information, and basic incident reports documenting the occurrence and nature of an incident are generally public',
            'Once prosecution concludes or investigation closes without charges, the interference rationale disappears and records generally become public',
            'Factual information in investigative files that does not reveal informants, techniques, or create safety risks must be segregated and released',
            'Challenge claims that disclosure would "reveal investigative techniques" where the technique described is standard, widely known police procedure',
            'The agency must identify with specificity which harm applies to each withheld record — a generic "investigation ongoing" response is insufficient',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(D) is Rhode Island\'s law enforcement investigative records exemption. It mirrors the structure of federal FOIA Exemption 7 but applies to state and local law enforcement. Rhode Island courts have been relatively consistent in requiring specific harm justification for withholding, particularly for closed investigations. Incident reports and arrest records are among the most commonly requested public records in Rhode Island, and agencies may not use this exemption to shield them from disclosure.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(I)',
        'exemption_number': '§ 38-2-2(4)(I)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records that are subject to the attorney-client privilege or work product doctrine are exempt from disclosure under APRA. The exemption tracks the common-law privilege as applied to government attorneys representing state and municipal agencies.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation or in the course of ongoing legal proceedings. The privilege requires that the communication be: (1) between attorney and client; (2) for the purpose of obtaining legal advice; (3) made in confidence; and (4) not waived through disclosure. Billing records, engagement letters, and financial arrangements with outside counsel are not generally privileged. Facts independently known to the agency are not protected merely because they were communicated to an attorney. The privilege belongs to the agency and may be waived.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation privilege',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'confidential communication', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'Communications must be for the purpose of obtaining legal advice, not general business or policy guidance — the latter is not privileged',
            'Waiver occurs when the agency discloses the substance in public proceedings, to non-attorney personnel not in the attorney-client relationship, or to third parties',
            'Attorney billing records and invoices are generally public, even if detailed legal work descriptions might be redacted',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and mental impressions are protected',
            'The privilege belongs to the agency, which may waive it — challenge whether the agency has constructively waived by relying on the advice in public decisions',
            'Challenge whether communications labeled as "legal advice" are in fact policy or business guidance from in-house counsel who also performs non-legal functions',
        ]),
        'notes': 'Rhode Island recognizes the attorney-client privilege and work product doctrine for government entities under R.I.G.L. § 38-2-2(4)(I). The privilege is the same as that applicable to private parties, but courts are sensitive to the risk that government agencies will use privilege claims to shield embarrassing but non-privileged communications. Rhode Island courts apply the privilege with reference to its purpose: protecting the candid attorney-client relationship, not shielding government operations from public scrutiny.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(P)',
        'exemption_number': '§ 38-2-2(4)(P)',
        'short_name': 'Medical, Psychiatric, and Psychological Records',
        'category': 'privacy',
        'description': 'Records, reports, opinions, information, and statements required to be kept confidential pursuant to the medical records statutes, psychiatric and psychological records statutes, and similar health information confidentiality provisions are exempt from public disclosure.',
        'scope': 'Medical records, psychiatric and psychological records, treatment records, and health information pertaining to identifiable individuals, whether held by health departments, correctional facilities, public hospitals, or other state agencies. The exemption is broad and covers any health information that identifies a specific individual. Aggregate health statistics, anonymized epidemiological data, and public health program information are generally public. The exemption applies to records of public employees held in their capacity as patients, not in their capacity as employees.',
        'key_terms': json.dumps([
            'medical records', 'psychiatric records', 'psychological records', 'health information',
            'patient records', 'treatment records', 'HIPAA', 'health confidentiality',
            'medical privacy', 'mental health records', 'identifiable health information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics, anonymized data, and public health program information are not covered by this exemption',
            'Records of a public employee\'s conduct at work, including drug test results in some administrative proceedings, may be available notwithstanding the medical records exemption',
            'Challenge claims that operational health and safety records (inspection reports, facility compliance records) are protected as "medical records"',
            'Administrative records of a health agency (budget, staffing, contracts) are fully public regardless of this exemption',
            'Where a public official\'s medical condition is directly relevant to their capacity to perform public duties, the balance may favor disclosure',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(P) incorporates Rhode Island\'s medical confidentiality statutes into APRA\'s exemption framework. Rhode Island has strong medical privacy protections consistent with HIPAA. The exemption is most clearly applicable to individually identifiable health records. Program-level health information, aggregate data, and public health policy documents are public regardless of their location in health agency systems.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(A)(i)',
        'exemption_number': '§ 38-2-2(4)(A)(i)',
        'short_name': 'Security Plans for Public Infrastructure',
        'category': 'safety',
        'description': 'Records, the disclosure of which would constitute a serious threat to the security of any building, structure, or facility, or any system for the protection thereof, including cyber security plans and critical infrastructure assessments, are exempt from public disclosure.',
        'scope': 'Security plans, vulnerability assessments, intrusion detection system configurations, access control system details, and similar operational security documents where disclosure would create a specific, articulable threat to the security of public buildings or critical infrastructure. The exemption is narrowly targeted — it does not cover all security-related records, only those whose disclosure would directly enable a security breach. Budget records, expenditure data, and general descriptions of security programs are public. Agencies must demonstrate that the specific information in the withheld record would enable a specific harm.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security threat', 'access control', 'cyber security', 'infrastructure protection',
            'facility security', 'intrusion detection', 'security breach',
        ]),
        'counter_arguments': json.dumps([
            'The threat must be specific and articulable — a general assertion that records relate to "security" is insufficient',
            'Budget and expenditure records for security programs are public regardless of this exemption',
            'General descriptions of security policies and procedures that do not reveal specific vulnerabilities are not covered',
            'Challenge claims that entire contracts with security vendors are exempt when only narrow technical specifications warrant protection',
            'Security audits that identify systemic problems, if disclosed only in aggregate form without specific vulnerability details, may be subject to partial disclosure',
        ]),
        'notes': 'Rhode Island\'s security infrastructure exemption in APRA requires a specific connection between disclosure and a concrete security threat. Agencies may not claim this exemption for all security-related records — only for those specific records whose disclosure would directly enable a security breach. The exemption reflects the post-9/11 trend of protecting critical infrastructure information from public disclosure, but Rhode Island courts require specificity in the claimed harm.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(B)(ii)',
        'exemption_number': '§ 38-2-2(4)(B)(ii)',
        'short_name': 'Test Questions and Examination Materials',
        'category': 'commercial',
        'description': 'Test questions, scoring keys, and other examination data used to administer a licensing examination, academic examination, or employment examination are exempt from public disclosure to preserve the integrity and validity of the examinations.',
        'scope': 'Questions, scoring keys, model answers, rubrics, and examination materials used in licensing examinations, civil service examinations, academic assessments, and similar standardized tests administered by or on behalf of government agencies. The exemption applies prospectively — questions used in past examinations that will not be reused may lose protection. Aggregate examination results, pass/fail rates, and statistical analyses of examination performance are generally public. The exemption does not cover policies governing the examination process, scoring methodology in general terms, or administrative records about the examination program.',
        'key_terms': json.dumps([
            'test questions', 'examination materials', 'scoring key', 'licensing examination',
            'civil service examination', 'academic examination', 'employment test',
            'examination integrity', 'standardized test', 'answer key',
        ]),
        'counter_arguments': json.dumps([
            'Examination questions from past administrations that will not be reused are generally public once the examination cycle closes',
            'Aggregate pass/fail rates, score distributions, and statistical summaries of examination results are public',
            'Challenge whether general information about examination structure, content areas, and format is truly "examination data" warranting protection',
            'Examination scoring policies, grading criteria in general terms, and appeals procedures are public regardless of this exemption',
            'Examination results for specific individuals in licensing proceedings may be discoverable in administrative appeals',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(B)(ii) protects the integrity of government-administered examinations by preventing examinees from obtaining advance access to questions. The exemption is time-limited in practical effect — examination questions that are no longer in use for active administrations generally lose protection. Rhode Island agencies administering professional licensing examinations rely on this exemption to protect examination security.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(G)',
        'exemption_number': '§ 38-2-2(4)(G)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals, feasibility studies, and related valuation documents prepared by or for a government agency in connection with the prospective acquisition or sale of real property are exempt from public disclosure until the transaction is complete or abandoned.',
        'scope': 'Formal real estate appraisals, property valuations, feasibility studies, and related documents prepared in connection with a pending government acquisition or sale of real property. The exemption is temporary — it expires automatically when the transaction is complete, abandoned, or the property is no longer being actively considered for acquisition. The purpose is to prevent agencies from being disadvantaged in arm\'s-length negotiations if their maximum willingness to pay is disclosed pre-purchase. After transaction completion, all appraisal records are public. Budget estimates and general appropriation records are not protected merely because a property transaction is contemplated.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'feasibility study', 'pre-acquisition appraisal',
            'real property purchase', 'condemnation appraisal', 'eminent domain',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, abandoned, or the property is no longer being actively pursued',
            'Challenge the agency\'s claim that the transaction remains "pending" if there has been no active negotiation or legislative action for an extended period',
            'Appraisals for property already owned by the agency and not in active acquisition or sale mode are not covered',
            'Post-condemnation judgment, all valuation records are public regardless of this exemption',
            'Budget documents and legislative appropriations for property acquisition are public even when specific appraisal figures are protected',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(G) is a well-established, time-limited exemption in Rhode Island APRA practice. The exemption automatically expires upon transaction completion. Rhode Island courts have held that the exemption is narrowly limited to formal valuation documents — general discussions of property value in budget documents or legislative testimony do not qualify.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(E)',
        'exemption_number': '§ 38-2-2(4)(E)',
        'short_name': 'Tax Records — Individual and Business Returns',
        'category': 'privacy',
        'description': 'Individual and business tax returns and related tax information in the possession of the Rhode Island Division of Taxation and other tax collection agencies are exempt from public disclosure under APRA as well as under the state\'s tax confidentiality statutes.',
        'scope': 'Individual income tax returns, business and corporate tax returns, sales tax returns, and related return information submitted to or generated by the Rhode Island Division of Taxation in connection with tax collection, audit, and enforcement. The exemption applies to the specific return data — not to aggregate tax revenue statistics, policy documents, or the Division\'s operational records. Final court judgments in tax collection proceedings and recorded tax liens are public. The Division\'s enforcement statistics, audit policies, and program documents are public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Division of Taxation', 'income tax',
            'business tax return', 'tax confidentiality', 'taxpayer information',
            'tax audit', 'sales tax return', 'tax filing',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized taxpayer data are public',
            'Recorded tax liens, final tax court judgments, and public enforcement actions are accessible through court records systems',
            'The Division of Taxation\'s own operational records, budget documents, and policy statements are public',
            'Challenge whether the specific records requested constitute "tax return information" versus general regulatory correspondence or enforcement records',
        ]),
        'notes': 'Rhode Island\'s tax return confidentiality is among the most clearly established APRA exemptions, reinforced by separate statutory provisions governing the Division of Taxation. The exemption applies to return data, not to all Division of Taxation records. The Division\'s operational records, including enforcement statistics, audit program descriptions, and policy documents, are public under APRA.',
    },
    {
        'jurisdiction': 'RI',
        'statute_citation': 'R.I.G.L. § 38-2-2(4)(N)',
        'exemption_number': '§ 38-2-2(4)(N)',
        'short_name': 'Library Records — Patron Privacy',
        'category': 'privacy',
        'description': 'Library circulation records and other records that identify what library materials a specific patron has requested, accessed, or borrowed are exempt from public disclosure to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying which specific library patrons requested, accessed, borrowed, or inquired about library materials, databases, or electronic resources at public libraries and academic libraries at public institutions. Covers physical circulation records, electronic database access logs, interlibrary loan records, and reference inquiries that reveal the reading interests of identifiable individuals. Aggregate statistics about library usage, collection data, and general program information are public. Library administrative records, budget documents, and personnel files are public. The protection extends to digital resource access logs.',
        'key_terms': json.dumps([
            'library records', 'circulation records', 'library patron', 'borrower records',
            'database access', 'intellectual privacy', 'reading privacy', 'interlibrary loan',
            'library privacy', 'patron confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library usage statistics, collection data, and total circulation counts are not covered',
            'Library administrative records, contracts, budget documents, and personnel files are fully public',
            'Records subpoenaed pursuant to court order in a criminal investigation may be disclosed consistent with the court order',
            'The exemption covers patron-specific reading records, not library operations, programming, or system administration',
        ]),
        'notes': 'R.I.G.L. § 38-2-2(4)(N) reflects Rhode Island\'s strong commitment to protecting the intellectual privacy of library patrons. The exemption is absolute for patron-specific reading data — there is no balancing test. Rhode Island\'s library privacy protection is consistent with similar provisions in most states and reflects the principle that individuals should be able to access information without fear of government surveillance.',
    },
]

# =============================================================================
# RULES
# Rhode Island Access to Public Records Act, R.I.G.L. § 38-2-1 et seq.
# Key features: 10-business-day initial response deadline; 20-business-day
# extension with written notice; no administrative appeal (direct to Superior
# Court); $0.15/page copy fee cap; attorney's fees for prevailing requesters.
# =============================================================================

RI_RULES = [
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'R.I.G.L. § 38-2-3(e)',
        'notes': 'Rhode Island agencies must respond to APRA requests within 10 business days of receipt. The response must either provide the requested records, deny the request with specific legal justification, or notify the requester that an extension is being taken. A failure to respond within 10 business days constitutes a constructive denial that the requester may challenge in Superior Court. The 10-business-day clock begins on the day the request is received by the agency.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'extension_days',
        'param_value': '20',
        'day_type': 'business',
        'statute_citation': 'R.I.G.L. § 38-2-3(e)',
        'notes': 'Rhode Island agencies may extend the response deadline by up to 20 additional business days (30 business days total from receipt) upon written notice to the requester. The extension notice must state that the request is being reviewed, that additional time is needed, and that the requester may appeal the constructive denial to Superior Court after 10 business days if they believe the extension is improper. An extension without written notice is not valid. The agency must respond substantively within the extended period — a second extension is not available under the statute.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_statutory_citation',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-7',
        'notes': 'When denying access to records under APRA, Rhode Island agencies must provide a written denial that specifies the specific statutory exemption under which records are being withheld (citing the specific subsection of R.I.G.L. § 38-2-2(4)), and must advise the requester of the right to appeal the denial to Superior Court. A blanket denial without specific statutory citation is legally insufficient and may constitute an independent violation. The agency must also inform the requester that they may seek judicial review in Providence County Superior Court.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-3(b)',
        'notes': 'Rhode Island agencies must release all nonexempt portions of records when only part of a record qualifies for an exemption under APRA. The agency must redact exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is a violation of APRA. The agency must segregate and release all reasonably segregable nonexempt material. The agency\'s denial must specifically identify which portions of each record are being withheld and under what statutory authority.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-3(a)',
        'notes': 'Rhode Island\'s APRA grants the right to inspect and copy public records to "any person." Agencies may not require requesters to identify themselves or state the purpose of their request as a condition of access. Anonymous requests are valid. Some agencies may ask for contact information for delivery purposes, but providing that information must be voluntary and cannot be required. The "any person" standard includes out-of-state residents, non-citizens, and corporations.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-3(b)',
        'notes': 'The burden of demonstrating that any record is exempt from public access under APRA rests on the public body asserting the exemption, not on the requester. The agency must affirmatively demonstrate that a specific enumerated exemption in R.I.G.L. § 38-2-2(4) applies to each specific withheld record or portion of a record. General assertions that records fall within broad exemption categories are insufficient. The agency must specifically identify the harm that disclosure would cause and connect that harm to the specific language of the claimed exemption.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_cap_per_page',
        'param_value': '0.15',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-4',
        'notes': 'Rhode Island\'s APRA caps copy fees at $0.15 per page for paper copies. This is among the more clearly specified fee caps in New England public records law. Agencies may not charge for staff time spent locating, reviewing, or redacting records. For electronic records, fees may only cover the actual cost of the medium or transmission. Many agencies provide electronic records at no cost when delivered by email. Agencies may require advance payment of copying fees for large requests.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'fee_cap',
        'param_key': 'search_and_retrieval_fees',
        'param_value': 'not_permitted',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-4',
        'notes': 'Rhode Island agencies may not charge for the staff time spent searching for, locating, or reviewing records in response to an APRA request. The fee cap of $0.15 per page covers only the actual cost of reproduction. Agencies may not add surcharges for attorney review time, supervisory review, or administrative handling. A fee assessment that includes anything beyond the per-page reproduction cost may be challenged as an unlawful barrier to APRA access.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_public_interest',
        'param_value': 'available_by_agency_discretion',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-4',
        'notes': 'Rhode Island\'s APRA does not mandate fee waivers for any specific requester category, but agencies may waive or reduce fees at their discretion. Media organizations, nonprofit entities, and academic researchers commonly receive fee waivers in practice. For electronic records delivered by email, actual reproduction cost is often zero, effectively mooting the fee question. Requesters should affirmatively request a fee waiver and explain the public interest basis for the request.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-8',
        'notes': 'Rhode Island has NO formal administrative appeal mechanism for APRA denials. There is no agency head review process, no state attorney general review, and no administrative tribunal. A requester who receives an improper denial or constructive denial must go directly to Superior Court. The Attorney General\'s office may investigate APRA compliance upon complaint, but this is not a formal appeal mechanism and does not provide binding relief on a specific request. Requesters have a right to complain to the AG\'s office, which can issue non-binding advisory opinions.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available_providence_county',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-8',
        'notes': 'A requester may seek judicial enforcement of APRA in Providence County Superior Court. The court conducts a de novo review and may conduct in camera inspection of withheld records. If the court finds that the agency improperly denied access, it may order the agency to produce records and award attorney\'s fees and costs to the prevailing requester. There is a one-year statute of limitations for filing an APRA appeal in Superior Court, running from the date of the denial or constructive denial.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_for_prevailing_requester',
        'param_value': 'discretionary_award_available',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-9',
        'notes': 'A court may award reasonable attorney\'s fees and litigation costs to a requester who substantially prevails in an APRA enforcement action in Superior Court. Unlike Washington\'s mandatory fee-shifting, Rhode Island\'s attorney\'s fee award is discretionary — the court considers whether the agency\'s denial was justified and whether the requester\'s suit served the public interest. Courts have been willing to award fees where agencies engaged in a pattern of withholding without adequate justification or where disclosure was clearly required by the statute.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'penalty',
        'param_key': 'civil_fine_willful_violation',
        'param_value': 'up_to_2000_per_violation',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-9',
        'notes': 'Rhode Island\'s APRA provides for civil fines of up to $2,000 per violation for willful or knowing violations of the Act. The fine is assessed against the public body, not the individual officer. Courts have awarded fines where agencies denied access in bad faith, engaged in pattern violations, or willfully withheld clearly public records. A fine requires a showing of willful or knowing conduct — negligent or good-faith mistakes generally do not qualify. The fine is in addition to any attorney\'s fees award.',
    },
    {
        'jurisdiction': 'RI',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_accessible',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'R.I.G.L. § 38-2-3(h)',
        'notes': 'Rhode Island agencies must provide records in electronic format when requested and when records exist in electronic form. Agencies may not require requesters to accept paper copies when electronic records exist and electronic delivery is feasible. The right to electronic records is subject to the same $0.15/page fee cap in paper equivalent terms, though many agencies provide electronic records at no charge when delivered by email. Agencies may not convert electronic records to paper format and then charge paper copy fees as a way of increasing cost.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

RI_TEMPLATES = [
    {
        'jurisdiction': 'RI',
        'record_type': 'general',
        'template_name': 'General Rhode Island APRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer (or Custodian of Records)
{{agency_name}}
{{agency_address}}

Re: Access to Public Records Act Request — R.I.G.L. § 38-2-1 et seq.

Dear Public Records Officer:

Pursuant to the Rhode Island Access to Public Records Act (APRA), R.I.G.L. § 38-2-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional context:
{{additional_context}}

I request that records be provided in electronic format (via email or download link) where available and where the records exist in electronic form, consistent with R.I.G.L. § 38-2-3(h). Electronic delivery minimizes both cost and production time.

I am willing to pay copying fees at the rate established by R.I.G.L. § 38-2-4 ($0.15 per page for paper, or actual cost for electronic media). I am not willing to pay for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under APRA. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under R.I.G.L. § 38-2-3(b), the burden of demonstrating that any record is exempt from public access rests entirely on your agency. If any records or portions of records are withheld, I request that you:
(1) identify each record withheld by description;
(2) state the specific statutory basis for withholding, citing the precise subsection of R.I.G.L. § 38-2-2(4) that applies;
(3) confirm that all nonexempt, reasonably segregable portions of partially withheld records have been released; and
(4) inform me of my right to seek judicial review in Superior Court under R.I.G.L. § 38-2-8.

Under R.I.G.L. § 38-2-3(e), you must respond to this request within 10 business days of receipt. If additional time is needed, please provide written notice of an extension consistent with the statute. Failure to respond within 10 business days constitutes a constructive denial that I may challenge in Superior Court.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Rhode Island\'s APRA does not mandate fee waivers, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is effectively zero, making a fee waiver consistent with both the letter and spirit of R.I.G.L. § 38-2-4.

I appreciate your consideration of this fee waiver request.''',
        'expedited_language': '''I request that this APRA request be processed as expeditiously as possible within the statutory deadline. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that might allow faster production.''',
        'notes': 'General-purpose Rhode Island APRA template. Key RI features: (1) 10-business-day response deadline — cite R.I.G.L. § 38-2-3(e); (2) 20-business-day extension available with written notice; (3) no administrative appeal — go directly to Superior Court in Providence County under R.I.G.L. § 38-2-8; (4) $0.15/page copy fee cap — cite R.I.G.L. § 38-2-4; (5) no search/retrieval fees permitted; (6) attorney\'s fees available for prevailing requesters; (7) civil fine up to $2,000 for willful violations. Reference "APRA" or "Access to Public Records Act," not "FOIA." Statute of limitations for court appeal is one year from denial.',
    },
    {
        'jurisdiction': 'RI',
        'record_type': 'law_enforcement',
        'template_name': 'Rhode Island APRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Access to Public Records Act Request — Law Enforcement Records, R.I.G.L. § 38-2-1 et seq.

Dear Public Records Officer:

Pursuant to the Rhode Island Access to Public Records Act (APRA), R.I.G.L. § 38-2-1 et seq., I request copies of the following law enforcement records:

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
- Written communications (email, text, radio logs) relating to the above
- Officer disciplinary records for involved personnel
- Internal affairs investigation records relating to the above incident

Regarding claimed exemptions under R.I.G.L. § 38-2-2(4)(D): Rhode Island law does not permit blanket withholding of law enforcement records. Any withholding under the law enforcement investigative records exemption requires: (1) identification of the specific harm that disclosure would cause (e.g., interference with pending proceedings, revelation of informant identity, endangerment of safety, disclosure of investigative techniques); and (2) a specific connection between that harm and each particular withheld record — not records of this general type.

If any related criminal prosecution has concluded or if the investigation is closed, please note that the interference rationale no longer applies to records of completed matters.

Under R.I.G.L. § 38-2-3(b), the burden of demonstrating any exemption rests on your agency. Under R.I.G.L. § 38-2-3(b), all nonexempt, segregable portions of partially withheld records must be released.

I am willing to pay copying fees per R.I.G.L. § 38-2-4 up to ${{fee_limit}}. Please respond within 10 business days per R.I.G.L. § 38-2-3(e).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this law enforcement records request. These records concern {{public_interest_explanation}}, a matter of public accountability for government conduct. Electronic delivery incurs no reproduction cost. I appreciate your consideration of a fee waiver.''',
        'expedited_language': '''I request expedited processing within the statutory 10-business-day deadline. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Rhode Island law enforcement records template under APRA. Key RI law enforcement records features: (1) R.I.G.L. § 38-2-2(4)(D) exemption requires specific harm justification for each withheld record — not categorical withholding; (2) completed investigation files are generally public once prosecution concludes; (3) arrest records and incident reports documenting the existence and nature of an incident are public; (4) body-worn camera footage is a public record absent a specific enumerated harm; (5) no administrative appeal — Superior Court is the enforcement forum; (6) attorney\'s fees available for prevailing requesters; (7) 10-business-day initial deadline with 20-business-day extension option.',
    },
    {
        'jurisdiction': 'RI',
        'record_type': 'personnel',
        'template_name': 'Rhode Island APRA Request — Public Employee Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Access to Public Records Act Request — Public Employee Records, R.I.G.L. § 38-2-1 et seq.

Dear Public Records Officer:

Pursuant to the Rhode Island Access to Public Records Act (APRA), R.I.G.L. § 38-2-1 et seq., I request the following records relating to {{employee_name_or_description}} ({{employee_title_or_position}}):

{{description_of_records}}

This request includes, but is not limited to, the following categories of records to the extent they exist and are not covered by a specific statutory exemption:
- Compensation records, including salary, benefits, overtime, and bonus payments
- Employment contract and terms of employment (if applicable)
- Job title and classification
- Records of disciplinary action, including suspensions, demotions, and terminations
- Records of official conduct in the employee\'s public capacity
- Employment dates, appointment history, and position changes

Note on the personnel file exemption: Rhode Island law recognizes a limited personnel file exemption under R.I.G.L. § 38-2-2(4)(B). However, this exemption does not protect: (1) compensation and salary information; (2) disciplinary actions resulting in suspension, demotion, or termination; (3) records of official conduct in the employee\'s public capacity; or (4) policies and directives the employee is required to follow. The agency must segregate and release these non-exempt portions and provide a specific statutory citation for any material that is withheld.

Under R.I.G.L. § 38-2-3(b), the burden of demonstrating any exemption rests on your agency. Please respond within 10 business days per R.I.G.L. § 38-2-3(e).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request concerning public employee records. This request relates to {{public_interest_explanation}}, a matter of public accountability regarding the use of government resources and public trust. Electronic delivery would be at no cost. I appreciate your consideration.''',
        'expedited_language': '''I request that this request be processed promptly within the 10-business-day statutory deadline. This request is time-sensitive because: {{expedited_justification}}.''',
        'notes': 'Rhode Island public employee records template under APRA. Key points: (1) salary and compensation are always public — agencies cannot use the personnel file exemption to shield them; (2) disciplinary actions resulting in serious consequences are public; (3) records of official conduct are public regardless of their location in personnel systems; (4) the exemption in § 38-2-2(4)(B) protects only genuinely personal information (home address, medical, minor disciplinary matters); (5) 10-business-day response deadline; (6) no administrative appeal — Superior Court is the enforcement forum.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in RI_EXEMPTIONS:
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

    print(f'RI exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in RI_RULES:
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

    print(f'RI rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in RI_TEMPLATES:
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

    print(f'RI templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'RI total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ri', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
