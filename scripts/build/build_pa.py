#!/usr/bin/env python3
"""Build Pennsylvania Right-to-Know Law data: exemptions, rules, and templates.

Covers Pennsylvania's Right-to-Know Law (RTKL), 65 P.S. § 67.101 et seq.
Pennsylvania's 2009 RTKL significantly strengthened public access compared to
the prior 1957 law. The law presumes that government records are public and
places the burden on agencies to prove exemption. A distinctive feature is the
Office of Open Records (OOR), an independent state agency that handles appeals
from Commonwealth agencies and provides binding appeal decisions. Appeals from
local agencies go to common pleas court. Attorney's fees are available for
prevailing requesters.

Run: python3 scripts/build/build_pa.py
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
# Pennsylvania Right-to-Know Law, 65 P.S. § 67.101 et seq.
# The RTKL defines "public record" as a record of a Commonwealth or local
# agency, and the statute establishes a presumption that all records are
# public. Section 708 lists the categories of exempt records, and the burden
# of proving exemption is on the agency. The OOR has issued hundreds of
# binding final determinations interpreting these exemptions.
# =============================================================================

PA_EXEMPTIONS = [
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(1)',
        'exemption_number': '65 P.S. § 67.708(b)(1)',
        'short_name': 'Personal Identification Information',
        'category': 'privacy',
        'description': 'A record that contains information regarding an individual\'s personal identification, including Social Security numbers, financial account numbers, driver\'s license numbers, and home addresses, is exempt from disclosure under the RTKL to protect personal privacy.',
        'scope': 'Under § 708(b)(1)(i)-(vi), specific personal identifiers are exempt: SSNs, financial account numbers, driver\'s license numbers, home addresses, personal phone numbers, and personal email addresses of individuals. The exemption is field-specific — agencies must redact the protected identifiers and release the remainder of the record. It does not protect the entire document containing the identifier. Business addresses, work phone numbers, and work email addresses of public employees are not protected by this exemption. The OOR has consistently held that wholesale withholding of records based on a few protected fields is improper.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'financial account number', 'home address',
            'driver\'s license number', 'personal identification', '65 P.S. 67.708(b)(1)',
            'personal phone number', 'personal email', 'PII', 'identity theft',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — agencies must redact only the protected identifiers and release the rest of the record',
            'Business addresses, work phone numbers, and work email of public employees are public under the RTKL',
            'Challenge blanket withholding of entire documents when only specific identifier fields are exempt',
            'The OOR has repeatedly held that wholesale withholding based on personal identifier fields violates the RTKL',
            'Names, positions, and salaries of public employees are not protected by this exemption',
            'Information already in the public domain cannot be withheld under this exemption',
        ]),
        'notes': 'PA\'s personal identification exemption under § 708(b)(1) is field-specific and among the most frequently litigated RTKL provisions. The OOR consistently applies a redact-and-release approach. The exemption covers specific enumerated categories — agencies cannot expand it to cover general "personal" information not listed in § 708(b)(1).',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(17)',
        'exemption_number': '65 P.S. § 67.708(b)(17)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege or the work-product doctrine are exempt from disclosure under the RTKL. The privilege protects confidential communications between agency counsel and the agency made for the purpose of obtaining or providing legal advice.',
        'scope': 'Confidential communications between a government agency and its attorneys made for the purpose of legal advice, and attorney work product prepared in anticipation of litigation. The privilege is narrow: it covers legal advice (not business or policy guidance), requires confidentiality, and can be waived through voluntary disclosure. Billing records and financial arrangements with outside counsel are generally not privileged. Facts independently known by the agency are not protected merely because they were communicated to counsel. The OOR has held that agencies must demonstrate with specificity why each withheld record is privileged.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            '65 P.S. 67.708(b)(17)', 'privileged communication',
            'in anticipation of litigation', 'legal opinion', 'attorney work product',
            'confidential legal communication', 'litigation',
        ]),
        'counter_arguments': json.dumps([
            'Policy advice and business recommendations from attorneys are not privileged — only legal advice qualifies',
            'Waiver occurs when the agency publicly relies on the legal advice or discloses it to third parties',
            'Attorney billing records are generally public — they describe services rendered, not legal advice',
            'Facts underlying legal advice are not privileged — the agency cannot shield factual information by routing it through counsel',
            'The OOR requires record-specific justification for each claimed privilege; general assertions are insufficient',
            'Challenge whether communications to outside counsel who also performed non-legal services are truly privileged',
        ]),
        'notes': 'The OOR has issued numerous final determinations on attorney-client privilege under § 708(b)(17). Pennsylvania courts apply the privilege narrowly given the RTKL\'s presumption of openness. The OOR requires agencies to provide a privilege log with specific justification for each withheld record.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(11)',
        'exemption_number': '65 P.S. § 67.708(b)(11)',
        'short_name': 'Personal Security or Investigations',
        'category': 'law_enforcement',
        'description': 'Records relating to ongoing investigations by a law enforcement agency, records that would reveal the identity of a confidential informant, or records that would endanger the life or safety of a person are exempt from disclosure under the RTKL.',
        'scope': 'Records maintained by law enforcement that would: (1) reveal the identity of a confidential informant; (2) endanger the life or safety of any person; (3) reveal investigative techniques or procedures not generally known; or (4) impede pending criminal litigation. The exemption applies to active investigations and ongoing prosecutions — completed cases generally do not qualify. Factual information in investigative files that does not implicate an enumerated harm must be released. Arrest records, incident reports, and booking information are public even when investigations are ongoing.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'confidential informant', 'ongoing investigation',
            '65 P.S. 67.708(b)(11)', 'investigative technique', 'criminal investigation',
            'pending litigation', 'safety endangerment', 'law enforcement record',
        ]),
        'counter_arguments': json.dumps([
            'The exemption requires a specific articulable harm — generic "law enforcement record" labels are insufficient',
            'Completed investigations and concluded prosecutions do not retain this protection',
            'Arrest records, incident reports, and booking information are public regardless of this exemption',
            'The agency must demonstrate harm specific to each withheld record, not assert a blanket category exemption',
            'Challenge claims that standard, widely known police procedures are "investigative techniques not generally known"',
            'The OOR has consistently required agencies to identify specific harm for each withheld document',
        ]),
        'notes': 'PA\'s law enforcement exemption under § 708(b)(11) is strictly construed by the OOR and Pennsylvania courts. The OOR consistently requires record-specific justification. Once prosecution concludes, the exemption generally does not apply. The burden of proof is on the agency.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(10)(i)',
        'exemption_number': '65 P.S. § 67.708(b)(10)(i)',
        'short_name': 'Predecisional Deliberations',
        'category': 'deliberative',
        'description': 'Internal, predecisional deliberations of Commonwealth and local agencies — including deliberations relating to policy or agency management, including deliberations that occur during a meeting — are exempt from disclosure under the RTKL.',
        'scope': 'Under § 708(b)(10)(i), the deliberative process exemption protects internal, predecisional discussions among agency personnel about policy decisions. The exemption requires that the communication be: (1) internal to the agency; (2) predecisional (before a final agency decision); and (3) deliberative in nature (expressing opinions, recommendations, or policy analysis — not merely factual). Purely factual information within deliberative documents must be segregated and released. Final agency decisions and adopted policies are fully public. The OOR applies the exemption narrowly and frequently requires partial production.',
        'key_terms': json.dumps([
            'predecisional', 'deliberative process', 'internal deliberation',
            '65 P.S. 67.708(b)(10)(i)', 'policy deliberation', 'draft document',
            'agency deliberation', 'intra-agency', 'recommendations', 'working paper',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be segregated and released — only the opinion and recommendation portions are exempt',
            'Once a decision is final and adopted, the predecisional protection ends',
            'Documents circulated outside the agency or used in public proceedings lose their predecisional character',
            'The OOR applies this exemption narrowly and frequently requires partial production',
            '"Working law" — standards the agency actually applies — is not protected even if in internal documents',
            'Challenge claims that entire documents are deliberative when only specific recommendation portions qualify',
        ]),
        'notes': 'The RTKL\'s deliberative process exemption under § 708(b)(10)(i) is analogous to the federal deliberative process privilege but is narrower in Pennsylvania. The OOR consistently requires factual/opinion segregation and partial production. Pennsylvania courts apply the exemption narrowly given the RTKL\'s presumption of openness.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(16)',
        'exemption_number': '65 P.S. § 67.708(b)(16)',
        'short_name': 'Trade Secrets and Proprietary Information',
        'category': 'commercial',
        'description': 'A record that constitutes or reveals a trade secret as defined in the Pennsylvania Uniform Trade Secrets Act (12 Pa. C.S. § 5302) or proprietary information submitted in connection with regulatory compliance is exempt from disclosure under the RTKL.',
        'scope': 'Trade secrets as defined in 12 Pa. C.S. § 5302 (PA\'s UTSA): information that derives independent economic value from not being generally known and is subject to reasonable measures to maintain secrecy. Government-generated records cannot be trade secrets. The agency must independently evaluate vendor trade secret designations. Contract prices, government expenditures, and amounts paid with public funds are generally public even when vendors claim trade secret protection. The OOR has held that vendors cannot unilaterally designate records as trade secrets — the agency must make an independent determination.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', '65 P.S. 67.708(b)(16)',
            'Pennsylvania UTSA', '12 Pa. C.S. 5302', 'competitive harm',
            'commercial information', 'confidential business information',
            'economic value', 'vendor records',
        ]),
        'counter_arguments': json.dumps([
            'Contract prices and amounts paid with public funds are public regardless of vendor trade secret claims',
            'The submitter must demonstrate that information meets the UTSA definition — a "confidential" stamp is insufficient',
            'The agency must independently evaluate trade secret claims and cannot defer to vendor designations',
            'Information required by law to be submitted has reduced secrecy expectations',
            'Publicly available information cannot qualify as a trade secret',
            'Government-generated records and analysis are not trade secrets',
        ]),
        'notes': 'PA\'s trade secret exemption under § 708(b)(16) applies the UTSA framework. The OOR has issued numerous decisions requiring agencies to independently evaluate vendor claims and has frequently found that agencies over-withheld by accepting vendor designations without analysis. Contract amounts are consistently held to be public.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(7)',
        'exemption_number': '65 P.S. § 67.708(b)(7)',
        'short_name': 'Employee Personnel Files',
        'category': 'privacy',
        'description': 'The personal files of agency employees, including performance evaluations, disciplinary records below the level of formal action, and related personnel management documents, are exempt from disclosure to protect employee privacy.',
        'scope': 'Employee personnel files including: performance evaluations, pre-disciplinary counseling records, informal disciplinary actions below the level of formal written reprimand, medical information, and personal contact information. The exemption is bounded — the following are affirmatively public: employee name, current position, salary, and business contact information. Formal disciplinary actions (written reprimands, suspensions, terminations) and final disposition of disciplinary matters are generally public. The OOR applies a careful line between personal employment information and public accountability records.',
        'key_terms': json.dumps([
            'personnel file', 'employee record', 'performance evaluation',
            '65 P.S. 67.708(b)(7)', 'disciplinary record', 'employee privacy',
            'employment record', 'public employee', 'personnel management',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, salary, and business contact of public employees are public',
            'Formal disciplinary actions and their final dispositions are public accountability records, not personal files',
            'Records of employee conduct in their official capacity are public, not personal',
            'Challenge overbroad withholding where the agency treats all employment-related records as personal files',
            'The OOR has held that final dispositions of disciplinary matters are public even if the underlying investigative file is exempt',
        ]),
        'notes': 'The OOR has developed a nuanced body of decisions distinguishing public accountability records (salaries, formal discipline, official conduct) from personal files (evaluations, informal counseling, personal information). The key distinction is between records of official conduct versus records of personal employment management.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(2)',
        'exemption_number': '65 P.S. § 67.708(b)(2)',
        'short_name': 'Personal Health or Financial Information',
        'category': 'privacy',
        'description': 'A record containing a natural person\'s medical, psychiatric, or psychological history or disability status, or containing personal financial information about a specific person, is exempt from disclosure under the RTKL.',
        'scope': 'Individually identifiable health information and personal financial information submitted by private individuals to government agencies. Includes medical diagnoses, treatment records, psychiatric records, disability documentation, and personal tax or financial records. Aggregate health data, program statistics, and anonymized information are not covered. Business financial information submitted by entities (not individuals) is analyzed under the trade secret framework. Government expenditure data and public financial records are never protected by this provision.',
        'key_terms': json.dumps([
            'medical record', 'health information', 'disability status', 'financial information',
            '65 P.S. 67.708(b)(2)', 'personal health', 'psychiatric record',
            'medical history', 'PHI', 'HIPAA', 'personal finance',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health data and program statistics are public — only individually identifiable records are exempt',
            'Government expenditure and financial records are never protected',
            'Business financial information submitted by entities is governed by the trade secret analysis, not this provision',
            'Redaction of identifying information may allow disclosure of the underlying health data',
            'Challenge whether the record is truly about a "natural person" or a business entity',
        ]),
        'notes': 'Pennsylvania\'s personal health and financial information exemption aligns with HIPAA requirements for individually identifiable health information. The OOR applies it narrowly to specific personal records, not broadly to all records held by health-related agencies.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(18)',
        'exemption_number': '65 P.S. § 67.708(b)(18)',
        'short_name': 'Real Property Purchase and Negotiation Records',
        'category': 'commercial',
        'description': 'Records relating to the acquisition or sale of real property by a Commonwealth or local agency, including appraisals and negotiation communications, are exempt from disclosure until the transaction is completed.',
        'scope': 'Real estate appraisals, feasibility studies, and related records prepared by or for a government agency in connection with a prospective real property acquisition or sale. The exemption is time-limited — it applies only until the transaction is complete, cancelled, or abandoned. The exemption prevents disclosure of the agency\'s maximum willingness to pay during active negotiations. Post-transaction, all appraisal and negotiation records are public. General real property records (deeds, assessments, property history) are always public.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property sale',
            '65 P.S. 67.708(b)(18)', 'pre-acquisition', 'real property',
            'property valuation', 'land purchase', 'negotiation records',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned',
            'Challenge the claim that a transaction remains "pending" if there has been no activity for an extended period',
            'Appraisals for property already owned (not in acquisition mode) are not covered',
            'Post-transaction, all appraisal and negotiation records are public',
            'General real property records — deeds, assessments, ownership history — are always public',
        ]),
        'notes': 'Pennsylvania\'s real property exemption under § 708(b)(18) is a standard time-limited exemption designed to protect agency negotiating position. It is narrowly applied and automatically expires on transaction completion.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(20)',
        'exemption_number': '65 P.S. § 67.708(b)(20)',
        'short_name': 'Safety and Security Plans',
        'category': 'safety',
        'description': 'Records relating to safety and security plans, emergency response protocols, or vulnerability assessments for government facilities or critical infrastructure are exempt where disclosure would create a specific and articulable security risk.',
        'scope': 'Operational security plans, vulnerability assessments, and emergency response protocols for government buildings, utilities, and critical infrastructure. The exemption requires a specific security risk — it does not cover all security-related records. Budget records, contracts, and general program descriptions for security are public. The agency must identify the specific harm from disclosing each withheld record. General descriptions of security policies that do not reveal vulnerabilities are not exempt.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'emergency response',
            '65 P.S. 67.708(b)(20)', 'critical infrastructure', 'security risk',
            'facility security', 'access control', 'security protocol',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable, not speculative',
            'Budget and expenditure records for security programs are public',
            'Challenge claims that entire security contracts are exempt when only technical specifications warrant protection',
            'General policy descriptions that do not reveal specific vulnerabilities are public',
            'The agency must demonstrate specific harm from disclosure of each record, not assert a category exemption',
        ]),
        'notes': 'Pennsylvania\'s safety and security exemption under § 708(b)(20) requires specificity. The OOR has consistently rejected blanket security exemptions and required agencies to demonstrate specific, articulable harm from disclosure of each withheld record.',
    },
    {
        'jurisdiction': 'PA',
        'statute_citation': '65 P.S. § 67.708(b)(22)',
        'exemption_number': '65 P.S. § 67.708(b)(22)',
        'short_name': 'Noncriminal Investigative Records',
        'category': 'law_enforcement',
        'description': 'Records of a noncriminal investigation by a Commonwealth or local agency, including records of regulatory investigations, licensing reviews, and civil enforcement actions, where disclosure would: reveal a confidential source, endanger safety, reveal investigative techniques, or compromise the integrity of an ongoing investigation.',
        'scope': 'Records from noncriminal administrative investigations — regulatory enforcement, licensing reviews, professional discipline, civil fraud investigations — where disclosure would cause specific enumerated harm. The exemption requires active investigation — concluded noncriminal investigations generally lose this protection. Factual information that does not implicate an enumerated harm must be released. Final agency findings, orders, and decisions are always public even if the underlying investigative file is partially exempt.',
        'key_terms': json.dumps([
            'noncriminal investigation', 'regulatory investigation', 'licensing review',
            '65 P.S. 67.708(b)(22)', 'civil enforcement', 'professional discipline',
            'ongoing investigation', 'investigative record', 'administrative investigation',
        ]),
        'counter_arguments': json.dumps([
            'Final agency orders, decisions, and findings are always public regardless of this exemption',
            'Concluded investigations do not retain this protection',
            'Specific enumerated harm must be demonstrated for each withheld record',
            'Challenge whether an investigation is truly "ongoing" or effectively concluded',
            'Factual information that does not implicate any enumerated harm must be released',
        ]),
        'notes': 'The OOR has held that the noncriminal investigation exemption under § 708(b)(22) requires active investigation and specific harm. Final agency decisions and orders are never exempt under this provision. The OOR applies the exemption narrowly consistent with the RTKL\'s presumption of openness.',
    },
]

# =============================================================================
# RULES
# Pennsylvania Right-to-Know Law, 65 P.S. § 67.101 et seq.
# Distinctive features: 5-business-day initial response; 30-day extension;
# Office of Open Records (OOR) appeals for Commonwealth agencies (15 business
# days); appeals from local agencies to common pleas; $0.25/page; attorney's
# fees for prevailing requesters; OOR issues binding final determinations.
# =============================================================================

PA_RULES = [
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'initial_response_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': '65 P.S. § 67.901',
        'notes': 'Under § 901, a Commonwealth or local agency must respond to a RTKL request within 5 business days of receipt. "Respond" means either: (1) produce the records; (2) deny the request (stating the reason); or (3) invoke the 30-day extension under § 902. If the agency fails to respond within 5 business days, the request is deemed denied by operation of law (a "deemed denial"). This triggers the requester\'s right to appeal to the OOR (Commonwealth agencies) or common pleas court (local agencies). The 5-business-day clock starts the day after the agency receives the request.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'extension',
        'param_key': 'maximum_extension_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': '65 P.S. § 67.902',
        'notes': 'Under § 902, an agency may extend the response deadline by up to 30 calendar days if: (1) the request requires redaction of a record; (2) the request requires the retrieval of records stored off-site; (3) a timely response requires extraordinary use of agency resources; (4) the agency has a need to consult with another agency; (5) the agency and requester are discussing narrowing the request; or (6) the request requires the agency to compile data. The agency must notify the requester within the initial 5-business-day period that it is invoking the extension and state the reason. The extension notification must specify one of the § 902 grounds.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'deemed_denial_trigger',
        'param_value': 'failure_to_respond_in_5_business_days',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.901',
        'notes': 'If a Commonwealth or local agency fails to respond to a RTKL request within 5 business days (or within the extended period under § 902), the request is deemed denied. A deemed denial has the same legal effect as an explicit denial — it triggers the requester\'s right to appeal to the OOR (for Commonwealth agencies) or to common pleas court (for local agencies). Requesters should track the 5-business-day deadline and file an appeal promptly after a deemed denial to avoid procedural complications.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.1307; 37 Pa. Code § 93.2',
        'notes': 'Pennsylvania agencies may charge $0.25 per page for black-and-white paper copies. The OOR has set this rate by regulation. Agencies may not charge for: staff time spent searching for or reviewing records; redaction time; attorney review time; or overhead costs. Electronic records may be charged at the cost of the storage medium (often zero for email delivery). Agencies may require pre-payment of fees for large requests. Fees may not be used as a barrier to access.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_discretionary',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.1307',
        'notes': 'Pennsylvania\'s RTKL does not provide a statutory right to fee waiver for any requester category. Agencies may waive fees at their discretion, and many agencies do so for journalists, nonprofits, and academic researchers. Requesters can argue that fee waivers are appropriate when the request serves the public interest. For electronic records delivered by email, the actual cost is often zero, making fee waiver arguments less necessary.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'appeal_deadline',
        'param_key': 'oor_appeal_deadline_days',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': '65 P.S. § 67.1101(a)',
        'notes': 'A requester may appeal a denial (or deemed denial) by a Commonwealth agency to the Office of Open Records (OOR) within 15 business days of the denial or deemed denial. The appeal must be submitted to the OOR in writing, include a copy of the request and denial (if written), and state the grounds for appeal. The OOR is an independent executive agency with binding appellate authority over Commonwealth agency RTKL decisions. Note: this 15-business-day deadline applies to Commonwealth agencies — appeals from local agency denials go to common pleas court.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'appeal_deadline',
        'param_key': 'oor_determination_deadline_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': '65 P.S. § 67.1102',
        'notes': 'The OOR must issue a final determination on an appeal within 30 calendar days of receiving the appeal. The OOR may issue a written final determination granting or denying access, ordering production with redactions, or dismissing the appeal. OOR final determinations are binding on Commonwealth agencies. Either party may appeal an OOR determination to the Commonwealth Court within 30 days. OOR final determinations are publicly available on the OOR website and constitute a body of persuasive precedent on RTKL interpretation.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'appeal_deadline',
        'param_key': 'local_agency_appeal_common_pleas',
        'param_value': 'direct_court_appeal',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.1301(a)',
        'notes': 'Appeals from local agency (county, city, township, school district, etc.) RTKL denials are filed directly in the court of common pleas, NOT with the OOR. The appeal must be filed within 30 calendar days of the denial or deemed denial. Common pleas court reviews the denial de novo. This is a significant structural difference from Commonwealth agency appeals — there is no OOR appeal tier for local agencies. Some counties have developed their own RTKL appeal practices.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'commonwealth_court_appeal_deadline_days',
        'param_value': '30',
        'day_type': 'calendar',
        'statute_citation': '65 P.S. § 67.1301(a)',
        'notes': 'Either party may appeal an OOR final determination to the Commonwealth Court within 30 calendar days of the OOR\'s determination. Commonwealth Court applies a de novo standard of review to RTKL appeals. Parties may also appeal common pleas decisions to the Commonwealth Court in the normal course. The Pennsylvania Supreme Court may accept further review of significant RTKL questions.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'discretionary_for_prevailing_requester',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.1304',
        'notes': 'Under § 1304, if a requester substantially prevails in a RTKL appeal or litigation, the court or OOR may award reasonable attorney fees, expert witness fees, and costs. Unlike Ohio\'s mandatory fee provision, Pennsylvania\'s fee award is discretionary — the court considers factors including the public benefit from the records, the conduct of the agency, and whether the agency had a reasonable basis for its position. A pattern of bad-faith withholding or a clearly meritless denial supports a fee award. The availability of fees provides meaningful deterrence against unjustified denials.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.708(a)',
        'notes': 'Under § 708(a), the burden of proving that a record is exempt from disclosure under the RTKL rests on the agency. The RTKL creates a presumption that all records are public, and the agency must affirmatively demonstrate that each withheld record falls within a specific statutory exception. The agency must provide record-specific justification — general assertions of exemption categories are insufficient. The OOR consistently enforces this burden-shifting framework.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'written_request_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.703',
        'notes': 'Pennsylvania\'s RTKL requires that public records requests be submitted in writing. Oral requests are not RTKL requests. Written requests may be submitted by hand delivery, mail, email, or fax. The agency must designate an Open Records Officer to receive RTKL requests. Requesters should address their written requests to the agency\'s Open Records Officer. The requester need not state a reason for the request or provide identifying information beyond what is necessary for the agency to respond and return records.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.706',
        'notes': 'Under § 706, an agency must redact exempt information from a record and provide the remainder of the record if the exempt and nonexempt portions are reasonably separable. The agency may not withhold an entire record merely because some portion of it is exempt. The OOR consistently applies this segregability requirement and frequently orders partial production where agencies have over-withheld. Redactions must be specifically identified and justified.',
    },
    {
        'jurisdiction': 'PA',
        'rule_type': 'initial_response',
        'param_key': 'denial_must_cite_specific_exception',
        'param_value': 'required',
        'day_type': None,
        'statute_citation': '65 P.S. § 67.903',
        'notes': 'Under § 903, a denial of a RTKL request must specify the grounds for the denial, including the specific provision of § 708 upon which the agency relies. A denial that cites only a general category (e.g., "personnel matters") without identifying the specific § 708 subsection is procedurally deficient. The OOR has held that procedurally deficient denials may be grounds for reversal. Requesters should challenge denials that fail to cite specific statutory provisions.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

PA_TEMPLATES = [
    {
        'jurisdiction': 'PA',
        'record_type': 'general',
        'template_name': 'General Pennsylvania Right-to-Know Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — 65 P.S. § 67.101 et seq.

Dear Open Records Officer:

Pursuant to the Pennsylvania Right-to-Know Law, 65 P.S. § 67.101 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records, I provide the following additional information:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes reproduction costs. If electronic production is not feasible, I request paper copies.

I am willing to pay the actual cost of reproducing records per 65 P.S. § 67.1307 (up to $0.25 per page for paper copies). I am not willing to pay charges for staff time spent searching for or reviewing records, which is not a permissible fee under the RTKL. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under 65 P.S. § 67.708(a), the burden of demonstrating that any record falls within a statutory exception rests on the agency. Under 65 P.S. § 67.706, the agency must release all nonexempt, reasonably segregable portions of any record where only part qualifies for an exception.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) cite the specific statutory exception under 65 P.S. § 67.708 (specific subsection required per 65 P.S. § 67.903); (3) explain how the specific exception applies to each record; and (4) confirm that all nonexempt, segregable portions of partially withheld records have been released.

Under 65 P.S. § 67.901, please respond within 5 business days of receipt. If an extension is required under 65 P.S. § 67.902, please notify me within the initial 5-business-day period with the specific ground for the extension.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Pennsylvania\'s Right-to-Know Law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically via email or download link, the actual cost of reproduction is zero, making a fee waiver consistent with the spirit of the RTKL.''',
        'expedited_language': '''I request that this RTKL request be processed as expeditiously as possible. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Please contact me immediately at {{requester_email}} or {{requester_phone}} if there are any questions.''',
        'notes': 'General Pennsylvania RTKL template. Key features: (1) 5-business-day response deadline with 30-day extension option — cite § 67.901 and § 67.902; (2) failure to respond = deemed denial, triggering OOR appeal right; (3) OOR appeals for Commonwealth agencies within 15 business days — OOR issues binding determinations; (4) local agency appeals go to common pleas (NOT OOR); (5) discretionary attorney fees under § 67.1304; (6) burden of proof on agency under § 67.708(a); (7) written request required under § 67.703. The denial must cite specific § 708 subsection — challenge procedurally deficient denials.',
    },
    {
        'jurisdiction': 'PA',
        'record_type': 'law_enforcement',
        'template_name': 'Pennsylvania Right-to-Know Law Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — Law Enforcement Records, 65 P.S. § 67.101 et seq.

Dear Open Records Officer:

Pursuant to the Pennsylvania Right-to-Know Law, 65 P.S. § 67.101 et seq., I request copies of the following law enforcement records:

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
- Written communications relating to the above incident

Regarding the criminal investigation exemption under 65 P.S. § 67.708(b)(11): Pennsylvania law does not permit blanket withholding of law enforcement records. Any withholding must identify: (1) the specific harm — confidential informant identity, safety endangerment, investigative technique, or impeded ongoing prosecution; and (2) how disclosure of each specific record would cause that specific harm.

[If matter appears concluded:] If no criminal prosecution is currently pending, the interference-with-prosecution rationale under § 708(b)(11) does not apply to this matter.

Under 65 P.S. § 67.708(a), the burden of demonstrating that any record qualifies for an exception rests on the agency. Under 65 P.S. § 67.706, all nonexempt, segregable portions of partially withheld records must be released.

Please respond within 5 business days per 65 P.S. § 67.901.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern {{public_interest_explanation}}, a matter of public accountability. Electronic delivery incurs zero cost. A fee waiver is consistent with the RTKL\'s public access goals.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Pennsylvania law enforcement records template. Key points: (1) § 708(b)(11) requires specific harm identification — no blanket law enforcement exemptions; (2) completed investigations lose this protection; (3) arrest records and incident reports are generally public; (4) OOR appeal for Pennsylvania State Police and other Commonwealth law enforcement within 15 business days of denial; (5) local police department denials appealed to common pleas within 30 days; (6) discretionary attorney fees under § 67.1304.',
    },
    {
        'jurisdiction': 'PA',
        'record_type': 'financial',
        'template_name': 'Pennsylvania Right-to-Know Law Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Open Records Officer
{{agency_name}}
{{agency_address}}

Re: Right-to-Know Law Request — Contracts and Expenditure Records, 65 P.S. § 67.101 et seq.

Dear Open Records Officer:

Pursuant to the Pennsylvania Right-to-Know Law, 65 P.S. § 67.101 et seq., I request copies of the following records relating to government contracts and expenditures:

{{description_of_records}}

Contractor/vendor (if applicable): {{contractor_name}}
Contract period: {{date_range_start}} through {{date_range_end}}
Contract number (if known): {{contract_number}}

This request includes, but is not limited to:
- Executed contracts and all amendments/modifications
- Bid and proposal documents, including all submitted bids/proposals
- Invoices, payment records, and vouchers
- Performance evaluations and compliance records
- Correspondence between the agency and contractor

Regarding trade secret claims under 65 P.S. § 67.708(b)(16): Contract prices, amounts paid with public funds, and total government expenditures are public regardless of vendor trade secret designations. The agency must independently evaluate any trade secret claims under 12 Pa. C.S. § 5302 — it cannot simply defer to contractor designations. Per OOR precedent, vendors cannot unilaterally designate records as trade secrets.

Under 65 P.S. § 67.708(a), the burden of demonstrating that any record qualifies for an exception rests on the agency. Under 65 P.S. § 67.706, all nonexempt, segregable portions of partially withheld records must be released.

Please respond within 5 business days per 65 P.S. § 67.901.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived for this request. These records concern the expenditure of public funds — a core purpose of the Right-to-Know Law. Electronic delivery incurs zero cost. A fee waiver would advance the RTKL\'s transparency goals.''',
        'expedited_language': '''I request expedited processing because {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Pennsylvania government contracts template. Key points: (1) contract prices and public expenditures are always public; (2) OOR has extensive precedent requiring independent agency analysis of trade secret claims; (3) agencies cannot defer to vendor designations; (4) this template is useful for procurement transparency and government accountability research; (5) OOR appeal available for Commonwealth agencies within 15 business days.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in PA_EXEMPTIONS:
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

    print(f'PA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in PA_RULES:
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

    print(f'PA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in PA_TEMPLATES:
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

    print(f'PA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'PA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_pa', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
