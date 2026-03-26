#!/usr/bin/env python3
"""Build Louisiana Public Records Act data: exemptions, rules, and templates.

Covers Louisiana's Public Records Law, La. R.S. 44:1 et seq.
Louisiana has one of the strongest public records laws in the country —
3-business-day response deadline, mandatory written denial with specific
statutory basis, no administrative appeal (direct to district court),
attorney's fees for prevailing requester, civil penalties of $100-$300/day,
and possible criminal penalties for knowing and willful violations. The
state constitution also independently guarantees public access rights.

Run: python3 scripts/build/build_la.py
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
# Louisiana's Public Records Law, La. R.S. 44:1 et seq., establishes a strong
# presumption of public access. La. R.S. 44:31 mandates that all public records
# shall be open. Exemptions are found in La. R.S. 44:1-44:4.1 and throughout
# the Louisiana Revised Statutes. Louisiana's constitution (Art. XII, § 3)
# independently guarantees the right to examine and copy public documents.
# Courts strictly construe exemptions against the agency. The custodian bears
# the burden of proving an exemption applies.
# =============================================================================

LA_EXEMPTIONS = [
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(1)',
        'exemption_number': 'La. R.S. 44:3(A)(1)',
        'short_name': 'Law Enforcement Investigation Records — Active Cases',
        'category': 'law_enforcement',
        'description': 'Records pertaining to the identity of a confidential source of information, records pertaining to pending criminal litigation, and records of law enforcement investigative files compiled for law enforcement purposes are exempt where disclosure would: interfere with pending enforcement proceedings, deprive a person of a fair trial, identify a confidential informant, reveal investigative techniques, or endanger law enforcement personnel.',
        'scope': 'Law enforcement investigation records where disclosure would cause one of the enumerated harms: interference with pending proceedings, fair trial deprivation, confidential informant identification, investigative technique disclosure, or endangerment. The exemption applies only while enforcement proceedings are pending — once final disposition occurs (prosecution concluded, investigation closed), the records become public. Incident reports, arrest records, and booking information documenting the existence and nature of criminal events are public regardless of investigation status. The custodian must identify the specific harm for each withheld record.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'investigative technique', 'pending litigation', 'active investigation',
            'enforcement proceedings', 'criminal record', 'arrest record',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is limited to records of pending litigation and active investigations — completed matters are public',
            'Incident reports and arrest records are public regardless of investigation status',
            'The custodian must show specific, articulable harm from disclosure of each withheld record — categorical denial is insufficient',
            'Once prosecution concludes or investigation is closed, all exemptions under La. R.S. 44:3 expire for those records',
            'Louisiana courts strictly construe the law enforcement exemption against the agency',
            'La. Const. Art. XII, § 3\'s independent constitutional guarantee requires narrow reading of all exemptions',
            'Administrative records, budget, and policy documents of law enforcement agencies are public',
        ]),
        'notes': 'Louisiana\'s law enforcement exemption is strictly construed under both the statute and the constitutional guarantee. Courts have consistently held that the exemption terminates when proceedings conclude. See Lemmon v. Connick, 590 So. 2d 574 (La. 1991). The civil and criminal penalty provisions of La. R.S. 44:35 and 44:36 create strong deterrents against over-claiming this exemption.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(4)',
        'exemption_number': 'La. R.S. 44:3(A)(4)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records that would be protected from civil discovery by the attorney-client privilege or the work product doctrine are exempt from public disclosure under Louisiana\'s Public Records Law.',
        'scope': 'Confidential attorney-client communications made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of litigation. Louisiana\'s privilege tracks the civil discovery standard: communications must be confidential, made for the purpose of legal advice (not policy), and not waived. Government billing records and retainer agreements are generally public. Facts independently known are not protected merely because communicated to an attorney. Louisiana courts apply the privilege narrowly given the strong constitutional public access guarantee.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'litigation',
            'privileged communication', 'attorney work product', 'legal opinion',
            'in anticipation of litigation', 'civil discovery', 'La. R.S. 44:3(A)(4)',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice — not general policy or business guidance',
            'Waiver occurs when the agency uses the advice in public proceedings or discloses it to non-attorneys involved in the matter',
            'Attorney billing records and fee arrangements are generally public',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis',
            'The privilege is narrowly construed under Louisiana\'s strong constitutional public access guarantee',
            'Challenge claims that all correspondence with outside counsel is privileged',
        ]),
        'notes': 'Louisiana recognizes attorney-client privilege for government entities as an exception to the Public Records Law under La. R.S. 44:3(A)(4). The privilege is tied to the civil discovery standard and is narrowly applied consistent with La. Const. Art. XII, § 3. Billing records and routine correspondence are generally public.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(2)',
        'exemption_number': 'La. R.S. 44:3(A)(2)',
        'short_name': 'Personnel Records — Employee Privacy',
        'category': 'privacy',
        'description': 'Personnel records of public employees — specifically medical records, individual financial information, and similar private personal information — may be withheld to protect employee privacy. However, public employment information related to official duties remains public.',
        'scope': 'Personnel records containing private personal information: medical history, home address, personal financial data unrelated to public employment, and similar private data. Information about the exercise of public duties is not exempt: salary, job title, official disciplinary actions, performance evaluations related to public duties, and termination decisions are public. Louisiana courts apply the strong constitutional public access standard to personnel records — the exemption is narrow and applies only to genuinely private personal information unrelated to official duties.',
        'key_terms': json.dumps([
            'personnel records', 'public employee', 'medical record', 'salary',
            'disciplinary record', 'home address', 'employment record',
            'official duty', 'public employment', 'termination',
        ]),
        'counter_arguments': json.dumps([
            'Salary and compensation of public employees are public in Louisiana regardless of personnel file status',
            'Official disciplinary actions are public accountability records, not private information',
            'The constitutional guarantee (La. Const. Art. XII, § 3) requires a narrow reading of the personnel records exemption',
            'Performance evaluations related to official duties are public — only truly private personal information (medical, personal financial) may be withheld',
            'Termination decisions and the official reasons for them are public records of official agency action',
        ]),
        'notes': 'Louisiana\'s constitutional public access guarantee (Art. XII, § 3) requires narrow construction of personnel record exemptions. Courts have held that public employment information — salary, official discipline, job performance — is public. The exemption applies only to private personal information unrelated to the employee\'s public role.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:4.1(B)',
        'exemption_number': 'La. R.S. 44:4.1(B)',
        'short_name': 'Statutory Confidentiality — Cross-Referenced Exemptions',
        'category': 'statutory',
        'description': 'La. R.S. 44:4.1 cross-references dozens of other Louisiana statutes that establish specific confidentiality protections for particular types of records. Records protected by these other statutes are exempt from disclosure under the Public Records Law.',
        'scope': 'La. R.S. 44:4.1(B) lists specific statutes that establish confidentiality for particular record types — including tax records, social services records, certain health records, and other specialized categories. The cross-reference provision means that confidentiality requirements in other parts of the Louisiana Revised Statutes are preserved within the Public Records Law framework. Requesters should check whether a specific exemption claim is based on a cross-referenced statute under § 44:4.1(B) or on the general exemptions in § 44:3.',
        'key_terms': json.dumps([
            'statutory confidentiality', 'cross-referenced statute', 'La. R.S. 44:4.1',
            'specific exemption', 'statutory basis', 'confidential by law',
            'enumerated statute', 'Louisiana Revised Statutes',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific cross-referenced statute — a general claim that records are "confidential by law" is insufficient',
            'Challenge whether the specific statute cited by the agency actually covers the specific records at issue',
            'Cross-referenced confidentiality statutes are strictly construed — they do not expand beyond their specific scope',
            'Many cross-referenced statutes protect specific categories of data, not entire files — segregation and partial disclosure may be required',
        ]),
        'notes': 'La. R.S. 44:4.1(B) is an important cross-reference provision. When an agency claims exemption based on another statute, requesters should obtain and review that specific statute to verify that it actually covers the records at issue. Louisiana courts require agencies to cite the specific cross-referenced statute and demonstrate that the particular records fall within its scope.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(3)',
        'exemption_number': 'La. R.S. 44:3(A)(3)',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information of a proprietary nature submitted by private parties to a public body are exempt from disclosure where the information derives independent economic value from not being generally known and is subject to reasonable measures to maintain its secrecy.',
        'scope': 'Commercial and financial information submitted by private entities that qualifies as a trade secret under Louisiana law — specifically information that: (1) derives independent economic value from not being publicly known; and (2) is subject to reasonable measures to maintain confidentiality. Government-generated records are not trade secrets. Amounts paid with public funds are public regardless of vendor claims. The submitting entity bears the burden of establishing trade secret status — a confidentiality stamp is not sufficient.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'commercial information',
            'financial information', 'independent economic value', 'competitive harm',
            'confidential business information', 'trade secret misappropriation',
        ]),
        'counter_arguments': json.dumps([
            'Amounts paid with public funds are public regardless of vendor trade secret claims',
            'Publicly available information cannot constitute a trade secret',
            'The submitting entity must demonstrate actual trade secret status — not just claim confidentiality',
            'The agency, not the vendor, makes the final disclosure decision — agencies may not simply defer to confidentiality demands',
            'Louisiana\'s constitutional public access guarantee requires narrow reading of the trade secret exemption',
            'Contract terms, deliverables, and performance metrics for public contracts are generally public',
        ]),
        'notes': 'Louisiana\'s trade secret exemption is strictly construed under the Public Records Law\'s strong disclosure mandate. Courts have held that amounts paid with public funds are public and that vendors cannot veto disclosure of public expenditure data. The constitutional guarantee (La. Const. Art. XII, § 3) requires narrow reading of all exemptions.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(5)',
        'exemption_number': 'La. R.S. 44:3(A)(5)',
        'short_name': 'Security Plans and Critical Infrastructure',
        'category': 'safety',
        'description': 'Security plans, vulnerability assessments, and records identifying specific weaknesses in critical infrastructure are exempt from disclosure where disclosure would create a specific and articulable security risk to public safety.',
        'scope': 'Records specifically identifying vulnerabilities in critical public infrastructure — water systems, power grids, transportation networks, and public building security. The exemption requires that disclosure would create a specific, articulable security risk, not merely a speculative or general concern. Budget records and general descriptions of security programs are public. The agency must demonstrate that disclosure of the specific record (not just records of this general type) would enable exploitation of a specific vulnerability.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'infrastructure protection', 'access control',
            'emergency response', 'public safety',
        ]),
        'counter_arguments': json.dumps([
            'The security risk must be specific and articulable — general security concerns are insufficient',
            'Budget and expenditure records for security programs are public',
            'General descriptions of security policies that do not identify specific vulnerabilities are not covered',
            'Challenge claims that entire security department records are exempt',
            'Louisiana\'s strong constitutional guarantee requires the agency to demonstrate specific risk from specific records',
        ]),
        'notes': 'Louisiana\'s security exemption requires specific, articulable risk from specific records. The constitutional public access guarantee further limits the agency\'s ability to claim this exemption on general grounds.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(6)',
        'exemption_number': 'La. R.S. 44:3(A)(6)',
        'short_name': 'Medical and Mental Health Records',
        'category': 'privacy',
        'description': 'Individually identifiable medical and mental health records held by government agencies are exempt from public disclosure under the Public Records Law and specific Louisiana health record statutes.',
        'scope': 'Individually identifiable medical records, mental health treatment records, substance abuse treatment records, and similar health information held by public entities. Specific Louisiana statutes (La. R.S. 40:1165.1 et seq. for mental health; La. R.S. 40:1095 for substance abuse treatment) provide additional protections cross-referenced in § 44:4.1(B). Aggregate health statistics, de-identified data, and public health program information are public. The policies and budget of public health agencies are public.',
        'key_terms': json.dumps([
            'medical record', 'mental health record', 'substance abuse record',
            'patient privacy', 'HIPAA', 'individually identifiable', 'health information',
            'treatment record', 'La. R.S. 40:1165.1',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and de-identified data are not covered',
            'Policies, procedures, and budget records of public health agencies are public',
            'Challenge whether specific records actually contain individually identifiable health information',
            'Information about public health programs (as distinct from individual patient records) is public',
        ]),
        'notes': 'Louisiana\'s medical record exemptions derive from multiple sources: the Public Records Law, specific Louisiana health statutes cross-referenced in § 44:4.1(B), and federal HIPAA for covered entities. The exemption is firmly established for individually identifiable records.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 47:1508',
        'exemption_number': 'La. R.S. 47:1508',
        'short_name': 'Tax Return and Revenue Information',
        'category': 'statutory',
        'description': 'State tax return information and taxpayer data held by the Louisiana Department of Revenue is specifically exempt from public disclosure under La. R.S. 47:1508\'s taxpayer confidentiality provisions, cross-referenced in the Public Records Law.',
        'scope': 'Tax returns, tax application data, audit files, and related taxpayer information submitted to the Louisiana Department of Revenue. Covers state income tax, corporate franchise tax, sales tax, and other state tax filings. Aggregate revenue statistics published by the Department are public. Tax delinquency notices and final court judgments in tax cases are accessible through court records. Information about the Department\'s administrative operations is public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Louisiana Department of Revenue',
            'taxpayer records', 'state tax', 'income tax', 'sales tax',
            'tax confidentiality', 'La. R.S. 47:1508',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics are public',
            'Tax delinquency notices and final court judgments are accessible',
            'Information about the Department\'s enforcement programs is public',
            'Challenge whether specific records are "tax return information" vs. general regulatory correspondence',
        ]),
        'notes': 'Louisiana\'s tax confidentiality under La. R.S. 47:1508 is cross-referenced in § 44:4.1(B). The exemption is well-established for taxpayer-specific data and consistently enforced.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(7)',
        'exemption_number': 'La. R.S. 44:3(A)(7)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Real property appraisals and valuation records prepared for government acquisition or sale of real property are exempt until the transaction is completed or the agency\'s interest in the property is terminated.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuations prepared for the purpose of negotiating acquisition or disposal of real property. The exemption is time-limited and automatically expires when the transaction closes or is abandoned. Post-transaction, all appraisal and valuation records are public. The exemption prevents the agency from being disadvantaged in negotiations but does not create permanent secrecy.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'pre-acquisition', 'real property', 'land purchase', 'condemnation',
            'eminent domain', 'property sale', 'feasibility study',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction closes or is abandoned',
            'Post-transaction appraisals are fully public',
            'Challenge the claim that a transaction is still "pending" if no action has been taken for an extended period',
            'After condemnation proceedings conclude, all valuation records are public',
        ]),
        'notes': 'Louisiana\'s pre-acquisition appraisal exemption under § 44:3(A)(7) is time-limited. It expires automatically upon transaction completion. Post-transaction records are fully subject to the strong disclosure mandate of the Public Records Law.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(8)',
        'exemption_number': 'La. R.S. 44:3(A)(8)',
        'short_name': 'Juvenile Records',
        'category': 'privacy',
        'description': 'Records concerning juvenile proceedings and the identity of juveniles involved in delinquency matters are exempt from public disclosure to protect juvenile privacy and support rehabilitative objectives of the juvenile justice system.',
        'scope': 'Records identifying juveniles involved in delinquency proceedings, juvenile court records, and related records compiled in the context of juvenile justice matters. Adult criminal records are fully public. Records of adult courts handling transferred juvenile cases may be public. Aggregate juvenile justice statistics are public. Records of juvenile victims of crimes may have additional protections under specific statutes.',
        'key_terms': json.dumps([
            'juvenile record', 'juvenile delinquency', 'juvenile court', 'minor',
            'youth offender', 'juvenile justice', 'juvenile proceedings',
            'juvenile identity', 'delinquency record',
        ]),
        'counter_arguments': json.dumps([
            'Adult criminal records are fully public regardless of the defendant\'s prior juvenile history',
            'Aggregate juvenile justice statistics are public',
            'Records of transferred cases handled in adult court may be public',
            'Challenge claims that all records involving anyone who is or was a juvenile are exempt',
        ]),
        'notes': 'Louisiana\'s juvenile records exemption reflects the standard American approach to protecting the privacy of juveniles in the justice system. The exemption is categorical for juvenile proceedings records but does not extend to adult records or aggregate data.',
    },
    {
        'jurisdiction': 'LA',
        'statute_citation': 'La. R.S. 44:3(A)(9)',
        'exemption_number': 'La. R.S. 44:3(A)(9)',
        'short_name': 'Victims of Sex Offenses — Personal Identifying Information',
        'category': 'privacy',
        'description': 'Personal identifying information of victims of sex offenses is exempt from public disclosure in government records to protect victims from harassment and secondary trauma.',
        'scope': 'Personal identifying information of victims of sexual assault, rape, and related sex offenses in government records including law enforcement incident reports, court records, and agency files. The exemption is narrowly tailored to identifiers — name, address, and contact information. The nature and existence of the offense, and information about the investigation and prosecution, are public with victim identifiers redacted.',
        'key_terms': json.dumps([
            'sex offense victim', 'sexual assault victim', 'rape victim',
            'victim privacy', 'victim identity', 'personal identifying information',
            'victim address', 'victim name',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers victim identifiers, not the existence or nature of the crime',
            'Incident reports documenting the offense are public with victim identifiers redacted',
            'Challenge overbroad withholding where offense information is removed along with victim identifiers',
        ]),
        'notes': 'Louisiana\'s sex offense victim privacy exemption is narrowly focused on personal identifiers. Agencies must redact victim names and contact information but must produce the remainder of incident reports and records documenting the offense.',
    },
]

# =============================================================================
# RULES
# Louisiana Public Records Law, La. R.S. 44:1 et seq.
# Key features: 3-business-day response deadline; mandatory written denial
# with specific statutory basis; no administrative appeal; direct district
# court enforcement; attorney's fees for prevailing requester; civil penalties
# $100-$300/day; criminal penalties possible for willful violations;
# $0.25/page for paper; constitutional guarantee independently supports access.
# =============================================================================

LA_RULES = [
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': '3',
        'day_type': 'business',
        'statute_citation': 'La. R.S. 44:32(A)',
        'notes': 'Louisiana requires custodians to make public records available for inspection or copying within 3 business days of a written request. This is one of the shortest mandatory response deadlines in the United States. If the records cannot be produced within 3 business days, the custodian must acknowledge receipt of the request and provide a specific date by which records will be available. Failure to respond within 3 business days — either by producing records or providing written acknowledgment with an estimated date — is itself a Public Records Law violation that can support civil penalties.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_mandatory_with_specific_citation',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:32(D)',
        'notes': 'Louisiana law MANDATES a written denial when a custodian refuses to produce records. The written denial must: (1) state in writing that the request is denied; and (2) cite the specific statute, constitutional provision, or other legal authority justifying the denial. A denial without a specific legal citation is legally deficient. Louisiana courts and commentators have emphasized that this requirement is strictly enforced — custodians who deny access without a written denial with specific statutory basis are independently violating the Public Records Law. The written denial requirement is one of Louisiana\'s strongest procedural protections.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:32(C)(1)',
        'notes': 'Louisiana allows custodians to charge up to $0.25 per page for paper copies of public records. For electronic records, the fee is limited to the actual cost of the electronic medium. Agencies may not charge for staff research time spent locating or reviewing records under the standard copy fee provision. The $0.25/page cap is a statutory maximum — agencies may charge less. For electronic records delivered by email, the actual cost is typically zero.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:32(C)',
        'notes': 'Louisiana does not mandate fee waivers but custodians have discretion to reduce or waive fees. The strong constitutional and statutory public access mandate supports fee waivers for records of significant public interest. For electronic records provided by email, the actual cost is zero — requesters should request electronic delivery to avoid any per-page charge.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:35',
        'notes': 'Louisiana\'s Public Records Law has NO formal administrative appeal mechanism. A requester denied access must go directly to the district court under La. R.S. 44:35. There is no AG opinion process, no ombudsman, and no administrative tribunal. However, the combination of the 3-business-day deadline, mandatory written denial requirement, civil penalties, and attorney\'s fees makes Louisiana\'s direct court enforcement highly effective compared to states with administrative appeals but weaker remedies.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'district_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:35',
        'notes': 'Any person denied access to public records, or whose request is not responded to within the 3-business-day deadline, may bring a civil action in the district court of the parish where the records are located or where the requester resides. The court reviews the denial de novo and may order production, award attorney fees, and impose civil penalties. Louisiana courts have strongly enforced the Public Records Law consistent with the constitutional guarantee. La. R.S. 44:35(E) provides for summary proceedings in urgent cases.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_per_day',
        'param_value': '$100-$300 per day',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:35(E)',
        'notes': 'Louisiana courts may impose civil penalties of $100 to $300 per day for each day a custodian wrongfully denies access to public records after being ordered to produce them by a court. The penalty is distinct from attorney fees and may be awarded in addition to fees. The daily penalty provision is one of Louisiana\'s most powerful enforcement tools — for prolonged withholding, penalties can accumulate to substantial amounts. Courts have the discretion to set the daily rate within the $100-$300 range based on the egregiousness of the violation.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees',
        'param_value': 'mandatory_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:35(D)',
        'notes': 'Louisiana courts SHALL award reasonable attorney fees and litigation costs to a requester who substantially prevails in a Public Records Law enforcement action. The fee award is mandatory, not discretionary — unlike most states where attorney fees in public records cases are discretionary. This mandatory fee-shifting provision, combined with the daily civil penalty, makes Louisiana\'s enforcement regime one of the strongest in the country. The mandatory fee award applies when the requester substantially prevails on any significant portion of the case.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'penalty',
        'param_key': 'criminal_penalty',
        'param_value': 'possible_for_willful_violations',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:36',
        'notes': 'Louisiana\'s Public Records Law includes criminal penalty provisions for willful and knowing violations. Under La. R.S. 44:36, a public official who willfully and knowingly withholds records in violation of the law may be subject to criminal prosecution. Criminal penalties include fines and potential imprisonment. The criminal penalty provision is rarely invoked in practice, but its existence serves as a significant deterrent. Requesters facing egregious, willful denials should note the criminal penalty provision in communications with the agency.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'constitutional_guarantee',
        'param_value': 'La. Const. Art. XII, § 3',
        'day_type': None,
        'statute_citation': 'La. Const. Art. XII, § 3',
        'notes': 'Louisiana\'s constitution independently guarantees the right to examine and copy public documents: "No person shall be denied the right to observe the deliberations of public bodies and examine public documents, except in cases established by law." This constitutional guarantee is self-executing — it operates independently of the statutory Public Records Law. Courts have held that the constitutional guarantee requires narrow construction of all exemptions. When raising a Public Records Law claim, requesters should cite both the statutory rights under La. R.S. 44:1 et seq. AND the constitutional guarantee under Art. XII, § 3.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:31; La. Const. Art. XII, § 3',
        'notes': 'The burden of proving that any exemption applies rests entirely on the custodian. La. R.S. 44:31 establishes a strong presumption that all public records are open. The constitutional guarantee further reinforces this presumption. A custodian claiming an exemption must affirmatively demonstrate that the specific exemption applies to the specific withheld record — general assertions of exemption categories are insufficient. Louisiana courts review Public Records Law decisions de novo and apply no deference to agency determinations.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:32(B)',
        'notes': 'When a record contains both exempt and non-exempt portions, the custodian must allow inspection of the non-exempt portions and may withhold only the specific exempt material. Blanket withholding of documents containing some exempt content is a violation of the Public Records Law. The custodian bears the burden of segregating exempt content and releasing the remainder. Louisiana courts have imposed civil penalties for failure to segregate and release non-exempt portions of partially withheld records.',
    },
    {
        'jurisdiction': 'LA',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'La. R.S. 44:31(B)(2)',
        'notes': 'Louisiana does not require requesters to identify themselves or state the purpose of their public records request. Any person of the age of majority may inspect and copy public records. The right is not limited to Louisiana residents or U.S. citizens — any person may request. Agencies may not require identification as a precondition of access.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

LA_TEMPLATES = [
    {
        'jurisdiction': 'LA',
        'record_type': 'general',
        'template_name': 'General Louisiana Public Records Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Louisiana Public Records Law Request — La. R.S. 44:1 et seq.

Dear Custodian of Public Records:

Pursuant to the Louisiana Public Records Law, La. R.S. 44:1 et seq., and the Louisiana Constitution, Art. XII, § 3, I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. Electronic delivery eliminates per-page copying fees and is consistent with La. R.S. 44:32(C).

For paper copies, I am willing to pay up to $0.25 per page per La. R.S. 44:32(C)(1). If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request. I am not willing to pay for staff research or review time.

Under La. R.S. 44:31, all public records are presumptively open for inspection and copying. The burden of demonstrating any exemption rests on {{agency_name}}. Under La. R.S. 44:32(B), any record containing both exempt and non-exempt portions must be produced with only the specifically exempt portions withheld — the remainder must be made available.

Under La. R.S. 44:32(A), please make records available within 3 business days. If records cannot be produced within 3 days, please provide written acknowledgment of receipt and a specific date by which records will be available.

If any records or portions are denied, La. R.S. 44:32(D) REQUIRES a written denial stating the specific statute, constitutional provision, or legal authority justifying each denial. A denial without a specific legal citation is legally deficient. Please identify each withheld record and cite the specific provision relied upon.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that all fees for this public records request be waived. While Louisiana law does not mandate fee waivers, {{agency_name}} has discretion to reduce or waive fees. A waiver is appropriate because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest and governmental accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. To the extent records are available in electronic form and can be delivered by email, the actual cost of reproduction is zero, making a fee waiver consistent with La. R.S. 44:32(C).

Louisiana\'s constitutional guarantee (Art. XII, § 3) and the strong statutory presumption of access in La. R.S. 44:31 support a fee waiver that removes barriers to public access.''',
        'expedited_language': '''I request that this Public Records Law request be processed within Louisiana\'s 3-business-day deadline under La. R.S. 44:32(A). If records cannot be produced within 3 business days, please provide written acknowledgment with a specific production date as required by La. R.S. 44:32(A).

Prompt production is particularly important here because:
{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Failure to respond within 3 business days will be treated as a denial supporting district court enforcement under La. R.S. 44:35, including civil penalties of $100-$300/day and mandatory attorney fees.''',
        'notes': 'General Louisiana Public Records template. Key features: (1) 3-business-day response deadline (La. R.S. 44:32(A)); (2) mandatory written denial with specific legal citation required (La. R.S. 44:32(D)); (3) constitutional guarantee independently supports access (La. Const. Art. XII, § 3); (4) no administrative appeal — district court enforcement (La. R.S. 44:35); (5) civil penalties $100-$300/day (La. R.S. 44:35(E)); (6) MANDATORY attorney fees for prevailing requester (La. R.S. 44:35(D)); (7) possible criminal penalties for willful violations (La. R.S. 44:36); (8) $0.25/page maximum. Always cite BOTH the statutory and constitutional basis. The explicit threat of civil penalties and criminal prosecution in correspondence is appropriate for Louisiana given its statutory framework.',
    },
    {
        'jurisdiction': 'LA',
        'record_type': 'law_enforcement',
        'template_name': 'Louisiana Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Louisiana Public Records Law Request — Law Enforcement Records, La. R.S. 44:1 et seq.

Dear Custodian of Public Records:

Pursuant to the Louisiana Public Records Law, La. R.S. 44:1 et seq., and the Louisiana Constitution, Art. XII, § 3, I request the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes but is not limited to:
- Incident reports and offense reports
- Arrest reports and booking records (presumptively public under Louisiana law)
- Use-of-force reports and documentation
- Officer disciplinary records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Internal investigation records for this matter

Regarding claimed exemptions under La. R.S. 44:3(A)(1): This exemption applies ONLY to records involving pending criminal litigation and active investigations. For each withheld record, La. R.S. 44:32(D) requires a written denial stating: (1) the specific provision of § 44:3 relied upon; and (2) the specific harm that would result from disclosure of that particular record.

[If matter appears concluded:] If the related criminal matter has been disposed of or no prosecution is pending, please confirm that the pending-litigation rationale under § 44:3(A)(1) no longer applies and produce all relevant records.

Under La. R.S. 44:31 and La. Const. Art. XII, § 3, public records are presumptively public. The burden of demonstrating any exemption rests on {{agency_name}}.

I am willing to pay up to $0.25 per page for paper copies, up to ${{fee_limit}}. Electronic delivery preferred.

Under La. R.S. 44:32(A), please respond within 3 business days. Failure to respond or provide a legally sufficient written denial within that period will be treated as a constructive denial supporting district court enforcement under La. R.S. 44:35, including civil penalties of $100-$300/day and mandatory attorney fees under La. R.S. 44:35(D).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this law enforcement records request. These records concern {{public_interest_explanation}}, a core public accountability matter for government law enforcement conduct. Electronic delivery incurs no reproduction cost. Louisiana\'s constitutional public access guarantee supports a fee waiver.''',
        'expedited_language': '''I request processing within Louisiana\'s mandatory 3-business-day deadline under La. R.S. 44:32(A). These law enforcement records are needed urgently because: {{expedited_justification}}. I need them by {{needed_by_date}}. If records cannot be produced within 3 days, please provide written acknowledgment with a specific production date.''',
        'notes': 'Louisiana law enforcement records template. Key points: (1) La. R.S. 44:3(A)(1) exemption expires when pending litigation concludes — always ask about case disposition; (2) mandatory written denial with specific statutory citation is required under § 44:32(D) — a vague denial is legally deficient; (3) civil penalties $100-$300/day apply for wrongful withholding under § 44:35(E); (4) mandatory attorney fees under § 44:35(D) for prevailing requesters; (5) criminal penalties possible under § 44:36 for willful violations; (6) constitutional guarantee (Art. XII, § 3) independently supports access. Louisiana\'s is one of the strongest enforcement frameworks for law enforcement records in the country.',
    },
    {
        'jurisdiction': 'LA',
        'record_type': 'government_contracts',
        'template_name': 'Louisiana Public Records Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Public Records
{{agency_name}}
{{agency_address}}

Re: Louisiana Public Records Law Request — Government Contracts and Expenditure Records

Dear Custodian of Public Records:

Pursuant to the Louisiana Public Records Law, La. R.S. 44:1 et seq., and the Louisiana Constitution, Art. XII, § 3, I request the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments between {{agency_name}} and {{contractor_vendor_name}} from {{date_range_start}} through {{date_range_end}}
- Invoices, purchase orders, and payment records for the above contracts
- Correspondence relating to contract negotiation, performance, and compliance
- Any audits, performance evaluations, or assessments of the contractor's work

Government expenditure records are among the most clearly public documents under Louisiana law. Records showing how public funds are spent are at the heart of La. Const. Art. XII, § 3's constitutional guarantee of access to public documents. Amounts paid with public funds are public regardless of any vendor trade secret or confidentiality claims.

Any vendor assertion of trade secret status under La. R.S. 44:3(A)(3) must be specifically justified — a "confidential" designation alone is not sufficient. {{agency_name}}, not the vendor, makes the final disclosure determination.

Under La. R.S. 44:32(D), any denial must be in writing and cite the specific legal authority. Under La. R.S. 44:32(B), non-exempt portions of partially withheld records must be released.

I prefer electronic delivery at no charge. For paper copies, I am willing to pay up to $0.25/page, up to ${{fee_limit}} total.

Please respond within 3 business days per La. R.S. 44:32(A).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver for these government contracts and expenditure records. Records of public spending are central to governmental accountability. This request concerns {{public_interest_explanation}}. Electronic delivery is available at no reproduction cost. Louisiana\'s constitutional guarantee and the strong statutory presumption of access support a fee waiver.''',
        'expedited_language': '''I request processing within Louisiana\'s 3-business-day deadline. These government spending records are needed promptly for {{expedited_justification}}. Please contact me immediately with any questions that would allow faster production.''',
        'notes': 'Louisiana government contracts template. Key points: (1) amounts paid with public funds are public regardless of vendor confidentiality claims — this is well established under Louisiana law; (2) the constitutional guarantee (Art. XII, § 3) independently supports disclosure of public expenditure records; (3) mandatory written denial with specific citation required — vendors cannot veto disclosure; (4) civil penalties $100-$300/day and mandatory attorney fees make Louisiana\'s enforcement highly effective for contract records.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in LA_EXEMPTIONS:
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

    print(f'LA exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in LA_RULES:
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

    print(f'LA rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in LA_TEMPLATES:
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

    print(f'LA templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'LA total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_la', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
