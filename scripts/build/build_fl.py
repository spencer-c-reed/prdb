#!/usr/bin/env python3
"""Build Florida Public Records Law data: exemptions, rules, and templates.

Covers Florida's Government-in-the-Sunshine Law / Public Records Act,
Chapter 119, Florida Statutes. Florida has disclosure as the default rule —
all state, county, and municipal records are open unless a specific exemption
applies.

Run: python3 scripts/build/build_fl.py
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
# Florida has 1,000+ statutory exemptions scattered across the Florida Statutes.
# The core ones are in or cross-referenced by Ch. 119 itself. This list covers
# the 12 most commonly invoked exemptions in practice.
# =============================================================================

FL_EXEMPTIONS = [
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(c)',
        'exemption_number': '§ 119.071(2)(c)',
        'short_name': 'Active Criminal Intelligence / Investigation',
        'category': 'law_enforcement',
        'description': 'Exempts active criminal intelligence and investigative information from disclosure. This is one of the most frequently invoked exemptions in Florida and covers ongoing law enforcement operations.',
        'scope': 'Criminal intelligence information means data compiled by a criminal justice agency regarding identifiable individuals or groups in anticipation of criminal activity. Criminal investigative information means information compiled for a specified active criminal investigation. Both are exempt only while the investigation or prosecution is active. Once the investigation is inactive (closed without prosecution or prosecution is concluded), the records generally become public.',
        'key_terms': json.dumps([
            'active criminal investigation', 'criminal intelligence', 'criminal investigative information',
            'law enforcement', 'ongoing investigation', 'prosecution pending', 'active case',
            'confidential informant', 'undercover operation',
        ]),
        'counter_arguments': json.dumps([
            'Challenge whether the investigation is truly "active" — Florida courts have held that closed or inactive investigations do not qualify',
            'Request records from concluded prosecutions; once a case is adjudicated, the active-investigation rationale evaporates',
            'Ask the agency to confirm the investigation is active and provide a basis — vague assertions of ongoing activity are insufficient',
            'Factual information in the record that does not reveal investigative techniques or identify informants may be segregable',
            'Arrest records, booking information, and court records are separately public and not shielded by this exemption',
            'Florida AG opinions have held that the agency bears the burden of demonstrating active status',
        ]),
        'notes': 'Florida\'s most litigated public records exemption. The Supreme Court of Florida has held that "active" means the investigation is continuing with a reasonable expectation of prosecution. See Downs v. Austin, 559 So. 2d 246 (Fla. 1st DCA 1990). The exemption is in the statute, not self-executing — the agency must affirmatively invoke it.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(1)(d)',
        'exemption_number': '§ 119.071(1)(d)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Communications between a public agency and its attorney that are protected by attorney-client privilege under the Florida Evidence Code are exempt from disclosure.',
        'scope': 'Attorney-client privileged communications between a government agency and its legal counsel, including outside counsel. Protects confidential legal advice, litigation strategy, and privileged work product. Does not cover communications made in furtherance of a crime or fraud, and does not protect factual information that the attorney also communicated through non-privileged channels.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'legal advice', 'work product', 'litigation strategy',
            'confidential communication', 'privileged', 'counsel', 'legal opinion',
        ]),
        'counter_arguments': json.dumps([
            'Florida courts construe attorney-client privilege narrowly in the government context — the public interest in transparency weighs against broad privilege claims',
            'Communications that are primarily factual, rather than legal advice, are not protected',
            'The privilege belongs to the agency, not the attorney — the agency can waive it',
            'If the substance of the legal advice has been publicly disclosed or acted upon in public, privilege may be waived',
            'Billing records and invoices from outside counsel are generally not privileged',
            'Challenge whether the communication was made for the purpose of obtaining legal advice, not merely for business or policy advice',
        ]),
        'notes': 'Florida recognizes attorney-client privilege for government entities but applies it in tension with the Public Records Act\'s strong disclosure default. See City of Riviera Beach v. Barfield, 642 So. 2d 1135 (Fla. 4th DCA 1994). The Florida Bar has also issued guidance on the scope of government lawyer privilege.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(1)(b)',
        'exemption_number': '§ 119.071(1)(b)',
        'short_name': 'Sealed Bids / Competitive Solicitations',
        'category': 'commercial',
        'description': 'Bids and responses to requests for proposals received by a public agency are exempt until the agency provides notice of its decision or intended decision, or until 30 days after the bid opening.',
        'scope': 'Covers bids, proposals, replies, and responses to competitive solicitations (RFPs, ITBs, RFQs) received by an agency. The exemption is strictly time-limited: it expires when the agency posts notice of intended award or 30 days after opening, whichever occurs first. After that point, all bids are fully public. Also covers trade secret portions of bids if properly designated by the vendor.',
        'key_terms': json.dumps([
            'sealed bid', 'competitive solicitation', 'request for proposals', 'RFP', 'ITB', 'RFQ',
            'procurement', 'intended decision', 'bid opening', 'vendor proposal',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires 30 days after bid opening or upon notice of intended decision — request records after that point',
            'After contract award, all bid materials are public — a request at that stage cannot be denied under this exemption',
            'Trade secret designations by vendors must be reviewed by the agency; the agency cannot simply defer to vendor designations',
            'Final contract terms and prices are not protected after award — only pre-decisional bid materials qualify',
            'If the agency has already made an award decision public, the exemption has expired',
        ]),
        'notes': 'Florida\'s procurement exemption has a hard expiration tied to the award decision notice. See § 119.071(1)(b)(2). Vendors who designate trade secrets in bids must be prepared to defend those designations if a requester challenges them.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(a)',
        'exemption_number': '§ 119.071(2)(a)',
        'short_name': 'Social Security Numbers',
        'category': 'privacy',
        'description': 'Social Security numbers held by public agencies are exempt from public records disclosure.',
        'scope': 'Social Security numbers, in whole or in part, maintained by any agency. Applies regardless of the context in which the SSN appears. Agencies must redact SSNs from otherwise disclosable records before production. The underlying record remains public; only the SSN itself is protected.',
        'key_terms': json.dumps([
            'social security number', 'SSN', 'social security', 'identification number',
            'federal tax ID', 'redaction', 'personal identifier',
        ]),
        'counter_arguments': json.dumps([
            'Only the SSN itself is exempt — the rest of the record containing the SSN remains public and must be produced with the SSN redacted',
            'Challenge attempts to withhold entire documents because they contain an SSN somewhere in them',
            'The exemption does not protect other identifiers like employee IDs, driver\'s license numbers, or dates of birth',
        ]),
        'notes': 'One of the clearest and narrowest of Florida\'s exemptions. The statute is unambiguous that only the number itself is exempt; the surrounding record must be produced with SSN redacted. See Fla. Att\'y Gen. Op. 2006-47.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(j)',
        'exemption_number': '§ 119.071(2)(j)',
        'short_name': 'Medical Records',
        'category': 'privacy',
        'description': 'Medical records, including medical histories, mental health records, and similar health information, are exempt from public disclosure.',
        'scope': 'Medical records of individuals held by public agencies. Covers hospital and clinic records, mental health treatment records, substance abuse treatment records, and medical information obtained by agencies in the course of their functions. Also covers medical information about public employees obtained through employment-related medical examinations.',
        'key_terms': json.dumps([
            'medical record', 'health record', 'medical history', 'mental health', 'treatment record',
            'patient information', 'HIPAA', 'health information', 'diagnosis', 'medical examination',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects individually identified medical information — aggregate or anonymized health data does not qualify',
            'Records about an agency\'s management of a medical situation (e.g., communications about an employee\'s leave) may be distinguishable from the medical records themselves',
            'HIPAA applies to covered entities — not all government agencies are covered entities, and state law provides the relevant exemption',
            'Autopsy reports are treated as medical records in some contexts but as public records in others — consult case-specific authority',
        ]),
        'notes': 'Florida has multiple overlapping medical records exemptions in Ch. 395 (hospitals), Ch. 394 (mental health), and § 119.071. The Ch. 119 exemption is a catch-all. Florida\'s public records law and HIPAA both apply where agencies are HIPAA covered entities.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(e)',
        'exemption_number': '§ 119.071(2)(e)',
        'short_name': 'Security System Plans',
        'category': 'safety',
        'description': 'Building security system plans, access controls, and security procedures for public facilities are exempt to prevent exploitation for criminal purposes.',
        'scope': 'Security system plans, including schematic drawings, for any real property owned or leased by a public agency. Also covers security procedures, access controls, and any information revealing vulnerabilities in physical or electronic security systems. Includes cybersecurity threat information and vulnerability assessments.',
        'key_terms': json.dumps([
            'security system', 'security plan', 'access control', 'vulnerability assessment',
            'security procedure', 'schematic', 'cybersecurity', 'critical infrastructure',
            'building security', 'intrusion detection',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects security plans and procedures, not all information about a facility',
            'General information about a building\'s location or layout that does not reveal security vulnerabilities is not covered',
            'Expenditure records for security contracts are public — only the technical security details are exempt',
            'Challenge overly broad assertions that entire procurement files are security-sensitive',
        ]),
        'notes': 'Expanded significantly after 9/11 to cover cybersecurity and critical infrastructure. Florida courts have upheld this exemption broadly when agencies can articulate a specific security concern. See City of Tallahassee v. Florida Pub. Telecomm. Union, 766 So. 2d 1100 (Fla. 1st DCA 2000).',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(b)',
        'exemption_number': '§ 119.071(2)(b)',
        'short_name': 'Confidential Informants',
        'category': 'law_enforcement',
        'description': 'Information identifying a confidential informant or a source who provided information to a law enforcement agency under an express promise of confidentiality is exempt from disclosure.',
        'scope': 'Names and identifying information of confidential informants and sources. Also covers information that would indirectly identify a confidential source by process of elimination. Applies broadly to law enforcement, regulatory enforcement, and agency investigations where confidentiality was promised.',
        'key_terms': json.dumps([
            'confidential informant', 'CI', 'confidential source', 'informant identity',
            'promise of confidentiality', 'undercover', 'cooperating witness',
        ]),
        'counter_arguments': json.dumps([
            'The promise of confidentiality must be express — a general expectation of confidentiality is insufficient',
            'Once an informant has testified in open court, their identity may no longer be confidential',
            'Information that does not identify the informant but describes their information may be segregable and disclosable',
            'Challenge whether the agency actually made an express promise of confidentiality, or is retroactively claiming one',
        ]),
        'notes': 'Florida courts have applied this exemption broadly to protect informant safety. The express promise requirement is the key limiting principle — agencies cannot claim the exemption for information received without a specific confidentiality promise.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(d)',
        'exemption_number': '§ 119.071(2)(d)',
        'short_name': 'Draft Audit Reports',
        'category': 'deliberative',
        'description': 'Preliminary, draft, or tentative audit reports and workpapers prepared by internal or external auditors are exempt until the final audit report is released.',
        'scope': 'Draft audit reports, audit workpapers, and preliminary findings prepared in connection with internal or external audits of public agencies. The exemption expires when the final audit report is published or otherwise released. Covers state and local government audits, including those by the Auditor General and Office of Inspector General.',
        'key_terms': json.dumps([
            'draft audit', 'audit workpapers', 'preliminary findings', 'internal audit',
            'external audit', 'Inspector General', 'Auditor General', 'audit report',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is time-limited: once the final audit report is released, all draft materials become public',
            'Request the final audit report, which is unconditionally public',
            'Communications about audit findings that were circulated outside the audit process may not qualify',
            'Agency responses to audit findings are not covered by this exemption',
        ]),
        'notes': 'This exemption reflects the deliberative process rationale applied to auditing: protecting the integrity of the audit process by preventing premature disclosure that could trigger defensive responses. The final report is always public.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(f)',
        'exemption_number': '§ 119.071(2)(f)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets as defined in the Florida Uniform Trade Secrets Act (Fla. Stat. § 688.002) that are submitted to a public agency are exempt from disclosure.',
        'scope': 'Trade secrets submitted by private entities to government agencies as required by law or in connection with agency proceedings. The trade secret must meet the statutory definition: information that derives independent economic value from not being generally known, and the holder must have taken reasonable steps to maintain secrecy. Applies to formulas, processes, methods, technical data, and similar proprietary information submitted in regulatory filings, permits, and procurement.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive advantage', 'economic value',
            'confidential business information', 'formula', 'process', 'technical data',
            'Florida Uniform Trade Secrets Act', 'FUTSA',
        ]),
        'counter_arguments': json.dumps([
            'The submitter must demonstrate the information meets the statutory definition — a "confidential" label is not sufficient',
            'Information that is publicly available from other sources cannot be a trade secret',
            'Government-generated records reflecting the analysis or use of trade secret information may be separately disclosable',
            'The agency, not the submitter, determines whether the exemption applies — challenge agency deference to submitter designations',
            'The economic value from secrecy must be demonstrated, not assumed',
            'Challenge whether the submitter actually took reasonable steps to maintain secrecy',
        ]),
        'notes': 'Florida courts have held that the agency must independently verify that submitted information actually qualifies as a trade secret under § 688.002. See Forsberg v. Housing Authority of Miami Beach, 455 So. 2d 373 (Fla. 1984).',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.0712(2)',
        'exemption_number': '§ 119.0712(2)',
        'short_name': 'Driver License / Motor Vehicle Records',
        'category': 'privacy',
        'description': 'Personal information from motor vehicle records, including addresses, photographs, and medical information, is exempt from disclosure under Florida\'s implementation of the federal Driver\'s Privacy Protection Act.',
        'scope': 'Personal information in motor vehicle and driver license records maintained by the Department of Highway Safety and Motor Vehicles. Includes home addresses, telephone numbers, photographs, Social Security numbers, and medical information. There are exceptions for government agency use, licensed private investigators, certain commercial uses, and individuals requesting their own records.',
        'key_terms': json.dumps([
            'driver license', 'motor vehicle record', 'DPPA', 'Driver\'s Privacy Protection Act',
            'DHSMV', 'vehicle registration', 'home address', 'personal information',
        ]),
        'counter_arguments': json.dumps([
            'The DPPA exceptions are broad — confirm whether the requester\'s purpose fits a statutory exception',
            'Law enforcement agencies can obtain motor vehicle records without restriction',
            'Records researchers and commercial users may qualify under the permitted uses',
            'Challenge attempts to apply this exemption to non-DMV records that happen to contain an address',
        ]),
        'notes': 'Florida adopted § 119.0712(2) to implement the federal DPPA, 18 U.S.C. § 2721 et seq. The federal statute preempts state law to the extent Florida provides less protection. The DPPA exceptions are numerous and litigated frequently.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(3)(a)',
        'exemption_number': '§ 119.071(3)(a)',
        'short_name': 'Home Addresses / Personal Info of Public Employees',
        'category': 'privacy',
        'description': 'Home addresses, telephone numbers, Social Security numbers, and personal information of current and former agency employees and their family members are exempt from disclosure.',
        'scope': 'Home addresses, personal telephone numbers, SSNs, and similar personal information of public officers, employees, and their family members. Also covers the personal information of spouses and children. Notably does NOT protect salary, title, job duties, or other professional information, which remain public.',
        'key_terms': json.dumps([
            'home address', 'personal telephone number', 'public employee privacy',
            'officer privacy', 'family member', 'personal information', 'residential address',
        ]),
        'counter_arguments': json.dumps([
            'Only personal contact information (home address, personal phone) is exempt — official work contact information is public',
            'Salary, title, agency, and job duties of all public employees remain public regardless of this exemption',
            'The exemption does not protect a public official\'s official conduct, decisions, or use of public resources',
            'Former employees\' personal information remains protected, but records of their official acts do not',
        ]),
        'notes': 'Florida courts have drawn a clear line between personal contact information (protected) and official conduct/compensation (public). Salary databases are routinely produced under Florida\'s Public Records Act notwithstanding this exemption.',
    },
    {
        'jurisdiction': 'FL',
        'statute_citation': 'Fla. Stat. § 119.071(2)(g)',
        'exemption_number': '§ 119.071(2)(g)',
        'short_name': 'Victim Information / Domestic Violence',
        'category': 'privacy',
        'description': 'Names, addresses, and other identifying information of victims of sexual offenses, domestic violence, and certain other crimes are exempt from public records disclosure.',
        'scope': 'Identifying information of victims of sexual battery, lewd or lascivious offenses, incest, prostitution (as victim), and domestic violence. Also covers victims of stalking and human trafficking. Extends to witnesses who have requested confidentiality in certain cases. Applies to records held by law enforcement, courts, and social service agencies.',
        'key_terms': json.dumps([
            'victim identity', 'sexual offense victim', 'domestic violence victim', 'stalking victim',
            'human trafficking victim', 'victim confidentiality', 'witness protection',
        ]),
        'counter_arguments': json.dumps([
            'The exemption protects the victim\'s identity, not the entire record of the crime or prosecution',
            'Court records, prosecutorial records, and police records about the incident remain public with victim information redacted',
            'The accused\'s rights to court records for post-conviction relief may override this exemption in the judicial context',
            'Challenge attempts to withhold entire investigative files on the ground that they contain victim information',
        ]),
        'notes': 'Florida has among the most protective victim privacy laws in the country. The exemption was significantly expanded in the 2000s to cover human trafficking and stalking victims. Courts have upheld broad application to protect victim safety.',
    },
]

# =============================================================================
# RULES
# Florida's Public Records Act, Ch. 119, Fla. Stat.
# =============================================================================

FL_RULES = [
    {
        'jurisdiction': 'FL',
        'rule_type': 'initial_response',
        'param_key': 'response_timeline',
        'param_value': 'promptly',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(1)(c)',
        'notes': 'Florida\'s Public Records Act requires agencies to provide access to records "promptly." There is no specific number of days in the statute. Florida courts have held that "promptly" means within a reasonable time given the nature and volume of the request. Unreasonable delay can be challenged by mandamus or injunction. In practice, routine requests should be fulfilled within a few business days; complex requests may take longer.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'initial_response',
        'param_key': 'extensive_request_acknowledgment',
        'param_value': 'prompt_acknowledgment_required',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(1)(c)',
        'notes': 'For voluminous or complex requests, the agency must promptly acknowledge the request and provide an estimated time for fulfillment. The acknowledgment does not substitute for actually providing the records. Florida AG opinions have emphasized that agencies cannot simply sit on requests without communication.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_standard',
        'param_value': '0.15',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(4)(a)',
        'notes': 'Standard copy fee is $0.15 per one-sided page (8.5" x 14" or smaller). This is the statutory maximum for standard paper copies. Agencies may charge less. The $0.15 cap has been in place since 2004.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_per_page_certified',
        'param_value': '0.20',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(4)(a)',
        'notes': 'Certified copies may be charged at $0.20 per page. The extra $0.05 per page covers the cost of certification. Certification is required in certain legal proceedings.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'fee_cap',
        'param_key': 'duplication_extensive_use',
        'param_value': 'actual_cost_plus_reasonable_overhead',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(4)(b)',
        'notes': 'If the nature or volume of records requested requires extensive use of IT resources, clerical staff, or supervisory assistance, the agency may charge the actual cost of providing the records, including supervisory labor costs. "Extensive use" is a threshold agencies must demonstrate — they cannot charge for ordinary routine retrieval.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'fee_cap',
        'param_key': 'electronic_records_fee',
        'param_value': 'actual_cost_of_medium',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(4)(a)',
        'notes': 'For electronic records, agencies may charge the actual cost of the medium (e.g., USB drive, CD). Agencies may not charge per-page fees for electronic copies. If records exist electronically and can be transmitted via email, the cost is minimal.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'fee_waiver',
        'param_key': 'statutory_waiver',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(4)',
        'notes': 'Florida\'s Public Records Act does not have a statutory fee waiver provision. There is no media, nonprofit, or public interest fee waiver equivalent to federal FOIA. Requesters can ask agencies to waive fees as a matter of discretion, but there is no legal right to a waiver. The statutory per-page caps ($0.15, $0.20) are the main cost protection.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.11',
        'notes': 'Florida\'s Public Records Act has NO administrative appeal mechanism. There is no agency head appeal, no ombudsman review, and no administrative tribunal. A requester denied access must go directly to circuit court. This differs fundamentally from New York, Massachusetts, and federal FOIA.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_enforcement',
        'param_value': 'mandamus_or_injunction',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.11(1)',
        'notes': 'Any person denied access to public records may seek enforcement through the circuit court via mandamus or injunction. The court is required to give priority to public records cases on its docket. Florida courts have broad authority to order disclosure and to review withheld records in camera.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'attorneys_fees',
        'param_value': 'mandatory_if_unlawful_refusal',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.12',
        'notes': 'If a court determines that an agency unlawfully refused to permit inspection or copying of records, the court SHALL award reasonable attorney fees to the requester. Unlike federal FOIA and New York FOIL, Florida\'s fee award is mandatory (not discretionary) upon a finding of unlawful refusal. This provides a strong deterrent against bad-faith denials.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'criminal_penalty',
        'param_value': 'misdemeanor_first_degree',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.10(1)',
        'notes': 'Any public officer who violates Florida\'s Public Records Act by unlawfully refusing access to records commits a noncriminal infraction for first offense and a misdemeanor of the first degree for willful violations. Criminal charges for public records violations are rare but possible, particularly for willful and deliberate withholding.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(1)',
        'notes': 'Florida agencies may NOT require a requester to identify themselves or state the purpose of their request. Requiring identification or justification is itself a violation of the Public Records Act. This is one of the broadest access rights in the country — anonymous requests are fully protected.',
    },
    {
        'jurisdiction': 'FL',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Fla. Stat. § 119.07(1)',
        'notes': 'Florida does not require requests to be in writing. Oral requests are valid. However, submitting a written request is strongly advisable for documentation purposes and to ensure a clear record for any subsequent litigation. There is no required form or format for a public records request.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

FL_TEMPLATES = [
    {
        'jurisdiction': 'FL',
        'record_type': 'general',
        'template_name': 'General Florida Public Records Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Chapter 119, Florida Statutes

Dear Public Records Custodian:

Pursuant to the Florida Public Records Act, Chapter 119, Florida Statutes, I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

Please note that under Florida law, I am not required to state my identity or the purpose of this request. Fla. Stat. § 119.07(1).

I request that records be provided in electronic format (PDF or native format) where available, which minimizes cost and delay.

I am willing to pay copying fees up to ${{fee_limit}}. If you estimate fees will exceed this amount, please notify me before proceeding so I may refine my request. Florida law limits copy fees to $0.15 per page for standard copies (§ 119.07(4)(a)).

If any records are withheld in whole or in part, please: (1) identify each record withheld; (2) state the specific statutory exemption under Chapter 119 or other Florida Statute that you claim applies to each withheld record; (3) release all nonexempt portions of any partially exempt records; and (4) confirm that no administrative exemption beyond the cited statute is being applied.

Under Fla. Stat. § 119.07(1)(c), I request a prompt response. If this request requires extensive processing time, please acknowledge receipt and provide an estimated completion date.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that any fees be waived for this request. Although the Florida Public Records Act does not provide a statutory fee waiver, I ask that the agency exercise its discretion to waive or reduce fees because the records I am seeking relate to a matter of significant public interest: {{public_interest_explanation}}.

The standard $0.15/page copy fee cap provides some protection, but a full waiver would best serve the public interest in this case.''',
        'expedited_language': '''I request that this public records request be processed as promptly as possible. Under Florida law, agencies must furnish records "promptly" — Fla. Stat. § 119.07(1)(c). In this case, prompt production is especially important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. A delay beyond this date would {{harm_from_delay}}.

Thank you for your attention to this request.''',
        'notes': 'General-purpose Florida public records template. Florida is requester-friendly: no identification, no written request required, mandatory attorney fees for unlawful refusals, and direct court access. Note correct Florida terminology: "Public Records Custodian" (not Records Access Officer), Chapter 119 (not FOIA).',
    },
    {
        'jurisdiction': 'FL',
        'record_type': 'law_enforcement',
        'template_name': 'Florida Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Custodian
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, Chapter 119, Florida Statutes

Dear Public Records Custodian:

Pursuant to the Florida Public Records Act, Chapter 119, Florida Statutes, I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking information
- Use-of-force reports
- Disciplinary records for the officer(s) involved
- Body-worn camera footage and related metadata
- Dispatch records and CAD logs
- Any written communications related to the above incident

Regarding any claimed exemption under § 119.071(2)(c) (active criminal investigation): this exemption applies only to records of an ACTIVE criminal investigation or prosecution. If any related criminal proceedings have concluded or if no charges were filed, the active-investigation exemption no longer applies. Please provide the status of any related criminal case and release records accordingly.

If any records are withheld, please identify the specific statutory exemption relied upon for each withheld record and release all nonexempt, reasonably segregable portions.

I am willing to pay copying fees up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records relate to {{public_interest_explanation}}, a matter of significant community interest and public accountability. Disclosure will contribute to public understanding of law enforcement activity in this community.''',
        'expedited_language': None,
        'notes': 'Florida law enforcement records template. Includes preemptive language challenging the active-criminal-investigation exemption under § 119.071(2)(c). Body camera footage is public record in Florida unless a specific exemption applies. Note that Florida does not allow agencies to demand identification from requesters.',
    },
    {
        'jurisdiction': 'FL',
        'record_type': 'appeal',
        'template_name': 'Florida Public Records — Circuit Court Petition (Mandamus)',
        'template_text': '''IN THE CIRCUIT COURT OF THE {{judicial_circuit}} JUDICIAL CIRCUIT
IN AND FOR {{county_name}} COUNTY, FLORIDA

{{requester_name}},
    Petitioner,

v.

{{agency_name}}, and
{{custodian_name}}, as Custodian of Public Records,
    Respondents.

Case No.: ________________

PETITION FOR WRIT OF MANDAMUS TO ENFORCE FLORIDA PUBLIC RECORDS ACT

Petitioner {{requester_name}}, pursuant to Florida Rule of Civil Procedure 1.630 and Chapter 119, Florida Statutes, petitions this Court for a writ of mandamus compelling Respondents to produce the following public records, and states:

1. Petitioner is a person entitled to inspect and copy public records under Chapter 119, Florida Statutes.

2. Respondent {{agency_name}} is a public agency within the meaning of § 119.011(2), Florida Statutes, and is therefore subject to the Public Records Act.

3. Respondent {{custodian_name}} is the custodian of public records for {{agency_name}} and is responsible for fulfilling public records requests.

4. On {{original_request_date}}, Petitioner submitted a public records request to Respondents for:
   {{description_of_records}}

5. As of the date of this petition ({{petition_date}}), Respondents have {{description_of_denial_or_delay}}.

6. Respondents' refusal/failure to produce these records violates § 119.07(1)(c), Florida Statutes, which requires agencies to permit inspection and copying of records "promptly."

7. Respondents have no legal basis for withholding the requested records. [If exemption claimed:] Specifically, the claimed exemption under {{claimed_exemption}} does not apply because {{exemption_challenge_arguments}}.

8. Petitioner has no adequate remedy at law other than this extraordinary writ.

9. Under § 119.12, Florida Statutes, this Court is required to award reasonable attorney fees to Petitioner if the Court finds that Respondents unlawfully refused to permit inspection or copying of public records.

WHEREFORE, Petitioner respectfully requests that this Court:

(a) Issue a writ of mandamus compelling Respondents to promptly produce the requested records;
(b) Conduct an in camera review of any withheld records to determine whether any claimed exemption actually applies;
(c) Award Petitioner reasonable attorney fees and costs pursuant to § 119.12, Florida Statutes; and
(d) Grant such other relief as the Court deems just and proper.

Respectfully submitted,

{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}
{{date}}''',
        'fee_waiver_language': None,
        'expedited_language': None,
        'notes': 'Florida has no administrative appeal — requesters must go directly to circuit court. This template is a petition for writ of mandamus under Florida Rule of Civil Procedure 1.630. Courts are required to prioritize public records cases and to award mandatory attorney fees upon a finding of unlawful refusal (§ 119.12). This is a significant strategic advantage — attach this template to demands to signal seriousness.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in FL_EXEMPTIONS:
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

    print(f'FL exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in FL_RULES:
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

    print(f'FL rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in FL_TEMPLATES:
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

    print(f'FL templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'FL total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_fl', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
