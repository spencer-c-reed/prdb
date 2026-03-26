#!/usr/bin/env python3
"""Build District of Columbia Freedom of Information Act data: exemptions, rules, and templates.

Covers DC's Freedom of Information Act, D.C. Code § 2-531 et seq.
DC FOIA provides a 15-business-day response deadline with a 10-business-day
extension. Unique among US jurisdictions: appeal goes to the Mayor (via the
Office of Open Government), then to DC Superior Court. DC is also unique in
having civil penalties ($100-$200/day) for wrongful withholding and having
the DC Office of Open Government as an oversight body. Attorney's fees available
for prevailing requesters. Fee schedule: $0.25/page for paper copies.

Run: python3 scripts/build/build_dc.py
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
# DC FOIA, D.C. Code § 2-534, lists nine numbered exemptions roughly parallel
# to the federal FOIA exemptions. DC courts apply a presumption of openness
# (D.C. Code § 2-532) and require agencies to justify withholding with
# specificity. The Office of Open Government provides guidance and can issue
# non-binding recommendations. Civil penalties ($100-$200/day) are available
# for wrongful withholding — a distinctive enforcement tool.
# =============================================================================

DC_EXEMPTIONS = [
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(1)',
        'exemption_number': 'D.C. Code § 2-534(a)(1)',
        'short_name': 'Exemptions Required by Statute',
        'category': 'statutory',
        'description': 'Information specifically exempted from disclosure by statute (other than the DC FOIA itself) is exempt, provided the statute leaves no discretion on the issue or establishes particular criteria for withholding or refers to particular types of matters to be withheld.',
        'scope': 'Information independently made confidential or exempt by a specific DC or federal statute other than DC FOIA, where that statute either: (1) requires withholding on its face; (2) establishes specific criteria for withholding; or (3) identifies particular types of matters to be withheld. Common examples in DC law include: grand jury records, certain court records, tax return information (D.C. Code § 47-1805.04), and records protected under federal law applied in DC. The agency must identify the specific other statute — a general claim of confidentiality without citation is insufficient. Agency-level regulations that require confidentiality but are not grounded in statute do not qualify.',
        'key_terms': json.dumps([
            'statutory exemption', 'exempted by statute', 'required by law',
            'tax records', 'grand jury', 'statutory confidentiality',
            'D.C. Code § 47-1805.04', 'federal statute', 'statutory mandate',
        ]),
        'counter_arguments': json.dumps([
            'The agency must cite the specific statute — a general claim of confidentiality is insufficient',
            'Agency regulations without statutory grounding do not trigger this exemption',
            'The cited statute must actually require or authorize withholding of the specific type of record at issue',
            'Challenge whether the other statute\'s confidentiality provision was intended to cover the specific context',
            'Even where another statute applies, only the specific protected fields or categories need be withheld — the remainder must be released',
            'The existence of a discretionary authority to withhold does not satisfy this exemption — the statute must leave no discretion or establish specific criteria',
        ]),
        'notes': 'D.C. Code § 2-534(a)(1) mirrors the federal FOIA Exemption 3 framework. DC courts and the Office of Open Government require agencies to identify the specific other statute with precision. The distinction between mandatory and discretionary withholding is important — only mandatory statutory withholding or statutes establishing specific criteria qualify.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(2)',
        'exemption_number': 'D.C. Code § 2-534(a)(2)',
        'short_name': 'Internal Personnel Rules and Practices',
        'category': 'deliberative',
        'description': 'Information related solely to the internal personnel rules and practices of a public body is exempt from disclosure — paralleling federal FOIA Exemption 2.',
        'scope': 'Records related solely to the internal personnel rules and practices of a DC agency — internal staff guidance, personnel manuals, internal procedural rules that apply only to the agency\'s own employees, and similar purely internal operational documents with no public impact. The exemption is narrow: it covers internal staff management documents, not records about how the agency administers its public functions. External-facing policies, rules governing how the agency interacts with the public, and decisions affecting persons outside the agency are not covered. DC courts have applied this exemption narrowly.',
        'key_terms': json.dumps([
            'internal personnel rules', 'internal practices', 'staff guidance',
            'personnel manual', 'internal procedures', 'staff management',
            'internal policy', 'agency operations', 'human resources',
        ]),
        'counter_arguments': json.dumps([
            'The exemption covers only records "related solely" to internal personnel matters — mixed-purpose records are not covered',
            'External-facing policies and procedures that affect public interactions are not covered by this exemption',
            'Challenge claims that procedural guides for agency adjudications or public-facing services are "internal" personnel rules',
            'Records about disciplinary actions against specific employees are generally public once action is final',
            'The exemption does not cover how the agency performs its public functions — only its internal human resources matters',
        ]),
        'notes': 'D.C. Code § 2-534(a)(2) parallels federal FOIA Exemption 2 but DC courts have applied it narrowly. The "solely" qualifier is important — records that mix internal personnel matters with public-function guidance do not qualify for this exemption in DC.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(3)',
        'exemption_number': 'D.C. Code § 2-534(a)(3)',
        'short_name': 'Trade Secrets and Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and commercial or financial information obtained from a person or business where: (a) the information is privileged or confidential; and (b) disclosure would cause substantial harm to the competitive position of the submitter.',
        'scope': 'Information submitted by private parties to DC agencies that: (1) constitutes a trade secret or privileged/confidential commercial or financial information; and (2) whose disclosure would cause substantial competitive harm to the submitter. The agency must independently evaluate whether the information qualifies — submitter self-designations are not controlling. Government expenditures, contract prices, and amounts paid with DC public funds are generally public regardless of trade secret claims. DC courts require that competitive harm be substantial and specific, not speculative.',
        'key_terms': json.dumps([
            'trade secret', 'commercial information', 'competitive harm', 'financial information',
            'proprietary information', 'confidential business information', 'competitive advantage',
            'economic value', 'secrecy', 'substantial harm',
        ]),
        'counter_arguments': json.dumps([
            'The competitive harm must be "substantial" — speculative or de minimis harm is insufficient',
            'The submitter must establish that the information meets the trade secret or confidential commercial information definition',
            'Publicly available information cannot be withheld regardless of submitter characterization',
            'Contract prices and amounts paid with public funds are generally public',
            'The agency must conduct an independent analysis — it cannot simply defer to submitter designations',
            'Challenge whether the submitter maintained reasonable secrecy measures',
            'Government analysis and reports based on submitted data are public even if underlying submitted data might be exempt',
        ]),
        'notes': 'D.C. Code § 2-534(a)(3) parallels federal FOIA Exemption 4. DC courts apply the "substantial competitive harm" standard. The Office of Open Government has issued guidance that contract prices and government expenditures are public regardless of vendor trade secret claims.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(4)',
        'exemption_number': 'D.C. Code § 2-534(a)(4)',
        'short_name': 'Interagency and Intra-Agency Memorandums — Deliberative Process',
        'category': 'deliberative',
        'description': 'Interagency or intra-agency memorandums or letters that would not be available by law to a party other than an agency in litigation with the agency are exempt. This protects predecisional deliberative communications.',
        'scope': 'Interagency and intra-agency memorandums and letters that are predecisional and deliberative — they would not be discoverable by a private party litigating against the agency (i.e., they are covered by the deliberative process privilege in litigation). Covers working drafts, internal policy recommendations, and opinion-based communications prior to final agency decision. Does NOT cover: (1) purely factual material, even if embedded in deliberative documents; (2) adopted agency policy; (3) "working law" — the criteria agencies actually apply in decisions; or (4) records that have been disclosed publicly. Factual portions must be segregated and released.',
        'key_terms': json.dumps([
            'interagency memorandum', 'intra-agency memorandum', 'deliberative process',
            'predecisional', 'working draft', 'internal policy', 'recommendation',
            'deliberative privilege', 'working law', 'policy deliberation',
        ]),
        'counter_arguments': json.dumps([
            'Purely factual material within deliberative documents must be released — the exemption covers only opinion and recommendation portions',
            'Once adopted as agency policy or released publicly, documents are no longer predecisional',
            '"Working law" — the standards and criteria agencies actually apply in decisions — must be disclosed',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'Documents shared with parties outside the agency may lose their predecisional character',
            'The exemption requires the document would be withheld in litigation — if it would be discoverable in civil litigation against DC, it is not exempt here',
            'DC courts apply the deliberative process exemption narrowly, consistent with the presumption of openness',
        ]),
        'notes': 'D.C. Code § 2-534(a)(4) mirrors federal FOIA Exemption 5. DC courts apply the same deliberative process framework developed in federal FOIA case law but are mindful of DC\'s strong presumption of openness under D.C. Code § 2-532. The Office of Open Government has issued guidance emphasizing the factual/opinion distinction.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(5)',
        'exemption_number': 'D.C. Code § 2-534(a)(5)',
        'short_name': 'Investigatory Records — Privacy and Enforcement',
        'category': 'law_enforcement',
        'description': 'Investigatory records compiled for law enforcement purposes, but only to the extent that production would: (A) interfere with enforcement proceedings; (B) deprive a person of a right to a fair trial; (C) constitute an unwarranted invasion of personal privacy; (D) disclose the identity of a confidential source; (E) disclose investigative techniques; or (F) endanger the life or physical safety of any person.',
        'scope': 'Records compiled for law enforcement purposes where disclosure would cause a specific enumerated harm. The six enumerated harms must be demonstrated specifically for each withheld record — blanket assertions are insufficient. The exemption is not permanent: completed investigation files are generally public once prosecution concludes or investigation is closed. Arrest records, incident reports documenting the existence of events, and factual portions of investigative files that do not implicate an enumerated harm must be segregated and released. DC courts and the Office of Open Government require record-by-record justification.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'investigatory records', 'enforcement proceedings',
            'fair trial', 'personal privacy', 'confidential informant', 'investigative technique',
            'endangerment', 'active investigation', 'closed investigation',
        ]),
        'counter_arguments': json.dumps([
            'The agency must demonstrate a specific enumerated harm for each withheld record — "investigatory records" as a category is not sufficient',
            'Concluded investigation records are public once prosecution is complete or investigation is closed',
            'Arrest records, booking information, and incident reports are generally public regardless of investigation status',
            'Factual portions of investigative records that do not implicate an enumerated harm must be released',
            'Challenge "fair trial" claims when no trial is pending or reasonably anticipated',
            'The "privacy" sub-exemption requires an unwarranted invasion — not merely any privacy interest',
            'DC courts require record-by-record justification for investigatory record withholding',
        ]),
        'notes': 'D.C. Code § 2-534(a)(5) parallels federal FOIA Exemption 7. DC courts apply it narrowly, requiring specific demonstration of harm for each withheld record. The Office of Open Government has issued opinions emphasizing that concluded investigation files are public and that incident reports and arrest records are not shielded by this exemption.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(6)',
        'exemption_number': 'D.C. Code § 2-534(a)(6)',
        'short_name': 'Personnel and Medical Files — Privacy',
        'category': 'privacy',
        'description': 'Personnel and medical files and similar files whose disclosure would constitute a clearly unwarranted invasion of personal privacy are exempt. Salary, job title, and employment status of DC government employees are generally public.',
        'scope': 'Personnel files, medical files, and similar files containing personal information whose disclosure would constitute a "clearly unwarranted invasion of personal privacy." The standard requires actual balancing — not every personnel or medical record is automatically exempt. Generally protected: Social Security numbers, home addresses, home telephone numbers, medical information, and evaluations whose disclosure would not advance a legitimate public interest. Generally public: salary, job title, position, dates of employment, and disciplinary actions that resulted in formal employment decisions. DC courts emphasize public accountability for government employees and require significant privacy interest to justify withholding.',
        'key_terms': json.dumps([
            'personnel file', 'medical file', 'personal privacy', 'clearly unwarranted',
            'invasion of privacy', 'public employee', 'salary', 'disciplinary record',
            'home address', 'Social Security number', 'employment record',
        ]),
        'counter_arguments': json.dumps([
            'The standard is "clearly unwarranted" invasion — not merely any privacy interest; the agency must demonstrate a substantial privacy harm',
            'Salary, job title, and dates of employment for DC government employees are public',
            'Disciplinary records and their outcomes are generally public once the action is final',
            'The exemption requires case-by-case balancing — it is not a categorical shield for all personnel records',
            'Challenge overbroad claims that entire personnel files are exempt when only specific fields (SSN, home address, medical info) warrant protection',
            'DC courts apply an accountability principle: public employees have reduced privacy expectations regarding their job performance',
        ]),
        'notes': 'D.C. Code § 2-534(a)(6) parallels federal FOIA Exemption 6. DC courts apply the "clearly unwarranted invasion" standard rigorously, consistent with the accountability principle for government employees. The Office of Open Government has issued opinions confirming that DC employee compensation and disciplinary outcomes are public.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(7)',
        'exemption_number': 'D.C. Code § 2-534(a)(7)',
        'short_name': 'Specific Exemptions Under DC Law',
        'category': 'statutory',
        'description': 'Information specifically exempted from public disclosure by any provision of DC law other than the FOIA itself, including attorney-client privilege, executive privilege, and other recognized common-law and statutory privileges.',
        'scope': 'Records protected by common-law or statutory privileges recognized in DC law, including attorney-client privilege, attorney work product, and executive privilege. The attorney-client privilege applies to confidential communications between DC agencies and their attorneys made for the purpose of obtaining legal advice. Work product applies to documents prepared in anticipation of litigation. Executive privilege may apply to certain high-level deliberative communications, though DC courts apply it narrowly. Billing records, retainer agreements, and general financial arrangements with outside counsel are not privileged.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'executive privilege',
            'legal advice', 'litigation', 'privileged communication',
            'common-law privilege', 'legal opinion', 'in anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'The attorney-client privilege applies only to communications for legal advice — not policy or administrative guidance',
            'Waiver occurs through disclosure to third parties outside the legal matter',
            'Attorney billing records and invoices are generally public',
            'Facts underlying legal advice are not privileged — only the attorney\'s analysis',
            'Executive privilege is narrow in DC and does not cover routine agency deliberations',
            'Challenge whether the agency constructively waived by relying on legal advice in public decision-making',
        ]),
        'notes': 'D.C. Code § 2-534(a)(7) is a residual exemption covering other recognized DC privileges. The attorney-client and work product protections are most commonly invoked under this provision. DC courts apply these privileges narrowly given the strong disclosure presumption in D.C. Code § 2-532.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(8)',
        'exemption_number': 'D.C. Code § 2-534(a)(8)',
        'short_name': 'Security Plans and Infrastructure',
        'category': 'safety',
        'description': 'Information that would disclose techniques and procedures for law enforcement investigations or prosecutions, or would disclose guidelines for law enforcement investigations or prosecutions if such disclosure could reasonably be expected to risk circumvention of the law, is exempt. Also covers security plans for public facilities.',
        'scope': 'Security plans, vulnerability assessments, and related records for DC government facilities and critical infrastructure where disclosure would create a specific security risk. Also covers law enforcement investigative guidelines and techniques whose disclosure could enable circumvention of enforcement. Budget records, contract pricing, and expenditure data for security programs are generally public. General security policies that do not reveal specific vulnerabilities or enable circumvention are not covered.',
        'key_terms': json.dumps([
            'security plan', 'law enforcement guidelines', 'investigative techniques',
            'circumvention of law', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'enforcement guidelines', 'public safety',
        ]),
        'counter_arguments': json.dumps([
            'The risk of circumvention must be specific and reasonable, not speculative',
            'General security policies and publicly known procedures are not covered',
            'Budget and expenditure records for security and law enforcement programs are public',
            'Challenge claims that entire security contracts are exempt when only specific technical details might warrant protection',
            'Law enforcement guidelines that primarily describe administrative procedures — not investigative techniques — are not covered',
        ]),
        'notes': 'D.C. Code § 2-534(a)(8) covers both law enforcement technique protection and physical security for DC facilities. DC courts require agencies to demonstrate a reasonable risk of specific harm, not merely assert that records touch on security or law enforcement.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(9)',
        'exemption_number': 'D.C. Code § 2-534(a)(9)',
        'short_name': 'Real Estate Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Appraisals and other real property valuation documents prepared by or for a DC agency in connection with the acquisition of property are exempt until the transaction is complete or abandoned.',
        'scope': 'Real estate appraisals, feasibility studies, and property valuation documents prepared in connection with DC government acquisition or disposition of real property. The exemption protects the government\'s negotiating position by keeping its maximum willingness to pay confidential during negotiations. It is strictly time-limited — upon completion, cancellation, or abandonment of the transaction, all appraisal records become public. Does not cover appraisals for property already owned by DC when no acquisition or sale is contemplated.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property appraisal', 'property acquisition',
            'property valuation', 'pre-acquisition', 'real property', 'condemnation',
            'land purchase', 'property disposition',
        ]),
        'counter_arguments': json.dumps([
            'The exemption expires when the transaction is complete, cancelled, or abandoned — all appraisal records are then public',
            'Challenge claims that a transaction remains "pending" with no recent activity',
            'Appraisals for property already owned by DC are not covered',
            'Post-transaction, all valuation records including internal analyses are public',
        ]),
        'notes': 'D.C. Code § 2-534(a)(9) is DC\'s standard pre-acquisition appraisal exemption. It terminates automatically upon completion or abandonment of the transaction. Post-transaction, all records including internal valuations are public. The Office of Open Government has confirmed this time-limited nature in guidance.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 47-1805.04; D.C. Code § 2-534(a)(1)',
        'exemption_number': 'D.C. Code § 47-1805.04',
        'short_name': 'DC Tax Return Information',
        'category': 'statutory',
        'description': 'DC tax return information submitted to the Office of Tax and Revenue is confidential under D.C. Code § 47-1805.04 and therefore exempt from DC FOIA disclosure via the statutory exemption cross-reference.',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individuals or businesses to the DC Office of Tax and Revenue. Covers income tax, real property tax, sales tax, and other DC tax filings. Aggregate tax revenue data, enforcement orders, and final court judgments in tax disputes are public. The Office of Tax and Revenue\'s operational and enforcement records are public.',
        'key_terms': json.dumps([
            'tax return', 'DC tax information', 'Office of Tax and Revenue', 'OTR',
            'income tax', 'real property tax', 'taxpayer information', 'tax filing',
            'D.C. Code § 47-1805.04', 'tax confidentiality',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Final court judgments in tax collection cases are public court records',
            'Tax enforcement orders and public sanctions are not covered',
            'The Office of Tax and Revenue\'s own operations and enforcement programs are public',
            'Challenge whether specific records are actual "tax return information" versus general OTR administrative correspondence',
        ]),
        'notes': 'D.C. Code § 47-1805.04 independently requires confidentiality for DC tax return information, which is incorporated into the FOIA exemption framework via D.C. Code § 2-534(a)(1). This is one of the most clearly established FOIA exemptions in DC — taxpayer-specific return data is categorically protected, but OTR operational records are public.',
    },
    {
        'jurisdiction': 'DC',
        'statute_citation': 'D.C. Code § 2-534(a)(3); D.C. Code § 2-532',
        'exemption_number': 'Segregability Requirement',
        'short_name': 'Segregability — Non-Exempt Portions Must Be Released',
        'category': 'procedure',
        'description': 'When a record contains both exempt and non-exempt information, DC agencies must release the non-exempt portions after deleting the exempt content. Blanket withholding is not permitted.',
        'scope': 'The DC FOIA segregability requirement (D.C. Code § 2-532) mandates that when a record contains both exempt and non-exempt information, the public body must provide any reasonably segregable portion of a record after deleting the exempt portions. The agency must identify what it is withholding and why. Withholding an entire record when only a portion is exempt is not permissible. The agency bears the burden of demonstrating that exempt and non-exempt information cannot reasonably be separated.',
        'key_terms': json.dumps([
            'segregability', 'reasonably segregable', 'partial release', 'redaction',
            'non-exempt portion', 'withholding', 'D.C. Code § 2-532', 'separable',
        ]),
        'counter_arguments': json.dumps([
            'This is an affirmative obligation on the agency — agencies must proactively identify and release all reasonably segregable non-exempt portions',
            'The agency bears the burden of demonstrating that separation is not reasonably possible',
            'Challenge any response that withholds entire documents when only specific fields or sections could qualify for an exemption',
            'DC courts and the Office of Open Government strictly enforce the segregability requirement',
        ]),
        'notes': 'The DC FOIA segregability requirement under D.C. Code § 2-532 is one of the law\'s most important provisions. The Office of Open Government and DC courts have consistently held that agencies must identify and release all reasonably segregable non-exempt portions of records, and that blanket withholding of documents containing some exempt material violates the Act.',
    },
]

# =============================================================================
# RULES
# DC Freedom of Information Act, D.C. Code § 2-531 et seq.
# DC FOIA provides a 15-business-day initial response deadline with a
# 10-business-day extension available. Unique features: (1) appeal goes to
# the Mayor (via the Office of Open Government) before DC Superior Court;
# (2) civil penalties of $100-$200/day for wrongful withholding;
# (3) Office of Open Government provides oversight, guidance, and mediation;
# (4) $0.25/page for paper copies; (5) attorney's fees for prevailing
# requesters. DC's framework is one of the most developed among US
# jurisdictions, closely mirroring the federal FOIA structure.
# =============================================================================

DC_RULES = [
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'initial_response_deadline_days',
        'param_value': '15',
        'day_type': 'business',
        'statute_citation': 'D.C. Code § 2-532(d)',
        'notes': 'DC agencies must respond to FOIA requests within 15 business days of receiving the request. The response must either produce records, deny the request with written justification, or invoke the 10-business-day extension with written explanation. The 15-business-day clock begins on the day the agency receives the request. Failure to respond within 15 business days (without an extension) is treated as a constructive denial that the requester may appeal immediately.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'extension_available_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'D.C. Code § 2-532(d)',
        'notes': 'DC agencies may invoke a single 10-business-day extension of the initial 15-business-day deadline, but only with written notice to the requester stating: (1) the reason for the extension; and (2) the date by which the agency will respond. Valid reasons for extension include: unusual volume of records, need for consultation with another agency having substantial interest, or searching records at remote locations. Agencies may not routinely invoke extensions without genuine justification. An extension without written notice is not valid and the original deadline continues to apply.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'constructive_denial_on_missed_deadline',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532(d)',
        'notes': 'If a DC agency fails to respond within the 15-business-day deadline (or within the 10-business-day extension period if properly invoked), the failure to respond is treated as a denial of the request. This constructive denial may be appealed to the Mayor (via the Office of Open Government) immediately, without waiting for a formal denial letter. This constructive denial rule is an important enforcement tool — requesters do not need to wait indefinitely for an agency response before seeking relief.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'presumption_of_openness',
        'param_value': 'statutory_mandate',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532',
        'notes': 'D.C. Code § 2-532 establishes a broad right of public access to all records in the possession of DC public bodies. The statute creates a strong presumption that all records are open for inspection. The burden of demonstrating that any record is exempt rests on the public body — not on the requester. DC courts review withholding decisions de novo and apply the presumption of openness actively. The denial must cite the specific FOIA exemption (D.C. Code § 2-534 subsection) authorizing withholding.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'written_request_recommended',
        'param_value': 'strongly_recommended',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532',
        'notes': 'DC FOIA requests may be made in writing or orally, but written requests are strongly recommended because: (1) they establish the 15-business-day response clock; (2) they create a record of the scope of the request; (3) they document the basis for appeal and litigation; and (4) they trigger the requirement for a written denial with cited exemptions. Most agencies have FOIA request forms or online portals, but use of these is not legally required.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532',
        'notes': 'DC agencies may not require requesters to identify themselves or state the purpose of their FOIA request as a condition of access. The right of access under D.C. Code § 2-532 is universal. Agencies may ask for contact information for delivery purposes, but may not condition access on identity disclosure or statement of purpose.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532',
        'notes': 'DC agencies must release all reasonably segregable non-exempt portions of records when part of a record qualifies for an exemption. Blanket withholding of entire documents containing some exempt material is not permissible. The agency bears the burden of demonstrating that separation of exempt and non-exempt portions is not reasonably possible. The Office of Open Government strictly enforces the segregability requirement.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'fee_cap',
        'param_key': 'copy_rate_paper',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532(h)',
        'notes': 'DC agencies charge $0.25 per page for paper copies of public records. For electronic records provided on physical media (CD, USB), agencies may charge the actual cost of the media. For electronic records delivered by email, no copying charge applies. DC agencies may not charge for staff time spent locating, reviewing, or redacting records — those costs are part of the public body\'s service obligation. Fee schedules must be published.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-532(h)',
        'notes': 'DC agencies may waive fees for FOIA requests when the agency determines that the primary purpose of the request is to benefit the general public. DC FOIA does not have specific mandatory fee waiver categories (unlike federal FOIA), but agencies have discretion to waive. For electronic delivery, no copying fee applies, making fee waivers effectively moot for many requests. Requesters should assert public interest grounds when seeking a fee waiver.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'appeal_deadline',
        'param_key': 'mayoral_appeal_deadline_days',
        'param_value': '90',
        'day_type': 'calendar',
        'statute_citation': 'D.C. Code § 2-537(a)',
        'notes': 'A requester denied access (or constructively denied by agency inaction) may appeal to the Mayor within 90 days of the denial. In practice, the appeal goes to the Office of Open Government (OOG), which operates under the DC Board of Ethics and Government Accountability. The OOG reviews the agency\'s determination, may request additional information from the agency, and issues a written decision. The OOG\'s review is a prerequisite before seeking DC Superior Court enforcement. The OOG process is faster and cheaper than court enforcement — the OOG typically resolves appeals within 20 business days.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'appeal_deadline',
        'param_key': 'office_of_open_government_role',
        'param_value': 'oversight_and_mediation',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-592; D.C. Code § 2-537',
        'notes': 'The DC Office of Open Government (OOG) has multiple roles in DC FOIA enforcement: (1) it receives and reviews mayoral appeals of FOIA denials under D.C. Code § 2-537; (2) it provides guidance and training to agencies on FOIA compliance; (3) it issues advisory opinions on FOIA questions; and (4) it can recommend civil penalties for agencies that wrongfully withhold records. The OOG is a relatively strong oversight body compared to other jurisdictions\' FOIA ombudsmen — its recommendations carry significant weight and agencies generally comply.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'superior_court_enforcement',
        'param_value': 'available_after_mayoral_appeal',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-537(c)',
        'notes': 'After receiving a decision on the mayoral appeal (or if the Mayor fails to act within the statutory period), a requester may seek enforcement in DC Superior Court under D.C. Code § 2-537(c). The court reviews the agency\'s withholding de novo and may conduct in camera review of withheld records. The court may order production of records, award attorney fees, and impose civil penalties. The mayoral appeal to the OOG is a prerequisite — a requester generally must exhaust that administrative remedy before going to court.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'penalty',
        'param_key': 'civil_penalty_per_day',
        'param_value': '$100-$200 per day',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-537(c)',
        'notes': 'DC FOIA provides for civil penalties of $100 to $200 per day for each day records are wrongfully withheld after a court order to produce. This is one of the few US jurisdictions with per-day civil penalties for FOIA violations (similar to Washington State\'s per diem penalties). The court sets the daily penalty amount based on the egregiousness of the violation. Penalties accumulate from the date of the court\'s production order through the date records are actually produced. The civil penalty provision provides a significant deterrent for agencies tempted to delay or defy court orders.',
    },
    {
        'jurisdiction': 'DC',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_prevailing_requester',
        'param_value': 'discretionary',
        'day_type': None,
        'statute_citation': 'D.C. Code § 2-537(c)',
        'notes': 'DC Superior Court may award reasonable attorney fees and costs to a requester who substantially prevails in a DC FOIA enforcement action. Attorney fees are discretionary — the court considers the public benefit of disclosure, the nature of the agency\'s response, and whether the agency acted in good faith. In practice, courts award fees when agencies withheld records without a reasonable legal basis. The availability of attorney fees makes it viable for requesters and their attorneys to bring enforcement actions for important records.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

DC_TEMPLATES = [
    {
        'jurisdiction': 'DC',
        'record_type': 'general',
        'template_name': 'General DC Freedom of Information Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Freedom of Information Act Officer
{{agency_name}}
{{agency_address}}

Re: Freedom of Information Act Request — D.C. Code § 2-531 et seq.

Dear FOIA Officer:

Pursuant to the DC Freedom of Information Act, D.C. Code § 2-531 et seq., I hereby request access to and copies of the following records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available. Electronic delivery eliminates copying fees under D.C. Code § 2-532(h).

I am willing to pay fees up to ${{fee_limit}} for paper copies at the rate of $0.25/page consistent with D.C. Code § 2-532(h). If fees will exceed that amount, please notify me before proceeding so I may refine my request or arrange payment.

Under D.C. Code § 2-532, all records are presumptively public and the burden of demonstrating that any record is exempt rests on the agency. If any records are withheld in whole or in part, I request that you: (1) identify each withheld record; (2) state the specific DC FOIA exemption (D.C. Code § 2-534(a)(___)) authorizing withholding; (3) describe the withheld record with sufficient detail for me to evaluate the claimed exemption; and (4) confirm that all reasonably segregable non-exempt portions of partially withheld records have been released.

Under D.C. Code § 2-532(d), please respond within 15 business days of receipt of this request. If you require the 10-business-day extension, please provide written notice with the specific reason and the date by which you will respond.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. DC FOIA does not provide categorical fee waivers, but I ask that {{agency_name}} exercise its discretion to waive fees under D.C. Code § 2-532(h) because:

1. The primary purpose of this request is to benefit the general public. The requested records relate to {{public_interest_explanation}}, a matter of significant government accountability.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, no copying fee applies under D.C. Code § 2-532(h), making a fee waiver consistent with both the letter and purpose of DC FOIA's access mandate.''',
        'expedited_language': '''I request expedited processing of this FOIA request. Prompt production is particularly important here because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay beyond this date will {{harm_from_delay}}.

I understand that the 15-business-day initial deadline under D.C. Code § 2-532(d) applies. If you need clarification that would speed production, please contact me immediately.''',
        'notes': 'General-purpose DC FOIA template. Key DC features: (1) 15 business day initial deadline — cite D.C. Code § 2-532(d); (2) 10 business day extension available with written notice; (3) constructive denial if agency fails to respond — requester may appeal immediately; (4) appeal to Mayor (Office of Open Government) within 90 days under D.C. Code § 2-537(a) before going to Superior Court; (5) civil penalties $100-$200/day for wrongful withholding after court order; (6) attorney fees discretionary for prevailing requester; (7) $0.25/page for paper copies; (8) Office of Open Government (OOG) is a useful resource for guidance and mediation. Reference "D.C. Code § 2-531," not "federal FOIA."',
    },
    {
        'jurisdiction': 'DC',
        'record_type': 'law_enforcement',
        'template_name': 'DC FOIA Request — Law Enforcement and MPD Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Freedom of Information Act Officer
{{agency_name}}
{{agency_address}}

Re: DC Freedom of Information Act Request — Law Enforcement Records, D.C. Code § 2-531

Dear FOIA Officer:

Pursuant to the DC Freedom of Information Act, D.C. Code § 2-531 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and police reports (PD-251 forms)
- Arrest records and booking information
- Use-of-force reports (PD-901-a forms) and documentation
- Officer disciplinary and complaint records for involved personnel (UFRP and OPC records)
- Body-worn camera footage and associated metadata
- Criminal History Record Information (CHRI) for specified matters
- Dispatch records and Computer-Aided Dispatch (CAD) logs

Regarding D.C. Code § 2-534(a)(5): the investigatory records exemption requires the agency to demonstrate a specific enumerated harm for each withheld record. The enumerated harms are: (A) interference with enforcement proceedings; (B) deprivation of right to fair trial; (C) unwarranted invasion of personal privacy; (D) revealing confidential informant identity; (E) disclosing investigative techniques; or (F) endangering life or physical safety. A general assertion that records are "investigatory" is not sufficient.

[If matter appears concluded:] If any prosecution related to this incident has concluded or the investigation has been closed, the investigatory records exemption does not apply. Concluded investigation records are public.

Arrest records, incident reports, and basic factual information are public under DC FOIA regardless of investigation status.

Under D.C. Code § 2-532(d), please respond within 15 business days. Any extension must be accompanied by written notice stating the reason and a response date.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request. These records concern law enforcement actions and government accountability. Electronic delivery involves no copying fee under D.C. Code § 2-532(h). A fee waiver is consistent with the public benefit of disclosure.''',
        'expedited_language': '''I request expedited processing under the 15-business-day deadline of D.C. Code § 2-532(d). These records are needed by {{needed_by_date}} because {{urgency_explanation}}.''',
        'notes': 'DC law enforcement records template. Key DC features: (1) D.C. Code § 2-534(a)(5) requires specific enumerated harm for each withheld record; (2) concluded investigation records are public; (3) arrest records and incident reports are public regardless of investigation status; (4) MPD has its own FOIA office — submit to the MPD FOIA Officer specifically; (5) Office of Police Complaints (OPC) records have separate access procedures; (6) 15 business day response deadline; (7) mayoral appeal (OOG) before Superior Court; (8) civil penalties $100-$200/day after court order; (9) attorney fees discretionary.',
    },
    {
        'jurisdiction': 'DC',
        'record_type': 'mayoral_appeal',
        'template_name': 'DC FOIA Appeal to Mayor — Office of Open Government',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Director
Office of Open Government
Board of Ethics and Government Accountability
441 4th Street, NW, Suite 850 North
Washington, DC 20001

Re: DC FOIA Appeal — Denial by {{agency_name}}, Request dated {{original_request_date}}

Dear Director:

Pursuant to D.C. Code § 2-537(a), I hereby appeal the denial (or constructive denial) of my Freedom of Information Act request to {{agency_name}}.

Background:
- Original FOIA request submitted: {{original_request_date}}
- Agency response received: {{agency_response_date}} [or: "No response received within the 15-business-day deadline — constructive denial per D.C. Code § 2-532(d)"]
- Records requested: {{summary_of_records_requested}}
- Agency's stated basis for denial: {{agency_denial_reason}} [or: "Agency failed to respond within the required timeframe"]

Grounds for Appeal:

{{appeal_grounds}}

[Choose applicable grounds:]
[ ] The agency failed to demonstrate that the claimed exemption (D.C. Code § 2-534(a)(___)) applies to the specific withheld records.
[ ] The agency failed to release all reasonably segregable non-exempt portions of withheld records as required by D.C. Code § 2-532.
[ ] The agency failed to respond within the 15-business-day deadline and the 10-business-day extension is not applicable or was not properly invoked.
[ ] The agency's denial does not identify the specific exemption with sufficient particularity.
[ ] The claimed exemption does not apply for the following reason: {{specific_legal_argument}}

I request that the Office of Open Government review the agency's determination, direct the agency to produce all responsive records, and consider whether civil penalties under D.C. Code § 2-537(c) are appropriate given the circumstances.

Copies of my original FOIA request and the agency's response (if any) are attached.

Respectfully,
{{requester_name}}

Attachments:
1. Original FOIA request dated {{original_request_date}}
2. Agency response/denial dated {{agency_response_date}} [if received]''',
        'fee_waiver_language': '',
        'expedited_language': '''I request that the Office of Open Government process this appeal expeditiously. The records are needed for {{urgency_explanation}} by {{needed_by_date}}.''',
        'notes': 'DC FOIA appeal template for the mandatory pre-court administrative appeal to the Mayor/OOG. Key DC features: (1) appeal must be filed within 90 days of denial — D.C. Code § 2-537(a); (2) OOG typically responds within 20 business days; (3) OOG review is prerequisite for Superior Court enforcement; (4) constructive denial (agency silence) can be appealed immediately after 15-day deadline without extension; (5) send to: Office of Open Government, Board of Ethics and Government Accountability, 441 4th Street NW, Suite 850 North, Washington DC 20001; (6) attach copies of original request and agency response.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in DC_EXEMPTIONS:
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

    print(f'DC exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in DC_RULES:
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

    print(f'DC rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in DC_TEMPLATES:
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

    print(f'DC templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'DC total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_dc', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
