#!/usr/bin/env python3
"""Build Georgia Open Records Act data: exemptions, rules, and templates.

Covers Georgia's Open Records Act (ORA), O.C.G.A. § 50-18-70 et seq.
Georgia's ORA is one of the faster-deadline laws in the country — agencies
must produce records within 3 business days or provide a written description
of records not immediately available. There is no administrative appeal
mechanism; aggrieved requesters must go to superior court. Attorney's fees
and civil and criminal penalties are available. The first 50 pages of certain
copies are free; standard rate is $0.10/page thereafter.

Run: python3 scripts/build/build_ga.py
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
# Georgia Open Records Act, O.C.G.A. § 50-18-70 et seq.
# Georgia's ORA broadly defines "public record" as including all documents
# and other written materials prepared and maintained or received in the
# performance of a service or function by or on behalf of a public agency.
# Section 50-18-72 lists exemptions, and the burden of proving an exemption
# is on the agency. Georgia courts strictly construe exemptions.
# =============================================================================

GA_EXEMPTIONS = [
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(1)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(1)',
        'short_name': 'Law Enforcement Investigatory Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement, prosecution, and regulatory agencies pertaining to pending investigations, criminal proceedings, or matters where the investigation or disposition is not completed, are exempt from disclosure under Georgia\'s ORA.',
        'scope': 'Law enforcement investigation files while the investigation is ongoing and before final disposition of criminal proceedings. The exemption requires: (1) an ongoing investigation or pending prosecution; and (2) that the specific records pertain to that pending matter. Once prosecution concludes or the matter is closed, records generally become public. Arrest records, booking information, and incident reports that document the existence of an incident are generally public even when investigation is pending. Factual portions of investigative files that do not implicate the ongoing investigation may be required to be released.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'pending investigation',
            'O.C.G.A. 50-18-72(a)(1)', 'ongoing investigation', 'criminal proceeding',
            'pending prosecution', 'investigatory record', 'arrest record',
            'law enforcement exemption',
        ]),
        'counter_arguments': json.dumps([
            'Completed investigations and concluded prosecutions do not retain this protection',
            'Arrest records, booking information, and incident reports are generally public',
            'The investigation must be truly "pending" — labeling a closed matter as ongoing does not trigger the exemption',
            'Challenge claims that the exemption covers administrative or regulatory investigations unrelated to criminal proceedings',
            'Factual portions of investigative records that do not reveal ongoing investigation details must be released',
            'Georgia courts strictly construe exemptions — ambiguity goes against withholding',
            'The agency must show that disclosure would specifically harm the pending matter',
        ]),
        'notes': 'Georgia\'s law enforcement investigatory records exemption is strictly construed under O.C.G.A. § 50-18-72(a)(1). Georgia courts have consistently held that completed case files are public. The exemption does not apply to administrative or civil regulatory investigations unless specifically authorized. See Tillman v. Macon County, 288 Ga. App. 160 (2007).',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(4)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(4)',
        'short_name': 'Medical and Personal Health Records',
        'category': 'privacy',
        'description': 'Medical, psychiatric, and similar individually identifiable health information maintained by public agencies is exempt from disclosure under Georgia\'s ORA, consistent with HIPAA and Georgia health privacy laws.',
        'scope': 'Individually identifiable health information including medical records, psychiatric evaluations, disability documentation, and related personal health data. Georgia\'s medical records exemption aligns with HIPAA requirements for protected health information (PHI). Aggregate health data, program statistics, and anonymized information are public. The exemption covers the personal health information of private individuals — it does not protect aggregate data, program budgets, or general health agency records. Records about public employees\' job-related medical conditions may be subject to reduced protection in specific contexts.',
        'key_terms': json.dumps([
            'medical record', 'health information', 'PHI', 'HIPAA',
            'O.C.G.A. 50-18-72(a)(4)', 'health record', 'psychiatric record',
            'disability record', 'patient record', 'personal health',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health data and anonymized public health statistics are public',
            'Program budget and contract records for health agencies are public',
            'Challenge whether the record is truly "medical" or merely involves a health agency',
            'Redaction of identifying information may allow release of the underlying health data',
            'General descriptions of health programs and services are public',
        ]),
        'notes': 'Georgia\'s health records exemption aligns with HIPAA requirements. Georgia courts have held that the exemption covers individually identifiable health data, not general records of health agencies. Aggregate data and program-level information are not protected.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(2)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(2)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or attorney work product doctrine — confidential communications between government attorneys and their client agencies for the purpose of legal advice — are exempt from Georgia\'s ORA.',
        'scope': 'Confidential communications between government agencies and their legal counsel for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege is narrow: it covers legal advice, not general policy or business recommendations. Billing records and financial arrangements with counsel are generally public. Facts independently known by the agency are not privileged merely because communicated to counsel. Waiver occurs through voluntary public disclosure or reliance on the advice in public proceedings.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'O.C.G.A. 50-18-72(a)(2)', 'privileged communication',
            'attorney work product', 'in anticipation of litigation',
            'legal opinion', 'government attorney', 'litigation',
        ]),
        'counter_arguments': json.dumps([
            'Policy and business advice from attorneys is not privileged — only legal advice qualifies',
            'Waiver occurs through public reliance on the legal advice or disclosure to third parties',
            'Billing records are generally public — they describe services, not confidential advice',
            'Facts underlying legal advice are not privileged',
            'Georgia courts apply the privilege narrowly given the ORA\'s strong disclosure mandate',
            'Challenge claims that entire agency communications with counsel are privileged — only specific legal advice portions qualify',
        ]),
        'notes': 'Georgia\'s attorney-client privilege exemption under O.C.G.A. § 50-18-72(a)(2) is interpreted narrowly consistent with the ORA\'s general presumption of openness. Georgia courts require agencies to demonstrate specific privilege for each withheld communication.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(5)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(5)',
        'short_name': 'Deliberative Process — Advice, Recommendations, and Opinions',
        'category': 'deliberative',
        'description': 'Records consisting of advice, recommendations, and opinions reflecting the mental processes of an employee relating to the deliberative process of a public agency — predecisional, deliberative communications — are exempt from Georgia\'s ORA.',
        'scope': 'Internal predecisional deliberative materials where agency employees express opinions or make recommendations about agency decisions. The exemption covers the opinion and recommendation portions of deliberative documents — purely factual information within deliberative documents must be segregated and released. Final agency decisions, adopted policies, and "working law" must be disclosed. The exemption is strictly limited to predecisional material — once a decision is made and adopted, the protection ends. Georgia courts apply the factual/opinion distinction rigorously.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'advice and recommendation',
            'O.C.G.A. 50-18-72(a)(5)', 'mental process', 'intra-agency',
            'policy deliberation', 'working paper', 'draft document',
            'agency opinion', 'internal recommendation',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released',
            'Final agency decisions and adopted policies are fully public',
            '"Working law" — standards the agency actually applies — must be disclosed even if in internal documents',
            'Once a recommendation is adopted as final agency position, the exemption ends',
            'Challenge claims that entire documents are deliberative when only specific recommendation portions qualify',
            'Documents circulated outside the agency may lose their predecisional character',
            'Georgia courts apply the factual/opinion distinction rigorously in ORA cases',
        ]),
        'notes': 'Georgia\'s deliberative process exemption under O.C.G.A. § 50-18-72(a)(5) is applied narrowly. Georgia courts require agencies to specifically identify the opinion/recommendation portions and release factual portions. See Hackworth v. Board of Education, 214 Ga. App. 17 (1994).',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(9); O.C.G.A. § 50-18-72(b)(2)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(9)',
        'short_name': 'Trade Secrets and Proprietary Business Information',
        'category': 'commercial',
        'description': 'Trade secrets as defined by the Georgia Trade Secrets Act and proprietary business information submitted by private entities to Georgia public agencies are exempt from disclosure where disclosure would cause competitive harm.',
        'scope': 'Trade secrets under O.C.G.A. § 10-1-761 (Georgia Trade Secrets Act): information that derives independent economic value from not being generally known and is subject to reasonable measures to maintain secrecy. Government-generated records cannot be trade secrets. The agency must independently evaluate vendor designations. Contract prices, amounts paid with public funds, and government expenditures are public even when vendors claim trade secret protection. Georgia courts require the agency to conduct an independent analysis of trade secret claims.',
        'key_terms': json.dumps([
            'trade secret', 'Georgia Trade Secrets Act', 'O.C.G.A. 10-1-761',
            'O.C.G.A. 50-18-72(a)(9)', 'proprietary information', 'competitive harm',
            'commercial information', 'economic value', 'confidential business information',
            'vendor records', 'contractor information',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds are public regardless of vendor trade secret claims',
            'The submitter must demonstrate that information meets the Georgia Trade Secrets Act definition',
            'The agency must independently evaluate trade secret claims — vendor "confidential" designations are not self-executing',
            'Information required by law to be submitted has reduced secrecy expectations',
            'Government-generated records and analysis are not trade secrets',
            'Publicly available information cannot qualify as a trade secret',
        ]),
        'notes': 'Georgia\'s trade secret exemption applies the Georgia Trade Secrets Act (O.C.G.A. § 10-1-761). Georgia courts require independent agency analysis of trade secret claims. Contract amounts and public expenditures are consistently held to be public. The agency cannot simply defer to vendor designations.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(6)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(6)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related records prepared by or for a public agency in connection with the prospective acquisition of property are exempt from disclosure until the transaction is concluded.',
        'scope': 'Real estate appraisals, feasibility studies, and related valuation documents prepared for government acquisition of real property. The exemption is time-limited — it applies only until the acquisition is complete, abandoned, or the agency withdraws from the transaction. The purpose is to protect the agency\'s negotiating position. Post-transaction, all appraisal records are public. General real property records (deeds, assessments) are always public. The exemption does not cover appraisals of government-owned property not being acquired.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'pre-acquisition',
            'O.C.G.A. 50-18-72(a)(6)', 'property valuation', 'real property',
            'land purchase', 'appraisal record', 'negotiation records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction is complete, cancelled, or abandoned',
            'Challenge the claim that a transaction remains "pending" if there has been no activity for an extended period',
            'Post-transaction, all appraisal and negotiation records are public',
            'General real property records — deeds, tax assessments, ownership history — are always public',
            'Appraisals of property already owned (not being acquired) are not covered',
        ]),
        'notes': 'Georgia\'s pre-acquisition appraisal exemption under O.C.G.A. § 50-18-72(a)(6) is a standard time-limited provision. Georgia courts have narrowly defined its scope to formal appraisals, not general internal discussions about property values.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(11)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(11)',
        'short_name': 'Records of Mediation and Alternative Dispute Resolution',
        'category': 'deliberative',
        'description': 'Records related to mediation and alternative dispute resolution proceedings involving government agencies, including communications made during mediation, are exempt to encourage candid settlement discussions.',
        'scope': 'Records generated in or directly related to mediation proceedings involving a public agency, including mediator notes, communications during mediation sessions, and settlement discussions. The exemption does not cover: final settlement agreements (which are public as government contracts); correspondence prior to mediation; or general dispute records. The purpose is to encourage candid settlement discussions without fear that statements will become public records. Final settlements and consent agreements are public as government contracts.',
        'key_terms': json.dumps([
            'mediation record', 'alternative dispute resolution', 'ADR',
            'O.C.G.A. 50-18-72(a)(11)', 'settlement discussion', 'mediator notes',
            'dispute resolution', 'settlement communication', 'conciliation',
        ]),
        'counter_arguments': json.dumps([
            'Final settlement agreements are public — they are government contracts or dispositions of claims',
            'Pre-mediation correspondence and dispute records are generally public',
            'Challenge whether the dispute resolution process was formal mediation or informal negotiation',
            'The exemption does not cover all settlement-related records — only those generated in the mediation proceeding itself',
        ]),
        'notes': 'Georgia\'s mediation exemption under O.C.G.A. § 50-18-72(a)(11) is designed to encourage candid settlement discussions. Georgia courts have consistently held that final settlement agreements are public government contracts, not protected mediation records.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(3)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(3)',
        'short_name': 'Invasion of Personal Privacy',
        'category': 'privacy',
        'description': 'Records that would constitute an invasion of personal privacy are exempt from Georgia\'s ORA where the public interest in disclosure does not outweigh the privacy interest.',
        'scope': 'Records about private individuals where disclosure would constitute a genuine, substantial invasion of personal privacy — not merely discomfort or inconvenience. Georgia courts apply a balancing test weighing the public interest in disclosure against the individual privacy interest. The exemption is more protective of truly private information (home addresses of private citizens, sensitive personal circumstances) and less protective of information about public officials in their official capacity. The agency bears the burden of demonstrating that the privacy interest is substantial and outweighs the public interest.',
        'key_terms': json.dumps([
            'personal privacy', 'invasion of privacy', 'O.C.G.A. 50-18-72(a)(3)',
            'privacy balancing test', 'private individual', 'personal information',
            'substantial privacy interest', 'unwarranted invasion',
        ]),
        'counter_arguments': json.dumps([
            'Information about public officials in their official capacity rarely satisfies the substantial privacy test',
            'The public interest in government accountability must be weighed against the privacy interest',
            'The agency bears the burden of demonstrating that the privacy interest outweighs the public interest',
            'Discomfort with disclosure or embarrassment is not a sufficient privacy interest',
            'Information voluntarily placed in public documents has reduced privacy protection',
            'Georgia courts apply a genuine balancing test — mere assertions of privacy are insufficient',
        ]),
        'notes': 'Georgia\'s privacy exemption under O.C.G.A. § 50-18-72(a)(3) requires genuine balancing. Georgia courts have held that the exemption applies to truly private personal information about private individuals, not to information about public officials\' exercise of their duties.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(20)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(20)',
        'short_name': 'Infrastructure and Security Vulnerability Records',
        'category': 'safety',
        'description': 'Records that if disclosed would reveal the location of critical infrastructure, security vulnerabilities of critical infrastructure, or emergency response plans for critical infrastructure are exempt under Georgia\'s ORA.',
        'scope': 'Vulnerability assessments, security plans, and related records for critical public infrastructure — water systems, power grids, telecommunications, and emergency response systems. The exemption requires a specific, articulable security risk from disclosure. Budget records, general program descriptions, and contracts for infrastructure security (excluding technical specifications) are public. The agency must demonstrate specific harm from disclosing each withheld record, not assert a general "security" category.',
        'key_terms': json.dumps([
            'critical infrastructure', 'security vulnerability', 'infrastructure security',
            'O.C.G.A. 50-18-72(a)(20)', 'security plan', 'emergency response plan',
            'vulnerability assessment', 'facility security', 'infrastructure protection',
        ]),
        'counter_arguments': json.dumps([
            'Budget and expenditure records for security programs are public',
            'General policy descriptions and program information are public',
            'Challenge claims that entire security contracts are exempt when only specific technical specifications warrant protection',
            'The agency must demonstrate specific security harm, not assert a blanket security category',
            'Widely known security measures do not qualify for this exemption',
        ]),
        'notes': 'Georgia\'s infrastructure security exemption under O.C.G.A. § 50-18-72(a)(20) requires specificity. Georgia courts apply it narrowly and consistently require agencies to identify specific security harm from disclosure of each withheld record.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(7)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(7)',
        'short_name': 'Employee Academic Credentials and Background Checks',
        'category': 'privacy',
        'description': 'Records relating to the home address, personal telephone numbers, and bank account information of public employees are exempt. Additionally, academic credentials and background investigation records for job applicants are exempt during the hiring process.',
        'scope': 'Home addresses, personal phone numbers, and bank account information of public employees. Background investigation records for job applicants and credential verification documents during active hiring processes. The exemption is specifically bounded — name, current position, agency, work address, work phone, and compensation of hired employees are affirmatively public. The background check protection applies during the hiring process — once an employee is hired, their general employment information is public.',
        'key_terms': json.dumps([
            'employee home address', 'personal phone number', 'bank account information',
            'O.C.G.A. 50-18-72(a)(7)', 'background check', 'job applicant',
            'academic credentials', 'hiring process', 'employee personal information',
        ]),
        'counter_arguments': json.dumps([
            'Name, work address, work phone, position, and salary of public employees are public',
            'Once hired, the employee\'s general employment information becomes public',
            'Formal disciplinary records are public accountability records',
            'Challenge overbroad withholding that shields public employee information (position, salary) along with genuinely private data',
        ]),
        'notes': 'Georgia\'s employee personal information exemption is carefully bounded. Georgia courts consistently hold that name, position, compensation, and work contact information of public employees are public. The exemption covers specific personal contact information and hiring-process records.',
    },
    {
        'jurisdiction': 'GA',
        'statute_citation': 'O.C.G.A. § 50-18-72(a)(8)',
        'exemption_number': 'O.C.G.A. § 50-18-72(a)(8)',
        'short_name': 'Juvenile Court Records',
        'category': 'privacy',
        'description': 'Records of juvenile court proceedings and related records identifying juveniles involved in the juvenile justice system are exempt from Georgia\'s ORA to protect minors and support the rehabilitation goals of the juvenile justice system.',
        'scope': 'Individually identifiable records of juvenile court proceedings under O.C.G.A. Title 15, Chapter 11 (Georgia\'s juvenile code). Adult criminal records and adult court proceedings are fully public. Aggregate statistics about the juvenile justice system are public. Policy and budget records for juvenile courts are public. The exemption does not cover records about adults who were juveniles at the time of earlier proceedings — adult status changes the analysis.',
        'key_terms': json.dumps([
            'juvenile court record', 'juvenile proceeding', 'minor record',
            'O.C.G.A. 50-18-72(a)(8)', 'O.C.G.A. Title 15 Chapter 11',
            'delinquency record', 'juvenile adjudication', 'juvenile justice',
        ]),
        'counter_arguments': json.dumps([
            'Adult records are fully public even if the adult was a juvenile at the time of earlier proceedings',
            'Aggregate juvenile justice statistics and program data are public',
            'Policy and budget records for juvenile courts are public',
            'Challenge claims that records about adults involved in juvenile matters are protected',
        ]),
        'notes': 'Georgia\'s juvenile records exemption is reinforced by the Georgia Juvenile Code (O.C.G.A. Title 15, Chapter 11). The protection applies to the specific records of juvenile proceedings, not to all records held by juvenile courts or related agencies.',
    },
]

# =============================================================================
# RULES
# Georgia Open Records Act, O.C.G.A. § 50-18-70 et seq.
# Distinctive features: 3-business-day response deadline (produce OR give
# written description of timeline); no administrative appeal — superior court
# only; attorney's fees; civil penalties of up to $1,000 per violation;
# criminal penalties for knowing and willful violations; first 50 pages of
# standard copies free, $0.10/page thereafter.
# =============================================================================

GA_RULES = [
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'initial_response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'O.C.G.A. § 50-18-71(b)',
        'notes': 'Under O.C.G.A. § 50-18-71(b), a public agency must respond to an Open Records Act request within 3 business days of receipt. The response must either: (1) provide the records; (2) provide a written description of the records along with a timeline for production if records are not immediately available; or (3) deny the request with a statement of the specific legal basis for denial. The 3-business-day deadline is one of the shortest in the country. Failure to respond within 3 business days is itself a violation that supports the civil and criminal penalty provisions.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'reasonable_time_for_production',
        'param_value': 'reasonable_time_after_notice',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-71(b)(1)',
        'notes': 'Under O.C.G.A. § 50-18-71(b)(1), when records cannot be provided within 3 business days, the agency must provide a description of the records and a timeline for production "within a reasonable time not to exceed three business days" for the response itself. For large or complex requests, the production timeline extends beyond 3 days — but the agency must communicate this within 3 business days. Georgia courts have held that "reasonable time" depends on the complexity of the request and the agency\'s resources. Agencies cannot use a large request as justification for indefinite delay.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'fee_cap',
        'param_key': 'first_pages_free',
        'param_value': 'first_50_pages_free_search_and_retrieval',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-71(c)',
        'notes': 'Under O.C.G.A. § 50-18-71(c), agencies may not charge for the first hour of search and retrieval time, and the first 50 pages of standard 8.5x11 black-and-white paper copies must be provided free of charge. Beyond the first 50 pages, agencies may charge no more than $0.10 per page. This makes Georgia one of the more fee-generous states for basic records requests. For electronic records, charges must reflect actual cost. Agencies may not charge for supervisory review or attorney review time.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_per_page',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-71(c)',
        'notes': 'Beyond the first 50 free pages, Georgia agencies may charge $0.10 per page for standard 8.5x11 black-and-white paper copies. This is among the lowest per-page rates in the country. Agencies may charge the actual cost for non-standard copies (color, oversized). For electronic records, the charge is the actual cost of the digital medium — often zero for email delivery. Agencies may not charge for staff time spent searching, reviewing, or redacting records.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-71(a)',
        'notes': 'Georgia\'s ORA does not require records requests to be in writing. Oral requests are valid. However, written requests are strongly recommended to establish the record of the request, trigger the 3-business-day clock, and document any denials. Many Georgia agencies have online portals for FOIA/ORA requests. The requester need not state a reason for the request or provide identifying information beyond what is necessary for the agency to respond.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-73',
        'notes': 'Georgia has NO administrative appeal mechanism for ORA denials. There is no agency head appeal, no ombudsman review, and no state-level administrative tribunal. A requester who believes records were wrongfully withheld or that the 3-business-day deadline was violated must seek relief directly in superior court under O.C.G.A. § 50-18-73. This makes Georgia similar to Ohio in requiring direct judicial enforcement as the sole formal remedy.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-73',
        'notes': 'Under O.C.G.A. § 50-18-73, a requester may bring an action in superior court to compel production of records denied under the ORA. The court reviews the denial de novo. The action is filed in the superior court of the county where the agency is located. The court may award attorney\'s fees and assess civil penalties against the agency. There is no specific statute of limitations for ORA enforcement actions, but courts may consider unreasonable delay by the requester in their discretion on fees and penalties.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'discretionary_prevailing_requester',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-73(b)',
        'notes': 'Under O.C.G.A. § 50-18-73(b), a court may award reasonable attorney\'s fees and expenses of litigation to a requester who substantially prevails in an ORA enforcement action. The fee award is discretionary — the court considers the public benefit from the records, the conduct of the agency, and whether the agency had a reasonable good-faith basis for its position. A pattern of bad-faith withholding or clearly meritless denials supports a fee award. The availability of discretionary fees provides meaningful deterrence against unjustified denials.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty',
        'param_value': 'up_to_$1000',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-74',
        'notes': 'Under O.C.G.A. § 50-18-74, a court may assess a civil fine of up to $1,000 against a public agency that violates the ORA. The civil penalty is assessed per violation, not per day. Georgia courts have discretion in assessing penalties and consider the nature and severity of the violation, the agency\'s prior compliance history, and whether the violation was willful or negligent.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'penalty',
        'param_key': 'criminal_penalty',
        'param_value': 'misdemeanor_for_knowing_willful_violation',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-74',
        'notes': 'Under O.C.G.A. § 50-18-74, a knowing and willful violation of Georgia\'s ORA is a misdemeanor. This criminal penalty provision is unusual among state public records laws. It applies to individual officials who knowingly and willfully deny access to public records in violation of the Act. The criminal provision provides strong deterrence against bad-faith ORA violations. Criminal prosecution requires proof of knowing and willful conduct — mere negligence or poor judgment does not qualify.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-70(a)',
        'notes': 'Under O.C.G.A. § 50-18-70(a), the ORA is premised on a broad definition of "public record" and a strong presumption of openness. Georgia courts have held that the burden of establishing an exemption rests on the agency. The exemptions in § 50-18-72 are strictly construed against the agency — ambiguity is resolved in favor of disclosure. The agency must identify specific exemptions and demonstrate that each applies to each withheld record.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'denial_must_cite_specific_exemption',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-71(d)',
        'notes': 'Under O.C.G.A. § 50-18-71(d), a denial of access must state the specific legal basis (statute, rule, or regulation) for the denial. A denial that merely describes a category of records without citing the specific O.C.G.A. provision is procedurally deficient. Georgia courts have held that procedurally deficient denials support both fee awards and civil penalties. Requesters should challenge denials that fail to cite specific O.C.G.A. provisions.',
    },
    {
        'jurisdiction': 'GA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'O.C.G.A. § 50-18-72(c)',
        'notes': 'Under O.C.G.A. § 50-18-72(c), if a record contains both exempt and non-exempt information, the agency must redact the exempt portions and provide the non-exempt portions. Blanket withholding of records containing some exempt content is an ORA violation. The agency must specifically identify which portions are exempt and provide the remainder. Georgia courts apply the segregability requirement strictly.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

GA_TEMPLATES = [
    {
        'jurisdiction': 'GA',
        'record_type': 'general',
        'template_name': 'General Georgia Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Act Request — O.C.G.A. § 50-18-70 et seq.

Dear Records Custodian:

Pursuant to the Georgia Open Records Act, O.C.G.A. § 50-18-70 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes both cost and production time.

Under O.C.G.A. § 50-18-71(c), the first 50 pages of standard paper copies must be provided at no charge. For pages beyond the first 50, I am willing to pay the actual reproduction cost (not to exceed $0.10 per page per O.C.G.A. § 50-18-71(c)). I am not willing to pay charges for staff time spent searching for, reviewing, or redacting records, which is not a permissible fee under Georgia law. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under O.C.G.A. § 50-18-72(c), the agency must redact any exempt portions of records and provide the non-exempt portions. Blanket withholding of records containing some exempt content violates the ORA.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) cite the specific O.C.G.A. provision (subsection, not just "ORA exemption") per O.C.G.A. § 50-18-71(d); (3) explain how the specific exemption applies to each record; and (4) confirm that all non-exempt, segregable portions of partially withheld records have been released.

Under O.C.G.A. § 50-18-71(b), please respond within 3 business days. If production will extend beyond 3 business days, please provide a written description of the records and a production timeline within that period.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. Under O.C.G.A. § 50-18-71(c), the first 50 pages and the first hour of search and retrieval are already free. I additionally request a waiver of any fees beyond that amount because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically via email or download link, the actual reproduction cost is zero.

Georgia\'s ORA reflects a strong public policy of governmental transparency and accountability. A fee waiver for this request would advance that policy.''',
        'expedited_language': '''I request that this Open Records Act request be processed as expeditiously as possible. Georgia law already requires a 3-business-day response, but prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately at {{requester_email}} or {{requester_phone}} if there are any questions.''',
        'notes': 'General Georgia ORA template. Key features: (1) 3-business-day response deadline — cite O.C.G.A. § 50-18-71(b); (2) no administrative appeal — superior court enforcement under O.C.G.A. § 50-18-73; (3) first 50 pages and first hour of search free under § 50-18-71(c); (4) $0.10/page maximum for paper copies; (5) attorney\'s fees (discretionary) under § 50-18-73(b); (6) civil penalties up to $1,000 under § 50-18-74; (7) criminal misdemeanor for knowing/willful violations under § 50-18-74; (8) denial must cite specific O.C.G.A. provision. Reference O.C.G.A. § 50-18-70, not "FOIA."',
    },
    {
        'jurisdiction': 'GA',
        'record_type': 'law_enforcement',
        'template_name': 'Georgia Open Records Act Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Open Records Act Request — Law Enforcement Records, O.C.G.A. § 50-18-70 et seq.

Dear Records Custodian:

Pursuant to the Georgia Open Records Act, O.C.G.A. § 50-18-70 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Officer disciplinary and complaint records
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs

Regarding the criminal investigation exemption under O.C.G.A. § 50-18-72(a)(1): Georgia law does not permit blanket withholding of law enforcement records. Any withholding must identify: (1) a specific ongoing investigation or pending criminal proceeding; and (2) how disclosure of each specific record would harm that specific proceeding.

[If matter appears concluded:] If no criminal prosecution is currently pending related to this matter, the exemption under O.C.G.A. § 50-18-72(a)(1) does not apply. Completed investigation files are public.

Under O.C.G.A. § 50-18-72(c), all non-exempt, segregable portions of partially withheld records must be released. Under O.C.G.A. § 50-18-71(d), any denial must cite the specific O.C.G.A. provision relied upon.

Under O.C.G.A. § 50-18-71(c), the first 50 pages are free. Please respond within 3 business days per O.C.G.A. § 50-18-71(b).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees beyond the first 50 free pages be waived. These records concern {{public_interest_explanation}}, a matter of public accountability. Electronic delivery incurs zero reproduction cost. A fee waiver is consistent with Georgia\'s strong ORA transparency policy.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}. Georgia\'s 3-business-day deadline already provides for prompt access — please prioritize this request within that framework.''',
        'notes': 'Georgia law enforcement records template. Key points: (1) § 50-18-72(a)(1) requires ongoing investigation for the exemption — completed matters are public; (2) no administrative appeal — superior court under § 50-18-73; (3) first 50 pages free under § 50-18-71(c); (4) $0.10/page maximum; (5) criminal misdemeanor for knowing/willful violations under § 50-18-74 — cite this to signal awareness; (6) attorney\'s fees available for prevailing requesters.',
    },
    {
        'jurisdiction': 'GA',
        'record_type': 'financial',
        'template_name': 'Georgia Open Records Act Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Open Records Act Request — Contracts and Expenditure Records, O.C.G.A. § 50-18-70 et seq.

Dear Records Custodian:

Pursuant to the Georgia Open Records Act, O.C.G.A. § 50-18-70 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Contractor/vendor (if applicable): {{contractor_name}}
Contract period: {{date_range_start}} through {{date_range_end}}
Contract number (if known): {{contract_number}}

This request includes, but is not limited to:
- Executed contracts and all amendments
- Bid and proposal documents
- Invoices, payment records, and vouchers
- Performance evaluations and compliance records

Regarding trade secret claims under O.C.G.A. § 50-18-72(a)(9): Contract prices, amounts paid with public funds, and total government expenditures are public regardless of vendor trade secret designations. The agency must independently evaluate trade secret claims under the Georgia Trade Secrets Act (O.C.G.A. § 10-1-761) — it cannot defer to contractor "confidential" designations.

Under O.C.G.A. § 50-18-72(c), all non-exempt, segregable portions of partially withheld records must be released. Under O.C.G.A. § 50-18-71(c), the first 50 pages are free.

Please respond within 3 business days per O.C.G.A. § 50-18-71(b).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for pages beyond the first 50 free pages. These records concern the expenditure of public funds — a core purpose of the Georgia ORA. Electronic delivery incurs zero reproduction cost. A fee waiver would further the ORA\'s transparency mandate.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}. Georgia\'s 3-business-day deadline already ensures prompt access — please prioritize within that framework.''',
        'notes': 'Georgia government contracts template. Key points: (1) contract prices and public expenditures are always public; (2) trade secret claims require independent agency analysis under Georgia Trade Secrets Act; (3) first 50 pages free; (4) $0.10/page maximum thereafter; (5) no administrative appeal — superior court under § 50-18-73; (6) 3-business-day response deadline is among the fastest in the country.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in GA_EXEMPTIONS:
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

    print(f'GA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in GA_RULES:
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

    print(f'GA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in GA_TEMPLATES:
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

    print(f'GA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'GA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_ga', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
