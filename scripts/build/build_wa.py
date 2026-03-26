#!/usr/bin/env python3
"""Build Washington Public Records Act data: exemptions, rules, and templates.

Covers Washington's Public Records Act, RCW 42.56.
Washington has one of the strongest public disclosure mandates in the country —
the statute explicitly requires agencies to provide the "fullest assistance" and
"most timely possible action" on requests, and courts strictly construe exemptions
against the agency. Per diem penalties ($5-$100/day) are a unique enforcement tool.

Run: python3 scripts/build/build_wa.py
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
# Washington's PRA, RCW 42.56, lists hundreds of specific statutory exemptions
# across the code, but the core framework in RCW 42.56 itself covers the major
# categories. Exemptions are strictly construed against the agency — RCW 42.56.030
# commands the "fullest assistance" principle and shifts the burden of proof
# entirely onto the agency claiming an exemption. Courts apply a de novo standard
# and may impose per diem penalties for unjustified withholding.
# =============================================================================

WA_EXEMPTIONS = [
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.230(1)',
        'exemption_number': 'RCW 42.56.230(1)',
        'short_name': 'Personal Information — SSN, DOB, Financial',
        'category': 'privacy',
        'description': 'Personal information including Social Security numbers, dates of birth, financial account numbers, and similar identifying data submitted to or held by agencies is exempt from disclosure to protect against identity theft and unwarranted privacy intrusion.',
        'scope': 'Specific categories of personal identifying information: Social Security numbers (SSNs), dates of birth, financial account numbers, PINs, and similar data whose disclosure would enable identity theft or financial fraud. The exemption applies to the specific data points, not to records containing those data points in their entirety. Agencies must release records with these fields redacted rather than withholding entire documents. Does not protect general biographical information, employment history, or names.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'date of birth', 'DOB', 'financial account',
            'personal information', 'identity theft', 'bank account', 'PIN', 'account number',
            'personally identifiable information', 'PII',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects specific data fields, not entire records — agencies must redact and release the remainder',
            'Names, addresses, job titles, and salary of public employees are not covered by this exemption',
            'Information that is already publicly available (e.g., published in a court record) cannot be withheld under this exemption',
            'Challenge overbroad redactions where the agency has removed non-exempt contextual information along with the specific protected data',
            'The "personal privacy" exemption requires a showing that disclosure would be "clearly unwarranted" — a high bar for information about public employees',
        ]),
        'notes': 'RCW 42.56.230 covers a broad range of personal information, but Washington courts strictly limit it to the enumerated categories. The general personal privacy exemption under RCW 42.56.230(3) requires that disclosure constitute a "clearly unwarranted invasion of personal privacy" — agencies bear this burden. See Hearst Corp. v. Hoppe, 90 Wn.2d 123 (1978) for the foundational privacy analysis.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.240',
        'exemption_number': 'RCW 42.56.240',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of law enforcement investigations are exempt if disclosure would reveal the identity of a confidential informant, endanger a person\'s life or physical safety, reveal investigative techniques, or if the investigation is ongoing and disclosure would interfere with the proceeding.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) reveal the identity of a confidential informant; (2) reveal investigative techniques or procedures; (3) endanger the life or physical safety of any person; (4) cause a criminal defendant to escape prosecution; or (5) interfere with pending litigation. Completed investigations do not retain the same protection — when prosecution is complete or investigation closed, records generally become public. Factual portions that do not implicate any enumerated harm must be released. RCW 42.56.240(1) also covers specific categories like undercover officers and the names of juvenile crime victims.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'pending investigation', 'ongoing investigation',
            'undercover officer', 'interference with prosecution', 'endangerment',
            'RCW 42.56.240',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is not a blanket protection for all law enforcement records — each withheld document must implicate a specific enumerated harm',
            'Once prosecution concludes or investigation is closed, the interference rationale evaporates and records become public',
            'Factual information in investigative files that does not reveal informants or techniques must be segregated and released',
            'Arrest records, booking information, and incident reports documenting the existence and nature of the incident are generally public regardless of investigation status',
            'Challenge claims that disclosure would "reveal investigative techniques" where the technique is standard police procedure widely known to the public',
            'Washington courts apply a strict construction of law enforcement exemptions in favor of disclosure',
            'The agency must identify with specificity which harm applies to each withheld record — a generic "investigation ongoing" response is insufficient',
        ]),
        'notes': 'RCW 42.56.240 is one of Washington\'s most litigated exemptions. Washington courts consistently hold that the exemption does not protect completed investigation files. See Neighborhood Alliance of Spokane County v. County of Spokane, 172 Wn.2d 702 (2011). The Washington Supreme Court applies a strict construction: any ambiguity goes against withholding. Per diem penalties apply if records are unjustifiably withheld.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.280',
        'exemption_number': 'RCW 42.56.280',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, and intra-agency memorandums relating to an agency\'s deliberative process are exempt from disclosure to the extent that they contain opinions on legal or policy matters and are not adopted as the agency\'s position.',
        'scope': 'Preliminary drafts, notes, recommendations, and intra-agency or inter-agency memorandums, but only to the extent that they: (1) contain opinions on legal or policy matters; and (2) have not been adopted as the agency\'s final position. RCW 42.56.280 does NOT protect purely factual material, even if embedded in a deliberative document. Factual data underlying recommendations must be segregated and released. Final agency decisions, working law, and adopted policies are not covered. The exemption is narrow — Washington courts strictly limit it and frequently require partial production.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memorandum',
            'predecisional', 'working paper', 'recommendation', 'advisory opinion',
            'policy deliberation', 'draft document', 'opinion on legal matter',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released — the exemption covers only opinion and recommendation portions',
            'Once a draft or recommendation is adopted as the agency\'s final position, the exemption no longer applies',
            '"Working law" — standards and criteria agencies actually apply in practice — must be disclosed even if in internal documents',
            'Challenge claims that entire documents are deliberative where only recommendation sections qualify',
            'Documents circulated for comment to persons outside the agency may lose their predecisional character',
            'Washington courts apply the exemption narrowly and have been hostile to agencies using it as a general shield against accountability',
            'The agency must demonstrate that the specific document, or the specific portion claimed, is opinion-based and predecisional',
        ]),
        'notes': 'RCW 42.56.280 is Washington\'s analog to the federal deliberative process privilege, but it is codified and strictly limited by the PRA\'s strong disclosure mandate in RCW 42.56.030. Washington courts hold that the exemption must be narrowly construed. See Hearst Corp. v. Hoppe, 90 Wn.2d 123 (1978). The factual/opinion distinction is critical: factual data does not become deliberative just because it is included in a memo.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.290; RCW 5.60.060',
        'exemption_number': 'RCW 42.56.290',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records that are subject to the attorney-client privilege or work-product doctrine are exempt from disclosure under the PRA. The exemption tracks the common-law and statutory privilege (RCW 5.60.060) as applied to government attorneys.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and work product prepared by attorneys in anticipation of litigation. The attorney-client privilege for government entities in Washington is narrow: it requires that the communication be for legal advice (not business or policy advice), made in confidence, and not waived through disclosure. Billing records, retainer agreements, and general financial arrangements with outside counsel are generally not privileged. Facts independently known are not protected merely because they were communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'confidential communication',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice, not general business or policy guidance — the latter is not privileged',
            'Waiver occurs when the agency discloses the content in public proceedings, to non-attorney staff not involved in the legal matter, or to third parties',
            'Attorney billing records and invoices describing services rendered are generally public under Washington law',
            'The privilege belongs to the agency, which may waive it — challenge whether the agency has constructively waived by using the advice in public decision-making',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and opinion',
            'Washington courts apply the privilege narrowly given the PRA\'s strong disclosure mandate',
        ]),
        'notes': 'Washington recognizes attorney-client privilege and work product protection for government entities as incorporated into the PRA by RCW 42.56.290. The Washington Supreme Court has held that the privilege is not automatically waived when a government body takes action based on legal advice, but has also held that the strong PRA disclosure mandate limits the privilege\'s reach. See Soter v. Cowles Pub. Co., 162 Wn.2d 716 (2007).',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.270(1); RCW 19.108.010',
        'exemption_number': 'RCW 42.56.270(1)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Valuable commercial information whose disclosure would enable a competitor to profit or whose disclosure would impair the ability of the affected party to compete is exempt from public disclosure as a trade secret under the Uniform Trade Secrets Act.',
        'scope': 'Information submitted by private entities to government agencies that: (1) derives independent economic value from not being generally known; (2) is subject to reasonable measures to maintain secrecy; and (3) whose disclosure would cause competitive harm. Washington applies the Uniform Trade Secrets Act definition (RCW 19.108.010). Government-generated records cannot constitute trade secrets — only privately submitted information qualifies. The agency must independently evaluate trade secret designations and may not simply defer to vendor claims.',
        'key_terms': json.dumps([
            'trade secret', 'competitive harm', 'proprietary information', 'UTSA',
            'Uniform Trade Secrets Act', 'commercial information', 'economic value',
            'confidential business information', 'competitive advantage', 'secrecy',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate that the information meets the UTSA definition — a "confidential" stamp is not sufficient',
            'Publicly available information cannot qualify as a trade secret regardless of the submitter\'s designations',
            'Information required by law to be submitted to the government has reduced expectations of secrecy',
            'Government expenditures, contract pricing, and amounts paid with public funds are generally public regardless of trade secret claims',
            'Challenge whether the submitter actually maintained reasonable secrecy measures — careless disclosure elsewhere defeats the claim',
            'The agency, not the submitter, controls the final determination and must apply an independent analysis',
        ]),
        'notes': 'Washington\'s trade secret exemption under RCW 42.56.270(1) applies the UTSA framework. The Washington Supreme Court has held that agencies must conduct an independent analysis of trade secret claims and may not simply accept vendor designations. Contract amounts paid with public funds are uniformly public. See Confederated Tribes of Chehalis Reservation v. Johnson, 135 Wn.2d 734 (1998).',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.250',
        'exemption_number': 'RCW 42.56.250',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property and personal property appraisals and related documents prepared by or for an agency in connection with the acquisition or sale of the property are exempt until the transaction is complete or withdrawn.',
        'scope': 'Real estate appraisals, feasibility studies, property evaluations, and related valuation documents prepared by or for a government agency in connection with prospective acquisition or sale of real property. The exemption applies only until the transaction is complete, cancelled, or abandoned — at which point the records become public. The exemption exists to prevent agencies from being disadvantaged in negotiations if their maximum willingness to pay is disclosed pre-purchase. Post-transaction, all appraisal records are public.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'feasibility study', 'pre-acquisition', 'real property',
            'land purchase', 'property sale', 'condemnation appraisal',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires automatically when the transaction is complete, cancelled, or abandoned — post-transaction appraisals are public',
            'Challenge the agency\'s claim that the transaction remains "pending" if there has been no activity for an extended period',
            'Appraisals for property already owned by the agency (not in acquisition mode) are not covered',
            'Budget documents and agency discussions about the general property value range may not qualify if they are not formal appraisals',
            'After a final condemnation judgment, all valuation records are public',
        ]),
        'notes': 'RCW 42.56.250 is a time-limited exemption that automatically expires upon transaction completion. Washington courts have narrowly defined "appraisal" for purposes of this exemption — it must be a formal valuation document, not general internal discussions about property value.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.300',
        'exemption_number': 'RCW 42.56.300',
        'short_name': 'Archaeological and Cultural Site Information',
        'category': 'safety',
        'description': 'The locations, descriptions, and related records identifying specific archaeological sites, historic properties, or the locations of Native American burials and sacred sites are exempt from disclosure to protect against looting, vandalism, and desecration.',
        'scope': 'Specific location data, site descriptions, survey data, and records that identify the precise location of archaeological sites, historic properties eligible for or listed on the National Register of Historic Places, and Native American burial grounds and sacred sites. The exemption is narrowly targeted at location information that would enable looting or vandalism — aggregate statistics about the number of sites, general descriptions of historical periods, and information about site protection programs are public. Tribal cultural resource records held by tribal governments may have additional protections.',
        'key_terms': json.dumps([
            'archaeological site', 'historic property', 'Native American burial',
            'sacred site', 'cultural resource', 'site location', 'looting',
            'vandalism prevention', 'NHPA', 'National Register of Historic Places',
        ]),
        'counter_arguments': json.dumps([
            'General information about historical periods, cultural traditions, and the existence of site protection programs is public',
            'Aggregate statistics about the number and types of sites (without specific locations) are not covered',
            'Challenge claims that budget, staffing, and operational records for site protection programs are exempt',
            'Widely known or published site locations (e.g., in academic literature) cannot be withheld under this exemption',
        ]),
        'notes': 'RCW 42.56.300 reflects Washington\'s commitment to protecting tribal cultural heritage and archaeological resources from looting. The exemption is location-specific — it does not protect the existence of archaeological programs, funding levels, or general findings from cultural resource studies.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.420',
        'exemption_number': 'RCW 42.56.420',
        'short_name': 'Security Plans for Public Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and related records for critical infrastructure, public buildings, and emergency response systems are exempt where disclosure would create a specific security risk.',
        'scope': 'Security plans, vulnerability assessments, access control systems, intrusion detection systems, and similar operational security documents for public buildings, critical infrastructure (water systems, power grids, transportation networks), and emergency management systems. The exemption requires that disclosure would create a specific security risk — it does not cover all security-related records. Budget records, contracts, and expenditure data for security programs are generally public. The agency must articulate the specific harm from disclosure for each withheld record.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'access control', 'intrusion detection', 'emergency response',
            'public building security', 'infrastructure protection', 'cyber security',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative or general',
            'Budget and expenditure records for security programs are public regardless of this exemption',
            'Physical security plans for non-critical facilities with widely known access patterns do not qualify',
            'Challenge claims that entire contracts with security vendors are exempt when only specific technical details warrant protection',
            'General descriptions of security policies and procedures that do not reveal vulnerabilities are not covered',
        ]),
        'notes': 'RCW 42.56.420 is one of several security-related exemptions in Washington\'s PRA. Washington courts have applied it narrowly consistent with the overall disclosure mandate. Agencies must demonstrate a specific, articulable security risk — not merely assert that the records are "security-related."',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.230(5); RCW 29A.08.720',
        'exemption_number': 'RCW 42.56.230(5)',
        'short_name': 'Voter Registration — Personal Details',
        'category': 'privacy',
        'description': 'Certain personal details in voter registration records — specifically signatures, Social Security numbers, driver\'s license numbers, and dates of birth — are exempt from public disclosure to protect voters from identity theft and harassment.',
        'scope': 'Specific personal data fields within voter registration records: voter signatures, Social Security numbers or portions thereof, driver\'s license numbers, and dates of birth. The exemption is field-specific — the voter\'s name, registration status, address, and voting history are generally public. The name and address fields in voter registration data have historically been available to candidates, political parties, and researchers. The signature is protected because it can be misused for identity fraud. RCW 29A.08.720 provides additional protections for voter address confidentiality in cases of domestic violence or stalking.',
        'key_terms': json.dumps([
            'voter registration', 'voter signature', 'voter SSN', 'date of birth',
            'driver\'s license number', 'voter data', 'election records', 'voter privacy',
            'address confidentiality', 'RCW 29A.08.720',
        ]),
        'counter_arguments': json.dumps([
            'Voter names, addresses (with limited exception for protected persons), party affiliation, and voting history are generally public',
            'The exemption is field-specific — the agency must release the remainder of the voter file with protected fields redacted',
            'Aggregate election results and voter turnout data are fully public',
            'Challenge claims that entire voter files are exempt when only specific fields (SSN, DOB, signature) warrant protection',
        ]),
        'notes': 'Washington\'s voter registration exemption reflects the balance between democratic transparency (voter rolls as public records) and individual privacy and safety. RCW 29A.08.720 provides an additional address confidentiality program for voters who are victims of domestic violence, sexual assault, or stalking, allowing them to use a substitute address in public records.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.400(1); RCW 30A.04.075',
        'exemption_number': 'RCW 42.56.400(1)',
        'short_name': 'Financial Institution Examination Records',
        'category': 'commercial',
        'description': 'Examination reports, confidential supervisory information, and related records of the Department of Financial Institutions and the Office of the Insurance Commissioner relating to the examination and supervision of financial institutions are exempt from public disclosure.',
        'scope': 'Confidential supervisory information produced in connection with the examination and regulation of banks, credit unions, insurance companies, mortgage lenders, and other financial institutions licensed in Washington. Includes examination reports, matters requiring attention (MRA) letters, safety-and-soundness findings, and related correspondence between regulators and regulated entities. Aggregate financial data, enforcement orders, final settlements, consent agreements, and license status are generally public. The exemption is designed to protect the candid exchange of information between regulators and regulated entities that is essential to effective supervision.',
        'key_terms': json.dumps([
            'financial institution examination', 'supervisory information', 'bank examination',
            'Department of Financial Institutions', 'DFI', 'Insurance Commissioner',
            'examination report', 'safety and soundness', 'confidential supervisory information',
            'bank regulation',
        ]),
        'counter_arguments': json.dumps([
            'Final enforcement orders, consent agreements, and public sanctions are not covered — they are public regardless of this exemption',
            'License status, licensing history, and financial data aggregated for public reporting are public',
            'Challenge claims that all correspondence between a regulator and a financial institution is "examination records"',
            'Information about final regulatory decisions that affected the public (e.g., bank closures) is public',
        ]),
        'notes': 'Financial institution examination records are a standard categorical exemption in Washington\'s PRA, reflecting the federal model of confidential banking supervision. The exemption does not cover public enforcement actions — those are public record from the moment of issuance.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.230(2); RCW 82.32.330',
        'exemption_number': 'RCW 42.56.230(2)',
        'short_name': 'Tax Return Information',
        'category': 'statutory',
        'description': 'State tax return information submitted to or held by the Department of Revenue is confidential and exempt from public disclosure under RCW 82.32.330, which is incorporated into the PRA framework as a statutory confidentiality provision.',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individual or business taxpayers to the Washington Department of Revenue. Covers both business and occupation (B&O) tax, retail sales tax, and other state tax filings. RCW 82.32.330 establishes the specific confidentiality rule within the tax code, and RCW 42.56.230(2) cross-references tax information as a PRA exemption category. Aggregate tax statistics, revenue reports, and information about the Department\'s own operations are public. Specific tax enforcement actions and final judgments in tax disputes are generally public once filed in court.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'business and occupation tax',
            'B&O tax', 'sales tax return', 'taxpayer information', 'tax filing',
            'RCW 82.32.330', 'tax confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Tax delinquency notices and final court judgments in tax collection cases are public',
            'Information about the Department\'s own operations and enforcement programs is public',
            'Challenge whether the specific records requested are actually "tax return information" vs. general regulatory correspondence',
        ]),
        'notes': 'Washington\'s tax return confidentiality is one of the most clearly established and consistently enforced PRA exemptions. RCW 82.32.330 prohibits the Department of Revenue from disclosing tax return information, and this prohibition is incorporated into the PRA framework. The exemption applies to individual returns, not to aggregate data.',
    },
    {
        'jurisdiction': 'WA',
        'statute_citation': 'RCW 42.56.310; RCW 27.04.055',
        'exemption_number': 'RCW 42.56.310',
        'short_name': 'Library Records — Patron Privacy',
        'category': 'privacy',
        'description': 'Library circulation records, database access logs, borrower records, and other records identifying what library materials a specific patron accessed, checked out, or requested are exempt from public disclosure to protect intellectual privacy and freedom of inquiry.',
        'scope': 'Records identifying which specific library patrons accessed, borrowed, requested, or inquired about specific library materials or databases. Covers physical circulation records, electronic database access logs, interlibrary loan requests, and reference inquiries that reveal the specific reading interests of identifiable individuals. The exemption applies to public library records as well as school and academic library records at public institutions. Aggregate statistics about library usage, circulation counts, and collection data are public. Library administrative records, budget documents, and personnel files are public.',
        'key_terms': json.dumps([
            'library records', 'circulation records', 'library patron', 'borrower records',
            'database access', 'reading privacy', 'intellectual privacy', 'interlibrary loan',
            'library privacy', 'RCW 27.04.055',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate library usage statistics, total circulation counts, and collection data are not covered',
            'Library administrative records, contracts, and budget documents are fully public',
            'Records subpoenaed for a criminal investigation may be disclosed pursuant to court order regardless of this exemption',
            'The exemption covers what patrons read — not library operations, programming, or personnel',
        ]),
        'notes': 'Washington\'s library patron privacy exemption reflects the strong public policy that individuals should be able to access information without fear of government surveillance. RCW 27.04.055 specifically addresses library records confidentiality, and RCW 42.56.310 incorporates library records as a PRA exemption. The protection is absolute for patron-specific data — there is no balancing test.',
    },
]

# =============================================================================
# RULES
# Washington Public Records Act, RCW 42.56
# Washington has the most explicit statutory language of any state regarding
# agency obligations: "fullest assistance" and "most timely possible action"
# are statutory commands, not mere aspirational statements (RCW 42.56.100).
# The 5-business-day acknowledgment deadline, per diem penalties, mandatory
# attorney fees, and the direct-to-court enforcement model are distinctive.
# =============================================================================

WA_RULES = [
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'acknowledge_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'RCW 42.56.520',
        'notes': 'Washington agencies must acknowledge receipt of a PRA request and provide an estimate of when records will be available within 5 business days of receiving the request. This is a mandatory deadline — failure to acknowledge within 5 business days is itself a violation of the PRA that can support per diem penalties. The acknowledgment must be substantive: a bare receipt confirmation without an estimated production timeline does not satisfy the requirement. Agencies may also ask clarifying questions in the acknowledgment to refine the request.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'fullest_assistance_mandate',
        'param_value': 'statutory_requirement',
        'day_type': None,
        'statute_citation': 'RCW 42.56.100',
        'notes': 'RCW 42.56.100 imposes the strongest statutory assistance obligation in the United States: agencies must "adopt and enforce reasonable rules and regulations" to provide the "fullest assistance" and "most timely possible action" on requests. This is a direct statutory mandate, not an aspiration. Washington courts have held that an agency\'s failure to provide "fullest assistance" — including failing to help requesters describe records with sufficient specificity — is an independent PRA violation. Agencies may not take a passive or obstructive posture on requests.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'installment_production_allowed',
        'param_value': 'yes_with_active_notification',
        'day_type': None,
        'statute_citation': 'RCW 42.56.080',
        'notes': 'Agencies may produce records in installments (rolling production) for large requests where all records cannot be produced at once. Under RCW 42.56.080, an agency providing records in installments must actively notify the requester of the installment schedule and estimated production dates for remaining records. Agencies may not use installment production as a delay tactic — courts have imposed per diem penalties when installment timelines were unreasonably extended. The agency must actively update the requester if the schedule changes.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'fee_cap',
        'param_key': 'actual_cost_standard',
        'param_value': 'actual_cost_of_reproduction',
        'day_type': None,
        'statute_citation': 'RCW 42.56.120',
        'notes': 'Washington agencies may charge only the actual cost of reproducing records — not the staff time spent locating or reviewing records, not overhead, not attorney review time. For paper copies, actual cost is typically the cost of paper and toner. For electronic records, actual cost is minimal. RCW 42.56.120 explicitly prohibits charging for the time spent separating exempt from nonexempt content — that labor is part of the agency\'s public obligation. Fee schedules must be published and adopted by rule. A fee that is disproportionate to actual reproduction costs may constitute an unlawful barrier to access.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate',
        'param_value': '0.15',
        'day_type': None,
        'statute_citation': 'RCW 42.56.120(2)',
        'notes': 'If an agency has not adopted its own fee schedule by rule, the default rate for paper copies is $0.15 per page under RCW 42.56.120(2). Agencies with adopted fee schedules may charge different rates, but those rates must reflect actual cost of reproduction. The $0.15 default is among the most clearly specified default copy rates of any state PRA statute. For electronic records, the default rate is the actual cost of the digital medium or transmission — often zero for email delivery.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'RCW 42.56.120',
        'notes': 'Washington\'s PRA does not mandate fee waivers for any requester category. Agencies may waive fees at their discretion, and many do so for journalists, nonprofits, and academic researchers. However, there is no legal right to a fee waiver. Requesters can argue that the public interest in disclosure supports a fee waiver as consistent with the "fullest assistance" mandate. For electronic records delivered by email, the actual cost is often zero, effectively making a fee waiver moot for many requests.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'RCW 42.56.550',
        'notes': 'Washington has NO formal administrative appeal mechanism for PRA denials. There is no agency head appeal, no ombudsman review, and no administrative tribunal. A requester who is denied access, or whose request is unreasonably delayed, must go directly to superior court under RCW 42.56.550. Washington is one of the few states where direct judicial enforcement is the sole formal remedy. This makes Washington\'s PRA enforcement simultaneously more powerful (courts can impose per diem penalties) and more demanding (litigation required for enforcement).',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'RCW 42.56.550',
        'notes': 'A requester denied access to records, or whose request is unreasonably delayed, may seek enforcement in superior court under RCW 42.56.550. The court reviews the denial de novo and may conduct in camera review of withheld records. The court may order the agency to produce records and impose per diem penalties. There is no statute of limitations specified, but unreasonable delay in bringing suit may affect the court\'s discretion on penalties. Cases may be brought in the superior court of the county where the agency is located or where the requester resides.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'penalty',
        'param_key': 'per_diem_penalty_range',
        'param_value': '$5-$100 per day',
        'day_type': None,
        'statute_citation': 'RCW 42.56.550(4)',
        'notes': 'Washington\'s PRA imposes unique per diem penalties of $5 to $100 per day, per record, for each day the agency unjustifiably withholds or delays records. This is one of the most distinctive enforcement mechanisms in US public records law. The court sets the daily penalty amount based on the egregiousness of the violation. Per diem penalties run from the date of the wrongful denial (or after a reasonable production period) through the date records are actually produced. For large record sets or prolonged withholding, per diem penalties can accumulate to substantial amounts. The penalty is intended to be punitive and deterrent.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_mandatory',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'RCW 42.56.550(4)',
        'notes': 'Washington\'s PRA mandates attorney fees and costs for a prevailing requester — unlike most states where fees are discretionary. If a requester substantially prevails in a PRA lawsuit, the court SHALL (not "may") award reasonable attorney fees, other litigation costs, and the per diem penalty amount. The mandatory fee-shifting provision makes it economically viable for requesters and their attorneys to bring PRA enforcement actions even for modest-size requests. This is one of the strongest fee-shifting provisions in any state records statute.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'RCW 42.56.080',
        'notes': 'Washington agencies may NOT require requesters to identify themselves or state the purpose of their request. The PRA provides a universal right of access regardless of identity, citizenship, or stated purpose. Requiring identification as a condition of access is improper. Anonymous and pseudonymous requests are valid. Some agencies have online portals that request contact information for delivery purposes, but providing that information must be voluntary and may not be required.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'RCW 42.56.210(1)',
        'notes': 'Washington agencies must release all nonexempt portions of records when only part of a record qualifies for an exemption. RCW 42.56.210(1) explicitly requires agencies to delete exempt portions and release the remainder. Blanket withholding of documents containing some exempt content is a PRA violation. The agency must segregate and release all nonexempt, reasonably segregable material. Failure to segregate can support per diem penalties. This is one of the most vigorously enforced provisions of the PRA in Washington court practice.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'RCW 42.56.030',
        'notes': 'The burden of demonstrating that any record is exempt from disclosure is entirely on the agency, not the requester. RCW 42.56.030 establishes a strong presumption that all government records are public. An agency claiming an exemption must affirmatively demonstrate that the specific exemption applies to each specific withheld record. General assertions of exemption categories without record-specific justification are insufficient. Washington courts review PRA withholding decisions de novo — there is no deference to the agency\'s initial determination.',
    },
    {
        'jurisdiction': 'WA',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'RCW 42.56.080',
        'notes': 'Washington does not require public records requests to be submitted in writing. Oral requests are valid under the PRA. However, written requests are strongly recommended to create a paper trail, establish the 5-business-day acknowledgment deadline, and document the scope of the request. Many agencies have adopted online request portals or have designated public records officers who accept email requests. The 5-business-day clock for acknowledgment begins on receipt of a written or oral request.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

WA_TEMPLATES = [
    {
        'jurisdiction': 'WA',
        'record_type': 'general',
        'template_name': 'General Washington Public Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — RCW 42.56

Dear Public Records Officer:

Pursuant to the Washington Public Records Act, RCW 42.56 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes both cost and production time.

I am willing to pay reasonable fees reflecting the actual cost of reproduction per RCW 42.56.120. I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Washington law. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or arrange payment.

Under RCW 42.56.030, all government records are presumptively public and the burden of demonstrating that any record is exempt rests entirely on the agency. Under RCW 42.56.100, the agency must provide the "fullest assistance" and "most timely possible action" on this request. Under RCW 42.56.210(1), the agency must release all nonexempt, reasonably segregable portions of any record where only part qualifies for exemption.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) state the specific statutory basis for withholding (RCW citation), not merely an exemption category; (3) describe the record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all nonexempt, segregable portions of partially withheld records have been released.

Under RCW 42.56.520, please acknowledge receipt of this request and provide an estimated production date within 5 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Washington\'s Public Records Act does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically (via email or download link), the actual cost of reproduction is zero, making a fee waiver consistent with both the letter and spirit of RCW 42.56.120.

Washington's PRA is premised on the "fullest assistance" mandate of RCW 42.56.100. A fee waiver for this request would advance that mandate.''',
        'expedited_language': '''I request that this PRA request be processed as expeditiously as possible under the "most timely possible action" mandate of RCW 42.56.100. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

Please contact me immediately if there are any questions that would allow faster production of the records.''',
        'notes': 'General-purpose Washington PRA template. Key Washington features: (1) 5-business-day acknowledgment deadline — cite RCW 42.56.520; (2) "fullest assistance" and "most timely possible action" are statutory mandates under RCW 42.56.100, not aspirations; (3) no administrative appeal — go directly to superior court if denied (RCW 42.56.550); (4) per diem penalties of $5-$100/day for unjustified withholding; (5) mandatory attorney fees if requester prevails; (6) actual cost only for fees — no staff time charges; (7) default copy rate $0.15/page if agency has no adopted schedule. Reference RCW 42.56, not "FOIA."',
    },
    {
        'jurisdiction': 'WA',
        'record_type': 'law_enforcement',
        'template_name': 'Washington PRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Act Request — Law Enforcement Records, RCW 42.56

Dear Public Records Officer:

Pursuant to the Washington Public Records Act, RCW 42.56 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Written communications (email, text, radio logs) relating to the above
- Internal investigation records relating to the above incident

Regarding claimed exemptions under RCW 42.56.240: Washington law does not permit blanket withholding of law enforcement records. Any withholding under RCW 42.56.240 requires: (1) identification of the specific exemption subcategory that applies (e.g., identifies confidential informant; would endanger life; would interfere with pending prosecution); and (2) articulation of how disclosure of each specific record — not records of this general type — would cause that specific harm.

[If matter appears concluded:] If no criminal prosecution is pending or if any related prosecution has concluded, please apply the standard that applies to completed investigations — the interference rationale under RCW 42.56.240 does not apply to closed matters.

Under RCW 42.56.030, the burden of demonstrating that any record is exempt rests on the agency. Under RCW 42.56.210(1), all nonexempt, segregable portions of partially withheld records must be released. Under RCW 42.56.100, the agency must provide the "fullest assistance" and "most timely possible action."

I am willing to pay the actual cost of reproduction per RCW 42.56.120, up to ${{fee_limit}}, but not charges for staff review time.

Please acknowledge receipt and provide an estimated production date within 5 business days per RCW 42.56.520.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. Electronic delivery incurs zero reproduction cost. A fee waiver is consistent with Washington\'s "fullest assistance" mandate under RCW 42.56.100.''',
        'expedited_language': '''I request expedited processing of this PRA request under RCW 42.56.100\'s "most timely possible action" mandate. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Washington law enforcement records template. Washington-specific features: (1) RCW 42.56.240 is strictly construed — agencies must articulate harm specific to each withheld record, not broad categories; (2) completed investigation files are generally public once prosecution concludes; (3) body camera footage is public under Washington\'s PRA absent specific enumerated harm; (4) per diem penalties ($5-$100/day) apply to unjustified withholding — cite this to signal serious enforcement intent; (5) no administrative appeal — RCW 42.56.550 provides for direct superior court enforcement with mandatory fees for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in WA_EXEMPTIONS:
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

    print(f'WA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in WA_RULES:
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

    print(f'WA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in WA_TEMPLATES:
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

    print(f'WA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'WA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_wa', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
