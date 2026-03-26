#!/usr/bin/env python3
"""Build Colorado Open Records Act (CORA) data: exemptions, rules, and templates.

Covers Colorado's Open Records Act (CORA), C.R.S. § 24-72-200.1 et seq.
Colorado has a moderately strong public records law with a 3-business-day response
deadline, discretionary extensions, no mandatory administrative appeal, and
attorney's fees for prevailing requesters. Courts strictly construe exemptions.

Run: python3 scripts/build/build_co.py
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
# CORA, C.R.S. § 24-72-204, provides a list of records that are not subject
# to public inspection. Colorado courts construe exemptions narrowly consistent
# with the Act's strong disclosure mandate. The custodian bears the burden of
# proving an exemption applies. C.R.S. § 24-72-201 establishes that all public
# records are open for inspection unless a specific exemption applies.
# =============================================================================

CO_EXEMPTIONS = [
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(I)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(I)',
        'short_name': 'Personnel Files — Private Employee Information',
        'category': 'privacy',
        'description': 'Personnel files of public employees are exempt from public inspection to the extent they contain private information whose disclosure would constitute an unreasonable invasion of personal privacy. The exemption protects truly private personal information but does not shield performance reviews or disciplinary records of public employees exercising public duties.',
        'scope': 'Applies to personnel files containing private personal information such as medical records, home addresses, personal financial information unrelated to public employment, and similar private data. Does NOT protect salary information, job titles, dates of employment, final disciplinary actions, termination decisions, or information about the exercise of public duties. Colorado courts have held that disciplinary records of peace officers and other public employees exercising government authority are generally public because accountability outweighs privacy interests. The exemption is frequently invoked too broadly by agencies.',
        'key_terms': json.dumps([
            'personnel file', 'private employee information', 'personal privacy',
            'disciplinary record', 'employment record', 'public employee',
            'unreasonable invasion', 'home address', 'medical record',
        ]),
        'counter_arguments': json.dumps([
            'Salary, job title, and dates of employment are public regardless of the personnel file exemption',
            'Final disciplinary actions, terminations, and demotions of public employees are public — agencies may not use the personnel file exemption to hide accountability records',
            'The exemption requires an "unreasonable invasion of personal privacy" — a balancing test that favors disclosure for public employees acting in their official capacity',
            'Peace officer disciplinary records have specific public disclosure requirements under C.R.S. § 24-31-304 that override the general personnel file exemption',
            'Challenge overbroad redactions where the agency has removed publicly accountable information along with genuinely private data',
            'Request a privilege log identifying what specifically was withheld and why',
        ]),
        'notes': 'Colorado personnel file exemption is frequently over-applied. C.R.S. § 24-31-304 specifically requires disclosure of peace officer disciplinary records in many circumstances. Colorado courts consistently hold that public employees in their public roles have reduced privacy expectations. See Martinelli v. District Court, 612 P.2d 1083 (Colo. 1980) for foundational privacy analysis.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(2)(a)',
        'exemption_number': 'C.R.S. § 24-72-204(2)(a)',
        'short_name': 'Criminal Justice Records — Investigation Files',
        'category': 'law_enforcement',
        'description': 'Criminal justice records compiled for law enforcement purposes are subject to a separate statutory scheme (C.R.S. § 24-72-301 et seq.) and may be withheld where disclosure would: interfere with enforcement proceedings, deprive a person of a fair trial, constitute an unwarranted invasion of privacy, identify a confidential source, disclose investigative techniques, or endanger law enforcement personnel.',
        'scope': 'Criminal justice records as defined in C.R.S. § 24-72-302 — arrest and criminal records, investigation records, records of prosecutorial decisions, and related law enforcement files. Colorado has a separate criminal justice records statute that imposes its own balancing test. Arrest records, conviction records, and information about final criminal judgments are generally public. Active investigation records may be withheld, but agencies must apply a specific harm analysis for each withheld item, not a blanket categorical denial.',
        'key_terms': json.dumps([
            'criminal justice records', 'law enforcement investigation', 'arrest record',
            'criminal record', 'investigative technique', 'confidential informant',
            'criminal investigation', 'active investigation', 'C.R.S. § 24-72-302',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records and conviction records are presumptively public under the criminal justice records statute',
            'The agency must apply a specific harm analysis to each withheld record — blanket categorical denial is insufficient',
            'Once a criminal matter is concluded (prosecution complete, no pending charges), the active investigation rationale disappears',
            'Information about the existence and nature of incidents (crime reports) is generally public even when investigative details may be withheld',
            'Challenge claims that all law enforcement records fall within the criminal justice records exemption — only records compiled for law enforcement purposes qualify',
            'Use-of-force reports and officer conduct records that document completed incidents are public',
        ]),
        'notes': 'Colorado criminal justice records are governed by a separate statute, C.R.S. § 24-72-301 et seq., which provides its own balancing test distinct from the general CORA framework. The Colorado Court of Appeals and Supreme Court have repeatedly held that this balancing test requires record-specific analysis, not categorical withholding.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(IV)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(IV)',
        'short_name': 'Deliberative Process — Draft Documents',
        'category': 'deliberative',
        'description': 'Correspondence, memoranda, and other records of communications within a government agency that are essentially advisory and reflect the deliberative process are exempt where disclosure would harm the agency\'s candid policy-making process. The exemption does not protect factual material or records of final agency decisions.',
        'scope': 'Internal agency communications, draft reports, advisory memoranda, and predecisional deliberative materials that contain opinions and recommendations not yet adopted as agency policy. The exemption is narrow: factual material contained in deliberative documents must be segregated and released. Final agency decisions, adopted policies, working law applied to the public, and records of what the agency decided are fully public regardless of how they were developed. Colorado courts apply a two-part test: (1) the record must be predecisional, and (2) it must be deliberative (contain opinions/recommendations, not just facts).',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'advisory memorandum', 'draft',
            'policy deliberation', 'internal communication', 'working paper',
            'recommendation', 'intra-agency', 'opinion',
        ]),
        'counter_arguments': json.dumps([
            'Factual material within deliberative documents must be segregated and released — the exemption covers only the opinion and recommendation portions',
            'Once a draft or recommendation is adopted as agency policy, the exemption no longer applies',
            '"Working law" — the standards and criteria agencies actually apply in practice — must be disclosed even if found in internal documents',
            'Challenge the agency\'s claim that entire documents are deliberative — require specific identification of which portions are opinion-based',
            'Communications with persons outside the agency (third-party contractors, outside counsel on routine matters) may not qualify as internal deliberative communications',
            'The agency bears the burden of proving each record is both predecisional and deliberative',
        ]),
        'notes': 'Colorado\'s deliberative process exemption is narrowly construed consistent with CORA\'s strong disclosure mandate. C.R.S. § 24-72-204(3)(a)(IV) requires a specific showing for each withheld document. Colorado courts have rejected agency attempts to use the deliberative process exemption as a general shield.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(II)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(II)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and proprietary commercial or financial information submitted by private entities to government agencies are exempt where disclosure would impair the entity\'s competitive position and where the information is held in confidence.',
        'scope': 'Commercial or financial information submitted by private entities to government agencies that: (1) qualifies as a trade secret under Colorado\'s Uniform Trade Secrets Act, C.R.S. § 7-74-102; or (2) is confidential commercial/financial information whose disclosure would cause competitive harm. Government-generated records generally cannot qualify as trade secrets. Amounts paid with public funds (contract prices, grant amounts) are generally public. The submitting entity typically must demonstrate that it has taken reasonable measures to maintain the information in confidence and that the information derives economic value from being kept secret.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm', 'commercial information',
            'financial information', 'Uniform Trade Secrets Act', 'confidential business',
            'economic value', 'competitive position', 'C.R.S. § 7-74-102',
        ]),
        'counter_arguments': json.dumps([
            'The submitting party must demonstrate trade secret status — a "confidential" stamp is not sufficient',
            'Publicly available information cannot qualify as a trade secret regardless of the submitter\'s designations',
            'Contract prices, amounts paid with public funds, and expenditure data are generally public regardless of trade secret claims',
            'Information required to be submitted to the government (e.g., regulatory filings) has reduced expectations of secrecy',
            'Challenge whether the submitter actually maintained reasonable secrecy measures — prior disclosure defeats the claim',
            'The agency, not the submitter, makes the final disclosure decision — agencies may not simply defer to vendor confidentiality claims',
        ]),
        'notes': 'Colorado\'s trade secret exemption under CORA applies the UTSA framework. Courts have held that agencies must independently evaluate trade secret designations. Public expenditure data is consistently held to be public regardless of vendor objections.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(VIII)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(VIII)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that are subject to the attorney-client privilege or work-product doctrine, when the client is the public agency, are exempt from public inspection. The privilege tracks the common law and applies to confidential communications made for the purpose of obtaining legal advice.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The attorney-client privilege for government entities in Colorado is narrowly applied: it covers legal advice only, not business or policy advice. General counsel opinions on policy matters may not be fully protected. Billing records, retainer agreements, and general financial arrangements with outside counsel are generally not privileged. Facts independently known are not protected merely because they were communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice specifically — not general business or policy guidance',
            'Waiver occurs when the agency discloses the content in public proceedings or to non-attorney staff not involved in the legal matter',
            'Attorney billing records and invoices are generally public in Colorado',
            'The privilege belongs to the agency, which may waive it — challenge constructive waiver through public use of the advice',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and opinion',
            'Reject claims that entire files are privileged when only specific communications constitute legal advice',
        ]),
        'notes': 'Colorado recognizes attorney-client privilege for government entities as incorporated into CORA by C.R.S. § 24-72-204(3)(a)(VIII). Colorado courts apply the privilege narrowly consistent with the overall disclosure mandate. Billing records and routine correspondence with outside counsel are generally public.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(XI)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(XI)',
        'short_name': 'Infrastructure Security — Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and records identifying specific weaknesses in critical infrastructure systems (water, energy, transportation) are exempt where disclosure would create a specific and articulable security risk.',
        'scope': 'Records that specifically identify vulnerabilities in critical infrastructure such as water systems, power grids, transportation networks, and public building security. The exemption requires that disclosure would create a specific, articulable security risk — not a speculative or general risk. Budget records, contracts, and general descriptions of security programs are public. The agency must demonstrate that disclosure of the specific record (not just the general category) would enable exploitation of a vulnerability.',
        'key_terms': json.dumps([
            'vulnerability assessment', 'critical infrastructure', 'security plan',
            'security risk', 'water system', 'power grid', 'infrastructure protection',
            'access control', 'intrusion detection', 'cybersecurity',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable — general security concerns are insufficient',
            'Budget and expenditure records for security programs are public regardless of this exemption',
            'General descriptions of security policies that do not identify specific vulnerabilities are not covered',
            'Challenge claims that entire contracts with security vendors are exempt when only specific technical details warrant protection',
            'Widely known security features of public facilities cannot be withheld under this exemption',
        ]),
        'notes': 'Colorado\'s infrastructure security exemption under CORA requires a showing of specific, articulable risk. Courts have held that the agency must demonstrate how disclosure of the particular record would enable exploitation of the identified vulnerability.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(XIV)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(XIV)',
        'short_name': 'Mental Health and Medical Records',
        'category': 'privacy',
        'description': 'Medical and mental health records of identifiable individuals held by government agencies are exempt from disclosure to protect patient privacy. The exemption is categorical for individually identifiable health information.',
        'scope': 'Individually identifiable medical and mental health records, including treatment records, diagnostic information, prescription records, and records of mental health proceedings. Applies to records held by public health agencies, correctional facilities, publicly funded health programs, and other government entities. Aggregate, de-identified health statistics are public. Policies, procedures, and budget records of public health agencies are public. The exemption aligns with HIPAA requirements for covered government entities.',
        'key_terms': json.dumps([
            'medical record', 'mental health record', 'patient privacy', 'HIPAA',
            'individually identifiable', 'health information', 'treatment record',
            'diagnosis', 'prescription', 'mental health treatment',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate, de-identified health data is not covered and must be disclosed',
            'Policies, procedures, and quality metrics for public health programs are public',
            'Budget and expenditure records of public health agencies are public',
            'Challenge whether the specific records requested actually contain individually identifiable information',
            'Information about the health programs and services offered by public agencies (as distinct from individual patient records) is public',
        ]),
        'notes': 'Colorado\'s medical records exemption under CORA protects individually identifiable health information held by government agencies. The exemption is well-established and broadly consistent with federal HIPAA requirements. Government agencies that are HIPAA covered entities must comply with both CORA and HIPAA.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(XII)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(XII)',
        'short_name': 'Social Services and Public Assistance Records',
        'category': 'privacy',
        'description': 'Records of individuals receiving public assistance, social services, or child welfare services are exempt from public disclosure to protect the privacy of beneficiaries and encourage utilization of social safety net programs.',
        'scope': 'Case files and individually identifiable records of persons receiving Medicaid, SNAP, TANF, child welfare services, and other public assistance programs administered by state and county agencies. Aggregate program statistics (enrollment numbers, benefit amounts, program outcomes) are public. Policies, procedures, audit findings, and administrative records of social service agencies are public. The exemption is designed to protect beneficiary privacy — it does not shield agency administration from accountability.',
        'key_terms': json.dumps([
            'public assistance', 'social services', 'welfare records', 'Medicaid',
            'SNAP', 'TANF', 'child welfare', 'case file', 'beneficiary records',
            'public benefit', 'social safety net',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate enrollment and benefit statistics are public — the exemption protects individuals, not program data',
            'Administrative policies, audit findings, and operational records of social service agencies are public',
            'Challenge claims that all records from a social services agency are exempt — only individually identifiable beneficiary records qualify',
            'Information about systemic agency practices and policies that affect beneficiaries is public',
        ]),
        'notes': 'Colorado\'s social services records exemption is categorical for individually identifiable beneficiary information. The exemption is consistent with federal confidentiality requirements for programs like Medicaid and SNAP. However, the exemption does not shield the agency\'s own operations, policies, and practices from public scrutiny.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(6)(a)',
        'exemption_number': 'C.R.S. § 24-72-204(6)(a)',
        'short_name': 'Investigative Files — Ongoing Regulatory Investigations',
        'category': 'law_enforcement',
        'description': 'Records of ongoing regulatory investigations and enforcement proceedings are exempt where disclosure would compromise an active investigation, reveal confidential informants, or give subjects advance warning that allows destruction of evidence or evasion of enforcement.',
        'scope': 'Records compiled during active regulatory enforcement investigations, including evidence gathered, witness interviews, enforcement strategies, and related documents. The exemption applies only while the investigation is ongoing — once the matter is resolved (citation issued, penalty assessed, case closed), investigation records become subject to CORA. The agency must demonstrate that the specific investigation is active and that disclosure would cause a specific harm, not merely that the records are "investigative" in nature.',
        'key_terms': json.dumps([
            'regulatory investigation', 'enforcement proceeding', 'ongoing investigation',
            'active investigation', 'evidence', 'witness interview', 'enforcement strategy',
            'confidential source', 'regulatory enforcement',
        ]),
        'counter_arguments': json.dumps([
            'Once an investigation concludes, the exemption no longer applies and records are public',
            'The agency must show both that the investigation is active AND that specific harm would result from disclosure',
            'Challenge the agency\'s characterization of a matter as "ongoing" if no action has been taken for an extended period',
            'Formal citations, consent orders, and final enforcement actions are public once issued',
            'Challenge blanket claims that all investigation files are exempt — the exemption requires case-by-case analysis',
        ]),
        'notes': 'Colorado\'s regulatory investigation exemption is time-limited: it expires when the investigation concludes. Colorado courts have held that agencies cannot maintain investigation files in permanent secrecy by simply never closing cases.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(V)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(V)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and related valuation documents prepared by or for a government agency in connection with the prospective acquisition or sale of real property are exempt until the transaction is complete or the agency\'s interest in the property is terminated.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuations prepared for the purpose of negotiating acquisition or sale of real property. The exemption is time-limited: it expires automatically when the transaction closes or is abandoned. The exemption exists to prevent the agency from being disadvantaged in negotiations if its maximum willingness to pay is disclosed. Post-transaction, all appraisal records are public. The exemption does not cover general budget discussions or agency policy regarding property purchases.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'condemnation', 'pre-acquisition', 'real property', 'land purchase',
            'feasibility study', 'property sale', 'eminent domain',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction closes or is abandoned',
            'Challenge the claim that a transaction is still "pending" if it has been inactive for an extended period',
            'Appraisals for property already owned by the agency are not covered',
            'Budget documents and general discussions about property are not formal appraisals',
            'After condemnation proceedings conclude, all valuation records are public',
        ]),
        'notes': 'Colorado\'s pre-acquisition appraisal exemption is a standard real estate exemption found in most state public records statutes. The exemption is automatic and time-limited — no court order is needed to compel disclosure after the transaction completes.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(IX)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(IX)',
        'short_name': 'Library Patron Records',
        'category': 'privacy',
        'description': 'Records identifying which library materials a specific patron accessed, borrowed, or requested at a publicly funded library are exempt from disclosure to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying what specific individuals borrowed, accessed, or inquired about at public libraries. Covers circulation records, database access logs, interlibrary loan requests, and reference inquiries. Library administrative records, budget documents, collection statistics, and program information are public. The exemption applies to patron-specific data only — not to library operations generally.',
        'key_terms': json.dumps([
            'library records', 'circulation records', 'library patron', 'borrower records',
            'database access', 'intellectual privacy', 'interlibrary loan', 'reading privacy',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library usage statistics and collection data are not covered',
            'Library administrative and budget records are fully public',
            'Records subpoenaed pursuant to a valid court order may be disclosed',
            'The exemption covers patron-specific data — not library programming or operational records',
        ]),
        'notes': 'Colorado\'s library patron privacy exemption reflects the strong public policy interest in intellectual freedom. The exemption is absolute for patron-specific data — there is no balancing test. Court orders can override the exemption for law enforcement purposes.',
    },
    {
        'jurisdiction': 'CO',
        'statute_citation': 'C.R.S. § 24-72-204(3)(a)(VII)',
        'exemption_number': 'C.R.S. § 24-72-204(3)(a)(VII)',
        'short_name': 'Victim Personal Information',
        'category': 'privacy',
        'description': 'Personal identifying information of crime victims — including home addresses, telephone numbers, and in some cases names — are exempt from public disclosure in government records to protect victim safety and encourage reporting of crimes.',
        'scope': 'Personal identifying information of crime victims including home address, telephone number, and in specified cases (domestic violence, sexual assault, stalking, trafficking) the victim\'s name. The exemption does not protect the existence of the crime, the nature of the offense, or general information about law enforcement responses. Incident report information about the offense itself is generally public, with specific victim identifiers redacted.',
        'key_terms': json.dumps([
            'crime victim', 'victim privacy', 'victim address', 'victim name',
            'domestic violence', 'sexual assault victim', 'witness protection',
            'victim information', 'victim identification',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects victim identifiers — not the existence or nature of the crime',
            'Incident reports documenting the offense are public with victim identifiers redacted',
            'Challenge overbroad redactions where agencies have removed offense information along with victim identifiers',
            'Information about crimes against victims who have voluntarily made themselves public figures may have reduced protection',
        ]),
        'notes': 'Colorado\'s victim information exemption is narrowly tailored to protect identifiers, not to shield all records relating to crimes involving victims. Incident reports must be released with victim-identifying information redacted, not withheld entirely.',
    },
]

# =============================================================================
# RULES
# Colorado Open Records Act, C.R.S. § 24-72-200.1 et seq.
# Key features: 3-business-day response deadline with 7-day extension;
# $0.25/page for paper copies; no mandatory administrative appeal;
# district court enforcement; attorney's fees for prevailing requester.
# =============================================================================

CO_RULES = [
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'C.R.S. § 24-72-203(3)(b)',
        'notes': 'Colorado requires custodians to allow inspection or provide copies of public records within 3 business days of a written request. The 3-day period is triggered by a written request — oral requests may be handled immediately or converted to written form. The 3-day deadline is a hard deadline absent a proper extension under C.R.S. § 24-72-203(3)(b)(II). Failure to respond within 3 days is a CORA violation that may support an attorney fees award if the requester is forced to sue.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'extension_deadline_days',
        'param_value': '7',
        'day_type': 'business',
        'statute_citation': 'C.R.S. § 24-72-203(3)(b)(II)',
        'notes': 'A custodian may extend the 3-business-day response deadline by up to 7 additional business days (total of up to 10 business days) if the request is for a large volume of records, requires extensive research, or requires records from multiple agency offices. The extension requires written notice to the requester stating: (1) that an extension is being claimed; (2) the estimated date records will be available; and (3) the reason for the extension. Extensions are not automatic — they must be communicated in writing before the original 3-day deadline expires.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-205(5)',
        'notes': 'Colorado allows custodians to charge up to $0.25 per page for paper copies of public records. Electronic copies may be provided at actual cost — which for records already in digital form is typically near zero. Agencies may charge actual costs for extraordinary requests requiring specialized services, but the standard $0.25/page rate applies to typical paper copies. Colorado does not allow agencies to charge for research or staff time spent identifying, reviewing, or redacting records — only reproduction costs are permitted.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-205(5)',
        'notes': 'Colorado CORA does not mandate fee waivers for any class of requesters, but custodians have discretion to waive or reduce fees. Requesters may argue that a fee waiver is warranted when: (1) the records serve a significant public interest; (2) disclosure will not benefit the requester\'s commercial interests; and (3) the requester is a journalist, nonprofit, or academic researcher. For electronic records provided by email, the actual reproduction cost is zero, making fee arguments largely moot.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204',
        'notes': 'Colorado CORA has NO formal administrative appeal mechanism. There is no agency head review, no ombudsman, and no state agency that adjudicates CORA appeals. A requester who is denied access or whose request is ignored must go directly to district court for enforcement. The Colorado Sunshine Law also does not provide for an Attorney General opinion process as some other states do. This means litigation is the sole formal remedy, which raises the cost of enforcement compared to states with AG appeal processes.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(5)',
        'notes': 'A requester denied access to records may bring a civil action in the district court of the county where the records are located. The court reviews the denial de novo and may conduct in camera review of withheld records. If the requester prevails, the court may award attorney fees and costs. Colorado courts have held that de novo review means the court applies no deference to the agency\'s initial determination — the burden is entirely on the agency to justify withholding. Cases are typically handled expeditiously because of the nature of public access disputes.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(5)(b)',
        'notes': 'Colorado courts MAY award attorney fees and costs to a prevailing requester — the award is discretionary, not mandatory. Courts consider whether: (1) the requester substantially prevailed; (2) the agency had a reasonable basis for withholding; and (3) the litigation was necessary to obtain the records. The fee award provision is meaningful: it incentivizes agencies to respond properly in the first instance and makes it economically viable for requesters to pursue enforcement for significant denials. Fees are not available for partial prevailing — the requester must substantially prevail overall.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'penalty',
        'param_key': 'statutory_penalty',
        'param_value': 'none_beyond_fees',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(5)',
        'notes': 'Colorado CORA does not provide for per diem penalties, civil fines, or criminal penalties against agencies that wrongfully withhold records. The sole enforcement mechanism beyond court-ordered production is the discretionary attorney fees award. This makes Colorado\'s enforcement regime weaker than states like Washington (per diem penalties), Louisiana (daily civil penalties), or Oregon. Requesters must rely primarily on fee awards and court orders to incentivize compliance. Willful or knowing violations by individual officers may have other legal consequences, but CORA itself does not impose monetary penalties.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-203(1)',
        'notes': 'Colorado does not require requesters to identify themselves or state the purpose of their public records request. Any person may inspect or copy public records. Agencies may not demand identification as a precondition for access. Anonymous and pseudonymous requests are valid. Contact information (email, phone) may be requested for delivery coordination purposes but may not be required as a condition of access. This right extends to all persons, not just Colorado residents or U.S. citizens.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(1)',
        'notes': 'When a record contains both exempt and non-exempt portions, the custodian must allow inspection of all non-exempt portions and may withhold only the specific exempt material. Blanket withholding of documents containing some exempt content is a CORA violation. The burden is on the agency to identify and segregate exempt content. Redactions must be specific — agencies may not withhold entire documents when only portions qualify for an exemption.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(1)',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure rests entirely on the agency custodian. C.R.S. § 24-72-201 establishes a strong presumption that all public records are open for inspection. An agency claiming an exemption must affirmatively demonstrate that a specific, applicable exemption applies to each withheld record. General assertions of exemption categories without record-specific justification are insufficient. Colorado courts review CORA withholding decisions de novo with no deference to the agency\'s determination.',
    },
    {
        'jurisdiction': 'CO',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_statutory_basis',
        'day_type': None,
        'statute_citation': 'C.R.S. § 24-72-204(1)',
        'notes': 'When a custodian denies access to records, the denial should be in writing and must identify the specific statutory exemption(s) relied upon. CORA requires the custodian to cite the specific provision of C.R.S. § 24-72-204 or other applicable statute, not merely assert a general category. A denial without a specific statutory basis is procedurally deficient. Requesters should insist on written denials with specific statutory citations to support any subsequent judicial challenge.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

CO_TEMPLATES = [
    {
        'jurisdiction': 'CO',
        'record_type': 'general',
        'template_name': 'General Colorado Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Colorado Open Records Act Request — C.R.S. § 24-72-203

Dear Custodian of Records:

Pursuant to the Colorado Open Records Act (CORA), C.R.S. § 24-72-200.1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. For records available in electronic form, the actual cost of reproduction is typically zero, and I request they be provided accordingly.

For paper copies, I am willing to pay up to $0.25 per page per C.R.S. § 24-72-205(5). If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or make payment arrangements. I am not willing to pay for research or staff time spent locating, reviewing, or redacting records, which are not permissible charges under CORA.

Under C.R.S. § 24-72-201, all public records are presumptively open for inspection. The burden of proving that any exemption applies rests on {{agency_name}} as the records custodian. Under C.R.S. § 24-72-204(1), any record containing both exempt and non-exempt portions must be produced with only the specifically exempt material redacted — blanket withholding is not permitted.

If any records or portions of records are withheld, I request that {{agency_name}}: (1) identify each withheld record; (2) state the specific C.R.S. citation for each claimed exemption; (3) describe the record with sufficient detail for me to evaluate the claim; and (4) confirm that all non-exempt, segregable portions of partially withheld records have been provided.

Under C.R.S. § 24-72-203(3)(b), please respond within 3 business days. If you require an extension under C.R.S. § 24-72-203(3)(b)(II), please provide written notice within the initial 3-day period stating the reason and estimated response date.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that all fees associated with this request be waived. Although CORA does not mandate fee waivers, {{agency_name}} has discretion to waive fees when:

1. The records relate to {{public_interest_explanation}}, which is a matter of significant public interest and governmental accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}} and will not primarily serve any private commercial interest.

3. To the extent records are available in electronic form and can be delivered by email, the actual reproduction cost is zero, making a fee waiver consistent with C.R.S. § 24-72-205(5).

I ask that you exercise your discretion to waive fees in keeping with CORA's strong presumption in favor of public access.''',
        'expedited_language': '''I request that this CORA request be processed with particular urgency. While CORA already requires a response within 3 business days, prompt production is especially important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the requested records.''',
        'notes': 'General-purpose Colorado CORA template. Key features: (1) 3-business-day response deadline, with written notice required for up to 7-day extension (C.R.S. § 24-72-203(3)(b)); (2) no administrative appeal — go directly to district court if denied (C.R.S. § 24-72-204(5)); (3) discretionary attorney fees for prevailing requester (C.R.S. § 24-72-204(5)(b)); (4) $0.25/page maximum for paper copies (C.R.S. § 24-72-205(5)); (5) no identity requirement — any person may request; (6) agency bears burden of proving any exemption. Use "CORA" not "FOIA." Cite C.R.S. § 24-72, not RCW or other state codes.',
    },
    {
        'jurisdiction': 'CO',
        'record_type': 'law_enforcement',
        'template_name': 'Colorado CORA Request — Law Enforcement and Criminal Justice Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Colorado Open Records Act Request — Law Enforcement Records, C.R.S. § 24-72-201 et seq.; C.R.S. § 24-72-301 et seq.

Dear Custodian of Records:

Pursuant to the Colorado Open Records Act (CORA), C.R.S. § 24-72-200.1 et seq., and the Colorado Criminal Justice Records Act, C.R.S. § 24-72-301 et seq., I request copies of the following records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Peace officer disciplinary and complaint records for involved officers (see C.R.S. § 24-31-304)
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Written and electronic communications relating to the above

Regarding claimed exemptions: Colorado law does not permit blanket withholding of law enforcement records. Exemptions under C.R.S. § 24-72-204 and C.R.S. § 24-72-308 require record-specific analysis. For each withheld item, please identify: (1) the specific statutory exemption by C.R.S. citation; (2) how disclosure of that specific record — not records of this general type — would cause the specific harm the exemption is designed to prevent.

Regarding peace officer disciplinary records: C.R.S. § 24-31-304 imposes specific disclosure requirements for peace officer records that may supersede general personnel file exemptions. Please confirm that all applicable C.R.S. § 24-31-304 records have been reviewed and produced accordingly.

For completed matters: If any related criminal prosecution is concluded or if no prosecution is pending, please apply the standard applicable to closed matters — the active investigation rationale does not extend to closed cases.

I am willing to pay up to $0.25 per page for paper copies per C.R.S. § 24-72-205(5), up to ${{fee_limit}} total.

Please respond within 3 business days per C.R.S. § 24-72-203(3)(b).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement. Electronic delivery incurs zero reproduction cost. A fee waiver is consistent with CORA\'s strong presumption of public access.''',
        'expedited_language': '''I request expedited processing of this request within the 3-business-day CORA deadline. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Colorado law enforcement records template. Key features: (1) criminal justice records are governed by C.R.S. § 24-72-301 et seq. (separate from general CORA) — cite both; (2) C.R.S. § 24-31-304 requires disclosure of peace officer disciplinary records in many circumstances — cite specifically; (3) completed investigation files are generally public under the criminal justice records statute; (4) body camera footage is a public record under Colorado law; (5) no administrative appeal — district court is the sole formal review mechanism; (6) discretionary attorney fees for prevailing requester.',
    },
    {
        'jurisdiction': 'CO',
        'record_type': 'government_contracts',
        'template_name': 'Colorado CORA Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Colorado Open Records Act Request — Government Contracts and Expenditure Records

Dear Custodian of Records:

Pursuant to the Colorado Open Records Act, C.R.S. § 24-72-200.1 et seq., I request the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments between {{agency_name}} and {{contractor_vendor_name}} from {{date_range_start}} through {{date_range_end}}
- Invoices, purchase orders, and payment records for the above contracts
- Correspondence and communications relating to contract negotiation, performance, and compliance
- Any performance evaluations, audits, or assessments of the contractor's work
- Any subcontracts or subcontract agreements

Regarding trade secret/proprietary claims: Contract amounts, payment records, and expenditures of public funds are public under Colorado law regardless of vendor confidentiality claims. Per-unit pricing in competitive situations may have limited protection, but aggregate amounts paid with public dollars are public. If {{contractor_vendor_name}} has asserted any confidentiality claims, please identify the specific records and the specific claimed basis — the agency, not the vendor, makes the final disclosure determination.

The burden of demonstrating that any exemption applies rests on {{agency_name}} per C.R.S. § 24-72-201. Any records containing both exempt and non-exempt content must be produced with only the specifically exempt portions redacted.

I prefer electronic delivery at no charge. For paper copies, I am willing to pay up to $0.25 per page, up to ${{fee_limit}} total.

Please respond within 3 business days per C.R.S. § 24-72-203(3)(b).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for this government contracts request. These records concern the expenditure of public funds, which is a core government accountability matter. Disclosure will benefit the public by enabling oversight of how public dollars are spent. Electronic delivery incurs no reproduction cost.''',
        'expedited_language': '''I request prompt processing within CORA\'s 3-business-day deadline. These government expenditure records are needed for {{expedited_justification}}. Please contact me immediately if clarification would speed production.''',
        'notes': 'Colorado government contracts template. Key point: amounts paid with public funds are always public in Colorado regardless of vendor trade secret claims. Vendors cannot veto disclosure of public expenditure data. Use this template for procurement records, vendor contracts, grant agreements, and similar government spending records. The template explicitly addresses and pre-empts the most common objection — vendor confidentiality claims.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in CO_EXEMPTIONS:
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

    print(f'CO exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in CO_RULES:
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

    print(f'CO rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in CO_TEMPLATES:
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

    print(f'CO templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'CO total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_co', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
