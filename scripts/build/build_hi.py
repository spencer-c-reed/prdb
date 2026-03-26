#!/usr/bin/env python3
"""Build Hawaii Uniform Information Practices Act data: exemptions, rules, and templates.

Covers Hawaii's Uniform Information Practices Act (UIPA), HRS Ch. 92F.
Hawaii is distinctive in several ways: (1) the Office of Information Practices (OIP)
provides advisory opinions that are influential though not binding; (2) UIPA includes
a personal records access right analogous to the federal Privacy Act, allowing
individuals to access and correct records about themselves; (3) the copy fee ($0.05/page)
is among the lowest in the country; (4) there is no attorney's fees provision, making
litigation costly; and (5) the OIP advisory process is typically the primary dispute
resolution mechanism before any court action.

Run: python3 scripts/build/build_hi.py
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
# HRS § 92F-13 lists the categories of government records exempt from mandatory
# disclosure. Hawaii courts and the OIP construe exemptions narrowly. The burden
# of demonstrating an exemption is on the agency. HRS § 92F-14 provides a
# separate framework for records whose disclosure would constitute a clearly
# unwarranted invasion of personal privacy — applying a balancing test.
# =============================================================================

HI_EXEMPTIONS = [
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(1)',
        'exemption_number': '§ 92F-13(1)',
        'short_name': 'Government Records Whose Disclosure Would Frustrate Government Function',
        'category': 'deliberative',
        'description': 'Government records that, if disclosed, would frustrate a legitimate government function are exempt from mandatory disclosure. This is a functional harm test — the agency must demonstrate that the specific disclosure would frustrate a specific governmental interest.',
        'scope': 'Records whose disclosure would frustrate a legitimate government function: (1) compromise ongoing law enforcement investigations; (2) reveal confidential informants; (3) undermine agency deliberative functions by chilling candid policy debate (applies only to predecisional deliberative documents, not factual records); (4) interfere with pending legal proceedings. The exemption requires a showing of specific harm — not a generalized assertion that government functions might be affected. Factual portions of deliberative documents are not covered. Once a government function concludes (investigation complete, litigation resolved), the frustration rationale dissolves.',
        'key_terms': json.dumps([
            'government function', 'frustrate function', 'deliberative process',
            'law enforcement investigation', 'confidential informant',
            'predecisional document', 'ongoing investigation', 'legal proceedings',
        ]),
        'counter_arguments': json.dumps([
            'The agency must demonstrate a specific harm to a specific government function, not make a general assertion',
            'Completed investigations, concluded proceedings, and adopted policies are not covered',
            'Factual portions of deliberative documents must be segregated and released',
            '"Working law" — the standards and criteria the agency applies in practice — must be disclosed',
            'Challenge claims that releasing records would "frustrate" functions where the function has already concluded',
            'The OIP has consistently required agencies to articulate the specific function that would be frustrated',
        ]),
        'notes': 'HRS § 92F-13(1) is UIPA\'s primary multi-purpose exemption. The OIP has issued numerous advisory opinions applying a functional harm test. See OIP Op. Ltr. No. 94-25 and related opinions on the deliberative process. The narrow construction principle — expressed throughout UIPA — applies with full force here.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(2)',
        'exemption_number': '§ 92F-13(2)',
        'short_name': 'Law Enforcement — Specific Harms',
        'category': 'law_enforcement',
        'description': 'Government records relating to law enforcement investigations where disclosure would: (a) endanger the safety of persons; (b) prevent the apprehension of a suspect; (c) interfere with pending prosecution; or (d) identify a confidential informant.',
        'scope': 'Law enforcement records in active investigations where disclosure would cause one of four enumerated harms. The harms are specific, not categorical — the agency must connect each withheld record to an identified harm. Completed investigations do not retain this protection. Incident reports documenting the existence of events, arrest records, and booking information are generally public. Body camera footage is a law enforcement record subject to this specific harm analysis. The agency must show that disclosure of each specific record would cause a specific identified harm, not that the records are generally investigative in nature.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'endanger safety', 'prevent apprehension', 'interfere with prosecution',
            'ongoing investigation', 'active investigation', 'arrest record',
        ]),
        'counter_arguments': json.dumps([
            'Each withheld record must be tied to a specific enumerated harm — generic "investigation ongoing" claims are insufficient',
            'Completed investigations do not retain this protection',
            'Arrest records, booking information, and incident reports are generally public',
            'Factual information not revealing informants or investigative techniques must be released',
            'The OIP reviews law enforcement exemption claims carefully — consider requesting an OIP advisory opinion',
            'Body camera footage is not categorically exempt — the specific harm must be identified for each recording',
        ]),
        'notes': 'The OIP has extensively analyzed the law enforcement exemption under UIPA. The OIP\'s advisory opinions emphasize that the exemption requires a specific causal connection between disclosure and harm. See OIP Op. Ltr. No. 97-4 and related opinions on law enforcement records.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(3)',
        'exemption_number': '§ 92F-13(3)',
        'short_name': 'Unwarranted Invasion of Personal Privacy',
        'category': 'privacy',
        'description': 'Government records that would constitute a clearly unwarranted invasion of personal privacy are exempt. This requires a balancing test under HRS § 92F-14 between privacy interests and the public interest in disclosure.',
        'scope': 'Records containing personal information about identifiable individuals where disclosure would constitute a clearly unwarranted invasion of personal privacy. HRS § 92F-14 provides a non-exhaustive list of privacy interests and states that disclosure is not a clearly unwarranted invasion where the public interest in accountability substantially outweighs the privacy interest. Public employees have a reduced privacy expectation regarding their official conduct. The balancing test under § 92F-14 is the key analytical framework. Medical records, financial account details, and Social Security numbers typically qualify; employment and compensation data for public officials typically does not.',
        'key_terms': json.dumps([
            'personal privacy', 'invasion of privacy', 'clearly unwarranted',
            'privacy interest', 'public interest', 'balancing test', 'HRS § 92F-14',
            'personally identifiable information', 'personal information',
        ]),
        'counter_arguments': json.dumps([
            'HRS § 92F-14 requires balancing — the privacy interest must outweigh the public accountability interest',
            'Public employees have a reduced privacy expectation regarding their official conduct',
            'Names, titles, salaries, and public conduct of government employees are generally public under the balancing test',
            'The "clearly unwarranted" qualifier sets a high bar — minor or speculative privacy concerns do not qualify',
            'Information already in the public domain cannot be withheld as a privacy matter',
            'The OIP can advise on whether a specific disclosure meets the "clearly unwarranted" standard',
        ]),
        'notes': 'UIPA\'s privacy exemption is distinctive because HRS § 92F-14 explicitly provides both a list of privacy interests and the balancing methodology. The OIP has issued extensive guidance on applying this test. The OIP\'s advisory opinions on privacy under UIPA are highly influential and are the practical starting point for analyzing any privacy exemption claim.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(4)',
        'exemption_number': '§ 92F-13(4)',
        'short_name': 'Trade Secrets and Privileged Commercial Information',
        'category': 'commercial',
        'description': 'Government records containing trade secrets, or confidential commercial or financial information, provided to government agencies by private parties under an expectation of confidentiality, are exempt from disclosure.',
        'scope': 'Privately submitted information that: (1) constitutes a genuine trade secret — information with economic value from secrecy that is subject to reasonable protective measures; or (2) constitutes confidential commercial or financial information whose disclosure would cause genuine competitive harm. Government-generated financial records are not trade secrets. Amounts paid with public funds are public. The agency must independently evaluate trade secret claims. Blanket confidentiality designations by submitters do not control.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'financial information',
            'competitive harm', 'proprietary information', 'confidential business information',
            'contract pricing', 'business information', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Government expenditure amounts are public regardless of vendor confidentiality claims',
            'The submitter must demonstrate actual competitive harm, not merely assert confidentiality',
            'Publicly available information cannot be a trade secret',
            'Information required by law to be submitted has reduced confidentiality expectations',
            'Government-generated reports and analysis of submitted data are not trade secrets',
            'The OIP can advise on whether specific information meets the trade secret standard',
        ]),
        'notes': 'The OIP applies a narrow construction to trade secret and commercial information claims consistent with UIPA\'s disclosure mandate. Hawaii follows the general rule that government expenditure data is public regardless of vendor claims. See OIP Op. Ltr. No. 98-6 on commercial information claims.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(5)',
        'exemption_number': '§ 92F-13(5)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or attorney work-product doctrine are exempt from UIPA disclosure, consistent with Hawaii\'s evidentiary privilege rules.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and work product prepared in anticipation of litigation. The privilege requires the standard elements: lawyer-client relationship, confidential communication, for legal advice purposes. Business and policy advice from lawyers is not covered. Billing records are generally not privileged. Waiver through disclosure in public proceedings or to non-privileged persons eliminates the protection.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not policy or business guidance',
            'Attorney billing records are generally public',
            'Waiver occurs when the agency cites legal advice in public proceedings or relies on it in public decisions',
            'Settlement agreements and consent decrees are public once executed',
            'The OIP reviews privilege claims for their sufficiency — consider requesting an advisory opinion',
        ]),
        'notes': 'Hawaii\'s UIPA attorney-client exemption is consistent with standard privilege doctrine. The OIP has noted that the privilege must not be used to shield all agency communications that happen to involve legal counsel. The narrow construction principle under UIPA applies.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(6)',
        'exemption_number': '§ 92F-13(6)',
        'short_name': 'Personnel Records — Clearly Unwarranted Privacy Invasion',
        'category': 'privacy',
        'description': 'Personnel records and similar files, the disclosure of which would constitute a clearly unwarranted invasion of personal privacy, are exempt from disclosure under UIPA. This requires application of the balancing test under HRS § 92F-14.',
        'scope': 'Private personal information in public employee personnel files: medical records, Social Security numbers, home addresses, personal financial information, and similar data whose disclosure would fail the § 92F-14 balancing test. However, names, job titles, salaries, and the general employment status of public employees are public under the balancing test because the public accountability interest substantially outweighs the privacy interest. Disciplinary records involving serious misconduct or public-facing conduct are generally disclosable after balancing. The OIP applies § 92F-14 balancing to each personnel record category.',
        'key_terms': json.dumps([
            'personnel records', 'employee records', 'privacy invasion', 'public employee',
            'salary', 'disciplinary records', 'performance evaluation',
            'HR records', 'employment records', 'HRS § 92F-14',
        ]),
        'counter_arguments': json.dumps([
            'Names, job titles, and salaries of public employees are generally public after § 92F-14 balancing',
            'Disciplinary records resulting in suspension, demotion, or termination are typically public',
            'Separation agreements and severance payments are public',
            'The OIP has consistently held that public employee compensation and basic employment data must be disclosed',
            'Law enforcement officer misconduct records have heightened disclosure obligations',
            'Challenge overbroad claims that entire personnel files are exempt',
        ]),
        'notes': 'The OIP has issued extensive guidance on personnel record privacy under UIPA. The § 92F-14 balancing test consistently requires disclosure of public employee employment and compensation data. See OIP Op. Ltr. No. 96-18 and related opinions on personnel record requests.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(7)',
        'exemption_number': '§ 92F-13(7)',
        'short_name': 'Intra-Agency Memoranda — Deliberative Process',
        'category': 'deliberative',
        'description': 'Intra-agency memoranda that would not be available to a party in litigation with the agency are exempt from UIPA disclosure. This tracks the federal deliberative process privilege framework.',
        'scope': 'Predecisional intra-agency memoranda containing opinions, recommendations, and deliberative analysis that would be protected from discovery in litigation under the deliberative process privilege. The exemption does NOT cover: (1) purely factual material; (2) records adopted as final agency positions; (3) "working law"; (4) documents circulated outside the agency. Factual portions must be segregated and released. The test is whether the document would be protected from civil discovery — a meaningful limiting principle that prevents over-invocation of the exemption.',
        'key_terms': json.dumps([
            'intra-agency memorandum', 'deliberative process', 'predecisional',
            'internal memorandum', 'policy deliberation', 'draft document',
            'agency recommendations', 'working paper',
        ]),
        'counter_arguments': json.dumps([
            'Factual material in deliberative memos is not exempt — must be segregated and released',
            'Records adopted as final agency positions are no longer predecisional',
            '"Working law" must be disclosed regardless of its internal format',
            'The test is whether the document would be protected in litigation — challenge where it clearly would not be',
            'External communications and documents shared outside the agency are not intra-agency memos',
        ]),
        'notes': 'Hawaii\'s intra-agency memo exemption under § 92F-13(7) tracks the federal deliberative process privilege framework. The OIP applies it narrowly. The litigation-privilege test is a useful limiting principle that courts and the OIP apply to prevent overreach.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-13(8)',
        'exemption_number': '§ 92F-13(8)',
        'short_name': 'Information Made Confidential by Other Statutes',
        'category': 'statutory',
        'description': 'Government records made confidential by other state or federal statutes are exempt from disclosure under UIPA. This is a cross-reference exemption incorporating specific statutory confidentiality obligations.',
        'scope': 'Records specifically designated as confidential by Hawaii state statutes (other than UIPA itself) or by federal law — for example, tax return information (HRS § 237-34), medical records under HIPAA, student records under FERPA, and similar statutory confidentiality provisions. The exemption applies only to records specifically covered by the referenced statute — it does not create a general confidentiality zone for all records touching on sensitive topics. Agencies must identify the specific statute that applies and confirm it covers the specific records at issue.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'FERPA', 'HIPAA', 'tax information',
            'confidential by statute', 'federal law', 'state law confidentiality',
            'cross-reference exemption', 'statutory protection',
        ]),
        'counter_arguments': json.dumps([
            'The referenced statute must specifically cover the records at issue — general subject-matter overlap is not sufficient',
            'Challenge whether the agency has correctly identified an applicable statute',
            'Some statutes impose confidentiality only on specific agencies or in specific contexts — verify the statute applies here',
            'Aggregate and anonymized data may not be covered by the underlying confidentiality statute',
            'The agency must produce all records not specifically covered by the cited statute',
        ]),
        'notes': 'This catch-all statutory exemption requires agencies to identify a specific statute creating confidentiality, not merely argue that records are sensitive. The OIP carefully reviews statutory cross-reference claims to ensure the cited statute actually covers the specific records.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-14',
        'exemption_number': '§ 92F-14',
        'short_name': 'Privacy Balancing Test — Specific Personal Information Categories',
        'category': 'privacy',
        'description': 'HRS § 92F-14 establishes the privacy balancing test for UIPA, listing categories of information that implicate significant privacy interests and directing that disclosure is not a clearly unwarranted invasion when the public interest in accountability substantially outweighs the privacy interest.',
        'scope': 'HRS § 92F-14(b) lists categories of significant privacy interests: (1) Social Security numbers; (2) financial information other than salary; (3) personal health information; (4) home address, personal telephone number; (5) personal religious or political beliefs; (6) parole, probation, or criminal history. However, § 92F-14(a) directs that disclosure is "not a clearly unwarranted invasion" when the public accountability interest substantially outweighs the privacy interest. This balanced approach is unique — it provides both guidance and flexibility. The OIP applies this test routinely.',
        'key_terms': json.dumps([
            'privacy balancing test', 'HRS § 92F-14', 'clearly unwarranted invasion',
            'public accountability', 'privacy interest', 'Social Security number',
            'financial information', 'health information', 'home address',
        ]),
        'counter_arguments': json.dumps([
            'The balancing test can tip in favor of disclosure even for sensitive categories when the public accountability interest is strong',
            'Public employee performance of official duties always involves a reduced privacy expectation',
            'The OIP advisory process is the practical tool for resolving § 92F-14 disputes without litigation',
            'Challenge privacy claims for categories not listed in § 92F-14(b) — the listed categories are significant because the bar is higher for non-listed information',
            'Information relating to how public funds are spent typically passes the balancing test in favor of disclosure',
        ]),
        'notes': 'HRS § 92F-14 is Hawaii\'s most distinctive UIPA provision. The dual-function approach — listing privacy-sensitive categories while also providing a balancing test — gives both agencies and requesters a workable framework. The OIP has developed a substantial body of advisory opinions applying this test across different record types and fact patterns.',
    },
    {
        'jurisdiction': 'HI',
        'statute_citation': 'HRS § 92F-22',
        'exemption_number': '§ 92F-22',
        'short_name': 'Individual Right of Access to Personal Records',
        'category': 'privacy',
        'description': 'UIPA provides individuals a right to inspect and copy records about themselves that are maintained by government agencies, and a right to request correction of inaccurate records. This is a Privacy Act-like provision unique among state public records laws.',
        'scope': 'Individuals have a right to access records specifically about themselves maintained by state agencies (§ 92F-22), even if those records might not be publicly available to others. This includes personal files, individual case records, records used to make decisions about the individual, and similar personal records. The access right is not absolute — records containing information about others, records exempt under § 92F-13, and records that would frustrate government functions may still be withheld from the individual subject. Accompanying this is a right to request correction of inaccurate records (§ 92F-24).',
        'key_terms': json.dumps([
            'individual access right', 'personal records', 'Privacy Act', 'right to access',
            'records about self', 'correction of records', 'HRS § 92F-22', 'HRS § 92F-24',
            'individual subject access',
        ]),
        'counter_arguments': json.dumps([
            'The individual access right under § 92F-22 is broader than the general public\'s access right — individuals can request records about themselves that are not otherwise public',
            'Agencies must respond to § 92F-22 requests with the same procedural requirements (10 business days) as general UIPA requests',
            'Use § 92F-22 when requesting records about yourself — it provides a distinct legal basis for access',
            'The correction right under § 92F-24 can be exercised when records are inaccurate',
        ]),
        'notes': 'Hawaii\'s individual access right under HRS § 92F-22 is analogous to the federal Privacy Act, 5 U.S.C. § 552a. It is unusual among state public records laws and gives individuals a distinct right of access to records about themselves, even if those records would not be publicly available to others. This is a valuable tool for individuals seeking government records about themselves.',
    },
]

# =============================================================================
# RULES
# Hawaii UIPA, HRS Ch. 92F.
# 10 business days to respond. OIP advisory process is key — influential but
# not binding. $0.05/page copy fee (very low). No attorney's fees provision.
# Individual access right (§ 92F-22). OIP complaints before court action.
# =============================================================================

HI_RULES = [
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'HRS § 92F-15(b)',
        'notes': 'Hawaii agencies must respond to UIPA requests within 10 business days of receipt. Within those 10 days, the agency must either: (1) grant access to the requested records; (2) deny the request with a written explanation citing the applicable exemption; or (3) notify the requester that an extension is needed and provide a specific date for production. The 10-day clock begins on the date the written request is received by the agency.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'extension_available',
        'param_value': 'yes_with_notice',
        'day_type': 'business',
        'statute_citation': 'HRS § 92F-15(b)',
        'notes': 'Agencies may extend the 10-business-day response period if they provide written notice to the requester explaining the reason for the extension and specifying the date by which they will respond. Extensions must be reasonable — the OIP has found that open-ended extensions without a specific completion date are improper. The extension notice must give a definite response date.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'fee_cap',
        'param_key': 'copy_fee_per_page',
        'param_value': '0.05',
        'day_type': None,
        'statute_citation': 'HRS § 92F-21; HAR § 2-71-31',
        'notes': 'Hawaii has one of the lowest copy fees in the country: $0.05 per page for paper copies. This fee is set by administrative rule (HAR § 2-71-31) implementing UIPA. For electronic records, agencies may charge for the actual cost of reproduction (often nominal). Agencies may not charge staff time for searching or redacting — only actual reproduction costs are authorized. The low per-page fee makes large document productions more accessible.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'fee_cap',
        'param_key': 'search_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'HRS § 92F-21',
        'notes': 'Hawaii UIPA does not authorize agencies to charge for staff time spent searching for, reviewing, or redacting records. Only actual reproduction costs are permissible. A fee schedule that includes "research fees," "processing fees," or "staff time" is imposing charges not authorized by UIPA. Requesters should challenge such charges by citing § 92F-21 and the administrative rule.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'HRS § 92F-21',
        'notes': 'UIPA does not mandate fee waivers for specific requester categories, but agencies may waive fees at their discretion. Given Hawaii\'s very low $0.05/page rate, fee waivers are less critical than in states with higher copy fees. For electronic records, the reproduction cost is typically zero. Requesters seeking waivers should articulate the public interest served.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'appeal_deadline',
        'param_key': 'oip_complaint_available',
        'param_value': 'yes_advisory_only',
        'day_type': None,
        'statute_citation': 'HRS § 92F-42; HRS § 92F-15(a)',
        'notes': 'Hawaii\'s Office of Information Practices (OIP) can issue advisory opinions on UIPA disputes. OIP advisory opinions are influential — agencies generally follow them — but they are not legally binding. The OIP process is the practical first step for most UIPA disputes and is far less expensive than litigation. A requester denied access can request an OIP advisory opinion on whether the denial was proper. The OIP typically responds within several weeks to months. If the OIP concludes the denial was improper and the agency still refuses to comply, judicial enforcement becomes necessary.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'HRS § 92F-15(a)',
        'notes': 'A requester denied access may file an enforcement action in the circuit court of the appropriate circuit. The court reviews the denial de novo and may conduct in camera review of withheld records. There is no requirement to exhaust the OIP advisory process before going to court, but the OIP process is less expensive and often effective. Circuit court enforcement is available directly without any administrative exhaustion requirement.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'not_provided_by_statute',
        'day_type': None,
        'statute_citation': 'HRS Ch. 92F',
        'notes': 'Hawaii UIPA has NO attorney\'s fees provision. Unlike most state public records laws, UIPA does not authorize courts to award attorney fees to a prevailing requester. This is a significant limitation — it makes litigation expensive and reduces the practical enforceability of UIPA rights. The OIP advisory process is therefore especially important as a lower-cost alternative. Requesters should factor the lack of fee-shifting into litigation decisions. Some requesters use the OIP process specifically because it is the only economically viable dispute resolution option.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'HRS § 92F-11',
        'notes': 'Hawaii UIPA does not require requesters to identify themselves or state a purpose. The right to inspect government records is a general right not dependent on requester identity or stated reason. For personal records requests under § 92F-22, the individual must verify their identity to confirm they are the subject of the records. But for general public records requests, identity and purpose need not be provided.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'HRS § 92F-15(c)',
        'notes': 'When a record contains both exempt and non-exempt information, agencies must release all nonexempt, reasonably segregable portions. Blanket withholding of documents containing some exempt content is improper. The agency must identify what has been withheld and the statutory basis for each withholding. The OIP reviews segregability claims and has found violations where agencies redacted more than necessary.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'HRS § 92F-11; § 92F-15',
        'notes': 'UIPA establishes a presumption that all government records are open to public inspection. The burden of demonstrating that any record is exempt from disclosure is on the agency. In judicial enforcement proceedings, the agency must affirmatively establish that an exemption applies to each specific withheld record. The OIP applies the same burden in advisory opinion proceedings.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'individual_access_right',
        'param_value': 'available_under_section_92F-22',
        'day_type': None,
        'statute_citation': 'HRS § 92F-22',
        'notes': 'Hawaii\'s UIPA uniquely provides individuals a distinct right of access to records specifically about themselves (§ 92F-22), even if those records are not publicly available to others. This is analogous to the federal Privacy Act. Individuals may also request corrections of inaccurate records (§ 92F-24). This right is in addition to the general public records access right. When requesting records about yourself, invoke both the general access right under § 92F-11 and the individual access right under § 92F-22.',
    },
    {
        'jurisdiction': 'HI',
        'rule_type': 'initial_response',
        'param_key': 'oip_advisory_practical_first_step',
        'param_value': 'strongly_recommended',
        'day_type': None,
        'statute_citation': 'HRS § 92F-42',
        'notes': 'Given the absence of attorney\'s fees in Hawaii UIPA, the OIP advisory opinion process is the practical first step for most UIPA disputes. OIP opinions are influential — most agencies comply. The process is less expensive than litigation and typically faster than court proceedings. Requesters should request an OIP advisory opinion before filing suit in any case where litigation costs would not be justified by the records at stake. The OIP can be reached at oip.hawaii.gov.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

HI_TEMPLATES = [
    {
        'jurisdiction': 'HI',
        'record_type': 'general',
        'template_name': 'General Hawaii UIPA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: Uniform Information Practices Act Request — HRS Chapter 92F

Dear Records Access Officer:

Pursuant to Hawaii's Uniform Information Practices Act (UIPA), HRS Chapter 92F, I hereby request access to and copies of the following government records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format where available.

Regarding fees: Under HRS § 92F-21 and HAR § 2-71-31, copying fees are $0.05 per page for paper copies. I am willing to pay copying costs up to ${{fee_limit}}. If costs will exceed that amount, please notify me before proceeding. Note that search and retrieval time is not a chargeable cost under UIPA.

Under HRS § 92F-11, all government records are presumptively open to public inspection. The burden of demonstrating any exemption rests on the agency. Under HRS § 92F-15(c), all nonexempt, reasonably segregable portions of any record must be released.

If any records or portions are withheld, please: (1) identify each withheld record with sufficient description; (2) cite the specific UIPA exemption under HRS § 92F-13 or other applicable provision; (3) explain how the exemption applies to the specific record; (4) confirm that nonexempt, segregable portions have been released.

Under HRS § 92F-15(b), please respond within 10 business days of receipt of this request. If you require an extension, please provide written notice specifying a definite response date.

I am aware of the OIP advisory opinion process under HRS § 92F-42, and will request an OIP advisory opinion if this request is denied without adequate legal justification.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While UIPA does not mandate a fee waiver, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records concern {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. Hawaii\'s $0.05/page copying fee is already very low. For records provided electronically, the reproduction cost is zero.

A fee waiver is consistent with UIPA\'s purpose of open access to government information.''',
        'expedited_language': '''I request that this UIPA request be processed as quickly as possible within the 10-business-day window. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately if any clarification would allow faster processing.''',
        'notes': 'General-purpose Hawaii UIPA template. Key HI features: (1) 10 business days to respond per § 92F-15(b); (2) OIP advisory process is the practical dispute resolution mechanism — OIP opinions are influential though not binding; (3) NO attorney\'s fees provision — litigation is expensive, use OIP first; (4) $0.05/page copy fee (very low — among the lowest in the country); (5) individual access right under § 92F-22 for records about yourself; (6) § 92F-14 balancing test for privacy questions; (7) burden of proof on agency. Reference "UIPA" and HRS Ch. 92F, not "FOIA." The OIP website (oip.hawaii.gov) is a critical resource.',
    },
    {
        'jurisdiction': 'HI',
        'record_type': 'personal_records',
        'template_name': 'Hawaii UIPA Request — Individual Access to Personal Records (§ 92F-22)',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: UIPA Individual Access Request — HRS § 92F-22; HRS Chapter 92F

Dear Records Access Officer:

Pursuant to HRS § 92F-22 of Hawaii's Uniform Information Practices Act, I hereby request access to records maintained by {{agency_name}} that contain information specifically about me.

I am requesting the following records that I believe contain information about myself:

{{description_of_records}}

To verify my identity, I am providing the following identifying information:
{{identity_verification}}

[Enclose a copy of a government-issued ID if required by agency policy.]

This request is made under HRS § 92F-22, which provides individuals a distinct right of access to government records about themselves, in addition to the general public access right under HRS § 92F-11.

I also request, pursuant to HRS § 92F-22(b), a description of the information maintained about me in any records system maintained by {{agency_name}}, including the categories of records maintained and the routine uses to which such information is put.

If any records are withheld, please: (1) identify the record with sufficient description; (2) cite the specific exemption; (3) note whether the record may be withheld from me as the subject (some exemptions do not apply to the individual about whom the record pertains).

If any records are inaccurate, I reserve the right to request correction under HRS § 92F-24.

Under HRS § 92F-15(b), please respond within 10 business days. Copying fees at $0.05 per page under HAR § 2-71-31 are acceptable up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this personal records access request. Accessing records about oneself is a fundamental right under § 92F-22. Given the $0.05/page rate, a waiver would represent minimal cost to the agency. I am requesting these records to {{personal_access_reason}}.''',
        'expedited_language': '''I request prompt processing of this § 92F-22 personal access request. I need access to these records by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'Hawaii\'s individual access right under HRS § 92F-22 is unique among state public records laws and is analogous to the federal Privacy Act. This template is for individuals requesting records specifically about themselves. Key features: (1) § 92F-22 provides access to records about oneself even if not publicly available to others; (2) § 92F-22(b) entitles the individual to a description of records maintained about them; (3) § 92F-24 provides a correction right for inaccurate records; (4) identity verification may be required; (5) same 10-business-day response deadline; (6) no attorney\'s fees — OIP advisory process is the practical remedy for denials.',
    },
    {
        'jurisdiction': 'HI',
        'record_type': 'law_enforcement',
        'template_name': 'Hawaii UIPA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Records Access Officer
{{agency_name}}
{{agency_address}}

Re: UIPA Request — Law Enforcement Records, HRS Chapter 92F

Dear Records Access Officer:

Pursuant to Hawaii's Uniform Information Practices Act, HRS Chapter 92F, I request copies of the following law enforcement records:

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

Regarding any claimed exemption under HRS § 92F-13(2): this exemption requires a specific showing that disclosure of each identified record would: (a) endanger the safety of a specific person; (b) prevent apprehension of a named suspect; (c) interfere with a pending prosecution; or (d) identify a confidential informant. General assertions that records are "investigative" do not suffice. The agency must apply a record-by-record analysis.

[If matter appears concluded:] If no prosecution is pending and the investigation is complete, the § 92F-13(2) exemption does not apply. Completed investigation files are disclosable.

Under HRS § 92F-11, all government records are presumptively open. The agency bears the burden of establishing each claimed exemption. Under § 92F-15(c), nonexempt, segregable portions must be released.

Copying fees at $0.05 per page are acceptable up to ${{fee_limit}}.

Please respond within 10 business days per § 92F-15(b). If this request is denied, I will request an OIP advisory opinion under § 92F-42.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this request. These records concern {{public_interest_explanation}}, a matter of government accountability. At $0.05/page, Hawaii\'s copy fee is among the lowest in the country, and electronic delivery incurs no reproduction cost. A waiver is appropriate given the public interest in this request.''',
        'expedited_language': '''I request expedited processing. These records are needed by {{needed_by_date}} because {{urgency_explanation}}. Please contact me if any clarification would accelerate production.''',
        'notes': 'Hawaii law enforcement UIPA template. HI-specific features: (1) § 92F-13(2) requires specific harm per record for active investigations only; (2) completed investigations are public; (3) NO attorney\'s fees — OIP advisory process is the critical pre-litigation step; (4) $0.05/page (very low); (5) 10 business days to respond; (6) OIP at oip.hawaii.gov should be consulted if access is denied; (7) privacy balancing under § 92F-14 applies to personal information in law enforcement records; (8) individual access right under § 92F-22 if requesting records about oneself.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in HI_EXEMPTIONS:
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

    print(f'HI exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in HI_RULES:
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

    print(f'HI rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in HI_TEMPLATES:
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

    print(f'HI templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'HI total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_hi', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
