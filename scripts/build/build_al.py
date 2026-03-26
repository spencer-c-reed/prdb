#!/usr/bin/env python3
"""Build Alabama Open Records Act data: exemptions, rules, and templates.

Covers Alabama's Open Records Law, Ala. Code § 36-12-40 et seq.
Alabama has one of the weakest public records laws in the country — partially
codified, no specific response deadline, no fee cap in the statute, no
administrative appeal, and enforcement solely through circuit court mandamus.
Requesters face significant practical barriers. The key leverage points are
constitutional arguments and the mandamus petition standard.

Run: python3 scripts/build/build_al.py
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
# Alabama's Open Records Law, Ala. Code § 36-12-40, uses a broad "public
# character" test — records are public unless they are of "a purely private
# nature." Alabama courts also recognize common law and statutory exceptions.
# The law is relatively sparse: many exemptions derive from common law and
# scattered statutes rather than a consolidated exemptions list. This makes
# Alabama's exemption landscape more unpredictable than states with codified
# exemption lists. Additionally, Ala. Code § 36-12-41 allows agencies to deny
# requests where production would be "detrimental to the best interests of the
# state." This broad language is a significant weakness.
# =============================================================================

AL_EXEMPTIONS = [
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-12-40 ("purely private" standard)',
        'exemption_number': 'purely_private_standard',
        'short_name': 'Records of a Purely Private Nature',
        'category': 'privacy',
        'description': 'Alabama\'s Open Records Law exempts records that are "of a purely private nature" from the general public inspection requirement. This is the foundational exemption from the statute\'s text itself — records are public unless purely private. The scope of this exemption is determined by courts applying a balancing test.',
        'scope': 'Records whose content is purely personal or private in nature and bears no relationship to the agency\'s public functions or accountability. The exemption is narrow in theory — Alabama courts have stated that the Open Records Law should be broadly construed in favor of access. However, in practice agencies often over-assert this standard. Records relating to a public agency\'s official functions, spending of public funds, employment decisions, and exercise of public authority are not "purely private" regardless of how embarrassing or sensitive they may be. Personnel information about purely private personal conduct unrelated to official duties may qualify.',
        'key_terms': json.dumps([
            'purely private nature', 'private records', 'personal privacy',
            'public character', 'public function', 'official records',
            'governmental function', 'public nature', 'balancing test',
        ]),
        'counter_arguments': json.dumps([
            'Records relating to the expenditure of public funds are not "purely private" — public money is by definition a matter of public concern',
            'Employment decisions by public agencies about public employees are not purely private — they are exercises of public authority',
            'The "purely private" standard sets a high bar for withholding — the agency must demonstrate that the record has no public dimension whatsoever',
            'Alabama courts have held that records concerning official agency functions are public even if they contain some embarrassing personal information',
            'The burden is on the agency to demonstrate that a record is "purely private" — the presumption favors public access',
            'Challenge agencies that claim all personnel records are "purely private" — salary, disciplinary decisions, and job performance of public employees are public',
        ]),
        'notes': 'The "purely private nature" language from § 36-12-40 is the foundational exemption standard in Alabama. Unlike most states which have specific enumerated exemptions, Alabama\'s statute leaves the primary work to judicial interpretation of this phrase. Courts have generally held that records directly related to a public agency\'s official functions are public. See Ex parte Milteer, 494 So. 2d 729 (Ala. 1986) for early interpretation.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-12-41',
        'exemption_number': 'detrimental_to_state_interests',
        'short_name': 'Records Detrimental to Best Interests of the State',
        'category': 'deliberative',
        'description': 'Alabama\'s Open Records Law allows agencies to deny access to records where disclosure would be "detrimental to the best interests of the state." This is an extremely broad exception that has been used to withhold records on vague public interest grounds.',
        'scope': 'This exception under § 36-12-41 is the most problematic provision in Alabama\'s Open Records Law. It allows agencies to withhold records whenever they conclude that disclosure would harm "the best interests of the state" — a standard that is dangerously subjective and has been interpreted broadly by some agencies. However, Alabama courts have required agencies to articulate specific, concrete harm — not just assert a vague state interest. The exception does not authorize blanket withholding of records that are merely inconvenient or embarrassing to the agency.',
        'key_terms': json.dumps([
            'best interests of the state', 'state interests', 'detrimental',
            'public interest', 'governmental interest', 'harm to state',
            'Ala. Code § 36-12-41', 'general exemption',
        ]),
        'counter_arguments': json.dumps([
            'The "best interests of the state" standard requires articulation of specific, concrete harm — not merely agency embarrassment or inconvenience',
            'Alabama courts have held that this exception does not authorize blanket withholding of records about agency conduct or expenditures',
            'The exception cannot be used to shield records of public officer misconduct or waste of public funds — transparency in those areas IS in the best interests of the state',
            'Challenge the agency to identify the specific harm that would result from disclosure of each withheld record',
            'Vague assertions of "state interests" without specific factual basis should be challenged on mandamus as insufficient to overcome the presumption of public access',
            'Alabama\'s Constitution also provides some public access rights that cabin the scope of this exception',
        ]),
        'notes': 'Section 36-12-41 is one of the most frequently criticized provisions of Alabama\'s Open Records Law. Its broad language has been used to justify withholding records on questionable grounds. Courts applying mandamus review have required agencies to provide concrete justification, but the low enforcement bar in Alabama means agencies often go unchallenged. Requesters should explicitly challenge vague § 36-12-41 claims in any mandamus petition.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 12-21-3.1; common law',
        'exemption_number': 'attorney_client_work_product',
        'short_name': 'Attorney-Client Privilege and Work Product',
        'category': 'deliberative',
        'description': 'Communications between government agencies and their attorneys made for purposes of obtaining legal advice, and attorney work product prepared in anticipation of litigation, are exempt from public inspection under the attorney-client privilege and work product doctrine as applied to government entities.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice, and attorney work product prepared in anticipation of actual or prospective litigation. Alabama courts recognize the attorney-client privilege for government entities as an implied exception to the Open Records Law. The privilege is narrow: it covers legal advice only, not general business or policy guidance. Attorney billing records, retainer agreements, and financial arrangements with outside counsel are generally public. Facts independently known are not protected merely because communicated to an attorney.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice',
            'litigation', 'privileged communication', 'government attorney',
            'legal opinion', 'anticipation of litigation',
        ]),
        'counter_arguments': json.dumps([
            'The communication must be for legal advice specifically — not general policy or business guidance',
            'Attorney billing records and fee arrangements are generally public',
            'Waiver occurs when the agency uses the legal advice in public proceedings or discloses it to third parties',
            'Facts underlying the legal advice are not privileged — only the attorney\'s analysis and opinion',
            'Challenge claims that entire correspondence files with outside counsel are privileged',
            'Alabama courts apply the privilege narrowly given the Open Records Law\'s public access mandate',
        ]),
        'notes': 'Alabama recognizes attorney-client privilege for government entities as an implied exception to the Open Records Law. The Alabama Supreme Court has held that the privilege applies to government entities but must be narrowly construed. See State v. Jones, 616 So. 2d 949 (Ala. 1993). Billing records and routine correspondence are generally public.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-12-40; common law privacy',
        'exemption_number': 'personnel_privacy',
        'short_name': 'Personnel Files — Private Employee Information',
        'category': 'privacy',
        'description': 'Personnel files of public employees contain some purely private personal information that may be exempt from public inspection, but Alabama courts have held that information directly related to an employee\'s public duties is public.',
        'scope': 'Personnel files contain a mix of public and private information. Private personal information (medical history, home address, personal financial data unrelated to public employment) may be withheld. Information directly related to the exercise of public duties — salary, job title, disciplinary actions for official conduct, performance evaluations related to public duties, and termination decisions — is generally public. Alabama has no comprehensive personnel records exemption statute comparable to other states, so the "purely private" standard from § 36-12-40 governs each record.',
        'key_terms': json.dumps([
            'personnel file', 'public employee', 'salary', 'disciplinary record',
            'employment record', 'purely private', 'official duty',
            'public employment', 'termination', 'performance review',
        ]),
        'counter_arguments': json.dumps([
            'Salary and compensation of public employees are public under Alabama law',
            'Disciplinary records for official misconduct are public accountability records, not purely private',
            'The purely private standard from § 36-12-40 requires the agency to demonstrate that specific personnel record is purely personal and unrelated to official duties',
            'Termination decisions and the reasons for them are public records of official agency action',
            'Home addresses and truly private personal information may legitimately be withheld, but the remainder of a personnel file is public',
        ]),
        'notes': 'Alabama lacks a specific personnel file exemption statute for most public employees. The "purely private" standard from § 36-12-40 governs. Courts have consistently held that compensation, official conduct, and employment decisions of public employees are public. Alabama Code § 36-26-13 provides some civil service personnel record protections but does not broadly exempt such records from public access.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 26-14-8; Ala. Code § 38-2-6',
        'exemption_number': 'social_welfare_child_abuse',
        'short_name': 'Child Abuse and Social Welfare Case Records',
        'category': 'privacy',
        'description': 'Records of child abuse investigations, child welfare case files, and records of individuals receiving public welfare benefits are exempt from public disclosure under specific statutory confidentiality provisions.',
        'scope': 'Child abuse investigation records under § 26-14-8 are specifically protected from disclosure except to enumerated parties (courts, law enforcement, medical professionals, etc.). Public welfare case files and records identifying individual beneficiaries of public assistance programs are also protected under § 38-2-6. Aggregate statistics, program data, and administrative records of social service agencies are public. The exemption applies to individually identifiable beneficiary and client records, not to agency operations.',
        'key_terms': json.dumps([
            'child abuse', 'child welfare', 'DHR', 'Department of Human Resources',
            'welfare case', 'social services', 'public assistance',
            'beneficiary records', 'case file', 'child protective services',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate program statistics are not covered — the exemption protects individuals, not program data',
            'Administrative policies, audit findings, and operational records of DHR are public',
            'Final court orders in child welfare proceedings are generally public',
            'Challenge claims that all records from DHR are exempt — only individually identifiable client records qualify',
        ]),
        'notes': 'Alabama\'s child abuse and welfare record exemptions are among the most firmly established in the state. § 26-14-8 is a specific statutory confidentiality provision that operates alongside the Open Records Law. However, agency operational records, policies, and administrative actions remain public.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-12-40; common law',
        'exemption_number': 'deliberative_process',
        'short_name': 'Deliberative Process — Predecisional Documents',
        'category': 'deliberative',
        'description': 'Predecisional deliberative documents — internal drafts, recommendations, and advisory opinions not yet adopted as agency policy — are recognized as an implied exemption under Alabama common law, though they are not specifically codified in the Open Records statute.',
        'scope': 'Internal agency drafts, advisory memoranda, and predecisional deliberative documents that contain opinions and recommendations not yet adopted as the agency\'s final position. Alabama recognizes this exemption through common law and judicial interpretation of the "purely private" and "detrimental to state interests" standards in §§ 36-12-40 and 36-12-41. The exemption is narrow: factual material and adopted agency policies are public regardless of the deliberative process claim. The burden is on the agency to demonstrate that specific documents are predecisional and deliberative.',
        'key_terms': json.dumps([
            'deliberative process', 'predecisional', 'draft document', 'advisory opinion',
            'internal deliberation', 'recommendation', 'working paper',
            'intra-agency communication', 'policy deliberation',
        ]),
        'counter_arguments': json.dumps([
            'Alabama\'s deliberative process exemption is not codified — it derives from common law and is narrowly recognized',
            'Factual material within deliberative documents must be segregated and released',
            'Once a draft or recommendation is adopted as agency policy, the exemption expires',
            'Final agency decisions and adopted policies are always public',
            'Challenge claims that entire files are deliberative — require specific identification of each predecisional opinion-based portion',
            'Alabama courts have not established a clear, consistent deliberative process exemption — challenge its application aggressively',
        ]),
        'notes': 'Alabama\'s deliberative process protection is judicially implied, not codified. This makes it more vulnerable to challenge than in states with explicit statutory exemptions. Courts have not developed a robust body of law on this point, which cuts both ways — agencies have less authority to rely on it, but requesters also have less clear precedent supporting mandatory disclosure of deliberative documents.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-21-24; § 36-21-25',
        'exemption_number': 'law_enforcement_investigative_files',
        'short_name': 'Law Enforcement Investigative Files',
        'category': 'law_enforcement',
        'description': 'Investigative files and reports compiled by law enforcement agencies for law enforcement purposes are generally protected from mandatory disclosure under Alabama common law and specific provisions of the Law Enforcement Planning Agency statutes.',
        'scope': 'Records compiled during ongoing law enforcement investigations where disclosure would: identify confidential informants, interfere with prosecution, compromise investigative techniques, or endanger lives. The exemption is not codified comprehensively in the Open Records statute itself — it derives from common law and scattered statutory provisions. Arrest records, conviction records, and final court records are public. Incident reports documenting the existence of crimes are generally public. The exemption is strongest for active, ongoing investigation files.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'investigative file', 'criminal investigation',
            'confidential informant', 'active investigation', 'investigative technique',
            'arrest record', 'conviction record', 'incident report',
        ]),
        'counter_arguments': json.dumps([
            'Arrest records and booking information are public under Alabama law',
            'Incident reports documenting crimes are generally public',
            'Once prosecution is complete or investigation closed, the active investigation rationale disappears',
            'The exemption is not clearly codified in Alabama — agencies relying on implied common law exemptions bear a higher burden of justification',
            'Administrative records, budget, and policy documents of law enforcement agencies are public',
            'Use-of-force reports and officer conduct records that document completed incidents are public',
        ]),
        'notes': 'Alabama\'s law enforcement records exemption is less clearly defined than in most states because the Open Records statute does not contain a comprehensive law enforcement exemption. Agencies rely on a combination of common law, § 36-12-41\'s "state interests" language, and specific provisions scattered throughout the Alabama Code. This creates uncertainty for requesters but also limits the agency\'s ability to claim a clearly established right to withhold.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 40-2A-10',
        'exemption_number': 'tax_records',
        'short_name': 'State Tax Return Information',
        'category': 'statutory',
        'description': 'State tax return information and related taxpayer data held by the Alabama Department of Revenue is specifically exempt from public disclosure under § 40-2A-10\'s taxpayer bill of rights confidentiality provisions.',
        'scope': 'Tax returns, tax application data, audit work papers, and related financial information submitted by individual or business taxpayers to the Alabama Department of Revenue. Covers state income tax, business privilege tax, and other state tax filings. Aggregate tax statistics and revenue data published by the Department are public. Tax delinquency notices and final court judgments in tax collection cases that become part of the public court record are generally accessible. Information about the Department\'s own administrative operations and enforcement programs is public.',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Alabama Department of Revenue',
            'taxpayer records', 'state tax', 'income tax', 'business privilege tax',
            'tax confidentiality', 'Ala. Code § 40-2A-10',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and de-identified data are public',
            'Tax delinquency notices and final court judgments in tax cases are accessible through court records',
            'Information about the Department\'s enforcement programs and policies is public',
            'Challenge whether specific records are actually "tax return information" vs. general regulatory correspondence',
        ]),
        'notes': 'Alabama\'s tax record confidentiality under § 40-2A-10 is one of the most clearly established exemptions in the state. It applies broadly to taxpayer information but not to the Department\'s own administrative operations.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 22-11A-2; common law',
        'exemption_number': 'medical_records',
        'short_name': 'Medical and Health Records',
        'category': 'privacy',
        'description': 'Individually identifiable medical and health records held by government agencies — including public hospitals, health departments, and correctional facilities — are exempt from public inspection under specific statutory confidentiality provisions and common law privacy.',
        'scope': 'Individually identifiable medical records, health records, communicable disease reports, and similar sensitive health information held by public entities. Specific statutes protect communicable disease records (§ 22-11A-2), mental health treatment records, and correctional medical records. Aggregate public health statistics and program data are public. Policies, procedures, and budget records of public health agencies are public.',
        'key_terms': json.dumps([
            'medical record', 'health record', 'patient privacy', 'HIPAA',
            'communicable disease', 'mental health record', 'treatment record',
            'individually identifiable', 'public health',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate health statistics and de-identified data are not covered',
            'Policies and procedures of public health agencies are public',
            'Budget and administrative records of health agencies are fully public',
            'Challenge whether specific records actually contain individually identifiable health information',
        ]),
        'notes': 'Alabama\'s medical record protections derive from multiple sources: HIPAA for covered entities, specific disease-reporting statutes (§ 22-11A-2 for communicable diseases), and common law privacy principles. The protections are strongest for individually identifiable records.',
    },
    {
        'jurisdiction': 'AL',
        'statute_citation': 'Ala. Code § 36-12-40; trade secret common law',
        'exemption_number': 'trade_secrets',
        'short_name': 'Trade Secrets and Proprietary Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and confidential commercial information submitted by private entities to government agencies may be withheld as "purely private" under § 36-12-40 or as contrary to the "best interests of the state" under § 36-12-41, in addition to specific trade secret protections under Alabama\'s trade secrets statute.',
        'scope': 'Commercial and financial information submitted by private entities to government agencies that qualifies as trade secrets under Alabama\'s trade secret law (Ala. Code § 8-27-2, the Alabama Trade Secrets Act) or whose disclosure would harm the submitting entity\'s competitive position. Alabama\'s Open Records Law does not contain a specific trade secret exemption — agencies rely on the "purely private" standard or § 36-12-41 for this protection. Contract amounts and expenditures of public funds are generally not considered proprietary.',
        'key_terms': json.dumps([
            'trade secret', 'proprietary information', 'competitive harm',
            'Alabama Trade Secrets Act', 'commercial information', 'financial information',
            'Ala. Code § 8-27-2', 'confidential business',
        ]),
        'counter_arguments': json.dumps([
            'Amounts paid with public funds are public regardless of vendor trade secret claims',
            'Alabama\'s Open Records statute does not have a specific trade secret exemption — agencies must rely on general standards',
            'The burden is on the agency (or the submitting party) to demonstrate actual competitive harm, not just assert confidentiality',
            'Publicly available information cannot qualify as a trade secret',
            'Contract terms and deliverables for public contracts are generally public',
        ]),
        'notes': 'Alabama\'s Open Records Law lacks a specific trade secret exemption, making this protection weaker and less predictable than in states with explicit exemptions. Agencies typically rely on § 36-12-40\'s "purely private" language or § 36-12-41\'s "state interests" language. The Alabama Trade Secrets Act (§ 8-27-2 et seq.) may support withholding in some circumstances but does not create a categorical FOIA exemption.',
    },
]

# =============================================================================
# RULES
# Alabama Open Records Law, Ala. Code § 36-12-40 et seq.
# Key features: no statutory response deadline; no statutory fee cap
# (only "reasonable" fees); no administrative appeal; circuit court mandamus
# is the sole enforcement mechanism; no per diem penalties; no attorney's fees
# provision; no mandatory written denial requirement.
# Alabama has one of the weakest enforcement mechanisms in the country.
# =============================================================================

AL_RULES = [
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'response_deadline_days',
        'param_value': 'none_statutory',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40',
        'notes': 'Alabama\'s Open Records Law contains NO specific statutory response deadline. The statute simply provides that records are open for inspection during "business hours." Courts have interpreted this to require "prompt" or "reasonable" response, but there is no specific number of days. In practice, agencies can delay indefinitely without clear legal consequences short of a mandamus petition. Requesters should specify a reasonable deadline in their request (10 business days is defensible) and note that unreasonable delay will be treated as a constructive denial supporting mandamus. This is one of Alabama\'s most significant weaknesses as a public records law.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'prompt_response_standard',
        'param_value': 'prompt_and_reasonable',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40; Ex parte Milteer, 494 So. 2d 729 (Ala. 1986)',
        'notes': 'Although there is no statutory deadline, Alabama courts have held that public officials must respond to records requests "promptly" and within a "reasonable time." What constitutes reasonable time depends on the volume of records, the complexity of the request, and the agency\'s workload. Requesters should set a specific deadline in their request (e.g., 10 business days) and document any delay. Unreasonable delay is treated as a constructive denial that supports a mandamus petition.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'fee_cap',
        'param_key': 'fee_standard',
        'param_value': 'reasonable_cost',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40; § 36-12-43',
        'notes': 'Alabama\'s Open Records Law sets NO specific fee cap. The standard is that fees must be "reasonable" and reflect the actual cost of reproduction. Agencies may charge for copying but not for unlimited staff time. Ala. Code § 36-12-43 provides that agencies may establish fee schedules. Many agencies charge $0.25-$1.00 per page, and some charge significant amounts for staff research time. There is no statutory right to a free copy. The absence of a fee cap is a significant weakness — agencies can impose fees that effectively block access. Requesters should challenge fees that exceed actual reproduction costs as inconsistent with the Open Records Law\'s access mandate.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_available',
        'param_value': 'discretionary_no_statutory_right',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40',
        'notes': 'Alabama provides no statutory right to a fee waiver for any class of requesters. Agencies have discretion to reduce or waive fees but are not required to do so. Requesters may argue that fees should be waived for records of significant public interest, but there is no legal mechanism to compel a waiver. For electronic records that can be delivered by email, the actual reproduction cost is zero, which effectively eliminates fees for digital records.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40 et seq.',
        'notes': 'Alabama has NO administrative appeal mechanism for Open Records denials. There is no agency head review, no Attorney General opinion process, no ombudsman, and no administrative tribunal. A requester denied access — or facing unreasonable delay — must go directly to circuit court to seek a writ of mandamus. This makes Alabama one of the most litigation-dependent states for public records enforcement, and the cost of mandamus proceedings is a significant barrier to access for individual requesters.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_court_mandamus',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40; Rule 21, Ala. R. App. P.',
        'notes': 'The sole formal enforcement mechanism for Alabama Open Records denials is a petition for writ of mandamus in circuit court. The requester must demonstrate: (1) a clear legal right to the records; (2) a corresponding legal duty by the official to provide them; (3) no other adequate remedy at law. Alabama courts have held that public officials have a ministerial duty to provide access to public records, making mandamus the appropriate remedy. The standard of review is whether the denial was arbitrary and capricious. Mandamus is an extraordinary remedy — the process is complex, time-consuming, and expensive compared to states with simpler enforcement mechanisms.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'penalty',
        'param_key': 'statutory_penalty',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40 et seq.',
        'notes': 'Alabama\'s Open Records Law provides NO per diem penalties, civil fines, or statutory damages for wrongful withholding of records. There is also no attorney\'s fees provision in the statute. This is one of the most significant weaknesses of Alabama\'s public records law — an agency that wrongfully withholds records faces no monetary consequences beyond being ordered to produce them by a court. The lack of fee-shifting also means requesters bear the full cost of mandamus proceedings even when they prevail. Requesters should consider whether constitutional arguments (1st Amendment, due process) might support fee awards in egregious cases.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'penalty',
        'param_key': 'criminal_penalty',
        'param_value': 'none_in_open_records_statute',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40 et seq.',
        'notes': 'Unlike some states, Alabama\'s Open Records Law does not include criminal penalties for willful denial of access to public records. While other Alabama statutes may impose criminal penalties for specific types of record destruction or tampering, the Open Records Law itself does not criminalize willful withholding. This further reduces the deterrent value of the statute compared to states like Louisiana where criminal penalties are possible.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'written_request_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40',
        'notes': 'Alabama\'s Open Records Law does not explicitly require written requests — the statute provides for inspection during "business hours" for any person. However, written requests are strongly recommended to: (1) document the scope of the request; (2) establish a paper trail of the request date; (3) create evidence of delay or denial for mandamus proceedings. Email requests are generally accepted. Many agencies have established procedures requiring written requests as an administrative matter, which courts have generally upheld as reasonable.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true_with_caveats',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40',
        'notes': 'Alabama\'s Open Records Law provides access to "any citizen of Alabama." Courts have generally construed "citizen" broadly and have not required proof of Alabama citizenship as a condition of access. In practice, agencies rarely enforce citizenship requirements. However, requesters should be aware that the "citizen" language could theoretically be used to deny access to non-residents or non-citizens, though this interpretation has not been widely adopted. Anonymous requests are generally accepted in practice.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency_in_theory',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40; Ex parte Milteer',
        'notes': 'In theory, the burden of demonstrating that records are exempt from disclosure rests on the agency or public official claiming an exception. Alabama courts have stated that the Open Records Law creates a presumption in favor of public access. However, in practice the weak enforcement mechanisms (mandamus only, no fees) mean agencies face little practical pressure to justify withholding. The burden of proof formally rests on the agency but the requester bears the cost of enforcing that burden through mandamus proceedings.',
    },
    {
        'jurisdiction': 'AL',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'implied_yes',
        'day_type': None,
        'statute_citation': 'Ala. Code § 36-12-40',
        'notes': 'Alabama\'s statute does not explicitly require segregation of exempt and non-exempt portions of records, but courts applying general open records principles have held that agencies cannot withhold entire records when only portions are exempt. Requesters should explicitly request segregation of exempt and non-exempt portions in any request. Alabama\'s lack of an explicit segregability requirement is another weakness compared to states like Washington or California with clear statutory segregation mandates.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

AL_TEMPLATES = [
    {
        'jurisdiction': 'AL',
        'record_type': 'general',
        'template_name': 'General Alabama Open Records Act Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Ala. Code § 36-12-40

Dear Custodian of Records:

Pursuant to the Alabama Open Records Law, Ala. Code § 36-12-40 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in identifying the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or download link) where available, which eliminates reproduction costs.

For paper copies, I am willing to pay the reasonable cost of reproduction consistent with Ala. Code § 36-12-40 and § 36-12-43. I am not willing to pay for unlimited staff research time — only actual reproduction costs. If fees will exceed ${{fee_limit}}, please notify me before proceeding so I may refine my request or make payment arrangements.

Under Ala. Code § 36-12-40, all public records are presumptively open for inspection unless they are "of a purely private nature" or their disclosure would be clearly contrary to a specific and articulable state interest. The burden of demonstrating that any exception applies rests on {{agency_name}}.

If any records are withheld, I request: (1) identification of each withheld record; (2) the specific legal basis for withholding (statutory citation or legal doctrine); (3) a description of the record sufficient to evaluate the claimed exemption; and (4) confirmation that all non-exempt, segregable portions of partially withheld records have been provided.

Please respond within 10 business days. If a response cannot be provided within that period, please notify me in writing of the reason for the delay and the expected production date. Unreasonable delay will be treated as a constructive denial supporting a petition for writ of mandamus.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that all fees associated with this request be waived or minimized. Alabama\'s Open Records Law provides for access at reasonable reproduction cost. To the extent records are available in electronic format and can be delivered by email, the actual reproduction cost is zero and no fee is appropriate.

For any paper copies, I ask that {{agency_name}} limit fees to the actual per-page reproduction cost, as the Open Records Law does not authorize charges for unlimited staff research time.

These records relate to {{public_interest_explanation}}, a matter of public accountability. Excessive fees that effectively block access are inconsistent with the Open Records Law\'s fundamental purpose.''',
        'expedited_language': '''I request that this Open Records request be processed as promptly as possible. While Alabama law does not specify a response deadline, courts have required "prompt" responses within a "reasonable time." I need these records by {{needed_by_date}} because {{urgency_explanation}}.

Please contact me immediately if there are questions that would allow faster processing of this request.''',
        'notes': 'General Alabama Open Records template. Critical weaknesses to know: (1) no statutory response deadline — courts require only "prompt" response; (2) no statutory fee cap — fees must be "reasonable"; (3) no administrative appeal — mandamus in circuit court is the only formal remedy; (4) no per diem penalties; (5) no attorney\'s fees provision; (6) the "detrimental to best interests of state" exception under § 36-12-41 is dangerously broad. Always set a deadline in the request letter (10 business days) and state explicitly that unreasonable delay will be treated as a constructive denial. For important requests, be prepared to file mandamus if the agency delays or denies without adequate justification.',
    },
    {
        'jurisdiction': 'AL',
        'record_type': 'law_enforcement',
        'template_name': 'Alabama Open Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Law Enforcement Records, Ala. Code § 36-12-40

Dear Custodian of Records:

Pursuant to the Alabama Open Records Law, Ala. Code § 36-12-40 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request specifically includes:
- Incident reports and offense reports
- Arrest reports and booking records
- Use-of-force reports and related documentation
- Officer disciplinary records for involved personnel
- Dispatch records and CAD logs
- Body camera footage and associated metadata

Regarding claimed exemptions: Alabama courts have held that arrest records, booking information, and records of completed law enforcement actions are public records. For any withheld records, I request that {{agency_name}}: (1) identify each withheld document; (2) state the specific legal basis — by statute or clearly established common law doctrine — justifying withholding; and (3) confirm that all non-exempt, segregable portions of partially withheld records are produced.

The burden of demonstrating any exception to the Open Records Law rests on {{agency_name}}. A general claim that records are "part of an investigation" or "detrimental to state interests" without specific, articulable justification is insufficient to overcome the presumption of public access.

I am willing to pay reasonable reproduction costs, up to ${{fee_limit}} total.

Please respond within 10 business days. Unreasonable delay will be treated as a constructive denial.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived or limited to actual reproduction costs for this request. These records concern {{public_interest_explanation}}, a matter of public accountability for government law enforcement. Electronic delivery incurs no reproduction cost.''',
        'expedited_language': '''I request prompt processing of this request given the public accountability significance of law enforcement records. I need these records by {{needed_by_date}} for {{expedited_justification}}. Please contact me immediately with any questions.''',
        'notes': 'Alabama law enforcement records template. Key points: (1) Alabama\'s Open Records Law has no specific law enforcement exemption — agencies rely on § 36-12-40\'s "purely private" standard, § 36-12-41\'s "state interests" language, or common law; (2) arrest records and booking information are well-established public records under Alabama law; (3) body camera footage should be requested specifically; (4) mandamus is the enforcement mechanism — Alabama has no equivalent to other states\' law enforcement records acts; (5) document all communications carefully as evidence for potential mandamus proceedings.',
    },
    {
        'jurisdiction': 'AL',
        'record_type': 'government_contracts',
        'template_name': 'Alabama Open Records Request — Government Contracts and Expenditures',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Open Records Request — Government Contracts and Expenditure Records, Ala. Code § 36-12-40

Dear Custodian of Records:

Pursuant to the Alabama Open Records Law, Ala. Code § 36-12-40 et seq., I request the following records relating to government contracts and expenditures:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, and amendments between {{agency_name}} and {{contractor_vendor_name}} from {{date_range_start}} through {{date_range_end}}
- Invoices, purchase orders, and payment records for these contracts
- Communications relating to contract negotiation and performance
- Any audits or performance assessments of the contractor's work

Government expenditure records are quintessentially public in character under Alabama law — they are the direct exercise of public authority and the disposition of public funds. Records of how state money is spent are not "of a purely private nature" under § 36-12-40 and their disclosure is not "detrimental to the best interests of the state" under § 36-12-41 — to the contrary, accountability for public spending IS in the best interests of the state.

Any vendor claim of trade secret or proprietary status for contract amounts or payment data should be rejected — amounts paid with public funds are public regardless of vendor confidentiality designations.

I am willing to pay reasonable reproduction costs, up to ${{fee_limit}} total. Electronic delivery is preferred and incurs no reproduction cost.

Please respond within 10 business days.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived for these government contracts and expenditure records. Records of public spending are at the core of governmental accountability — they concern the exercise of public authority and the disposition of taxpayer funds. Electronic delivery incurs no reproduction cost. Charging fees for fundamental accountability records is inconsistent with the Open Records Law\'s access mandate.''',
        'expedited_language': '''I request prompt processing of this government spending records request within a reasonable time under Alabama law. I need these records by {{needed_by_date}} for {{expedited_justification}}. Please contact me with any questions.''',
        'notes': 'Alabama government contracts template. Key point: government expenditure records are the clearest case of "public character" under § 36-12-40 — they are among the most firmly established public records in Alabama. Agencies rarely succeed in withholding basic contract amounts and payment records under either the "purely private" or "state interests" standards. Vendor confidentiality claims about amounts paid with public funds are especially weak under Alabama law.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in AL_EXEMPTIONS:
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

    print(f'AL exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in AL_RULES:
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

    print(f'AL rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in AL_TEMPLATES:
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

    print(f'AL templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'AL total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_al', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
