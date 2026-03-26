#!/usr/bin/env python3
"""Build Illinois Freedom of Information Act data: exemptions, rules, and templates.

Covers Illinois's Freedom of Information Act (FOIA), 5 ILCS 140/.
Illinois FOIA was significantly strengthened by 2009 amendments. The law
creates a presumption of openness, places the burden of proving an exemption
on the agency, and provides for binding review by the Public Access Counselor
(PAC) in the Illinois Attorney General's office. Civil penalties of $2,500-
$5,000 per violation are available for willful or intentional non-compliance.
Attorney's fees are available for prevailing requesters.

Run: python3 scripts/build/build_il.py
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
# Illinois Freedom of Information Act, 5 ILCS 140/
# Illinois FOIA Section 7 lists exemptions from the general disclosure
# requirement. The 2009 amendments narrowed many exemptions and added a
# strong presumption of openness in Section 1.2. The PAC has issued thousands
# of binding opinions interpreting these exemptions. Illinois courts and the
# PAC consistently hold that exemptions are strictly construed.
# =============================================================================

IL_EXEMPTIONS = [
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(b)',
        'exemption_number': '5 ILCS 140/7(1)(b)',
        'short_name': 'Personnel Records — Private Employee Information',
        'category': 'privacy',
        'description': 'Private information of public employees — including home addresses, personal phone numbers, personal email addresses, Social Security numbers, and similar personal identifiers — is exempt from FOIA disclosure. However, the name, position, work address, work phone, and salary of public employees are specifically made public by Illinois law.',
        'scope': 'Under 5 ILCS 140/7(1)(b), "private information" means personal data belonging to an individual, including home address, home phone, personal email, SSN, financial account numbers, and disability or medical status. The exemption is field-specific and does not protect the entirety of personnel records. Section 7.5(c) of the Illinois Personnel Record Review Act and 5 ILCS 140/2.20 affirmatively require disclosure of the name, current and past positions, current and past work locations, and compensation of public employees. Illinois courts and the PAC have consistently held that salary, job title, and work contact information are public.',
        'key_terms': json.dumps([
            'private information', 'home address', 'Social Security number',
            'personal email', '5 ILCS 140/7(1)(b)', 'employee privacy',
            'personnel record', 'public employee compensation', 'salary disclosure',
            'work address', 'personal identifier',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, current and prior work addresses, and salary of public employees are affirmatively public under 5 ILCS 140/2.20',
            'The exemption is field-specific — agencies must redact only the specifically protected fields and release the rest',
            'Records of official conduct and work activities are not "private information" under the FOIA',
            'Challenge overbroad withholding where public employee information (salary, title, work address) is redacted along with genuinely private data',
            'Formal disciplinary actions and their outcomes are public accountability records, not private personnel information',
            'The PAC has consistently held that Illinois requires a liberal interpretation of public employee information disclosure',
        ]),
        'notes': 'Illinois affirmatively requires disclosure of public employee name, position, and compensation under 5 ILCS 140/2.20. The PAC has issued numerous binding opinions holding that agencies may not use the § 7(1)(b) exemption to shield this publicly required information. Key PAC opinions include 11-006 and 12-015.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(c)',
        'exemption_number': '5 ILCS 140/7(1)(c)',
        'short_name': 'Personal Privacy — Unwarranted Invasion',
        'category': 'privacy',
        'description': 'Personal information compiled in the course of government operations whose disclosure would constitute a clearly unwarranted invasion of personal privacy is exempt. The exemption requires a balancing test — the privacy interest must outweigh the public interest in disclosure.',
        'scope': 'Information about individuals whose disclosure constitutes a "clearly unwarranted invasion of personal privacy." Under 5 ILCS 140/7(1)(c), courts apply a balancing test weighing the public interest in disclosure against the individual\'s privacy interest. The standard is "clearly unwarranted" — a high threshold. Information about public officials in their official capacity, government actions and decisions, and public employees\' exercise of their duties is unlikely to satisfy this threshold. Personal information unrelated to government functions is more likely to be protected. The PAC has held that the agency bears the burden of demonstrating the clear invasion of privacy.',
        'key_terms': json.dumps([
            'clearly unwarranted invasion of personal privacy', 'personal privacy',
            '5 ILCS 140/7(1)(c)', 'privacy balancing test', 'personal information',
            'individual privacy', 'privacy interest', 'public interest balancing',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" — a high bar that cannot be satisfied by mere discomfort with disclosure',
            'Information about public officials in their official capacity rarely meets this standard',
            'The public interest in government accountability must be weighed against the privacy interest',
            'The agency bears the burden of demonstrating that the privacy interest clearly outweighs the public interest',
            'Information voluntarily placed in public documents (filings, testimony, statements) has reduced privacy protection',
            'Challenge claims where the agency has not articulated a specific, concrete privacy harm from disclosure',
        ]),
        'notes': 'Illinois\'s personal privacy exemption under § 7(1)(c) requires a genuine balancing test, not a simple privacy claim. The PAC has held that general "privacy concerns" without specific harm are insufficient. Illinois courts apply the exemption narrowly consistent with the Act\'s presumption of openness under 5 ILCS 140/1.2.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(d)',
        'exemption_number': '5 ILCS 140/7(1)(d)',
        'short_name': 'Law Enforcement — Ongoing Investigation and Intelligence',
        'category': 'law_enforcement',
        'description': 'Records that, if disclosed, would obstruct ongoing criminal investigations or prosecutions, endanger the life or safety of a person, reveal confidential sources or techniques, or constitute interference with law enforcement proceedings are exempt from Illinois FOIA.',
        'scope': 'Under 5 ILCS 140/7(1)(d), law enforcement records may be withheld where disclosure would: (1) interfere with pending criminal proceedings; (2) deprive a person of a fair trial; (3) create substantial danger to any person; (4) disclose the identity of a confidential informant; (5) reveal specific investigative techniques; or (6) endanger law enforcement personnel. The exemption requires a specific, articulable harm for each withheld record. Closed investigations, concluded prosecutions, and arrest records are generally public. The burden is on the agency to demonstrate which specific harm applies to each record.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            '5 ILCS 140/7(1)(d)', 'ongoing investigation', 'investigative technique',
            'pending prosecution', 'law enforcement exemption', 'safety endangerment',
            'interference with law enforcement',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a specific articulable harm — the agency cannot assert a blanket law enforcement category exemption',
            'Completed investigations and concluded prosecutions do not retain this protection',
            'Arrest records, incident reports, booking information, and dispatch logs are public',
            'Challenge claims that standard police procedures are "specific investigative techniques"',
            'The burden is on the agency to demonstrate specific harm for each withheld record',
            'The PAC has consistently rejected blanket withholding of law enforcement records without record-specific justification',
            'Illinois\'s 2009 FOIA amendments strengthened the public\'s right to law enforcement records',
        ]),
        'notes': 'The PAC has extensively developed Illinois law enforcement FOIA exemptions. Illinois courts consistently hold that the exemption is strictly construed. The 2009 amendments added specific requirements that agencies demonstrate concrete harm rather than merely asserting an exemption category. See Gekas v. Williamson, 393 Ill. App. 3d 573 (2009).',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(f)',
        'exemption_number': '5 ILCS 140/7(1)(f)',
        'short_name': 'Preliminary Drafts and Deliberative Process',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, recommendations, memoranda, and other records in which opinions are expressed or policies or actions are formulated, except that a specific record is not exempt if put in issue in any action in court or administrative proceeding.',
        'scope': 'Internal predecisional deliberative materials: preliminary drafts, working papers, notes, and intra-agency memoranda where the author expresses opinions or makes recommendations. The exemption does not cover purely factual material, even if embedded in a deliberative document. Factual data underlying recommendations must be segregated and released. Final agency decisions, adopted policies, and records used in legal proceedings are not covered. Illinois courts and the PAC apply the exemption narrowly — the factual/opinion distinction is critical. The exemption is specifically negated if the record is put in issue in any court or administrative proceeding.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'intra-agency memo',
            '5 ILCS 140/7(1)(f)', 'predecisional', 'working paper',
            'recommendation', 'policy deliberation', 'draft document',
            'opinion in record', 'formulating policy',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released',
            'Once a draft or recommendation is adopted as the agency\'s final position, the exemption no longer applies',
            'If the record has been put in issue in any court or administrative proceeding, the exemption is negated',
            'Final agency decisions and adopted policies are fully public regardless of their deliberative origins',
            '"Working law" — standards the agency actually applies — must be disclosed',
            'Challenge claims that entire documents are deliberative when only specific recommendation portions qualify',
            'Documents circulated outside the agency may lose their predecisional character',
        ]),
        'notes': 'Illinois\'s deliberative process exemption under § 7(1)(f) has an important carveout: if the record is put in issue in any court or administrative proceeding, the exemption does not apply. This narrows the exemption further than most states. The PAC applies the factual/opinion distinction rigorously.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(g)',
        'exemption_number': '5 ILCS 140/7(1)(g)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information that is proprietary or privileged, or that consists of competitive bid documents where disclosure would have an adverse effect on competitive bidding, is exempt from Illinois FOIA.',
        'scope': 'Trade secrets as defined under the Illinois Trade Secrets Act (765 ILCS 1065/) and proprietary commercial information submitted by private entities to government agencies. Government-generated records cannot be trade secrets. The agency must independently evaluate vendor designations — it cannot simply defer to contractor claims. Contract prices, amounts paid with public funds, and government expenditures are public even when vendors claim trade secret protection. Competitive bid documents are protected only before bid opening — post-award, all bid documents are public.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', '5 ILCS 140/7(1)(g)',
            'Illinois Trade Secrets Act', '765 ILCS 1065', 'competitive bid',
            'commercial information', 'financial information', 'competitive harm',
            'vendor records', 'contractor information',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds are always public regardless of trade secret claims',
            'Post-award bid documents are public — the competitive bid exemption applies only before bid opening',
            'The agency must independently evaluate trade secret claims under the ITSA, not defer to vendor designations',
            'Government-generated records are not trade secrets',
            'Information required by law to be submitted has reduced secrecy expectations',
            'The PAC has consistently held that agencies must provide independent analysis supporting trade secret withholding',
        ]),
        'notes': 'Illinois\'s trade secret exemption applies the Illinois Trade Secrets Act framework. The PAC has required agencies to provide detailed analysis of each claimed trade secret, including explanation of the competitive harm from disclosure. Contract amounts and public expenditures are uniformly held to be public by the PAC and Illinois courts.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(e)',
        'exemption_number': '5 ILCS 140/7(1)(e)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that are covered by attorney-client privilege or constitute attorney work product are exempt from Illinois FOIA. The privilege protects confidential communications between government lawyers and their client agencies for the purpose of obtaining or providing legal advice.',
        'scope': 'Confidential communications between government agencies and their legal counsel made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. The privilege is narrow — it covers legal advice, not business or policy recommendations. Billing records and financial arrangements with outside counsel are generally public. Facts independently known by the agency are not privileged merely because communicated to counsel. Waiver occurs through voluntary disclosure. The PAC requires agencies to provide a privilege log with record-specific justification.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            '5 ILCS 140/7(1)(e)', 'privileged communication', 'attorney work product',
            'in anticipation of litigation', 'legal opinion', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'Policy and business advice from attorneys is not privileged — only legal advice qualifies',
            'Waiver occurs through public disclosure of the advice or action based on it',
            'Billing records are generally public — they describe services, not legal advice',
            'Facts underlying legal advice are not privileged',
            'The PAC requires record-specific privilege logs — general assertions are insufficient',
            'The privilege is narrow given Illinois FOIA\'s strong presumption of openness',
        ]),
        'notes': 'Illinois FOIA § 7(1)(e) incorporates common-law attorney-client privilege and work product doctrine for government agencies. The PAC consistently requires agencies to provide detailed privilege logs and has frequently found agencies have over-withheld by claiming privilege for non-privileged communications.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(a)',
        'exemption_number': '5 ILCS 140/7(1)(a)',
        'short_name': 'Federal Law or State Statute Prohibitions',
        'category': 'statutory',
        'description': 'Records that are specifically prohibited from disclosure by federal or state statute, or protected from disclosure by rules adopted under authority of a statute, are exempt from Illinois FOIA.',
        'scope': 'Records whose disclosure is specifically prohibited by an identified federal statute (e.g., tax return information under 26 U.S.C. § 6103, education records under FERPA) or Illinois statute. The exemption requires a specific prohibition in an identified statute — a general grant of agency authority is insufficient. The agency must cite the specific federal or state statute prohibiting disclosure. Courts have required that the prohibiting statute specifically address disclosure, not merely provide that certain information is "confidential" in an administrative context.',
        'key_terms': json.dumps([
            'federal statute', 'state statute', 'prohibited by law',
            '5 ILCS 140/7(1)(a)', 'FERPA', 'tax return information',
            'statutory prohibition', 'federal preemption', 'legal prohibition',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify a specific federal or state statute that prohibits disclosure — a general administrative confidentiality designation is insufficient',
            'A statute granting agencies discretion to maintain confidentiality is not the same as a specific prohibition',
            'Challenge whether the cited statute actually prohibits disclosure or merely permits confidential treatment',
            'Many federal "confidentiality" provisions do not actually prohibit state FOIA disclosure',
            'Request that the agency identify the specific statutory section, not just the name of a statute',
        ]),
        'notes': 'The § 7(1)(a) exemption requires a specific, identifiable statutory prohibition. The PAC has consistently held that agencies citing this exemption must identify the specific statute and explain how it prohibits disclosure of each withheld record. General claims of "federal confidentiality" without specific citations are insufficient.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(x)',
        'exemption_number': '5 ILCS 140/7(1)(x)',
        'short_name': 'Security Plans and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Security plans and security codes or programs for any building, facility, or the operation of any unit of local government are exempt from Illinois FOIA to prevent disclosure that would create a security risk.',
        'scope': 'Operational security plans, security codes, and security programs for government buildings, facilities, and utility systems. The exemption is targeted at information that would enable someone to circumvent security — specific access codes, technical specifications of security systems, and vulnerability assessments. Budget records, contracts, general policy descriptions, and general information about security programs are public. The agency must demonstrate a specific security risk from disclosure, not merely assert that records are "security-related."',
        'key_terms': json.dumps([
            'security plan', 'security code', 'security program',
            '5 ILCS 140/7(1)(x)', 'facility security', 'vulnerability',
            'building security', 'access code', 'security system',
        ]),
        'counter_arguments': json.dumps([
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not reveal specific vulnerabilities are public',
            'Challenge claims that entire security contracts are exempt when only technical specifications warrant protection',
            'Widely known security measures do not qualify for this exemption',
            'The agency must demonstrate a specific security risk from disclosure of each record',
        ]),
        'notes': 'Illinois\'s security plans exemption under § 7(1)(x) is narrowly applied. The PAC requires agencies to demonstrate specific security risk, not assert a blanket exemption. General security policy documents and budget records for security programs are consistently held to be public.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(n)',
        'exemption_number': '5 ILCS 140/7(1)(n)',
        'short_name': 'Personal Identifying Information — Multiple Databases',
        'category': 'privacy',
        'description': 'Records containing personal identifying information maintained in multiple public databases that, if combined, would constitute a clearly unwarranted invasion of personal privacy, are exempt under Illinois FOIA\'s "mosaic" privacy protection.',
        'scope': 'Information that is individually innocuous but whose combination across multiple government databases would create an aggregated profile constituting a clearly unwarranted privacy invasion. This exemption reflects concerns about aggregated data enabling stalking, harassment, or identity theft. It applies primarily to bulk data requests that would compile comprehensive personal profiles of private individuals. Records about public officials in their official capacity and public expenditures are not protected. The PAC applies this exemption narrowly — it requires genuine mosaic/aggregation harm, not mere assertion that information is personal.',
        'key_terms': json.dumps([
            'personal information aggregation', 'mosaic effect', 'database combination',
            '5 ILCS 140/7(1)(n)', 'privacy invasion', 'data compilation',
            'aggregated personal data', 'identity theft risk', 'stalking risk',
        ]),
        'counter_arguments': json.dumps([
            'The harm must come from combination of multiple databases — individual records are analyzed under standard privacy exemptions',
            'Information about public officials in their official capacity is not covered',
            'Government expenditures and public financial records are not protected',
            'Challenge whether a request actually seeks to aggregate data or merely requests a specific set of records',
            'The PAC requires a genuine showing of aggregation harm, not mere assertion that some information is personal',
        ]),
        'notes': 'Illinois\'s § 7(1)(n) aggregation/mosaic exemption reflects modern concerns about data compilation. The PAC applies it narrowly and has rejected agencies that use it as a general privacy shield. Genuine aggregation harm — where combination of databases creates comprehensive personal profiles — is the required showing.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(v)',
        'exemption_number': '5 ILCS 140/7(1)(v)',
        'short_name': 'Juvenile Court and Child Welfare Records',
        'category': 'privacy',
        'description': 'Juvenile court records, DCFS (Department of Children and Family Services) records, and related child welfare records are exempt from Illinois FOIA to protect minors involved in the child welfare and juvenile justice systems.',
        'scope': 'Records of juvenile court proceedings, DCFS investigations and case files, and related child welfare records identifying specific minors or their families. Illinois\'s Juvenile Court Act (705 ILCS 405/) and DCFS records confidentiality statutes (325 ILCS 5/) provide comprehensive protections. Adult criminal records and adult court proceedings are fully public. Aggregate statistics about juvenile justice and child welfare system outcomes and program performance are public.',
        'key_terms': json.dumps([
            'juvenile court record', 'DCFS record', 'child welfare record',
            '5 ILCS 140/7(1)(v)', '705 ILCS 405', '325 ILCS 5',
            'minor record', 'child abuse investigation', 'delinquency record',
        ]),
        'counter_arguments': json.dumps([
            'Adult records are fully public even if an adult was a juvenile at the time of earlier proceedings',
            'Aggregate statistics about system outcomes and program performance are public',
            'Policy and budget records for DCFS and juvenile courts are public',
            'Challenge claims that records about adults involved in these matters are protected as juvenile or child welfare records',
        ]),
        'notes': 'Illinois\'s juvenile and child welfare records exemption is reinforced by the Juvenile Court Act and DCFS confidentiality statutes. The PAC has held that aggregate system data and policy documents are not protected — only individually identifiable records about specific minors.',
    },
    {
        'jurisdiction': 'IL',
        'statute_citation': '5 ILCS 140/7(1)(m)',
        'exemption_number': '5 ILCS 140/7(1)(m)',
        'short_name': 'Library Patron Records',
        'category': 'privacy',
        'description': 'Library patron records — including circulation records, borrower information, and records of materials accessed by library patrons — are exempt from Illinois FOIA to protect intellectual freedom and the confidentiality of library use.',
        'scope': 'Individually identifiable records of library patrons\' borrowing, circulation, and material access activities maintained by public libraries subject to the Illinois Library Records Confidentiality Act (75 ILCS 70/). The protection is absolute for patron-specific data — there is no balancing test. Aggregate circulation statistics, library acquisition records, and general library program records are public. The exemption reflects Illinois\'s strong public policy that individuals should be able to access information and ideas without fear of government surveillance.',
        'key_terms': json.dumps([
            'library patron record', 'circulation record', 'library confidentiality',
            '5 ILCS 140/7(1)(m)', '75 ILCS 70', 'borrower record',
            'library privacy', 'intellectual freedom', 'library records',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate circulation statistics and general program data are public',
            'Library acquisition, budget, and operational records are public',
            'Challenge claims that non-patron-specific library records are protected',
            'Policy records about library services and programs are public',
        ]),
        'notes': 'Illinois\'s library patron confidentiality under § 7(1)(m) and 75 ILCS 70/ is among the strongest in the country. The protection is absolute for individually identifiable patron records — courts do not apply a balancing test. The policy reflects Illinois\'s commitment to intellectual freedom and preventing government surveillance of reading and information access.',
    },
]

# =============================================================================
# RULES
# Illinois Freedom of Information Act, 5 ILCS 140/
# Key features: 5-business-day response; 5-business-day extension; Public
# Access Counselor (PAC) in the AG's office provides binding review; civil
# penalties $2,500-$5,000 for willful/intentional violations; attorney's
# fees for prevailing requesters; strong presumption of openness under
# 5 ILCS 140/1.2.
# =============================================================================

IL_RULES = [
    {
        'jurisdiction': 'IL',
        'rule_type': 'initial_response',
        'param_key': 'initial_response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '5 ILCS 140/3(d)',
        'notes': 'Under 5 ILCS 140/3(d), a public body must respond to a FOIA request within 5 business days of receipt. The response must either: (1) provide the records; (2) deny the request stating specific grounds; or (3) invoke the 5-business-day extension under § 3(e). The 5-business-day clock starts on the business day after receipt. If the public body fails to respond within 5 business days (or within the extended period), the request is deemed denied by operation of law. Illinois\'s 5-day response deadline is one of the shorter deadlines among large states.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'extension',
        'param_key': 'maximum_extension_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '5 ILCS 140/3(e)',
        'notes': 'Under 5 ILCS 140/3(e), a public body may extend the response deadline by up to 5 additional business days if: (1) the requested records are stored at a location other than the office receiving the request; (2) the request requires the collection of a substantial number of records; (3) the request requires an extensive search; (4) the requested records have not been located and require additional effort to find; (5) the records need to be reviewed by agency counsel; or (6) the request involves records from multiple units of the agency. The extension notice must specify the reason for the extension and a date by which the agency will respond.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'initial_response',
        'param_key': 'deemed_denial_trigger',
        'param_value': 'failure_to_respond_in_5_business_days',
        'day_type': None,
        'statute_citation': '5 ILCS 140/3(d)',
        'notes': 'If a public body fails to respond to a FOIA request within 5 business days (or within the extended period), the request is deemed denied by operation of law. A deemed denial triggers the requester\'s right to seek review from the PAC within 60 calendar days. Requesters should track the 5-business-day deadline carefully and file a PAC complaint promptly after a deemed denial.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_per_page',
        'param_value': '0.15',
        'day_type': None,
        'statute_citation': '5 ILCS 140/6',
        'notes': 'Under 5 ILCS 140/6, public bodies may charge the actual cost of reproducing records. The standard rate for black-and-white paper copies is $0.15 per page. Agencies may not charge for: searching for or retrieving records; reviewing records for exemptions; attorney review time; or overhead. For electronic records, the charge is the actual cost of the storage medium — often zero for email delivery. Color copies may be charged at a higher rate reflecting actual cost. Fees may not function as barriers to access.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_for_news_media',
        'param_value': 'mandatory',
        'day_type': None,
        'statute_citation': '5 ILCS 140/6(c)',
        'notes': 'Under 5 ILCS 140/6(c), a public body must waive or reduce fees for requests by news media where the requester states that the fee waiver is in the public interest. Additionally, agencies must waive fees for requests by non-profit organizations when the principal purpose is not for commercial use. Illinois\'s mandatory fee waiver for news media and nonprofits is more protective than most states\' discretionary waiver provisions.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'fee_waiver',
        'param_key': 'first_50_pages_free',
        'param_value': 'first_50_pages_no_charge',
        'day_type': None,
        'statute_citation': '5 ILCS 140/6(b)',
        'notes': 'Under 5 ILCS 140/6(b), a public body may not charge a requester for the first 50 pages of paper copies requested. The first 50 pages must be provided free of charge. Only pages beyond the first 50 may be charged at the applicable per-page rate. This provision effectively creates a free initial production for many FOIA requests.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'appeal_deadline',
        'param_key': 'pac_review_deadline_days',
        'param_value': '60',
        'day_type': 'calendar',
        'statute_citation': '5 ILCS 140/9.5',
        'notes': 'Under 5 ILCS 140/9.5, a requester may submit a request for review to the Public Access Counselor (PAC) in the Illinois Attorney General\'s office within 60 calendar days of a denial or deemed denial. The PAC review is the primary administrative remedy for Illinois FOIA denials. The PAC may issue a binding opinion requiring the public body to produce records. PAC review is free, informal, and often faster than court proceedings. The PAC has issued thousands of binding opinions that constitute a comprehensive body of Illinois FOIA interpretive authority.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'appeal_deadline',
        'param_key': 'pac_determination_deadline_days',
        'param_value': '60',
        'day_type': 'calendar',
        'statute_citation': '5 ILCS 140/9.5(f)',
        'notes': 'The PAC must issue a binding opinion within 60 calendar days of receiving a request for review, unless the PAC grants an extension. PAC opinions are binding on the public body unless the body files a lawsuit to contest the opinion within 35 days. If a public body ignores a binding PAC opinion, the requester may bring a civil enforcement action in circuit court. PAC opinions are published on the AG\'s website and constitute persuasive authority for similar disputes.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_action',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': '5 ILCS 140/11',
        'notes': 'A requester may file a lawsuit in circuit court under 5 ILCS 140/11 to compel disclosure of records. The court reviews the denial de novo and may conduct in camera inspection of withheld records. Requesters may pursue PAC review and circuit court action concurrently or sequentially. Failure to pursue PAC review does not bar a circuit court action. The circuit court action is available for both Commonwealth and local agencies.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_willful_violation',
        'param_value': '$2,500-$5,000',
        'day_type': None,
        'statute_citation': '5 ILCS 140/11(j)',
        'notes': 'Under 5 ILCS 140/11(j), a court may impose civil penalties of $2,500 to $5,000 per violation against a public body that wilfully or intentionally fails to comply with Illinois FOIA. This penalty provision was added by the 2009 amendments to deter bad-faith denials and provide meaningful enforcement. Penalties apply to willful or intentional violations — reckless or negligent non-compliance typically does not trigger the penalty. The penalty amount is per violation, not per day, distinguishing it from Ohio\'s per diem approach.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': '5 ILCS 140/11(i)',
        'notes': 'Under 5 ILCS 140/11(i), if a requester substantially prevails in a circuit court action, the court SHALL award reasonable attorney fees and costs against the public body. The mandatory fee-shifting provision was added by the 2009 amendments to provide meaningful enforcement incentives. The fee award is mandatory (not discretionary) for prevailing requesters — this is one of the strongest attorney fee provisions among state FOIA laws. The availability of mandatory fees makes it economically viable to litigate Illinois FOIA violations.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': '5 ILCS 140/1.2; 5 ILCS 140/11(f)',
        'notes': 'Under 5 ILCS 140/1.2, all records in the custody or possession of a public body are presumed to be open to inspection and copying. The public body bears the burden of establishing that records are exempt from disclosure by clear and convincing evidence. Under § 11(f), in any court proceeding, the burden of proof is on the public body. This is a higher burden than most states\' preponderance standard — "clear and convincing evidence" is a demanding threshold for agencies claiming exemptions.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'initial_response',
        'param_key': 'denial_must_cite_specific_exemption',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': '5 ILCS 140/9(a)',
        'notes': 'Under 5 ILCS 140/9(a), a denial must specify the reasons for denial, including the specific exemption provisions claimed under § 7. A denial that cites only a general category without identifying specific § 7 subsections is legally deficient. The denial must also state the name and title of the person responsible for the denial. Procedurally deficient denials may be treated as wrongful by the PAC and courts. Requesters should challenge denials that fail to identify specific statutory provisions.',
    },
    {
        'jurisdiction': 'IL',
        'rule_type': 'initial_response',
        'param_key': 'foia_officer_required',
        'param_value': 'required_with_training',
        'day_type': None,
        'statute_citation': '5 ILCS 140/3.5',
        'notes': 'Under 5 ILCS 140/3.5 (added by 2009 amendments), each public body must designate a trained FOIA Officer to receive and process FOIA requests. FOIA Officers must complete annual training provided by the Illinois Attorney General\'s office. The requirement ensures that agencies have qualified personnel processing requests. Requesters should address FOIA requests specifically to the designated FOIA Officer. A list of FOIA Officers may be available on agency websites.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

IL_TEMPLATES = [
    {
        'jurisdiction': 'IL',
        'record_type': 'general',
        'template_name': 'General Illinois Freedom of Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — 5 ILCS 140/

Dear FOIA Officer:

Pursuant to the Illinois Freedom of Information Act, 5 ILCS 140/ et seq., I hereby request access to and copies of the following records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes cost for both parties.

Under 5 ILCS 140/6(b), the first 50 pages of paper copies must be provided at no charge. I am willing to pay the actual cost of reproducing records per 5 ILCS 140/6 ($0.15 per page beyond the first 50) for paper copies. I am not willing to pay charges for staff time spent searching for, reviewing, or redacting records, which is not a permissible fee under Illinois FOIA. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under 5 ILCS 140/1.2, all records in your custody are presumed open to inspection and copying. The burden of establishing that any record is exempt from disclosure rests on the public body — by clear and convincing evidence. Under 5 ILCS 140/7(2), the agency must release all nonexempt portions of records where only part qualifies for an exemption.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) cite the specific exemption provision under 5 ILCS 140/7 (specific subsection required per 5 ILCS 140/9(a)); (3) explain how the specific exemption applies to each record; and (4) confirm that all nonexempt, segregable portions of partially withheld records have been released.

Under 5 ILCS 140/3(d), please respond within 5 business days. If an extension is required under 5 ILCS 140/3(e), please notify me within the initial 5-business-day period with the specific statutory ground for the extension.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. Under 5 ILCS 140/6(c):

[If news media:] As a member of the news media, I request a fee waiver. These records relate to {{public_interest_explanation}}, a matter of public interest. Disclosure will benefit the public by {{public_benefit_explanation}}.

[If nonprofit:] As a nonprofit organization, the principal purpose of this request is not commercial use. These records serve the public interest by {{public_benefit_explanation}}.

[General:] I request a fee waiver because: (1) these records relate to {{public_interest_explanation}}, a matter of significant public interest; (2) I am {{requester_category_description}}; and (3) disclosure will benefit the public by {{public_benefit_explanation}}. If records are delivered electronically, the actual reproduction cost is zero.''',
        'expedited_language': '''I request expedited processing of this FOIA request. Prompt production is needed because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately at {{requester_email}} or {{requester_phone}} if any clarification would allow faster production.''',
        'notes': 'General Illinois FOIA template. Key features: (1) 5-business-day response, 5-business-day extension — cite § 3(d) and § 3(e); (2) first 50 pages free under § 6(b); (3) mandatory fee waiver for news media and nonprofits under § 6(c); (4) PAC review available within 60 days of denial; (5) mandatory attorney fees for prevailing requesters under § 11(i); (6) civil penalties $2,500-$5,000 for willful violations under § 11(j); (7) FOIA Officer required under § 3.5; (8) burden of proof on agency by clear and convincing evidence under § 1.2. Reference 5 ILCS 140/, not "FOIA."',
    },
    {
        'jurisdiction': 'IL',
        'record_type': 'law_enforcement',
        'template_name': 'Illinois FOIA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Law Enforcement Records, 5 ILCS 140/

Dear FOIA Officer:

Pursuant to the Illinois Freedom of Information Act, 5 ILCS 140/ et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Written communications relating to the above

Regarding the criminal investigation exemption under 5 ILCS 140/7(1)(d): Illinois law does not permit blanket withholding of law enforcement records. Any withholding requires specific identification of: (1) which enumerated harm applies — interference with pending proceedings, fair trial prejudice, safety endangerment, confidential informant identity, specific investigative technique, or officer safety; and (2) how disclosure of each specific record would cause that harm.

[If matter appears concluded:] If no criminal prosecution is currently pending, the interference-with-proceedings rationale under § 7(1)(d) does not apply to this matter.

Under 5 ILCS 140/1.2, the burden of establishing that any record is exempt rests on the public body by clear and convincing evidence. Under 5 ILCS 140/7(2), all nonexempt, segregable portions of partially withheld records must be released.

Under 5 ILCS 140/6(b), the first 50 pages are provided at no charge.

Please respond within 5 business days per 5 ILCS 140/3(d).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records concern {{public_interest_explanation}}. Under 5 ILCS 140/6(b), the first 50 pages are already free. Electronic delivery incurs zero reproduction cost. A fee waiver for any additional pages is in the public interest.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Illinois law enforcement records template. Key features: (1) § 7(1)(d) requires specific harm identification per record — no blanket law enforcement exemptions; (2) completed investigations are generally public; (3) first 50 pages free under § 6(b); (4) PAC review available within 60 days of denial — fast, free, and often effective; (5) mandatory attorney fees under § 11(i); (6) civil penalties for willful violations under § 11(j); (7) burden of proof on agency by clear and convincing evidence.',
    },
    {
        'jurisdiction': 'IL',
        'record_type': 'financial',
        'template_name': 'Illinois FOIA Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

FOIA Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — Contracts and Expenditure Records, 5 ILCS 140/

Dear FOIA Officer:

Pursuant to the Illinois Freedom of Information Act, 5 ILCS 140/ et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Contractor/vendor (if applicable): {{contractor_name}}
Contract period: {{date_range_start}} through {{date_range_end}}
Contract number (if known): {{contract_number}}

This request includes, but is not limited to:
- Executed contracts and all amendments/modifications
- Bid and proposal documents, including all submitted bids/proposals
- Invoices, payment records, and vouchers
- Performance evaluations and compliance records

Regarding trade secret claims under 5 ILCS 140/7(1)(g): Contract prices, amounts paid with public funds, and total government expenditures are public regardless of vendor trade secret designations. The agency must independently evaluate trade secret claims under the Illinois Trade Secrets Act (765 ILCS 1065/) — it cannot defer to contractor designations. Per PAC precedent, vendors cannot unilaterally shield public expenditure records from disclosure.

Under 5 ILCS 140/1.2, the burden of establishing that any record is exempt rests on the public body by clear and convincing evidence. Under 5 ILCS 140/7(2), all nonexempt, segregable portions of partially withheld records must be released.

Under 5 ILCS 140/6(b), the first 50 pages are provided at no charge. Please respond within 5 business days per 5 ILCS 140/3(d).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. These records concern the expenditure of public funds — a core purpose of the Illinois FOIA. The first 50 pages are free under § 6(b). Electronic delivery incurs zero additional cost. A fee waiver would further the FOIA\'s transparency mandate.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Illinois government contracts template. Key points: (1) contract prices and public expenditures are always public; (2) first 50 pages free; (3) PAC has extensive precedent requiring independent agency analysis of trade secret claims; (4) agencies cannot defer to vendor designations; (5) PAC review available within 60 days — binding and free; (6) mandatory attorney fees under § 11(i) for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in IL_EXEMPTIONS:
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

    print(f'IL exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in IL_RULES:
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

    print(f'IL rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in IL_TEMPLATES:
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

    print(f'IL templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'IL total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_il', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
