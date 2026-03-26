#!/usr/bin/env python3
"""Build Indiana Access to Public Records Act data: exemptions, rules, and templates.

Covers Indiana's Access to Public Records Act (APRA), IC 5-14-3.
Indiana has a tiered response system: 24 hours for informal requests and
7 calendar days for formal written requests. The Public Access Counselor (PAC)
provides advisory opinions — persuasive but not binding. Attorney's fees are
available. Copy fees are $0.10/page for paper. Electronic records must be
provided in the format maintained unless the agency chooses a different format.

Run: python3 scripts/build/build_in.py
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
# Indiana's APRA, IC 5-14-3, divides records into three categories:
# (1) records that must be disclosed (IC 5-14-3-3);
# (2) records that are declared confidential by statute (IC 5-14-3-4(a));
# (3) records that may be withheld at agency discretion (IC 5-14-3-4(b)).
# The discretionary withholding category is notable — Indiana agencies have
# discretion to withhold certain records even if they are not strictly exempt,
# but courts apply a balancing test and may compel production where the public
# interest outweighs the harm from disclosure.
# =============================================================================

IN_EXEMPTIONS = [
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(a)(9)',
        'exemption_number': 'IC 5-14-3-4(a)(9)',
        'short_name': 'Personal Information — SSN, Financial Data',
        'category': 'privacy',
        'description': 'Records declared confidential by state or federal statute, including those containing Social Security numbers, financial account numbers, and similar personally identifying information protected by applicable law.',
        'scope': 'Specific personal identifying data — Social Security numbers, financial account numbers, PINs, and similar data — that is protected by applicable federal law (e.g., Privacy Act) or Indiana statute. The exemption is field-specific: agencies must redact the protected data and release the remainder of the record. Does not protect names, addresses, job titles, or general biographical information. Public employees\' names, salaries, and employment information remain public. Indiana courts have applied this exemption narrowly to the specific data categories rather than entire documents.',
        'key_terms': json.dumps([
            'Social Security number', 'SSN', 'financial account', 'personal information',
            'identity theft', 'bank account', 'personally identifiable information', 'PII',
            'account number', 'PIN', 'federal confidentiality statute',
        ]),
        'counter_arguments': json.dumps([
            'The exemption is field-specific — agencies must redact protected fields and release the remainder',
            'Public employee names, salaries, job titles, and positions are always public under IC 5-14-3-3(b)',
            'Challenge overbroad redactions where the agency removed non-exempt contextual information',
            'Information publicly available through other channels cannot be withheld under this exemption',
            'The Indiana Public Access Counselor has consistently held that agencies cannot withhold entire records merely because they contain some protected fields',
        ]),
        'notes': 'Indiana\'s APRA provides that records made confidential by state or federal statute are exempt under IC 5-14-3-4(a)(9). The exemption is limited to what the underlying statute protects — agencies cannot expand the exemption beyond the statute\'s scope. Indiana courts apply a strict interpretation that favors disclosure of non-exempt portions.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(1)',
        'exemption_number': 'IC 5-14-3-4(b)(1)',
        'short_name': 'Investigatory Records of Law Enforcement',
        'category': 'law_enforcement',
        'description': 'Investigatory records compiled by a law enforcement agency are among the discretionary exemptions — agencies MAY withhold them but are not required to. Disclosure must be withheld only to the extent that disclosure would: reveal the identity of a confidential informant; reveal investigative techniques; endanger life; or interfere with pending prosecution.',
        'scope': 'Law enforcement investigatory records where disclosure would cause specific, enumerated harm: (1) reveal confidential informant identity; (2) reveal investigative techniques; (3) endanger any person\'s life; or (4) interfere with a pending prosecution. Indiana\'s characterization of this as a "discretionary" exemption (IC 5-14-3-4(b)) means that even when one of the enumerated harms is present, the agency has discretion to release. Arrest records, 911 logs, dispatch records, and incident reports documenting the fact of an incident are generally public under IC 5-14-3-3. Once prosecution concludes or no prosecution is pursued, the interference rationale evaporates.',
        'key_terms': json.dumps([
            'law enforcement investigation', 'criminal investigation', 'confidential informant',
            'ongoing investigation', 'pending prosecution', 'investigative technique',
            'endanger life', 'arrest record', 'incident report', 'CAD log',
        ]),
        'counter_arguments': json.dumps([
            'This is a DISCRETIONARY exemption under IC 5-14-3-4(b) — agencies may release even if technically exempt',
            'Arrest records, incident reports, and booking records are mandatory disclosures under IC 5-14-3-3',
            'Once prosecution concludes, the "pending prosecution" basis for withholding evaporates',
            'The agency must articulate a specific harm — not a categorical claim — for each withheld record',
            'Factual material not implicating any enumerated harm must be segregated and released',
            'The Indiana Public Access Counselor has routinely found that closed investigation records should be disclosed',
            'Body camera footage is generally public in Indiana absent specific enumerated harm',
        ]),
        'notes': 'Indiana\'s APRA uniquely characterizes law enforcement investigatory records as a discretionary (not mandatory) exemption. This means agencies have the authority to release even technically exempt records. The Indiana Public Access Counselor has issued numerous opinions encouraging agencies to release completed investigation materials. IC 5-14-3-3(b)(1) explicitly requires disclosure of arrest records, making them mandatory disclosures regardless of investigation status.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(2)',
        'exemption_number': 'IC 5-14-3-4(b)(2)',
        'short_name': 'Deliberative Material — Pre-Decisional',
        'category': 'deliberative',
        'description': 'Preliminary drafts, notes, memoranda, and other pre-decisional deliberative materials are a discretionary exemption — agencies MAY withhold them but are not required to. Only opinion-based and predecisional content qualifies; factual material must be segregated and released.',
        'scope': 'Preliminary drafts, notes, recommendations, and intra-agency memoranda that: (1) are predecisional (created before a final agency decision); and (2) contain opinion, recommendation, or deliberative content rather than purely factual material. Indiana\'s characterization of this as a discretionary exemption means agencies may release deliberative documents even when technically exempt. Final agency decisions, rules, adopted policies, and "working law" are not covered. Factual data embedded in deliberative documents must be segregated and released. Once a document is adopted as the agency\'s final position, the exemption no longer applies.',
        'key_terms': json.dumps([
            'preliminary draft', 'deliberative process', 'predecisional', 'intra-agency memorandum',
            'working paper', 'recommendation', 'advisory opinion', 'policy deliberation',
            'draft document', 'opinion on policy matter',
        ]),
        'counter_arguments': json.dumps([
            'This is a DISCRETIONARY exemption under IC 5-14-3-4(b) — agencies may release even if technically exempt',
            'Purely factual material in deliberative documents must be segregated and released',
            'Once adopted as the agency\'s final position, the document loses its predecisional character',
            '"Working law" — the standards actually applied by the agency — must be disclosed',
            'Challenge claims that entire documents are deliberative when only recommendation sections qualify',
            'Indiana courts have held that the exemption does not protect facts from disclosure',
        ]),
        'notes': 'Indiana\'s deliberative process exemption is discretionary under IC 5-14-3-4(b)(2). The Indiana Public Access Counselor has taken the position that agencies should err toward disclosure of deliberative materials when the public interest is strong. The factual/opinion distinction is critical under Indiana law.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(a)(8)',
        'exemption_number': 'IC 5-14-3-4(a)(8)',
        'short_name': 'Attorney-Client Privilege',
        'category': 'deliberative',
        'description': 'Records protected by attorney-client privilege or work product doctrine are among the mandatory exemptions — agencies must withhold these records. The privilege applies to government entities and their attorneys in the same manner as private clients.',
        'scope': 'Confidential communications between government agencies and their attorneys made for the purpose of obtaining legal advice. Covers attorney-client communications and attorney work product prepared in anticipation of litigation. The privilege requires that the communication be for legal (not business or policy) advice, made in confidence, and not waived. Attorney billing records and general retainer terms are generally not privileged. Facts independently known to the agency are not privileged merely because they were communicated to an attorney. Indiana courts apply the privilege to government entities but with sensitivity to the public records presumption.',
        'key_terms': json.dumps([
            'attorney-client privilege', 'work product', 'legal advice', 'in anticipation of litigation',
            'privileged communication', 'legal opinion', 'confidential communication',
            'government attorney', 'corporation counsel',
        ]),
        'counter_arguments': json.dumps([
            'The communication must seek legal advice, not business or policy guidance — the latter is not privileged',
            'Attorney billing records and invoices are generally public',
            'Waiver occurs when the agency discloses the content in public proceedings or to third parties outside the privilege',
            'Facts independently known to the agency are not privileged merely because they were shared with counsel',
            'Challenge whether the agency has constructively waived by acting on the advice in public proceedings',
            'Final legal settlements and consent decrees are public regardless of underlying privileged communications',
        ]),
        'notes': 'Indiana\'s APRA lists attorney-client privilege as a mandatory confidentiality provision under IC 5-14-3-4(a)(8). Unlike the discretionary exemptions, agencies must withhold attorney-client communications. However, Indiana courts have interpreted the privilege narrowly for government entities, consistent with the strong public disclosure presumption in the APRA.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(a)(9); IC 6-8.1-7-1',
        'exemption_number': 'IC 5-14-3-4(a)(9); IC 6-8.1-7-1',
        'short_name': 'Tax Return Information',
        'category': 'statutory',
        'description': 'State tax return information submitted to or held by the Indiana Department of Revenue is confidential under IC 6-8.1-7-1, which is incorporated into APRA as a statutory confidentiality provision.',
        'scope': 'Tax returns, tax application data, and related financial information submitted by individual or business taxpayers to the Indiana Department of Revenue. Covers income tax, sales tax, financial institutions tax, and related state tax filings. Aggregate tax revenue statistics, enforcement program information, and records about the Department\'s own operations are public. Final court judgments in tax collection cases and public tax liens are public. IC 6-8.1-7-1 establishes the specific confidentiality rule within the tax code, incorporated into APRA by IC 5-14-3-4(a)(9).',
        'key_terms': json.dumps([
            'tax return', 'tax information', 'Department of Revenue', 'income tax',
            'sales tax return', 'taxpayer information', 'tax filing', 'tax confidentiality',
            'IC 6-8.1-7-1', 'financial institutions tax',
        ]),
        'counter_arguments': json.dumps([
            'Aggregate tax revenue statistics and anonymized data are public',
            'Final court judgments in tax collection cases are public',
            'Tax liens recorded in court records are public',
            'Information about the Department\'s own enforcement policies and operations is public',
            'Property tax assessment records (distinct from returns) are generally public in Indiana',
        ]),
        'notes': 'Indiana\'s tax return confidentiality under IC 6-8.1-7-1 is incorporated into APRA as a statutory confidentiality provision. Property tax assessment records are treated differently and are generally public. The exemption covers tax returns and derived information, not all Department of Revenue records.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(3)',
        'exemption_number': 'IC 5-14-3-4(b)(3)',
        'short_name': 'Personnel Files — Personal Information',
        'category': 'privacy',
        'description': 'Diaries, journals, and other personal notes of public agency employees are a discretionary exemption. Personal contact information, medical records, and similar sensitive personal data of public employees may also be withheld.',
        'scope': 'Personal diaries, notes, and journals of public employees — to the extent they are personal rather than work-related. Separate provisions protect personal contact information (home address, personal phone) and medical records of public employees. Employment information including name, compensation, department, job title, and employment status is a mandatory disclosure under IC 5-14-3-3(b)(6). Disciplinary records and performance evaluations are generally public. The exemption is narrow and does not protect work-related communications or official decision-making records merely because they were created by an employee.',
        'key_terms': json.dumps([
            'personnel file', 'public employee', 'personal notes', 'diary', 'journal',
            'home address', 'personal telephone', 'employee privacy', 'employment record',
            'salary', 'disciplinary record',
        ]),
        'counter_arguments': json.dumps([
            'Public employee name, job title, salary, department, and date of hire are MANDATORY disclosures under IC 5-14-3-3(b)(6)',
            'Disciplinary records and formal reprimands are generally public under Indiana law',
            'This is a DISCRETIONARY exemption — agencies may release even if technically exempt',
            'Work-related communications on government systems are generally public even if created by individual employees',
            'The Public Access Counselor has consistently held that employment performance data is public',
        ]),
        'notes': 'Indiana\'s APRA specifically requires disclosure of public employee compensation information under IC 5-14-3-3(b)(6). This is one of the few areas where Indiana\'s statute creates an explicit affirmative disclosure requirement. Personnel files as a whole are not exempt; only specific personal data categories within them are potentially protected as discretionary exemptions.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(4)',
        'exemption_number': 'IC 5-14-3-4(b)(4)',
        'short_name': 'Trade Secrets and Confidential Commercial Information',
        'category': 'commercial',
        'description': 'Trade secrets and confidential commercial or financial information submitted by private entities to government agencies are a discretionary exemption — agencies MAY withhold them but are not required to.',
        'scope': 'Proprietary commercial and financial information, trade secrets, and confidential business information submitted by private entities to government agencies. Covers information that: (1) derives economic value from not being generally known; (2) is subject to reasonable confidentiality measures; and (3) whose disclosure would cause competitive harm. Indiana\'s characterization as a discretionary exemption means agencies may release even technically exempt commercial information. Contract prices and amounts paid with public funds are generally not trade secrets and must be disclosed. Agencies cannot simply defer to vendor confidentiality designations.',
        'key_terms': json.dumps([
            'trade secret', 'confidential commercial information', 'proprietary information',
            'competitive harm', 'financial information', 'business confidential',
            'economic value', 'secrecy', 'regulatory submission',
        ]),
        'counter_arguments': json.dumps([
            'This is a DISCRETIONARY exemption under IC 5-14-3-4(b) — agencies may release',
            'Contract prices and amounts paid with public funds must be disclosed',
            'The submitter must demonstrate competitive harm — a confidentiality label is insufficient',
            'Publicly available information cannot be withheld as a trade secret',
            'Information required by law to be submitted has reduced secrecy expectations',
            'The Public Access Counselor has held that government contract amounts are always public',
        ]),
        'notes': 'Indiana\'s trade secret exemption is discretionary — a meaningful distinction from states where exemptions are mandatory. The Indiana Public Access Counselor has consistently issued opinions that agencies should release contract pricing information even where vendors claim trade secret protection. Government contract amounts paid with public funds are uniformly public under Indiana practice.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(19)',
        'exemption_number': 'IC 5-14-3-4(b)(19)',
        'short_name': 'Security Plans for Public Facilities',
        'category': 'safety',
        'description': 'Records containing specific information about the security of a public facility, infrastructure, or system, where disclosure would enable exploitation of a security vulnerability, are a discretionary exemption.',
        'scope': 'Specific vulnerability assessments, security plans, and related records for public facilities and critical infrastructure where disclosure would enable exploitation of specific security weaknesses. The exemption is narrow — it requires a specific, articulable nexus between disclosure and exploitation risk. Budget records, general security policies, and contracts with security vendors are generally public unless specific technical vulnerabilities are implicated. The agency must justify withholding each record based on specific rather than general security concerns.',
        'key_terms': json.dumps([
            'security plan', 'vulnerability assessment', 'public facility', 'security risk',
            'infrastructure', 'access control', 'cyber security', 'intrusion detection',
            'emergency response', 'security protocol',
        ]),
        'counter_arguments': json.dumps([
            'This is a DISCRETIONARY exemption — agencies may release',
            'The security risk must be specific and articulable for each withheld record',
            'Budget and expenditure records for security programs are public',
            'General security policies that do not reveal specific vulnerabilities are public',
            'Challenge claims that entire vendor contracts are exempt when only specific technical details warrant protection',
        ]),
        'notes': 'Indiana\'s security plans exemption under IC 5-14-3-4(b)(19) is both discretionary and narrow. Agencies must identify a specific, exploitable vulnerability that would be revealed by disclosure. General security concerns do not satisfy the exemption standard under Indiana law.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(a)(1)',
        'exemption_number': 'IC 5-14-3-4(a)(1)',
        'short_name': 'Records Declared Confidential by Federal Law',
        'category': 'statutory',
        'description': 'Records declared confidential by federal law are mandatory exemptions under APRA. This provision incorporates federal confidentiality statutes (e.g., HIPAA, FERPA, Privacy Act) into Indiana\'s public records framework.',
        'scope': 'Records whose disclosure is prohibited by federal law — examples include: individually identifiable health information under HIPAA, student education records under FERPA, tax return information under IRC § 6103, and personal information held in connection with federally funded programs under the Privacy Act. The exemption is limited to what federal law actually prohibits — not everything arguably related to a federally regulated program. Agencies must identify the specific federal statute requiring confidentiality for each withheld record.',
        'key_terms': json.dumps([
            'federal confidentiality', 'HIPAA', 'FERPA', 'Privacy Act', 'federal law',
            'IRC 6103', 'federal statute', 'federally required confidentiality',
            'protected health information', 'education records',
        ]),
        'counter_arguments': json.dumps([
            'The agency must identify the specific federal statute prohibiting disclosure, not make a general "federal law" claim',
            'Not all records held in connection with a federally funded program are confidential — only those specifically protected by a named federal statute',
            'Aggregate and anonymized data derived from individually protected records may be public',
            'Challenge whether the specific record falls within the federal statute\'s scope',
            'Federal confidentiality statutes are often more specific than agencies claim — scrutinize whether the exemption actually applies',
        ]),
        'notes': 'IC 5-14-3-4(a)(1) is Indiana\'s mechanism for incorporating federal confidentiality requirements. It is a mandatory exemption — agencies must withhold records when a federal statute prohibits disclosure. However, the specific federal statute must be identified. Generic invocations of "federal law" without citing the specific provision are insufficient.',
    },
    {
        'jurisdiction': 'IN',
        'statute_citation': 'IC 5-14-3-4(b)(6)',
        'exemption_number': 'IC 5-14-3-4(b)(6)',
        'short_name': 'Ongoing Negotiations',
        'category': 'deliberative',
        'description': 'Records relating to negotiations with private persons or entities, including labor negotiations, real property acquisition negotiations, and commercial negotiations, are a discretionary exemption until the negotiations conclude.',
        'scope': 'Records reflecting the agency\'s negotiating position, internal strategy, and communications regarding active negotiations with private parties — including collective bargaining negotiations, real property acquisition, and commercial contracts. The exemption is time-limited: it applies only while negotiations are genuinely ongoing. Once negotiations conclude (either by agreement or failure), the records become subject to full disclosure. Contract prices, terms of completed agreements, and final contract documents are public. The agency must demonstrate that negotiations are genuinely active and not merely described as ongoing to avoid disclosure.',
        'key_terms': json.dumps([
            'negotiation', 'collective bargaining', 'real property acquisition',
            'negotiating position', 'commercial negotiation', 'labor negotiation',
            'ongoing negotiation', 'pending negotiation', 'contract negotiation',
        ]),
        'counter_arguments': json.dumps([
            'This is a DISCRETIONARY exemption — agencies may release',
            'Once negotiations conclude, records become fully public',
            'Final contract terms and prices are public regardless of this exemption',
            'Challenge whether negotiations are genuinely ongoing vs. nominally described as such',
            'Records about completed negotiations for already-executed contracts are not covered',
        ]),
        'notes': 'Indiana\'s ongoing negotiations exemption under IC 5-14-3-4(b)(6) is a time-limited discretionary exemption. The Indiana Public Access Counselor has consistently held that it expires upon conclusion of negotiations. Final contract terms are always public. This exemption is frequently misapplied to shield completed transaction documents.',
    },
]

# =============================================================================
# RULES
# Indiana Access to Public Records Act, IC 5-14-3
# Indiana has a tiered response system: 24 hours for informal requests and
# 7 calendar days for formal written requests. The Public Access Counselor
# provides advisory opinions that are persuasive but not binding.
# Attorney's fees are available. Copy fee $0.10/page.
# =============================================================================

IN_RULES = [
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'informal_request_response_hours',
        'param_value': '24',
        'day_type': 'hours',
        'statute_citation': 'IC 5-14-3-9(a)',
        'notes': 'Indiana agencies must respond to informal public records requests within 24 hours of receipt. An "informal request" is typically an oral request made in person or by phone. The 24-hour response clock is one of the most demanding in US public records law. However, the 24-hour deadline can be extended for good cause. If the agency cannot produce the records within 24 hours, it must at minimum acknowledge receipt and provide a timeline for production. The 24-hour clock does not apply to formal written requests.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'formal_request_response_days',
        'param_value': '7',
        'day_type': 'calendar',
        'statute_citation': 'IC 5-14-3-9(a)',
        'notes': 'Indiana agencies must respond to formal written public records requests within 7 calendar days. If the agency needs more time, it must notify the requester within the 7-day period and provide a specific timeline. The 7-day clock begins on receipt of the written request. Indiana\'s 7-day formal response period is shorter than most states. Failure to respond within 7 days is itself an APRA violation actionable through the Public Access Counselor or the courts.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'extension_with_notice',
        'param_value': 'allowed_with_specific_timeline',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-9(c)',
        'notes': 'Indiana agencies may extend the 7-day response period, but only if they notify the requester within the initial 7-day period and provide a specific, reasonable timeline for production. A blanket extension without a specific date is not sufficient. The extension must be justified and reasonable — agencies may not use extension provisions to indefinitely delay responses. The Indiana Public Access Counselor has issued numerous opinions that unreasonable extensions violate APRA.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'fee_cap',
        'param_key': 'default_copy_rate_per_page',
        'param_value': '0.10',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-8(c)',
        'notes': 'Indiana agencies may charge up to $0.10 per page for paper copies of public records. This is one of the lowest standard copy rates in the United States. Agencies may not charge more than the actual cost of reproduction, which is capped at $0.10 per page for standard paper copies. For electronic records, the actual cost is typically minimal. Agencies cannot charge for staff time spent locating or reviewing records — only the reproduction cost is permissible.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'fee_cap',
        'param_key': 'staff_time_not_chargeable',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-8',
        'notes': 'Indiana agencies may not charge requesters for staff time spent locating, reviewing, or preparing records for disclosure. Only the actual cost of reproduction is chargeable. The $0.10/page cap applies to the reproduction cost, not a per-record search fee. Requesters should challenge any invoice that includes search fees, review fees, or labor charges beyond the per-page reproduction cost.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'fee_waiver',
        'param_key': 'fee_waiver_for_public_interest',
        'param_value': 'agency_discretion',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-8',
        'notes': 'Indiana does not provide a statutory right to fee waiver, but agencies may waive fees at their discretion. Given the $0.10/page rate, fees are rarely a significant barrier. For electronic records delivered by email, the actual cost is often zero. Requesters may argue for fee waivers based on public interest, news media status, or nonprofit purpose, but these arguments rest on agency discretion.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'appeal_deadline',
        'param_key': 'public_access_counselor',
        'param_value': 'advisory_only',
        'day_type': None,
        'statute_citation': 'IC 5-14-5-2',
        'notes': 'Indiana\'s Public Access Counselor (PAC) reviews complaints about APRA violations and issues advisory opinions. PAC opinions are not legally binding on agencies, but they carry persuasive authority in subsequent court proceedings. Filing a PAC complaint is free and relatively fast — the PAC typically issues an opinion within 30 days. Many requesters use the PAC process as a first step before litigation. A favorable PAC opinion significantly strengthens a requester\'s legal position and often prompts agencies to comply voluntarily.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'judicial_review_deadline',
        'param_key': 'circuit_or_superior_court_enforcement',
        'param_value': 'available',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-9(f)',
        'notes': 'A requester denied access or facing unreasonable delay may file a lawsuit in circuit or superior court. The court reviews the denial de novo and may order the agency to produce records. Courts may award attorney\'s fees and litigation costs to prevailing requesters. There is no requirement to exhaust the PAC process before filing suit, though PAC opinions are often useful evidence. Indiana courts have enforced APRA through injunctive relief orders compelling disclosure.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'penalty',
        'param_key': 'attorneys_fees_available',
        'param_value': 'available_for_prevailing_requester',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-9(i)',
        'notes': 'A requester who substantially prevails in an APRA lawsuit may recover reasonable attorney\'s fees and court costs. The fee award is not mandatory (unlike some states) but is routinely granted to prevailing requesters. The availability of attorney\'s fees makes litigation economically viable even for modest-value requests. The catalyst theory applies in Indiana — fees may be available where the agency releases records after suit is filed, even without a formal court judgment.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'discretionary_vs_mandatory_exemptions',
        'param_value': 'two-tier_system',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-4(a); IC 5-14-3-4(b)',
        'notes': 'Indiana\'s APRA uniquely distinguishes between mandatory exemptions (IC 5-14-3-4(a)) — where agencies must withhold — and discretionary exemptions (IC 5-14-3-4(b)) — where agencies may withhold but are not required to. Most investigatory, deliberative process, and commercial records fall into the discretionary category, meaning agencies can choose to release them. This two-tier system creates an important advocacy hook: requesters can argue the agency should exercise its discretion to release even technically exempt records.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'segregability_required',
        'param_value': 'yes',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-9(d)',
        'notes': 'Indiana agencies must release all non-exempt portions of records when only part of a record qualifies for an exemption. Blanket withholding of documents containing some exempt content is an APRA violation. Agencies must segregate exempt portions and release the remainder. Indiana courts and the Public Access Counselor have consistently enforced the segregability requirement.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'mandatory_disclosure_categories',
        'param_value': 'IC_5-14-3-3_listed_records',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-3',
        'notes': 'IC 5-14-3-3 creates a category of records that MUST be disclosed — agencies have no discretion to withhold them. These include: (1) arrest records; (2) adoption decrees once finalized; (3) public employee compensation; (4) voting records; (5) public agency budgets and financial records; (6) court records in custody of agencies; (7) most regulatory license and permit records. Requesters should cite IC 5-14-3-3 specifically when seeking records in the mandatory disclosure categories — it removes agency discretion entirely.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'identity_not_required',
        'param_value': 'true',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-3(a)',
        'notes': 'Indiana agencies may not require requesters to state their purpose for requesting records or to identify themselves as a condition of access. The APRA right of access does not depend on the requester\'s identity or reason for the request. Agencies cannot condition access on identity verification. However, providing contact information facilitates delivery of records, and agencies may request (but not require) contact details.',
    },
    {
        'jurisdiction': 'IN',
        'rule_type': 'initial_response',
        'param_key': 'electronic_records_format',
        'param_value': 'format_maintained_or_reasonable_alternative',
        'day_type': None,
        'statute_citation': 'IC 5-14-3-3(c)',
        'notes': 'Indiana agencies must provide electronic records in the format in which they are maintained if the requester requests that format, unless the agency demonstrates it is unable to do so. If the agency cannot provide records in the requested electronic format, it must provide a reasonable alternative. Agencies cannot charge to convert electronic records from their maintained format to a deliverable format when doing so involves minimal effort. The Public Access Counselor has held that agencies must provide workable electronic formats, not PDFs of printouts of digital files when the original digital format is more useful.',
    },
]

# =============================================================================
# TEMPLATES
# =============================================================================

IN_TEMPLATES = [
    {
        'jurisdiction': 'IN',
        'record_type': 'general',
        'template_name': 'General Indiana APRA Request',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}
{{requester_phone}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: Public Records Request — Indiana Access to Public Records Act, IC 5-14-3

Dear Public Records Officer:

Pursuant to Indiana's Access to Public Records Act (APRA), IC 5-14-3 et seq., I hereby request access to and copies of the following public records:

{{description_of_records}}

Time period covered: {{date_range_start}} through {{date_range_end}}.

To assist in locating the requested records:
{{additional_context}}

I request that records be provided in electronic format (email or downloadable file) where available. Under IC 5-14-3-3(c), electronic records must be provided in the format in which they are maintained, which minimizes both cost and production time.

I am willing to pay the actual cost of reproduction, not to exceed the $0.10/page statutory maximum per IC 5-14-3-8(c). I am not willing to pay charges for staff time spent locating, reviewing, or redacting records, which is not a permissible fee under Indiana law. If fees will exceed ${{fee_limit}}, please notify me before proceeding.

Under APRA, public records are presumptively subject to disclosure. If records fall within the mandatory disclosure categories of IC 5-14-3-3, those records must be disclosed without exception. For any records withheld, please note that many exemptions under IC 5-14-3-4(b) are discretionary — I ask that you exercise any discretion in favor of disclosure given the public interest in this information.

If any records or portions of records are withheld, I request that you: (1) identify each record withheld; (2) state the specific APRA citation (IC 5-14-3-4(a) or (b) subsection); (3) state whether the exemption is mandatory or discretionary; and (4) confirm that all non-exempt, segregable portions have been released.

Under IC 5-14-3-9(a), please respond within 7 calendar days of receipt of this written request.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I respectfully request that copying fees be waived for this request. While Indiana law does not provide a statutory fee waiver right, I ask that {{agency_name}} exercise its discretion to waive fees because:

1. These records relate to {{public_interest_explanation}}, a matter of significant public interest.

2. I am {{requester_category_description}}. Disclosure will benefit the public by {{public_benefit_explanation}}.

3. If records are delivered electronically, the actual cost of reproduction is zero.

Given Indiana's strong public records policy, a fee waiver for this request is appropriate.''',
        'expedited_language': '''I request expedited processing of this APRA request. Under IC 5-14-3-9(a), informal requests must be addressed within 24 hours. Even for formal written requests, I ask for the most prompt production possible because:

{{expedited_justification}}

I need these records by {{needed_by_date}}. Delay beyond that date will {{harm_from_delay}}.''',
        'notes': 'General-purpose Indiana APRA template. Key Indiana features: (1) 24 hours for informal requests, 7 calendar days for formal written requests (IC 5-14-3-9(a)); (2) TWO-TIER exemption system — IC 5-14-3-4(a) mandatory, IC 5-14-3-4(b) discretionary; (3) IC 5-14-3-3 mandatory disclosure categories including arrest records and employee compensation; (4) Public Access Counselor (PAC) advisory opinions available pre-litigation; (5) attorney\'s fees for prevailing requesters; (6) $0.10/page standard copy fee — lowest common standard rate in US; (7) electronic records in format maintained. Reference "APRA" or "IC 5-14-3," not "FOIA."',
    },
    {
        'jurisdiction': 'IN',
        'record_type': 'law_enforcement',
        'template_name': 'Indiana APRA Request — Law Enforcement Records',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: APRA Request — Law Enforcement Records, IC 5-14-3

Dear Public Records Officer:

Pursuant to Indiana's Access to Public Records Act, IC 5-14-3 et seq., I request copies of the following law enforcement records:

{{description_of_records}}

Relating to: {{subject_or_incident}}
Date range: {{date_range_start}} through {{date_range_end}}
Location (if applicable): {{location}}

This request includes, but is not limited to:
- Incident reports and offense reports
- Arrest records and booking records [MANDATORY DISCLOSURE under IC 5-14-3-3(b)(1)]
- Use-of-force reports
- Officer disciplinary and complaint records for involved personnel
- Body-worn camera footage and metadata
- Dispatch records and CAD logs
- Written communications related to the above

Regarding claimed exemptions: Arrest records are a MANDATORY disclosure under IC 5-14-3-3(b)(1) — they may not be withheld. Investigatory records under IC 5-14-3-4(b)(1) are DISCRETIONARY — the agency may release them, and I ask that you do so. Any withholding of investigatory records requires identification of a specific enumerated harm (reveals informant; endangers life; impedes ongoing investigation; interferes with pending prosecution) for each specific record withheld.

[If matter appears concluded:] If prosecution has concluded or no prosecution is pending, the "ongoing investigation" and "pending prosecution" rationales are no longer available, and records should be released.

Under IC 5-14-3-9(a), please respond within 7 calendar days. I am willing to pay reproduction costs up to ${{fee_limit}} at the statutory $0.10/page rate.

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that copying fees be waived. These records concern {{public_interest_explanation}}, a core public accountability matter. Electronic delivery incurs zero reproduction cost. Indiana\'s APRA reflects a strong policy of open government.''',
        'expedited_language': '''I request expedited processing under IC 5-14-3-9(a). Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Indiana law enforcement records template. Key Indiana features: (1) arrest records are MANDATORY disclosures under IC 5-14-3-3(b)(1) — cannot be withheld; (2) investigatory records are DISCRETIONARY under IC 5-14-3-4(b)(1) — agencies may release; (3) 7-day response deadline for written requests; (4) Public Access Counselor (PAC) advisory opinions available; (5) attorney\'s fees available; (6) IC 5-14-3-4(b)(1) harm-based standard requires specific articulation of harm for each withheld record.',
    },
    {
        'jurisdiction': 'IN',
        'record_type': 'government_contracts',
        'template_name': 'Indiana APRA Request — Government Contracts and Spending',
        'template_text': '''{{requester_name}}
{{requester_address}}
{{requester_email}}

{{date}}

Public Records Officer
{{agency_name}}
{{agency_address}}

Re: APRA Request — Government Contracts and Expenditures, IC 5-14-3

Dear Public Records Officer:

Pursuant to Indiana's Access to Public Records Act, IC 5-14-3 et seq., I request access to the following government contracts and expenditure records:

{{description_of_records}}

Specifically, I request:
- All contracts, agreements, amendments, and change orders between {{agency_name}} and {{vendor_or_contractor_name}} from {{date_range_start}} through {{date_range_end}}
- Solicitation documents (RFPs, IFBs, RFQs) and all responsive bids or proposals
- Bid tabulation sheets and scoring documents
- Invoices, payment records, and expenditure documentation
- Correspondence related to the contract and its performance

Public agency financial records and expenditure data are subject to mandatory disclosure under IC 5-14-3-3. Contract prices and amounts paid with public funds must be disclosed regardless of any trade secret claim. If trade secret claims are made under IC 5-14-3-4(b)(4), that is a DISCRETIONARY exemption — I ask that the agency exercise its discretion to release, as the public interest in accountability for government expenditures outweighs any claimed commercial confidentiality.

I am willing to pay the actual reproduction cost at the $0.10/page statutory rate, up to ${{fee_limit}}.

Please respond within 7 calendar days per IC 5-14-3-9(a).

Sincerely,
{{requester_name}}''',
        'fee_waiver_language': '''I request that fees be waived. These records concern the expenditure of public funds, a core accountability matter. Electronic delivery incurs zero cost. Indiana\'s APRA reflects a strong policy of financial transparency in government.''',
        'expedited_language': '''I request expedited processing under IC 5-14-3-9(a). Prompt production is needed because: {{expedited_justification}}. I need these records by {{needed_by_date}}.''',
        'notes': 'Indiana government contracts template. Key Indiana features: (1) financial records are mandatory disclosures under IC 5-14-3-3; (2) trade secret exemptions for contracts are DISCRETIONARY under IC 5-14-3-4(b)(4) — agencies may release; (3) contract prices and public expenditures always public; (4) Public Access Counselor has consistently held that government contract amounts cannot be withheld as trade secrets; (5) 7-day formal response deadline; (6) $0.10/page copy rate.',
    },
]


# =============================================================================
# MAIN
# =============================================================================

def build_exemptions(conn):
    added = 0
    skipped = 0
    errors = 0

    for exemption in IN_EXEMPTIONS:
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

    print(f'IN exemptions: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_rules(conn):
    added = 0
    skipped = 0
    errors = 0

    for rule in IN_RULES:
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

    print(f'IN rules: {added} added, {skipped} updated, {errors} errors')
    return added, skipped, errors


def build_templates(conn):
    added = 0
    skipped = 0
    errors = 0

    for template in IN_TEMPLATES:
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

    print(f'IN templates: {added} added, {skipped} updated, {errors} errors')
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
    print(f'IN total: {total_added} added, {total_skipped} updated, {total_errors} errors ({elapsed:.1f}s)')
    write_receipt(script='build_in', added=total_added, skipped=total_skipped, errors=total_errors, elapsed_s=elapsed)


if __name__ == '__main__':
    main()
