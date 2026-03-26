#!/usr/bin/env python3
"""Build the Texas Public Information Act exemptions catalog.

Exemptions under Tex. Gov't Code Chapter 552, Subchapter C (§§ 552.101–552.153).
These are statutory exceptions to mandatory disclosure under the TPIA.
Data sourced from the statute text and Texas AG Open Records decisions.

Run: python3 scripts/build/build_tx_exemptions.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')

TX_EXEMPTIONS = [
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.101',
        'exemption_number': '§ 552.101',
        'short_name': 'Confidential by Law (Other Statutes)',
        'category': 'statutory',
        'description': 'Excepts information that is confidential by law, either constitutional, statutory, or by judicial decision. This is a catch-all provision that incorporates other state and federal statutes making particular records confidential.',
        'scope': 'Information considered confidential by law, including constitutional provisions, state and federal statutes, and court decisions that designate specific categories of information as confidential. Common examples: tax records (Tex. Tax Code § 111.006), certain social services records, mental health records (Tex. Health & Safety Code § 611.002), HIV/AIDS test results (Tex. Health & Safety Code § 81.103).',
        'key_terms': json.dumps(['confidential by law', 'statute', 'constitutional provision', 'court decision', 'tax records', 'mental health', 'HIV', 'social services', 'medical records', 'juvenile records']),
        'counter_arguments': json.dumps([
            'The government body must identify the specific statute, constitutional provision, or court decision that makes the information confidential — a general claim is insufficient',
            'Challenge whether the cited statute actually applies to these specific records and this specific governmental body',
            'If the underlying statute has been repealed or amended, the § 552.101 claim may fail',
            'Many statutes that appear to create confidentiality are discretionary (the agency "may" withhold) — argue § 552.101 requires mandatory confidentiality',
            'Check whether the cited confidentiality statute has exceptions that apply to your situation (e.g., records about yourself, media exceptions)',
            'If the information has been publicly disclosed by the government body before, the confidentiality claim may be waived',
        ]),
        'notes': 'Tex. AG Open Records Decision No. OR2014-10311 illustrates that the citing body must affirmatively demonstrate the specific legal basis for confidentiality, not merely assert that records are "sensitive." Courts and the AG apply the specific statute cited, not a general sensitivity standard.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.102',
        'exemption_number': '§ 552.102',
        'short_name': 'Personnel Records — Competitive Examinations',
        'category': 'personnel',
        'description': 'Excepts from required disclosure information in a personnel file, the disclosure of which would constitute a clearly unwarranted invasion of personal privacy. Also excepts test questions and answers used in competitive examinations for employment.',
        'scope': 'Information in a personnel file whose disclosure would constitute a clearly unwarranted invasion of personal privacy; test questions and answers for state employment examinations prior to or after administration. The file of an employee must be open to the employee or the employee\'s authorized representative.',
        'key_terms': json.dumps(['personnel file', 'employee records', 'employment', 'competitive examination', 'test questions', 'personal privacy', 'unwarranted invasion']),
        'counter_arguments': json.dumps([
            'Public employees have a reduced privacy expectation in their official conduct — records of job performance, disciplinary action for on-the-job conduct, and job duties are generally not protected',
            'Salary, compensation, and benefits of public employees are public information under § 552.024',
            'The "clearly unwarranted" standard requires balancing — argue the public interest in accountability outweighs the privacy interest',
            'Disciplinary records related to misconduct in office are generally public, not personal',
            'This exception protects the employee, not the agency — an employee may choose to allow disclosure',
            'Administrative findings and reports about an employee\'s official conduct are not purely personal in nature',
        ]),
        'notes': 'The Texas AG has consistently held that information about an employee\'s official conduct, as opposed to purely personal information, does not fall within this exception. See, e.g., Tex. AG ORD No. OR2011-07534. Note that § 552.024 expressly provides that an employee\'s name, sex, ethnicity, salary, and dates of employment are public.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.103',
        'exemption_number': '§ 552.103',
        'short_name': 'Litigation / Pending Legal Proceedings',
        'category': 'litigation',
        'description': 'Excepts information relating to litigation of a civil or criminal nature to which the state or a political subdivision is or may be a party, where the release would give an advantage to the adverse party.',
        'scope': 'Information relating to a civil or criminal proceeding in which the governmental body is or may be a party, or may have an interest, where the release would give an advantage to the adverse party. Applies to pending as well as reasonably anticipated litigation.',
        'key_terms': json.dumps(['litigation', 'civil proceeding', 'criminal proceeding', 'adverse party', 'legal proceedings', 'lawsuit', 'pending litigation', 'advantage']),
        'counter_arguments': json.dumps([
            'The government body must demonstrate both (1) that litigation is pending or reasonably anticipated, and (2) that releasing the information would give an advantage to the opposing party',
            'A mere threat or speculation about future litigation is insufficient — there must be a real, identifiable legal proceeding',
            'If the litigation has concluded, this exception no longer applies',
            'Challenge whether the specific records would actually provide a legal advantage, not just general sensitivity',
            'Information that is independently public or discoverable through other means does not confer an "advantage"',
            'The Texas AG has scrutinized overbroad claims under this section — the entire file cannot be withheld without record-by-record analysis',
            'The requester\'s own records or information about the requester cannot generally be withheld under this provision when sought by the requester',
        ]),
        'notes': 'The AG requires specific, not conclusory, showings that particular records would give an advantage to an adverse party. See Tex. AG ORD No. OR2009-02337. The litigation must be concrete, not theoretical.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.104',
        'exemption_number': '§ 552.104',
        'short_name': 'Competitive Bidding / Procurement',
        'category': 'commercial',
        'description': 'Excepts information that would give advantage to competitors or bidders in a competitive procurement process. Protects bids and proposals while a competitive process is pending.',
        'scope': 'Information relating to a request for bids or proposals that, if disclosed, would give advantage to a competitor or bidder. This exception is largely inapplicable once a contract is awarded; bids and proposals generally become public after award.',
        'key_terms': json.dumps(['competitive bid', 'request for proposals', 'RFP', 'bid', 'procurement', 'competitive advantage', 'contractor', 'vendor', 'contract award']),
        'counter_arguments': json.dumps([
            'After a contract is awarded, bids and proposals are generally public — the competitive process has concluded',
            'The exception applies only while the competitive process is pending, not indefinitely',
            'Financial terms of awarded contracts are public — challenge overbroad withholding that extends to contract price',
            'Proprietary or trade secret information within bids may be protected under § 552.110, but not the entire bid',
            'Request the contract itself (not just the bid) — awarded contracts are not protected by this provision',
            'Government-generated analyses and evaluations of bids are not the bids themselves and may not qualify',
        ]),
        'notes': 'This exception is time-limited by nature. The Texas AG has held that once a contract is awarded, the competitive rationale for withholding no longer applies to most information in the bid file.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.105',
        'exemption_number': '§ 552.105',
        'short_name': 'Location of Real Property for Public Purpose',
        'category': 'real_property',
        'description': 'Excepts information relating to the location of real property for a public purpose prior to formal announcement of the project, where disclosure could give financial advantage to speculators.',
        'scope': 'Information that relates to the location or price of real property that a governmental body plans to acquire for a public purpose and that, if prematurely disclosed, could enable a person to speculate and take undue advantage of the government.',
        'key_terms': json.dumps(['real property', 'land acquisition', 'public purpose', 'speculation', 'price', 'location', 'eminent domain', 'condemnation']),
        'counter_arguments': json.dumps([
            'Once a project is publicly announced, the speculative harm no longer applies and the information should be released',
            'Challenge whether there is a concrete acquisition plan — speculative future projects do not qualify',
            'General land-use planning documents that do not specify parcels for acquisition are not covered',
            'After the government commits publicly to a project, disclosure is appropriate',
            'Request post-acquisition records — once property is purchased, the exception no longer applies',
        ]),
        'notes': 'This is a narrow, time-limited exception designed to prevent real estate speculation. It does not permit permanent withholding — once the project is publicly committed, the basis for withholding evaporates.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.106',
        'exemption_number': '§ 552.106',
        'short_name': 'Drafts and Working Papers',
        'category': 'deliberative',
        'description': 'Excepts draft or working papers used to prepare a final written report. This is a narrow deliberative process exception intended to protect the internal deliberative process, not final decisions or reports.',
        'scope': 'Draft or working papers incident to the preparation of a final written report. The exception does not apply to the final report itself, and does not apply broadly to all predecisional documents — only to drafts of specific written reports.',
        'key_terms': json.dumps(['draft', 'working papers', 'predecisional', 'deliberative', 'preliminary', 'working document', 'final report', 'preparation']),
        'counter_arguments': json.dumps([
            'This exception is narrower than the federal deliberative process privilege — it applies only to drafts of specific final written reports, not all predecisional materials',
            'If no final report was prepared, there are no "working papers incident to preparation" of a final report',
            'Factual information in drafts is not protected — only the deliberative, opinion-based portions may qualify',
            'The final report itself must be disclosed, and challenge any attempt to use § 552.106 to withhold the final version',
            'Drafts of rules, regulations, or policies that carry legal effect may not qualify as merely "internal working papers"',
            'Challenge whether the document is truly a draft versus an internal policy or guideline that was effectively adopted',
            'The Texas AG has construed this exception narrowly — it does not swallow the general rule of openness',
        ]),
        'notes': 'Courts and the Texas AG have emphasized that § 552.106 is a limited exception. Unlike the federal deliberative process privilege, it does not broadly cover all predecisional agency communications. See Tex. AG ORD No. OR2003-7455.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.107',
        'exemption_number': '§ 552.107',
        'short_name': 'Attorney-Client Privilege',
        'category': 'privilege',
        'description': 'Excepts information that is protected by the attorney-client privilege, including communications between an attorney and client made for the purpose of legal advice, and information reflecting attorney work product.',
        'scope': 'Information protected by the attorney-client privilege under Tex. R. Evid. 503, including confidential communications between a governmental body and its attorney relating to legal advice, and information constituting attorney work product under Tex. R. Civ. P. 192.5. The privilege belongs to the client (the governmental body).',
        'key_terms': json.dumps(['attorney-client privilege', 'legal advice', 'work product', 'attorney', 'counsel', 'confidential communication', 'legal opinion', 'representation', 'litigation support']),
        'counter_arguments': json.dumps([
            'Not every communication involving an attorney is privileged — the communication must be for the purpose of legal advice, not purely administrative or policy matters',
            'The privilege belongs to the governmental body (the client), not the attorney — but the government body may waive it',
            'Challenge whether the attorney was acting as legal counsel versus as a policy advisor, lobbyist, or administrator',
            'The privilege does not apply to the underlying facts, only the communication about those facts',
            'Pre-existing documents sent to an attorney do not become privileged merely because counsel received them',
            'Work product protection is not absolute — there is no work product protection for factual materials, and necessity can overcome protection for ordinary work product',
            'If a third party was present during the communication, privilege may be waived',
            'Challenge whether the government body has waived privilege by disclosing the substance of advice in public proceedings',
        ]),
        'notes': 'The Texas AG routinely reviews attorney-client privilege claims and requires the governmental body to demonstrate both the attorney-client relationship and that the communication was for legal advice. See City of Garland v. Dallas Morning News, 22 S.W.3d 351 (Tex. 2000).',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.108',
        'exemption_number': '§ 552.108',
        'short_name': 'Law Enforcement Records',
        'category': 'law_enforcement',
        'description': 'Excepts certain law enforcement records and information compiled in connection with a criminal investigation, unless the criminal matter has been resolved, the information is about a person who is deceased, or the public interest outweighs the harm.',
        'scope': 'Information held by a law enforcement agency or prosecutor that deals with the detection, investigation, or prosecution of crime, or the internal records of a law enforcement agency. Includes: information relating to an investigation that could interfere with the investigation; information revealing the identity of a confidential informant; information about an undercover officer. This exception is subject to several overrides and does not categorically exempt all law enforcement records.',
        'key_terms': json.dumps(['law enforcement', 'criminal investigation', 'prosecution', 'police records', 'detective', 'informant', 'undercover', 'criminal offense', 'investigation records', 'incident report']),
        'counter_arguments': json.dumps([
            'Basic incident reports and offense reports are generally public under Texas law — the exception does not categorically cover all police records',
            'Once an investigation is concluded (case closed, charges dismissed, conviction final), the investigative rationale for withholding typically no longer applies',
            'Challenge whether the record was truly "compiled in connection with" a criminal investigation versus routine administrative records',
            'Information about the identity and conduct of public employees acting in their official capacity is generally public even within law enforcement agencies',
            'The statute has specific subsets — challenge which specific subsection the agency is invoking and whether the facts satisfy it',
            'Records of agency policies and procedures for law enforcement operations are not investigative records',
            'Records of completed investigations, final reports, and prosecutorial dispositions are generally public',
            'The Texas AG has required line-by-line analysis — a blanket claim over an entire file is insufficient',
        ]),
        'notes': 'One of the most litigated TPIA exceptions. The AG routinely requires in camera review of claimed law enforcement records. Note that § 552.108 does not apply to regulatory agencies or administrative proceedings — only to criminal law enforcement. See, e.g., City of Houston v. Houston Chronicle Publishing Co., 531 S.W.2d 177 (Tex. Civ. App. 1975).',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.110',
        'exemption_number': '§ 552.110',
        'short_name': 'Trade Secrets / Commercial Information',
        'category': 'commercial',
        'description': 'Excepts trade secrets and commercial or financial information submitted to a governmental body where the submitting party has a reasonable expectation of confidentiality and disclosure would cause competitive harm.',
        'scope': 'Trade secrets obtained from a person and privileged or confidential by statute or judicial decision; or commercial or financial information for which it is demonstrated based on specific factual evidence that disclosure would cause substantial competitive harm to the person from whom the information was obtained.',
        'key_terms': json.dumps(['trade secret', 'commercial information', 'financial information', 'competitive harm', 'proprietary', 'confidential', 'business records', 'competitive disadvantage', 'third party']),
        'counter_arguments': json.dumps([
            'The information must come from a private party — government-generated information is not protected under § 552.110',
            'The competitive harm must be "substantial" and must be demonstrated with specific factual evidence, not conclusory assertions',
            'Information that is publicly available through other means cannot suffer competitive harm from disclosure',
            'Request information from the third party submitter — if the submitter does not object or cannot demonstrate harm, the claim fails',
            'Challenge whether the information truly constitutes a trade secret under Texas law — secret, continuous use in trade, reasonable efforts to maintain secrecy',
            'Financial terms of government contracts are generally not protected even if the contractor claims them as confidential — the public interest in contract transparency is high',
            'Pricing information submitted in competitive bids may become public after contract award',
            'The governmental body cannot assert § 552.110 on its own — only the submitting party can demonstrate competitive harm',
        ]),
        'notes': 'Texas courts have applied a substantial competitive harm standard. The third-party submitter, not the governmental body, typically has the burden to demonstrate the harm. See Boeing Co. v. Paxton, 466 S.W.3d 831 (Tex. 2015), holding that a company must make a specific factual showing of competitive harm, not merely assert that records are proprietary.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.111',
        'exemption_number': '§ 552.111',
        'short_name': 'Intra-Agency Advisory Opinions',
        'category': 'deliberative',
        'description': 'Excepts internal communications of a governmental body, consisting of advice, recommendations, and opinions reflecting the policy deliberations of agency officials, if disclosure would interfere with the deliberative process.',
        'scope': 'An interagency or intraagency memorandum or letter that would not be available by law to a party in litigation with the agency, encompassing the deliberative process privilege. Protects communications that are both predecisional and deliberative in nature. Does not protect purely factual material or adopted agency policy.',
        'key_terms': json.dumps(['advisory opinion', 'intra-agency', 'interagency', 'deliberative process', 'predecisional', 'recommendation', 'policy deliberation', 'internal memorandum', 'opinion', 'advice']),
        'counter_arguments': json.dumps([
            'The communication must be both predecisional AND deliberative — factual portions are not protected even within a deliberative memorandum',
            'Final decisions, adopted policies, and the agency\'s working law are not predecisional and must be disclosed',
            'If the agency relied on a memorandum as the basis for a final decision, the memorandum may lose its predecisional character',
            'Communications that reflect final agency positions, even if labeled "internal," are not protected',
            'Factual investigations and reports — even if conducted internally — are generally not deliberative',
            'Challenge whether the author had decision-making authority — not all opinions from subordinate employees qualify',
            'Under § 552.022, certain categories such as final opinions and interpretations of law are expressly made public and cannot be withheld under § 552.111',
            'The deliberative process privilege is qualified — demonstrate that the public interest in disclosure outweighs the government\'s interest in confidentiality',
        ]),
        'notes': 'Modeled on the federal deliberative process privilege under FOIA Exemption 5. The Texas AG has held that § 552.111 protects the frank exchange of ideas within an agency, but requires the deliberative process to be ongoing and the documents to be truly preparatory to a decision. See Open Records Decision No. OR2005-08985.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.112',
        'exemption_number': '§ 552.112',
        'short_name': 'Student Records',
        'category': 'education',
        'description': 'Excepts student records at an educational institution funded wholly or partly from state revenue, to the extent required by the federal Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g.',
        'scope': 'Student records at publicly funded educational institutions, to the extent confidential under FERPA. Student means a person who is or was enrolled at the institution. Incorporates FERPA\'s definition of "education records" and its exceptions (e.g., directory information if no opt-out, records of former employees, law enforcement unit records).',
        'key_terms': json.dumps(['student records', 'FERPA', 'education records', 'enrollment', 'university', 'school', 'academic records', 'student privacy', 'directory information']),
        'counter_arguments': json.dumps([
            'FERPA has numerous exceptions — directory information (name, address, dates of attendance) is public unless the student has opted out',
            'Law enforcement unit records maintained separately from education records are not FERPA-protected',
            'Records of employees who are not currently enrolled students are not student education records',
            'Aggregate, de-identified statistical data about students is generally not protected',
            'Challenge whether the specific records qualify as "education records" under FERPA\'s definition',
            'Records about a deceased student may not be protected under FERPA',
            'Records available to the student themselves (under FERPA\'s access rights) should be accessible to the student upon their own TPIA request',
            'If the institution has disclosed the information before, FERPA\'s privacy interest may be diminished or waived',
        ]),
        'notes': '§ 552.112 incorporates FERPA by reference — the TPIA exception tracks FERPA\'s scope. Therefore, understanding FERPA\'s exceptions is critical to challenging a § 552.112 claim. The U.S. Supreme Court\'s ruling in Gonzaga University v. Doe, 536 U.S. 273 (2002), affects FERPA enforcement but not the TPIA exception itself.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.114',
        'exemption_number': '§ 552.114',
        'short_name': 'Personnel Records — Home Address, Birth Date, SSN',
        'category': 'privacy',
        'description': 'Excepts from mandatory disclosure certain identifying personal information of current and former employees of governmental bodies, specifically including home addresses, home telephone numbers, emergency contact information, date of birth, and social security numbers.',
        'scope': 'Information that relates to the home address, home telephone number, emergency contact information, and date of birth of an employee or former employee of a governmental body, and the social security number of a living person. The exception is subject to overrides: the person themselves can request their own information; the governmental body may choose to disclose with employee consent; law enforcement agencies may obtain the information.',
        'key_terms': json.dumps(['home address', 'home phone', 'date of birth', 'SSN', 'social security number', 'emergency contact', 'personal information', 'employee information', 'former employee']),
        'counter_arguments': json.dumps([
            'Only specifically listed categories are protected — work address, work phone, professional credentials, and official job duties are not covered',
            'Name, salary, title, and dates of employment are expressly made public under § 552.024 and are not protected by § 552.114',
            'The information the requester seeks may not actually be within the listed protected categories',
            'Public officials who voluntarily make their personal contact information public in their official capacity may have reduced expectations of privacy',
            'If the individual has publicly disclosed their own home address (e.g., on a public filing), the privacy interest is diminished',
            'Challenge whether the specific records sought actually contain the listed protected categories — a blanket claim over entire personnel files is not proper',
        ]),
        'notes': 'This provision reflects Texas\'s policy of protecting employees\' personal security information while preserving transparency in their public roles. Note the interplay with § 552.024, which expressly lists certain information about employees that must be made available. The protection runs to current and former employees.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.115',
        'exemption_number': '§ 552.115',
        'short_name': 'Photographs of Peace Officers / Prosecutors',
        'category': 'privacy',
        'description': 'Excepts photographs of peace officers and employees of a county, municipality, or state agency that operates a law enforcement agency, as well as prosecuting attorneys, when disclosure could endanger the safety of those persons.',
        'scope': 'Photographs of peace officers, employees of law enforcement agencies, and prosecuting attorneys where the photograph is on file with the agency and the officer or attorney has not consented to its public release. The safety rationale is presumed to apply without requiring specific threat evidence.',
        'key_terms': json.dumps(['photograph', 'peace officer', 'law enforcement officer', 'prosecutor', 'safety', 'identity', 'photo', 'police officer', 'undercover']),
        'counter_arguments': json.dumps([
            'If the officer or prosecutor has voluntarily made their photograph public (e.g., on official website, press releases, social media in official capacity), the exception may not apply',
            'Challenge whether the person whose photograph is sought is actually a "peace officer" as defined by law',
            'Photographs used in official public communications, press releases, or public profiles may have waived this protection',
            'This exception does not apply to body camera footage depicting officers in the performance of their duties, which is governed by separate provisions',
            'Photographs of retired or former officers may have a diminished basis for the safety rationale',
            'Public-facing officers (e.g., public information officers) who routinely appear in media may have diminished claims',
        ]),
        'notes': 'This exception was added to address officer safety concerns. It is distinct from the body camera footage statute (Tex. Gov\'t Code Chapter 1701) and does not prevent disclosure of video footage depicting officers. The AG has distinguished between file photographs and video recordings.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.116',
        'exemption_number': '§ 552.116',
        'short_name': 'Audit Working Papers',
        'category': 'audit',
        'description': 'Excepts working papers and internal audit documents assembled in connection with an audit, examination, or investigation of a governmental body, until the audit is completed and the final audit report is available.',
        'scope': 'Working papers assembled in connection with an audit by the state auditor, by a federal audit agency, or by the internal auditor of a governmental body, until the final audit report is released. Once the final audit is released, the working papers supporting the conclusions become subject to disclosure. Internal investigations may also qualify during the pendency of the investigation.',
        'key_terms': json.dumps(['audit', 'working papers', 'state auditor', 'internal audit', 'examination', 'investigation', 'audit report', 'financial audit', 'compliance audit']),
        'counter_arguments': json.dumps([
            'Once the final audit report is released, this exception no longer applies and working papers supporting the report\'s conclusions should be disclosed',
            'Challenge whether the records are truly "working papers" or are final documents that preexisted the audit',
            'Documents that were public before the audit began do not become protected merely because auditors reviewed them',
            'The audit must be a real, ongoing audit by a recognized audit body — informal reviews by staff do not qualify',
            'Challenge whether the final audit has been completed — if so, the working papers should be releasable',
            'Factual data and source documents used by auditors that are independently public records do not become protected by virtue of the audit process',
        ]),
        'notes': 'The exception is explicitly time-limited to the pendency of the audit. Tex. Gov\'t Code § 321.019 provides additional protections for working papers of the state auditor. The AG has held that the exception expires upon issuance of the final report.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.117',
        'exemption_number': '§ 552.117',
        'short_name': 'Personal Information — Home Address, Phone, SSN (Public Generally)',
        'category': 'privacy',
        'description': 'Excepts certain personal identifying information of individuals — including home address, home telephone number, social security number, and emergency contact information — from mandatory disclosure when held by any governmental body. This applies to both employees and private individuals whose information is in government records.',
        'scope': 'Information that relates to the home address, home telephone number, emergency contact information, and social security number of a current or former elected or appointed official, or of a peace officer, as well as any person who requests nondisclosure of their information under § 552.024(c). Unlike § 552.114 (employees), this provision extends to elected officials and individuals who opt out of disclosure under § 552.024.',
        'key_terms': json.dumps(['home address', 'home phone', 'social security number', 'SSN', 'emergency contact', 'elected official', 'appointed official', 'peace officer', 'personal information', 'nondisclosure request']),
        'counter_arguments': json.dumps([
            'Only the specifically listed categories (home address, home phone, SSN, emergency contact) are protected — other personal information is not covered',
            'Official address, official contact information, and professional credentials are not covered by this exception',
            'Challenge whether the person has actually requested nondisclosure under § 552.024(c) — the opt-out protection only applies to those who actually filed a nondisclosure request',
            'Information the person has voluntarily placed in the public domain is not protected',
            'Professional or official-capacity contact information used in the performance of public duties is not personal information under this section',
            'Aggregate or de-identified data does not implicate individual privacy interests',
        ]),
        'notes': 'This exception works in tandem with § 552.024, which establishes the mechanism for public officials and employees to request nondisclosure of their personal information. The two provisions together create a framework where covered individuals can protect their home contact information by affirmatively requesting nondisclosure. See Tex. Gov\'t Code § 552.024(c).',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.130',
        'exemption_number': '§ 552.130',
        'short_name': 'Motor Vehicle Records',
        'category': 'privacy',
        'description': 'Excepts information obtained from motor vehicle records, including personal information defined under the federal Driver\'s Privacy Protection Act (DPPA), 18 U.S.C. § 2721.',
        'scope': 'Information obtained from motor vehicle records as defined by the DPPA, including name, address, telephone number, and other personal information contained in motor vehicle records. The exception tracks the DPPA\'s permitted uses and exceptions, including disclosures for law enforcement, safety recalls, and research.',
        'key_terms': json.dumps(['motor vehicle records', 'driver\'s license', 'vehicle registration', 'DPPA', 'Driver\'s Privacy Protection Act', 'personal information', 'DPS records', 'license plate']),
        'counter_arguments': json.dumps([
            'The DPPA has 14 enumerated permissible uses — if your purpose qualifies, the information must be disclosed',
            'Information not defined as personal information under the DPPA (e.g., vehicle identification numbers, registration status) may not be protected',
            'Challenge whether the specific records sought contain personal information as defined under the DPPA or are merely vehicle-related records',
            'Aggregate statistical data and de-identified information are not covered',
            'Research, journalism, and public safety are recognized DPPA permissible purposes that may entitle requesters to access',
        ]),
        'notes': 'This exception incorporates federal DPPA requirements by reference. Because both state and federal law apply, challenges must address the DPPA framework. The Texas DPS also has separate rules governing motor vehicle record access under Tex. Transp. Code § 730.005.',
    },
    {
        'jurisdiction': 'TX',
        'statute_citation': 'Tex. Gov\'t Code § 552.148',
        'exemption_number': '§ 552.148',
        'short_name': 'Personal Information of Minors',
        'category': 'privacy',
        'description': 'Excepts certain personal information about a minor child, including name, sex, age, address, and phone number, in records held by a governmental body.',
        'scope': 'Personal information of minor children, specifically name, sex, age, educational information, name and address of a parent or guardian, and other personal information about a minor that the governmental body determines could endanger the health or safety of the minor. Applies broadly to records held by any governmental body.',
        'key_terms': json.dumps(['minor', 'child', 'juvenile', 'personal information', 'age', 'educational', 'parent', 'guardian', 'safety', 'health']),
        'counter_arguments': json.dumps([
            'Aggregate or de-identified data about minors is not protected',
            'Information about minors who have been identified in public proceedings (e.g., a minor tried as an adult) may not be protected',
            'Once a minor reaches adulthood, the protection for their personal information may change',
            'Challenge whether the specific information sought actually falls within the listed categories',
            'Programmatic data about services provided to minors (without individual identification) is generally public',
            'Government body must demonstrate an actual safety or privacy concern, not assert a blanket exemption for all records involving minors',
        ]),
        'notes': 'This exception reflects Texas\'s strong interest in protecting child safety. It is separate from the FERPA-based protection in § 552.112 and applies more broadly to any governmental body holding personal information about minors, not just educational institutions.',
    },
]


def main():
    start = time.time()
    conn = db_connect(DB_PATH)
    added = 0
    skipped = 0
    errors = 0

    try:
        for exemption in TX_EXEMPTIONS:
            # Check if already exists
            existing = conn.execute(
                'SELECT id FROM exemptions WHERE jurisdiction = ? AND statute_citation = ?',
                (exemption['jurisdiction'], exemption['statute_citation'])
            ).fetchone()

            if existing:
                # Update
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

        conn.commit()
    except Exception as e:
        errors += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    print(f'Texas TPIA exemptions: {added} added, {skipped} updated, {errors} errors')
    write_receipt(script='build_tx_exemptions', added=added, skipped=skipped, errors=errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
