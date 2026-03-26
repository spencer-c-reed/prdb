#!/usr/bin/env python3
"""Build Arizona Public Records Law data: exemptions, rules, and templates.

Covers Arizona's Public Records Law, A.R.S. §§ 39-121 through 39-161.
Arizona has one of the strongest public access presumptions in the country —
relatively few categorical exemptions, with courts applying a balancing test
(Carlson v. Pima County) for claimed privacy interests.

Run: python3 scripts/build/build_az.py
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
# Arizona has fewer categorical exemptions than most states. The primary
# framework is: (1) confidential by statute; (2) the Carlson balancing test
# for privacy (weighs individual privacy against public benefit of disclosure);
# (3) specific common-law privileges. Courts construe disclosure broadly.
# =============================================================================

AZ_EXEMPTIONS = [
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121; Carlson v. Pima County, 141 Ariz. 487 (1984)',
        'exemption_number': 'Carlson balancing test',
        'short_name': 'Privacy Balancing Test (Carlson)',
        'category': 'privacy',
        'description': 'Arizona does not have a general privacy exemption in the Public Records Law. Instead, courts apply a balancing test from Carlson v. Pima County: the privacy interest of the individual is weighed against the public interest in disclosure. The party seeking confidentiality must show a significant privacy interest that outweighs the public benefit.',
        'scope': 'Any record where an individual claims a privacy interest. The Carlson test requires weighing: (1) the nature of the privacy interest; (2) the public interest in disclosure; (3) the potential harm from disclosure. Unlike most states, Arizona has no general privacy exemption codified in the statute — the balancing test is entirely judge-made. Courts and agencies apply it to personnel records, medical information, and similar data.',
        'key_terms': json.dumps([
            'Carlson balancing test', 'privacy interest', 'public benefit', 'individual privacy',
            'balancing test', 'personnel records', 'medical information', 'privacy vs. disclosure',
            'confidentiality interest',
        ]),
        'counter_arguments': json.dumps([
            'The party claiming confidentiality bears the burden of demonstrating a significant privacy interest — the default is disclosure',
            'Public employees have minimal privacy interests in their official conduct, salary, and disciplinary records',
            'The public interest in government accountability is strong and is given significant weight by Arizona courts',
            'Articulate the specific public benefit of disclosure — courts weigh this directly against the claimed privacy interest',
            'Carlson does not protect embarrassing information; the privacy interest must be legally cognizable, not merely personal preference for secrecy',
            'Arizona courts have consistently held that routine personnel files of government employees are public, applying Carlson broadly in favor of disclosure',
            'Challenge whether the claimed privacy interest is specific and concrete, not speculative',
        ]),
        'notes': 'The foundational Arizona case for public records privacy analysis. Carlson v. Pima County, 141 Ariz. 487, 687 P.2d 1242 (1984) established the balancing test that Arizona courts and the AG apply when agencies claim records are private. The test strongly favors disclosure in matters of government accountability. See also Scottsdale Unified School Dist. No. 48 v. KPNX Broadcasting Co., 191 Ariz. 297 (1998).',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121 (confidential by statute)',
        'exemption_number': 'Statutory Confidentiality',
        'short_name': 'Confidential by Other Statute',
        'category': 'statutory',
        'description': 'Records that are specifically designated as confidential by another Arizona statute or federal law are exempt from the Public Records Law.',
        'scope': 'Records that a specific Arizona statute or federal law declares confidential or restricts from public disclosure. Arizona courts construe this category narrowly: a statute must affirmatively declare the records confidential or restricted, not merely regulate the information. Examples include certain tax records (A.R.S. § 42-2001), child welfare records (A.R.S. § 8-807), and medical records governed by specific statutes.',
        'key_terms': json.dumps([
            'confidential by statute', 'specifically designated', 'statutory exemption',
            'federal law', 'tax records', 'child welfare', 'restricted by law',
            'affirmative prohibition',
        ]),
        'counter_arguments': json.dumps([
            'The statute must affirmatively prohibit disclosure — a general confidentiality policy or agency regulation is not sufficient',
            'Challenge whether the specific record at issue falls within the scope of the cited exempting statute',
            'Arizona courts interpret statutory exemptions narrowly and in favor of disclosure',
            'A statute that merely regulates the use of records, without prohibiting disclosure, does not qualify',
            'If the agency is citing federal law, confirm the federal statute actually mandates confidentiality rather than merely permitting it',
        ]),
        'notes': 'Arizona courts apply a strict construction to statutory exemptions. The Arizona AG has repeatedly opined that only statutes that affirmatively prohibit or restrict disclosure — not merely regulations or policy — qualify as statutory exemptions to the Public Records Law.',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-123; A.R.S. § 39-124',
        'exemption_number': '§ 39-123 / § 39-124',
        'short_name': 'Law Enforcement Records — Investigations',
        'category': 'law_enforcement',
        'description': 'Criminal investigation records are protected if disclosure would interfere with a pending prosecution or investigation. The protection expires when the prosecution is completed or the investigation is closed.',
        'scope': 'Records of active criminal investigations and prosecutions where disclosure would: (1) endanger the life or physical safety of any person; (2) interfere with a pending criminal investigation; (3) reveal the identity of a confidential informant; (4) reveal the identity of an undercover officer; or (5) unreasonably invade the privacy of a crime victim. The exemption is narrower than many states — it requires a specific articulated harm from disclosure, not just an active investigation.',
        'key_terms': json.dumps([
            'criminal investigation', 'pending prosecution', 'active investigation',
            'confidential informant', 'undercover officer', 'crime victim privacy',
            'investigation interference', 'endanger life',
        ]),
        'counter_arguments': json.dumps([
            'Arizona requires a specific, articulable harm from disclosure — not just that an investigation is ongoing',
            'Once prosecution is complete or the investigation is closed, the exemption no longer applies',
            'Factual portions of investigative records that do not identify informants or reveal investigation methods may be segregable',
            'Arrest records, booking information, and police incident reports are generally public regardless of ongoing investigation status',
            'Challenge the agency to specify which of the enumerated harms would result from disclosure of each withheld record',
            'The privacy interest of crime victims must be balanced against the public interest in accountability — it is not absolute',
        ]),
        'notes': 'Arizona\'s law enforcement exemption is more limited than many states. A.R.S. § 39-123 protects only the specific categories enumerated. The Arizona AG and courts have held that agencies must articulate the specific harm category for each withheld item. See Carlson v. Pima County and Arpaio v. Figueroa, 229 Ariz. 364 (App. 2012).',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121 (common law privilege)',
        'exemption_number': 'Attorney-Client Privilege',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Attorney-client communications between a government agency and its legal counsel, and attorney work product, are protected from disclosure under the common law attorney-client privilege as incorporated into the Public Records Law.',
        'scope': 'Confidential legal advice communications between government agencies and their attorneys, and work product prepared in anticipation of litigation. Arizona courts recognize the attorney-client privilege for government entities but apply it narrowly. Business or policy advice that does not constitute legal advice is not covered. Facts known independently of the attorney-client relationship are not protected.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'legal advice', 'work product', 'litigation',
            'privileged communication', 'government attorney', 'legal opinion', 'confidential',
        ]),
        'counter_arguments': json.dumps([
            'Arizona applies attorney-client privilege narrowly for government entities given the strong public interest in transparency',
            'Communications primarily about business or policy decisions, not legal strategy or advice, are not privileged',
            'Waiver: public disclosure or use of the legal advice in public proceedings may waive the privilege',
            'Billing invoices and retainer agreements are generally public',
            'The privilege belongs to the agency, not the attorney — the agency can waive it',
            'Challenge whether the communication was made in confidence for the purpose of legal advice, or merely for business advice',
        ]),
        'notes': 'Arizona recognizes the attorney-client privilege for government entities as a common-law protection incorporated into the public records framework. See Samaritan Foundation v. Goodfarb, 176 Ariz. 497 (1993). The privilege is narrower in the government context because of the public\'s interest in accountability.',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121 (common law); A.R.S. § 44-401 (trade secrets)',
        'exemption_number': 'Trade Secrets',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets submitted by private entities to government agencies may be protected from public records disclosure where the submitter can demonstrate the information meets the statutory definition of a trade secret and that disclosure would cause competitive harm.',
        'scope': 'Commercially sensitive information submitted by private parties to government agencies that: (1) derives independent economic value from not being generally known; (2) is subject to reasonable efforts to maintain secrecy; and (3) whose disclosure would cause substantial competitive harm. Arizona applies the Uniform Trade Secrets Act definition (A.R.S. § 44-401). Government-generated records are not trade secrets.',
        'key_terms': json.dumps([
            'trade secret', 'competitive harm', 'proprietary information', 'economic value',
            'confidential business information', 'Uniform Trade Secrets Act', 'UTSA',
            'reasonable secrecy measures', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must affirmatively demonstrate the trade secret definition is met — a "confidential" label is insufficient',
            'Publicly available information cannot be a trade secret',
            'The agency, not the submitter, determines whether the exemption applies',
            'Information required to be submitted to the government by law has a reduced expectation of secrecy',
            'Government expenditures reflected in contracts are public regardless of trade secret claims',
            'Challenge whether the submitter actually took reasonable steps to maintain secrecy',
        ]),
        'notes': 'Arizona courts have applied the UTSA definition to public records trade secret claims. The agency must independently evaluate trade secret claims rather than deferring to vendor designations. See Arizona Newspapers Assoc. v. Small Business Administration (federal analogue applied by AZ courts).',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121 (deliberative process)',
        'exemption_number': 'Deliberative Process',
        'short_name': 'Deliberative Process / Predecisional Records',
        'category': 'deliberative',
        'description': 'Predecisional deliberative communications — internal drafts, recommendations, and advisory opinions — may be protected from disclosure under a common-law deliberative process privilege. However, Arizona applies this protection more narrowly than most states.',
        'scope': 'Predecisional, deliberative internal communications, including draft documents, policy recommendations, and inter-agency advisory communications. Arizona courts have recognized a limited deliberative process privilege but have applied it narrowly, emphasizing that final agency decisions, factual data, and "working law" (rules agencies actually apply) must be disclosed. The privilege does not protect factual information embedded in deliberative documents.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'draft', 'recommendation', 'advisory',
            'policy development', 'internal memorandum', 'working paper', 'opinion',
        ]),
        'counter_arguments': json.dumps([
            'Arizona courts apply the deliberative process privilege narrowly — factual information must be segregated and released',
            'Final agency decisions and the factual basis for them are not protected',
            '"Working law" — rules and standards agencies apply in practice — must be disclosed even if in internal documents',
            'Documents that have been adopted as final agency policy lose their predecisional character',
            'Challenge attempts to use this privilege to withhold entire documents when only recommendation sections qualify',
            'The strong Arizona disclosure presumption reduces the weight of this privilege compared to other states',
        ]),
        'notes': 'Arizona recognizes a limited deliberative process privilege as a common-law matter, not as a statutory exemption. The Arizona Supreme Court has emphasized the strong public interest in disclosure and has required agencies to demonstrate specific harm from revealing the deliberative content. See Mecham v. Babbitt, 321 Ariz. Adv. Rep. 3 (App.).',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-127',
        'exemption_number': '§ 39-127',
        'short_name': 'Personnel Records — Limited Privacy',
        'category': 'privacy',
        'description': 'State employee personnel records are generally public, but certain specific categories of personal information within those files — such as home addresses, telephone numbers, and medical information — may be withheld under the Carlson balancing test.',
        'scope': 'Arizona public employee personnel records are broadly public under the strong disclosure presumption. However, the Carlson balancing test permits withholding specific personal data points (home address, personal phone number, medical information unrelated to job duties) where the privacy interest is concrete and outweighs the public benefit. Salary, title, disciplinary history, and official conduct are uniformly public.',
        'key_terms': json.dumps([
            'personnel records', 'state employee', 'salary', 'discipline', 'official conduct',
            'home address', 'personal information', 'public employee', 'employment records',
        ]),
        'counter_arguments': json.dumps([
            'Salary, title, job duties, and disciplinary history of public employees are unconditionally public under Arizona law',
            'Only specific personal data points (home address, personal phone) qualify for protection under Carlson',
            'The agency must produce the entire personnel record with only the protected personal data points redacted',
            'Disciplinary records reflecting official misconduct have a strong public interest that overrides the privacy interest',
            'Arizona courts have repeatedly held that government employee conduct in their official capacity is not private',
        ]),
        'notes': 'Arizona has a strong tradition of public access to government personnel records. The Arizona AG has consistently opined that salary and disciplinary records of public employees are public. Only truly personal data (home address, medical) survives the Carlson balancing test. See Scottsdale Unified School Dist. No. 48 v. KPNX Broadcasting Co., 191 Ariz. 297 (1998).',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-124',
        'exemption_number': '§ 39-124',
        'short_name': 'Critical Infrastructure / Security Plans',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and similar records for critical infrastructure and government facilities may be withheld where disclosure would create a specific, articulable security risk.',
        'scope': 'Security plans, vulnerability assessments, access control information, and similar security-sensitive records for critical infrastructure including water systems, power grids, transportation facilities, and government buildings. The agency must demonstrate a specific, articulable risk from disclosure — generalized security concerns are insufficient.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'access control', 'security risk', 'facility security', 'infrastructure protection',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative or generalized',
            'General information about facility operations or locations that is publicly known is not covered',
            'Challenge claims that entire project files are security-sensitive when only specific technical details qualify',
            'Expenditure records for security contracts are public — only the security plan details themselves may be withheld',
        ]),
        'notes': 'Arizona added enhanced critical infrastructure protection in response to post-9/11 concerns. The exemption requires a specific articulated security basis. Arizona courts apply a narrow reading consistent with the state\'s strong disclosure presumption.',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 8-807',
        'exemption_number': '§ 8-807',
        'short_name': 'Child Welfare and Juvenile Records',
        'category': 'privacy',
        'description': 'Records of the Department of Child Safety, juvenile court proceedings, and child welfare investigations are confidential under a specific statutory exemption in the Public Records Law framework.',
        'scope': 'Records of the Department of Child Safety (DCS) relating to investigations of child abuse, neglect, or dependency. Also covers juvenile court records and records of minors in the child welfare system. Specific exceptions allow disclosure to: the subject child or parent, law enforcement, courts, and certain other agencies. Aggregate statistics about the child welfare system are generally public.',
        'key_terms': json.dumps([
            'child welfare', 'DCS', 'Department of Child Safety', 'juvenile records',
            'child abuse', 'neglect investigation', 'dependency', 'minor records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate and anonymized statistics about child welfare outcomes are not covered',
            'Administrative and oversight records about DCS operations are not records of specific investigations',
            'Challenge claims that budget, contract, or staffing records are "child welfare records"',
            'The subject child, parent, or legal guardian can access their own records',
        ]),
        'notes': 'A.R.S. § 8-807 is one of Arizona\'s few express statutory confidentiality provisions that clearly qualifies as a statutory exemption to the Public Records Law. The Arizona legislature has periodically amended it to allow greater public access to aggregate data about the child welfare system.',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 42-2001 et seq.',
        'exemption_number': '§ 42-2001 et seq.',
        'short_name': 'Tax Records — Confidentiality',
        'category': 'statutory',
        'description': 'State tax return information and records of individual taxpayers maintained by the Arizona Department of Revenue are confidential under A.R.S. § 42-2001 and exempt from public records disclosure.',
        'scope': 'Tax returns, applications, and records submitted by individual and business taxpayers to the Arizona Department of Revenue. The confidentiality covers both state income tax and transaction privilege tax (sales tax) records. There are specific exceptions for disclosure to law enforcement, courts, and other tax agencies. Aggregate tax data and statistics are generally public.',
        'key_terms': json.dumps([
            'tax records', 'tax return', 'Department of Revenue', 'taxpayer information',
            'transaction privilege tax', 'income tax', 'confidential tax information',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax statistics, revenue reports, and anonymized data are not covered',
            'Records about the Department of Revenue\'s own operations are not "taxpayer records"',
            'Disclosed information about tax settlements (reported in public court records) may not retain confidentiality',
            'Business license data and publicly registered entity information are generally accessible elsewhere',
        ]),
        'notes': 'One of the clearest and most consistently applied statutory exemptions in Arizona. The confidentiality provision is codified in the tax code, not the Public Records Law, and qualifies as a "confidential by statute" exemption. A.R.S. § 42-2002 specifies the limited categories of permitted disclosure.',
    },
    {
        'jurisdiction': 'AZ',
        'statute_citation': 'A.R.S. § 39-121 (victim privacy)',
        'exemption_number': 'Victim Privacy (common law + statute)',
        'short_name': 'Crime Victim Privacy',
        'category': 'privacy',
        'description': 'Arizona\'s Victims\' Bill of Rights (Arizona Constitution Art. II § 2.1) and A.R.S. § 13-4434 protect crime victims\' privacy, including in public records contexts, particularly for sexual offense victims.',
        'scope': 'Identifying information of crime victims, particularly victims of sexual offenses, domestic violence, and child abuse. Arizona\'s constitutional Victims\' Bill of Rights is one of the strongest in the country and creates privacy rights that apply in the public records context. Law enforcement and prosecution records containing victim information must be produced with victim identifying information redacted.',
        'key_terms': json.dumps([
            'crime victim', 'victim privacy', 'Victims\' Bill of Rights', 'sexual offense victim',
            'domestic violence victim', 'victim identification', 'A.R.S. § 13-4434',
        ]),
        'counter_arguments': json.dumps([
            'Only victim identifying information is protected — the records about the crime and prosecution remain public',
            'Records must be produced with victim identification redacted, not withheld entirely',
            'Challenge claims that entire incident reports are protected because they mention a victim',
            'The constitutional Victims\' Bill of Rights applies primarily to the criminal justice process, not as a blanket public records exemption',
        ]),
        'notes': 'Arizona\'s constitutional Victims\' Bill of Rights is among the most protective in the country. A.R.S. § 13-4434 specifically provides privacy rights for sexual assault victims in court and related proceedings. The Carlson balancing test may also apply to victim information in the public records context, weighing victim safety and privacy against the public interest.',
    },
]

# =============================================================================
# RULES
# Arizona Public Records Law, A.R.S. §§ 39-121 through 39-161
# =============================================================================

AZ_RULES = [
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'response_timeline',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.01(D)(1)',
        'notes': 'Arizona\'s Public Records Law requires agencies to furnish copies of public records "promptly." There is no specific number of days codified in the statute for initial response. Arizona courts have held that "promptly" means within a reasonable time, which courts consider to be a few business days for routine requests. Unreasonable delay can support a special action petition. The AG has interpreted "promptly" to mean as soon as reasonably possible given the scope of the request.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'five_day_practice_standard',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'A.R.S. § 39-121.01(D)(1); Ariz. Att\'y Gen. Op. I74-12',
        'notes': 'While not a statutory deadline, the Arizona AG and courts have generally held that a response within 5 business days is expected for routine requests. Delays beyond this should be accompanied by communication explaining the reason and providing an estimated production date. The absence of a hard deadline is a known gap in Arizona\'s Public Records Law.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'fee_cap',
        'param_key': 'fee_standard',
        'param_value': 'reasonable_not_to_exceed_actual_cost',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.01(D)(1)',
        'notes': 'Arizona agencies may charge a "reasonable fee" for copies of public records, not to exceed the actual cost of reproduction. There is no per-page statutory cap equivalent to Massachusetts ($0.05) or New York ($0.25). The AG has interpreted "actual cost" to include paper, ink, and modest overhead but not the time spent reviewing records for exempt content. "Reasonable" fees are subject to challenge if they appear to be calculated to deter disclosure.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_records_fee',
        'param_value': 'actual_cost_of_production',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.01(D)(1)',
        'notes': 'For electronic records, agencies may charge the actual cost of producing them in electronic format. If records already exist in an accessible electronic format, the actual cost is minimal. Arizona courts have held that agencies cannot charge for the time spent by attorneys or senior officials reviewing records for exempt content — that cost is part of the agency\'s public records duty.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.01',
        'notes': 'Arizona has no statutory fee waiver provision. Agencies may waive fees as a matter of discretion, particularly for journalists, nonprofits, and academic researchers, but there is no legal right to a fee waiver. The "reasonable fee" standard gives agencies some flexibility in fee-setting, and excessive fees can be challenged as an effective denial of access.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.02',
        'notes': 'Arizona has NO formal administrative appeal mechanism for public records denials. There is no agency head appeal, no ombudsman, and no administrative tribunal equivalent to Massachusetts\'s Supervisor of Records or New York\'s agency appeals process. A requester who is denied access must go directly to court via special action in the superior court.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'special_action_superior_court',
        'param_value': 'special_action_available',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.02',
        'notes': 'A person denied access to public records may bring a special action (mandamus-type proceeding) in the superior court. The court reviews the denial de novo and may conduct in camera review of withheld records. Special actions under the Public Records Law are typically expedited. The burden of demonstrating that records are exempt is on the agency.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'discretionary_if_prevails',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121.02(B)',
        'notes': 'The court may award reasonable attorney fees and other legal costs to the requester if the requester substantially prevails and the agency did not have a reasonable basis for withholding. Fee awards are discretionary, not mandatory as in Florida. However, Arizona courts have been willing to award fees where agencies stonewalled or made unjustified withholding claims.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121',
        'notes': 'Arizona agencies may NOT require requesters to identify themselves or state the purpose of their request. The Public Records Law provides a broad right of inspection and copying without requiring justification. Requiring identification as a condition of access is improper. Anonymous and pseudonymous requests are valid.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121',
        'notes': 'Arizona does not require public records requests to be in writing. Oral requests are valid. However, written requests are strongly recommended for documentation. There is no prescribed form or format. Some agencies have created online portals for submitting requests, but use of those portals is optional, not required.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'disclosure_presumption',
        'param_value': 'strong_presumption_of_disclosure',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121; Carlson v. Pima County, 141 Ariz. 487 (1984)',
        'notes': 'Arizona\'s Public Records Law creates one of the strongest presumptions of public access in the country. The Arizona Supreme Court in Carlson v. Pima County emphasized that the law\'s purpose is to open government records to the public, and that any claimed exception must be narrowly construed. The party seeking confidentiality bears the burden of demonstrating that an exception applies.',
    },
    {
        'jurisdiction': 'AZ',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'A.R.S. § 39-121',
        'notes': 'Arizona agencies must release all non-exempt portions of records when only part of a record qualifies for protection. Blanket withholding of documents containing some exempt content is improper. Agencies must redact only the protected portions and produce the rest. This principle applies to all claimed exemptions, including the Carlson privacy balancing test.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

AZ_TEMPLATES = [
    {
        'jurisdiction': 'AZ',
        'record_type': 'general',
        'template_name': 'General Arizona Public Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — A.R.S. § 39-121

Dear Public Records Officer:

Pursuant to the Arizona Public Records Law, A.R.S. § 39-121 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format where available, which minimizes cost and production time.

I am willing to pay reasonable fees up to ${{fee_limit}}. Under A.R.S. § 39-121.01(D)(1), fees must not exceed the actual cost of reproduction. If you anticipate fees exceeding this amount, please notify me before proceeding so I may refine my request.

Arizona law creates a strong presumption in favor of public access. See Carlson v. Pima County, 141 Ariz. 487 (1984). If any records are withheld, please: (1) identify each record withheld; (2) state the specific legal basis for withholding (citing the statute or common-law privilege that applies); (3) explain why the public interest in disclosure does not outweigh the claimed interest in confidentiality; and (4) release all nonexempt, reasonably segregable portions of any partially protected records.

Under Arizona law, the burden of demonstrating that records are exempt rests on the agency, not the requester.

I request a prompt response. If you cannot respond within 5 business days, please contact me with an estimated production date.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that any fees be waived for this request. Although Arizona\'s Public Records Law does not have a statutory fee waiver provision, I ask that the agency exercise its discretion to waive fees because these records relate to a matter of significant public interest: {{public_interest_explanation}}.

I am {{requester_category_description}}. Disclosure of these records will benefit the public by {{public_benefit_explanation}}.

Additionally, if records are provided electronically (via email or digital download), the actual cost of reproduction is minimal or zero, making a fee waiver consistent with both the letter and spirit of A.R.S. § 39-121.01.''',
        'expedited_language': '''I request that this public records request be processed as promptly as possible. Arizona law requires agencies to furnish records "promptly" — A.R.S. § 39-121.01(D)(1). In this case, prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

Please contact me as soon as possible if there are any questions about this request.''',
        'notes': 'General-purpose Arizona public records request template. Key Arizona features: (1) no administrative appeal — go directly to superior court if denied; (2) no per-page fee cap, but fees must not exceed actual cost of reproduction; (3) Carlson balancing test — cite it to preempt privacy claims; (4) burden of proof on agency to justify withholding; (5) anonymous requests are valid. Reference A.R.S. § 39-121, not "FOIA."',
    },
    {
        'jurisdiction': 'AZ',
        'record_type': 'law_enforcement',
        'template_name': 'Arizona Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, A.R.S. § 39-121

Dear Public Records Officer:

Pursuant to the Arizona Public Records Law, A.R.S. § 39-121 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and documentation
- Officer disciplinary records for involved personnel
- Body-worn camera footage and metadata
- Dispatch records and CAD (Computer-Aided Dispatch) logs
- Any written communications relating to the above

Regarding claimed exemptions: Arizona law requires a specific, articulable basis for withholding law enforcement records. See A.R.S. § 39-123. The claimed exemption must identify a specific harm from disclosure (endanger life, identify confidential informant, interfere with pending prosecution, etc.) — not simply that an investigation is or was ongoing.

[If investigation appears concluded:] If any related criminal prosecution has been completed or if no charges were filed, please apply the reduced withholding standard — the interference rationale no longer applies to concluded matters.

Arizona's strong disclosure presumption (Carlson v. Pima County, 141 Ariz. 487 (1984)) requires that the agency demonstrate a specific harm from disclosure, not merely assert a general interest in confidentiality. Please release all nonexempt portions of any partially protected records, with only the specifically exempt content redacted.

I am willing to pay reasonable fees, not to exceed actual reproduction cost per A.R.S. § 39-121.01(D)(1), up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records relate to {{public_interest_explanation}}, a matter of public accountability for government law enforcement actions. The actual cost of electronic production is minimal, and a fee waiver is consistent with Arizona\'s strong public disclosure policy.''',
        'expedited_language': None,
        'notes': 'Arizona law enforcement records template. Arizona has no administrative appeal — if denied, file a special action in superior court under A.R.S. § 39-121.02. The Carlson balancing test applies to claimed privacy interests. The specific harm requirement under § 39-123 is the key limiting principle. Body camera footage is generally public under Arizona law. Cite Carlson and the specific harm requirement to preempt overbroad withholding claims.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in AZ_EXEMPTIONS:
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

    print(f'AZ exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in AZ_RULES:
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

    print(f'AZ rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in AZ_TEMPLATES:
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

    print(f'AZ templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'AZ total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_az', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
