#!/usr/bin/env python3
"""Build Oregon Public Records Law data: exemptions, rules, and templates.

Covers Oregon's Public Records Law (ORPRL), ORS 192.311-192.478 (formerly
ORS 192.410-192.505). Key features: 5-business-day acknowledgment deadline,
10-additional-day extension option, appeal to district attorney (unusual),
fee waiver available when disclosure serves the public interest, attorney's
fees for prevailing requesters, $0.25/page standard copy rate. Oregon courts
strictly construe exemptions against agencies.

Run: python3 scripts/build/build_or.py
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
# Oregon Public Records Law exemptions are codified at ORS 192.338 (mandatory
# exemptions — records exempt by law) and ORS 192.345 (discretionary
# exemptions — records that may be withheld). The distinction is important:
# discretionary exemptions can be waived by the agency. Oregon courts apply
# strict construction against withholding. The district attorney appeal process
# is unusual and creates a state-law intermediate review option.
# =============================================================================

OR_EXEMPTIONS = [
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.338',
        'exemption_number': 'ORS 192.338',
        'short_name': 'Records Exempt by Law — Mandatory Confidentiality',
        'category': 'statutory',
        'description': 'Records that are specifically designated confidential by another Oregon statute or rule, or by federal law, are mandatorily exempt from disclosure under Oregon\'s Public Records Law.',
        'scope': 'Records specifically designated confidential by another Oregon statute, state administrative rule, or federal law. Examples include: income tax records under ORS 314.835; child welfare records under ORS 419B.035; certain health records; motor vehicle records under the DPPA; and federally protected program records. The mandatory exemption applies to the full scope of the other law — no more and no less. The agency must identify the specific statute or rule and explain how it applies. Aggregate and anonymized data from confidential records are generally public.',
        'key_terms': json.dumps([
            'exempt by law', 'statutory confidentiality', 'mandatory exemption',
            'tax records', 'child welfare records', 'DPPA', 'federal confidentiality',
            'ORS 192.338', 'confidential by statute',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific statute — a generic "exempt by law" claim is insufficient',
            'The other statute\'s exceptions and disclosure permissions apply',
            'Aggregate and de-identified data are generally public even if individual records are confidential',
            'Administrative records of agencies holding confidential records are public',
            'Challenge whether the specific record actually falls within the cited statute\'s scope',
        ]),
        'notes': 'ORS 192.338 is the mandatory exemption provision — it applies when another law requires confidentiality. Oregon courts distinguish this from ORS 192.345 (discretionary exemptions), where agencies have the option to withhold. The distinction matters strategically: if an exemption is discretionary, the requester can seek voluntary disclosure or argue that the public interest requires it.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(1)',
        'exemption_number': 'ORS 192.345(1)',
        'short_name': 'Communications Within or Between Public Bodies — Deliberative Process',
        'category': 'deliberative',
        'description': 'Communications within a public body or between public bodies of an advisory nature that precede a final agency decision on policy or operational matters are discretionarily exempt — the agency may but need not withhold them.',
        'scope': 'Internal communications between government employees, between agencies, or communications from non-employees to government decision-makers that are: (1) advisory in nature; (2) preliminary to a final policy or operational decision; and (3) part of the deliberative process for developing that decision. Oregon\'s deliberative process exemption is permissive — agencies have discretion to disclose. Purely factual information is not covered even if embedded in deliberative documents. Final decisions, working law, and adopted policies are public. Oregon courts apply a strict factual/opinion distinction.',
        'key_terms': json.dumps([
            'deliberative process', 'advisory communication', 'predecisional',
            'intra-agency communication', 'inter-agency communication',
            'preliminary to decision', 'policy development', 'working paper',
            'staff recommendation', 'draft policy',
        ]),
        'counter_arguments': json.dumps([
            'ORS 192.345(1) is DISCRETIONARY — the agency may disclose even if the exemption technically applies; argue for voluntary disclosure',
            'Purely factual material within deliberative documents must be segregated and released',
            'Once a recommendation is adopted as final agency policy, the exemption does not apply',
            '"Working law" — standards and criteria agencies actually apply — must be disclosed',
            'Documents circulated outside the agency may lose their predecisional character',
            'Oregon courts strictly limit the exemption to opinion-containing, predecisional documents',
        ]),
        'notes': 'ORS 192.345(1) is a discretionary exemption — one of Oregon\'s key distinctions. The permissive nature means agencies have authority to disclose even if the exemption technically applies, and requesters can advocate for voluntary disclosure on public interest grounds. Oregon courts apply the exemption narrowly. The Attorney General\'s Public Records Manual provides detailed guidance on applying ORS 192.345(1).',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(2)',
        'exemption_number': 'ORS 192.345(2)',
        'short_name': 'Personnel Records — Limited Privacy Protection',
        'category': 'privacy',
        'description': 'Information of a personal nature about an individual, including employment-related information, whose disclosure would constitute an unreasonable invasion of personal privacy — where the public interest in disclosure does not clearly outweigh the privacy interest — is discretionarily exempt.',
        'scope': 'Personal information about individuals, including employment-related records, where disclosure would constitute an unreasonable invasion of personal privacy AND the public interest in disclosure does not clearly outweigh the privacy interest. Oregon applies a two-pronged test: (1) the information must be genuinely private; and (2) the privacy interest must outweigh the demonstrated public interest. For public employees acting in their official capacity, the public interest in accountability typically outweighs privacy. Salary information, job title, and work history of public employees are generally public. The exemption is discretionary — agencies may disclose.',
        'key_terms': json.dumps([
            'personal privacy', 'unreasonable invasion', 'personnel records',
            'personal information', 'privacy vs. public interest', 'employment record',
            'public employee privacy', 'discretionary privacy exemption',
        ]),
        'counter_arguments': json.dumps([
            'ORS 192.345(2) is DISCRETIONARY — agencies may disclose even if the exemption technically applies',
            'The public interest in disclosure must "clearly" fail to outweigh privacy — a high bar for public employee official conduct',
            'Salary, job title, and employment history of public employees are generally public',
            'Information about how a public employee performed official duties is not purely personal',
            'Oregon courts hold that public employees have reduced privacy expectations for records of official conduct',
            'The district attorney can be petitioned to order disclosure even over an agency\'s privacy claim',
        ]),
        'notes': 'Oregon\'s personal privacy exemption is broader than many states\' equivalents but is tempered by the discretionary nature of the exemption and the public interest override test. Oregon\'s Attorney General has issued extensive guidance on applying the public interest override. In practice, Oregon agencies routinely disclose salary and work history information for public employees.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(4)',
        'exemption_number': 'ORS 192.345(4)',
        'short_name': 'Trade Secrets and Confidential Submitted Business Information',
        'category': 'commercial',
        'description': 'Trade secrets, and confidential commercial or financial information submitted by a private party, are discretionarily exempt from Oregon Public Records Law disclosure when disclosure would cause substantial harm to the competitive position of the submitter.',
        'scope': 'Commercially valuable information submitted by private entities to Oregon government agencies where: (1) the information constitutes a trade secret or is treated as confidential commercial/financial data; (2) the submitter had a reasonable expectation of confidentiality; and (3) disclosure would cause substantial competitive harm. Oregon applies the Uniform Trade Secrets Act. Contract prices and amounts paid with public funds are generally public. The exemption is discretionary — agencies may disclose. The agency must independently evaluate trade secret claims.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'financial information',
            'competitive harm', 'UTSA', 'proprietary data', 'substantial competitive harm',
            'business information', 'commercial secrecy',
        ]),
        'counter_arguments': json.dumps([
            'ORS 192.345(4) is DISCRETIONARY — agencies may disclose even if the exemption technically applies',
            'Contract prices and amounts paid with public funds are public regardless of vendor designations',
            '"Substantial" competitive harm is required — speculative or minor harm is insufficient',
            'The agency must independently evaluate the claim — it cannot simply defer to the vendor',
            'Publicly available information cannot qualify as a trade secret',
            'Information required by law to be submitted has reduced secrecy expectations',
        ]),
        'notes': 'Oregon\'s trade secret exemption requires substantial competitive harm — a higher standard than mere competitive disadvantage. The discretionary nature means agencies can disclose even if the exemption technically applies. Oregon courts have consistently held that government contract amounts and performance data are public. The Attorney General\'s manual provides specific guidance on evaluating trade secret claims.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(3)',
        'exemption_number': 'ORS 192.345(3)',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Records protected by the attorney-client privilege and work product doctrine are discretionarily exempt from Oregon Public Records Law disclosure.',
        'scope': 'Confidential communications between government agencies and their attorneys for the purpose of obtaining or providing legal advice (attorney-client privilege), and documents prepared by attorneys specifically in anticipation of litigation (work product). Oregon applies the common-law attorney-client privilege to government entities. Billing records and retainer agreements are generally public. Work product requires anticipation of specific litigation — generalized future litigation is insufficient. The exemption is discretionary — agencies may disclose even privileged records.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'privileged communication', 'in anticipation of litigation',
            'government attorney', 'legal opinion', 'attorney work product',
        ]),
        'counter_arguments': json.dumps([
            'ORS 192.345(3) is DISCRETIONARY — agencies may disclose even privileged records',
            'Communications for policy or business advice (not legal advice) are not privileged',
            'Billing records are generally public',
            'Waiver occurs when advice is used in public decision-making or disclosed to non-essential parties',
            'Facts underlying legal advice are not privileged',
            'Work product requires specific anticipated litigation — generalized future litigation is insufficient',
        ]),
        'notes': 'Oregon\'s attorney-client exemption is discretionary — a key distinction from states with mandatory privilege protection. The district attorney, on petition, may find that the public interest requires disclosure of otherwise privileged records. Oregon courts apply the privilege narrowly given the Public Records Law\'s strong disclosure mandate.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(12)',
        'exemption_number': 'ORS 192.345(12)',
        'short_name': 'Law Enforcement Records — Active Investigations',
        'category': 'law_enforcement',
        'description': 'Records compiled by a public body for criminal law enforcement purposes are discretionarily exempt where disclosure would interfere with enforcement, deprive a person of a fair trial, identify confidential informants, constitute an unwarranted invasion of privacy, reveal investigative techniques, or endanger life.',
        'scope': 'Records compiled by law enforcement agencies for criminal law enforcement purposes where disclosure would: (1) interfere with enforcement proceedings; (2) deprive a person of the right to a fair trial; (3) identify confidential informants; (4) constitute an unwarranted invasion of privacy; (5) reveal investigative techniques; (6) endanger the life of any person; or (7) disclose the identity of an undercover agent. The exemption is discretionary. Once investigations are completed and prosecution concludes, the exemption weakens significantly. Incident reports, arrest records, and booking information are generally public.',
        'key_terms': json.dumps([
            'law enforcement records', 'criminal investigation', 'confidential informant',
            'investigative technique', 'pending prosecution', 'law enforcement sensitive',
            'criminal intelligence', 'investigation file', 'undercover agent',
        ]),
        'counter_arguments': json.dumps([
            'ORS 192.345(12) is DISCRETIONARY — agencies may disclose even if technically exempt',
            'Incident reports, arrest records, and booking information are generally public regardless of investigation status',
            'Records of completed investigations are generally public once prosecution concludes',
            'Each withheld record requires a specific harm showing — "active investigation" labels are insufficient',
            'Factual information not implicating any enumerated harm must be released',
            'The district attorney may order disclosure even over law enforcement objections',
        ]),
        'notes': 'Oregon\'s law enforcement exemption is discretionary under ORS 192.345(12). The permissive nature means agencies can voluntarily disclose records even if the exemption technically applies. Oregon\'s Attorney General and district attorneys have issued guidance emphasizing that the exemption is narrow and that completed investigation files are generally accessible. Incident reports and arrest records are public.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(5)',
        'exemption_number': 'ORS 192.345(5)',
        'short_name': 'Real Property Appraisals — Pre-Acquisition',
        'category': 'commercial',
        'description': 'Appraisal documents and related valuation records for real or personal property being acquired or sold by a public body are discretionarily exempt prior to completion of the transaction.',
        'scope': 'Formal property appraisals, feasibility studies, and related valuation documents prepared in connection with a government body\'s pending acquisition or sale of real property. The exemption is discretionary and time-limited — it expires when the transaction closes or is abandoned. Post-transaction, all appraisal records are public. The exemption protects the government\'s negotiating position. Internal general budget estimates do not constitute formal appraisals.',
        'key_terms': json.dumps([
            'real estate appraisal', 'property acquisition', 'property valuation',
            'pre-acquisition', 'property sale', 'negotiating position',
            'real property', 'condemnation appraisal',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is DISCRETIONARY — the agency may disclose pre-acquisition appraisals',
            'The exemption expires when the transaction closes or is abandoned',
            'Challenge claims that an acquisition remains "pending" after extended inactivity',
            'Internal budget estimates are not formal appraisals',
            'Post-transaction records are fully public',
        ]),
        'notes': 'Oregon\'s pre-acquisition appraisal exemption is discretionary and narrow. Oregon courts apply it strictly to formal appraisal documents in connection with actual pending transactions. The discretionary nature means advocacy for voluntary disclosure is always available.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(7)',
        'exemption_number': 'ORS 192.345(7)',
        'short_name': 'Test Questions and Examination Materials',
        'category': 'deliberative',
        'description': 'Unpublished test questions, scoring keys, and examination materials used in civil service, licensing, and competitive employment evaluations are discretionarily exempt prior to and during administration.',
        'scope': 'Unpublished test questions, answer keys, and scoring materials for government-administered examinations including civil service tests, licensing examinations, and competitive hiring evaluations. The exemption is discretionary and prospective — it expires after administration and when results are finalized. General examination policies, scoring methodology in the abstract, and aggregate performance data are public. The exemption is narrowly tailored to protect test security.',
        'key_terms': json.dumps([
            'test questions', 'scoring key', 'examination materials',
            'civil service exam', 'licensing test', 'competitive evaluation',
            'test security', 'answer key',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is DISCRETIONARY — agencies may disclose',
            'The exemption expires after administration',
            'General examination policy and methodology are public',
            'Prior-year examination questions that are retired from use may not remain protected',
            'Aggregate performance data and passing rates are public',
        ]),
        'notes': 'Oregon\'s examination exemption is standard and narrow. The discretionary nature allows flexibility — some agencies voluntarily release past examination questions for study purposes after administration. Oregon courts have consistently held that the exemption does not cover general examination policy or aggregate results.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(22)',
        'exemption_number': 'ORS 192.345(22)',
        'short_name': 'Security Plans and Vulnerability Assessments',
        'category': 'safety',
        'description': 'Records containing the specific details of security plans, vulnerability assessments, or emergency response procedures for critical infrastructure or government facilities — where disclosure would significantly impair the effectiveness of those measures — are discretionarily exempt.',
        'scope': 'Specific technical details of physical security systems, vulnerability assessments identifying specific exploitable weaknesses, and detailed emergency protocols for critical infrastructure. The exemption requires a specific showing that disclosure would significantly impair security effectiveness — not a generalized security classification. General emergency management policy, security program budgets, and after-action reports focused on policy improvements are public. The exemption is discretionary.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'emergency response procedure',
            'critical infrastructure', 'physical security', 'facility security',
            'security protocol', 'cybersecurity', 'security vulnerability',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is DISCRETIONARY — agencies may disclose',
            'General emergency management policy and procedures are public',
            'Security program budgets and staffing are public',
            'After-action reports focused on policy improvements are public',
            'The agency must show that specific security would be significantly impaired — not a general security label',
        ]),
        'notes': 'Oregon\'s security exemption is discretionary and requires a specific showing of significant impairment. Oregon courts and the district attorney review process have both applied the exemption narrowly, requiring agencies to demonstrate the specific security risk from disclosure rather than relying on broad security classifications.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.345(9)',
        'exemption_number': 'ORS 192.345(9)',
        'short_name': 'Records of Juvenile Court Proceedings',
        'category': 'privacy',
        'description': 'Records related to juvenile court proceedings and juvenile justice matters, including police records of juveniles, are discretionarily exempt under Oregon\'s Public Records Law, consistent with Oregon\'s Juvenile Code.',
        'scope': 'Records specifically related to juvenile court proceedings, juvenile arrests, detention records, and related juvenile justice information. The exemption works in conjunction with Oregon\'s Juvenile Code (ORS Chapter 419A) and reflects the strong policy of rehabilitative confidentiality for juvenile offenders. Non-identifying aggregate statistics about juvenile justice system outcomes and agency operations are public. Records of juveniles tried as adults are public to the same extent as adult criminal records.',
        'key_terms': json.dumps([
            'juvenile records', 'juvenile court', 'juvenile justice',
            'minor records', 'juvenile arrest record', 'youth offender',
            'ORS Chapter 419A', 'juvenile proceedings',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is DISCRETIONARY — agencies may disclose in some circumstances',
            'Juveniles tried as adults have public records to the same extent as adult defendants',
            'Aggregate juvenile justice statistics are public',
            'Agency policies, programs, and budgets for juvenile justice are public',
            'Records of adult misconduct even if the subject was a juvenile at the time of the underlying incident may have been made public through court proceedings',
        ]),
        'notes': 'Oregon\'s juvenile records exemption works in conjunction with the comprehensive protections in ORS Chapter 419A. The Oregon legislature has periodically expanded and contracted juvenile record access, particularly for serious violent offenders. Practitioners should review current ORS Chapter 419A for the most recent specific provisions.',
    },
    {
        'jurisdiction': 'OR',
        'statute_citation': 'ORS 192.355(8)',
        'exemption_number': 'ORS 192.355(8)',
        'short_name': 'Public Interest Override — Discretionary Exemptions',
        'category': 'deliberative',
        'description': 'Oregon\'s Public Records Law provides that even when a discretionary exemption technically applies, the public body must balance the public interest in disclosure against the interest in confidentiality. If the public interest in disclosure clearly outweighs the confidentiality interest, disclosure is required.',
        'scope': 'Not strictly an exemption — rather, this is the public interest override that applies to all discretionary exemptions under ORS 192.345. When a public body invokes a discretionary exemption, it must affirmatively determine that the interest in confidentiality outweighs the public interest in disclosure. If the requester can demonstrate a strong public interest — such as accountability for government misconduct, public safety, or the exercise of government power — the override may require disclosure even where a discretionary exemption technically applies. This makes Oregon\'s discretionary exemption framework meaningfully different from states with mandatory exemptions.',
        'key_terms': json.dumps([
            'public interest override', 'discretionary exemption override',
            'public interest vs. confidentiality', 'balancing test', 'accountability',
            'ORS 192.345', 'interest in disclosure', 'public interest in disclosure',
        ]),
        'counter_arguments': json.dumps([
            'Always invoke the public interest override when challenging a discretionary exemption',
            'Accountability for government misconduct, waste, or abuse of power is a strong public interest',
            'Safety and public health concerns can override discretionary exemptions',
            'Document the specific public interest served by disclosure when making arguments to the district attorney',
            'Oregon courts apply the override seriously — it is not merely aspirational',
        ]),
        'notes': 'The public interest override is one of Oregon\'s most important public records provisions. It applies to all discretionary exemptions under ORS 192.345 and means that even technically exempt records must be disclosed if the public interest clearly outweighs the confidentiality interest. The Oregon Attorney General\'s Public Records Manual provides detailed guidance on applying the override. Requesters should always articulate the public interest argument when seeking records that may be subject to discretionary exemptions.',
    },
]

# =============================================================================
# RULES
# Oregon Public Records Law, ORS 192.311-192.478.
# Key features: 5-business-day acknowledgment deadline, 10-additional-day
# extension, appeal to district attorney (unique), fee waiver in public
# interest, attorney's fees for prevailing requesters, $0.25/page copy rate.
# =============================================================================

OR_RULES = [
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'acknowledgment_deadline_days',
        'param_value': '5',
        'day_type': 'business',
        'statute_citation': 'ORS 192.329(1)',
        'notes': 'Oregon public bodies must acknowledge receipt of a public records request within 5 business days and provide an estimated date when the records will be available. The acknowledgment must include the estimated date of production — a mere receipt confirmation without an estimated production timeline does not satisfy Oregon\'s requirements. This acknowledgment deadline is separate from the actual production deadline, which must be "as soon as practicable." Failure to acknowledge within 5 business days supports a district attorney complaint or court action.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'response_extension_days',
        'param_value': '10',
        'day_type': 'business',
        'statute_citation': 'ORS 192.329(2)',
        'notes': 'Oregon public bodies may extend the estimated production date by up to 10 additional business days beyond the initial estimate if: (1) the request requires a large volume of records; (2) the request requires information from widely separated offices; (3) consultation with other agencies is required; or (4) the request requires extensive examination to determine which portions are exempt. The agency must notify the requester of the extension in writing, providing the new estimated date and the reason for the extension. The extension is for the production estimate, not the acknowledgment.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'production_timeline',
        'param_value': 'as_soon_as_practicable',
        'day_type': None,
        'statute_citation': 'ORS 192.329(1)',
        'notes': 'Oregon\'s general production standard is "as soon as practicable and without unreasonable delay." This standard requires agencies to actively work to produce responsive records, not to wait until the maximum allowed time. Oregon courts have held that unreasonable delay — even within formal statutory timelines — can constitute a violation of the Public Records Law. The "as soon as practicable" standard reflects Oregon\'s policy that public records belong to the people and that access should be timely and meaningful.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'fee_cap',
        'param_key': 'standard_copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'ORS 192.324(2)',
        'notes': 'Oregon agencies may charge a fee to cover the actual cost of making public records available. For paper copies, the standard rate is $0.25 per page. For electronic records, agencies may charge the actual cost of retrieving and transmitting the records. Oregon permits agencies to charge for staff time at the actual cost of the lowest-paid employee capable of performing the work. If estimated fees exceed $25, the agency must provide an advance cost estimate before incurring the charges. The fee must be "reasonable" and cover actual costs — excess profit is not permitted.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_charges_allowed',
        'param_value': 'yes_at_actual_cost_lowest_paid_employee',
        'day_type': None,
        'statute_citation': 'ORS 192.324(2)',
        'notes': 'Oregon allows agencies to charge for staff time spent searching, reviewing, and preparing records, at the actual cost of the lowest-paid employee capable of performing the task. This is a significant fee component for complex requests. If the estimated fee exceeds $25, the agency must notify the requester with an itemized estimate before proceeding. The requester may then refine the request to reduce costs or arrange payment. Oregon courts have found fees unreasonable where they bore no relationship to actual costs.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_public_interest',
        'param_value': 'available_when_disclosure_primarily_benefits_public',
        'day_type': None,
        'statute_citation': 'ORS 192.324(3)',
        'notes': 'Oregon mandates a fee waiver when the disclosure "primarily benefits the general public rather than the requester." ORS 192.324(3) requires agencies to waive fees when the public interest in disclosure outweighs the requester\'s personal interest. This is a meaningful mandatory waiver provision — unlike states with purely discretionary waivers. Factors supporting a public interest waiver: the records relate to government accountability, public safety, or the exercise of government power; the requester is a journalist, nonprofit, or academic researcher; the information will be disseminated to the public; and the requester has no commercial purpose. Requesters should document the public benefit explicitly.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_advance_estimate_threshold',
        'param_value': '25',
        'day_type': None,
        'statute_citation': 'ORS 192.324(2)',
        'notes': 'When the estimated fee for a public records request exceeds $25, Oregon agencies must provide the requester with a written advance cost estimate itemizing the anticipated costs before incurring them. The requester may then pay, revise the request to reduce costs, or withdraw. This advance notice requirement prevents surprise charges and gives requesters budget visibility. Agencies may not charge fees exceeding $25 without providing this advance notice and receiving the requester\'s agreement to proceed.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'appeal_deadline',
        'param_key': 'district_attorney_petition_deadline_days',
        'param_value': '60',
        'day_type': 'calendar',
        'statute_citation': 'ORS 192.411',
        'notes': 'Oregon\'s most distinctive procedural feature is the ability to petition the district attorney to review a public records denial. A requester may petition the district attorney of the county in which the public body is located to require disclosure of records denied under ORS 192.345 (discretionary exemptions) within 60 calendar days of the denial. The district attorney\'s decision is binding on the public body. The DA review is free, faster than court, and provides an independent evaluation of whether the discretionary exemption was properly invoked. The DA\'s decision can be appealed to circuit court.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'appeal_deadline',
        'param_key': 'circuit_court_action_available',
        'param_value': 'yes_independent_of_da_appeal',
        'day_type': None,
        'statute_citation': 'ORS 192.415',
        'notes': 'A requester may also file an action in Oregon circuit court to compel disclosure without first petitioning the district attorney. Circuit court actions are appropriate for mandatory exemption disputes (ORS 192.338), where the DA has no jurisdiction, and for cases where the DA review was unsatisfactory. Courts apply de novo review to ORPRL withholding decisions. The circuit court may conduct in camera review of withheld records. Oregon courts have consistently applied strict construction against exemptions.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'ORS 192.431',
        'notes': 'Oregon courts may award attorney fees and costs to requesters who substantially prevail in circuit court actions under the Oregon Public Records Law. ORS 192.431 provides for fee awards to prevailing requesters. While not as explicitly mandatory as New Jersey\'s provision, Oregon courts consistently award fees to requesters who substantially prevail. The availability of attorney fees makes Oregon PRL enforcement economically viable for complex cases. Courts have awarded substantial fees in cases involving systematic non-compliance.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'penalty',
        'param_key': 'civil_fine_possible',
        'param_value': 'available_for_willful_refusal',
        'day_type': None,
        'statute_citation': 'ORS 192.431(2)',
        'notes': 'Oregon courts may impose civil fines for willful refusal to comply with the Oregon Public Records Law. The fine provision applies to public officials who knowingly and willfully refused to disclose public records without legal justification. Fines may also be assessed against agencies for systematic non-compliance. The civil fine provision is distinct from attorney fees and is intended to punish and deter bad-faith violations.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_public_body',
        'day_type': None,
        'statute_citation': 'ORS 192.335',
        'notes': 'The burden of establishing that a public record is exempt from disclosure rests on the public body — not the requester. ORS 192.335 establishes a presumption of public access. When a public body claims an exemption, it must affirmatively demonstrate that the specific exemption applies to the specific record at issue. Generic assertions of exemption categories are insufficient. Oregon courts apply de novo review and give no deference to agency exemption determinations. The strong burden-of-proof rule makes Oregon\'s Public Records Law one of the more requester-favorable in the country.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_required',
        'param_value': 'yes_with_specific_citation',
        'day_type': None,
        'statute_citation': 'ORS 192.329(3)',
        'notes': 'When denying a public records request, Oregon agencies must provide a written denial stating the specific statutory provision that authorizes withholding. A denial without a specific statutory citation to ORS 192.338 or 192.345 (with applicable subsection) is legally deficient and strengthens the requester\'s position on appeal. The denial must inform the requester of the right to petition the district attorney (for discretionary exemptions) or file in circuit court. The denial must be prompt — unreasonable delay in issuing a formal denial can itself be actionable.',
    },
    {
        'jurisdiction': 'OR',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'ORS 192.338; ORS 192.345',
        'notes': 'Oregon public bodies must release all reasonably segregable non-exempt portions of records when only part of a record qualifies for an exemption. Blanket withholding of complex documents because one section contains exempt material is improper under Oregon law. Oregon courts have consistently required agencies to demonstrate that they reviewed documents for partial disclosure. Failure to segregate exempt from non-exempt content strengthens a requester\'s case before the district attorney or circuit court.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

OR_TEMPLATES = [
    {
        'jurisdiction': 'OR',
        'record_type': 'general',
        'template_name': 'General Oregon Public Records Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Oregon Public Records Law Request — ORS 192.311 et seq.

Dear Public Records Officer:

Pursuant to the Oregon Public Records Law, ORS 192.311 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which minimizes costs.

Regarding fees: I am willing to pay reasonable fees reflecting the actual costs of reproduction and necessary staff time as permitted by ORS 192.324(2), at the rate of the lowest-paid employee capable of performing each task. The standard paper copy rate is $0.25/page. If estimated fees will exceed $25, please provide an itemized advance estimate before incurring charges so I may revise my request if needed.

Under ORS 192.335, the burden of establishing that any record is exempt rests on the public body. If any records are withheld, I request that you: (1) identify each record or category withheld; (2) state the specific ORS provision (specific subsection) authorizing withholding; (3) explain how that provision applies to each specific record; and (4) confirm that all reasonably segregable non-exempt portions have been released.

Note: Oregon Public Records Law exemptions in ORS 192.345 are DISCRETIONARY — the agency may disclose records even where a technical exemption applies. I encourage {{agency_name}} to exercise its discretion to disclose these records in the public interest.

Under ORS 192.329(1), please acknowledge receipt of this request and provide an estimated production date within 5 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for this request pursuant to ORS 192.324(3). Under Oregon law, fees must be waived when disclosure "primarily benefits the general public rather than the requester."

This request primarily benefits the public because: {{public_benefit_explanation}}. These records concern {{public_interest_explanation}}, a matter of government accountability and public interest. I am {{requester_category_description}} and will disseminate the information to the public. I have no commercial purpose.

The public\'s interest in accountability for the actions of {{agency_name}} clearly outweighs any interest in charging fees for this request. I respectfully ask {{agency_name}} to invoke its mandatory fee waiver obligation under ORS 192.324(3).''',
        'expedited_language': '''I request that this public records request be processed as soon as practicable per ORS 192.329(1)\'s "without unreasonable delay" standard. Prompt production is important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if clarification would allow faster production.''',
        'notes': 'General Oregon Public Records Law template. Key OR features: (1) 5-business-day acknowledgment deadline with estimated production date (ORS 192.329(1)); (2) DISCRETIONARY exemptions in ORS 192.345 — always note that agencies may disclose; (3) district attorney petition within 60 days for discretionary exemption denials; (4) $0.25/page copy rate; (5) mandatory fee waiver when disclosure primarily benefits public (ORS 192.324(3)); (6) advance cost estimate required when fees exceed $25; (7) attorney fees for prevailing requesters; (8) burden of proof on public body; (9) public interest override applies to all discretionary exemptions; (10) use "Oregon Public Records Law" and "ORS 192" — not federal "FOIA."',
    },
    {
        'jurisdiction': 'OR',
        'record_type': 'law_enforcement',
        'template_name': 'Oregon Public Records Law Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Oregon Public Records Law Request — Law Enforcement Records, ORS 192.311 et seq.

Dear Public Records Officer:

Pursuant to the Oregon Public Records Law, ORS 192.311 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and police offense reports
- Arrest reports, booking records, and charging documents
- Use-of-force reports and documentation
- Body-worn camera and dash camera footage and associated metadata
- Dispatch records and Computer-Aided Dispatch (CAD) logs
- Officer disciplinary records (final dispositions)
- Internal investigation records for completed matters

Regarding the law enforcement exemption at ORS 192.345(12): This exemption is DISCRETIONARY under Oregon law — {{agency_name}} may disclose records even if the exemption technically applies. I encourage the agency to exercise its discretion to disclose records where the public interest in accountability supports transparency.

For any records withheld under ORS 192.345(12), please: (1) identify the specific harm enumerated in that subsection that applies to each withheld record; (2) explain why disclosure would cause that harm; and (3) confirm that all segregable non-exempt portions have been released.

Under ORS 192.335, the burden of establishing that a public record is exempt rests on the public body. Generic "active investigation" claims are insufficient — each withheld record requires specific harm documentation.

If this request is denied in whole or in part, I intend to petition the district attorney of {{county}} County under ORS 192.411 for review of any claimed discretionary exemptions.

Fees: I am willing to pay up to ${{fee_limit}}. Please provide an advance estimate if fees will exceed $25.

Please acknowledge within 5 business days per ORS 192.329(1).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived under ORS 192.324(3). These law enforcement records concern {{public_interest_explanation}}, a matter of public accountability for government actions. Disclosure primarily benefits the public by enabling scrutiny of law enforcement conduct. I am {{requester_category_description}} with no commercial purpose and will disseminate information to the public.''',
        'expedited_language': '''I request expedited processing of this public records request. These records are time-sensitive because: {{expedited_justification}}. I need them by {{needed_by_date}}.''',
        'notes': 'Oregon law enforcement public records template. Key features: (1) law enforcement exemption (ORS 192.345(12)) is DISCRETIONARY — always emphasize this and advocate for voluntary disclosure; (2) incident reports, arrest records, and booking information are generally public; (3) district attorney petition available within 60 days for discretionary exemption denials (ORS 192.411); (4) 5-business-day acknowledgment deadline; (5) mandatory fee waiver when disclosure primarily benefits public; (6) attorney fees available for prevailing requesters; (7) public interest override applies to all ORS 192.345 exemptions.',
    },
    {
        'jurisdiction': 'OR',
        'record_type': 'contracts_procurement',
        'template_name': 'Oregon Public Records Law Request — Government Contracts and Procurement',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer / Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Oregon Public Records Law Request — Government Contracts and Procurement Records, ORS 192.311 et seq.

Dear Public Records Officer:

Pursuant to the Oregon Public Records Law, ORS 192.311 et seq., I request copies of the following records relating to government contracts and procurement:

{{description_of_records}}

Specifically, I request:
- All contracts, task orders, and amendments between {{agency_name}} and {{contractor_or_vendor_name}} for {{date_range_start}} through {{date_range_end}}
- Requests for Proposals (RFPs), Invitations for Bids (IFBs), and solicitation documents
- All proposal and bid submissions from competing vendors
- Evaluation criteria, scoring sheets, and selection committee records
- Invoices, payment records, and change orders
- Correspondence relating to the above contracts

Regarding trade secret and commercial information exemption at ORS 192.345(4): This exemption is DISCRETIONARY and requires a showing of "substantial" competitive harm from disclosure. Contract prices, amounts paid with public funds, and performance metrics are public records and do not qualify as trade secrets under Oregon law. Any claimed exemption must be supported by specific evidence identifying the precise information claimed as proprietary and explaining the substantial competitive harm that would result from its disclosure.

Vendor designations of information as "confidential" or "proprietary" are not sufficient — {{agency_name}} must independently evaluate each claim and may not simply defer to vendor preferences. I encourage {{agency_name}} to exercise its discretion to disclose these records, as the public interest in government accountability for expenditure of public funds is strong.

Under ORS 192.335, the burden of establishing that any record is exempt rests on the public body.

Fees: I request a fee waiver under ORS 192.324(3) because these records primarily benefit the general public. If fees are not waived, I am willing to pay up to ${{fee_limit}}. Please provide an advance estimate if fees will exceed $25.

Please acknowledge within 5 business days per ORS 192.329(1).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived under ORS 192.324(3). These procurement records concern the expenditure of public funds by {{agency_name}}. Disclosure primarily benefits the general public by enabling scrutiny of how public money is spent. I am {{requester_category_description}} with no commercial purpose. The public interest in government accountability clearly outweighs the interest in fee collection for this request.''',
        'expedited_language': '''I request expedited processing because these procurement records relate to {{time_sensitive_reason}} and delay would harm the public interest by {{harm_from_delay}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Oregon procurement public records template. Key features: (1) trade secret exemption (ORS 192.345(4)) is DISCRETIONARY and requires "substantial" competitive harm; (2) contract prices and amounts paid with public funds are definitively public; (3) mandatory fee waiver when disclosure primarily benefits public (ORS 192.324(3)); (4) district attorney petition available within 60 days for discretionary exemption denials; (5) 5-business-day acknowledgment deadline; (6) public interest override applies to all ORS 192.345 exemptions; (7) attorney fees for prevailing requesters.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in OR_EXEMPTIONS:
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

    print(f'OR exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in OR_RULES:
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

    print(f'OR rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in OR_TEMPLATES:
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

    print(f'OR templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'OR total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_or', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
