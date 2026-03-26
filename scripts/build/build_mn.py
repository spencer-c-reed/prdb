#!/usr/bin/env python3
"""Build Minnesota Government Data Practices Act data classifications, rules, and templates.

Minnesota Statutes Chapter 13 — Government Data Practices Act (MGDPA).
Minnesota's law is NOT an exemptions-based system. It classifies government data
into categories: public, private, confidential, nonpublic, and protected nonpublic.
Default for data on individuals is private; default for other government data is public.
This is a fundamental structural difference from traditional FOIA laws.

Run: python3 scripts/build/build_mn.py
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest.utils.dedup import db_connect
from ingest.utils.receipt import write_receipt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'prdb.db')


# In Minnesota, "exemptions" are really data classifications. We store them as
# exemptions for DB consistency but the descriptions reflect MN's classification
# framework. Each entry explains the classification category and what data falls into it.
MN_EXEMPTIONS = [
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.02, subd. 15; § 13.03',
        'exemption_number': '§ 13.03',
        'short_name': 'Public Data — Default for Non-Individual Data',
        'category': 'classification',
        'description': 'Government data that is not classified as private, confidential, nonpublic, or protected nonpublic is public data and must be made available to any person upon request. Public data is the default classification for data not about individuals.',
        'scope': 'All government data not classified otherwise is public. This includes most government operational records, contracts, financial records, meeting minutes, and policies. Government bodies must actively make public data available and cannot require requesters to explain their purpose. This is the baseline presumption for non-individual data under the MGDPA.',
        'key_terms': json.dumps([
            'public data', 'default classification', 'open to all', 'no purpose required',
            'government records', 'operational records', 'non-individual data',
        ]),
        'counter_arguments': json.dumps([
            'If a government body claims data is not public, it must identify the specific statutory authority for the classification',
            'The MGDPA places the burden on the government to justify non-public classification',
            'Data cannot be reclassified from public to private without legislative authority',
            'Challenge whether the classification authority cited actually applies to the specific data requested',
            'Operational data, financial data, and policy data about government functions — not individuals — is presumptively public',
        ]),
        'notes': 'Under the MGDPA, the concept of "default public" applies to data that is not about individuals. Data about individuals defaults to private unless classified as public by statute. This is the opposite presumption from most state FOIA laws for individual data. See Minn. Stat. § 13.03 for the access procedures for public data.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.02, subd. 12; § 13.04',
        'exemption_number': '§ 13.02, subd. 12',
        'short_name': 'Private Data on Individuals',
        'category': 'privacy',
        'description': 'Private data on individuals is accessible only to the subject of the data, to people whose work assignment reasonably requires access, and to others authorized by law or the subject\'s consent. Private data is not available to the public.',
        'scope': 'Data about individuals that is not public. Private data includes Social Security numbers, home addresses (for certain employees), medical and health data, financial data about individuals, welfare and assistance records, and data specifically classified as private by statute. The classification applies to identifiable data about a natural person. Government bodies may share private data internally on a need-to-know basis.',
        'key_terms': json.dumps([
            'private data', 'individual data', 'Social Security number', 'medical data',
            'financial data', 'personal information', 'identifiable', 'subject of data',
        ]),
        'counter_arguments': json.dumps([
            'The subject of private data has the right to access their own data under § 13.04',
            'Government bodies must identify the specific statute that classifies the data as private',
            'Aggregate or de-identified data that cannot identify individuals may be public',
            'Data about an individual\'s role as a public employee in their official capacity is often public under § 13.43',
            'Challenge whether the data is truly "about" an individual or is instead operational/institutional data',
            'The requestor can appeal to the Information Policy Analysis Division (IPAD) of MN IT Services',
        ]),
        'notes': 'Private data is the default classification for most data about individuals under the MGDPA (§ 13.02, subd. 12). Unlike most state FOIA laws, Minnesota classifies individual data as private unless a statute makes it public. The subject of the data always has the right to access their own private data.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.02, subd. 3; § 13.02, subd. 8',
        'exemption_number': '§ 13.02, subd. 3 & 8',
        'short_name': 'Confidential and Protected Nonpublic Data',
        'category': 'confidential',
        'description': 'Confidential data is inaccessible to the public AND to the subject of the data. Protected nonpublic data is inaccessible to the public but not classified as confidential. Both require specific statutory authority.',
        'scope': 'Confidential data (subd. 3): accessible only to the government entity and persons authorized by law — not even the subject may access it. Examples include active criminal investigation data, certain child abuse reporting data, and security-sensitive information. Protected nonpublic data (subd. 8): data not on individuals that is not public, accessible only to those with a statutory right. Must be specifically authorized by statute.',
        'key_terms': json.dumps([
            'confidential data', 'protected nonpublic', 'active investigation',
            'security information', 'not accessible to subject', 'statutory authority required',
        ]),
        'counter_arguments': json.dumps([
            'Confidential classification requires specific statutory authority — agencies cannot self-classify data as confidential',
            'Challenge whether the specific statute cited actually authorizes confidential classification for this data type',
            'Active investigation status may change — once an investigation closes, the data may become accessible',
            'Even confidential data may be subject to disclosure in judicial proceedings or to oversight bodies',
            'The government must identify the exact statutory provision authorizing confidential treatment for each record type',
        ]),
        'notes': 'Confidential classification is the most restrictive — it bars even the data subject from access. This is used for active criminal investigations (§ 13.82) and child abuse reporting (§ 626.556). Confidential data must be specifically authorized by statute; agencies cannot create confidential classifications by policy.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.02, subd. 9',
        'exemption_number': '§ 13.02, subd. 9',
        'short_name': 'Nonpublic Data',
        'category': 'classification',
        'description': 'Nonpublic data is data not on individuals that is not public and is accessible only to the government entity and persons authorized by law.',
        'scope': 'Data about entities or operations (not about specific individuals) that is not public due to specific statutory classification. Examples include certain trade secret information submitted to agencies, security plans, and competitive bid data before opening. Unlike confidential or private data, nonpublic data is about government operations or submitted business information, not individual persons.',
        'key_terms': json.dumps([
            'nonpublic data', 'non-individual data', 'government operations',
            'business information', 'trade secrets', 'security plans',
        ]),
        'counter_arguments': json.dumps([
            'Nonpublic classification requires specific statutory authority',
            'Challenge whether the data is truly "not on individuals" or actually contains individual-level data',
            'General operational data about government functions is presumptively public',
            'After a transaction concludes (e.g., bid opening, contract award), formerly nonpublic data may become public',
        ]),
        'notes': 'Nonpublic is the classification for non-individual data that is not public. It is distinct from "private" (individual data) and "confidential" (even more restricted). Most commonly applied to trade secrets, security plans, and sealed bid data.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.43',
        'exemption_number': '§ 13.43',
        'short_name': 'Personnel Data — Largely Public in Minnesota',
        'category': 'personnel',
        'description': 'Minnesota treats most public employee personnel data as PUBLIC — a major distinction from most states. Public includes: name, employee ID, actual gross salary, salary range, contract fees, actual gross pension, terms and conditions of employment, job description, education and training background, previous work experience, date of first and last employment, position, work location, and work phone number.',
        'scope': 'Section 13.43 creates an extensive list of public employee data — far more disclosure-friendly than most state personnel exemptions. Public data on public employees includes name, title, compensation, work location, education, employment dates, and more. Private data on employees includes home address, personal phone, medical records, performance evaluations (during employment), and disciplinary data for offenses that did not result in discipline. Final disciplinary action is public.',
        'key_terms': json.dumps([
            'public employee', 'personnel data', 'salary public', 'name public',
            'final disciplinary action', 'work location', 'job description',
            'compensation public', 'terms and conditions',
        ]),
        'counter_arguments': json.dumps([
            'Minnesota is among the most disclosure-friendly states for public employee data — use this proactively',
            'Final disciplinary action, including any resulting suspension or termination, is public under § 13.43',
            'Compensation data including actual gross salary and benefits is fully public',
            'An agency cannot claim personnel privacy for the public categories enumerated in § 13.43',
            'Work location and official contact information (work phone, work email) are public',
            'The fact of an investigation into alleged employee misconduct is public under § 13.43, subd. 2(b)',
        ]),
        'notes': 'Minnesota § 13.43 is unusually disclosure-friendly for public employee data. The statute explicitly lists public categories. The fact of an investigation, the final disposition, and any resulting discipline are all public. Home address and personal phone remain private. This is a significant tool for accountability journalism and public oversight.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.82',
        'exemption_number': '§ 13.82',
        'short_name': 'Law Enforcement Data',
        'category': 'law_enforcement',
        'description': 'Law enforcement data has a complex tiered classification under the MGDPA. Some data is public (arrest records, charges, booking data, incident reports after investigation), some is private (ongoing investigation data, victim information), and some is confidential (active undercover operation details).',
        'scope': 'Under § 13.82: arrest data, charges, booking information, and final disposition are public. Active investigation data is confidential while the investigation is ongoing. Victim information is private. Intelligence data about ongoing criminal activity is confidential. Once an investigation concludes, much of the data becomes accessible. The classification shifts as cases move through the criminal justice process.',
        'key_terms': json.dumps([
            'arrest data', 'criminal charges', 'booking information', 'investigation data',
            'active investigation', 'victim information', 'intelligence data',
            'law enforcement records', 'criminal history',
        ]),
        'counter_arguments': json.dumps([
            'Arrest data, charges, and booking information are public under § 13.82, subd. 2',
            'Once an investigation is closed, the active-investigation confidential classification dissolves',
            'Request the case disposition and final investigation report after case closure',
            'The government bears the burden of showing an investigation remains active to justify confidential classification',
            'Use-of-force data and officer discipline are public under § 13.43 and Law Enforcement Agency Report Act',
            'Challenge whether "active investigation" status is being used as a pretext to withhold closed case data',
        ]),
        'notes': 'Minnesota § 13.82 is one of the more complex provisions in the MGDPA. The tiered classification requires tracking where in the criminal justice process the case sits. The IPAD (Information Policy Analysis Division) has issued numerous advisory opinions on law enforcement data classification.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.384; § 144.291 et seq.',
        'exemption_number': '§ 13.384',
        'short_name': 'Medical Data',
        'category': 'privacy',
        'description': 'Medical data about patients and health care recipients maintained by a government entity is classified as private. Includes diagnoses, treatment records, prescription information, and related health data.',
        'scope': 'Medical, dental, and health data maintained by government bodies about individuals. This includes treatment records at public hospitals and clinics, public health records identifying individuals, and similar data. Aggregate statistical health data without individual identifiers is public. Minnesota Health Records Act (§ 144.291 et seq.) provides additional patient data protections.',
        'key_terms': json.dumps([
            'medical data', 'health records', 'patient data', 'diagnosis', 'treatment',
            'prescription', 'mental health', 'public hospital', 'health care',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and epidemiological data without individual identifiers are public',
            'Government health program descriptions, budgets, and policies are public',
            'Data about the subject of the records is accessible to that person under § 13.04',
            'Challenge whether the data truly identifies individuals vs. describes population-level health trends',
        ]),
        'notes': 'Minnesota medical data privacy is reinforced by both the MGDPA and the Minnesota Health Records Act. The overlap between state and federal HIPAA protections is significant — most government-held medical records would be protected under both frameworks.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.32',
        'exemption_number': '§ 13.32',
        'short_name': 'Educational Data',
        'category': 'privacy',
        'description': 'Educational data on students maintained by a government educational agency is classified as private. Includes student records, grades, disciplinary records, and education-related assessments.',
        'scope': 'Student education records maintained by public schools, colleges, and universities. Covers grades, transcripts, disciplinary records, and educational assessments. This aligns with and is reinforced by the federal Family Educational Rights and Privacy Act (FERPA). Public aggregate data about school performance is public; individual student records are private.',
        'key_terms': json.dumps([
            'student data', 'education records', 'grades', 'transcript', 'disciplinary records',
            'FERPA', 'school records', 'student assessment',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate school performance data, testing scores at the school level, and institutional records are public',
            'Faculty and staff employment records at public universities are governed by § 13.43, not § 13.32',
            'Former students retain privacy rights in their records under both FERPA and § 13.32',
            'Challenge whether the records are truly about individual students or describe institutional programs and policies',
        ]),
        'notes': 'Minnesota § 13.32 must be read alongside FERPA. Government educational institutions have a dual obligation under both state and federal law. Institutional records about programs, budgets, and administration (not individual students) are public.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.46',
        'exemption_number': '§ 13.46',
        'short_name': 'Welfare and Assistance Data',
        'category': 'privacy',
        'description': 'Data about recipients of public assistance programs, welfare benefits, or social services is classified as private. Includes data about public housing, food assistance, Medicaid, and similar programs.',
        'scope': 'Data maintained by government agencies about individuals receiving public assistance, welfare benefits, or social services. Includes SNAP, Medicaid, housing assistance, and similar program data. The identities of recipients and their specific benefit details are private. General program data and aggregate statistics about assistance programs are public.',
        'key_terms': json.dumps([
            'public assistance', 'welfare', 'benefit recipient', 'Medicaid', 'SNAP',
            'housing assistance', 'social services', 'recipient data',
        ]),
        'counter_arguments': json.dumps([
            'Program-level data about the administration of assistance programs is public',
            'Aggregate statistics about benefit recipients without individual identification are public',
            'Government expenditures on assistance programs are public financial data',
            'Challenge whether the data identifies specific individuals vs. describes program operations',
        ]),
        'notes': 'Minnesota has strong protections for assistance recipient privacy to encourage program participation without stigma. Program effectiveness data and aggregate reporting are public. Individual benefit records are private.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.02, subd. 3; § 13.37',
        'exemption_number': '§ 13.37',
        'short_name': 'Security Information',
        'category': 'security',
        'description': 'Security plans, emergency response plans, vulnerability assessments, and similar security-sensitive information maintained by government bodies is nonpublic data.',
        'scope': 'Security information including: plans designed to protect from sabotage or criminal activity, emergency response plans, facility security plans, and critical infrastructure vulnerability assessments. The exemption reflects concerns about disclosing weaknesses that could be exploited. Must be directly related to actual security, not general operational plans.',
        'key_terms': json.dumps([
            'security information', 'vulnerability assessment', 'emergency response plan',
            'sabotage', 'critical infrastructure', 'facility security', 'security plan',
        ]),
        'counter_arguments': json.dumps([
            'General emergency management policies that do not reveal specific vulnerabilities may be public',
            'After-action reports about past security incidents may be less sensitive than current plans',
            'Budget and resource information about security programs may be separable from tactical security details',
            'Challenge whether the specific information reveals current exploitable vulnerabilities or is just historical',
        ]),
        'notes': 'Minnesota § 13.37 was expanded after 9/11. The statute requires that the security information be "not necessary for the public to have" and that its release "would pose a serious risk." General security policies and non-tactical emergency plans may remain public.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.591',
        'exemption_number': '§ 13.591',
        'short_name': 'Trade Secret and Proprietary Data',
        'category': 'commercial',
        'description': 'Trade secret information and other proprietary data submitted by private entities to government bodies is classified as nonpublic.',
        'scope': 'Trade secrets and proprietary business data submitted to government agencies in connection with permits, applications, compliance filings, and similar submissions. The submitter must claim trade secret status at the time of submission. Government-generated analysis of the submitted data is not itself a trade secret. Financial terms of public contracts reflect public expenditures and are generally not protected.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary data', 'confidential business information',
            'competitive information', 'submitted data', 'permit application',
        ]),
        'counter_arguments': json.dumps([
            'Trade secret status must be claimed at the time of submission — post-hoc claims may not qualify',
            'Government-generated analysis of private submissions is not a trade secret',
            'Financial terms of public contracts are generally public as they reflect expenditure of public funds',
            'Information publicly available elsewhere cannot qualify as a trade secret',
            'Challenge the government body to independently verify trade secret status rather than deferring to the submitter',
        ]),
        'notes': 'Minnesota § 13.591 requires that trade secret claims be made at the time data is submitted to the government. IPAD has issued advisory opinions clarifying that government bodies must independently evaluate trade secret claims and cannot simply rubber-stamp submitter designations.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.601; § 175.10',
        'exemption_number': '§ 13.601',
        'short_name': 'Financial Institution and Tax Data',
        'category': 'privacy',
        'description': 'Financial data about individuals — including tax records, financial institution examination data, and individual financial circumstances — is private data.',
        'scope': 'Individual financial data maintained by government agencies including: tax return information, financial institution examination records, individual financial circumstances in assistance applications, and similar data. Financial data about government entities and government expenditures is public. The exemption covers individual financial privacy, not government financial transparency.',
        'key_terms': json.dumps([
            'financial data', 'tax records', 'financial institution', 'individual finances',
            'bank examination', 'income information', 'financial circumstances',
        ]),
        'counter_arguments': json.dumps([
            'Government financial records — budgets, expenditures, contracts — are public',
            'Aggregate financial data without individual identification is public',
            'Public employee compensation is public under § 13.43 regardless of this provision',
            'Challenge whether the financial data is truly about individuals vs. about government operations',
        ]),
        'notes': 'Individual financial privacy is a core MGDPA protection. Contrast with government financial transparency: public budgets, contracts, and expenditures are fully public. The exemption protects private citizens\' financial information, not the government\'s own finances.',
    },
    {
        'jurisdiction': 'MN',
        'statute_citation': 'Minn. Stat. § 13.40',
        'exemption_number': '§ 13.40',
        'short_name': 'Attorney-Client and Work Product',
        'category': 'deliberative',
        'description': 'Attorney-client communications between a government body and its legal counsel, and attorney work product prepared in anticipation of litigation, are protected as nonpublic or confidential data.',
        'scope': 'Confidential communications between a government entity and its attorneys seeking or providing legal advice, and work product prepared in anticipation of litigation or administrative proceedings. The privilege operates similarly to the private-party attorney-client privilege but is subject to the MGDPA\'s classification framework. Final legal determinations that guide agency policy may lose protection.',
        'key_terms': json.dumps([
            'attorney-client', 'work product', 'legal advice', 'litigation preparation',
            'privileged communication', 'legal counsel', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'Not all communications with attorneys are privileged — communications must seek or provide legal advice',
            'Factual information conveyed to an attorney does not become privileged simply by being in a legal memo',
            'Final legal determinations adopted as agency policy may lose protection',
            'Work product applies only to documents prepared for litigation, not routine legal correspondence',
            'The privilege may be waived if the communication was disclosed to third parties',
        ]),
        'notes': 'Minnesota § 13.40 codifies attorney-client and work product protection in the MGDPA context. IPAD advisory opinions have addressed the scope of government attorney-client privilege, consistent with the general principle that public bodies cannot use the privilege to shield policy decisions from disclosure.',
    },
]


MN_RULES = [
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'response_for_inspection',
        'param_value': 'immediate',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.03, subd. 2(a)',
        'notes': 'A government entity must respond immediately to a request to inspect public data. If the data is not immediately available, the entity must provide it within a "reasonable time." For requests to inspect (not copy) public data, the government cannot impose a waiting period. This is one of the most immediate access requirements among all state public records laws.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'response_for_copies',
        'param_value': 'appropriate_and_prompt',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.03, subd. 2(a)',
        'notes': 'For requests for copies of public data, the government must respond "appropriately and promptly." There is no specific day count for copy requests, unlike most state FOIA laws. "Appropriate and prompt" is interpreted based on the volume and complexity of the request. In practice, government bodies typically aim for a few business days for routine requests. Courts have found that weeks-long delays for routine requests violate the statute.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'fee_cap',
        'param_key': 'copying_fee',
        'param_value': 'actual_cost',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.03, subd. 3(c)',
        'notes': 'Government bodies may charge a fee for copies of public data that does not exceed the actual cost of searching for and retrieving the data, including the cost of duplication. No markup above actual cost is permitted. The fee may not include programming time if the data already exists in accessible form. Unlike Michigan\'s $0.10/page cap, Minnesota\'s fee is based on actual cost with no fixed per-page maximum.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'fee_cap',
        'param_key': 'no_fee_for_inspection',
        'param_value': 'no_fee',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.03, subd. 3(a)',
        'notes': 'Inspection of public data must be provided without charge. A fee may only be charged for copies, not for viewing records. This is an important distinction — requesters can inspect records for free and decide what to copy.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'appeal_deadline',
        'param_key': 'appeal_to_ipad',
        'param_value': 'commissioner_of_administration',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.085',
        'notes': 'A person denied access to government data may request a data practices compliance opinion from the Information Policy Analysis Division (IPAD), which is part of Minnesota IT Services (MNIT). Previously this was under the Commissioner of Administration. IPAD issues advisory opinions on data practices questions. While advisory opinions are not legally binding, they carry persuasive authority and government bodies typically comply.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'appeal_deadline',
        'param_key': 'district_court_appeal',
        'param_value': 'after_ipad_or_direct',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.08',
        'notes': 'A person aggrieved by a violation of the MGDPA may bring a civil action in district court. Court action may be brought after seeking an IPAD opinion or directly. Courts may grant injunctive relief requiring access to data. An IPAD opinion is not a prerequisite to court action but as a practical matter requesters often seek an IPAD opinion first because it is faster and free.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'no_statutory_fee_award',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.08',
        'notes': 'Minnesota\'s MGDPA does not include an attorney\'s fees provision for prevailing requesters — unlike Michigan FOIA (mandatory fees) and Washington PRA (mandatory fees). This is a significant gap. A requester who wins in court does not automatically recover attorney fees. Some requesters have argued for fees under Minnesota\'s general fee-shifting provisions, but the statute does not expressly authorize it.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'damages',
        'param_value': 'actual_damages_plus_punitive',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.08, subd. 1',
        'notes': 'A person who suffers harm as a result of a violation of the MGDPA may recover actual damages, punitive damages up to $15,000 if the violation was willful, and costs of the action including reasonable attorney fees. The $15,000 punitive cap and actual damages provision provide a meaningful remedy for willful violations.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'responsible_authority_required',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.02, subd. 16; § 13.05',
        'notes': 'Every government body must designate a "Responsible Authority" who is responsible for implementing the MGDPA and responding to data requests. The Responsible Authority must prepare public documents, provide access to public data, and ensure the entity\'s data practices comply with the MGDPA. Requesters should direct their requests to the Responsible Authority.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'data_practices_policy_required',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.025',
        'notes': 'Government bodies must prepare and make publicly available a data practices policy describing the types of data they maintain, the classifications of that data, and the procedures for requesting data. This policy must be publicly available and updated regularly. Requesters should review the entity\'s data practices policy before submitting a request to identify what data exists and how it is classified.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'purpose_not_required',
        'param_value': 'no_purpose_required',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.03, subd. 1',
        'notes': 'Requesters of public data are not required to provide a reason for the request. The government cannot require requesters to identify their purpose or justify why they want public data. A government body that conditions access to public data on the requester\'s stated purpose is violating the MGDPA.',
    },
    {
        'jurisdiction': 'MN',
        'rule_type': 'initial_response',
        'param_key': 'subject_access_rights',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'Minn. Stat. § 13.04',
        'notes': 'The subject of private data on an individual always has the right to access, correct, and supplement their own data maintained by a government entity. The entity must inform the subject of: what data it maintains, how the data is used, who has access to the data, and whether providing data is mandatory or voluntary. These rights exist regardless of whether the data is public or private.',
    },
]


MN_TEMPLATES = [
    {
        'jurisdiction': 'MN',
        'record_type': 'general',
        'template_name': 'General Minnesota Government Data Practices Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Responsible Authority
{{agency_name}}
{{agency_address}}

Re: Request for Government Data Under Minnesota Government Data Practices Act, Minn. Stat. Ch. 13

Dear Responsible Authority:

[Note: Minnesota law is different from most states. Data is classified as "public," "private," "nonpublic," "protected nonpublic," or "confidential." Public data must be made available to any person. There is no requirement to state a purpose for requesting public data.]

Pursuant to the Minnesota Government Data Practices Act, Minn. Stat. Chapter 13, I request access to and copies of the following government data, which I believe is classified as public data:

{{description_of_data}}

I am requesting data for the period {{date_range_start}} through {{date_range_end}}.

Under Minn. Stat. § 13.03, subd. 2(a), the government entity must respond immediately to requests to inspect public data, and must provide copies "appropriately and promptly." I request that you respond promptly.

I am not required to state a purpose for this request under Minn. Stat. § 13.03, subd. 1.

If you provide copies, I understand that fees may not exceed the actual cost of searching for, retrieving, and copying the data under Minn. Stat. § 13.03, subd. 3(c). Inspection of public data must be provided without charge under subd. 3(a).

If you believe any portion of the requested data is not public, I ask that you:
(1) Identify the specific statutory provision under Chapter 13 that classifies the data as private, nonpublic, protected nonpublic, or confidential;
(2) Release all portions of the data that are public; and
(3) Advise me of my right to seek a data practices compliance opinion from the Information Policy Analysis Division (IPAD) under Minn. Stat. § 13.085.

I prefer to receive data in electronic format where available, including as structured data (CSV, JSON, or Excel) for any data maintained in database format.

If you have questions about this request, please contact me at {{requester_email}} or {{requester_phone}}.

Sincerely,
{{requester_name}}

[Strategic note: Minnesota data requests go to the "Responsible Authority," not a "Records Access Officer" or "FOIA Officer." The MGDPA uses the term "data" rather than "records" throughout.]''',
        'fee_waiver_language': '''I request that fees be waived or minimized for the following reasons:

Under Minn. Stat. § 13.03, subd. 3(a), inspection of public data is provided without charge. I am willing to inspect the data in person at your offices if that reduces costs.

For copies, I understand that fees must not exceed actual costs under § 13.03, subd. 3(c). I ask that you: (1) provide data in electronic format at no more than the cost of the electronic medium; and (2) waive any programming or staff time charges if the data already exists in accessible form, as the statute does not permit charging for the cost of making retrievable data accessible.

If you believe fees will exceed ${{fee_threshold}}, please provide a written estimate before processing so I may determine whether to narrow my request or review the data in person.''',
        'expedited_language': '''I request that this data request be processed on an expedited basis. Under Minn. Stat. § 13.03, subd. 2(a), the government entity must respond "appropriately and promptly" to requests for public data.

I need the requested data by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

The statute requires immediate response for inspection requests. I am available to inspect the data in person immediately if that is faster than producing copies.''',
        'notes': 'Minnesota MGDPA requests use different terminology than typical FOIA requests: "data" not "records," "Responsible Authority" not "FOIA Coordinator," "public data" not "public records," "data classification" not "exemptions." There is no specific response day count for copies (unlike most states) — the standard is "appropriate and prompt." Requesters may appeal to IPAD for a free advisory opinion before filing in district court.',
    },
    {
        'jurisdiction': 'MN',
        'record_type': 'appeal',
        'template_name': 'Minnesota MGDPA Request for IPAD Compliance Opinion',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Information Policy Analysis Division (IPAD)
Minnesota IT Services (MNIT)
658 Cedar Street
St. Paul, MN 55155
(Or submit electronically via the IPAD website)

Re: Request for Data Practices Compliance Opinion
    Government Entity: {{agency_name}}
    Date of Original Data Request: {{original_request_date}}

To the Information Policy Analysis Division:

Pursuant to Minn. Stat. § 13.085, I request a data practices compliance opinion regarding the following situation:

BACKGROUND

On {{original_request_date}}, I submitted a request to {{agency_name}} for the following data:

{{description_of_data}}

On {{response_date}}, {{agency_name}} {{description_of_denial}}.

ISSUE

The issue I am presenting is: {{specific_question_for_ipad}}

Specifically, I request an opinion on whether the following data is public under the Minnesota Government Data Practices Act, Minn. Stat. Chapter 13:

{{data_description}}

RELEVANT STATUTORY PROVISIONS

[If applicable]: I believe the requested data is public under:
- Minn. Stat. § 13.03 (public data access)
- Minn. Stat. § 13.43 (public employee data — if personnel records at issue)
- Minn. Stat. § 13.82 (law enforcement data — if applicable)
- [Other applicable sections]

The government entity has asserted that the data is classified as {{claimed_classification}} under {{claimed_statute}}. I dispute this classification because {{challenge_grounds}}.

REQUESTED RELIEF

I request that IPAD issue an opinion that:
(1) The requested data is public data under the MGDPA;
(2) {{agency_name}} is required to provide access to the data; and
(3) Any other relief IPAD determines is appropriate.

I have attached copies of: my original data request, the government entity\'s response, and any other relevant correspondence.

Respectfully submitted,
{{requester_name}}
Date: {{date}}

[Note: An IPAD opinion is advisory, not binding, but government bodies typically comply. IPAD opinions are faster and free compared to district court action. IPAD opinions are public and may influence future data practices across Minnesota government. After receiving an IPAD opinion, a requester may still file in district court if necessary under Minn. Stat. § 13.08.]''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'IPAD (Information Policy Analysis Division) advisory opinions are the Minnesota equivalent of an administrative appeal, though they are not legally required before filing in court. IPAD is part of Minnesota IT Services (MNIT). Opinions are free, public, and typically issued within 30-60 days. Unlike most state FOIA appeals, there is no mandatory timeline for IPAD to respond. The lack of mandatory attorney fee recovery under § 13.08 makes the IPAD opinion route attractive as a lower-cost alternative to litigation.',
    },
    {
        'jurisdiction': 'MN',
        'record_type': 'personnel_records',
        'template_name': 'Minnesota MGDPA — Public Employee Data Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Responsible Authority
{{agency_name}}
{{agency_address}}

Re: Request for Public Employee Data Under Minn. Stat. § 13.43

Dear Responsible Authority:

Pursuant to the Minnesota Government Data Practices Act, Minn. Stat. Chapter 13, and specifically § 13.43, I request the following public employee data:

Employee name / position: {{employee_name_or_position}}
Agency / department: {{department}}
Date range (if applicable): {{date_range_start}} through {{date_range_end}}

Under Minn. Stat. § 13.43, subd. 2, the following data about public employees is public and must be provided:
- Employee name
- Employee ID number
- Actual gross salary
- Salary range
- Terms and conditions of employment
- Contract fees
- Actual gross pension
- Cost of fringe benefits
- Job description
- Education and training background
- Previous work experience
- Date of first and last employment
- The existence and status of any complaints or charges against the employee (fact of investigation)
- Final disposition of any disciplinary action taken, including the specific reasons for the action
- Work location and work telephone number

I specifically request: {{specific_data_requested}}

Note on Final Disciplinary Action: Under § 13.43, subd. 2(b), the final outcome of any disciplinary proceeding, including the specific reasons for disciplinary action, is public. Please provide any final disciplinary records related to the above employee for the specified period.

If you believe any requested data is not public, please identify the specific provision of Chapter 13 that classifies it otherwise. Do not withhold public employee data categories that are expressly enumerated as public in § 13.43, subd. 2.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Minnesota § 13.43 is unusually comprehensive in classifying public employee data as public. Salary, title, compensation, employment dates, work location, and final disciplinary actions are all explicitly public. This is one of the most disclosure-friendly public employee data statutes in the country. Use this section explicitly when making employee data requests to preempt overbroad privacy claims.',
    },
]


def build_exemptions(conn):
    added = 0
    skipped = 0
    for ex in MN_EXEMPTIONS:
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
    for rule in MN_RULES:
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
    for tmpl in MN_TEMPLATES:
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
        print(f'MN MGDPA classifications: {ea} added, {es} updated')
        print(f'MN MGDPA rules:           {ra} added, {rs} updated')
        print(f'MN MGDPA templates:       {ta} added, {ts} updated')
    except Exception as e:
        totals['errors'] += 1
        print(f'Error: {e}', file=sys.stderr)
    finally:
        conn.close()

    elapsed = time.time() - start
    write_receipt(
        script='build_mn',
        added=totals['added'],
        skipped=totals['skipped'],
        errors=totals['errors'],
        elapsed_s=elapsed,
    )


if __name__ == '__main__':
    main()
