#!/usr/bin/env python3
"""Build Wisconsin Public Records Law data: exemptions, rules, and templates.

Covers Wisconsin's Public Records Law, Wis. Stat. §§ 19.31-19.39.
Wisconsin has one of the strongest public records laws in the country, with
an explicit balancing test that creates a strong presumption in favor of
disclosure. Courts apply mandamus review and award attorney's fees plus $100
punitive damages for unjustified withholding. The "as soon as practicable
and without delay" response standard is among the most demanding in the US.

Run: python3 scripts/build/build_wi.py
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
# Wisconsin's Public Records Law applies a statutory balancing test that
# strongly favors disclosure. Under Wis. Stat. § 19.35(1)(a), records are
# presumptively subject to disclosure. Agencies invoking an exemption must
# demonstrate that the public interest in non-disclosure outweighs the
# public interest in disclosure — a high bar. Courts apply this test de novo
# and have consistently held that exemptions must be narrowly construed.
# Wisconsin's exemptions include statutory exemptions, the common law
# balancing test, and specific categorical exceptions.
# =============================================================================

WI_EXEMPTIONS = [
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(1); 5 U.S.C. § 552(b)(7)',
        'exemption_number': 'Wis. Stat. § 19.36(1)',
        'short_name': 'Records Made Confidential by Federal Law',
        'category': 'statutory',
        'description': 'Records whose disclosure is prohibited or restricted by federal law are exempt from Wisconsin\'s Public Records Law under § 19.36(1). This provision incorporates applicable federal confidentiality statutes into the Wisconsin public records framework.',
        'scope': 'Records where a specific federal law prohibits or restricts disclosure — examples include HIPAA-protected health information, FERPA-protected student records, federal tax return information under IRC § 6103, and information protected under the federal Privacy Act. The exemption is limited to what the specific federal law actually prohibits; agencies must identify the specific federal statute. General invocations of "federal law" without a specific citation are insufficient. Not all records held in connection with a federally funded program are confidential — only those specifically protected by a named federal statute.',
        'key_terms': json.dumps([
            'federal law', 'HIPAA', 'FERPA', 'federal confidentiality statute', 'Privacy Act',
            'IRC 6103', 'federally required confidentiality', 'federal preemption',
            'protected health information', 'student records',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific federal statute prohibiting disclosure — a generic "federal law" claim is insufficient',
            'Not all records related to a federal program are confidential — only those specifically named in a federal statute',
            'Aggregate and anonymized data may be public even if the underlying individual-level data is federally protected',
            'Challenge whether the specific record actually falls within the federal statute\'s scope',
            'Wisconsin\'s balancing test applies independently to any aspects of the record not covered by the federal exemption',
        ]),
        'notes': 'Wis. Stat. § 19.36(1) incorporates federal confidentiality requirements into Wisconsin\'s framework. Wisconsin courts apply it narrowly — the federal law must specifically prohibit or restrict disclosure, not merely authorize confidentiality as an option. The Wisconsin Supreme Court has held that the balancing test still applies to portions of records not covered by the specific federal exemption.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(2)',
        'exemption_number': 'Wis. Stat. § 19.36(2)',
        'short_name': 'Personnel Records',
        'category': 'privacy',
        'description': 'Employee personnel records are exempt from disclosure in Wisconsin, but this exemption is subject to significant carve-outs. Information about public employees\' names, positions, salaries, and work history are always public. The exemption protects personal data unrelated to employment performance.',
        'scope': 'Employee personnel records — to the extent they contain information whose disclosure would constitute a clearly unwarranted invasion of personal privacy under the balancing test. However, substantial carve-outs exist: the following information in personnel records is ALWAYS public in Wisconsin regardless of this exemption: (1) name; (2) current position; (3) gross compensation; (4) date of employment commencement; (5) office location; and (6) all other information relating to employment. Disciplinary records and performance evaluations involving public employees acting in their public capacity are subject to the balancing test but have generally been held public in Wisconsin courts. The exemption protects personal information unrelated to official duties.',
        'key_terms': json.dumps([
            'personnel record', 'public employee', 'salary', 'compensation',
            'disciplinary record', 'performance evaluation', 'employment history',
            'privacy', 'home address', 'Social Security number',
        ]),
        'counter_arguments': json.dumps([
            'Name, position, salary, date of hire, and office location are ALWAYS public under Wis. Stat. § 19.36(2) — no balancing required',
            'Disciplinary records for misconduct are generally public in Wisconsin under the strong balancing test presumption',
            'Wisconsin courts have held that police officer disciplinary records are public given the public accountability interest',
            'Apply Wisconsin\'s statutory balancing test: the public interest in accountability for public employee misconduct typically outweighs privacy interests',
            'Challenge blanket withholding of entire personnel files — the carve-outs are broad and agencies must release all public employment information',
        ]),
        'notes': 'Wisconsin\'s personnel records exemption under § 19.36(2) contains significant mandatory disclosure carve-outs and is also subject to the general balancing test of § 19.35(1)(a). The Wisconsin Supreme Court has consistently held that misconduct records for public employees acting in their public capacity are generally public. The balancing test strongly favors disclosure of information about official conduct.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(3)',
        'exemption_number': 'Wis. Stat. § 19.36(3)',
        'short_name': 'Law Enforcement Investigation Records',
        'category': 'law_enforcement',
        'description': 'Records of a law enforcement agency relating to an ongoing criminal investigation or intelligence gathering are potentially exempt under the balancing test, subject to specific harm-based limitations. Arrest and booking records are separately governed.',
        'scope': 'Law enforcement investigation records where disclosure would: (1) endanger the life of a witness or informant; (2) impede an ongoing criminal investigation; (3) reveal the identity of a confidential informant; or (4) interfere with a pending prosecution. All withholding is also subject to Wisconsin\'s general balancing test — even when a specific harm is present, the public interest in disclosure must be weighed. Arrest records, booking information, and records documenting the fact of police contact are generally public. Completed investigation files are subject to full balancing test analysis. Wisconsin courts have required agencies to articulate specific harm for each withheld record.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'ongoing investigation', 'pending prosecution', 'investigative technique',
            'endanger life', 'criminal intelligence', 'arrest record', 'booking record',
        ]),
        'counter_arguments': json.dumps([
            'All withholding is subject to Wisconsin\'s balancing test — even if a specific harm is present, the public interest may still favor disclosure',
            'Arrest records and booking information are generally public and not covered by this exemption',
            'Completed investigation files are subject to full balancing test — the interference rationale expires upon conclusion of prosecution',
            'Apply the statutory balancing test: in completed cases, the public accountability interest typically outweighs any remaining investigatory interests',
            'Wisconsin courts have held that the agency must articulate specific harm for each withheld record, not assert categorical exemptions',
            'Officer misconduct investigation records are especially likely to pass the balancing test in favor of disclosure',
        ]),
        'notes': 'Wisconsin\'s law enforcement exemption is always subject to the statutory balancing test of § 19.35(1)(a). The Wisconsin Supreme Court has held that the balancing test creates a strong presumption of disclosure that agencies must overcome with specific, non-speculative harm. Even where the investigation is ongoing, the court applies the balancing test to determine whether the public interest in disclosure outweighs the specific harm.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(4)',
        'exemption_number': 'Wis. Stat. § 19.36(4)',
        'short_name': 'Student Records',
        'category': 'privacy',
        'description': 'Student education records at public educational institutions are exempt from disclosure in Wisconsin, consistent with FERPA protections. Individually identifiable student information is protected while aggregate statistical data is public.',
        'scope': 'Education records directly related to individual students at public schools, colleges, and universities, including transcripts, grades, disciplinary records, enrollment information, and other personally identifiable student data. Incorporates FERPA (20 U.S.C. § 1232g) protections as a matter of Wisconsin law. Aggregate educational statistics (graduation rates, test score distributions, enrollment figures) that do not identify individual students are public. Administrative and financial records of public educational institutions are public. Records about faculty and staff are not student records and are subject to regular public records analysis.',
        'key_terms': json.dumps([
            'student record', 'education record', 'FERPA', 'student privacy',
            'transcript', 'grades', 'student disciplinary record', 'enrollment record',
            'personally identifiable information', 'public school', 'university',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate statistics that do not identify individual students are fully public',
            'Administrative and financial records of public educational institutions are public',
            'Faculty and staff records are not student records — apply the regular balancing test',
            'Systemic patterns in disciplinary records may be public even if individual records are protected',
            'Apply the Wisconsin balancing test — strong institutional misconduct interests may override student privacy in specific cases',
        ]),
        'notes': 'Wisconsin\'s student records exemption under § 19.36(4) incorporates FERPA and is subject to the statutory balancing test for any aspects not strictly required by federal law. Wisconsin courts have applied the exemption strictly to individually identifiable student data, not to all records of educational institutions.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(5)',
        'exemption_number': 'Wis. Stat. § 19.36(5)',
        'short_name': 'Law Enforcement Officer Home Addresses',
        'category': 'privacy',
        'description': 'Home addresses of law enforcement officers and certain other public safety personnel are exempt from public disclosure in Wisconsin to protect officers from targeting or harassment.',
        'scope': 'Home addresses of active law enforcement officers and certain public safety employees (firefighters, corrections officers) are exempt from disclosure. The exemption is narrow: it protects only home addresses, not other personal information. Names, job titles, badge numbers, official workplace locations, and all other employment information remain public. The exemption applies to current employees — the status of exemption for retired officers is subject to balancing test analysis. Wisconsin courts have held the exemption is address-specific.',
        'key_terms': json.dumps([
            'law enforcement officer', 'home address', 'officer privacy',
            'public safety employee', 'firefighter', 'corrections officer',
            'officer safety', 'personal address', 'residential address',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is limited to home addresses — names, official workplace addresses, badge numbers, and all other employment information are public',
            'Professional contact information and official duty station addresses are public',
            'Challenge claims that the exemption extends beyond residential address to other personal information',
            'Retired officer addresses are subject to balancing test rather than automatic exemption',
        ]),
        'notes': 'Wisconsin\'s officer home address exemption under § 19.36(5) is narrowly targeted at residential addresses. It does not create a general privacy zone around officer information. Wisconsin courts have enforced the exemption\'s specific, limited scope.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(6)',
        'exemption_number': 'Wis. Stat. § 19.36(6)',
        'short_name': 'Trade Secrets',
        'category': 'commercial',
        'description': 'Trade secrets as defined by Wis. Stat. § 134.90 (the Wisconsin Uniform Trade Secrets Act) are exempt from public disclosure when submitted by private entities to government agencies, subject to the general balancing test.',
        'scope': 'Information submitted by private entities to government agencies that qualifies as a trade secret under § 134.90: information that (1) derives independent economic value from not being generally known or readily ascertainable; and (2) is subject to reasonable measures to maintain secrecy. Government-generated information does not constitute a trade secret. Contract prices and amounts paid with public funds are generally not trade secrets and must be disclosed under Wisconsin\'s strong public accountability interest. Wisconsin\'s balancing test applies even to trade secret claims — agencies must weigh the public interest in disclosure.',
        'key_terms': json.dumps([
            'trade secret', 'Wisconsin Uniform Trade Secrets Act', 'section 134.90',
            'proprietary information', 'competitive harm', 'economic value',
            'secrecy', 'confidential business information', 'competitive advantage',
        ]),
        'counter_arguments': json.dumps([
            'Wisconsin\'s balancing test applies even to trade secret claims — the public interest in disclosure must be weighed',
            'Contract prices and amounts paid with public funds must be disclosed under Wisconsin\'s strong public accountability interest',
            'The submitter must demonstrate that information meets the § 134.90 definition — a label is not sufficient',
            'Government-generated information cannot constitute a trade secret',
            'Challenge whether the submitter actually maintained reasonable secrecy measures',
            'The agency must independently analyze trade secret claims, not simply defer to vendor designations',
        ]),
        'notes': 'Wisconsin\'s trade secret exemption under § 19.36(6) applies the § 134.90 UTSA definition but is also subject to the general balancing test of § 19.35(1)(a). Wisconsin courts have held that contract pricing information paid with public funds is presumptively public under the balancing test even when the vendor claims trade secret protection.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(8)',
        'exemption_number': 'Wis. Stat. § 19.36(8)',
        'short_name': 'Peer Review and Credentialing Records',
        'category': 'privacy',
        'description': 'Records of a peer review committee or credentialing committee of a public health care provider are exempt from public disclosure, consistent with the policy of encouraging candid peer review of medical practice.',
        'scope': 'Records of a peer review committee, credentialing committee, or quality assurance committee of a public hospital or other public health care entity that relate to the professional competence of individual health care providers. The exemption is designed to protect the candid evaluation process. Final credentialing decisions, license status, and formal disciplinary actions are generally public. Records about facility-wide policies, aggregate quality statistics, and public safety programs are not covered. The exemption does not protect individual patient records (covered separately by § 19.36(1) incorporating HIPAA).',
        'key_terms': json.dumps([
            'peer review', 'credentialing', 'quality assurance', 'medical staff',
            'hospital committee', 'provider competence', 'medical review committee',
            'health care peer review', 'clinical competence',
        ]),
        'counter_arguments': json.dumps([
            'Final credentialing decisions and license status are public',
            'Formal disciplinary actions against health care professionals are public',
            'Facility-wide quality statistics and public safety reports are public',
            'Apply the Wisconsin balancing test — strong public safety interests may override peer review confidentiality in cases of serious misconduct',
            'Challenge claims that administrative correspondence and budget records are "peer review records"',
        ]),
        'notes': 'Wisconsin\'s peer review exemption under § 19.36(8) reflects the standard policy of protecting candid peer review. However, Wisconsin\'s balancing test may require disclosure of peer review records in cases where public safety concerns are particularly acute. The Wisconsin Supreme Court has noted that the exemption does not shield systematic institutional failures from public scrutiny.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.35(1)(a); common law balancing test',
        'exemption_number': 'Wis. Stat. § 19.35(1)(a) balancing test',
        'short_name': 'Common Law Balancing Test',
        'category': 'deliberative',
        'description': 'Wisconsin\'s Public Records Law creates a statutory balancing test under § 19.35(1)(a): the public interest in disclosure is presumed to outweigh the public interest in non-disclosure unless the agency demonstrates otherwise. This test applies to all records not covered by a specific statutory exemption.',
        'scope': 'All public records not specifically exempted by statute are subject to Wisconsin\'s balancing test. The test creates a strong presumption in favor of disclosure: the agency bears the burden of demonstrating that "public policy or statute" requires non-disclosure. Under Wisconsin case law, the balancing test is applied with a strong thumb on the scale toward disclosure. Deliberative process materials, pre-decisional documents, and intra-agency communications are subject to this test. The test is not a blanket deliberative process privilege — courts have required production of many internal documents after balancing.',
        'key_terms': json.dumps([
            'balancing test', 'public interest', 'presumption of disclosure',
            'non-disclosure interest', 'deliberative process', 'predecisional',
            'intra-agency', 'public policy', 'open records presumption',
        ]),
        'counter_arguments': json.dumps([
            'The balancing test creates a strong presumption in favor of disclosure — the burden is entirely on the agency to justify withholding',
            'Courts apply de novo review of the balancing determination — no deference to the agency\'s initial assessment',
            'Vague claims that disclosure would harm agency operations are insufficient — the harm must be specific and substantial',
            'Wisconsin courts have consistently held that the public accountability interest in knowing what government did and why typically outweighs internal process interests',
            'Challenge the agency\'s characterization of the balance — request that the court conduct in camera review',
            'Attorney\'s fees and $100 punitive damages are available if the requester substantially prevails',
        ]),
        'notes': 'Wisconsin\'s statutory balancing test under § 19.35(1)(a) is the central feature that distinguishes Wisconsin\'s public records law from most states. The Wisconsin Supreme Court established the analytical framework in Hathaway v. Green Bay School District and has consistently reinforced the strong presumption of disclosure. The test applies even to records that might otherwise qualify for a common-law privilege.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(10)',
        'exemption_number': 'Wis. Stat. § 19.36(10)',
        'short_name': 'Victim and Witness Personal Information',
        'category': 'privacy',
        'description': 'Home addresses, telephone numbers, and other personal contact information of crime victims and witnesses contained in law enforcement records are exempt from public disclosure to protect victim privacy and prevent witness intimidation.',
        'scope': 'Personal contact information — home address, personal phone number, employer information — of crime victims and witnesses contained in law enforcement records. The exemption is field-specific and narrow: it protects identifying contact information that could enable harassment or retaliation, not all information about victims or witnesses. Names of crime victims and the fact of victimization are generally public. Wisconsin courts have applied this exemption narrowly to the specific data categories. The exemption reflects balancing test analysis — in cases of particularly serious privacy interests (domestic violence, sexual assault), courts have upheld broader protection.',
        'key_terms': json.dumps([
            'crime victim', 'witness', 'victim privacy', 'home address',
            'personal contact information', 'witness intimidation', 'harassment',
            'domestic violence', 'sexual assault victim', 'witness protection',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — names of victims and the fact of victimization are generally public',
            'The exemption covers contact information enabling harassment, not all victim-related information',
            'Apply the balancing test — the public interest in transparency about crime patterns may outweigh narrow privacy claims',
            'Challenge claims that entire police reports are exempt because they reference victim contact information',
        ]),
        'notes': 'Wisconsin\'s victim/witness contact information exemption is field-specific. It reflects the balancing test applied to the specific harm of enabling harassment. Wisconsin courts have required agencies to redact the specific contact data and release the remainder of incident reports and police records.',
    },
    {
        'jurisdiction': 'WI',
        'statute_citation': 'Wis. Stat. § 19.36(11)',
        'exemption_number': 'Wis. Stat. § 19.36(11)',
        'short_name': 'Security Plans for Public Infrastructure',
        'category': 'safety',
        'description': 'Specific vulnerability assessments and security plans for critical public infrastructure are exempt from disclosure where disclosure would create a specific, articulable security risk, subject to Wisconsin\'s balancing test.',
        'scope': 'Detailed vulnerability assessments, security plans, and related records for critical infrastructure (utility systems, water supply, transportation networks) and public facilities where disclosure would enable exploitation of a specific security vulnerability. The exemption applies only to records identifying specific exploitable weaknesses — general security policies, budget records, and vendor contracts are not covered. All claims are subject to Wisconsin\'s balancing test. The agency must demonstrate that the specific record reveals an exploitable vulnerability and that the public interest in security outweighs the public interest in disclosure.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'critical infrastructure',
            'security risk', 'infrastructure protection', 'public facility',
            'cyber security', 'access control', 'emergency response',
        ]),
        'counter_arguments': json.dumps([
            'Subject to Wisconsin\'s balancing test — the security interest must outweigh the disclosure interest',
            'Budget and expenditure records for security programs are public',
            'General security policies that do not reveal specific vulnerabilities are public',
            'Challenge claims that entire security contracts are exempt when only specific technical details warrant protection',
            'After vulnerabilities are remediated, the exemption no longer applies to the historical finding',
        ]),
        'notes': 'Wisconsin\'s security plans exemption is subject to the statutory balancing test. Agencies must demonstrate a specific, non-speculative security risk and must weigh it against the public interest in transparency about public infrastructure management.',
    },
]

# =============================================================================
# RULES
# Wisconsin Public Records Law, Wis. Stat. §§ 19.31-19.39
# Wisconsin's response standard — "as soon as practicable and without delay"
# — is among the most demanding in the country. $0.25/page copy fee.
# Enforcement is through mandamus in circuit court. Attorney's fees plus
# $100 punitive damages for prevailing requesters. No administrative appeal.
# =============================================================================

WI_RULES = [
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'response_standard',
        'param_value': 'as_soon_as_practicable_and_without_delay',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(4)',
        'notes': 'Wisconsin agencies must respond to public records requests "as soon as practicable and without delay." This is one of the most demanding response standards in US public records law. Courts have interpreted the standard to mean the agency must begin processing the request immediately and must produce records as quickly as reasonably possible given the agency\'s resources and the scope of the request. Unreasonable delay — even a few weeks for a modest request — can constitute a violation. Wisconsin courts have not established a safe harbor number of days; the "without delay" standard is evaluated case-by-case but leaves little room for bureaucratic sluggishness.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'written_denial_with_legal_basis_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(4)(b)',
        'notes': 'If a Wisconsin agency denies a public records request in whole or in part, the denial must be in writing and must cite the specific legal authority for the denial. Under § 19.35(4)(b), the written denial must include the statutory or common-law basis for withholding and must be provided promptly. A verbal denial without a written follow-up does not satisfy this requirement. The written denial preserves the record for potential mandamus proceedings. Courts have imposed attorney\'s fees where agencies provided inadequate written denials.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'balancing_test_presumption',
        'param_value': 'strong_presumption_of_disclosure',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.31; § 19.35(1)(a)',
        'notes': 'Wisconsin\'s Public Records Law codifies a strong presumption of disclosure: § 19.31 states that government records must be open to the public "to the greatest possible extent" and that any limitation "must be narrowly construed in light of this policy." § 19.35(1)(a) creates a statutory balancing test where the default is disclosure and the agency must demonstrate that the public interest in non-disclosure outweighs the public interest in disclosure. Wisconsin courts apply this test rigorously and have consistently rejected vague or generalized non-disclosure claims.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate_per_page',
        'param_value': '0.25',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(3)',
        'notes': 'Wisconsin agencies may charge a fee for copies of public records. The permitted fee is the actual cost of reproduction. The commonly applied default for standard paper copies is $0.25 per page. Agencies may not charge for the staff time spent locating, reviewing, or redacting records — only the actual reproduction cost is permissible. For electronic records, the actual cost is minimal or zero. Fee schedules must be reasonable and reflect actual reproduction costs. Unreasonably high fees constitute an effective denial of access and are subject to challenge.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(3)',
        'notes': 'Wisconsin agencies may not charge requesters for staff time spent locating, reviewing, or preparing records. Only the actual cost of reproduction is chargeable. This means agencies cannot impose search fees, review fees, or legal-review charges as part of a public records response. Requesters should challenge any invoice that includes labor costs beyond the per-page reproduction cost.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_agency_discretion',
        'param_value': 'agency_discretion_no_statutory_right',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(3)',
        'notes': 'Wisconsin does not provide a statutory right to fee waiver. Agencies may waive fees at their discretion. For electronic records delivered by email, the actual reproduction cost is typically zero, effectively rendering the fee waiver question moot. Requesters may argue for waivers based on public interest, media status, or nonprofit purpose, but these arguments rest on agency discretion.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'appeal_deadline',
        'param_key': 'administrative_appeal',
        'param_value': 'none',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.37',
        'notes': 'Wisconsin has NO formal administrative appeal mechanism for public records denials. There is no agency head appeal, no ombudsman, and no administrative tribunal. A requester denied access or facing unreasonable delay must seek mandamus in circuit court under § 19.37. This direct-to-court enforcement model is consistent with Wisconsin\'s strong disclosure mandate. The absence of administrative remedies means requesters should document denials and delays carefully for potential litigation.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'mandamus_in_circuit_court',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.37(1)',
        'notes': 'A requester denied access or facing unreasonable delay may seek mandamus in circuit court under § 19.37(1). The court applies de novo review of the agency\'s withholding decision. Courts may conduct in camera review of withheld records. If the requester substantially prevails, the court must award reasonable attorney\'s fees, costs, and a $100 punitive damage award. There is no formal statute of limitations, but promptness in filing is advisable. Wisconsin courts have been willing to grant expedited mandamus proceedings in time-sensitive cases.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_and_punitive_damages',
        'param_value': 'mandatory_attorney_fees_plus_100_punitive',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.37(2)',
        'notes': 'Wisconsin\'s Public Records Law mandates that a requester who substantially prevails in a records action shall receive: (1) reasonable attorney\'s fees and costs; AND (2) $100 in punitive damages. The $100 punitive damage award is unique among US state public records statutes — it is a nominal but symbolic penalty that underscores the seriousness of improper withholding. The mandatory fee-shifting (unlike discretionary awards in some states) makes litigation economically viable for all requester types. The punitive damages provision signals that Wisconsin treats unjustified withholding as a sanctionable wrong.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'burden_of_proof',
        'param_value': 'on_agency',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(1)(a)',
        'notes': 'Under Wisconsin\'s balancing test framework, the burden of demonstrating that non-disclosure is required or permissible rests entirely on the agency. The agency must show that "public policy or statute" requires withholding and must demonstrate that the public interest in non-disclosure outweighs the public interest in disclosure. Requesters need not justify their interest in the records. Wisconsin courts apply de novo review with no deference to the agency\'s initial balancing determination.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.36',
        'notes': 'Wisconsin agencies must release all non-exempt portions of records when only part of a record qualifies for withholding. Blanket withholding of documents containing some exempt content is inconsistent with Wisconsin\'s strong disclosure mandate. Agencies must redact the specifically protected portions and release the remainder. Wisconsin courts have enforced segregability requirements and have declined to uphold agency claims that segregation is "not reasonably practicable" absent a specific showing.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'requester_identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.35(1)(i)',
        'notes': 'Wisconsin agencies may not require requesters to state their purpose for requesting records. Requiring a stated purpose or justification as a condition of access is inconsistent with the presumptive right of access. Anonymous and pseudonymous requests are valid. Agencies may request contact information for delivery purposes but may not condition access on the requester\'s identity or purpose. § 19.35(1)(i) specifically prohibits agencies from conditioning access on the requester disclosing their intended use of the records.',
    },
    {
        'jurisdiction': 'WI',
        'rule_type': 'initial_response',
        'param_key': 'broad_definition_custodian',
        'param_value': 'all_entities_performing_government_function',
        'day_type': None,
        'statute_citation': 'Wis. Stat. § 19.32(1); § 19.32(2)',
        'notes': 'Wisconsin\'s Public Records Law applies to all "authorities" — a broadly defined term covering state agencies, local governments, school districts, and all bodies exercising government functions, including quasi-governmental entities and private entities performing governmental functions under contract. The definition is broader than many states. Courts have found the law applies to joint ventures, public-private partnerships, and contractor records when the entity is performing a government function. The broad jurisdictional scope is consistent with Wisconsin\'s strong disclosure policy.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

WI_TEMPLATES = [
    {
        'jurisdiction': 'WI',
        'record_type': 'general',
        'template_name': 'General Wisconsin Public Records Law Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Wisconsin Public Records Law, Wis. Stat. § 19.35 et seq.

Dear Custodian of Records:

Pursuant to Wisconsin's Public Records Law, Wis. Stat. §§ 19.31-19.39, I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or downloadable file) where available, which minimizes both cost and production time.

I am willing to pay fees reflecting the actual cost of reproduction per Wis. Stat. § 19.35(3). I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Wisconsin law. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under Wis. Stat. § 19.31, Wisconsin's Public Records Law must be "construed in every instance with a presumption of complete public access, consistent with the conduct of governmental business." Under § 19.35(1)(a), the public interest in disclosure is presumed to outweigh any competing interest in non-disclosure. The burden of overcoming this presumption rests entirely on {{agency_name}}.

If any records or portions of records are withheld, please note:
1. Any denial must be in writing and must cite the specific statutory or common-law authority for withholding (Wis. Stat. § 19.35(4)(b)).
2. Discretionary withholding requires that you apply the balancing test and demonstrate the public interest in non-disclosure outweighs the public interest in disclosure.
3. All non-exempt, segregable portions of records must be released.

Under § 19.35(4), please respond "as soon as practicable and without delay."

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived. While Wisconsin's Public Records Law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest under Wis. Stat. § 19.31.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual reproduction cost is zero.

Wisconsin's public records policy requires the "greatest possible public access." A fee waiver advances that policy.''',
        'expedited_language': '''I request the most expedited production possible under Wisconsin's "as soon as practicable and without delay" standard (Wis. Stat. § 19.35(4)). Prompt production is particularly important because:

{{expedited_justification}}

I need these records by {{needed_by_date}} because {{urgency_explanation}}. Delay will {{harm_from_delay}}.''',
        'notes': 'General-purpose Wisconsin Public Records Law template. Key Wisconsin features: (1) "as soon as practicable and without delay" is the response standard (§ 19.35(4)) — one of the most demanding in the US; (2) strong statutory balancing test with presumption of disclosure (§ 19.31, § 19.35(1)(a)); (3) no administrative appeal — mandamus in circuit court (§ 19.37); (4) mandatory attorney\'s fees plus $100 punitive damages for prevailing requesters (§ 19.37(2)); (5) $0.25/page standard copy fee; (6) written denial with specific legal authority required (§ 19.35(4)(b)); (7) broad "authority" definition covers quasi-governmental entities. Reference Wis. Stat. § 19.35, not "FOIA."',
    },
    {
        'jurisdiction': 'WI',
        'record_type': 'law_enforcement',
        'template_name': 'Wisconsin Public Records Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Law Enforcement Records, Wis. Stat. § 19.35 et seq.

Dear Custodian of Records:

Pursuant to Wisconsin's Public Records Law, Wis. Stat. §§ 19.31-19.39, I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking records
- Use-of-force reports and related documentation
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and associated metadata
- Dispatch records and CAD logs
- Written communications relating to the above
- Internal investigation records relating to the above incident

Regarding claimed exemptions: All withholding under Wisconsin's Public Records Law must satisfy the statutory balancing test of § 19.35(1)(a). Even where a specific statutory exemption applies (e.g., § 19.36(3) for ongoing investigation records), the agency must still weigh the public interest in disclosure. For each record withheld:
1. Cite the specific statutory or common-law basis.
2. Apply the balancing test and explain why non-disclosure outweighs disclosure.
3. For § 19.36(3) claims: identify the specific harm (endanger life; impede investigation; reveal informant; interfere with prosecution) and why it applies to the specific record.

[If matter appears concluded:] If prosecution has concluded or no prosecution is pending, the "ongoing investigation" rationale under § 19.36(3) is no longer available. Records of completed investigations are subject to the full balancing test, which strongly favors disclosure.

Any denial must be in writing with specific legal authority per § 19.35(4)(b). Please respond "as soon as practicable and without delay." I will pay reproduction costs at $0.25/page up to ${{fee_limit}}.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records concern {{public_interest_explanation}}, a matter of core public accountability. Electronic delivery incurs zero reproduction cost. Wisconsin's public records policy — "greatest possible public access" — supports a fee waiver here.''',
        'expedited_language': '''I request the most expedited production possible under § 19.35(4)'s "without delay" standard. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Wisconsin law enforcement records template. Key Wisconsin features: (1) ALL withholding subject to the § 19.35(1)(a) balancing test — strong presumption of disclosure; (2) § 19.36(3) law enforcement exemption is not categorical — each record requires specific harm identification AND balancing; (3) completed investigation files are subject to full balancing test; (4) officer disciplinary records are generally public under the balancing test; (5) written denial with specific statutory authority required (§ 19.35(4)(b)); (6) mandatory attorney\'s fees plus $100 punitive damages; (7) mandamus in circuit court for enforcement.',
    },
    {
        'jurisdiction': 'WI',
        'record_type': 'government_contracts',
        'template_name': 'Wisconsin Public Records Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Custodian of Records
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Government Contracts and Expenditures, Wis. Stat. § 19.35 et seq.

Dear Custodian of Records:

Pursuant to Wisconsin's Public Records Law, Wis. Stat. §§ 19.31-19.39, I request access to the following government contracts and financial records:

{{description_of_records}}

Specifically, I request:
- All contracts, amendments, and change orders between {{agency_name}} and {{vendor_or_contractor_name}} from {{date_range_start}} through {{date_range_end}}
- Solicitation documents (RFPs, IFBs, RFQs) and all responsive bids or proposals
- Bid tabulation sheets and evaluation scoring
- Invoices, payment records, and expenditure documentation
- Performance and compliance documentation

Regarding trade secret claims under § 19.36(6): Contract prices and amounts paid with public funds must be disclosed regardless of vendor trade secret claims. Wisconsin's balancing test under § 19.35(1)(a) strongly favors disclosure of contract pricing as a matter of public accountability. Any trade secret claim for specific technical materials requires the agency to apply the balancing test — the public interest in knowing how public funds are spent typically outweighs commercial confidentiality interests.

Under § 19.31, these records must be subject to the "greatest possible public access." Any denial must be in writing with specific legal authority.

I will pay reproduction costs at $0.25/page up to ${{fee_limit}}. Please respond without delay per § 19.35(4).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request a fee waiver. These records concern public expenditures — a core public accountability matter. Electronic delivery incurs zero cost. Wisconsin\'s "greatest possible public access" policy supports a waiver here.''',
        'expedited_language': '''I request expedited production under § 19.35(4)'s "without delay" standard. Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Wisconsin government contracts template. Key Wisconsin features: (1) all withholding subject to balancing test — public expenditure accountability interest is very strong; (2) trade secret exemption under § 19.36(6) requires balancing test — contract prices always public; (3) "as soon as practicable and without delay" response standard; (4) written denial with specific legal authority required; (5) mandatory attorney\'s fees plus $100 punitive damages; (6) no administrative appeal — mandamus in circuit court.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in WI_EXEMPTIONS:
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

    print(f'WI exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in WI_RULES:
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

    print(f'WI rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in WI_TEMPLATES:
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

    print(f'WI templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'WI total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_wi', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
