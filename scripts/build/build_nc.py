#!/usr/bin/env python3
"""Build North Carolina Public Records Law data: exemptions, rules, and templates.

Covers North Carolina's Public Records Law, N.C.G.S. § 132-1 et seq.
North Carolina's law is notable for its broad definition of "public record"
and its explicit statement that all public records must be made available for
inspection and examination. The statute lacks a specific deadline — agencies
must respond "as promptly as possible." There is no administrative appeal
mechanism; superior court is the enforcement venue. Attorney's fees are
available for prevailing requesters. The law is generally interpreted broadly
in favor of access.

Run: python3 scripts/build/build_nc.py
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
# North Carolina Public Records Law, N.C.G.S. § 132-1 et seq.
# North Carolina defines "public record" broadly in § 132-1 as all documents,
# papers, letters, maps, books, photographs, films, sound recordings,
# magnetic or other tapes, electronic data processing records, artifacts,
# or other documentary material, regardless of physical form or characteristics,
# made or received pursuant to law or ordinance or in connection with the
# transaction of public business by any agency. Exemptions are listed in
# § 132-1.1 through § 132-6A and in scattered statutes. The burden is on the
# agency to demonstrate applicability of an exemption.
# =============================================================================

NC_EXEMPTIONS = [
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.4',
        'exemption_number': 'N.C.G.S. § 132-1.4',
        'short_name': 'Criminal Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of criminal investigations compiled by law enforcement agencies, including but not limited to records relating to persons charged or sought for criminal offenses, information regarding criminal intelligence, and records of criminal informants, are exempt from North Carolina\'s Public Records Law.',
        'scope': 'Under N.C.G.S. § 132-1.4, records of criminal investigations include: reports of investigation, criminal intelligence information, and information about criminal informants. The exemption applies to ongoing and pending investigations. However, § 132-1.4(c) specifically requires disclosure of: the time, date, location, and nature of the crime; the identity of the victim; the agency and its officers involved; any arrests made; and the charges filed. These must be produced regardless of investigation status. Completed investigations and concluded prosecutions generally lose the broader exemption protection.',
        'key_terms': json.dumps([
            'criminal investigation record', 'law enforcement investigation',
            'N.C.G.S. 132-1.4', 'criminal intelligence', 'criminal informant',
            'ongoing investigation', 'pending investigation', 'arrest record',
            'law enforcement exemption', 'incident record',
        ]),
        'counter_arguments': json.dumps([
            'N.C.G.S. § 132-1.4(c) requires disclosure of specific information regardless of investigation status: time/date/location/nature of crime, victim identity, agency and officers, arrests, and charges',
            'Completed investigations and concluded prosecutions do not retain the full investigation records exemption',
            'Arrest records, booking information, and incident reports are public under § 132-1.4(c)',
            'Challenge claims that the exemption covers non-criminal administrative investigations',
            'The agency must demonstrate that the investigation is genuinely ongoing, not merely label it as such',
            'Factual information that does not reveal criminal intelligence or informant identities may be required to be released',
            'NC courts broadly construe the public disclosure obligation and strictly limit exemptions',
        ]),
        'notes': 'N.C.G.S. § 132-1.4 is one of North Carolina\'s most important law enforcement records provisions. The mandatory disclosure provisions in § 132-1.4(c) are often overlooked by agencies — requesters should specifically cite these subsections when seeking basic incident information. See News & Observer Publishing Co. v. Poole, 330 N.C. 465 (1992) for the foundational NC law enforcement records analysis.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.1(a)',
        'exemption_number': 'N.C.G.S. § 132-1.1(a)',
        'short_name': 'Confidential Personnel Records',
        'category': 'privacy',
        'description': 'Personnel records of current and former state and local government employees, applicants for state and local government employment, and current and former members of the General Assembly are confidential and are not considered public records under North Carolina law.',
        'scope': 'Under N.C.G.S. § 132-1.1 and N.C.G.S. § 126-22 through § 126-25, the following employee information is exempt: home addresses, home telephone numbers, personal email, SSNs, medical information, academic transcripts in some contexts, and the content of personnel files. However, § 132-1.1(a) and § 126-23 affirmatively require disclosure of: employee name, current position, salary, date of first employment, and current duties. North Carolina has a detailed statutory framework balancing employee privacy against public accountability. Formal disciplinary actions (written reprimands, suspensions, dismissals) and their outcomes are public.',
        'key_terms': json.dumps([
            'personnel record', 'employee privacy', 'N.C.G.S. 132-1.1',
            'N.C.G.S. 126-22', 'N.C.G.S. 126-23', 'home address',
            'disciplinary record', 'public employee', 'personnel file',
            'employee information', 'employment record',
        ]),
        'counter_arguments': json.dumps([
            'Name, current position, date of first employment, current duties, and salary are affirmatively public under N.C.G.S. § 126-23',
            'Formal disciplinary actions (written reprimands, suspensions, dismissals) and their outcomes are public',
            'Records of an employee\'s official conduct are not "personnel records" in the exemption sense',
            'Challenge overbroad withholding that shields public employee information along with genuinely private data',
            'N.C.G.S. § 126-24 provides a mechanism for employees to request correction of false personnel records — not a basis for withholding true records',
            'Aggregate data and statistical reports on agency employment are public',
        ]),
        'notes': 'North Carolina\'s personnel records framework under N.C.G.S. § 132-1.1 and § 126-22 through § 126-25 is detailed and carefully balanced. The State Personnel Act provisions provide the specific framework for state employees; local government employees are covered by similar provisions. See Piedmont Publishing Co. v. City of Winston-Salem, 334 N.C. 595 (1993).',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.1(b)',
        'exemption_number': 'N.C.G.S. § 132-1.1(b)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that are privileged under attorney-client privilege or attorney work product doctrine are exempt from North Carolina\'s Public Records Law. The privilege protects confidential communications between government attorneys and their client agencies for the purpose of legal advice.',
        'scope': 'Confidential communications between government agencies and their legal counsel for the purpose of legal advice, and attorney work product prepared in anticipation of litigation. The privilege is narrow — it covers legal advice, not policy or business recommendations. Billing records and financial arrangements with counsel are generally public. Facts independently known are not privileged. Waiver occurs through voluntary disclosure. North Carolina courts apply the privilege narrowly given the Public Records Law\'s strong disclosure mandate.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'N.C.G.S. 132-1.1(b)', 'privileged communication',
            'attorney work product', 'in anticipation of litigation',
            'legal opinion', 'government attorney',
        ]),
        'counter_arguments': json.dumps([
            'Policy and business advice from attorneys is not privileged',
            'Waiver through public reliance on the advice negates the privilege',
            'Billing records are generally public',
            'Facts underlying legal advice are not privileged',
            'North Carolina courts apply the privilege narrowly given the PRL\'s strong openness presumption',
            'Challenge claims that entire communications with counsel are privileged — only specific legal advice portions qualify',
        ]),
        'notes': 'North Carolina\'s attorney-client privilege exemption under N.C.G.S. § 132-1.1(b) is applied narrowly. NC courts consistently require agencies to demonstrate specific privilege for each withheld communication and apply the exemption consistent with the statute\'s strong disclosure mandate.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.1(c)',
        'exemption_number': 'N.C.G.S. § 132-1.1(c)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information obtained from a person and privileged or confidential if the information would be exempt under FOIA (5 U.S.C. § 552(b)(4)) or where disclosure would cause competitive harm, are exempt from North Carolina\'s Public Records Law.',
        'scope': 'Trade secrets as defined in N.C.G.S. § 66-152 (North Carolina Trade Secrets Protection Act): business or technical information that provides a competitive advantage and is kept confidential. Government-generated records cannot be trade secrets. The agency must independently evaluate vendor trade secret designations. Contract prices, amounts paid with public funds, and government expenditures are generally public even when vendors claim trade secret protection. NC courts require agencies to provide record-specific analysis supporting trade secret withholding.',
        'key_terms': json.dumps([
            'trade secret', 'North Carolina Trade Secrets Protection Act',
            'N.C.G.S. 66-152', 'N.C.G.S. 132-1.1(c)', 'proprietary information',
            'competitive harm', 'commercial information', 'financial information',
            'vendor records', 'contractor information', 'business information',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds are public regardless of trade secret claims',
            'The submitter must demonstrate that information meets the NC Trade Secrets Protection Act definition',
            'The agency must independently evaluate trade secret claims — vendor designations are not self-executing',
            'Government-generated records and analysis are not trade secrets',
            'Information required by law to be submitted has reduced secrecy expectations',
            'Publicly available information cannot qualify as a trade secret',
        ]),
        'notes': 'NC\'s trade secret exemption under N.C.G.S. § 132-1.1(c) applies the NC Trade Secrets Protection Act. NC courts require agencies to provide specific, record-level analysis supporting trade secret claims. Contract amounts and public expenditures are consistently held to be public.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-6(b)',
        'exemption_number': 'N.C.G.S. § 132-6(b)',
        'short_name': 'Personal Privacy — Unwarranted Invasion',
        'category': 'privacy',
        'description': 'Information in public records whose disclosure would constitute a clearly unwarranted invasion of personal privacy is exempt from North Carolina\'s Public Records Law, subject to a balancing test weighing the public interest against the individual privacy interest.',
        'scope': 'Information about private individuals where disclosure would constitute a genuine, substantial invasion of personal privacy. North Carolina courts apply a balancing test weighing the public interest in disclosure against the individual privacy interest. Information about public officials in their official capacity is generally not protected — the privacy interest of officials exercising public duties is minimal compared to the public interest in accountability. The agency bears the burden of demonstrating that the privacy interest is substantial and outweighs the public interest. Mere embarrassment or discomfort is not a sufficient privacy interest.',
        'key_terms': json.dumps([
            'personal privacy', 'clearly unwarranted invasion',
            'N.C.G.S. 132-6(b)', 'privacy balancing test', 'private individual',
            'privacy interest', 'public interest balancing', 'personal information',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" — a high threshold not met by mere discomfort with disclosure',
            'Information about public officials in their official capacity rarely satisfies this standard',
            'The agency bears the burden of demonstrating that the privacy interest clearly outweighs the public interest',
            'Voluntarily disclosed information has reduced privacy protection',
            'Information about conduct in an official capacity is subject to a strong public interest in accountability',
            'NC courts apply a genuine balancing test — generic "privacy concerns" are insufficient',
        ]),
        'notes': 'North Carolina\'s privacy exemption under N.C.G.S. § 132-6(b) requires genuine balancing. NC courts apply it narrowly and have been particularly clear that information about public officials in their official capacity receives minimal privacy protection. The burden is on the agency to justify withholding.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.4A',
        'exemption_number': 'N.C.G.S. § 132-1.4A',
        'short_name': 'Body-Worn Camera and Dash Camera Footage',
        'category': 'law_enforcement',
        'description': 'Recordings from law enforcement body-worn cameras (BWC) and dashboard cameras (dash cam) are specifically classified as personnel records and are not public records under North Carolina law unless the agency head or a court orders disclosure.',
        'scope': 'N.C.G.S. § 132-1.4A (enacted 2016) creates a specific exemption for law enforcement BWC and dash cam footage, classifying it as personnel records. However, footage may be disclosed in six enumerated circumstances: (1) subject of footage requests their own footage; (2) footage documents serious bodily injury or death; (3) the agency head determines release is in the public interest; (4) a court orders disclosure after in camera review; (5) footage is needed for a criminal or civil legal proceeding; or (6) footage documents use of force. Requesters seeking BWC footage should specifically argue these disclosure triggers and consider petitioning a court for release.',
        'key_terms': json.dumps([
            'body camera footage', 'body-worn camera', 'BWC', 'dashboard camera',
            'dash cam', 'N.C.G.S. 132-1.4A', 'law enforcement camera footage',
            'police video', 'use of force footage', 'BWC disclosure',
        ]),
        'counter_arguments': json.dumps([
            'Footage documenting serious bodily injury or death must be disclosed or considered for disclosure',
            'Footage documenting use of force by law enforcement is subject to disclosure under § 132-1.4A(c)(2)',
            'The agency head may determine that release is in the public interest — request this determination formally',
            'File a petition in superior court for in camera review and potential disclosure order',
            'Challenge whether the footage truly qualifies as a "personnel record" if it documents civilian-agency interactions',
            'Footage that has already been publicly released in any form loses its exempt status',
        ]),
        'notes': 'N.C.G.S. § 132-1.4A is North Carolina\'s most significant recent public records development, enacted in 2016 in response to high-profile officer-involved incidents. The statute creates a detailed framework for BWC footage access that is more restrictive than most states. Requesters seeking footage should specifically invoke the enumerated disclosure triggers in § 132-1.4A(c) and consider the superior court petition process under § 132-1.4A(g).',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.7',
        'exemption_number': 'N.C.G.S. § 132-1.7',
        'short_name': 'Infrastructure and Security Vulnerability Records',
        'category': 'safety',
        'description': 'Records that contain information about the physical security of government facilities or critical infrastructure, including vulnerability assessments and security plans, are exempt from North Carolina\'s Public Records Law where disclosure would create a specific security risk.',
        'scope': 'Vulnerability assessments, security plans, and related records for government buildings, utilities, and critical public infrastructure. The exemption requires a specific, articulable security risk from disclosure — general "security" labels are insufficient. Budget records, general policy descriptions, and program overviews for security programs are public. The agency must demonstrate specific harm from disclosing each withheld record.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'N.C.G.S. 132-1.7', 'security risk', 'infrastructure security',
            'facility security', 'emergency response plan', 'security vulnerability',
        ]),
        'counter_arguments': json.dumps([
            'Budget and expenditure records for security programs are public',
            'General policy descriptions that do not reveal specific vulnerabilities are public',
            'Challenge claims that entire security contracts are exempt when only technical specifications warrant protection',
            'The agency must demonstrate a specific, articulable security risk for each withheld record',
            'Widely known security measures do not qualify for this exemption',
        ]),
        'notes': 'NC\'s security exemption under N.C.G.S. § 132-1.7 is applied narrowly. NC courts require agencies to demonstrate specific security risk from disclosure, not assert a blanket security category. Budget and program records for security functions are consistently held to be public.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.3',
        'exemption_number': 'N.C.G.S. § 132-1.3',
        'short_name': 'Juvenile Records',
        'category': 'privacy',
        'description': 'Records of juvenile proceedings and related records identifying juveniles involved in North Carolina\'s juvenile justice system are exempt from public records disclosure to protect minors and support rehabilitation goals.',
        'scope': 'Records of juvenile court proceedings under N.C.G.S. Chapter 7B (Juvenile Code). Adult criminal records and adult court proceedings are fully public. Aggregate statistics about the juvenile justice system and program performance are public. Policy and budget records for juvenile courts are public. The exemption does not cover general information about the juvenile justice system — only individually identifiable records of specific juveniles.',
        'key_terms': json.dumps([
            'juvenile record', 'juvenile court', 'juvenile proceeding',
            'N.C.G.S. 132-1.3', 'N.C.G.S. Chapter 7B', 'minor record',
            'juvenile justice', 'delinquency record', 'juvenile adjudication',
        ]),
        'counter_arguments': json.dumps([
            'Adult records are fully public',
            'Aggregate juvenile justice statistics and program data are public',
            'Policy and budget records for juvenile courts are public',
            'Challenge claims that records about adults involved in juvenile matters are protected',
        ]),
        'notes': 'North Carolina\'s juvenile records exemption is reinforced by the Juvenile Code (N.C.G.S. Chapter 7B). The protection applies to specific records of juvenile proceedings, not to general records held by juvenile courts or related agencies.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.1(e)',
        'exemption_number': 'N.C.G.S. § 132-1.1(e)',
        'short_name': 'Mediation and Settlement Records',
        'category': 'deliberative',
        'description': 'Records from court-ordered or state-agency-supervised mediation proceedings are confidential and exempt from North Carolina\'s Public Records Law to encourage candid settlement discussions.',
        'scope': 'Communications and records from formal mediation proceedings involving public agencies, including mediator notes and settlement communications made during mediation. The exemption does not cover: final settlement agreements and consent orders (which are public as government actions); pre-mediation dispute records; or general agency correspondence about disputes. Final settlements resolving claims against or by a public agency are public as government documents.',
        'key_terms': json.dumps([
            'mediation record', 'settlement record', 'N.C.G.S. 132-1.1(e)',
            'dispute resolution', 'mediator notes', 'settlement communication',
            'ADR', 'alternative dispute resolution', 'consent order',
        ]),
        'counter_arguments': json.dumps([
            'Final settlement agreements are public — they are government actions',
            'Pre-mediation dispute correspondence is generally public',
            'Challenge whether the process was formal "mediation" or informal negotiation',
            'Consent orders and judgments are always public court records',
        ]),
        'notes': 'NC\'s mediation records exemption under N.C.G.S. § 132-1.1(e) follows the majority rule that final settlements are public. NC courts consistently hold that the exemption covers only the mediation process itself, not the outcome.',
    },
    {
        'jurisdiction': 'NC',
        'statute_citation': 'N.C.G.S. § 132-1.10',
        'exemption_number': 'N.C.G.S. § 132-1.10',
        'short_name': 'Social Security Numbers and Personal Identifiers',
        'category': 'privacy',
        'description': 'Social Security numbers and similar government-issued identification numbers in public records are exempt from disclosure under North Carolina\'s Public Records Law to protect against identity theft and financial fraud.',
        'scope': 'Social Security numbers, driver\'s license numbers, bank account numbers, and similar personal identifiers appearing in public records. The exemption is field-specific — agencies must redact the specific identifier and release the remainder of the record. The exemption does not protect entire documents containing identifiers. Names, positions, salaries, and other non-identifier information in the same document are not covered by this exemption. N.C.G.S. § 132-1.10 requires agencies to develop and implement policies for redacting SSNs from public records.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'driver\'s license number',
            'N.C.G.S. 132-1.10', 'personal identifier', 'identity theft',
            'bank account number', 'PII', 'personally identifiable information',
            'financial account number',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — agencies must redact only the identifier and release the rest',
            'Challenge blanket withholding of documents containing a few protected identifiers',
            'Names, positions, salaries, and other information in the same document are not protected',
            'The agency\'s obligation to redact SSNs does not create authority to withhold entire documents',
        ]),
        'notes': 'North Carolina\'s SSN and personal identifier protection under N.C.G.S. § 132-1.10 is clear and well-established. NC courts consistently hold that the exemption is field-specific and that agencies must redact and release rather than withhold entire documents containing protected identifiers.',
    },
]

# =============================================================================
# RULES
# North Carolina Public Records Law, N.C.G.S. § 132-1 et seq.
# Key features: "as promptly as possible" standard (no specific deadline);
# no administrative appeal — superior court is the enforcement venue;
# attorney's fees for prevailing requesters; $0.05/page for paper copies;
# no identity or purpose requirement; strong broad definition of public record.
# =============================================================================

NC_RULES = [
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'response_standard',
        'param_value': 'as_promptly_as_possible',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6(a)',
        'notes': 'Under N.C.G.S. § 132-6(a), every custodian of public records must furnish copies of such records upon request at a time and under conditions that will not damage or alter the records and will not materially interfere with the operations of the agency. The statute requires that records be made available "as promptly as possible." There is no specific statutory deadline — the standard is promptness. North Carolina courts have found agencies in violation of the PRL for unreasonable delays, but the standard is flexible and fact-specific. Requesters facing significant delays should send follow-up letters citing § 132-6(a) and the potential for attorney\'s fee awards.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'no_specific_deadline',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6(a)',
        'notes': 'Unlike most states, North Carolina\'s Public Records Law does not impose a specific numerical deadline (no 3-day, 5-day, or 10-day rule). The "as promptly as possible" standard is intentionally flexible and depends on the complexity of the request and the agency\'s resources. This is a notable weakness of NC\'s PRL compared to states with specific deadlines. Requesters should document their requests and follow up promptly if not receiving a timely response, as unreasonable delay can support a court action for attorney\'s fees.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6(a)',
        'notes': 'North Carolina\'s Public Records Law does not require written requests — oral requests are valid. However, written requests are strongly recommended to create a paper trail, document the request\'s scope, and establish a record for potential litigation. Many agencies have online portals for public records requests. Requesters need not state a reason for the request or provide identity beyond contact information for delivery.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'purpose_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6(a)',
        'notes': 'North Carolina agencies may NOT require requesters to state the purpose of their records request or provide identifying information as a condition of access. The right of access under the PRL is universal and does not depend on the requester\'s identity or purpose. NC courts have held that purpose and motive are irrelevant to the right of access. An agency that conditions access on a stated purpose is violating the PRL.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_per_page',
        'param_value': '0.05',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6.2',
        'notes': 'Under N.C.G.S. § 132-6.2, agencies may charge fees for copies of public records not to exceed the actual cost of reproducing the records. The standard rate for black-and-white paper copies is $0.05 per page in many jurisdictions, though this is not uniformly set by statute — actual practice varies by agency. Agencies may not charge for staff time spent searching or reviewing records. For electronic records, the charge is the actual cost of the storage medium — often zero for email delivery.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'fee_cap',
        'param_key': 'no_search_or_review_fees',
        'param_value': 'prohibited',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6.2(b)',
        'notes': 'Under N.C.G.S. § 132-6.2(b), agencies may not charge for the time spent locating, retrieving, or reviewing records. Only actual reproduction costs are permissible. An agency that charges hourly rates for "research" or "review" is violating the PRL. NC courts have struck down fee arrangements that include staff labor charges. This is a meaningful protection for requesters seeking large volumes of records.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-9',
        'notes': 'North Carolina has NO administrative appeal mechanism for public records denials. There is no agency head appeal, no ombudsman review, and no state administrative tribunal. A requester who believes records were wrongfully withheld or that response was unreasonably delayed must seek relief directly in superior court under N.C.G.S. § 132-9. This is a significant structural limitation of NC\'s PRL — the absence of an administrative appeal tier means requesters must litigate to enforce their rights.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-9(a)',
        'notes': 'Under N.C.G.S. § 132-9(a), any person denied access to public records may apply to the superior court of the county where the agency is located for an order compelling disclosure. The court reviews the denial de novo and may conduct in camera inspection of withheld records. The court may grant preliminary injunctive relief without requiring bond where the public interest in disclosure is strong. No specific statute of limitations is provided. The superior court action is the sole formal enforcement mechanism for NC public records disputes.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'discretionary_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-9(c)',
        'notes': 'Under N.C.G.S. § 132-9(c), if a requester substantially prevails in a superior court action for access to public records, the court may award reasonable attorney\'s fees against the agency. The fee award is discretionary — the court considers the public benefit from the records, the agency\'s conduct, and whether the agency had a reasonable good-faith basis for its position. A pattern of bad-faith withholding or a clearly meritless denial supports a fee award. The availability of discretionary fees provides meaningful deterrence against unjustified denials.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-1(b)',
        'notes': 'Under N.C.G.S. § 132-1(b), the Public Records Law is premised on the principle that "the public interest is served by open government." NC courts have consistently held that the burden of demonstrating an exemption rests on the agency. The exemptions are strictly construed in favor of disclosure, and ambiguity is resolved against withholding. Agencies must affirmatively demonstrate that each withheld record falls within a specific statutory exemption.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6(a)',
        'notes': 'North Carolina agencies must release all nonexempt, reasonably segregable portions of records when only part qualifies for an exemption. Blanket withholding of documents containing some exempt content is a PRL violation. The agency must specifically redact only the exempt portions and provide the remainder. NC courts apply this segregability requirement and have found agencies in violation for over-withholding. The agency must identify the specific exemption claimed for each redacted or withheld portion.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'broad_definition_of_public_record',
        'param_value': 'all_materials_in_connection_with_public_business',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-1(a)',
        'notes': 'North Carolina\'s definition of "public record" under N.C.G.S. § 132-1(a) is exceptionally broad: all documents, papers, letters, maps, books, photographs, films, sound recordings, magnetic or other tapes, electronic data processing records, artifacts, or other documentary material, regardless of physical form or characteristics, made or received pursuant to law or ordinance or in connection with the transaction of public business. This broad definition means that emails, text messages, social media posts, voicemails, and other modern communications by government officials are public records when related to government business. NC courts have consistently applied this broad definition.',
    },
    {
        'jurisdiction': 'NC',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_access',
        'param_value': 'required_in_electronic_format',
        'day_type': None,
        'statute_citation': 'N.C.G.S. § 132-6.1',
        'notes': 'Under N.C.G.S. § 132-6.1, agencies must provide electronic records in an electronic format on request, using formats that do not require purchase of proprietary software. If a record exists in an electronic form, the agency cannot require the requester to accept a paper copy. Agencies may not charge more than the actual cost of providing electronic records — for email delivery, the actual cost is often zero. This provision is important for journalists and researchers seeking data in usable form.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

NC_TEMPLATES = [
    {
        'jurisdiction': 'NC',
        'record_type': 'general',
        'template_name': 'General North Carolina Public Records Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Public Records Law Request — N.C.G.S. § 132-1 et seq.

Dear Custodian of Public Records:

Pursuant to North Carolina's Public Records Law, N.C.G.S. § 132-1 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

Under N.C.G.S. § 132-6.1, I request that electronic records be provided in an electronic format (email or download link) where available. This minimizes reproduction cost and often results in zero-cost delivery.

I am willing to pay the actual cost of reproducing records per N.C.G.S. § 132-6.2. Under N.C.G.S. § 132-6.2(b), agencies may not charge for staff time spent locating, retrieving, or reviewing records — only actual reproduction costs are permissible. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under N.C.G.S. § 132-1(b), the Public Records Law reflects the principle that the public interest is served by open government. The burden of demonstrating that any record is exempt rests on the agency. All exemptions are strictly construed in favor of disclosure. Under N.C.G.S. § 132-6(a), all nonexempt, reasonably segregable portions of partially withheld records must be provided.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) cite the specific N.C.G.S. provision authorizing the exemption; (3) explain how the specific exemption applies to each record; and (4) confirm that all nonexempt, segregable portions of partially withheld records have been provided.

Under N.C.G.S. § 132-6(a), please provide records "as promptly as possible." If production will be delayed, please advise me of the expected timeline.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. While North Carolina\'s Public Records Law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. Under N.C.G.S. § 132-6.1, electronic delivery incurs zero reproduction cost.

North Carolina's Public Records Law reflects the strong public interest in open government. A fee waiver for this request would advance that interest.''',
        'expedited_language': '''I request that this public records request be processed as promptly as possible, as required by N.C.G.S. § 132-6(a). These records are particularly time-sensitive because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond that date will {{harm_from_delay}}. Please contact me immediately at {{requester_email}} or {{requester_phone}} if any clarification would expedite production.''',
        'notes': 'General NC Public Records Law template. Key features: (1) no specific deadline — "as promptly as possible" under § 132-6(a); (2) no administrative appeal — superior court enforcement under § 132-9; (3) attorney\'s fees (discretionary) for prevailing requesters under § 132-9(c); (4) electronic records must be provided in electronic format under § 132-6.1; (5) no search/review fees under § 132-6.2(b); (6) broad public record definition — all materials in connection with public business under § 132-1(a); (7) BWC footage has specific exemption under § 132-1.4A. Reference N.C.G.S. § 132, not "FOIA."',
    },
    {
        'jurisdiction': 'NC',
        'record_type': 'law_enforcement',
        'template_name': 'North Carolina Public Records Law Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Public Records Law Request — Law Enforcement Records, N.C.G.S. § 132-1 et seq.

Dear Custodian of Public Records:

Pursuant to North Carolina's Public Records Law, N.C.G.S. § 132-1 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

Under N.C.G.S. § 132-1.4(c), the following information must be disclosed regardless of the status of any investigation:
- The time, date, and location of the occurrence
- The name and age of the victim (unless victim identity is otherwise protected)
- The factual circumstances surrounding the crime or incident
- A description of any injuries
- The name of the investigating officers
- Whether any arrests were made and the identity of persons arrested
- The charges filed

This request includes, but is not limited to, all records required to be disclosed under § 132-1.4(c) plus:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports and documentation
- Officer disciplinary and complaint records for involved personnel
- Dispatch records and Computer-Aided Dispatch (CAD) logs

Regarding body-worn camera footage: Under N.C.G.S. § 132-1.4A, I request disclosure of any BWC or dash cam footage because: [select applicable] (a) the footage documents use of force by law enforcement; (b) the footage documents an officer-involved death or serious bodily injury; (c) public interest requires disclosure. I am prepared to petition the superior court for in camera review and a disclosure order under § 132-1.4A(g) if the agency head declines to authorize release.

Regarding the general criminal investigation exemption under N.C.G.S. § 132-1.4: Any withholding beyond the specific categories listed above must be justified by identification of a specific ongoing criminal investigation that would be harmed by disclosure of each specific record.

Under N.C.G.S. § 132-6(a), please provide records as promptly as possible.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records concern {{public_interest_explanation}}. Under N.C.G.S. § 132-6.1, electronic delivery incurs zero reproduction cost. A fee waiver would advance the Public Records Law\'s transparency goals.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}. North Carolina\'s Public Records Law requires records be provided "as promptly as possible" — please prioritize this request.''',
        'notes': 'North Carolina law enforcement records template. Key features: (1) § 132-1.4(c) mandatory disclosures — cite these specifically, agencies routinely fail to provide them; (2) BWC footage has specific exemption under § 132-1.4A with enumerated disclosure triggers — cite applicable trigger; (3) superior court petition available for BWC disclosure under § 132-1.4A(g); (4) no administrative appeal — superior court under § 132-9; (5) discretionary attorney\'s fees under § 132-9(c); (6) "as promptly as possible" standard — document request date carefully for delay claims.',
    },
    {
        'jurisdiction': 'NC',
        'record_type': 'financial',
        'template_name': 'North Carolina Public Records Law Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Public Records Law Request — Contracts and Expenditure Records, N.C.G.S. § 132-1 et seq.

Dear Custodian of Public Records:

Pursuant to North Carolina's Public Records Law, N.C.G.S. § 132-1 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Contractor/vendor (if applicable): {{contractor_name}}
Contract period: {{date_range_start}} through {{date_range_end}}
Contract number (if known): {{contract_number}}

This request includes, but is not limited to:
- Executed contracts and all amendments/modifications
- Bid and proposal documents, including all submitted bids/proposals
- Invoices, payment records, and vouchers
- Performance evaluations and compliance records

Regarding trade secret claims under N.C.G.S. § 132-1.1(c): Contract prices, amounts paid with public funds, and total government expenditures are public regardless of vendor trade secret designations. The agency must independently evaluate trade secret claims under N.C.G.S. § 66-152 (NC Trade Secrets Protection Act). Vendor "confidential" designations are not self-executing — the agency bears the burden of demonstrating that each withheld record satisfies the statutory trade secret definition.

Under N.C.G.S. § 132-6(a), all nonexempt, segregable portions of partially withheld records must be provided. Under N.C.G.S. § 132-6.1, electronic records must be provided in electronic format on request.

Under N.C.G.S. § 132-6.2(b), I will pay reproduction costs but not staff time for searching or reviewing records. Please respond as promptly as possible.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. These records concern the expenditure of public funds — a core purpose of North Carolina\'s Public Records Law. Electronic delivery under § 132-6.1 incurs zero reproduction cost. A fee waiver would further the PRL\'s transparency mandate.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'NC government contracts template. Key points: (1) contract prices and public expenditures are always public; (2) trade secret claims require independent analysis under NC Trade Secrets Protection Act; (3) no administrative appeal — superior court under § 132-9; (4) discretionary attorney\'s fees under § 132-9(c); (5) electronic records must be provided electronically under § 132-6.1; (6) no search or review fees under § 132-6.2(b).',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in NC_EXEMPTIONS:
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

    print(f'NC exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in NC_RULES:
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

    print(f'NC rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in NC_TEMPLATES:
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

    print(f'NC templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'NC total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_nc', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
